#!/usr/bin/env python3
"""State helper for an Evidence-Gated Work workspace: staleness, record numbers, a new report set, the manifest.

Usage: python3 -I -B scripts/egw_state.py COMMAND WORKSPACE [options]
  stale WORKSPACE [--apply] [--json]
        recompute every file and folder that a VALID record lists under dependencies (sha256, dir-digest-v1), then follow
        the claim: dependencies: a VALID record that depends on a record that is changed, STALE, FAILED or NOT_VERIFIED is
        STALE too, transitively. Prints one line per record that must become STALE. Without --apply nothing is written
        and the exit code is 1 when there is such a record. With --apply the line "validity: VALID" of each such record
        is rewritten as "validity: STALE   # <reason>; marked <date> by egw_state.py" (nothing else changes) and the exit code is 0.
  next-id WORKSPACE [--prefix O|S] [--request N]
        print the next free record ID. With --request N the number is N*100 plus a running number (request 10: 1001 to 1099).
  init WORKSPACE --ref REF [--ts YYYYMMDD_HHMMSS]
        copy assets/templates into WORKSPACE (an existing directory): the seven state files (decisions.md included), plan,
        knowledge graph and handover of a new report set named by REF and the timestamp (default: now, UTC), handover.md,
        and state/evidence/. Refuses, and writes nothing, when any of those files exists. The templates cite the example
        record O-0001, which is not copied: check_state FAILs S3, S4, S6 and S8 until it is written (egw_record.py run
        --id O-0001) or the example IDs are replaced. The digest of state/ in the handover stays a placeholder (check S15
        is NOT_VERIFIED until it is filled with the output of manifest). The last lines say what to do next.
  manifest WORKSPACE
        print the rows of handover section 7: state/ and every folder that holds a SKILL.md, each with its dir-digest-v1.
  sync-handover WORKSPACE
        copy the newest handover_<ref>_<ts>.md to handover.md (a byte copy).

Writes only below the named WORKSPACE: state/evidence/*.md (stale --apply), the template files (init), handover.md
(sync-handover); never into a skill folder. Standard library only (Python 3.8+), no network.
Exit codes: 0 done, 1 refusal or (stale without --apply) a record to mark, 3 usage error, 5 internal error.
Last line: checked_at=<UTC>.
"""
import datetime
import glob
import hashlib
import json
import os
import re
import shutil
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dir_digest  # noqa: E402

MOUNT_POINT_TAG = 0xA0000003  # IO_REPARSE_TAG_MOUNT_POINT: a Windows junction
ID_RE = re.compile(r"^[OS]-(\d{4,6})$")
SKIP_DIRS = (".git", "node_modules", "build", "evals", "archive", "probes", "__pycache__")


