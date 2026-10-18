"""Проверка выбора имени образа без запуска Docker. Требуются Git и GNU Make."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


MAKEFILE = Path(__file__).resolve().parents[1] / "Makefile"


class ImageNameTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory(prefix="sphinx-image-name-")
        self.addCleanup(workspace.cleanup)
        self.project = Path(workspace.name)
        self.env = os.environ.copy()
        for name in ("IMAGE_NAME", "MAKEFLAGS", "MFLAGS", "MAKEOVERRIDES"):
            self.env.pop(name, None)
        shutil.copyfile(MAKEFILE, self.project / "Makefile")
        self.run_command("git", "init", "--quiet")
        self.run_command("git", "add", "Makefile")
        self.run_command("git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
                         "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Initial")

    def run_command(self, *command, env=None):
        result = subprocess.run(
            command, cwd=self.project, env=self.env if env is None else env,
            text=True, capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def assert_image(self, expected, *arguments, env=None):
        output = self.run_command("make", "--no-print-directory", "-n", "build",
                                  *arguments, env=env)
        self.assertEqual(output.strip(), f"docker build -t {expected} .")

    def test_default_is_independent_of_origin(self):
        for origin in (None, "https://github.com/mekras/sphinx-doc.git",
                       "git@github.com:mekras/sphinx-doc.git"):
            if origin:
                self.run_command("git", "config", "remote.origin.url", origin)
            with self.subTest(origin=origin):
                self.assert_image("mekras/sphinx-doc:latest")

    def test_exact_tag_is_preserved(self):
        self.run_command("git", "remote", "add", "origin",
                         "git@github.com:mekras/sphinx-doc.git")
        self.run_command("git", "tag", "8.2.3")
        self.assert_image("mekras/sphinx-doc:8.2.3")

    def test_overrides(self):
        env = self.env | {"IMAGE_NAME": "registry.example/docs:environment"}
        self.assert_image("registry.example/docs:environment", env=env)
        self.assert_image("registry.example/docs:argument",
                          "IMAGE_NAME=registry.example/docs:argument", env=env)


if __name__ == "__main__":
    unittest.main()
