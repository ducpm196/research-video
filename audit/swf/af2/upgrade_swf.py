"""Nâng trọn bộ 14 bài SWF (L00–L13) lên chuẩn AF2 theo bảng quyết định BN-08.

Toàn bộ 14 bài đều là bài tập Python thực thi thật qua labs/cham.sh: bất biến vòng lặp,
tràn biên (lo + hi)//2, BVA tam giác, phủ nhánh, property testing, FSM, xung đột đồng thời,
hợp nhất ba chiều, truy vấn tham số hoá chống SQLi trên sqlite3.
"""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[2])); import _frozen  # noqa: E402,F401
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

LESSONS = [
    (
        "L00", "py", "Hợp đồng: tiền điều kiện đúng thì hàm bảo đảm hậu điều kiện",
        "# Lab SWF L00 — Đặc tả hợp đồng: tiền điều kiện và hậu điều kiện\n\n"
        "Viết chương trình Python cài hàm `bsearch_checked(a, x)` kiểm tra tiền điều kiện mảng `a` đã sắp tăng "
        "(nếu chưa sắp ném `ValueError`), tìm vị trí `x`, kiểm hậu điều kiện `a[i] == x` và chạy thử trên `[2, 5, 8, 12]` (tìm 8) và `[5, 2]` (bắt lỗi), in đúng 3 dòng:\n"
        "1. `found_idx=2`\n2. `missing_idx=-1`\n3. `unsorted_rejected=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L00 duong_dan/bai_cua_ban.py\n```",
        "def bs(a, x):\n    if any(a[i] > a[i+1] for i in range(len(a)-1)): raise ValueError('unsorted')\n"
        "    lo, hi = 0, len(a) - 1\n    while lo <= hi:\n        m = lo + (hi - lo) // 2\n"
        "        if a[m] == x: return m\n        if a[m] < x: lo = m + 1\n        else: hi = m - 1\n    return -1\n"
        "rej = 0\ntry: bs([5, 2], 2)\nexcept ValueError: rej = 1\n"
        "print(f'found_idx={bs([2,5,8,12], 8)}')\nprint(f'missing_idx={bs([2,5,8,12], 7)}')\nprint(f'unsorted_rejected={rej}')\n",
    ),
    (
        "L01", "py", "Bất biến vòng lặp giữ đúng trước, trong và ngay khi kết thúc vòng",
        "# Lab SWF L01 — Kiểm chứng bất biến vòng lặp s = i*(i-1)//2\n\n"
        "Viết chương trình Python mô phỏng vòng cộng `0 + 1 + ... + (n - 1)` với `n = 20`: "
        "tại mỗi vòng kiểm khẳng định bất biến `s == i * (i - 1) // 2`, in đúng 3 dòng:\n"
        "1. `invariant_holds_all=1`\n2. `final_i=20`\n3. `final_sum=190`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L01 duong_dan/bai_cua_ban.py\n```",
        "s, ok = 0, True\nfor i in range(20):\n    ok = ok and (s == i * (i - 1) // 2)\n    s += i\ni = 20\nok = ok and (s == i * (i - 1) // 2)\n"
        "print(f'invariant_holds_all={int(ok)}')\nprint(f'final_i={i}')\nprint(f'final_sum={s}')\n",
    ),
    (
        "L02", "py", "Hàm biến thiên giảm nghiêm ngặt và không âm bảo đảm vòng lặp dừng",
        "# Lab SWF L02 — Hàm biến thiên và thuật toán Euclid dừng tất yếu\n\n"
        "Viết chương trình Python cài thuật toán Euclid đếm số bước lặp cho `(a=1071, b=462)` "
        "và kiểm chứng ở mọi bước biến `b` giảm nghiêm ngặt (`b_new < b_old`) và `b_new >= 0`, in đúng 3 dòng:\n"
        "1. `gcd=21`\n2. `steps=3`\n3. `strictly_decreasing=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L02 duong_dan/bai_cua_ban.py\n```",
        "a, b, steps, dec = 1071, 462, 0, True\nwhile b > 0:\n    nxt = a % b\n"
        "    dec = dec and (0 <= nxt < b)\n    a, b = b, nxt; steps += 1\n"
        "print(f'gcd={a}')\nprint(f'steps={steps}')\nprint(f'strictly_decreasing={int(dec)}')\n",
    ),
    (
        "L03", "py", "Tránh tràn số nguyên 32 bit bằng công thức lo + (hi - lo) // 2",
        "# Lab SWF L03 — Lỗi lệch một và tràn số (lo + hi)//2 trên 32 bit\n\n"
        "Viết chương trình Python mô phỏng số nguyên có dấu 32 bit (`INT32_MAX = 2**31 - 1`): "
        "với `lo = 2_000_000_000, hi = 2_100_000_000`, tính điểm giữa bằng `(lo + hi) // 2` bị tràn có dấu so với `lo + (hi - lo) // 2`, in đúng 3 dòng:\n"
        "1. `naive_sum_overflows=1`\n2. `safe_mid=2050000000`\n3. `in_bounds=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L03 duong_dan/bai_cua_ban.py\n```",
        "lo, hi, mx = 2_000_000_000, 2_100_000_000, (1 << 31) - 1\n"
        "mid = lo + (hi - lo) // 2\n"
        "print(f'naive_sum_overflows={int(lo + hi > mx)}')\n"
        "print(f'safe_mid={mid}')\nprint(f'in_bounds={int(lo <= mid <= hi)}')\n",
    ),
    (
        "L04", "py", "Phân hoạch tương đương và biên tam giác (phép == là so sánh bằng, a + b == c không phải tam giác)",
        "# Lab SWF L04 — Kiểm thử phân hoạch tương đương và giá trị biên tam giác\n\n"
        "Viết chương trình Python cài hàm phân loại tam giác `classify(a, b, c)` trả về `'none'`, `'equilateral'`, `'isosceles'`, hoặc `'scalene'` "
        "và kiểm thử các ca chuẩn `[3,3,3]`, `[3,3,4]`, `[3,4,5]`, `[1,2,3]`, in đúng 3 dòng:\n"
        "1. `t333=equilateral t334=isosceles`\n2. `t345=scalene`\n3. `boundary_123=none`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L04 duong_dan/bai_cua_ban.py\n```",
        "def tri(a, b, c):\n    x, y, z = sorted((a, b, c))\n    if x <= 0 or x + y <= z: return 'none'\n"
        "    if x == z: return 'equilateral'\n    return 'isosceles' if (x == y or y == z) else 'scalene'\n"
        "print(f't333={tri(3,3,3)} t334={tri(3,3,4)}')\n"
        "print(f't345={tri(3,4,5)}')\nprint(f'boundary_123={tri(1,2,3)}')\n",
    ),
    (
        "L05", "py", "Phủ nhánh 3 câu if độc lập chỉ cần 2 ca, nhưng phủ đường cần 2^3 = 8 ca",
        "# Lab SWF L05 — Độ phủ lệnh, nhánh và đường đi trên 3 nhánh độc lập\n\n"
        "Viết chương trình Python theo dõi tập nhánh `6` cạnh (`(i, True/False)`) và tập đường đi `(b0, b1, b2)` "
        "khi chạy hàm có 3 câu `if` độc lập với `[TTT, FFF]` (2 ca) vs đầy đủ `8` tổ hợp, in đúng 3 dòng:\n"
        "1. `two_cases_branches=6/6`\n2. `two_cases_paths=2/8`\n3. `full_cases_needed=8`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L05 duong_dan/bai_cua_ban.py\n```",
        "import itertools\ndef run(cases):\n    br, pa = set(), set()\n    for a, b, c in cases:\n"
        "        for i, v in enumerate((a, b, c)): br.add((i, bool(v)))\n        pa.add((a, b, c))\n    return len(br), len(pa)\n"
        "b2, p2 = run([(1,1,1), (0,0,0)]); _, p8 = run(list(itertools.product([0,1], repeat=3)))\n"
        "print(f'two_cases_branches={b2}/6')\nprint(f'two_cases_paths={p2}/8')\nprint(f'full_cases_needed={p8}')\n",
    ),
    (
        "L06", "py", "Kiểm thử dựa trên tính chất kiểm chứng bất biến trên toàn miền mẫu",
        "# Lab SWF L06 — Kiểm thử dựa trên tính chất (idempotence & bảo toàn phần tử)\n\n"
        "Viết chương trình Python duyệt toàn bộ `3^4 = 81` dãy độ dài `4` lấy giá trị trong `{0, 1, 2}` "
        "và kiểm hai tính chất của `sorted(xs)`: `sorted(sorted(xs)) == sorted(xs)` và đếm tần suất phần tử không đổi, in đúng 3 dòng:\n"
        "1. `tested_sequences=81`\n2. `idempotent_pass=81`\n3. `multiset_preserved=81`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L06 duong_dan/bai_cua_ban.py\n```",
        "import itertools\nfrom collections import Counter\ntot = idemp = mult = 0\n"
        "for xs in itertools.product((0, 1, 2), repeat=4):\n    tot += 1; s = sorted(xs)\n"
        "    if sorted(s) == s: idemp += 1\n    if Counter(s) == Counter(xs): mult += 1\n"
        "print(f'tested_sequences={tot}')\nprint(f'idempotent_pass={idemp}')\nprint(f'multiset_preserved={mult}')\n",
    ),
    (
        "L07", "py", "Duyệt giữa cây tìm kiếm nhị phân (BST) cho dãy tăng nghiêm ngặt; bất biến đống: cha <= con",
        "# Lab SWF L07 — Kiểm chứng bất biến của cây tìm kiếm nhị phân (BST) và Min-Heap (đống nhỏ nhất)\n\n"
        "Viết chương trình Python kiểm duyệt giữa (inorder) một cây tìm kiếm nhị phân (BST) trả về `[2, 5, 7, 9, 12]` (tăng chặt) "
        "và kiểm bất biến min-heap `h[i] <= h[2i+1], h[2i+2]` trên mảng `[1, 4, 3, 7, 8]` vs mảng lỗi `[1, 5, 3, 2, 8]`, in đúng 3 dòng:\n"
        "1. `bst_inorder_sorted=1`\n2. `valid_heap=1`\n3. `broken_heap=0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L07 duong_dan/bai_cua_ban.py\n```",
        "def inord(n): return [] if not n else inord(n[1]) + [n[0]] + inord(n[2])\n"
        "bst = (7, (5, (2, None, None), None), (9, None, (12, None, None)))\n"
        "seq = inord(bst); b_ok = all(seq[i] < seq[i+1] for i in range(len(seq)-1))\n"
        "def is_heap(h): return all(h[i] <= h[c] for i in range(len(h)) for c in (2*i+1, 2*i+2) if c < len(h))\n"
        "print(f'bst_inorder_sorted={int(b_ok)}')\n"
        "print(f'valid_heap={int(is_heap([1,4,3,7,8]))}')\nprint(f'broken_heap={int(is_heap([1,5,3,2,8]))}')\n",
    ),
    (
        "L08", "py", "Máy trạng thái hữu hạn chỉ chấp nhận chuyển tiếp hợp lệ trong bảng",
        "# Lab SWF L08 — Máy trạng thái hữu hạn đèn giao thông có kiểm chứng chuyển tiếp\n\n"
        "Viết chương trình Python cài FSM đèn giao thông (`RED -> GREEN -> YELLOW -> RED`): "
        "kiểm chuỗi bước `['GREEN', 'YELLOW', 'RED']` từ `RED` và từ chối nhảy tắt `RED -> RED` hoặc `GREEN -> RED`, in đúng 3 dòng:\n"
        "1. `valid_cycle_ok=1`\n2. `skip_green_to_red_rejected=1`\n3. `final_state=RED`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L08 duong_dan/bai_cua_ban.py\n```",
        "TRANS = {'RED': {'GREEN'}, 'GREEN': {'YELLOW'}, 'YELLOW': {'RED'}}\n"
        "cur = 'RED'; ok = True\n"
        "for nxt in ('GREEN', 'YELLOW', 'RED'):\n    if nxt not in TRANS[cur]: ok = False; break\n    cur = nxt\n"
        "bad = 'RED' not in TRANS['GREEN']\n"
        "print(f'valid_cycle_ok={int(ok)}')\nprint(f'skip_green_to_red_rejected={int(bad)}')\nprint(f'final_state={cur}')\n",
    ),
    (
        "L09", "py", "Số cách xen kẽ 2 luồng x 6 bước là C(12, 6) = 924, có lối ra x=2,3,4",
        "# Lab SWF L09 — Kiểm tổ hợp xen kẽ C(12,6)=924 trong bài toán tranh chấp\n\n"
        "Viết chương trình Python tính số cách xen kẽ `C(12, 6) = 924` và chạy duyệt tổ hợp hai luồng mỗi luồng tăng `x += 1` 2 lần "
        "để đếm số đường dẫn cho ra giá trị `x < 4`, in đúng 3 dòng:\n"
        "1. `total_interleavings=924`\n2. `distinct_x=2,3,4`\n3. `buggy_paths_gt0=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L09 duong_dan/bai_cua_ban.py\n```",
        "import math\nres = {}\ndef dfs(p0, p1, r0, r1, x):\n    if p0==6 and p1==6: res[x] = res.get(x, 0) + 1; return\n"
        "    if p0 < 6: dfs(p0+1, p1, x if p0%3==0 else (r0+1 if p0%3==1 else r0), r1, r0 if p0%3==2 else x)\n"
        "    if p1 < 6: dfs(p0, p1+1, r0, x if p1%3==0 else (r1+1 if p1%3==1 else r1), r1 if p1%3==2 else x)\n"
        "dfs(0, 0, 0, 0, 0)\n"
        "print(f'total_interleavings={math.comb(12, 6)}')\n"
        "print('distinct_x=' + ','.join(map(str, sorted(res))))\n"
        "print(f'buggy_paths_gt0={int(sum(v for k,v in res.items() if k<4) > 0)}')\n",
    ),
    (
        "L10", "py", "Đo ghép cặp trên cùng 30 tập mẫu và báo khoảng tin cậy 95%",
        "# Lab SWF L10 — Đo hiệu năng thực nghiệm có khoảng tin cậy 95%\n\n"
        "Viết chương trình Python với mẫu hiệu số thời gian `d = [12.0 + (i % 5 - 2) * 0.5 for i in range(30)]` (30 cặp đo): "
        "tính trung bình hiệu, độ lệch chuẩn mẫu `s`, sai số chuẩn `s/sqrt(30)` và khoảng tin cậy 95% xấp xỉ `mean +- 2.045 * SE`, in đúng 3 dòng:\n"
        "1. `n=30 mean=12.00`\n2. `sd=0.719 se=0.131`\n3. `ci95=11.73,12.27`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L10 duong_dan/bai_cua_ban.py\n```",
        "import math\nd = [12.0 + (i % 5 - 2) * 0.5 for i in range(30)]; n = len(d)\n"
        "m = sum(d) / n; sd = math.sqrt(sum((x - m)**2 for x in d) / (n - 1)); se = sd / math.sqrt(n); hw = 2.045 * se\n"
        "print(f'n={n} mean={m:.2f}')\nprint(f'sd={sd:.3f} se={se:.3f}')\nprint(f'ci95={m-hw:.2f},{m+hw:.2f}')\n",
    ),
    (
        "L11", "py", "Hợp nhất ba chiều dựa trên tổ tiên chung phân biệt thay đổi thật vs xung đột",
        "# Lab SWF L11 — Thuật toán hợp nhất ba chiều (Base, Branch A, Branch B)\n\n"
        "Viết chương trình Python cài hàm `merge3(base, a, b)`: nếu `a == b` lấy `a`; nếu một nhánh không đổi so với `base` "
        "thì lấy nhánh kia; nếu cả hai sửa khác nhau báo `'CONFLICT'`, in đúng 3 dòng:\n"
        "1. `merge_1_2_1=2`\n2. `merge_1_3_3=3`\n3. `merge_1_2_3=CONFLICT`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L11 duong_dan/bai_cua_ban.py\n```",
        "def m3(base, a, b):\n    if a == b or b == base: return a\n    if a == base: return b\n    return 'CONFLICT'\n"
        "print(f'merge_1_2_1={m3(1,2,1)}')\nprint(f'merge_1_3_3={m3(1,3,3)}')\nprint(f'merge_1_2_3={m3(1,2,3)}')\n",
    ),
    (
        "L12", "py", "Truy vấn tham số hoá ? chặn hoàn toàn tấn công chèn câu lệnh (SQL / SQLi)",
        "# Lab SWF L12 — Đối chiếu ghép chuỗi vs truy vấn tham số hoá thật trên SQLite (ngôn ngữ SQL)\n\n"
        "Viết chương trình Python dùng `sqlite3` thật tạo bảng `users(name TEXT, role TEXT)` có 2 dòng `('an','user'),('root','admin')`, "
        "thử payload `' OR '1'='1` vào ghép chuỗi so với `?` tham số hoá, in đúng 3 dòng:\n"
        "1. `unsafe_rows_leaked=2`\n2. `param_rows_returned=0`\n3. `sqli_blocked=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L12 duong_dan/bai_cua_ban.py\n```",
        "import sqlite3\nc = sqlite3.connect(':memory:')\n"
        "c.execute('CREATE TABLE u(n TEXT, r TEXT)'); c.executemany('INSERT INTO u VALUES(?,?)', [('an','user'),('root','admin')])\n"
        "pay = \"' OR '1'='1\"; bad = c.execute(f\"SELECT * FROM u WHERE n='{pay}'\").fetchall()\n"
        "safe = c.execute('SELECT * FROM u WHERE n=?', (pay,)).fetchall()\n"
        "print(f'unsafe_rows_leaked={len(bad)}')\nprint(f'param_rows_returned={len(safe)}')\nprint(f'sqli_blocked={int(len(safe)==0)}')\n",
    ),
    (
        "L13", "py", "(Mô phỏng định lượng) Quy mô kho mã 20 lần lưu thay đổi (commit)/phút = 28 800 commit/ngày",
        "# Lab SWF L13 (Mô phỏng quy mô kho mã) — Tính tần suất lưu thay đổi (commit) ngày & mật độ đổi tệp\n\n"
        "Viết chương trình Python tính số thay đổi mỗi ngày ở tốc độ `20` thay đổi/phút, mật độ thay đổi trung bình `35 000` "
        "chỗ sửa trên `3 100` mô-đun và tải kiểm thử nếu 1 thay đổi chạm trung bình 15 mục, in đúng 3 dòng:\n"
        "1. `commits_per_day=28800`\n2. `edits_per_part=11.29`\n3. `test_triggers_day=432000`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SWF L13 duong_dan/bai_cua_ban.py\n```",
        "cpd = 20 * 60 * 24\nprint(f'commits_per_day={cpd}')\n"
        "print(f'edits_per_part={35000 / 3100:.2f}')\nprint(f'test_triggers_day={cpd * 15}')\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    cov = [(1, "stage1" if lid == "L13" else "example"), (2, "check"), (3, "practice")]
    fp, lo = up.apply_upgrade("SWF", lid, de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov)
    print(f"OK SWF {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("SWF", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")
tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "swf", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl SWF:", tpl.stdout.strip() or tpl.stderr.strip())
