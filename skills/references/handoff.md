# Durable state and handoff

Keeps long or multi-session work resumable from durable artifacts alone, never from chat history. Labels follow SKILL.md section 2; records follow SKILL.md sections 3 and 4. Domain labels used here: PASS | FAIL | NOT_VERIFIED, REQUIRED | OPTIONAL, NOT_STARTED | ACTIVE, OPEN | CLOSED, SIMULATED, as registered in SKILL.md section 2. On claude.ai, with no repository, `state/` is a set of files delivered with the session's file-delivery tool and re-uploaded to resume (SKILL.md, Claude.ai runtime notes).

## 5-Stage operational lifecycle (Scan -> Plan -> Execute -> Audit -> Handover)
Whenever an agent receives a user request or task, execute this complete 5-stage lifecycle:
1. **Stage 1 (Deep Scan & Knowledge Graph)**:
   - Perform a deep scan of the workspace, environment, constraints, and requirements.
   - Synthesize the initial knowledge graph file: `knowledge-graph_<reference_code>_<timestamp>.md` (and update `state/knowledge-graph.md`).
   - Register all initial observation nodes (`O-xxxx`), citation nodes (`S-xxxx`), initial claim nodes (`C-xxxx`), detected contract bottleneck nodes (`BN-xxxx`), and artifact nodes (`A-xxxx`).
   - Render an explicit Mermaid DAG (`flowchart TD`) and define staleness propagation edges.
2. **Stage 2 (Precise Reasoning & Execution Plan)**:
   - Reason strictly from the knowledge graph and generate the execution plan file: `plan_<reference_code>_<timestamp>.md`.
   - Specify: matching Reference Code and Timestamp, Task Objectives, Committed Scope & Exclusions, Ordered Work Packages with acceptance criteria (REQUIRED/OPTIONAL, SKILL.md section 2), Contract Bottlenecks register (7 mandatory fields, SKILL.md section 5), and Empirical Evidence Verification Plan.
3. **Stage 3 (Strict Execution per Plan)**:
   - Execute the task sequentially following the plan's work packages.
   - Gather direct empirical evidence (OBSERVED or CITED, SKILL.md section 1) for every material action.
   - Resolve and close open contract bottlenecks through their resolution tests before performing dependent actions; never build on open bottlenecks without marking dependent results conditional.
4. **Stage 4 (Audit, Acceptance & Knowledge Graph Update)**:
   - Perform rigorous audit and acceptance verification against 100% of the plan's acceptance criteria.
   - Run verification scripts and commands independently; observe real exit codes and outputs.
   - Update `knowledge-graph_<reference_code>_<timestamp>.md` (and `state/knowledge-graph.md`): transition claim nodes to VALID, FAILED, or STALE, mark resolved bottlenecks as CLOSED (with evidence ID), and verify the graph remains acyclic and grounded.
5. **Stage 5 (Professional Handover Synthesis)**:
   - Synthesize and publish the final handover report: `handover_<reference_code>_<timestamp>.md`.
   - Ensure `<reference_code>` and `<timestamp>` correspond exactly 1:1 to `plan_<reference_code>_<timestamp>.md`.
   - Simultaneously synchronize `handover.md` at the workspace root as the unified durable entrypoint for seamless cross-session continuation.
   - Follow the 7 mandatory handover sections defined below.

## State artifacts (repository, not chat)
Under `state/`:
- `objective.md`: `Objective | Committed scope | Excluded | Dependencies`.
- `baseline.md`: `Item | Path/version | Capability | Evidence ID`. Every capability uses the Capability set.
- `work-packages.md`: `ID | Goal | Acceptance criteria (REQUIRED/OPTIONAL) | Depends on | Lifecycle (NOT_STARTED/ACTIVE) | Final (DONE/PARTIAL/BLOCKED)`. Final stays `-` until every REQUIRED criterion is VALID. A completion that someone only reports, with no acceptance criteria and no VALID evidence, is written in the notes as `reported: DONE (by <who>, not verified)` and is never entered as Final.
- `bottlenecks.md`: the register from SKILL.md section 5.
- `evidence/`: one record per claim (SKILL.md section 3).
- `knowledge-graph.md`: explicit Directed Acyclic Graph (DAG) mapping every claim to its supporting observations or upstream claims, node validity, and staleness links.
- `next-task.md`: `Task | Inputs (files, evidence IDs) | Done when | Blocked by`. Blocked by lists bottleneck IDs and every input only the person can supply (access, files, decisions); write `none` only when neither exists.
- `handoff/`: reconstructions written by the receiving agent. The sealed ground truth stays outside `state/` and goes only to the grader, so a resuming agent cannot read it.
- `handover.md` (at workspace root): synthesized durable report generated at the completion of each task, recording what was done, what was not done, blockers/bottlenecks, next actions, and the DAG state.

