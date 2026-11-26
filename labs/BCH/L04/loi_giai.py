import sys
s = sys.stdin.read().strip() or "700,400|850 20"
ins, ps = s.split("|")
inputs = [int(x) for x in ins.split(",")]
pay, fee = map(int, ps.split())
change = sum(inputs) - pay - fee
print(f"in_sum={sum(inputs)/100:.1f} change={change/100:.1f}")
