"""Sinh lab CS112 L15–L29 (nửa B, nâng chuẩn AF2 2026-11-14): ghi labs/CS112/Lxx/{de.md, mong_doi.txt, loi_giai.py} qua audit/labkit.write_lab.
mong_doi.txt = ĐẦU RA THẬT của lời giải (chạy bằng .venv Python). Số liệu lab KHÁC ví dụ trong bài. Độc lập kiểm: verify_cs112_af2b.py tính lại bằng cách khác.
Chạy: .venv/Scripts/python -B audit/cs112/gen_labs_b.py [L15 L16 …]   (không đối số: mọi lab)"""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit"))
sys.stdout.reconfigure(encoding="utf-8")
from labkit import write_lab  # noqa: E402

LABS = {}


def lab(lid, de_md, solution, ext="py"):
    LABS[lid] = (de_md, solution, ext)


def run_py(code, stdin=""):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "s.py"
        p.write_text(code, encoding="utf-8", newline="\n")
        r = subprocess.run([sys.executable, "-B", str(p)], capture_output=True, text=True, encoding="utf-8", input=stdin, cwd=d,
                           env={"PYTHONIOENCODING": "utf-8", "SYSTEMROOT": "C:/Windows"})
        assert r.returncode == 0, r.stderr
        return r.stdout


# ───────────────────────── L15 ─────────────────────────
lab("L15", """
# Lab CS112 L15 — Cận dưới của bốn thành phố và chu trình tối ưu

Cần: Python 3.11 trở lên (không cần thư viện ngoài). Tạo `tsp4.py` (số liệu minh hoạ, khác ví dụ trong bài). Ma trận chi phí 4 thành phố, hàng i cột j là chi phí đi từ i tới j (thành phố đánh số từ 0 trong mã), đường chéo là vô cùng:

```
INF  3 11 13
14 INF 14  7
15  6 INF  2
 8  3  5 INF
```

Viết chương trình: đặt `INF = float("inf")`, khai ma trận bằng danh sách lồng nhau, rồi

1. tìm số nhỏ nhất của mỗi hàng, trừ đi; trên ma trận MỚI tìm số nhỏ nhất của mỗi cột (không phải trên ma trận gốc);
2. in `min hang: [...]`, `min cot: [...]` (hai danh sách số nguyên) và `LB goc: <tổng hai loại rút gọn>`;
3. vét cạn mọi thứ tự ghé ba thành phố còn lại, chỉ số 1, 2, 3 trong mã (dùng `itertools.permutations`) rồi in `Toi uu: <chi phí> qua <thứ tự thành phố đánh số từ 1, bắt đầu và kết thúc ở 1>`, ví dụ `qua 1 3 2 4 1`;
4. in `LB <= toi uu: CO` nếu cận dưới không vượt chi phí tối ưu, ngược lại `KHONG`;
5. tính cận dưới của hai nút con của gốc: nút "đi từ thành phố 1 tới thành phố j" (chỉ số `0` tới `j - 1`): lấy `R` là ma trận đã rút gọn (hàng rồi cột) ở bước 1, gán `INF` cho cả hàng `0`, cả cột `j - 1` và ô `C[j - 1][0]`, rút gọn lại (hàng rồi cột, bỏ qua hàng hay cột chỉ toàn `INF`), cận con = cận gốc + `R[0][j - 1]` + lượng rút gọn mới. In `Nut con 1->2: <cận>` và `Nut con 1->3: <cận>`.

Chạy: `python tsp4.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L15 tsp4.py`.
""", '''
import itertools

INF = float("inf")
C = [[INF, 3, 11, 13], [14, INF, 14, 7], [15, 6, INF, 2], [8, 3, 5, INF]]
n = len(C)
hang = [min(r) for r in C]
R = [[v - m for v in r] for r, m in zip(C, hang)]
cot = [min(R[i][j] for i in range(n)) for j in range(n)]
lb = sum(hang) + sum(cot)
print("min hang:", hang)
print("min cot:", cot)
print("LB goc:", lb)
best = min((sum(C[a][b] for a, b in zip((0,) + p, p + (0,))), p) for p in itertools.permutations(range(1, n)))
print("Toi uu:", best[0], "qua", " ".join(str(x + 1) for x in (0,) + best[1]), "1")
print("LB <= toi uu:", "CO" if lb <= best[0] else "KHONG")


def nut_con(j):
    N = [[v - cot[c] for c, v in enumerate(r)] for r in R]
    chi_phi = N[0][j]
    for k in range(n):
        N[0][k] = INF
        N[k][j] = INF
    N[j][0] = INF
    them = 0
    for i in range(n):
        m = min(N[i])
        if m < INF:
            N[i] = [v - m for v in N[i]]
            them += m
    for c in range(n):
        m = min(N[i][c] for i in range(n))
        if m < INF:
            for i in range(n):
                N[i][c] -= m
            them += m
    return lb + chi_phi + them


print("Nut con 1->2:", nut_con(1))
print("Nut con 1->3:", nut_con(2))
''')


# ───────────────────────── L16 ─────────────────────────
lab("L16", """
# Lab CS112 L16 — Cái túi phân số, và vì sao tham lam sai với cái túi 0/1

Cần: Python 3.11 trở lên (không cần thư viện ngoài). Tạo `tui.py` (số liệu minh hoạ, khác ví dụ trong bài). Túi chứa tối đa `M = 15` kg; năm món đánh số từ 1:

| món | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| nặng `w` (kg) | 10 | 9 | 5 | 6 | 5 |
| giá trị `p` | 37 | 39 | 26 | 22 | 33 |

Dùng `from fractions import Fraction` để phần lấy và giá trị là số chính xác (không làm tròn). Viết chương trình:

1. sắp các món theo đơn giá `p / w` giảm dần (tính đơn giá bằng `Fraction(p, w)`) rồi in `Thu tu mon: ` và số hiệu món (từ 1) theo thứ tự đó, cách nhau một dấu cách;
2. chạy quy tắc tham lam của cái túi PHÂN SỐ, in `x:` và phần lấy `x` của món 1 đến món 5 (mỗi số in bằng `str(Fraction)`, ví dụ `1`, `0`, `5/9`), rồi in `Tong gia tri: <phân số> = <số thập phân làm tròn 2 chữ số>`;
3. chạy cùng thứ tự đơn giá nhưng cho cái túi 0/1 (lấy nguyên món nếu còn vừa, ngược lại bỏ qua món đó, đi tiếp), và vét cạn mọi tập món (dùng `itertools.combinations`) để tìm giá trị lớn nhất có thể của cái túi 0/1; in `Tham lam 0/1: <giá trị>, toi uu 0/1: <giá trị>`;
4. in `Phan so >= 0/1: CO` nếu giá trị tối ưu của cái túi phân số không nhỏ hơn tối ưu 0/1 (lấy một phần là được thêm quyền, nên không thể tệ hơn).

Cú pháp cần dùng (nếu chưa gặp): `Fraction(5, 9)` là phân số 5/9 chính xác, cộng trừ nhân chia các `Fraction` vẫn ra phân số (`Fraction(1, 2) + Fraction(1, 3)` là `5/6`), `str(Fraction(4, 2))` là `'2'`. `from itertools import combinations` rồi `list(combinations([1, 2, 3], 2))` ra `[(1, 2), (1, 3), (2, 3)]`: mọi cách chọn 2 phần tử, không lặp. `sorted(day, key=lambda i: gia_tri[i])` sắp các phần tử của `day` theo số `gia_tri[i]` tăng dần (thêm dấu trừ trước giá trị để giảm dần).

Chạy: `python tui.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L16 tui.py`.
""", '''
import itertools
from fractions import Fraction

M = 15
w = [10, 9, 5, 6, 5]
p = [37, 39, 26, 22, 33]
n = len(w)
thu_tu = sorted(range(n), key=lambda i: -Fraction(p[i], w[i]))
print("Thu tu mon:", " ".join(str(i + 1) for i in thu_tu))

x = [Fraction(0)] * n
con_lai = Fraction(M)
tong = Fraction(0)
for i in thu_tu:
    if w[i] <= con_lai:
        x[i] = Fraction(1)
        con_lai -= w[i]
        tong += p[i]
    else:
        x[i] = con_lai / w[i]
        tong += x[i] * p[i]
        break
print("x:", " ".join(str(v) for v in x))
print(f"Tong gia tri: {tong} = {float(tong):.2f}")

con, tham = M, 0
for i in thu_tu:
    if w[i] <= con:
        con -= w[i]
        tham += p[i]
toi_uu = max(sum(p[i] for i in S) for r in range(n + 1) for S in itertools.combinations(range(n), r) if sum(w[i] for i in S) <= M)
print(f"Tham lam 0/1: {tham}, toi uu 0/1: {toi_uu}")
print("Phan so >= 0/1:", "CO" if tong >= toi_uu else "KHONG")
''')


