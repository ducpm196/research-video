import re
toks = re.findall(r'[A-Za-z_]\w*|\d+|[=+*/-]', 'total = 108 - cnt')
print(f"count={len(toks)} toks={toks}")
