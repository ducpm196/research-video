#!/usr/bin/env python3
"""Write one evidence record (state/evidence/<ID>.md) from a command that this script runs itself, or from a cited source.

Usage:
  python3 -I -B scripts/egw_record.py run  --workspace DIR --id O-1001 --claim TEXT --spec TEXT [--impl TEXT]
                                           [--dep PATH]... [--expect-exit N] [--timeout SECONDS] [--revision TEXT]
                                           [--runtime TEXT] -- COMMAND [ARG]...
  python3 -I -B scripts/egw_record.py cite --workspace DIR --id S-1001 --claim TEXT --source URL_OR_PATH --impl TEXT
                                           --method TEXT (--observed TEXT | --file PATH) [--revision TEXT] [--dep PATH]...

run   starts COMMAND without a shell, in DIR, reads its exit code and output, takes the time from the clock, and records
      method = the command as run, observed = exit code and the start of the output (with the sha256 of the whole output),
      validity VALID when the exit code equals --expect-exit (default 0), otherwise FAILED. basis OBSERVED.
cite  records a source that was read by another tool: basis CITED, --source goes to spec_evidence, --observed is what the
      source said (or --file names a saved copy: its size and sha256 are recorded and the text of the file is not copied),
      revision defaults to "no revision given". validity VALID.
--dep names a file or folder of the workspace (its sha256 or dir-digest-v1 is recorded), or claim:ID of another record;
      a workspace file or folder named in --impl is added as a dependency too (check_state S12 asks for it)
      (its validity@checked_at is recorded). A path outside the workspace, behind a link, or missing refuses the record.
The revision defaults to "git <HEAD>" when DIR is a git repository, else "not recorded".

Writes exactly one file, <DIR>/state/evidence/<ID>.md, and never overwrites an existing record. Standard library only
(Python 3.8+), no network. Exit codes: 0 record written (read the printed validity), 1 refusal, 3 usage error, 5 internal error.
Last line: checked_at=<UTC>.
"""
import argparse
import datetime
import hashlib
import os
import platform
import re
import shlex
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dir_digest  # noqa: E402

MOUNT_POINT_TAG = 0xA0000003  # IO_REPARSE_TAG_MOUNT_POINT: a Windows junction
ID_RE = re.compile(r"^[OS]-\d{4,6}$")
KEYS = ["claim_id", "claim", "basis", "spec_evidence", "impl_evidence", "method", "observed", "artifact_revision",
        "runtime", "dependencies", "validity", "checked_at"]


class Refusal(Exception):
    pass


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def one_line(v):
    return re.sub(r"\s+", " ", str(v)).strip().replace('"', "'")


def inside(ws, rel):
    """Return the full path of a workspace-relative path, refusing links, junctions and paths that leave the workspace."""
    if os.path.isabs(rel) or re.match(r"^[A-Za-z]:", rel):
        raise Refusal("%s is an absolute path" % rel)
    parts = [p for p in rel.replace("\\", "/").split("/") if p not in ("", ".")]
    if ".." in parts:
        raise Refusal("%s leaves the workspace" % rel)
    cur = ws
    for p in parts:
        cur = os.path.join(cur, p)
        try:
            st = os.lstat(cur)
        except OSError:
            raise Refusal("%s does not exist" % rel)
        if os.path.islink(cur) or getattr(st, "st_reparse_tag", 0) == MOUNT_POINT_TAG:
            raise Refusal("%s crosses a link or junction" % rel)
    return cur


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def dependencies(ws, deps):
    out = []
    for d in deps:
        if d.startswith("claim:"):
            rid = d[6:]
            p = os.path.join(ws, "state", "evidence", rid + ".md")
            if not ID_RE.match(rid) or not os.path.isfile(p):
                raise Refusal("%s names no record" % d)
            with open(p, encoding="utf-8") as fh:
                text = fh.read()
            v = re.search(r"^validity:[ \t]*(\w+)", text, re.M)
            c = re.search(r'^checked_at:[ \t]*"?([^"\n]*)"?', text, re.M)
            if not v or not c:
                raise Refusal("%s has no validity or checked_at" % d)
            out.append((d, "%s@%s" % (v.group(1), c.group(1).strip())))
            continue
        full = inside(ws, d)
        if os.path.isdir(full):
            digest, _files, findings = dir_digest.compute(full)
            if digest is None:
                raise Refusal("%s has no valid dir-digest-v1: %s" % (d, findings[:1]))
        else:
            digest = sha256_file(full)
        out.append((d.replace("\\", "/"), digest))
    return out


