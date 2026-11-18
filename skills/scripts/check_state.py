#!/usr/bin/env python3
"""Check the durable state and the newest report set of an Evidence-Gated Work repository.

Usage: python3 -I -B scripts/check_state.py [ROOT] [--ref REF] [--digest-script PATH] [--legacy ID,ID]
  ROOT            repository root (default: current directory)
  --ref REF       use the report set of this reference code (default: the newest timestamp)
  --digest-script a dir_digest.py, to recompute manifest digests
                  (default: the dir_digest.py next to this script)
  --legacy IDS    comma-separated IDs from older sets that text may still mention (for example BN-04)

Reads files only (standard library, Python 3.8+); runs dir_digest.py as a script, never imports it.
Closed result labels: PASS | FAIL | NOT_VERIFIED | N/A (N/A carries a reason). No check is omitted.
Exit codes: 0 all PASS or N/A, 1 any FAIL, 4 none FAIL but some NOT_VERIFIED, 3 usage error, 5 internal error.
Last line: checked_at=<UTC>. It checks structure and cross-references, not whether a claim's
wording is true: semantic fit between a claim and its evidence stays a human judgment (INFERRED).

S1  newest plan, knowledge graph and handover share reference code and timestamp; handover.md equals the handover
S2  the six state files and state/evidence/ exist
S3  every evidence record: 12 fields in order, closed sets, claim_id = file name, no bare status,
    OBSERVED needs a recorded method and observation, INFERRED is never VALID, checked_at is ISO UTC or `not recorded`
S4  every evidence, bottleneck and claim ID cited in the report set and state files resolves
S5  record dependencies: claim: links resolve with a validity@date digest, other digests hold a hex digest,
    and a VALID record never depends on a claim that is no longer VALID (staleness propagation)
S6  every VALID claim in the knowledge graph is grounded only in existing VALID records; "BN-nn open/closed" matches the register
S7  Mermaid DAG: nodes declared, acyclic, none isolated, every grounding ID reaches its claim
S8  bottleneck register: 7 fields, state OPEN or CLOSED(evidence ID); handover section 4 agrees with it
S9  state/knowledge-graph.md: same reference and timestamp, Open list equals the OPEN set, Final equals the handover,
    claim validity words equal the graph
S10 handover manifest: each listed repository path recomputes to its recorded 64-hex dir-digest-v1
S11 Final DONE only with no OPEN bottleneck and no claim other than VALID
S12 every file or directory a VALID record depends on is recomputed (sha256, dir-digest-v1) and must equal the recorded digest;
    a missing path or a changed digest FAILS, a path outside the workspace or behind a link is NOT_VERIFIED
S13 handover has the headings 1 to 7 in order and exactly one **Final line; plan, graph and handover titles carry the reference and timestamp
"""
import glob
import hashlib
import os
import re
import stat
import subprocess
import sys
import time

VALIDITY = ("VALID", "STALE", "FAILED", "NOT_VERIFIED")
BASIS = ("OBSERVED", "CITED", "INFERRED")
KEYS = ["claim_id", "claim", "basis", "spec_evidence", "impl_evidence", "method", "observed",
        "artifact_revision", "runtime", "dependencies", "validity", "checked_at"]
EV_ID = r"(?:E\d-\d{2}|[OS]-\d{4})"
EV_RE = re.compile(r"\b" + EV_ID + r"\b")
BN_RE = re.compile(r"\bBN-\d+\b")
C_RE = re.compile(r"\bC-\d+\b")
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
CHECK_IDS = ["S%d" % i for i in range(1, 14)]
MOUNT_POINT_TAG = 0xA0000003  # IO_REPARSE_TAG_MOUNT_POINT: a Windows junction
STATE_FILES = ["objective.md", "baseline.md", "work-packages.md", "bottlenecks.md", "next-task.md", "knowledge-graph.md"]


