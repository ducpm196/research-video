def valid(amt, acc):
    ok_a = isinstance(amt, int) and not isinstance(amt, bool)
    return ok_a and 0 < amt <= 10_000_000 and len(acc) == 10 and acc.isdigit()
calls = [
    (750_000, '9876543210'), (True, '9876543210'), (-100, '9876543210'),
    (250_000, '12345'), (15_000_000, '9876543210'),
]
ok = [i for i, c in enumerate(calls) if valid(*c)]
print(f"total_calls={len(calls)} valid_count={len(ok)} idx={ok}")