class Refusal(Exception):
    pass


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def write_new(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "x", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def load_records(ws):
    recs = {}
    for p in sorted(glob.glob(os.path.join(ws, "state", "evidence", "*.md"))):
        rid = os.path.basename(p)[:-3]
        text = read(p)
        v = re.search(r"^validity:[ \t]*(\w+)", text, re.M)
        deps = re.findall(r'^\s+- path: "(.*?)"\n\s+digest: "(.*?)"', text, re.M)
        recs[rid] = {"path": p, "text": text, "validity": v.group(1) if v else "", "deps": deps}
    return recs


def changed_dependency(ws, rel, digest):
    """Return a reason when the file or folder no longer has the recorded digest, else None."""
    m = re.search(r"[0-9a-f]{16,64}", digest)
    if not m:
        return None
    if os.path.isabs(rel) or re.match(r"^[A-Za-z]:", rel) or ".." in rel.replace("\\", "/").split("/"):
        return None  # outside the workspace: the state checker reports it as NOT_VERIFIED
    full = os.path.join(ws, *[p for p in rel.replace("\\", "/").split("/") if p not in ("", ".")])
    if not os.path.exists(full):
        return "%s is missing" % rel
    if os.path.isdir(full):
        now, _files, _findings = dir_digest.compute(full)
        if now is None:
            return None
    else:
        now = sha256_file(full)
    return None if now.startswith(m.group(0)) else "%s changed" % rel


def stale_set(ws):
    recs = load_records(ws)
    stale = {}
    for rid, r in recs.items():
        if r["validity"] != "VALID":
            continue
        for p, d in r["deps"]:
            if p.startswith("claim:"):
                continue
            why = changed_dependency(ws, p, d)
            if why:
                stale[rid] = why
                break
    bad = set(stale) | {rid for rid, r in recs.items() if r["validity"] != "VALID"}
    again = True
    while again:
        again = False
        for rid, r in recs.items():
            if r["validity"] != "VALID" or rid in stale:
                continue
            for p, _d in r["deps"]:
                if p.startswith("claim:") and p[6:] in bad:
                    stale[rid] = "depends on %s, which is no longer VALID" % p[6:]
                    bad.add(rid)
                    again = True
                    break
    return recs, stale


def cmd_stale(ws, apply_, as_json):
    recs, stale = stale_set(ws)
    if apply_:
        today = time.strftime("%Y-%m-%d", time.gmtime())
        for rid, why in sorted(stale.items()):
            text = recs[rid]["text"]
            new = re.sub(r"^validity:[ \t]*VALID[^\n]*$", lambda m: "validity: STALE   # %s; marked %s by egw_state.py" % (why, today), text, count=1, flags=re.M)
            with open(recs[rid]["path"], "w", encoding="utf-8", newline="\n") as fh:
                fh.write(new)
    if as_json:
        print(json.dumps({"schema_version": 1, "tool": "egw_state", "command": "stale", "applied": bool(apply_),
                          "stale": [{"id": k, "reason": v} for k, v in sorted(stale.items())], "records": len(recs),
                          "checked_at": utc_now()}, indent=1, sort_keys=True))
    else:
        for rid, why in sorted(stale.items()):
            print("STALE %s: %s" % (rid, why))
        print("records=%d stale=%d%s" % (len(recs), len(stale), " (marked)" if apply_ and stale else ""))
        print("checked_at=" + utc_now())
    return 0 if apply_ or not stale else 1


def cmd_next_id(ws, prefix, request):
    nums = [int(ID_RE.match(i).group(1)) for i in load_records(ws) if ID_RE.match(i) and i[0] == prefix]
    if request is not None:
        lo, hi = request * 100 + 1, request * 100 + 99
        used = [n for n in nums if lo <= n <= hi]
        n = max(used) + 1 if used else lo
        if n > hi:
            raise Refusal("the range %d to %d of request %d is full" % (lo, hi, request))
    else:
        n = max(nums) + 1 if nums else 1001
    width = 4 if n < 10000 else (5 if n < 100000 else 6)
    if n > 999999:
        raise Refusal("no record number left")
    print("%s-%0*d" % (prefix, width, n))
    return 0


def templates_dir():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "templates")


def cmd_init(ws, ref, ts):
    if not re.match(r"^[A-Z][A-Z0-9-]*$", ref) or not re.match(r"^\d{8}_\d{6}$", ts):
        raise Refusal("REF is capital letters, digits and hyphens; the timestamp is YYYYMMDD_HHMMSS")
    tpl = templates_dir()
    if not os.path.isdir(tpl):
        raise Refusal("no assets/templates next to this script")
    plan = [("plan.md", "plan_%s_%s.md" % (ref, ts)), ("knowledge-graph.md", "knowledge-graph_%s_%s.md" % (ref, ts)),
            ("handover.md", "handover_%s_%s.md" % (ref, ts)), ("handover.md", "handover.md")]
    for name in sorted(os.listdir(os.path.join(tpl, "state"))):
        plan.append((os.path.join("state", name), os.path.join("state", name)))
    clash = [dst for _src, dst in plan if os.path.exists(os.path.join(ws, dst))]
    if clash:
        raise Refusal("these files exist and are never overwritten: %s" % ", ".join(clash))
    made = []
    for src, dst in plan:
        text = read(os.path.join(tpl, src)).replace("EGW-EXAMPLE-001", ref).replace("20260101_000000", ts)
        write_new(os.path.join(ws, dst), text)
        made.append(dst.replace(os.sep, "/"))
    os.makedirs(os.path.join(ws, "state", "evidence"), exist_ok=True)
    for m in made:
        print("created " + m)
    print("created state/evidence/")
    print("next: the templates cite record O-0001, which init does not write; until it exists check_state FAILs S3, S4, S6 "
          "and S8. Write it with scripts/egw_record.py run --id O-0001 (or replace the example IDs), then put the rows "
          "printed by 'egw_state.py manifest' into section 7 of both handover files")
    return 0


