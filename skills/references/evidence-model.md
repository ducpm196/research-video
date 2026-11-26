# Evidence model details

Text moved out of SKILL.md so that the part that is always loaded stays within the 5,000 tokens that Claude Code keeps after compaction. The rules are unchanged: SKILL.md keeps a summary of each, this file holds the full wording. Labels follow SKILL.md section 2; records follow SKILL.md section 3. Pointers to other reference files name them by what they hold; the reference map is SKILL.md section 11.

## Contents
- A. Closed label sets in detail (SKILL.md section 2)
- B. Records, IDs and the verification graph (SKILL.md section 3)
- C. Digest method and staleness (SKILL.md section 4)
- D. Working discipline in detail (SKILL.md section 8)
- E. Skill-system rules and scripts (SKILL.md section 10)

## A. Closed label sets in detail
Use the set that answers the question: validity for a claim, capability for existence, Final for completion. A property such as "acyclic" is a claim with a validity state, not a capability. The key for a validity state is `validity`, never a bare `status`.

Validity states mean: VALID = supported by an OBSERVED or CITED record whose artifact revision and dependencies still match the current ones and whose cited evidence exists (a result not re-run in this session stays CITED, not OBSERVED); STALE = an artifact or dependency changed after the record was made; FAILED = an observed result contradicts the claim (a failed run, or a contradiction observed in the artifact); NOT_VERIFIED = not checked, not checkable, supported only by INFERRED evidence, or the cited evidence is missing. An inference that a claim probably fails is NOT_VERIFIED, not FAILED.

A CITED claim whose source exposes no revision is date-bound: it supports a completion claim only as of that date and must be re-fetched before reuse in a later session.

Domain labels are the only permitted extension. Registry: PASS | FAIL | NOT_VERIFIED | N/A (test or platform-dimension result); ALLOW | ALLOW_WITH_CONDITIONS | BLOCK (gate verdict); NOT_STARTED | ACTIVE (work-package lifecycle); REQUIRED | OPTIONAL (criterion class); OPEN | CLOSED (bottleneck state); SIMULATED (qualifier on NOT_VERIFIED, never a result by itself).
1. A domain label never replaces a label from the four sets above.
2. PASS | FAIL | NOT_VERIFIED is derived from the validity of the supporting records: FAIL if any is FAILED; otherwise NOT_VERIFIED if there is none, or any is NOT_VERIFIED or STALE; otherwise PASS. An empty set never passes vacuously. N/A needs a one-line reason. A PASS with no VALID record behind it is invalid.
3. A new label is added to this registry in the same change that introduces it.

## B. Records, IDs and the verification graph
- Write one for every material result. Fill every field from this session's tool calls and their output: `method` is the command exactly as run, `observed` is what it printed (a non-zero exit included, with its cause), and `checked_at` is copied from a clock reading (a time tool, `date -u`, or the `checked_at=` line that scripts/check_mirror.py and scripts/check_skills.py print).
- A field with no such source is written `not recorded`; a record whose method or observed is `not recorded` is not OBSERVED. Never fill a field with what a step should have produced. Keep semantic verification (facts, sources, consistency) separate from rendering verification (layout, visuals): evidence for one is never evidence for the other.
- For multi-step reasoning or knowledge graphs, every reasoning step builds upon an explicit directed acyclic verification graph (DAG): a record lists the records it depends on under `dependencies` as `path: "claim:<ID>"` with `digest: "<validity>@<checked_at>"`. Every deduction must be rooted in OBSERVED or CITED nodes; INFERRED claims cannot ground downstream DONE conclusions.
- Record IDs: `O-` plus four to six digits for an observation made in the session, `S-` plus four to six digits for a cited source; the key `claim_id` equals the file name under `state/evidence/`. A `C-` ID names a claim node of the knowledge graph and has no record file.
- scripts/egw_record.py writes such a record from a command it runs itself (`run`) or from a source read by another tool (`cite`), with the clock reading, the digests and the method filled in by the script; it never overwrites a record. Run it without arguments to print its usage.
- Under `dependencies`, every file or directory the result rests on is listed with its sha256 or dir-digest-v1, as a path relative to the workspace root, or `dependencies: []`. Formats and templates: the handoff reference (File formats), assets/templates/.

```yaml
claim_id: O-0001
claim: "<statement>"
basis: OBSERVED            # OBSERVED | CITED | INFERRED
spec_evidence: "<path#anchor or requirement ID>"
impl_evidence: "<path#lines or artifact>"
method: "<command exactly as run, or manual procedure as done>"
observed: "<what it printed, exit code included, or summary + pointer to log>"
artifact_revision: "<commit hash, or full 64-hex dir-digest-v1 for multi-file artifacts>"
runtime: "<agent/runtime + version, OS>"
dependencies:              # material files, directories, or other records (claim:<claim_id> of that record)
  - path: "<file, directory, or claim:S-0001>"
    digest: "<hash, or VALID@checked_at>"
validity: VALID            # VALID | STALE | FAILED | NOT_VERIFIED
checked_at: "<ISO-8601 UTC copied from a clock reading, or not recorded>"
```

