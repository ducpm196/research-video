import sys
s = sys.stdin.read().strip() or "0,2.0;1,4.9;2,8.1;3,11.0"
pts = [tuple(map(float, p.split(","))) for p in s.split(";") if p]
mx = sum(x for x, _ in pts) / len(pts); my = sum(y for _, y in pts) / len(pts)
a = sum((x - mx)*(y - my) for x, y in pts) / sum((x - mx)**2 for x, _ in pts)
b = my - a * mx
print(f"slope={a:.2f} intercept={b:.2f}")
