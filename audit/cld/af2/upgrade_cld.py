"""Nâng trọn bộ 16 bài CLD (L00–L15) lên chuẩn AF4 (common.upgrade_lesson force_code=True + lab P8 độc lập)."""
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
        "L00", "py", "So sánh độ trễ gọi hàm nội bộ (ns) vs gọi mạng vi dịch vụ (ms)",
        "# Lab CLD L00 — Chi phí gọi qua mạng khi tách vi dịch vụ\n\n"
        "Tính tổng thời gian cho `20 000` lượt gọi trong hai trường hợp: gọi hàm nội bộ (`15` na-nô-giây/lần) và gọi dịch vụ qua mạng (`1.5` mi-li-giây/lần), rồi tính tỉ lệ chậm hơn.\n\n"
        "Định dạng đầu ra (3 dòng):\n`local_ms=<3 chữ số>`\n`rpc_ms=<1 chữ số>`\n`slowdown=<số nguyên>x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L00 duong_dan/bai_cua_ban.py\n```",
        "n = 20_000\n"
        "loc_ms = n * 15e-6\n"
        "rpc_ms = n * 1.5\n"
        "print(f'local_ms={loc_ms:.3f}')\nprint(f'rpc_ms={rpc_ms:.1f}')\n"
        "print(f'slowdown={round(rpc_ms / loc_ms)}x')\n",
    ),
    (
        "L01", "py", "Bộ nhớ nền của 12 ứng dụng khi chạy container chung nhân vs máy ảo",
        "# Lab CLD L01 — So sánh bộ nhớ (RAM) nền giữa container và máy ảo\n\n"
        "Trên một máy chủ chạy `12` ứng dụng, mỗi ứng dụng tự chiếm `40 MB` (`MB = mê-ga-byte`). "
        "Container dùng chung nhân hệ điều hành (`0 MB` nhân thêm), còn mỗi máy ảo (`VM`) tốn riêng `450 MB` cho hệ điều hành khách. Tính tổng RAM (tính theo `MB` và phần dư tính bằng `GB`, `1 GB = 1000 MB`).\n\n"
        "Định dạng đầu ra (3 dòng):\n`container_mb=<số nguyên>`\n`vm_mb=<số nguyên>`\n`vm_extra_gb=<2 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L01 duong_dan/bai_cua_ban.py\n```",
        "apps, app_mb, os_mb = 12, 40, 450\n"
        "cont = apps * app_mb\n"
        "vm = apps * (app_mb + os_mb)\n"
        "print(f'container_mb={cont}')\nprint(f'vm_mb={vm}')\n"
        "print(f'vm_extra_gb={(vm - cont) / 1000:.2f}')\n",
    ),
    (
        "L02", "py", "Ảnh chồng lớp: sửa bước chép thư viện hay sửa mã nguồn phá bộ đệm",
        "# Lab CLD L02 — Tận dụng bộ nhớ đệm các lớp khi dựng ảnh\n\n"
        "Cho chuỗi 4 lớp dựng ảnh `['FROM py', 'COPY req.txt', 'RUN pip install', 'COPY src']` (dựng lại một lớp buộc dựng lại toàn bộ lớp phía sau). "
        "Đếm số lớp vẫn dùng lại được từ bộ đệm (`cache hits`) khi thay đổi chỉ ở bước `'COPY src'` so với thay đổi ở `'COPY req.txt'`.\n\n"
        "Định dạng đầu ra (2 dòng):\n`hits_src_change=<số nguyên>`\n`hits_req_change=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L02 duong_dan/bai_cua_ban.py\n```",
        "layers = ['FROM py', 'COPY req.txt', 'RUN pip install', 'COPY src']\n"
        "hits = lambda ch: layers.index(ch)\n"
        "print(f'hits_src_change={hits(\"COPY src\")}')\n"
        "print(f'hits_req_change={hits(\"COPY req.txt\")}')\n",
    ),
    (
        "L03", "py", "Độ sẵn sàng chuỗi 4 dịch vụ nối tiếp nhau cùng đạt 99,8%",
        "# Lab CLD L03 — Sẵn sàng của chuỗi phụ thuộc đồng bộ\n\n"
        "Chuỗi `4` dịch vụ gọi đồng bộ nối tiếp nhau, mỗi dịch vụ có độ sẵn sàng `0.998` (`99.8%`). "
        "Tính độ sẵn sàng chung của chuỗi (`0.998^4`) và tổng số phút gián đoạn kỳ vọng trong 1 năm (`525 600` phút).\n\n"
        "Định dạng đầu ra (2 dòng):\n`avail_pct=<2 chữ số>%`\n`downtime_min=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L03 duong_dan/bai_cua_ban.py\n```",
        "avail = 0.998 ** 4\n"
        "down = (1.0 - avail) * 525_600\n"
        "print(f'avail_pct={avail * 100:.2f}%')\n"
        "print(f'downtime_min={down:.1f}')\n",
    ),
    (
        "L04", "py", "Bão thử lại qua 4 tầng gọi đồng bộ và tổng chờ lùi lũy thừa",
        "# Lab CLD L04 — Khuếch đại thử lại và thời gian chờ lùi lũy thừa\n\n"
        "Một yêu cầu đi qua chuỗi `4` tầng, mỗi tầng thử lại tối đa `2` lần khi gặp lỗi (hệ số khuếch đại `2^4`). "
        "Đồng thời với dãy chờ lùi lũy thừa cơ bản `50, 100, 200 ms`, tính tổng độ trễ chờ đợi cộng dồn qua 3 lần thử lại.\n\n"
        "Định dạng đầu ra (2 dòng):\n`amplified_reqs=<số nguyên>`\n`backoff_sum_ms=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L04 duong_dan/bai_cua_ban.py\n```",
        "amp = 2 ** 4\n"
        "backoff_ms = sum([50, 100, 200])\n"
        "print(f'amplified_reqs={amp}')\n"
        "print(f'backoff_sum_ms={backoff_ms}')\n",
    ),
    (
        "L05", "py", "Vòng điều khiển khai báo tạo bù các Pod còn thiếu về trạng thái mong muốn",
        "# Lab CLD L05 — Vòng đối chiếu trạng thái mong muốn và thực tế\n\n"
        "Viết hàm `reconcile(desired, running)` nhận trạng thái mong muốn `desired = ['p1', 'p2', 'p3', 'p4']` và trạng thái đang chạy `running = ['p1', 'p3']`. "
        "Tính danh sách các bản cần khởi tạo mới (`created`), cập nhật `running` khớp `desired`, và kiểm tra kết quả sau 1 vòng.\n\n"
        "Định dạng đầu ra (2 dòng):\n`created=<danh sách>`\n`converged=<1 hoặc 0>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L05 duong_dan/bai_cua_ban.py\n```",
        "def reconcile(des, cur):\n"
        "    miss = [p for p in des if p not in cur]\n"
        "    return sorted(cur + miss), miss\n"
        "des, cur = ['p1', 'p2', 'p3', 'p4'], ['p1', 'p3']\n"
        "after, created = reconcile(des, cur)\n"
        "print(f'created={created}')\nprint(f'converged={int(after == sorted(des))}')\n",
    ),
    (
        "L06", "py", "Xếp Pod 2.2 CPU lên nút 6.0 CPU: phầnCPU dư bị kẹt không đủ cho Pod tiếp",
        "# Lab CLD L06 — Phân mảnh tài nguyên khi xếp Pod lên nút máy\n\n"
        "Mỗi nút máy có `6.0 CPU` (`CPU` = đơn vị xử lý), mỗi `Pod` yêu cầu `2.2 CPU`. Tính số `Pod` tối đa xếp được vào một nút và phần trăm tài nguyên bị kẹt không sử dụng.\n\n"
        "Định dạng đầu ra (2 dòng):\n`pods_per_node=<số nguyên>`\n`stranded_pct=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L06 duong_dan/bai_cua_ban.py\n```",
        "cap, req = 6.0, 2.2\n"
        "fit = int(cap // req)\n"
        "wasted = (cap - fit * req) / cap * 100\n"
        "print(f'pods_per_node={fit}')\nprint(f'stranded_pct={wasted:.1f}%')\n",
    ),
    (
        "L07", "py", "Bộ tự co giãn ngang (HPA) với vùng đệm dung sai 10% tránh dao động",
        "# Lab CLD L07 — Công thức tự co giãn ngang (HPA) kèm dung sai\n\n"
        "Viết hàm `hpa(cur, cpu, tgt=60, tol=0.10)` trả về `cur` nếu `|cpu/tgt - 1| <= tol`, ngược lại trả về `ceil(cur * cpu / tgt)`. "
        "Kiểm tra từ `cur = 6` với mức tải cao `cpu = 84%` (cần mở rộng) và tải gần đích `cpu = 64%` (giữ nguyên).\n\n"
        "Định dạng đầu ra (2 dòng):\n`replicas_at_84=<số nguyên>`\n`replicas_at_64=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L07 duong_dan/bai_cua_ban.py\n```",
        "import math\n"
        "def hpa(cur, cpu, tgt=60, tol=0.10):\n"
        "    if abs(cpu / tgt - 1.0) <= tol: return cur\n"
        "    return math.ceil(cur * cpu / tgt)\n"
        "print(f'replicas_at_84={hpa(6, 84)}')\n"
        "print(f'replicas_at_64={hpa(6, 64)}')\n",
    ),
    (
        "L08", "py", "Cập nhật cuốn chiếu 12 Pod: tính min sẵn sàng và tổng tối đa",
        "# Lab CLD L08 — Tham số an toàn khi cập nhật cuốn chiếu\n\n"
        "Với `12` bản sao, đặt `maxUnavailable = 25%` (làm tròn xuống) và `maxSurge = 25%` (làm tròn lên). Tính số bản sao tối thiểu luôn sẵn sàng phục vụ và tổng số bản sao tối đa chạy tạm thời trong lúc cập nhật.\n\n"
        "Định dạng đầu ra (2 dòng):\n`min_ready=<số nguyên>`\n`max_total=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L08 duong_dan/bai_cua_ban.py\n```",
        "import math\n"
        "n, unavail_p, surge_p = 12, 0.25, 0.25\n"
        "min_r = n - math.floor(n * unavail_p)\n"
        "max_t = n + math.ceil(n * surge_p)\n"
        "print(f'min_ready={min_r}')\nprint(f'max_total={max_t}')\n",
    ),
    (
        "L09", "py", "Cân bằng tải: chọn 1 máy ngẫu nhiên vs tốt hơn trong 2 lựa chọn",
        "# Lab CLD L09 — Giảm đỉnh tải nhờ chọn tốt hơn trong hai (P2C)\n\n"
        "Dùng `random.Random(99)` mô phỏng `15 000` yêu cầu vào `50` máy với giả định các yêu cầu nằm lại tích lũy trên máy theo đếm lượt. "
        "So sánh tải cực đại khi chọn ngẫu nhiên 1 máy (`rand1`) so với chọn 2 máy khác nhau và lấy máy ít tải hơn (`p2c`).\n\n"
        "Định dạng đầu ra (3 dòng):\n`max_rand1=<số nguyên>`\n`max_p2c=<số nguyên>`\n`p2c_better=<1 hoặc 0>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L09 duong_dan/bai_cua_ban.py\n```",
        "import random\n"
        "def sim(p2c):\n"
        "    r = random.Random(99); c = [0] * 50\n"
        "    for _ in range(15_000):\n"
        "        a = r.randrange(50)\n"
        "        if p2c:\n"
        "            b = r.randrange(50)\n"
        "            if c[b] < c[a]: a = b\n"
        "        c[a] += 1\n"
        "    return max(c)\n"
        "r1, r2 = sim(False), sim(True)\n"
        "print(f'max_rand1={r1}')\nprint(f'max_p2c={r2}')\nprint(f'p2c_better={int(r2 < r1)}')\n",
    ),
    (
        "L10", "py", "Độ trễ bùng nổ theo công thức 1/(mu - lam) khi tải tiến sát công suất 200/s",
        "# Lab CLD L10 — Dư địa công suất quyết định độ trễ hàng chờ\n\n"
        "Với công suất phục vụ `mu = 200` yêu cầu/giây, áp dụng công thức độ trễ hàng chờ `W = 1000 / (mu - lam)` (đơn vị mi-li-giây) tại mức tải an toàn `150/s` và mức tải gần trần `190/s`.\n\n"
        "Định dạng đầu ra (2 dòng):\n`w_at_150=<1 chữ số>ms`\n`w_at_190=<1 chữ số>ms`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L10 duong_dan/bai_cua_ban.py\n```",
        "mu = 200.0\n"
        "w150 = 1000.0 / (mu - 150.0)\n"
        "w190 = 1000.0 / (mu - 190.0)\n"
        "print(f'w_at_150={w150:.1f}ms')\n"
        "print(f'w_at_190={w190:.1f}ms')\n",
    ),
    (
        "L11", "py", "Độ trễ đuôi khuếch đại qua 80 máy gọi song song với xác suất chậm 1.5%",
        "# Lab CLD L11 — Xác suất dính đuôi chậm khi phân nhánh qua 80 máy\n\n"
        "Một yêu cầu gọi song song tới `80` máy độc lập và phải chờ tất cả cùng xong. Biết mỗi máy có tỉ lệ chậm bất thường là `1.5%` (`0.015`), tính tỉ lệ (%) các yêu cầu bị dính chậm do ít nhất 1 máy chậm.\n\n"
        "Định dạng đầu ra (2 dòng):\n`all_fast_pct=<1 chữ số>%`\n`slow_req_pct=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L11 duong_dan/bai_cua_ban.py\n```",
        "p_slow, k = 0.015, 80\n"
        "all_fast = (1.0 - p_slow) ** k\n"
        "print(f'all_fast_pct={all_fast * 100:.1f}%')\n"
        "print(f'slow_req_pct={(1.0 - all_fast) * 100:.1f}%')\n",
    ),
    (
        "L12", "py", "Tính ngân sách lỗi cho mục tiêu sẵn sàng 99,95% và 99,99% trong 30 ngày",
        "# Lab CLD L12 — Quy đổi mục tiêu mức dịch vụ (SLO) ra ngân sách lỗi\n\n"
        "Trong một chu kỳ `30` ngày (`43 200` phút), tính số phút ngừng hoạt động tối đa được phép (ngân sách lỗi) ứng với hai mức mục tiêu `99.95%` và `99.99%`.\n\n"
        "Định dạng đầu ra (2 dòng):\n`budget_9995_min=<2 chữ số>`\n`budget_9999_min=<2 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L12 duong_dan/bai_cua_ban.py\n```",
        "mins = 30 * 24 * 60\n"
        "b1 = mins * (1.0 - 0.9995)\n"
        "b2 = mins * (1.0 - 0.9999)\n"
        "print(f'budget_9995_min={b1:.2f}')\n"
        "print(f'budget_9999_min={b2:.2f}')\n",
    ),
    (
        "L13", "py", "Xoá tệp bí mật ở lớp ảnh sau nhưng bí mật vẫn tồn tại ở lớp bất biến trước",
        "# Lab CLD L13 — Rò rỉ bí mật trong các lớp ảnh bất biến\n\n"
        "Mô phỏng 3 lớp ảnh cộng gộp: lớp 1 tạo `{'app.py', 'key.env'}`, lớp 2 sao chép thêm `'cfg.yml'`, lớp 3 xoá `'key.env'` khỏi giao diện cuối (`visible`). "
        "Kiểm tra xem tệp nhìn thấy cuối cùng có còn `'key.env'` không và lịch sử toàn bộ các lớp ảnh có vẫn còn giữ `'key.env'` không.\n\n"
        "Định dạng đầu ra (2 dòng):\n`in_final_view=<1 hoặc 0>`\n`leaked_in_layers=<1 hoặc 0>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L13 duong_dan/bai_cua_ban.py\n```",
        "layers = [\n"
        "    {'app.py', 'key.env'},\n"
        "    {'app.py', 'key.env', 'cfg.yml'},\n"
        "    {'app.py', 'cfg.yml'},\n"
        "]\n"
        "in_final = int('key.env' in layers[-1])\n"
        "leaked = int(any('key.env' in l for l in layers))\n"
        "print(f'in_final_view={in_final}')\nprint(f'leaked_in_layers={leaked}')\n",
    ),
    (
        "L14", "py", "Bù trừ nhả ghế khi bước thanh toán trong Saga đặt vé thất bại",
        "# Lab CLD L14 — Bù trừ nhả tài nguyên trong Saga đặt vé\n\n"
        "Rạp có `15` ghế trống ban đầu (`available = 15`). Bước 1 giữ `2` ghế (`reserve`), nhưng bước 2 thanh toán thất bại nên phải kích hoạt hàm bù trừ nhả lại `2` ghế (`release`). In trạng thái tồn kho qua từng bước.\n\n"
        "Định dạng đầu ra (2 dòng):\n`after_reserve=<số nguyên>`\n`after_compensate=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L14 duong_dan/bai_cua_ban.py\n```",
        "avail = 15\n"
        "avail -= 2; after_res = avail\n"
        "avail += 2; after_comp = avail\n"
        "print(f'after_reserve={after_res}')\n"
        "print(f'after_compensate={after_comp}')\n",
    ),
    (
        "L15", "py", "Ước lượng chi phí bổ sung 25% máy khi tách tải tương tác và xử lý lô",
        "# Lab CLD L15 — Máy cần thêm khi tách luồng phục vụ quy mô lớn\n\n"
        "Cho cụm `10 000` máy cần thêm phần dự phòng ở điểm giữa `25%` (`2 500` máy) để tách luồng tương tác và xử lý lô, và giả lập mất `10` phút gián đoạn trong cửa sổ cập nhật lớn `14 400` phút (tỉ lệ `0.07%`). Tính số máy thêm và tỉ lệ phần trăm thời gian mất kết nối.\n\n"
        "Định dạng đầu ra (2 dòng):\n`extra_machines=<số nguyên>`\n`downtime_pct=<2 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLD L15 duong_dan/bai_cua_ban.py\n```",
        "extra = round(10_000 * 0.25)\n"
        "pct = 10.0 / 14_400 * 100\n"
        "print(f'extra_machines={extra}')\n"
        "print(f'downtime_pct={pct:.2f}%')\n",
    ),
]

COVERS_MAP = {
    "L00": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L01": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L02": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L03": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L04": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L05": [(1, "example"), (2, "sym"), (3, "pitfalls")],
    "L06": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L07": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L08": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L09": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L10": [(1, "sym"), (2, "example"), (3, "check")],
    "L11": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L12": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L13": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "L14": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L15": [(1, "intuition"), (2, "check"), (3, "stage5")],
}

if __name__ == "__main__":
    for lid, ext, hint, de_md, sol in LESSONS:
        common.upgrade_lesson(
            "CLD", lid, hint, de_md, sol,
            add_code_if_missing=True,
            covers=COVERS_MAP[lid],
            force_code=True,
        )
    led_p, nblk = up.sync_course_ledger("CLD", default_lang="python")
    for lid, _, _, _, sol in LESSONS:
        common.sync_practice_run_blocks("CLD", lid, sol)
    print(f"=== CLD: {len(LESSONS)} bài OK, ledger={nblk} blocks ===", flush=True)
    tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "CLD", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print("sync_tpl CLD:", tpl.stdout.strip() or tpl.stderr.strip())
