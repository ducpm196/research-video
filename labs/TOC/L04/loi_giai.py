import sys
s = sys.stdin.read().strip() or "5|00|00|011111|2"
ps, x, y, z, rs = s.split("|")
p, rep = int(ps), int(rs)
target = "0" * p + "1" * p
split_ok = (x + y + z == target) and (len(x + y) <= p) and (len(y) >= 1)
pumped = x + y * rep + z
in_lang = (len(pumped) % 2 == 0) and (pumped == "0" * (len(pumped) // 2) + "1" * (len(pumped) // 2))
print(f"split_ok={int(split_ok)} pumped_len={len(pumped)} valid={int(in_lang)}")
