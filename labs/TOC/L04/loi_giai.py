p = 5
s = '0' * p + '1' * p
x, y, z = '00', '00', '011111'
split_ok = (x + y + z == s) and (len(x + y) <= p) and (len(y) >= 1)
pumped = x + y * 2 + z
in_lang = (pumped == '0' * (len(pumped) // 2) + '1' * (len(pumped) // 2)) and (len(pumped) % 2 == 0)
print(f"split_ok={int(split_ok)} pumped_len={len(pumped)} valid={int(in_lang)}")
