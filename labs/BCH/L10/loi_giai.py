import sys
s = sys.stdin.read().strip() or "2000000 400 600"
blk_b, tx_b, sec = map(int, s.split())
print(f"max_tps={blk_b / tx_b / sec:.2f}")
