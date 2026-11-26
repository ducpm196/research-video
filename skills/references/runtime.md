# Runtime notes

Labels follow SKILL.md section 2. The Runtime notes of SKILL.md keep the short form; this file holds the detail, for every runtime. Domain labels used here: NOT_VERIFIED, as registered in SKILL.md section 2.

## Contents
- A. Rules for every runtime
- B. Claude runtimes (Claude Code, Claude.ai, Anthropic API)
- C. Gemini runtimes (Google Antigravity, Gemini CLI, Gemini Chat, Google GenAI SDK)

## A. Rules for every runtime
Discovery evidence is the session's skill listing. A skill present in the skills directory but absent from the listing EXISTS but is not discoverable; report the two claims separately and never call it MISSING on file evidence alone. A skill installed, replaced or removed during a session is reported as installed only from two observations made after the change: dir-digest-v1 of the installed folder and the runtime's current skill listing. Whether a running session picks up the change differs by runtime and version: never state it from memory, and report NOT_VERIFIED when either observation is missing. A runtime may update or remove a synced folder at any time.

Repository access exists only if files are uploaded or a connector is present; otherwise repo-level checks are NOT_VERIFIED. If network is disabled or a source is unreachable, record NOT_VERIFIED; never decide from memory.

Never write into an installed or synced skill folder, not even an empty file to test write access: a stray file changes its digest and may sync. To check or edit a skill, copy it to a working directory, compute dir-digest-v1 of the source and the copy, and check or edit only the copy; if the two digests differ, or the source digest changes when recomputed after the check, the folder changed during the check: copy again and re-run. Deliver an edited skill as files for the person to install.

## B. Claude runtimes
Context independence: Do not rely on ephemeral chat history, prompt context, or model memory across turns. Long-horizon work must persist state in durable files (`state/` and `handover.md`). Deliver state artifacts with the file-delivery tool the runtime lists; where the runtime writes straight into the workspace (for example Claude Code), the workspace files are the delivery. Never assume a tool name or output path from this file: check the runtime's listing and record NOT_VERIFIED when it is absent. A fresh agent or resumed session reads only `handover.md` and `state/` without relying on prior chat memory.

Zip package layout: the zip holds the folder `evidence-gated-work/` as its single top-level entry with SKILL.md inside it, and the folder name equals the `name` field; a zip with SKILL.md at its root is not recognized by claude.ai. Check the layout before upload with `unzip -l`, or where unzip is absent (as on Windows) with `python -I -c "import sys, zipfile; print(*zipfile.ZipFile(sys.argv[1]).namelist(), sep=chr(10))" FILE.zip`.

Report claude.ai, Claude Code, and Anthropic API as separate platforms and check each one's own skill listing; never assume a skill present on one surface exists on another.

## C. Gemini runtimes
Cross-platform OS and tool execution: Runs on Windows (PowerShell/cmd) and Linux/macOS (bash). Use the runtime's own file and command tools as they appear in its tool listing; never assume a tool name or flag from this file, check the listing first and record NOT_VERIFIED when it is absent. Never poll background tasks in loops; wait for the runtime's completion notice.

Artifacts and scratch files: Store formal reports, verification DAG diagrams (Mermaid flowchart TD) and user-facing summaries in the runtime's artifact or output directory when one exists, otherwise in the workspace. Use a scratch/ subdirectory outside the skill folder for temporary scripts.

Subagents and teamwork: Delegate isolated verification or research to a subagent only when the runtime offers one. Do not poll its progress, and do not use inter-agent messaging to communicate with the user.

Slash commands and the web zip route: a slash command or an upload route is used only after the runtime's own listing or documentation shows it exists; otherwise report NOT_VERIFIED.

Zip package layout: the zip holds the folder `evidence-gated-work/` as its single top level entry (SKILL.md inside that folder), the layout claude.ai requires and the Agent Skills layout; a zip with SKILL.md at its root is not recognized there. Gemini app (formerly Gemini Chat, web), by its help pages as retrieved on 2026-11-24 (no revision given; fetch them again before relying on this): a skill is uploaded as a SKILL.md file, a folder, or a .zip file that holds SKILL.md in its main folder; the folder name must match the skill name; at most 100 MB in total; scripts that need the internet are not supported; Gems became read only on 2026-11-17 and are removed on 2026-12-17. Whether a zip with one top-level folder counts as SKILL.md in its main folder is NOT_VERIFIED: upload the folder `evidence-gated-work/` itself, and check that the skill is listed afterwards. Elsewhere install through the runtime's own skill mechanism, or use the instructions file (gemini-instructions.md).

Context independence: Do not rely on ephemeral chat history, prompt context, or model memory across turns. Long-horizon work must persist state in durable files (`state/` and `handover.md`). Deliver state artifacts using the session's file-delivery tool. A fresh agent or resumed session reads only `handover.md` and `state/` without relying on prior chat memory.

Report Google Antigravity, Gemini CLI, Gemini Chat, and Google GenAI SDK as separate platforms and check each one's own skill listing; never assume a skill present on one surface exists on another.
