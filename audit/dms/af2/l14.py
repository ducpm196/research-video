"""DMS L14 → AF2 (WP5 phiên 2). Chạy: .venv/Scripts/python -B audit/dms/af2/l14.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L14"

C1 = r"""for e in (100, 10 ** 6, 10 ** 12):
    kq, a, x, phep = 1, 3, e, 0
    while x > 0:
        if x % 2 == 1:
            kq = kq * a % 1000007
        a = a * a % 1000007
        phep = phep + 1 + x % 2
        x = x // 2
    print(e, 'phep nhan:', phep, 'thay vi', e - 1, ', dung:', kq == pow(3, e, 1000007))"""
O1 = run_py(C1)
print(O1)

TAB_A = read_step([
    ("for e in (100, 10 ** 6, 10 ** 12):", "với mỗi e lần lượt trong ngoặc, làm các dòng thụt vào bên dưới; <code>**</code> là lũy thừa, <code>10 ** 6</code> là một triệu", "ba lượt: e = 100, rồi một triệu, rồi một nghìn tỉ"),
    ("kq, a, x, phep = 1, 3, e, 0", "một dấu bằng là <b>gán</b>; gán nhiều giá trị cùng lúc: kq nhận 1, a nhận 3, x nhận e, phep nhận 0", "e = 100: kq = 1, a = 3, x = 100, phep = 0"),
    ("while x > 0:", "lặp lại các dòng thụt vào bên dưới chừng nào x còn lớn hơn 0", "x = 100 thì lặp; x = 0 thì dừng"),
    ("if x % 2 == 1:", "<code>x % 2</code> là số dư khi chia x cho 2; <code>==</code> là so sánh bằng (khác với một dấu bằng là gán); chỉ khi đúng mới làm dòng thụt vào, tức khi x lẻ", "x = 13: 13 % 2 = 1 nên đúng; x = 12: sai"),
], "Chương trình đếm phép nhân dùng chín ký hiệu, ta đọc bốn cái đầu trước.", [
    "Dòng mở đầu vòng lặp: với mỗi e lần lượt là 100, một triệu, rồi một nghìn tỉ, làm các dòng thụt vào bên dưới.",
    "Một dấu bằng là gán, và có thể gán nhiều giá trị cùng lúc: kết quả nhận 1, cơ số nhận 3, x nhận e, biến đếm nhận 0.",
    "Vòng lặp này lặp lại các dòng thụt vào chừng nào x còn lớn hơn 0.",
    "Dấu phần trăm là chia lấy số dư, hai dấu bằng là so sánh bằng, nên dòng này chỉ làm dòng thụt vào khi x lẻ.",
])

TAB_B = read_steps([
    ("a = a * a % 1000007, kq = kq * a % 1000007", "nhân rồi lấy dư cho 1000007, cất lại vào tên bên trái: dòng đầu bình phương a, dòng sau nhân kq với a", "a = 3: 3 * 3 % 1000007 = 9"),
    ("phep = phep + 1 + x % 2", "đếm phép nhân: mỗi vòng có một phép bình phương, thêm một phép nữa khi x lẻ", "x = 13: phep tăng 2; x = 12: tăng 1"),
    ("x = x // 2", "<code>//</code> là chia lấy phần nguyên: bỏ chữ số nhị phân cuối của x", "13 // 2 = 6"),
    ("kq == pow(3, e, 1000007)", "<code>pow(3, e, m)</code> là hàm có sẵn cho 3 mũ e rồi lấy dư cho m; <code>==</code> cho True nếu hai giá trị bằng nhau", "pow(3, 4, 7) = 4"),
    ("print(e, 'phep nhan:', phep, 'thay vi', e - 1, ...)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách; e − 1 là số phép nếu nhân từng lần", "in ra 100 phep nhan: 10 thay vi 99 …"),
], "Năm ký hiệu còn lại nằm trong thân vòng lặp và dòng in kết quả.", [
    "Hai dòng này nhân rồi lấy dư cho 1000007 và cất lại, một dòng bình phương cơ số, một dòng nhân kết quả với cơ số.",
    "Dòng này đếm phép nhân: mỗi vòng có một phép bình phương, và thêm một phép nữa khi x lẻ.",
    "Hai dấu gạch chéo là chia lấy phần nguyên, nên dòng này bỏ chữ số nhị phân cuối của x.",
    "Hàm có sẵn này cho 3 mũ e rồi lấy dư, và so sánh bằng cho True nếu kết quả của ta khớp với nó.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
], split=3)

quymo = scene("quymo", "example", "Khi số mũ lớn dần: nhân từng lần không kịp, bình phương liên tiếp chỉ vài chục lần", [
    step(
        "<p><b>Chạy thật</b>: tính $3^e \\bmod 1\\,000\\,007$ bằng bình phương liên tiếp, đếm số phép nhân, so với nhân từng lần</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Mỗi vòng lặp bình phương cơ số và lấy dư, rồi chia đôi số mũ, và nhân thêm vào kết quả khi chữ số nhị phân cuối của số mũ, gọi là bit thấp, là một. "
        "Số mũ 100 chỉ cần 10 phép nhân, thay vì 99. Số mũ một triệu cần 27 phép nhân, thay vì gần một triệu. "
        "Số mũ mười mũ mười hai cần 53 phép nhân.",
        focus=[2, ["2.3", "2.8"], "4.1", "4.2", "4.3"], clear=True),
    step(
        '<table class="t"><tr><th>số mũ $e$</th><th>nhân từng lần ($e - 1$ phép)</th><th>bình phương liên tiếp</th></tr>'
        "<tr><td>100</td><td>99 phép</td><td>10 phép</td></tr>"
        "<tr><td>$10^{12}$</td><td>$10^{12}$ phép, khoảng 17 phút (một tỉ phép mỗi giây, số minh hoạ)</td><td>53 phép</td></tr>"
        "<tr><td>số mũ 2048 bit (cỡ mật mã khoá công khai)</td><td>cỡ $2^{2048}$ phép, số có 617 chữ số: không bao giờ xong</td><td>nhiều nhất $2 \\times 2048 = 4096$ phép nhân</td></tr></table>"
        '<div class="box key">Số phép nhân chỉ tỉ lệ với <b>số bit</b> của số mũ, không với giá trị của nó. Mỗi phép nhân vẫn lấy dư ngay, nên số luôn nhỏ hơn $n^2$.</div>',
        "Bảng này cho thấy số phép nhân của bình phương liên tiếp tỉ lệ với số bit, tức số chữ số nhị phân 0 hoặc 1, của số mũ. Với mười mũ mười hai, nhân từng lần mất khoảng 17 phút, còn bình phương liên tiếp chỉ 53 phép. "
        "Với số mũ 2048 bit của mật mã khoá công khai, nhân từng lần không bao giờ xong, còn bình phương liên tiếp tối đa 4 096 phép nhân. "
        "Người làm nghề phải lấy dư sau mỗi phép nhân, để số không phình ra.",
        focus=[1, "1.3", "1.4", 2][:4], clear=True),
], checks=[
    "[(lambda e: (lambda f: f(f, e, 0))(lambda f, x, n: n if x == 0 else f(f, x // 2, n + 1 + x % 2)))(e) for e in (100, 10 ** 6, 10 ** 12)] == [10, 27, 53]",
    "all(pow(3, e, 1000007) == __import__('functools').reduce(lambda r, _: r * 3 % 1000007, range(e), 1) for e in (100, 10 ** 4))",
    "round(10 ** 12 / 1e9 / 60) == 17 and len(str(2 ** 2048)) == 617 and 2 * 2048 == 4096",
])
quymo["steps"] = flat(TAB_A, TAB_B, quymo["steps"])

DE = """# Lab DMS L14 — Nghịch đảo mô-đun, Fermat nhỏ và lũy thừa nhanh bằng chương trình

