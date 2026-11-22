reg = 0x12
reg |= (1 << 3); r_set = reg
reg &= ~(1 << 1); r_clr = reg
reg ^= (1 << 0); r_tog = reg
print(f"set={hex(r_set)} clr={hex(r_clr)} tog={hex(r_tog)}")
