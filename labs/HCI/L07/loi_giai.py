import sys
s = sys.stdin.read().strip() or "5,2,5,1,4,2,5,1,4,2"
ans = [int(x) for x in s.split(",")]
odd_s = sum(x - 1 for x in ans[0::2])
even_s = sum(5 - x for x in ans[1::2])
print(f"odd={odd_s} even={even_s} SUS={(odd_s + even_s) * 2.5:.1f}")
