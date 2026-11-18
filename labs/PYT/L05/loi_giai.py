import csv
import json
from pathlib import Path

Path("gd.csv").write_text("ma,loai,tai_khoan,so_tien\n1,rut,A02,500000\n2,chuyen,A01,1200000\n3,nap,A03,3000000\n4,chuyen,A02,250000\n5,rut,A01,700000\n6,chuyen,A03,90000\n", encoding="utf-8")
tong = {}
dem = 0
with open("gd.csv", encoding="utf-8", newline="") as f:
    for hang in csv.DictReader(f):
        dem = dem + 1
        tong[hang["loai"]] = tong.get(hang["loai"], 0) + int(hang["so_tien"])
bao_cao = {"so_giao_dich": dem, "tong_theo_loai": tong}
with open("bao_cao.json", "w", encoding="utf-8") as f:
    json.dump(bao_cao, f, ensure_ascii=False, sort_keys=True)
doc = json.loads(Path("bao_cao.json").read_text(encoding="utf-8"))
print(Path("bao_cao.json").read_text(encoding="utf-8"))
print(doc["so_giao_dich"], doc["tong_theo_loai"]["nap"])
