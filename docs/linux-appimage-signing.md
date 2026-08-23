# Linux AppImage signing

`Sign Linux AppImage release candidate` turns one exact, successful
`HolderTeam/holder-staging` AppImage artifact into a signed and tested release
candidate. It deliberately does not create or update a GitHub release.

## Trust boundary

The workflow lives in `holder-release` so ordinary changes to Holder's source,
build, and staging repositories cannot also change the signing policy. Configure
the fixed `linux-release-signing` GitHub environment with required reviewers;
the signing job cannot read that environment's secrets until a reviewer approves
the job.

The workflow:

1. Downloads an explicitly selected staging run and checks its SHA-256 manifest.
2. Checks the archive layout and requires the external provenance to exactly
   match the provenance embedded in the AppDir.
3. Repeats those checks inside the protected signing job.
4. Imports one passphrase-protected OpenPGP secret key into a temporary keyring.
5. Rebuilds and signs the AppImage with a reviewed, checksum-pinned AppImage
   runtime.
6. Signs the final SHA-256 manifest, exports the public key, and destroys the
   temporary secret keyring.
7. Verifies the manifest signature and smoke-tests the signed AppImage only
   after the private key is gone.
8. Creates a GitHub artifact attestation and uploads a 30-day release-candidate
   artifact.

Official GitHub actions, appimagetool 1.9.1, and AppImage runtime 20251108 are
pinned by digest or commit. Changing those pins is a reviewable release-policy
change.

## Required GitHub configuration

Create an environment named exactly `linux-release-signing` in
`HolderTeam/holder-release` and add:

- Environment secret `HOLDER_GPG_SIGNING_KEY_B64`: a base64 encoding of the
  exported private signing subkeys.
- Environment secret `HOLDER_GPG_SIGNING_PASSPHRASE`: the key passphrase.

The expected public identity is anchored by
`keys/holder-linux-release.asc` in this repository. Its primary fingerprint is
`E60EEFC6E1CCB99988DA2E274B0C85A5A86B24A2`; the workflow derives and checks the
fingerprint from that reviewed file rather than trusting a mutable GitHub
variable.

Configure required reviewers and restrict deployment branches to `main`. Keep
the private key and passphrase at environment scope, not as ordinary repository
secrets.

Cross-repository artifact downloads may also require the existing repository or
organisation secret `HOLDER_CI_ARTIFACT_TOKEN`. It needs only Actions read access
to `HolderTeam/holder-staging`; it is not a signing secret.

## Running the workflow

Start `Sign Linux AppImage release candidate` manually and provide:

- `expected_version`: the exact product version in the staging artifact.
- `staging_run_id`: the exact successful `Linux AppImage staged package` run.
- The default staging repository and artifact name normally need no changes.

Requiring an exact run is intentional. “Latest green main” is convenient for
staging, but signing should leave an unambiguous approval record.

The uploaded artifact is named
`Holder-linux-appimage-signed-<version>` and contains:

- The signed AppImage.
- The staged component provenance.
- Signing metadata identifying both workflow runs and the key fingerprint.
- The armored public key and a copy of the embedded AppImage signature.
- A one-file SHA-256 manifest for the AppImage and a detached OpenPGP signature
  over that manifest.

## Independent verification

After downloading and extracting the release-candidate artifact:

```sh
gpg --import Holder-linux-release-key.asc
gpg --verify Holder-<version>-SHA256SUMS.asc Holder-<version>-SHA256SUMS
sha256sum -c Holder-<version>-SHA256SUMS
gh attestation verify Holder-<version>-x86_64.AppImage \
  --repo HolderTeam/holder-release
```

The detached manifest signature is the straightforward end-user verification
path. The AppImage also contains an embedded OpenPGP signature for AppImage-aware
tools.

## Promoting to a draft release

Run `Promote Linux AppImage to draft release` with the exact version and
successful signing workflow run ID. The workflow re-verifies the signature,
provenance, smoke test, and GitHub artifact attestation before uploading these
release-facing files:

- `Holder-<version>-x86_64.AppImage`
- `Holder-<version>-SHA256SUMS`
- `Holder-<version>-SHA256SUMS.asc`
- `Holder-linux-release-key.asc`

The default tag is `v<version>`. An override is accepted only when it still
identifies the exact same version. The workflow uses an existing draft for that
tag or creates one with placeholder notes. It refuses to alter a published
release and never edits an existing draft's title or description.
