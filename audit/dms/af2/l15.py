"""DMS L15 → AF2 (WP5 phiên 2). Chạy: .venv/Scripts/python -B audit/dms/af2/l15.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L15"

C1 = r"""for p, q in ((3, 11), (1009, 1013), (1000003, 1000033)):
    n, d, thu = p * q, 2, 1
    while n % d != 0:
        d = d + 1
        thu = thu + 1
    print(n, ': thu', thu, 'so chia, tim ra uoc', d)"""
O1 = run_py(C1)
print(O1)

TAB = read_steps([
    ("for p, q in ((3, 11), …):", "với mỗi cặp trong danh sách, gán số thứ nhất cho p và số thứ hai cho q, rồi làm các dòng thụt vào bên dưới", "lượt đầu: p = 3, q = 11"),
    ("n, d, thu = p * q, 2, 1", "một dấu bằng là <b>gán</b>; gán nhiều giá trị cùng lúc; <code>*</code> là nhân", "p = 3, q = 11: n = 33, d = 2, thu = 1"),
    ("while n % d != 0:", "<code>n % d</code> là số dư khi chia n cho d, <code>!=</code> là khác: lặp chừng nào d chưa chia hết n", "n = 33: d = 2 dư 1 nên lặp; d = 3 dư 0 nên dừng"),
    ("d = d + 1, thu = thu + 1", "gán: tính bên phải rồi cất vào tên bên trái, tức tăng d và thu thêm 1", "d = 2 thành 3"),
    ("print(n, ': thu', thu, 'so chia, tim ra uoc', d)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách; <code>thu</code> là số lần thử", "in ra 33 : thu 2 so chia, tim ra uoc 3"),
], "Chương trình phân tích n dùng năm ký hiệu, ta đọc từng cái trước khi chạy.", [
    "Dòng mở đầu vòng lặp: với mỗi cặp trong danh sách, gán số thứ nhất cho p và số thứ hai cho q, rồi làm các dòng thụt vào.",
    "Một dấu bằng là gán, và có thể gán nhiều giá trị cùng lúc, còn dấu sao là nhân, nên n nhận p nhân q.",
    "Dấu phần trăm là chia lấy số dư, dấu chấm than kèm bằng là khác, nên vòng lặp chạy chừng nào d chưa chia hết n.",
    "Hai dòng này gán lại bằng chính nó cộng một, tức tăng d và biến đếm lần thử thêm một.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách, và chữ thử là số lần thử.",
], split=3)

quymo = scene("quymo", "example", "Khi n lớn dần: phân tích n bằng cách chia thử tăng theo căn của n", [
    step(
        "<p><b>Chạy thật</b>: kẻ nghe lén phân tích $n = p \\times q$ bằng cách chia thử cho 2, 3, 4, … tới khi tìm được ước</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Kẻ nghe lén biết n và muốn tìm p, nên chia thử n lần lượt cho 2, 3, 4 và cứ thế, đếm số lần chia cho tới khi tìm được ước. "
        "Với n bằng 33, chỉ 2 lần chia. Với n cỡ một triệu, hơn một nghìn lần chia. Với n cỡ mười mũ mười hai, hơn một triệu lần chia. "
        "Cứ thêm sáu chữ số cho n, số lần chia tăng khoảng một nghìn lần.",
        focus=[2, ["2.2", "2.4"], "4.1", "4.2", "4.3", 4][:6], clear=True),
    step(
        '<table class="t"><tr><th>$n$</th><th>số lần chia thử</th><th>ở một tỉ phép chia mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>33</td><td>2</td><td>tức khắc</td></tr>"
        "<tr><td>$10^{12}$ (hai thừa số cỡ $10^6$)</td><td>cỡ $10^6$</td><td>một phần nghìn giây</td></tr>"
        "<tr><td>$10^{24}$ (hai thừa số cỡ $10^{12}$)</td><td>cỡ $10^{12}$</td><td>khoảng 17 phút</td></tr>"
        "<tr><td>$n$ dài 2048 bit (thừa số nhỏ nhất cỡ $2^{1023}$)</td><td>cỡ $2^{1023}$, một số có 308 chữ số</td><td>cỡ $10^{291}$ năm</td></tr></table>"
        '<div class="box key">Chia thử cần khoảng <b>căn của $n$</b> lần, tăng rất nhanh theo độ dài của $n$. Có cách phân tích nhanh hơn chia thử, nhưng theo hiểu biết công khai hiện nay, với $n$ dài 2048 bit vẫn chưa ai làm nổi. Đánh đổi: khoá dài thì <b>chậm hơn</b> khi mã hoá, nên phải chọn độ dài vừa đủ an toàn.</div>',
        "Bảng này cho thấy chia thử cần số lần cỡ căn của n. Với n cỡ mười mũ hai mươi bốn, mất khoảng 17 phút, nhưng với n dài 2048 bit, tức 2048 chữ số nhị phân, thì cỡ mười mũ hai trăm chín mươi mốt năm. "
        "Có những cách phân tích nhanh hơn chia thử, nhưng theo hiểu biết công khai hiện nay, với 2048 bit vẫn chưa ai làm nổi. "
        "Người làm nghề phải chọn độ dài khoá vừa đủ an toàn, vì khoá càng dài thì mã hoá càng chậm.",
        focus=[1, "1.4", 2, 2][:4], clear=True),
], checks=[
    "[(lambda n: next(d for d in range(2, n) if n % d == 0))(p * q) for p, q in ((3, 11), (1009, 1013), (1000003, 1000033))] == [3, 1009, 1000003]",
    "len(str(2 ** 1023)) == 308 and 2.8e291 < 2 ** 1023 / 1e9 / 31557600 < 2.9e291",
    "round(10 ** 12 / 1e9 / 60) == 17 and 10 ** 6 / 1e9 == 0.001",
])
quymo["steps"] = flat(TAB, quymo["steps"])

DE = """# Lab DMS L15 — RSA trên số nhỏ bằng chương trình

