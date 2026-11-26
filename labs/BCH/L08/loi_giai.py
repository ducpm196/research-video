import sys
s = sys.stdin.read().strip() or "75000 40"
gas, gwei = map(int, s.split())
print(f"fee_eth={gas * gwei * 1e-9:.5f}")
