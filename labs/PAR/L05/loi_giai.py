import sys
s = sys.stdin.read().strip() or "64 8 4"
lb, ib, cnt = map(int, s.split())
print(f"shared_per_64B={lb // ib} count={cnt} padded_total_B={cnt * lb}")
