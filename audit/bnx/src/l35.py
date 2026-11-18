import lib2
from lib2 import *
from spoken_b import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from libj import jstep
from labkit import write_lab, practice_steps, practice_scene

lib2.begin("L35")

# ── Mã chạy THẬT: Python 3 (Decimal, chuỗi). Số đo là phép tính tất định; không có sản phẩm ngoài. Đệm ở audit/bnx/progcache/L35.json ──
PY_SLA = prog("NganSach", r'''
from decimal import Decimal as D

THANG = 30 * 24 * 60                      # 43 200 phút trong tháng 30 ngày
for muc in ("99", "99.9", "99.95", "99.99"):
    ns = THANG * (100 - D(muc)) / 100
    print(f"{muc}% mot thang 30 ngay: toi da {ns.normalize():f} phut ngung")
''', lang="python", claims=["ngân sách ngừng tối đa: 99% → 432 phút; 99,9% → 43,2; 99,95% → 21,6; 99,99% → 4,32"])

PY_CHUOI = prog("ChuoiPhuThuoc", r'''
from decimal import Decimal as D

THANG = 30 * 24 * 60
ba = D("0.9995") * D("0.999") * D("0.999")
print(f"3 dich vu noi tiep (99.95, 99.9, 99.9): {ba * 100:.4f}%")
print(f"ngan sach neu cam ket chung: {THANG * (1 - ba):.2f} phut/thang")
''', lang="python", claims=["ba dịch vụ nối tiếp 99,95%, 99,9%, 99,9% cho 99,7502%; ngân sách 107,91 phút"])

PY_SUCO = prog("SuCoThang", r'''
from decimal import Decimal as D

THANG = 30 * 24 * 60
ngan_sach = THANG * D("0.1") / 100         # SLA 99,9% → 43,2 phút
su_co = [(12, "P2"), (30, "P1"), (5, "P3")]
tong = sum(p for p, _ in su_co)
cac = " + ".join(str(p) for p, _ in su_co)
print(f"su co: {cac} = {tong} phut; ngan sach {ngan_sach} phut")
print(f"san sang thuc te: {100 - D(tong) / THANG * 100:.4f}%")
kq = "vuot ngan sach" if tong > ngan_sach else "con trong ngan sach"
print(kq, f"{abs(tong - ngan_sach)} phut")
''', lang="python", claims=["sự cố 12 + 30 + 5 = 47 phút vượt ngân sách 43,2 phút của SLA 99,9% một khoảng 3,8 phút"])

PY_QUYMO = prog("QuyMoChuoi", r'''
from decimal import Decimal as D, getcontext

getcontext().prec = 50
THANG = 30 * 24 * 60
for n in (1, 100, 10000):
    a = D("0.999") ** n
    print(f"{n} dich vu 99.9% noi tiep: {a * 100:.4f}% ; "
          f"ngung toi da {THANG * (1 - a):.1f} phut/thang")
''', lang="python", claims=["chuỗi dịch vụ 99,9%: 1 → 99,9%; 100 → 90,4792%; 10000 → 0,0045%"])

PY_TL = prog("KiemTaiLieu", r'''
TOT = """# ADR 7: Dung hang doi cho thong bao sao ke
Trang thai: Da duyet
## Boi canh
Sao ke dem co 2 trieu dong; goi truc tiep tung tin se nghen cong SMS.
## Quyet dinh
Chung toi se dua tin vao hang doi va gui theo toc do cong cho phep.
## He qua
Tich cuc: cong SMS khong bi nghen. Tieu cuc: tin den tre toi 15 phut.
"""
XAU = """# Thiet ke thong bao
Dung hang doi cho nhanh.
"""

def kiem(vb):
    loi = []
    for muc in ("## Boi canh", "## Quyet dinh", "## He qua"):
        if muc not in vb:
            loi.append("thieu " + muc[3:])
    if "Chung toi se" not in vb:
        loi.append("quyet dinh khong viet 'Chung toi se ...'")
    if "Tieu cuc" not in vb:
        loi.append("he qua khong neu mat tieu cuc")
    return loi

for ten, vb in (("tot", TOT), ("xau", XAU)):
    loi = kiem(vb)
    print(f"{ten}:", "dat" if not loi else f"{len(loi)} loi")
    for x in loi:
        print("  " + x)
''', lang="python", claims=["bản tốt đạt; bản xấu thiếu 3 mục và các yêu cầu khác"])

# ── Lab (loi_giai.md; lab_gate kiểm mọi dòng của mong_doi.txt có trong lời giải): SLA tháng 31 ngày ──
LAB_MD = """# Lời giải lab BNX L35

Tháng 31 ngày có 31 × 24 × 60 = 44 640 phút.

1. Ngân sách ngừng của SLA 99,8%: 44 640 × (100 − 99,8) : 100 = 89,28 phút.
   ngan sach 99.8% thang 31 ngay: 89.28 phut
2. Chuỗi hai dịch vụ nối tiếp 99,9% và 99,5%: 0,999 × 0,995 = 0,994005.
   chuoi 99.9% va 99.5%: 99.4005%
3. Hai sự cố 20 và 75 phút: 20 + 75 = 95 phút; 95 − 89,28 = 5,72 phút.
   su co 20 + 75 = 95 phut: vuot ngan sach 5.72 phut
4. Tài liệu thiết kế có đủ ba mục Bối cảnh, Quyết định, Hệ quả; quyết định viết "Chúng tôi sẽ …"; hệ quả nêu cả mặt tiêu cực.
   tai lieu thiet ke: du 3 muc, quyet dinh chu dong, he qua co mat tieu cuc

## Khung tài liệu thiết kế mẫu

```
# ADR <số>: <cụm danh từ ngắn>
Trạng thái: Đã duyệt
## Bối cảnh      (sự thật và lực kéo, trung lập)
## Quyết định    (Chúng tôi sẽ …)
## Hệ quả        (tích cực, tiêu cực, trung tính)
```
"""
LAB_OUT = """ngan sach 99.8% thang 31 ngay: 89.28 phut
chuoi 99.9% va 99.5%: 99.4005%
su co 20 + 75 = 95 phut: vuot ngan sach 5.72 phut
tai lieu thiet ke: du 3 muc, quyet dinh chu dong, he qua co mat tieu cuc"""
LAB_DE = """# Lab BNX L35 — Ngân sách SLA và khung tài liệu thiết kế (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, và `cham.sh` không chấm tệp `.md`. Tính tay, ghi từng dòng đáp án đúng định dạng dưới đây, rồi tự so với `loi_giai.md` (đáp án và cách tính).

Số liệu (số minh hoạ): tháng **31 ngày**; SLA **99,8%**; hai dịch vụ nối tiếp **99,9%** và **99,5%**; trong tháng có **hai sự cố 20 phút và 75 phút**.

Viết bốn dòng:
1. `ngan sach 99.8% thang 31 ngay: <số> phut` — số phút ngừng tối đa trong tháng.
2. `chuoi 99.9% va 99.5%: <số>%` — độ sẵn sàng chung khi hai dịch vụ nối tiếp (nhân hai tỉ lệ), 4 chữ số sau dấu phẩy.
3. `su co 20 + 75 = <tổng> phut: vuot ngan sach <số> phut` (hoặc `con trong ngan sach` nếu không vượt).
4. Viết khung tài liệu thiết kế một trang cho quyết định "dùng hàng đợi cho thông báo sao kê": ba mục **Bối cảnh, Quyết định, Hệ quả**; câu quyết định bắt đầu bằng "Chúng tôi sẽ"; hệ quả nêu cả mặt tiêu cực. **Danh mục kiểm** (tự chấm, có ngay ở đây): (a) có đủ ba mục Bối cảnh, Quyết định, Hệ quả; (b) câu quyết định bắt đầu bằng "Chúng tôi sẽ"; (c) hệ quả nêu cả mặt tiêu cực. Đạt cả ba thì ghi dòng `tai lieu thiet ke: du 3 muc, quyet dinh chu dong, he qua co mat tieu cuc`. Khung mẫu nằm ở cuối `loi_giai.md`.
"""

