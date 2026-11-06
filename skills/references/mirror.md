## 2. Evidence
- Label every material claim: OBSERVED (ran/read in this session; a result from an earlier session is CITED with its date or re-checked), CITED (specific source and revision; if none, retrieval date plus `no revision given`, date-bound, re-fetch before reuse in a later session), INFERRED (reasoned, not checked).
- Only OBSERVED or CITED can support a completion claim. Wording that a claim was verified, checked or recomputed needs an OBSERVED or CITED record from this session; otherwise label it INFERRED. Never infer that a file, skill, tool, dependency or platform exists from documentation; check. Unobservable means NOT_VERIFIED. Never fabricate sources, versions, commands or results.

## 3. Closed label sets (no others)
- Capability: EXISTS | PARTIAL | MISSING | CONFLICTING | NOT_VERIFIED
- Validity: VALID | STALE | FAILED | NOT_VERIFIED (key is `validity`, never a bare `status`)
- Adoption: REUSE | ADOPT | ADAPT | REFERENCE | REJECT | NOT_APPLICABLE
- Final: DONE | PARTIAL | BLOCKED
- Validity means: VALID = OBSERVED or CITED record whose revision and dependencies still match and whose cited evidence exists (a result not re-run in this session stays CITED, not OBSERVED); STALE = artifact or dependency changed after the record; FAILED = observed result contradicts the claim; NOT_VERIFIED = unchecked, unobservable, INFERRED-only or evidence missing. A probable failure that was not observed is NOT_VERIFIED.
- Domain labels (only permitted extension, never replacing the four sets): PASS | FAIL | NOT_VERIFIED | N/A; ALLOW | ALLOW_WITH_CONDITIONS | BLOCK; NOT_STARTED | ACTIVE; REQUIRED | OPTIONAL; OPEN | CLOSED; SIMULATED (qualifier on NOT_VERIFIED).
- PASS/FAIL derive from record validity: FAIL if any FAILED; NOT_VERIFIED if none, or any NOT_VERIFIED or STALE; else PASS. N/A needs a one-line reason.

## 4. Records and digest
- Every material result gets a record: claim_id | claim | basis | spec evidence | impl evidence | method | observed | artifact revision | runtime | dependencies (path + digest) | validity | checked_at. Fill fields only from this session's tool calls and output: method as run, observed as printed (non-zero exits included), checked_at from a clock reading; otherwise write `not recorded`; a record missing its method or observation is not OBSERVED.
- Revision of a multi-file artifact is `dir-digest-v1`: sha256 over, for each regular file sorted bytewise by POSIX relative path in UTF-8, the relpath bytes, 0x00, the file bytes, 0x00; no exclusions and no line-ending normalization; a symlink, any other non-regular file, an unreadable entry or a non-UTF-8 name means no valid digest (NOT_VERIFIED). Store 64 hex digits; reports may show 16. Never digest SKILL.md alone.
- When a dependency changes, mark STALE only records that depend on it. STALE or NOT_VERIFIED never supports DONE. Keep semantic and rendering verification separate.

## 5. Contract bottleneck
An unresolved or unverified interface, assumption or decision that other work depends on. Record: ID | undefined or unverified | dependent work | missing evidence | consequence | resolution test | state (OPEN, or CLOSED with evidence ID). Mark every dependent result conditional while open; close only by running the test and recording evidence.

## 6. Completion and gates
- DONE only if every REQUIRED criterion in the committed scope is VALID; PARTIAL lists gaps; BLOCKED states the cause. A required platform not passing prevents DONE; an unverified optional one does not.
- Keep separate claims: file exists, structure valid, discoverable, activates, behaves, composes, portable, production ready. Recompute every count, total and percentage, supplied ones included, from source data with a tool and record the command; a figure not recomputed by a tool is INFERRED, a stated figure that differs is FAILED.
- Ask the person or record an open decision before architecture decisions, irreversible actions, scope changes, adopting external code, and high-cost choices resting on INFERRED evidence. State options and evidence.
