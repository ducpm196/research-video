#!/usr/bin/env python3
"""Reference parser for the skill dependency graph and structure (EGW SKILL.md section 10).

Read-only, standard library only, no network, writes nothing but stdout.

Usage:  python3 check_skills.py SKILLS_DIR [--root-skill NAME] [--expect-root-digest HEX]
                                    [--platform-skill NAME[,NAME...]]...
  SKILLS_DIR            directory whose subdirectories are skills (each has SKILL.md)
  --root-skill NAME     the registry owner (default: evidence-gated-work)
  --expect-root-digest  16 or 64 hex digits: compare with dir-digest-v1 of the root skill
                        (the sync check of an instruction text that mirrors the root)
  --platform-skill      a platform-provided skill installed in SKILLS_DIR (repeatable,
                        or comma-separated). EGW section 10 makes the ecosystem rules N/A
                        for it: C6, C7, C9, C10, C11, C12 and C14 print N/A with a reason;
                        packaging and file checks C1-C5, C13 and C15 still run; it is
                        left out of the C8 graph. Naming the root, or a skill that is not
                        installed, is a usage error. The person supplies the list (for
                        example from the runtime's skill listing); the script never guesses it.

Each check prints PASS | FAIL | NOT_VERIFIED | N/A (domain labels registered in EGW
section 2). NOT_VERIFIED means the script cannot decide and a person must.
The last line is checked_at=<UTC ISO-8601>, the time of the run, for records.
Exit codes: 0 every check PASS or N/A | 1 at least one FAIL | 4 no FAIL, some NOT_VERIFIED | 3 usage |
5 internal error: the run stopped, so no result was produced (never read it as FAIL).
Checks C1-C16 are listed in CHECKS below.
"""
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone

sys.dont_write_bytecode = True  # keep skill directories free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dir_digest  # noqa: E402

CONTRACT_ORDER = [
    "Capability ownership", "Trigger conditions", "Exclusions", "Required capabilities",
    "Optional dependencies", "Canonical standards referenced",
    "Compatible specialist workflows", "Verification requirements",
]
DOMAIN_LABELS = ["ALLOW_WITH_CONDITIONS", "NOT_STARTED", "ALLOW", "BLOCK", "PASS", "FAIL",
                 "ACTIVE", "OPEN", "CLOSED", "SIMULATED", "REQUIRED", "OPTIONAL"]
LABEL_RE = re.compile(r"(?<![A-Z_])(%s)(?![A-Z_])|(?<![A-Za-z])N/A(?![A-Za-z])" % "|".join(DOMAIN_LABELS))
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")  # hyphenated: read as a skill name
WORD = re.compile(r"^[a-z0-9]{1,64}$")  # single word: a skill only if installed, else ambiguous
CHECKS = {
    "C1": "front matter has name and description in single-line form",
    "C2": "name equals directory name, [a-z0-9-]{1,64}, no reserved word",
    "C3": "description 1-1024 characters, no XML tag",
    "C4": "SKILL.md at most 500 lines (front matter included, stricter than body-only)",
    "C5": "all text files are Unicode NFC",
    "C6": "Dependency contract has the 8 bullets in the required order",
    "C7": "every skill named in Required capabilities is installed",
    "C8": "dependency graph (Required + Optional) is acyclic",
    "C9": "root is the only root: others require it, it references no installed skill",
    "C10": "a file that names a domain label cites 'EGW section 2' (legacy 'VGHS section 2' accepted)",
    "C11": "no bare `status:` key (the validity key is `validity`)",
    "C12": "references/ files do not point to other references/ files",
    "C13": "every references/ or scripts/ file named in SKILL.md or references/ exists (own or cross-skill)",
    "C14": "every 'section N' reference points to an existing numbered heading",
    "C15": "no __pycache__ or .pyc inside a skill directory (would change its digest)",
    "C16": "root digest equals the expected digest (only with --expect-root-digest)",
}


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def parse_front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, "no front matter"
    fm, problem = {}, None
    for line in m.group(1).split("\n"):
        kv = re.match(r"^([A-Za-z0-9_-]+):[ ]?(.*)$", line)
        if not kv:
            problem = "unsupported line: %r" % line[:40]
            continue
        val = kv.group(2).strip()
        if val in ("", ">", "|", ">-", "|-"):
            problem = "multi-line value for %s" % kv.group(1)
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        fm[kv.group(1)] = val
    return fm, problem


