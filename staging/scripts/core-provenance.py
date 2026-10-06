#!/usr/bin/env python3
"""Validate framework component pins against the selected published core SDK."""
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


def load_pin(path, platform="linux"):
    document = json.loads(Path(path).read_text())
    pin = document
    if "platforms" in document:
        require(platform in document["platforms"], f"Release manifest has no {platform} selection")
        pin = {**document["platforms"][platform], "core": document["core"],
               "appimage_version": document["version"]}
    elif platform != "linux":
        require(False, "Windows/macOS require a framework manifest with platforms")
    commit(pin["core"]["commit"])
    require(pin["core"]["build_type"] in ("Release", "RelWithDebInfo"),
            "Unsupported pinned core build type")
    require(isinstance(pin["appimage_version"], str) and
            re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.+-]+)?", pin["appimage_version"]),
            "Invalid pinned AppImage version")
    # A manifest written when Windows and macOS still had a launcher may name one; it is ignored.
    for name in ("desktop", "backend"):
        component = pin[name]
        commit(component["commit"])
        require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", component["repository"]),
                f"Invalid {name} repository")
        require(re.fullmatch(r"[0-9]+", str(component["run_id"])), f"Invalid {name} run ID")
    return pin


def verify(selection, core, desktop_commit, backend_commit, pin=None, platform="linux", architecture="x86_64", expected_build_type=None):
    require(core["commit"] == selection["commit"],
            "Backend core revision differs from the selected SDK; choose a matching backend run")
    require(core["version"] == selection["version"], "Backend core version differs from selected SDK")
    require(core["platform"] == platform and core["architecture"] == architecture,
            f"Package requires the {platform} {architecture} SDK")
    assets = [asset for asset in selection["assets"]
              if asset["platform"] == core["platform"] and
              asset["architecture"] == core["architecture"] and
              asset["build_type"] == core["build_type"]]
    require(len(assets) == 1, "Backend SDK configuration is absent from the selected publication")
    if expected_build_type:
        require(core["build_type"] == expected_build_type, "Backend SDK build type differs from selected configuration")
    if pin:
        require(core["commit"] == pin["core"]["commit"] and
                core["build_type"] == pin["core"]["build_type"], "Backend does not match release core pin")
        require(desktop_commit == pin["desktop"]["commit"], "Desktop does not match release pin")
        require(backend_commit == pin["backend"]["commit"], "Backend does not match release pin")
    return {**core, "repository": selection["repository"],
            "release_tag": selection["release_tag"], "sdk_asset": assets[0],
            **({"daemon_commit": backend_commit} if backend_commit else {})}


def verify_component_builds(pin, desktop):
    require(desktop["commit"] == pin["desktop"]["commit"], "Desktop build metadata differs from release pin")
    require(desktop["build_type"] == "release", "Production manifest requires a release desktop artifact")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify"))
    parser.add_argument("--release-manifest")
    parser.add_argument("--selection")
    parser.add_argument("--desktop-root")
    parser.add_argument("--backend-root")
    parser.add_argument("--output")
    parser.add_argument("--core-manifest")
    parser.add_argument("--desktop-commit")
    parser.add_argument("--build-type", choices=("RelWithDebInfo", "Release"))
    parser.add_argument("--platform", default="linux", choices=("linux", "windows", "macos"))
    args = parser.parse_args()
    pin = load_pin(args.release_manifest, args.platform) if args.release_manifest else None
    if args.command == "prepare":
        components = ("desktop", "backend")
        values = {name: os.environ.get(name.upper() + "_INPUT", "") for name in
                  ("desktop_run_id", "backend_run_id", "appimage_version")}
        values["core_ref"] = os.environ.get("CORE_REF_INPUT", "latest-green")
        values["build_type"] = "RelWithDebInfo"
        for name in components:
            values[name + "_repository"] = os.environ[name.upper() + "_REPOSITORY_INPUT"]
        if pin:
            require(not any(values[name + "_run_id"] for name in components) and not values["appimage_version"]
                    and values["core_ref"] == "latest-green",
                    "Use the release manifest alone, without run, version or core-ref overrides")
            values.update(core_ref=pin["core"]["commit"], appimage_version=pin["appimage_version"],
                          build_type=pin["core"]["build_type"])
            for name in components:
                values[name + "_run_id"] = str(pin[name]["run_id"])
                values[name + "_repository"] = pin[name]["repository"]
        with open(os.environ["GITHUB_OUTPUT"], "a") as output:
            for key, value in values.items():
                require("\n" not in value and "\r" not in value, "Inputs must be single lines")
                output.write(f"{key}={value}\n")
    else:
        desktop_commit = args.desktop_commit
        backend_commit = None
        if args.desktop_root and args.platform == "linux":
            desktop_commit = (Path(args.desktop_root) / "release/holder-desktop-commit.txt").read_text().strip()
        if args.backend_root:
            backend = Path(args.backend_root)
            daemon_commit_file = backend / "release/holder-daemon-commit.txt"
            if daemon_commit_file.exists():
                backend_commit = daemon_commit_file.read_text().strip()
            core_path = (backend / "usr/share/holder-daemon/core-build.json" if args.platform == "linux"
                         else backend / "core-build.json")
        else:
            core_path = Path(args.core_manifest)
        result = verify(json.loads(Path(args.selection).read_text()),
                        json.loads(core_path.read_text()), desktop_commit, backend_commit, pin,
                        args.platform, "arm64" if args.platform == "macos" else "x86_64",
                        args.build_type)
        if pin and pin["core"]["build_type"] == "Release":
            desktop_info = json.loads((Path(args.desktop_root) / "release/holder-desktop-build.json").read_text())
            verify_component_builds(pin, desktop_info)
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
        print(f"Verified framework core SDK {result['commit']} ({result['build_type']})")


if __name__ == "__main__":
    main()
