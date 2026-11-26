import sys
s = sys.stdin.read().strip() or "9600 10 24"
baud, bpb, nb = map(int, s.split())
bps = baud // bpb
tx_ms = nb / bps * 1000.0
print(f"bytes_per_sec={bps} tx_24B_ms={tx_ms:.1f}")
