#!/usr/bin/env python3
"""Select successful, unexpired component artifacts and their source revisions."""
import argparse
import json
import os
import subprocess


def api(path, **query):
    command = ["gh", "api", "--method", "GET", path]
    for name, value in query.items():
        command += ["-f", f"{name}={value}"]
    return json.loads(subprocess.check_output(command, text=True))


def resolve(repository, workflow, branch, artifact, provided="", request=api):
    if provided and not provided.isdecimal():
        raise ValueError("Provided run ID must be numeric")
    if provided:
        runs = [request(f"repos/{repository}/actions/runs/{provided}")]
    else:
        runs = request(f"repos/{repository}/actions/workflows/{workflow}/runs",
                       branch=branch, status="success", per_page="30")["workflow_runs"]
    for run in runs:
        if run["status"] != "completed" or run["conclusion"] != "success":
            continue
        artifacts = request(f"repos/{repository}/actions/runs/{run['id']}/artifacts")["artifacts"]
        if any(item["name"] == artifact and not item["expired"] for item in artifacts):
            return str(run["id"]), run["head_sha"]
    raise ValueError(f"No successful {repository}@{branch} run has an unexpired {artifact} artifact")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=("windows", "macos"), required=True)
    args = parser.parse_args()
    suffix = args.platform
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        for component in ("desktop", "backend", "launcher"):
            repository = os.environ[component.upper() + "_REPOSITORY"]
            workflow = f"{suffix}-{component}.yml"
            if component == "backend":
                workflow = "daemon-integration.yml" if repository == "HolderTeam/holder-core" else "ci.yml"
                artifact = f"holder-daemon-{suffix}-backend"
            else:
                artifact = f"holder-{component}-{suffix}"
            run_id, sha = resolve(repository, workflow,
                                  os.environ.get(component.upper() + "_REF", "main"), artifact,
                                  os.environ.get(component.upper() + "_RUN_ID_INPUT", ""))
            output.write(f"{component}_run_id={run_id}\n{component}_commit={sha}\n")
            print(f"Selected {repository}#{run_id}: {artifact} at {sha}")


if __name__ == "__main__":
    main()