# ───────────────────────── L17 ─────────────────────────
lab("L17", """
# Lab CS112 L17 — Xếp lịch hội trường: ba tiêu chí và vét cạn

Cần: Python 3.11 trở lên. Tạo `lich.py` (số liệu minh hoạ, khác ví dụ trong bài). Chín sự kiện đánh số từ 1, mỗi sự kiện là `(s, f)` = (giờ bắt đầu, giờ kết thúc); hai sự kiện không chồng giờ khi `f` của cái trước `<= s` của cái sau:

`(6, 8), (4, 9), (1, 3), (10, 12), (3, 6), (0, 5), (6, 13), (6, 11), (1, 7)`

Viết hàm `chon(ds, khoa)`: sắp chỉ số các sự kiện bằng `sorted(range(len(ds)), key=khoa)` (sắp ổn định: hai sự kiện cùng khoá giữ thứ tự ban đầu), rồi duyệt, chọn sự kiện nếu `s >= last` (`last` ban đầu `-1`), trả về danh sách số hiệu (từ 1) đã chọn theo thứ tự duyệt. Rồi in:

1. `Chon theo ket thuc som nhat: ` và danh sách số hiệu, cách nhau một dấu cách (khoá: giờ kết thúc);
2. `So su kien: ` số sự kiện đã chọn;
3. `Bat dau som nhat: <số>, ngan nhat: <số>, vet can: <số>`: số sự kiện chọn được theo khoá giờ bắt đầu, theo khoá độ dài `f - s`, và số lớn nhất tìm bằng vét cạn (thử mọi tập con bằng `itertools.combinations`, giảm dần kích thước tới khi có tập không chồng giờ);
4. `Tham lam = vet can: CO` nếu kết thúc sớm nhất bằng số của vét cạn, ngược lại `KHONG`.

Cú pháp cần dùng (nếu chưa gặp): `key=` là hàm cho mỗi phần tử một "khoá" để sắp; `lambda i: ds[i][1]` là hàm nhỏ trả về giờ kết thúc của sự kiện số `i`. Ví dụ `sorted([0, 1, 2], key=lambda i: [5, 9, 7][i])` ra `[0, 2, 1]` (các khoá 5, 7, 9 tăng dần). `from itertools import combinations` rồi `list(combinations([1, 2, 3], 2))` ra `[(1, 2), (1, 3), (2, 3)]`.

Chạy: `python lich.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L17 lich.py`.
""", '''
import itertools

ds = [(6, 8), (4, 9), (1, 3), (10, 12), (3, 6), (0, 5), (6, 13), (6, 11), (1, 7)]


def chon(ds, khoa):
    last, ra = -1, []
    for i in sorted(range(len(ds)), key=khoa):
        if ds[i][0] >= last:
            ra.append(i + 1)
            last = ds[i][1]
    return ra


def khong_chong(S):
    return all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(S, 2))


def vet_can(ds):
    for k in range(len(ds), 0, -1):
        if any(khong_chong(S) for S in itertools.combinations(ds, k)):
            return k


ket_thuc = chon(ds, lambda i: ds[i][1])
bat_dau = chon(ds, lambda i: ds[i][0])
ngan = chon(ds, lambda i: ds[i][1] - ds[i][0])
vc = vet_can(ds)
print("Chon theo ket thuc som nhat:", " ".join(map(str, ket_thuc)))
print("So su kien:", len(ket_thuc))
print(f"Bat dau som nhat: {len(bat_dau)}, ngan nhat: {len(ngan)}, vet can: {vc}")
print("Tham lam = vet can:", "CO" if len(ket_thuc) == vc else "KHONG")
''')


# ───────────────────────── L18 ─────────────────────────
lab("L18", """
# Lab CS112 L18 — Đổi tiền với mệnh giá 1, 4, 6: bảng từ dưới lên, ghi nhớ từ trên xuống, tham lam sai

Cần: Python 3.11 trở lên. Tạo `doi_tien.py` (số liệu minh hoạ, khác ví dụ trong bài). Mệnh giá `(1, 4, 6)`.

1. Lập bảng `dp[a]` từ dưới lên: số đồng ít nhất để đổi số tiền `a`, với `a` từ 0 đến 20 (`dp[0] = 0`; `dp[a] = 1 + min(dp[a - c])` cho mọi mệnh giá `c <= a`). In `dp: ` và 13 số đầu (`a` từ 0 đến 12), cách nhau một dấu cách.
2. Dựng lại cách đổi 8: từ `a = 8` lùi theo đồng đã dùng (duyệt mệnh giá tăng dần, lấy đồng đầu tiên cho `1 + dp[a - c] == dp[a]`). In `Doi 8: dp <số đồng> dong (<các đồng, từ lớn tới nhỏ>), tham lam <số đồng> dong`, trong đó "tham lam" là lấy đồng lớn nhất còn vừa, lặp lại.
3. In `Tham lam sai o a = ` và danh sách các `a` từ 1 đến 20 mà tham lam cho nhiều đồng hơn `dp`, cách nhau dấu phẩy rồi dấu cách.
4. Đếm lời gọi: viết hàm đệ quy thô `f(a)` (không ghi nhớ) và hàm đệ quy có ghi nhớ bằng từ điển, mỗi hàm tăng một biến đếm mỗi lần được gọi (kể cả lần dừng ở `a == 0` và lần tra bảng). In `Goi f(20): tho <số>, ghi nho <số>`.

Cú pháp cần dùng ở mục 4 (nếu chưa gặp): từ điển `nho = {}` lưu kết quả đã tính: `nho[a] = giatri` ghi, `a in nho` hỏi đã có chưa, `nho[a]` đọc. Biến đếm dùng chung cho mọi lời gọi: đặt `dem = [0]` ở ngoài hàm, trong hàm viết `dem[0] += 1`; hoặc đặt `dem = 0` ở ngoài và viết `global dem` ở dòng đầu của hàm để hàm được sửa biến ngoài.

Chạy: `python doi_tien.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L18 doi_tien.py`.
""", '''
COINS = (1, 4, 6)
A = 20
dp = [0] * (A + 1)
for a in range(1, A + 1):
    dp[a] = 1 + min(dp[a - c] for c in COINS if c <= a)
print("dp:", " ".join(map(str, dp[:13])))


def dung_lai(a):
    ra = []
    while a > 0:
        for c in COINS:
            if c <= a and 1 + dp[a - c] == dp[a]:
                ra.append(c)
                a -= c
                break
    return sorted(ra, reverse=True)


def tham_lam(a):
    n = 0
    for c in sorted(COINS, reverse=True):
        n += a // c
        a %= c
    return n


cach = dung_lai(8)
print(f"Doi 8: dp {len(cach)} dong ({' '.join(map(str, cach))}), tham lam {tham_lam(8)} dong")
sai = [a for a in range(1, A + 1) if tham_lam(a) > dp[a]]
print("Tham lam sai o a =", ", ".join(map(str, sai)))

dem_tho = 0


def f(a):
    global dem_tho
    dem_tho += 1
    if a == 0:
        return 0
    return 1 + min(f(a - c) for c in COINS if c <= a)


nho = {}
dem_nho = 0


def g(a):
    global dem_nho
    dem_nho += 1
    if a in nho:
        return nho[a]
    nho[a] = 0 if a == 0 else 1 + min(g(a - c) for c in COINS if c <= a)
    return nho[a]


assert f(20) == g(20) == dp[20]
print(f"Goi f(20): tho {dem_tho}, ghi nho {dem_nho}")
''')


