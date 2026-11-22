"""Nâng trọn bộ 14 bài DVO (L00–L13) lên chuẩn AF2 theo bảng quyết định BN-08.

Bao phủ Git/CI bisect, xác suất xung đột hợp nhất, SemVer, flaky tests, SHA-256 bất biến,
IaC lũy đẳng, lộ bí mật lịch sử Git, canary p-value, expand-contract DB migration,
4 chỉ số DORA, MTTR/sẵn sàng, lưu lượng log, ký tạo tác RSA, và chuẩn hoá khoảng DORA.
"""
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
        "L00", "py", "(Mô phỏng định lượng) Tìm lỗi bằng tìm kiếm nhị phân (git bisect) giảm từ 300 xuống <= 9 bước",
        "# Lab DVO L00 (Mô phỏng vòng phản hồi) — Tìm kiếm nhị phân bằng lệnh git bisect\n\n"
        "Viết chương trình Python tính số bước tối đa (`ceil(log2(N))`) của `git bisect` (lệnh Git chia đôi lịch sử tìm lần lưu thay đổi gây lỗi) "
        "khi quy mô lô thay đổi là `3`, `300`, và kiểm tra kết quả tìm đúng vị trí commit hỏng đầu tiên `bad = 187` trong `0..299`, in đúng 3 dòng:\n"
        "1. `bisect_steps_3=2`\n2. `bisect_steps_300=9`\n3. `found_bad_commit=187`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L00 duong_dan/bai_cua_ban.py\n```",
        "import math\nlo, hi = 0, 299\nwhile lo < hi:\n    m = (lo + hi) // 2\n    if m >= 187: hi = m\n    else: lo = m + 1\n"
        "print(f'bisect_steps_3={math.ceil(math.log2(3))}')\n"
        "print(f'bisect_steps_300={math.ceil(math.log2(300))}')\n"
        "print(f'found_bad_commit={lo}')\n",
    ),
    (
        "L01", "py", "(Mô phỏng định lượng) Nhánh sống càng lâu, xác suất đụng tệp càng tăng mạnh",
        "# Lab DVO L01 (Mô phỏng nhánh & CI) — Tính xác suất xung đột hợp nhất\n\n"
        "Viết chương trình Python tính xác suất ít nhất 1 trong `k = 40` thay đổi ngẫu nhiên chạm vào tập `5` trên `100` tệp "
        "theo công thức `1 - (1 - 5/100)^40`, so với nhánh nhỏ `5` thay đổi xen vào, in đúng 3 dòng:\n"
        "1. `p_conflict_40=87.1%`\n2. `p_conflict_5=22.6%`\n3. `shorter_branch_safer=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L01 duong_dan/bai_cua_ban.py\n```",
        "p1 = 1 - (1 - 5/100)**40; p2 = 1 - (1 - 5/100)**5\n"
        "print(f'p_conflict_40={100*p1:.1f}%')\nprint(f'p_conflict_5={100*p2:.1f}%')\n"
        "print(f'shorter_branch_safer={int(p2 < p1)}')\n",
    ),
    (
        "L02", "py", "So sánh phiên bản ngữ nghĩa (SemVer — ba số Chính.Phụ.Vá) phải tách thành bộ ba số nguyên, không so như chuỗi chữ",
        "# Lab DVO L02 — Phân tích & sắp xếp phiên bản ngữ nghĩa (SemVer — Chính.Phụ.Vá) đúng (tránh bẫy so chuỗi)\n\n"
        "Viết hàm `parse_ver(s)` tách `'1.10.0'` và `'1.9.3'` thành bộ số nguyên để so sánh, "
        "kiểm tra so chuỗi cho kết quả ngược và sắp danh sách `['1.10.0', '1.2.0', '1.9.3']`, in đúng 3 dòng:\n"
        "1. `semver_1_10_gt_1_9=1`\n2. `str_cmp_bug=1`\n3. `sorted_desc=1.10.0,1.9.3,1.2.0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L02 duong_dan/bai_cua_ban.py\n```",
        "key = lambda s: tuple(map(int, s.split('.')))\n"
        "vs = sorted(['1.10.0', '1.2.0', '1.9.3'], key=key, reverse=True)\n"
        "print(f'semver_1_10_gt_1_9={int(key(\"1.10.0\") > key(\"1.9.3\"))}')\n"
        "print(f'str_cmp_bug={int(\"1.10.0\" < \"1.9.3\")}')\n"
        "print('sorted_desc=' + ','.join(vs))\n",
    ),
    (
        "L03", "py", "(Mô phỏng định lượng) 300 bài test lỗi ngẫu nhiên 0.5% làm 77.8% lần chạy tích hợp liên tục (CI) đỏ",
        "# Lab DVO L03 (Mô phỏng tích hợp liên tục CI) — Xác suất đường ống đỏ vì bài kiểm thử chập chờn (flaky)\n\n"
        "Viết chương trình Python tính xác suất ít nhất 1 trong `300` test độc lập lỗi với `p = 0.005`, "
        "và so với khi giảm `p` xuống `0.0005` trên cùng `300` test, in đúng 3 dòng:\n"
        "1. `flaky_fail_pct_300=77.8%`\n2. `flaky_fail_pct_p0005=13.9%`\n3. `pipeline_always_green_pct=22.2%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L03 duong_dan/bai_cua_ban.py\n```",
        "g = (1 - 0.005)**300; f1 = 1 - g; f2 = 1 - (1 - 0.0005)**300\n"
        "print(f'flaky_fail_pct_300={100*f1:.1f}%')\nprint(f'flaky_fail_pct_p0005={100*f2:.1f}%')\n"
        "print(f'pipeline_always_green_pct={100*g:.1f}%')\n",
    ),
    (
        "L04", "py", "Sản phẩm dựng bất biến được định danh bằng SHA-256 thay vì dựng lại mỗi môi trường",
        "# Lab DVO L04 — Kiểm chứng SHA-256 sản phẩm dựng bất biến và tái lập\n\n"
        "Viết chương trình Python băm SHA-256 hai bản dựng nhị phân giống nhau `b'app-v1.4.2'` "
        "so với bản thay 1 byte `b'app-v1.4.3'`, kiểm tra toàn bộ `64` ký tự hệ 16 trùng khớp khi không đổi và đổi khác khi sửa 1 byte, in đúng 3 dòng:\n"
        "1. `same_artifact_same_hash=1`\n2. `changed_byte_different_hash=1`\n3. `sha256_len_hex=64`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L04 duong_dan/bai_cua_ban.py\n```",
        "import hashlib\nh = lambda b: hashlib.sha256(b).hexdigest()\n"
        "h1, h2, h3 = h(b'app-v1.4.2'), h(b'app-v1.4.2'), h(b'app-v1.4.3')\n"
        "print(f'same_artifact_same_hash={int(h1 == h2)}')\n"
        "print(f'changed_byte_different_hash={int(h1 != h3)}')\n"
        "print(f'sha256_len_hex={len(h1)}')\n",
    ),
    (
        "L05", "py", "Hạ tầng dạng mã (IaC — Infrastructure as Code) khai báo lũy đẳng đạt đúng trạng thái đích dù chạy 1 lần hay 10 lần",
        "# Lab DVO L05 — Đối chiếu Hạ tầng dạng mã khai báo (lũy đẳng) vs mệnh lệnh\n\n"
        "Viết hai hàm Python: `declarative_apply(cur, target=5)` (luôn đặt `replicas=5`) và "
        "`imperative_add(cur, delta=2)` chạy lặp 2 lần từ trạng thái ban đầu `3`, in đúng 3 dòng:\n"
        "1. `decl_after_2_runs=5`\n2. `imp_after_2_runs=7`\n3. `decl_is_idempotent=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L05 duong_dan/bai_cua_ban.py\n```",
        "decl = lambda cur, target=5: target\nimp = lambda cur, delta=2: cur + delta\n"
        "d1 = decl(decl(3)); i2 = imp(imp(3))\n"
        "print(f'decl_after_2_runs={d1}')\nprint(f'imp_after_2_runs={i2}')\n"
        "print(f'decl_is_idempotent={int(decl(d1) == d1)}')\n",
    ),
    (
        "L06", "py", "Bí mật từng commit rồi xoá vẫn còn trong lịch sử; dùng trình quét chặn trước commit",
        "# Lab DVO L06 — Quét rò rỉ bí mật và kiểm tra bí mật tồn tại trong lịch sử commit\n\n"
        "Viết chương trình Python quét 3 bản ghi lịch sử `['API_KEY=sk_live_987654', 'API_KEY=env_only', 'PORT=8080']`: "
        "chứng minh ở trạng thái cuối (`HEAD`) chuỗi sạch nhưng lịch sử vẫn giữ khoá ở mục 1, và viết regex phát hiện định dạng khoá `sk_live_...`, in đúng 3 dòng:\n"
        "1. `head_has_secret=0`\n2. `history_leaked_commits=1`\n3. `rotation_required=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L06 duong_dan/bai_cua_ban.py\n```",
        "import re\nhist = ['API_KEY=sk_live_987654', 'API_KEY=env_only', 'PORT=8080']\n"
        "pat = re.compile(r'sk_live_[0-9a-zA-Z]+')\n"
        "leaks = sum(bool(pat.search(c)) for c in hist)\n"
        "head = int(bool(pat.search(hist[-1])))\n"
        "print(f'head_has_secret={head}')\nprint(f'history_leaked_commits={leaks}')\n"
        "print(f'rotation_required={int(leaks > 0)}')\n",
    ),
    (
        "L07", "py", "(Mô phỏng định lượng) Kiểm tra ngưỡng canary dừng phát hành khi lỗi vượt nền",
        "# Lab DVO L07 (Mô phỏng Canary) — Tính tỉ lệ lỗi canary và xác suất p nhị thức\n\n"
        "Viết chương trình Python cho canary `1 000` yêu cầu gặp `20` lỗi trong khi nền lỗi cũ `p = 0.01`: "
        "tính số lỗi kỳ vọng (`10`), xác suất đuôi `P(X >= 20)` dưới `Binomial(1000, 0.01)` để ra quyết định rollback, in đúng 3 dòng:\n"
        "1. `expected_errors=10`\n2. `tail_prob_ge20=0.0033`\n3. `rollback_triggered=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L07 duong_dan/bai_cua_ban.py\n```",
        "import math\nn, p = 1000, 0.01\ntail = sum(math.comb(n, k)*(p**k)*((1-p)**(n-k)) for k in range(20, 60))\n"
        "print(f'expected_errors={int(n*p)}')\nprint(f'tail_prob_ge20={tail:.4f}')\n"
        "print(f'rollback_triggered={int(tail < 0.01)}')\n",
    ),
    (
        "L08", "py", "Di chuyển lược đồ mở rộng–thu gọn (Expand-Contract) giữ cả ứng dụng cũ lẫn mới chạy không đứt",
        "# Lab DVO L08 — Mô phỏng 4 bước mở rộng–thu gọn (Expand-Contract) đổi tên cột ten -> ho_ten không downtime\n\n"
        "Viết chương trình Python mô phỏng trình tự 4 bước mở rộng–thu gọn (Expand-Contract) trên danh sách 2 bản ghi `['An', 'Binh']`: "
        "B1 thêm cột mới, B2 ghi kép cả 2 cột + chép ngược dòng cũ, B3 chuyển sang đọc `ho_ten` (đếm số dòng thiếu `ho_ten` khi chuyển = `downtime_s`), B4 xoá cột cũ khi hết tham chiếu, in đúng 3 dòng:\n"
        "1. `steps_count=4`\n2. `dual_write_synced=1`\n3. `downtime_s=0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L08 duong_dan/bai_cua_ban.py\n```",
        "steps = ['expand_col', 'dual_write_backfill', 'switch_reads', 'drop_old_col']\n"
        "rows = [{'ten': 'An', 'ho_ten': None}, {'ten': 'Binh', 'ho_ten': None}]\n"
        "for r in rows: r['ho_ten'] = r['ten']\n"
        "ok = all(r['ten'] == r['ho_ten'] for r in rows)\n"
        "dt = sum(1 for r in rows if r['ho_ten'] is None)\n"
        "for r in rows: del r['ten']\n"
        "print(f'steps_count={len(steps)}')\nprint(f'dual_write_synced={int(ok)}')\nprint(f'downtime_s={dt}')\n",
    ),
    (
        "L09", "py", "Thời gian đưa thay đổi lên đo bằng trung vị (5h), không dùng trung bình lệch (8.8h)",
        "# Lab DVO L09 — Tính chỉ số DORA: tần suất triển khai và trung vị Lead Time\n\n"
        "Viết chương trình Python tính tần suất triển khai `40` lần trong `30` ngày, và trung vị thời gian "
        "của `[2, 5, 26, 8, 3]` giờ thay vì trung bình bị kéo bởi ca 26h, in đúng 3 dòng:\n"
        "1. `deploy_per_day=1.33`\n2. `lead_median_h=5`\n3. `lead_mean_h=8.8`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L09 duong_dan/bai_cua_ban.py\n```",
        "t = sorted([2, 5, 26, 8, 3])\nmed = t[len(t)//2]; avg = sum(t)/len(t)\n"
        "print(f'deploy_per_day={40/30:.2f}')\nprint(f'lead_median_h={med}')\nprint(f'lead_mean_h={avg:.1f}')\n",
    ),
    (
        "L10", "py", "Giảm thời gian phục hồi MTTR từ 1 giờ xuống 15 phút (MTBF 720h) giảm 4 lần gián đoạn",
        "# Lab DVO L10 — Độ sẵn sàng MTBF / (MTBF + MTTR) khi giảm MTTR 4 lần\n\n"
        "Viết chương trình Python tính độ sẵn sàng với `MTBF = 720 giờ` khi `MTTR = 1 giờ` so với khi tự động khôi phục còn `0.25 giờ` (15 phút), in đúng 3 dòng:\n"
        "1. `avail_1h=99.861%`\n2. `avail_15m=99.965%`\n3. `downtime_cut_factor=4.0x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L10 duong_dan/bai_cua_ban.py\n```",
        "av = lambda mtbf, mttr: 100 * mtbf / (mtbf + mttr)\n"
        "print(f'avail_1h={av(720, 1.0):.3f}%')\nprint(f'avail_15m={av(720, 0.25):.3f}%')\n"
        "print(f'downtime_cut_factor={1.0 / 0.25:.1f}x')\n",
    ),
    (
        "L11", "py", "1000 yêu cầu/giây (req/s) x 1 KB/req sinh 86.4 GB nhật ký (log)/ngày; giữ 30 ngày cần ~2.59 TB (nghìn tỉ byte)",
        "# Lab DVO L11 — Tính toán dung lượng lưu trữ nhật ký (log) theo lưu lượng yêu cầu/giây (req/s)\n\n"
        "Viết chương trình Python tính lượng nhật ký (theo hệ thập phân `1 GB = 10^9 B, 1 TB = 10^12 B`) "
        "khi phát sinh `1 000 yêu cầu/giây (req/s)`, mỗi dòng `1 000 B`, lưu giữ `30` ngày, in đúng 3 dòng:\n"
        "1. `gb_per_day=86.4`\n2. `tb_30_days=2.59`\n3. `sampling_10pct_tb=0.26`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L11 duong_dan/bai_cua_ban.py\n```",
        "b_day = 1000 * 1000 * 86400; gb = b_day / 1e9; tb30 = (b_day * 30) / 1e12\n"
        "print(f'gb_per_day={gb:.1f}')\nprint(f'tb_30_days={tb30:.2f}')\n"
        "print(f'sampling_10pct_tb={tb30 * 0.1:.2f}')\n",
    ),
    (
        "L12", "py", "Ký SHA-256 sản phẩm dựng bảo đảm mã chạy ở máy chủ thật (prod) đúng từ quy trình tích hợp (CI) đã duyệt",
        "# Lab DVO L12 — Ký và xác minh chữ ký gói dựng bằng RSA đồ chơi + SHA-256 thật\n\n"
        "Viết chương trình Python băm SHA-256 gói `b'release-v1.0'`, rút gọn `digest_int % 3233`, "
        "ký bằng khoá bí mật `d = 2753` trên `n = 61 * 53 = 3233`, rồi kiểm chứng lại bằng `e = 17`, in đúng 3 dòng:\n"
        "1. `n=3233 e=17`\n2. `sig_matches_digest=1`\n3. `tamper_detected=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L12 duong_dan/bai_cua_ban.py\n```",
        "import hashlib\nn, e, d = 3233, 17, 2753\n"
        "m = int(hashlib.sha256(b'release-v1.0').hexdigest(), 16) % n\n"
        "sig = pow(m, d, n); chk = pow(sig, e, n)\n"
        "m_bad = int(hashlib.sha256(b'release-tampered').hexdigest(), 16) % n\n"
        "print(f'n={n} e={e}')\nprint(f'sig_matches_digest={int(chk == m)}')\n"
        "print(f'tamper_detected={int(chk != m_bad)}')\n",
    ),
    (
        "L13", "py", "(Mô phỏng định lượng) Nhóm DORA (DevOps) mức cao (Elite) triển khai gấp 209 lần nhóm thấp (Low)",
        "# Lab DVO L13 (Mô phỏng nhóm DORA) — So sánh tỉ lệ triển khai giữa nhóm thấp (Low) và cao nhất (Elite)\n\n"
        "Viết chương trình Python chuẩn hoá khoảng `1 tháng..6 tháng` sang trung điểm `7 lần/năm` (nhóm thấp Low) "
        "so với `4 lần/ngày = 1 460 lần/năm` (nhóm cao nhất Elite) và tính bội số chênh lệch, in đúng 3 dòng:\n"
        "1. `low_per_year=7`\n2. `elite_per_year=1460`\n3. `ratio_round=209x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DVO L13 duong_dan/bai_cua_ban.py\n```",
        "low = (2 + 12) // 2; elite = 4 * 365\n"
        "print(f'low_per_year={low}')\nprint(f'elite_per_year={elite}')\n"
        "print(f'ratio_round={round(elite / low)}x')\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    cov = [(1, "stage1" if lid == "L13" else "example"), (2, "check"), (3, "practice")]
    fp, lo = up.apply_upgrade("DVO", lid, de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov)
    print(f"OK DVO {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("DVO", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")
tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "dvo", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl DVO:", tpl.stdout.strip() or tpl.stderr.strip())
