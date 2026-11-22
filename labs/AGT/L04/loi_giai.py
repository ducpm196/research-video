miss = 0.50 * (0.60 ** 2)
cov = (1.0 - miss) * 100
src = 'He thong thanh toan rut ngan 45% thoi gian xu ly.'
quote = 'rut ngan 45% thoi gian xu ly'
matched = int(quote in src)
print(f"recall_after_3={cov:.1f}% matched_quote={matched}")
