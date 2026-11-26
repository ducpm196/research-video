ngan_hang = {"a1": 150, "a2": 250, "a3": 350, "a4": 450, "a5": 550, "a6": 650}
chuyen_mach = {"a1": 150, "a2": 250, "a3": 300, "a4": 450, "a7": 700, "a8": 50}
khop = [m for m in ngan_hang if m in chuyen_mach and ngan_hang[m] == chuyen_mach[m]]
lech = [m for m in ngan_hang if m in chuyen_mach and ngan_hang[m] != chuyen_mach[m]]
chi_nh = [m for m in ngan_hang if m not in chuyen_mach]
chi_cm = [m for m in chuyen_mach if m not in ngan_hang]
print("khop", len(khop), "- lech tien", len(lech), "- chi ngan hang", len(chi_nh), "- chi chuyen mach", len(chi_cm))
print("chenh tien:", sum(chuyen_mach.values()) - sum(ngan_hang.values()))
