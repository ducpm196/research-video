q = lambda n: n // 2 + 1; mf = lambda n: n - q(n)
print(f'quorum_4={q(4)} max_fail_4={mf(4)}')
print(f'quorum_5={q(5)} max_fail_5={mf(5)}')
print(f'odd_beats_even={int(mf(5) > mf(4))}')
