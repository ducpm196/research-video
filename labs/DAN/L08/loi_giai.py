import sys
rev = sorted([float(x) for x in sys.stdin.read().strip().split('=', 1)[1].split(',')], reverse=True)
n = len(rev); mn = sum(rev) / n
med = rev[n // 2] if n % 2 else (rev[n // 2 - 1] + rev[n // 2]) / 2.0
topk = max(1, n // 5); sh = sum(rev[:topk]) / sum(rev) * 100
print(f'mean={mn:.1f} median={med:.1f} top20={sh:.1f}%')
