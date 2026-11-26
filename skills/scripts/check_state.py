#!/usr/bin/env python3
"""Check the durable state and the newest report set of an Evidence-Gated Work repository.

Usage: python3 -I -B scripts/check_state.py [ROOT] [--ref REF] [--digest-script PATH] [--legacy ID,ID] [--strict-from ID] [--json]
  ROOT            repository root (default: current directory)
  --ref REF       use the report set of this reference code (default: the newest timestamp)
  --digest-script a dir_digest.py, to recompute manifest digests
                  (default: the dir_digest.py next to this script)
  --legacy IDS    comma-separated IDs from older sets that text may still mention (for example BN-04)
  --strict-from   a record ID (for example O-1001): the stricter record rules of S3 and S12 (CITED sources, block scalars,
                  files named in impl_evidence, git revisions) apply to records numbered from that ID on; default: all records
  --json          print one JSON object instead of the text lines (schema_version 1: checks with id, result, detail, fix)

Reads files only (standard library, Python 3.8+); runs dir_digest.py as a script, never imports it; asks git only whether a
commit exists (git cat-file -e), when a record names one.
Closed result labels: PASS | FAIL | NOT_VERIFIED | N/A (N/A carries a reason). No check is omitted.
Exit codes: 0 all PASS or N/A, 1 any FAIL, 4 none FAIL but some NOT_VERIFIED, 3 usage error, 5 internal error.
Last line: checked_at=<UTC>. It checks structure and cross-references, not whether a claim's
wording is true: semantic fit between a claim and its evidence stays a human judgment (INFERRED).

S1  newest plan, knowledge graph and handover share reference code and timestamp; handover.md equals the handover
S2  the six state files and state/evidence/ exist
S3  every evidence record: 12 fields in order, closed sets, claim_id = file name, no bare status, OBSERVED needs a recorded
    method and observation, INFERRED is never VALID, checked_at is ISO UTC (not in the future) or "not recorded";
    a VALID CITED record names a URL or path and a recorded method; a block scalar is NOT_VERIFIED
S4  every evidence, bottleneck and claim ID cited in the report set and state files resolves
S5  record dependencies: claim: links resolve with a validity@date digest, other digests hold a hex digest (the words
    "not recorded" are NOT_VERIFIED: nothing could compute it), and a VALID record never depends on a claim that is no
    longer VALID (staleness propagation)
S6  every VALID claim in the knowledge graph is grounded only in existing VALID records; "BN-nn open/closed" matches the register
S7  Mermaid DAG: nodes declared, acyclic, none isolated, every grounding ID reaches its claim and every claim reaches Final
S8  bottleneck register: 7 fields, state OPEN or CLOSED(evidence ID); handover section 4 agrees with it
S9  state/knowledge-graph.md: same reference and timestamp, Open list equals the OPEN set, Final equals the handover,
    claim validity words equal the graph
S10 handover manifest: each listed repository path recomputes to its recorded 64-hex dir-digest-v1
S11 Final DONE only with no OPEN bottleneck that has a REQUIRED dependent, and no claim other than VALID unless it depends on
    an open OPTIONAL bottleneck
S12 every file or directory a VALID record depends on is recomputed (sha256, dir-digest-v1) and must equal the recorded digest;
    a missing path or a changed digest FAILS, a path outside the workspace or behind a link is NOT_VERIFIED; a file named in
    impl_evidence but not listed, and a git revision that cannot be checked, are NOT_VERIFIED; a git revision that does not exist FAILS
S13 handover has the headings 1 to 7 in order and exactly one **Final line; plan, graph and handover titles carry the reference and timestamp
S14 register (v2): an OPEN row has a REQUIRED or OPTIONAL class with a resolvable ID, "OPEN (since REF; owner: X)", no empty field,
    and appears unchanged in handover section 4; a CLOSED row cites no FAILED record and at least one VALID record or a decision
    (or says historical); next-task names open bottlenecks only; state/decisions.md is well formed; an OPEN row older than three
    report sets has an escalation row in handover section 5
S15 manifest rows: handover section 7 lists state/ and every folder that holds a SKILL.md, each with its 64-hex digest
    (a row that says NOT_VERIFIED, as a session without a shell must write, gives NOT_VERIFIED, not FAIL)
S16 record graph: no cycle among claim: dependencies, and each digest validity@checked_at equals the target's current pair
S17 claims: Basis from the closed set, VALID needs OBSERVED or CITED, no VALID claim depends on a claim that is not VALID or on an
    OPEN bottleneck, claim IDs are unique, the validity in handover section 6 equals the graph
S18 completion: work packages and baseline use the closed sets; Final DONE needs every package with a REQUIRED criterion DONE;
    the plan names scope, a REQUIRED criterion, the bottlenecks and the evidence plan
S19 freshness: a VALID claim grounded in a CITED record without a revision, retrieved before the date of the set, is NOT_VERIFIED
"""
import calendar
import glob
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time