# ───────────────────────── L19 ─────────────────────────
lab("L19", """
# Lab CS112 L19 — Nhân chuỗi sáu ma trận: bảng theo đoạn, ngoặc và vét cạn

Cần: Python 3.11 trở lên. Tạo `chuoi.py` (số liệu minh hoạ, khác ví dụ trong bài). Sáu ma trận `A1 … A6`, chỉ số từ 1, `A_i` có cỡ `p[i-1] x p[i]` với `p = (7, 4, 9, 5, 8, 3, 6)`.

1. Lập bảng `m[i][j]` (số phép nhân số ít nhất cho `A_i … A_j`, `m[i][i] = 0`) điền theo độ dài đoạn tăng dần, `m[i][j] = min` qua mọi chỗ cắt `k` (`i <= k < j`) của `m[i][k] + m[k+1][j] + p[i-1] * p[k] * p[j]`. Đếm số lần tính biểu thức trong dấu `min` (mỗi cặp `(đoạn, k)` một lần).
2. Truy vết chỗ cắt tốt nhất (nhiều chỗ cắt cùng cho giá trị nhỏ nhất thì lấy `k` nhỏ nhất) rồi dựng chuỗi ngoặc: đoạn một ma trận viết `A<i>`, đoạn dài hơn viết `(` trái, một dấu cách, phải `)`.
3. Vét cạn: liệt kê mọi cách đặt ngoặc bằng đệ quy (với mỗi chỗ cắt, ghép mọi cách của nửa trái với mọi cách của nửa phải), tính số phép nhân của từng cách bằng công thức `a * b * c`, lấy số cách và giá trị nhỏ nhất.

In đúng năm dòng:

```
So phep nhan it nhat: <m[1][6]>
Dat ngoac: <chuỗi ngoặc>
So lan thu cho cat: <số lần đếm ở bước 1>
Vet can: <số cách> cach, nho nhat <giá trị>
Vet can = bang: CO
```

(dòng cuối `CO` nếu giá trị nhỏ nhất của vét cạn bằng `m[1][6]`, ngược lại `KHONG`).

Chạy: `python chuoi.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L19 chuoi.py`.
""", '''
p = (7, 4, 9, 5, 8, 3, 6)
n = len(p) - 1
m = [[0] * (n + 1) for _ in range(n + 1)]
cat = [[0] * (n + 1) for _ in range(n + 1)]
so_lan = 0
for do_dai in range(2, n + 1):
    for i in range(1, n - do_dai + 2):
        j = i + do_dai - 1
        m[i][j] = None
        for k in range(i, j):
            so_lan += 1
            c = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
            if m[i][j] is None or c < m[i][j]:
                m[i][j], cat[i][j] = c, k


def ngoac(i, j):
    if i == j:
        return f"A{i}"
    k = cat[i][j]
    return "(" + ngoac(i, k) + " " + ngoac(k + 1, j) + ")"


def moi_cach(i, j):
    """Mọi cách đặt ngoặc đoạn i..j: danh sách (số phép nhân, hàng, cột)."""
    if i == j:
        return [(0, p[i - 1], p[i])]
    ra = []
    for k in range(i, j):
        for tl, a, b in moi_cach(i, k):
            for tp, b2, c in moi_cach(k + 1, j):
                ra.append((tl + tp + a * b * c, a, c))
    return ra


tat_ca = moi_cach(1, n)
nho_nhat = min(c[0] for c in tat_ca)
print("So phep nhan it nhat:", m[1][n])
print("Dat ngoac:", ngoac(1, n))
print("So lan thu cho cat:", so_lan)
print(f"Vet can: {len(tat_ca)} cach, nho nhat {nho_nhat}")
print("Vet can = bang:", "CO" if nho_nhat == m[1][n] else "KHONG")
''')


# ───────────────────────── L20 ─────────────────────────
lab("L20", """
# Lab CS112 L20 — Dãy con tăng dài nhất và xâu con chung dài nhất

Cần: Python 3.11 trở lên. Tạo `lis_lcs.py` (số liệu minh hoạ, khác ví dụ trong bài).

**Phần 1 — dãy con tăng dài nhất (tăng hẳn)**: `a = [9, 4, 7, 2, 8, 11, 3, 10, 5, 12]`.
1. Lập bảng `L[i]` (độ dài dãy con tăng hẳn dài nhất kết thúc tại `a[i]`, `L[i] = 1 + max(L[j])` qua mọi `j < i` với `a[j] < a[i]`, không có `j` thì `1`). Đếm số lần so sánh `a[j] < a[i]` (mỗi cặp `j < i` một lần).
2. Truy vết một dãy: bắt đầu ở chỉ số `i` NHỎ NHẤT đạt `max(L)`; rồi lùi: chọn `j < i` NHỎ NHẤT có `a[j] < a[i]` và `L[j] == L[i] - 1`; lặp tới khi `L == 1`; in dãy đọc xuôi.
3. Vét cạn: thử mọi tập con KHÁC RỖNG của các chỉ số, tức kích thước `r` từ 1 tới `n` (`itertools.combinations(range(n), r)`; không đếm tập rỗng), lấy độ dài lớn nhất của một dãy con tăng hẳn; số tập con đã thử là `2**n - 1`.

**Phần 2 — xâu con chung dài nhất**: `X = "THUATTOAN"`, `Y = "TOANTHUAT"`. Lập bảng `c` kích thước `(len(X)+1) x (len(Y)+1)`; truy vết từ ô cuối: hai ký tự bằng nhau thì lấy và đi chéo; khác nhau thì đi lên nếu `c[i-1][j] >= c[i][j-1]`, ngược lại sang trái.

In đúng năm dòng:

```
L: <10 số của bảng L, cách nhau một dấu cách>
LIS: <độ dài> qua <dãy, cách nhau dấu cách>; so sanh bang: <số lần so sánh>
Vet can LIS: <độ dài lớn nhất> (<số tập con đã thử> tap con)
LCS: <độ dài> qua <xâu chung>
Bang = vet can: CO
```

(dòng cuối `CO` nếu độ dài LIS của bảng bằng của vét cạn, ngược lại `KHONG`).

Cú pháp cần dùng (nếu chưa gặp): "tập con" là chọn một số phần tử của dãy (có thể không chọn gì, hoặc chọn hết). `from itertools import combinations` rồi `list(combinations(range(3), 2))` ra `[(0, 1), (0, 2), (1, 2)]`: mọi cách chọn 2 chỉ số trong 0, 1, 2, theo thứ tự tăng.

Chạy: `python lis_lcs.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L20 lis_lcs.py`.
""", '''
import itertools

a = [9, 4, 7, 2, 8, 11, 3, 10, 5, 12]
n = len(a)
L = [1] * n
so_sanh = 0
for i in range(n):
    for j in range(i):
        so_sanh += 1
        if a[j] < a[i]:
            L[i] = max(L[i], L[j] + 1)
print("L:", " ".join(map(str, L)))

i = L.index(max(L))
day = [a[i]]
while L[i] > 1:
    i = min(j for j in range(i) if a[j] < a[i] and L[j] == L[i] - 1)
    day.append(a[i])
day.reverse()
print(f"LIS: {max(L)} qua {' '.join(map(str, day))}; so sanh bang: {so_sanh}")

tot, thu = 0, 0
for r in range(1, n + 1):
    for S in itertools.combinations(range(n), r):
        thu += 1
        if all(a[S[t]] < a[S[t + 1]] for t in range(r - 1)):
            tot = max(tot, r)
print(f"Vet can LIS: {tot} ({thu} tap con)")

X, Y = "THUATTOAN", "TOANTHUAT"
c = [[0] * (len(Y) + 1) for _ in range(len(X) + 1)]
for i in range(1, len(X) + 1):
    for j in range(1, len(Y) + 1):
        if X[i - 1] == Y[j - 1]:
            c[i][j] = c[i - 1][j - 1] + 1
        else:
            c[i][j] = max(c[i - 1][j], c[i][j - 1])
i, j, xau = len(X), len(Y), []
while i > 0 and j > 0:
    if X[i - 1] == Y[j - 1]:
        xau.append(X[i - 1])
        i, j = i - 1, j - 1
    elif c[i - 1][j] >= c[i][j - 1]:
        i -= 1
    else:
        j -= 1
print(f"LCS: {c[len(X)][len(Y)]} qua {''.join(reversed(xau))}")
print("Bang = vet can:", "CO" if max(L) == tot else "KHONG")
''')


