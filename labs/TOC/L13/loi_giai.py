S = [5, 9, 14, 18, 27]; T = 46; cert = [5, 14, 27]
pool = list(S); in_S = True
for x in cert:
    if x in pool: pool.remove(x)
    else: in_S = False
tot = sum(cert)
print(f"cert_steps={len(cert)} verified={int(in_S and tot == T)} cert_sum={tot}")
