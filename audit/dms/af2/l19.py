"""DMS L19 → AF2 (WP5 phiên 2). Chạy: .venv/Scripts/python -B audit/dms/af2/l19.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L19"

C1 = r"""for m in (365, 10 ** 6, 2 ** 32):
    khong_trung, n = 1.0, 0
    while khong_trung > 0.5:
        khong_trung = khong_trung * (m - n) / m
        n = n + 1
    print(m, 'o: can', n, 'khoa; ti so n / can(m) =', round(n / m ** 0.5, 2))"""
O1 = run_py(C1)
print(O1)

TAB = read_steps([
    ("for m in (365, 10 ** 6, 2 ** 32):", "với mỗi m lần lượt trong ngoặc, làm các dòng thụt vào; <code>**</code> là lũy thừa: <code>10 ** 6</code> là một triệu, <code>2 ** 32</code> là hơn bốn tỉ", "ba lượt: m = 365, rồi 1000000, rồi 4294967296"),
    ("khong_trung, n = 1.0, 0", "một dấu bằng là <b>gán</b>; gán hai giá trị cùng lúc: khong_trung nhận 1.0 (số có phần thập phân, chắc chắn chưa trùng), n nhận 0", "khong_trung = 1.0 là 100%; n = 0 khoá"),
    ("while khong_trung > 0.5:", "lặp lại các dòng thụt vào bên dưới chừng nào khong_trung còn lớn hơn 0.5", "0.51 thì lặp tiếp; 0.49 thì dừng"),
    ("khong_trung = khong_trung * (m - n) / m, n = n + 1", "nhân với tỉ số ô còn trống (m − n) / m rồi cất lại, rồi tăng n thêm 1; <code>*</code> là nhân, <code>/</code> là chia ra số có phần thập phân", "m = 365, n = 1: 1.0 * 364 / 365 ≈ 0.9973"),
    ("round(n / m ** 0.5, 2)", "<code>m ** 0.5</code> là m mũ một nửa, tức căn bậc hai của m; <code>round(x, 2)</code> làm tròn x tới hai chữ số thập phân", "round(1.18321, 2) = 1.18"),
    ("print(m, 'o: can', n, ...)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách; <code>o</code> là ô, <code>can</code> là cần", "in ra 365 o: can 23 khoa; …"),
], "Chương trình tìm số khoá dùng sáu ký hiệu, ta đọc từng cái trước khi chạy.", [
    "Vòng lặp cho m lần lượt là 365, một triệu, rồi hơn bốn tỉ, trong đó hai dấu sao là lũy thừa.",
    "Một dấu bằng là gán hai giá trị cùng lúc: xác suất không trùng bắt đầu bằng 1 chấm 0, số khoá bằng 0.",
    "Vòng lặp này chạy chừng nào xác suất không trùng còn lớn hơn 0 chấm 5.",
    "Hai dòng này nhân xác suất với tỉ số ô còn trống, dấu sao là nhân, dấu gạch chéo là chia, rồi tăng số khoá thêm một.",
    "Hai dấu sao với 0 chấm 5 là căn bậc hai, và hàm làm tròn giữ hai chữ số thập phân.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
], split=3)

quymo = scene("quymo", "example", "Khi số ô lớn dần: số khoá để có va chạm chỉ cỡ căn của số ô", [
    step(
        "<p><b>Chạy thật</b>: số khoá nhỏ nhất để xác suất có hai khoá cùng ô đạt 50% khi có $m$ ô</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật, dừng khi xác suất không trùng tụt xuống dưới một nửa. "
        "Với 365 ngày là 23 người. Với một triệu ô là 1 178 khoá. Với hơn bốn tỉ ô là 77 164 khoá. "
        "Cả ba lần, số khoá gần bằng 1 phẩy 18 nhân căn của số ô.",
        focus=[2, "4.1", "4.2", "4.3", 4], clear=True),
    step(
        '<table class="t"><tr><th>mã băm dài $b$ bit ($m = 2^b$ ô)</th><th>số khoá để va chạm đạt 50% ($\\approx 1{,}18 \\times 2^{b/2}$)</th><th>thử một tỉ khoá mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>32</td><td>khoảng 77 000</td><td>chưa tới một phần nghìn giây</td></tr>"
        "<tr><td>64</td><td>khoảng $5{,}1 \\times 10^9$</td><td>khoảng 5 giây</td></tr>"
        "<tr><td>128</td><td>khoảng $2{,}2 \\times 10^{19}$</td><td>khoảng 690 năm</td></tr>"
        "<tr><td>256</td><td>khoảng $4{,}0 \\times 10^{38}$</td><td>khoảng $1{,}3 \\times 10^{22}$ năm</td></tr></table>"
        '<div class="box key">Mỗi lần gấp đôi độ dài bit chỉ <b>bình phương</b> số khoá cần thử. Vì vậy mã băm cần giữ an toàn trước va chạm phải dài <b>gấp đôi</b> mức an toàn mong muốn: muốn khoảng $2^{128}$ phép thử thì dùng 256 bit.</div>',
        "Bảng này cho thấy số khoá để có va chạm chỉ cỡ căn của số ô. Với 64 bit mất vài giây, với 128 bit khoảng 690 năm, với 256 bit thì không bao giờ xong. "
        "Người làm nghề chọn độ dài mã băm gấp đôi mức an toàn mong muốn, đánh đổi bằng mã dài hơn và chậm hơn một chút.",
        focus=[1, ["1.3", "1.4", "1.5"], 2], clear=True),
], checks=[
    "[next(n for n, p in enumerate(__import__('itertools').accumulate(((m - i) / m for i in range(10 ** 6)), __import__('operator').mul), 1) if p <= 0.5) for m in (365, 10 ** 6, 2 ** 32)] == [23, 1178, 77164]",
    "[round(n / m ** 0.5, 2) for n, m in ((23, 365), (1178, 10 ** 6), (77164, 2 ** 32))] == [1.2, 1.18, 1.18]",
    "[abs(1.17741 * 2 ** (b / 2) / 1e9 / 31557600 - y) / y < 0.01 for b, y in ((128, 688), (256, 1.27e22))] == [True, True]",
    "round(1.17741 * 2 ** 32 / 1e9, 0) == 5.0",
])
quymo["steps"] = flat(TAB, quymo["steps"])

DE = """# Lab DMS L19 — Xác suất rời rạc: ngày sinh, va chạm băm, kỳ vọng bằng chương trình