# ───────────────────────── L21 ─────────────────────────
lab("L21", """
# Lab CS112 L21 — Quy hoạch tuyến tính hai biến: thử mọi giao điểm và chứng chỉ

Cần: Python 3.11 trở lên. Tạo `qhtt.py` (số liệu minh hoạ, khác ví dụ trong bài). Bài toán: lớn nhất `z = 3*x1 + 2*x2` với

```
x1 + x2   <= 9
3*x1 + x2 <= 18
x1        <= 7
x2        <= 6
x1 >= 0, x2 >= 0
```

Dùng `from fractions import Fraction` (nghiệm là phân số chính xác) và `itertools.combinations`. Mỗi ràng buộc và mỗi trục là một đường `a*x1 + b*x2 = c`: bốn đường biên của bốn ràng buộc trên và hai trục `x1 = 0`, `x2 = 0`, cả thảy 6 đường. Viết chương trình:

1. với mọi cặp trong 6 đường, giải hệ hai phương trình bằng trừ vế (cặp song song, định thức `a1*b2 - a2*b1 == 0`, bỏ qua); đếm số cặp giải được;
2. giữ giao điểm thoả cả bốn ràng buộc và `x1 >= 0`, `x2 >= 0` (đó là đỉnh của miền chấp nhận được); tính `z` tại từng đỉnh;
3. dựng chứng chỉ chặn trên: tìm `y1`, `y2` sao cho `y1*(x1 + x2) + y2*(3*x1 + x2)` đúng bằng `3*x1 + 2*x2` (giải hai phương trình theo hệ số của `x1` và `x2`), rồi chặn trên là `y1*9 + y2*18`.

In đúng chín dòng (phân số in bằng `str(Fraction)`, ví dụ `9/2`; đỉnh sắp theo `z` tăng dần):

```
Cap duong giai duoc: <số cặp>
Dinh hop le: <số đỉnh>
(<x1>, <x2>) z = <z>        (một dòng cho mỗi đỉnh, đúng thứ tự trên)
Toi uu: z = <z lớn nhất> tai (<x1>, <x2>)
Chung chi: y1 = <y1>, y2 = <y2>, can tren <chặn trên>
```

Chạy: `python qhtt.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L21 qhtt.py`.
""", '''
import itertools
from fractions import Fraction

rang_buoc = [(1, 1, 9), (3, 1, 18), (1, 0, 7), (0, 1, 6)]
duong = rang_buoc + [(1, 0, 0), (0, 1, 0)]


def hop_le(x, y):
    return x >= 0 and y >= 0 and all(a * x + b * y <= c for a, b, c in rang_buoc)


giai_duoc = 0
dinh = set()
for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(duong, 2):
    det = a1 * b2 - a2 * b1
    if det == 0:
        continue
    giai_duoc += 1
    x = Fraction(c1 * b2 - c2 * b1, det)
    y = Fraction(a1 * c2 - a2 * c1, det)
    if hop_le(x, y):
        dinh.add((x, y))

ds = sorted(dinh, key=lambda p: (3 * p[0] + 2 * p[1], p))
print("Cap duong giai duoc:", giai_duoc)
print("Dinh hop le:", len(ds))
for x, y in ds:
    print(f"({x}, {y}) z = {3 * x + 2 * y}")
x, y = ds[-1]
print(f"Toi uu: z = {3 * x + 2 * y} tai ({x}, {y})")

# y1 + 3*y2 = 3 (he so cua x1), y1 + y2 = 2 (he so cua x2)
y2 = Fraction(3 - 2, 3 - 1)
y1 = 2 - y2
print(f"Chung chi: y1 = {y1}, y2 = {y2}, can tren {y1 * 9 + y2 * 18}")
''')


# ───────────────────────── L22 ─────────────────────────
lab("L22", """
# Lab CS112 L22 — Đơn hình bằng phân số chính xác, và khối Klee–Minty

Cần: Python 3.11 trở lên. Tạo `donhinh.py` (số liệu minh hoạ, khác ví dụ trong bài). Bài toán: lớn nhất `z = 5*x1 + 4*x2` với

```
6*x1 + 4*x2 <= 24
  x1 + 2*x2 <= 6
 -x1 +   x2 <= 1
         x2 <= 2
x1, x2 >= 0
```

Viết hàm `don_hinh(c, A, b, quy_tac)` (dùng `from fractions import Fraction`): bảng gồm `m` hàng ràng buộc (hệ số của biến chính, biến bù `s1…sm`, vế phải) và hàng `z` (hệ số `-c`); gốc toạ độ hợp lệ (mọi `b >= 0`). Mỗi vòng:

- cột vào: với `quy_tac = "am_nhat"` là cột có hệ số hàng `z` âm nhất (hoà thì chỉ số nhỏ nhất); với `quy_tac = "chi_so_nho"` là cột có chỉ số nhỏ nhất trong các cột có hệ số hàng `z` âm (thứ tự cột: `x1, x2, …, s1, s2, …`); không còn hệ số âm thì dừng;
- hàng ra: chỉ xét hệ số dương trong cột vào, lấy tỉ số `vế phải / hệ số` nhỏ nhất, hoà thì hàng của biến cơ sở có chỉ số cột nhỏ nhất;
- xoay: chia hàng ra cho phần tử xoay, trừ bội của nó khỏi mọi hàng khác (kể cả hàng `z`).

Hàm trả về `z`, giá trị các biến chính và số lần xoay; mỗi lần xoay in `Xoay <k>: cot vao <biến>, hang ra <biến cơ sở bị thay>, z = <z>` (tên biến `x1, x2, s1, s2, …`). Rồi in:

```
Xoay 1: ...
Xoay 2: ...
Toi uu: z = <z>, x1 = <x1>, x2 = <x2>
So lan xoay: <số lần>
Klee-Minty n = 4: am nhat <số lần> lan xoay, chi so nho <số lần> lan xoay
```

Khối Klee–Minty `n = 4` (chỉ số `i, j` từ 1 đến `n`): `c[j] = 2**(n-j)`; `A[i][j] = 2**(i-j+1)` nếu `j < i`, `1` nếu `j == i`, `0` nếu `j > i`; `b[i] = 5**i`. Chạy hàm với cả hai quy tắc trên khối đó (không in từng lần xoay ở đây).

Cú pháp cần dùng (nếu chưa gặp): `Fraction(5, 9)` là phân số 5/9 chính xác; cộng, trừ, nhân, chia, so sánh các `Fraction` như số thường (`Fraction(1, 2) + Fraction(1, 3)` ra `5/6`), nên phép xoay không mất độ chính xác. `min(day, key=lambda j: (T[-1][j], j))` lấy phần tử `j` của `day` có cặp `(T[-1][j], j)` nhỏ nhất (so số trước, hoà thì so `j`).

Chạy: `python donhinh.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L22 donhinh.py`.
""", '''
from fractions import Fraction


def don_hinh(c, A, b, quy_tac, in_ra=False):
    n, m = len(c), len(A)
    ten = [f"x{j + 1}" for j in range(n)] + [f"s{i + 1}" for i in range(m)]
    T = [[Fraction(v) for v in A[i]] + [Fraction(int(i == k)) for k in range(m)] + [Fraction(b[i])] for i in range(m)]
    T.append([Fraction(-v) for v in c] + [Fraction(0)] * (m + 1))
    co_so = [n + i for i in range(m)]
    xoay = 0
    while True:
        am = [j for j in range(n + m) if T[-1][j] < 0]
        if not am:
            break
        cot = min(am) if quy_tac == "chi_so_nho" else min(am, key=lambda j: (T[-1][j], j))
        ung = [(T[i][-1] / T[i][cot], co_so[i], i) for i in range(m) if T[i][cot] > 0]
        _, _, hang = min(ung)
        p = T[hang][cot]
        T[hang] = [v / p for v in T[hang]]
        for i in range(m + 1):
            if i != hang and T[i][cot] != 0:
                f = T[i][cot]
                T[i] = [a - f * r for a, r in zip(T[i], T[hang])]
        xoay += 1
        if in_ra:
            print(f"Xoay {xoay}: cot vao {ten[cot]}, hang ra {ten[co_so[hang]]}, z = {T[-1][-1]}")
        co_so[hang] = cot
    x = [Fraction(0)] * (n + m)
    for i, v in enumerate(co_so):
        x[v] = T[i][-1]
    return T[-1][-1], x[:n], xoay


z, x, k = don_hinh([5, 4], [[6, 4], [1, 2], [-1, 1], [0, 1]], [24, 6, 1, 2], "am_nhat", in_ra=True)
print(f"Toi uu: z = {z}, x1 = {x[0]}, x2 = {x[1]}")
print("So lan xoay:", k)
N = 4
c = [2 ** (N - j) for j in range(1, N + 1)]
A = [[2 ** (i - j + 1) if j < i else (1 if j == i else 0) for j in range(1, N + 1)] for i in range(1, N + 1)]
b = [5 ** i for i in range(1, N + 1)]
print(f"Klee-Minty n = 4: am nhat {don_hinh(c, A, b, 'am_nhat')[2]} lan xoay, chi so nho {don_hinh(c, A, b, 'chi_so_nho')[2]} lan xoay")
''')


