import pytest  # noqa: F401  (máy chấm cần thấy thư viện kiểm thử)
import subprocess
import sys
import tempfile
from pathlib import Path

DU_LIEU = "ma,loai,so_tien\n1,chuyen,500000\n2,nap,2000000\n3,rut,300000\n4,chuyen,xyz\n5,nap,1000000\n6,chuyen,150000\n"

def cham(thu_muc):
    p = Path(thu_muc)
    ma = (p / "phan_tich.py").read_text(encoding="utf-8")
    diem = 0
    c1 = ".read(" not in ma and "readlines" not in ma
    print("1. Doc tung dong:", "DAT" if c1 else "CHUA", "(2/2)" if c1 else "(0/2)")
    if not c1:
        print("   Ly do: phan_tich.py con dung .read( hoac readlines")
    diem = diem + (2 if c1 else 0)
    sys.path.insert(0, str(p))  # sys.path: danh sach thu muc may tim mo-dun; chen thu muc cua ban len dau
    import phan_tich as mo_dun  # nap phan_tich.py vua ghi
    (p / "du_lieu.csv").write_text(DU_LIEU, encoding="utf-8")
    ket = mo_dun.tong_theo_loai(str(p / "du_lieu.csv"))
    c2 = ket == ({"chuyen": 650000, "nap": 3000000, "rut": 300000}, 1)
    print("2. Ket qua dung:", "DAT" if c2 else "CHUA", "(3/3)" if c2 else "(0/3)")
    if not c2:
        print("   Ly do: nhan duoc", ket, "- mong doi ({'chuyen': 650000, 'nap': 3000000, 'rut': 300000}, 1)")
    diem = diem + (3 if c2 else 0)
    (p / "rong.csv").write_text("ma,loai,so_tien\n", encoding="utf-8")
    ket = mo_dun.tong_theo_loai(str(p / "rong.csv"))
    c3 = ket == ({}, 0)
    print("3. Tep rong:", "DAT" if c3 else "CHUA", "(2/2)" if c3 else "(0/2)")
    if not c3:
        print("   Ly do: nhan duoc", ket, "- mong doi ({}, 0)")
    diem = diem + (2 if c3 else 0)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=line", "-p", "no:cacheprovider", "test_phan_tich.py"], cwd=p, capture_output=True, text=True)
    c4 = r.returncode == 0 and "3 passed" in r.stdout
    print("4. Ba ca kiem qua:", "DAT" if c4 else "CHUA", "(2/2)" if c4 else "(0/2)")
    if not c4:
        print("   Ly do (pytest):", " | ".join(r.stdout.strip().split("\n")[-4:]))
    diem = diem + (2 if c4 else 0)
    req = (p / "requirements.txt").read_text(encoding="utf-8")
    c5 = "==" in req
    print("5. Ghim phien ban:", "DAT" if c5 else "CHUA", "(1/1)" if c5 else "(0/1)")
    if not c5:
        print("   Ly do: requirements.txt khong co dong ghim ==")
    diem = diem + (1 if c5 else 0)
    print("Tong diem:", str(diem) + "/10")


MODULE = """import csv

def tong_theo_loai(duong_dan):
    tong = {}
    bo_qua = 0
    with open(duong_dan, encoding="utf-8", newline="") as f:
        for hang in csv.DictReader(f):
            try:
                tien = int(hang["so_tien"])
            except ValueError:
                bo_qua = bo_qua + 1
                continue
            tong[hang["loai"]] = tong.get(hang["loai"], 0) + tien
    return tong, bo_qua
"""
TESTS = """import tempfile
from pathlib import Path

from phan_tich import tong_theo_loai

def chay(noi_dung):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "gd.csv"
        p.write_text(noi_dung, encoding="utf-8")
        return tong_theo_loai(str(p))

def test_tong():
    assert chay("ma,loai,so_tien\\n1,nap,100\\n2,nap,50\\n") == ({"nap": 150}, 0)

def test_dong_hong():
    assert chay("ma,loai,so_tien\\n1,nap,abc\\n") == ({}, 1)

def test_rong():
    assert chay("ma,loai,so_tien\\n") == ({}, 0)
"""

with tempfile.TemporaryDirectory() as d:
    (Path(d) / "phan_tich.py").write_text(MODULE, encoding="utf-8")
    (Path(d) / "test_phan_tich.py").write_text(TESTS, encoding="utf-8")
    (Path(d) / "requirements.txt").write_text("pytest==9.2.0\n", encoding="utf-8")
    cham(d)

    import tracemalloc
    ns = {}
    exec(MODULE, ns)
    dinh = []
    for n in (2000, 20000):
        (Path(d) / "lon.csv").write_text("ma,loai,so_tien\n" + "".join("%d,nap,100\n" % i for i in range(n)), encoding="utf-8")
        tracemalloc.start()
        ns["tong_theo_loai"](str(Path(d) / "lon.csv"))
        dinh.append(tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
    print("Bo nho khi dong tang 10 lan:", "gan nhu khong doi" if dinh[1] < 3 * dinh[0] else "tang theo so dong")
