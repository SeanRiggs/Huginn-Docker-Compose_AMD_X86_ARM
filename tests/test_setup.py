import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in (".env.example", "docker-compose.yaml"):
            shutil.copyfile(ROOT / name, self.root / name)

    def run_setup(self):
        return subprocess.run([os.sys.executable, str(ROOT / "scripts/setup.py")],
                              cwd=self.root, capture_output=True, text=True)

    def test_generates_unique_secrets_without_disclosing_them(self):
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        values = dict(line.split("=", 1) for line in (self.root / ".env").read_text().splitlines()
                      if line and not line.startswith("#"))
        keys = ("MYSQL_ROOT_PASSWORD", "MYSQL_PASSWORD", "APP_SECRET_TOKEN", "SEED_PASSWORD", "INVITATION_CODE")
        self.assertEqual(len({values[k] for k in keys}), len(keys))
        for key in keys:
            self.assertGreaterEqual(len(values[key]), 48)
            self.assertNotIn(values[key], result.stdout + result.stderr)
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE((self.root / ".env").stat().st_mode), 0o600)

    def test_existing_env_is_never_overwritten(self):
        (self.root / ".env").write_text("preserve me\n")
        self.assertNotEqual(self.run_setup().returncode, 0)
        self.assertEqual((self.root / ".env").read_text(), "preserve me\n")

    def test_legacy_install_requires_migration(self):
        for directory in ("data", "database", "huginn"):
            with self.subTest(directory=directory):
                (self.root / directory).mkdir()
                self.assertNotEqual(self.run_setup().returncode, 0)
                self.assertFalse((self.root / ".env").exists())
                (self.root / directory).rmdir()

    def test_env_symlink_is_not_followed(self):
        target = self.root / "private"
        target.write_text("unchanged")
        (self.root / ".env").symlink_to(target)
        self.assertNotEqual(self.run_setup().returncode, 0)
        self.assertEqual(target.read_text(), "unchanged")


if __name__ == "__main__":
    unittest.main()
