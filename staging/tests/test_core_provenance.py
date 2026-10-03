import copy
import importlib.util
from pathlib import Path
import unittest

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


if __name__ == "__main__":
    unittest.main()