PY_FRAC = prog("Phanso", r'''
from fractions import Fraction as F

thang = 30 * 24 * 60
print(thang * (1 - F(999, 1000)))
print(f"{float(1 - F(9995, 10000) * F(999, 1000) ** 2):.6f}")
print(sum(1 for _ in range(thang)))
''', lang="python", claims=["phân số: ngân sách 216/5 = 43,2 phút; tỉ lệ ngừng của chuỗi 0,002498; 43200 phút"])


X_TICKET = prog("PhieuSuCo", r'''
ma: PRD-1042
muc: P2
tom_tat: Tra cuu so du cham tren ung dung
anh_huong: khach le, khoang 15 phan tram yeu cau, tu 09:10
bang_chung:
  - nhat_ky: ma tuong quan 7f3a
  - chi_so: p95 do tre 4,2 giay (binh thuong 0,8)
buoc_tai_hien: goi dich vu so du voi tai khoan co nhieu giao dich
hanh_dong_tam_thoi: tang so ban dich vu tu 3 len 5
nguoi_nhan: ho tro muc 3
han_phan_hoi: 15 phut
''', lang="yaml", kind="other", reason="Phiếu sự cố môi trường thật (ví dụ minh hoạ, số minh hoạ): các trường cần để người nhận không phải hỏi lại.",
    read_check="Phân tích được bằng yaml.safe_load (cổng làm khi kind other + lang yaml); đây là mẫu của bài, không phải mẫu của tổ chức nào.")


lib2.other("ngan sach 99.8% thang 31 ngay", kind="other", lang="text", reason="Đáp án của lab giấy bút L35 (labs/BNX/L35/mong_doi.txt).",
           read_check="Cổng labs/lab_gate (loại .md) kiểm mọi dòng của mong_doi.txt có trong loi_giai.md; audit/bnx/ver/l35.py tính lại bốn số bằng Fraction (89,28; 99,4005%; 95 phút, vượt 5,72).")


