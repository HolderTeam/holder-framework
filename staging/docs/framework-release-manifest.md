# Framework release manifests

Development staging follows latest-green. For an RC or production release,
commit one manifest and pass the same `release_manifest` path to all three
staging workflows. Each reads its platform entry, uses the shared product
version/core pin, and bundles the original manifest in the package.

1. Select one published core commit and record its full SHA.
2. Dispatch daemon `ci.yml` with that `core_ref` and `core_build_type=Release`.
3. Dispatch desktop artifact workflows with `build_type=release`, and the
   Windows/macOS launcher workflows with `build_type=Release`.
4. After the selected runs pass, record their run IDs and source commits below.
5. Commit the manifest and run staging with its relative path. Leave core/run
   overrides at defaults. Windows branch validation can additionally use
   `sign_test_installer=false`; normal main staging retains protected signing.

```json
{
  "version": "0.2.1-rc.1",
  "core": {"commit": "<full core SHA>", "build_type": "Release"},
  "platforms": {
    "linux": {
      "desktop": {"repository": "HolderTeam/holder-desktop", "run_id": "<Linux desktop run>", "commit": "<desktop SHA>"},
      "backend": {"repository": "HolderTeam/holder-daemon", "run_id": "<daemon Release run>", "commit": "<daemon SHA>"}
    },
    "windows": {
      "desktop": {"repository": "HolderTeam/holder-desktop", "run_id": "<Windows desktop run>", "commit": "<desktop SHA>"},
      "backend": {"repository": "HolderTeam/holder-daemon", "run_id": "<daemon Release run>", "commit": "<daemon SHA>"},
      "launcher": {"repository": "HolderTeam/holder-launcher", "run_id": "<Windows launcher run>", "commit": "<launcher SHA>"}
    },
    "macos": {
      "desktop": {"repository": "HolderTeam/holder-desktop", "run_id": "<macOS desktop run>", "commit": "<desktop SHA>"},
      "backend": {"repository": "HolderTeam/holder-daemon", "run_id": "<daemon Release run>", "commit": "<daemon SHA>"},
      "launcher": {"repository": "HolderTeam/holder-launcher", "run_id": "<macOS launcher run>", "commit": "<launcher SHA>"}
    }
  }
}
```

Replace placeholders with full lowercase commit SHAs and numeric run IDs.
The same daemon run supplies all three platform artifacts. Desktop and launcher
commits may differ between platform entries when deliberately selected; each
entry is checked against its selected run and build metadata.

A Release manifest selects artifact names ending in `-release` and rejects
development desktop, daemon/core or launcher configurations. Backend's own
source revision is checked independently of the workflow run revision. Missing
platform entries, expired artifacts, failed runs or mismatched pins stop staging
before assembly. Existing Linux-only manifests with `appimage_version` and
top-level component entries remain supported.

Actions component artifacts have limited retention. Stage the candidate while
those inputs are available; signing and promotion subsequently consume the
verified staged product. Pin changes require rebuilding/rechecking the affected
candidate rather than silently selecting different component runs.
