pt = {0: 5, 1: 2, 2: 9, 3: 7}
va = 0x3A7F; vpn, off = va >> 12, va & 0xFFF
pa = (pt[vpn] << 12) | off
eat = 0.9 * (20 + 100) + 0.1 * (20 + 100 + 100)
print(f'va=0x{va:04X} vpn={vpn} offset=0x{off:03X}')
print(f'pa=0x{pa:04X}')
print(f'eat_ns={eat:.1f}')
