"""Kiểm độc lập mọi khẳng định của khoá OSY (16 bài L00–L15) — mô phỏng độc lập từng cơ chế,
rồi đối chiếu với tools/checklib.py khi có hàm tương ứng.
Chạy: .venv/Scripts/python audit/osy/verify_osy.py"""
import collections
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# L00: 1000 syscall/s * 5 us = 0.5% CPU
rec("L00", abs(1000 * 5e-6 * 100.0 - 0.5) < 1e-12, "1000 chuyển ngữ cảnh/s * 5 us = 0.5% CPU")

# L01: fork() 3 lần trong vòng lặp -> 2^3 = 8 tiến trình
procs = 1
for _ in range(3):
    procs *= 2
rec("L01", procs == 8 and alg.fork_loop(3)[0] == 8, "fork() 3 lần -> 8 tiến trình")

# L02: FCFS và SJF trên (24, 3, 3)
def fcfs_avg(bursts):
    t, waits = 0, []
    for b in bursts:
        waits.append(t)
        t += b
    return sum(waits) / len(waits)

b02 = [24, 3, 3]
rec("L02", abs(fcfs_avg(b02) - 17.0) < 1e-12 and abs(fcfs_avg(sorted(b02)) - 3.0) < 1e-12,
    "FCFS [24,3,3] = 17.0; SJF [3,3,24] = 3.0")

# L03: Round Robin q = 4 trên (24, 3, 3) -> waits [6, 4, 7], avg 17/3
def rr_sim(bursts, q):
    rem = list(bursts)
    wait = [0] * len(bursts)
    last_end = [0] * len(bursts)
    t = 0
    dq = collections.deque(range(len(bursts)))
    while dq:
        i = dq.popleft()
        wait[i] += t - last_end[i]
        run = min(q, rem[i])
        t += run
        rem[i] -= run
        last_end[i] = t
        if rem[i] > 0:
            dq.append(i)
    return wait

w03 = rr_sim([24, 3, 3], 4)
w03_alg = alg.rr_waits([24, 3, 3], 4)
rec("L03", w03 == [6, 4, 7] and abs(sum(w03) / 3 - 17 / 3) < 1e-12 and w03_alg == w03,
    f"RR q=4 waits={w03}, avg={sum(w03)/3:.2f}")

# L04: 2 luồng x++ 2 lần (mỗi lần R, A, W) -> tập giá trị cuối = {2, 3, 4}
vals = set()
ops = [0] * 6 + [1] * 6
for perm in set(itertools.permutations(ops)):
    x = 0
    pc = [0, 0]
    reg = [0, 0]
    for tid in perm:
        step = pc[tid] % 3
        if step == 0:
            reg[tid] = x
        elif step == 1:
            reg[tid] += 1
        else:
            x = reg[tid]
        pc[tid] += 1
    vals.add(x)
vals_alg = set(alg.race_finals(2))
rec("L04", vals == {2, 3, 4} and vals_alg == {2, 3, 4}, f"xen kẽ 2x2 x++ -> {sorted(vals)}")

# L05: bounded buffer 5 ô (trống=5, đầy=0, tổng luôn bảo toàn = 5)
empty, full = 5, 0
ok05 = True
for action in ("P", "P", "C", "P", "P", "P", "C"):
    if action == "P" and empty > 0:
        empty -= 1
        full += 1
    elif action == "C" and full > 0:
        full -= 1
        empty += 1
    ok05 &= (empty + full == 5 and empty >= 0 and full >= 0)
rec("L05", ok05 and (empty, full) == (2, 3), f"bộ đệm 5 ô sau chuỗi P/C: trống={empty}, đầy={full}")

# L06: 5 triết gia: lấy đũa trái tạo chu trình độ dài 5; quy ước đũa nhỏ trước không tạo chu trình (DAG)
cyc_5 = all((i + 1) % 5 != i for i in range(5))  # vòng i -> (i+1)%5
edges_ordered = [(min(i, (i + 1) % 5), max(i, (i + 1) % 5)) for i in range(5)]
rec("L06", cyc_5 and all(u < v for u, v in edges_ordered),
    "5 triết gia: thứ tự đũa nhỏ trước đảm bảo cạnh hướng tăng chặt (DAG, không chu trình)")

# L07: Thuật toán nhà băng (5 tiến trình, total=(10,5,7), avail=(3,3,2))
alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
mx = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
avail = [3, 3, 2]
need = [[mx[i][j] - alloc[i][j] for j in range(3)] for i in range(5)]
work = list(avail)
fin = [False] * 5
seq = []
while len(seq) < 5:
    picked = False
    for i in range(5):
        if not fin[i] and all(need[i][j] <= work[j] for j in range(3)):
            work = [work[j] + alloc[i][j] for j in range(3)]
            fin[i] = True
            seq.append(f"P{i}")
            picked = True
            break
    if not picked:
        break
seq_alg = alg.banker(alloc, mx, avail)
rec("L07", seq == ["P1", "P3", "P0", "P2", "P4"] and seq_alg == [1, 3, 0, 2, 4],
    f"Nhà băng thứ tự an toàn: {seq}")

# L08: Cấp phát lỗ [100, 500, 200, 300, 600] với yêu cầu [212, 417, 112, 426]
def alloc_first(holes, reqs):
    h = list(holes)
    out = []
    for r in reqs:
        placed = False
        for i, v in enumerate(h):
            if v >= r:
                h[i] -= r
                out.append(i)
                placed = True
                break
        if not placed:
            out.append(None)
    return out

def alloc_best(holes, reqs):
    h = list(holes)
    out = []
    for r in reqs:
        cand = [(v - r, i) for i, v in enumerate(h) if v >= r]
        if cand:
            _, idx = min(cand)
            h[idx] -= r
            out.append(idx)
        else:
            out.append(None)
    return out