def impl_tokens(text):
    """The path-like words of impl_evidence, split as check_state.py (S12) splits them."""
    out = []
    for tok in re.split(r"[;,\s]+", text or ""):
        tok = tok.strip("\"'()[]").split("#")[0].rstrip(".:")
        if not tok or tok.startswith("http") or ":" in tok or ("/" not in tok and "." not in tok):
            continue
        out.append(tok)
    return out


def with_implied(ws, deps, impl):
    """Add every workspace file or folder named in impl_evidence that no --dep covers yet (check S12 asks for them)."""
    given = [d.replace("\\", "/").rstrip("/") for d in deps if not d.startswith("claim:")]
    extra = []
    for tok in impl_tokens(impl):
        t = tok.replace("\\", "/").rstrip("/")
        if any(t == g or t.startswith(g + "/") or g in ("", ".") for g in given + extra):
            continue
        try:
            full = inside(ws, t)
        except Refusal:
            continue
        if os.path.exists(full):
            extra.append(t)
    return list(deps) + extra


def git_revision(ws):
    if not os.path.exists(os.path.join(ws, ".git")):
        return "not recorded"
    try:
        r = subprocess.run(["git", "-C", ws, "rev-parse", "HEAD"], capture_output=True, text=True)
    except OSError:
        return "not recorded"
    h = r.stdout.strip()
    return "git " + h if r.returncode == 0 and re.match(r"^[0-9a-f]{40}$", h) else "not recorded"


def record_text(fields, deps):
    lines = ["# " + fields["claim_id"], "", "```yaml"]
    for k in KEYS:
        if k == "dependencies":
            if deps:
                lines.append("dependencies:")
                for p, d in deps:
                    lines.append('  - path: "%s"' % one_line(p))
                    lines.append('    digest: "%s"' % one_line(d))
            else:
                lines.append("dependencies: []")
        elif k in ("basis", "validity"):
            lines.append("%s: %s" % (k, fields[k]))
        else:
            lines.append('%s: "%s"' % (k, one_line(fields[k])))
    lines.append("```")
    return "\n".join(lines) + "\n"


def write_new(ws, rid, text):
    d = os.path.join(ws, "state", "evidence")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, rid + ".md")
    with open(path, "x", encoding="utf-8", newline="\n") as fh:  # "x": never overwrite
        fh.write(text)
    return path


def default_runtime():
    return "egw_record.py, Python %s, %s %s" % (platform.python_version(), platform.system(), platform.release())


