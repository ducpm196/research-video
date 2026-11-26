import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
pt = {int(k): int(v) for p in kv['pt'].split(',') for k, v in [p.split(':')]}
va = int(kv['va'], 16); pb = int(kv['page_bits'])
vpn, off = va >> pb, va & ((1 << pb) - 1)
pa = (pt[vpn] << pb) | off
h, tlb, ram = float(kv['tlb_hit']), float(kv['tlb_ns']), float(kv['ram_ns'])
eat = h * (tlb + ram) + (1.0 - h) * (tlb + ram + ram)
print(f'va=0x{va:04X} vpn={vpn} offset=0x{off:03X}')
print(f'pa=0x{pa:04X}')
print(f'eat_ns={eat:.1f}')
