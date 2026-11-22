baud, bits_per_byte = 9600, 10
bps = baud // bits_per_byte
tx_ms = 24 / bps * 1000.0
print(f"bytes_per_sec={bps} tx_24B_ms={tx_ms:.1f}")