def cmd_run(a):
    ws = os.path.abspath(a.workspace)
    command = list(a.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise Refusal("no command after --")
    deps = dependencies(ws, with_implied(ws, a.dep, a.impl))
    started = utc_now()
    try:
        r = subprocess.run(command, cwd=ws, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=a.timeout)
        out = r.stdout.decode("utf-8", "replace")
        code = r.returncode
        observed = None
    except subprocess.TimeoutExpired as err:
        out, code, observed = (err.stdout or b"").decode("utf-8", "replace"), None, "timed out after %s seconds" % a.timeout
    except OSError as err:
        out, code, observed = "", None, "could not start the command: %s" % err
    if observed is None:
        flat = re.sub(r"\s+", " ", out).strip()
        shown = flat if len(flat) <= 1500 else flat[:1500] + " ... [truncated, %d characters in total]" % len(flat)
        observed = "exit %d; output: %s (output sha256 %s)" % (code, shown or "none", hashlib.sha256(out.encode("utf-8")).hexdigest()[:16])
    valid = code is not None and code == a.expect_exit
    fields = {"claim_id": a.id, "claim": a.claim, "basis": "OBSERVED", "spec_evidence": a.spec,
              "impl_evidence": a.impl or ("; ".join(p for p, _ in deps) or command[0]),
              "method": " ".join(shlex.quote(c) for c in command), "observed": observed,
              "artifact_revision": a.revision or git_revision(ws), "runtime": a.runtime or default_runtime(),
              "validity": "VALID" if valid else "FAILED", "checked_at": started}
    return write_new(ws, a.id, record_text(fields, deps)), fields["validity"]


def cmd_cite(a):
    ws = os.path.abspath(a.workspace)
    deps = dependencies(ws, with_implied(ws, a.dep, a.impl))
    if bool(a.observed) == bool(a.file):
        raise Refusal("give exactly one of --observed and --file")
    if a.file:
        saved = os.path.abspath(a.file)
        if not os.path.isfile(saved):
            raise Refusal("%s is not a file" % a.file)
        observed = "saved copy %s, %d bytes, sha256 %s" % (os.path.basename(saved), os.path.getsize(saved), sha256_file(saved))
    else:
        observed = a.observed
    fields = {"claim_id": a.id, "claim": a.claim, "basis": "CITED", "spec_evidence": a.source, "impl_evidence": a.impl,
              "method": a.method, "observed": observed, "artifact_revision": a.revision or "no revision given",
              "runtime": a.runtime or default_runtime(), "validity": "VALID", "checked_at": utc_now()}
    return write_new(ws, a.id, record_text(fields, deps)), "VALID"


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("usage error: %s\n%s" % (message, __doc__))
        sys.exit(3)


def build_parser():
    p = Parser(add_help=False)
    sub = p.add_subparsers(dest="mode")
    for name in ("run", "cite"):
        s = sub.add_parser(name, add_help=False)
        s.add_argument("--workspace", required=True)
        s.add_argument("--id", required=True)
        s.add_argument("--claim", required=True)
        s.add_argument("--dep", action="append", default=[])
        s.add_argument("--revision")
        s.add_argument("--runtime")
        if name == "run":
            s.add_argument("--spec", required=True)
            s.add_argument("--impl")
            s.add_argument("--expect-exit", type=int, default=0)
            s.add_argument("--timeout", type=int, default=300)
            s.add_argument("command", nargs=argparse.REMAINDER)
        else:
            s.add_argument("--source", required=True)
            s.add_argument("--impl", required=True)
            s.add_argument("--method", required=True)
            s.add_argument("--observed")
            s.add_argument("--file")
    return p


def main(argv):
    a = build_parser().parse_args(argv[1:])
    if a.mode is None:
        sys.stderr.write("usage error: choose run or cite\n%s" % __doc__)
        return 3
    if not ID_RE.match(a.id) or (a.mode == "run" and not a.id.startswith("O-")) or (a.mode == "cite" and not a.id.startswith("S-")):
        sys.stderr.write("usage error: run takes an O- ID and cite an S- ID (four to six digits)\n")
        return 3
    if not os.path.isdir(a.workspace):
        sys.stderr.write("usage error: %s is not a directory\n" % a.workspace)
        return 3
    try:
        path, validity = cmd_run(a) if a.mode == "run" else cmd_cite(a)
    except Refusal as err:
        print("REFUSED: %s" % err)
        return 1
    except FileExistsError:
        print("REFUSED: %s already exists; a record is never overwritten" % a.id)
        return 1
    print("wrote %s validity=%s" % (os.path.relpath(path, a.workspace).replace(os.sep, "/"), validity))
    print("checked_at=" + utc_now())
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except SystemExit:
        raise
    except Exception as exc:  # no result
        print("internal error: %r" % (exc,))
        sys.exit(5)
