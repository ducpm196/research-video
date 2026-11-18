from pathlib import Path
import pandas as pd

Path("gd.csv").write_text("ma,ngay,loai,kenh,so_tien\n1,2026-04-01,rut,atm,500000\n2,2026-04-01,chuyen,app,1200000\n3,2026-04-02,nap,quay,5000000\n4,2026-04-02,chuyen,app,250000\n5,2026-04-03,rut,atm,700000\n6,2026-04-03,thanh_toan,pos,\n7,2026-04-04,chuyen,web,90000\n8,2026-04-04,nap,app,3000000\n", encoding="utf-8")
gd = pd.read_csv("gd.csv", parse_dates=["ngay"])
print("Thieu so_tien:", gd["so_tien"].isna().sum())
sach = gd.dropna(subset=["so_tien"])
theo_loai = sach.groupby("loai")["so_tien"].agg(["count", "sum"])
print(theo_loai)
theo_ngay = sach.groupby(sach["ngay"].dt.day)["so_tien"].sum()
print(theo_ngay)
print("Ngay nhieu nhat:", theo_ngay.idxmax(), int(theo_ngay.max()))