## Knowledge graph and verification DAG
Ensures every reasoning step is grounded in verifiable evidence and visualized as a directed acyclic graph (DAG).
1. Node types:
   - `O-xxxx`: Observation (direct observation from command output or inspected file in this session).
   - `S-xxxx`: Citation (external authoritative source, revision or date).
   - `C-xxxx`: Claim (verified factual, structural, or logical claim).
   - `A-xxxx`: Artifact (created or edited file, script, or configuration).
   - `BN-xxxx`: Bottleneck (contract bottleneck gating downstream progress, SKILL.md section 5).
2. Edge types:
   - `grounded_in`: Claim -> Observation or Citation (basis: OBSERVED or CITED).
   - `depends_on`: Claim -> Upstream Claim (`claim:C-xxxx`).
   - `validates` / `invalidates`: Observation -> Claim.
   - `blocks`: Bottleneck -> Claim or Work package.
3. Graph invariants:
   - Acyclic: no circular dependencies permitted.
   - Grounding invariant: every material claim must connect via `grounded_in` or `depends_on` to at least one valid root observation (`O-xxxx`) or citation (`S-xxxx`). Pure inferences cannot ground DONE.
   - Downward staleness propagation: when any upstream node becomes STALE, FAILED or NOT_VERIFIED, all reachable downstream nodes in the DAG are immediately marked STALE.
   - Visual format: render the DAG as a Mermaid flowchart (`flowchart TD`) in state files and reports.

## Handover document protocol (handover.md and handover_<ref>_<ts>.md)
Whenever a task, milestone or session boundary is reached, synthesize and update `handover_<reference_code>_<timestamp>.md` and `handover.md` at the workspace root. This file is the primary entry point enabling zero-context continuation without relying on chat history.
Mandatory sections:
1. **Task Summary & Scope**: statement of task objective, committed scope, and explicit exclusions.
2. **Completed Work (Những gì đã làm được)**: list of delivered items, each mapped to its VALID verification record ID and corresponding DAG claim node.
3. **Unfinished Work & Gaps (Những gì chưa làm được)**: incomplete items, deferred scope, or missing criteria, with explicit causes.
4. **Blockers & Contract Bottlenecks (Blocker & Điểm nghẽn hợp đồng)**: full 7-field table for all OPEN bottlenecks (SKILL.md section 5), identifying missing evidence and consequences.
5. **Next Actions (Các việc cần làm tiếp theo)**: self-contained definitions of immediately executable next tasks, including required input files, completion criteria, and blockers.
6. **Knowledge Graph Snapshot (Đồ thị tri thức)**: Mermaid DAG diagram and node table showing current validity of all claims and dependencies.
7. **Integrity & Digest Manifest**: full 64-hex `dir-digest-v1` hashes of modified skill directories and `state/`, accompanied by ISO-8601 UTC timestamp.

## Checkpoints
Update the artifacts at every work-package boundary and before ending a session. After editing a file, recompute digests and mark STALE only the evidence that depends on it. A checkpoint is complete only when `handover.md` (or `handover_<ref>_<ts>.md`) and `next-task.md` are executable by an agent that has seen nothing else.

## Resume protocol (context independence)
1. Read `handover.md` (or latest `handover_<ref>_<ts>.md`) and `state/` only; do not rely on conversation history.
2. Re-observe the baseline items you will touch; do not trust a recorded capability or validity blindly.
3. Recompute digests; mark changed dependents STALE down the DAG.
4. List open bottlenecks and mark dependent work conditional.
5. Execute `next-task.md`, or report why it cannot run.

## Cross-agent handoff test
Interoperability is claimed only after a second, independently available runtime passes this test. Results are PASS | FAIL | NOT_VERIFIED; a same-runtime or simulated run is NOT_VERIFIED, labelled SIMULATED. This file holds the only copy of the definitions below.

Definitions:
- **Independent runtime**: a runtime whose product or surface differs from A's, or whose model family differs from A's. B starts in a new session that a person (or an orchestration A does not control) opens, and shares with A no conversation, memory, connector state or filesystem except the delivered repository. A second chat of the same product and model is the same runtime.
- **Grader**: a person or an agent other than B that holds the sealed ground truth. A may be the grader.
- **Match**: compare items 1 to 6 one by one. IDs, file paths, capability, validity and Final labels must be identical. Prose items match when the grader's rubric, written before B runs, judges them equivalent. One mismatch fails that item; PASS needs all six.

Procedure:
1. Agent A (runtime X) writes the sealed ground truth with six answers: (1) objective, (2) current baseline, (3) completed and active work packages, (4) open contract bottlenecks, (5) valid vs stale evidence, (6) next executable task. It is stored OUTSIDE the repository and `state/` that B will receive. Then A persists the state artifacts.
2. Agent B (independent runtime Y, fresh context, no conversation history) receives only the repository and `state/`, and writes `state/handoff/reconstruction-<runtime>.md` with the same six answers.
3. The grader compares B to the ground truth by the Match rule. PASS requires all six to match. Record differences.
4. If B could read the ground truth, the test is invalid: NOT_VERIFIED.
5. One runtime only, B saw the conversation, or B was simulated by A: NOT_VERIFIED, labelled SIMULATED. Never count it as interoperability.
6. The test report records: product, surface, model and version of A and B; the `dir-digest-v1` of the `state/` directory delivered to B; who graded; per-item results.
