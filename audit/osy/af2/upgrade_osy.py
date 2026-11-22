"""Nâng trọn bộ 16 bài OSY (L00–L15) lên chuẩn AF2 theo bảng quyết định BN-08.

- Toàn bộ 16 bài kiểm chuẩn thực thi qua labs/cham.sh (mô phỏng định lượng tất định
  + lời gọi hệ thống / kiểm chứng quy mô số học), gắn nhãn rõ ràng '(Mô phỏng định lượng)'.
- Giữ nguyên toàn bộ cảnh gốc đã kiểm duyệt; thêm cảnh `practice`, `covers`, đồng bộ
  sổ screen_code/OSY.yaml và template curriculum/osy.yaml.
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
        "L00", "c", "Chi phí chuyển ngữ cảnh = số lần/giây nhân thời gian mỗi lần",
        "# Lab OSY L00 — Chế độ nhân, lời gọi hệ thống và chi phí chuyển ngữ cảnh\n\n"
        "Viết chương trình C chuẩn C11 tính chi phí CPU khi thực hiện `1 000` lần "
        "chuyển ngữ cảnh mỗi giây (mỗi lần `5 us`) và so với mức `50 000` lần/giây, "
        "cũng như đọc đúng mã phân biệt chuyển ngữ cảnh vs gọi hàm thường (`mode_switch=1`), in đúng 3 dòng:\n"
        "1. `cpu_pct_1k=0.50`\n2. `cpu_pct_50k=25.00`\n3. `syscall_mode_switch=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L00 duong_dan/bai_cua_ban.c\n```",
        "#include <stdio.h>\nint main(void) {\n"
        "    double t_1k = 1000.0 * 5e-6 * 100.0;\n"
        "    double t_50k = 50000.0 * 5e-6 * 100.0;\n"
        "    printf(\"cpu_pct_1k=%.2f\\n\", t_1k);\n"
        "    printf(\"cpu_pct_50k=%.2f\\n\", t_50k);\n"
        "    printf(\"syscall_mode_switch=1\\n\");\n    return 0;\n}\n",
    ),
    (
        "L01", "py", "(Mô phỏng định lượng) k lần fork() (nhân bản tiến trình) liên tiếp tạo 2^k tiến trình",
        "# Lab OSY L01 (Mô phỏng tiến trình) — Đếm cây tiến trình fork()\n\n"
        "Viết chương trình Python mô phỏng số tiến trình sinh ra sau `3` và `4` lệnh `fork()` (nhân bản tiến trình) "
        "liên tiếp (`2^k` kể cả tiến trình gốc) và đếm số không gian địa chỉ dùng chung nếu 4 luồng nằm trong cùng 1 tiến trình `pid=100`, in đúng 3 dòng:\n"
        "1. `procs_fork3=8`\n2. `procs_fork4=16`\n3. `shared_spaces_4threads=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L01 duong_dan/bai_cua_ban.py\n```",
        "procs = [1]\nfor _ in range(4): procs.append(procs[-1] * 2)\n"
        "thread_addr_spaces = [100 for _ in range(4)]\n"
        "print(f'procs_fork3={procs[3]}')\n"
        "print(f'procs_fork4={procs[4]}')\n"
        "print(f'shared_spaces_4threads={len(set(thread_addr_spaces))}')\n",
    ),
    (
        "L02", "py", "(Mô phỏng định lượng) SJF giảm thời gian chờ trung bình của [24, 3, 3]",
        "# Lab OSY L02 (Mô phỏng lập lịch CPU) — So sánh FCFS và SJF\n\n"
        "Viết chương trình Python mô phỏng hai thuật toán FCFS (đến trước phục vụ trước) và SJF (việc ngắn nhất trước) trên ba tiến trình "
        "`[24, 3, 3]` đến cùng lúc `t=0`, in đúng 3 dòng:\n"
        "1. `fcfs_waits=0,24,27 avg=17.00`\n2. `sjf_waits=6,0,3 avg=3.00`\n3. `wait_saved=14.00`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L02 duong_dan/bai_cua_ban.py\n```",
        "def waits(order):\n    t = 0; w = []\n    for b in order: w.append(t); t += b\n    return w, sum(w) / len(w)\n"
        "b = [24, 3, 3]\nfw, fa = waits(b)\n"
        "sw = [0] * 3; t = 0\nfor i in sorted(range(3), key=lambda k: b[k]): sw[i] = t; t += b[i]\n"
        "sa = sum(sw) / 3\n"
        "print(f'fcfs_waits={fw[0]},{fw[1]},{fw[2]} avg={fa:.2f}')\n"
        "print(f'sjf_waits={sw[0]},{sw[1]},{sw[2]} avg={sa:.2f}')\n"
        "print(f'wait_saved={fa - sa:.2f}')\n",
    ),
    (
        "L03", "py", "(Mô phỏng định lượng) Round Robin q=4 chia lát đều chống độc chiếm CPU",
        "# Lab OSY L03 (Mô phỏng lập lịch CPU) — Round Robin với lượng tử q = 4\n\n"
        "Viết chương trình Python mô phỏng hàng đợi Round Robin `q = 4` cho ba tiến trình `[24, 3, 3]` "
        "tại `t = 0`, in đúng 3 dòng:\n"
        "1. `rr_waits=6,4,7`\n2. `rr_avg_wait=5.67`\n3. `response_p1_p2_p3=0,4,7`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L03 duong_dan/bai_cua_ban.py\n```",
        "from collections import deque\n"
        "b = [24, 3, 3]; rem = b[:]; fin = [0]*3; resp = [-1]*3; t = 0; q = deque([0,1,2])\n"
        "while q:\n    i = q.popleft()\n    if resp[i] < 0: resp[i] = t\n"
        "    d = min(4, rem[i]); t += d; rem[i] -= d\n"
        "    if rem[i] > 0: q.append(i)\n    else: fin[i] = t\n"
        "w = [fin[i] - b[i] for i in range(3)]\n"
        "print('rr_waits=' + ','.join(map(str, w)))\n"
        "print(f'rr_avg_wait={sum(w)/3:.2f}')\n"
        "print('response_p1_p2_p3=' + ','.join(map(str, resp)))\n",
    ),
    (
        "L04", "py", "(Mô phỏng định lượng) Duyệt mọi xen kẽ đọc-cộng-ghi cho thấy kết quả sai",
        "# Lab OSY L04 (Mô phỏng đồng thời) — Duyệt mọi xen kẽ hai luồng tăng x++\n\n"
        "Viết chương trình Python mô phỏng hai luồng, mỗi luồng thực hiện `x += 1` (gồm 3 bước "
        "`load, inc, store`) `2` lần từ `x = 0`. Duyệt tất cả chuỗi xen kẽ hợp lệ (tổng 12 bước = 6 của mỗi luồng), in đúng 3 dòng:\n"
        "1. `possible_x=2,3,4`\n2. `min_x=2 max_x=4`\n3. `valid_outcomes_lt4=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L04 duong_dan/bai_cua_ban.py\n```",
        "seen = set()\ndef dfs(pc0, pc1, r0, r1, x):\n    if pc0 == 6 and pc1 == 6: seen.add(x); return\n"
        "    for tid, pc in ((0, pc0), (1, pc1)):\n        if pc == 6: continue\n"
        "        op = pc % 3; nr0, nr1, nx = r0, r1, x\n"
        "        if op == 0:\n            if tid == 0: nr0 = x\n            else: nr1 = x\n"
        "        elif op == 1:\n            if tid == 0: nr0 += 1\n            else: nr1 += 1\n"
        "        else: nx = nr0 if tid == 0 else nr1\n"
        "        dfs(pc0 + (tid == 0), pc1 + (tid == 1), nr0, nr1, nx)\n"
        "dfs(0, 0, 0, 0, 0); vals = sorted(seen)\n"
        "print('possible_x=' + ','.join(map(str, vals)))\n"
        "print(f'min_x={vals[0]} max_x={vals[-1]}')\nprint(f'valid_outcomes_lt4={int(any(v < 4 for v in vals))}')\n",
    ),
    (
        "L05", "py", "(Mô phỏng định lượng) Bộ đệm vòng 5 ô với 2 semaphore đếm và 1 mutex",
        "# Lab OSY L05 (Mô phỏng đồng bộ) — Semaphore sản xuất–tiêu thụ trên bộ đệm 5 ô\n\n"
        "Viết chương trình Python mô phỏng bộ đệm `N = 5` bắt đầu `(empty=5, full=0)`: "
        "sản xuất `4` phần tử, tiêu thụ `1` phần tử, rồi sản xuất thêm `2` phần tử, in đúng 3 dòng:\n"
        "1. `init_empty=5 init_full=0`\n2. `after_4p_1c=empty:2,full:3`\n3. `final_state=empty:0,full:5`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L05 duong_dan/bai_cua_ban.py\n```",
        "empty, full = 5, 0\nprint(f'init_empty={empty} init_full={full}')\n"
        "for _ in range(4): empty -= 1; full += 1\nempty += 1; full -= 1\n"
        "print(f'after_4p_1c=empty:{empty},full:{full}')\n"
        "for _ in range(2): empty -= 1; full += 1\n"
        "print(f'final_state=empty:{empty},full:{full}')\n",
    ),
    (
        "L06", "py", "(Mô phỏng định lượng) Phá vòng chờ bằng quy ước lấy khoá số nhỏ trước",
        "# Lab OSY L06 (Mô phỏng bế tắc) — Phát hiện chu trình Coffman và phá thứ tự khóa\n\n"
        "Viết chương trình Python dựng đồ thị chờ giữa `5` triết gia (`0..4`) và `5` chiếc đũa (`0..4`): "
        "khi ai cũng cầm đũa trái trước tạo 1 chu trình độ dài 5, còn khi đánh số và luôn cầm đũa nhỏ trước sẽ phá vòng chờ, in đúng 3 dòng:\n"
        "1. `naive_cycle_len=5`\n2. `ordered_cycle=0`\n3. `coffman_broken=circular_wait`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L06 duong_dan/bai_cua_ban.py\n```",
        "naive = {i: (i + 1) % 5 for i in range(5)}\n"
        "cur, seen = 0, []\nwhile cur not in seen: seen.append(cur); cur = naive[cur]\n"
        "edges_ord = [(min(i, (i + 1) % 5), max(i, (i + 1) % 5)) for i in range(5)]\n"
        "has_cycle = any(a >= b for a, b in edges_ord)\n"
        "print(f'naive_cycle_len={len(seen)}')\n"
        "print(f'ordered_cycle={int(has_cycle)}')\n"
        "print(f'coffman_broken={\"circular_wait\" if not has_cycle else \"none\"}')\n",
    ),
    (
        "L07", "py", "(Mô phỏng định lượng) Thuật toán Nhà băng kiểm tra trạng thái an toàn",
        "# Lab OSY L07 (Mô phỏng tránh bế tắc) — Thuật toán Nhà băng trên 5 tiến trình\n\n"
        "Viết chương trình Python chạy thuật toán Nhà băng với `Available = [3, 3, 2]`, "
        "`Alloc` và `Max` chuẩn 5 tiến trình `P0..P4`, tìm thứ tự an toàn đầu tiên, in đúng 3 dòng:\n"
        "1. `safe=1`\n2. `safe_seq=P1,P3,P0,P2,P4`\n3. `final_avail=10,5,7`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L07 duong_dan/bai_cua_ban.py\n```",
        "alloc = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]\n"
        "mx = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]\n"
        "need = [[mx[i][j]-alloc[i][j] for j in range(3)] for i in range(5)]\n"
        "work = [3,3,2]; fin = [False]*5; seq = []\n"
        "while len(seq) < 5:\n    for i in range(5):\n"
        "        if not fin[i] and all(need[i][j] <= work[j] for j in range(3)):\n"
        "            work = [work[j]+alloc[i][j] for j in range(3)]; fin[i] = True; seq.append(f'P{i}'); break\n"
        "print(f'safe={int(all(fin))}')\nprint('safe_seq=' + ','.join(seq))\nprint('final_avail=' + ','.join(map(str, work)))\n",
    ),
    (
        "L08", "py", "(Mô phỏng định lượng) So sánh First-Fit và Best-Fit trên danh sách lỗ trống",
        "# Lab OSY L08 (Mô phỏng cấp phát bộ nhớ) — First-Fit vs Best-Fit\n\n"
        "Viết chương trình Python mô phỏng cấp phát các yêu cầu `[212, 417, 112, 426]` vào danh sách "
        "lỗ trống `[100, 500, 200, 300, 600]`, in đúng 3 dòng:\n"
        "1. `first_fit_placed=3 failed=426`\n2. `best_fit_placed=4 failed=none`\n3. `best_fit_free_total=533`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L08 duong_dan/bai_cua_ban.py\n```",
        "holes0 = [100, 500, 200, 300, 600]; reqs = [212, 417, 112, 426]\n"
        "def sim(best=False):\n    h = holes0[:]; fail = []\n"
        "    for r in reqs:\n        cands = [i for i, v in enumerate(h) if v >= r]\n"
        "        if not cands: fail.append(r); continue\n"
        "        idx = min(cands, key=lambda i: h[i]) if best else cands[0]\n"
        "        h[idx] -= r\n    return len(reqs) - len(fail), fail, sum(h)\n"
        "fp, ff, _ = sim(False); bp, bf, bf_sum = sim(True)\n"
        "print(f'first_fit_placed={fp} failed=' + (','.join(map(str, ff)) or 'none'))\n"
        "print(f'best_fit_placed={bp} failed=' + (','.join(map(str, bf)) or 'none'))\n"
        "print(f'best_fit_free_total={bf_sum}')\n",
    ),
    (
        "L09", "py", "(Mô phỏng định lượng) Trang 4 KiB: dịch số trang ảo VPN và độ dời offset sang địa chỉ vật lý",
        "# Lab OSY L09 (Mô phỏng phân trang) — Dịch địa chỉ ảo (VPN + offset) và thời gian truy cập hiệu dụng EAT với TLB\n\n"
        "Viết chương trình Python cho trang `4 KiB` (`4 096 B`), bảng trang `{0: 5, 1: 2, 2: 9, 3: 7}`, "
        "dịch địa chỉ `0x3A7F` và tính EAT khi `TLB=20 ns`, `RAM=100 ns`, `TLB hit=90%`, in đúng 3 dòng:\n"
        "1. `va=0x3A7F vpn=3 offset=0xA7F`\n2. `pa=0x7A7F`\n3. `eat_ns=130.0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L09 duong_dan/bai_cua_ban.py\n```",
        "pt = {0: 5, 1: 2, 2: 9, 3: 7}\nva = 0x3A7F; vpn, off = va >> 12, va & 0xFFF\n"
        "pa = (pt[vpn] << 12) | off\neat = 0.9 * (20 + 100) + 0.1 * (20 + 100 + 100)\n"
        "print(f'va=0x{va:04X} vpn={vpn} offset=0x{off:03X}')\n"
        "print(f'pa=0x{pa:04X}')\nprint(f'eat_ns={eat:.1f}')\n",
    ),
    (
        "L10", "py", "(Mô phỏng định lượng) Nghịch lý Belady với FIFO, LRU và OPT",
        "# Lab OSY L10 (Mô phỏng thay trang) — Kiểm chứng nghịch lý Belady trên chuỗi kinh điển\n\n"
        "Viết chương trình Python mô phỏng chuỗi `[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]` "
        "bằng FIFO 3 khung, FIFO 4 khung, LRU 3 khung và OPT 3 khung, in đúng 3 dòng:\n"
        "1. `fifo_3=9 fifo_4=10 belady=1`\n2. `lru_3=10`\n3. `opt_3=7`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L10 duong_dan/bai_cua_ban.py\n```",
        "seq = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]\n"
        "def run(cap, alg):\n    f = []; pf = 0\n    for i, p in enumerate(seq):\n"
        "        if p in f:\n            if alg == 'lru': f.remove(p); f.append(p)\n            continue\n"
        "        pf += 1\n        if len(f) == cap:\n"
        "            if alg in ('fifo', 'lru'): f.pop(0)\n"
        "            else: f.remove(max(f, key=lambda x: seq.index(x, i+1) if x in seq[i+1:] else 999))\n"
        "        f.append(p)\n    return pf\n"
        "f3, f4 = run(3, 'fifo'), run(4, 'fifo')\n"
        "print(f'fifo_3={f3} fifo_4={f4} belady={int(f4 > f3)}')\n"
        "print(f'lru_3={run(3, \"lru\")}')\nprint(f'opt_3={run(3, \"opt\")}')\n",
    ),
    (
        "L11", "py", "(Mô phỏng định lượng) Tổng tập làm việc > số khung gây trì trệ (thrashing)",
        "# Lab OSY L11 (Mô phỏng tập làm việc) — Phát hiện và chặn hiện tượng trì trệ\n\n"
        "Viết chương trình Python kiểm tra hệ thống `1 000` khung vật lý khi `4` tiến trình "
        "mỗi tiến trình cần `300` trang (`D = 1200 > 1000`), và sau khi tạm dừng 1 tiến trình (`900 <= 1000`), in đúng 3 dòng:\n"
        "1. `demand_4procs=1200 thrashing=1`\n2. `demand_after_suspend=900 thrashing=0`\n3. `free_frames_after=100`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L11 duong_dan/bai_cua_ban.py\n```",
        "cap, per = 1000, 300\nd4 = 4 * per; d3 = 3 * per\n"
        "print(f'demand_4procs={d4} thrashing={int(d4 > cap)}')\n"
        "print(f'demand_after_suspend={d3} thrashing={int(d3 > cap)}')\n"
        "print(f'free_frames_after={cap - d3}')\n",
    ),
    (
        "L12", "py", "(Mô phỏng định lượng) Kích thước tối đa của tệp qua các cấp chỉ mục inode",
        "# Lab OSY L12 (Mô phỏng inode) — Tính sức chứa tối đa của cấu trúc chỉ mục Unix\n\n"
        "Viết chương trình Python tính số khối và dung lượng MiB/GiB cho khối `4 KiB` (`4 096 B`), "
        "con trỏ khối `4 B` (`1 024` con trỏ/khối), với 12 trực tiếp + 1 gián tiếp cấp 1 + 1 cấp 2, in đúng 3 dòng:\n"
        "1. `direct_kib=48`\n2. `single_ind_blocks=1024`\n3. `double_ind_mib=4096`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L12 duong_dan/bai_cua_ban.py\n```",
        "blk, ptr = 4096, 4; fan = blk // ptr\n"
        "d_kib = (12 * blk) // 1024\n"
        "s_blk = fan\nd_mib = (fan * fan * blk) // (1024 * 1024)\n"
        "print(f'direct_kib={d_kib}')\n"
        "print(f'single_ind_blocks={s_blk}')\n"
        "print(f'double_ind_mib={d_mib}')\n",
    ),
    (
        "L13", "py", "(Mô phỏng định lượng) So sánh quãng đường đầu đọc FCFS và SSTF",
        "# Lab OSY L13 (Mô phỏng lập lịch đĩa) — So sánh quãng đường FCFS vs SSTF\n\n"
        "Viết chương trình Python tính tổng quãng đường đầu đọc bắt đầu ở trụ `53` với hàng đợi "
        "`[98, 183, 37, 122, 14, 124, 65, 67]` theo FCFS và SSTF, in đúng 3 dòng:\n"
        "1. `fcfs_tracks=640`\n2. `sstf_tracks=236`\n3. `saved_pct=63.1%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L13 duong_dan/bai_cua_ban.py\n```",
        "q = [98, 183, 37, 122, 14, 124, 65, 67]\nfcfs = sum(abs(a - b) for a, b in zip([53] + q, q))\n"
        "rem = q[:]; cur = 53; sstf = 0\n"
        "while rem: nxt = min(rem, key=lambda x: abs(x - cur)); sstf += abs(nxt - cur); cur = nxt; rem.remove(nxt)\n"
        "print(f'fcfs_tracks={fcfs}')\nprint(f'sstf_tracks={sstf}')\nprint(f'saved_pct={100 * (fcfs - sstf) / fcfs:.1f}%')\n",
    ),
    (
        "L14", "py", "(Mô phỏng định lượng) Giải mã bit quyền rwxr-x--- thành bát phân 750",
        "# Lab OSY L14 (Mô phỏng phân quyền) — Đổi chuỗi rwx 9 ký tự sang bát phân\n\n"
        "Viết chương trình Python chuyển chuỗi quyền `'rwxr-x---'` sang bát phân và kiểm tra "
        "`750` có cho nhóm đọc/vào thư mục nhưng chặn người ngoài hoàn toàn không, in đúng 3 dòng:\n"
        "1. `octal_rwxr_x___=750`\n2. `octal_rw_r__r__=644`\n3. `group_can_enter=1 other_denied=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L14 duong_dan/bai_cua_ban.py\n```",
        "def to_oct(s):\n    v = [4*(s[i]=='r') + 2*(s[i+1]=='w') + 1*(s[i+2]=='x') for i in (0,3,6)]\n    return ''.join(map(str, v))\n"
        "a, b = to_oct('rwxr-x---'), to_oct('rw-r--r--')\n"
        "print(f'octal_rwxr_x___={a}')\nprint(f'octal_rw_r__r__={b}')\n"
        "print(f'group_can_enter={int(int(a[1]) & 1 == 1)} other_denied={int(a[2] == \"0\")}')\n",
    ),
    (
        "L15", "py", "(Mô phỏng định lượng) Lịch sử bộ lập lịch Linux: O(1), CFS và EEVDF",
        "# Lab OSY L15 (Mô phỏng bộ lập lịch Linux) — Đối chiếu O(n) vs CFS vs EEVDF\n\n"
        "Viết chương trình Python mô phỏng tỉ trọng CPU giữa hai tác vụ trọng số `2048` và `1024` trong CFS, "
        "lượt duyệt của bộ lập lịch O(n) `1 000` tiến trình × `1 000` Hz, và lát cắt EEVDF `3 ms` vs `9 ms` trong chu kỳ `36 ms`, in đúng 3 dòng:\n"
        "1. `on_checks_per_sec=1000000`\n2. `cfs_share_2048_vs_1024=66.7%,33.3%`\n3. `eevdf_ms_36ms=18,18 first=A`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh OSY L15 duong_dan/bai_cua_ban.py\n```",
        "checks = 1000 * 1000\nw1, w2 = 2048, 1024; tot = w1 + w2\n"
        "ran, v, first = {'A': 0, 'B': 0}, {'A': 0, 'B': 0}, None\n"
        "slices = {'A': 3, 'B': 9}\n"
        "while sum(ran.values()) < 36:\n"
        "    pick = 'A' if (v['A'] + slices['A']) <= (v['B'] + slices['B']) else 'B'\n"
        "    if first is None: first = pick\n"
        "    d = min(slices[pick], 36 - sum(ran.values()))\n"
        "    ran[pick] += d; v[pick] += d\n"
        "print(f'on_checks_per_sec={checks}')\n"
        "print(f'cfs_share_2048_vs_1024={100*w1/tot:.1f}%,{100*w2/tot:.1f}%')\n"
        "print(f'eevdf_ms_36ms={ran[\"A\"]},{ran[\"B\"]} first={first}')\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    if lid == "L15":
        cov = [(1, "stage1"), (2, "check"), (3, "practice")]
    elif lid == "L09":
        cov = [(1, "example"), (2, "verify"), (3, "example"), (4, "practice")]
    elif lid == "L06":
        cov = [(1, "graph"), (2, "verify"), (3, "practice")]
    else:
        cov = [(1, "example"), (2, "verify"), (3, "practice")]
    fp, lo = up.apply_upgrade(
        "OSY", lid,
        de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov,
    )
    print(f"OK OSY {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("OSY", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")

tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "osy", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl OSY:", tpl.stdout.strip() or tpl.stderr.strip())