Viết `xacsuat.py` (Python 3.11 trở lên); chạy: `python xacsuat.py`.

In đúng năm dòng (không dấu):
1. `P(trung ngay sinh) voi 30 nguoi: <số>` — xác suất có ít nhất hai người trùng ngày sinh trong 30 người, 365 ngày rải đều (tính `1 − tích` các tỉ số `(365 − i) / 365`, `i` từ 0 đến 29), làm tròn 4 chữ số thập phân (`round(x, 4)`)
2. `so nguoi nho nhat de P >= 0.5 voi 1000 ngay: <số>` — số người n nhỏ nhất để xác suất trùng đạt ít nhất 0,5 khi có 1000 "ngày" (vòng lặp nhân dần tỉ số không trùng, dừng khi tích không trùng ≤ 0,5)
3. `ky vong so cap va cham 200 khoa vao 10000 o: <số>` — `C(200, 2) / 10000` (mỗi cặp va chạm với xác suất 1/10000, kỳ vọng của tổng bằng tổng kỳ vọng), in bằng `print(..)` của số thực
4. `so diem co dinh trung binh cua 7 vat: <số>` — trung bình số vật ở đúng chỗ cũ trên MỌI hoán vị của 7 vật (`itertools.permutations(range(7))`: 5040 hoán vị), in số thực
5. `P(khong trung) 5 nguoi, 10 ngay (liet ke het): <số>` — liệt kê mọi bộ 5 giá trị từ 10 "ngày" (`product(range(10), repeat=5)`, 100000 bộ), đếm các bộ đôi một khác nhau, chia cho 100000