Viết `luythua.py` (Python 3.11 trở lên); chạy: `python luythua.py`.

In đúng năm dòng (không dấu):
1. `nghich dao cua 7 theo mo-dun 40: <số>` — số b trong 1..39 có `(7*b) % 40 == 1` (duyệt từng b)
2. `nghich dao cua 12 theo mo-dun 18: khong co` — nếu không có b nào trong 1..17 thoả `(12*b) % 18 == 1` thì in `khong co` (viết chương trình in `<số>` nếu có, `khong co` nếu không; với 12 và 18 là `khong co` vì ước chung lớn nhất là 6)
3. `6^100 mod 19: <a> <b>` — `a` tính bằng lũy thừa nhanh (bình phương liên tiếp, lấy dư mỗi bước, tự viết vòng `while`); `b` tính bằng Fermat nhỏ: 19 nguyên tố nên `6^18` đồng dư 1, hạ số mũ 100 thành `100 % 18`, rồi tính `6` mũ số đó theo mô-đun 19. Hai số phải bằng nhau.
4. `so phep nhan cua luy thua nhanh voi mu 1000: <số>` — đếm số lần nhân trong vòng `while` của lũy thừa nhanh khi số mũ là 1000 (mỗi vòng có một phép bình phương, và thêm một phép nhân vào kết quả khi bit thấp của số mũ bằng 1)
5. `2^560 mod 561: <số>, uoc nho nhat cua 561: <số>` — tính 2 mũ 560 theo mô-đun 561 bằng lũy thừa nhanh; rồi tìm ước nhỏ nhất lớn hơn 1 của 561 bằng cách thử chia (561 là hợp số nhưng vẫn qua phép thử Fermat với cơ số 2)

