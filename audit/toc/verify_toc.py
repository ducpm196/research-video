"""Kiểm mọi con số dự định đưa lên màn hình của khoá TOC, bằng tools/checklib.py VÀ một cách tính độc lập (đối chiếu chéo).
Chạy: .venv/Scripts/python audit/toc/verify_toc.py → in PASS/FAIL từng mục."""
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def ok(name, cond):
    R.append((name, bool(cond)))
    print("PASS" if cond else "FAIL", name)


B = "01"
# L00
ok("L00 chuỗi nhị phân độ dài ≤ 3: 15", len(alg.strings(B, 3)) == 15 == 1 + 2 + 4 + 8)
ok("L00 |Σ^k| = 2^k, k=0..6", all(len(alg.strings(B, k, exact=True)) == 2 ** k for k in range(7)))
ok("L00 Σ={a,b,c}: đúng 2 → 9, ≤ 2 → 13", len(alg.strings("abc", 2, True)) == 9 and len(alg.strings("abc", 2)) == 13)
ok("L00 số 1 chẵn, độ dài ≤ 3: 8", sum(w.count("1") % 2 == 0 for w in alg.strings(B, 3)) == 8)
# L01: DFA chia hết cho 3
D3 = {(r, b): (2 * r + int(b)) % 3 for r in range(3) for b in B}
ok("L01 DFA đầy đủ", alg.dfa_complete(D3, {0, 1, 2}, B))
ok("L01 đúng với n = 1..1999", all(alg.dfa_run(D3, 0, {0}, format(n, "b"))[0] == (n % 3 == 0) for n in range(1, 2000)))
ok("L01 110 nhận, đường 0,1,0,0", alg.dfa_run(D3, 0, {0}, "110") == (True, [0, 1, 0, 0]))
ok("L01 111 từ chối, dừng ở 1", alg.dfa_run(D3, 0, {0}, "111") == (False, [0, 1, 0, 1]))
ok("L01 quiz 1001 nhận (9), đường 0,1,2,1,0", alg.dfa_run(D3, 0, {0}, "1001") == (True, [0, 1, 2, 1, 0]))
ok("L01 quiz 1010 từ chối (10), dừng ở 1", alg.dfa_run(D3, 0, {0}, "1010") == (False, [0, 1, 2, 2, 1]))
# L02: NFA kết thúc bằng 01
N01 = {("A", "0"): {"A", "B"}, ("A", "1"): {"A"}, ("B", "1"): {"C"}}
order, tr = alg.subset_construct(N01, "A", B)
ok("L02 dựng tập con: 3 trạng thái tới được", [sorted(s) for s in order] == [["A"], ["A", "B"], ["A", "C"]])
ok("L02 NFA đúng = endswith 01, mọi chuỗi ≤ 10", all(alg.nfa_run(N01, "A", {"C"}, w)[0] == w.endswith("01") for w in alg.strings(B, 10)))
acc, trace = alg.nfa_run(N01, "A", {"C"}, "1101")
ok("L02 chạy 1101: {A},{A},{A},{A,B},{A,C}", acc and [sorted(s) for s in trace] == [["A"], ["A"], ["A"], ["A", "B"], ["A", "C"]])
acc, trace = alg.nfa_run(N01, "A", {"C"}, "0110")
ok("L02 quiz 0110: {A},{A,B},{A,C},{A},{A,B} từ chối", (not acc) and [sorted(s) for s in trace] == [["A"], ["A", "B"], ["A", "C"], ["A"], ["A", "B"]])


def nth_from_end(n):
    d = {(0, "0"): {0}, (0, "1"): {0, 1}}
    for i in range(1, n):
        d[(i, "0")] = {i + 1}; d[(i, "1")] = {i + 1}
    return d


for n in (2, 3, 4, 5):
    o, _ = alg.subset_construct(nth_from_end(n), 0, B)
    ok(f"L02 “ký hiệu thứ {n} từ cuối là 1”: NFA {n + 1} trạng thái → DFA {len(o)} = 2^{n}", len(o) == 2 ** n)
