import ast
src = 'def f(a,b,xs):\n if a: pass\n for x in xs:\n  if x>0 and b: return x\n return 0'
t = ast.parse(src)
pts = sum(isinstance(n, (ast.If, ast.For, ast.While, ast.BoolOp)) for n in ast.walk(t))
m = pts + 1
print(f'decision_points={pts}')
print(f'mccabe_complexity={m}')
print(f'max_recommended_le10={int(m<=10)}')
