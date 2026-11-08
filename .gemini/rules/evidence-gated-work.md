# Evidence-Gated Work Rule for Google Antigravity & Gemini runtimes

Optional always-on rule. Copy it into the rules or context location that your runtime documents (the exact path for Antigravity and Gemini CLI is NOT_VERIFIED here; check the runtime's own documentation). The full procedures live in the skill `evidence-gated-work`.

## 5-Stage Operational Lifecycle (Mandatory Protocol)
Whenever receiving a user request or initiating a non-trivial task, follow this exact sequence:
1. **Stage 1 (Deep Scan & Knowledge Graph)**: Perform a deep scan of the workspace, files, and dependencies. Synthesize the initial knowledge graph file `knowledge-graph_<ref>_<ts>.md` (and maintain `state/knowledge-graph.md`). Graph nodes include observations (`O-xxxx`), citations (`S-xxxx`), claims (`C-xxxx`), contract bottlenecks (`BN-xxxx`), and artifacts (`A-xxxx`) arranged in an explicit Mermaid DAG (`flowchart TD`).
2. **Stage 2 (Precise Reasoning & Execution Plan)**: Reason with precision from the knowledge graph and generate `plan_<ref>_<ts>.md`. Specify matching Reference Code and Timestamp, Task Objectives, Committed Scope & Exclusions, Ordered Work Packages with acceptance criteria (REQUIRED/OPTIONAL), Contract Bottlenecks register (7 mandatory fields), and Evidence verification plan.
3. **Stage 3 (Strict Execution per Plan)**: Execute sequentially per plan. Gather direct empirical evidence (OBSERVED/CITED) for every material action. Resolve and close open contract bottlenecks through their resolution tests before dependent actions; never build on open bottlenecks without marking conditional.
4. **Stage 4 (Audit Acceptance & Knowledge Graph Update)**: Perform rigorous audit and acceptance verification against 100% of plan criteria. Re-run verification commands independently; inspect real outputs. Update `knowledge-graph_<ref>_<ts>.md` (and `state/knowledge-graph.md`): transition nodes to VALID/CLOSED.
5. **Stage 5 (Professional Handover Synthesis)**: Synthesize and output `handover_<ref>_<ts>.md` (with `<ref>` and `<ts>` matching `plan_<ref>_<ts>.md` 1:1) and synchronize `handover.md` at the workspace root covering the 7 standard EGW sections.

## Core Rules & Invariants
1. **Evidence Basis**: Label every material claim OBSERVED, CITED, or INFERRED. Only OBSERVED or CITED can support completion statements. INFERRED never can.
2. **Verification DAG & Staleness**: Multi-step reasoning must build upon a Directed Acyclic Graph (DAG). When an upstream node becomes STALE, FAILED, or NOT_VERIFIED, immediately propagate STALE transitively down all downstream claims.
3. **Contract Bottlenecks**: Record open interfaces, assumptions, or unverified dependencies with all 7 mandatory fields:
   `ID | undefined or unverified | dependent work | missing evidence | consequence | resolution test | state (OPEN | CLOSED with evidence ID)`.
   Never build on an OPEN bottleneck without explicitly marking dependent claims conditional.
4. **Context Independence**: Never rely on ephemeral chat history across turns. Persist durable state to `state/` and deliver state files so a fresh session resumes with zero chat context.
