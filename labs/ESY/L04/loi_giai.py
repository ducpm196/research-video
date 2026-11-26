import sys
s = sys.stdin.read().strip() or "10 5.0 256"
bs, vs, cs = s.split()
bits, vref, code = int(bs), float(vs), int(cs)
levels = 1 << bits
step_mv = vref / levels * 1000.0
vcode = code * vref / levels
snr_db = 6.02 * bits + 1.76
print(f"lsb_mv={step_mv:.2f} V256={vcode:.3f} V SNR={snr_db:.2f} dB")
