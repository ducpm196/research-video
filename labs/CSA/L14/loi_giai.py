va = 0x5ABC; vpn = va >> 12; off = va & 0xFFF; pfn = 0x12; pa = (pfn << 12) | off
eat = 0.98 * (1 + 100) + 0.02 * (1 + 100 + 100)
print(f'vpn=0x{vpn:02X} offset=0x{off:03X}')
print(f'phys_addr=0x{pa:05X}')
print(f'eat_ns={eat:.2f}')
