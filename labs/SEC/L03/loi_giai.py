p3 = 3 / 1_000_000; p500 = 500_000 / 1_000_000
print(f'prob_3_tries={p3:.0e}')
print(f'prob_unbounded_500k={p500:.2f}')
print(f'rate_limit_factor={round(p500 / p3)}x')