def build():
    write_lab("BNX", "L35", LAB_DE, "md", LAB_MD, LAB_OUT)
    hook = sc("hook", "hook", "99,9% nghe thì cao, nhưng một tháng chỉ cho phép 43 phút ngừng", [
        st("""<p>Hợp đồng ghi dịch vụ sẵn sàng <b>99,9%</b>. Trong tháng có ba sự cố: <b>12, 30 và 5 phút</b>.</p>
<div class="box key">Một tháng 30 ngày có 43 200 phút; 99,9% nghĩa là ngừng tối đa <b>43,2 phút</b>. Ba sự cố cộng lại <b>47 phút</b>: <b>vượt 3,8 phút</b> (giả sử hợp đồng tính cả ba sự cố vào phút ngừng).
Và nếu dịch vụ này nối tiếp với hai dịch vụ khác, 99,95% và 99,9%, độ sẵn sàng chung còn bao nhiêu?</div>""",
           """Chào bạn, hợp đồng ghi chín mươi chín phẩy chín phần trăm sẵn sàng, mà tháng có ba sự cố, mười hai, ba mươi và năm phút. Tháng ba mươi ngày có bốn mươi ba nghìn hai trăm phút, nên mức này cho ngừng tối đa bốn mươi ba phẩy hai phút, còn ba sự cố cộng bốn mươi bảy phút, vượt ba phẩy tám. Nối tiếp với hai dịch vụ khác thì độ sẵn sàng chung còn bao nhiêu?""", focus=[1, 2, 2, 2, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["SLA, SLO, SLI, OLA khác nhau thế nào", "<b>chỉ số</b> (SLI) đo; <b>mục tiêu</b> (SLO) đặt; <b>thoả thuận</b> (SLA) có hệ quả khi trượt; <b>thoả thuận nội bộ</b> (OLA) giữa các đội"],
                  ["99,9% là bao nhiêu phút", "<b>ngân sách ngừng</b> = số phút trong tháng × (100 − tỉ lệ) : 100"],
                  ["hỗ trợ mức 3 và phiếu sự cố", "ai nhận khi mức 1–2 không giải quyết được; phiếu phải đủ chứng cứ để khỏi hỏi lại"],
                  ["bản thiết kế cần gì", "<b>bối cảnh – quyết định – hệ quả</b>, chấm bằng danh mục kiểm"]]),
           """Hôm nay ta trả lời bốn câu: các chữ viết tắt khác nhau thế nào, chín mươi chín phẩy chín phần trăm là bao nhiêu phút, phiếu sự cố cần gì, và bản thiết kế cần gì.""",
           focus=[0], clear=True),
    ], checks=["alg.bnx_l35_budget('99.9', 30) == 43.2", "12 + 30 + 5 == 47 and alg.bnx_l35_over(47, alg.bnx_l35_budget('99.9', 30)) == 3.8",
               "alg.bnx_l35_chain(['0.999', '0.9995', '0.999']) == 0.997502"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① độ sẵn sàng", "phần trăm thời gian dịch vụ hoạt động được", "99,9% một tháng"],
                  ["② sự cố", "lúc dịch vụ không đạt yêu cầu; có mức độ nặng nhẹ", "ứng dụng tra số dư không trả lời"],
                  ["③ hỗ trợ theo mức", "mức 1 nhận tin; mức 2 xử lý theo kịch bản; <b>mức 3</b> là kỹ sư sửa mã, cấu hình", "mức 3 mới đọc được nhật ký sâu"],
                  ["④ môi trường thật và môi trường kiểm thử", "môi trường thật có khách thật; môi trường kiểm thử để thử trước, không có khách", "thử bản sửa ở kiểm thử rồi mới lên thật"],
                  ["⑤ nhà cung cấp", "bên ngoài cung cấp một phần dịch vụ; bên mình phụ thuộc vào họ", "cổng thanh toán của đối tác"]]),
           """Trước hết ta cần hiểu năm điều. Độ sẵn sàng là phần trăm thời gian dịch vụ hoạt động được, sự cố là lúc dịch vụ không đạt yêu cầu. Hỗ trợ mức một nhận tin, mức hai xử lý theo kịch bản, mức ba là kỹ sư sửa mã. Môi trường kiểm thử để thử trước khi lên môi trường thật. Nhà cung cấp là bên ngoài mà mình phụ thuộc.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["alg.bnx_l35_budget('99', 30) == 432"])

    sym = sc("sym", "symbol", "Giải mã các chữ viết tắt trên màn hình", [
        st(table(["chữ", "nghĩa"],
                 [["SLI", "chỉ số mức dịch vụ: con số <b>đo</b> được, như tỉ lệ yêu cầu thành công"],
                  ["SLO", "mục tiêu mức dịch vụ: giá trị <b>đặt</b> cho chỉ số, như ≥ 99,9%"],
                  ["SLA", "thoả thuận mức dịch vụ: hợp đồng <b>có hệ quả</b> khi không đạt mục tiêu"],
                  ["OLA", "thoả thuận mức vận hành: thoả thuận <b>giữa các đội trong nội bộ</b> để đạt SLA"],
                  ["P1…P4", "mức độ sự cố do tổ chức quy định; P1 nặng nhất"],
                  ["ADR", "bản ghi quyết định thiết kế: một trang gồm bối cảnh, quyết định, hệ quả"],
                  ["API, cổng API", "API: cách một chương trình nhờ chương trình khác làm việc, bằng yêu cầu và trả lời. <b>Cổng API</b>: cửa chung mà mọi yêu cầu từ ngoài đi qua trước khi vào các dịch vụ"],
                  ["mã tương quan", "chuỗi ký tự gắn vào một yêu cầu và có mặt ở mọi dòng nhật ký của yêu cầu đó, để tìm lại hành trình của nó; ví dụ <code>7f3a</code>"],
                  ["đối soát", "so hai sổ ghi cùng một việc để tìm dòng lệch; ví dụ sổ ngân hàng so với sổ đối tác thanh toán"]]),
           """Bảng này giải mã các chữ viết tắt: chỉ số là con số đo được, mục tiêu là giá trị đặt cho nó. Thoả thuận với khách có hệ quả khi không đạt, thoả thuận nội bộ là giữa các đội. Cổng API là cửa chung mọi yêu cầu đi qua, mã tương quan giúp tìm lại hành trình của một yêu cầu, và đối soát là so hai sổ để tìm dòng lệch.""",
           focus=[0, "1.2", "1.4", "1.6", "1.8", "1.9", "1.10"]),
    ], checks=["alg.bnx_l35_budget('99.95', 30) == 21.6"])

    intu = sc("intuition", "intuition", "Hình dung: ngân sách ngừng và dịch vụ nối tiếp", [
        st(svg(1500, 520,
               txt(750, 40, "Một tháng 43 200 phút: ngân sách ngừng của mỗi mức (thanh vẽ đúng tỉ lệ)", 26, "middle", "#1f2937", True),
               box(60, 110, 1380, 60, "99%: 432 phút", C_RED, 24, True),
               box(60, 190, 138, 60, "", C_AMBER, 24, True), txt(218, 232, "99,9%: 43,2 phút", 24, "start", "#92400e", True),
               box(60, 270, 69, 60, "", C_AMBER, 20, True), txt(149, 312, "99,95%: 21,6 phút", 24, "start", "#92400e", True),
               box(60, 350, 14, 60, "", C_GREEN, 20, True), txt(94, 392, "99,99%: 4,32 phút", 24, "start", "#16a34a", True),
               txt(750, 470, "Mỗi chữ số 9 thêm vào chia ngân sách cho 10 (phép tính); chi phí để đạt thường tăng thêm, mức tăng tuỳ hệ thống", 24, "middle", "#1f2937", True)),
           """Hình này là ngân sách ngừng trong một tháng bốn mươi ba nghìn hai trăm phút, thanh vẽ đúng tỉ lệ. Chín mươi chín phần trăm cho bốn trăm ba mươi hai phút, chín mươi chín phẩy chín cho bốn mươi ba phẩy hai. Chín mươi chín phẩy chín lăm cho hai mươi mốt phẩy sáu, chín mươi chín phẩy chín chín cho bốn phẩy ba hai. Thêm một chữ số chín thì thanh ngắn đi mười lần."""),
        st(svg(1500, 460,
               txt(750, 40, "Dịch vụ nối tiếp: mọi mắt xích phải sống thì cả chuỗi mới sống", 26, "middle", "#1f2937", True),
               box(60, 130, 280, 90, ["cổng API", "99,95%"], C_BLUE, 24, True), box(430, 130, 280, 90, ["dịch vụ lõi", "99,9%"], C_BLUE, 24, True),
               box(800, 130, 280, 90, ["đối tác", "99,9%"], C_AMBER, 24, True),
               arrow(345, 175, 425, 175), arrow(715, 175, 795, 175),
               box(1170, 130, 270, 90, ["chung:", "99,7502%"], C_RED, 24, True),
               arrow(1085, 175, 1165, 175),
               txt(750, 300, "độ sẵn sàng chung = tích các độ sẵn sàng: 0,9995 × 0,999 × 0,999", 24, "middle", "#1f2937", True),
               txt(750, 350, "luôn thấp hơn mắt xích yếu nhất; thêm mắt xích thì tụt thêm", 24, "middle", "#dc2626", True),
               txt(750, 410, "hình này tính đúng khi các lỗi độc lập; lỗi chung (cùng một hạ tầng) làm số thật khác", 22, "middle", "#475569")),
           """Hình thứ hai là dịch vụ nối tiếp: mọi mắt xích phải sống thì cả chuỗi mới sống. Độ sẵn sàng chung bằng tích, ở đây chín mươi chín phẩy bảy năm không hai phần trăm, thấp hơn mắt xích yếu nhất. Tính vậy chỉ đúng khi các lỗi độc lập."""),
    ], checks=["[alg.bnx_l35_budget(a, 30) for a in ('99', '99.9', '99.95', '99.99')] == [432, 43.2, 21.6, 4.32]",
               "alg.bnx_l35_chain(['0.9995', '0.999', '0.999']) == 0.997502"])

    form = sc("formula", "formula", "Suy ra từng bước: từ cam kết tới việc phải làm", [
        st("""<p><b>Bước 1. Bốn chữ cái.</b> Muốn nói về &laquo;dịch vụ tốt&raquo; mà không cãi nhau, ta tách bốn việc (ví dụ cho dịch vụ chuyển tiền, số minh hoạ):</p>"""
           + table(["việc", "chữ", "ví dụ"],
                   [["đo", "SLI", "tỉ lệ yêu cầu chuyển tiền thành công"],
                    ["đặt", "SLO", "tỉ lệ ấy ≥ 99,9% mỗi tháng"],
                    ["cam kết với khách, có hệ quả", "SLA", "99,9%; trượt thì hoàn phí"],
                    ["cam kết nội bộ giữa các đội", "OLA", "hạ tầng 99,95% và cơ sở dữ liệu 99,95%: 0,9995 × 0,9995 = 0,99900025 ≥ 0,999"]]),
           """Bước một là bốn chữ cái, vì muốn nói về dịch vụ tốt mà không cãi nhau ta tách bốn việc. Đo là chỉ số, đặt là mục tiêu, cam kết với khách có hệ quả khi trượt, như hoàn phí. Cam kết nội bộ là các đội hứa với nhau: hạ tầng và cơ sở dữ liệu mỗi đội chín mươi chín phẩy chín lăm, nhân nhau vẫn đủ giữ lời hứa với khách.""",
           clear=True),
        jstep([(("<code>from decimal import Decimal as D</code>, <code>D(\"0.9995\") * D(\"0.999\")</code>", "nạp kiểu số thập phân, gọi tắt <code>D</code>: giữ đúng từng chữ số, không sai số làm tròn; <code>*</code> nhân hai số <code>D</code>", "Kiểu số thập phân, gọi tắt bằng chữ D, giữ đúng từng chữ số."), "<code>D(\"0.5\") * D(\"0.5\")</code> ra <code>0.25</code>", ""),
               (("<code>for muc in (\"99\", \"99.9\"):</code>", "mỗi vòng <code>muc</code> nhận một giá trị trong dãy; các dòng thụt vào là thân vòng", "Vòng lặp cho biến nhận lần lượt từng giá trị trong dãy."), "", ""),
               (("<code>{ns.normalize():f}</code>, <code>{x:.4f}</code>", "trong chuỗi f (phần trong ngoặc nhọn thay bằng giá trị): <code>normalize()</code> bỏ chữ số 0 thừa cuối, có thể ra <code>4.32E+2</code>; <code>:f</code> ép in dạng thường <code>432</code>; <code>:.4f</code>: đúng 4 chữ số sau dấu chấm thập phân, chữ số cuối làm tròn", "Trong chuỗi f, đuôi f in dạng thường, đuôi chấm bốn f giữ bốn chữ số sau dấu thập phân."), "<code>3.8</code> với <code>:.4f</code> in <code>3.8000</code>", ""),
               (("<code>print(f\"…\")</code>, <code>#</code>", "in một dòng ra màn hình; từ <code>#</code> tới hết dòng là ghi chú, máy bỏ qua", "Lệnh in đưa một dòng ra màn hình, còn dấu thăng mở đầu ghi chú."), "", "")],
              intro="Mã tính ngân sách có bốn ký hiệu nên ta đọc trước."),
        st("""<p><b>Bước 2. Ngân sách ngừng.</b> Số phút ngừng tối đa = số phút trong tháng × (100 − tỉ lệ) : 100.</p>"""
           + PY_SLA.show(lines=(1, 7), title="NganSach.py")
           + """$$43\\,200 \\times (100 - 99{,}9) : 100 = \\hl{43{,}2} \\text{ phút}$$""",
           """Bước hai là ngân sách ngừng. Số phút ngừng tối đa bằng số phút trong tháng nhân phần trăm còn lại, vì phần còn lại là phần được phép hỏng.
           Với chín mươi chín phẩy chín phần trăm, bốn mươi ba nghìn hai trăm nhân không phẩy một phần trăm là bốn mươi ba phẩy hai phút.""",
           clear=True),
        st("""<p><b>Bước 3. Nối tiếp thì nhân.</b> Yêu cầu đi qua nhiều dịch vụ, mỗi dịch vụ phải sống: độ sẵn sàng chung = tích. Dịch vụ càng nhiều, số càng tụt.</p>"""
           + PY_CHUOI.show(lines=(1, 6), title="ChuoiPhuThuoc.py")
           + """$$0{,}9995 \\times 0{,}999 \\times 0{,}999 = \\hl{0{,}997502}$$""",
           """Bước ba là nối tiếp thì nhân, vì mỗi dịch vụ trên đường đi đều phải sống.
           Ba dịch vụ chín mươi chín phẩy chín lăm, chín mươi chín phẩy chín và chín mươi chín phẩy chín cho chín mươi chín phẩy bảy năm không hai phần trăm, thấp hơn cả ba.""",
           clear=True),
        st("""<p><b>Bước 4. Sự cố, mức độ và hỗ trợ mức 3.</b> Mỗi sự cố có mức (ví dụ P1–P4, do tổ chức đặt, số minh hoạ) và hạn phản hồi. Mức 1 nhận, mức 2 xử lý theo kịch bản; khi vượt khả năng, <b>chuyển mức 3</b> kèm phiếu đủ chứng cứ.</p>"""
           + table(["mức (ví dụ)", "ý nghĩa", "hạn phản hồi (số minh hoạ)"],
                   [["P1", "ngừng hoàn toàn dịch vụ chính", "15 phút"], ["P2", "chậm hoặc lỗi một phần dịch vụ chính", "30 phút"],
                    ["P3", "một chức năng phụ lỗi, có cách tạm", "4 giờ"], ["P4", "câu hỏi, cải tiến", "2 ngày làm việc"]])
           + """<p><b>Ca 1:</b> tra số dư chậm với 15% yêu cầu, báo lúc 09:10 → P2, phản hồi trước 09:10 + 30 phút = 09:40. <b>Ca 2:</b> xuất sao kê PDF lỗi, khách vẫn xem trên ứng dụng → P3, hạn 4 giờ.</p>""",
           """Bước bốn là sự cố và hỗ trợ mức ba. Mỗi sự cố có một mức do tổ chức tự đặt kèm hạn phản hồi, bảng này là số minh hoạ. Tra số dư chậm với mười lăm phần trăm yêu cầu là mức hai, báo lúc chín giờ mười thì phản hồi trước chín giờ bốn mươi. Vượt khả năng thì chuyển hỗ trợ mức ba cùng phiếu đủ chứng cứ.""",
           clear=True),
        st("""<p><b>Bước 5. Phiếu sự cố.</b> Phiếu tốt cho người nhận <b>mọi thứ để bắt đầu</b>: mức, ảnh hưởng, chứng cứ (mã tương quan, chỉ số), cách tái hiện, hành động tạm thời, người nhận, hạn phản hồi.</p>"""
           + X_TICKET.show(title="PhieuSuCo.yaml (mẫu minh hoạ)"),
           """Bước năm là phiếu sự cố. Phiếu tốt cho người nhận mọi thứ để bắt đầu mà không phải hỏi lại: mức độ, ảnh hưởng, chứng cứ, cách tái hiện, hành động tạm thời, người nhận, hạn phản hồi. Chữ p chín mươi lăm là mức mà chín mươi lăm phần trăm yêu cầu nhanh hơn, nên bốn phẩy hai giây nghĩa là một trong hai mươi yêu cầu chậm hơn thế.""",
           clear=True),
        jstep([(("<code>TOT = \"\"\"# ADR 7: …\"\"\"</code>", "chuỗi nhiều dòng giữa ba dấu nháy kép; <code>#</code> đầu dòng trong chuỗi là tiêu đề, không phải ghi chú; ADR 7: bản ghi quyết định số 7", "Chuỗi nhiều dòng nằm giữa ba dấu nháy kép, dấu thăng đầu dòng là tiêu đề."), "", ""),
               (("<code>SMS</code>", "tin nhắn văn bản tới điện thoại; <b>cổng SMS</b>: cửa của nhà cung cấp mà mọi tin gửi đi phải qua", "Tin nhắn điện thoại đi qua một cổng chỉ gửi được số tin có hạn mỗi giây."), "", "")],
              intro="Bản ghi mẫu có hai chỗ lạ nên ta đọc trước."),
        st("""<p><b>Bước 6. Bản thiết kế một trang.</b> Mỗi quyết định kiến trúc có một bản ghi ngắn: <b>Bối cảnh</b> (sự thật, lực kéo, trung lập), <b>Quyết định</b> (câu đầy đủ &laquo;Chúng tôi sẽ…&raquo;), <b>Hệ quả</b> (cả tích cực lẫn tiêu cực), kèm trạng thái. Theo bài viết gốc về mẫu này: hệ quả liệt kê &laquo;not just the positive ones&raquo;.</p>"""
           + PY_TL.show(lines=(1, 8), title="KiemTaiLieu.py (trích): một bản ghi quyết định mẫu"),
           """Bước sáu là bản thiết kế một trang, vì người đến sau cần hiểu lý do. Bối cảnh nêu sự thật, quyết định là câu bắt đầu bằng chúng tôi sẽ, hệ quả liệt kê cả tích cực lẫn tiêu cực. Hàng đợi là nơi xếp tin chờ gửi dần theo tốc độ cổng cho phép.""",
           clear=True),
        st("""<p><b>Bước 7. Kịch bản kiểm thử, môi trường kiểm thử, nhà cung cấp.</b> Trước khi đưa bản sửa lên môi trường thật: có <b>kịch bản kiểm thử</b> (bước, dữ liệu, kết quả mong đợi), chạy ở <b>môi trường kiểm thử</b> giống môi trường thật ở điều quan trọng (phiên bản, cấu hình), và với <b>nhà cung cấp</b> thì có <b>thoả thuận nội bộ hoặc hợp đồng</b> với hạn phản hồi, và ca kiểm riêng cho phần phụ thuộc họ.</p>"""
           + table(["việc", "đầu ra cần có", "dấu hiệu làm thiếu"],
                   [["kịch bản kiểm thử", "bước, dữ liệu mẫu, kết quả mong đợi, ai chạy", "&laquo;thử rồi, chạy được&raquo; mà không ghi gì"],
                    ["môi trường kiểm thử", "cùng phiên bản và cấu hình với môi trường thật ở phần liên quan", "bản sửa chạy ở kiểm thử, hỏng ở môi trường thật"],
                    ["nhà cung cấp", "hạn phản hồi, người liên hệ, ca kiểm cho phần phụ thuộc", "đối tác ngừng mà không ai biết gọi ai"]]),
           """Bước bảy là kịch bản kiểm thử, môi trường kiểm thử và nhà cung cấp. Kịch bản ghi bước, dữ liệu và kết quả mong đợi, nên ai chạy cũng ra cùng kết luận. Môi trường kiểm thử giống môi trường thật ở phiên bản và cấu hình, còn nhà cung cấp cần thoả thuận có hạn phản hồi.""",
           clear=True),
    ], checks=["alg.bnx_l35_budget('99.9', 30) == 43.2", "alg.bnx_l35_chain(['0.9995', '0.999', '0.999']) == 0.997502",
               "alg.bnx_l35_chain(['0.9995', '0.9995'], 8) == 0.99900025 and 0.99900025 >= 0.999",
               "9 * 60 + 10 + 30 == 9 * 60 + 40"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st(PY_SLA.out_html()
           + """$$① \\; 99\\% \\to 432; \\;\\; 99{,}9\\% \\to 43{,}2; \\;\\; 99{,}95\\% \\to 21{,}6; \\;\\; 99{,}99\\% \\to \\hlg{4{,}32} \\text{ phút}$$""",
           """Phép tính thứ nhất là ngân sách ngừng của bốn mức, đã chạy thật: bốn trăm ba mươi hai, bốn mươi ba phẩy hai, hai mươi mốt phẩy sáu và bốn phẩy ba hai phút một tháng.""",
           clear=True),
        st(PY_CHUOI.out_html()
           + """$$② \\; 0{,}9995 \\times 0{,}999 \\times 0{,}999 = \\hl{0{,}997502}; \\quad \\text{ngân sách chung } 107{,}91 \\text{ phút}$$""",
           """Phép tính thứ hai là ba dịch vụ nối tiếp, độ sẵn sàng chung chín mươi chín phẩy bảy năm không hai phần trăm. Cam kết chung thì ngân sách ngừng là một trăm linh bảy phẩy chín mốt phút.""",
           clear=True),
        jstep([(("<code>su_co = [(12, \"P2\"), …]</code>, <code>sum(p for p, _ in su_co)</code>", "danh sách các cặp (số phút, mức); <code>for p, _ in su_co</code>: <code>p</code> là phần đầu của mỗi cặp, <code>_</code> bỏ phần sau; <code>sum</code> cộng hết", "Mỗi cặp có số phút và mức, vòng lặp lấy số phút, gạch dưới bỏ mức, hàm tổng cộng hết."), "<code>sum(p for p, _ in [(2, \"a\"), (3, \"b\")])</code> ra 5", ""),
               (("<code>\" + \".join(str(p) for p, _ in su_co)</code>", "<code>str(p)</code> đổi số thành chữ; <code>\" + \".join(…)</code> nối các chữ, giữa hai chữ chèn dấu cộng", "Hàm nối ghép các chữ, giữa hai chữ chèn dấu cộng."), "ra <code>12 + 30 + 5</code>", ""),
               (("<code>\"vuot…\" if tong &gt; ngan_sach else \"con…\"</code>", "biểu thức điều kiện: giá trị là chữ đầu nếu <code>tong</code> lớn hơn <code>ngan_sach</code>, ngược lại là chữ sau", "Biểu thức điều kiện cho chữ đầu nếu điều kiện đúng, ngược lại chữ sau."), "47 lớn hơn 43,2 nên ra <code>vuot…</code>", ""),
               (("<code>abs(tong - ngan_sach)</code>", "giá trị tuyệt đối: bỏ dấu âm nếu có", "Giá trị tuyệt đối bỏ dấu âm nếu có."), "<code>abs(-3.8)</code> ra <code>3.8</code>", "")]),
        st(PY_SUCO.show(lines=(1, 11), title="SuCoThang.py: cộng sự cố, so với ngân sách"),
           """Phép tính thứ ba là so sự cố với ngân sách: lấy ngân sách chín mươi chín phẩy chín, cộng các sự cố trong tháng, rồi so hai số.""",
           clear=True),
        st(PY_SUCO.out_html()
           + """$$③ \\; 12 + 30 + 5 = 47 > 43{,}2 \\Rightarrow \\hl{\\text{vượt } 3{,}8 \\text{ phút}}; \\quad 100 - 47 : 432 = 99{,}8912\\%$$"""
           + """<div class="box key"><b>Giả định:</b> hợp đồng tính cả ba sự cố vào phút ngừng. Nếu sự cố P3 (5 phút) không tính: 12 + 30 = 42 &lt; 43,2, chưa vượt.</div>""",
           """Ba sự cố cộng bốn mươi bảy phút, vượt ngân sách ba phẩy tám phút; độ sẵn sàng thực tế chín mươi chín phẩy tám chín một hai phần trăm. Đó là khi hợp đồng tính cả ba sự cố; bỏ sự cố nhẹ năm phút thì chỉ bốn mươi hai phút, chưa vượt.""",
           clear=True),
        jstep([(("<code>def kiem(vb): … return loi</code>", "khai hàm <code>kiem</code> nhận văn bản <code>vb</code>; các dòng thụt vào là thân hàm; <code>return loi</code> trả danh sách lỗi về chỗ gọi", "Hàm kiểm nhận một văn bản và trả về danh sách lỗi."), "<code>kiem(TOT)</code> ra danh sách rỗng", ""),
               (("<code>if muc not in vb: loi.append(…)</code>, <code>muc[3:]</code>", "nếu mục không có trong văn bản <code>vb</code> thì thêm một lỗi vào danh sách <code>loi</code>; <code>muc[3:]</code> bỏ 3 ký tự đầu", "Nếu mục không có trong văn bản thì thêm một lỗi vào danh sách, và cắt lát bỏ ba ký tự đầu."), "<code>\"## He qua\"[3:]</code> ra <code>He qua</code>", ""),
               (("<code>\"dat\" if not loi else …</code>", "giá trị là <code>\"dat\"</code> nếu danh sách <code>loi</code> rỗng, ngược lại là chữ sau", "Biểu thức điều kiện chọn một trong hai giá trị."), "", "")]),
        st(PY_TL.show_from("def kiem", 12, title="KiemTaiLieu.py (trích): danh mục kiểm bản thiết kế")
           , """Phép tính thứ tư là tự chấm bản thiết kế. Hàm kiểm duyệt ba mục bắt buộc, câu quyết định chủ động, và hệ quả có mặt tiêu cực. Rồi nó chấm một bản ghi tốt và một bản ghi xấu.""",
           clear=True),
        st(PY_TL.out_html()
           + """$$④ \\; \\text{bản tốt: đạt}; \\quad \\text{bản xấu: } \\hl{5} \\text{ lỗi}$$""",
           """Kết quả thật: bản ghi tốt đạt cả danh mục kiểm, bản ghi xấu báo năm lỗi, gồm thiếu cả ba mục, quyết định không chủ động và hệ quả không nêu mặt tiêu cực.""",
           clear=True),
    ], checks=["alg.bnx_l35_budget('99.95', 30) == 21.6 and alg.bnx_l35_budget('99.99', 30) == 4.32", "alg.bnx_l35_over(47, 43.2) == 3.8",
               "alg.bnx_l35_chain(['0.9995', '0.999', '0.999']) == 0.997502"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: tính bằng phân số và bằng cách trừ dần", [
        jstep([(("<code>from fractions import Fraction as F</code>, <code>F(999, 1000)</code>", "nạp kiểu phân số, gọi tắt <code>F</code>: đúng 999 phần 1000, không làm tròn", "Kiểu phân số giữ đúng tử số và mẫu số, không làm tròn."), "<code>F(1, 2) + F(1, 3)</code> ra <code>5/6</code>", ""),
               (("<code>F(999, 1000) ** 2</code>", "<code>**</code>: lũy thừa, <code>x ** 2</code> là x nhân x", "Hai dấu sao là lũy thừa, bình phương là nhân với chính nó."), "<code>F(1, 2) ** 2</code> ra <code>1/4</code>", ""),
               (("<code>{float(…):.6f}</code>", "<code>float</code> đổi phân số thành số thập phân thường; <code>:.6f</code>: 6 chữ số sau dấu chấm", "Hàm đổi sang số thập phân thường, đuôi chấm sáu f giữ sáu chữ số."), "<code>float(F(1, 4))</code> ra <code>0.25</code>", ""),
               (("<code>sum(1 for _ in range(thang))</code>", "mỗi số của <code>range(thang)</code> được cộng 1, nên tổng là số lần lặp; <code>_</code>: tên biến bỏ đi", "Mỗi số trong dãy được cộng một, nên tổng là số lần lặp."), "<code>sum(1 for _ in range(5))</code> ra 5", "")]),
        st(PY_FRAC.show(title="Kiểm bằng phân số, không dùng số thập phân của chương trình trước"),
           """Ta kiểm bằng đường khác hẳn: dùng phân số thay cho số thập phân, nên không có sai số làm tròn.
           Dòng đầu tính ngân sách, dòng hai tính tỉ lệ ngừng của chuỗi ba dịch vụ, dòng ba đếm từng phút trong tháng.""",
           clear=True),
        st(PY_FRAC.out_html() + table(["cách", "ngân sách 99,9%", "chuỗi ba dịch vụ: tỉ lệ ngừng"],
                                     [["số thập phân (Decimal)", "43,2 phút", "1 − 0,997502 = 0,002498"], ["phân số (Fraction)", "216/5 = 43,2 phút", "0,002498"]]),
           """Hai trăm mười sáu phần năm bằng bốn mươi ba phẩy hai phút, khớp số thập phân; tỉ lệ ngừng của chuỗi là không phẩy không không hai bốn chín tám, cũng khớp.
           Đếm từng phút ra bốn mươi ba nghìn hai trăm, nên hai đường độc lập cho cùng kết quả.""",
           focus=[0, "2.2", "2.3"], clear=True),
    ], checks=["Fraction(216, 5) == Fraction('43.2')", "30 * 24 * 60 == 43200"])

    quymo = sc("quymo", "example", "Khi hệ thống lớn dần: chuỗi dài làm độ sẵn sàng tụt", [
        jstep([(("<code>getcontext().prec = 50</code>, <code>D(\"0.999\") ** n</code>", "đặt số chữ số tối đa của phép tính <code>D</code> là 50 (mặc định 28); <code>** n</code>: nhân 0,999 với chính nó <code>n</code> lần", "Dòng đầu đặt số chữ số tối đa của phép tính là năm mươi, và lũy thừa là nhân với chính nó nhiều lần."), "<code>n = 3</code>: <code>0.999 * 0.999 * 0.999</code>", "")]),
        st(PY_QUYMO.show(lines=(1, 8), title="QuyMoChuoi.py"), """Ta chạy ba cỡ hệ thống, mọi dịch vụ nối tiếp đều chín mươi chín phẩy chín phần trăm, và in độ sẵn sàng cùng số phút ngừng.""", clear=True),
        st(PY_QUYMO.out_html()
           + """$$1 \\to 100 \\to 10\\,000 \\text{ dịch vụ } 99{,}9\\%: \\; 99{,}9\\% \\to \\hl{90{,}4792\\%} \\to \\hl{0{,}0045\\%}$$""",
           """Số đo thật: một dịch vụ ngừng tối đa bốn mươi ba phẩy hai phút một tháng. Một trăm dịch vụ nối tiếp chỉ còn chín mươi phẩy bốn bảy chín hai phần trăm, tức ngừng hơn bốn nghìn phút. Mười nghìn dịch vụ thì tiến về không.""",
           clear=True),
        st(table(["cách", "được", "mất", "chọn khi"],
                 [["thêm chữ số 9 cho từng dịch vụ", "chuỗi bớt tụt", "chi phí thường tăng thêm với mỗi chữ số 9 (mức tăng tuỳ hệ thống)", "dịch vụ lõi mọi chuỗi cùng đi qua"],
                  ["rút ngắn chuỗi: gọi song song, bỏ mắt xích không bắt buộc", "ít mắt xích phải sống cùng lúc", "thiết kế phức tạp hơn", "các mắt xích có thể làm sau, không chặn yêu cầu"],
                  ["suy giảm có kiểm soát: mắt xích phụ hỏng thì bỏ phần phụ", "yêu cầu chính vẫn chạy", "khách thấy bản thiếu tính năng", "mắt xích phụ không quan trọng"]]),
           """Bảng này nêu cái phải chọn. Thêm chữ số chín cho từng dịch vụ làm chuỗi bớt tụt nhưng chi phí tăng thêm. Rút ngắn chuỗi giảm số mắt xích phải sống cùng lúc. Suy giảm có kiểm soát giữ yêu cầu chính chạy khi mắt xích phụ hỏng, đổi lại khách thấy bản thiếu tính năng.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l35_chain(['0.999'] * 100) == 0.904792", "alg.bnx_l35_budget('99.9', 30) == 43.2"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Đọc <b class="red">99,9% là &laquo;gần như không bao giờ ngừng&raquo;</b>. Chạy thật: 99,9% vẫn cho phép 43,2 phút ngừng mỗi tháng; 3 sự cố 12 + 30 + 5 = 47 phút là vượt. Luôn đổi phần trăm sang phút trước khi cam kết.</div>"""
           + PY_SUCO.out_html(),
           """Lỗi thứ nhất, của người mới, là đọc chín mươi chín phẩy chín phần trăm là gần như không bao giờ ngừng. Nó vẫn cho ngừng bốn mươi ba phẩy hai phút mỗi tháng, nên ba sự cố bốn mươi bảy phút là vượt.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Cam kết với khách <b class="red">cao hơn cam kết của chính các dịch vụ phụ thuộc</b>: ba dịch vụ 99,95%, 99,9%, 99,9% nối tiếp cho 99,7502%, nên hứa 99,9% là hứa điều không thể giữ. Cam kết ngoài phải ≤ tích các cam kết trong.</div>""",
           """Lỗi thứ hai, của người đã đi làm, lộ ra lúc mới dựng: cam kết với khách cao hơn cam kết của các dịch vụ phụ thuộc. Ba dịch vụ nối tiếp cho chín mươi chín phẩy bảy năm không hai phần trăm, nên hứa chín mươi chín phẩy chín là không giữ được.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Cứ <b class="red">thêm dịch vụ nối tiếp</b> khi hệ thống lớn: 100 dịch vụ 99,9% chỉ còn 90,4792% (ngừng tới hơn 4 000 phút một tháng). Giữ chuỗi ngắn, gọi song song, và có đường suy giảm có kiểm soát.</div>""",
           """Lỗi thứ ba, của người đã đi làm, lộ ra khi hệ thống lớn dần: cứ thêm dịch vụ nối tiếp. Một trăm dịch vụ chín mươi chín phẩy chín chỉ còn chín mươi phẩy bốn bảy chín hai phần trăm. Cần giữ chuỗi ngắn, gọi song song và có đường suy giảm.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> <b class="red">Không ghi lại quyết định thiết kế</b>: sau một năm không ai nhớ vì sao chọn hàng đợi, người mới &laquo;sửa lại cho gọn&raquo; và phá điều kiện ban đầu. Mỗi quyết định lớn một trang theo khung bối cảnh – quyết định – hệ quả; quyết định đổi thì đánh dấu bản cũ là đã bị thay, không xoá.</div>"""
           + PY_TL.out_html(),
           """Lỗi thứ tư, của người đã đi làm, lộ ra khi vận hành lâu dài: không ghi lại quyết định thiết kế, nên sau một năm người mới sửa cho gọn và phá điều kiện ban đầu.""", clear=True),
    ], checks=["alg.bnx_l35_over(47, 43.2) == 3.8", "alg.bnx_l35_chain(['0.999'] * 100, 4) == 0.9048"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Tháng 30 ngày, SLA 99,95%. Ngân sách ngừng bao nhiêu phút? Tháng đó có sự cố 8 + 15 phút: còn lại bao nhiêu phút ngân sách?"],
                  ["2", "Hai dịch vụ nối tiếp, 99,9% và 99,8%. Độ sẵn sàng chung (4 chữ số thập phân)? Có đủ để cam kết 99,9% với khách không?"],
                  ["3", "Quyết định (số minh hoạ): đối tác thanh toán cam kết 99,5% còn bạn đã cam kết 99,9% với khách. Chọn: đòi đối tác nâng lên 99,95%, thêm đối tác dự phòng, hay thêm đường suy giảm (nhận lệnh, xử lý sau)? Vì sao?"]]),
           """Đến lượt bạn. Câu một: tháng ba mươi ngày, thoả thuận chín mươi chín phẩy chín lăm; tính ngân sách ngừng rồi trừ sự cố tám cộng mười lăm phút. Câu hai: hai dịch vụ nối tiếp chín mươi chín phẩy chín và chín mươi chín phẩy tám có đủ cam kết chín mươi chín phẩy chín không? Câu ba: đối tác cam kết chín mươi chín phẩy năm, bạn cam kết chín mươi chín phẩy chín; chọn cách nào? Hãy dừng và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=30),
        st("""<p>Câu 1: ngân sách = 43 200 × (100 − 99,95) : 100; trừ sự cố đã dùng.</p>
