import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
print(f'btree_wa={kv["page_b"] / kv["rec_b"]:.1f}x\nlsm_tiered_wa={float(2 + kv["tiers"]):.1f}x')
