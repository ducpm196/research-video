"""Nâng trọn bộ 15 bài DEN (L00–L14) lên chuẩn AF4 (common.upgrade_lesson force_code=True + lab P8 độc lập)."""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[2])); import _frozen  # noqa: E402,F401
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402
import common  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

LESSONS = [
    (
        "L00", "py", "So sánh lượng dữ liệu đọc theo hàng vs theo cột trên bảng 50M x 40",
        "# Lab DEN L00 — Lưu trữ theo hàng vs theo cột\n\n"
        "Tính tổng dung lượng (`GB`, quy ước `1 GB = 10^9 byte`) phải đọc cho bảng `50 000 000` dòng x `40` cột x `8 byte/ô` khi truy vấn chỉ cần `4` cột, theo hai kiểu lưu: theo hàng (đọc đủ `40` cột) và theo cột (chỉ đọc `4` cột), cùng tỉ lệ tiết kiệm (%).\n\n"
        "Định dạng đầu ra (3 dòng):\n`row_scan_gb=<1 chữ số>`\n`col_scan_gb=<1 chữ số>`\n`io_saved_pct=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L00 duong_dan/bai_cua_ban.py\n```",
        "rows, cols, used, width = 50_000_000, 40, 4, 8\n"
        "row_gb = rows * cols * width / 1e9\n"
        "col_gb = rows * used * width / 1e9\n"
        "print(f'row_scan_gb={row_gb:.1f}')\nprint(f'col_scan_gb={col_gb:.1f}')\n"
        "print(f'io_saved_pct={100 * (row_gb - col_gb) / row_gb:.1f}%')\n",
    ),
    (
        "L01", "py", "Kỳ vọng số bảng SSTable phải mở khi có bộ lọc Bloom 2% trên 8 tệp",
        "# Lab DEN L01 — Bộ lọc xác suất Bloom trên cây LSM\n\n"
        "Khi tìm một khoá không tồn tại trên `8` tệp dữ liệu đã sắp (`SSTable`), mỗi tệp có bộ lọc xác suất Bloom với tỉ lệ dương tính giả (`FPR`) là `2%` (`0.02`), tính kỳ vọng số tệp phải mở đĩa và phần trăm đọc đĩa được tránh (%).\n\n"
        "Định dạng đầu ra (2 dòng):\n`expected_disk_reads=<2 chữ số>`\n`disk_avoided_pct=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L01 duong_dan/bai_cua_ban.py\n```",
        "files, fpr = 8, 0.02\n"
        "reads = files * fpr\n"
        "print(f'expected_disk_reads={reads:.2f}')\n"
        "print(f'disk_avoided_pct={100 * (1 - fpr):.1f}%')\n",
    ),
    (
        "L02", "py", "Khuếch đại ghi của cây B (trang 8192 B, bản ghi 128 B) vs gộp theo bậc",
        "# Lab DEN L02 — Khuếch đại ghi cây B vs LSM\n\n"
        "Sửa một bản ghi `128 byte` nằm trong trang `8 192 byte` của cây B (phải ghi lại cả trang). So sánh khuếch đại ghi của cây B với mô hình gộp theo bậc có `5` tầng nối tiếp nhau.\n\n"
        "Định dạng đầu ra (2 dòng):\n`btree_wa=<1 chữ số>x`\n`lsm_tiered_wa=<1 chữ số>x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L02 duong_dan/bai_cua_ban.py\n```",
        "page_b, rec_b, tiers = 8192, 128, 5\n"
        "print(f'btree_wa={page_b / rec_b:.1f}x')\n"
        "print(f'lsm_tiered_wa={float(tiers):.1f}x')\n",
    ),
    (
        "L03", "py", "Giới hạn số phần tử nhúng tối đa vào bản ghi 16 MiB (256 byte/phần tử)",
        "# Lab DEN L03 — Giới hạn kích thước bản ghi khi nhúng phần tử\n\n"
        "Cho ngưỡng tối đa một bản ghi là `16 MiB` (`16 * 1024 * 1024 byte`). Tính số phần tử kích thước `256 byte` tối đa có thể nhúng vào một bản ghi và kích thước còn thừa khi thêm `1` phần tử vượt giới hạn.\n\n"
        "Định dạng đầu ra (2 dòng):\n`max_embedded=<số nguyên>`\n`bytes_if_exceed=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L03 duong_dan/bai_cua_ban.py\n```",
        "limit_b, item_b = 16 * 1024 * 1024, 256\n"
        "max_n = limit_b // item_b\n"
        "print(f'max_embedded={max_n}')\n"
        "print(f'bytes_if_exceed={(max_n + 1) * item_b}')\n",
    ),
    (
        "L04", "py", "Chữa phân vùng nóng bằng thêm hậu tố muối chia đều 400 sự kiện vào 5 rổ",
        "# Lab DEN L04 — Tán điểm nóng bằng thêm hậu tố muối (salting)\n\n"
        "Mô phỏng `400` sự kiện của một cửa hàng quá tải `'vip'` đổ dồn vào 1 phân vùng nếu giữ khoá thô `'vip'`, so với rải bằng hậu tố `'vip#' + str(i % 5)` qua `5` phân vùng. Tính tải phân vùng lớn nhất trước và sau khi rải muối.\n\n"
        "Định dạng đầu ra (2 dòng):\n`raw_hot_max=<số nguyên>`\n`salted_max=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L04 duong_dan/bai_cua_ban.py\n```",
        "from collections import Counter\n"
        "raw = Counter(['vip'] * 400)\n"
        "salted = Counter(f'vip#{i % 5}' for i in range(400))\n"
        "print(f'raw_hot_max={max(raw.values())}')\n"
        "print(f'salted_max={max(salted.values())}')\n",
    ),
    (
        "L05", "py", "Chia bảng 30 ngày theo ngày để giảm lượng quét cho truy vấn 2 ngày",
        "# Lab DEN L05 — Chia phân vùng theo ngày để khoanh vùng truy vấn\n\n"
        "Một bảng nhật ký lưu `30` ngày liên tiếp, mỗi ngày phát sinh `50 MB` (`MB = mê-ga-byte`). Tính lượng dữ liệu (`MB`) phải quét cho truy vấn chỉ lọc đúng `2` ngày khi có phân vùng theo ngày so với quét toàn bảng.\n\n"
        "Định dạng đầu ra (3 dòng):\n`full_scan_mb=<số nguyên>`\n`pruned_scan_mb=<số nguyên>`\n`saved_pct=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L05 duong_dan/bai_cua_ban.py\n```",
        "days, per_day_mb, query_days = 30, 50, 2\n"
        "full_mb = days * per_day_mb\n"
        "pruned_mb = query_days * per_day_mb\n"
        "print(f'full_scan_mb={full_mb}')\nprint(f'pruned_scan_mb={pruned_mb}')\n"
        "print(f'saved_pct={100 * (full_mb - pruned_mb) / full_mb:.1f}%')\n",
    ),
    (
        "L06", "py", "Duyệt đồ thị theo chiều rộng (BFS) 2 bước có lọc đỉnh trùng",
        "# Lab DEN L06 — Duyệt đồ thị nhiều bước có lọc đỉnh đã thăm\n\n"
        "Cho đồ thị có hướng `g = {'u0': ['u1', 'u2'], 'u1': ['u2', 'u3'], 'u2': ['u3', 'u4'], 'u3': ['u5'], 'u4': [], 'u5': []}`. "
        "Bắt đầu từ `'u0'`, thực hiện tìm kiếm theo chiều rộng (`BFS`) trong đúng `2` bước đi (hop <= 2) có giữ tập đã thăm để loại trùng. In danh sách đã sắp xếp các đỉnh chạm tới ở vòng 1–2 (trừ `'u0'`) và tổng số đỉnh riêng biệt tìm được.\n\n"
        "Định dạng đầu ra (2 dòng):\n`reached_sorted=<danh sách>`\n`unique_count=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L06 duong_dan/bai_cua_ban.py\n```",
        "g = {'u0': ['u1', 'u2'], 'u1': ['u2', 'u3'], 'u2': ['u3', 'u4'],\n"
        "     'u3': ['u5'], 'u4': [], 'u5': []}\n"
        "seen, frontier = {'u0'}, ['u0']\n"
        "for _ in range(2):\n"
        "    nxt = []\n"
        "    for u in frontier:\n"
        "        for v in g[u]:\n"
        "            if v not in seen: seen.add(v); nxt.append(v)\n"
        "    frontier = nxt\n"
        "res = sorted(seen - {'u0'})\n"
        "print(f'reached_sorted={res}')\nprint(f'unique_count={len(res)}')\n",
    ),
    (
        "L07", "py", "Dựng chỉ mục ngược và tính điểm BM25 cho truy vấn ngắn trên 3 văn bản",
        "# Lab DEN L07 — Chỉ mục ngược và công thức xếp hạng BM25\n\n"
        "Cho kho 3 đoạn văn `docs = {1: 'may chu nhanh', 2: 'du lieu lon', 3: 'tim nhanh du lieu'}`. "
        "Dựng chỉ mục ngược từ tập đoạn văn này để lấy danh sách mã chứa từ `'nhanh'`, rồi tính điểm xếp hạng chuẩn `BM25` (`k1=1.2, b=0.75`) cho từ `'nhanh'` trong đoạn `1` (dùng công thức trực tiếp trên độ dài kho, không gán cứng).\n\n"
        "Định dạng đầu ra (2 dòng):\n`docs_with_nhanh=<danh sách ID>`\n`bm25_doc1=<4 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L07 duong_dan/bai_cua_ban.py\n```",
        "import math\n"
        "docs = {1: 'may chu nhanh', 2: 'du lieu lon', 3: 'tim nhanh du lieu'}\n"
        "postings = sorted(i for i, t in docs.items() if 'nhanh' in t.split())\n"
        "avgdl = sum(len(t.split()) for t in docs.values()) / len(docs)\n"
        "N, df, dl = len(docs), len(postings), len(docs[1].split())\n"
        "idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)\n"
        "tf = docs[1].split().count('nhanh')\n"
        "score = idf * (tf * 2.2) / (tf + 1.2 * (1 - 0.75 + 0.75 * dl / avgdl))\n"
        "print(f'docs_with_nhanh={postings}')\nprint(f'bm25_doc1={score:.4f}')\n",
    ),
    (
        "L08", "py", "Chia đều 10 phân vùng cho 4 thành viên nhóm tiêu thụ",
        "# Lab DEN L08 — Phân bổ phân vùng cho nhóm người đọc\n\n"
        "Chia `10` phân vùng cho `4` thành viên sao cho chênh lệch tối đa giữa các thành viên nhỏ nhất có thể. Tính số phân vùng từng người nhận theo thứ tự giảm dần và mức lệch phần trăm `(max - min) / min * 100`.\n\n"
        "Định dạng đầu ra (2 dòng):\n`counts=<danh sách 4 số>`\n`skew_pct=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L08 duong_dan/bai_cua_ban.py\n```",
        "P, M = 10, 4\n"
        "counts = [P // M + (1 if i < P % M else 0) for i in range(M)]\n"
        "skew = (max(counts) - min(counts)) / min(counts) * 100\n"
        "print(f'counts={counts}')\nprint(f'skew_pct={skew:.1f}%')\n",
    ),
    (
        "L09", "py", "Điểm kiểm tra và thời gian phát lại khi dòng mới vẫn đổ 8000/s",
        "# Lab DEN L09 — Phát lại từ điểm kiểm tra khi dòng mới tiếp tục đổ vào\n\n"
        "Khoảng cách giữa các điểm kiểm tra là `120` giây ở tốc độ nhận `8 000` sự kiện mỗi giây. Khi khởi động lại sau sự cố và xử lý ở công suất `24 000` sự kiện mỗi giây (trong khi dòng mới vẫn đến `8 000/s`), tính số sự kiện phải phát lại và thời gian đuổi kịp.\n\n"
        "Định dạng đầu ra (2 dòng):\n`replay_events=<số nguyên>`\n`catchup_s=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L09 duong_dan/bai_cua_ban.py\n```",
        "lag_s, in_r, proc_r = 120, 8000, 24000\n"
        "replay = lag_s * in_r\n"
        "catchup = replay / (proc_r - in_r)\n"
        "print(f'replay_events={replay}')\nprint(f'catchup_s={catchup:.1f}')\n",
    ),
    (
        "L10", "py", "Hộp thư đi (Outbox) trong SQLite đảm bảo tính nguyên tử giữa dữ liệu và sự kiện",
        "# Lab DEN L10 — Mẫu hộp thư đi nguyên tử trong SQLite\n\n"
        "Dùng `sqlite3` (CSDL SQLite trong bộ nhớ) tạo hai bảng `orders(id TEXT)` và `outbox(id TEXT)`. Thử ghi `('O100')` vào `orders` rồi kích hoạt lỗi trước khi ghi `outbox` để hoàn tác (`ROLLBACK`); sau đó thực hiện giao dịch hợp lệ ghi cả hai bảng với `('O200')`.\n\n"
        "Định dạng đầu ra (2 dòng):\n`orders_after_tx=<danh sách id>`\n`outbox_after_tx=<danh sách id>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L10 duong_dan/bai_cua_ban.py\n```",
        "import sqlite3\n"
        "c = sqlite3.connect(':memory:')\n"
        "c.executescript('CREATE TABLE orders(id TEXT); CREATE TABLE outbox(id TEXT);')\n"
        "c.execute(\"INSERT INTO orders VALUES('O100')\")\n"
        "c.rollback()\n"
        "c.execute(\"INSERT INTO orders VALUES('O200')\")\n"
        "c.execute(\"INSERT INTO outbox VALUES('O200')\")\n"
        "c.commit()\n"
        "o = [r[0] for r in c.execute('SELECT id FROM orders').fetchall()]\n"
        "ob = [r[0] for r in c.execute('SELECT id FROM outbox').fetchall()]\n"
        "print(f'orders_after_tx={o}')\nprint(f'outbox_after_tx={ob}')\n",
    ),
    (
        "L11", "py", "Thống kê nhỏ nhất–lớn nhất để bỏ qua 79/80 nhóm hàng được sắp theo cột",
        "# Lab DEN L11 — Bỏ qua nhóm hàng nhờ thống kê nhỏ nhất–lớn nhất\n\n"
        "Có `80` nhóm hàng sắp theo giá trị `(0..9), (10..19), ..., (790..799)`. Khi truy vấn lọc đúng `x = 123`, đếm số nhóm hàng bắt buộc phải đọc và tỉ lệ nhóm được bỏ qua (%).\n\n"
        "Định dạng đầu ra (2 dòng):\n`groups_scanned=<số nguyên>`\n`skipped_pct=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L11 duong_dan/bai_cua_ban.py\n```",
        "rgs = [(i * 10, i * 10 + 9) for i in range(80)]\n"
        "hit = sum(mn <= 123 <= mx for mn, mx in rgs)\n"
        "skip = 100 * (len(rgs) - hit) / len(rgs)\n"
        "print(f'groups_scanned={hit}')\nprint(f'skipped_pct={skip:.1f}%')\n",
    ),
    (
        "L12", "py", "Bảng chiều thay đổi chậm (SCD Loại 2) truy vấn lịch sử ở hai mốc thời gian",
        "# Lab DEN L12 — Truy vấn lịch sử trên bảng chiều thay đổi chậm trong SQLite\n\n"
        "Dùng `sqlite3` dựng bảng `scd(city TEXT, f TEXT, t TEXT)` lưu hai giai đoạn cho một khách hàng chuyển từ `'HCM'` sang `'HN'` ngày `'2026-04-15'` (`'2026-01-01'..'2026-04-14'` và `'2026-04-15'..'9999-12-31'`). Truy vấn thành phố hiệu lực tại `'2026-03-20'` và `'2026-05-01'`.\n\n"
        "Định dạng đầu ra (3 dòng):\n`scd_rows=<số nguyên>`\n`city_mar20=<tên>`\n`city_may01=<tên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L12 duong_dan/bai_cua_ban.py\n```",
        "import sqlite3\n"
        "c = sqlite3.connect(':memory:')\n"
        "c.execute('CREATE TABLE scd(city TEXT, f TEXT, t TEXT)')\n"
        "rows = [('HCM','2026-01-01','2026-04-14'),('HN','2026-04-15','9999-12-31')]\n"
        "c.executemany('INSERT INTO scd VALUES(?,?,?)', rows)\n"
        "sql = 'SELECT city FROM scd WHERE ? BETWEEN f AND t'\n"
        "q = lambda d: c.execute(sql, (d,)).fetchone()[0]\n"
        "n_r = c.execute('SELECT COUNT(*) FROM scd').fetchone()[0]\n"
        "print(f'scd_rows={n_r}')\nprint(f'city_mar20={q(\"2026-03-20\")}')\n"
        "print(f'city_may01={q(\"2026-05-01\")}')\n",
    ),
    (
        "L13", "py", "Nối 800 GB với 2 GB trên 50 máy: phát tán bảng nhỏ vs xáo trộn cả hai",
        "# Lab DEN L13 — So sánh chi phí mạng của nối phát tán và nối xáo trộn\n\n"
        "Nối bảng lớn `800 GB` (`GB = ghi-ga-byte`) với bảng nhỏ `2 GB` trên `50` máy. Tính tổng `GB` truyền qua mạng của cách phát tán bảng nhỏ (gửi bản sao tới `49` máy còn lại) so với xáo trộn đều cả hai bảng qua `50` máy (`49/50` phần mỗi bảng phải đi qua mạng).\n\n"
        "Định dạng đầu ra (3 dòng):\n`broadcast_gb=<số nguyên>`\n`shuffle_gb=<2 chữ số>`\n`network_saved_pct=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L13 duong_dan/bai_cua_ban.py\n```",
        "big_gb, sm_gb, nodes = 800, 2, 50\n"
        "bc = (nodes - 1) * sm_gb\n"
        "sh = (big_gb + sm_gb) * (nodes - 1) / nodes\n"
        "print(f'broadcast_gb={bc}')\nprint(f'shuffle_gb={sh:.2f}')\n"
        "print(f'network_saved_pct={100 * (sh - bc) / sh:.1f}%')\n",
    ),
    (
        "L14", "py", "Tần suất chết máy và sao lưu tác vụ dự phòng trên lô xử lý phân tán",
        "# Lab DEN L14 — Tái thử tác vụ trong mô hình ánh xạ–rút gọn\n\n"
        "Trong lô lịch sử `29 423` việc với trung bình `1.2` lần máy chết mỗi việc, tính tổng số lần mất máy ước lượng và xác nhận hệ thống hoàn thành toàn bộ việc khi bộ điều phối tự động chạy lại tác vụ hỏng trên máy khác.\n\n"
        "Định dạng đầu ra (3 dòng):\n`jobs=<số nguyên>`\n`worker_failures=<số nguyên>`\n`completed_all=<1 hoặc 0>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DEN L14 duong_dan/bai_cua_ban.py\n```",
        "jobs = 29423\n"
        "fails = round(jobs * 1.2)\n"
        "completed_all = int(jobs > 0 and fails > 0)\n"
        "print(f'jobs={jobs}')\nprint(f'worker_failures={fails}')\n"
        "print(f'completed_all={completed_all}')\n",
    ),
]

COVERS_MAP = {
    "L00": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L01": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L02": [(1, "sym"), (2, "example"), (3, "check")],
    "L03": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L04": [(1, "example"), (2, "pitfalls"), (3, "check")],
    "L05": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L06": [(1, "sym"), (2, "example"), (3, "check")],
    "L07": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L08": [(1, "example"), (2, "check"), (3, "practice")],
    "L09": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L10": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L11": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L12": [(1, "example"), (2, "check"), (3, "practice")],
    "L13": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L14": [(1, "stage1"), (2, "check"), (3, "stage5")],
}

if __name__ == "__main__":
    for lid, ext, hint, de_md, sol in LESSONS:
        common.upgrade_lesson(
            "DEN", lid, hint, de_md, sol,
            add_code_if_missing=True,
            covers=COVERS_MAP[lid],
            force_code=True,
        )
    led_p, nblk = up.sync_course_ledger("DEN", default_lang="python")
    for lid, _, _, _, sol in LESSONS:
        common.sync_practice_run_blocks("DEN", lid, sol)
    print(f"=== DEN: {len(LESSONS)} bài OK, ledger={nblk} blocks ===", flush=True)
    tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "DEN", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print("sync_tpl DEN:", tpl.stdout.strip() or tpl.stderr.strip())
