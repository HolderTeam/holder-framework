import copy
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "core_provenance", Path(__file__).parents[1] / "scripts/linux-appimage/core-provenance.py")
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.sha = "a" * 40
        self.core = dict(commit=self.sha, version="0.2.0", platform="linux",
                         architecture="x86_64", build_type="RelWithDebInfo", compiler="GNU 13")
        self.selection = dict(repository="HolderTeam/holder-core", commit=self.sha,
                              version="0.2.0", release_tag="sdk-" + self.sha,
                              assets=[dict(platform="linux", architecture="x86_64",
                                           build_type="RelWithDebInfo", sha256="b" * 64,
                                           name="linux-sdk.tar.gz")])
        self.pin = dict(core=dict(commit=self.sha, build_type="RelWithDebInfo"),
                        desktop=dict(commit="c" * 40), backend=dict(commit="d" * 40))

    def verify(self, pin=None):
        return tool.verify(self.selection, self.core, "c" * 40, "d" * 40, pin)

    def test_matching_sdk_records_published_asset_checksum(self):
        result = self.verify()
        self.assertEqual(result["sdk_asset"]["sha256"], "b" * 64)
        self.assertEqual(result["release_tag"], "sdk-" + self.sha)

    def test_stale_backend_cannot_pass_latest_green_selection(self):
        self.core["commit"] = "e" * 40
        with self.assertRaisesRegex(ValueError, "revision differs"):
            self.verify()

    def test_wrong_platform_is_rejected(self):
        self.core["platform"] = "windows"
        with self.assertRaisesRegex(ValueError, "Linux x86_64"):
            self.verify()

    def test_unpublished_configuration_is_rejected(self):
        self.core["build_type"] = "Debug"
        with self.assertRaisesRegex(ValueError, "configuration is absent"):
            self.verify()

    def test_release_pin_checks_every_component_and_core_configuration(self):
        self.verify(self.pin)
        for component, field, value in (("desktop", "commit", "e" * 40),
                                        ("backend", "commit", "e" * 40),
                                        ("core", "commit", "e" * 40),
                                        ("core", "build_type", "Release")):
            pin = copy.deepcopy(self.pin)
            pin[component][field] = value
            with self.subTest(component=component, field=field), self.assertRaises(ValueError):
                self.verify(pin)

    def test_release_manifest_controls_selection_and_rejects_conflicting_overrides(self):
        pin = {**self.pin, "appimage_version": "0.2.1-rc.1"}
        for name in ("desktop", "backend"):
            pin[name] = {**pin[name], "repository": "HolderTeam/holder-" + name, "run_id": "123"}
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "release.json"
            output = Path(directory) / "outputs"
            manifest.write_text(json.dumps(pin))
            env = {"GITHUB_OUTPUT": str(output), "CORE_REF_INPUT": "latest-green",
                   "DESKTOP_REPOSITORY_INPUT": "HolderTeam/holder-desktop",
                   "BACKEND_REPOSITORY_INPUT": "HolderTeam/holder-core"}
            args = ["core-provenance.py", "prepare", "--release-manifest", str(manifest)]
            with patch.dict(os.environ, env, clear=True), patch.object(sys, "argv", args):
                tool.main()
                values = dict(line.split("=", 1) for line in output.read_text().splitlines())
                self.assertEqual(values["core_ref"], self.sha)
                self.assertEqual(values["appimage_version"], "0.2.1-rc.1")
                self.assertEqual(values["backend_run_id"], "123")
                self.assertEqual(values["backend_repository"], "HolderTeam/holder-backend")
                os.environ["BACKEND_RUN_ID_INPUT"] = "456"
                with self.assertRaisesRegex(ValueError, "manifest alone"):
                    tool.main()

    def test_release_manifest_rejects_moving_core_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "release.json"
            manifest.write_text(json.dumps({"core": {"commit": "latest-green"}}))
            with self.assertRaisesRegex(ValueError, "full lowercase commit"):
                tool.load_pin(manifest)


if __name__ == "__main__":
    unittest.main()
