import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
va = int(kv['va'], 16); pfn = int(kv['pfn'], 16); pb = int(kv['page_bits'])
vpn = va >> pb; off = va & ((1 << pb) - 1); pa = (pfn << pb) | off
h, tlb, ram = float(kv['tlb_hit']), float(kv['tlb_ns']), float(kv['ram_ns'])
eat = h * (tlb + ram) + (1.0 - h) * (tlb + ram + ram)
print(f'vpn=0x{vpn:02X} offset=0x{off:03X}')
print(f'phys_addr=0x{pa:05X}')
print(f'eat_ns={eat:.2f}')