Viết `rsa.py` (Python 3.11 trở lên); chạy: `python rsa.py`.

Chọn `p = 7`, `q = 13`, `e = 5`. In đúng sáu dòng (không dấu):
1. `n = <n>, L = <L>` — `n = p*q`, `L = (p-1)*(q-1)`
2. `khoa bi mat d = <d>` — `d` là số trong 1..L-1 có `(e*d) % L == 1` (duyệt từng d)
3. `ma hoa 10: <số>` — bản mã của bản tin 10: `10**e % n` (dùng `pow(10, e, n)`)
4. `giai ma <bản mã vừa tính>: <số>` — giải mã bản mã đó bằng `pow(bản_mã, d, n)`; phải ra lại 10
5. `ma hoa roi giai ma moi ban tin 0..90: <số bản tin ra đúng> / 91 dung` — thử MỌI bản tin x từ 0 đến 90 (mã hoá rồi giải mã) và đếm số bản tin được trả lại đúng
6. `phan tich n: <n> = <p nhỏ> x <q>` — tìm ước nhỏ nhất lớn hơn 1 của n bằng cách chia thử, rồi in n, ước đó và thương

Chấm: `bash labs/cham.sh DMS L15 rsa.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""p, q, e = 7, 13, 5
n = p * q
L = (p - 1) * (q - 1)
print('n = ' + str(n) + ', L = ' + str(L))
d = 1
while (e * d) % L != 1:
    d = d + 1
print('khoa bi mat d =', d)
ban_ma = pow(10, e, n)
print('ma hoa 10:', ban_ma)
print('giai ma ' + str(ban_ma) + ':', pow(ban_ma, d, n))
dung = 0
for x in range(n):
    if pow(pow(x, e, n), d, n) == x:
        dung = dung + 1
print('ma hoa roi giai ma moi ban tin 0..90:', dung, '/ 91 dung')
u = 2
while n % u != 0:
    u = u + 1
print('phan tich n: ' + str(n) + ' = ' + str(u) + ' x ' + str(n // u))"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> $d$ là nghịch đảo của $e$ theo mô-đun $L$: thử $d = 1, 2, \\dots$ tới khi <code>(e * d) % L == 1</code> (không phải theo mô-đun $n$). '
    "Mã hoá là <code>pow(x, e, n)</code>, giải mã là <code>pow(c, d, n)</code>. Phân tích: chia thử cho 2, 3, 4, … "
    "Lời giải ở <code>labs/DMS/L15/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, khoá bí mật d là nghịch đảo của e theo mô-đun L, chứ không phải theo mô-đun n. Hãy thử d bằng một, hai, ba và cứ thế tới khi tích chia L dư một. "
    "Mã hoá và giải mã đều là lũy thừa theo mô-đun n, với số mũ e và d.")
HINT_TAIL = "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử."
H_HTML, H_SAY, H_FOC = hint_parts2(HINT_BOX, HINT_SAY, [
    ("(e * d) % L == 1", "<code>*</code> là nhân, <code>%</code> là chia lấy số dư, <code>==</code> là so sánh bằng: đúng khi e nhân d chia L dư 1", "e = 3, d = 7, L = 20: 21 % 20 = 1, đúng"),
    ("pow(x, e, n)", "hàm có sẵn cho x mũ e rồi lấy dư cho n; <code>pow(c, d, n)</code> làm tương tự với c và d", "pow(4, 3, 33) = 31"),
], [
    "Dấu sao là nhân, dấu phần trăm là chia lấy số dư, hai dấu bằng là so sánh bằng, nên điều kiện đúng khi e nhân d chia L dư một.",
    "Hàm có sẵn này nâng số thứ nhất lên lũy thừa số thứ hai rồi lấy dư cho số thứ ba, nên một lời gọi mã hoá và lời gọi kia giải mã.",
], HINT_TAIL)

prac = practice(
    LID, "Tự làm: dựng một bộ khoá RSA với p = 7, q = 13 và thử mọi bản tin",
    "<p><b>Đề</b>: với $p = 7$, $q = 13$, $e = 5$, viết <code>rsa.py</code> tính $n$, $L$, khoá bí mật $d$; mã hoá bản tin 10 rồi giải mã lại; "
    "thử mã hoá rồi giải mã MỌI bản tin từ 0 đến 90; và phân tích $n$ bằng cách chia thử (sáu dòng, định dạng ở <code>labs/DMS/L15/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài (p = 3, q = 11). Chỉ để học: bộ khoá nhỏ như vậy phá được ngay.</p>',
    "Bây giờ tới phần bạn tự làm, với p bằng 7, q bằng 13 và e bằng 5. Hãy viết chương trình tính n, L và khoá bí mật d. "
    "Sau đó mã hoá bản tin 10 rồi giải mã lại, thử mã hoá và giải mã mọi bản tin từ 0 đến 90, và phân tích n bằng cách chia thử. "
    "Bộ khoá nhỏ thế này phá được ngay, nên chỉ dùng để học. Sáu dòng và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "rsa.py", H_HTML, H_SAY,
    pause=420, focus1=[1, 1, 1, 1, 2, 0][:6], focus3=H_FOC)
patch_cham(prac, LID, "rsa.py")

OBJ = [
    "Sinh khoá, mã hoá, giải mã một hệ mã khoá công khai trên số nhỏ",
    "Nêu vì sao giải mã trả lại đúng bản tin",
    "Nêu vì sao độ an toàn dựa vào độ khó phân tích thừa số",
    "Đếm số lần chia thử khi phân tích n lớn dần và nêu vì sao khoá phải rất dài",
    "Viết chương trình dựng bộ khoá RSA nhỏ, mã hoá, giải mã mọi bản tin và phân tích n",
]
f, _, _ = apply(LID, quiz_pause=30, repl=asr_keep(LID) + [
                    ('Chữ L bằng p trừ 1 nhân q trừ 1, chỉ dùng', 'Chữ L bằng tích của p trừ 1 và q trừ 1, chỉ dùng'),
                    ('Tổng kết lại, n bằng p nhân q, L bằng p trừ 1 nhân q trừ 1.', 'Tổng kết lại, n bằng p nhân q, L bằng tích của p trừ 1 và q trừ 1.'),
                    ('Hệ thật dùng khoá rất dài và thêm phần đệm ngẫu nhiên trước khi mã hoá.', 'Hệ thật dùng khoá rất dài, và thêm vào bản tin một đoạn dữ liệu ngẫu nhiên gọi là phần đệm trước khi mã hoá, để cùng bản tin không còn ra cùng bản mã.'),
                    ('Thử với x bằng 2, 2 mũ 20 chia cho 3, cho 11 và cho 33 đều dư 1, và máy đã kiểm mọi bản tin từ 0 đến 32."',
                     'Trường hợp x chia hết cho p hoặc cho q cũng cho kết quả đúng, nhưng bài này chưa chứng minh nó, chỉ kiểm bằng máy với mọi bản tin từ 0 đến 32. Thử với x bằng 2, 2 mũ 20 chia cho 3, cho 11 và cho 33 đều dư 1."'),
                    ('focus: [1, 1, 1, "2.2", "2.3", "2.4", 3]\n        say: "Vì sao giải mã đúng?', 'focus: [1, 1, 1, "2.2", "2.3", "2.4", 3, 3]\n        say: "Vì sao giải mã đúng?'),
                ],
                objectives=OBJ,
                covers=[(1, "keygen"), (2, "why"), (3, "why"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                assumes_add=("dms_menhde", "dms_dinhly", "dms_tuongduong"))
print(f)
print(ledger_sync(LID, claims={"quymo": "n = 33 cần 2 lần chia, n cỡ một triệu hơn một nghìn lần, n cỡ mười mũ mười hai hơn một triệu lần"}))
