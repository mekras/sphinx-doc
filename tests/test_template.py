"""Проверка сборки свежей копии шаблона. Требуются Docker и GNU Make."""

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


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

    def test_clean_creates_directory_and_preserves_service_files(self):
        self.make("clean")
        output = self.project / "htdocs"
        for name in (".gitignore", "robots.txt", "obsolete.html"):
            (output / name).write_text(name)
        self.make("clean")
        self.assertEqual({p.name for p in output.iterdir()}, {".gitignore", "robots.txt"})


if __name__ == "__main__":
    unittest.main()