Chấm: `bash labs/cham.sh DMS L14 luythua.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""def nghich_dao(a, n):
    for b in range(1, n):
        if (a * b) % n == 1:
            return b
    return None

def luy_thua_nhanh(a, e, n):
    kq, phep = 1, 0
    while e > 0:
        if e % 2 == 1:
            kq = (kq * a) % n
            phep = phep + 1
        a = (a * a) % n
        e = e // 2
        phep = phep + 1
    return kq, phep

print('nghich dao cua 7 theo mo-dun 40:', nghich_dao(7, 40))
b = nghich_dao(12, 18)
print('nghich dao cua 12 theo mo-dun 18:', 'khong co' if b is None else b)
a1, _ = luy_thua_nhanh(6, 100, 19)
a2, _ = luy_thua_nhanh(6, 100 % 18, 19)
print('6^100 mod 19:', a1, a2)
print('so phep nhan cua luy thua nhanh voi mu 1000:', luy_thua_nhanh(2, 1000, 10 ** 9 + 7)[1])
d = 2
while 561 % d != 0:
    d = d + 1
print('2^560 mod 561: ' + str(luy_thua_nhanh(2, 560, 561)[0]) + ', uoc nho nhat cua 561: ' + str(d))"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> nghịch đảo: thử từng $b$ trong 1..n−1. Lũy thừa nhanh: lặp <code>if e % 2 == 1: kq = kq * a % n</code>, rồi <code>a = a * a % n</code>, <code>e = e // 2</code>. '
    "Fermat: $p$ nguyên tố thì $a^{p-1} \\equiv 1$, nên hạ số mũ bằng <code>e % (p - 1)</code>. "
    "Lời giải ở <code>labs/DMS/L14/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, tìm nghịch đảo bằng cách thử từng số nhỏ hơn mô-đun. Lũy thừa nhanh lặp việc bình phương cơ số và chia đôi số mũ, và nhân vào kết quả khi bit thấp là một. "
    "Với Fermat, số mũ được hạ bằng cách lấy dư cho số nguyên tố trừ một.")
HINT_TAIL = "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử."
H_HTML, H_SAY, H_FOC = hint_parts2(HINT_BOX, HINT_SAY, [
    ("if e % 2 == 1:", "<code>e % 2</code> là số dư khi chia e cho 2, <code>==</code> là so sánh bằng: chỉ khi e lẻ mới làm dòng thụt vào", "e = 5: 5 % 2 = 1 nên đúng"),
    ("kq = kq * a % n, a = a * a % n", "<code>*</code> là nhân; nhân rồi lấy dư cho n và cất lại vào tên bên trái", "kq = 3, a = 9, n = 7: kq thành 27 % 7 = 6"),
    ("e = e // 2", "<code>//</code> là chia lấy phần nguyên: chia đôi số mũ, bỏ chữ số nhị phân cuối", "13 // 2 = 6"),
    ("e % (p - 1)", "số dư khi chia e cho p − 1, không phải cho p", "e = 100, p = 7: 100 % 6 = 4"),
], [
    "Dòng đầu chỉ làm dòng thụt vào khi số mũ lẻ, vì dấu phần trăm là chia lấy số dư và hai dấu bằng là so sánh bằng.",
    "Hai dòng sau nhân rồi lấy dư cho mô-đun và cất lại vào tên bên trái, một dòng cho kết quả, một dòng cho cơ số.",
    "Hai dấu gạch chéo là chia lấy phần nguyên, nên dòng này chia đôi số mũ và bỏ chữ số nhị phân cuối.",
    "Biểu thức cuối là số dư của số mũ khi chia cho p trừ 1, chứ không phải cho p.",
], HINT_TAIL)

prac = practice(
    LID, "Tự làm: nghịch đảo, Fermat nhỏ, lũy thừa nhanh và số giả nguyên tố",
    "<p><b>Đề</b>: viết <code>luythua.py</code> tìm nghịch đảo của 7 theo mô-đun 40 và kiểm 12 theo mô-đun 18; tính $6^{100} \\bmod 19$ bằng lũy thừa nhanh và bằng Fermat nhỏ; "
    "đếm số phép nhân của lũy thừa nhanh với số mũ 1 000; và chỉ ra 561 là hợp số dù $2^{560} \\bmod 561 = 1$ (năm dòng, định dạng ở <code>labs/DMS/L14/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Dòng cuối là lý do phép thử Fermat chỉ loại trừ, không chứng minh nguyên tố.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình tìm nghịch đảo theo mô-đun và nhận ra khi nào không có nghịch đảo. "
    "Sau đó tính một lũy thừa lớn theo mô-đun bằng hai cách, bình phương liên tiếp và định lý Fermat nhỏ, và đếm số phép nhân của cách thứ nhất. "
    "Cuối cùng chỉ ra rằng 561 là hợp số dù vẫn qua phép thử Fermat. Năm dòng và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "luythua.py", H_HTML, H_SAY,
    pause=420, focus1=[1, 1, 1, 1, 1, 0][:6], focus3=H_FOC)
patch_cham(prac, LID, "luythua.py")

OBJ = [
    "Tìm nghịch đảo theo mô-đun khi ước chung lớn nhất bằng 1",
    "Dùng định lý Fermat nhỏ để hạ số mũ",
    "Tính lũy thừa theo mô-đun bằng bình phương liên tiếp",
    "Đếm số phép nhân của bình phương liên tiếp khi số mũ lớn dần và so với nhân từng lần",
    "Viết chương trình tìm nghịch đảo, tính lũy thừa theo mô-đun hai cách và nhận ra số giả nguyên tố",
]
# fix6b (SHOULD, thiếu chiều ngược của "khi và chỉ khi"): nếu a x ≡ 1 thì ước chung của a và n chia hết 1
NGUOC = [
    ("vậy $x$ là nghịch đảo.</p>", "vậy $x$ là nghịch đảo. Ngược lại, nếu $a x \\equiv 1$ thì mọi ước chung của $a$ và $n$ chia hết 1, nên $\\gcd(a, n) = 1$.</p>"),
    ("vậy x chính là nghịch đảo. Với a bằng 3 và n bằng 7,", "vậy x chính là nghịch đảo. Ngược lại, nếu a nhân x đồng dư 1 thì mọi ước chung của a và n chia hết 1, nên ước chung lớn nhất bằng 1. Với a bằng 3 và n bằng 7,"),
    ("        focus: [1, 2, 2, 3, 3]\n        say: \"Định lý, a có nghịch đảo", "        focus: [1, 2, 2, 2, 3, 3]\n        say: \"Định lý, a có nghịch đảo"),
]
f, _, _ = apply(LID, quiz_pause=30, drop_asr=("Ba, khi hạ số mũ bằng Fermat, nhớ chia số mũ cho p trừ 1",), repl=asr_keep(LID) + NGUOC + [('focus: [1, 2, 2, 3, 3]\n        say: "Định lý Fermat nhỏ, nếu p là số nguyên tố và p không chia hết a, thì a mũ p trừ 1 đồng dư với 1 theo mô-đun p. Thử với',
                       'focus: [1, 1, 2, 2, 3, 3, 3, 3]\n        say: "Định lý Fermat nhỏ, nếu p là số nguyên tố và p không chia hết a, thì a mũ p trừ 1 đồng dư với 1 theo mô-đun p. Số nguyên tố là số lớn hơn 1 chỉ chia hết cho 1 và chính nó. Thử với'),
                      # fix4 (R2 SHOULD B): bước giản ước (p − 1)! trong ý chứng minh; chu kỳ "chia hết p − 1", không phải "đúng p − 1"
                      ("Mà tích mới bằng a mũ p trừ 1 nhân tích cũ, nên a mũ p trừ 1 phải đồng dư 1.",
                       "Mà tích mới bằng a mũ p trừ 1 nhân tích cũ. Tích cũ là p trừ 1 giai thừa, không chia hết cho p vì p nguyên tố, nên có nghịch đảo theo mô-đun p, và ta giản ước nó ở hai vế được. Vậy a mũ p trừ 1 phải đồng dư 1."),
                      ("mà tích mới $= a^{p - 1} \\times$ tích cũ, nên $a^{p - 1} \\equiv 1$.</p>",
                       "mà tích mới $= a^{p - 1} \\times$ tích cũ. Tích cũ $1 \\times 2 \\times \\dots \\times (p - 1)$ không chia hết cho $p$ (vì $p$ nguyên tố) nên có nghịch đảo: <b>giản ước</b> nó ở hai vế được $a^{p - 1} \\equiv 1$.</p>"),
                      ("Vì 6 bằng 7 trừ 1, vòng này dài đúng p trừ 1 bước, nên các số mũ 0, 6, 12 đều rơi vào cùng chỗ.",
                       "Vì 6 bằng 7 trừ 1, với cơ số 3 vòng này dài đúng p trừ 1 bước. Với cơ số khác, vòng có thể ngắn hơn, nhưng độ dài của nó luôn chia hết p trừ 1, nên các số mũ 0, 6, 12 đều rơi vào cùng chỗ."),
                      ("        focus: [1, 1, 1, 1]\n        say: \"Hình này cho thấy Fermat nhỏ hoạt động thế nào.", "        focus: [1, 1, 1, 1, 1]\n        say: \"Hình này cho thấy Fermat nhỏ hoạt động thế nào."),
                      ("dư 4. Ba, khi hạ số mũ bằng Fermat, nhớ chia số mũ cho p trừ 1, vì chu kỳ lặp là p trừ 1, không phải p.\"", "dư 4. Ba, khi hạ số mũ bằng Fermat, nhớ lấy dư của số mũ cho p trừ 1, vì chu kỳ lặp chia hết cho p trừ 1, chứ không phải cho p.\""),
                      ("chia số mũ cho $p - 1$, <b>không</b> chia cho $p$", "lấy dư số mũ cho $p - 1$ (chu kỳ chia hết $p - 1$), <b>không</b> cho $p$"),
                      ],
                objectives=OBJ,
                covers=[(1, "find_inv"), (2, "example"), (3, "verify"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                assumes_add=("dms_menhde", "dms_dinhly", "dms_tuongduong"))
print(f)
print(ledger_sync(LID, claims={"quymo": "Số mũ 100 cần 10 phép nhân thay vì 99, một triệu cần 27, mười mũ mười hai cần 53, kết quả khớp phép tính có sẵn"}))