$$43\\,200 \\times 0{,}05 : 100 = \\hlg{21{,}6} \\text{ phút}; \\quad 21{,}6 - (8 + 15) = \\hlg{-1{,}4} \\Rightarrow \\text{vượt } 1{,}4 \\text{ phút}$$""",
           """Đáp án câu một. Ngân sách là bốn mươi ba nghìn hai trăm nhân không phẩy không năm phần trăm, bằng hai mươi mốt phẩy sáu phút. Sự cố đã dùng hai mươi ba phút, nên vượt một phẩy bốn phút."""),
        st("""<p>Câu 2: nhân hai tỉ lệ; so với cam kết 0,999.</p>
$$0{,}999 \\times 0{,}998 = \\hlg{0{,}9970} < 0{,}999 \\Rightarrow \\text{không đủ để cam kết } 99{,}9\\%$$""",
           """Đáp án câu hai. Không phẩy chín chín chín nhân không phẩy chín chín tám bằng không phẩy chín chín bảy không, thấp hơn không phẩy chín chín chín.
           Vậy hai dịch vụ nối tiếp không đủ để cam kết chín mươi chín phẩy chín với khách."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["đòi đối tác nâng lên 99,95%", "chuỗi gần mục tiêu", "phụ thuộc đối tác chịu và chịu chi phí; vẫn chưa bảo đảm"],
                  ["thêm đối tác dự phòng", "một bên ngừng thì bên kia gánh", "chi phí và độ phức tạp tăng gấp đôi; phải kiểm chuyển đổi"],
                  ["đường suy giảm: nhận lệnh, xử lý sau khi đối tác sống lại", "yêu cầu khách vẫn được nhận; không còn phụ thuộc đồng bộ", "khách thấy kết quả trễ; cần đối soát sau"]]),
           """Đáp án câu ba. Đòi đối tác nâng mức đưa chuỗi gần mục tiêu nhưng vẫn phụ thuộc đối tác. Đối tác dự phòng cho bên kia gánh, đổi lại chi phí gấp đôi. Đường suy giảm giữ được yêu cầu khách, đổi lại kết quả trễ và cần đối soát.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_l35_budget('99.95', 30) == 21.6 and alg.bnx_l35_over(8 + 15, 21.6) == 1.4", "alg.bnx_l35_chain(['0.999', '0.998'], 4) == 0.997"])

    lab_pr = practice_scene(sc, "Tự làm: ngân sách SLA và khung bản thiết kế", practice_steps_giay(
        st, "BNX", "L35",
        """<p><b>Đề</b> (giấy bút, số minh hoạ): tháng <b>31 ngày</b>, SLA <b>99,8%</b>, hai dịch vụ nối tiếp <b>99,9%</b> và <b>99,5%</b>, hai sự cố <b>20 và 75 phút</b>. Viết 4 dòng: ngân sách ngừng; độ sẵn sàng chuỗi (4 chữ số); tổng sự cố và vượt bao nhiêu; và khung bản thiết kế một trang cho &laquo;dùng hàng đợi cho thông báo sao kê&raquo;, tự chấm bằng danh mục kiểm.</p>
