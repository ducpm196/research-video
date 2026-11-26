import sys
s = sys.stdin.read().strip() or "2.0 0.95 8.0"
r, g, mQ = map(float, s.split())
print(f"dqn_target={r + g * mQ:.1f} terminal_target={r:.1f}")