Chấm: `bash labs/cham.sh DMS L19 xacsuat.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from itertools import permutations, product
from math import comb

khong_trung = 1.0
for i in range(30):
    khong_trung = khong_trung * (365 - i) / 365
print('P(trung ngay sinh) voi 30 nguoi:', round(1 - khong_trung, 4))

khong_trung, n = 1.0, 0
while khong_trung > 0.5:
    khong_trung = khong_trung * (1000 - n) / 1000
    n = n + 1
print('so nguoi nho nhat de P >= 0.5 voi 1000 ngay:', n)

print('ky vong so cap va cham 200 khoa vao 10000 o:', comb(200, 2) / 10000)

tong = 0
for p in permutations(range(7)):
    tong = tong + sum(1 for i in range(7) if p[i] == i)
print('so diem co dinh trung binh cua 7 vat:', tong / 5040)

khac = sum(1 for b in product(range(10), repeat=5) if len(set(b)) == 5)
print('P(khong trung) 5 nguoi, 10 ngay (liet ke het):', khac / 100000)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

prac = practice(
    LID, "Tự làm: xác suất ngày sinh, va chạm băm và kỳ vọng của biến chỉ báo",
    "<p><b>Đề</b>: viết <code>xacsuat.py</code> tính xác suất trùng ngày sinh của 30 người, số người nhỏ nhất để trùng đạt 50% với 1 000 ngày, kỳ vọng số cặp va chạm của 200 khoá vào 10 000 ô, "
    "số điểm cố định trung bình của 7 vật (liệt kê mọi hoán vị, tức mọi cách xếp lại; điểm cố định là vật ở đúng chỗ cũ), và xác suất không trùng khi liệt kê hết (năm dòng, định dạng ở <code>labs/DMS/L19/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Dự đoán trước phần thứ tư: trung bình mấy vật ở đúng chỗ cũ?</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình tính xác suất trùng ngày sinh của 30 người, và số người nhỏ nhất để xác suất trùng đạt một nửa khi có một nghìn ngày. "
    "Sau đó tính kỳ vọng số cặp va chạm, số điểm cố định trung bình của bảy vật, tức vật nằm đúng chỗ cũ, và một xác suất tính bằng cách liệt kê hết. "
    "Năm dòng và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "xacsuat.py",
    '<div class="box key"><b>Nếu kẹt:</b> xác suất không trùng là tích các tỉ số $(m - i)/m$; xác suất trùng là $1$ trừ tích đó. Kỳ vọng số cặp va chạm = số cặp $\\times$ xác suất mỗi cặp. '
    "Điểm cố định trung bình: cộng số điểm cố định của từng hoán vị rồi chia cho 5 040. "
    "Lời giải ở <code>labs/DMS/L19/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>",
    "Nếu kẹt, xác suất không trùng là tích các tỉ số số ô còn lại chia tổng số ô, và xác suất trùng là một trừ tích đó. Kỳ vọng số cặp va chạm bằng số cặp nhân xác suất của mỗi cặp. "
    "Số điểm cố định trung bình lấy tổng trên mọi hoán vị chia cho số hoán vị. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.",
    pause=420, focus1=[1, 1, 1, 1, 0][:5])
patch_cham(prac, LID, "xacsuat.py")

OBJ = [
    "Dùng biến chỉ báo và tính tuyến tính của kỳ vọng",
    "Tính xác suất có hai người trùng ngày sinh",
    "Ước lượng khi nào bảng băm bắt đầu có va chạm",
    "Đếm số khoá cần để có va chạm khi số ô lớn dần và nêu vì sao mã băm phải dài gấp đôi mức an toàn mong muốn",
    "Viết chương trình tính xác suất trùng, số khoá để va chạm và kỳ vọng bằng biến chỉ báo",
]
SHOULD = [
    # fix12 (R8): kể lại bối cảnh trả mũ ngay tại chỗ
    ("<b>Trả mũ</b> (bài 12): trung bình bao nhiêu người nhận đúng mũ?", "<b>Trả mũ</b>: $n$ người gửi mũ, mũ bị trả ngẫu nhiên; trung bình bao nhiêu người nhận đúng mũ của mình?"),
    ("Áp dụng cho bài trả mũ ở bài 12, trung bình có bao nhiêu người nhận đúng mũ?", "Áp dụng cho bài trả mũ, n người gửi mũ và mũ bị trả ngẫu nhiên, trung bình có bao nhiêu người nhận đúng mũ của mình?"),
    ("Kết quả đúng với mọi n, máy đã kiểm n từ 1 đến 6.", "Kết quả đúng với mọi n."),
    # fix6b: "đồng khả năng" nói bằng lời thường; điều kiện "không có điểm yếu" của cận 256 bit
    ("Đến đây là hết phần kiến thức của khoá Toán rời rạc, với logic, chứng minh, tập hợp, quan hệ, hàm, đếm, số học mô-đun, đồ thị và xác suất rời rạc.", "Đến đây là hết phần kiến thức của khoá Toán rời rạc."),
    # fix6b (giới hạn 2 300 từ): bỏ ba câu ít giá trị (số liệu vẫn nằm trên màn hình)
    ("focus: [2, 3, 0]\n        say: \"Bước hai,", "focus: [2, 3]\n        say: \"Bước hai,"),
    (" Nhưng mỗi người thêm vào lại nhân thêm một tỉ số nhỏ hơn, và tích giảm ngày càng nhanh.", ""),
    ("focus: [1, 2, 2]\n        say: \"Lỗi thứ nhất,", "focus: [1, 2]\n        say: \"Lỗi thứ nhất,"),
    (" Bảng cho thấy lý do, câu hỏi thứ nhất chỉ có 22 lần so sánh, câu hỏi thứ hai có tới 253 cặp.", ""),
    (" Một hàm băm tồi cũng làm va chạm tăng lên.", ""),
    ("Khi mọi kết quả <b>đồng khả năng</b>:", "Khi mọi kết quả <b>đồng khả năng</b> (khả năng như nhau):"),
    ("Khi mọi kết quả đồng khả năng, nó bằng số kết quả thuận lợi chia số kết quả có thể.", "Khi mọi kết quả đồng khả năng, tức khả năng như nhau, nó bằng số kết quả thuận lợi chia số kết quả có thể."),
    ("mã băm phải dài <b>256 bit</b> — gấp đôi số bit bạn nghĩ.", "mã băm phải dài <b>256 bit</b> (nếu hàm băm không có điểm yếu) — gấp đôi số bit bạn nghĩ."),
    ("Vì vậy, muốn kẻ tấn công phải thử cỡ 2 mũ 128 lần mới tìm được va chạm, mã băm phải dài 256 bit, gấp đôi số bit bạn nghĩ ban đầu.", "Vì vậy, muốn kẻ tấn công phải thử cỡ 2 mũ 128 lần, mã băm phải dài 256 bit, nếu hàm băm không có điểm yếu, gấp đôi số bit bạn nghĩ."),
]
f, _, _ = apply(LID, quiz_pause=30, repl=asr_keep(LID) + SHOULD + [('say: "Cùng hiện tượng này quyết định khi nào bảng băm bắt đầu va chạm,',
                       'say: "Bảng băm là một dãy ô, hàm băm chỉ mỗi khoá, tức mã định danh của dữ liệu, tới một ô, và va chạm là hai khoá rơi vào cùng một ô. Cùng hiện tượng này quyết định khi nào bảng băm bắt đầu va chạm,')],
                objectives=OBJ,
                covers=[(1, "linearity"), (2, "example"), (3, "hashing"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop"),
                requires_ext=None)
print(f)
print(ledger_sync(LID, claims={"quymo": "Với 365 ngày là 23 người; một triệu ô là 1 178 khoá; hơn bốn tỉ ô là 77 164 khoá; số khoá gần 1,18 nhân căn của số ô"}))