# ───────────────────────── L23 ─────────────────────────
lab("L23", """
# Lab CS112 L23 — Sắp xếp nhanh: đếm so sánh, ca tệ nhất, cận dưới và sắp xếp đếm

Cần: Python 3.11 trở lên. Tạo `nhanh.py` (số liệu minh hoạ, khác ví dụ trong bài).

1. Viết `phan_hoach(a, lo, hi)` đúng như bài (chốt `p = a[hi]`, `i = lo - 1`, duyệt `j` từ `lo` tới `hi - 1`, nếu `a[j] <= p` thì tăng `i` và đổi chỗ `a[i]`, `a[j]`; cuối cùng đổi `a[i+1]` với `a[hi]`, trả về `i + 1`) và `sap_nhanh(a, lo, hi)` gọi đệ quy hai bên chốt (không gọi cho đoạn có `lo >= hi`). Dùng hai biến đếm: số phép so sánh `a[j] <= p`, và độ sâu đệ quy lớn nhất (lời gọi ngoài cùng tính là tầng 1; chỉ đếm lời gọi có `lo < hi`).
2. Với `a = [7, 3, 9, 1, 8, 2, 6, 4]`: phân hoạch một lần trên bản sao, in mảng sau đó, vị trí chốt và số so sánh; rồi sắp xếp nhanh toàn bộ một bản sao khác, in tổng số so sánh và độ sâu.
3. Với mảng đã sắp `[1, 2, 3, 4, 5, 6, 7, 8]`: in tổng số so sánh và độ sâu.
4. In cận dưới `ceil(log2(n!))` của số so sánh tệ nhất cho `n = 8` (dùng `math.factorial` và `math.ceil(math.log2(...))`).
5. Sắp xếp đếm cho `b = [2, 0, 3, 2, 1, 0, 2, 3, 1]` với khoá `0..3`: đếm số lần, ghi ra mảng đã sắp, in mảng.

In đúng năm dòng:

```
Phan hoach: <mảng sau phân hoạch>, chot o vi tri <q>, <số so sánh> so sanh
Sap nhanh: tong <số> so sanh, do sau <số>
Da sap: tong <số> so sanh, do sau <số>
Can duoi n = 8: <số>
Sap xep dem: <mảng đã sắp>
```

Cú pháp cần dùng (nếu chưa gặp): một biến đếm dùng chung cho mọi lời gọi đệ quy. Cách một: đặt `dem = [0]` ngoài hàm, trong hàm viết `dem[0] += 1`. Cách hai: đặt `so_sanh = 0` ngoài hàm, rồi dòng đầu của hàm viết `global so_sanh` (cho phép hàm sửa biến bên ngoài), sau đó `so_sanh += 1`. Nếu thiếu dòng `global`, Python báo lỗi vì cho rằng `so_sanh` là biến mới của hàm. Hàm vắng dòng `return` trả về `None`.

Chạy: `python nhanh.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L23 nhanh.py`.
""", '''
import math

dem_ss = 0
sau_max = 0


def phan_hoach(a, lo, hi):
    global dem_ss
    p, i = a[hi], lo - 1
    for j in range(lo, hi):
        dem_ss += 1
        if a[j] <= p:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def sap_nhanh(a, lo, hi, sau=1):
    global sau_max
    if lo < hi:
        sau_max = max(sau_max, sau)
        q = phan_hoach(a, lo, hi)
        sap_nhanh(a, lo, q - 1, sau + 1)
        sap_nhanh(a, q + 1, hi, sau + 1)


a = [7, 3, 9, 1, 8, 2, 6, 4]
x = a[:]
q = phan_hoach(x, 0, len(x) - 1)
print(f"Phan hoach: {x}, chot o vi tri {q}, {dem_ss} so sanh")

dem_ss, sau_max = 0, 0
y = a[:]
sap_nhanh(y, 0, len(y) - 1)
print(f"Sap nhanh: tong {dem_ss} so sanh, do sau {sau_max}")

dem_ss, sau_max = 0, 0
z = [1, 2, 3, 4, 5, 6, 7, 8]
sap_nhanh(z, 0, len(z) - 1)
print(f"Da sap: tong {dem_ss} so sanh, do sau {sau_max}")

print("Can duoi n = 8:", math.ceil(math.log2(math.factorial(8))))

b = [2, 0, 3, 2, 1, 0, 2, 3, 1]
dem = [0] * 4
for v in b:
    dem[v] += 1
ra = []
for gia_tri, so_lan in enumerate(dem):
    ra += [gia_tri] * so_lan
print("Sap xep dem:", ra)
''')


