bytes_kv = 2 * 24 * 2048 * 8192 * 2
gib_kv = bytes_kv / (1024 ** 3)
print(f"kv_bytes={bytes_kv} kv_GiB={gib_kv:.1f}")
