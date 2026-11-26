import ast, sys
src = sys.stdin.read().strip()
t = ast.parse(src)
pts = 0
for n in ast.walk(t):
    if isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.IfExp)):
        pts += 1
    elif isinstance(n, ast.BoolOp):
        pts += len(n.values) - 1
m = pts + 1
print(f'decision_points={pts}')
print(f'mccabe_complexity={m}')
print(f'max_recommended_le10={int(m <= 10)}')
