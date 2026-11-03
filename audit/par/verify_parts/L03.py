# PAR L03 — tính lại bằng cách KHÁC checks của bài: liệt kê xen kẽ bằng chọn vị trí (itertools.combinations, không dùng hàm đệ quy
# của checklib), đếm tổ hợp bằng math.comb, mô phỏng bộ đếm đổi sang phép nguyên tử, số thực đối chiếu bằng phân số chính xác
# (Fraction của chính số máy) và bằng math.fsum, số bước rút gọn bằng mô phỏng từng bước của các luồng.
import itertools
import math
from collections import Counter
from fractions import Fraction as F


def run_positions(times, atomic=False):
    steps = 1 if atomic else 3
    per = steps * times
    out = Counter()
    for pos in itertools.combinations(range(2 * per), per):
        seq, ia, ib = [], 0, 0
        for i in range(2 * per):
            if i in pos:
                seq.append(("A", ia)); ia += 1
            else:
                seq.append(("B", ib)); ib += 1
        x, reg = 0, {}
        for t, j in seq:
            if atomic:
                x += 1
            elif j % 3 == 0:
                reg[t] = x
            elif j % 3 == 1:
                reg[t] += 1
            else:
                x = reg[t]
        out[x] += 1
    return dict(out)


c1, c2, a2 = run_positions(1), run_positions(2), run_positions(2, atomic=True)
rec("L03a", c1 == {1: 18, 2: 2} == alg.par_race_counts(1) and math.comb(6, 3) == 20,
    "một lần mỗi luồng: 20 cách, 18 ra 1, 2 ra 2 (chọn vị trí; khớp checklib và khoá Hệ điều hành)")
rec("L03b", c2 == {2: 702, 3: 216, 4: 6} == alg.par_race_counts(2) and math.comb(12, 6) == 924 and 924 - 6 == 918,
    "hai lần mỗi luồng: 924 cách = C(12, 6); 702 / 216 / 6; 918 cách sai")
rec("L03c", a2 == {4: 6} == alg.par_atomic_counts(2) and math.comb(4, 2) == 6,
    "nguyên tử: 6 thứ tự = C(4, 2), tất cả ra 4")


def sim_steps(threads, k, mode):
    """Mô phỏng theo đồng hồ: mỗi bước, biến chung nhận tối đa 1 phép nguyên tử; mỗi luồng làm 1 phép riêng."""
    if mode == "atomic":
        left, t = [k] * threads, 0
        while any(left):
            i = next(j for j in range(threads) if left[j]); left[i] -= 1; t += 1
        return t
    t, part = k, threads  # k bước song song trên biến riêng
    while part > 1:
        part, t = math.ceil(part / 2), t + 1
    return t


rec("L03d", [sim_steps(4, 3, m) for m in ("atomic", "reduce")] == [12, 5]
    and [sim_steps(8, 1000, m) for m in ("atomic", "reduce")] == [8000, 1003]
    and [sim_steps(16, 10000, m) for m in ("atomic", "reduce")] == [160000, 10004]
    and alg.par_shared_steps(16, 10000, "reduce") == 10004 and round(8000 / 1003, 2) == 7.98 and round(160000 / 10004, 1) == 16.0,
    "số bước: 12/5; 8000/1003 (≈ 7,98 lần); 160 000/10 004 (≈ 16 lần)")
x = 0.1
seq8 = x
for _ in range(7):
    seq8 = seq8 + x
pairs = [x] * 8
while len(pairs) > 1:
    pairs = [pairs[i] + pairs[i + 1] for i in range(0, len(pairs), 2)]
exact = 8 * F(x)
rec("L03e", repr(seq8) == "0.7999999999999999" and repr(pairs[0]) == "0.8" and F(pairs[0]) == exact
    and F(seq8) - exact == -F(1, 2 ** 53) and math.fsum([x] * 8) == 0.8,
    "8 × 0,1: cộng dồn 0,7999999999999999, cây 0,8 = tổng chính xác của 8 số máy (lệch 2⁻⁵³), fsum xác nhận")
rec("L03f", repr((0.1 + 0.2) + 0.3) == "0.6000000000000001" and repr(0.1 + (0.2 + 0.3)) == "0.6"
    and repr(0.1 + 0.2) == "0.30000000000000004" and abs(F((0.1 + 0.2) + 0.3) - F(0.1 + (0.2 + 0.3))) < F(1, 10 ** 15),
    "không kết hợp: 0,6000000000000001 so với 0,6; lệch < 10⁻¹⁵; 0,1 + 0,2 = 0,30000000000000004")
rec("L03g", sum([10] * 8) == 80 and len({sum(p) for p in itertools.permutations([10, 10, 20, 40])}) == 1,
    "số nguyên xu: mọi thứ tự cộng cùng một tổng (80 xu)")
