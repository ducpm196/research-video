C, G, ovl = 120, 40, 25
eff_seq = C / (C + G) * 100
eff_ovl = C / (C + G - ovl) * 100
print(f"seq_eff={eff_seq:.1f}% overlap_eff={eff_ovl:.1f}%")
