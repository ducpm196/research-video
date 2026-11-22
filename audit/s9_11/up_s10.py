"""Nâng cấp AF2 Chặng 10: TOC (15) + PLC (14) + PAR (14) + HCI (13) + SEP (12) + CAS (12) = 80 bài."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
sys.stdout.reconfigure(encoding="utf-8")

import af2_upgrader as up  # noqa: E402
import common  # noqa: E402

COVERS = {
    # TOC (L00..L14)
    "TOC:L00": [(1, "sym"), (2, "lang"), (3, "example")],
    "TOC:L01": [(1, "example"), (2, "example"), (3, "verify")],
    "TOC:L02": [(1, "example"), (2, "example"), (3, "pitfalls")],
    "TOC:L03": [(1, "example"), (2, "prec"), (3, "kleene")],
    "TOC:L04": [(1, "why"), (2, "example"), (3, "pitfalls")],
    "TOC:L05": [(1, "sym"), (2, "example"), (3, "unique")],
    "TOC:L06": [(1, "example"), (2, "example"), (3, "verify")],
    "TOC:L07": [(1, "trees"), (2, "example"), (3, "pitfalls")],
    "TOC:L08": [(1, "machine"), (2, "example"), (3, "pitfalls")],
    "TOC:L09": [(1, "design"), (2, "example"), (3, "pitfalls")],
    "TOC:L10": [(1, "evidence"), (2, "universal"), (3, "pitfalls")],
    "TOC:L11": [(1, "intuition"), (2, "proof"), (3, "pitfalls")],
    "TOC:L12": [(1, "example"), (2, "rice"), (3, "classify")],
    "TOC:L13": [(1, "sym"), (2, "equiv"), (3, "picture")],
    "TOC:L14": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5"), (3, "practice")],

    # PLC (L00..L13)
    "PLC:L00": [(1, "sym"), (2, "example"), (3, "impl")],
    "PLC:L01": [(1, "sym"), (2, "example"), (3, "automaton")],
    "PLC:L02": [(1, "example"), (2, "code"), (3, "pitfalls")],
    "PLC:L03": [(1, "sym"), (2, "assoc"), (3, "example")],
    "PLC:L04": [(1, "sym"), (2, "example"), (3, "late")],
    "PLC:L05": [(1, "example"), (2, "sym"), (3, "tradeoff")],
    "PLC:L06": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L07": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L08": [(1, "sym"), (2, "methods"), (3, "pitfalls")],
    "PLC:L09": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L10": [(1, "gen"), (2, "example"), (3, "pitfalls")],
    "PLC:L11": [(1, "limit"), (2, "example"), (3, "pitfalls")],
    "PLC:L12": [(1, "example"), (2, "sharing"), (3, "pitfalls")],
    "PLC:L13": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5"), (3, "practice")],

    # PAR (L00..L13)
    "PAR:L00": [(1, "example"), (2, "measure"), (3, "quiz")],
    "PAR:L01": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PAR:L02": [(1, "example"), (2, "formula"), (3, "pitfalls")],
    "PAR:L03": [(1, "intuition"), (2, "example"), (3, "example")],
    "PAR:L04": [(1, "example"), (2, "check"), (3, "check")],
    "PAR:L05": [(1, "example"), (2, "example"), (3, "check")],
    "PAR:L06": [(1, "example"), (2, "formula"), (3, "check")],
    "PAR:L07": [(1, "example"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L08": [(1, "example"), (2, "example"), (3, "check"), (4, "check")],
    "PAR:L09": [(1, "example"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L10": [(1, "check"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L11": [(1, "formula"), (2, "example"), (3, "example"), (4, "check")],
    "PAR:L12": [(1, "example"), (2, "example"), (3, "check"), (4, "quiz")],
    "PAR:L13": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5"), (3, "practice")],

    # HCI (L00..L12)
    "HCI:L00": [(1, "sym"), (2, "concept"), (3, "example")],
    "HCI:L01": [(1, "example"), (2, "example"), (3, "pitfalls")],
    "HCI:L02": [(1, "example"), (2, "formula"), (3, "check")],
    "HCI:L03": [(1, "formula"), (2, "example"), (3, "check")],
    "HCI:L04": [(1, "formula"), (2, "example"), (3, "pitfalls")],
    "HCI:L05": [(1, "formula"), (2, "example"), (3, "pitfalls")],
    "HCI:L06": [(1, "formula"), (2, "example"), (3, "example"), (4, "pitfalls")],
    "HCI:L07": [(1, "example"), (2, "formula"), (3, "pitfalls")],
    "HCI:L08": [(1, "example"), (2, "pitfalls"), (3, "check")],
    "HCI:L09": [(1, "example"), (2, "formula"), (3, "concept"), (4, "example")],
    "HCI:L10": [(1, "concept"), (2, "example"), (3, "pitfalls")],
    "HCI:L11": [(1, "formula"), (2, "intuition"), (3, "example"), (4, "pitfalls")],
    "HCI:L12": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (2, "check"), (3, "stage4"), (3, "practice")],

    # SEP (L00..L11)
    "SEP:L00": [(1, "sym"), (2, "example"), (3, "formula"), (4, "pitfalls")],
    "SEP:L01": [(1, "example"), (2, "formula"), (3, "law"), (4, "pitfalls")],
    "SEP:L02": [(1, "example"), (2, "formula"), (3, "example"), (4, "check")],
    "SEP:L03": [(1, "example"), (2, "check"), (3, "pitfalls"), (4, "log")],
    "SEP:L04": [(1, "sym"), (2, "example"), (3, "formula"), (4, "pitfalls")],
    "SEP:L05": [(1, "example"), (2, "formula"), (3, "formula"), (4, "pitfalls")],
    "SEP:L06": [(1, "example"), (2, "formula"), (3, "check")],
    "SEP:L07": [(1, "policy"), (2, "example"), (3, "pitfalls")],
    "SEP:L08": [(1, "example"), (2, "formula"), (3, "check")],
    "SEP:L09": [(1, "example"), (2, "formula"), (3, "say_no")],
    "SEP:L10": [(1, "example"), (2, "check"), (3, "duty"), (4, "pitfalls")],
    "SEP:L11": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "lookup"), (4, "stage5")],

    # CAS (L00..L11)
    "CAS:L00": [(1, "example"), (2, "concept"), (3, "formula"), (4, "check")],
    "CAS:L01": [(1, "example"), (2, "formula"), (3, "check"), (4, "check")],
    "CAS:L02": [(1, "formula"), (2, "example"), (3, "check"), (4, "pitfalls")],
    "CAS:L03": [(1, "example"), (2, "formula"), (3, "check"), (4, "example")],
    "CAS:L04": [(1, "formula"), (2, "example"), (3, "check"), (4, "pitfalls")],
    "CAS:L05": [(1, "timeline"), (2, "example"), (3, "check"), (4, "check")],
    "CAS:L06": [(1, "example"), (2, "check"), (3, "pitfalls"), (4, "check")],
    "CAS:L07": [(1, "example"), (2, "check"), (3, "example"), (4, "pitfalls")],
    "CAS:L08": [(1, "example"), (2, "check"), (3, "check"), (4, "check")],
    "CAS:L09": [(1, "formula"), (2, "example"), (3, "example"), (4, "practice")],
    "CAS:L10": [(1, "example"), (2, "check"), (3, "check"), (4, "pitfalls")],
    "CAS:L11": [(1, "formula"), (2, "example"), (3, "inventory"), (4, "quiz")],
}

DATA = {
    "TOC": [
        ("L00", "Liệt kê và đếm mọi chuỗi nhị phân có độ dài tối đa 4",
         "Dùng vòng lặp sinh và liệt kê toàn bộ các chuỗi thuộc bảng chữ cái `{0, 1}` có độ dài từ `0` tới `4` (tính cả chuỗi rỗng `\"\"` độ dài 0), rồi đếm tổng số chuỗi và số chuỗi khác rỗng.\n\n"
         "Định dạng đầu ra (1 dòng):\n`count_le4=<số nguyên> nonempty=<số nguyên>`",
         """from itertools import product
chains = [''.join(p) for k in range(5) for p in product('01', repeat=k)]
nonempty = [s for s in chains if len(s) > 0]
print(f"count_le4={len(chains)} nonempty={len(nonempty)}")"""),

        ("L01", "Dựng DFA 5 trạng thái kiểm tra số nhị phân chia hết cho 5",
         "Cài đặt máy hữu hạn đơn định (DFA) gồm 5 trạng thái phần dư `0..4` theo công thức `du = (2 * du + bit) % 5` bắt đầu từ `0`, nhận khi `du == 0`. Kiểm tra bảng chuyển đủ cả `'0'` và `'1'` tại mọi trạng thái (`complete=1`), kiểm thử toàn bộ số `1..1999`, cùng hai chuỗi `'1010'` (`10`) và `'1011'` (`11`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`states=<số> complete=<0 hoặc 1> s1010=<0 hoặc 1> s1011=<0 hoặc 1> all_2000=<0 hoặc 1>`",
         """tbl = {(r, b): (2 * r + int(b)) % 5
       for r in range(5) for b in ('0', '1')}
complete = all((r, b) in tbl for r in range(5) for b in ('0', '1'))
def dfa_div5(bits):
    s = 0
    for ch in bits: s = tbl[(s, ch)]
    return s == 0
ok = all(dfa_div5(bin(n)[2:]) == (n % 5 == 0) for n in range(1, 2000))
print(f"states=5 complete={int(complete)}",
      f"s1010={int(dfa_div5('1010'))}",
      f"s1011={int(dfa_div5('1011'))} all_2000={int(ok)}")"""),

        ("L02", "Cài phép dựng tập con chuyển NFA {A, B, C} kết thúc bằng '10' sang DFA",
         "Cài đặt thuật toán dựng tập con thật bằng tìm kiếm theo chiều rộng (BFS) từ trạng thái khởi đầu `{A}` của NFA nhận chuỗi kết thúc bằng `'10'` (bảng chuyển NFA: `('A','0')->{'A'}`, `('A','1')->{'A','B'}`, `('B','0')->{'C'}`, trạng thái nhận `'C'`). Chạy DFA vừa dựng trên `'110'` và `'101'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`dfa_states=<số> acc_110=<0 hoặc 1> acc_101=<0 hoặc 1>`",
         """from functools import reduce
