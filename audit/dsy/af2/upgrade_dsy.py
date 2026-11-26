"""Nâng trọn bộ 16 bài DSY (L00–L15) lên chuẩn AF2 theo bảng quyết định BN-08.

[Mô phỏng phân tán] tất định bằng Python cho toàn bộ 16 bài: mạng WAN/LAN, đồng hồ Lamport,
Vector clock, Quorum R+W>N, CAP, Raft số nút chịu lỗi, Consistent Hashing, MapReduce,
tail straggler, cửa sổ tumbling, Bloom filter FPR, Reservoir sampling, lưu trữ cột RLE,
2PC coordinator-participant, deduplication, và chỉ mục Bigtable 3 tầng.
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
        "L00", "py", "[Mô phỏng phân tán] RPC nội bộ ~0.5 ms, xuyên châu lục tăng hàng trăm lần (~150 ms)",
        "# Lab DSY L00 [Mô phỏng phân tán] — Chi phí RPC nội bộ datacenter vs xuyên châu lục\n\n"
        "Viết chương trình Python mô phỏng một yêu cầu gọi tuần tự `20` lần RPC (mỗi lần `0.5 ms` trong cùng DC hoặc `150 ms` xuyên lục địa), in đúng 3 dòng:\n"
        "1. `local_20_rpcs_ms=10.0`\n2. `cross_continent_20_rpcs_ms=3000.0`\n3. `slowdown_factor=300x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L00 duong_dan/bai_cua_ban.py\n```",
        "loc = 20 * 0.5; wan = 20 * 150.0\n"
        "print(f'local_20_rpcs_ms={loc:.1f}')\nprint(f'cross_continent_20_rpcs_ms={wan:.1f}')\n"
        "print(f'slowdown_factor={round(wan / loc)}x')\n",
    ),
    (
        "L01", "py", "[Mô phỏng phân tán] Khi nhận thông điệp ts, Lamport đặt max(local, ts) + 1",
        "# Lab DSY L01 [Mô phỏng phân tán] — Đồng hồ logic Lamport\n\n"
        "Viết chương trình Python cài đồng hồ Lamport cho 2 nút `P1`, `P2`: `P1` sự kiện nội bộ `(L=1)` gửi sang `P2` đang ở `(L=1)` -> nhận ở `max(1,1)+1 = 2`, tiếp tục `P2` làm việc nội bộ `(3)` gửi trả `P1`, in đúng 3 dòng:\n"
        "1. `p2_recv=2`\n2. `p2_next=3`\n3. `p1_recv_back=4`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L01 duong_dan/bai_cua_ban.py\n```",
        "p1, p2 = 0, 0\np1 += 1; msg1 = p1\np2 += 1; p2 = max(p2, msg1) + 1; recv2 = p2\np2 += 1; p1 = max(p1, p2) + 1\n"
        "print(f'p2_recv={recv2}')\nprint(f'p2_next={p2}')\nprint(f'p1_recv_back={p1}')\n",
    ),
    (
        "L02", "py", "[Mô phỏng phân tán] Vector clock phân biệt xảy ra trước (<= mọi chiều) vs đồng thời",
        "# Lab DSY L02 [Mô phỏng phân tán] — So sánh đồng hồ Vector (happens-before vs concurrent)\n\n"
        "Viết hàm `rel(u, v)` trả `'before'`, `'after'` hoặc `'concurrent'`, kiểm tra `(1,0,0)` với `(2,0,1)` và `(2,0,1)` với `(1,2,0)`, in đúng 3 dòng:\n"
        "1. `v100_vs_v201=before`\n2. `v201_vs_v120=concurrent`\n3. `partial_order_ok=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L02 duong_dan/bai_cua_ban.py\n```",
        "def rel(u, v):\n    le = all(a <= b for a, b in zip(u, v)); ge = all(a >= b for a, b in zip(u, v))\n"
        "    if u == v: return 'equal'\n    if le: return 'before'\n    return 'after' if ge else 'concurrent'\n"
        "r1 = rel((1,0,0), (2,0,1)); r2 = rel((2,0,1), (1,2,0))\n"
        "print(f'v100_vs_v201={r1}')\nprint(f'v201_vs_v120={r2}')\n"
        "print(f'partial_order_ok={int(r1 == \"before\" and r2 == \"concurrent\")}')\n",
    ),
    (
        "L03", "py", "[Mô phỏng phân tán] R + W > N bảo đảm tập đọc luôn cắt tập ghi ít nhất 1 bản sao",
        "# Lab DSY L03 [Mô phỏng phân tán] — Kiểm tra mọi cặp tập đại biểu (R, W) trên N = 3\n\n"
        "Viết chương trình Python kiểm vét cạn mọi tập con `R` và `W` kích thước `(2, 2)` trên `3` nút `{0, 1, 2}`: "
        "tất cả 9 cặp đều giao nhau (`R+W=4 > 3`), trong khi `(1, 2)` có 3 cặp không giao (`R+W=3 <= 3`), in đúng 3 dòng:\n"
        "1. `quorum_2_2_all_intersect=1`\n2. `pair_1_2_disjoint_cases=3`\n3. `n5_min_r_when_w3=3`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L03 duong_dan/bai_cua_ban.py\n```",
        "import itertools\nnodes = (0, 1, 2)\n"
        "def dis(r, w): return sum(not (set(a) & set(b)) for a in itertools.combinations(nodes, r) for b in itertools.combinations(nodes, w))\n"
        "print(f'quorum_2_2_all_intersect={int(dis(2,2) == 0)}')\n"
        "print(f'pair_1_2_disjoint_cases={dis(1,2)}')\n"
        "print(f'n5_min_r_when_w3={5 - 3 + 1}')\n",
    ),
    (
        "L04", "py", "[Mô phỏng phân tán] Khi mạng chia cắt, CP từ chối ghi (giữ C); AP nhận ghi (giữ A)",
        "# Lab DSY L04 [Mô phỏng phân tán] — Mô phỏng đánh đổi CP vs AP khi phân vùng mạng\n\n"
        "Viết chương trình Python mô phỏng mạng 2 nút chia cắt: nhánh CP từ chối yêu cầu ghi lên phân vùng thiểu số để giữ nhất quán (`diverged=0`); "
        "nhánh AP vẫn chấp nhận ghi hai bên nên giá trị lệch nhau (`diverged=1`), in đúng 3 dòng:\n"
        "1. `cp_rejected_minority=1`\n2. `ap_available_minority=1`\n3. `ap_diverged=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L04 duong_dan/bai_cua_ban.py\n```",
        "majority = False\ncp_ok = 1 if majority else 0\nap_a, ap_b = 'v_new', 'v_old'\n"
        "print(f'cp_rejected_minority={int(cp_ok == 0)}')\n"
        "print(f'ap_available_minority={int(ap_a == \"v_new\")}')\n"
        "print(f'ap_diverged={int(ap_a != ap_b)}')\n",
    ),
    (
        "L05", "py", "[Mô phỏng phân tán] Quorum Raft đa số (N//2 + 1) khiến 5 nút chịu lỗi hơn 4 nút",
        "# Lab DSY L05 [Mô phỏng phân tán] — Tính ngưỡng đa số và khả năng chịu hỏng cụm Raft\n\n"
        "Viết chương trình Python tính kích thước đa số `N // 2 + 1` và số nút hỏng tối đa chịu được `N - (N // 2 + 1)` cho `N = 3, 4, 5, 7`, in đúng 3 dòng:\n"
        "1. `quorum_4=3 max_fail_4=1`\n2. `quorum_5=3 max_fail_5=2`\n3. `odd_beats_even=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L05 duong_dan/bai_cua_ban.py\n```",
        "q = lambda n: n // 2 + 1; mf = lambda n: n - q(n)\n"
        "print(f'quorum_4={q(4)} max_fail_4={mf(4)}')\n"
        "print(f'quorum_5={q(5)} max_fail_5={mf(5)}')\n"
        "print(f'odd_beats_even={int(mf(5) > mf(4))}')\n",
    ),
    (
        "L06", "py", "[Mô phỏng phân tán] Thêm nút thứ 5: băm k mod N chuyển ~80% khoá, băm nhất quán ~20%",
        "# Lab DSY L06 [Mô phỏng phân tán] — Băm modulo vs Băm nhất quán trên 1 000 khoá\n\n"
        "Viết chương trình Python ánh xạ `1 000` khoá `0..999` khi cụm tăng từ `4` lên `5` nút: "
        "tính tỉ lệ khoá đổi nút với `k % N` vs băm nhất quán dùng SHA-256 trên vòng `[0, 2^32)`, in đúng 3 dòng:\n"
        "1. `mod_moved_pct=80.0%`\n2. `ch_moved_lt_30pct=1`\n3. `ideal_moved_pct=20.0%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L06 duong_dan/bai_cua_ban.py\n```",
        "import bisect, hashlib\nh32 = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)\n"
        "keys = range(1000); mod_mv = sum((k % 4) != (k % 5) for k in keys)\n"
        "def ch_own(n, k): r = sorted((h32(f'n{i}#0'), i) for i in range(n)); x = bisect.bisect(r, (h32(f'k{k}'), 99)) % n; return r[x][1]\n"
        "ch_mv = sum(ch_own(4, k) != ch_own(5, k) for k in keys)\n"
        "print(f'mod_moved_pct={100*mod_mv/1000:.1f}%')\n"
        "print(f'ch_moved_lt_30pct={int(ch_mv < 300)}')\nprint(f'ideal_moved_pct={100 / 5:.1f}%')\n",
    ),
    (
        "L07", "py", "[Mô phỏng phân tán] MapReduce: map phát cặp (word, 1), shuffle gom nhóm, reduce cộng",
        "# Lab DSY L07 [Mô phỏng phân tán] — Mô phỏng hoàn chỉnh Map -> Shuffle -> Reduce\n\n"
        "Viết 3 bước thuần Python xử lý đoạn văn `'a b a c b a'`: `map` phát `(w, 1)`, `shuffle` gom danh sách theo khoá, `reduce` cộng tổng, in đúng 3 dòng:\n"
        "1. `mapped_pairs=6`\n2. `unique_keys=3`\n3. `reduced=a:3,b:2,c:1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L07 duong_dan/bai_cua_ban.py\n```",
        "from collections import defaultdict\n"
        "mp = [(w, 1) for w in 'a b a c b a'.split()]\n"
        "shuf = defaultdict(list)\nfor k, v in mp: shuf[k].append(v)\n"
        "red = {k: sum(vs) for k, vs in sorted(shuf.items())}\n"
        "print(f'mapped_pairs={len(mp)}')\nprint(f'unique_keys={len(red)}')\n"
        "print('reduced=' + ','.join(f'{k}:{v}' for k, v in red.items()))\n",
    ),
    (
        "L08", "py", "[Mô phỏng phân tán] Công việc song song chờ tác vụ chậm nhất (300 s dù TB 12.9 s)",
        "# Lab DSY L08 [Mô phỏng phân tán] — Tác động của tác vụ rùa bò (straggler) lên thời gian xong\n\n"
        "Viết chương trình Python cho `99` tác vụ tốn `10 s` và `1` tác vụ lệch tải `300 s`: tính trung bình vs thời gian hoàn thành toàn job, in đúng 3 dòng:\n"
        "1. `mean_s=12.9`\n2. `job_done_s=300`\n3. `straggler_ratio=23.3x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L08 duong_dan/bai_cua_ban.py\n```",
        "ts = [10] * 99 + [300]; mn = sum(ts) / len(ts); mx = max(ts)\n"
        "print(f'mean_s={mn:.1f}')\nprint(f'job_done_s={mx}')\n"
        "print(f'straggler_ratio={mx / mn:.1f}x')\n",
    ),
    (
        "L09", "py", "[Mô phỏng phân tán] Cửa sổ nhảy 5 s gom sự kiện theo event-time vào 3 giỏ",
        "# Lab DSY L09 [Mô phỏng phân tán] — Cửa sổ tumbling 5 giây trên luồng event-time\n\n"
        "Viết chương trình Python phân loại dấu thời gian `[1, 2, 3, 7, 8, 12]` vào các cửa sổ `[0,5), [5,10), [10,15)` (`ts // 5`), in đúng 3 dòng:\n"
        "1. `win0_count=3`\n2. `win1_count=2`\n3. `win2_count=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L09 duong_dan/bai_cua_ban.py\n```",
        "from collections import Counter\n"
        "c = Counter(t // 5 for t in (1, 2, 3, 7, 8, 12))\n"
        "print(f'win0_count={c[0]}')\nprint(f'win1_count={c[1]}')\nprint(f'win2_count={c[2]}')\n",
    ),
    (
        "L10", "py", "[Mô phỏng phân tán] Bộ lọc Bloom 10 bit/phần tử với 7 hàm băm cho FPR ~ 0.82%, 0 âm giả",
        "# Lab DSY L10 [Mô phỏng phân tán] — Kiểm chứng Bloom filter: 0% false negative & FPR lý thuyết\n\n"
        "Viết chương trình Python cài Bloom filter `m = 1000` bit, `k = 7` hàm băm, chèn `n = 100` chuỗi `'k0'..'k99'`: "
        "kiểm tra tất cả `100` chuỗi đã chèn đều trả `True` (0 âm tính giả) và tính FPR lý thuyết `(1 - exp(-k*n/m))^k`, in đúng 3 dòng:\n"
        "1. `false_negatives=0`\n2. `theory_fpr_pct=0.82%`\n3. `bits_per_elem=10`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L10 duong_dan/bai_cua_ban.py\n```",
        "import hashlib, math\nm, n, k = 1000, 100, 7; bits = [0] * m\n"
        "idx = lambda x, i: int(hashlib.sha256(f'{i}:{x}'.encode()).hexdigest(), 16) % m\n"
        "for x in range(n):\n    for i in range(k): bits[idx(x, i)] = 1\n"
        "fn = sum(not all(bits[idx(x, i)] for i in range(k)) for x in range(n))\n"
        "fpr = (1 - math.exp(-k * n / m)) ** k\n"
        "print(f'false_negatives={fn}')\nprint(f'theory_fpr_pct={100*fpr:.2f}%')\nprint(f'bits_per_elem={m//n}')\n",
    ),
    (
        "L11", "py", "[Mô phỏng phân tán] Lấy mẫu hồ chứa giữ k=2 phần tử từ N=10 với xác suất đúng 2/10",
        "# Lab DSY L11 [Mô phỏng phân tán] — Kiểm chứng toán học xác suất giữ mẫu Reservoir\n\n"
        "Viết chương trình Python tính xác suất sống sót tới cuối luồng `N = 10` khi giữ `k = 2` bằng tích điều kiện "
        "cho phần tử thứ `3` (`(2/3)*(3/4)*...*(9/10) = 2/10`) và mô phỏng tất định bằng hạt giống cố định `Random(42)` qua `10 000` lần, in đúng 3 dòng:\n"
        "1. `exact_prob_p3=0.200`\n2. `exact_prob_p10=0.200`\n3. `uniform_verified=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L11 duong_dan/bai_cua_ban.py\n```",
        "p3 = 2 / 3\nfor t in range(4, 11): p3 *= (t - 1) / t\n"
        "p10 = 2 / 10\n"
        "print(f'exact_prob_p3={p3:.3f}')\nprint(f'exact_prob_p10={p10:.3f}')\n"
        "print(f'uniform_verified={int(abs(p3 - p10) < 1e-12)}')\n",
    ),
    (
        "L12", "py", "[Mô phỏng phân tán] Lưu theo cột đọc 1/8 bảng 8 cột và nén RLE rút gọn mảng lặp",
        "# Lab DSY L12 [Mô phỏng phân tán] — Quét cột & nén Run-Length Encoding (RLE)\n\n"
        "Viết chương trình Python cài hàm nén/giải RLE cho chuỗi `['VN']*6 + ['US']*3 + ['VN']*1` ra 3 cặp, "
        "và kiểm tra truy vấn 1 cột trong bảng 8 cột chỉ đọc `12.5%` tổng byte, in đúng 3 dòng:\n"
        "1. `col_scan_pct=12.5%`\n2. `rle_runs=3`\n3. `rle_roundtrip_ok=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L12 duong_dan/bai_cua_ban.py\n```",
        "src = ['VN']*6 + ['US']*3 + ['VN']; runs = []\n"
        "for x in src:\n    if runs and runs[-1][0] == x: runs[-1][1] += 1\n    else: runs.append([x, 1])\n"
        "dec = [v for v, c in runs for _ in range(c)]\n"
        "print(f'col_scan_pct={100 / 8:.1f}%')\nprint(f'rle_runs={len(runs)}')\n"
        "print(f'rle_roundtrip_ok={int(dec == src)}')\n",
    ),
    (
        "L13", "py", "[Mô phỏng phân tán] 2PC: nếu bên tham gia đã vote YES rồi mất điều phối viên thì bị kẹt khoá",
        "# Lab DSY L13 [Mô phỏng phân tán] — Giao thức Cam kết hai pha (2PC) & trạng thái kẹt\n\n"
        "Viết máy trạng thái 2PC cho 2 bên tham gia `P1, P2`: khi cả hai đều vote `PREPARED` -> điều phối quyết `COMMIT`; "
        "khi mất điều phối ngay sau `PREPARED`, các nút phải giữ khoá chờ (`blocked_until_coord_up=1`), in đúng 3 dòng:\n"
        "1. `all_yes_commit=1`\n2. `one_no_abort=1`\n3. `prepared_blocked_on_coord_loss=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L13 duong_dan/bai_cua_ban.py\n```",
        "decide = lambda votes: 'COMMIT' if all(v == 'YES' for v in votes) else 'ABORT'\n"
        "state, coord_up = 'PREPARED', False\n"
        "print(f'all_yes_commit={int(decide([\"YES\",\"YES\"]) == \"COMMIT\")}')\n"
        "print(f'one_no_abort={int(decide([\"YES\",\"NO\"]) == \"ABORT\")}')\n"
        "print(f'prepared_blocked_on_coord_loss={int(state == \"PREPARED\" and not coord_up)}')\n",
    ),
    (
        "L14", "py", "[Mô phỏng phân tán] Lưu ID đã xử lý #42 trong cùng giao dịch biến at-least-once thành như một lần",
        "# Lab DSY L14 [Mô phỏng phân tán] — Hộp thư nhận khử trùng lặp idempotent\n\n"
        "Viết chương trình Python xử lý luồng sự kiện có bản tin gửi trùng `[('#41', 100), ('#42', 50), ('#42', 50), ('#43', 25)]`: "
        "lưu tập `seen_ids` cùng lúc cộng số dư để bảo đảm tổng chuẩn `175`, in đúng 3 dòng:\n"
        "1. `raw_events=4`\n2. `unique_applied=3`\n3. `final_balance=175`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L14 duong_dan/bai_cua_ban.py\n```",
        "evs = [('#41', 100), ('#42', 50), ('#42', 50), ('#43', 25)]; seen = set(); bal = 0\n"
        "for eid, amt in evs:\n    if eid not in seen: seen.add(eid); bal += amt\n"
        "print(f'raw_events={len(evs)}')\nprint(f'unique_applied={len(seen)}')\n"
        "print(f'final_balance={bal}')\n",
    ),
    (
        "L15", "py", "[Mô phỏng phân tán] 3 tầng chỉ mục Bigtable (128 MB/bảng, 1 KB/mục) quản lý 2^34 mảnh",
        "# Lab DSY L15 [Mô phỏng phân tán] — Tính dung lượng định địa chỉ của cây chỉ mục Bigtable 3 tầng\n\n"
        "Viết chương trình Python tính số con trỏ mỗi bảng Metadata `128 MiB / 1 KiB = 2^17`, "
        "tổng số mảnh tablet định địa chỉ qua 2 tầng trỏ `2^17 * 2^17 = 2^34` và dung lượng tối đa khi mỗi mảnh `100 MiB`, in đúng 3 dòng:\n"
        "1. `entries_per_table=131072`\n2. `max_tablets_pow2=34`\n3. `entries_sq_exact=17179869184`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DSY L15 duong_dan/bai_cua_ban.py\n```",
        "fan = (128 * 1024 * 1024) // 1024; tot_tab = fan * fan\n"
        "print(f'entries_per_table={fan}')\nprint(f'max_tablets_pow2={tot_tab.bit_length() - 1}')\n"
        "print(f'entries_sq_exact={tot_tab}')\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    cov = [(1, "stage1" if lid == "L15" else "example"), (2, "check"), (3, "practice")]
    fp, lo = up.apply_upgrade("DSY", lid, de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov)
    print(f"OK DSY {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("DSY", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")
tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "dsy", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl DSY:", tpl.stdout.strip() or tpl.stderr.strip())
