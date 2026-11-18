"""fix4 CS112 L00-L14 (2026-11-15): kiểm độc lập bằng mã thật cho các điểm sửa theo báo cáo người đọc R2_CS112_A.
Chạy: .venv/Scripts/python -B audit/cs112/verify_cs112_fix4.py   (exit 0 = tất cả đúng)
Mỗi hàm check_* tính lại số bằng mã thật (không đọc số từ bài), rồi đối chiếu chữ trên màn hình trong bài YAML."""
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
LES = ROOT / "lessons" / "cs112"
fails = []


def lesson(prefix):
    return next(LES.glob(prefix + "_*.yaml")).read_text(encoding="utf-8")


def ok(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (" — " + str(extra) if extra else ""))
    if not cond:
        fails.append(name)


def check_l00():
    t = lesson("L00")
    ok("L00 hook: A và B cùng kết quả", all(sum(range(1, n + 1)) == n * (n + 1) // 2 for n in range(0, 300)))
    ok("L00 y >= ceil(n/2): n = 5 thì y nhỏ nhất là 3", min(y for y in range(1, 6) if 5 - y <= y) == 3 == math.ceil(5 / 2))
    ok("L00 mọi n: đoạn không rỗng khi và chỉ khi y >= ceil(n/2)", all((len(range(n - y, y + 1)) > 0) == (y >= -(-n // 2)) for n in range(1, 60) for y in range(1, n + 1)))
    ok("L00 hook có hai mã A và B trên màn hình", "chương trình A" in t and "chương trình B" in t and "tong = n * (n + 1) / 2;" in t)


def check_l03():
    caps, prev = [], None
    x = []
    for _ in range(140):
        s = sys.getsizeof(x)
        if s != prev:
            caps.append((s - sys.getsizeof([])) // 8)
            prev = s
        x.append(0)
    print("  sức chứa list đo bằng sys.getsizeof (Python %s): %s" % (sys.version.split()[0], caps))
    ratios = [b / a for a, b in zip(caps[1:], caps[2:])]
    ok("L03 list CPython KHÔNG gấp đôi sức chứa mỗi lần (hệ số tăng dài hạn < 1,5)", caps[-1] / caps[-3] < 1.5, caps)
    if sys.version_info[:2] == (3, 13):
        ok("L03 ghi chú trên màn hình khớp đo thật (3.13): 4, 8, 16, 24, 32, 40, 52, 64", caps[1:9] == [4, 8, 16, 24, 32, 40, 52, 64], caps[1:9])
    t = lesson("L03")
    ok("L03 bài nói rõ không gấp đôi", "không gấp đôi" in t and "4, 8, 16, 24, 32, 40, 52, 64" in t)


def check_l05():
    memo = {0: 1, 1: 2}

    def n_min(h):
        if h not in memo:
            memo[h] = n_min(h - 1) + n_min(h - 2) + 1
        return memo[h]
    seq = [n_min(h) for h in range(11)]
    ok("L05 N(h) = 1, 2, 4, 7, 12, 20, ..., N(10) = 232", seq[:6] == [1, 2, 4, 7, 12, 20] and seq[10] == 232 and seq[8] == 88, seq)
    ok("L05 N(h) >= 2 N(h-2) và N(h) >= 2^(h/2); AVL dưới 232 nút cao tối đa 9", all(n_min(h) >= 2 * n_min(h - 2) for h in range(2, 30)) and all(n_min(h) >= 2 ** (h / 2) for h in range(40)) and n_min(9) < 232)
    t = lesson("L05")
    ok("L05 bảng trên màn hình có 232 và 88", "<td>232</td>" in t and "2 \\cdot 88" in t)


def hanoi_moves(n, a="A", b="B", c="C"):
    return [] if n == 0 else hanoi_moves(n - 1, a, c, b) + [(a, c)] + hanoi_moves(n - 1, b, a, c)


def check_l08():
    for n in (3, 10):
        st = {"A": list(range(n, 0, -1)), "B": [], "C": []}
        legal = True
        for a, c in hanoi_moves(n):
            d = st[a].pop()
            if st[c] and st[c][-1] < d:
                legal = False
            st[c].append(d)
        ok("L08 chạy thật n = %d: mọi nước hợp lệ, cọc C đủ đĩa, số nước = 2^n - 1" % n, legal and st["C"] == list(range(n, 0, -1)) and len(hanoi_moves(n)) == 2 ** n - 1)
    t = lesson("L08")
    ok("L08 lời gọi thứ hai là chuyen(n - 1, b, a, c, dem)", "chuyen(n - 1, b, a, c, dem)" in t)
    ok("L08 bài giảng công thức đóng và biến đếm một ô", "Công thức đóng</b>" in t and "danh sách chỉ có một ô" in t)
    ok("L08 T(10) = 1023 từ công thức đóng", 2 ** 10 - 1 == 1023)


def check_l09():
    first = [n for n in range(1, 70) if int(2.0 ** n - 1) != 2 ** n - 1][0]
    ok("L09 n đầu tiên số thực sai là 54", first == 54, first)
    ok("L09 n = 53 đúng; 2^53 - 1 có 53 bit, 2^54 - 1 có 54 bit", int(2.0 ** 53 - 1) == 2 ** 53 - 1 and (2 ** 53 - 1).bit_length() == 53 and (2 ** 54 - 1).bit_length() == 54)
    ok("L09 5 viết nhị phân là 101", bin(5) == "0b101")
    t = lesson("L09")
    ok("L09 màn hình: dòng n = 54 và 18014398509481983/4", "54 18014398509481983 18014398509481984 False" in t and "18 014 398 509 481 983" in t)
    ok("L09 mục tiêu nói n = 54, không còn n = 60 là chỗ sai đầu", "sai từ n = 54" in t and "sai từ n = 60" not in t)
    ok("L09 lời nói n bằng 54 là chỗ sai đầu tiên", "n bằng 54 là chỗ sai đầu tiên" in t)


def check_l11():
    ok("L11 số tầng khi lấy căn = log2 log2 n = 4, 5, 6, 10", [int(math.log2(m)) for m in (16, 32, 64, 1024)] == [4, 5, 6, 10])
    t = lesson("L11")
    ok("L11 màn hình có cột 4, 5, 6, 10", "<td>16</td><td>4</td>" in t and "<td>1024</td><td>10</td>" in t)


def check_l12():
    ok("L12 điều kiện đều đặn ví dụ: f = n^2, a = b = 2 cho c = 1/2", all(2 * (n // 2) ** 2 * 2 == n * n for n in range(2, 400, 2)))


def check_l13():
    ok("L13 hàng 1 000 000: n(n-1)/2 = 499 999 500 000, n - 1 = 999 999", 10 ** 6 * (10 ** 6 - 1) // 2 == 499999500000 and 10 ** 6 - 1 == 999999)
    t = lesson("L13")
    ok("L13 hàng công thức đủ 5 ô", "<tr><td>1 000 000 (công thức)</td><td>chưa chạy</td><td>499 999 500 000</td><td>chưa chạy</td><td>999 999</td></tr>" in t)


def derange(n, cat_tia, lech=1):
    x, used, kq = [], [False] * (n + 1), [0, 0]

    def thu(i):
        kq[1] += 1
        if i == n:
            if all(x[k] != k + 1 for k in range(n)):
                kq[0] += 1
            return
        for j in range(1, n + 1):
            if used[j] or (cat_tia and j == i + lech):
                continue
            used[j] = True
            x.append(j)
            thu(i + 1)
            x.pop()
            used[j] = False
    thu(0)
    return kq[0], kq[1]


def check_l14():
    got = [(n, derange(n, True), derange(n, False)) for n in (4, 5, 6)]
    want = [(4, (9, 31), (9, 65)), (5, (44, 147), (44, 326)), (6, (265, 853), (265, 1957))]
    ok("L14 lab: j == i + 1 (vị trí đếm từ 0) cho đúng số nghiệm và số nút của mong_doi", got == want, got)
    ok("L14 chép slide cũ (j == i với i đếm từ 0) cho số khác 31 nút (lab chấm SAI)", derange(4, True, lech=0)[1] != 31 and derange(4, True)[1] == 31, derange(4, True, lech=0))
    t = lesson("L14")
    ok("L14 slide Tự làm nói j = i + 1, đếm từ 0", "j = i + 1$ trước khi đi sâu" in t and "đếm từ 0" in t)


for fn in (check_l00, check_l03, check_l05, check_l08, check_l09, check_l11, check_l12, check_l13, check_l14):
    fn()
print("TỔNG: %s" % ("TẤT CẢ ĐÚNG" if not fails else "%d LỖI: %s" % (len(fails), fails)))
sys.exit(1 if fails else 0)