# ───────────────────────── L24 ─────────────────────────
lab("L24", """
# Lab CS112 L24 — Dijkstra, Bellman–Ford và chu trình âm

Cần: Python 3.11 trở lên. Tạo `ngan_nhat.py` (số liệu minh hoạ, khác ví dụ trong bài). Đồ thị có hướng, mỗi cạnh là `(u, v, w)` (từ `u` tới `v`, trọng số `w`).

**Đồ thị 1** (mọi `w >= 0`), đỉnh xuất phát `S`:
`(S, A, 7), (S, B, 2), (B, A, 3), (A, C, 1), (B, C, 8), (C, D, 2), (B, D, 9)`

1. Viết Dijkstra: chốt đỉnh chưa chốt có `d` nhỏ nhất (hoà thì theo thứ tự tên `S, A, B, C, D`), nới các cạnh đi ra. In `Chot: ` và thứ tự chốt, `d: ` và `d` của `S, A, B, C, D` (dạng `S=0 A=5 …`), `Duong toi D: ` đường từ `S` tới `D` (lần ngược theo cạnh đã làm `d` giảm lần cuối) kèm ` = ` độ dài.

**Đồ thị 2** (có cạnh âm), đỉnh xuất phát `S`, các cạnh theo đúng thứ tự này:
`(A, C, 2), (B, A, -2), (S, A, 2), (S, B, 3)`

2. Chạy Dijkstra (như bước 1) và Bellman–Ford (lặp tối đa `n - 1 = 3` vòng, mỗi vòng nới mọi cạnh theo thứ tự trên, dừng khi một vòng không đổi gì). In `Canh am: Dijkstra d[A] = <số>, Bellman-Ford d[A] = <số>, so vong co doi: <số vòng có ít nhất một cạnh nới được>`.

**Đồ thị 3**: `(S, A, 1), (A, B, 1), (B, A, -3)`.

3. Chạy Bellman–Ford `n - 1` vòng rồi thêm một vòng kiểm: còn cạnh nới được thì in `Chu trinh am: CO`, ngược lại `Chu trinh am: KHONG`.

Phải in đúng năm dòng theo mẫu:

```
Chot: ...
d: ...
Duong toi D: ... = ...
Canh am: Dijkstra d[A] = ..., Bellman-Ford d[A] = ..., so vong co doi: ...
Chu trinh am: ...
```

Cú pháp cần dùng (nếu chưa gặp): `min(con, key=lambda v: (d[v], dinh.index(v)))` lấy đỉnh `v` trong `con` có cặp `(d[v], vị trí của v trong danh sách dinh)` nhỏ nhất, tức `d` nhỏ nhất, hoà thì đỉnh đứng trước trong `dinh`; `dinh.index("B")` là vị trí của `"B"` trong danh sách `dinh`. Để lần ngược đường đi, ghi `cha[v] = u` mỗi khi `d[v]` giảm, rồi từ `D` lấy `cha` liên tiếp tới `S`. Vô cùng: `float("inf")`.

Chạy: `python ngan_nhat.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L24 ngan_nhat.py`.
""", '''
import heapq

INF = float("inf")


def dijkstra(dinh, canh, s):
    d = {v: INF for v in dinh}
    d[s] = 0
    cha = {}
    chot = []
    xong = set()
    while True:
        con = [v for v in dinh if v not in xong and d[v] < INF]
        if not con:
            break
        u = min(con, key=lambda v: (d[v], dinh.index(v)))
        xong.add(u)
        chot.append(u)
        for a, b, w in canh:
            if a == u and b not in xong and d[u] + w < d[b]:
                d[b] = d[u] + w
                cha[b] = u
    return d, chot, cha


def bellman_ford(dinh, canh, s):
    d = {v: INF for v in dinh}
    d[s] = 0
    co_doi = 0
    for _ in range(len(dinh) - 1):
        doi = False
        for a, b, w in canh:
            if d[a] + w < d[b]:
                d[b] = d[a] + w
                doi = True
        if not doi:
            break
        co_doi += 1
    am = any(d[a] + w < d[b] for a, b, w in canh)
    return d, co_doi, am


D1 = ["S", "A", "B", "C", "D"]
E1 = [("S", "A", 7), ("S", "B", 2), ("B", "A", 3), ("A", "C", 1), ("B", "C", 8), ("C", "D", 2), ("B", "D", 9)]
d, chot, cha = dijkstra(D1, E1, "S")
print("Chot:", " ".join(chot))
print("d:", " ".join(f"{v}={d[v]}" for v in D1))
duong = ["D"]
while duong[-1] != "S":
    duong.append(cha[duong[-1]])
print("Duong toi D:", " ".join(reversed(duong)), "=", d["D"])

D2 = ["S", "A", "B", "C"]
E2 = [("A", "C", 2), ("B", "A", -2), ("S", "A", 2), ("S", "B", 3)]
dd, _, _ = dijkstra(D2, E2, "S")
bd, vong, _ = bellman_ford(D2, E2, "S")
print(f"Canh am: Dijkstra d[A] = {dd['A']}, Bellman-Ford d[A] = {bd['A']}, so vong co doi: {vong}")

D3 = ["S", "A", "B"]
E3 = [("S", "A", 1), ("A", "B", 1), ("B", "A", -3)]
print("Chu trinh am:", "CO" if bellman_ford(D3, E3, "S")[2] else "KHONG")
''')


# ───────────────────────── L25 ─────────────────────────
lab("L25", """
# Lab CS112 L25 — Cây khung nhỏ nhất: hai thuật toán, hợp–tìm và vét cạn

Cần: Python 3.11 trở lên. Tạo `cay_khung.py` (số liệu minh hoạ, khác ví dụ trong bài). Đồ thị VÔ HƯỚNG, sáu đỉnh `A…F`, mười cạnh (mọi trọng số khác nhau):

`A-B 4, A-C 7, B-C 2, B-D 9, C-D 5, C-E 8, D-E 3, D-F 6, E-F 10, A-F 11`

1. **Xét cạnh từ nhẹ đến nặng**: sắp cạnh theo trọng số tăng dần; dùng cấu trúc hợp–tìm (`find` có nén đường đi, `union` gắn gốc nhóm nhỏ hơn vào gốc nhóm lớn hơn) để chỉ lấy cạnh nối hai nhóm khác nhau. In `Kruskal: ` các cạnh đã lấy theo thứ tự lấy, mỗi cạnh dạng `X-Y(w)` (`X` đứng trước `Y` theo thứ tự chữ cái), cách nhau một dấu cách, rồi `, tong <tổng>`.
2. **Mở rộng cây từ A**: mỗi bước thêm cạnh nhẹ nhất có đúng một đầu trong cây (không cần đống: duyệt hết các cạnh). In `Prim tu A: ` các cạnh theo thứ tự thêm (cùng dạng) rồi `, tong <tổng>`.
3. **Vét cạn**: duyệt mọi bộ `n - 1 = 5` trong 10 cạnh (`itertools.combinations`), giữ bộ nối được cả sáu đỉnh (kiểm bằng hợp–tìm: không cạnh nào nối hai đỉnh đã cùng nhóm). In `Vet can: <số cây khung> cay khung, nho nhat <tổng>`.
4. In `Cung tong: CO` nếu ba tổng bằng nhau, ngược lại `KHONG`.

Gợi ý hợp–tìm (nếu chưa gặp): giữ hai danh sách `cha` (cha của mỗi đỉnh, ban đầu mỗi đỉnh là cha của chính nó) và `size` (số đỉnh của nhóm, ban đầu 1 ở mỗi gốc); `find(x)` đi theo `cha` tới gốc (gán lại `cha` của các đỉnh trên đường về gốc để nén đường đi); `union(a, b)` tìm hai gốc, nếu khác nhau thì gắn gốc có `size` nhỏ hơn vào gốc kia rồi cộng `size`, và trả về `True`; nếu cùng gốc trả về `False`. Đừng dùng `all(union(...) for ...)` để lặp: `all` dừng ngay ở phần tử `False` đầu tiên, nên các phép gắn sau không chạy.

Chạy: `python cay_khung.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L25 cay_khung.py`.
""", '''
import itertools

CANH = [("A", "B", 4), ("A", "C", 7), ("B", "C", 2), ("B", "D", 9), ("C", "D", 5), ("C", "E", 8), ("D", "E", 3), ("D", "F", 6), ("E", "F", 10), ("A", "F", 11)]
DINH = "ABCDEF"


class HopTim:
    def __init__(self):
        self.cha = {v: v for v in DINH}
        self.co = {v: 1 for v in DINH}

    def tim(self, x):
        if self.cha[x] != x:
            self.cha[x] = self.tim(self.cha[x])
        return self.cha[x]

    def hop(self, a, b):
        ra, rb = self.tim(a), self.tim(b)
        if ra == rb:
            return False
        if self.co[ra] < self.co[rb]:
            ra, rb = rb, ra
        self.cha[rb] = ra
        self.co[ra] += self.co[rb]
        return True


def ten(e):
    return f"{e[0]}-{e[1]}({e[2]})"


ht = HopTim()
kr = [e for e in sorted(CANH, key=lambda e: e[2]) if ht.hop(e[0], e[1])]
print("Kruskal:", " ".join(map(ten, kr)) + f", tong {sum(e[2] for e in kr)}")

trong = {"A"}
pr = []
while len(trong) < len(DINH):
    e = min((e for e in CANH if (e[0] in trong) != (e[1] in trong)), key=lambda e: e[2])
    pr.append(e)
    trong |= {e[0], e[1]}
print("Prim tu A:", " ".join(map(ten, pr)) + f", tong {sum(e[2] for e in pr)}")

so_cay, nho = 0, None
for bo in itertools.combinations(CANH, len(DINH) - 1):
    h = HopTim()
    if all(h.hop(e[0], e[1]) for e in bo):
        so_cay += 1
        t = sum(e[2] for e in bo)
        nho = t if nho is None or t < nho else nho
print(f"Vet can: {so_cay} cay khung, nho nhat {nho}")
print("Cung tong:", "CO" if sum(e[2] for e in kr) == sum(e[2] for e in pr) == nho else "KHONG")
''')


