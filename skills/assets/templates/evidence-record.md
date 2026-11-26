# O-0001
<!-- Template: copy, rename with your reference code and timestamp, replace the example text. Formats: the File formats section of the handoff reference. -->

```yaml
claim_id: O-0001
claim: "Example: the sample export parses and its row count equals the count in its header"
basis: OBSERVED
spec_evidence: "export-format.md#header"
impl_evidence: "samples/export.csv"
method: "python parse.py samples/export.csv"
observed: "printed rows=120 header=120, exit 0"
artifact_revision: "sha256 of samples/export.csv, see dependencies"
runtime: "agent and version, operating system"
dependencies: []
validity: VALID
checked_at: "2026-01-01T00:00:00Z"
```

Dependencies, when the result rests on files: list each as a path relative to the workspace root with its sha256 (file) or dir-digest-v1 (directory), or `claim:<record ID>` with `<validity>@<checked_at>`:

    dependencies:
      - path: "samples/export.csv"
        digest: "<64 hex digits>"
