doors = {2, 5}
bel = [(1.0 / 8.0) * (0.85 if i in doors else 0.15) for i in range(8)]
tot = sum(bel)
bel = [b / tot for b in bel]
print(f"p_door2={bel[2]:.3f} p_wall0={bel[0]:.3f} sum={sum(bel):.1f}")
