import sys
s = sys.stdin.read().strip() or "256 12|1,1,0,0"
hs, fs = s.split("|")
din, dout = map(int, hs.split())
flags = [int(x) for x in fs.split(",")]
params = din * dout + dout
broken = sum(1 for ok in flags if not ok)
print(f"head_params={params} broken_augs={broken}")