def skill_dirs(ws):
    out = []
    for dp, dirs, files in os.walk(ws):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if "SKILL.md" in files:
            out.append(os.path.relpath(dp, ws).replace(os.sep, "/"))
    return sorted(out)


def cmd_manifest(ws):
    at = utc_now()
    print("| Artifact | Digest | Checked |")
    print("|---|---|---|")
    for rel in ["state"] + skill_dirs(ws):
        digest, _files, findings = dir_digest.compute(os.path.join(ws, rel))
        if digest is None:
            raise Refusal("%s has no valid dir-digest-v1: %s" % (rel, findings[:1]))
        print("| %s/ | `%s` | %s |" % (rel, digest, at))
    return 0


def cmd_sync_handover(ws):
    best = None
    for p in glob.glob(os.path.join(ws, "handover_*_*.md")):
        m = re.match(r"^handover_(.+)_(\d{8}_\d{6})\.md$", os.path.basename(p))
        if m and (best is None or m.group(2) > best[0]):
            best = (m.group(2), p)
    if not best:
        raise Refusal("no handover_<ref>_<ts>.md in the workspace")
    with open(best[1], "rb") as fh:
        data = fh.read()
    with open(os.path.join(ws, "handover.md"), "wb") as fh:
        fh.write(data)
    print("handover.md is a copy of " + os.path.basename(best[1]))
    return 0


def usage(why):
    sys.stderr.write("usage error: %s\n%s" % (why, __doc__))
    return 3


def main(argv):
    args = argv[1:]
    if len(args) < 2 or args[0] not in ("stale", "next-id", "init", "manifest", "sync-handover"):
        return usage("COMMAND and WORKSPACE are required")
    cmd, ws, rest = args[0], args[1], args[2:]
    if not os.path.isdir(ws):
        return usage("%s is not a directory" % ws)
    ws = os.path.abspath(ws)
    opts = {}
    i = 0
    flags = {"stale": ("--apply", "--json"), "next-id": (), "init": (), "manifest": (), "sync-handover": ()}
    values = {"stale": (), "next-id": ("--prefix", "--request"), "init": ("--ref", "--ts"), "manifest": (), "sync-handover": ()}
    while i < len(rest):
        a = rest[i]
        if a in flags[cmd]:
            opts[a] = True
            i += 1
        elif a in values[cmd]:
            if i + 1 >= len(rest) or rest[i + 1].startswith("--"):
                return usage("%s needs a value" % a)
            opts[a] = rest[i + 1]
            i += 2
        else:
            return usage("unknown argument %s for %s" % (a, cmd))
    try:
        if cmd == "stale":
            return cmd_stale(ws, "--apply" in opts, "--json" in opts)
        if cmd == "next-id":
            prefix = opts.get("--prefix", "O")
            req = opts.get("--request")
            if prefix not in ("O", "S") or (req is not None and not req.isdigit()):
                return usage("--prefix is O or S and --request a number")
            return cmd_next_id(ws, prefix, int(req) if req is not None else None)
        if cmd == "init":
            if "--ref" not in opts:
                return usage("init needs --ref")
            return cmd_init(ws, opts["--ref"], opts.get("--ts") or time.strftime("%Y%m%d_%H%M%S", time.gmtime()))
        if cmd == "manifest":
            return cmd_manifest(ws)
        return cmd_sync_handover(ws)
    except Refusal as err:
        print("REFUSED: %s" % err)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as exc:  # no result
        print("internal error: %r" % (exc,))
        sys.exit(5)