def contract_bullets(text):
    sec = re.search(r"^## Dependency contract\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not sec:
        return None
    return re.findall(r"^- ([^:\n]+): (.*)$", sec.group(1), re.M)


def headings(text):
    return {int(n) for n in re.findall(r"^#{2,3} (\d+)\.", text, re.M)}


def section_numbers(spec):
    nums = set()
    for a, b in re.findall(r"(\d+)(?:\s+to\s+(\d+))?", spec):
        nums.update(range(int(a), int(b or a) + 1))
    return nums


SEC = r"([0-9]+(?:\s+to\s+[0-9]+)?(?:(?:,|\s+and)\s+[0-9]+(?:\s+to\s+[0-9]+)?)*)"


def find_cycle(graph):
    state = {}

    def dfs(u, path):
        state[u] = 1
        for v in sorted(graph[u]):
            if v not in graph:
                continue
            if state.get(v) == 1:
                return path + [u, v]
            if v not in state:
                found = dfs(v, path + [u])
                if found:
                    return found
        state[u] = 2
        return None

    for s in sorted(graph):
        if s not in state:
            found = dfs(s, [])
            if found:
                return found
    return None


def run(skills_dir, root_skill, expect_digest, platform=frozenset()):
    results = []  # (check_id, skill, result, detail)
    PLATFORM_NA = "platform-provided skill (EGW section 10)"

    def add(cid, skill, result, detail=""):
        results.append((cid, skill, result, detail))

    names = sorted(d for d in os.listdir(skills_dir)
                   if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md")))
    texts = {s: read(os.path.join(skills_dir, s, "SKILL.md")) for s in names}
    if root_skill not in names:
        add("C9", root_skill, "FAIL", "root skill is not installed in %s" % skills_dir)
    root_headings = headings(texts.get(root_skill, ""))
    graph, required = {}, {}

    for s in names:
        t = texts[s]
        fm, problem = parse_front_matter(t)
        if fm is None or "name" not in fm or "description" not in fm:
            add("C1", s, "FAIL", problem or "name or description missing")
        elif problem:
            add("C1", s, "NOT_VERIFIED", problem)
        else:
            add("C1", s, "PASS")
        fm = fm or {}
        name, desc = fm.get("name", ""), fm.get("description", "")
        bad = []
        if name != s:
            bad.append("name %r != directory" % name)
        if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
            bad.append("name pattern")
        if "anthropic" in name or "claude" in name:
            bad.append("reserved word")
        add("C2", s, "FAIL" if bad else "PASS", "; ".join(bad))
        bad = []
        if not 1 <= len(desc) <= 1024:
            bad.append("length %d" % len(desc))
        if re.search(r"</?[A-Za-z][^>]*>", desc):
            bad.append("XML tag")
        add("C3", s, "FAIL" if bad else "PASS", "; ".join(bad))
        n_lines = len(t.splitlines())
        add("C4", s, "FAIL" if n_lines > 500 else "PASS", "%d lines" % n_lines)

        bad, not_nfc, bare_status = [], [], []
        for dirpath, _dirs, files in os.walk(os.path.join(skills_dir, s)):
            for f in files:
                p = os.path.join(dirpath, f)
                rel = os.path.relpath(p, skills_dir)
                if "__pycache__" in rel or f.endswith(".pyc"):
                    bad.append(rel)
                    continue
                try:
                    body = read(p)
                except (UnicodeDecodeError, OSError):
                    continue  # binary or unreadable: not a text file
                if unicodedata.normalize("NFC", body) != body:
                    not_nfc.append(rel)
                if re.search(r"^\s*-?\s*status\s*:", body, re.M | re.I):
                    bare_status.append(rel)
        add("C5", s, "FAIL" if not_nfc else "PASS", ", ".join(not_nfc[:3]))
        if s in platform:
            add("C11", s, "N/A", PLATFORM_NA)
        else:
            add("C11", s, "FAIL" if bare_status else "PASS", ", ".join(bare_status[:3]))
        add("C15", s, "FAIL" if bad else "PASS", ", ".join(bad[:3]))

        bullets = contract_bullets(t)
        keys = [k for k, _ in bullets] if bullets else None
        if s in platform:
            for cid in ("C6", "C7", "C9"):
                add(cid, s, "N/A", PLATFORM_NA)
            graph[s], required[s] = set(), set()
        elif keys != CONTRACT_ORDER:
            add("C6", s, "FAIL", "found %s" % (keys,))
            add("C7", s, "NOT_VERIFIED", "contract unparsable (see C6)")
            add("C9", s, "NOT_VERIFIED", "contract unparsable (see C6)")
            graph[s], required[s] = set(), set()
        else:
            add("C6", s, "PASS")
            d = dict(bullets)
            tick = lambda x: set(re.findall(r"`([^`]+)`", x))  # noqa: E731
            req, opt = tick(d["Required capabilities"]), tick(d["Optional dependencies"])
            # A backticked token is a skill name when it is installed or hyphenated.
            # An uninstalled single word (`pdf`, `python3`) may be a skill or a tool.
            is_skill = lambda x: x in names or bool(KEBAB.match(x))  # noqa: E731
            req_sk = {x for x in req if is_skill(x)}
            opt_sk = {x for x in opt if is_skill(x)}
            ambiguous = sorted(x for x in req - req_sk if WORD.match(x))
            missing = sorted(x for x in req_sk if x not in names)
            if missing:
                add("C7", s, "FAIL", "not installed: %s" % missing)
            elif ambiguous:
                add("C7", s, "NOT_VERIFIED", "single-word names not installed (skill or tool?): %s" % ambiguous)
            else:
                add("C7", s, "PASS")
            graph[s] = (req_sk | opt_sk)
            required[s] = req_sk
            if s == root_skill:
                spec = {x for x in tick(d["Compatible specialist workflows"]) if x in names}
                refs = sorted((req_sk | opt_sk | spec) & set(names))
                add("C9", s, "FAIL" if refs else "PASS", "root references %s" % refs if refs else "")
            elif root_skill not in req_sk:
                add("C9", s, "FAIL", "does not list %s under Required capabilities" % root_skill)
            else:
                add("C9", s, "PASS")

        if s in platform:
            add("C10", s, "N/A", PLATFORM_NA)
        elif s != root_skill:
            used = sorted({m.group(0) for m in LABEL_RE.finditer(t)})
            if not used:
                add("C10", s, "PASS", "no domain label named")
            elif "EGW section 2" in t or "VGHS section 2" in t:
                add("C10", s, "PASS", "labels named: %s" % ", ".join(used))
            else:
                add("C10", s, "NOT_VERIFIED",
                    "names %s without citing 'EGW section 2' (uses vs mentions is a judgment)" % ", ".join(used))
        else:
            add("C10", s, "N/A", "root skill: check applies to dependents only")

        bad = []
        for dirpath, _dirs, files in os.walk(os.path.join(skills_dir, s, "references")):
            for f in files:
                try:
                    body = read(os.path.join(dirpath, f))
                except (UnicodeDecodeError, OSError):
                    continue  # binary or unreadable: not a text file
                if re.search(r"references/[\w.-]+", body):
                    bad.append(f)
        if s in platform:
            add("C12", s, "N/A", PLATFORM_NA)
        else:
            add("C12", s, "FAIL" if bad else "PASS", ", ".join(bad))

        bad = []
        path_re = r"(?<![\w/.-])(?:([a-z0-9-]+)/)?(references|scripts)/([\w.-]+\.[A-Za-z0-9]+)"
        sources = [t]
        for dp, _d, fs in os.walk(os.path.join(skills_dir, s, "references")):
            for f in sorted(fs):
                try:
                    sources.append(read(os.path.join(dp, f)))
                except (UnicodeDecodeError, OSError):
                    continue
        found = set()
        for body in sources:
            found.update(re.findall(path_re, body))
        for owner, folder, fname in found:
            owner = owner or s
            if not os.path.isfile(os.path.join(skills_dir, owner, folder, fname)):
                bad.append("%s/%s/%s" % (owner, folder, fname))
        add("C13", s, "FAIL" if bad else "PASS", "missing: %s" % sorted(bad) if bad else "")

        bad = []
        own = headings(t)
        for spec in re.findall(r"(?:EGW|VGHS) sections? " + SEC, t):
            bad += ["cited %d" % n for n in sorted(section_numbers(spec)) if n not in root_headings]
        for spec in re.findall(r"(?<!VGHS )(?<!EGW )\b[Ss]ections? " + SEC, t):
            bad += ["own %d" % n for n in sorted(section_numbers(spec)) if n not in own]
        for dp, _d, fs in os.walk(os.path.join(skills_dir, s, "references")):
            for f in sorted(fs):
                try:
                    body = read(os.path.join(dp, f))
                except (UnicodeDecodeError, OSError):
                    continue
                for spec in re.findall(r"(?:EGW|VGHS) sections? " + SEC, body):
                    bad += ["cited %d (%s)" % (n, f) for n in sorted(section_numbers(spec)) if n not in root_headings]
                for spec in re.findall(r"(?<!VGHS )(?<!EGW )\b[Ss]ections? " + SEC, body):
                    bad += ["own %d (%s)" % (n, f) for n in sorted(section_numbers(spec)) if n not in own]
        if s in platform:
            add("C14", s, "N/A", PLATFORM_NA)
        else:
            add("C14", s, "FAIL" if bad else "PASS", "dangling: %s" % sorted(set(bad)) if bad else "")

    cyc = find_cycle({k: v for k, v in graph.items() if k not in platform})
    add("C8", "(graph)", "FAIL" if cyc else "PASS", "cycle: %s" % " -> ".join(cyc) if cyc else "")

    if expect_digest is not None:
        digest, _files, findings = dir_digest.compute(os.path.join(skills_dir, root_skill))
        if digest is None:
            add("C16", root_skill, "NOT_VERIFIED", "no valid digest: %s" % findings[:2])
        else:
            ok = digest.startswith(expect_digest.lower())
            add("C16", root_skill, "PASS" if ok else "FAIL", "actual %s" % digest[:16])
    else:
        add("C16", root_skill, "N/A", "not requested (no --expect-root-digest)")
    return names, results


def main(argv):
    args, root, expect, platform, i = [], None, None, set(), 1
    while i < len(argv):
        if argv[i] == "--root-skill" and i + 1 < len(argv):
            root, i = argv[i + 1], i + 2
        elif argv[i] == "--expect-root-digest" and i + 1 < len(argv):
            expect, i = argv[i + 1], i + 2
        elif argv[i] == "--platform-skill" and i + 1 < len(argv):
            platform.update(x.strip() for x in argv[i + 1].split(",") if x.strip())
            i += 2
        elif argv[i].startswith("--"):
            sys.stderr.write(__doc__)
            return 3
        else:
            args.append(argv[i])
            i += 1
    if len(args) != 1 or not os.path.isdir(args[0]):
        sys.stderr.write(__doc__)
        return 3
    if root is None:
        cand = sorted(d for d in os.listdir(args[0]) if os.path.isfile(os.path.join(args[0], d, "SKILL.md")))
        root = "evidence-gated-work" if "evidence-gated-work" in cand else (cand[0] if len(cand) == 1 else None)
        if root is None:
            sys.stderr.write("--root-skill is required when several skills are installed\n")
            return 3
    if expect is not None and not re.fullmatch(r"[0-9a-fA-F]{16}|[0-9a-fA-F]{64}", expect):
        sys.stderr.write("--expect-root-digest needs 16 or 64 hex digits\n")
        return 3
    installed = {d for d in os.listdir(args[0]) if os.path.isfile(os.path.join(args[0], d, "SKILL.md"))}
    if root in platform:
        sys.stderr.write("--platform-skill cannot name the root skill %s\n" % root)
        return 3
    unknown = sorted(platform - installed)
    if unknown:
        sys.stderr.write("--platform-skill names skills not installed in %s: %s\n" % (args[0], unknown))
        return 3
    try:
        names, results = run(args[0], root, expect, frozenset(platform))
    except Exception as err:  # exit 1 means FAIL; a crash is no result at all
        sys.stderr.write("INTERNAL ERROR, no result: %s: %s\n" % (type(err).__name__, err))
        return 5
    for cid, skill, res, detail in sorted(results, key=lambda r: (int(r[0][1:]), r[1])):
        print("%-4s %-34s %-12s %s" % (cid, skill, res, detail))
    counts = {k: sum(1 for r in results if r[2] == k) for k in ("PASS", "FAIL", "NOT_VERIFIED", "N/A")}
    print("skills=%d checks=%d PASS=%d FAIL=%d NOT_VERIFIED=%d N/A=%d" % (
        len(names), len(results), counts["PASS"], counts["FAIL"], counts["NOT_VERIFIED"], counts["N/A"]))
    print("checked_at=%s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return 1 if counts["FAIL"] else (4 if counts["NOT_VERIFIED"] else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
