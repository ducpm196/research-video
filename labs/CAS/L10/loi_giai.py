cdc, gft = 5.5, 12.0
ratio = gft / cdc
rel_err = (gft - cdc) / cdc * 100
print(f"ratio={ratio:.2f}x rel_err_pct={rel_err:.1f}%")
