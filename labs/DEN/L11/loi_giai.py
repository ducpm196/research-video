rgs = [(i * 10, i * 10 + 9) for i in range(80)]
hit = sum(mn <= 123 <= mx for mn, mx in rgs)
skip = 100 * (len(rgs) - hit) / len(rgs)
print(f'groups_scanned={hit}')
print(f'skipped_pct={skip:.1f}%')