nfa = {('A', '0'): {'A'}, ('A', '1'): {'A', 'B'}, ('B', '0'): {'C'}}
st = frozenset({'A'}); q, seen, d = [st], {st}, {}
while q:
    S = q.pop(0)
    for b in '01':
        nx = frozenset().union(*(nfa.get((u, b), set()) for u in S))
        d[(S, b)] = nx
        if nx not in seen: seen.add(nx); q.append(nx)
run = lambda s: 'C' in reduce(lambda u, c: d[(u, c)], s, st)
print(f"dfa_states={len(seen)} acc_110={int(run('110'))}",
      f"acc_101={int(run('101'))}")"""),

        ("L03", "Kiểm chứng biểu thức chính quy (0|1)*10 trên mọi chuỗi dài 0..7",
         "So khớp từng chuỗi nhị phân có độ dài từ `0` tới `7` giữa biểu thức chính quy `^(0|1)*10$` và phép kiểm tra kết thúc bằng `'10'`, đồng thời đếm tổng số chuỗi khớp.\n\n"
         "Định dạng đầu ra (1 dòng):\n`matches=<số nguyên> exact=<0 hoặc 1>`",
         """import re
pat = re.compile(r'^(0|1)*10$')
ok = True; cnt = 0
for L in range(8):
    for m in range(1 << L):
        s = format(m, f'0{L}b') if L else ''
        hit = bool(pat.fullmatch(s))
        if hit != s.endswith('10'):
            ok = False
        cnt += int(hit)
print(f"matches={cnt} exact={int(ok)}")"""),

        ("L04", "Kiểm tra đầy đủ điều kiện tách bơm x, y, z cho p=5 trên 0^5 1^5",
         "Với độ dài bơm `p = 5`, chuỗi `s = '0000011111'` và phép tách `x = '00'`, `y = '00'`, `z = '011111'`: viết chương trình kiểm tra đồng thời các điều kiện `x + y + z == s`, `len(x + y) <= p`, `len(y) >= 1`, sau đó bơm lặp `y` thành `i = 2` (`x + y*2 + z`) và kiểm tra chuỗi mới có phá vỡ tính bằng nhau số chữ `'0'` và `'1'` hay không.\n\n"
         "Định dạng đầu ra (1 dòng):\n`split_ok=<0 hoặc 1> pumped_len=<số nguyên> valid=<0 hoặc 1>`",
         """p = 5
