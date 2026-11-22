raw = [0.0, 1.0, 2.0, 3.0, 4.0]; loop_meas = 3.5
err = loop_meas - raw[-1]
edge_corr = err / 5.0
corr = [round(raw[i] + i * edge_corr, 3) for i in range(5)]
print(f"edge_corr={edge_corr:.3f} corrected_poses={corr}")
