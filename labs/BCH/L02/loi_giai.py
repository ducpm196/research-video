import sys, math
s = sys.stdin.read().strip() or "4096 32"
ntx, hlen = map(int, s.split())
ph = int(math.log2(ntx))
print(f"merkle_hashes={ph} proof_bytes={ph * hlen}")
