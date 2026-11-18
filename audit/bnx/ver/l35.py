"""Kiểm độc lập BNX L35 (Vận hành và tài liệu). Đường khác với tools/checklib_bnx/l35.py (dùng Decimal):
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình (Python 3 thuần) và so từng ký tự với đầu ra đã hiện;
- mọi con số tính lại bằng PHÂN SỐ (fractions.Fraction) và bằng đếm từng phút (vòng lặp), không dùng Decimal;
- phiếu sự cố phân tích bằng yaml.safe_load; danh mục kiểm bản thiết kế tính lại bằng biểu thức chính quy;
- lab giấy bút: mọi dòng của mong_doi.txt phải có trong loi_giai.md và khớp phép tính lại bằng Fraction."""
import re
import sys
from fractions import Fraction as F
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l35 as src  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L35"


def phut(ngay):
    return sum(1 for _ in range(ngay * 24 * 60))


def run(rec):
    lib2.verify_programs(rec, "L35")
    P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L35"}
    th = phut(30)
    rec("L35", th == 43200, "tháng 30 ngày = 43 200 phút (đếm từng phút)")
    bud = {m: th * (1 - F(m) / 100) for m in ("99", "99.9", "99.95", "99.99")}
    rec("L35", [float(v) for v in bud.values()] == [432.0, 43.2, 21.6, 4.32] and [alg.bnx_l35_budget(m, 30) for m in bud] == [432, 43.2, 21.6, 4.32], "ngân sách ngừng 432; 43,2; 21,6; 4,32 phút (Fraction = alg)")
    rec("L35", P["NganSach"].out.splitlines() == [f"{m}% mot thang 30 ngay: toi da {str(alg.bnx_l35_budget(m, 30)).rstrip('0').rstrip('.')} phut ngung" for m in bud], "đầu ra NganSach khớp bốn ngân sách")
    chain = F(9995, 10000) * F(999, 1000) * F(999, 1000)
    rec("L35", round(float(chain), 6) == 0.997502 == alg.bnx_l35_chain(["0.9995", "0.999", "0.999"]) and f"{float(chain) * 100:.4f}" == "99.7502", "ba dịch vụ nối tiếp: 99,7502% (Fraction = alg)")
    rec("L35", f"{float(th * (1 - chain)):.2f}" == "107.91" and P["ChuoiPhuThuoc"].out.splitlines()[1] == "ngan sach neu cam ket chung: 107.91 phut/thang", "ngân sách nếu cam kết chung: 107,91 phút")
    ngan_sach = th * F(1, 10) / 100
    tong = 12 + 30 + 5
    rec("L35", ngan_sach == F(216, 5) and tong - ngan_sach == F(19, 5) and float(100 - F(tong, th) * 100) > 99.8911 and alg.bnx_l35_over(tong, 43.2) == 3.8, "sự cố 47 phút vượt ngân sách 43,2 một khoảng 3,8 phút; sẵn sàng thực tế 99,8912%")
    rec("L35", P["SuCoThang"].out.splitlines() == ["su co: 12 + 30 + 5 = 47 phut; ngan sach 43.2 phut", "san sang thuc te: 99.8912%", "vuot ngan sach 3.8 phut"], "đầu ra SuCoThang khớp")
    lines = P["QuyMoChuoi"].out.splitlines()
    exp = []
    for n in (1, 100, 10000):
        a = F(999, 1000) ** n
        exp.append((n, float(a) * 100, float(th * (1 - a))))
    ok = all(abs(float(re.search(r": ([\d.]+)% ;", l).group(1)) - e[1]) < 5e-5 and abs(float(re.search(r"toi da ([\d.]+) phut", l).group(1)) - e[2]) < 0.06 for l, e in zip(lines, exp))
    rec("L35", ok and [round(e[1], 4) for e in exp] == [99.9, 90.4792, 0.0045], "quy mô chuỗi 1, 100, 10 000 dịch vụ: 99,9%; 90,4792%; 0,0045% (Fraction)")
    rec("L35", alg.bnx_l35_chain(["0.999"] * 100) == 0.904792 and alg.bnx_l35_chain(["0.999"] * 100, 4) == 0.9048, "alg khớp ở 100 dịch vụ")
    tk = yaml.safe_load(P["PhieuSuCo"].code)
    rec("L35", all(k in tk for k in ("ma", "muc", "anh_huong", "bang_chung", "buoc_tai_hien", "hanh_dong_tam_thoi", "nguoi_nhan", "han_phan_hoi")), "phiếu sự cố phân tích được, đủ 8 trường")
    code = P["KiemTaiLieu"].code
    tot = re.search(r'TOT = """(.*?)"""', code, re.S).group(1)
    xau = re.search(r'XAU = """(.*?)"""', code, re.S).group(1)

    def kiem_re(vb):
        loi = [f"thieu {m}" for m in ("Boi canh", "Quyet dinh", "He qua") if not re.search(r"^## " + m, vb, re.M)]
        if not re.search(r"Chung toi se", vb):
            loi.append("quyet dinh khong viet 'Chung toi se ...'")
        if not re.search(r"Tieu cuc", vb):
            loi.append("he qua khong neu mat tieu cuc")
        return loi
    rec("L35", kiem_re(tot) == [] and len(kiem_re(xau)) == 5 and P["KiemTaiLieu"].out.splitlines()[:2] == ["tot: dat", "xau: 5 loi"], "danh mục kiểm (regex): bản tốt đạt, bản xấu 5 lỗi")
    p2 = P["Phanso"].out.splitlines()
    rec("L35", p2 == ["216/5", "0.002498", "43200"] and F(216, 5) == F("43.2"), "phân số: 216/5, 0,002498, 43200 phút")
    q1 = th * (1 - F("99.95") / 100)
    rec("L35", q1 == F(108, 5) and q1 - (8 + 15) == F(-7, 5) and alg.bnx_l35_budget("99.95", 30) == 21.6 and alg.bnx_l35_over(23, 21.6) == 1.4 and round(float(F(999, 1000) * F(998, 1000)), 4) == 0.997, "quiz: 21,6 phút, vượt 1,4; 0,999 × 0,998 = 0,9970 < 0,999")
    t31 = phut(31)
    lab = {"ns": t31 * (1 - F("99.8") / 100), "chuoi": F("0.999") * F("0.995"), "vuot": (20 + 75) - t31 * (1 - F("99.8") / 100)}
    md = (LAB / "loi_giai.md").read_text(encoding="utf-8")
    want = (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip().splitlines()
    rec("L35", t31 == 44640 and float(lab["ns"]) == 89.28 and f"{float(lab['chuoi']) * 100:.4f}" == "99.4005" and float(lab["vuot"]) == 5.72, "lab: 44 640 phút, ngân sách 89,28; chuỗi 99,4005%; vượt 5,72 (Fraction)")
    rec("L35", all(l in md for l in want) and want[0] == "ngan sach 99.8% thang 31 ngay: 89.28 phut" and want[1] == "chuoi 99.9% va 99.5%: 99.4005%" and want[2] == "su co 20 + 75 = 95 phut: vuot ngan sach 5.72 phut", "lab: mọi dòng đáp án có trong loi_giai.md và khớp phép tính")
    # ── phần thêm trong đợt sửa theo báo cáo người đọc ──
    ola = F(9995, 10000) * F(9995, 10000)
    rec("L35", ola == F("0.99900025") and ola >= F(999, 1000) and float(ola) > 0.999, "OLA nội bộ: 0,9995 × 0,9995 = 0,99900025 ≥ 0,999 (đủ giữ SLA 99,9%)")
    hook3 = F(999, 1000) * F(9995, 10000) * F(999, 1000)
    ba_dv_999 = F(999, 1000) ** 3
    rec("L35", f"{float(hook3) * 100:.4f}" == "99.7502" and f"{float(ba_dv_999) * 100:.4f}" == "99.7003" and hook3 == chain, "hook: dịch vụ 99,9% nối tiếp 99,95% và 99,9% = 99,7502% (khác 3 × 99,9% = 99,7003%)")
    rec("L35", 9 * 60 + 10 + 30 == 9 * 60 + 40 and F(15, 100) * 20 == 3 and F(5, 100) * 20 == 1, "ca sự cố: báo 09:10 + hạn 30 phút = 09:40; p95 = 1 trong 20 yêu cầu chậm hơn")
    txt = next((ROOT / "lessons" / "bnx").glob("L35_*.yaml")).read_text(encoding="utf-8")
    rong = [1380 * float(b) / 432 for b in (432, F("43.2"), F("21.6"), F("4.32"))]
    rec("L35", [round(x) for x in rong] == [1380, 138, 69, 14] and all(f'width="{w}"' in txt or f"width='{w}'" in txt or str(w) in txt for w in (1380, 138, 69, 14)),
        "hình 1: độ dài thanh đúng tỉ lệ 432 : 43,2 : 21,6 : 4,32 = 1380 : 138 : 69 : 14")
    de = (LAB / "de.md").read_text(encoding="utf-8")
    rec("L35", "Danh mục kiểm" in de and "cham.sh" in de and "(b) câu quyết định bắt đầu bằng" in de, "lab: de.md nêu danh mục kiểm ngay trong đề và nói cham.sh không chấm .md")
    # ── vòng fix4: giả định tính sự cố, in dòng quy mô, ngân sách 10 lần ──
    rec("L35", F(12 + 30) < F("43.2") < F(12 + 30 + 5) and "Nếu sự cố P3 (5 phút) không tính: 12 + 30 = 42" in " ".join(txt.split()),"giả định P3: bỏ sự cố 5 phút thì 42 < 43,2 (chưa vượt); tính cả ba thì 47 > 43,2; bài nêu rõ giả định")
    rec("L35", F("43.2") / 10 == F("4.32") and F("432") / 10 == F("43.2") and "nhiều hơn 10 lần" not in txt and "tăng hơn mười lần" not in txt, "mỗi chữ số 9 chia ngân sách cho 10 (phép tính); bỏ khẳng định chi phí 'hơn 10 lần' không có nguồn")
