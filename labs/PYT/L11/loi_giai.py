import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

kenh = ["atm", "app", "quay"]
tong = [4200, 6100, 1500]
fig, ax = plt.subplots()
ax.bar(kenh, tong)
ax.set_title("Tong tien theo kenh (nghin dong)")
ax.set_ylabel("nghin dong")
fig.savefig("bieu_do.png")
print("Ve xong:", Path("bieu_do.png").exists())
print("Do cao cot:", [int(p.get_height()) for p in ax.patches])
print("Truc y bat dau tu 0:", ax.get_ylim()[0] == 0)
print("Tieu de:", ax.get_title())
lon = tong.index(max(tong))
nho = tong.index(min(tong))
print("Lon nhat:", kenh[lon], "- gap", round(tong[lon] / tong[nho], 1), "lan nho nhat")