# ───────────────────────── L26 ─────────────────────────
lab("L26", """
# Lab CS112 L26 — Tập độc lập và phủ đỉnh, kiểm chứng chỉ, cái túi 0/1 giả đa thức

Cần: Python 3.11 trở lên. Tạo `np_khoi.py` (số liệu minh hoạ, khác ví dụ trong bài).

**Phần 1 — quy dẫn**: đồ thị 7 đỉnh `0…6`, 9 cạnh: `(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,0), (1,5), (2,6)`.
- Vét cạn mọi tập con đỉnh (`itertools.combinations`) để tìm kích thước LỚN NHẤT của một tập độc lập (không cạnh nào có cả hai đầu trong tập) và NHỎ NHẤT của một phủ đỉnh (mọi cạnh có ít nhất một đầu trong tập).
- Kiểm chứng chỉ: lấy một tập độc lập lớn nhất `S` (tập đầu tiên tìm được khi duyệt kích thước giảm dần, trong mỗi kích thước theo thứ tự của `combinations`) và duyệt đúng một lần mọi cạnh để kiểm không cạnh nào có cả hai đầu trong `S`; đếm số cạnh đã duyệt.

**Phần 2 — cái túi 0/1** (quy hoạch động bảng `n` hàng, `W + 1` cột): các món `(nặng, giá trị)` = `(3, 8), (5, 10), (4, 7), (6, 13), (2, 3), (7, 12)`. Chạy với `W = 14` và với `W = 14000`; mỗi lần in giá trị lớn nhất, số ô của bảng (`n * (W + 1)`) và số bit để ghi `W` (`W.bit_length()`). Với `W` lớn, được dùng cách tối ưu bộ nhớ, nhưng số ô tính theo công thức vẫn là `n * (W + 1)`.

In đúng bốn dòng:

```
Tap doc lap lon nhat: <a>, phu dinh nho nhat: <b>, tong = <a + b>
Kiem chung chi: duyet <số cạnh> canh, hop le: CO
Cai tui 0/1 W = 14: toi uu <giá trị>, so o bang <số>, so bit cua W: <số>
Cai tui 0/1 W = 14000: toi uu <giá trị>, so o bang <số>, so bit cua W: <số>
```

Chạy: `python np_khoi.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L26 np_khoi.py`.
""", '''
import itertools

N = 7
CANH = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0), (1, 5), (2, 6)]


def doc_lap(S):
    return all(not (a in S and b in S) for a, b in CANH)


def phu(S):
    return all(a in S or b in S for a, b in CANH)


tot = {}
for k in range(N, -1, -1):
    for S in itertools.combinations(range(N), k):
        if doc_lap(set(S)) and "mis" not in tot:
            tot["mis"] = (k, set(S))
        if phu(set(S)):
            tot["mvc"] = k
a, S = tot["mis"]
b = tot["mvc"]
print(f"Tap doc lap lon nhat: {a}, phu dinh nho nhat: {b}, tong = {a + b}")
duyet = 0
hop_le = True
for u, v in CANH:
    duyet += 1
    if u in S and v in S:
        hop_le = False
print(f"Kiem chung chi: duyet {duyet} canh, hop le: {'CO' if hop_le else 'KHONG'}")

MON = [(3, 8), (5, 10), (4, 7), (6, 13), (2, 3), (7, 12)]


def tui(W):
    dp = [0] * (W + 1)
    for w, g in MON:
        for c in range(W, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + g)
    return dp[W]


for W in (14, 14000):
    print(f"Cai tui 0/1 W = {W}: toi uu {tui(W)}, so o bang {len(MON) * (W + 1)}, so bit cua W: {W.bit_length()}")
''')


# ───────────────────────── L27 ─────────────────────────
lab("L27", """
# Lab CS112 L27 — Mini bài tập lớn: ba cách nhân chuỗi ma trận và một quy tắc tham lam

Cần: Python 3.11 trở lên. Tạo `mini_btl.py` (số liệu minh hoạ, khác ví dụ trong bài). Bảy ma trận `A1 … A7`, `A_i` cỡ `p[i-1] x p[i]` với `p = (22, 9, 18, 24, 20, 16, 27, 13)` (chỉ số từ 1; `n = 7`). Cài bốn chiến lược cho cùng một việc "số phép nhân số ít nhất của đoạn `i..j`", mỗi chiến lược một hàm nhận `(i, j)`:

1. **bảng** (từ dưới lên): `m[i][j] = min` qua chỗ cắt `k` của `m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]`, điền theo độ dài đoạn; đếm số lần tính biểu thức trong `min`;
2. **ghi nhớ** (từ trên xuống, từ điển): đệ quy có nhớ; đếm số lần hàm được gọi (kể cả lần tra bảng ra ngay);
3. **vét cạn** (đệ quy không nhớ): đếm số lần hàm được gọi (kể cả lần ở đoạn một ma trận, trả 0);
4. **tham lam**: chọn chỗ cắt `k` có `p[k]` nhỏ nhất trong đoạn (hoà thì `k` nhỏ nhất), rồi làm tiếp hai nửa theo cùng quy tắc; trả về tổng số phép nhân của cách đặt ngoặc đó.

Rồi in đúng sáu dòng, các giá trị tính từ chương trình (không gõ sẵn):

```
Bang: <số phép nhân>, <số lần tính> lan thu cat
Ghi nho: <số phép nhân>, <số lần gọi> loi goi
Vet can: <số phép nhân>, <số lần gọi> loi goi
Tham lam: <số phép nhân>, lech <phần trăm làm tròn 1 chữ số> % so voi toi uu
Ba cach dung bang nhau: CO
Vet can khi n = 9: <số lần gọi> loi goi
```

(Dòng cuối chạy vét cạn thêm một lần với chuỗi `n = 9` ma trận có `p = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12)` và chỉ in số lần gọi; các dòng khác dùng `p` của đề.)

Chạy: `python mini_btl.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L27 mini_btl.py`.
""", '''
P = (22, 9, 18, 24, 20, 16, 27, 13)


def bang(p):
    n = len(p) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    thu = 0
    for do_dai in range(2, n + 1):
        for i in range(1, n - do_dai + 2):
            j = i + do_dai - 1
            ung = []
            for k in range(i, j):
                thu += 1
                ung.append(m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j])
            m[i][j] = min(ung)
    return m[1][n], thu


def ghi_nho(p):
    nho = {}
    goi = [0]

    def f(i, j):
        goi[0] += 1
        if i == j:
            return 0
        if (i, j) not in nho:
            nho[(i, j)] = min(f(i, k) + f(k + 1, j) + p[i - 1] * p[k] * p[j] for k in range(i, j))
        return nho[(i, j)]
    return f(1, len(p) - 1), goi[0]


def vet_can(p):
    goi = [0]

    def f(i, j):
        goi[0] += 1
        if i == j:
            return 0
        return min(f(i, k) + f(k + 1, j) + p[i - 1] * p[k] * p[j] for k in range(i, j))
    return f(1, len(p) - 1), goi[0]


def tham_lam(p):
    def g(i, j):
        if i == j:
            return 0
        k = min(range(i, j), key=lambda k: (p[k], k))
        return g(i, k) + g(k + 1, j) + p[i - 1] * p[k] * p[j]
    return g(1, len(p) - 1)


b, thu = bang(P)
g, goi_g = ghi_nho(P)
v, goi_v = vet_can(P)
t = tham_lam(P)
print(f"Bang: {b}, {thu} lan thu cat")
print(f"Ghi nho: {g}, {goi_g} loi goi")
print(f"Vet can: {v}, {goi_v} loi goi")
print(f"Tham lam: {t}, lech {100 * (t - b) / b:.1f} % so voi toi uu")
print("Ba cach dung bang nhau:", "CO" if b == g == v else "KHONG")
print(f"Vet can khi n = 9: {vet_can((3, 4, 5, 6, 7, 8, 9, 10, 11, 12))[1]} loi goi")
''')