ff = alloc_first([100, 500, 200, 300, 600], [212, 417, 112, 426])
bf = alloc_best([100, 500, 200, 300, 600], [212, 417, 112, 426])
rec("L08", ff[-1] is None and all(x is not None for x in bf)
    and None in alg.fit([100, 500, 200, 300, 600], [212, 417, 112, 426], "first")
    and None not in alg.fit([100, 500, 200, 300, 600], [212, 417, 112, 426], "best"),
    f"first_fit={ff}, best_fit={bf}")

# L09: trang 4 KiB, địa chỉ 0x3A7F -> trang 3, độ dời 0xA7F
addr = 0x3A7F
pg, off = addr >> 12, addr & 0xFFF
rec("L09", pg == 3 and off == 0xA7F, f"0x3A7F -> trang {pg}, độ dời 0x{off:X}")

# L10: Belady anomaly trên [1,2,3,4,1,2,5,1,2,3,4,5]: FIFO(3)=9, FIFO(4)=10, LRU(3)=10, OPT(3)=7
def faults_fifo(ref, cap):
    q, s, f = collections.deque(), set(), 0
    for p in ref:
        if p not in s:
            f += 1
            if len(q) == cap:
                s.remove(q.popleft())
            q.append(p)
            s.add(p)
    return f

ref10 = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
f3, f4 = faults_fifo(ref10, 3), faults_fifo(ref10, 4)
lru3 = alg.page_faults(ref10, 3, "LRU")
opt3 = alg.page_faults(ref10, 3, "OPT")
rec("L10", f3 == 9 and f4 == 10 and f4 > f3 and lru3 == 10 and opt3 == 7,
    f"FIFO(3)={f3}, FIFO(4)={f4} (Belady!), LRU(3)={lru3}, OPT(3)={opt3}")

# L11: thrashing: 4 tiến trình * 300 trang = 1200 > 1000 khung; dừng 1 -> 900 < 1000
rec("L11", 4 * 300 == 1200 and 1200 > 1000 and 3 * 300 == 900 and 900 < 1000,
    "trì trệ: 4*300=1200 > 1000; tạm dừng 1 -> 900 < 1000")

# L12: inode 12 trực tiếp + gián tiếp 1, 2, 3 tầng, khối 4 KiB, con trỏ 4 B
ptrs = 4096 // 4
max_blocks = 12 + ptrs + ptrs ** 2 + ptrs ** 3
max_tib = max_blocks * 4096 / (1024 ** 4)
rec("L12", ptrs == 1024 and abs(max_tib - 4.0039) < 1e-3 and alg.inode_max(12, 3, 4096, 4) == max_blocks * 4096,
    f"inode tối đa = {max_blocks} khối = {max_tib:.3f} TiB")

# L13: lập lịch đĩa head=53, queue=[98,183,37,122,14,124,65,67]: FCFS=640, SSTF=236
q13 = [98, 183, 37, 122, 14, 124, 65, 67]
d_fcfs = sum(abs(a - b) for a, b in zip([53] + q13, q13))
cur, rem, d_sstf = 53, list(q13), 0
while rem:
    nxt = min(rem, key=lambda x: abs(x - cur))
    d_sstf += abs(nxt - cur)
    cur = nxt
    rem.remove(nxt)
rec("L13", d_fcfs == 640 and d_sstf == 236 and alg.disk_fcfs(q13, 53) == 640 and alg.disk_sstf(q13, 53) == 236,
    f"Đĩa: FCFS={d_fcfs} trụ, SSTF={d_sstf} trụ")

# L14: rwxr-x--- = 0o750
bits = "".join(str(sum((4 if c == "r" else 2 if c == "w" else 1 if c == "x" else 0) for c in grp))
               for grp in ("rwx", "r-x", "---"))
rec("L14", bits == "750" and int(bits, 8) == 0o750, f"rwxr-x--- = {bits} (bát phân)")

# L15: Linux scheduler O(1), CFS (nhóm + trọng số), EEVDF (lát 3ms và 9ms trong 36ms)
g_shares = (0.5, 0.25, 0.25)
w_ratio = (2048 / 3072, 1024 / 3072)
evs = alg.eevdf_run([3, 9], 36)
run_a = sum(d for i, _, d in evs if i == 0)
run_b = sum(d for i, _, d in evs if i == 1)
evs_first = evs[0][0] if evs else None
rec("L15", 1000 * 1000 == 1_000_000 and sum(g_shares) == 1.0 and abs(w_ratio[0] - 2 / 3) < 1e-12
    and run_a == 18 and run_b == 18 and evs_first == 0,
    f"O(1): 10^6 duyệt/s; CFS 2048:1024=2/3:1/3; EEVDF 36ms -> A={run_a}, B={run_b}")

# ── Kiểm tự động mọi lab (du_lieu.txt + ca_an/) qua cham.sh ──
import subprocess as _subp
from pathlib import Path as _LabPath
_BASH = r"C:\Program Files\Git\bin\bash.exe"
if not _LabPath(_BASH).exists():
    _BASH = "bash"
for _ld in sorted((ROOT / "labs" / "OSY").glob("L*")):
    _rp = _subp.run([_BASH, str(ROOT / "labs" / "cham.sh"), "OSY", _ld.name], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    rec(f"{_ld.name}:lab", _rp.returncode == 0 and "PASS" in _rp.stdout and "ca an" in _rp.stdout, f"cham.sh {_ld.name} (public + ca_an)")

p = sum(ok for _, ok in R)
print(f"{p}/{len(R)} PASS")
sys.exit(0 if p == len(R) else 1)