ok("L02 NFA thứ 3 từ cuối đúng nghĩa (≤ 9)", all(alg.nfa_run(nth_from_end(3), 0, {3}, w)[0] == (len(w) >= 3 and w[-3] == "1") for w in alg.strings(B, 9)))
# DFA tối tiểu cho “thứ 3 từ cuối” thật sự cần 8 trạng thái
o3, t3 = alg.subset_construct(nth_from_end(3), 0, B)
cls, dead, _ = alg.minimize(o3, B, t3, frozenset([0]), {s for s in o3 if 3 in s})
ok("L02 DFA 8 trạng thái đó đã tối tiểu (8 lớp)", len(cls) == 8 and not dead)
# L03
ok("L03 (0|1)*01 = kết thúc bằng 01, ≤ 8", alg.regex_lang("(0|1)*01", B, 8) == {w for w in alg.strings(B, 8) if w.endswith("01")})
ok("L03 0*(10*10*)* = số 1 chẵn, ≤ 8", alg.regex_lang("0*(10*10*)*", B, 8) == {w for w in alg.strings(B, 8) if w.count("1") % 2 == 0})
ok("L03 (0|1)*11(0|1)* = chứa 11, ≤ 8", alg.regex_lang("(0|1)*11(0|1)*", B, 8) == {w for w in alg.strings(B, 8) if "11" in w})
ok("L03 01* khớp 0111 không khớp 0101; (01)* ngược lại",
   re.fullmatch("01*", "0111") and not re.fullmatch("01*", "0101") and re.fullmatch("(01)*", "0101") and not re.fullmatch("(01)*", "0111"))
ok("L03 0|1*: khớp 0 và 111, không khớp 0111", re.fullmatch("0|1*", "0") and re.fullmatch("0|1*", "111") and not re.fullmatch("0|1*", "0111"))
ok("L03 tham chiếu ngược (0|1)+\\1... dùng (.+)\\1: khớp 0101, không khớp 0110",
   re.fullmatch(r"(.+)\1", "0101") and not re.fullmatch(r"(.+)\1", "0110"))
ok("L03 quiz độ dài chẵn ((0|1)(0|1))*", alg.regex_lang("((0|1)(0|1))*", B, 8) == {w for w in alg.strings(B, 8) if len(w) % 2 == 0})
# L04 bổ đề bơm


def L0n1n(s):
    n = len(s) // 2
    return s == "0" * n + "1" * n


for p in range(1, 9):
    ok(f"L04 0^p1^p, p={p}: không cách tách nào bơm được", alg.pump_survivors("0" * p + "1" * p, p, L0n1n) == [])
ok("L04 p=4: có 10 cách tách", sum(1 for i in range(5) for j in range(i + 1, 5)) == 10)
ok("L04 p=4: mọi cách tách có y toàn số 0", all(set("00001111"[i:j]) == {"0"} for i in range(5) for j in range(i + 1, 5)))
ok("L04 ví dụ y = 00 (k=2), bơm lên: 000000 1111 có 6 số 0, 4 số 1", "0" * 2 + "00" * 2 + "1111" == "000000" + "1111")


def L0n12n(s):
    n = s.count("0")
    return s == "0" * n + "1" * (2 * n)


for p in range(1, 7):
    ok(f"L04 quiz 0^p1^2p, p={p}: không cách tách nào bơm được", alg.pump_survivors("0" * p + "1" * (2 * p), p, L0n12n) == [])
ok("L04 quiz p=3, y=0, i=0: 00 111111 — 2 số 0, 6 số 1, 6 ≠ 2·2", not L0n12n("00" + "111111"))
# Ngôn ngữ chính quy thoả bổ đề: (01)* với p = 2
ok("L04 (01)* chính quy, mọi w ≤ 10 dài ≥ 2 bơm được với p=2",
   all(alg.pump_survivors(w, 2, lambda s: re.fullmatch("(01)*", s) is not None) for w in alg.strings(B, 10)
       if len(w) >= 2 and re.fullmatch("(01)*", w)))
# L05 tối thiểu hoá
S4 = {("s", "0"): "a", ("s", "1"): "c", ("a", "0"): "a", ("a", "1"): "b", ("b", "0"): "a", ("b", "1"): "c",
      ("c", "0"): "a", ("c", "1"): "c", ("d", "0"): "b", ("d", "1"): "d"}