VALIDITY = ("VALID", "STALE", "FAILED", "NOT_VERIFIED")
BASIS = ("OBSERVED", "CITED", "INFERRED")
CAPABILITY = ("EXISTS", "PARTIAL", "MISSING", "CONFLICTING", "NOT_VERIFIED")
LIFECYCLE = ("NOT_STARTED", "ACTIVE", "-")
FINAL = ("DONE", "PARTIAL", "BLOCKED", "-")
KEYS = ["claim_id", "claim", "basis", "spec_evidence", "impl_evidence", "method", "observed",
        "artifact_revision", "runtime", "dependencies", "validity", "checked_at"]
EV_ID = r"(?:E\d-\d{2}|[OS]-\d{4,6})"
EV_RE = re.compile(r"\b" + EV_ID + r"\b")
BN_RE = re.compile(r"\bBN-\d+\b")
C_RE = re.compile(r"\bC-\d+\b")
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
URL_RE = re.compile(r"https?://\S+")
PATH_RE = re.compile(r"(?:[\w.-]+/)+[\w.-]+|[\w-]+\.(?:md|txt|py|json|yml|yaml|csv|pdf|html|toml|cfg|log)\b")
OPEN_RE = re.compile(r"^OPEN \(since ([A-Z][A-Z0-9-]*); owner: (agent|person|external)\)$")
CLOSED_RE = re.compile(r"^CLOSED \(([^)]*)\)$")
CHECK_IDS = ["S%d" % i for i in range(1, 20)]
MOUNT_POINT_TAG = 0xA0000003  # IO_REPARSE_TAG_MOUNT_POINT: a Windows junction
STATE_FILES = ["objective.md", "baseline.md", "work-packages.md", "bottlenecks.md", "next-task.md", "knowledge-graph.md"]
FIX = {
    "S1": "write plan, knowledge graph and handover of one set with the same reference code and timestamp, and copy the newest handover to handover.md",
    "S2": "create the missing state file or state/evidence/ from assets/templates/state/",
    "S3": "rewrite the record from assets/templates/evidence-record.md: 12 keys in order, a recorded method and observation, a URL or path for a CITED record, single-line values",
    "S4": "write the missing record, register row or claims row, or correct the ID",
    "S5": "give each claim: dependency a validity@checked_at digest and each file dependency a hex digest; mark a record STALE when its dependency is not VALID",
    "S6": "ground each VALID claim only in existing VALID records; make BN-nn open or closed equal the register",
    "S7": "declare every node as id[\"label\"], draw edges from evidence to claim and from claim to the Final node, remove cycles and isolated nodes",
    "S8": "give each register row 7 fields and a state OPEN or CLOSED (record ID); copy it unchanged to handover section 4",
    "S9": "make state/knowledge-graph.md name the same reference and timestamp, the open bottlenecks, the Final label and the validity of each claim",
    "S10": "recompute dir-digest-v1 of each listed folder and write it with its clock reading in handover section 7",
    "S11": "do not write DONE while a REQUIRED-dependent bottleneck is open or a claim is not VALID; write PARTIAL or BLOCKED",
    "S12": "re-run the method of the record and store the new digest, or mark the record STALE; list every file the result rests on under dependencies",
    "S13": "use headings ## 1. to ## 7. in order and exactly one **Final: <label>.** line; title each file with its reference and timestamp",
    "S14": "write OPEN (since REF; owner: agent|person|external), a REQUIRED or OPTIONAL class with a WP or claim ID, no empty field; close only with a VALID record or a decision; add an escalation row after three report sets",
    "S15": "list state/ and every folder that holds a SKILL.md in handover section 7 with its 64-hex digest",
    "S16": "break the cycle; copy validity@checked_at of the target record into the dependency digest",
    "S17": "use OBSERVED or CITED for a VALID claim, mark a claim NOT_VERIFIED while a dependency is not VALID or an open bottleneck stands under it, keep claim IDs unique, copy validity to handover section 6",
    "S18": "use the closed sets in work-packages.md and baseline.md; write Final DONE only after every REQUIRED package is DONE; give the plan scope, a REQUIRED criterion, a bottleneck section and an evidence plan",
    "S19": "fetch the source again, write a new S- record dated in this set, and ground the claim in it",
}


