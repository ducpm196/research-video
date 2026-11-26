import sys
s = sys.stdin.read().strip() or "1200 6 2 150"
steps, period, bonus, finish = map(int, s.split())
loop_r = (steps // period) * bonus
print(f"intended={finish} reward_hacked={loop_r} broken={int(loop_r > finish)}")
