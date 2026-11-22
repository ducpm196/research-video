t_before = 18 + 1200 * 0.06 + 22
t_after = 18 + 500 * 0.06 + 22
tail8 = (1.0 - 0.985 ** 8) * 100
print(
    f"p99_before={t_before:.0f}ms p99_after={t_after:.0f}ms "
    f"tail8={tail8:.1f}%"
)
