total, min_healthy, req = 120, 90, 40
max_rm = total - min_healthy
print(f"max_removable={max_rm} req={req} blocked={int(req > max_rm)}")
