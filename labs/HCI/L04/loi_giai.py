import sys
s = sys.stdin.read().strip() or "6149283750 2 4"
txt, csz_s, lim_s = s.split()
csz, lim = int(csz_s), int(lim_s)
chunks = [txt[i:i+csz] for i in range(0, len(txt), csz)]
print(f"raw_units={len(txt)} grouped_chunks={len(chunks)} fits_wm={int(len(chunks) <= lim)}")