def rd(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table_rows(text, skip_header=True):
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        c = cells(line)
        if all(re.match(r"^:?-+:?$", x) for x in c if x):
            continue
        rows.append(c)
    return rows[1:] if skip_header and rows else rows


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


def rec_num(fid):
    m = re.match(r"^[OS]-(\d+)$", fid)
    return int(m.group(1)) if m else 0


def newest_set(root, ref):
    sets = []
    for p in glob.glob(os.path.join(root, "plan_*_*.md")):
        m = re.match(r"^plan_(.+)_(\d{8}_\d{6})\.md$", os.path.basename(p))
        if m and (ref is None or m.group(1) == ref):
            sets.append((m.group(2), m.group(1)))
    return max(sets) if sets else None


def all_sets(root):
    found = set()
    for pat in (os.path.join(root, "plan_*_*.md"), os.path.join(root, "archive", "reports", "plan_*_*.md")):
        for p in glob.glob(pat):
            m = re.match(r"^plan_(.+)_(\d{8}_\d{6})\.md$", os.path.basename(p))
            if m:
                found.add((m.group(2), m.group(1)))
    return sorted(found)


def parse_record(text):
    m = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not m:
        return None
    body = m.group(1)
    keys = re.findall(r"^([a-z_]+):", body, re.M)
    rec = {"_keys": keys, "_deps": [], "_block": []}
    for k in KEYS:
        mm = re.search(r"^" + k + r":[ \t]*(.*)$", body, re.M)
        rec[k] = mm.group(1).strip() if mm else None
        if rec[k] is not None and re.match(r"^[|>][+-]?$", rec[k]):
            rec["_block"].append(k)
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


def impl_paths(text):
    out = []
    for tok in re.split(r"[;,\s]+", text):
        tok = tok.strip("\"'()[]").split("#")[0].rstrip(".:")
        if not tok or tok.startswith("http") or ":" in tok or ("/" not in tok and "." not in tok):
            continue
        out.append(tok)
    return out


ARROW = r"--[ \t][^\n]*?[ \t]-->|(?:-->|-\.->|==>)(?:\|[^|\n]*\|)?"


def parse_mermaid(mm):
    """Return ({id: label}, [(from, to)]); a node may be declared inline and edges may be chained."""
    decl, edges = {}, []
    for line in mm.split("\n"):
        s = line.strip()
        if not s or re.match(r"^(flowchart|graph|%%|subgraph|end\b|classDef|class |style |linkStyle)", s):
            continue

        def d(m):
            decl[m.group(1)] = m.group(2)
            return m.group(1)
        s = re.sub(r'(\w+)\["(.*?)"\]', d, s)
        parts = re.split("(" + ARROW + ")", s)
        nodes = [p.strip() for p in parts[0::2]]
        if len(nodes) < 2:
            continue
        for a, b in zip(nodes, nodes[1:]):
            if re.match(r"^\w+$", a) and re.match(r"^\w+$", b):
                edges.append((a, b))
    return decl, edges


def check(root, ref, digest_script, legacy, strict_from):
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
    recs, bad, nv = {}, [], []
    now = time.time()
    for p in sorted(glob.glob(os.path.join(evdir, "*.md"))):
        fid = os.path.basename(p)[:-3]
        rec = parse_record(rd(p))
        if rec is None:
            bad.append("%s: no yaml block" % fid)
            continue
        recs[fid] = rec
        if not re.match(r"^" + EV_ID + "$", fid):
            bad.append("%s: not a record ID (O- or S- plus 4 to 6 digits)" % fid)
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
        elif ISO.match(ca) and calendar.timegm(time.strptime(ca, "%Y-%m-%dT%H:%M:%SZ")) > now + 300:
            bad.append("%s: checked_at %s is in the future" % (fid, ca))
        if rec_num(fid) >= strict_from:
            if b == "CITED" and v == "VALID":
                spec = strip_q(rec["spec_evidence"])
                if not (URL_RE.search(spec) or PATH_RE.search(spec)):
                    bad.append("%s: CITED without a URL or a path in spec_evidence" % fid)
                for k in ("method", "observed"):
                    if not strip_q(rec[k]) or strip_q(rec[k]).startswith("not recorded"):
                        bad.append("%s: CITED with %s not recorded" % (fid, k))
                if not ISO.match(ca):
                    bad.append("%s: CITED without a clock reading in checked_at" % fid)
            if rec["_block"]:
                nv.append("%s: block scalar in %s (the checker reads single-line values)" % (fid, ",".join(rec["_block"])))
    if bad:
        R.add("S3", "FAIL", "; ".join(bad[:8]))
    elif not recs:
        R.add("S3", "FAIL", "no records")
    elif nv:
        R.add("S3", "NOT_VERIFIED", "; ".join(nv[:6]))
    else:
        R.add("S3", "PASS", "%d records" % len(recs))

    # S4 ID resolution
    reg = rd(os.path.join(sdir, "bottlenecks.md"))
    bn_rows = {}
    for line in reg.splitlines():
        m = re.match(r"^\|\s*(BN-\d+)\s*\|", line)
        if m:
            bn_rows[m.group(1)] = cells(line)
    claims, claim_count = {}, {}
    for line in kg.splitlines():
        m = re.match(r"^\|\s*(C-\d+)\s", line)
        if m:
            claims[m.group(1)] = cells(line)
            claim_count[m.group(1)] = claim_count.get(m.group(1), 0) + 1
    texts = [(names["plan"], plan_text), (names["kg"], kg), (names["ho"], ho)]
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
    bad, nv5 = [], []
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
                if d.strip() == "not recorded":  # no tool could compute it (for example a session without a shell): not recomputable
                    nv5.append("%s: digest of %s is not recorded" % (fid, p))
                else:
                    bad.append("%s: digest of %s is not a hash (%r)" % (fid, p, d[:30]))
    R.add("S5", "FAIL" if bad else ("NOT_VERIFIED" if nv5 else "PASS"), "; ".join((bad or nv5)[:8]))

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
    decl, edges, by_id, graph_ok, final_nodes = {}, [], {}, False, []
    m = re.search(r"```mermaid\n(.*?)```", kg, re.S)
    if not m:
        R.add("S7", "FAIL", "no mermaid block")
    else:
        decl, edges = parse_mermaid(m.group(1))
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
        for nid, label in decl.items():
            mt = re.match(r"^(" + EV_ID + r"|BN-\d+|C-\d+)\b", label)
            if mt:
                by_id[mt.group(1)] = nid
            if label.startswith("Final"):
                final_nodes.append(nid)

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
        if not final_nodes:
            bad.append("no Final node")
        for cid, c in claims.items():
            if cid not in by_id or len(c) < 4:
                bad.append("claim %s not drawn" % cid)
                continue
            if final_nodes and not any(reach(by_id[cid], f) for f in final_nodes):
                bad.append("%s has no path to Final" % cid)
            if first_word(c[2]) == "FAILED":
                continue
            for i in EV_RE.findall(c[3]):
                if i not in by_id:
                    bad.append("%s: %s not drawn" % (cid, i))
                elif not reach(by_id[i], by_id[cid]):
                    bad.append("no path %s -> %s" % (i, cid))
        graph_ok = not bad
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
            if not ids and not re.search(r"\bD\d+\b", st):
                bad.append("%s: CLOSED without evidence ID" % bn)
            for i in ids:
                if i not in recs:
                    bad.append("%s: closing evidence %s missing" % (bn, i))
    sec4 = re.search(r"## 4\..*?(?=\n## 5\.)", ho, re.S)
    ho_rows = {}
    if sec4:
        for line in sec4.group(0).splitlines():
            mt = re.match(r"^\|\s*(BN-\d+)\s*\|", line)
            if mt:
                ho_rows[mt.group(1)] = cells(line)
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
    rows, listed, placeholders = [], set(), set()
    if sec7:
        for line in sec7.group(0).splitlines():
            c = cells(line)
            if len(c) >= 2 and os.path.isdir(os.path.join(root, c[0].rstrip("/"))):
                mh = re.search(r"`([0-9a-f]{64})`", c[1])
                if mh:
                    rows.append((c[0].rstrip("/"), mh.group(1)))
                    listed.add(c[0].rstrip("/"))
                elif re.search(r"<[^>]*digest[^>]*>", c[1]) or re.match(r"\W*NOT_VERIFIED", c[1]):
                    placeholders.add(c[0].rstrip("/"))  # a placeholder, or an honest "not computed" (no shell in that session)
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

    # open bottleneck classes (v2) shared by S11, S14, S18
    open_cls, parse_bad = {}, []
    for b, c in bn_rows.items():
        if len(c) == 7 and c[6].startswith("OPEN"):
            mc = re.match(r"^(REQUIRED|OPTIONAL):", c[2])
            open_cls[b] = mc.group(1) if mc else "?"

    # S11 final
    if fin_h and fin_h.group(1) == "DONE":
        bad = [b for b in open_set if open_cls.get(b) != "OPTIONAL"]
        for c_id, v in claims.items():
            if len(v) > 2 and first_word(v[2]) != "VALID":
                deps = [x for x in BN_RE.findall(re.sub(r"\bsee BN-\d+", "", v[4])) if x in open_cls]
                if first_word(v[2]) == "FAILED" or not deps or any(open_cls[x] != "OPTIONAL" for x in deps):
                    bad.append(c_id)
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
                code, now_d = run_digest(digest_script, full)
                if code != 0:
                    nv.append("%s: %s has no valid dir-digest-v1 (exit %d)" % (fid, p, code))
                    continue
            else:
                now_d = sha256_of(full)
            done += 1
            if not now_d.startswith(m.group(0)):
                bad.append("%s: %s recorded %s now %s" % (fid, p, m.group(0)[:16], now_d[:16]))
        if rec_num(fid) >= strict_from:
            for tok in impl_paths(strip_q(rec["impl_evidence"])):
                full, why = resolve_dependency(root, tok)
                if full is None or not os.path.exists(full):
                    continue
                covered = any(not p.startswith("claim:") and (p.rstrip("/") == tok.rstrip("/") or tok.startswith(p.rstrip("/") + "/") or p in (".", "./"))
                              for p, _d in rec["_deps"])
                if not covered:
                    nv.append("%s: impl_evidence names %s, which is not listed under dependencies" % (fid, tok))
            mg = re.match(r"^git ([0-9a-f]{7,40})\b", strip_q(rec["artifact_revision"]))
            if mg:
                if not os.path.exists(os.path.join(root, ".git")):
                    nv.append("%s: git revision %s cannot be checked (no .git)" % (fid, mg.group(1)))
                else:
                    try:
                        r2 = subprocess.run(["git", "-C", root, "cat-file", "-e", mg.group(1) + "^{commit}"], capture_output=True, text=True)
                        if r2.returncode != 0:
                            bad.append("%s: git revision %s does not exist" % (fid, mg.group(1)))
                    except OSError:
                        nv.append("%s: git revision %s cannot be checked (git not available)" % (fid, mg.group(1)))
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

    # work packages (used by S14, S18)
    wp_rows = {}
    wp_path = os.path.join(sdir, "work-packages.md")
    for c in table_rows(rd(wp_path)):
        wp_rows[c[0]] = c

    # S14 register v2
    bad, nvl = [], []
    sets = all_sets(root)
    sec5 = re.search(r"## 5\..*?(?=\n## 6\.)", ho, re.S)
    sec5_text = sec5.group(0) if sec5 else ""
    dec_ids = set()
    dec_path = os.path.join(sdir, "decisions.md")
    if os.path.isfile(dec_path):
        head = [ln for ln in rd(dec_path).splitlines() if ln.startswith("|")]
        want_head = ["ID", "question", "options", "chosen", "decided by", "date", "evidence or quote", "cost of reversal"]
        if not head or cells(head[0]) != want_head:
            bad.append("decisions.md header is not %s" % " | ".join(want_head))
        for c in table_rows(rd(dec_path)):
            if len(c) != 8 or any(not x for x in c):
                bad.append("decisions.md row %s has empty or missing fields" % (c[0] if c else "?"))
                continue
            if not re.match(r"^D\d+$", c[0]) or c[0] in dec_ids:
                bad.append("decisions.md ID %r is malformed or repeated" % c[0])
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", c[5]):
                bad.append("decisions.md %s: date %r" % (c[0], c[5]))
            dec_ids.add(c[0])
    for bn, c in sorted(bn_rows.items()):
        if len(c) != 7:
            continue
        st = c[6]
        if st.startswith("OPEN"):
            mo2 = OPEN_RE.match(st)
            if not mo2:
                bad.append("%s: state %r is not OPEN (since REF; owner: agent|person|external)" % (bn, st[:40]))
            if any(x in ("", "-") for x in c[1:6]):
                bad.append("%s: an empty field among 2 to 6" % bn)
            if not re.match(r"^(REQUIRED|OPTIONAL):", c[2]):
                bad.append("%s: dependent work does not start with REQUIRED: or OPTIONAL:" % bn)
            else:
                ids = re.findall(r"\b(?:WP-[0-9A-Za-z]+|C-\d+)\b", c[2])
                if not any(i in wp_rows or i in claims for i in ids):
                    bad.append("%s: dependent work names no work package or claim that exists" % bn)
            hr = ho_rows.get(bn)
            if hr is None:
                bad.append("%s: OPEN but missing from handover section 4" % bn)
            elif hr != c:
                bad.append("%s: handover section 4 differs from the register row" % bn)
            if mo2 and sets:
                ref_sets = [i for i, s in enumerate(sets) if s[1] == mo2.group(1)]
                if ref_sets:
                    age = len(sets) - 1 - ref_sets[0]
                    if age >= 3 and not re.search(bn + r".*escalat|escalat.*" + bn, sec5_text, re.I):
                        nvl.append("%s open for %d report sets: no escalation row in handover section 5" % (bn, age))
        elif st.startswith("CLOSED"):
            mc = CLOSED_RE.match(st)
            if not mc:
                bad.append("%s: state %r is not CLOSED (record or decision IDs[; historical])" % (bn, st[:40]))
                continue
            parts = [x.strip() for x in mc.group(1).split(";")]
            hist = "historical" in parts[1:]
            rids = EV_RE.findall(parts[0])
            dids = re.findall(r"\bD\d+\b", parts[0])
            for d in dids:
                if d not in dec_ids:
                    bad.append("%s: closed by decision %s that is not in decisions.md" % (bn, d))
            states = [first_word(recs[i]["validity"]) for i in rids if i in recs]
            if "FAILED" in states:
                bad.append("%s: closed by a FAILED record" % bn)
            elif not hist and not dids and "VALID" not in states:
                nvl.append("%s: every closing record is STALE or NOT_VERIFIED: run its test again or write historical" % bn)
    nt = os.path.join(sdir, "next-task.md")
    for c in table_rows(rd(nt)):
        for b in BN_RE.findall(c[-1]):
            if b not in bn_rows:
                bad.append("next-task names %s, which is not in the register" % b)
            elif b not in open_cls:
                bad.append("next-task names %s, which is not OPEN" % b)
    if bad:
        R.add("S14", "FAIL", "; ".join(bad[:8]))
    elif nvl:
        R.add("S14", "NOT_VERIFIED", "; ".join(nvl[:6]))
    else:
        R.add("S14", "PASS", "%d rows, %d open" % (len(bn_rows), len(open_cls)))

    # S15 manifest rows
    skill_dirs = []
    for dp, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "build", "evals", "archive", "probes", "__pycache__")]
        if "SKILL.md" in files:
            skill_dirs.append(os.path.relpath(dp, root).replace(os.sep, "/"))
    want = ["state"] + sorted(skill_dirs)
    miss = [w for w in want if w not in listed and w not in placeholders]
    unfilled = [w for w in want if w in placeholders]
    if miss:
        R.add("S15", "FAIL", "no manifest row for: " + ", ".join(miss))
    elif unfilled:
        R.add("S15", "NOT_VERIFIED", "the digest of %s is a placeholder or says NOT_VERIFIED" % ", ".join(unfilled))
    else:
        R.add("S15", "PASS", "%d rows" % len(want))

    # S16 record graph
    bad = []
    g2 = {}
    for fid, rec in recs.items():
        g2[fid] = [p[6:] for p, _d in rec["_deps"] if p.startswith("claim:") and p[6:] in recs]
    st2 = {}

    def dfs2(n, path):
        st2[n] = 1
        for x in g2.get(n, ()):
            if st2.get(x) == 1:
                return path + [n, x]
            if x not in st2:
                f = dfs2(x, path + [n])
                if f:
                    return f
        st2[n] = 2
        return None
    for n in sorted(g2):
        if n not in st2:
            cyc = dfs2(n, [])
            if cyc:
                bad.append("cycle " + " -> ".join(cyc))
                break
    for fid, rec in recs.items():
        if first_word(rec["validity"]) != "VALID":
            continue
        for p, d in rec["_deps"]:
            if p.startswith("claim:") and p[6:] in recs:
                t = recs[p[6:]]
                cur = "%s@%s" % (first_word(t["validity"]), strip_q(t["checked_at"]))
                if re.match(r"^(VALID|STALE|FAILED|NOT_VERIFIED)@\S", d) and d != cur:
                    bad.append("%s: dependency %s says %s, the record is %s" % (fid, p[6:], d, cur))
    R.add("S16", "FAIL" if bad else "PASS", "; ".join(bad[:8]))

    # S17 claims
    bad = []
    for cid, n in claim_count.items():
        if n > 1:
            bad.append("%s appears %d times in the claims table" % (cid, n))
    bn_state = {b: ("OPEN" if b in open_cls else "CLOSED") for b in bn_rows}
    for cid, c in claims.items():
        if len(c) < 5:
            continue
        v = first_word(c[2])
        toks = re.findall(r"\b[A-Z]{4,}\b", c[1])
        if any(t not in BASIS for t in toks) or (not toks and c[1].strip().lower() not in ("none", "-")):
            bad.append("%s: Basis %r is outside OBSERVED, CITED, INFERRED" % (cid, c[1][:30]))
        elif v == "VALID" and not any(t in ("OBSERVED", "CITED") for t in toks):
            bad.append("%s: VALID needs a Basis of OBSERVED or CITED" % cid)
        if v == "VALID":
            dep_text = re.sub(r"\bsee (?:BN|C)-\d+", "", c[4])
            for d in C_RE.findall(dep_text):
                if d in claims and first_word(claims[d][2]) != "VALID":
                    bad.append("%s VALID but depends on %s (%s)" % (cid, d, first_word(claims[d][2])))
            for b in BN_RE.findall(dep_text):
                if bn_state.get(b) == "OPEN":
                    bad.append("%s VALID but depends on the open bottleneck %s" % (cid, b))
    if graph_ok or edges:
        inv = {nid: k for k, nid in by_id.items()}
        for a, b in edges:
            ka, kb = inv.get(a), inv.get(b)
            if not ka or not kb or kb not in claims or first_word(claims[kb][2]) != "VALID":
                continue
            if ka.startswith("C-") and ka in claims and first_word(claims[ka][2]) != "VALID":
                bad.append("edge %s -> %s: %s is VALID but %s is %s" % (ka, kb, kb, ka, first_word(claims[ka][2])))
            if ka.startswith("BN-") and bn_state.get(ka) == "OPEN":
                bad.append("edge %s -> %s: %s is VALID but %s is OPEN" % (ka, kb, kb, ka))
    sec6 = re.search(r"## 6\..*?(?=\n## 7\.)", ho, re.S)
    if sec6:
        for line in sec6.group(0).splitlines():
            mt2 = re.match(r"^\|\s*(C-\d+)\b", line)
            if mt2:
                cc = cells(line)
                if mt2.group(1) not in claims:
                    bad.append("handover section 6 names %s, which is not in the graph" % mt2.group(1))
                elif len(cc) > 1 and first_word(cc[1]) != first_word(claims[mt2.group(1)][2]):
                    bad.append("handover section 6 says %s %s, the graph says %s" % (mt2.group(1), first_word(cc[1]), first_word(claims[mt2.group(1)][2])))
    R.add("S17", "FAIL" if bad else "PASS", "; ".join(bad[:8]))

    # S18 completion
    bad = []
    for wid, c in wp_rows.items():
        if len(c) != 6:
            bad.append("work package %s has %d columns" % (wid, len(c)))
            continue
        if c[4] not in LIFECYCLE:
            bad.append("%s: Lifecycle %r is outside NOT_STARTED, ACTIVE, -" % (wid, c[4]))
        if c[5] not in FINAL:
            bad.append("%s: Final %r is outside DONE, PARTIAL, BLOCKED, -" % (wid, c[5]))
        if c[4] == "NOT_STARTED" and c[5] != "-":
            bad.append("%s: NOT_STARTED with Final %s" % (wid, c[5]))
    for c in table_rows(rd(os.path.join(sdir, "baseline.md"))):
        if len(c) == 4 and first_word(c[2]) not in CAPABILITY:
            bad.append("baseline %s: capability %r is outside the closed set" % (c[0], c[2][:20]))
    if fin_h and fin_h.group(1) == "DONE":
        for wid, c in wp_rows.items():
            if len(c) == 6 and "REQUIRED" in c[2] and c[5] != "DONE":
                bad.append("Final DONE but %s (REQUIRED) is %s" % (wid, c[5]))
    heads = re.findall(r"(?m)^#{1,3} .*$", plan_text)
    htxt = "\n".join(heads)
    if not wp_rows:
        bad.append("work-packages.md lists no package")
    if "REQUIRED" not in plan_text:
        bad.append("the plan names no REQUIRED acceptance criterion")
    for label, pat in (("scope or objective", r"(?i)scope|objective|phạm vi|mục tiêu"), ("contract bottlenecks", r"(?i)bottleneck"), ("an evidence plan", r"(?i)evidence|bằng chứng")):
        if not re.search(pat, htxt):
            bad.append("the plan has no heading for %s" % label)
    R.add("S18", "FAIL" if bad else "PASS", "; ".join(bad[:8]))

    # S19 freshness of cited sources
    nvl = []
    set_date = "%s-%s-%s" % (ts[0:4], ts[4:6], ts[6:8])
    for cid, c in claims.items():
        if len(c) < 5 or first_word(c[2]) != "VALID":
            continue
        for i in EV_RE.findall(c[3]):
            r_ = recs.get(i)
            if r_ and first_word(r_["basis"]) == "CITED" and strip_q(r_["artifact_revision"]).startswith("no revision given"):
                at = strip_q(r_["checked_at"])[:10]
                if re.match(r"^\d{4}-\d{2}-\d{2}$", at) and at < set_date:
                    nvl.append("%s rests on %s retrieved %s without a revision, before %s" % (cid, i, at, set_date))
    R.add("S19", "NOT_VERIFIED" if nvl else "PASS", "; ".join(nvl[:6]))
    return R


