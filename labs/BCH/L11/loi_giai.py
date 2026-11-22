vals = sorted([199, 200, 202, 203, 204, 9999, 9999, 9999, 9999])
med = vals[len(vals) // 2]
print(f"median_price={med} safe_in_band={int(199 <= med <= 204)}")
