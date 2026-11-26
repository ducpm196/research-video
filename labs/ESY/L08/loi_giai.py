import sys
s = sys.stdin.read().strip() or "100000 8"
clk, nb = map(int, s.split())
t_spi_us = (nb * 8) / clk * 1e6
t_i2c_us = ((nb + 1) * 9) / clk * 1e6
print(f"spi_8B_us={t_spi_us:.1f} i2c_8B_us={t_i2c_us:.1f}")
