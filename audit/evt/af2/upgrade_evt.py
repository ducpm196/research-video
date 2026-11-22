"""Nâng trọn bộ 12 bài EVT (L00–L11) lên chuẩn AF4 (common.upgrade_lesson force_code=True + lab P8 độc lập)."""
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
        "L00", "py", "Kênh sự kiện giảm liên kết điểm–điểm theo N*(N-1)/2 xuống N kết nối",
        "# Lab EVT L00 — Giảm độ phức tạp kết nối nhờ kênh sự kiện\n\n"
        "Viết chương trình Python tính số kết nối tối đa điểm–điểm `N*(N-1)//2` so với qua 1 kênh sự kiện trung tâm `N` cho hai quy mô `N = 8` và `N = 40` dịch vụ, đồng thời tính phần trăm giảm kết nối ở `N = 40`.\n\n"
        "Định dạng đầu ra (3 dòng):\n`p2p_8=<số> bus_8=<số>`\n`p2p_40=<số> bus_40=<số>`\n`reduction_40=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L00 duong_dan/bai_cua_ban.py\n```",
        "p = lambda n: n * (n - 1) // 2\n"
        "p8, p40 = p(8), p(40)\n"
        "red = 100 * (p40 - 40) / p40\n"
        "print(f'p2p_8={p8} bus_8=8')\nprint(f'p2p_40={p40} bus_40=40')\n"
        "print(f'reduction_40={red:.1f}%')\n",
    ),
    (
        "L01", "py", "Kiểm tra tương thích lược đồ lược bỏ mặc định vs thiếu trường bắt buộc",
        "# Lab EVT L01 — Tiến hoá lược đồ tương thích xuôi và ngược\n\n"
        "Cho hai bản ghi sự kiện `v1 = {'order_id': 10, 'amount': 200}` và `v2 = {'order_id': 11, 'amount': 350, 'tier': 'vip'}`. "
        "Người nhận cũ bỏ qua trường lạ `tier` và chỉ cần đọc `order_id`, người nhận mới đọc `amount` với giá trị mặc định `'std'` nếu thiếu `tier` (tương thích hai chiều).\n\n"
        "Định dạng đầu ra (2 dòng):\n`old_reads_v2=<order_id nguyên>`\n`new_reads_v1=<tier mặc định>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L01 duong_dan/bai_cua_ban.py\n```",
        "v1 = {'order_id': 10, 'amount': 200}\n"
        "v2 = {'order_id': 11, 'amount': 350, 'tier': 'vip'}\n"
        "old_read = v2['order_id']\n"
        "new_tier = v1.get('tier', 'std')\n"
        "print(f'old_reads_v2={old_read}')\nprint(f'new_reads_v1={new_tier}')\n",
    ),
    (
        "L02", "py", "Kênh thư chết (DLQ) cách ly thông điệp độc sau 3 lần thử lại",
        "# Lab EVT L02 — Cô lập thông điệp độc vào kênh thư chết (DLQ)\n\n"
        "Mô phỏng vòng lặp tiêu thụ `500` thông điệp đánh số `1..500`, trong đó thông điệp `#7` luôn hỏng vĩnh viễn. "
        "Mỗi thông điệp hỏng được thử lại tối đa `3` lượt rồi đẩy sang kênh thư chết (`DLQ`) để các phần tử sau tiếp tục được xử lý.\n\n"
        "Định dạng đầu ra (3 dòng):\n`processed=<số nguyên>`\n`dlq=<danh sách>`\n`poison_attempts=<số lần thử của #7>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L02 duong_dan/bai_cua_ban.py\n```",
        "done, dlq, p_tries = 0, [], 0\n"
        "for msg in range(1, 501):\n"
        "    ok = False\n"
        "    for _ in range(3):\n"
        "        if msg == 7: p_tries += 1\n"
        "        else: ok = True; break\n"
        "    if ok: done += 1\n"
        "    else: dlq.append(msg)\n"
        "print(f'processed={done}')\nprint(f'dlq={dlq}')\n"
        "print(f'poison_attempts={p_tries}')\n",
    ),
    (
        "L03", "py", "Chặn bản cũ ghi đè bản mới bằng số phiên bản tăng dần theo khoá",
        "# Lab EVT L03 — Bảo toàn phiên bản đơn điệu khi gói tin đến lệch thứ tự\n\n"
        "Cho chuỗi cập nhật địa chỉ đến lệch thứ tự `[(2, 'HN'), (5, 'DN'), (3, 'HCM')]` theo cặp `(version, city)`. "
        "Chỉ áp dụng bản cập nhật có `version` lớn hơn phiên bản hiện đang giữ (trả về phiên bản và thành phố cuối).\n\n"
        "Định dạng đầu ra (2 dòng):\n`final_ver=<số nguyên>`\n`final_city=<tên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L03 duong_dan/bai_cua_ban.py\n```",
        "cur_ver, cur_city = 0, ''\n"
        "for ver, city in [(2, 'HN'), (5, 'DN'), (3, 'HCM')]:\n"
        "    if ver > cur_ver:\n"
        "        cur_ver, cur_city = ver, city\n"
        "print(f'final_ver={cur_ver}')\nprint(f'final_city={cur_city}')\n",
    ),
    (
        "L04", "py", "Gấp chuỗi sự kiện dựng trạng thái và tính giới hạn phát lại với ảnh chụp",
        "# Lab EVT L04 — Gấp chuỗi sự kiện (Event Sourcing) và ảnh chụp định kỳ\n\n"
        "Gấp danh sách biến động số dư `[+250, -80, +120, -40]` từ `0` để ra số dư hiện tại. "
        "Sau đó với kho `200 000` sự kiện chụp ảnh mỗi `500` sự kiện, tính tổng số ảnh chụp và số sự kiện tối đa cần phát lại khi phục hồi.\n\n"
        "Định dạng đầu ra (3 dòng):\n`balance=<số nguyên>`\n`snapshots=<số nguyên>`\n`max_replay=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L04 duong_dan/bai_cua_ban.py\n```",
        "events = [250, -80, 120, -40]\n"
        "bal = sum(events)\n"
        "snaps, replay = 200_000 // 500, 500\n"
        "print(f'balance={bal}')\nprint(f'snapshots={snaps}')\n"
        "print(f'max_replay={replay}')\n",
    ),
    (
        "L05", "py", "Tách ghi và đọc (CQRS): tính độ trễ bộ chiếu và thời gian xả tồn",
        "# Lab EVT L05 — Mô hình tách ghi–đọc (CQRS) và độ trễ chiếu\n\n"
        "Mô hình ghi nhận `600` sự kiện mỗi giây còn bộ chiếu xử lý `450` sự kiện mỗi giây trong `10` phút (`600` giây). "
        "Tính tổng sự kiện tồn chưa chiếu, độ trễ theo giây dữ liệu (`tồn / tốc độ ghi`), và thời gian xả hết tồn nếu mở song song `2` bộ chiếu (`900/s`) trong lúc vẫn ghi `600/s`.\n\n"
        "Định dạng đầu ra (3 dòng):\n`backlog=<số nguyên>`\n`data_lag_s=<1 chữ số>`\n`drain_with_2_s=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L05 duong_dan/bai_cua_ban.py\n```",
        "w, p, t = 600, 450, 600\n"
        "backlog = (w - p) * t\n"
        "lag_s = backlog / w\n"
        "drain_2 = backlog / (2 * p - w)\n"
        "print(f'backlog={backlog}')\nprint(f'data_lag_s={lag_s:.1f}')\n"
        "print(f'drain_with_2_s={drain_2:.1f}')\n",
    ),
    (
        "L06", "py", "Saga 3 bước với chạy bù trừ ngược thứ tự khi bước cuối thất bại",
        "# Lab EVT L06 — Bù trừ ngược thứ tự trong giao dịch dài (Saga)\n\n"
        "Chạy tuần tự 3 bước `['reserve_stock', 'charge_card', 'ship_order']`. "
        "Khi bước `'ship_order'` thất bại, hoàn tác các bước đã chạy thành công theo thứ tự đảo ngược thành danh sách `'undo_<bước>'`.\n\n"
        "Định dạng đầu ra (2 dòng):\n`failed_at=<tên bước>`\n`compensations=<danh sách>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L06 duong_dan/bai_cua_ban.py\n```",
        "steps = ['reserve_stock', 'charge_card', 'ship_order']\n"
        "done, failed = [], None\n"
        "for s in steps:\n"
        "    if s == 'ship_order': failed = s; break\n"
        "    done.append(s)\n"
        "comp = [f'undo_{s}' for s in reversed(done)]\n"
        "print(f'failed_at={failed}')\nprint(f'compensations={comp}')\n",
    ),
    (
        "L07", "py", "Nối hai luồng hiển thị và bấm theo khoá trong cửa sổ 600 giây",
        "# Lab EVT L07 — Nối luồng sự kiện trong cửa sổ thời gian\n\n"
        "Cho bảng mốc hiển thị `imps = {'x1': 50, 'x2': 180, 'x3': 310}` (giây) và các lượt bấm `[('x1', 200), ('x2', 900), ('x3', 500)]`. "
        "Tính hiệu thời gian và đếm số lượt bấm hợp lệ nằm trong cửa sổ `[0, 600]` giây sau hiển thị.\n\n"
        "Định dạng đầu ra (2 dòng):\n`matched=<danh sách mã>`\n`match_count=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L07 duong_dan/bai_cua_ban.py\n```",
        "imps = {'x1': 50, 'x2': 180, 'x3': 310}\n"
        "clicks = [('x1', 200), ('x2', 900), ('x3', 500)]\n"
        "hit = [k for k, t in clicks if k in imps and 0 <= t - imps[k] <= 600]\n"
        "print(f'matched={hit}')\nprint(f'match_count={len(hit)}')\n",
    ),
    (
        "L08", "py", "Độ trễ tiêu thụ khi gửi 900/s, xử lý 750/s trong 1 giờ và tăng lực",
        "# Lab EVT L08 — Tốc độ tăng độ trễ và thời gian xả tồn đọng\n\n"
        "Dịch vụ nhận `900` sự kiện mỗi giây trong khi bộ tiêu thụ chỉ xử lý `750` mỗi giây suốt `1` giờ (`3600` giây). "
        "Sau đó tăng năng lực xử lý lên `1 200` sự kiện mỗi giây (trong khi vẫn nhận `900/s`), tính số tồn sau 1 giờ và thời gian xả hết tồn.\n\n"
        "Định dạng đầu ra (2 dòng):\n`backlog_1h=<số nguyên>`\n`drain_s=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L08 duong_dan/bai_cua_ban.py\n```",
        "backlog = (900 - 750) * 3600\n"
        "drain_s = backlog / (1200 - 900)\n"
        "print(f'backlog_1h={backlog}')\nprint(f'drain_s={drain_s:.1f}')\n",
    ),
    (
        "L09", "py", "Thời gian đuổi kịp khi phát lại 20 ngày lịch sử gấp 4x trong lúc vẫn có dòng mới",
        "# Lab EVT L09 — Tính đúng thời gian phát lại lịch sử khi dòng mới vẫn chảy\n\n"
        "Cần phát lại toàn bộ `20` ngày lịch sử ở tốc độ đọc tối đa bằng `4` lần tốc độ đến hằng ngày, trong lúc sự kiện mới vẫn tiếp tục đổ về với tốc độ `1x`. "
        "So sánh ước lượng sai (quên dòng mới) với thời gian đuổi kịp thực tế.\n\n"
        "Định dạng đầu ra (2 dòng):\n`naive_days=<1 chữ số>`\n`real_catchup_days=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L09 duong_dan/bai_cua_ban.py\n```",
        "hist_days, speed = 20.0, 4.0\n"
        "naive = hist_days / speed\n"
        "real = hist_days / (speed - 1.0)\n"
        "print(f'naive_days={naive:.1f}')\nprint(f'real_catchup_days={real:.1f}')\n",
    ),
    (
        "L10", "py", "Đường găng trên đồ thị vết (DAG) có hai nhánh chạy song song",
        "# Lab EVT L10 — Độ trễ đầu–cuối qua đồ thị vết phụ thuộc (DAG)\n\n"
        "Trong một đồ thị phụ thuộc (`DAG`): bước `A` (`15 ms`) rẽ thành hai nhánh song song `B` (`30 ms`) và `C` (`70 ms`), cuối cùng bước `D` (`25 ms`) chờ cả hai xong. "
        "Tính tổng độ trễ nếu chạy tuần tự cả 4 bước so với đường găng song song.\n\n"
        "Định dạng đầu ra (2 dòng):\n`seq_ms=<số nguyên>`\n`critical_ms=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L10 duong_dan/bai_cua_ban.py\n```",
        "a, b, c, d = 15, 30, 70, 25\n"
        "seq = a + b + c + d\n"
        "crit = a + max(b, c) + d\n"
        "print(f'seq_ms={seq}')\nprint(f'critical_ms={crit}')\n",
    ),
    (
        "L11", "py", "Quy đổi lưu lượng ngày và giảm số vòng gọi mạng (RPC) nhờ gom lô",
        "# Lab EVT L11 — Quy mô luồng tin và giảm vòng gọi mạng nhờ gom lô\n\n"
        "Quy đổi tải `864 000 000` tin nhắn mỗi ngày ra tốc độ trung bình mỗi giây, đồng thời tính số lô phải gửi và hệ số giảm số vòng gọi mạng (`RPC`) khi gom `400 000` tin thành từng lô `40` tin.\n\n"
        "Định dạng đầu ra (3 dòng):\n`msgs_per_sec=<số nguyên>`\n`batches=<số nguyên>`\n`rpc_cut=<số nguyên>x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh EVT L11 duong_dan/bai_cua_ban.py\n```",
        "mps = round(864_000_000 / 86400)\n"
        "batch_sz = 40\n"
        "batches = 400_000 // batch_sz\n"
        "print(f'msgs_per_sec={mps}')\nprint(f'batches={batches}')\n"
        "print(f'rpc_cut={400_000 // batches}x')\n",
    ),
]

