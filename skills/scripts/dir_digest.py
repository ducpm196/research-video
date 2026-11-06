#!/usr/bin/env python3
"""Reference implementation of dir-digest-v1 (EGW SKILL.md, section 4).

Read-only, standard library only, no network, writes nothing but stdout.

Usage:  python3 dir_digest.py DIR [--short] [--list]
  --short  print the first 16 hex digits instead of all 64
  --list   also print every hashed file (relative path and size) to stderr

Method: sha256 over, for each regular file sorted bytewise by its POSIX
relative path in UTF-8: the bytes of the relative path, 0x00, the file
contents, 0x00. No file is excluded and no line endings are normalized.

A symbolic link, any other non-regular file, or a name that is not valid
UTF-8 is never followed or hashed, and an entry that cannot be listed or
read is never skipped silently. A directory that contains one has no
valid digest: the script prints the findings to stderr and exits 2.
The root argument itself may be a symbolic link to a directory.

Exit codes: 0 digest printed | 2 no valid digest | 3 not a directory.
"""
import hashlib
import os
import stat
import sys

sys.dont_write_bytecode = True  # a stray __pycache__ would change the digest


def compute(root):
    """Return (hex_digest_or_None, hashed_files, findings)."""
    hashed, findings = [], []

    def walk_error(err):  # os.walk would otherwise skip an unlistable directory
        rel = os.path.relpath(err.filename or root, root).replace(os.sep, "/")
        findings.append((rel, "cannot be listed: %s" % err.strerror))

    for dirpath, dirnames, filenames in os.walk(root, onerror=walk_error, followlinks=False):
        for name in list(dirnames) + list(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            rel_b = os.fsencode(rel)
            try:
                rel_b.decode("utf-8")
            except UnicodeDecodeError:
                findings.append((rel_b.decode("utf-8", "replace"), "name is not valid UTF-8"))
                continue
            try:
                mode = os.lstat(full).st_mode
            except OSError as err:
                findings.append((rel, "cannot be inspected: %s" % err.strerror))
                continue
            if name in dirnames:
                if stat.S_ISLNK(mode):
                    findings.append((rel, "symbolic link to a directory"))
                continue  # real directories are traversed, never hashed
            if stat.S_ISREG(mode):
                hashed.append((rel_b, full))
            else:
                findings.append((rel, "symbolic link" if stat.S_ISLNK(mode) else "not a regular file"))
    if findings:
        return None, hashed, findings
    hashed.sort(key=lambda item: item[0])
    h = hashlib.sha256()
    for rel_b, full in hashed:
        try:
            with open(full, "rb") as fh:
                data = fh.read()
        except OSError as err:
            findings.append((rel_b.decode("utf-8"), "cannot be read: %s" % err.strerror))
            continue
        h.update(rel_b + b"\x00" + data + b"\x00")
    if findings:
        return None, hashed, findings
    return h.hexdigest(), hashed, findings


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    if len(args) != 1 or not flags <= {"--short", "--list"}:
        sys.stderr.write(__doc__)
        return 3
    if not os.path.isdir(args[0]):
        sys.stderr.write("not a directory: %s\n" % args[0])
        return 3
    digest, hashed, findings = compute(args[0])
    if digest is None:
        for rel, why in findings:
            sys.stderr.write("NO VALID DIGEST: %s: %s\n" % (rel, why))
        return 2
    if "--list" in flags:
        for rel_b, full in hashed:
            sys.stderr.write("%s\t%d\n" % (rel_b.decode("utf-8"), os.path.getsize(full)))
    print(digest[:16] if "--short" in flags else digest)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
