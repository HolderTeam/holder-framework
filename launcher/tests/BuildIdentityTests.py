"""Verify identity refresh without committing or changing the developer repository."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

CMAKE, GIT = sys.argv[1:3]
del sys.argv[1:3]
SOURCE = Path(__file__).resolve().parents[1]


class BuildIdentityTests(unittest.TestCase):
    def test_clean_dirty_new_commit_and_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo, output = root / "repo", root / "build"
            (repo / "cmake").mkdir(parents=True)
            for name in ("BuildIdentity.h.in", "source.json.in"):
                shutil.copy2(SOURCE / "cmake" / name, repo / "cmake" / name)

            def git(*args):
                return subprocess.check_output([GIT, "-C", str(repo), *args], text=True, stderr=subprocess.STDOUT).strip()

            def capture(git_executable=GIT):
                subprocess.run([CMAKE, f"-DSOURCE_DIR={repo}", f"-DOUTPUT_DIR={output}",
                                f"-DGIT_EXECUTABLE={git_executable}", "-P",
                                str(SOURCE / "cmake" / "WriteBuildIdentity.cmake")], check=True)
                return json.loads((output / "source.json").read_text())

            git("init")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "fixture")
            initial = git("rev-parse", "HEAD")
            self.assertEqual(capture(), {"commit": initial, "dirty": False})
            header = output / "BuildIdentity.h"
            timestamp = header.stat().st_mtime_ns
            capture()
            self.assertEqual(header.stat().st_mtime_ns, timestamp, "unchanged identity must not trigger rebuilds")
            (repo / "new-file").write_text("untracked change")
            self.assertTrue(capture()["dirty"])
            self.assertIn(initial + "-dirty", header.read_text())
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "next")
            next_commit = git("rev-parse", "HEAD")
            self.assertNotEqual(initial, next_commit)
            self.assertEqual(capture(), {"commit": next_commit, "dirty": False})
            self.assertIn(next_commit, header.read_text())
            self.assertEqual(capture(""), {"commit": "unknown", "dirty": True})

    def test_source_in_subdirectory_of_larger_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            source, output = repo / "launcher", root / "build"
            (source / "cmake").mkdir(parents=True)
            (repo / "other").mkdir()
            for name in ("BuildIdentity.h.in", "source.json.in"):
                shutil.copy2(SOURCE / "cmake" / name, source / "cmake" / name)
            (repo / "other" / "file").write_text("belongs to another component")

            def git(*args):
                return subprocess.check_output([GIT, "-C", str(repo), *args], text=True, stderr=subprocess.STDOUT).strip()

            def capture():
                subprocess.run([CMAKE, f"-DSOURCE_DIR={source}", f"-DOUTPUT_DIR={output}",
                                f"-DGIT_EXECUTABLE={GIT}", "-P",
                                str(SOURCE / "cmake" / "WriteBuildIdentity.cmake")], check=True)
                return json.loads((output / "source.json").read_text())

            git("init")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "fixture")
            commit = git("rev-parse", "HEAD")
            self.assertEqual(capture(), {"commit": commit, "dirty": False})
            (repo / "other" / "file").write_text("changed elsewhere in the repository")
            self.assertEqual(capture(), {"commit": commit, "dirty": False},
                             "changes outside the source directory must not mark the build dirty")
            (source / "new-file").write_text("untracked change")
            self.assertEqual(capture(), {"commit": commit, "dirty": True})

    def test_unpacked_archive_inside_unrelated_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outer, source, output = root / "outer", root / "outer" / "unpacked", root / "build"
            (source / "cmake").mkdir(parents=True)
            for name in ("BuildIdentity.h.in", "source.json.in"):
                shutil.copy2(SOURCE / "cmake" / name, source / "cmake" / name)
            subprocess.check_call([GIT, "-C", str(outer), "init", "-q"])
            (outer / "unrelated").write_text("not part of the archive")
            subprocess.check_call([GIT, "-C", str(outer), "add", "unrelated"])
            subprocess.check_call([GIT, "-C", str(outer), "-c", "user.name=Fixture",
                                   "-c", "user.email=fixture@example.invalid", "commit", "-q", "-m", "outer"])
            subprocess.run([CMAKE, f"-DSOURCE_DIR={source}", f"-DOUTPUT_DIR={output}",
                            f"-DGIT_EXECUTABLE={GIT}", "-P",
                            str(SOURCE / "cmake" / "WriteBuildIdentity.cmake")], check=True)
            self.assertEqual(json.loads((output / "source.json").read_text()), {"commit": "unknown", "dirty": True})


if __name__ == "__main__":
    unittest.main(verbosity=2)