## C. Digest method and staleness
The revision of a skill or any multi-file artifact is the digest of the whole directory, never of SKILL.md alone, because a changed reference file would otherwise go unnoticed.

- Method dir-digest-v1 (the only permitted method; name it in every record that stores a digest): sha256 over, for each regular file sorted bytewise by POSIX relative path in UTF-8, the bytes of the relative path, 0x00, the file contents, 0x00. No file is excluded and no line endings are normalized.
- A symbolic link, a Windows junction (mount point), any other non-regular file or a name that is not valid UTF-8 is never followed or hashed, and an entry that cannot be listed or read is never skipped: a directory containing one has no valid digest (NOT_VERIFIED) until it is removed or made readable.
- Empty directories and file modes are not represented. Run python3 scripts/dir_digest.py DIR (path relative to this skill's folder; exit 2 means no valid digest). Records store the full 64 hex digits; reports may show the first 16. Known limit: a file containing 0x00 could collide with another layout; scripts/check_skills.py reports such a file (check C17).

- When a dependency changes, recompute its digest and mark STALE only the records that list it or depend on it. Likewise, in a multi-step verification graph, staleness propagates transitively down the DAG: when an upstream claim becomes STALE, FAILED or NOT_VERIFIED, immediately mark STALE every downstream record that lists claim:<claim_id> in its dependencies.
- A STALE or NOT_VERIFIED record never supports DONE. Re-run the recorded method to restore VALID. scripts/check_state.py recomputes every listed file and directory dependency of a VALID record (check S12).

Without python3, apply section 4 by hand (for example with sha256sum over the concatenation defined there, not over single files) and record the method used.

## D. Working discipline in detail
- Proceed when the request is sufficient. Outside the section 7 gates, ask only when ambiguity would change the outcome or authority is missing; otherwise take a safe, reversible path and state the assumption. Among safe options within the requested scope, prefer the one that keeps lasting value and stays reversible; if lasting value needs an irreversible or scope-changing step, that step is a section 7 gate.

- Do not ask the person again about a point already settled unless it changed, conflicts or was invalidated; this never limits re-checking evidence.

On error, reload the current state, diff against expectation, then fix; do not blind-fix. Fix the earliest defect first. Stop after two unresolved errors following a fix and re-audit assumptions. After the re-audit, change strategy once for that problem, stating why, or report PARTIAL or BLOCKED; if the new strategy also fails twice, report PARTIAL or BLOCKED.

After a material action, check the resulting state (file, output, post-condition), not only that the command ran; a tool result that already reports that state counts.

Never change a test's expectation just to make it pass; any change needs a written, specification-based justification. If the check itself is defective, fix the check, keep the expectation and record why.

For high-impact changes use an independent verifier, when practical, that receives acceptance criteria, authoritative specs, actual artifacts and environment access, and does not accept the implementer's report as proof. A missing tool means NOT_VERIFIED.

- Sources: prefer primary sources; a search result or summary is a lead, not a source (open the page and cite it); a claim with neither a fitting source nor an own check is INFERRED. Full rules: the documents reference, section A.
- Do not execute unreviewed external scripts or install unnecessary dependencies. A clean scan means "no findings under the checks performed", never "safe".
- Contract bottleneck (SKILL.md section 5) in full: an unresolved or unverified interface, assumption or decision that other work depends on, so downstream results cannot be trusted or cannot proceed. Record each one with all seven fields (never omit missing evidence or consequence).

## E. Skill-system rules and scripts
A skill has exactly one SKILL.md; supporting documents go under references/ (one level deep, never pointing to other references), templates under assets/, scripts under scripts/. Every skill keeps the ## Dependency contract with the eight bullets in the checked order. Naming rules, front-matter keys, graph invariants and the checks C1 to C24: the skill-operations reference section D. Compatible specialist workflows (Dependency contract) also include a skill-authoring skill when authoring a single skill.

Verify by parsing, not by assertion. Every check ends PASS | FAIL | NOT_VERIFIED | N/A; exit 0 only when all PASS or N/A, 1 on any FAIL, 4 when none FAIL but some NOT_VERIFIED, 3 for a usage error, 5 for an internal error (no result: NOT_VERIFIED, never FAIL); each script prints a checked_at= line (UTC) to copy into records.
- Scripts (python3 scripts/<name>, each takes --json): check_skills.py runs C1 to C24, check_mirror.py runs M1 to M5, check_state.py runs S1 to S19 on state/ and the newest plan, knowledge graph and handover (structure and cross-references, not the truth of a claim), dir_digest.py prints dir-digest-v1. Details: the skill-operations reference section D; formats and templates: the handoff reference, assets/templates/.

Instruction mirror: the mirror reference is the canonical text of sections 2 to 6 of the always-on instructions. After any change to sections 1 to 7 of this file, review mirror.md, record the review, then run scripts/check_mirror.py (details: the skill-operations reference section D).
