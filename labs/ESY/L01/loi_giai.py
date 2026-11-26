import sys
s = sys.stdin.read().strip() or "0x12 3 1 0"
rs, bs, bc, bt = s.split()
reg = int(rs, 16)
reg |= (1 << int(bs)); r_set = reg
reg &= ~(1 << int(bc)); r_clr = reg
reg ^= (1 << int(bt)); r_tog = reg
print(f"set={hex(r_set)} clr={hex(r_clr)} tog={hex(r_tog)}")
