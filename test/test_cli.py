"""The bundled CLI: flags, argument rules, hostile input."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
CLI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cli")
sys.path.insert(0, CLI)
from omarchy_pets import api, cli, package


class CliTests(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.home.cleanup()

    def run_cli(self, *args):
        env = {"HOME": self.home.name, "PATH": os.environ.get("PATH", "/usr/bin:/bin"), "PYTHONPATH": CLI, "OMARCHY_PETS_API_BASE": "http://127.0.0.1:9"}
        return subprocess.run([sys.executable, "-B", "-m", "omarchy_pets", *args], env=env, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=30)

    def test_json_flag_works_after_the_verb(self):
        for argv in (["list", "--dir", self.home.name, "--json"], ["--json", "list", "--dir", self.home.name]):
            done = self.run_cli(*argv)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertEqual(json.loads(done.stdout), {"ok": True, "pets": [], "skipped": [], "message": "No pets installed."})

    def test_without_json_prose_is_printed(self):
        done = self.run_cli("list", "--dir", self.home.name)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout, "No pets installed.\n")

    def test_id_and_collection_together_are_refused_before_any_request(self):
        done = self.run_cli("install", "guga", "--collection", "starter", "--dir", self.home.name, "--json")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(json.loads(done.stdout)["error"], "give a pet id or --collection, not both")

    def test_deeply_nested_manifest_is_a_package_error(self):
        with self.assertRaisesRegex(package.PackageError, "not valid JSON"):
            package.parse_manifest(b"[" * 60000)

    def test_deeply_nested_server_answer_is_a_server_error(self):
        with self.assertRaises(api.ServerError):
            api._decode(200, b"[" * 100000)

    def test_owner_handle_is_url_encoded(self):
        paths = []

        def fake(method, path, payload=None, token=None):
            paths.append(path)
            return {"user": {"handle": "a b&c"}} if path == "/api/me" else {"pets": [], "totalPages": 1}

        with mock.patch.object(api, "api_json", fake):
            self.assertEqual(cli.remote_pets("token"), [])
        self.assertEqual(paths[1], "/api/pets?owner=a%20b%26c&pageSize=60&page=1")


if __name__ == "__main__":
    unittest.main()
