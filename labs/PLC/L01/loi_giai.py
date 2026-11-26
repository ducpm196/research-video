import sys, re
s = sys.stdin.read().strip() or "total = 108 - cnt"
toks = re.findall(r"[A-Za-z_]\w*|\d+|[=+*/-]", s)
print(f"count={len(toks)} toks={toks}")
