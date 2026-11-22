s = '6149283750'
chunks = [s[i:i+2] for i in range(0, len(s), 2)]
print(f"raw_units={len(s)} grouped_chunks={len(chunks)} fits_wm={int(len(chunks) <= 4)}")
