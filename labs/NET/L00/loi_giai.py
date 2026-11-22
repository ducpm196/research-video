hdr = 20 + 20 + 18; frame = 1460 + hdr
print(f'headers_B={hdr}')
print(f'frame_B={frame}')
print(f'efficiency_pct={100 * 1460 / frame:.1f}%')
