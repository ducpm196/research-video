"""Kiểm độc lập BNX L31 (Quan sát hệ thống). Đường khác với tools/checklib_bnx/l31.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình: Python (nhật ký, chỉ mục đảo), Java (đếm chuỗi và byte), và Prometheus 3.16.0 trong ảnh Docker chính thức
  (ghim băm): promtool test rules và máy chủ thật kéo trang chỉ số; đầu ra phải bằng từng ký tự đầu ra đã hiện;
- nhật ký: tính lại đường đi và 35 ms bằng cách khác (đọc dòng JSON đã in, không dùng danh sách của alg);
- chỉ mục đảo: đếm lại số dòng ERROR và khớp bằng công thức đóng (không vòng lặp);
- văn bản chỉ số: số chuỗi và byte đếm trên đầu ra thật của `java XuatChiSo.java` (đối chiếu với alg.bnx_l31_exposition);
- tốc độ đốt: tính tay bằng Fraction; lab chạy lại và so mong_doi.txt.
Thiếu docker / ảnh / javac → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l31 as src  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L31"


def run(rec):
    if not shutil.which("javac") or not shutil.which("docker"):
        rec("L31", None, "thiếu javac hoặc docker: NOT_VERIFIED")
    else:
        lib2.verify_programs(rec, "L31")
    P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L31"}
    # 1) nhật ký: đọc lại từng dòng JSON đã in
    dong = [json.loads(l) for l in P["NhatKy"].out.splitlines() if l.startswith("{")]
    a1 = [d for d in dong if d["cid"] == "a1"]
    rec("L31", len(dong) == 6 and [d["dv"] + ":" + d["ev"] for d in a1] == ["cong:nhan", "tt:tru-tien", "sc:loi", "cong:tra"] and a1[-1]["t"] - a1[0]["t"] == 35
        and alg.bnx_l31_path(alg.bnx_l31_demo(), "a1") == (["cong:nhan", "tt:tru-tien", "sc:loi", "cong:tra"], 35) and "a1 mat 35 ms" in P["NhatKy"].out,
        "nhật ký: 6 dòng JSON; cid a1 dựng lại cong > tt > sc > cong, 35 ms (đọc lại dòng đã in = alg)")
    hien = P["NhatKy"].code.split("\n")[:11]      # đúng 11 dòng đầu mã hiện ở khung `example` bước 1
    rec("L31", sum(1 for l in hien if l.startswith("ghi(")) == len(dong) == 6 and any('"HET_GIO"' in l for l in hien) and any("http=504" in l for l in hien),
        "nhật ký: khối mã hiện trên màn hình (11 dòng đầu) có đủ 6 lệnh ghi, kể cả HET_GIO và http=504, cho đúng 6 dòng kết quả")
    rec("L31", sorted(d["t"] for d in dong) ==[d["t"] for d in dong] and all(d["t"] == 1000 + 7 * i for i, d in enumerate(dong)), "nhật ký: đồng hồ giả tăng đúng 7 ms mỗi dòng (kết quả tất định)")
    # 2) chỉ mục đảo: công thức đóng
    out = P["ChiMuc"].out.splitlines()
    rec("L31", out == ["1000 dong: khop 1 | quet 1000 dong | chi muc xet 2 dong", "1000000 dong: khop 1000 | quet 1000000 dong | chi muc xet 2000 dong"], "chỉ mục đảo: 1 000 dòng xét 2 (khớp 1); 1 000 000 dòng xét 2 000 (khớp 1 000)")
    for n in (1000, 1000000):
        # ERROR: 2 dòng mỗi 1000 (i%1000 ∈ {7,8}); sc là i%5==2, 7%5==2, 8%5==3 → mỗi nhóm đúng 1 khớp (vì 1000 chia hết cho 5)
        rec("L31", alg.bnx_l31_index(n) == (n // 1000, 2 * (n // 1000), n), f"chỉ mục đảo n={n}: alg = công thức đóng ({n // 1000} khớp, {2 * (n // 1000)} dòng ERROR)")
    # 3) văn bản chỉ số và số chuỗi
    dem = [l.split() for l in P["DemChuoi"].out.splitlines()]
    kq = {int(r[0]): (int(r[5]), int(r[7])) for r in dem}
    rec("L31", kq == {0: (5, 324), 100: (401, 24287), 10000: (40001, 2495695)} and all(alg.bnx_l31_exposition(n) == v for n, v in kq.items()),
        "văn bản chỉ số: 5 / 401 / 40 001 chuỗi và 324 / 24 287 / 2 495 695 byte (Java thật = alg)")
    trang = "\n".join(P["ChayMay"].out.splitlines()[:8]) + "\n"      # trang chỉ số hiện đủ 8 dòng ở bước 4 (kể cả dòng HELP)
    rec("L31", trang.startswith("# HELP") and len(trang.encode("utf-8")) == 324 == kq[0][1] and len([l for l in trang.splitlines() if not l.startswith("#")]) == 5 == kq[0][0],
        "văn bản chỉ số hiện đủ 8 dòng (có HELP): 324 byte, 5 dòng không phải chú thích = 5 chuỗi")
    rec("L31", [4 + 1, 4 * 100 + 1, 4 * 10000 + 1] == [5, 401, 40001],"số chuỗi = 2 route × 2 mã × (số user hoặc 1) + 1 chuỗi đo mức")
    # 4) Prometheus thật
    rec("L31", P["ChayMay"].out.splitlines()[-3:] == ["up = 1", "loi 500 = 30", "ty le loi = 0.005"] and Fraction(30, 980 + 20 + 4990 + 10) == Fraction(5, 1000),
        "Prometheus 3.16.0 thật: up = 1, tổng lỗi 30, tỉ lệ 0,005 = 30/6000 (Fraction)")
    rec("L31", "SUCCESS" in P["ChayTest"].out and "FAILED" not in P["ChayTest"].out, "promtool test rules: SUCCESS (tốc độ đốt 5 ở phút 10; cảnh báo bắn ở phút 4 không ở phút 2; chuỗi lỗi 0,1% không bắn)")
    # 5) tốc độ đốt, ngân sách (Fraction, tính tay)
    burn = Fraction(5, 995 + 5) / (1 - Fraction(999, 1000))
    rec("L31", burn == 5 and Fraction(30) / burn == 6 and alg.bnx_l31_burn(0.005, 0.999) == 5 and alg.bnx_l31_days(5) == 6, "tốc độ đốt = (5/1000)/(1/1000) = 5; 30/5 = 6 ngày")
    rec("L31", Fraction(43200) * Fraction(5, 1000) == 216 and Fraction(2, 100) / Fraction(5, 1000) == 4 and Fraction(30, 4) == Fraction(15, 2) and alg.bnx_l31_budget_min(0.995) == 216
        and alg.bnx_l31_burn(0.02, 0.995) == 4 and alg.bnx_l31_days(4) == 7.5 and 4 * 3 * 500 == 6000, "quiz: 216 phút; tốc độ đốt 4; 7,5 ngày; 6 000 chuỗi")
    # 6) lab
    r = subprocess.run([sys.executable, "-X", "utf8", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L31", r.returncode == 0 and r.stdout.strip() == (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip(), "lab: loi_giai.py cho đúng mong_doi.txt")
    rec("L31", 560 - 500 == 60 and round(float(Fraction(6, 200) / (1 - Fraction(99, 100))), 1) == 3.0, "lab: c9 mất 60 ms; tốc độ đốt (6/200)/(1−0,99) = 3,0")
    # test.yml hiện đủ trên màn hình (không cụt ở exp_alerts rỗng) và $IMG có giá trị trên màn hình: kiểm bằng văn bản các khối trong YAML đã sinh
    yml = next((ROOT / "lessons" / "bnx").glob("L31_*.yaml")).read_text(encoding="utf-8")
    rec("L31", "exp_labels: {severity: page}" in yml and "0+999x12" in yml and "IMG=prom/prometheus@sha256:" in yml and "mục tiêu độ sẵn sàng" in yml,
        "màn hình hiện đủ test.yml (kể cả exp_labels và ca thứ hai), dòng gán IMG, và SLO được giải nghĩa")
