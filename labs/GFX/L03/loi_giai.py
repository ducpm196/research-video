import sys
s = sys.stdin.read().strip() or "1280|-1.0,0.25,1.0"
ws, xs = s.split("|")
W = int(ws); vals = [float(v) for v in xs.split(",")]
res = [round((x + 1.0) / 2.0 * W) for x in vals]
print(f"ndc_to_px={res}")