# ───────────────────────── L28 ─────────────────────────
lab("L28", """
# Lab CS112 L28 — Tổng ôn: kiểm ba hệ thức truy hồi bằng tỉ số, và một bẫy tham lam

Cần: Python 3.11 trở lên. Tạo `tong_on.py` (số liệu minh hoạ, khác ví dụ trong bài).

**Phần 1 — hệ thức truy hồi**: với `n = 2**k`, `T(1) = 1`, ba hệ thức

- `A`: `T(n) = 3*T(n/2) + n`
- `B`: `T(n) = 2*T(n/2) + n*n`
- `C`: `T(n) = T(n/2) + 1`

Viết hàm tính `T(n)` đệ quy có nhớ (từ điển) cho từng hệ thức. Dùng định lý thợ trên giấy để chọn hàm chuẩn `g(n)` cho mỗi hệ thức (lũy thừa của `n`, hoặc `log2(n)`), rồi in, cho `n = 1024` và `n = 1048576`, giá trị `T(n)` và tỉ số `T(n) / g(n)` làm tròn 3 chữ số thập phân. Nếu chọn `g` đúng bậc, hai tỉ số ở hai cỡ gần nhau.

**Phần 2 — bẫy tham lam**: mệnh giá `1, 6, 10`, đổi `12`: in số đồng của tham lam (đồng lớn nhất còn vừa, lặp lại) và của quy hoạch động.

In đúng bốn dòng:

```
A: T(1024) = <số>, T(1048576) = <số>, ti so: <số>, <số>
B: T(1024) = <số>, T(1048576) = <số>, ti so: <số>, <số>
C: T(1024) = <số>, T(1048576) = <số>, ti so: <số>, <số>
Doi 12 voi 1, 6, 10: tham lam <số> dong, quy hoach dong <số> dong
```

Chạy: `python tong_on.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L28 tong_on.py`.
""", '''
import math
import sys

sys.setrecursionlimit(10000)


def lam_t(he_thuc):
    nho = {1: 1}

    def t(n):
        if n not in nho:
            nho[n] = he_thuc(t, n)
        return nho[n]
    return t


A = lam_t(lambda t, n: 3 * t(n // 2) + n)
B = lam_t(lambda t, n: 2 * t(n // 2) + n * n)
C = lam_t(lambda t, n: t(n // 2) + 1)
chuan = {"A": lambda n: n ** math.log2(3), "B": lambda n: n ** 2, "C": lambda n: math.log2(n)}
for ten, t in (("A", A), ("B", B), ("C", C)):
    n1, n2 = 1024, 1048576
    print(f"{ten}: T(1024) = {t(n1)}, T(1048576) = {t(n2)}, ti so: {t(n1) / chuan[ten](n1):.3f}, {t(n2) / chuan[ten](n2):.3f}")

menh = (1, 6, 10)
so = 12
n_tl, con = 0, so
for c in sorted(menh, reverse=True):
    n_tl += con // c
    con %= c
dp = [0] * (so + 1)
for a in range(1, so + 1):
    dp[a] = 1 + min(dp[a - c] for c in menh if c <= a)
print(f"Doi 12 voi 1, 6, 10: tham lam {n_tl} dong, quy hoach dong {dp[so]} dong")
''')


# ───────────────────────── L29 ─────────────────────────
lab("L29", """
# Lab CS112 L29 — Mô phỏng ngăn xếp đoạn chờ của Timsort: minrun, bất biến cũ và bản sửa

Cần: Python 3.11 trở lên (không cần thư viện). Tạo `timsort_mo_phong.py` (số liệu minh hoạ, khác ví dụ trong bài).

**Phần 1 — minrun**: hàm `minrun(n)`: đặt `r = 0`; khi `n >= 64`: `r = r | (n & 1)` rồi `n = n >> 1`; trả về `n + r`. Với mỗi `n` trong `1000, 4097, 5000`: tính `minrun`, số đoạn `= ceil(n / minrun)` (dùng `math.ceil`) và xem số đoạn có là lũy thừa của 2 không (số `k` là lũy thừa của 2 khi `k & (k - 1) == 0`). In `n = <n>: minrun <số>, <số đoạn> doan, luy thua cua 2: CO/KHONG`.

**Phần 2 — ngăn xếp đoạn chờ**: dãy độ dài đoạn lần lượt được đẩy vào ngăn xếp (danh sách, đỉnh ở cuối): `62, 109, 119, 37, 22, 55`. Sau mỗi lần đẩy, chạy vòng gộp: khi ngăn xếp có hơn 1 phần tử, đặt `n = len - 2` (chỉ số đoạn B; A là `n - 1`, C là `n + 1`):

- nếu `(n > 0 và s[n-1] <= s[n] + s[n+1])` hoặc (CHỈ ở bản sửa) `(n > 1 và s[n-2] <= s[n-1] + s[n])`: nếu `s[n-1] < s[n+1]` thì `n = n - 1`; rồi gộp `s[n]` và `s[n+1]` thành một phần tử (tổng);
- ngược lại nếu `s[n] <= s[n+1]`: gộp `s[n]` và `s[n+1]`;
- ngược lại: dừng.

Viết hàm nhận cờ `ban_sua` (False là bản cũ, chỉ xét 3 đoạn trên cùng; True là thêm điều kiện thứ hai, xét 4 đoạn). Sau khi đẩy hết, kiểm bất biến trên toàn ngăn xếp: mọi `s[i] > s[i+1] + s[i+2]` và mọi `s[i] > s[i+1]`. In `Ban cu: ngan xep cuoi <danh sách>, bat bien DUNG/HONG` rồi dòng tương tự cho `Ban sua`.

Phải in đúng năm dòng:

```
n = 1000: minrun ..., ... doan, luy thua cua 2: ...
n = 4097: ...
n = 5000: ...
Ban cu: ngan xep cuoi [...], bat bien ...
Ban sua: ngan xep cuoi [...], bat bien ...
```

Chạy: `python timsort_mo_phong.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L29 timsort_mo_phong.py`.
""", '''
import math


def minrun(n):
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


for n in (1000, 4097, 5000):
    m = minrun(n)
    k = math.ceil(n / m)
    print(f"n = {n}: minrun {m}, {k} doan, luy thua cua 2: {'CO' if k & (k - 1) == 0 else 'KHONG'}")


def gop(s, ban_sua):
    while len(s) > 1:
        n = len(s) - 2
        if (n > 0 and s[n - 1] <= s[n] + s[n + 1]) or (ban_sua and n > 1 and s[n - 2] <= s[n - 1] + s[n]):
            if s[n - 1] < s[n + 1]:
                n -= 1
            s[n:n + 2] = [s[n] + s[n + 1]]
        elif s[n] <= s[n + 1]:
            s[n:n + 2] = [s[n] + s[n + 1]]
        else:
            break


def bat_bien(s):
    return all(s[i] > s[i + 1] + s[i + 2] for i in range(len(s) - 2)) and all(s[i] > s[i + 1] for i in range(len(s) - 1))


def chay(day, ban_sua):
    s = []
    for r in day:
        s.append(r)
        gop(s, ban_sua)
    return s


DAY = [62, 109, 119, 37, 22, 55]
for ten, sua in (("Ban cu", False), ("Ban sua", True)):
    s = chay(DAY, sua)
    print(f"{ten}: ngan xep cuoi {s}, bat bien {'DUNG' if bat_bien(s) else 'HONG'}")
''')


def build(ids):
    for lid in ids:
        de, sol, ext = LABS[lid]
        exp = run_py(sol.strip("\n") + "\n") if ext == "py" else None
        d = write_lab("CS112", lid, de, ext, sol, exp)
        print(lid, "→", d)
        print(exp)


if __name__ == "__main__":
    build(sys.argv[1:] or sorted(LABS))
