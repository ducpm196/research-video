need = lambda s, w, ttp, trust: s and w and (not ttp) and (not trust)
central_ops = 1
maj_quorum = (5 // 2) + 1
n_sch = int(need(True, True, True, False))
n_riv = int(need(True, True, False, False))
print(f"central_ops={central_ops} maj_quorum_5={maj_quorum}",
      f"school_need={n_sch} rivals_need={n_riv}")
