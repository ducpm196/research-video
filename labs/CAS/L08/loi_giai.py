host, target = 'db-primary', 'db-secondary'
hours = (240 * 8000) / 80 / 3600
print(f"aborted={int(host != target)} restore_hours={hours:.2f}")
