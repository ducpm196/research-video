import sys
s = sys.stdin.read().strip() or "10|25,5,30|45"
hz_s, n_s, blk_s = s.split("|")
period_ms = 1000.0 / float(hz_s)
norm = [int(x) for x in n_s.split(",")]
normal = sum(norm)
inverted = normal + int(blk_s)
ovl = int(inverted > period_ms)
print(f"period_ms={period_ms:.0f} normal_ms={normal} inverted_ms={inverted} overload={ovl}")