COVERS_MAP = {
    "L00": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L01": [(1, "example"), (2, "sym"), (3, "check")],
    "L02": [(1, "example"), (2, "sym"), (3, "practice")],
    "L03": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L04": [(1, "example"), (2, "check"), (3, "practice")],
    "L05": [(1, "practice"), (2, "example"), (3, "pitfalls")],
    "L06": [(1, "example"), (2, "practice"), (3, "check")],
    "L07": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L08": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L09": [(1, "example"), (2, "check"), (3, "practice")],
    "L10": [(1, "sym"), (2, "example"), (3, "practice")],
    "L11": [(1, "stage1"), (2, "check"), (3, "stage5")],
}

if __name__ == "__main__":
    for lid, ext, hint, de_md, sol in LESSONS:
        common.upgrade_lesson(
            "EVT", lid, hint, de_md, sol,
            add_code_if_missing=True,
            covers=COVERS_MAP[lid],
            force_code=True,
        )
    led_p, nblk = up.sync_course_ledger("EVT", default_lang="python")
    for lid, _, _, _, sol in LESSONS:
        common.sync_practice_run_blocks("EVT", lid, sol)
    print(f"=== EVT: {len(LESSONS)} bài OK, ledger={nblk} blocks ===", flush=True)
    tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "EVT", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print("sync_tpl EVT:", tpl.stdout.strip() or tpl.stderr.strip())