s = '0' * p + '1' * p
x, y, z = '00', '00', '011111'
split_ok = (x + y + z == s) and (len(x + y) <= p) and (len(y) >= 1)
pumped = x + y * 2 + z
in_lang = (pumped == '0' * (len(pumped) // 2) + '1' * (len(pumped) // 2)) and (len(pumped) % 2 == 0)
print(f"split_ok={int(split_ok)} pumped_len={len(pumped)} valid={int(in_lang)}")"""),

        ("L05", "Cài thuật toán đánh dấu cặp tối thiểu hoá DFA 5 trạng thái",
         "Cho DFA 5 trạng thái `{0,1,2,3,4}` (khởi đầu `0`, nhận `{2,4}`, bảng chuyển: `(0,'0')->1, (0,'1')->2, (1,'0')->1, (1,'1')->2, (2,'0')->2, (2,'1')->1, (3,'0')->4, (3,'1')->4, (4,'0')->4, (4,'1')->3`). Hãy chạy lọc trạng thái tới được từ `0`, rồi chạy thuật toán đánh dấu cặp (lặp tới khi không thêm cặp phân biệt mới) để đếm số cặp bị đánh dấu và số trạng thái tối tiểu còn lại.\n\n"
         "Định dạng đầu ra (1 dòng):\n`reachable=<số> marked_pairs=<số> min_dfa_states=<số>`",
         """tr = [(1, 2), (1, 2), (2, 1), (4, 4), (4, 3)]
acc, reach, q = {2, 4}, {0}, [0]
while q:
    for v in tr[q.pop(0)]:
        if v not in reach: reach.add(v); q.append(v)
st = sorted(reach); prs = [(u, v) for u in st for v in st if u < v]
dist = {(u, v) for u, v in prs if (u in acc) != (v in acc)}
pair = lambda a, b: (a, b) if a < b else (b, a)
for _ in st:
    dist |= {(u, v) for u, v in prs
             if any(pair(tr[u][a], tr[v][a]) in dist for a in (0, 1))}
cls = {tuple(v for v in st if pair(u, v) not in dist) for u in st}
print(f"reachable={len(st)} marked_pairs={len(dist)}",
      f"min_dfa_states={len(cls)}")"""),

        ("L06", "Đếm số chuỗi ngoặc cân bằng gồm 5 cặp ngoặc (độ dài 10)",
         "Duyệt tất cả `2^10 = 1024` chuỗi gồm hai ký tự `'('` và `')'` độ dài `10`, giữ lại mọi chuỗi mà số ngoặc đóng không bao giờ vượt ngoặc mở ở bất kỳ tiền tố nào và kết thúc về `0` (số Catalan `C_5`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`catalan_5=<số nguyên>`",
         """valid = []
for m in range(1 << 10):
    s = ''.join('(' if (m >> i) & 1 else ')' for i in range(10))
    bal, ok = 0, True
    for ch in s:
        bal += 1 if ch == '(' else -1
        if bal < 0:
            ok = False; break
    if ok and bal == 0:
        valid.append(s)
print(f"catalan_5={len(valid)}")"""),

        ("L07", "Cài bộ phân tích phân tầng ưu tiên so với tính từ trái sang phải trên '2+3*4'",
         "Cài bộ phân tích đệ quy tách hai tầng (ưu tiên phép nhân `*` chặt hơn phép cộng `+`) và so sánh với bộ tính tuần tự từ trái sang phải trên cùng biểu thức `'2+3*4'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`precedence=<số nguyên> left_to_right=<số nguyên>`",
         """def eval_prec(expr):
    ts = list(expr)
    def fold(op, fn):
        v = fn()
        while ts and ts[0] == op:
            ts.pop(0); v = v * fn() if op == '*' else v + fn()
        return v
    return fold('+', lambda: fold('*', lambda: int(ts.pop(0))))
s = '2+3*4'; v = int(s[0])
for op, d in zip(s[1::2], s[2::2]):
    v = v + int(d) if op == '+' else v * int(d)
print(f"precedence={eval_prec(s)} left_to_right={v}")"""),

        ("L08", "Kiểm chuẩn ôtômat đẩy xuống (PDA) trên toàn bộ chuỗi nhị phân dài 0..10",
         "Cài ôtômat đẩy xuống (đẩy `'0'` vào ngăn xếp ở pha đầu, chuyển pha và lấy `'0'` ra khi gặp `'1'`, từ chối ký tự lạ hoặc `'0'` đứng sau `'1'`). Đối chiếu kết quả của hàm với ngôn ngữ `0^n 1^n` trên toàn bộ `2047` chuỗi nhị phân độ dài `0..10`, cùng hai mẫu `'00001111'` và `'01010101'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`tested=<số> all_match=<0 hoặc 1> ex_00001111=<0 hoặc 1> ex_01010101=<0 hoặc 1>`",
         """def pda(s):
    st, ph1 = [], False
    for ch in s:
        if ch == '0' and not ph1: st.append('0')
        elif ch == '1' and st: ph1 = True; st.pop()
        else: return False
    return not st
spec = lambda s: s == '0' * (len(s) // 2) + '1' * (len(s) // 2)
strs = [format(m, f'0{L}b') if L else ''
        for L in range(11) for m in range(1 << L)]
ok = all(pda(s) == spec(s) for s in strs)
print(f"tested={len(strs)} all_match={int(ok)}",
      f"ex_00001111={int(pda('00001111'))} ex_01010101={int(pda('01010101'))}")"""),

        ("L09", "Chạy máy Turing cộng 1 nhị phân từ phải sang trái trên '10111'",
         "Cài băng và đầu đọc máy Turing bắt đầu từ ô phải nhất của băng `'10111'` (23), dịch sang trái và đổi mọi `'1'` thành `'0'` cho tới khi gặp `'0'` (hoặc ô trống `'_'`) thì ghi `'1'` và dừng ở trạng thái `H`. Đếm tổng số bước thực hiện.\n\n"
         "Định dạng đầu ra (1 dòng):\n`tm_inc=<chuỗi nhị phân> steps=<số bước>`",
         """tape = list('10111'); pos = len(tape) - 1; state = 'C'; steps = 0
while state != 'H':
    sym = '_' if pos < 0 else tape[pos]
    steps += 1
    if sym == '1':
        tape[pos] = '0'; pos -= 1
    else:
        if pos < 0: tape.insert(0, '1')
        else: tape[pos] = '1'
        state = 'H'
print(f"tm_inc={''.join(tape)} steps={steps}")"""),

        ("L10", "Cài bộ mô phỏng máy Turing vạn năng U hỗ trợ đọc, ghi và dịch đầu đọc",
         "Cài bộ mô phỏng máy Turing vạn năng U nhận bảng luật `(trạng_thái, ký_tự_đọc) -> (trạng_thái_mới, ký_tự_ghi, hướng_dịch)` (hướng `'R'` sang phải, `'L'` sang trái, `'S'` đứng yên). Chạy máy đảo mọi bit trên băng `'10110'` cho tới khi gặp ô trống `'_'` thì dừng ở `'H'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`tape_out=<chuỗi> steps=<số nguyên> final_state=<tên trạng thái>`",
         """tbl = {('F', '0'): ('F', '1', 'R'), ('F', '1'): ('F', '0', 'R'), ('F', '_'): ('H', '_', 'S')}
tape = list('10110'); pos = 0; st = 'F'; steps = 0
while st != 'H':
    ch = tape[pos] if 0 <= pos < len(tape) else '_'
    st, write, mv = tbl[(st, ch)]
    if 0 <= pos < len(tape): tape[pos] = write
    pos += 1 if mv == 'R' else (-1 if mv == 'L' else 0)
    steps += 1
print(f"tape_out={''.join(tape)} steps={steps} final_state={st}")"""),

        ("L11", "Kiểm chứng nghịch lý đường chéo trên bảng 3×3 của bài toán dừng",
         "Cho bảng dự đoán giả định 3×3 `rows = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]` ứng với `H(P_i, P_j)` (`1` là dừng, `0` là lặp vô hạn). Duyệt từng hàng ứng viên `D = [d0, d1, d2]` trong `2^3 = 8` khả năng hành vi trên 3 đầu vào để kiểm chứng: nếu `D == row[idx]` thì bắt buộc `D[idx] == 1 - row[idx]` là điều không thể xảy ra.\n\n"
         "Định dạng đầu ra (1 dòng):\n`table_size=<số> candidates=<số> possible_matches=<số nguyên>`",
         """rows = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]
matches = 0
for mask in range(8):
    D = [(mask >> i) & 1 for i in range(3)]
    for idx, row in enumerate(rows):
        if D == row and D[idx] == (1 - row[idx]):
            matches += 1
print(f"table_size=3 candidates=8 possible_matches={matches}")"""),

        ("L12", "Kiểm tra hai điều kiện Định lý Rice trên một họ hàm cụ thể",
         "Xét tính chất ngữ nghĩa `T`: 'hàm luôn trả về số chẵn với mọi đầu vào x thuộc {0, 1, 2}'. Dùng ba hàm thử `f1(x)=2`, `f2(x)=1+1`, `f3(x)=x+1` để kiểm tra bằng máy: (1) có hàm thỏa `T`; (2) có hàm không thỏa `T`; (3) hai hàm viết khác cú pháp (`f1` vs `f2`) cho cùng đầu ra trên `{0, 1, 2}`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`has_yes=<0 hoặc 1> has_no=<0 hoặc 1> syn_diff_same_sem=<0 hoặc 1> rice_applies=<0 hoặc 1>`",
         """f1, f2, f3 = lambda x: 2, lambda x: 1 + 1, lambda x: x + 1
is_even = lambda f: all(f(x) % 2 == 0 for x in (0, 1, 2))
has_yes = any(is_even(f) for f in (f1, f2, f3))
has_no = any(not is_even(f) for f in (f1, f2, f3))
same_sem = [f1(x) for x in (0, 1, 2)] == [f2(x) for x in (0, 1, 2)]
applies = has_yes and has_no and same_sem
print(f"has_yes={int(has_yes)} has_no={int(has_no)}",
      f"syn_diff_same_sem={int(same_sem)} rice_applies={int(applies)}")"""),

        ("L13", "Kiểm chứng chứng chỉ Tổng tập con (Subset Sum) trong thời gian đa thức",
         "Cho tập số `S = [5, 9, 14, 18, 27]` và mục tiêu `T = 46`. Viết hàm kiểm tra chứng chỉ `C = [5, 14, 27]`: xác nhận mọi phần tử của `C` nằm đúng với bội số không vượt quá trong `S` và tổng bằng `T`, đồng thời đếm số phần tử cộng kiểm chứng.\n\n"
         "Định dạng đầu ra (1 dòng):\n`cert_steps=<số nguyên> verified=<0 hoặc 1> cert_sum=<số nguyên>`",
         """S = [5, 9, 14, 18, 27]; T = 46; cert = [5, 14, 27]
pool = list(S); in_S = True
for x in cert:
    if x in pool: pool.remove(x)
    else: in_S = False
tot = sum(cert)
print(f"cert_steps={len(cert)} verified={int(in_S and tot == T)} cert_sum={tot}")"""),

        ("L14", "So sánh bùng nổ nhánh quay lui 2^n và số tập vị trí n + 1 trên mẫu dài n=25",
         "Với mẫu `(a?){n}a{n}` ở `n = 25` (chuỗi `'a'*25`): tính số nhánh quay lui tệ nhất `2^n`, kích thước tập vị trí chạy song song của máy Thompson `n + 1`, và tổng số bước kiểm tra trên toàn chuỗi dài `n` (`n * (n + 1)`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`backtrack=<số nguyên> subset_pos=<số nguyên> linear_checks=<số nguyên>`",
         """n = 25
backtrack = 2 ** n
subset_pos = n + 1
linear_checks = n * subset_pos
print(f"backtrack={backtrack} subset_pos={subset_pos} linear_checks={linear_checks}")"""),
    ],

    "PLC": [
        ("L00", "Phân biệt lỗi pha cú pháp (pha 2) và pha ngữ nghĩa (pha 3) trên danh sách từ tố",
         "Cài hàm kiểm tra cho danh sách từ tố (token): pha cú pháp (pha 2) duyệt ngăn xếp/độ sâu ngoặc kiểm tra đóng mở cân bằng và không âm dọc chuỗi `['(', '1', '+', '2']`; pha ngữ nghĩa (pha 3) tra bảng biến đã khai báo `{'x': 1}` với biến `'y'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`syn_err=<0 hoặc 1> sem_err=<0 hoặc 1>`",
         """def check_syntax(tokens):
    depth = 0
    for tk in tokens:
        if tk == '(': depth += 1
        elif tk == ')': depth -= 1
        if depth < 0: return False
    return depth == 0
def check_sem(env, var):
    return var in env
print(f"syn_err={int(not check_syntax(['(', '1', '+', '2']))} sem_err={int(not check_sem({'x': 1}, 'y'))}")"""),

        ("L01", "Bộ tách từ tố cho biểu thức 'total = 108 - cnt'",
         "Dùng `re.findall` với mẫu nhận chữ danh định `[A-Za-z_]\\w*`, số nguyên `\\d+` và toán tử `[=+*/-]` để tách chuỗi `'total = 108 - cnt'` thành danh sách các từ tố.\n\n"
         "Định dạng đầu ra (1 dòng):\n`count=<số nguyên> toks=<danh sách từ tố>`",
         r"""import re
toks = re.findall(r'[A-Za-z_]\w*|\d+|[=+*/-]', 'total = 108 - cnt')
print(f"count={len(toks)} toks={toks}")"""),

        ("L02", "Bộ phân tích đệ quy xuống theo tầng expr/term/atom cho hai biểu thức số học",
         "Cài bộ phân tích đệ quy xuống theo đúng thứ tự ba tầng `expr`, `term`, `atom` (nhân `*` gắn chặt hơn cộng `+`), kiểm tra trên `'3+4*5'` và `'(3+4)*5'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`p1=<số nguyên> p2=<số nguyên>`",
         """def parse_val(s):
    ts = list(s.replace(' ', ''))
    def atom():
        if ts[0] != '(': return int(ts.pop(0))
        ts.pop(0); v = expr(); ts.pop(0); return v
    def fold(op, fn):
        v = fn()
        while ts and ts[0] == op:
            ts.pop(0); v = v * fn() if op == '*' else v + fn()
        return v
    expr = lambda: fold('+', lambda: fold('*', atom))
    return expr()
print(f"p1={parse_val('3+4*5')} p2={parse_val('(3+4)*5')}")"""),

        ("L03", "Tính kết hợp trái của phép trừ trên bộ ba số [15, 6, 2]",
         "So sánh kết quả gộp trái đúng luật của biểu thức `15 - 6 - 2` với cách gộp phải sai `15 - (6 - 2)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`left_assoc=<số nguyên> right_assoc=<số nguyên>`",
         """nums = [15, 6, 2]
left_assoc = (nums[0] - nums[1]) - nums[2]
right_assoc = nums[0] - (nums[1] - nums[2])
print(f"left_assoc={left_assoc} right_assoc={right_assoc}")"""),

        ("L04", "Mô phỏng chuỗi môi trường tra tên: phạm vi tĩnh so với phạm vi động",
         "Cài hàm `lookup(env, name)` duyệt theo liên kết cha để so sánh tra tên theo phạm vi tĩnh (từ vị trí định nghĩa hàm với `x = 15`) và phạm vi động (theo ngăn xếp lời gọi với `x = 30`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`static=<số nguyên> dynamic=<số nguyên>`",
         """def lookup(env, name):
    while env is not None:
        if name in env['vars']: return env['vars'][name]
        env = env['parent']
global_env = {'vars': {'x': 15}, 'parent': None}
fn_def_parent = global_env
def call_fn(caller_env, dynamic=False):
    local_env = {'vars': {}, 'parent': caller_env if dynamic else fn_def_parent}
    return lookup(local_env, 'x')
caller_env = {'vars': {'x': 30}, 'parent': global_env}
print(f"static={call_fn(caller_env, False)} dynamic={call_fn(caller_env, True)}")"""),

        ("L05", "Kiểm kiểu tĩnh đệ quy trên cây phép toán (+, -, *, /) bắt lỗi int + str",
         "Cài hàm đệ quy `check_tree(node)` cho cây phép toán gồm lá `('lit', kieu)` và nút `(op, trai, phai)` với `op` thuộc `{'+', '-', '*', '/'}`: chỉ hợp lệ khi hai nhánh cùng kiểu `'int'`. Kiểm tra cây đúng `('+', ('lit','int'), ('*', ('lit','int'), ('lit','int')))` và cây lỗi `('-', ('lit','int'), ('lit','str'))`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`ok_expr=<0 hoặc 1> err_expr=<0 hoặc 1>`",
         """def check_tree(node):
    if node[0] == 'lit': return node[1]
    _, a, b = node
    ta, tb = check_tree(a), check_tree(b)
    return 'int' if (ta == 'int' and tb == 'int') else None
t_ok = ('+', ('lit', 'int'), ('*', ('lit', 'int'), ('lit', 'int')))
t_err = ('-', ('lit', 'int'), ('lit', 'str'))
print(f"ok_expr={int(check_tree(t_ok) is not None)} err_expr={int(check_tree(t_err) is not None)}")"""),

        ("L06", "Giải ràng buộc kiểu bằng thuật toán hợp nhất thay thế lặp",
         "Cho danh sách ràng buộc kiểu giữa các biến chưa biết và kiểu cụ thể `constraints = [('ret', 't_x'), ('t_x', 't_y'), ('t_y', 'int')]`. Chạy vòng lặp hợp nhất thế dần cho tới khi cả `'t_x'` và `'ret'` đều được suy ra kiểu `'int'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`inferred_tx=<kiểu> ret=<kiểu>`",
         """constraints = [('ret', 't_x'), ('t_x', 't_y'), ('t_y', 'int')]
known = {}
for _ in range(len(constraints)):
    for lhs, rhs in constraints:
        if rhs in known: known[lhs] = known[rhs]
        elif rhs in ('int', 'bool'): known[lhs] = rhs
print(f"inferred_tx={known['t_x']} ret={known['ret']}")"""),

        ("L07", "Bao đóng giữ môi trường riêng: hai bộ cộng độc lập với step khác nhau",
         "Cài hàm `make_adder(start, step)` trả về bao đóng mỗi lần gọi cộng thêm `step` vào biến đếm riêng bắt đầu từ `start`. Tạo `a1 = make_adder(20, 4)` gọi 2 lần và `a2 = make_adder(20, 7)` gọi 1 lần.\n\n"
         "Định dạng đầu ra (1 dòng):\n`a1=<danh sách 2 phần tử> a2=<số nguyên>`",
         """def make_adder(start, step):
    val = [start]
    def inc():
        val[0] += step
        return val[0]
    return inc
a1, a2 = make_adder(20, 4), make_adder(20, 7)
print(f"a1={[a1(), a1()]} a2={a2()}")"""),

        ("L08", "Đánh dấu-quét theo chiều rộng (BFS) thu hồi vòng rác trên đồ thị vùng đống",
         "Cài thuật toán đánh dấu-quét dùng hàng đợi tìm theo chiều rộng (`pop(0)`) từ gốc `'R'` trên đồ thị đối tượng `{'R': ['A'], 'A': ['B'], 'B': [], 'C': ['D'], 'D': ['C'], 'E': []}` để giữ lại các nút sống và liệt kê danh sách nút rác bị thu hồi theo thứ tự tăng dần.\n\n"
         "Định dạng đầu ra (1 dòng):\n`alive=<danh sách sắp xếp> reclaimed=<danh sách sắp xếp>`",
         """adj = {'R': ['A'], 'A': ['B'], 'B': [], 'C': ['D'], 'D': ['C'], 'E': []}
alive = {'R'}; q = ['R']
while q:
    u = q.pop(0)
    for v in adj[u]:
        if v not in alive:
            alive.add(v); q.append(v)
reclaimed = sorted(set(adj) - alive)
print(f"alive={sorted(alive)} reclaimed={reclaimed}")"""),

        ("L09", "Tránh bẫy giá trị mặc định biến đổi được: bad(10)/bad(20) vs good(10)/good(20)",
         "So sánh hàm sai dùng danh sách mặc định chung `lst=[]` với hàm đúng dùng `lst=None` rồi tạo mới bên trong khi gọi lần lượt với `10` rồi `20`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`bad=<danh sách> good=<danh sách>`",
         """def bad(x, lst=[]): lst.append(x); return lst
def good(x, lst=None): lst = [] if lst is None else lst; lst.append(x); return lst
bad(10); r_bad = bad(20)
good(10); r_good = good(20)
print(f"bad={r_bad} good={r_good}")"""),

        ("L10", "Máy ảo ngăn xếp giữ đúng thứ tự toán hạng trừ trên biểu thức hậu tố",
         "Thực thi dãy lệnh máy ảo ngăn xếp `['PUSH 12', 'PUSH 3', 'PUSH 2', 'MUL', 'SUB']`, lấy `b = pop()` (số trừ) trước `a = pop()` (số bị trừ) để tính đúng `a - b`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`vm_result=<số nguyên>`",
         """st = []
for ins in ['PUSH 12', 'PUSH 3', 'PUSH 2', 'MUL', 'SUB']:
    if ins.startswith('PUSH'): st.append(int(ins.split()[1]))
    elif ins == 'MUL': b, a = st.pop(), st.pop(); st.append(a * b)
    elif ins == 'SUB': b, a = st.pop(), st.pop(); st.append(a - b)
print(f"vm_result={st[0]}")"""),

        ("L11", "Tối ưu gấp hằng số trên cả 4 phép +, -, *, // cho cây biểu thức",
         "Cài hàm đệ quy `fold(node)` hỗ trợ cả 4 phép `'+'`, `'-'`, `'*'`, `'//'` trên cây biểu thức có lá số nguyên hoặc tên biến chuỗi, rồi rút gọn `('+', ('*', 3, 6), 'y')`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`folded=<biểu thức rút gọn>`",
         """def fold(node):
    if not isinstance(node, tuple): return node
    op, a, b = node[0], fold(node[1]), fold(node[2])
    if isinstance(a, int) and isinstance(b, int):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '//' and b != 0: return a // b
    return (op, a, b)
print(f"folded={fold(('+', ('*', 3, 6), 'y'))}")"""),

        ("L12", "Cập nhật dữ liệu bất biến bằng bộ cố định (tuple)",
         "Dùng kiểu bộ cố định (tuple) trong Python tạo `xs2 = xs1 + (35,)` từ `xs1 = (5, 15, 25)` và kiểm chứng `xs1` ban đầu vẫn nguyên vẹn.\n\n"
         "Định dạng đầu ra (1 dòng):\n`xs1=<bộ gốc> xs2=<bộ mới> unchanged=<0 hoặc 1>`",
         """xs1 = (5, 15, 25)
xs2 = xs1 + (35,)
print(f"xs1={xs1} xs2={xs2} unchanged={int(len(xs1) == 3)}")"""),

        ("L13", "Kiểm chứng tỉ lệ lỗi bộ nhớ Chromium (2019) và mức giảm trên Android (2019->2024)",
         "Tính lại hai số liệu công bố trong bài hành trình: (1) tỉ lệ lỗ hổng nghiêm trọng **do hỏng bộ nhớ** của Chromium (khi chỉ `5` trên `130` lỗ hổng là không do hỏng bộ nhớ); (2) mức giảm tương đối tỉ lệ lỗ hổng bộ nhớ Android từ `76%` (2019) xuống `24%` (2024).\n\n"
         "Định dạng đầu ra (1 dòng):\n`mem_bug_pct=<1 chữ số>% android_drop_pct=<1 chữ số>%`",
         """mem_bug = (130 - 5) / 130 * 100
android_drop = (76 - 24) / 76 * 100
print(f"mem_bug_pct={mem_bug:.1f}% android_drop_pct={android_drop:.1f}%")"""),
    ],

    "PAR": [
        ("L00", "Định luật Amdahl: phần song song p=0.80 trên N=8 lõi và trần giới hạn",
         "Tính hệ số tăng tốc theo Amdahl `1 / ((1 - p) + p / N)` với `p = 0.80` trên `N = 8` lõi cùng giới hạn khi `N` tiến ra vô cực (`1 / (1 - p)`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`amdahl_8=<2 chữ số>x max_limit=<1 chữ số>x`",
         """p = 0.80
s8 = 1.0 / ((1.0 - p) + p / 8.0)
s_inf = 1.0 / (1.0 - p)
print(f"amdahl_8={s8:.2f}x max_limit={s_inf:.1f}x")"""),

        ("L01", "Định luật Gustafson (mở rộng yếu): phần tuần tự đo trên 12 lõi là q=20%",
         "Tính tăng tốc mở rộng yếu `G(N) = q + (1 - q) * N` khi phần tuần tự đo trên `N = 12` lõi bằng `q = 0.20`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`gustafson_12=<2 chữ số>x`",
         """q, N = 0.20, 12
gust = q + (1.0 - q) * N
print(f"gustafson_12={gust:.2f}x")"""),

        ("L02", "Mô hình công việc - đường găng (T1=511, T_inf=9) và cận trên Brent trên 16 lõi",
         "Tính cận dưới `max(T_inf, T1 / P)` và cận trên Brent `T_inf + (T1 - T_inf) / P` cho `T1 = 511`, `T_inf = 9`, `P = 16` lõi.\n\n"
         "Định dạng đầu ra (1 dòng):\n`work=<số> span=<số> lower_bound=<2 chữ số> brent_upper=<2 chữ số>`",
         """T1, Tinf, P = 511, 9, 16
lower_b = max(Tinf, T1 / P)
brent_upper = Tinf + (T1 - Tinf) / P
print(f"work={T1} span={Tinf} lower_bound={lower_b:.2f} brent_upper={brent_upper:.2f}")"""),

        ("L03", "Điều kiện tranh chấp 2 luồng tăng 3 lần: mất cập nhật còn 3 thay vì 6",
         "Mô phỏng hai luồng cùng tăng biến đếm chung `c = 0` tổng cộng 3 lượt mỗi luồng nhưng bị đọc-cộng-ghi xen kẽ mất nửa số lần cập nhật so với phép cộng nguyên tử.\n\n"
         "Định dạng đầu ra (1 dòng):\n`racy_final=<số nguyên> expected_atomic=<số nguyên>`",
         """c = 0
for _ in range(3):
    r1 = c; r2 = c
    c = r1 + 1; c = r2 + 1
print(f"racy_final={c} expected_atomic=6")"""),

        ("L04", "So sánh lập lịch chia đôi tĩnh và việc dài trước (LPT) trên 2 lõi",
         "Trên danh sách 8 việc `jobs = [4, 9, 2, 8, 1, 7, 3, 6]` chia cho 2 lõi: tính thời gian hoàn thành tối đa (makespan) của chia khối nửa đầu–nửa sau và của thuật toán LPT (sắp giảm dần `sorted(jobs, reverse=True)` rồi gán cho lõi đang rảnh nhất).\n\n"
         "Định dạng đầu ra (1 dòng):\n`static_makespan=<số nguyên> lpt_makespan=<số nguyên>`",
         """jobs = [4, 9, 2, 8, 1, 7, 3, 6]
static_ms = max(sum(jobs[:4]), sum(jobs[4:]))
loads = [0, 0]
for j in sorted(jobs, reverse=True):
    i = 0 if loads[0] <= loads[1] else 1
    loads[i] += j
print(f"static_makespan={static_ms} lpt_makespan={max(loads)}")"""),

        ("L05", "Chia sẻ giả (False Sharing): tính số bộ đếm 8 byte/dòng 64 byte và phần đệm",
         "Tính số biến 8 byte vừa khít một dòng bộ nhớ đệm 64 byte (`cache line`), rồi tính tổng bộ nhớ khi tách đệm 4 biến đếm mỗi biến một dòng 64 byte riêng.\n\n"
         "Định dạng đầu ra (1 dòng):\n`shared_per_64B=<số> count=4 padded_total_B=<số>`",
         """per_line = 64 // 8
count = 4
padded_total = count * 64
print(f"shared_per_64B={per_line} count={count} padded_total_B={padded_total}")"""),

        ("L06", "Vector hoá thanh ghi 512-bit (16 làn số thực 32 bit) trên mảng 100 phần tử",
         "Tính số làn `512 // 32 = 16`, số lệnh vector `100 // 16` và số phần tử dư xử lý vô hướng `100 % 16` cho mảng 100 phần tử số thực 32 bit.\n\n"
         "Định dạng đầu ra (1 dòng):\n`simd_lanes=<số> vec_ops=<số> scalar_tail=<số>`",
         """n, lanes = 100, 512 // 32
print(f"simd_lanes={lanes} vec_ops={n // lanes} scalar_tail={n % lanes}")"""),

        ("L07", "Mô hình mái nhà (Roofline): đỉnh 20 nghìn tỉ phép/giây (TF/s), 2 TB/s, cường độ 2",
         "Với đỉnh tính toán `20 TF/s` và băng thông bộ nhớ chính `2 TB/s`: tính điểm gãy (tỉ lệ đỉnh chia băng thông) và hiệu năng tối đa đạt được tại cường độ số học `AI = 2.0 FLOP/byte`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`ridge_intensity=<1 chữ số> ai=<3 chữ số> max_tflops=<3 chữ số>`",
         """ridge = 20e12 / 2e12
ai = 2.0
attained_tflops = min(20.0, ai * 2.0)
print(f"ridge_intensity={ridge:.1f} ai={ai:.3f} max_tflops={attained_tflops:.3f}")"""),

        ("L08", "Nhóm 32 luồng GPU (Warp): phân kỳ thành 3 nhánh tốn 3 lượt chạy",
         "Một nhóm 32 luồng phân kỳ thành 3 nhánh (10 luồng vào nhánh A, 12 vào B, 10 vào C) nên phần cứng phải chạy tuần tự 3 lượt cho mỗi nhóm 32 luồng. Tính hiệu suất trung bình `(10 + 12 + 10) / (3 * 32) * 100`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`warp_eff_diverged=<số nguyên>%`",
         """warp = 32; branches = [10, 12, 10]
eff = sum(branches) / (len(branches) * warp) * 100
print(f"warp_eff_diverged={eff:.0f}%")"""),

        ("L09", "Nhân ma trận n=512 chia khối 16×16 cắt giảm 16 lần truy cập bộ nhớ chậm",
         "Với cỡ ma trận vuông `n = 512` và cỡ khối `b = 16`, tính số phần tử phải đọc từ bộ nhớ chậm khi nhân ngây thơ `2 * n^3` và khi chia khối `2 * n^3 // b`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`naive_reads=<số nguyên> tiled_reads=<số nguyên> reduction=<số nguyên>x`",
         """n, b = 512, 16
naive = 2 * (n ** 3)
tiled = naive // b
print(f"naive_reads={naive} tiled_reads={tiled} reduction={b}x")"""),

        ("L10", "Gộp toàn phần theo vòng trên N=4 máy với lượng dữ liệu D=2.0 GB",
         "Tính tổng dữ liệu gửi qua mạng mỗi máy theo công thức `2 * (N - 1) / N * D` với `N = 4` máy và kích thước mảng `D = 2.0 GB`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`ring_allreduce_sent_GB=<2 chữ số>`",
         """N, D = 4, 2.0
sent_gb = 2.0 * (N - 1) / N * D
print(f"ring_allreduce_sent_GB={sent_gb:.2f}")"""),

        ("L11", "Chồng truyền gradient với tính toán bước tiếp (C=120 ms, G=40 ms, chồng 25 ms)",
         "So sánh hiệu suất mở rộng của cách chạy nối tiếp `C / (C + G)` với cách chồng được `25 ms` truyền thông vào tính toán `C / (C + G - overlap)` khi `C = 120`, `G = 40`, `overlap = 25`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`seq_eff=<1 chữ số>% overlap_eff=<1 chữ số>%`",
         """C, G, ovl = 120, 40, 25
eff_seq = C / (C + G) * 100
eff_ovl = C / (C + G - ovl) * 100
print(f"seq_eff={eff_seq:.1f}% overlap_eff={eff_ovl:.1f}%")"""),

        ("L12", "Áp định luật Amdahl chẩn đoán cụm 16 thẻ giảm phần tuần tự từ 20% xuống 4%",
         "Trong một thí nghiệm cụm `N = 16` thẻ xử lý đồ hoạ: tính độ tăng tốc khi phần nạp dữ liệu tuần tự là `s = 0.20` và sau khi sửa ống nạp dữ liệu xuống còn `s = 0.04`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`amdahl_before=<2 chữ số>x amdahl_after=<2 chữ số>x`",
         """N = 16
s_bad = 1.0 / (0.20 + 0.80 / N)
s_fix = 1.0 / (0.04 + 0.96 / N)
print(f"amdahl_before={s_bad:.2f}x amdahl_after={s_fix:.2f}x")"""),

        ("L13", "Kiểm chứng hiệu suất chặng 2017: 5 120 ảnh/giây trên cụm 256 thẻ xử lý",
         "Dùng số liệu chặng 2017 của bài: một thẻ đạt `22.7 ảnh/giây`, cụm `256` thẻ đạt `5 120 ảnh/giây`. Tính tỉ lệ giữ hiệu suất mở rộng `5120 / (256 * 22.7) * 100`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`ideal_img_s=<1 chữ số> scaling_eff=<1 chữ số>%`",
         """ideal = 256 * 22.7
eff = 5120.0 / ideal * 100
print(f"ideal_img_s={ideal:.1f} scaling_eff={eff:.1f}%")"""),
    ],

    "HCI": [
        ("L00", "Kiểm chứng tách nhãn nút bấm điều khiển và đo thời gian trễ diễn tập",
         "Kiểm tra danh sách điều khiển tách biệt rõ hai nhãn nút bấm `drill_btn = 'XAC NHAN TAP TRAN'` và `real_btn = 'GUI CANH BAO THAT'`, đồng thời tính số phút trôi qua giữa hai mốc `13:18` và `13:52`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`distinct=<0 hoặc 1> diff_min=<số nguyên>`",
         """drill_btn = 'XAC NHAN TAP TRAN'; real_btn = 'GUI CANH BAO THAT'
t1 = 13 * 60 + 18; t2 = 13 * 60 + 52
print(f"distinct={int(drill_btn != real_btn)} diff_min={t2 - t1}")"""),

        ("L01", "Ánh xạ tự nhiên: đếm hoán vị ghép nối của hàng 6 nút rời so với ghép đúng vị trí",
         "Tính số hoán vị ghép có thể sinh ra khi đặt `n = 6` nút xoay thẳng hàng điều khiển 6 vùng không gian rời (`math.factorial(6)`), so với đúng `1` ánh xạ khớp vị trí 2 chiều duy nhất.\n\n"
         "Định dạng đầu ra (1 dòng):\n`linear_guesses=<số nguyên> matched_2d=<số nguyên>`",
         """import math
n = 6
guesses = math.factorial(n)
matched = int(len(set(range(n))) == n)
print(f"linear_guesses={guesses} matched_2d={matched}")"""),

        ("L02", "Định luật Fitts trên khoảng cách D=360 px giữa nút 18 px và nút 72 px",
         "Áp dụng công thức Fitts `T = a + b * log2(D / W + 1)` với `a = 0.1`, `b = 0.15`, `D = 360 px` cho hai bề rộng nút `W = 18 px` và `W = 72 px`, in chỉ số độ khó `ID = log2(D / W + 1)` và thời gian trỏ.\n\n"
         "Định dạng đầu ra (1 dòng):\n`id_18=<3 chữ số> t_18px=<3 chữ số>s id_72=<3 chữ số> t_72px=<3 chữ số>s`",
         """import math
id_fn = lambda D, W: math.log2(D / W + 1.0)
t_fn = lambda idv: 0.1 + 0.15 * idv
id1, id2 = id_fn(360, 18), id_fn(360, 72)
print(f"id_18={id1:.3f} t_18px={t_fn(id1):.3f}s id_72={id2:.3f} t_72px={t_fn(id2):.3f}s")"""),

        ("L03", "Định luật Hick–Hyman: thực đơn 24 mục phẳng vs chia 2 cấp 4 nhóm × 6 mục",
         "Với hằng số `b = 0.18 s/bit`, tính thời gian chọn theo định luật Hick–Hyman cho thực đơn phẳng `24` mục và thực đơn hai cấp `4` nhóm × `6` mục mỗi nhóm.\n\n"
         "Định dạng đầu ra (1 dòng):\n`flat_24=<3 chữ số>s two_level=<3 chữ số>s`",
         """import math
t_flat = 0.18 * math.log2(24 + 1)
t_2lvl = 0.18 * math.log2(4 + 1) + 0.18 * math.log2(6 + 1)
print(f"flat_24={t_flat:.3f}s two_level={t_2lvl:.3f}s")"""),

        ("L04", "Gom nhóm thông tin: chia chuỗi số thành cụm 2 chữ số và kiểm ngưỡng 4 khe nhớ",
         "Tách chuỗi 10 chữ số `'6149283750'` thành từng cụm 2 chữ số (`['61', '49', ...]`) và kiểm tra xem số cụm mới có nằm gọn trong ngưỡng trí nhớ làm việc `<= 4` cụm hay không.\n\n"
         "Định dạng đầu ra (1 dòng):\n`raw_units=<số nguyên> grouped_chunks=<số nguyên> fits_wm=<0 hoặc 1>`",
         """s = '6149283750'
chunks = [s[i:i+2] for i in range(0, len(s), 2)]
print(f"raw_units={len(s)} grouped_chunks={len(chunks)} fits_wm={int(len(chunks) <= 4)}")"""),

        ("L05", "Mô hình thao tác từng bước KLM: đổi tên bằng chuột so với dùng phím tắt",
         "Cộng chi phí chuẩn KLM (`K=0.20, P=1.10, H=0.40, M=1.35, BB=0.20`): dùng chuột chọn rồi bấm sửa (`H + M + P + BB + P + BB + 3*K`) so với dùng phím tắt `Ctrl+R` (`H + 2*K + M + 3*K + K`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`mouse_s=<2 chữ số> keyboard_s=<2 chữ số>`",
         """mouse_s = 0.4 + 1.35 + 1.1 + 0.2 + 1.1 + 0.2 + 3 * 0.2
key_s = 0.4 + 2 * 0.2 + 1.35 + 3 * 0.2 + 0.2
print(f"mouse_s={mouse_s:.2f} keyboard_s={key_s:.2f}")"""),

        ("L06", "Công thức phát hiện lỗi khả dụng theo số người thử độc lập N",
         "Với vấn đề có xác suất một người phát hiện được là `lam = 0.25` (tức xác suất một người bỏ sót `p_miss = 1 - lam = 0.75`): tính tỉ lệ lỗi phát hiện được `1 - (1 - lam)^N` (theo %) khi thử `N = 6` và `N = 12` người dùng độc lập.\n\n"
         "Định dạng đầu ra (1 dòng):\n`n6_pct=<1 chữ số>% n12_pct=<1 chữ số>%`",
         """cov = lambda n, lam=0.25: (1.0 - (1.0 - lam) ** n) * 100
print(f"n6_pct={cov(6):.1f}% n12_pct={cov(12):.1f}%")"""),

        ("L07", "Tính điểm chuẩn thang SUS (System Usability Scale) 10 câu hỏi",
         "Cho bộ trả lời 10 câu hỏi theo thang 1–5: `[5, 2, 5, 1, 4, 2, 5, 1, 4, 2]`. Cộng các câu lẻ theo `(x - 1)` và các câu chẵn theo `(5 - x)`, rồi nhân tổng với `2.5`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`odd=<số nguyên> even=<số nguyên> SUS=<1 chữ số>`",
         """ans = [5, 2, 5, 1, 4, 2, 5, 1, 4, 2]
odd_s = sum(x - 1 for x in ans[0::2])
even_s = sum(5 - x for x in ans[1::2])
print(f"odd={odd_s} even={even_s} SUS={(odd_s + even_s) * 2.5:.1f}")"""),

        ("L08", "Dựng hình vuông La-tinh 5×5 cân bằng thứ tự cho 5 giao diện",
         "Tạo hình vuông La-tinh xoay vòng kích thước `5 × 5` cho 5 giao diện `['A', 'B', 'C', 'D', 'E']`, kiểm tra mọi hàng và mọi cột đều chứa đủ 5 giao diện, và tính tổng số hoán vị đầy đủ `5!`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`size=<số nguyên> balanced=<0 hoặc 1> perms_total=<số nguyên>`",
         """import math
items = ['A', 'B', 'C', 'D', 'E']
n = len(items)
latin = [items[r:] + items[:r] for r in range(n)]
r_ok = all(len(set(row)) == n for row in latin)
c_ok = all(len({latin[r][c] for r in range(n)}) == n for c in range(n))
print(f"size={n} balanced={int(r_ok and c_ok)} perms_total={math.factorial(n)}")"""),

        ("L09", "Tính lợi ích vùng bấm 48 px so với 28 px ở khoảng cách D=300 px và tỉ lệ diện tích",
         "Dùng công thức Fitts (`a = 0.1, b = 0.15, D = 300 px`) cho bề rộng nút `28 px` và `48 px`, đồng thời tính tỉ số diện tích nút vuông `(48*48) / (28*28)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`area_ratio=<2 chữ số>x t_28px=<3 chữ số>s t_48px=<3 chữ số>s`",
         """import math
fitts = lambda D, W: 0.1 + 0.15 * math.log2(D / W + 1.0)
ratio = (48 * 48) / (28 * 28)
print(f"area_ratio={ratio:.2f}x t_28px={fitts(300, 28):.3f}s t_48px={fitts(300, 48):.3f}s")"""),

        ("L10", "Phòng vệ phô mai Thụy Sĩ: hai lớp độc lập (1/500 × 1/50) so với đồng bộ giả",
         "Tính xác suất lỗi lọt qua tầng 1 (`1 / 500 = 0.002`) rồi qua tầng 2 nếu lớp 2 bắt được `98%` (`lọt = 1/50`) độc lập so với khi lớp 2 chỉ bấm đồng ý theo thói quen.\n\n"
         "Định dạng đầu ra (1 dòng):\n`indep_leak=<khoa học .2e> shared_leak=<khoa học .2e>`",
         """p1 = 1.0 / 500.0
p_indep = p1 * (1.0 / 50.0)
print(f"indep_leak={p_indep:.2e} shared_leak={p1:.2e}")"""),

        ("L11", "Kiểm chứng rào chắn cảnh báo khẩn cấp và thời lượng phản hồi diễn tập",
         "Kiểm tra danh sách rào chắn an toàn của giao diện mới `['env_split', 'preview_nonempty', 'two_person', 'cancel_tpl']` và tính tổng thời lượng trễ diễn tập từ mốc `09:12` tới `09:49`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`mins_delay=<số nguyên> guards_passed=<số nguyên>`",
         """mins = (9 * 60 + 49) - (9 * 60 + 12)
guards = ['env_split', 'preview_nonempty', 'two_person', 'cancel_tpl']
print(f"mins_delay={mins} guards_passed={len(guards)}")"""),

        ("L12", "Hành trình WCAG: kiểm chứng tổng điểm kiểm, tỉ lệ tương phản và diện tích đích bấm",
         "Tính tổng số điểm kiểm của ba mức chuẩn năm 1999 (`[16, 30, 19]`), tính tỉ lệ tương phản `(L1 + 0.05) / (L2 + 0.05)` cho cặp độ sáng `(L1=0.90, L2=0.05)`, tính diện tích đích tối thiểu `24×24` (`area_24`) và tỉ lệ diện tích nút chuẩn `48×48` so với `24×24`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`wcag1=<số nguyên> contrast_ratio=<1 chữ số> area_24=<số> ratio_48_24=<2 chữ số>x`",
         """wcag1 = sum([16, 30, 19])
contrast = (0.90 + 0.05) / (0.05 + 0.05)
area_24 = 24 * 24
ratio = (48 * 48) / area_24
print(f"wcag1={wcag1} contrast_ratio={contrast:.1f} area_24={area_24} ratio_48_24={ratio:.2f}x")"""),
    ],

    "SEP": [
        ("L00", "Tác động phần mềm quy mô lớn: lỗi 0.5% trên 500 000 người dùng và thử 150 người",
         "Với một lỗi hiếm xảy ra với xác suất `p = 0.005`: tính số người bị ảnh hưởng khi phát hành cho `500 000` người dùng và xác suất thử nội bộ trên `n = 150` người mà gặp `0` ca lỗi `(1 - p)^n`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`affected=<số nguyên> prob_zero_150=<3 chữ số>`",
         """p = 0.005
affected = int(500_000 * p)
prob_zero = (1.0 - p) ** 150
print(f"affected={affected} prob_zero_150={prob_zero:.3f}")"""),

        ("L01", "Dữ liệu cá nhân: ước lượng khả năng duy nhất qua tập thuộc tính dân cư",
         "Tính tổng tổ hợp `c = 365 * 50 * 2` (ngày sinh × độ tuổi × giới tính) và ước lượng xác suất một người là duy nhất trong vùng dân cư `N = 8 000` người theo công thức `(1 - 1/c)^(N - 1)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`combos=<số nguyên> prob_unique=<3 chữ số>`",
         """combos = 365 * 50 * 2
p_unique = (1.0 - 1.0 / combos) ** (8000 - 1)
print(f"combos={combos} prob_unique={p_unique:.3f}")"""),

        ("L02", "Bất khả thi đồng thời: tính giá trị dự báo dương (PPV) khi tỉ lệ nền 40% vs 15%",
         "Với mô hình giữ `TPR = 0.90` (tỉ lệ dương thật) và `FPR = 0.15` (tỉ lệ dương giả): tính `PPV = (b * TPR) / (b * TPR + (1 - b) * FPR)` cho nhóm A (`b = 0.40`) và nhóm B (`b = 0.15`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`ppv_A=<3 chữ số> ppv_B=<3 chữ số> mismatch=<0 hoặc 1>`",
         """ppv = lambda b: (b * 0.90) / (b * 0.90 + (1.0 - b) * 0.15)
pa, pb = round(ppv(0.40), 3), round(ppv(0.15), 3)
print(f"ppv_A={pa:.3f} ppv_B={pb:.3f} mismatch={int(pa != pb)}")"""),

        ("L03", "Giải thích phản chứng: tính điểm hồ sơ và số năm cần thêm để đạt ngưỡng 22",
         "Tính điểm hiện tại của hồ sơ `(income = 30, years = 2)` theo công thức `0.4 * income + 3 * years`, kiểm tra đạt ngưỡng `22` hay chưa, và tính số năm kinh nghiệm cần tăng thêm tối thiểu để đạt `22`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`score=<1 chữ số> pass=<0 hoặc 1> need_extra_years=<1 chữ số>`",
         """score = 0.4 * 30 + 3 * 2
need_years = (22 - score) / 3.0
print(f"score={score:.1f} pass={int(score >= 22)} need_extra_years={need_years:.1f}")"""),

        ("L04", "Kiểm tra chuỗi phụ thuộc giấy phép MIT/Apache vs GPL-3.0 trên danh sách gói",
         "Duyệt danh sách phụ thuộc `[('auth', 'MIT'), ('fmt', 'Apache-2.0'), ('csv_fast', 'GPL-3.0'), ('http', 'BSD-3-Clause')]`, lọc tên các gói dùng giấy phép buộc mở mã (`GPL...`) khi phân phối phần mềm đóng.\n\n"
         "Định dạng đầu ra (1 dòng):\n`total_deps=<số nguyên> closed_app_conflict=<danh sách tên gói>`",
         """deps = [('auth', 'MIT'), ('fmt', 'Apache-2.0'), ('csv_fast', 'GPL-3.0'), ('http', 'BSD-3-Clause')]
copyleft = [n for n, lic in deps if lic.startswith('GPL')]
print(f"total_deps={len(deps)} closed_app_conflict={copyleft}")"""),

        ("L05", "Rủi ro lặp trên đội 500 máy: xác suất có ít nhất 1 sự cố và kỳ vọng thiệt hại",
         "Với rủi ro hiếm xác suất `p = 0.002/năm` có mức hại `D_A = 500 000` so với rủi ro thường `0.05` hại `D_B = 2 000`: tính kỳ vọng thiệt hại của A và B, cùng xác suất gặp ít nhất 1 sự cố trong đội `500` máy `1 - (1 - p)^500`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`exp_A=<số nguyên> exp_B=<số nguyên> fleet_prob=<4 chữ số>`",
         """exp_a = 0.002 * 500_000
exp_b = 0.05 * 2_000
p_fleet = 1.0 - (1.0 - 0.002) ** 500
print(f"exp_A={exp_a:.0f} exp_B={exp_b:.0f} fleet_prob={p_fleet:.4f}")"""),

        ("L06", "Dấu chân điện năng & CO2: 16 GPU × 0.35 kW × 500 giờ × PUE 1.15 ở lưới 0.45 kg/kWh",
         "Tính điện năng tiêu thụ `kWh` có nhân hệ số trung tâm dữ liệu `PUE = 1.15` và lượng khí thải `CO2` tính bằng kg.\n\n"
         "Định dạng đầu ra (1 dòng):\n`kwh=<1 chữ số> co2_kg=<1 chữ số>`",
         """kwh = 16 * 0.35 * 500 * 1.15
co2_kg = kwh * 0.45
print(f"kwh={kwh:.1f} co2_kg={co2_kg:.1f}")"""),

        ("L07", "Tính hạn công bố lỗ hổng theo lịch thật (năm nhuận 2024): hạn 90 ngày, sau vá +30 ngày (khi v<=90), và hạn 7 ngày",
         "Dùng `datetime.date` bắt đầu từ ngày `2024-02-01` (năm nhuận 2024 có 29/02): tính hạn chuẩn 90 ngày, ngày công bố sau khi vá sớm ở ngày `v = 45` (`v <= 90`, công bố ở `min(90, v + 30)` ngày sau ngày báo), và hạn khẩn `7` ngày nếu lỗi đang bị khai thác.\n\n"
         "Định dạng đầu ra (1 dòng):\n`d90=<YYYY-MM-DD> d_patched=<YYYY-MM-DD> exploit_7d=<YYYY-MM-DD>`",
         """import datetime as dt
d0 = dt.date(2024, 2, 1); v = 45
days_pub = min(90, v + 30) if v <= 90 else 90
print(f"d90={d0 + dt.timedelta(days=90)}",
      f"d_patched={d0 + dt.timedelta(days=days_pub)}",
      f"exploit_7d={d0 + dt.timedelta(days=7)}")"""),

        ("L08", "Luật 3 bước chọn phương án đa bên: ràng buộc không âm, tổng điểm, và ưu tiên bên yếu thế",
         "Cho điểm tác động trên thang `[-2, 2]` tới 4 bên `[công_ty, khách, nhà_hàng, tài_xế]` của ba phương án: `'P1': [2, 2, 1, -1]`, `'P2': [1, 1, 2, 0]`, `'P3': [0, 1, 1, 2]`. Áp dụng đúng luật trong bài: (1) chỉ giữ phương án có điểm nhỏ nhất `>= 0`; (2) xếp theo `(tổng điểm, điểm của bên yếu thế nhất [tài_xế])`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`filtered=<danh sách tên> fair_pick=<tên phương án>`",
         """plans = {'P1': [2, 2, 1, -1], 'P2': [1, 1, 2, 0], 'P3': [0, 1, 1, 2]}
safe = sorted(k for k, v in plans.items() if min(v) >= 0)
best = max(safe, key=lambda k: (sum(plans[k]), plans[k][-1]))
print(f"filtered={safe} fair_pick={best}")"""),

        ("L09", "Ước lượng ba điểm (O, M, B) với O=2, M=6, B=16 ngày cho chuỗi 3 việc",
         "Áp dụng công thức của bài `E = (O + 4*M + B) / 6` và `s = (B - O) / 6` cho một công việc có `(O=2, M=6, B=16)` ngày, rồi tính kỳ vọng tổng cho 3 công việc giống nhau nối tiếp.\n\n"
         "Định dạng đầu ra (1 dòng):\n`E=<2 chữ số> SD=<2 chữ số> sum_3E=<2 chữ số>`",
         """O, M, B = 2.0, 6.0, 16.0
E = (O + 4.0 * M + B) / 6.0
SD = (B - O) / 6.0
print(f"E={E:.2f} SD={SD:.2f} sum_3E={3 * E:.2f}")"""),

        ("L10", "Đếm số gói chịu ảnh hưởng bắc cầu trên cây phụ thuộc khi rút gói 'leftpad'",
         "Cho đồ thị phụ thuộc ngược `rev = {'leftpad': ['tpl', 'cli'], 'tpl': ['web'], 'web': ['app'], 'cli': ['app'], 'app': []}`. Duyệt tìm tất cả các gói phía trên phụ thuộc trực tiếp hoặc bắc cầu vào `'leftpad'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`broken_upstream=<số nguyên> pkgs=<danh sách sắp xếp>`",
         """rev = {'leftpad': ['tpl', 'cli'], 'tpl': ['web'], 'web': ['app'], 'cli': ['app'], 'app': []}
broken = set(); stack = list(rev['leftpad'])
while stack:
    p = stack.pop()
    if p not in broken:
        broken.add(p); stack.extend(rev.get(p, []))
print(f"broken_upstream={len(broken)} pkgs={sorted(broken)}")"""),

        ("L11", "Tổ hợp nhận dạng và mức phạt tối đa theo Luật Bảo vệ dữ liệu cá nhân (5% doanh thu)",
         "Tính số tổ hợp phân biệt `2 * 5 * 365 * 100` (2 giới tính, 5 mã vùng, 365 ngày sinh, 100 năm), xác suất một người không trùng ai `(1 - 1/c)^(N - 1)` trong nhóm `N = 50 000` dân, và mức phạt tối đa `5%` doanh thu (Điều 8 Luật 91/2025) cho công ty doanh thu `200 tỉ đồng`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`combos=<số nguyên> prob_unique=<3 chữ số> max_fine_B=<1 chữ số>`",
         """combos = 2 * 5 * 365 * 100
p_uniq = (1.0 - 1.0 / combos) ** (50000 - 1)
fine_b = max(3.0, 200.0 * 0.05)
print(f"combos={combos} prob_unique={p_uniq:.3f} max_fine_B={fine_b:.1f}")"""),
    ],

    "CAS": [
        ("L00", "Phòng thủ nhiều lớp: 4 lớp độc lập × 15% lọt so với lỗi cùng giả định",
         "So sánh xác suất lỗi lọt qua cả 4 lớp phòng vệ độc lập (mỗi lớp lọt `15%`) với xác suất khi cả 4 lớp phụ thuộc vào cùng một giả định sai (`15%`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`indep_pct=<2 chữ số>% shared_pct=<1 chữ số>%`",
         """p_indep = (0.15 ** 4) * 100
p_shared = 0.15 * 100
print(f"indep_pct={p_indep:.2f}% shared_pct={p_shared:.1f}%")"""),

        ("L01", "Patriot (1991): sai số nhị phân 24-bit của 0.1 giây tích lũy sau 50h và 100h",
         "Mô phỏng thanh ghi 24-bit (1 bit dấu + 23 bit phần lẻ, bước `scale = 1 << 23`) biểu diễn `1/10 = 0.1`: tính sai số chặt cụt mỗi tích tắc `0.1 - int(0.1 * scale)/scale`, rồi nhân với `50 giờ` và `100 giờ` ở tần số `10 Hz` (`0.1 giây/nhịp`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`drift_50h=<4 chữ số> drift_100h=<4 chữ số>`",
         """scale = 1 << 23
err_tick = 0.1 - int(0.1 * scale) / scale
d50 = err_tick * (50 * 3600 * 10)
d100 = err_tick * (100 * 3600 * 10)
print(f"drift_50h={d50:.4f} drift_100h={d100:.4f}")"""),

        ("L02", "Ariane 5 (1996): mô phỏng 3 cách xử lý giá trị vượt ngưỡng 16-bit có dấu",
         "Cho giá trị tốc độ đứng mô phỏng `val = 38_000` vượt trần `[-32768, 32767]` của số nguyên 16 bit có dấu: tính kết quả khi (1) quay vòng hai bù, (2) bão hoà kẹp vào biên gần nhất, (3) gắn cờ dừng báo tràn.\n\n"
         "Định dạng đầu ra (1 dòng):\n`wrap=<số nguyên> saturate=<số nguyên> overflow=<0 hoặc 1>`",
         """lo, hi = -(1 << 15), (1 << 15) - 1
val = 38000
wrap = ((val - lo) % (1 << 16)) + lo
sat = max(lo, min(hi, val))
print(f"wrap={wrap} saturate={sat} overflow={int(not lo <= val <= hi)}")"""),

        ("L03", "Mars Climate Orbiter (1999): chuyển đổi 250.0 lbf-giây sang N-giây",
         "Tính lực đẩy thực tế bằng N-giây khi phần mềm mặt đất xuất giá trị `250.0 lbf-giây` (`1 lbf = 4.44822 N`) nhưng tàu đọc hiểu thành N-giây.\n\n"
         "Định dạng đầu ra (1 dòng):\n`reported=<1 chữ số> actual=<2 chữ số> factor=<2 chữ số>`",
         """lbf_to_n = 4.44822
cmd = 250.0
actual = cmd * lbf_to_n
print(f"reported={cmd:.1f} actual={actual:.2f} factor={lbf_to_n:.2f}")"""),

        ("L04", "Đảo ngược ưu tiên (Pathfinder): so sánh thời gian chờ không kế thừa vs có kế thừa",
         "Nếu tác vụ thấp giữ khoá thêm `3 ms` và bị tác vụ vừa chen mất `40 ms`: tính tổng thời gian tác vụ cao phải chờ khi không có và khi bật cơ chế kế thừa ưu tiên.\n\n"
         "Định dạng đầu ra (1 dòng):\n`wait_no_inherit=<số>ms wait_with_inherit=<số>ms`",
         """no_inh = 3 + 40
with_inh = 3
print(f"wait_no_inherit={no_inh}ms wait_with_inherit={with_inh}ms")"""),

        ("L05", "Knight Capital (2012): tốc độ lỗ trên 460 triệu / 45 phút và xác suất sót triển khai 8 máy",
         "Dùng số liệu sự cố năm 2012 (`460 triệu đô` trong `45 phút`) tính tốc độ lỗ mỗi phút, đồng thời tính xác suất có ít nhất 1 trên `8` máy chủ bị bỏ sót nếu mỗi máy có xác suất thao tác tay sai `p = 0.05` (`1 - (1 - p)^8`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`loss_per_min_M=<1 chữ số> prob_any_miss=<4 chữ số>`",
         """rate_m = 460.0 / 45.0
prob_miss = 1.0 - (1.0 - 0.05) ** 8
print(f"loss_per_min_M={rate_m:.1f} prob_any_miss={prob_miss:.4f}")"""),

        ("L06", "Amazon S3 (2017): rào chắn ngưỡng tối thiểu khoẻ mạnh khi gỡ máy khỏi cụm",
         "Cho cụm `120` máy chủ có ngưỡng an toàn tối thiểu phải giữ lại `90` máy đang chạy: viết kiểm tra chặn yêu cầu gỡ `40` máy.\n\n"
         "Định dạng đầu ra (1 dòng):\n`max_removable=<số> req=40 blocked=<0 hoặc 1>`",
         """total, min_healthy, req = 120, 90, 40
max_rm = total - min_healthy
print(f"max_removable={max_rm} req={req} blocked={int(req > max_rm)}")"""),

        ("L07", "Cloudflare (2019): bùng nổ bậc ba O(n^3) của mẫu `.*.*=.*` khi quét mọi vị trí đầu",
         "Tính tổng số bước quay lui tích lũy khi bộ khớp không neo thử lại ở mọi vị trí bắt đầu `s = 0..n-1` trên chuỗi `n = 150` ký tự thiếu dấu `'='`: mỗi vị trí `s` xét `m*(m+1)//2` với `m = n - s`, so với `n` bước tuyến tính.\n\n"
         "Định dạng đầu ra (1 dòng):\n`n=<số nguyên> cubic_steps=<số nguyên> ratio=<số nguyên>x`",
         """n = 150
cubic = sum((n - s) * (n - s + 1) // 2 for s in range(n))
print(f"n={n} cubic_steps={cubic} ratio={cubic // n}x")"""),

        ("L08", "GitLab (2017): tính thời gian chép khôi phục 240 GB ở 80 Mbps & khoá an toàn hostname",
         "Kiểm tra cổng an toàn ngăn lệnh xoá chạy trên máy `'db-primary'` khi mục tiêu cho phép chỉ là `'db-secondary'`, đồng thời tính số giờ truyền khôi phục bản chụp `240 GB` qua mạng `80 Mbps` (`1 GB = 8 000 Mb`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`aborted=<0 hoặc 1> restore_hours=<2 chữ số>`",
         """host, target = 'db-primary', 'db-secondary'
hours = (240 * 8000) / 80 / 3600
print(f"aborted={int(host != target)} restore_hours={hours:.2f}")"""),

        ("L09", "Heartbleed (2014): kiểm đúng chuẩn RFC 6520 là 1 + 2 + payload_len + 16 <= record_len",
         "Cài hàm kiểm tra bản ghi nhịp tim RFC 6520: hợp lệ khi `payload_len >= 0` và `1 + 2 + payload_len + 16 <= record_len` (1 byte loại + 2 byte độ dài + dữ liệu + 16 byte đệm tối thiểu). Kiểm tra hai gói: gói chuẩn `(payload=4, record_len=23)` và gói Heartbleed `(payload=65535, record_len=20)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`valid_ok=<0 hoặc 1> hb_ok=<0 hoặc 1> hb_overread_B=<số nguyên>`",
         """def rfc6520_ok(claimed_n, rec_len):
    return claimed_n >= 0 and (1 + 2 + claimed_n + 16) <= rec_len
overread = 65535 - (20 - 3)
print(f"valid_ok={int(rfc6520_ok(4, 23))} hb_ok={int(rfc6520_ok(65535, 20))} hb_overread_B={overread}")"""),

        ("L10", "Google Flu Trends (2013): tính phần trăm sai số tương đối và tỉ số dự báo vượt đỉnh",
         "Với dữ liệu đối chiếu trực tiếp `cdc = 5.5%` và mô hình ngoại suy dự báo `gft = 12.0%`: tính tỉ số `gft / cdc` và phần trăm sai số tương đối `(gft - cdc) / cdc * 100`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`ratio=<2 chữ số>x rel_err_pct=<1 chữ số>%`",
         """cdc, gft = 5.5, 12.0
ratio = gft / cdc
rel_err = (gft - cdc) / cdc * 100
print(f"ratio={ratio:.2f}x rel_err_pct={rel_err:.1f}%")"""),

        ("L11", "Sự cố Năm 2038: so sánh hạn 32-bit có dấu (2038), không dấu (2106) & hợp đồng 2040",
         "Dùng `datetime(1970, 1, 1, tzinfo=timezone.utc)` tính ngày tràn của mốc `2^31 - 1` (có dấu 32-bit) và `2^32 - 1` (không dấu 32-bit), đồng thời kiểm xem ngày đáo hạn trái phiếu `2040-06-01` có vượt ngưỡng 2038 hay không.\n\n"
         "Định dạng đầu ra (1 dòng):\n`i32_date=<YYYY-MM-DD> u32_date=<YYYY-MM-DD> bond_2040_fails=<0 hoặc 1>`",
         """import datetime as dt
t0 = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
t_i32 = (t0 + dt.timedelta(seconds=(1 << 31) - 1)).date()
t_u32 = (t0 + dt.timedelta(seconds=(1 << 32) - 1)).date()
bond = dt.date(2040, 6, 1)
print(f"i32_date={t_i32} u32_date={t_u32} bond_2040_fails={int(bond > t_i32)}")"""),
    ],
}

want = {a.upper() for a in sys.argv[1:]}
for course, labs in DATA.items():
    if want and course not in want:
        continue
    for lid, hint, de_body, sol in labs:
        de_md = f"# Lab {course} {lid} — {hint}\n\n{de_body}\n\nChấm tự động:\n```bash\nbash labs/cham.sh {course} {lid} duong_dan/bai_cua_ban.py\n```\n"
        common.upgrade_lesson(
            course, lid, hint, de_md, sol,
            add_code_if_missing=True,
            covers=COVERS[f"{course}:{lid}"],
            force_code=True,
        )
    led_p, nblk = up.sync_course_ledger(course, default_lang="python")
    for lid, _, _, sol in labs:
        out_p = ROOT / "labs" / course / lid / "mong_doi.txt"
        common.sync_practice_run_blocks(course, lid, sol, out_p.read_text(encoding="utf-8"))
    print(f"=== {course}: {len(labs)} bài OK, ledger={nblk} blocks ===", flush=True)

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for c in DATA:
    if want and c not in want:
        continue
    for cmd in (
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
    ):
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"failed: {cmd}"
print("ALL S10 PASSED!", flush=True)
