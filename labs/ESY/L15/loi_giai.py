period_ms = 1000 / 10
normal = sum([25, 5, 30])
inverted = sum([25, 45, 5, 30])
ovl = int(inverted > period_ms)
print(f"period_ms={period_ms:.0f} normal_ms={normal}",
      f"inverted_ms={inverted} overload={ovl}")
