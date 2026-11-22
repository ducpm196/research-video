a_sm, b_sm = 46/50, 176/200
a_lg, b_lg = 140/200, 32/50
a_all, b_all = (46+140)/(50+200), (176+32)/(200+50)
won = int(a_sm > b_sm and a_lg > b_lg)
print(f"sub_A_wins={won} pooled_A={a_all:.3f} pooled_B={b_all:.3f}")
