import sys
s = sys.stdin.read().strip() or "leftpad|leftpad:tpl,cli;tpl:web;web:app;cli:app;app:"
root, g_str = s.split("|", 1)
rev = {}
for item in g_str.split(";"):
    k, vs = item.split(":", 1)
    rev[k] = [x for x in vs.split(",") if x]
broken = set(); stack = list(rev[root])
while stack:
    p = stack.pop()
    if p not in broken:
        broken.add(p); stack.extend(rev.get(p, []))
print(f"broken_upstream={len(broken)} pkgs={sorted(broken)}")
