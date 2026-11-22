mmr = lambda rel, sim, l=0.6: l * rel - (1.0 - l) * sim
sx, sy = mmr(0.95, 0.85), mmr(0.75, 0.15)
print(f"mmr_X={sx:.3f} mmr_Y={sy:.3f} pick={'Y' if sy > sx else 'X'}")
