tr, te = [2.0, 4.0, 6.0], [12.0, 12.0]
m_tr = sum(tr) / len(tr)
m_all = sum(tr + te) / len(tr + te)
print(f"train_mean={m_tr:.1f} leaked_mean={m_all:.1f}")
