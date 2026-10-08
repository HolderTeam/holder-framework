"""Generation checks must detect drift without refreshing the stored contract."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_check_rejects_owning_contract_drift_without_writing(tmp_path):
    snapshot = ROOT / "openapi/openapi.yaml"
    provenance = ROOT / "openapi/provenance.json"
    before = (snapshot.read_bytes(), provenance.read_bytes())
    source = tmp_path / "openapi.yaml"
    source.write_bytes(before[0] + b"\n# Changed owning contract\n")

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/generate.py"),
            "--check",
            "--source",
            str(source),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "Contract snapshot differs from the owning API" in result.stderr
    assert "Generating" not in result.stdout
    assert (snapshot.read_bytes(), provenance.read_bytes()) == before
