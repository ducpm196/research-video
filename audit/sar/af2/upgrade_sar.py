"""Nâng trọn bộ 14 bài SAR (L00–L13) lên chuẩn AF4 (common.upgrade_lesson force_code=True + lab P8 độc lập)."""
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
        "L00", "py", "Kiểm chứng phân vị thứ 95 (P95) với mục tiêu mức dịch vụ (SLO <= 160 ms)",
        "# Lab SAR L00 — Đo phân vị thứ 95 (P95) và kiểm tra mục tiêu mức dịch vụ (SLO)\n\n"
        "Sắp xếp chuỗi `100` mẫu độ trễ `[60 + (i % 25) * 4 for i in range(100)]` (đơn vị ms). "
        "Trích giá trị phân vị 95 (`P95` ở chỉ số `94`), phân vị 99 (`P99` ở chỉ số `98`) và kiểm tra mục tiêu mức dịch vụ (`SLO`: `P95 <= 160 ms`).\n\n"
        "Định dạng đầu ra (3 dòng):\n`p95_ms=<số>`\n`p99_ms=<số>`\n`slo_pass=<0|1>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L00 duong_dan/bai_cua_ban.py\n```",
        "lats = sorted(60 + (i % 25) * 4 for i in range(100))\n"
        "p95, p99 = lats[94], lats[98]\n"
        "print(f'p95_ms={p95}')\n"
        "print(f'p99_ms={p99}')\n"
        "print(f'slo_pass={int(p95 <= 160)}')\n",
    ),
    (
        "L01", "py", "Chấm điểm bản ghi quyết định kiến trúc (ADR) theo trọng số tiêu chí",
        "# Lab SAR L01 — Ma trận đánh đổi cho bản ghi quyết định kiến trúc (ADR)\n\n"
        "Chấm điểm hai phương án cơ sở dữ liệu theo bộ tiêu chí `(toàn vẹn ACID, nối bảng JOIN, mở rộng ghi)` với trọng số `(0.5, 0.2, 0.3)` cho dịch vụ ghi nhật ký phân tích tải cao: "
        "`RDBMS` đạt `(5, 5, 1)` và kho khoá-giá trị chia mảnh (`ShardedKV`) đạt `(3, 2, 5)`. Tính điểm từng phương án và chọn phương án ưu tiên.\n\n"
        "Định dạng đầu ra (3 dòng):\n`rdbms_score=<2 chữ số>`\n`sharded_kv_score=<2 chữ số>`\n`chosen=<RDBMS|ShardedKV>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L01 duong_dan/bai_cua_ban.py\n```",
        "w = (0.5, 0.2, 0.3)\n"
        "sc = lambda v: sum(a * b for a, b in zip(v, w))\n"
        "r, k = sc((5, 5, 1)), sc((3, 2, 5))\n"
        "chosen = 'RDBMS' if r >= k else 'ShardedKV'\n"
        "print(f'rdbms_score={r:.2f}')\n"
        "print(f'sharded_kv_score={k:.2f}')\n"
        "print(f'chosen={chosen}')\n",
    ),
    (
        "L02", "py", "Quy đổi 4 triệu người dùng hằng ngày (DAU) ra QPS trung bình và đỉnh x3",
        "# Lab SAR L02 — Ước lượng yêu cầu mỗi giây (QPS) và băng thông ở cao điểm\n\n"
        "Hệ thống có `4 000 000` người dùng hoạt động mỗi ngày (`DAU`), mỗi người phát `30` yêu cầu/ngày, kích thước trung bình `1,5 KB` (`1 500 byte`) mỗi yêu cầu. "
        "Tính `QPS` trung bình, `QPS` cao điểm (nhân `3x`) và băng thông đỉnh tính bằng `MB/giây`.\n\n"
        "Định dạng đầu ra (3 dòng):\n`avg_qps=<số>`\n`peak_qps=<số>`\n`peak_mb_per_s=<2 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L02 duong_dan/bai_cua_ban.py\n```",
        "avg = (4_000_000 * 30) / 86400\n"
        "peak = avg * 3\n"
        "mb_s = (peak * 1500) / 1e6\n"
        "print(f'avg_qps={round(avg)}')\n"
        "print(f'peak_qps={round(peak)}')\n"
        "print(f'peak_mb_per_s={mb_s:.2f}')\n",
    ),
    (
        "L03", "py", "Kiểm tra phụ thuộc một chiều Giao diện → Nghiệp vụ → Dữ liệu bằng đồ thị",
        "# Lab SAR L03 — Máy quét ranh giới phụ thuộc 3 lớp kiến trúc\n\n"
        "Xếp hạng 3 lớp `RANK = {'UI': 0, 'App': 1, 'Data': 2}`. Một cạnh gọi `(caller, callee)` chỉ hợp lệ khi `RANK[caller] < RANK[callee]`. "
        "Kiểm tra danh sách `[('UI', 'App'), ('App', 'Data'), ('UI', 'Data'), ('Data', 'App')]` để đếm cạnh hợp lệ và số vi phạm.\n\n"
        "Định dạng đầu ra (3 dòng):\n`valid_edges=<số>`\n`violations=<số>`\n`arch_clean=<0|1>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L03 duong_dan/bai_cua_ban.py\n```",
        "RANK = {'UI': 0, 'App': 1, 'Data': 2}\n"
        "edges = [('UI', 'App'), ('App', 'Data'), ('UI', 'Data'), ('Data', 'App')]\n"
        "ok = sum(RANK[u] < RANK[v] for u, v in edges)\n"
        "bad = len(edges) - ok\n"
        "print(f'valid_edges={ok}')\n"
        "print(f'violations={bad}')\n"
        "print(f'arch_clean={int(bad == 0)}')\n",
    ),
    (
        "L04", "py", "Độ trễ hiệu dụng khi bộ nhớ đệm (2 ms) vs cơ sở dữ liệu (80 ms) trúng 85% và 98%",
        "# Lab SAR L04 — Độ trễ trung bình theo tỉ lệ trúng bộ nhớ đệm (Cache Hit Rate)\n\n"
        "Cho thời gian đọc bộ nhớ đệm (`Cache`) là `2 ms` và cơ sở dữ liệu (`DB`) là `80 ms`. "
        "Tính độ trễ trung bình `h * 2 + (1 - h) * 80` tại tỉ lệ trúng `85%` và `98%`, cùng hệ số tăng tốc ở `98%` so với khi không có bộ nhớ đệm.\n\n"
        "Định dạng đầu ra (3 dòng):\n`lat_85pct_ms=<2 chữ số>`\n`lat_98pct_ms=<2 chữ số>`\n`speedup_98=<1 chữ số>x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L04 duong_dan/bai_cua_ban.py\n```",
        "eff = lambda h: h * 2.0 + (1.0 - h) * 80.0\n"
        "l85, l98 = eff(0.85), eff(0.98)\n"
        "print(f'lat_85pct_ms={l85:.2f}')\n"
        "print(f'lat_98pct_ms={l98:.2f}')\n"
        "print(f'speedup_98={80.0 / l98:.1f}x')\n",
    ),
    (
        "L05", "py", "Tính số phân mảnh (shard) và tổng số nút cho kho 8 TB với giới hạn 400 GB/nút",
        "# Lab SAR L05 — Quy mô phân mảnh (shard) khi nhân bản hệ số RF = 3\n\n"
        "Kho dữ liệu logic dung lượng `8 TB` (`8 000 GB`) cần chia mảnh sao cho mỗi nút giữ tối đa `400 GB`. "
        "Với hệ số sao chép (`RF`) bằng `3`, tính số phân mảnh tối thiểu, tổng số nút vật lý và tổng dung lượng lưu trên cụm.\n\n"
        "Định dạng đầu ra (3 dòng):\n`shards_needed=<số>`\n`total_nodes_rf3=<số>`\n`total_stored_tb=<số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L05 duong_dan/bai_cua_ban.py\n```",
        "import math\n"
        "rf = 3\n"
        "shards = math.ceil(8000 / 400)\n"
        "nodes = shards * rf\n"
        "print(f'shards_needed={shards}')\n"
        "print(f'total_nodes_rf3={nodes}')\n"
        "print(f'total_stored_tb={8 * rf}')\n",
    ),
    (
        "L06", "py", "So sánh độ sẵn sàng ghép song song vs nối tiếp hai nút độc lập 98%",
        "# Lab SAR L06 — Mạch sẵn sàng song song vs nối tiếp (98% mỗi thành phần)\n\n"
        "Hai thành phần độc lập có độ sẵn sàng `a = 0,98` mỗi nút. "
        "Tính độ sẵn sàng khi ghép song song (`1 - (1 - a)^2`), ghép nối tiếp (`a^2`) và tỉ số thời gian gián đoạn giữa nối tiếp với song song.\n\n"
        "Định dạng đầu ra (3 dòng):\n`parallel_pct=<2 chữ số>%`\n`series_pct=<2 chữ số>%`\n`downtime_ratio=<số>x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L06 duong_dan/bai_cua_ban.py\n```",
        "a = 0.98\n"
        "par = 1.0 - (1.0 - a) ** 2\n"
        "ser = a * a\n"
        "ratio = round((1.0 - ser) / (1.0 - par))\n"
        "print(f'parallel_pct={100 * par:.2f}%')\n"
        "print(f'series_pct={100 * ser:.2f}%')\n"
        "print(f'downtime_ratio={ratio}x')\n",
    ),
    (
        "L07", "py", "Mô phỏng thùng token (Token Bucket) nạp 15/s, sức chứa 30 trên luồng 3 200 yêu cầu",
        "# Lab SAR L07 — Bộ giới hạn tốc độ thùng token (Token Bucket)\n\n"
        "Thùng token bắt đầu đầy với sức chứa `cap = 30`, tốc độ nạp `rate = 15` token/giây. "
        "Mô phỏng từng giây trong `4` giây (`0..4` s) nhận tổng `3 200` yêu cầu dồn vào (`800` yêu cầu/s ở 4 đợt, kiểm tra lượng token khả dụng tích lũy theo quy tắc thùng token), đếm số yêu cầu được nhận (`accepted`) và bị từ chối bảo vệ hệ thống (`rejected`).\n\n"
        "Định dạng đầu ra (3 dòng):\n`accepted=<số>`\n`rejected=<số>`\n`accept_pct=<2 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L07 duong_dan/bai_cua_ban.py\n```",
        "tokens, total, acc = 30, 3200, 0\n"
        "for sec in range(5):\n"
        "    if sec > 0:\n"
        "        tokens += 15\n"
        "    take = min(tokens, 800 if sec > 0 else tokens)\n"
        "    acc += take\n"
        "    tokens -= take\n"
        "rej = total - acc\n"
        "print(f'accepted={acc}')\n"
        "print(f'rejected={rej}')\n"
        "print(f'accept_pct={100 * acc / total:.2f}%')\n",
    ),
    (
        "L08", "py", "Hàng đợi tồn đọng sau 30 phút (250/s vs 200/s) và thời gian xả khi nguồn giảm 140/s",
        "# Lab SAR L08 — Tính tồn đọng hàng đợi (backlog) và thời gian xả (drain)\n\n"
        "Trong `30` phút cao điểm (`1 800` giây), nguồn gửi `250 thông điệp/giây` trong khi dịch vụ xử lý `200 thông điệp/giây`. "
        "Sau đó nguồn giảm xuống `140 thông điệp/giây`. Tính tổng tồn đọng tích lũy, tốc độ xả ròng và số phút xả sạch.\n\n"
        "Định dạng đầu ra (3 dòng):\n`backlog_30m=<số>`\n`drain_net_per_s=<số>`\n`drain_minutes=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L08 duong_dan/bai_cua_ban.py\n```",
        "bl = (250 - 200) * 1800\n"
        "dr = 200 - 140\n"
        "print(f'backlog_30m={bl}')\n"
        "print(f'drain_net_per_s={dr}')\n"
        "print(f'drain_minutes={bl / dr / 60:.1f}')\n",
    ),
    (
        "L09", "py", "Khoá lũy đẳng trên SQLite: thử lại 3 lần cùng khoá 'req-42' chỉ trừ tiền 1 lần",
        "# Lab SAR L09 — Bảo toàn lũy đẳng giao dịch trên cơ sở dữ liệu SQLite\n\n"
        "Dùng `sqlite3` thật tạo bảng sổ cái `ledger(bal INT)` khởi tạo `400` và bảng khoá duy nhất `idem(k TEXT PRIMARY KEY)`. "
        "Chạy vòng lặp `3` lần thử trừ `125` với cùng khoá `'req-42'` trong cùng giao dịch `with conn:`, xác nhận số dư cuối cùng còn `275`.\n\n"
        "Định dạng đầu ra (3 dòng):\n`tx_attempts=<số>`\n`applied_once=<số>`\n`final_balance=<số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L09 duong_dan/bai_cua_ban.py\n```",
        "import sqlite3\n"
        "c = sqlite3.connect(':memory:')\n"
        "for q in ['CREATE TABLE ledger(bal INT)', 'INSERT INTO ledger VALUES(400)']:\n"
        "    c.execute(q)\n"
        "c.execute('CREATE TABLE idem(k TEXT PRIMARY KEY)')\n"
        "app = 0\n"
        "for att in range(1, 4):\n"
        "    try:\n"
        "        with c:\n"
        "            c.execute(\"INSERT INTO idem VALUES('req-42')\")\n"
        "            c.execute('UPDATE ledger SET bal = bal - 125')\n"
        "        app += 1\n"
        "    except sqlite3.IntegrityError: pass\n"
        "bal = c.execute('SELECT bal FROM ledger').fetchone()[0]\n"
        "print(f'tx_attempts={att}\\napplied_once={app}\\nfinal_balance={bal}')\n",
    ),
    (
        "L10", "py", "Độ trễ tối thiểu theo vòng khứ hồi (RTT = 72 ms) của ghi đồng bộ đa vùng",
        "# Lab SAR L10 — Đối chiếu độ trễ ghi đồng bộ liên vùng với ghi bất đồng bộ tại chỗ\n\n"
        "Hai vùng cách nhau độ trễ truyền một chiều `36 ms` (vòng khứ hồi `RTT = 2 * 36 = 72 ms`). "
        "So sánh độ trễ ghi đồng bộ liên vùng với ghi bất đồng bộ tại chỗ (`3 ms`) và tính tỉ số chênh lệch.\n\n"
        "Định dạng đầu ra (3 dòng):\n`sync_rtt_ms=<số>`\n`local_async_ms=<số>`\n`latency_ratio=<số>x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L10 duong_dan/bai_cua_ban.py\n```",
        "rtt, loc = 2 * 36, 3\n"
        "print(f'sync_rtt_ms={rtt}')\n"
        "print(f'local_async_ms={loc}')\n"
        "print(f'latency_ratio={rtt // loc}x')\n",
    ),
    (
        "L11", "py", "Kiểm chứng quyền tối thiểu chỉ đọc trên bản sao SQLite chặn mọi lệnh xoá",
        "# Lab SAR L11 — Khoá tài khoản báo cáo ở chế độ chỉ đọc trên SQLite\n\n"
        "Mở cơ sở dữ liệu `sqlite3` có bảng `invoices(amt INT)` chứa giá trị `950`, bật chế độ chỉ đọc (`PRAGMA query_only = ON`). "
        "Kiểm chứng lệnh đọc `SELECT` trả về đúng `950`, còn lệnh `DELETE` ném ngoại lệ `OperationalError` để khoanh vùng thiệt hại.\n\n"
        "Định dạng đầu ra (3 dòng):\n`read_allowed=<0|1>`\n`write_blocked=<0|1>`\n`blast_contained=<0|1>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L11 duong_dan/bai_cua_ban.py\n```",
        "import sqlite3\n"
        "c = sqlite3.connect(':memory:')\n"
        "c.execute('CREATE TABLE invoices(amt INT)')\n"
        "c.execute('INSERT INTO invoices VALUES(950)')\n"
        "c.execute('PRAGMA query_only = ON')\n"
        "val = c.execute('SELECT amt FROM invoices').fetchone()[0]\n"
        "blk = 0\n"
        "try:\n"
        "    c.execute('DELETE FROM invoices')\n"
        "except sqlite3.OperationalError:\n"
        "    blk = 1\n"
        "print(f'read_allowed={int(val == 950)}')\n"
        "print(f'write_blocked={blk}')\n"
        "print(f'blast_contained={int(blk == 1 and val == 950)}')\n",
    ),
    (
        "L12", "py", "Ước lượng tải đọc/ghi và lưu trữ 5 năm cho dịch vụ rút gọn đường dẫn 150M/tháng",
        "# Lab SAR L12 — Quy mô QPS đọc/ghi và dung lượng 5 năm cho trình rút gọn đường dẫn (URL)\n\n"
        "Dịch vụ rút gọn đường dẫn (`URL Shortener`) tạo `150 triệu` đường dẫn mới mỗi tháng (`30` ngày = `2 592 000` giây), tỉ lệ đọc gấp `200` lần ghi, mỗi bản ghi tốn `400 byte`. "
        "Tính tốc độ ghi `QPS`, tốc độ đọc tương ứng và tổng dung lượng lưu trữ `5` năm (`60` tháng).\n\n"
        "Định dạng đầu ra (3 dòng):\n`write_qps=<1 chữ số>`\n`read_qps=<số>`\n`storage_5yr_tb=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L12 duong_dan/bai_cua_ban.py\n```",
        "wq = 150_000_000 / (30 * 86400)\n"
        "rq = round(wq * 200)\n"
        "tb5 = (60 * 150_000_000 * 400) / 1e12\n"
        "print(f'write_qps={wq:.1f}')\n"
        "print(f'read_qps={rq}')\n"
        "print(f'storage_5yr_tb={tb5:.1f}')\n",
    ),
    (
        "L13", "py", "Tính lưu lượng ngày, tốc độ tweet/giây trung bình và đỉnh x3 trên quy mô 800 triệu/ngày",
        "# Lab SAR L13 — Quy đổi lưu lượng dòng thời gian 800 triệu bài đăng mỗi ngày\n\n"
        "Tính dung lượng thô mỗi ngày khi hệ thống nhận `800 000 000` bài đăng (`tweet`) ngắn, mỗi bài `250 byte` (`200 GB/ngày`), "
        "cùng tốc độ trung bình mỗi giây, tốc độ cao điểm hệ số `3x` và tổng dung lượng thô sau `1` năm (`365` ngày).\n\n"
        "Định dạng đầu ra (3 dòng):\n`daily_gb=<số>`\n`avg_and_peak_tps=<avg,peak>`\n`yearly_tb=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SAR L13 duong_dan/bai_cua_ban.py\n```",
        "daily_gb = (800_000_000 * 250) // 1_000_000_000\n"
        "avg_tps = 800_000_000 / 86400\n"
        "peak_tps = round(avg_tps * 3)\n"
        "print(f'daily_gb={daily_gb}')\n"
        "print(f'avg_and_peak_tps={round(avg_tps)},{peak_tps}')\n"
        "print(f'yearly_tb={daily_gb * 365 / 1000:.1f}')\n",
    ),
]

COVERS_MAP = {
    "L00": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L01": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L02": [(1, "example"), (2, "check"), (3, "practice")],
    "L03": [(1, "intuition"), (2, "example"), (3, "check")],
    "L04": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L05": [(1, "example"), (2, "check"), (3, "practice")],
    "L06": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L07": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L08": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L09": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L10": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L11": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L12": [(1, "example"), (2, "check"), (3, "practice")],
    "L13": [(1, "stage1"), (2, "stage5"), (3, "practice")],
}

if __name__ == "__main__":
    for lid, ext, hint, de_md, sol in LESSONS:
        common.upgrade_lesson(
            "SAR", lid, hint, de_md, sol,
            add_code_if_missing=True,
            covers=COVERS_MAP[lid],
            force_code=True,
        )
    led_p, nblk = up.sync_course_ledger("SAR", default_lang="python")
    for lid, _, _, _, sol in LESSONS:
        common.sync_practice_run_blocks("SAR", lid, sol)
    print(f"=== SAR: {len(LESSONS)} bài OK, ledger={nblk} blocks ===", flush=True)
    tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "SAR", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print("sync_tpl SAR:", tpl.stdout.strip() or tpl.stderr.strip())
