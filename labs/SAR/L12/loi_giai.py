wq = 150_000_000 / (30 * 86400)
rq = round(wq * 200)
tb5 = (60 * 150_000_000 * 400) / 1e12
print(f'write_qps={wq:.1f}')
print(f'read_qps={rq}')
print(f'storage_5yr_tb={tb5:.1f}')
