wait_ms = 15 * (1000 / 200)
tp_single = 1000 / 4
tp_batch = 16 * 1000 / 15
print(f"first_wait_ms={wait_ms:.0f} single_rps={tp_single:.0f} batch_rps={tp_batch:.0f}")
