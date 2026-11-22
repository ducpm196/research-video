scale = 2.0 / 127.0
q = round(-0.9 / scale)
deq = q * scale
print(f"q={q} deq={deq:.4f} err={abs(deq - (-0.9)):.4f}")
print(f"fp32_gb={13*4} int8_gb={13*1}")
