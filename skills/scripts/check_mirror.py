#!/usr/bin/env python3
"""Mechanical check of the always-on instruction mirror against this skill.

Usage:  python3 check_mirror.py SKILL_DIR INSTRUCTIONS_FILE

Read-only, standard library only, no network, writes nothing but stdout.

SKILL_DIR is the skill directory (it holds SKILL.md and references/mirror.md).
INSTRUCTIONS_FILE is the always-on instruction text (the file pasted into the
person's preferences). Checks, each PASS | FAIL | NOT_VERIFIED:
  M1  references/mirror.md exists and SKILL.md has the four closed label lines
  M2  sections 2 to 6 of INSTRUCTIONS_FILE equal references/mirror.md after
      normalization (NFC, LF, trailing whitespace removed, no leading or
      trailing blank lines)
  M3  the closed label sets and the domain-label registry in mirror.md equal
      those in SKILL.md section 2
  M4  `Sync: EGW dir-digest-v1 [:16] = HEX` equals the digest of SKILL_DIR
  M5  `Mirror sha256 [:16] = HEX` equals the sha256 of the normalized mirror.md
Every run prints all five checks; a check that cannot run prints NOT_VERIFIED
with its reason. Semantic equivalence beyond M3 is a judgment, not decided here (INFERRED).

The last line is checked_at=<UTC ISO-8601>, the time of the run, for records.

Exit codes: 0 all PASS | 1 any FAIL | 4 none FAIL but some NOT_VERIFIED | 3 usage |
5 internal error: the run stopped, so no result was produced (never read it as FAIL).
"""
import hashlib
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone

sys.dont_write_bytecode = True  # keep the skill directory free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dir_digest  # noqa: E402

TOKEN = re.compile(r"[A-Z][A-Z_]*[A-Z]|N/A")
SETS = [("Capability", "- Capability:", "- Capability:"),
        ("Validity", "- Evidence validity:", "- Validity:"),
        ("Adoption", "- Adoption decision:", "- Adoption:"),
        ("Final", "- Final:", "- Final:")]


def normalize(text):
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    lines = [ln.rstrip() for ln in text.split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def find_line(text, prefix):
    for ln in text.split("\n"):
        if ln.startswith(prefix):
            return ln
    return None


def labels(line):
    return set(TOKEN.findall(line))


def run(skill_dir, instr_path):
    out = []

    def add(cid, res, detail=""):
        out.append((cid, res, detail))

    mirror_path = os.path.join(skill_dir, "references", "mirror.md")
    skill_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(mirror_path) or not os.path.isfile(skill_path):
        add("M1", "FAIL", "references/mirror.md or SKILL.md missing")
        for cid in ("M2", "M3", "M4", "M5"):  # never omit a check silently
            add(cid, "NOT_VERIFIED", "not run: M1 failed")
        return out
    mirror_raw, skill, instr = read(mirror_path), read(skill_path), read(instr_path)
    mirror = normalize(mirror_raw)
    add("M1", "PASS")

    m = re.search(r"^## 2\..*?(?=^## 7\.)", instr, re.S | re.M)
    if not m:
        add("M2", "FAIL", "sections 2 to 6 not found in %s" % os.path.basename(instr_path))
    else:
        got = normalize(m.group(0))
        if got == mirror:
            add("M2", "PASS")
        else:
            a, b = got.split("\n"), mirror.split("\n")
            i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            add("M2", "FAIL", "first difference at mirror line %d" % (i + 1))

    bad = []
    for name, skill_prefix, mirror_prefix in SETS:
        s_line, m_line = find_line(skill, skill_prefix), find_line(mirror, mirror_prefix)
        if s_line is None or m_line is None:
            bad.append("%s: line not found" % name)
        elif labels(s_line) != labels(m_line):
            bad.append("%s differs: %s" % (name, sorted(labels(s_line) ^ labels(m_line))))
    s_dom = next((ln for ln in skill.split("\n") if "Registry:" in ln), None)
    m_dom = find_line(mirror, "- Domain labels")
    if s_dom is None or m_dom is None:
        bad.append("Domain: line not found")
    elif labels(s_dom) != labels(m_dom):
        bad.append("Domain differs: %s" % sorted(labels(s_dom) ^ labels(m_dom)))
    add("M3", "FAIL" if bad else "PASS", "; ".join(bad))

    digest, _files, findings = dir_digest.compute(skill_dir)
    sync = re.search(r"Sync: EGW dir-digest-v1 \[:16\] = ([0-9a-fA-F]{16})\b", instr)
    if digest is None:
        add("M4", "NOT_VERIFIED", "no valid digest: %s" % findings[:2])
    elif not sync:
        add("M4", "NOT_VERIFIED", "no Sync line in instructions")
    else:
        add("M4", "PASS" if digest.startswith(sync.group(1).lower()) else "FAIL", "actual %s" % digest[:16])

    mir = re.search(r"Mirror sha256 \[:16\] = ([0-9a-fA-F]{16})\b", instr)
    actual = hashlib.sha256(mirror.encode("utf-8")).hexdigest()
    if not mir:
        add("M5", "NOT_VERIFIED", "no Mirror line in instructions")
    else:
        add("M5", "PASS" if actual.startswith(mir.group(1).lower()) else "FAIL", "actual %s" % actual[:16])
    return out


def main(argv):
    if len(argv) != 3 or not os.path.isdir(argv[1]) or not os.path.isfile(argv[2]):
        sys.stderr.write(__doc__)
        return 3
    try:
        results = run(argv[1], argv[2])
    except Exception as err:  # exit 1 means FAIL; a crash is no result at all
        sys.stderr.write("INTERNAL ERROR, no result: %s: %s\n" % (type(err).__name__, err))
        return 5
    for cid, res, detail in results:
        print("%-3s %-12s %s" % (cid, res, detail))
    counts = {k: sum(1 for r in results if r[1] == k) for k in ("PASS", "FAIL", "NOT_VERIFIED")}
    print("checks=%d PASS=%d FAIL=%d NOT_VERIFIED=%d" % (
        len(results), counts["PASS"], counts["FAIL"], counts["NOT_VERIFIED"]))
    print("checked_at=%s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return 1 if counts["FAIL"] else (4 if counts["NOT_VERIFIED"] else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
