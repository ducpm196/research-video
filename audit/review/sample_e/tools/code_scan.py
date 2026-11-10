"""Quét mọi khối mã trên màn hình (<div class="code"> / <pre>) trong lessons/**/*.yaml, thử compile() như Python.
Chỉ báo khối trông giống Python (có def/class/import/print(/for … in/ return) mà compile lỗi."""
import re, html, glob, sys, yaml, ast, collections
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:/research-video/lessons"
PYISH = re.compile(r"^\s*(def |class |import |from \w+ import|print\(|for \w+ in |while |return |if .*:$)", re.M)
NOTPY = re.compile(r"(;\s*$|\{\s*$|public |SELECT |#include|System\.out|=>|function |const |let |var )", re.M | re.I)


def blocks(show):
    for m in re.finditer(r'<div class="code"[^>]*>(.*?)</div>\s*(?=<(?!div>)|$)', show, re.S):
        yield m.group(1)
    for m in re.finditer(r"<pre[^>]*>(.*?)</pre>", show, re.S):
        yield m.group(1)


def to_text(b):
    b = re.sub(r"</div>\s*<div[^>]*>", "\n", b)
    b = re.sub(r"<br\s*/?>", "\n", b)
    b = re.sub(r"<[^>]+>", "", b)
    return html.unescape(b).replace("\u00a0", " ")


def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "show" and isinstance(v, str):
                yield v
            else:
                yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


bad = collections.defaultdict(list)
n = 0
for f in sorted(glob.glob(ROOT + "/*/L*.yaml")):
    spec = yaml.safe_load(open(f, encoding="utf-8"))
    for show in walk(spec):
        for b in blocks(show):
            t = to_text(b)
            if not PYISH.search(t) or NOTPY.search(t):
                continue
            n += 1
            try:
                ast.parse(t)
            except SyntaxError as e:
                lines = t.splitlines()
                ln = lines[e.lineno - 1] if e.lineno and e.lineno <= len(lines) else ""
                bad[f].append(f"{e.msg} @{e.lineno}: {ln.strip()[:90]}")
print("khối giống Python:", n, "| lỗi cú pháp:", sum(map(len, bad.values())), "ở", len(bad), "bài")
for f, v in bad.items():
    print(f.replace("\\", "/").split("lessons/")[1])
    for x in v[:4]:
        print("   ", x)
