"""Проверка сборки свежей копии шаблона. Требуются Docker и GNU Make."""

from pathlib import Path
import os
import shlex
import shutil
import struct
import subprocess
import tempfile
import time
import unittest
from urllib.request import urlopen
import uuid
import zlib


TEMPLATE = Path(__file__).resolve().parents[1] / "project-template"


class TemplateBuildTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="sphinx-template-")
        self.addCleanup(self.workspace.cleanup)
        self.project = Path(self.workspace.name) / "my-docs"
        shutil.copytree(TEMPLATE, self.project, ignore=shutil.ignore_patterns("htdocs"))

    def make(self, *arguments):
        command = ["make", *arguments]
        if image := os.environ.get("SPHINX_TEST_IMAGE"):
            command.append(f"SPHINX_DOCKER_IMAGE={image}")
        result = subprocess.run(
            command, cwd=self.project, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        return result.stdout

    def assert_html(self):
        html = self.project / "htdocs/index.html"
        self.assertIn("Начальная страница", html.read_text())

    def assert_pdf(self):
        pdf = self.project / "htdocs/document.pdf"
        self.assertTrue(pdf.read_bytes().startswith(b"%PDF-"))

    def test_all_from_fresh_copy(self):
        self.make("all")
        self.assert_html()
        self.assert_pdf()

    def test_html_from_fresh_copy(self):
        self.make("html")
        self.assert_html()

    def test_parallel_all_and_rebuild_preserve_both_formats(self):
        self.make("-j2", "all")
        self.assert_html()
        self.assert_pdf()
        obsolete = self.project / "htdocs/obsolete.html"
        obsolete.write_text("obsolete")
        self.make("-j2", "all")
        self.assert_html()
        self.assert_pdf()
        self.assertFalse(obsolete.exists())

    def test_html_preserves_existing_pdf(self):
        self.make("pdf")
        pdf = self.project / "htdocs/document.pdf"
        before = pdf.read_bytes()
        self.make("html")
        self.assert_html()
        self.assertEqual(pdf.read_bytes(), before)

    def test_pdf_from_fresh_copy(self):
        self.make("pdf")
        self.assert_pdf()

    def test_figures_in_builds_and_preview(self):
        def png(red):
            def chunk(kind, data):
                return (struct.pack(">I", len(data)) + kind + data
                        + struct.pack(">I", zlib.crc32(kind + data)))
            return (b"\x89PNG\r\n\x1a\n"
                    + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
                    + chunk(b"IDAT", zlib.compress(bytes([0, red, 0, 0])))
                    + chunk(b"IEND", b""))

        figure = self.project / "src/figures/preview-check.png"
        figure.write_bytes(png(255))
        with (self.project / "src/pages/index.rst").open("a") as page:
            page.write("\n.. image:: ../figures/preview-check.png\n")
        self.assertNotIn("image file not readable", self.make("html"))
        self.assertEqual(
            (self.project / "htdocs/_images/preview-check.png").read_bytes(),
            figure.read_bytes(),
        )
        self.assertNotIn("image file not readable", self.make("pdf"))
        self.assert_pdf()

        preview_command = ["make", "--no-print-directory", "-n", "start-server"]
        if image := os.environ.get("SPHINX_TEST_IMAGE"):
            preview_command.append(f"SPHINX_DOCKER_IMAGE={image}")
        recipe = subprocess.check_output(
            preview_command,
            cwd=self.project, text=True,
        )
        command = shlex.split(recipe.replace("\\\n", " "))
        # Для автоматического запуска нужны свободный порт и отключённый TTY.
        command.remove("--tty")
        command[command.index("--publish") + 1] = "127.0.0.1::8000"
        name = f"sphinx-preview-test-{uuid.uuid4().hex}"
        command[2:2] = ["--name", name]
        with tempfile.TemporaryFile(mode="w+") as log:
            server = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
            try:
                deadline = time.monotonic() + 60
                url = None
                while time.monotonic() < deadline:
                    self.assertIsNone(server.poll(), "Сервер завершился до проверки")
                    port = subprocess.run(
                        ["docker", "port", name, "8000/tcp"],
                        text=True, capture_output=True,
                    )
                    if port.returncode == 0 and port.stdout.strip():
                        url = "http://" + port.stdout.strip()
                        break
                    time.sleep(0.2)
                self.assertIsNotNone(url, "Docker не опубликовал порт")

                def wait_for(path, expected):
                    deadline = time.monotonic() + 60
                    while time.monotonic() < deadline:
                        self.assertIsNone(server.poll(), "Сервер завершился до проверки")
                        try:
                            with urlopen(url + path, timeout=2) as response:
                                if expected in response.read():
                                    return
                        except OSError:
                            pass
                        time.sleep(0.2)
                    log.seek(0)
                    self.fail(f"Не получен ожидаемый ответ {path}\n{log.read()}")

                wait_for("/", b"_images/preview-check.png")
                wait_for("/_images/preview-check.png", figure.read_bytes())
                # Дать наблюдателю завершить запуск после начальной сборки.
                time.sleep(1)
                figure.write_bytes(png(128))
                wait_for("/_images/preview-check.png", figure.read_bytes())
                log.seek(0)
                self.assertNotIn("image file not readable", log.read())
            finally:
                subprocess.run(["docker", "rm", "-f", name], capture_output=True)
                server.wait(timeout=15)

    def test_clean_creates_directory_and_preserves_service_files(self):
        self.make("clean")
        output = self.project / "htdocs"
        for name in (".gitignore", "robots.txt", "obsolete.html"):
            (output / name).write_text(name)
        self.make("clean")
        self.assertEqual({p.name for p in output.iterdir()}, {".gitignore", "robots.txt"})


if __name__ == "__main__":
    unittest.main()