def rd(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


class Run(object):
    def __init__(self):
        self.res = []

    def add(self, cid, res, detail=""):
        self.res.append((cid, res, detail))

    def skip_rest(self, start, reason):
        done = {c for c, _, _ in self.res}
        for cid in CHECK_IDS:
            if int(cid[1:]) >= start and cid not in done:
                self.add(cid, "NOT_VERIFIED", "not run: " + reason)


def newest_set(root, ref):
    sets = []
    for p in glob.glob(os.path.join(root, "plan_*_*.md")):
        m = re.match(r"^plan_(.+)_(\d{8}_\d{6})\.md$", os.path.basename(p))
        if m and (ref is None or m.group(1) == ref):
            sets.append((m.group(2), m.group(1)))
    return max(sets) if sets else None


def parse_record(text):
    m = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not m:
        return None
    body = m.group(1)
    keys = re.findall(r"^([a-z_]+):", body, re.M)
    rec = {"_keys": keys, "_deps": []}
    for k in KEYS:
        mm = re.search(r"^" + k + r":[ \t]*(.*)$", body, re.M)
        rec[k] = mm.group(1).strip() if mm else None
    for p, d in re.findall(r'^\s+- path: "(.*?)"\n\s+digest: "(.*?)"', body, re.M):
        rec["_deps"].append((p, d))
    return rec


def first_word(v):
    return (v or "").split()[0] if (v or "").split() else ""


def strip_q(v):
    v = (v or "").strip()
    return v[1:-1] if len(v) >= 2 and v[0] == '"' and v[-1] == '"' else v


def run_digest(script, path):
    r = subprocess.run([sys.executable, "-I", "-B", script, path], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def resolve_dependency(root, rel):
    """Return (full path, None) for a dependency path inside the workspace, or (None, reason) when it cannot be recomputed."""
    if os.path.isabs(rel) or re.match(r"^[A-Za-z]:", rel):
        return None, "is an absolute path"
    parts = [x for x in rel.replace("\\", "/").split("/") if x not in ("", ".")]
    if ".." in parts:
        return None, "leaves the workspace"
    cur = root
    for part in parts:
        cur = os.path.join(cur, part)
        try:
            st = os.lstat(cur)
        except OSError:
            return cur, None  # missing: the caller decides
        if stat.S_ISLNK(st.st_mode) or getattr(st, "st_reparse_tag", 0) == MOUNT_POINT_TAG:
            return None, "crosses a link or junction"
    return cur, None


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check(root, ref, digest_script, legacy):
    R = Run()
    found = newest_set(root, ref)
    if not found:
        R.add("S1", "FAIL", "no plan_<ref>_<ts>.md found")
        R.skip_rest(2, "S1 failed")
        return R
    ts, rc = found
    names = {"plan": "plan_%s_%s.md" % (rc, ts), "kg": "knowledge-graph_%s_%s.md" % (rc, ts),
             "ho": "handover_%s_%s.md" % (rc, ts)}
    miss = [n for n in names.values() if not os.path.isfile(os.path.join(root, n))]
    if not os.path.isfile(os.path.join(root, "handover.md")):
        miss.append("handover.md")
    if miss:
        R.add("S1", "FAIL", "missing: " + ", ".join(miss))
        R.skip_rest(2, "S1 failed")
        return R
    ho = rd(os.path.join(root, names["ho"]))
    kg = rd(os.path.join(root, names["kg"]))
    plan_text = rd(os.path.join(root, names["plan"]))
    if rd(os.path.join(root, "handover.md")) != ho:
        R.add("S1", "FAIL", "handover.md differs from " + names["ho"])
    else:
        R.add("S1", "PASS", "%s %s" % (rc, ts))

    sdir = os.path.join(root, "state")
    miss = [f for f in STATE_FILES if not os.path.isfile(os.path.join(sdir, f))]
    evdir = os.path.join(sdir, "evidence")
    if not os.path.isdir(evdir):
        miss.append("evidence/")
    R.add("S2", "FAIL" if miss else "PASS", "missing: " + ", ".join(miss) if miss else "")
    if miss:
        R.skip_rest(3, "S2 failed")
        return R

    # S3 evidence records
    recs, bad = {}, []
    for p in sorted(glob.glob(os.path.join(evdir, "*.md"))):
        fid = os.path.basename(p)[:-3]
        rec = parse_record(rd(p))
        if rec is None:
            bad.append("%s: no yaml block" % fid)
            continue
        recs[fid] = rec
        if rec["_keys"] != KEYS:
            bad.append("%s: fields/order %s" % (fid, [k for k in rec["_keys"] if k not in KEYS] or "order"))
            continue
        if strip_q(rec["claim_id"]) != fid and rec["claim_id"] != fid:
            bad.append("%s: claim_id %s" % (fid, rec["claim_id"]))
        v, b = first_word(rec["validity"]), first_word(rec["basis"])
        if v not in VALIDITY:
            bad.append("%s: validity %r" % (fid, v))
        if b not in BASIS:
            bad.append("%s: basis %r" % (fid, b))
        if b == "INFERRED" and v == "VALID":
            bad.append("%s: INFERRED cannot be VALID" % fid)
        if b == "OBSERVED":
            for k in ("method", "observed"):
                if not strip_q(rec[k]) or strip_q(rec[k]).startswith("not recorded"):
                    bad.append("%s: OBSERVED with %s not recorded" % (fid, k))
        for k in ("claim", "spec_evidence", "impl_evidence", "artifact_revision", "runtime"):
            if not strip_q(rec[k]):
                bad.append("%s: empty %s" % (fid, k))
        ca = strip_q(rec["checked_at"])
        if not (ISO.match(ca) or ca.startswith("not recorded")):
            bad.append("%s: checked_at %r" % (fid, ca))
    R.add("S3", "FAIL" if bad else ("PASS" if recs else "FAIL"),
          "; ".join(bad[:8]) if bad else ("%d records" % len(recs) if recs else "no records"))

    # S4 ID resolution
    reg = rd(os.path.join(sdir, "bottlenecks.md"))
    bn_rows = {}
    for line in reg.splitlines():
        m = re.match(r"^\|\s*(BN-\d+)\s*\|", line)
        if m:
            bn_rows[m.group(1)] = cells(line)
    claims = {}
    for line in kg.splitlines():
        m = re.match(r"^\|\s*(C-\d+)\s", line)
        if m:
            claims[m.group(1)] = cells(line)
    texts = [(names["plan"], rd(os.path.join(root, names["plan"]))), (names["kg"], kg), (names["ho"], ho)]
    for p in sorted(glob.glob(os.path.join(sdir, "*.md"))):
        texts.append(("state/" + os.path.basename(p), rd(p)))
    bad = []
    for n, t in texts:
        for i in sorted(set(EV_RE.findall(t))):
            if i not in recs and i not in legacy:
                bad.append("%s: evidence %s" % (n, i))
        for i in sorted(set(BN_RE.findall(t))):
            if i not in bn_rows and i not in legacy:
                bad.append("%s: bottleneck %s" % (n, i))
        for i in sorted(set(C_RE.findall(t))):
            if i not in claims and i not in legacy:
                bad.append("%s: claim %s" % (n, i))
    R.add("S4", "FAIL" if bad else "PASS", "unresolved: " + "; ".join(bad[:8]) if bad else "")

    # S5 dependencies and propagation
    bad = []
    for fid, rec in recs.items():
        for p, d in rec["_deps"]:
            if p.startswith("claim:"):
                tgt = p[6:]
                if tgt not in recs:
                    bad.append("%s: dependency %s missing" % (fid, tgt))
                    continue
                if not re.match(r"^(VALID|STALE|FAILED|NOT_VERIFIED)@\S", d):
                    bad.append("%s: digest %r for %s" % (fid, d, tgt))
                if first_word(rec["validity"]) == "VALID" and first_word(recs[tgt]["validity"]) != "VALID":
                    bad.append("%s VALID but %s is %s" % (fid, tgt, first_word(recs[tgt]["validity"])))
            elif not re.search(r"[0-9a-f]{16,64}", d):
                bad.append("%s: digest of %s is not a hash (%r)" % (fid, p, d[:30]))
    R.add("S5", "FAIL" if bad else "PASS", "; ".join(bad[:8]))

    # S6 claims
    bad = []
    for cid, c in claims.items():
        if len(c) < 5:
            bad.append("%s: %d columns" % (cid, len(c)))
            continue
        v = first_word(c[2])
        if v not in VALIDITY:
            bad.append("%s: validity %r" % (cid, v))
        if v == "VALID":
            ids = EV_RE.findall(c[3])
            if not ids:
                bad.append("%s: VALID without grounding" % cid)
            for i in ids:
                if i not in recs:
                    bad.append("%s: %s missing" % (cid, i))
                elif first_word(recs[i]["validity"]) != "VALID":
                    bad.append("%s VALID but %s is %s" % (cid, i, first_word(recs[i]["validity"])))
        for bn, word in re.findall(r"\b(BN-\d+)\s+(open|closed)\b", c[4], re.I):
            st = first_word(bn_rows.get(bn, ["", "", "", "", "", "", ""])[6]) if bn in bn_rows else ""
            if st.lower() != word.lower():
                bad.append("%s says %s %s, register says %s" % (cid, bn, word, st or "absent"))
    R.add("S6", "FAIL" if bad else ("PASS" if claims else "FAIL"), "; ".join(bad[:8]) if bad or claims else "no claims table")

    # S7 mermaid
    m = re.search(r"```mermaid\n(.*?)```", kg, re.S)
    if not m:
        R.add("S7", "FAIL", "no mermaid block")
    else:
        mm = m.group(1)
        decl = {}
        for nid, label in re.findall(r'^\s+(\w+)\["(.*?)"\]', mm, re.M):
            decl[nid] = label
        # an edge may carry a label: A -->|text| B  or  A -- text --> B
        edges = re.findall(r"^\s+(\w+)\s+(?:-->(?:\|[^|\n]*\|)?|--\s[^\n]*?\s-->)\s*(\w+)", mm, re.M)
        bad = []
        for a, b in edges:
            for n in (a, b):
                if n not in decl:
                    bad.append("undeclared " + n)
        g = {}
        for a, b in edges:
            g.setdefault(a, set()).add(b)
        state = {}

        def dfs(n):
            state[n] = 1
            for x in g.get(n, ()):
                if state.get(x) == 1 or (x not in state and dfs(x)):
                    return True
            state[n] = 2
            return False
        if any(dfs(n) for n in list(g) if n not in state):
            bad.append("cycle")
        used = {n for e in edges for n in e}
        for n in decl:
            if n not in used:
                bad.append("isolated " + n)
        by_id = {}
        for nid, label in decl.items():
            mt = re.match(r"^(" + EV_ID + r"|BN-\d+|C-\d+)\b", label)
            if mt:
                by_id[mt.group(1)] = nid

        def reach(a, b):
            seen, st = set(), [a]
            while st:
                x = st.pop()
                if x == b:
                    return True
                if x not in seen:
                    seen.add(x)
                    st.extend(g.get(x, ()))
            return False
        for cid, c in claims.items():
            if cid not in by_id or len(c) < 4:
                bad.append("claim %s not drawn" % cid)
                continue
            if first_word(c[2]) == "FAILED":
                continue
            for i in EV_RE.findall(c[3]):
                if i not in by_id:
                    bad.append("%s: %s not drawn" % (cid, i))
                elif not reach(by_id[i], by_id[cid]):
                    bad.append("no path %s -> %s" % (i, cid))
        R.add("S7", "FAIL" if bad else "PASS", "; ".join(bad[:8]) if bad else "%d nodes, %d edges" % (len(decl), len(edges)))

    # S8 register vs handover
    bad = []
    for bn, c in bn_rows.items():
        if len(c) != 7:
            bad.append("%s: %d fields" % (bn, len(c)))
            continue
        st = c[6]
        if not re.match(r"^(OPEN|CLOSED)\b", st):
            bad.append("%s: state %r" % (bn, st[:20]))
        elif st.startswith("CLOSED"):
            ids = EV_RE.findall(st)
            if not ids:
                bad.append("%s: CLOSED without evidence ID" % bn)
            for i in ids:
                if i not in recs:
                    bad.append("%s: closing evidence %s missing" % (bn, i))
    sec4 = re.search(r"## 4\..*?(?=\n## 5\.)", ho, re.S)
    if sec4:
        for line in sec4.group(0).splitlines():
            mt = re.match(r"^\|\s*(BN-\d+)\s*\|", line)
            if mt and mt.group(1) in bn_rows and len(bn_rows[mt.group(1)]) == 7:
                a, b = first_word(cells(line)[-1]), first_word(bn_rows[mt.group(1)][6])
                if a != b:
                    bad.append("%s handover %s vs register %s" % (mt.group(1), a, b))
    R.add("S8", "FAIL" if bad or not bn_rows else "PASS", "; ".join(bad[:8]) if bad or bn_rows else "empty register")

    # S9 pointer
    pt = rd(os.path.join(sdir, "knowledge-graph.md"))
    bad = []
    mt = re.search(r"Reference (\S+), timestamp (\S+?)\.?\s", pt + " ")
    if not mt or (mt.group(1), mt.group(2)) != (rc, ts):
        bad.append("reference/timestamp %s vs %s %s" % (mt.groups() if mt else None, rc, ts))
    mo = re.search(r"^Open: (.*?)\. Final:", pt, re.M)
    open_set = sorted(b for b, c in bn_rows.items() if len(c) == 7 and c[6].startswith("OPEN"))
    if not mo or sorted(BN_RE.findall(mo.group(1))) != open_set:
        bad.append("Open list %s vs register %s" % (sorted(BN_RE.findall(mo.group(1))) if mo else None, open_set))
    fin_h = re.search(r"\*\*Final: (DONE|PARTIAL|BLOCKED)", ho)
    fin_p = re.search(r"Final: (DONE|PARTIAL|BLOCKED)", pt)
    if not fin_h or not fin_p or fin_h.group(1) != fin_p.group(1):
        bad.append("Final %s vs handover %s" % (fin_p.group(1) if fin_p else None, fin_h.group(1) if fin_h else None))
    for cid, tail in re.findall(r"(C-\d+)((?:(?!C-\d)[^.;\n]){0,60}?\b(?:VALID|STALE|FAILED|NOT_VERIFIED)\b)", pt):
        word = re.findall(r"\b(VALID|STALE|FAILED|NOT_VERIFIED)\b", tail)[-1]
        if cid in claims and len(claims[cid]) > 2 and first_word(claims[cid][2]) != word:
            bad.append("pointer says %s %s, graph says %s" % (cid, word, first_word(claims[cid][2])))
    R.add("S9", "FAIL" if bad else "PASS", "; ".join(bad[:8]))

    # S10 manifest
    sec7 = re.search(r"## 7\..*", ho, re.S)
    rows = []
    if sec7:
        for line in sec7.group(0).splitlines():
            c = cells(line)
            if len(c) >= 2:
                mh = re.search(r"`([0-9a-f]{64})`", c[1])
                if mh and os.path.isdir(os.path.join(root, c[0].rstrip("/"))):
                    rows.append((c[0].rstrip("/"), mh.group(1)))
    if not rows:
        R.add("S10", "N/A", "no manifest row names a repository directory with a 64-hex digest")
    elif not (digest_script and os.path.isfile(digest_script)):
        R.add("S10", "NOT_VERIFIED", "no dir_digest.py available")
    else:
        bad = []
        for path, hx in rows:
            rcode, d = run_digest(digest_script, os.path.join(root, path))
            if rcode != 0 or d != hx:
                bad.append("%s recorded %s now %s" % (path, hx[:16], d[:16] if rcode == 0 else "exit %d" % rcode))
        R.add("S10", "FAIL" if bad else "PASS", "; ".join(bad) if bad else "%d paths" % len(rows))

    # S11 final
    if fin_h and fin_h.group(1) == "DONE":
        bad = [b for b in open_set]
        bad += [c for c, v in claims.items() if len(v) > 2 and first_word(v[2]) != "VALID"]
        R.add("S11", "FAIL" if bad else "PASS", "DONE with: " + ", ".join(bad) if bad else "")
    else:
        R.add("S11", "N/A", "Final is %s, not DONE" % (fin_h.group(1) if fin_h else "unknown"))

    # S12 file and directory dependencies of VALID records, recomputed
    bad, nv, done, no_dep = [], [], 0, 0
    for fid, rec in sorted(recs.items()):
        if first_word(rec["validity"]) != "VALID":
            continue
        if first_word(rec["basis"]) == "OBSERVED" and not rec["_deps"]:
            no_dep += 1
        for p, d in rec["_deps"]:
            if p.startswith("claim:"):
                continue
            full, why = resolve_dependency(root, p)
            if full is None:
                nv.append("%s: %s %s, not recomputed" % (fid, p, why))
                continue
            if not os.path.exists(full):
                bad.append("%s: %s is missing" % (fid, p))
                continue
            m = re.search(r"[0-9a-f]{16,64}", d)
            if not m:
                continue  # S5 reports a digest that is not a hash
            if os.path.isdir(full):
                if not (digest_script and os.path.isfile(digest_script)):
                    nv.append("%s: %s needs dir_digest.py" % (fid, p))
                    continue
                code, now = run_digest(digest_script, full)
                if code != 0:
                    nv.append("%s: %s has no valid dir-digest-v1 (exit %d)" % (fid, p, code))
                    continue
            else:
                now = sha256_of(full)
            done += 1
            if not now.startswith(m.group(0)):
                bad.append("%s: %s recorded %s now %s" % (fid, p, m.group(0)[:16], now[:16]))
    info = "%d dependencies recomputed; %d VALID OBSERVED records list no dependency" % (done, no_dep)
    if bad:
        R.add("S12", "FAIL", "; ".join(bad[:8]))
    elif nv:
        R.add("S12", "NOT_VERIFIED", "; ".join(nv[:8]))
    else:
        R.add("S12", "PASS", info)

    # S13 structure of the report set
    bad = []
    nums = [int(n) for n in re.findall(r"^## (\d+)\.", ho, re.M)]
    if nums != list(range(1, 8)):
        bad.append("handover headings %s, expected 1 to 7 in order" % nums)
    n_final = len(re.findall(r"\*\*Final: (?:DONE|PARTIAL|BLOCKED)", ho))
    if n_final != 1:
        bad.append("%d **Final lines in the handover, expected 1" % n_final)
    for what, text, head in (("plan", plan_text, "Plan"), ("graph", kg, "Knowledge graph"), ("handover", ho, "Handover")):
        first = text.split("\n", 1)[0].rstrip("\r")
        want = "# %s %s | %s" % (head, rc, ts)
        if first != want:
            bad.append("%s title %r, expected %r" % (what, first[:60], want))
    R.add("S13", "FAIL" if bad else "PASS", "; ".join(bad[:8]))
    return R


def usage(why):
    sys.stderr.write("usage error: %s\n%s" % (why, __doc__))
    return 3


def main(argv):
    args = argv[1:]
    root, ref, dscript, legacy, root_set = ".", None, None, set(), False
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--ref", "--digest-script", "--legacy"):
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                return usage("%s needs a value" % a)
            v = args[i + 1]
            if a == "--ref":
                ref = v
            elif a == "--digest-script":
                dscript = v
            else:
                legacy = set(x for x in v.split(",") if x)
            i += 2
        elif a.startswith("--"):
            return usage("unknown flag %s" % a)
        else:
            if root_set:
                return usage("more than one ROOT")
            root, root_set = a, True
            i += 1
    if dscript is None:
        dscript = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dir_digest.py")
    R = check(root, ref, dscript, legacy)
    for cid, res, detail in R.res:
        print("%-4s %-13s %s" % (cid, res, detail))
    n = lambda x: sum(1 for _, r, _ in R.res if r == x)
    print("checks=%d PASS=%d FAIL=%d NOT_VERIFIED=%d N/A=%d" % (len(R.res), n("PASS"), n("FAIL"), n("NOT_VERIFIED"), n("N/A")))
    print("checked_at=" + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    return 1 if n("FAIL") else (4 if n("NOT_VERIFIED") else 0)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as exc:
        print("internal error: %r" % (exc,))
        sys.exit(5)