ok("L05 DFA 4(+1) trạng thái đầy đủ", alg.dfa_complete(S4, {"s", "a", "b", "c", "d"}, B))
ok("L05 DFA s,a,b,c đúng = kết thúc bằng 01 (≤ 10)", all(alg.dfa_run(S4, "s", {"b"}, w)[0] == w.endswith("01") for w in alg.strings(B, 10)))
cls, dead, rounds = alg.minimize(["s", "a", "b", "c", "d"], B, S4, "s", {"b"})
ok("L05 d không tới được; lớp {s,c}, {a}, {b}", dead == {"d"} and sorted(sorted(c) for c in cls) == [["a"], ["b"], ["c", "s"]])
ok("L05 cặp đánh dấu vòng đầu: (b,·) 3 cặp", sum(1 for x in "sac" for y in "b") == 3)
ok("L05 (s,a): ký hiệu 1 đưa tới (c,b) đã đánh dấu", (S4[("s", "1")], S4[("a", "1")]) == ("c", "b"))
ok("L05 (a,c): ký hiệu 1 đưa tới (b,c)", (S4[("a", "1")], S4[("c", "1")]) == ("b", "c"))
ok("L05 (s,c): 0 → (a,a), 1 → (c,c)", (S4[("s", "0")], S4[("c", "0")], S4[("s", "1")], S4[("c", "1")]) == ("a", "a", "c", "c"))
# Nếu không bỏ d trước: d không nhận, gộp sai? kiểm d khác s (d đi tới b bằng 0)
Q4 = {(r, b): (r + int(b)) % 4 for r in range(4) for b in B}
cls4, dead4, _ = alg.minimize([0, 1, 2, 3], B, Q4, 0, {0, 2})
ok("L05 quiz: đếm 1 theo dư 4, nhận khi dư 0 hoặc 2 → 2 lớp {0,2},{1,3}", sorted(sorted(c) for c in cls4) == [[0, 2], [1, 3]])
# L06 văn phạm
PAR = {"S": ["(S)S", ""]}
ok("L06 văn phạm ngoặc sinh đúng các chuỗi cân bằng ≤ 8", alg.cfg_lang(PAR, "S", 8) == {w for w in alg.strings("()", 8) if alg.balanced(w)})
ok("L06 độ dài 6: 5 chuỗi = C3", sum(alg.balanced(w) for w in alg.strings("()", 6, True)) == 5 == math.comb(6, 3) // 4)
ok("L06 5 chuỗi đó", sorted(w for w in alg.strings("()", 6, True) if alg.balanced(w)) == sorted(["((()))", "(()())", "(())()", "()(())", "()()()"]))
ok("L06 quiz độ dài 8: 14 = C4", sum(alg.balanced(w) for w in alg.strings("()", 8, True)) == 14 == math.comb(8, 4) // 5)
Z = {"S": ["0S1", ""]}
ok("L06 S → 0S1 | ε sinh đúng 0^n1^n (≤ 10)", alg.cfg_lang(Z, "S", 10) == {"0" * n + "1" * n for n in range(6)})
ok("L06 suy dẫn 0011: S ⇒ 0S1 ⇒ 00S11 ⇒ 0011 (3 bước)", "S".replace("S", "0S1").replace("S", "0S1").replace("S", "") == "0011")
# L07 mơ hồ
v = alg.bracket_values([1, 2, 3], "+*")
ok("L07 1 + 2 * 3: 2 cây, giá trị 9 và 7", sorted(v) == [7, 9])
ok("L07 văn phạm ưu tiên → 7 (= Python)", eval("1+2*3") == 7)
v = alg.bracket_values([8, 3, 2], "--")
ok("L07 8 - 3 - 2: 2 cây, 3 (kết hợp trái) và 7", sorted(v) == [3, 7] and eval("8-3-2") == 3)
v = alg.bracket_values([2, 3, 4, 5], "*+*")
ok("L07 quiz 2*3+4*5: 5 cây = C3, giá trị {26,46,50,70}", len(v) == 5 and sorted(set(v)) == [26, 46, 50, 70] and sorted(v) == [26, 46, 50, 70, 70])
ok("L07 quiz theo ưu tiên: 26", eval("2*3+4*5") == 26)
ok("L07 số cây n toán tử = Catalan", all(len(alg.bracket_values(list(range(1, n + 2)), "+" * n)) == math.comb(2 * n, n) // (n + 1) for n in range(1, 7)))
# văn phạm không mơ hồ E → E+T | T, T → T*F | F: đếm cây bằng CYK đơn giản — mỗi xâu chỉ một cây (dựng bằng đệ quy)


def trees_unamb(toks):
    """số cây của E → E+T|T; T → T*F|F; F → số. E: tách ở dấu + cuối cùng ngoài; T: tách ở * cuối cùng."""
    from functools import lru_cache

    @lru_cache(None)
    def E(i, j):
        n = T(i, j)
        n += sum(E(i, k) * T(k + 1, j) for k in range(i + 1, j) if toks[k] == "+")
        return n

    @lru_cache(None)
    def T(i, j):
        n = F(i, j)
        n += sum(T(i, k) * F(k + 1, j) for k in range(i + 1, j) if toks[k] == "*")
        return n

    def F(i, j):
        return 1 if i + 1 == j and toks[i].isdigit() else 0
    return E(0, len(toks))


ok("L07 văn phạm ưu tiên: 1+2*3 đúng 1 cây; 2*3+4*5 đúng 1 cây",
   trees_unamb(tuple("1+2*3")) == 1 and trees_unamb(tuple("2*3+4*5")) == 1)
# L08 PDA
acc, tr, why = alg.pda_0n1n("0011")
ok("L08 0011 nhận; ngăn: X, XX, X, rỗng", acc and [s for _, s in tr] == ["X", "XX", "X", ""])
ok("L08 0010 từ chối (0 sau 1)", alg.pda_0n1n("0010")[0] is False and alg.pda_0n1n("0010")[2] == "0 sau 1")
ok("L08 011 từ chối (lấy từ ngăn rỗng)", alg.pda_0n1n("011")[2] == "lấy từ ngăn rỗng")
ok("L08 001 từ chối (còn X)", alg.pda_0n1n("001")[2] == "còn X")
ok("L08 PDA đúng = 0^n1^n (≤ 12)", all(alg.pda_0n1n(w)[0] == L0n1n(w) for w in alg.strings(B, 12)))
acc, tr, _ = alg.pda_0n1n("000111")
ok("L08 quiz 000111: cao nhất 3 X, nhận", acc and max(len(s) for _, s in tr) == 3)
ok("L08 quiz 00111: từ chối, lấy từ ngăn rỗng ở ký hiệu thứ 5", alg.pda_0n1n("00111")[2] == "lấy từ ngăn rỗng" and len(alg.pda_0n1n("00111")[1]) == 4)
# L09 máy Turing cộng một: đầu đọc ở chữ số phải nhất, trạng thái C (nhớ)
INC = {("C", "1"): ("C", "0", "L"), ("C", "0"): ("H", "1", "S"), ("C", "_"): ("H", "1", "S")}
out, steps, st, trace = alg.tm_run(INC, "1011", 3, "C")
ok("L09 1011 → 1100, 3 bước", out == "1100" and steps == 3 and st == "H")
out, steps, st, _ = alg.tm_run(INC, "111", 2, "C")
ok("L09 111 → 1000, 4 bước", out == "1000" and steps == 4)
ok("L09 đúng với mọi n = 0..2047 (n+1)", all(alg.tm_run(INC, format(n, "b"), len(format(n, "b")) - 1, "C")[0] == format(n + 1, "b") for n in range(2048)))
out, steps, _, _ = alg.tm_run(INC, "1001", 3, "C")
ok("L09 quiz 1001 → 1010, 2 bước", out == "1010" and steps == 2)
ok("L09 số bước = số chữ 1 ở cuối + 1", all(alg.tm_run(INC, format(n, "b"), len(format(n, "b")) - 1, "C")[1] ==
   len(format(n, "b")) - len(format(n, "b").rstrip("1")) + 1 for n in range(1, 2048)))
# L10 máy vạn năng: cùng bộ mô phỏng, bảng khác — đảo bit: đi phải, đổi 0↔1, gặp ô trống thì dừng
FLIP = {("F", "0"): ("F", "1", "R"), ("F", "1"): ("F", "0", "R"), ("F", "_"): ("H", "_", "S")}
out, steps, _, _ = alg.tm_run(FLIP, "1011", 0, "F")
ok("L10 đảo bit 1011 → 0100, 5 bước", out == "0100" and steps == 5)
# máy nhận 0^n1^n bằng cách gạch cặp: dùng làm ví dụ máy Turing quyết định ngôn ngữ không chính quy
M01 = {("q0", "0"): ("q1", "x", "R"), ("q0", "y"): ("q3", "y", "R"), ("q0", "_"): ("H", "_", "S"),
       ("q1", "0"): ("q1", "0", "R"), ("q1", "y"): ("q1", "y", "R"), ("q1", "1"): ("q2", "y", "L"),
       ("q2", "0"): ("q2", "0", "L"), ("q2", "y"): ("q2", "y", "L"), ("q2", "x"): ("q0", "x", "R"),
       ("q3", "y"): ("q3", "y", "R"), ("q3", "_"): ("H", "_", "S")}
ok("L10 máy gạch cặp quyết định 0^n1^n (≤ 10)", all((alg.tm_run(M01, w, 0, "q0")[2] == "H") == L0n1n(w) for w in alg.strings(B, 10)))
ok("L10 0011 nhận sau 13 bước", alg.tm_run(M01, "0011", 0, "q0")[1:3] == (13, "H"))
# L10: mã trên màn hình (chép nguyên văn, đổi tên hướng T/P/Đ) phải cho cùng kết quả với alg.tm_run trên cả ba máy


def chay(bang_chuyen, bang, dau, q):
    while (q, bang.get(dau, "_")) in bang_chuyen:
        q, ghi, di = bang_chuyen[(q, bang.get(dau, "_"))]
        bang[dau] = ghi
        dau = dau + {"T": -1, "P": 1, "Đ": 0}[di]
    return bang, q


def vn(table):
    return {k: (a, b, {"L": "T", "R": "P", "S": "Đ"}[m]) for k, (a, b, m) in table.items()}


def chay_ra(table, w, head, q):
    b, q = chay(vn(table), dict(enumerate(w)), head, q)
    lo, hi = min(b), max(b)
    return "".join(b.get(i, "_") for i in range(lo, hi + 1)).strip("_"), q


ok("L10 mã màn hình: cộng một 1011 → 1100", chay_ra(INC, "1011", 3, "C") == ("1100", "H"))
ok("L10 mã màn hình: đảo bit 1011 → 0100", chay_ra(FLIP, "1011", 0, "F") == ("0100", "H"))
ok("L10 mã màn hình = alg.tm_run trên máy gạch cặp, mọi chuỗi ≤ 10",
   all((chay_ra(M01, w, 0, "q0")[1] == "H") == (alg.tm_run(M01, w, 0, "q0")[2] == "H") for w in alg.strings(B, 10)))
ok("L10 mã màn hình: cộng một đúng với n = 0..511 (đi trái quá ô 0)",
   all(chay_ra(INC, format(n, "b"), len(format(n, "b")) - 1, "C")[0] == format(n + 1, "b") for n in range(512)))
# L11
ok("L11 Collatz 27: 111 bước, lớn nhất 9232", alg.collatz(27) == (111, 9232))
ok("L11 Collatz 6: 8 bước", alg.collatz(6)[0] == 8)
# bảng chéo: hàng = chương trình, cột = đầu vào; D đảo đường chéo → khác mọi hàng
T = [[1, 0, 1, 1], [0, 0, 1, 0], [1, 1, 1, 0], [0, 1, 0, 0]]
Dg = [1 - T[i][i] for i in range(4)]
ok("L11 đường chéo 1,0,1,0 → D = 0,1,0,1", [T[i][i] for i in range(4)] == [1, 0, 1, 0] and Dg == [0, 1, 0, 1])
ok("L11 D khác mọi hàng ít nhất ở ô chéo", all(Dg[i] != T[i][i] for i in range(4)) and all(Dg != T[i] for i in range(4)))
# L13
sols, tried = alg.subset_sums([3, 34, 4, 12, 5, 2], 9)
ok("L13 tổng con = 9: 64 tập con, nghiệm {4,5},{3,4,2},{4,5}…", tried == 64 and sorted(sorted(s) for s in sols) == [[2, 3, 4], [4, 5]])
ok("L13 kiểm chứng chỉ {4,5}: 2 phép cộng... 1 phép cộng, so 9", 4 + 5 == 9)
ok("L13 2^n: n=20 → 1048576, n=60 > 10^18", 2 ** 20 == 1048576 and 2 ** 60 > 10 ** 18)
sols, tried = alg.subset_sums([7, 11, 2, 9], 20)
ok("L13 quiz {7,11,2,9} tổng 20: 16 tập con; nghiệm {11,9} và {7,11,2}", tried == 16 and sorted(sorted(s) for s in sols) == [[2, 7, 11], [9, 11]])
# L14 — bài hành trình (audit/toc/sources_L14.md). Hai bộ khớp tham chiếu của bài đối chiếu với re.fullmatch trên mọi mẫu, chuỗi nhỏ.
import itertools as _it
import re as _re
import sympy as sp
_pats = ["".join(p) for k in range(1, 4) for p in _it.product(["a", "a?", "a*", ".", ".*", "=", "b?"], repeat=k)]
_strs = alg.strings("a=b", 4)
ok("L14 bt_match, thompson_match = re.fullmatch trên mọi mẫu ≤ 3 phần × chuỗi ≤ 4 ký tự",
   all(alg.bt_match(p, s)[0] == alg.thompson_match(p, s)[0] == bool(_re.fullmatch(p, s)) for p in _pats for s in _strs))
ok("L14 a?a?a?aaa: 8 cách chọn, chỉ cách cuối (0,0,0) khớp; cách giữ tập 3 nhân 4 = 12 lần xét",
   [c for c in _it.product((1, 0), repeat=3) if sum(c) == 0] == [list(_it.product((1, 0), repeat=3))[-1]]
   and alg.thompson_match("a?a?a?aaa", "aaa")[1:] == ([4, 4, 4], 12))
ok("L14 n lần a?: cách giữ tập n·(n+1) với n = 1..29; n = 29 → 870; 2^29 = 536 870 912",
   all(alg.thompson_match("a?" * n + "a" * n, "a" * n)[2] == n * (n + 1) for n in range(1, 30)) and 2 ** 29 == 536870912)
ok("L14 quay lui (bộ đếm của bài): 142, 7166, 311 294 với n = 5, 10, 15; gấp > 2000 lần từ 5 tới 15",
   [alg.bt_match("a?" * n + "a" * n, "a" * n)[1] for n in (5, 10, 15)] == [142, 7166, 311294] and 311294 > 2000 * 142)
ok("L14 hậu kiểm 2019: 13:42 → 14:09 = 27 phút; 476 thay đổi / 60 ngày ≈ 3,03 giờ một lần",
   (14 * 60 + 9) - (13 * 60 + 42) == 27 and round(60 * 24 / 476, 2) == 3.03)
_k = sp.Symbol("k")
ok("L14 khớp đa thức qua (1,23),(2,33),(3,45) = k² + 7k + 15, cho 555 ở k = 20 (điểm thứ tư CITED)",
   sp.expand(sp.interpolate([(1, 23), (2, 33), (3, 45)], _k) - (_k ** 2 + 7 * _k + 15)) == 0 and 20 ** 2 + 7 * 20 + 15 == 555)
ok("L14 .*.*=.* bằng cách giữ tập: 5 vị trí; x= + 20 x: 106 ≤ 22·5; 20 x: 60 ≤ 20·5, không khớp",
   alg.thompson_match(".*.*=.*", "x=" + "x" * 20) == (True, [3] + [5] * 21, 106)
   and alg.thompson_match(".*.*=.*", "x" * 20)[0] is False and alg.thompson_match(".*.*=.*", "x" * 20)[2] == 60)
ok("L14 RE2 ≈ 10 KB so với ≈ 0,5 KB: gấp 20; 200 mẫu → 2000 KB so với 100 KB", 10 / 0.5 == 20 and 200 * 10 == 2000 and 200 * 0.5 == 100)
print(f"\n{sum(c for _, c in R)}/{len(R)} PASS")
