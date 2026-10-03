#!/usr/bin/env python3
"""Validate AppImage component pins against the selected published core SDK."""
import argparse
import json
import os
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def commit(value):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value),
            "Release pins must use full lowercase commit SHAs")
    return value


def load_pin(path):
    pin = json.loads(Path(path).read_text())
    commit(pin["core"]["commit"])
    require(pin["core"]["build_type"] in ("Release", "RelWithDebInfo"),
            "Unsupported pinned core build type")
    require(isinstance(pin["appimage_version"], str) and
            re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.+-]+)?", pin["appimage_version"]),
            "Invalid pinned AppImage version")
    for name in ("desktop", "backend"):
        component = pin[name]
        commit(component["commit"])
        require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", component["repository"]),
                f"Invalid {name} repository")
        require(re.fullmatch(r"[0-9]+", str(component["run_id"])), f"Invalid {name} run ID")
    return pin


def verify(selection, core, desktop_commit, backend_commit, pin=None):
    require(core["commit"] == selection["commit"],
            "Backend core revision differs from the selected SDK; choose a matching backend run")
    require(core["version"] == selection["version"], "Backend core version differs from selected SDK")
    require(core["platform"] == "linux" and core["architecture"] == "x86_64",
            "AppImage requires the Linux x86_64 SDK")
    assets = [asset for asset in selection["assets"]
              if asset["platform"] == core["platform"] and
              asset["architecture"] == core["architecture"] and
              asset["build_type"] == core["build_type"]]
    require(len(assets) == 1, "Backend SDK configuration is absent from the selected publication")
    if pin:
        require(core["commit"] == pin["core"]["commit"] and
                core["build_type"] == pin["core"]["build_type"], "Backend does not match release core pin")
        require(desktop_commit == pin["desktop"]["commit"], "Desktop does not match release pin")
        require(backend_commit == pin["backend"]["commit"], "Backend does not match release pin")
    return {**core, "repository": selection["repository"],
            "release_tag": selection["release_tag"], "sdk_asset": assets[0]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify"))
    parser.add_argument("--release-manifest")
    parser.add_argument("--selection")
    parser.add_argument("--desktop-root")
    parser.add_argument("--backend-root")
    parser.add_argument("--output")
    args = parser.parse_args()
    pin = load_pin(args.release_manifest) if args.release_manifest else None
    if args.command == "prepare":
        values = {name: os.environ.get(name.upper() + "_INPUT", "") for name in
                  ("desktop_run_id", "backend_run_id", "appimage_version")}
        values["core_ref"] = os.environ.get("CORE_REF_INPUT", "latest-green")
        for name in ("desktop", "backend"):
            values[name + "_repository"] = os.environ[name.upper() + "_REPOSITORY_INPUT"]
        if pin:
            require(not any(values[name] for name in ("desktop_run_id", "backend_run_id", "appimage_version"))
                    and values["core_ref"] == "latest-green",
                    "Use the release manifest alone, without run, version or core-ref overrides")
            values.update(core_ref=pin["core"]["commit"], appimage_version=pin["appimage_version"])
            for name in ("desktop", "backend"):
                values[name + "_run_id"] = str(pin[name]["run_id"])
                values[name + "_repository"] = pin[name]["repository"]
        with open(os.environ["GITHUB_OUTPUT"], "a") as output:
            for key, value in values.items():
                require("\n" not in value and "\r" not in value, "Inputs must be single lines")
                output.write(f"{key}={value}\n")
    else:
        desktop = Path(args.desktop_root)
        backend = Path(args.backend_root)
        result = verify(json.loads(Path(args.selection).read_text()),
                        json.loads((backend / "usr/share/holder-daemon/core-build.json").read_text()),
                        (desktop / "release/holder-desktop-commit.txt").read_text().strip(),
                        (backend / "release/holder-daemon-commit.txt").read_text().strip(), pin)
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
        print(f"Verified AppImage core SDK {result['commit']} ({result['build_type']})")


if __name__ == "__main__":
    main()