def usage(why):
    sys.stderr.write("usage error: %s\n%s" % (why, __doc__))
    return 3


def main(argv):
    args = argv[1:]
    root, ref, dscript, legacy, root_set, strict_from, as_json = ".", None, None, set(), False, 0, False
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--ref", "--digest-script", "--legacy", "--strict-from"):
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                return usage("%s needs a value" % a)
            v = args[i + 1]
            if a == "--ref":
                ref = v
            elif a == "--digest-script":
                dscript = v
            elif a == "--strict-from":
                mm = re.search(r"(\d+)$", v)
                if not mm:
                    return usage("--strict-from needs a record ID such as O-1001")
                strict_from = int(mm.group(1))
            else:
                legacy = set(x for x in v.split(",") if x)
            i += 2
        elif a == "--json":
            as_json = True
            i += 1
        elif a.startswith("--"):
            return usage("unknown flag %s" % a)
        else:
            if root_set:
                return usage("more than one ROOT")
            root, root_set = a, True
            i += 1
    if dscript is None:
        dscript = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dir_digest.py")
    R = check(root, ref, dscript, legacy, strict_from)
    n = lambda x: sum(1 for _, r, _ in R.res if r == x)
    code = 1 if n("FAIL") else (4 if n("NOT_VERIFIED") else 0)
    at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if as_json:
        print(json.dumps({"schema_version": 1, "tool": "check_state", "root": os.path.abspath(root),
                          "checks": [{"id": c, "result": r, "detail": d, "fix": FIX.get(c, "") if r in ("FAIL", "NOT_VERIFIED") else ""} for c, r, d in R.res],
                          "summary": {"checks": len(R.res), "PASS": n("PASS"), "FAIL": n("FAIL"), "NOT_VERIFIED": n("NOT_VERIFIED"), "N/A": n("N/A")},
                          "exit_code": code, "checked_at": at}, indent=1, sort_keys=True))
        return code
    for cid, res, detail in R.res:
        print("%-4s %-13s %s" % (cid, res, detail))
    print("checks=%d PASS=%d FAIL=%d NOT_VERIFIED=%d N/A=%d" % (len(R.res), n("PASS"), n("FAIL"), n("NOT_VERIFIED"), n("N/A")))
    print("checked_at=" + at)
    return code


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as exc:
        print("internal error: %r" % (exc,))
        sys.exit(5)