<p class="note">Định dạng bốn dòng đáp án nằm trong <code>de.md</code>; đối chiếu với <code>loi_giai.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm bằng giấy bút, với số liệu mới. Tính ngân sách ngừng, độ sẵn sàng chung của chuỗi và phần vượt của tháng, rồi viết khung bản thiết kế cho quyết định dùng hàng đợi và tự chấm. Hãy dừng video và tự làm.""",
        LAB_OUT,
        """<div class="box key"><b>Nếu kẹt:</b> tháng 31 ngày có 31 × 24 × 60 phút; ngân sách = số phút × (100 − 99,8) : 100. Chuỗi: nhân hai tỉ lệ dạng số thập phân. Sự cố: cộng rồi trừ ngân sách. Khung bản ghi: ba mục Bối cảnh, Quyết định, Hệ quả.
Lời giải đầy đủ ở <code>labs/BNX/L35/loi_giai.md</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, chuỗi thì nhân hai tỉ lệ, sự cố thì cộng rồi trừ ngân sách. Lời giải đầy đủ nằm trong thư mục thực hành.""", pause=180), "BNX", "L35")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("đo → đặt → cam kết → cam kết nội bộ", "phần trăm → phút ngừng", "nối tiếp thì nhân", "phiếu sự cố đủ chứng cứ", "ghi quyết định một trang"),
           """Tổng kết chuỗi lập luận. Ta đo, đặt mục tiêu, cam kết với khách và nội bộ, đổi phần trăm sang phút, và dịch vụ nối tiếp thì nhân. Phiếu đủ chứng cứ để mức ba bắt đầu ngay, quyết định lớn ghi trong một trang."""),
        st("""<div class='box key'><b>Tư duy:</b> con số trong cam kết phải <b>đổi được ra phút</b> và <b>nhân được qua chuỗi</b>. Vận hành tốt là làm cho người khác (và chính mình sau một năm) <b>không phải hỏi lại</b>: phiếu đủ chứng cứ, bản ghi có bối cảnh và hệ quả.</div>""",
           """Điều cần mang theo. Con số trong cam kết phải đổi được ra phút và nhân được qua chuỗi dịch vụ. Vận hành tốt là làm cho người khác, và chính mình sau một năm, không phải hỏi lại."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Hỗ trợ mức 3 và SLA/OLA là gì?", "mức 3 là kỹ sư sửa mã/cấu hình nhận khi mức 1–2 không giải quyết được; SLA là cam kết có hệ quả với khách, OLA là cam kết nội bộ giữa các đội để đạt SLA; đổi % sang phút ngừng: 99,9% = 43,2 phút/tháng 30 ngày"],
                  ["Làm sao viết bản thiết kế và quản lý môi trường kiểm thử?", "khung bối cảnh – quyết định – hệ quả, kèm trạng thái, ghi cả hệ quả tiêu cực; môi trường kiểm thử giống môi trường thật ở phần quan trọng; có kịch bản kiểm thử ghi bước, dữ liệu, kết quả mong đợi"],
                  ["Quản lý nhà cung cấp thế nào?", "thoả thuận có hạn phản hồi, người liên hệ; tính độ sẵn sàng chuỗi (tích) để biết cam kết với khách có giữ được không; có đường suy giảm khi họ ngừng"]]),
           """Nếu bị hỏi về dòng vận hành và bản thiết kế, đây là ba câu hay gặp. Hỗ trợ mức ba là kỹ sư sửa mã nhận khi mức một và hai không giải quyết được. Bản thiết kế theo khung bối cảnh, quyết định, hệ quả; nhà cung cấp cần thoả thuận và đường suy giảm.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Bài sau: <b>phỏng vấn thiết kế hệ thống</b>: khung sáu bước cho một trung tâm thanh toán và hệ thống tín dụng.</p>""",
           """Ở bài ba mươi sáu, ta tập phỏng vấn thiết kế hệ thống, với khung sáu bước cho một trung tâm thanh toán và hệ thống tín dụng.""",
           forward_ref=True),
    ], checks=["alg.bnx_l35_budget('99.9', 30) == 43.2"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L35", "van_hanh_sla_tai_lieu",
                  "Bài 35 — Vận hành: hỗ trợ mức 3, SLA/OLA, phiếu sự cố và bản thiết kế",
                  "curriculum/bnx.yaml L35; audit/bnx/verify_bnx.py L35; audit/bnx/sources_l35.md: Google SRE Book (Service Level Objectives; Embracing Risk), "
                  "Michael Nygard 'Documenting Architecture Decisions' (cognitect.com, 2011), Wikipedia (Operational-level agreement, Service-level agreement) (đọc 2026-11-14); mã Python 3 (Decimal, Fraction) chạy thật",
                  ["Tính ngân sách phút ngừng của mục tiêu sẵn sàng 99%, 99,9%, 99,95% và 99,99%",
                   "Phân biệt chỉ số, mục tiêu, thoả thuận mức dịch vụ và thoả thuận nội bộ bằng ví dụ có số",
                   "Tính độ sẵn sàng chung của các dịch vụ nối tiếp và nói vì sao chuỗi dài làm tụt",
                   "Xác định một tháng có vượt ngân sách hay không từ danh sách sự cố",
                   "Phân loại sự cố theo mức và nêu việc hỗ trợ mức 3 phải làm cùng nội dung phiếu sự cố",
                   "Viết bản thiết kế theo khung bối cảnh, quyết định, hệ quả và tự chấm bằng danh mục kiểm",
                   "Đếm độ sẵn sàng của chuỗi 1, 100 và 10 000 dịch vụ",
                   "Tính tay ngân sách SLA, độ sẵn sàng chuỗi và dựng khung bản thiết kế trên số liệu mới"],
                  scenes,
                  covers=[(1, "example"), (2, "formula"), (3, "example"), (4, "example"), (5, "formula"), (6, "example"), (7, "quymo"), (8, "practice")])
