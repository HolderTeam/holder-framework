import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "component_runs", Path(__file__).parents[1] / "scripts/resolve-component-runs.py")
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class RunSelectionTests(unittest.TestCase):
    def request(self, path, **query):
        if path.endswith("/runs"):
            return {"workflow_runs": [self.make_run(2), self.make_run(1)]}
        if path.endswith("/artifacts"):
            return {"artifacts": [{"name": "backend", "expired": "/2/" in path}]}
        return self.make_run(2)

    @staticmethod
    def make_run(identifier):
        return dict(id=identifier, status="completed", conclusion="success", head_sha="a" * 40)

    def test_auto_selection_skips_expired_artifacts(self):
        result = tool.resolve("owner/repo", "ci.yml", "main", "backend", request=self.request)
        self.assertEqual(result, ("1", "a" * 40))

    def test_explicit_run_must_have_unexpired_artifact(self):
        with self.assertRaises(ValueError):
            tool.resolve("owner/repo", "ci.yml", "main", "backend", "2", self.request)

    def test_explicit_failed_run_is_rejected(self):
        def request(path, **query):
            return {**self.make_run(1), "conclusion": "failure"}
        with self.assertRaises(ValueError):
            tool.resolve("owner/repo", "ci.yml", "main", "backend", "1", request)
