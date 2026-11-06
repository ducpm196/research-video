"""Thuật toán tham chiếu cho `checks` của bài giảng (dùng trong biểu thức check dưới tên `alg`, xem lv._check_namespace).
Mỗi hàm trả về cả các bước trung gian để check được mọi con số trên bảng (vết phân hoạch, bảng d theo vòng…), không chỉ đáp án.
Được đối chiếu độc lập bằng vét cạn trong audit/cs112/verify_cs112_p2.py (mục X1) — sửa file này phải chạy lại script đó."""
import heapq
import itertools
import math
import random
from fractions import Fraction


# ── sắp xếp ──
def partition(a, lo=0, hi=None):
    """Phân hoạch Lomuto, chốt = a[hi], so sánh a[j] <= chốt. Sửa a tại chỗ.
    Trả (vị trí chốt, số phép so sánh, vết) — vết[k] = (j, a[j] lúc xét, có ≤ chốt?, mảng sau bước)."""
    hi = len(a) - 1 if hi is None else hi
    p, i, c, trace = a[hi], lo - 1, 0, []
    for j in range(lo, hi):
        c += 1
        x = a[j]
        if x <= p:
            i += 1
            a[i], a[j] = a[j], a[i]
        trace.append((j, x, x <= p, list(a)))
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1, c, trace


def quicksort(a, lo=0, hi=None):
    """Sắp xếp nhanh (chốt cuối, Lomuto) tại chỗ; trả tổng số phép so sánh."""
    hi = len(a) - 1 if hi is None else hi
    if lo >= hi:
        return 0
    q, c, _ = partition(a, lo, hi)
    return c + quicksort(a, lo, q - 1) + quicksort(a, q + 1, hi)


def qs_count(xs):
    return quicksort(list(xs))


def counting_sort(keys, k):
    cnt = [0] * (k + 1)
    for x in keys:
        cnt[x] += 1
    start = list(itertools.accumulate([0] + cnt[:-1]))
    out = [v for v in range(k + 1) for _ in range(cnt[v])]
    return cnt, start, out


# ── đường đi ngắn nhất ──
def dijkstra(g, s):
    """g: {u: {v: w}}. Trả (d cuối, [(đỉnh chốt, d lúc chốt)], [ảnh d sau mỗi lần chốt])."""
    d = {v: math.inf for v in g}
    d[s] = 0
    done, order, snaps = set(), [], []
    while len(done) < len(g):
        u = min((v for v in g if v not in done), key=lambda v: (d[v], v))
        if d[u] == math.inf:
            break
        done.add(u)
        order.append((u, d[u]))
        for v, w in g[u].items():
            if v not in done and d[u] + w < d[v]:
                d[v] = d[u] + w
        snaps.append(dict(d))
    return d, order, snaps


def bellman_ford(vs, edges, s):
    """edges: [(u, v, w)] theo thứ tự nới. Trả (d, [ảnh d sau mỗi vòng], còn giảm được ở vòng thứ n?)."""
    d = {v: math.inf for v in vs}
    d[s] = 0
    rounds = []
    for _ in range(len(vs) - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
        rounds.append(dict(d))
    return d, rounds, any(d[u] + w < d[v] for u, v, w in edges)


def shortest_brute(g, s, t):
    best = math.inf

    def go(u, cost, seen):
        nonlocal best
        if u == t:
            best = min(best, cost)
            return
        for v, w in g[u].items():
            if v not in seen:
                go(v, cost + w, seen | {v})
    go(s, 0, {s})
    return best


# ── cây khung nhỏ nhất ──
class DSU:
    """Hợp–tìm: hợp theo kích thước, nén đường đi trọn vẹn khi tìm."""
    def __init__(self, vs):
        self.p = {v: v for v in vs}
        self.sz = {v: 1 for v in vs}

    def find(self, x):
        """Đi lên gốc, rồi cho mọi nút trên đường trỏ thẳng về gốc (nén đường đi trọn vẹn)."""
        r = x
        while self.p[r] != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        return True


def kruskal(vs, edges):
    """Trả ([(u+v, w, có lấy?)] theo thứ tự xét, tổng trọng số cây)."""
    dsu, trace, tot = DSU(vs), [], 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ok = dsu.union(u, v)
        trace.append((u + v, w, ok))
        tot += w if ok else 0
    return trace, tot


def prim(vs, edges, s):
    """Trả [(cạnh theo thứ tự thêm, w)]."""
    adj = {v: [] for v in vs}
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    inT, pq, order = {s}, [(w, s, v) for w, v in adj[s]], []
    heapq.heapify(pq)
    while pq and len(inT) < len(vs):
        w, u, v = heapq.heappop(pq)
        if v in inT:
            continue
        inT.add(v)
        order.append((u + v, w))
        for w2, x in adj[v]:
            if x not in inT:
                heapq.heappush(pq, (w2, v, x))
    return order


def mst_brute(vs, edges):
    """Tổng nhỏ nhất trên mọi bộ n − 1 cạnh không tạo chu trình, và số bộ đạt được."""
    best, cnt = math.inf, 0
    for S in itertools.combinations(edges, len(vs) - 1):
        d = DSU(vs)
        if all(d.union(u, v) for u, v, _ in S):
            t = sum(e[2] for e in S)
            if t < best:
                best, cnt = t, 1
            elif t == best:
                cnt += 1
    return best, cnt


def run_asm(prog, regs=None, limit=100000):
    """Máy tập lệnh tí hon cho CSA L07–L09 (kiểu RISC, 3 toán hạng). prog: danh sách (nhãn hoặc None, lệnh, *toán hạng):
    li rd, k | add rd, ra, rb | addi rd, ra, k | ble ra, rb, nhãn | j nhãn. Trả về (thanh ghi, số lệnh đã chạy, dãy tên lệnh đã chạy)."""
    r = dict(regs or {})
    labels = {ins[0]: i for i, ins in enumerate(prog) if ins[0]}
    pc, n, trace = 0, 0, []
    while pc < len(prog) and n < limit:
        _, op, *a = prog[pc]
        n += 1; trace.append(op); pc += 1
        if op == "li":
            r[a[0]] = a[1]
        elif op == "add":
            r[a[0]] = r.get(a[1], 0) + r.get(a[2], 0)
        elif op == "addi":
            r[a[0]] = r.get(a[1], 0) + a[2]
        elif op == "ble":
            if r.get(a[0], 0) <= r.get(a[1], 0):
                pc = labels[a[2]]
        elif op == "j":
            pc = labels[a[0]]
        else:
            raise ValueError(op)
    return r, n, trace


SUM_1_TO_10 = [(None, "li", "r1", 0), (None, "li", "r2", 1), (None, "li", "r3", 10),
               ("lap", "add", "r1", "r1", "r2"), (None, "addi", "r2", "r2", 1), (None, "ble", "r2", "r3", "lap")]


def cache_hits(blocks, sets, ways):
    """Mô phỏng bộ nhớ đệm kết hợp theo tập, thay thế LRU, trên dãy SỐ KHỐI. ways = 1 là ánh xạ trực tiếp.
    Trả về số lần trúng (CSA L10–L12)."""
    cache = [[] for _ in range(sets)]
    hits = 0
    for b in blocks:
        s = cache[b % sets]
        if b in s:
            hits += 1; s.remove(b)
        elif len(s) == ways:
            s.pop(0)
        s.append(b)                      # cuối danh sách = mới dùng nhất
    return hits


def addr_blocks(addrs, line):
    return [a // line for a in addrs]


# ───────── Hệ điều hành (OSY): mô phỏng dùng trong checks — mỗi hàm trả về con số đưa lên màn hình ─────────
def sched_waits(bursts):
    """Đến trước phục vụ trước (mọi tiến trình đến lúc 0, theo thứ tự danh sách): thời gian chờ của từng tiến trình."""
    t, w = 0, []
    for b in bursts:
        w.append(t); t += b
    return w


def rr_waits(bursts, q):
    """Xoay vòng lượng tử q (mọi tiến trình đến lúc 0): thời gian chờ = hoàn thành − thời gian chạy."""
    rem, t, fin, queue = list(bursts), 0, [0] * len(bursts), list(range(len(bursts)))
    while queue:
        i = queue.pop(0); run = min(q, rem[i]); t += run; rem[i] -= run
        if rem[i]:
            queue.append(i)
        else:
            fin[i] = t
    return [fin[i] - bursts[i] for i in range(len(bursts))]


def goodness_scan(n_ready, cpus=1):
    """Bộ lập lịch kiểu 2.4 (OSY L15): mỗi lần chọn, MỘT hàng đợi chung, duyệt hết n_ready tiến trình → số phép so sánh mỗi lần chọn
    (n_ready − 1) và số CPU phải chờ khoá chung khi mọi CPU cùng chọn một lúc (cpus − 1)."""
    return n_ready - 1, cpus - 1


def cfs_run(weights, quantum, rounds):
    """CFS rút gọn (OSY L15): luôn chạy tác vụ có thời gian chạy ảo nhỏ nhất (hoà → chỉ số nhỏ), mỗi lượt chạy `quantum`;
    thời gian ảo tăng quantum · 1024 / trọng số. Trả (thứ tự chạy, thời gian chạy thật của từng tác vụ)."""
    vr, run, order = [0.0] * len(weights), [0] * len(weights), []
    for _ in range(rounds):
        i = min(range(len(weights)), key=lambda k: (vr[k], k))
        order.append(i); run[i] += quantum; vr[i] += quantum * 1024 / weights[i]
    return order, run


def cfs_groups(groups, quantum, rounds, gweights=None):
    """Lập lịch theo nhóm (OSY L15): chọn NHÓM có thời gian ảo nhỏ nhất, rồi chọn tác vụ có thời gian ảo nhỏ nhất trong nhóm đó.
    groups = số tác vụ của từng nhóm; trả thời gian chạy thật của từng tác vụ, theo nhóm."""
    gw = gweights or [1024] * len(groups)
    gv, tv, run = [0.0] * len(groups), [[0.0] * n for n in groups], [[0] * n for n in groups]
    for _ in range(rounds):
        g = min(range(len(groups)), key=lambda k: (gv[k], k))
        t = min(range(groups[g]), key=lambda k: (tv[g][k], k))
        run[g][t] += quantum; gv[g] += quantum * 1024 / gw[g]; tv[g][t] += quantum
    return run


def eevdf_run(slices, total):
    """EEVDF rút gọn (OSY L15), mọi tác vụ cùng trọng số, đều sẵn sàng từ lúc 0: trễ (lag) = trung bình thời gian ảo − thời gian ảo của
    tác vụ; đủ điều kiện khi trễ ≥ 0; hạn chót ảo = thời gian ảo + lát; chọn tác vụ đủ điều kiện có hạn chót sớm nhất (hoà → chỉ số nhỏ),
    chạy trọn một lát. Trả danh sách (tác vụ, lúc bắt đầu, độ dài) tới khi đủ `total`."""
    vr, t, log = [0] * len(slices), 0, []
    while t < total:
        avg = sum(vr) / len(vr)
        ok = [k for k in range(len(slices)) if avg - vr[k] >= 0]
        i = min(ok, key=lambda k: (vr[k] + slices[k], k))
        d = min(slices[i], total - t)
        log.append((i, t, d)); vr[i] += d; t += d
    return log


def _interleavings(a, b):
    if not a:
        yield list(b); return
    if not b:
        yield list(a); return
    for r in _interleavings(a[1:], b):
        yield [a[0]] + r
    for r in _interleavings(a, b[1:]):
        yield [b[0]] + r


def race_finals(times=2):
    """Hai luồng A, B, mỗi luồng chạy x++ `times` lần (đọc–cộng–ghi), x ban đầu 0: tập mọi giá trị cuối qua MỌI cách xen kẽ."""
    ops = lambda t: [(t, k) for k in ("load", "add", "store") * times]
    finals = set()
    for seq in _interleavings(ops("A"), ops("B")):
        x, reg = 0, {"A": 0, "B": 0}
        for t, k in seq:
            if k == "load": reg[t] = x
            elif k == "add": reg[t] += 1
            else: x = reg[t]
        finals.add(x)
    return finals


def banker(alloc, mx, avail):
    """Thuật toán nhà băng: trả về một thứ tự an toàn (chỉ số tiến trình), hoặc None nếu không an toàn."""
    n = len(alloc)
    need = [[m - a for m, a in zip(mx[i], alloc[i])] for i in range(n)]
    work, done, seq = list(avail), [False] * n, []
    while len(seq) < n:
        for i in range(n):
            if not done[i] and all(x <= w for x, w in zip(need[i], work)):
                work = [w + a for w, a in zip(work, alloc[i])]; done[i] = True; seq.append(i); break
        else:
            return None
    return seq


def fit(holes, req, how):
    """Cấp phát liên tục: how = 'first' (vừa đầu tiên) hoặc 'best' (vừa nhất). Trả về chỉ số lỗ cho từng yêu cầu (None = không đặt được)."""
    h, out = list(holes), []
    for r in req:
        c = [i for i in range(len(h)) if h[i] >= r]
        if not c:
            out.append(None); continue
        i = c[0] if how == "first" else min(c, key=lambda k: h[k])
        out.append(i); h[i] -= r
    return out


def page_faults(ref, frames, policy):
    """Số lỗi trang với policy ∈ {'FIFO', 'LRU', 'OPT'}."""
    mem, f = [], 0
    for i, p in enumerate(ref):
        if p in mem:
            if policy == "LRU":
                mem.remove(p); mem.append(p)
            continue
        f += 1
        if len(mem) == frames:
            if policy == "OPT":
                fut = ref[i + 1:]
                mem.remove(max(mem, key=lambda q: fut.index(q) if q in fut else 10 ** 9))
            else:
                mem.pop(0)
        mem.append(p)
    return f


def disk_fcfs(queue, head):
    return sum(abs(b - a) for a, b in zip([head] + list(queue), queue))


def disk_sstf(queue, head):
    q, t = list(queue), 0
    while q:
        n = min(q, key=lambda x: abs(x - head)); t += abs(n - head); head = n; q.remove(n)
    return t


def rr_response(bursts, q):
    """Xoay vòng lượng tử q (mọi tiến trình đến lúc 0): thời gian phản hồi = lúc được chạy lần ĐẦU."""
    rem, t, first, queue = list(bursts), 0, [None] * len(bursts), list(range(len(bursts)))
    while queue:
        i = queue.pop(0)
        if first[i] is None:
            first[i] = t
        run = min(q, rem[i]); t += run; rem[i] -= run
        if rem[i]:
            queue.append(i)
    return first


def race_run(order, times=1):
    """Chạy MỘT cách xen kẽ cụ thể: order là chuỗi nhãn luồng, mỗi chữ = bước kế tiếp (đọc → cộng → ghi, lặp `times` lần) của luồng đó.
    Trả về (x cuối, vết [(luồng, bước, thanh ghi, x)])."""
    ops = {t: [k for k in ("load", "add", "store") * times] for t in set(order)}
    pos, x, reg, trace = {t: 0 for t in ops}, 0, {t: 0 for t in ops}, []
    for t in order:
        k = ops[t][pos[t]]; pos[t] += 1
        if k == "load": reg[t] = x
        elif k == "add": reg[t] += 1
        else: x = reg[t]
        trace.append((t, k, reg[t], x))
    assert all(pos[t] == len(ops[t]) for t in ops), "chuỗi xen kẽ thiếu bước"
    return x, trace


def fork_loop(n, print_after=True):
    """Mô phỏng `for (i = 0; i < n; i++) { fork(); printf(...); }`: mỗi vòng, MỌI tiến trình đang có đều tách đôi (con chạy tiếp
    từ sau fork với cùng i). Trả về (số tiến trình cuối, số lần in). print_after=False: không có printf trong vòng."""
    procs, prints = [0], 0          # mỗi phần tử = giá trị i mà tiến trình sẽ chạy tiếp
    for _ in range(n):
        procs = [i + 1 for i in procs for _ in (0, 1)]
        prints += len(procs) if print_after else 0
    return len(procs), prints


def prodcons(n_slots=2, rounds=3, consumer_swapped=False, producer_swapped=False):
    """Duyệt MỌI cách xen kẽ của 1 luồng sản xuất và 1 luồng tiêu thụ, mỗi luồng `rounds` vòng, bộ đệm `n_slots` ô.
    Sản xuất:  wait(trống); wait(khoá); đặt; signal(khoá); signal(đầy)
    Tiêu thụ:  wait(đầy); wait(khoá); lấy; signal(khoá); signal(trống)   (consumer_swapped: wait(khoá) TRƯỚC wait(đầy);
    producer_swapped: wait(khoá) TRƯỚC wait(trống))
    wait(s): chỉ đi tiếp khi s > 0 rồi giảm 1; signal(s): tăng 1. Trả về dict: bế tắc có xảy ra không, số món ít/nhiều nhất
    từng thấy trong bộ đệm, và có lúc nào hai luồng cùng ở bước đặt/lấy (vi phạm loại trừ) không."""
    P = [("w", "empty"), ("w", "mutex"), ("put",), ("s", "mutex"), ("s", "full")]
    C = [("w", "full"), ("w", "mutex"), ("get",), ("s", "mutex"), ("s", "empty")]
    if consumer_swapped:
        C[0], C[1] = C[1], C[0]
    if producer_swapped:
        P[0], P[1] = P[1], P[0]
    progs = (P, C)
    start = (0, 0, 0, 0, n_slots, 0, 1, 0)   # pcP, pcC, vòngP, vòngC, trống, đầy, khoá, số món
    seen, stack = {start}, [start]
    res = {"deadlock": False, "min_items": 0, "max_items": 0, "both_inside": False}
    while stack:
        st = stack.pop()
        pcs, rnd, sem, items = list(st[0:2]), list(st[2:4]), {"empty": st[4], "full": st[5], "mutex": st[6]}, st[7]
        res["min_items"] = min(res["min_items"], items); res["max_items"] = max(res["max_items"], items)
        if all(rnd[k] < rounds for k in (0, 1)) and progs[0][pcs[0]][0] == "put" and progs[1][pcs[1]][0] == "get":
            res["both_inside"] = True
        moved, done = False, all(rnd[k] == rounds for k in (0, 1))
        for k in (0, 1):
            if rnd[k] == rounds:
                continue
            op = progs[k][pcs[k]]
            s2, it2 = dict(sem), items
            if op[0] == "w":
                if s2[op[1]] == 0:
                    continue
                s2[op[1]] -= 1
            elif op[0] == "s":
                s2[op[1]] += 1
            elif op[0] == "put":
                it2 += 1
            else:
                it2 -= 1
            pc2, rn2 = list(pcs), list(rnd)
            pc2[k] += 1
            if pc2[k] == len(progs[k]):
                pc2[k] = 0; rn2[k] += 1
            nst = (pc2[0], pc2[1], rn2[0], rn2[1], s2["empty"], s2["full"], s2["mutex"], it2)
            moved = True
            if nst not in seen:
                seen.add(nst); stack.append(nst)
        if not moved and not done:
            res["deadlock"] = True
    return res


def philosophers(n=5, ordered=False, rounds=1):
    """Duyệt MỌI cách xen kẽ của n triết gia ngồi vòng tròn, đũa i nằm giữa người i và i+1 (mod n). Mỗi người: cầm đũa thứ nhất,
    cầm đũa thứ hai, ăn, đặt cả hai — lặp `rounds` lần. Mặc định cầm đũa TRÁI (số i) trước; ordered=True: cầm đũa SỐ NHỎ trước.
    Trả về (có bế tắc không, số trạng thái đã duyệt)."""
    def order(i):
        a, b = i, (i + 1) % n
        return (min(a, b), max(a, b)) if ordered else (a, b)
    start = (tuple([0] * n), tuple([-1] * n), tuple([0] * n))   # pc, chủ của từng đũa, số vòng đã ăn
    seen, stack, dead = {start}, [start], False
    while stack:
        pc, owner, done = stack.pop()
        moved = False
        for i in range(n):
            if done[i] == rounds:
                continue
            f1, f2 = order(i)
            p, o, d = list(pc), list(owner), list(done)
            if pc[i] == 0 and owner[f1] == -1:
                o[f1] = i; p[i] = 1
            elif pc[i] == 1 and owner[f2] == -1:
                o[f2] = i; p[i] = 2
            elif pc[i] == 2:
                o[f1] = o[f2] = -1; p[i] = 0; d[i] += 1
            else:
                continue
            moved = True
            st = (tuple(p), tuple(o), tuple(d))
            if st not in seen:
                seen.add(st); stack.append(st)
        if not moved and any(x < rounds for x in done):
            dead = True
    return dead, len(seen)


def inode_max(direct, levels, block, ptr):
    """Kích thước tệp tối đa (byte) của inode có `direct` con trỏ trực tiếp và các con trỏ gián tiếp 1..levels tầng."""
    p = block // ptr
    return (direct + sum(p ** k for k in range(1, levels + 1))) * block


def inode_reads(offset, direct, block, ptr):
    """Số lần đọc đĩa để lấy khối chứa byte `offset` khi chưa có gì trong bộ nhớ đệm: đọc inode + mỗi tầng gián tiếp + khối dữ liệu."""
    p, b, k = block // ptr, offset // block, 0
    if b < direct:
        return 2
    b -= direct
    while True:
        k += 1
        if b < p ** k:
            return 2 + k
        b -= p ** k


def disk_scan(queue, head, toward_zero=True, go_to_end=True, max_cyl=199):
    """Thang máy: đi một chiều phục vụ mọi yêu cầu trên đường, rồi quay đầu. go_to_end=True (SCAN) chạy tới tận trụ 0 / max_cyl
    trước khi quay; False (LOOK) quay ngay ở yêu cầu xa nhất. Trả về (tổng quãng đường, thứ tự phục vụ)."""
    lo = sorted((c for c in queue if c <= head), reverse=True)
    hi = sorted(c for c in queue if c > head)
    first, second = (lo, hi) if toward_zero else (hi, lo)
    end = 0 if toward_zero else max_cyl
    path = [head] + first + ([end] if go_to_end and second else []) + second
    return sum(abs(b - a) for a, b in zip(path, path[1:])), first + second


# ───────── Lý thuyết tính toán (TOC): mô phỏng ôtômat, văn phạm, máy Turing — mỗi hàm trả về con số / vết đưa lên màn hình ─────────
def strings(alpha, n, exact=False):
    """Mọi chuỗi trên bảng chữ `alpha` có độ dài ≤ n (exact=True: đúng n), kể cả chuỗi rỗng ''."""
    ks = [n] if exact else range(n + 1)
    return ["".join(w) for k in ks for w in itertools.product(alpha, repeat=k)]


def dfa_complete(delta, states, alpha):
    """DFA hợp lệ: mỗi (trạng thái, ký hiệu) có ĐÚNG một chuyển, và chuyển tới một trạng thái có thật."""
    return all((q, a) in delta and delta[(q, a)] in states for q in states for a in alpha) and \
        all(q in states and a in alpha for q, a in delta)


def dfa_run(delta, start, accept, w):
    """Chạy DFA trên w. delta: {(q, a): q'}. Trả (nhận?, dãy trạng thái đi qua, gồm cả trạng thái đầu)."""
    path = [start]
    for a in w:
        path.append(delta[(path[-1], a)])
    return path[-1] in accept, path


def nfa_run(delta, start, accept, w):
    """Chạy NFA bằng TẬP trạng thái. delta: {(q, a): {q', …}} (thiếu khoá = không đi được). Không có chuyển rỗng.
    Trả (nhận?, dãy tập trạng thái — mỗi tập là frozenset)."""
    cur, trace = frozenset([start]), []
    trace.append(cur)
    for a in w:
        cur = frozenset(r for q in cur for r in delta.get((q, a), ()))
        trace.append(cur)
    return bool(cur & set(accept)), trace


def subset_construct(delta, start, alpha):
    """Dựng tập con, chỉ giữ các tập TỚI ĐƯỢC từ {start}. Trả (danh sách tập theo thứ tự tìm thấy, chuyển {(tập, a): tập})."""
    s0 = frozenset([start]); seen, order, trans, todo = {s0}, [s0], {}, [s0]
    while todo:
        S = todo.pop(0)
        for a in alpha:
            T = frozenset(r for q in S for r in delta.get((q, a), ()))
            trans[(S, a)] = T
            if T not in seen:
                seen.add(T); order.append(T); todo.append(T)
    return order, trans


def reachable(delta, start, alpha):
    seen, todo = {start}, [start]
    while todo:
        q = todo.pop()
        for a in alpha:
            r = delta[(q, a)]
            if r not in seen:
                seen.add(r); todo.append(r)
    return seen


def minimize(states, alpha, delta, start, accept):
    """Tối thiểu hoá bằng bảng đánh dấu cặp (thuật toán lấp bảng): bỏ trạng thái không tới được, đánh dấu cặp (nhận, không nhận),
    rồi lặp: cặp (p, q) bị đánh dấu nếu có ký hiệu a đưa tới một cặp đã đánh dấu. Trả (các lớp tương đương — list of frozenset,
    tập trạng thái không tới được, số vòng lặp đánh dấu)."""
    live = reachable(delta, start, alpha)
    dead = set(states) - live
    qs = sorted(live, key=str)
    marked = {frozenset((p, q)) for p, q in itertools.combinations(qs, 2) if (p in accept) != (q in accept)}
    rounds, changed = 0, True
    while changed:
        changed, rounds = False, rounds + 1
        for p, q in itertools.combinations(qs, 2):
            pq = frozenset((p, q))
            if pq not in marked and any(frozenset((delta[(p, a)], delta[(q, a)])) in marked
                                        for a in alpha if delta[(p, a)] != delta[(q, a)]):
                marked.add(pq); changed = True
    classes = []
    for q in qs:
        for c in classes:
            if frozenset((q, next(iter(c)))) not in marked:
                c.add(q); break
        else:
            classes.append({q})
    return [frozenset(c) for c in classes], dead, rounds


def regex_lang(pattern, alpha, n):
    """Tập chuỗi độ dài ≤ n mà biểu thức chính quy (cú pháp Python re) khớp TRỌN chuỗi."""
    import re
    rx = re.compile(pattern)
    return {w for w in strings(alpha, n) if rx.fullmatch(w)}


def pump_survivors(w, p, in_lang, imax=3):
    """Bổ đề bơm: mọi cách tách w = xyz với |xy| ≤ p, |y| ≥ 1. Trả các cách tách (x, y, z) mà x yⁱ z ∈ L với MỌI i = 0..imax.
    Danh sách rỗng = không cách tách nào bơm được → w là phản ví dụ cho p này."""
    out = []
    for i in range(p + 1):
        for j in range(i + 1, p + 1):
            x, y, z = w[:i], w[i:j], w[j:]
            if all(in_lang(x + y * k + z) for k in range(imax + 1)):
                out.append((x, y, z))
    return out


def cfg_lang(rules, start, maxlen):
    """Mọi chuỗi kết thúc (chỉ ký hiệu kết thúc) độ dài ≤ maxlen mà văn phạm sinh ra. rules: {biến: [vế phải, …]}, biến là
    một chữ HOA, vế phải là chuỗi ('' = rỗng). Cắt nhánh khi số ký hiệu kết thúc đã vượt maxlen (đúng khi không có quy tắc
    xoá ký hiệu kết thúc — luôn đúng với văn phạm)."""
    out, seen, todo = set(), {start}, [start]
    while todo:
        f = todo.pop()
        k = next((i for i, c in enumerate(f) if c in rules), None)
        if k is None:
            out.add(f); continue
        for rhs in rules[f[k]]:
            g = f[:k] + rhs + f[k + 1:]
            if sum(c not in rules for c in g) <= maxlen and len(g) <= 3 * maxlen + 2 and g not in seen:
                seen.add(g); todo.append(g)
    return out


def balanced(s):
    d = 0
    for c in s:
        d += 1 if c == "(" else -1
        if d < 0:
            return False
    return d == 0


def bracket_values(nums, ops):
    """Giá trị của MỌI cây suy dẫn (mọi cách đặt ngoặc đầy đủ) cho nums[0] ops[0] nums[1] … — văn phạm mơ hồ E → E+E | E*E | E-E | số.
    Trả list (một phần tử mỗi cây; số cây = số Catalan)."""
    f = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}

    def go(i, j):
        if i == j:
            return [nums[i]]
        return [f[ops[k]](a, b) for k in range(i, j) for a in go(i, k) for b in go(k + 1, j)]
    return go(0, len(nums) - 1)


def pda_0n1n(w):
    """Ôtômat đẩy xuống cho {0ⁿ1ⁿ}: đọc 0 thì đẩy X (chỉ khi chưa gặp 1), đọc 1 thì lấy X ra. Nhận khi đọc hết và ngăn xếp rỗng.
    Trả (nhận?, vết [(ký hiệu đọc, ngăn xếp sau bước — chuỗi, đáy bên trái)], lý do dừng)."""
    st, seen1, trace = "", False, []
    for c in w:
        if c == "0":
            if seen1:
                return False, trace, "0 sau 1"
            st += "X"
        elif c == "1":
            seen1 = True
            if not st:
                return False, trace, "lấy từ ngăn rỗng"
            st = st[:-1]
        trace.append((c, st))
    return st == "", trace, ("ngăn xếp rỗng" if st == "" else "còn X")


def tm_run(table, tape, head, state, blank="_", halt=("H",), limit=10000):
    """Máy Turing một băng. table: {(q, a): (q', b, 'L'|'R'|'S')}. Thiếu chuyển = dừng (từ chối nếu chưa ở trạng thái halt).
    Trả (băng sau khi bỏ ô trống hai đầu, số bước, trạng thái cuối, vết [(trạng thái, vị trí đầu, băng)])."""
    cells = dict(enumerate(tape)) or {head: blank}; steps, trace = 0, []
    while state not in halt and steps < limit:
        a = cells.get(head, blank)
        if (state, a) not in table:
            break
        snap = "".join(cells.get(i, blank) for i in range(min(cells), max(cells) + 1))
        trace.append((state, head - min(cells), snap))
        state, b, mv = table[(state, a)]
        cells[head] = b
        head += {"L": -1, "R": 1, "S": 0}[mv]
        steps += 1
    lo, hi = min(cells), max(cells)
    return "".join(cells.get(i, blank) for i in range(lo, hi + 1)).strip(blank), steps, state, trace


def collatz(n):
    """Số bước tới 1 của dãy 3n + 1 và giá trị lớn nhất gặp trên đường."""
    steps, top = 0, n
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps, top = steps + 1, max(top, n)
    return steps, top


def subset_sums(nums, target):
    """Mọi tập con (theo chỉ số tăng dần, trả về giá trị) có tổng đúng target, và số tập con đã thử (2ⁿ)."""
    sols = [tuple(nums[i] for i in c) for k in range(len(nums) + 1) for c in itertools.combinations(range(len(nums)), k)
            if sum(nums[i] for i in c) == target]
    return sols, 2 ** len(nums)


def rx_tokens(pat):
    """Biểu thức chính quy rất nhỏ (TOC L14) → danh sách (ký tự, lượng từ): ký tự là chữ hoặc '.', lượng từ '', '?', '*'.
    Không có ngoặc, không có '|'. Ví dụ 'a?a?aa' → [('a','?'), ('a','?'), ('a',''), ('a','')]."""
    out, i = [], 0
    while i < len(pat):
        q = pat[i + 1] if i + 1 < len(pat) and pat[i + 1] in "?*" else ""
        out.append((pat[i], q))
        i += 2 if q else 1
    return out


def bt_match(pat, s):
    """Khớp TRỌN chuỗi bằng QUAY LUI kiểu Perl/PCRE (tham: thử lấy nhiều trước, '?' thử 1 rồi 0).
    Trả (khớp?, số lần thử đặt một ký hiệu của mẫu vào một vị trí của chuỗi) — đơn vị đếm của bài, không phải số bước của Perl."""
    toks, tries = rx_tokens(pat), [0]

    def go(k, i):
        if k == len(toks):
            return i == len(s)
        c, q = toks[k]
        ok = lambda j: j < len(s) and (c == "." or s[j] == c)  # noqa: E731
        if q == "":
            tries[0] += 1
            return ok(i) and go(k + 1, i + 1)
        if q == "?":
            tries[0] += 1
            if ok(i) and go(k + 1, i + 1):
                return True
            return go(k + 1, i)
        n = 0                                   # '*': ăn tham nhiều nhất có thể rồi nhả dần từng ký tự
        while True:
            tries[0] += 1
            if not ok(i + n):
                break
            n += 1
        return any(go(k + 1, i + m) for m in range(n, -1, -1))
    return go(0, 0), tries[0]


def thompson_match(pat, s):
    """Khớp TRỌN chuỗi bằng cách của Thompson (1968): giữ TẬP vị trí trong mẫu, đọc mỗi ký tự một lần.
    Trả (khớp?, danh sách cỡ tập sau mỗi ký tự, tổng số lần xét một phần tử của tập)."""
    toks = rx_tokens(pat)

    def close(S):                               # thêm các vị trí bỏ qua được (lượng từ '?' hoặc '*' cho phép 0 lần)
        S, todo = set(S), list(S)
        while todo:
            k = todo.pop()
            if k < len(toks) and toks[k][1] in ("?", "*") and k + 1 not in S:
                S.add(k + 1); todo.append(k + 1)
        return S
    cur, sizes, work = close({0}), [], 0
    for ch in s:
        nxt = set()
        for k in cur:
            work += 1
            if k < len(toks) and (toks[k][0] == "." or toks[k][0] == ch):
                nxt.add(k if toks[k][1] == "*" else k + 1)
        cur = close(nxt)
        sizes.append(len(cur))
    return len(toks) in cur, sizes, work


# ───────── Mạng máy tính (NET): mỗi hàm trả về con số / vết đưa lên màn hình ─────────
def crc_remainder(data, gen):
    """Phần dư CRC: nối len(gen)−1 số 0 vào data rồi chia đa thức theo mod 2 (XOR). data, gen là chuỗi bit.
    Trả (phần dư — chuỗi len(gen)−1 bit, vết [(vị trí bắt đầu XOR, chuỗi sau XOR)])."""
    k = len(gen) - 1
    a, trace = list(data + "0" * k), []
    for i in range(len(data)):
        if a[i] == "1":
            for j, g in enumerate(gen):
                a[i + j] = "1" if a[i + j] != g else "0"
            trace.append((i, "".join(a)))
    return "".join(a[-k:]), trace


def crc_check(codeword, gen):
    """Bên nhận: chia cả từ mã (dữ liệu + phần dư) cho gen; phần dư toàn 0 = không phát hiện lỗi."""
    k = len(gen) - 1
    a = list(codeword)
    for i in range(len(codeword) - k):
        if a[i] == "1":
            for j, g in enumerate(gen):
                a[i + j] = "1" if a[i + j] != g else "0"
    return "".join(a[-k:])


def inet_checksum(words):
    """Checksum Internet 16 bit: cộng bù một (cuốn bit nhớ về), rồi đảo bit. words: list số 0..65535. Trả (tổng sau cuốn, checksum)."""
    s = 0
    for w in words:
        s += w
        s = (s & 0xFFFF) + (s >> 16)
    return s, (~s) & 0xFFFF


def subnet(cidr):
    """(địa chỉ mạng, địa chỉ quảng bá, số máy dùng được, máy đầu, máy cuối) của một khối IPv4 dạng 'a.b.c.d/n'."""
    import ipaddress
    n = ipaddress.ip_network(cidr, strict=True)
    hosts = list(n.hosts())
    return str(n.network_address), str(n.broadcast_address), len(hosts), str(hosts[0]), str(hosts[-1])


def split_subnets(cidr, new_prefix):
    import ipaddress
    return [str(s) for s in ipaddress.ip_network(cidr).subnets(new_prefix=new_prefix)]


def lpm(table, addr):
    """Khớp tiền tố dài nhất. table: [(khối 'a.b.c.d/n', cổng)]; trả (cổng, khối thắng, danh sách khối khớp)."""
    import ipaddress
    a = ipaddress.ip_address(addr)
    hits = [(ipaddress.ip_network(c), port) for c, port in table if a in ipaddress.ip_network(c)]
    if not hits:
        return None, None, []
    best = max(hits, key=lambda h: h[0].prefixlen)
    return best[1], str(best[0]), [str(h[0]) for h in hits]


def undirected(edges):
    g = {}
    for u, v, w in edges:
        g.setdefault(u, {})[v] = w
        g.setdefault(v, {})[u] = w
    return g


def next_hops(g, s):
    """Bảng chuyển tiếp của bộ định tuyến s từ cây đường đi ngắn nhất (Dijkstra): {đích: (chặng kế tiếp, chi phí)}."""
    dist, prev, done = {v: math.inf for v in g}, {}, set()
    dist[s] = 0
    while len(done) < len(g):
        u = min((v for v in g if v not in done), key=lambda v: (dist[v], v))
        done.add(u)
        for v, w in g[u].items():
            if dist[u] + w < dist[v]:
                dist[v], prev[v] = dist[u] + w, u
    out = {}
    for t in g:
        if t == s:
            continue
        hop = t
        while prev[hop] != s:
            hop = prev[hop]
        out[t] = (hop, dist[t])
    return out


def count_to_infinity(rounds=6, poison=False, inf=16):
    """Đường thẳng A —1— B —1— C. Liên kết A–B đứt. Mỗi vòng B và C cập nhật ĐỒNG THỜI theo Bellman-Ford từ vectơ của hàng xóm
    (vòng trước). poison=True: C quảng bá ∞ cho B về đích A vì đường của C đi qua B (đầu độc ngược).
    Trả [(khoảng cách của B tới A, của C tới A)] sau mỗi vòng, bắt đầu từ trạng thái trước khi đứt (1, 2)."""
    b, c, out = 1, 2, [(1, 2)]
    c_via_b = True
    for _ in range(rounds):
        adv_c_to_b = inf if (poison and c_via_b) else c
        nb = min(inf, adv_c_to_b + 1)            # B chỉ còn hàng xóm C
        nc = min(inf, b + 1)                      # C chỉ có hàng xóm B
        b, c = nb, nc
        out.append((b, c))
    return out


def stop_wait_util(l_bits, rate, rtt):
    """Hiệu suất dừng–chờ = thời gian phát / (RTT + thời gian phát)."""
    t = l_bits / rate
    return t / (rtt + t)


def window_util(w, l_bits, rate, rtt):
    t = l_bits / rate
    return min(1.0, w * t / (rtt + t))


def cwnd_trace(rounds, ssthresh, loss_at=(), variant="reno"):
    """Cửa sổ tắc nghẽn (đơn vị gói) theo từng RTT. Khởi động chậm: nhân đôi nhưng không vượt ssthresh; sau đó +1 mỗi RTT.
    Vòng có mặt trong loss_at: mất gói phát hiện bằng 3 ACK trùng → ssthresh = cwnd // 2; reno: cwnd = ssthresh; tahoe: cwnd = 1."""
    cw, th, out = 1, ssthresh, []
    for r in range(rounds):
        out.append(cw)
        if r in loss_at:
            th = max(cw // 2, 2)
            cw = th if variant == "reno" else 1
        elif cw < th:
            cw = min(2 * cw, th)
        else:
            cw += 1
    return out


def http_rtts(n_objects, persistent=False, pipelined=False):
    """Số RTT tải trang HTML + n đối tượng (bỏ qua thời gian truyền): mỗi kết nối TCP mới tốn 1 RTT bắt tay, mỗi yêu cầu 1 RTT."""
    if not persistent:
        return 2 + 2 * n_objects
    return 2 + (1 if (pipelined and n_objects) else n_objects)


def dh(p, g, a, b):
    """Diffie–Hellman: (A = g^a mod p, B = g^b mod p, khoá của bên a = B^a mod p, khoá của bên b = A^b mod p)."""
    A, B = pow(g, a, p), pow(g, b, p)
    return A, B, pow(B, a, p), pow(A, b, p)


def rsa_toy(n, e, d, m):
    """Ký m bằng khoá bí mật d: s = m^d mod n; kiểm bằng khoá công khai e: s^e mod n. Trả (s, s^e mod n)."""
    s = pow(m, d, n)
    return s, pow(s, e, n)


def learn_switch(frames):
    """Bộ chuyển mạch tự học. frames: [(MAC nguồn, MAC đích, cổng vào)]. Trả [(hành động, bảng sau khung)] — hành động là
    'tràn' (chưa biết đích: gửi mọi cổng trừ cổng vào), 'gửi cổng k', hoặc 'lọc' (đích ở chính cổng vào)."""
    table, out = {}, []
    for src, dst, port in frames:
        table[src] = port
        if dst not in table:
            act = "tràn"
        elif table[dst] == port:
            act = "lọc"
        else:
            act = f"gửi cổng {table[dst]}"
        out.append((act, dict(table)))
    return out



# ───────── Toán cho robot (RBM): phép quay, động học, ODE, điều khiển, Kalman, lấy mẫu, A* — góc tính bằng ĐỘ ─────────
def _np():
    import numpy
    return numpy


def rot2(deg):
    """Ma trận quay 2D ngược chiều kim đồng hồ một góc deg độ."""
    np, t = _np(), math.radians(deg)
    return np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])


def rotx(deg):
    np, t = _np(), math.radians(deg)
    return np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])


def roty(deg):
    np, t = _np(), math.radians(deg)
    return np.array([[math.cos(t), 0, math.sin(t)], [0, 1, 0], [-math.sin(t), 0, math.cos(t)]])


def rotz(deg):
    np, t = _np(), math.radians(deg)
    return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])


def qmul(a, b):
    """Tích Hamilton của hai quaternion (w, x, y, z)."""
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return (w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2)


def qaxis(axis, deg):
    """Quaternion đơn vị quay deg độ quanh trục đơn vị axis: (cos(θ/2), sin(θ/2)·axis)."""
    h = math.radians(deg) / 2
    n = math.sqrt(sum(c * c for c in axis))
    return (math.cos(h),) + tuple(math.sin(h) * c / n for c in axis)


def qrot(q, v):
    """Quay vectơ v bằng quaternion đơn vị q: q·(0, v)·q̄, trả 3 toạ độ."""
    conj = (q[0], -q[1], -q[2], -q[3])
    return qmul(qmul(q, (0.0,) + tuple(v)), conj)[1:]


def qmat(q):
    """Ma trận quay 3 × 3 của quaternion đơn vị q."""
    np = _np()
    return np.array([qrot(q, e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]).T


def homog2(deg, tx, ty):
    """Ma trận thuần nhất 3 × 3: quay deg độ rồi tịnh tiến (tx, ty)."""
    np = _np()
    T = np.eye(3)
    T[:2, :2], T[:2, 2] = rot2(deg), (tx, ty)
    return T


def fk2(l1, l2, t1, t2):
    """Động học thuận tay máy 2 khâu phẳng; t2 là góc khớp 2 TƯƠNG ĐỐI với khâu 1. Trả (khuỷu, đầu tay)."""
    a, b = math.radians(t1), math.radians(t1 + t2)
    e = (l1 * math.cos(a), l1 * math.sin(a))
    return e, (e[0] + l2 * math.cos(b), e[1] + l2 * math.sin(b))


def ik2(l1, l2, x, y):
    """Động học ngược 2 khâu: mọi nghiệm (t1, t2) theo độ, t2 ≥ 0 trước; [] nếu (x, y) ngoài tầm với."""
    c2 = (x * x + y * y - l1 * l1 - l2 * l2) / (2 * l1 * l2)
    if c2 > 1 + 1e-12 or c2 < -1 - 1e-12:
        return []
    c2 = max(-1.0, min(1.0, c2))
    out = []
    for s2 in sorted({math.sqrt(1 - c2 * c2), -math.sqrt(1 - c2 * c2)}, reverse=True):
        t2 = math.atan2(s2, c2)
        t1 = math.atan2(y, x) - math.atan2(l2 * s2, l1 + l2 * c2)
        out.append((round(math.degrees(t1), 9), round(math.degrees(t2), 9)))
    return out


def jac2(l1, l2, t1, t2):
    """Jacobian 2 × 2 của đầu tay theo (θ1, θ2), góc theo độ, đạo hàm theo radian."""
    np, a, b = _np(), math.radians(t1), math.radians(t1 + t2)
    return np.array([[-l1 * math.sin(a) - l2 * math.sin(b), -l2 * math.sin(b)],
                     [l1 * math.cos(a) + l2 * math.cos(b), l2 * math.cos(b)]])


def euler_ode(f, x0, h, n, t0=0.0):
    """Phương pháp Euler: x_{k+1} = x_k + h·f(t_k, x_k). Trả danh sách n + 1 giá trị (x có thể là số hoặc mảng numpy)."""
    xs, t = [x0], t0
    for _ in range(n):
        xs.append(xs[-1] + h * f(t, xs[-1]))
        t += h
    return xs


def rk4_ode(f, x0, h, n, t0=0.0):
    """Runge–Kutta bậc 4 cổ điển. Trả danh sách n + 1 giá trị."""
    xs, t = [x0], t0
    for _ in range(n):
        x = xs[-1]
        k1 = f(t, x)
        k2 = f(t + h / 2, x + h / 2 * k1)
        k3 = f(t + h / 2, x + h / 2 * k2)
        k4 = f(t + h, x + h * k3)
        xs.append(x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4))
        t += h
    return xs


def rk4_stages(f, x, h, t=0.0):
    """Bốn độ dốc k1..k4 của một bước RK4 (để đưa lên bảng)."""
    k1 = f(t, x)
    k2 = f(t + h / 2, x + h / 2 * k1)
    k3 = f(t + h / 2, x + h / 2 * k2)
    k4 = f(t + h, x + h * k3)
    return k1, k2, k3, k4


def pid_sim(kp, ki=0.0, kd=0.0, r=1.0, a=1.0, b=1.0, h=0.001, T=10.0):
    """Vòng kín: đối tượng bậc nhất x' = −a·x + b·u, u = kp·e + ki·∫e + kd·e', e = r − x, x(0) = 0 (Euler bước h).
    Trả (x cuối, sai số cuối, x lớn nhất)."""
    x, integ, e_prev, xmax = 0.0, 0.0, r, 0.0
    for _ in range(int(round(T / h))):
        e = r - x
        integ += e * h
        u = kp * e + ki * integ + kd * (e - e_prev) / h
        e_prev = e
        x += h * (-a * x + b * u)
        xmax = max(xmax, x)
    return x, r - x, xmax


def kalman1d_update(x, P, z, R):
    """Bước cập nhật Kalman 1 chiều: K = P/(P + R); trả (K, x mới, P mới)."""
    K = P / (P + R)
    return K, x + K * (z - x), (1 - K) * P


def kalman_cv(x, P, z, dt, Q, R):
    """Một bước dự đoán–cập nhật mô hình vận tốc không đổi, chỉ đo vị trí. x: (vị trí, vận tốc), P: 2 × 2,
    Q: 2 × 2 nhiễu quá trình, R: phương sai phép đo. Trả (x dự đoán, P dự đoán, K, x mới, P mới)."""
    np = _np()
    F, H = np.array([[1.0, dt], [0.0, 1.0]]), np.array([[1.0, 0.0]])
    xp, Pp = F @ np.asarray(x, float), F @ np.asarray(P, float) @ F.T + np.asarray(Q, float)
    S = (H @ Pp @ H.T)[0, 0] + R
    K = (Pp @ H.T / S).ravel()
    xn = xp + K * (z - xp[0])
    Pn = (np.eye(2) - np.outer(K, H.ravel())) @ Pp
    return xp, Pp, K, xn, Pn


def alias_freq(f, fs):
    """Tần số biểu kiến (trong [0, fs/2]) khi lấy mẫu tín hiệu tần số f với tần số lấy mẫu fs."""
    r = f % fs
    return min(r, fs - r)


def dft_mag(x):
    """Độ lớn các hệ số DFT |X_k|, k = 0..N−1."""
    N = len(x)
    out = []
    for k in range(N):
        re = sum(x[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
        im = -sum(x[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
        out.append(math.hypot(re, im))
    return out


def astar_grid(grid, s, t, hfun=None):
    """A* trên lưới ô ('.' đi được, '#' tường), 4 hướng, mỗi bước giá 1. hfun(p, t) mặc định Manhattan.
    Hoà f thì ưu tiên g lớn hơn, rồi theo (hàng, cột). Trả (giá, đường đi, thứ tự mở rộng) — giá None nếu không tới được."""
    hfun = hfun or (lambda p, q: abs(p[0] - q[0]) + abs(p[1] - q[1]))
    pq, g, par, order, done = [(hfun(s, t), 0, s)], {s: 0}, {s: None}, [], set()
    while pq:
        p = heapq.heappop(pq)[2]
        if p in done:
            continue
        done.add(p)
        order.append(p)
        if p == t:
            path = [p]
            while par[path[-1]] is not None:
                path.append(par[path[-1]])
            return g[p], path[::-1], order
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            q = (p[0] + dr, p[1] + dc)
            if 0 <= q[0] < len(grid) and 0 <= q[1] < len(grid[0]) and grid[q[0]][q[1]] != "#" and g[p] + 1 < g.get(q, 1e9):
                g[q], par[q] = g[p] + 1, p
                heapq.heappush(pq, (g[q] + hfun(q, t), -g[q], q))
    return None, [], order


def bfs_grid(grid, s):
    """Khoảng cách thật (số bước) từ s tới mọi ô đi được — dùng kiểm ước lượng không vượt thật."""
    from collections import deque
    dist, dq = {s: 0}, deque([s])
    while dq:
        p = dq.popleft()
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            q = (p[0] + dr, p[1] + dc)
            if 0 <= q[0] < len(grid) and 0 <= q[1] < len(grid[0]) and grid[q[0]][q[1]] != "#" and q not in dist:
                dist[q] = dist[p] + 1
                dq.append(q)
    return dist


def lsq_line(xs, ys):
    """Bình phương tối thiểu y ≈ a·x + b. Trả (a, b, phần dư, độ lệch chuẩn phần dư s với n − 2 bậc tự do, sai số chuẩn của a)."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    b = my - a * mx
    res = [y - (a * x + b) for x, y in zip(xs, ys)]
    s = math.sqrt(sum(r * r for r in res) / (n - 2))
    return a, b, res, s, s / math.sqrt(sxx)


# ───────── Cơ sở dữ liệu (DBS): SQL chạy thật trên sqlite3, phụ thuộc hàm, chỉ mục, chi phí nối, lịch thực thi ─────────
DB_DEMO = """
PRAGMA foreign_keys = ON;
CREATE TABLE Lop (ma_lop TEXT PRIMARY KEY, ten_lop TEXT NOT NULL);
CREATE TABLE SinhVien (mssv INTEGER PRIMARY KEY, ten TEXT NOT NULL, lop TEXT REFERENCES Lop(ma_lop), diem REAL);
INSERT INTO Lop VALUES ('K1', 'Khoa học máy tính'), ('K2', 'Kỹ thuật phần mềm');
INSERT INTO SinhVien VALUES (1, 'An', 'K1', 8), (2, 'Bình', 'K1', 6), (3, 'Chi', 'K2', 9), (4, 'Dũng', NULL, 7);
"""


def sql(query, setup=DB_DEMO):
    """Chạy `setup` (mặc định: CSDL mẫu Lop/SinhVien) trên sqlite3 trong bộ nhớ rồi chạy `query`; trả danh sách dòng (tuple)."""
    import sqlite3
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(setup)
        return [tuple(r) for r in con.execute(query).fetchall()]
    finally:
        con.close()


def sql_error(stmt, setup=DB_DEMO):
    """Chạy `stmt` sau `setup`; trả thông báo lỗi của sqlite3 (chuỗi) hoặc None nếu câu lệnh được chấp nhận."""
    import sqlite3
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(setup)
        con.executescript(stmt)
        return None
    except sqlite3.Error as e:
        return str(e)
    finally:
        con.close()


def attr_closure(attrs, fds):
    """Bao đóng thuộc tính X⁺ theo tập phụ thuộc hàm fds = [(trái, phải)] (chuỗi chữ cái). Trả (tập, vết các bước)."""
    x, trace, changed = set(attrs), [], True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if set(lhs) <= x and not set(rhs) <= x:
                x |= set(rhs)
                trace.append((lhs, rhs, "".join(sorted(x))))
                changed = True
    return x, trace


def candidate_keys(R, fds):
    """Mọi khoá ứng viên (tối tiểu) của lược đồ R (chuỗi chữ cái)."""
    keys = []
    for k in range(1, len(R) + 1):
        for combo in itertools.combinations(sorted(R), k):
            if attr_closure(combo, fds)[0] >= set(R) and not any(set(key) <= set(combo) for key in keys):
                keys.append("".join(combo))
    return keys


def lossless_binary(R1, R2, fds):
    """Phép tách R thành R1, R2 không mất thông tin ⟺ (R1 ∩ R2)⁺ chứa R1 hoặc chứa R2."""
    c = attr_closure(set(R1) & set(R2), fds)[0]
    return c >= set(R1) or c >= set(R2)


def bcnf_violations(R, fds):
    """Các phụ thuộc hàm không tầm thường X → Y (trên R) mà X không phải siêu khoá."""
    return [(l, r) for l, r in fds if not set(r) <= set(l) and not attr_closure(l, fds)[0] >= set(R)]


def project(rows, cols, allcols):
    """Chiếu một bảng (danh sách dict hoặc tuple theo allcols) lên cols, bỏ dòng trùng (quan hệ là tập)."""
    idx = [allcols.index(c) for c in cols]
    return sorted({tuple(r[i] for i in idx) for r in rows})


def natural_join(r1, c1, r2, c2):
    """Nối tự nhiên hai bảng tuple với tên cột c1, c2. Trả (dòng, cột)."""
    common = [c for c in c1 if c in c2]
    cols = list(c1) + [c for c in c2 if c not in c1]
    out = set()
    for a in r1:
        for b in r2:
            if all(a[c1.index(c)] == b[c2.index(c)] for c in common):
                out.add(tuple(a) + tuple(b[c2.index(c)] for c in c2 if c not in c1))
    return sorted(out), cols


def bplus_height(n_keys, fanout):
    """Số tầng cây B+ (kể cả tầng lá) tối thiểu khi mỗi nút chứa tới `fanout` con / khoá: nhỏ nhất h với fanout^h ≥ n."""
    h, cap = 1, fanout
    while cap < n_keys:
        h += 1
        cap *= fanout
    return h


def join_costs(R, S, B=None):
    """Chi phí (số lần đọc trang) nối R ⋈ S, R ở vòng ngoài: lồng theo trang R + R·S; lồng theo khối (B trang đệm)
    R + ⌈R/(B − 2)⌉·S; nối băm Grace 3(R + S) (giả sử đủ đệm để chia một lần)."""
    out = {"page_nlj": R + R * S, "hash": 3 * (R + S)}
    if B:
        out["block_nlj"] = R + math.ceil(R / (B - 2)) * S
    return out


def precedence_graph(schedule):
    """Đồ thị ưu tiên của lịch [(giao dịch, 'R'|'W', mục)]: cạnh Ti → Tj khi một thao tác của Ti đi trước và XUNG ĐỘT
    (cùng mục, khác giao dịch, ít nhất một bên ghi) với thao tác sau của Tj. Trả (tập cạnh, có chu trình?)."""
    edges = set()
    for i, (ti, ai, xi) in enumerate(schedule):
        for tj, aj, xj in schedule[i + 1:]:
            if ti != tj and xi == xj and "W" in (ai, aj):
                edges.add((ti, tj))
    nodes = {t for t, _, _ in schedule}
    color = {n: 0 for n in nodes}

    def dfs(u):
        color[u] = 1
        for a, b in edges:
            if a == u and (color[b] == 1 or (color[b] == 0 and dfs(b))):
                return True
        color[u] = 2
        return False

    return edges, any(color[n] == 0 and dfs(n) for n in sorted(nodes))


# Cây B+ mẫu ba tầng, bậc 3 (DBS bài 8) — hình audit/dbs/figs.py vẽ từ đúng dữ liệu này.
BPT_ROOT = [30, 60]
BPT_INNER = [[10, 20], [40, 50], [70, 80]]
BPT_LEAVES = [[1, 5], [10, 15], [20, 25], [30, 35], [40, 45], [50, 55], [60, 65], [70, 75], [80, 85]]


def bpt_search(k):
    """Tra khoá k trên cây mẫu: (chỉ số nút trong, chỉ số lá, số trang đọc = 3). Đi xuống con thứ (số khoá phân cách ≤ k)."""
    i = sum(1 for x in BPT_ROOT if x <= k)
    j = 3 * i + sum(1 for x in BPT_INNER[i] if x <= k)
    return i, j, 3


def bpt_range(lo, hi):
    """Truy vấn khoảng [lo, hi] trên cây mẫu: xuống lá chứa lo (đọc gốc + nút trong), rồi đi theo liên kết lá tới khi khoá đầu
    của lá vượt hi. Trả (danh sách chỉ số lá, số trang đọc)."""
    j = bpt_search(lo)[1]
    leaves = []
    while j < len(BPT_LEAVES) and BPT_LEAVES[j][0] <= hi:
        leaves.append(j)
        j += 1
    return leaves, 2 + len(leaves)


def sql_txn(setup, stmts, query, transaction=True):
    """Chạy các câu `stmts` trên sqlite3 sau `setup`. transaction=True: gói trong một giao dịch (lỗi ở câu nào thì huỷ cả nhóm);
    False: mỗi câu tự commit ngay (lỗi chỉ huỷ câu đó). Trả (thông báo lỗi hoặc None, kết quả `query` sau cùng)."""
    import sqlite3
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(setup)
        err = None
        if transaction:
            try:
                with con:
                    for st in stmts:
                        con.execute(st)
            except sqlite3.Error as e:
                err = str(e)
        else:
            con.isolation_level = None
            for st in stmts:
                try:
                    con.execute(st)
                except sqlite3.Error as e:
                    err = str(e)
                    break
        return err, [tuple(r) for r in con.execute(query).fetchall()]
    finally:
        con.close()


def lost_update(start, deltas):
    """Hai (hay nhiều) giao dịch cùng ĐỌC giá trị `start` trước khi bất kỳ ai ghi, mỗi giao dịch ghi đọc + delta của mình.
    Trả giá trị cuối (giao dịch ghi sau cùng thắng) và giá trị đúng nếu chạy lần lượt."""
    reads = [start for _ in deltas]
    final = start
    for r, d in zip(reads, deltas):
        final = r + d
    return final, start + sum(deltas)


def strict_2pl(order):
    """Khoá hai pha nghiêm ngặt. order: danh sách (giao dịch, 'R'|'W'|'C', mục) theo thứ tự các giao dịch XIN chạy
    (C = commit, mục bỏ trống). Đọc xin khoá chia sẻ S, ghi xin khoá độc quyền X (nâng S lên X nếu chỉ mình giữ S);
    commit nhả mọi khoá. Thao tác không lấy được khoá thì giao dịch đó ĐỢI (các thao tác sau của nó cũng chờ).
    Giới hạn có chủ đích: KHÔNG đánh thức giao dịch đã bị chặn sau khi khoá được nhả — chỉ dùng cho câu hỏi “ai đợi ai, có bế tắc
    không” tới thời điểm đó. Trả (vết [(thao tác, 'chạy'|'đợi Tj')], cạnh đồ thị chờ, có bế tắc?)."""
    locks, trace, waits, blocked = {}, [], set(), set()
    for t, op, x in order:
        if t in blocked:
            trace.append(((t, op, x), "đợi (đang bị chặn)"))
            continue
        if op == "C":
            for k in list(locks):
                locks[k] = [(h, m) for h, m in locks[k] if h != t]
            trace.append(((t, op, x), "chạy"))
            continue
        held = locks.setdefault(x, [])
        others = [(h, m) for h, m in held if h != t]
        if op == "R":
            ok = all(m == "S" for _, m in others)
            mode = "S"
        else:
            ok = not others
            mode = "X"
        if ok:
            held[:] = [(h, m) for h, m in held if h != t] + [(t, "X" if mode == "X" or any(h == t and m == "X" for h, m in held) else "S")]
            trace.append(((t, op, x), "chạy"))
        else:
            for h, _ in others:
                waits.add((t, h))
            blocked.add(t)
            trace.append(((t, op, x), "đợi " + ", ".join(sorted({h for h, _ in others}))))
    nodes = {a for a, _ in waits} | {b for _, b in waits}

    def cyc(u, seen):
        return any(b in seen or cyc(b, seen | {b}) for a, b in waits if a == u)

    return trace, waits, any(cyc(n, {n}) for n in nodes)


def wal_recover(log, disk):
    """Khôi phục sau sự cố theo nhật ký ghi trước (mô hình tối giản, không có điểm kiểm tra).
    log: [(giao dịch, 'U', mục, cũ, mới) | (giao dịch, 'C')] — các bản ghi ĐÃ xuống đĩa trước sự cố, theo thứ tự.
    disk: {mục: giá trị} trên đĩa lúc sự cố (có thể chứa thay đổi chưa commit, và thiếu thay đổi đã commit).
    Pha làm lại: áp mọi bản ghi U theo thứ tự (lặp lại lịch sử). Pha huỷ: đi ngược, trả giá trị cũ cho giao dịch chưa commit.
    Trả (trạng thái cuối, trạng thái sau pha làm lại, tập giao dịch bị huỷ)."""
    state = dict(disk)
    committed = {r[0] for r in log if r[1] == "C"}
    for r in log:
        if r[1] == "U":
            state[r[2]] = r[4]
    after_redo = dict(state)
    losers = {r[0] for r in log if r[1] == "U"} - committed
    for r in reversed(log):
        if r[1] == "U" and r[0] in losers:
            state[r[2]] = r[3]
    return state, after_redo, losers


def iso_reads(level, start, events):
    """Kết quả các lần ĐỌC của T1 dưới một mức cô lập (mô hình nhiều phiên bản, tối giản).
    start: {mục: giá trị đã commit lúc đầu}. events theo thời gian: ('T1', 'R', mục) | ('T2', 'W', mục, giá trị) |
    ('T2', 'C') commit | ('T2', 'A') huỷ | ('T2', 'INS', mục, giá trị) thêm một mục mới | ('T1', 'COUNT', hàm lọc) đếm mục thoả.
    level: 'RU' đọc cả ghi chưa commit; 'RC' đọc bản commit mới nhất tại lúc đọc; 'SNAP' đọc ảnh chụp lúc T1 bắt đầu.
    Trả danh sách giá trị T1 đọc được, theo thứ tự."""
    committed, pending, snap, out = dict(start), {}, dict(start), []
    for e in events:
        t, op = e[0], e[1]
        if t == "T2" and op in ("W", "INS"):
            pending[e[2]] = e[3]
        elif t == "T2" and op == "C":
            committed.update(pending)
            pending = {}
        elif t == "T2" and op == "A":
            pending = {}
        elif t == "T1":
            view = {"RU": {**committed, **pending}, "RC": committed, "SNAP": snap}[level]
            out.append(view.get(e[2]) if op == "R" else sum(1 for v in view.values() if e[2](v)))
    return out


# ───────── Hệ nhúng (ESY): thao tác bit, chống dội, định thời, ADC, lọc, dấu phẩy tĩnh, UART, lập lịch thời gian thực, pin ─────────
def bit_ops(reg, width=8):
    """Bật bit 5, tắt bit 5, đảo bit 3 trên giá trị reg (8 bit). Trả bộ ba kết quả."""
    m = (1 << width) - 1
    return (reg | (1 << 5)) & m, (reg & ~(1 << 5)) & m, (reg ^ (1 << 3)) & m


def debounce(samples, n):
    """Chống dội bằng lấy mẫu: trạng thái ổn định chỉ đổi sau n mẫu liên tiếp giống nhau. Trả dãy trạng thái sau mỗi mẫu."""
    stable, last, run, out = samples[0], samples[0], 0, []
    for x in samples:
        run = run + 1 if x == last else 1
        last = x
        if run >= n:
            stable = x
        out.append(stable)
    return out


def timer_freq(fclk, prescale, top):
    """Tần số tràn của bộ định thời đếm 0..TOP: fclk / (prescale · (TOP + 1))."""
    return fclk / (prescale * (top + 1))


def adc_volts(code, bits, vref):
    """Mã ADC → điện áp theo quy ước mã · Vref / 2^bits (mỗi mức Vref / 2^bits)."""
    return code * vref / 2 ** bits


def ema_step(y, x, a):
    """Lọc thông thấp bậc nhất y ← y + a(x − y)."""
    return y + a * (x - y)


def q_mul(a, b, frac=8, bits=16):
    """Nhân hai số dấu phẩy tĩnh Q(bits−frac).frac (số nguyên có dấu): (a·b) >> frac, bão hoà về [−2^(bits−1), 2^(bits−1) − 1].
    Trả (kết quả bão hoà, kết quả nếu để tràn quay vòng)."""
    raw = (a * b) >> frac
    lo, hi = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
    wrap = ((raw - lo) % (1 << bits)) + lo
    return max(lo, min(hi, raw)), wrap


def rm_bound(n):
    """Cận Liu–Layland cho n tác vụ: n(2^(1/n) − 1)."""
    return n * (2 ** (1 / n) - 1)


def rta(tasks):
    """Phân tích thời gian đáp ứng cho ưu tiên cố định, tasks = [(C, T)] sắp theo ưu tiên giảm dần (hạn = chu kỳ).
    R = C + Σ_{j ưu tiên cao hơn} ⌈R / T_j⌉ C_j, lặp tới điểm bất động. Trả danh sách (R, vết các lần lặp); R = None nếu vượt T."""
    out = []
    for i, (c, t) in enumerate(tasks):
        r, trace = c, [c]
        while True:
            nr = c + sum(math.ceil(r / tj) * cj for cj, tj in tasks[:i])
            trace.append(nr)
            if nr == r:
                break
            if nr > t:
                r = None
                break
            r = nr
        out.append((r, trace))
    return out


def schedule_sim(tasks, horizon, policy):
    """Mô phỏng lập lịch có ưu tiên chiếm theo từng đơn vị thời gian. tasks = [(C, T)] (hạn = chu kỳ, cùng thả ở 0).
    policy 'RM': ưu tiên chu kỳ ngắn; 'EDF': hạn gần nhất. Trả (dãy tác vụ chạy mỗi đơn vị, danh sách trễ hạn (tác vụ, thời điểm))."""
    jobs, timeline, misses = [], [], []
    for t in range(horizon):
        for i, (c, p) in enumerate(tasks):
            if t % p == 0:
                jobs.append([i, c, t + p])
        for j in [j for j in jobs if j[2] <= t and j[1] > 0]:
            misses.append((j[0], j[2]))
            jobs.remove(j)
        ready = [j for j in jobs if j[1] > 0]
        if not ready:
            timeline.append(None)
            continue
        key = (lambda j: (tasks[j[0]][1], j[0])) if policy == "RM" else (lambda j: (j[2], j[0]))
        j = min(ready, key=key)
        j[1] -= 1
        timeline.append(j[0])
        jobs = [x for x in jobs if x[1] > 0]
    return timeline, misses


def avg_current(duty, i_on, i_off):
    """Dòng trung bình với tỉ lệ thức duty: duty·i_on + (1 − duty)·i_off."""
    return duty * i_on + (1 - duty) * i_off


# ───────── Ngôn ngữ lập trình (PLC): từ tố, phân tích đệ quy xuống, cây cú pháp, phạm vi, kiểu, bao đóng, bộ nhớ, máy ngăn xếp ─────────
PLC_TOKENS = [("SO", r"\d+"), ("TEN", r"[A-Za-z_]\w*"), ("PHEP", r"==|<=|>=|[-+*/=<>()]"), ("CACH", r"\s+")]
PLC_KEYWORDS = {"if", "while", "return", "def"}


def lex(src):
    """Phân tích từ vựng theo luật khớp dài nhất, thử các mẫu theo thứ tự PLC_TOKENS. Trả [(loại, chữ)], bỏ khoảng trắng.
    Tên trùng từ khoá → loại 'KHOA'. Ký tự lạ → ('LOI', ký tự)."""
    import re
    out, i = [], 0
    while i < len(src):
        best = None
        for kind, pat in PLC_TOKENS:
            m = re.compile(pat).match(src, i)
            if m and (best is None or len(m.group()) > len(best[1])):
                best = (kind, m.group())
        if best is None:
            out.append(("LOI", src[i]))
            i += 1
            continue
        i += len(best[1])
        if best[0] == "CACH":
            continue
        out.append(("KHOA", best[1]) if best[0] == "TEN" and best[1] in PLC_KEYWORDS else best)
    return out


def parse_expr(src, assoc="left"):
    """Đệ quy xuống: expr → term ((+|−) term)*, term → atom ((*|/) atom)*, atom → số | tên | ( expr ).
    assoc='right' dựng cây kết hợp phải (để so sánh). Trả cây dạng bộ (phép, trái, phải); lá là int hoặc tên (str)."""
    ts = [t for _, t in lex(src)]
    pos = [0]

    def peek():
        return ts[pos[0]] if pos[0] < len(ts) else None

    def eat():
        pos[0] += 1
        return ts[pos[0] - 1]

    def atom():
        t = eat()
        if t == "(":
            v = expr()
            eat()
            return v
        return int(t) if t.isdigit() else t

    def chain(sub, ops):
        items, opl = [sub()], []
        while peek() in ops:
            opl.append(eat())
            items.append(sub())
        if assoc == "left":
            v = items[0]
            for op, it in zip(opl, items[1:]):
                v = (op, v, it)
            return v
        v = items[-1]
        for op, it in zip(reversed(opl), reversed(items[:-1])):
            v = (op, it, v)
        return v

    def term():
        return chain(atom, ("*", "/"))

    def expr():
        return chain(term, ("+", "-"))

    return expr()


def ast_eval(t, env=None):
    """Đánh giá cây: phép chia là chia nguyên lấy phần nguyên về 0 như C. Tên tra trong env."""
    if isinstance(t, int):
        return t
    if isinstance(t, str):
        return (env or {})[t]
    a, b = ast_eval(t[1], env), ast_eval(t[2], env)
    return {"+": a + b, "-": a - b, "*": a * b, "/": int(a / b) if b else None}[t[0]]


def ast_str(t):
    """Cây → chuỗi tiền tố “(+ 1 (* 2 3))”."""
    if not isinstance(t, tuple):
        return str(t)
    return f"({t[0]} {ast_str(t[1])} {ast_str(t[2])})"


def scope_lookup(mode, gx=1, lx=2):
    """Trình thông dịch tí hon: x = gx toàn cục; f() trả x; g() đặt x = lx cục bộ rồi gọi f(). Trả giá trị f() thấy được.
    'static': tra từ môi trường nơi f được ĐỊNH NGHĨA; 'dynamic': tra theo chuỗi lời GỌI."""
    glob = {"vars": {"x": gx}, "up": None}

    def look(env, k):
        while env is not None:
            if k in env["vars"]:
                return env["vars"][k]
            env = env["up"]
        raise NameError(k)

    def call_f(caller):
        return look({"vars": {}, "up": glob if mode == "static" else caller}, "x")

    g_env = {"vars": {"x": lx}, "up": glob}
    return call_f(g_env)


def shadow_late():
    """Phạm vi tĩnh chọn BIẾN, không chụp GIÁ TRỊ: inner đọc y của outer lúc được gọi (y đã đổi thành 20) → 21."""
    def outer():
        y = 10

        def inner():
            return y + 1
        y = 20
        return inner()
    return outer()


def unbound_local():
    """Gán x ở bất kỳ đâu trong hàm làm x thành biến cục bộ của CẢ hàm: đọc trước khi gán → lỗi. Trả tên lỗi."""
    src = "x = 1\ndef h():\n    y = x + 1\n    x = 5\n    return y\nh()\n"
    try:
        exec(src, {})
    except Exception as e:  # noqa: BLE001
        return type(e).__name__
    return None


def unify(a, b, s=None):
    """Hợp nhất hai kiểu. Kiểu: 'int', 'bool', biến kiểu bắt đầu bằng "'" (như "'a"), hoặc hàm ('->', đối, kết quả).
    Trả từ điển thế (biến → kiểu) hoặc None nếu không hợp nhất được (kể cả kiểm tra xuất hiện)."""
    s = dict(s or {})

    def walk(t):
        while isinstance(t, str) and t.startswith("'") and t in s:
            t = s[t]
        return t

    def occurs(v, t):
        t = walk(t)
        return t == v or (isinstance(t, tuple) and any(occurs(v, x) for x in t[1:]))

    a, b = walk(a), walk(b)
    if a == b:
        return s
    if isinstance(a, str) and a.startswith("'"):
        return None if occurs(a, b) else {**s, a: b}
    if isinstance(b, str) and b.startswith("'"):
        return unify(b, a, s)
    if isinstance(a, tuple) and isinstance(b, tuple) and a[0] == b[0] and len(a) == len(b):
        for x, y in zip(a[1:], b[1:]):
            s = unify(x, y, s)
            if s is None:
                return None
        return s
    return None


def resolve(t, s):
    """Áp dụng thế s cho kiểu t tới khi không đổi."""
    while isinstance(t, str) and t in s:
        t = s[t]
    if isinstance(t, tuple):
        return (t[0],) + tuple(resolve(x, s) for x in t[1:])
    return t


def py_add_error(a="3", b=1):
    """Chạy a + b thật trong Python; trả tên lỗi nếu có, không thì kết quả."""
    try:
        return a + b
    except Exception as e:  # noqa: BLE001
        return type(e).__name__


def sharing_demo():
    """Chạy thật các ví dụ truyền tham số kiểu “chia sẻ đối tượng” của Python. Trả từ điển kết quả."""
    src = (
        "def them(ds): ds.append(1)\n"
        "def gan_lai(ds): ds = [9]\n"
        "def doi_cho(a, b): a, b = b, a\n"
        "def bad(x, acc=[]):\n    acc.append(x)\n    return acc\n"
        "def good(x, acc=None):\n    acc = [] if acc is None else acc\n    acc.append(x)\n    return acc\n"
        "a = [0]; them(a)\n"
        "b = [0]; gan_lai(b)\n"
        "p, q = 1, 2; doi_cho(p, q)\n"
        "r1 = bad(1); r2 = bad(2)\n"
        "g1 = good(1); g2 = good(2)\n"
    )
    env = {}
    exec(src, env)
    return {"them": env["a"], "gan_lai": env["b"], "doi_cho": (env["p"], env["q"]), "bad": (env["r1"], env["r2"]),
            "bad_same": env["r1"] is env["r2"], "good": (env["g1"], env["g2"])}


def make_counter():
    """Bao đóng: mỗi lần gọi tạo biến n riêng; hàm trả về tăng n rồi trả n."""
    n = 0

    def inc():
        nonlocal n
        n += 1
        return n

    return inc


def late_binding(k=3):
    """Bao đóng tạo trong vòng lặp cùng giữ biến i: gọi sau vòng lặp ra giá trị cuối. Trả (bắt muộn, bắt sớm bằng đối mặc định)."""
    late = [lambda: i for i in range(k)]
    early = [lambda i=i: i for i in range(k)]
    return [f() for f in late], [f() for f in early]


def mark_sweep(heap, roots):
    """Đánh dấu từ gốc theo cạnh tham chiếu; trả (tập sống, tập bị thu hồi)."""
    live, st = set(), list(roots)
    while st:
        v = st.pop()
        if v not in live:
            live.add(v)
            st += heap[v]
    return live, set(heap) - live


def ref_counts(heap, roots):
    """Số tham chiếu tới mỗi đối tượng (gốc tính là một tham chiếu)."""
    c = {k: sum(vs.count(k) for vs in heap.values()) for k in heap}
    for r in roots:
        c[r] += 1
    return c


def refcount_free(heap, roots):
    """Đếm tham chiếu: thu hồi dây chuyền mọi đối tượng có số tham chiếu 0 (giảm số của các đối tượng nó trỏ tới). Trả tập bị thu hồi."""
    c = ref_counts(heap, roots)
    freed, todo = set(), [k for k, v in c.items() if v == 0]
    while todo:
        k = todo.pop()
        if k in freed:
            continue
        freed.add(k)
        for t in heap[k]:
            c[t] -= 1
            if c[t] == 0:
                todo.append(t)
    return freed


def stack_gen(t, out=None):
    """Sinh mã máy ngăn xếp theo duyệt sau: con trái, con phải, phép. Lá số → ('push', số); tên → ('load', tên)."""
    out = [] if out is None else out
    if isinstance(t, int):
        out.append(("push", t))
    elif isinstance(t, str):
        out.append(("load", t))
    else:
        stack_gen(t[1], out)
        stack_gen(t[2], out)
        out.append(({"+": "add", "-": "sub", "*": "mul", "/": "div"}[t[0]],))
    return out


def stack_vm(code, env=None, trace=False):
    """Chạy mã ngăn xếp: phép hai ngôi lấy b (đỉnh) trước, a sau, đẩy a ∘ b. Trả ngăn xếp cuối (và vết nếu trace)."""
    s, tr = [], []
    for ins in code:
        if ins[0] == "push":
            s.append(ins[1])
        elif ins[0] == "load":
            s.append((env or {})[ins[1]])
        else:
            b, a = s.pop(), s.pop()
            s.append({"add": a + b, "sub": a - b, "mul": a * b, "div": int(a / b)}[ins[0]])
        tr.append(list(s))
    return (s, tr) if trace else s


def const_fold(t):
    """Gấp hằng số từ dưới lên: nút có hai con đều là số thì tính luôn; còn tên thì giữ nguyên."""
    if not isinstance(t, tuple):
        return t
    a, b = const_fold(t[1]), const_fold(t[2])
    if isinstance(a, int) and isinstance(b, int):
        return ast_eval((t[0], a, b))
    return (t[0], a, b)



# ───────── Phần mềm đúng đắn (SWF): đặc tả, bất biến, biên, kiểm thử, độ phủ, máy trạng thái, hợp nhất ba chiều, đo đạc ─────────
def bin_search(a, x):
    """Tìm kiếm nhị phân trên khoảng nửa mở [lo, hi). Tiền điều kiện: a sắp tăng. Trả (vị trí hoặc −1, vết [(lo, hi, mid)])."""
    lo, hi, tr = 0, len(a), []
    while lo < hi:
        mid = lo + (hi - lo) // 2
        tr.append((lo, hi, mid))
        if a[mid] == x:
            return mid, tr
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return -1, tr


def sum_loop_invariant(n):
    """Vòng s = 0; for i in 0..n−1: s += i. Trả danh sách (i, s) trước mỗi vòng và sau vòng cuối — để kiểm s = i(i − 1)/2."""
    s, out = 0, []
    for i in range(n):
        out.append((i, s))
        s += i
    out.append((n, s))
    return out


def euclid_trace(a, b):
    """Euclid: (a, b) → (b, a mod b) tới khi b = 0. Trả dãy các cặp; b giảm thật sự và ≥ 0 nên dừng."""
    tr = [(a, b)]
    while b:
        a, b = b, a % b
        tr.append((a, b))
    return tr


def mixed_search(a, x, max_steps=100):
    """Lỗi trộn hai kiểu khoảng: khởi tạo nửa mở hi = len(a) và cập nhật hi = mid, nhưng điều kiện vòng kiểu đóng lo <= hi.
    Trả 'IndexError', 'vô hạn' (quá max_steps vòng), hoặc kết quả."""
    lo, hi, k = 0, len(a), 0
    while lo <= hi:
        k += 1
        if k > max_steps:
            return "vô hạn"
        mid = (lo + hi) // 2
        if mid >= len(a):
            return "IndexError"
        if a[mid] == x:
            return mid
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return -1


def halving_steps(x=1.0):
    """Đếm số lần chia đôi một số thực dương (IEEE 754 nhị phân 64 bit) tới khi bị làm tròn về 0."""
    n = 0
    while x > 0:
        x /= 2
        n += 1
    return n


def deadlock_states(order_a, order_b):
    """Kiểm mô hình hai luồng: mỗi luồng lấy các khoá theo thứ tự cho trước rồi nhả theo thứ tự ngược. Duyệt mọi trạng thái đi tới được;
    trả số trạng thái mà cả hai luồng đều chưa xong và không luồng nào đi tiếp được (bế tắc)."""
    progs = [[("lay", k) for k in o] + [("nha", k) for k in reversed(o)] for o in (order_a, order_b)]
    start = (0, 0, frozenset())
    seen, stack, dead = {start}, [start], 0
    while stack:
        pa, pb, held = stack.pop()
        moves = []
        for t, pc in ((0, pa), (1, pb)):
            if pc == len(progs[t]):
                continue
            op, k = progs[t][pc]
            if op == "lay" and any(h[0] == k for h in held):
                continue
            nh = held | {(k, t)} if op == "lay" else held - {(k, t)}
            moves.append((pa + 1, pb, frozenset(nh)) if t == 0 else (pa, pb + 1, frozenset(nh)))
        if not moves and (pa < len(progs[0]) or pb < len(progs[1])):
            dead += 1
        for m in moves:
            if m not in seen:
                seen.add(m)
                stack.append(m)
    return dead


def wrap32(x):
    """Số nguyên có dấu 32 bit quay vòng (bù hai)."""
    return (x + 2 ** 31) % 2 ** 32 - 2 ** 31


def mid32(lo, hi, safe):
    """Điểm giữa trong số học 32 bit: safe=False → (lo + hi) / 2 (tổng có thể tràn); safe=True → lo + (hi − lo) / 2."""
    if safe:
        return wrap32(lo + wrap32(hi - lo) // 2)
    return int(wrap32(lo + hi) / 2)


def triangle(a, b, c):
    """Phân loại tam giác theo độ dài cạnh nguyên dương: 'không phải', 'đều', 'cân', 'thường' (bất đẳng thức tam giác chặt)."""
    x, y, z = sorted((a, b, c))
    if x <= 0 or x + y <= z:
        return "không phải"
    if x == z:
        return "đều"
    if x == y or y == z:
        return "cân"
    return "thường"


def triangle_buggy(a, b, c):
    """Bản LỖI LỆCH MỘT ở biên: dùng x + y < z thay cho x + y <= z, nên (1, 2, 3) bị coi là tam giác."""
    x, y, z = sorted((a, b, c))
    if x <= 0 or x + y < z:
        return "không phải"
    if x == z:
        return "đều"
    if x == y or y == z:
        return "cân"
    return "thường"


def branch_path_cover(n_ifs, tests):
    """n câu if độc lập; mỗi ca kiểm là bộ n giá trị đúng/sai. Trả (số nhánh đã phủ / 2n, số đường đã phủ / 2^n)."""
    br = {(i, t[i]) for t in tests for i in range(n_ifs)}
    paths = {tuple(t) for t in tests}
    return len(br), 2 * n_ifs, len(paths), 2 ** n_ifs


def find_counterexample(prop, cases):
    """Kiểm tính chất trên mọi ca; trả ca đầu tiên làm tính chất sai, hoặc None."""
    for c in cases:
        if not prop(c):
            return c
    return None


def bst_local_ok(t):
    """Kiểm SAI (chỉ con trực tiếp): t = (khoá, trái, phải) hoặc None."""
    if t is None:
        return True
    k, l, r = t
    if l is not None and l[0] >= k:
        return False
    if r is not None and r[0] <= k:
        return False
    return bst_local_ok(l) and bst_local_ok(r)


def bst_ok(t, lo=None, hi=None):
    """Kiểm ĐÚNG: mọi khoá trong cây con trái < khoá gốc < mọi khoá cây con phải (truyền khoảng [lo, hi] xuống)."""
    if t is None:
        return True
    k, l, r = t
    if (lo is not None and k <= lo) or (hi is not None and k >= hi):
        return False
    return bst_ok(l, lo, k) and bst_ok(r, k, hi)


def inorder(t):
    return [] if t is None else inorder(t[1]) + [t[0]] + inorder(t[2])


def heap_ok(a):
    """Đống nhỏ nhất trên mảng: a[(i − 1) // 2] ≤ a[i] với mọi i ≥ 1."""
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))


TRAFFIC = {("ĐỎ", "hết giờ"): "XANH", ("XANH", "hết giờ"): "VÀNG", ("XANH", "bấm nút"): "VÀNG", ("VÀNG", "hết giờ"): "ĐỎ",
           ("ĐỎ", "bấm nút"): "ĐỎ", ("VÀNG", "bấm nút"): "VÀNG"}


def fsm_run(delta, start, events, error="LỖI"):
    """Chạy máy trạng thái; sự kiện không có trong bảng → trạng thái lỗi tường minh (dừng ở đó). Trả dãy trạng thái."""
    s, out = start, [start]
    for e in events:
        s = delta.get((s, e), error) if s != error else error
        out.append(s)
    return out


def merge3(base, a, b):
    """Hợp nhất ba chiều từng dòng (cùng số dòng): chỉ một bên đổi → lấy bên đổi; hai bên đổi giống nhau → lấy; khác nhau → XUNG ĐỘT."""
    out = []
    for o, x, y in zip(base, a, b):
        if x == y:
            out.append(x)
        elif x == o:
            out.append(y)
        elif y == o:
            out.append(x)
        else:
            out.append(("XUNG ĐỘT", x, y))
    return out


def paired_ci(a, b, z=1.96):
    """Ghép cặp: d_i = a_i − b_i. Trả (trung bình d, sai số chuẩn s/√n, cận dưới, cận trên) với s độ lệch chuẩn mẫu (chia n − 1)."""
    d = [x - y for x, y in zip(a, b)]
    n = len(d)
    m = sum(d) / n
    s = math.sqrt(sum((x - m) ** 2 for x in d) / (n - 1))
    se = s / math.sqrt(n)
    return m, se, m - z * se, m + z * se


def run_error(src):
    """Chạy đoạn mã Python; trả tên lỗi nếu có, không thì None."""
    try:
        exec(src, {})
    except Exception as e:  # noqa: BLE001
        return type(e).__name__
    return None


def perf_data(seed=7, n=30):
    """Số liệu đo giả lập tái lập được: n bộ dữ liệu cỡ khác nhau; thời gian (ms) của A và B trên CÙNG bộ. B nhanh hơn A khoảng 4%,
    cỡ bộ dữ liệu làm thời gian dao động lớn hơn nhiều so với khác biệt A − B. Làm tròn 1 chữ số thập phân."""
    import random
    r = random.Random(seed)
    a, b = [], []
    for _ in range(n):
        base = r.uniform(80, 220)
        a.append(round(base * r.gauss(1.00, 0.01), 1))
        b.append(round(base * r.gauss(0.96, 0.01), 1))
    return a, b


def unpaired_ci(a, b, z=1.96):
    """Không ghép cặp: hiệu hai trung bình, sai số chuẩn √(s_a²/n + s_b²/n)."""
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a) / (n - 1)
    vb = sum((x - mb) ** 2 for x in b) / (n - 1)
    se = math.sqrt(va / n + vb / n)
    return ma - mb, se, ma - mb - z * se, ma - mb + z * se


def overflow_sim(inp, bufsize=8, checked=False):
    """Mô hình bộ nhớ: mảng ký tự buf[bufsize] nằm ngay trước một byte cờ is_admin = 0. Chép chuỗi inp + ký tự kết thúc 0.
    checked=False: chép không kiểm độ dài (như strcpy); True: cắt còn bufsize − 1 ký tự + 0. Trả (giá trị byte cờ, số byte tràn)."""
    mem = bytearray(bufsize + 16)
    data = inp.encode() + b"\x00"
    if checked:
        data = inp.encode()[:bufsize - 1] + b"\x00"
    for i, ch in enumerate(data):
        mem[i] = ch
    return mem[bufsize], max(0, len(data) - bufsize)


def sql_concat_error(user):
    """Ghép chuỗi đầu vào hợp lệ có dấu nháy vào câu truy vấn: trả tên lỗi (nếu có) và số dòng của bản tham số hoá."""
    import sqlite3
    con = sqlite3.connect(":memory:")
    con.executescript("CREATE TABLE users(name TEXT); INSERT INTO users VALUES ('alice'),('bob'),('O''Brien');")
    try:
        con.execute("SELECT name FROM users WHERE name = '" + user + "'").fetchall()
        err = None
    except sqlite3.Error as e:
        err = type(e).__name__
    n = len(con.execute("SELECT name FROM users WHERE name = ?", (user,)).fetchall())
    con.close()
    return err, n


def sql_concat_vs_param(user):
    """Bảng users (alice, bob). Ghép chuỗi: SELECT … WHERE name = '<user>' → số dòng; tham số hoá → số dòng."""
    import sqlite3
    con = sqlite3.connect(":memory:")
    con.executescript("CREATE TABLE users(name TEXT, pw TEXT); INSERT INTO users VALUES ('alice','a1'),('bob','b2');")
    q1 = "SELECT name FROM users WHERE name = '" + user + "'"
    r1 = con.execute(q1).fetchall()
    r2 = con.execute("SELECT name FROM users WHERE name = ?", (user,)).fetchall()
    con.close()
    return q1, len(r1), len(r2)



# ───────── Hệ phân tán (DSY): đồng hồ lôgic, vector, đại biểu, đồng thuận, băm nhất quán, MapReduce, luồng, Bloom, hồ chứa, cột, 2PC ─────────
def lamport_run(events):
    """events: danh sách (tiến trình, loại, nhãn thông điệp) theo thứ tự thực hiện thật; loại ∈ {'local', 'send', 'recv'}.
    Luật Lamport: local/send: C ← C + 1; recv: C ← max(C, nhãn gửi) + 1. Trả danh sách nhãn thời gian theo thứ tự events."""
    clock, sent, out = {}, {}, []
    for p, kind, msg in events:
        c = clock.get(p, 0)
        if kind == "recv":
            c = max(c, sent[msg]) + 1
        else:
            c = c + 1
        clock[p] = c
        if kind == "send":
            sent[msg] = c
        out.append(c)
    return out


def vector_run(events, procs):
    """Như lamport_run nhưng đồng hồ vector: tiến trình i tăng thành phần i; nhận thì lấy max từng thành phần rồi tăng thành phần mình."""
    idx = {p: i for i, p in enumerate(procs)}
    vc = {p: [0] * len(procs) for p in procs}
    sent, out = {}, []
    for p, kind, msg in events:
        v = vc[p]
        if kind == "recv":
            v = [max(a, b) for a, b in zip(v, sent[msg])]
        v = list(v)
        v[idx[p]] += 1
        vc[p] = v
        if kind == "send":
            sent[msg] = tuple(v)
        out.append(tuple(v))
    return out


def vc_compare(u, v):
    """'trước' nếu u xảy ra trước v (u ≤ v từng thành phần và u ≠ v); 'sau'; 'bằng'; 'đồng thời' nếu không so được."""
    le = all(a <= b for a, b in zip(u, v))
    ge = all(a >= b for a, b in zip(u, v))
    if le and ge:
        return "bằng"
    if le:
        return "trước"
    if ge:
        return "sau"
    return "đồng thời"


def quorum_overlap(n, r, w):
    """Mọi tập đọc cỡ r và mọi tập ghi cỡ w trong n bản sao có giao nhau không (vét cạn)."""
    import itertools as it
    return all(set(a) & set(b) for a in it.combinations(range(n), r) for b in it.combinations(range(n), w))


def majority_tolerance(n):
    """Đồng thuận đa số trên n nút: cỡ đa số ⌊n/2⌋ + 1 và số nút hỏng chịu được n − đa số."""
    m = n // 2 + 1
    return m, n - m


def mod_moved(n_old, n_new, keys=100000):
    """Tỉ lệ khoá đổi nút khi băm k mod N đổi từ n_old sang n_new."""
    return sum(1 for k in range(keys) if k % n_old != k % n_new) / keys


def _h(s):
    import hashlib
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def ring_owner_fn(nodes, vnodes=200):
    """Vòng băm nhất quán với vnodes nút ảo mỗi nút (băm md5). Trả hàm khoá → nút."""
    import bisect as bs
    pts = sorted((_h(f"{n}#{i}"), n) for n in nodes for i in range(vnodes))
    hs = [p[0] for p in pts]

    def owner(k):
        i = bs.bisect(hs, _h(str(k)))
        return pts[i % len(pts)][1]
    return owner


def ring_moved(n_old, n_new, keys=20000, vnodes=200):
    a, b = ring_owner_fn(range(n_old), vnodes), ring_owner_fn(range(n_new), vnodes)
    return sum(1 for k in range(keys) if a(k) != b(k)) / keys


def word_count(lines, combine=False):
    """MapReduce đếm từ. Mỗi dòng là một tác vụ map; combine=True gộp cục bộ trước khi xáo trộn.
    Trả (kết quả, số cặp (từ, số) gửi qua mạng ở bước xáo trộn)."""
    from collections import Counter
    shuffled = []
    for line in lines:
        pairs = [(w, 1) for w in line.split()]
        if combine:
            pairs = list(Counter(w for w, _ in pairs).items())
        shuffled += pairs
    res = Counter()
    for w, c in shuffled:
        res[w] += c
    return dict(res), len(shuffled)


def tumbling(times, size):
    """Cửa sổ nhảy cỡ `size`: đếm sự kiện theo [k·size, (k+1)·size)."""
    from collections import Counter
    return dict(sorted(Counter(t // size for t in times).items()))


def stream_windows(arrivals, size, lateness):
    """Cửa sổ nhảy theo thời gian SỰ KIỆN với mốc nước = (thời gian sự kiện lớn nhất đã thấy) − lateness. arrivals: thời gian sự kiện theo
    thứ tự ĐẾN. Cửa sổ [k·size, (k+1)·size) đóng (xuất kết quả) khi mốc nước ≥ (k+1)·size; sự kiện tới sau khi cửa sổ của nó đã đóng bị bỏ.
    Trả (kết quả {k: số sự kiện} theo thứ tự đóng, danh sách sự kiện bị bỏ, vị trí đến lúc mỗi cửa sổ đóng)."""
    from collections import Counter
    open_w, closed, dropped, when = Counter(), {}, [], {}
    wm = None
    for i, t in enumerate(arrivals):
        k = t // size
        if k in closed:
            dropped.append(t)
        else:
            open_w[k] += 1
        mx = t if wm is None else max(wm + lateness, t)
        wm = mx - lateness
        for kk in sorted(list(open_w)):
            if wm >= (kk + 1) * size:
                closed[kk] = open_w.pop(kk)
                when[kk] = i
    for kk in sorted(open_w):
        closed[kk] = open_w[kk]
        when[kk] = None
    return closed, dropped, when


def bloom_fp(m_per_n, k):
    """Xấp xỉ tỉ lệ dương tính giả của bộ lọc Bloom: (1 − e^(−k·n/m))^k với m/n bit mỗi phần tử."""
    return (1 - math.exp(-k / m_per_n)) ** k


def bloom_sim(n=1000, bits_per=10, k=7, probes=200000, seed=1):
    """Bộ lọc Bloom thật: chèn n khoá, đo tỉ lệ dương tính giả trên `probes` khoá không có; kiểm không có âm tính giả."""
    m = n * bits_per
    bits = bytearray(m)

    def idx(x):
        h1, h2 = _h(f"a{x}"), _h(f"b{x}")
        return [(h1 + i * h2) % m for i in range(k)]
    for x in range(n):
        for j in idx(x):
            bits[j] = 1
    fn = sum(1 for x in range(n) if not all(bits[j] for j in idx(x)))
    fp = sum(1 for x in range(n, n + probes) if all(bits[j] for j in idx(x)))
    return fp / probes, fn


def kmv_estimate(items, k=256):
    """Đếm số phần tử khác nhau bằng k giá trị băm nhỏ nhất (KMV): băm mỗi phần tử về [0, 1), giữ k giá trị nhỏ nhất KHÁC NHAU;
    ước lượng (k − 1) / (giá trị nhỏ thứ k). Bộ nhớ chỉ k số, không phụ thuộc số phần tử."""
    import heapq as hq
    top, seen = [], set()
    for x in items:
        v = _h(f"kmv{x}") / 2 ** 128
        if v in seen:
            continue
        if len(top) < k:
            hq.heappush(top, -v)
            seen.add(v)
        elif v < -top[0]:
            seen.discard(-hq.heappushpop(top, -v))
            seen.add(v)
    if len(top) < k:
        return len(top)
    return (k - 1) / (-top[0])


def reservoir_exact(n, k, off=0):
    """Xác suất chính xác (Fraction) mỗi phần tử còn trong hồ chứa cỡ k sau luồng n phần tử (thuật toán R: phần tử thứ i > k được nhận
    với xác suất k/i, thay một ô ngẫu nhiên). off ≠ 0 mô phỏng lỗi lệch một: nhận với xác suất k/(i + off)."""
    from fractions import Fraction as Fr
    ps = []
    for i in range(1, n + 1):
        p = Fr(1) if i <= k else Fr(k, i + off)
        for j in range(max(i, k) + 1, n + 1):
            p *= 1 - Fr(k, j + off) * Fr(1, k)
        ps.append(p)
    return ps


def rle(col):
    """Nén theo loạt: [(giá trị, số lần lặp liền nhau)]."""
    out = []
    for v in col:
        if out and out[-1][0] == v:
            out[-1] = (v, out[-1][1] + 1)
        else:
            out.append((v, 1))
    return out


def two_phase(votes, coordinator_alive=True):
    """Cam kết hai pha: votes = phiếu của các bên ('có'/'không'). Trả quyết định 'cam kết'/'huỷ', hoặc 'chờ' cho bên đã bỏ 'có'
    khi bên điều phối chết trước khi gửi quyết định."""
    if not coordinator_alive:
        return ["chờ" if v == "có" else "huỷ" for v in votes]
    d = "cam kết" if all(v == "có" for v in votes) else "huỷ"
    return [d] * len(votes)


def deliver(msgs, dedupe):
    """Giao ít nhất một lần (có thể lặp). dedupe=True: người nhận nhớ mã thông điệp đã xử lý. Trả tổng số tiền cộng vào tài khoản."""
    seen, total = set(), 0
    for mid, amount in msgs:
        if dedupe and mid in seen:
            continue
        seen.add(mid)
        total += amount
    return total



# ───────── Khoa học dữ liệu (DSC): thang đo, nối bảng, thiếu dữ liệu, thống kê bền vững, tương quan, Simpson, A/B, kiểm định nhiều lần,
#           rò rỉ, tỉ lệ nền, đa cộng tuyến, k-ẩn danh ─────────
def sample_var(a):
    """Phương sai mẫu (chia n − 1)."""
    m = sum(a) / len(a)
    return sum((x - m) ** 2 for x in a) / (len(a) - 1)


def pearson(x, y):
    """Hệ số tương quan Pearson."""
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))


def join_rows(left, right, key=0):
    """Nối trong (inner join) hai danh sách bộ theo cột khoá; trả danh sách bộ ghép."""
    return [l + r[:key] + r[key + 1:] for l in left for r in right if l[key] == r[key]]


def median(a):
    s = sorted(a)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def quartiles(a):
    """Q1, Q3 theo nội suy tuyến tính (cách mặc định của numpy.percentile)."""
    import numpy as np
    return float(np.percentile(a, 25)), float(np.percentile(a, 75))


def iqr_outliers(a, k=1.5):
    """Ngoại lai theo quy tắc Tukey: ngoài [Q1 − k·IQR, Q3 + k·IQR]."""
    q1, q3 = quartiles(a)
    lo, hi = q1 - k * (q3 - q1), q3 + k * (q3 - q1)
    return [x for x in a if x < lo or x > hi], (lo, hi)


def ab_sample_size(p1, p2, alpha=0.05, power=0.8):
    """Cỡ mẫu mỗi nhóm cho kiểm định hai tỉ lệ (hai phía), công thức xấp xỉ chuẩn."""
    from statistics import NormalDist
    za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p1 - p2) ** 2)


def peeking_fpr(n_max=1000, looks=10, sims=4000, seed=3):
    """Mô phỏng nhìn trộm: hai nhóm GIỐNG HỆT nhau (p = 0,1), kiểm z hai tỉ lệ sau mỗi n_max/looks người, dừng ngay khi p < 0,05.
    Trả (tỉ lệ dương tính giả khi nhìn trộm, khi chỉ kiểm một lần cuối)."""
    import random
    from statistics import NormalDist
    r = random.Random(seed)
    z = NormalDist().inv_cdf(0.975)
    step = n_max // looks
    peek = final = 0
    for _ in range(sims):
        a = b = 0
        hit = False
        for k in range(1, looks + 1):
            a += sum(r.random() < 0.1 for _ in range(step))
            b += sum(r.random() < 0.1 for _ in range(step))
            n = k * step
            p = (a + b) / (2 * n)
            se = math.sqrt(2 * p * (1 - p) / n) if 0 < p < 1 else 0
            sig = se > 0 and abs(a - b) / n / se > z
            if sig and not hit:
                hit = True
            if k == looks and sig:
                final += 1
        peek += hit
    return peek / sims, final / sims


def leak_demo(n=60, p=2000, k=10, seed=0, reps=50):
    """Rò rỉ khi chọn đặc trưng: dữ liệu NHIỄU THUẦN (nhãn ngẫu nhiên, đặc trưng ngẫu nhiên, không liên quan gì). Chia đôi huấn luyện/kiểm tra.
    Chọn k đặc trưng tương quan mạnh nhất với nhãn trên (a) CẢ tập — rò rỉ, hoặc (b) chỉ tập huấn luyện — đúng; phân loại bằng dấu của tổng
    các đặc trưng đã đổi dấu theo tương quan. Trả độ chính xác trung bình trên tập kiểm tra qua `reps` lần: (rò rỉ, đúng)."""
    import numpy as np
    rng = np.random.default_rng(seed)
    acc_leak, acc_ok = [], []
    for _ in range(reps):
        X = rng.standard_normal((n, p))
        y = rng.choice([-1.0, 1.0], n)
        tr, te = np.arange(n // 2), np.arange(n // 2, n)

        def fit(idx):
            c = (X[idx] * y[idx, None]).mean(axis=0)
            top = np.argsort(-np.abs(c))[:k]
            return top, np.sign(c[top])

        for idx, out in ((np.arange(n), acc_leak), (tr, acc_ok)):
            top, sg = fit(idx)
            pred = np.sign(X[te][:, top] @ sg)
            out.append(float((pred == y[te]).mean()))
    return round(sum(acc_leak) / reps, 3), round(sum(acc_ok) / reps, 3)


def collinear_demo(n=40, rho=0.9, seed=4):
    """Hai biến giải thích tương quan ≈ rho; y = x1 + x2 + nhiễu. Khớp hồi quy tuyến tính (có hệ số chặn) trên hai nửa dữ liệu khác nhau.
    Trả (r mẫu giữa x1 và x2, hệ số (b1, b2) nửa đầu, nửa sau) — làm tròn 2 chữ số."""
    import numpy as np
    rng = np.random.default_rng(seed)
    x1 = rng.standard_normal(2 * n)
    x2 = rho * x1 + math.sqrt(1 - rho * rho) * rng.standard_normal(2 * n)
    y = x1 + x2 + rng.standard_normal(2 * n)
    out = []
    for sl in (slice(0, n), slice(n, 2 * n)):
        A = np.column_stack([np.ones(n), x1[sl], x2[sl]])
        b = np.linalg.lstsq(A, y[sl], rcond=None)[0]
        out.append((round(float(b[1]), 2), round(float(b[2]), 2)))
    return round(float(np.corrcoef(x1, x2)[0, 1]), 2), out[0], out[1]


def ppv(sens, spec, prev):
    """Giá trị dự đoán dương P(bệnh | dương tính) theo định lý Bayes."""
    return sens * prev / (sens * prev + (1 - spec) * (1 - prev))


def vif_two(r):
    """Hệ số phóng đại phương sai khi chỉ có hai biến giải thích tương quan r: 1 / (1 − r²)."""
    return 1 / (1 - r * r)


def k_anonymity(rows, quasi):
    """k nhỏ nhất: số lần xuất hiện ít nhất của một tổ hợp các cột định danh gián tiếp."""
    from collections import Counter
    return min(Counter(tuple(r[i] for i in quasi) for r in rows).values())



# ───────── Kỹ thuật lập trình & mẫu thiết kế (SDP): mọi ví dụ là mã Python chạy thật, trả con số đưa lên màn hình ─────────
def mccabe(src):
    """Độ phức tạp vòng McCabe của MỘT hàm: số điểm rẽ + 1. Điểm rẽ: if/elif, for, while, except, biểu thức if,
    mỗi toán tử and/or thêm (số vế − 1), mỗi điều kiện if trong bộ sinh. Đếm trên cây cú pháp ast của Python."""
    import ast
    d = 0
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.IfExp, ast.AsyncFor)):
            d += 1
        elif isinstance(node, ast.BoolOp):
            d += len(node.values) - 1
        elif isinstance(node, ast.comprehension):
            d += len(node.ifs)
    return d + 1


def parse_prefix(s):
    """Đọc số nguyên ở đầu chuỗi, DỪNG ÂM THẦM ở kí tự lạ (kiểu atoi của C): “12a” → 12."""
    n = 0
    for ch in s:
        if not ch.isdigit():
            break
        n = n * 10 + int(ch)
    return n


def int_or_error(s):
    """int() của Python: thất bại sớm, trả tên ngoại lệ nếu lỗi."""
    try:
        return int(s)
    except ValueError as e:
        return type(e).__name__


class Account:
    """Tài khoản với bất biến số dư ≥ 0: chỉ đổi số dư qua nap/rut, rút quá số dư thì báo lỗi."""
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError("số dư âm")
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def nap(self, x):
        if x <= 0:
            raise ValueError("số tiền phải dương")
        self._balance += x

    def rut(self, x):
        if x <= 0 or x > self._balance:
            raise ValueError("không đủ số dư")
        self._balance -= x


def account_demo():
    """Rút 150 từ 100 qua phương thức → lỗi; gán thẳng trường công khai → số dư −50 lọt vào."""
    a = Account(100)
    try:
        a.rut(150)
        guarded = a.balance
    except ValueError:
        guarded = "ValueError"

    class Naked:
        balance = 100
    n = Naked()
    n.balance -= 150
    return guarded, n.balance


class Shape:
    def area(self):
        raise NotImplementedError


class Rect(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2


class Triangle(Shape):
    def __init__(self, b, h):
        self.b, self.h = b, h

    def area(self):
        return self.b * self.h / 2


def total_area(shapes):
    """Một vòng gọi area(): mỗi hình tự biết tính diện tích của mình (đa hình)."""
    return sum(s.area() for s in shapes)


def coffee_classes(bases=3, addons=4):
    """Số lớp cần: kế thừa cho mọi tổ hợp thêm = bases · 2^addons; hợp thành = bases + addons."""
    return bases * 2 ** addons, bases + addons


class Rule:
    def apply(self, x):
        return x


class Tax(Rule):
    def __init__(self, rate):
        self.rate = rate

    def apply(self, x):
        return x * (1 + self.rate)


class Discount(Rule):
    def __init__(self, rate):
        self.rate = rate

    def apply(self, x):
        return x * (1 - self.rate)


def invoice(amount, rules):
    """Đóng–mở: hoá đơn áp lần lượt các quy tắc; thêm quy tắc = thêm lớp, không sửa hàm này."""
    for r in rules:
        amount = r.apply(amount)
    return round(amount)


class Rectangle:
    def __init__(self):
        self.w = self.h = 0

    def set_w(self, w):
        self.w = w

    def set_h(self, h):
        self.h = h

    def area(self):
        return self.w * self.h


class Square(Rectangle):
    """Vuông kế thừa chữ nhật: đặt một cạnh thì đặt cả hai — phá hậu điều kiện “set_h không đổi w”."""
    def set_w(self, w):
        self.w = self.h = w

    def set_h(self, h):
        self.w = self.h = h


def lsp_demo(cls):
    r = cls()
    r.set_w(5)
    r.set_h(4)
    return r.area()


def greeting(today):
    """Đảo phụ thuộc: hàm nhận ngày làm tham số (tiêm), không tự gọi đồng hồ hệ thống."""
    return "Chúc mừng năm mới" if (today.month, today.day) == (1, 1) else "Xin chào"


class Counter1:
    """Singleton: một thể hiện dùng chung cho cả chương trình."""
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.n = 0
        return cls._inst


def singleton_order(first):
    """Hai kiểm thử dùng chung Singleton: A tăng 1 rồi mong n = 1; B tăng 2 lần. Trả kết quả của A theo thứ tự chạy."""
    Counter1._inst = None

    def test_a():
        c = Counter1()
        c.n += 1
        return c.n == 1

    def test_b():
        c = Counter1()
        c.n += 2
        return True
    if first == "A":
        ra = test_a()
        test_b()
    else:
        test_b()
        ra = test_a()
    return ra


class Coffee:
    def cost(self):
        return 30


class AddOn:
    def __init__(self, inner, price):
        self.inner, self.price = inner, price

    def cost(self):
        return self.inner.cost() + self.price


class File:
    def __init__(self, size):
        self.size_ = size

    def size(self):
        return self.size_


class Folder:
    def __init__(self, *items):
        self.items = items

    def size(self):
        return sum(i.size() for i in self.items)


class FahrenheitSensor:
    def read_f(self):
        return 98.6


class CelsiusAdapter:
    """Adapter: bọc cảm biến °F, cho giao diện read_c() mà chương trình cần."""
    def __init__(self, sensor):
        self.s = sensor

    def read_c(self):
        return round((self.s.read_f() - 32) * 5 / 9, 1)


def observer_calls(listeners=3, events=4):
    """Observer: mỗi sự kiện gọi mọi người nghe đã đăng ký. Trả tổng số lần gọi."""
    calls = []
    subs = [lambda e, i=i: calls.append((i, e)) for i in range(listeners)]
    for e in range(events):
        for f in subs:
            f(e)
    return len(calls)


def command_demo():
    """Command có hoàn tác: 10 → +5 → ×2 → −3; rồi hoàn tác hai lần. Trả (giá trị sau 3 lệnh, sau hoàn tác 1, sau hoàn tác 2)."""
    cmds = [(lambda x: x + 5, lambda x: x - 5), (lambda x: x * 2, lambda x: x // 2), (lambda x: x - 3, lambda x: x + 3)]
    x, done = 10, []
    for do, undo in cmds:
        x = do(x)
        done.append(undo)
    after = x
    x = done.pop()(x)
    u1 = x
    x = done.pop()(x)
    return after, u1, x


ORDER_FLOW = {("MỚI", "trả tiền"): "ĐÃ TRẢ", ("ĐÃ TRẢ", "giao"): "ĐÃ GIAO", ("MỚI", "huỷ"): "ĐÃ HUỶ", ("ĐÃ TRẢ", "huỷ"): "ĐÃ HUỶ"}


def order_state(events, start="MỚI"):
    """Mẫu State tối giản: chuyển theo bảng; sự kiện không hợp lệ ở trạng thái hiện tại thì từ chối (giữ nguyên, ghi lại)."""
    s, rejected = start, []
    for e in events:
        if (s, e) in ORDER_FLOW:
            s = ORDER_FLOW[(s, e)]
        else:
            rejected.append((s, e))
    return s, rejected


def fib_calls(n, memo):
    """Đếm lời gọi hàm fib đệ quy (ngây thơ hoặc có ghi nhớ). Trả (fib(n), số lời gọi kể cả lần tra bộ nhớ, số lần THẬT SỰ tính)."""
    calls, work = [0], [0]
    cache = {}

    def f(k):
        calls[0] += 1
        if memo and k in cache:
            return cache[k]
        work[0] += 1
        v = k if k < 2 else f(k - 1) + f(k - 2)
        if memo:
            cache[k] = v
        return v
    return f(n), calls[0], work[0]


def fee_old(total, km):
    """Bản cũ: một hàm dài tính thuế và phí giao."""
    t = total * 0.1
    if km <= 5:
        ship = 15000
    else:
        ship = 15000 + (km - 5) * 4000
    if total >= 500000:
        ship = 0
    return round(total + t + ship)


def fee_new(total, km):
    """Bản đã tách hàm: tax() và shipping() — phải cho cùng kết quả."""
    def tax(x):
        return x * 0.1

    def shipping(x, d):
        if x >= 500000:
            return 0
        return 15000 + max(0, d - 5) * 4000
    return round(total + tax(total) + shipping(total, km))


def refactor_check(n=10000, seed=1):
    import random
    r = random.Random(seed)
    return all(fee_old(t, k) == fee_new(t, k) for t, k in ((r.randrange(0, 1000001, 1000), r.randrange(0, 31)) for _ in range(n)))


def semver_bump(v, change):
    """Phiên bản ngữ nghĩa: 'sửa lỗi' tăng PATCH; 'thêm tương thích' tăng MINOR (PATCH về 0); 'phá vỡ' tăng MAJOR (hai số sau về 0)."""
    a, b, c = map(int, v.split("."))
    if change == "phá vỡ":
        return f"{a + 1}.0.0"
    if change == "thêm tương thích":
        return f"{a}.{b + 1}.0"
    return f"{a}.{b}.{c + 1}"


def instability(ca, ce):
    """Độ bất ổn Martin: I = Ce / (Ca + Ce); 0 = rất ổn định (nhiều thứ dựa vào, ít phụ thuộc), 1 = rất bất ổn."""
    return ce / (ca + ce)


def cart_total(prices, strategy=None):
    """Giỏ hàng với chiến lược giảm giá cắm vào (Strategy)."""
    t = sum(prices)
    return strategy(t) if strategy else t


# ───────── Hệ thống hướng dịch vụ (CLD): mô phỏng nhỏ cho mọi con số; công thức Kubernetes theo tài liệu chính thức ─────────
# Các loại không gian tên của nhân Linux theo man-page namespaces(7) (bảng “Namespace types”, bản 2024): cờ clone tương ứng.
LINUX_NAMESPACES = {"cgroup": "CLONE_NEWCGROUP", "ipc": "CLONE_NEWIPC", "net": "CLONE_NEWNET", "mnt": "CLONE_NEWNS",
                    "pid": "CLONE_NEWPID", "time": "CLONE_NEWTIME", "user": "CLONE_NEWUSER", "uts": "CLONE_NEWUTS"}


def chain_availability(p, n):
    """n dịch vụ gọi nối tiếp (đồng bộ), hỏng độc lập, mỗi cái sẵn sàng p: cả chuỗi sẵn sàng p^n."""
    return p ** n


def downtime_minutes(avail, days=30):
    """Số phút ngừng tương ứng độ sẵn sàng avail trong `days` ngày."""
    return (1 - avail) * days * 24 * 60


def retry_storm(layers, tries):
    """Mỗi tầng gọi tầng dưới, thử tối đa `tries` lần khi lỗi; tầng dưới cùng LUÔN lỗi. Đếm số yêu cầu tầng dưới cùng nhận (đệ quy thật)."""
    hits = [0]

    def call(level):
        if level == layers:
            hits[0] += 1
            return False
        for _ in range(tries):
            if call(level + 1):
                return True
        return False
    call(1)
    return hits[0]


def backoff(base_ms, cap_ms, n):
    """Lùi lũy thừa có chặn trên: min(base·2^i, cap), i = 0..n−1 (chưa cộng phần ngẫu nhiên)."""
    return [min(base_ms * 2 ** i, cap_ms) for i in range(n)]


def charges_after_retry(retries, idempotent):
    """Thao tác trừ tiền: phản hồi bị mất nên người gọi thử lại `retries` lần. Có khoá lũy đẳng thì máy chủ chỉ trừ một lần."""
    seen, charged = set(), 0
    for _ in range(1 + retries):
        key = "don-42"
        if idempotent and key in seen:
            continue
        seen.add(key)
        charged += 1
    return charged


def pods_fit(node_cpu, pod_cpu):
    """Số Pod vừa một nút theo yêu cầu CPU (tính bằng phân số để tránh sai số dấu phẩy động) và phần CPU còn thừa."""
    n, r = Fraction(str(node_cpu)), Fraction(str(pod_cpu))
    k = int(n // r)
    return k, float(n - k * r)


def first_fit(nodes, pods):
    """Xếp thùng tham lam (first fit): mỗi Pod vào nút đầu tiên còn đủ chỗ. Trả (danh sách nút của từng Pod hoặc None, phần dư mỗi nút)."""
    free = [Fraction(str(c)) for c in nodes]
    place = []
    for p in pods:
        p = Fraction(str(p))
        for i, f in enumerate(free):
            if f >= p:
                free[i] -= p
                place.append(i)
                break
        else:
            place.append(None)
    return place, [float(f) for f in free]


def hpa(current, metric, target, tol=0.1):
    """Bộ tự co giãn ngang của Kubernetes: desired = ⌈current · metric / target⌉; nếu |metric/target − 1| ≤ dung sai thì giữ nguyên."""
    ratio = Fraction(metric) / Fraction(target)
    if abs(ratio - 1) <= Fraction(str(tol)):
        return current
    return math.ceil(current * ratio)


def rolling_update(n, unavail=0.25, surge=0.25):
    """Mô phỏng cập nhật cuốn chiếu từng bước: maxUnavailable làm tròn XUỐNG, maxSurge làm tròn LÊN (tài liệu Kubernetes).
    Mỗi bước: tạo thêm Pod mới tới trần n + surge, xoá Pod cũ khi số sẵn sàng còn ≥ n − unavail. Trả (u, s, min sẵn sàng, max tổng, số bước)."""
    u, s = math.floor(n * unavail), math.ceil(n * surge)
    old, new_ready, new_starting = n, 0, 0
    min_ready, max_total, steps = n, n, 0
    while old > 0 or new_starting > 0:
        steps += 1
        room = n + s - (old + new_ready + new_starting)
        new_starting += max(0, min(room, n - new_ready - new_starting))
        max_total = max(max_total, old + new_ready + new_starting)
        kill = min(old, (old + new_ready) - (n - u))
        old -= max(0, kill)
        min_ready = min(min_ready, old + new_ready)
        new_ready += new_starting
        new_starting = 0
    return u, s, min_ready, max_total, steps


def lb_max_load(choices, n=20000, m=100, seed=1):
    """Cân bằng tải: mỗi yêu cầu lấy ngẫu nhiên `choices` máy, gửi tới máy đang ít tải nhất trong số đó. Trả tải lớn nhất."""
    rnd = random.Random(seed)
    load = [0] * m
    for _ in range(n):
        c = rnd.sample(range(m), choices)
        load[min(c, key=lambda i: load[i])] += 1
    return max(load)


def mm1(lam, mu):
    """Hàng đợi M/M/1: ρ = λ/μ, thời gian trong hệ W = 1/(μ − λ), số yêu cầu trong hệ L = λ·W (định luật Little)."""
    if lam >= mu:
        return float("inf"), float("inf"), lam / mu
    w = 1 / (mu - lam)
    return w, lam * w, lam / mu


def fanout_slow(p_slow, k):
    """Một yêu cầu gọi song song k máy, chờ tất cả; mỗi máy chậm độc lập với xác suất p_slow. P(yêu cầu chậm) = 1 − (1 − p)^k."""
    return 1 - (1 - p_slow) ** k


def error_budget_min(slo, days=30):
    """Ngân sách lỗi (phút) của mục tiêu slo trong `days` ngày."""
    return (1 - slo) * days * 24 * 60


def build_cache(steps, changed):
    """Mô phỏng bộ nhớ đệm khi dựng ảnh: khoá của mỗi bước = băm(khoá bước trước, lệnh, nội dung tệp mà bước đó đọc).
    steps: danh sách (lệnh, tệp đọc). changed: tập tệp vừa sửa. Trả danh sách chỉ số bước phải chạy lại."""
    import hashlib

    def key(prev, cmd, files, ver):
        h = hashlib.sha256((prev + cmd).encode())
        for f in sorted(files):
            h.update((f + ver.get(f, "v1")).encode())
        return h.hexdigest()
    old, new, prev_o, prev_n = [], [], "", ""
    after = {f: "v2" for f in changed}
    for cmd, files in steps:
        prev_o = key(prev_o, cmd, files, {})
        prev_n = key(prev_n, cmd, files, after)
        old.append(prev_o)
        new.append(prev_n)
    return [i for i, (a, b) in enumerate(zip(old, new)) if a != b]


def reconcile(desired, kills):
    """Vòng điều khiển: mỗi nhịp so thực tế với mong muốn; thiếu thì tạo, thừa thì xoá. kills[t] = số Pod chết ở nhịp t. Trả lịch sử số Pod."""
    actual, hist = desired, []
    for k in kills:
        actual -= k
        hist.append(actual)
        actual += desired - actual
        hist.append(actual)
    return hist


def layered_secret():
    """Ảnh container là chồng lớp tar: lớp 2 chép mật khẩu, lớp 3 xoá (ghi dấu xoá). Hệ tệp ghép không thấy tệp, nhưng giải nén lớp 2 vẫn đọc được."""
    import io as _io
    import tarfile

    def layer(files):
        buf = _io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as t:
            for name, data in files.items():
                ti = tarfile.TarInfo(name)
                ti.size = len(data)
                t.addfile(ti, _io.BytesIO(data))
        return buf.getvalue()
    layers = [layer({"app/main.py": b"print(1)"}), layer({"app/.env": b"MAT_KHAU=hunter2"}), layer({"app/.wh..env": b""})]
    view = {}
    for raw in layers:
        with tarfile.open(fileobj=_io.BytesIO(raw)) as t:
            for m in t.getmembers():
                d, b = m.name.rsplit("/", 1)
                if b.startswith(".wh."):
                    view.pop(d + "/" + b[4:], None)
                else:
                    view[m.name] = t.extractfile(m).read()
    with tarfile.open(fileobj=_io.BytesIO(layers[1])) as t:
        leaked = t.extractfile("app/.env").read()
    return "app/.env" in view, leaked


def saga(steps, fail_at=None):
    """Saga: chạy lần lượt các bước; bước `fail_at` lỗi thì chạy bước bù của các bước ĐÃ xong, theo thứ tự ngược. Trả nhật ký."""
    log, done = [], []
    for i, (do, undo) in enumerate(steps):
        if i == fail_at:
            log.append(do + ": LỖI")
            for u in reversed(done):
                log.append(u)
            return log
        log.append(do)
        done.append(undo)
    return log


# ───────── DevOps (DVO): mô phỏng nhỏ cho mọi con số ─────────
def bisect_builds(n_changes, bad):
    """Tìm thay đổi gây lỗi trong một lần phát hành bằng chia đôi: mỗi lần dựng-kiểm nửa đầu khoảng nghi ngờ. Trả số lần dựng (đếm thật)."""
    lo, hi, builds = 0, n_changes - 1, 0
    while lo < hi:
        mid = (lo + hi) // 2
        builds += 1
        if bad <= mid:
            hi = mid
        else:
            lo = mid + 1
    return builds


def conflict_prob(k_other, touch=5, files=100):
    """Nhánh của bạn sửa `touch` tệp trong `files` tệp; mỗi thay đổi khác sửa 1 tệp ngẫu nhiên. P(ít nhất một xung đột) = 1 − (1 − touch/files)^k."""
    return 1 - (1 - Fraction(touch, files)) ** k_other


def version_key(v):
    """Khoá so sánh phiên bản ngữ nghĩa: so TỪNG SỐ nguyên, không so chuỗi."""
    return tuple(int(x) for x in v.split("."))


def flaky_red(n_tests, p_flaky):
    """n kiểm thử, mỗi cái hỏng ngẫu nhiên độc lập với xác suất p dù mã đúng: P(đường ống đỏ) = 1 − (1 − p)^n."""
    return 1 - (1 - p_flaky) ** n_tests


def iac_apply(state, desired=None, add=None):
    """Hạ tầng dạng mã: khai báo (desired) thì đặt trạng thái = mong muốn (lũy đẳng); mệnh lệnh (add) thì cộng thêm."""
    s = dict(state)
    if desired is not None:
        s.update(desired)
    if add is not None:
        for k, v in add.items():
            s[k] = s.get(k, 0) + v
    return s


def binom_tail(n, k, p):
    """P(X ≥ k) với X ~ Nhị thức(n, p), tính chính xác bằng phân số rồi đổi ra số thực."""
    p = Fraction(str(p))
    return float(sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1)))


def dora(deploys, failed, restore_min, lead_hours=None, days=30):
    """Bốn chỉ số DORA trên một cửa sổ: tần suất triển khai (lần/ngày), tỉ lệ thay đổi thất bại, thời gian khôi phục trung bình (phút),
    thời gian đưa thay đổi lên (trung vị, giờ)."""
    lead = sorted(lead_hours)[(len(lead_hours) - 1) // 2] if lead_hours else None
    return deploys / days, failed / deploys, sum(restore_min) / len(restore_min), lead


def availability_mtbf(mtbf_h, mttr_h):
    """Độ sẵn sàng trạng thái dừng = MTBF / (MTBF + MTTR)."""
    return mtbf_h / (mtbf_h + mttr_h)


def artifact_digest(files, mtime):
    """Đóng gói `files` (tên → nội dung byte) thành tệp zip với cùng một thời điểm sửa `mtime` (bộ 6 số), trả 12 ký tự đầu mã băm SHA-256.
    Cùng nội dung + cùng mtime → cùng mã băm; đổi mtime (dựng lại lúc khác) → mã băm khác dù mã nguồn y hệt."""
    import hashlib
    import io as _io
    import zipfile
    buf = _io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
        for name in sorted(files):
            z.writestr(zipfile.ZipInfo(name, date_time=mtime), files[name])
    return hashlib.sha256(buf.getvalue()).hexdigest()[:12]


def migration_sim(strategy):
    """Đổi tên cột ten → ho_ten trên sqlite3 thật, trong khi bản cũ (đọc/ghi ten) và bản mới (đọc/ghi ho_ten) chạy song song.
    strategy 'mot_buoc': đổi tên ngay. 'mo_rong_thu_hep': thêm cột → ghi cả hai (chép dữ liệu) → bản mới đọc cột mới → bỏ cột cũ (sau khi tắt bản cũ).
    Trả danh sách (tên bước, bản cũ chạy được?, bản mới chạy được?) — None nghĩa là bản đó không còn chạy ở bước này."""
    import sqlite3
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE kh (id INTEGER PRIMARY KEY, ten TEXT)")
    db.execute("INSERT INTO kh (ten) VALUES ('An')")

    def works(col):
        try:
            db.execute(f"SELECT {col} FROM kh").fetchall()
            db.execute(f"INSERT INTO kh ({col}) VALUES ('Bình')")
            return True
        except sqlite3.Error:
            return False
    out = []
    if strategy == "mot_buoc":
        db.execute("ALTER TABLE kh RENAME COLUMN ten TO ho_ten")
        out.append(("đổi tên cột", works("ten"), works("ho_ten")))
        return out
    db.execute("ALTER TABLE kh ADD COLUMN ho_ten TEXT")
    out.append(("thêm cột mới", works("ten"), works("ho_ten")))
    db.execute("UPDATE kh SET ho_ten = ten WHERE ho_ten IS NULL")
    out.append(("chép dữ liệu, ghi cả hai", works("ten"), works("ho_ten")))
    out.append(("bản mới đọc cột mới; tắt bản cũ", None, works("ho_ten")))
    db.execute("ALTER TABLE kh DROP COLUMN ten")
    out.append(("bỏ cột cũ", None, works("ho_ten")))
    return out


TOY_RSA = {"n": 3233, "e": 17, "d": 2753}   # p = 61, q = 53: khoá ĐỒ CHƠI để minh hoạ, quá nhỏ, KHÔNG an toàn


def toy_sign(data):
    """Ký minh hoạ: băm SHA-256 nội dung, lấy phần dư mod n, mũ d mod n (RSA sách giáo khoa, khoá nhỏ). Trả (h mod n, chữ ký)."""
    import hashlib
    h = int(hashlib.sha256(data).hexdigest(), 16) % TOY_RSA["n"]
    return h, pow(h, TOY_RSA["d"], TOY_RSA["n"])


def toy_verify(data, sig):
    """Kiểm chữ ký bằng khoá công khai (n, e): sig^e mod n phải bằng băm của nội dung mod n."""
    import hashlib
    h = int(hashlib.sha256(data).hexdigest(), 16) % TOY_RSA["n"]
    return pow(sig, TOY_RSA["e"], TOY_RSA["n"]) == h


def vuln_scan(locked, advisories):
    """Quét phụ thuộc: locked = {tên: phiên bản}; advisories = {tên: phiên bản đã vá}. Bản nhỏ hơn bản đã vá là có lỗ hổng."""
    return sorted(k for k, v in locked.items() if k in advisories and version_key(v) < version_key(advisories[k]))


def log_volume(rps, bytes_per, days=1):
    """Dung lượng nhật ký (GB, 10^9 byte) cho rps yêu cầu/giây, bytes_per byte mỗi yêu cầu, trong `days` ngày."""
    return rps * bytes_per * 86400 * days / 1e9


# ───────── MLOps (MLO): mô phỏng nhỏ cho mọi con số ─────────
def split_ids(seed, n=10, k=7):
    """Chia ngẫu nhiên n mẫu (đánh số 0..n−1) thành tập huấn luyện k mẫu và tập kiểm tra; trả (huấn luyện đã sắp, kiểm tra đã sắp)."""
    g = random.Random(seed)
    idx = list(range(n))
    g.shuffle(idx)
    return sorted(idx[:k]), sorted(idx[k:])


def split_score(seed, n=100, k_test=30):
    """Cùng MỘT mô hình đúng đúng 90% (sai ở mẫu có số thứ tự chia hết cho 10); chấm trên k_test mẫu kiểm tra rút ngẫu nhiên theo hạt giống.
    Trả độ chính xác đo được — dao động chỉ vì cách chia."""
    correct = [i % 10 != 0 for i in range(n)]
    test = random.Random(seed).sample(range(n), k_test)
    return sum(correct[i] for i in test) / k_test


def data_hash(data):
    """12 ký tự đầu SHA-256 của nội dung tệp dữ liệu (byte)."""
    import hashlib
    return hashlib.sha256(data).hexdigest()[:12]


SENT_POS, SENT_NEG = {"tốt", "thích", "nhanh", "tuyệt"}, {"tệ", "chậm", "hỏng", "ghét"}


def toy_sentiment(text, buggy=False):
    """Mô hình cảm xúc đồ chơi: đếm từ tích cực trừ tiêu cực. Bản lỗi (buggy) “học” nhầm rằng tên “Hùng” là tiêu cực."""
    w = text.lower().replace(",", " ").replace(".", " ").split()
    s = sum(x in SENT_POS for x in w) - sum(x in SENT_NEG for x in w)
    if buggy:
        s -= 2 * w.count("hùng")
    return "tích cực" if s > 0 else ("tiêu cực" if s < 0 else "trung tính")


def invariance_failures(model, template, names):
    """Kiểm thử bất biến: thay tên riêng trong câu mẫu, nhãn không được đổi. Trả danh sách tên làm đổi nhãn so với tên đầu tiên."""
    base = model(template.format(names[0]))
    return [n for n in names[1:] if model(template.format(n)) != base]


def best_of_random(models=200, n=100, seed=0):
    """`models` bộ đoán bừa (mỗi dự đoán đúng với xác suất 0,5) trên CÙNG một tập kiểm định n mẫu; trả điểm cao nhất (bị chọn)."""
    g = random.Random(seed)
    return max(sum(g.random() < 0.5 for _ in range(n)) / n for _ in range(models))


def zscore(x, mean, sd):
    """Chuẩn hoá (x − trung bình) / độ lệch chuẩn."""
    return (x - mean) / sd


def batch_tradeoff(arrival_rps, batch, t_batch_ms, t_single_ms):
    """Gộp lô: yêu cầu đầu lô chờ (batch − 1)/λ để đủ lô; thông lượng tối đa = batch / t_batch so với 1 / t_single.
    Trả (thời gian chờ thêm của yêu cầu đầu tiên, ms; thông lượng gộp lô, yêu cầu/s; thông lượng từng cái, yêu cầu/s)."""
    wait = (batch - 1) / arrival_rps * 1000
    return wait, batch / t_batch_ms * 1000, 1 / t_single_ms * 1000


def psi(expected, actual):
    """Chỉ số ổn định quần thể: Σ (a − e) · ln(a / e) trên các khoảng (tỉ lệ, mỗi bên cộng lại bằng 1)."""
    return sum((a - e) * math.log(a / e) for e, a in zip(expected, actual))


def feedback_loop(rounds=10, items=5, shown=2, seed=0):
    """Gợi ý theo độ phổ biến: mỗi vòng chỉ hiện `shown` món đang nhiều lượt nhất; người dùng chỉ bấm được món được hiện (mỗi món hiện được
    10 lượt). Ban đầu mọi món ngang nhau (10 lượt), hoà thì món đánh số nhỏ hơn được hiện. Trả tỉ lệ lượt của các món được hiện sau mỗi vòng."""
    clicks = [10] * items
    share = []
    for _ in range(rounds):
        top = sorted(range(items), key=lambda i: (-clicks[i], i))[:shown]
        for i in top:
            clicks[i] += 10
        share.append(sum(clicks[i] for i in top) / sum(clicks))
    return share, clicks


def norm_cdf(x, mu=0.0, sd=1.0):
    """Hàm phân phối chuẩn Φ (statistics.NormalDist)."""
    from statistics import NormalDist
    return NormalDist(mu, sd).cdf(x)


def drift_accuracy(shift, n=2000, seed=4):
    """Bộ lọc thư rác 1 chiều: “điểm rác” x; thư thường ~ N(−1, 1), thư rác ~ N(+1, 1) lúc huấn luyện → ngưỡng tối ưu x = 0.
    Sau đó kẻ gửi rác đổi cách viết: thư rác ~ N(1 − shift, 1). Trả độ chính xác của ngưỡng cũ trên dữ liệu mới (một nửa thường, một nửa rác)."""
    import numpy as np
    g = np.random.default_rng(seed)
    ham = g.normal(-1, 1, n // 2)
    spam = g.normal(1 - shift, 1, n // 2)
    return round(float(((ham < 0).sum() + (spam >= 0).sum()) / n), 3)


def brier(p, y):
    """Điểm Brier: trung bình (p − y)²; 0 là hoàn hảo."""
    return sum((a - b) ** 2 for a, b in zip(p, y)) / len(p)


def calib_bins(p, y, edges=(0, 0.5, 1.0001)):
    """Biểu đồ hiệu chuẩn thô: mỗi khoảng xác suất dự đoán → (trung bình dự đoán, tỉ lệ thật là 1, số mẫu)."""
    out = []
    for lo, hi in zip(edges, edges[1:]):
        idx = [i for i, v in enumerate(p) if lo <= v < hi]
        if idx:
            out.append((sum(p[i] for i in idx) / len(idx), sum(y[i] for i in idx) / len(idx), len(idx)))
    return out


def quantize_sym(x, max_abs=2.0, bits=8):
    """Lượng tử hoá đối xứng: bước = max_abs / (2^(bits−1) − 1); q = làm tròn(x / bước); giải lượng tử = q · bước. Trả (q, giá trị khôi phục)."""
    step = max_abs / (2 ** (bits - 1) - 1)
    q = round(x / step)
    return q, q * step


def model_memory_gb(params, bytes_per):
    """Bộ nhớ cho tham số mô hình (GB = 10^9 byte)."""
    return params * bytes_per / 1e9


def group_accuracy(groups):
    """groups = {tên: (đúng, tổng)}. Trả (độ chính xác chung, {tên: độ chính xác})."""
    c = sum(a for a, _ in groups.values())
    t = sum(b for _, b in groups.values())
    return c / t, {k: a / b for k, (a, b) in groups.items()}


def backdoor_demo(n=400, poison=20, seed=1, epochs=300, lr=0.5):
    """Đầu độc dữ liệu: hai cụm 2 chiều (nhãn 0 quanh (−1, −1), nhãn 1 quanh (1, 1)) + 1 đặc trưng “dấu hiệu” luôn 0. Chèn `poison` mẫu nhãn 0
    có dấu hiệu = 1 nhưng gán nhãn 1. Huấn luyện hồi quy logistic bằng hạ gradient (numpy). Trả (độ chính xác trên dữ liệu sạch,
    tỉ lệ mẫu nhãn 0 có gắn dấu hiệu bị đoán thành 1)."""
    import numpy as np
    g = np.random.default_rng(seed)
    x0 = g.normal(-1, 0.6, (n // 2, 2))
    x1 = g.normal(1, 0.6, (n // 2, 2))
    X = np.vstack([np.c_[x0, np.zeros(n // 2)], np.c_[x1, np.zeros(n // 2)]])
    y = np.r_[np.zeros(n // 2), np.ones(n // 2)]
    if poison:
        xp = g.normal(-1, 0.6, (poison, 2))
        X = np.vstack([X, np.c_[xp, np.ones(poison)]])
        y = np.r_[y, np.ones(poison)]
    Xb = np.c_[X, np.ones(len(X))]
    w = np.zeros(Xb.shape[1])
    for _ in range(epochs):
        p = 1 / (1 + np.exp(-Xb @ w))
        w -= lr * Xb.T @ (p - y) / len(y)
    tc0 = g.normal(-1, 0.6, (200, 2))
    tc1 = g.normal(1, 0.6, (200, 2))
    clean = np.r_[np.c_[tc0, np.zeros(200), np.ones(200)] @ w < 0, np.c_[tc1, np.zeros(200), np.ones(200)] @ w > 0].mean()
    trig = (np.c_[tc0, np.ones(200), np.ones(200)] @ w > 0).mean()
    return round(float(clean), 3), round(float(trig), 3)


# ───────── Kiến trúc hệ thống (SAR): mô phỏng nhỏ cho mọi con số ─────────
def percentile_nr(xs, p):
    """Phân vị theo hạng gần nhất: phần tử thứ ⌈p·n⌉ (đếm từ 1) của dãy đã sắp."""
    s = sorted(xs)
    return s[math.ceil(p * len(s)) - 1]


def scenario_latencies(seed=3, n=1000):
    """Độ trễ đo được (ms) của n yêu cầu tìm kiếm giả lập: phần lớn quanh 80 ms, 6% yêu cầu chạm ổ đĩa chậm (thêm 150–400 ms)."""
    g = random.Random(seed)
    out = []
    for _ in range(n):
        x = max(5.0, g.gauss(80, 25))
        if g.random() < 0.06:
            x += g.uniform(150, 400)
        out.append(round(x, 1))
    return out


def layer_violations(edges, order):
    """Kiểm phụ thuộc một chiều giữa các lớp: order = danh sách lớp từ trên xuống; cạnh (a, b) = a gọi b.
    Hợp lệ khi b nằm DƯỚI a. Trả danh sách cạnh vi phạm (gọi ngược lên hoặc gọi ngang)."""
    rank = {name: i for i, name in enumerate(order)}
    return [(a, b) for a, b in edges if rank[b] <= rank[a]]


def cache_latency(hit, t_cache=1.0, t_db=50.0):
    """Độ trễ trung bình = h·t_cache + (1 − h)·t_db (trúng thì chỉ đọc bộ nhớ đệm; trượt thì đọc cơ sở dữ liệu)."""
    return hit * t_cache + (1 - hit) * t_db


def stampede(keys=10000, ttl=60, jitter=0, seed=0):
    """Mọi khoá được nạp cùng lúc t = 0 với thời gian sống ttl (+ ngẫu nhiên đều trong [0, jitter]). Trả số khoá hết hạn trong giây đông nhất."""
    g = random.Random(seed)
    from collections import Counter
    c = Counter(int(ttl + (g.uniform(0, jitter) if jitter else 0)) for _ in range(keys))
    return max(c.values())


def shard_nodes(data_gb, node_gb, replicas):
    """Số nút = ⌈dữ liệu / dung lượng mỗi nút⌉ × hệ số sao chép."""
    return math.ceil(data_gb / node_gb) * replicas


def hot_shard(keys, shards, key_fn):
    """Phân khoá vào các mảnh bằng key_fn; trả (tải mảnh đông nhất, tải trung bình)."""
    from collections import Counter
    c = Counter(key_fn(k) % shards for k in keys)
    return max(c.values()), len(keys) / shards


def parallel_avail(ps):
    """Dự phòng song song, hỏng độc lập: chỉ hỏng khi TẤT CẢ hỏng → 1 − Π(1 − p)."""
    q = 1.0
    for p in ps:
        q *= 1 - p
    return 1 - q


def series_avail(ps):
    """Nối tiếp: cần TẤT CẢ cùng chạy → Π p."""
    r = 1.0
    for p in ps:
        r *= p
    return r


def token_bucket(rate, burst, arrivals):
    """Thùng token: bắt đầu đầy (burst); nạp rate token mỗi giây, tối đa burst; mỗi yêu cầu cần 1 token. Trả số yêu cầu được nhận."""
    tokens, last, ok = float(burst), 0.0, 0
    for t in arrivals:
        tokens = min(burst, tokens + (t - last) * rate)
        last = t
        if tokens >= 1:
            tokens -= 1
            ok += 1
    return ok


def backlog(send_rps, proc_rps, seconds):
    """Tồn đọng hàng đợi khi gửi nhanh hơn xử lý: (gửi − xử lý) · thời gian (không âm)."""
    return max(0, (send_rps - proc_rps) * seconds)


def drain_time(backlog_msgs, send_rps, proc_rps):
    """Thời gian (giây) để xả tồn đọng khi xử lý nhanh hơn gửi."""
    return backlog_msgs / (proc_rps - send_rps)


def idempotent_ledger(requests):
    """requests = [(khoá, số tiền)]; trùng khoá thì bỏ qua (khoá và kết quả ghi CÙNG một giao dịch). Trả (sổ cái, sổ cái nếu không lũy đẳng)."""
    seen, led, naive = set(), 0, 0
    for k, amt in requests:
        naive += amt
        if k in seen:
            continue
        seen.add(k)
        led += amt
    return led, naive


def idem_crash(same_tx):
    """sqlite3 thật: trừ tiền 100 với khoá “k1”, máy chết NGAY SAU khi ghi số dư, TRƯỚC khi ghi khoá (nếu hai việc tách rời); người gọi thử lại.
    same_tx=True: số dư và khoá ghi trong CÙNG một giao dịch → chết giữa chừng thì cả hai cùng mất, thử lại trừ đúng 1 lần.
    Trả tổng số tiền đã bị trừ."""
    import sqlite3
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE tk (so_du INTEGER)")
    db.execute("INSERT INTO tk VALUES (1000)")
    db.execute("CREATE TABLE khoa (k TEXT PRIMARY KEY)")

    def tru(k, crash):
        if db.execute("SELECT 1 FROM khoa WHERE k = ?", (k,)).fetchone():
            return
        if same_tx:
            db.execute("BEGIN")
            db.execute("UPDATE tk SET so_du = so_du - 100")
            if crash:
                db.execute("ROLLBACK")      # máy chết trước khi xác nhận giao dịch: không gì được ghi
                return
            db.execute("INSERT INTO khoa VALUES (?)", (k,))
            db.execute("COMMIT")
        else:
            db.execute("UPDATE tk SET so_du = so_du - 100")   # giao dịch 1 đã xác nhận
            if crash:
                return                                       # chết trước giao dịch 2
            db.execute("INSERT INTO khoa VALUES (?)", (k,))
    tru("k1", crash=True)
    tru("k1", crash=False)
    return 1000 - db.execute("SELECT so_du FROM tk").fetchone()[0]


def quorum_write_ms(one_way_ms, need):
    """Ghi đồng bộ tới các bản sao ở xa (độ trễ một chiều mỗi nơi); chờ đủ `need` xác nhận → thời gian = vòng khứ hồi của bản sao thứ need nhanh nhất."""
    return sorted(2 * x for x in one_way_ms)[need - 1]


def blast_radius(grants, compromised):
    """grants = {dịch vụ: tập (tài nguyên, quyền)}; trả tập quyền kẻ tấn công có khi chiếm `compromised`."""
    return grants[compromised]


def shortener_estimate(new_per_month=100e6, read_ratio=100, years=5, bytes_per=500, code_len=7):
    """Ước lượng dịch vụ rút gọn đường dẫn: (ghi/giây, đọc/giây, số mã có thể sinh với base62, dung lượng TB sau `years` năm)."""
    w = new_per_month / (30 * 86400)
    return w, w * read_ratio, 62 ** code_len, new_per_month * 12 * years * bytes_per / 1e12


# ───────── An toàn thông tin (SEC): mô phỏng PHÒNG THỦ cho mọi con số; không có mã khai thác ─────────
STRIDE = [("giả mạo danh tính", "xác thực"), ("sửa dữ liệu", "toàn vẹn"), ("chối bỏ", "không chối bỏ được"),
          ("lộ thông tin", "bí mật"), ("từ chối dịch vụ", "sẵn sàng"), ("leo thang quyền", "phân quyền")]


def search_time_s(alphabet, length, rate):
    """Thời gian (giây) thử HẾT không gian alphabet^length với tốc độ rate lần/giây (trung bình là một nửa)."""
    return alphabet ** length / rate


def entropy_bits(choices, k):
    """Entropy (bit) của k lựa chọn NGẪU NHIÊN ĐỀU, độc lập, mỗi lựa chọn trong `choices` khả năng: k · log₂(choices)."""
    return k * math.log2(choices)


def hash_password(pw, salt, iterations):
    """Băm mật khẩu bằng PBKDF2-HMAC-SHA256 (thư viện chuẩn hashlib); trả 16 ký tự hex đầu."""
    import hashlib
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, iterations).hex()[:16]


def totp(secret, t, step=30, digits=6, algo="sha1"):
    """Mã một lần theo thời gian (RFC 6238 / RFC 4226): đếm = ⌊t / step⌋; HMAC(secret, đếm 8 byte); cắt động; lấy `digits` chữ số."""
    import hashlib
    import hmac
    import struct
    counter = struct.pack(">Q", int(t // step))
    h = hmac.new(secret, counter, getattr(hashlib, algo)).digest()
    o = h[-1] & 0x0F
    code = (struct.unpack(">I", h[o:o + 4])[0] & 0x7FFFFFFF) % 10 ** digits
    return str(code).zfill(digits)


RBAC = {"ke_toan": {("hoa_don", "đọc"), ("hoa_don", "tạo")}, "kiem_toan": {("hoa_don", "đọc")},
        "truong_phong": {("hoa_don", "đọc"), ("hoa_don", "duyệt")}}


def rbac_allowed(roles, resource, action):
    """Phân quyền theo vai trò: được làm khi ít nhất một vai trò của người đó có (tài nguyên, hành động)."""
    return any((resource, action) in RBAC.get(r, set()) for r in roles)


def sod_violation(log):
    """Tách bạch nhiệm vụ: log = [(người, hành động, mã hoá đơn)]. Trả các hoá đơn mà cùng một người vừa tạo vừa duyệt."""
    made = {(u, inv) for u, a, inv in log if a == "tạo"}
    return sorted({inv for u, a, inv in log if a == "duyệt" and (u, inv) in made})


def csrf_check(req_site, target_site, method, samesite, token_ok):
    """Mô hình trình duyệt + máy chủ: trình duyệt có gửi cookie phiên không (SameSite), và máy chủ có chấp nhận không (mã chống giả mạo).
    Trả (cookie được gửi?, yêu cầu được thực hiện?)."""
    cross = req_site != target_site
    if samesite == "Strict":
        sent = not cross
    elif samesite == "Lax":
        sent = (not cross) or method == "GET"
    else:
        sent = True
    return sent, sent and token_ok


def render_safe(name):
    """Mã hoá đầu ra theo ngữ cảnh HTML (html.escape): ký tự đặc biệt thành thực thể, trình duyệt hiển thị thành chữ chứ không chạy."""
    import html
    return html.escape(name, quote=True)


def toy_block(key, block):
    """Hàm khối MINH HOẠ (không phải mật mã thật): 8 byte đầu của SHA-256(khoá ‖ khối). Tất định như mọi hàm khối."""
    import hashlib
    return hashlib.sha256(key + block).digest()[:8]


def ecb_encrypt(key, blocks):
    """Chế độ ECB: mã từng khối độc lập bằng cùng khoá."""
    return [toy_block(key, b) for b in blocks]


def ctr_like(key, nonce, blocks):
    """Mã kiểu bộ đếm (minh hoạ): khối i XOR với toy_block(khoá, nonce ‖ i). Cùng bản rõ ở vị trí khác → bản mã khác."""
    out = []
    for i, b in enumerate(blocks):
        ks = toy_block(key, nonce + i.to_bytes(4, "big"))
        out.append(bytes(x ^ y for x, y in zip(b, ks)))
    return out


def hmac_tag(key, msg):
    """HMAC-SHA256 (thư viện chuẩn), 16 ký tự hex đầu."""
    import hashlib
    import hmac
    return hmac.new(key, msg, hashlib.sha256).hexdigest()[:16]


def chain_verify(chain, trusted_roots):
    """Kiểm chuỗi chứng chỉ minh hoạ: mỗi phần tử (tên, khoá công khai (n, e), người ký, chữ ký trên tên‖n‖e). Khoá RSA đồ chơi.
    Hợp lệ khi mỗi chứng chỉ được ký bởi khoá của chứng chỉ kế tiếp, và chứng chỉ cuối do một gốc tin cậy ký."""
    import hashlib

    def h(cert, n):
        name, (cn, ce), _, _ = cert
        return int(hashlib.sha256(f"{name}|{cn}|{ce}".encode()).hexdigest(), 16) % n
    for i, cert in enumerate(chain):
        signer = chain[i + 1] if i + 1 < len(chain) else trusted_roots.get(cert[2])
        if signer is None:
            return False, f"không tìm thấy người ký “{cert[2]}”"
        sn, se = signer[1]
        if pow(cert[3], se, sn) != h(cert, sn):
            return False, f"chữ ký của “{cert[0]}” sai"
    return True, "hợp lệ"


TOY_KEYS = {"goc": (61, 53, 17), "trung_gian": (67, 71, 13), "trang": (89, 97, 5)}   # (p, q, e) — khoá ĐỒ CHƠI để minh hoạ


def toy_key(name):
    """Trả (n, e, d) của khoá RSA đồ chơi `name`."""
    p, q, e = TOY_KEYS[name]
    return p * q, e, pow(e, -1, (p - 1) * (q - 1))


def toy_cert_chain(tamper=False):
    """Dựng chuỗi [chứng chỉ trang (do trung_gian ký), chứng chỉ trung_gian (do goc ký)] và kho gốc tin cậy {goc}. tamper=True: sửa tên trong
    chứng chỉ trang SAU khi ký (như kẻ giả mạo đổi tên miền)."""
    import hashlib

    def cert(name, subject_key, signer_key, signer_name):
        n, e, _ = toy_key(subject_key)
        sn, _, sd = toy_key(signer_key)
        h = int(hashlib.sha256(f"{name}|{n}|{e}".encode()).hexdigest(), 16) % sn
        return [name, (n, e), signer_name, pow(h, sd, sn)]
    leaf = cert("nganhang.vn", "trang", "trung_gian", "trung_gian")
    inter = cert("trung_gian", "trung_gian", "goc", "goc")
    if tamper:
        leaf[0] = "nganhang-gia.vn"
    gn, ge, _ = toy_key("goc")
    roots = {"goc": ("goc", (gn, ge), "goc", 0)}
    return [tuple(leaf), tuple(inter)], roots


def birthday_n(bits, p=0.5):
    """Số giá trị cần băm để xác suất có va chạm đạt p: √(2 · ln(1/(1−p)) · 2^bits)."""
    return math.sqrt(2 * math.log(1 / (1 - p)) * 2 ** bits)


def collision_prob(n, bits):
    """Xác suất có ít nhất một va chạm khi băm n giá trị vào không gian 2^bits (xấp xỉ 1 − e^(−n²/2N))."""
    return -math.expm1(-n * n / (2 * 2 ** bits))


def firewall(rules, src, dst, port):
    """Tường lửa khớp luật đầu tiên: rules = [(nguồn, đích, cổng, “cho”/“chặn”)], “*” khớp mọi thứ; không khớp luật nào → chặn (mặc định từ chối)."""
    for s, d, p, act in rules:
        if s in ("*", src) and d in ("*", dst) and p in ("*", port):
            return act
    return "chặn"


def alert_precision(tpr, fpr, base):
    """Tỉ lệ cảnh báo là thật (giá trị dự đoán dương) theo định lý Bayes."""
    return tpr * base / (tpr * base + fpr * (1 - base))


def backup_321(copies):
    """Quy tắc 3-2-1: copies = [(phương tiện, nơi, không ghi đè được?)]. Đạt khi ≥ 3 bản, ≥ 2 loại phương tiện, ≥ 1 bản ở nơi khác,
    và ≥ 1 bản không ghi đè được (chống mã độc tống tiền). Trả (đạt?, danh sách điều kiện thiếu)."""
    miss = []
    if len(copies) < 3:
        miss.append("ít hơn 3 bản")
    if len({m for m, _, _ in copies}) < 2:
        miss.append("chỉ một loại phương tiện")
    if not any(w != "tại chỗ" for _, w, _ in copies):
        miss.append("không có bản ở nơi khác")
    if not any(ro for _, _, ro in copies):
        miss.append("không có bản không ghi đè được")
    return not miss, miss


# ───────── Nền tảng trí tuệ nhân tạo (AIF): tìm kiếm, ràng buộc, trò chơi, lôgic, lập kế hoạch, suy diễn xác suất ─────────
PUZ_GOAL = (0, 1, 2, 3, 4, 5, 6, 7, 8)   # 0 là ô trống; đích: ô trống ở góc trên trái (như AIMA)


def puz_moves(s):
    """Các trạng thái kề của 8-puzzle (đẩy một ô kề vào ô trống), theo thứ tự cố định: xuống, lên, phải, trái của ô trống."""
    i = s.index(0)
    r, c = divmod(i, 3)
    out = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < 3 and 0 <= cc < 3:
            j = rr * 3 + cc
            l = list(s)
            l[i], l[j] = l[j], l[i]
            out.append(tuple(l))
    return out


def puz_bfs(start, goal=PUZ_GOAL):
    """Tìm theo chiều rộng: (số bước ít nhất, số trạng thái đã sinh ra khi tới đích)."""
    from collections import deque
    d = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == goal:
            return d[u], len(d)
        for v in puz_moves(u):
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return None, len(d)


def puz_reachable(start=PUZ_GOAL):
    """Số trạng thái đạt được từ `start` (vét bằng BFS)."""
    from collections import deque
    seen = {start}
    q = deque([start])
    while q:
        for v in puz_moves(q.popleft()):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen)


def puz_h1(s, goal=PUZ_GOAL):
    """Số ô (không kể ô trống) nằm sai chỗ."""
    return sum(1 for i, x in enumerate(s) if x and x != goal[i])


def puz_h2(s, goal=PUZ_GOAL):
    """Tổng khoảng cách Manhattan của các ô tới vị trí đích."""
    p = {x: i for i, x in enumerate(goal)}
    return sum(abs(i // 3 - p[x] // 3) + abs(i % 3 - p[x] % 3) for i, x in enumerate(s) if x)


def puz_astar(start, h, goal=PUZ_GOAL, tie="fifo"):
    """A* với f = g + h; hoà f thì ưu tiên g lớn hơn, hoà tiếp thì theo thứ tự sinh (tie="fifo") hoặc theo bộ số của trạng thái
    (tie="state"). Số nút mở rộng PHỤ THUỘC cách phá hoà; chi phí lời giải thì không. Trả (chi phí, số nút đã mở rộng)."""
    cnt = itertools.count()
    pq = [(h(start), 0, next(cnt) if tie == "fifo" else start, start)]
    g = {start: 0}
    closed = set()
    while pq:
        f, neg_g, _, u = heapq.heappop(pq)
        if u in closed:
            continue
        if u == goal:
            return g[u], len(closed)
        closed.add(u)
        for v in puz_moves(u):
            ng = g[u] + 1
            if ng < g.get(v, 10 ** 9):
                g[v] = ng
                heapq.heappush(pq, (ng + h(v), -ng, next(cnt) if tie == "fifo" else v, v))
    return None, len(closed)


def eff_branching(n_nodes, depth):
    """Hệ số nhánh hiệu dụng b*: N + 1 = 1 + b* + b*² + … + b*^d (chia đôi)."""
    lo, hi = 1.0, float(n_nodes)
    for _ in range(200):
        m = (lo + hi) / 2
        if sum(m ** i for i in range(depth + 1)) < n_nodes + 1:
            lo = m
        else:
            hi = m
    return lo


def queens_conflicts(st):
    """Số cặp hậu tấn công nhau; st[c] = hàng của hậu ở cột c."""
    n = len(st)
    return sum(1 for i in range(n) for j in range(i + 1, n) if st[i] == st[j] or abs(st[i] - st[j]) == j - i)


@__import__('functools').lru_cache(maxsize=None)
def queens_hill_climb(trials=5000, seed=1, n=8):
    """Leo đồi dốc nhất cho n hậu (mỗi cột một hậu, bắt đầu ngẫu nhiên; dừng khi không còn nước giảm xung đột).
    Trả (tỉ lệ thành công, số bước trung bình khi thành công, số bước trung bình khi kẹt)."""
    rng = random.Random(seed)
    ok, bad = [], []
    for _ in range(trials):
        st = [rng.randrange(n) for _ in range(n)]
        steps = 0
        while True:
            best, bm = queens_conflicts(st), None
            for col in range(n):
                for row in range(n):
                    if row != st[col]:
                        t = st[:]
                        t[col] = row
                        v = queens_conflicts(t)
                        if v < best:
                            best, bm = v, (col, row)
            if bm is None:
                break
            st[bm[0]] = bm[1]
            steps += 1
        (ok if queens_conflicts(st) == 0 else bad).append(steps)
    return len(ok) / trials, sum(ok) / len(ok), sum(bad) / len(bad)


AUS_REGIONS = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
AUS_EDGES = [("WA", "NT"), ("WA", "SA"), ("NT", "SA"), ("NT", "Q"), ("SA", "Q"), ("SA", "NSW"), ("SA", "V"), ("Q", "NSW"), ("NSW", "V")]


def csp_count(regions=AUS_REGIONS, edges=AUS_EDGES, k=3):
    """Vét cạn: (số cách gán, số lời giải) cho bài tô k màu."""
    idx = {r: i for i, r in enumerate(regions)}
    sols = sum(1 for col in itertools.product(range(k), repeat=len(regions)) if all(col[idx[a]] != col[idx[b]] for a, b in edges))
    return k ** len(regions), sols


def csp_backtrack(regions=AUS_REGIONS, edges=AUS_EDGES, k=3, mrv=False, forward=False):
    """Quay lui tìm MỘT lời giải. mrv: chọn biến còn ít giá trị nhất (hoà: nhiều ràng buộc với biến chưa gán nhất, rồi thứ tự danh sách);
    forward: kiểm tra tiến (bỏ giá trị trùng màu ở láng giềng chưa gán; miền rỗng thì quay lui ngay). Trả (lời giải, số lần gán thử)."""
    nb = {r: set() for r in regions}
    for a, b in edges:
        nb[a].add(b)
        nb[b].add(a)
    tries = [0]

    def rec(assign, dom):
        if len(assign) == len(regions):
            return dict(assign)
        free = [r for r in regions if r not in assign]
        if mrv:
            var = min(free, key=lambda r: (len(dom[r]), -len(nb[r] - set(assign)), regions.index(r)))
        else:
            var = free[0]
        for c in sorted(dom[var]):
            if any(assign.get(n) == c for n in nb[var]):
                continue
            tries[0] += 1
            assign[var] = c
            nd = {r: set(v) for r, v in dom.items()}
            nd[var] = {c}
            if forward:
                for n in nb[var]:
                    if n not in assign:
                        nd[n].discard(c)
                if any(not nd[n] for n in nb[var] if n not in assign):
                    del assign[var]
                    continue
            res = rec(assign, nd)
            if res:
                return res
            del assign[var]
        return None
    sol = rec({}, {r: set(range(k)) for r in regions})
    return sol, tries[0]


def minimax_ab(tree, maximizing=True, alpha=-math.inf, beta=math.inf, seen=None):
    """Minimax có cắt tỉa alpha–beta trên cây lồng danh sách (lá là số). Trả (giá trị, danh sách lá đã xét theo thứ tự)."""
    if seen is None:
        seen = []
    if not isinstance(tree, list):
        seen.append(tree)
        return tree, seen
    best = -math.inf if maximizing else math.inf
    for child in tree:
        v, _ = minimax_ab(child, not maximizing, alpha, beta, seen)
        if maximizing:
            best = max(best, v)
            alpha = max(alpha, v)
        else:
            best = min(best, v)
            beta = min(beta, v)
        if alpha >= beta:
            break
    return best, seen


def minimax(tree, maximizing=True):
    """Minimax không cắt tỉa."""
    if not isinstance(tree, list):
        return tree
    vals = [minimax(c, not maximizing) for c in tree]
    return max(vals) if maximizing else min(vals)


def ucb1(wins, visits, total, c=math.sqrt(2)):
    """UCB1 = wins/visits + c·√(ln total / visits)."""
    return wins / visits + c * math.sqrt(math.log(total) / visits)


def pl_models(formula, names):
    """Liệt kê mô hình (dict tên → bool) thoả `formula` (hàm nhận dict)."""
    return [m for m in (dict(zip(names, v)) for v in itertools.product([False, True], repeat=len(names))) if formula(m)]


def pl_entails(kb, alpha, names):
    """KB ⊨ α: α đúng ở mọi mô hình của KB. Trả (kéo theo?, số mô hình của KB, tổng số mô hình)."""
    ms = pl_models(kb, names)
    return all(alpha(m) for m in ms), len(ms), 2 ** len(names)


def forward_chain(rules, facts):
    """Suy diễn tiến cho luật Horn (AIMA PL-FC-ENTAILS): rules = [(tập tiền đề, kết luận)]. Trả thứ tự các mệnh đề MỚI suy ra."""
    count = [len(p) for p, _ in rules]
    known, agenda, order = set(), list(facts), []
    while agenda:
        p = agenda.pop(0)
        if p in known:
            continue
        known.add(p)
        if p not in facts:
            order.append(p)
        for i, (pre, c) in enumerate(rules):
            if p in pre:
                count[i] -= 1
                if count[i] == 0:
                    agenda.append(c)
    return order


def backward_chain(rules, facts, goal, stack=()):
    """Suy diễn lùi (có chặn vòng): trả True nếu chứng minh được `goal`."""
    if goal in facts:
        return True
    if goal in stack:
        return False
    return any(all(backward_chain(rules, facts, p, stack + (goal,)) for p in pre) for pre, c in rules if c == goal)


def blocks_plan(start, goal):
    """Thế giới khối, hành động “đặt x lên y” (y là khối khác hoặc bàn “T”); x và y phải trống. start, goal: tập cặp (x, nằm trên).
    BFS tìm kế hoạch ngắn nhất; trả danh sách (x, y)."""
    from collections import deque
    start = frozenset(start)
    blocks = sorted({x for x, _ in start})

    def clear(s, x):
        return all(y != x for _, y in s)
    prev = {start: None}
    q = deque([start])
    while q:
        u = q.popleft()
        if set(goal) <= u:
            plan = []
            while prev[u]:
                u, act = prev[u]
                plan.append(act)
            return plan[::-1]
        on = dict(u)
        for x in blocks:
            if not clear(u, x):
                continue
            for y in blocks + ["T"]:
                if y != x and y != on[x] and (y == "T" or clear(u, y)):
                    v = frozenset((u - {(x, on[x])}) | {(x, y)})
                    if v not in prev:
                        prev[v] = (u, (x, y))
                        q.append(v)
    return None


ALARM_CPT = {"B": 0.001, "E": 0.002, "A": {(1, 1): 0.95, (1, 0): 0.94, (0, 1): 0.29, (0, 0): 0.001}, "J": {1: 0.90, 0: 0.05}, "M": {1: 0.70, 0: 0.01}}


def alarm_joint(b, e, a, j, m, cpt=ALARM_CPT):
    """P(b, e, a, j, m) = P(b)·P(e)·P(a | b, e)·P(j | a)·P(m | a) — mạng báo trộm (AIMA)."""
    pb = cpt["B"] if b else 1 - cpt["B"]
    pe = cpt["E"] if e else 1 - cpt["E"]
    pa = cpt["A"][(b, e)] if a else 1 - cpt["A"][(b, e)]
    pj = cpt["J"][a] if j else 1 - cpt["J"][a]
    pm = cpt["M"][a] if m else 1 - cpt["M"][a]
    return pb * pe * pa * pj * pm


def alarm_query(var, evidence, cpt=ALARM_CPT):
    """P(var = 1 | evidence) bằng liệt kê mọi biến ẩn."""
    names = ["b", "e", "a", "j", "m"]
    num = den = 0.0
    for vals in itertools.product([0, 1], repeat=5):
        w = dict(zip(names, vals))
        if any(w[k] != v for k, v in evidence.items()):
            continue
        p = alarm_joint(*vals, cpt=cpt)
        den += p
        if w[var]:
            num += p
    return num / den


def grid43(step_reward=-0.04, gamma=1.0, p_ok=0.8, iters=1000, policy_out=False):
    """Lặp giá trị trên thế giới lưới 4×3 của AIMA: tường ở (2,2), đích +1 ở (4,3), −1 ở (4,2) (toạ độ cột, hàng tính từ 1).
    Đi đúng hướng p_ok, lệch sang mỗi bên vuông góc (1 − p_ok)/2; đâm tường thì đứng yên. Trả U (dict (cột, hàng) → giá trị)."""
    cells = [(x, y) for x in range(1, 5) for y in range(1, 4) if (x, y) != (2, 2)]
    term = {(4, 3): 1.0, (4, 2): -1.0}
    mv = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
    side = {"N": "EW", "S": "EW", "E": "NS", "W": "NS"}
    U = {s: 0.0 for s in cells}

    def go(s, a):
        n = (s[0] + mv[a][0], s[1] + mv[a][1])
        return n if n in U else s

    def q(s, a, U):
        q_side = (1 - p_ok) / 2
        return p_ok * U[go(s, a)] + q_side * U[go(s, side[a][0])] + q_side * U[go(s, side[a][1])]
    for _ in range(iters):
        U = {s: term[s] if s in term else step_reward + gamma * max(q(s, a, U) for a in mv) for s in cells}
    if policy_out:
        return U, {s: max(mv, key=lambda a: q(s, a, U)) for s in cells if s not in term}
    return U


def vacuum_reflex(n_cells, loc, dirty, max_steps=20, measure="clean"):
    """Thế giới máy hút bụi n ô trên một hàng (AIMA). Tác tử phản xạ: ô đang đứng bẩn → hút; sạch → đi sang phải, tới mép thì quay trái.
    measure="clean": mỗi bước cộng số ô sạch; measure="sucked": cộng 1 mỗi lần hút (thước đo SAI — xem L00 lỗi 1).
    Trả (dãy hành động tới khi mọi ô sạch, điểm hiệu năng sau các bước đó)."""
    dirty = set(dirty)
    acts, score, direction = [], 0, 1
    for _ in range(max_steps):
        if not dirty:
            break
        if loc in dirty:
            dirty.discard(loc)
            acts.append("hút")
            score += 1 if measure == "sucked" else 0
        else:
            if not 0 <= loc + direction < n_cells:
                direction = -direction
            loc += direction
            acts.append("phải" if direction == 1 else "trái")
        if measure == "clean":
            score += n_cells - len(dirty)
    return acts, score


def vacuum_states(n_cells):
    """Số trạng thái: vị trí máy × mỗi ô bẩn hoặc sạch."""
    return n_cells * 2 ** n_cells


def graph_search(graph, start, goal, mode="bfs"):
    """Tìm kiếm trên đồ thị có trọng số graph = {u: {v: chi phí}} có tập đã thăm.
    mode="bfs": theo chiều rộng (kiểm đích khi SINH nút, như AIMA); mode="ucs": chi phí đều (kiểm đích khi LẤY nút ra).
    Hoà chi phí thì lấy theo thứ tự sinh. Trả (đường đi, tổng chi phí, thứ tự mở rộng)."""
    from collections import deque
    if mode == "bfs":
        if start == goal:
            return [start], 0, []
        parent, q, order = {start: None}, deque([start]), []
        while q:
            u = q.popleft()
            order.append(u)
            for v in graph.get(u, {}):
                if v not in parent:
                    parent[v] = u
                    if v == goal:
                        path = [v]
                        while parent[path[-1]] is not None:
                            path.append(parent[path[-1]])
                        path.reverse()
                        return path, sum(graph[a][b] for a, b in zip(path, path[1:])), order
                    q.append(v)
        return None, None, order
    cnt = itertools.count()
    pq, best, parent, done, order = [(0, next(cnt), start)], {start: 0}, {start: None}, set(), []
    while pq:
        d, _, u = heapq.heappop(pq)
        if u in done:
            continue
        if u == goal:
            path = [u]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            return path[::-1], d, order
        done.add(u)
        order.append(u)
        for v, w in graph.get(u, {}).items():
            if d + w < best.get(v, math.inf):
                best[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (d + w, next(cnt), v))
    return None, None, order


def puz_all_stats():
    """Duyệt hết 181 440 trạng thái đạt được từ đích (BFS ngược; mọi bước đảo được nên khoảng cách tới đích bằng khoảng cách từ đích).
    Trả (h₁ ≤ h₂ ≤ h* ở mọi trạng thái?, khoảng cách lớn nhất, trung bình h₁, trung bình h₂, trung bình h*)."""
    from collections import deque
    d = {PUZ_GOAL: 0}
    q = deque([PUZ_GOAL])
    while q:
        u = q.popleft()
        for v in puz_moves(u):
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    n = len(d)
    ok = all(puz_h1(s) <= puz_h2(s) <= k for s, k in d.items())
    return ok, max(d.values()), sum(puz_h1(s) for s in d) / n, sum(puz_h2(s) for s in d) / n, sum(d.values()) / n


def ucb_bandit(probs, pulls=1000, seed=7, c=math.sqrt(2), greedy=False):
    """Máy đánh bạc nhiều tay: tay i thắng với xác suất probs[i]. Mỗi tay thử một lần, sau đó chọn theo UCB1 (greedy=True: chỉ theo tỉ lệ thắng).
    Trả (số lần kéo mỗi tay, tổng số lần thắng)."""
    rng = random.Random(seed)
    k = len(probs)
    n, w = [0] * k, [0] * k
    for t in range(pulls):
        if t < k:
            i = t
        elif greedy:
            i = max(range(k), key=lambda j: (w[j] / n[j], -j))
        else:
            i = max(range(k), key=lambda j: (ucb1(w[j], n[j], t, c), -j))
        n[i] += 1
        w[i] += rng.random() < probs[i]
    return n, sum(w)


def blocks_apply(state, plan):
    """Thực hiện kế hoạch (danh sách (x, y): đặt x lên y) trên trạng thái thế giới khối; trả tập cặp (x, nằm trên) mới.
    Không kiểm tiền điều kiện — dùng cho kế hoạch do alg.blocks_plan sinh ra."""
    s = set(state)
    for x, y in plan:
        s = {(a, b) for a, b in s if a != x} | {(x, y)}
    return s


def blocks_subgoals(start, subgoals):
    """Đạt TỪNG mục tiêu con theo thứ tự, mỗi lần chỉ nhìn mục tiêu con đó (kế hoạch ngắn nhất cho riêng nó), lặp lại tới khi mọi mục tiêu
    con cùng đúng. Trả danh sách kế hoạch con."""
    s, plans = set(start), []
    for _ in range(10):
        if all(g in s for g in subgoals):
            return plans
        for g in subgoals:
            if g not in s:
                p = blocks_plan(s, {g})
                plans.append(p)
                s = blocks_apply(s, p)
    return plans


# ───────── Mô hình ngôn ngữ lớn (LLM): n-gram, từ tố, vector nhúng, sinh văn bản, chi phí, đánh giá ─────────
LLM_CORPUS = ["<s> tôi thích mèo </s>", "<s> tôi thích chó </s>", "<s> bạn thích mèo </s>"]


def bigram_counts(corpus=LLM_CORPUS):
    """Đếm (đơn từ làm ngữ cảnh, cặp liên tiếp) trên kho câu đã có <s>, </s>."""
    from collections import Counter
    toks = [c.split() for c in corpus]
    uni = Counter(w for t in toks for w in t[:-1])
    bi = Counter((a, b) for t in toks for a, b in zip(t, t[1:]))
    return uni, bi


def bigram_prob(sentence, corpus=LLM_CORPUS, add_k=0):
    """Xác suất câu theo bigram (Fraction). add_k > 0: làm trơn cộng k, từ vựng dự đoán = mọi từ trừ <s>."""
    uni, bi = bigram_counts(corpus)
    vocab = {w for c in corpus for w in c.split()} - {"<s>"}
    s = sentence.split()
    p = Fraction(1)
    for a, b in zip(s, s[1:]):
        num = bi[(a, b)] + add_k
        den = uni[a] + add_k * len(vocab)
        if den == 0:
            return Fraction(0)
        p *= Fraction(num, den)
    return p


def perplexity(prob, n_pred):
    """Độ hỗn loạn = xác suất^(−1/số lần dự đoán)."""
    return float(prob) ** (-1 / n_pred) if prob else math.inf


def bpe_merges(vocab, n):
    """BPE kiểu Sennrich (2016): vocab = {"l o w </w>": tần số}. Trả danh sách (cặp, số lần) của n lần gộp đầu; hoà lấy cặp gặp trước."""
    import re
    from collections import Counter
    out = []
    for _ in range(n):
        st = Counter()
        for w, f in vocab.items():
            sy = w.split()
            for a, b in zip(sy, sy[1:]):
                st[(a, b)] += f
        if not st:
            break
        best = max(st, key=st.get)
        out.append((best, st[best]))
        pat = re.compile(r"(?<!\S)" + re.escape(" ".join(best)) + r"(?!\S)")
        vocab = {pat.sub("".join(best), w): f for w, f in vocab.items()}
    return out, vocab


def cosine(a, b):
    """Độ tương tự cosin."""
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


def causal_mask(n):
    """Mặt nạ nhân quả n × n: 1 nếu vị trí i được nhìn vị trí j (j ≤ i)."""
    return [[1 if j <= i else 0 for j in range(n)] for i in range(n)]


def kv_cache_bytes(layers, d_model, ctx, bytes_per=2, batch=1):
    """Bộ nhớ đệm khoá–giá trị: 2 (khoá, giá trị) · tầng · chiều · độ dài ngữ cảnh · byte mỗi số · số chuỗi."""
    return 2 * layers * d_model * ctx * bytes_per * batch


def softmax_t(z, T=1.0):
    """Hàm chuẩn hoá mũ có nhiệt độ T."""
    m = max(z)
    e = [math.exp((x - m) / T) for x in z]
    s = sum(e)
    return [x / s for x in e]


def top_p_keep(probs, p):
    """Lấy mẫu hạt nhân: giữ ít từ tố nhất (theo xác suất giảm dần) có tổng ≥ p. Trả chỉ số được giữ."""
    order = sorted(range(len(probs)), key=lambda i: -probs[i])
    keep, acc = [], 0.0
    for i in order:
        keep.append(i)
        acc += probs[i]
        if acc >= p:
            break
    return keep


def lora_params(d_in, d_out, r):
    """Số tham số huấn luyện của LoRA hạng r cho ma trận d_out × d_in: r·(d_in + d_out)."""
    return r * (d_in + d_out)


def bradley_terry(r1, r2):
    """Xác suất chọn câu 1 hơn câu 2: σ(r1 − r2)."""
    return 1 / (1 + math.exp(-(r1 - r2)))


def acc_ci95(p, n):
    """Nửa độ rộng khoảng tin cậy 95% xấp xỉ chuẩn cho tỉ lệ đúng p trên n câu."""
    return 1.96 * math.sqrt(p * (1 - p) / n)


def majority_vote(p, k):
    """Xác suất biểu quyết đa số đúng khi mỗi lần đúng độc lập với xác suất p, k lẻ."""
    return sum(math.comb(k, j) * p ** j * (1 - p) ** (k - j) for j in range(k // 2 + 1, k + 1))


def recall_at_k(ranked, relevant, k):
    """Độ phủ@k: tỉ lệ câu hỏi có ít nhất một đoạn đúng trong k đoạn đầu. ranked: [danh sách mã đoạn], relevant: [tập mã đúng]."""
    return sum(1 for r, g in zip(ranked, relevant) if set(r[:k]) & g) / len(ranked)


def train_flops(params, tokens):
    """Ước lượng phép tính huấn luyện C ≈ 6·N·D (Kaplan và cộng sự, 2020)."""
    return 6 * params * tokens


def bpe_encode(word, merges):
    """Tách một từ MỚI theo các luật gộp đã học, áp dụng đúng thứ tự học. merges: danh sách cặp (a, b). Trả danh sách từ tố."""
    sy = list(word) + ["</w>"]
    for a, b in merges:
        i, out = 0, []
        while i < len(sy):
            if i + 1 < len(sy) and sy[i] == a and sy[i + 1] == b:
                out.append(a + b)
                i += 2
            else:
                out.append(sy[i])
                i += 1
        sy = out
    return sy


def paired_sign_p(b, c):
    """Kiểm định dấu chính xác hai phía cho hai mô hình trên CÙNG bộ câu: b = số câu chỉ A đúng, c = số câu chỉ B đúng.
    Dưới giả thuyết không khác nhau, mỗi câu bất đồng nghiêng về A với xác suất 1/2."""
    n, k = b + c, min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def n_for_margin(p, margin, z=1.96):
    """Số câu tối thiểu để nửa độ rộng khoảng tin cậy ≤ margin khi tỉ lệ đúng ≈ p."""
    return math.ceil(z * z * p * (1 - p) / margin ** 2)


def ece(groups):
    """Sai số hiệu chuẩn kỳ vọng: groups = [(số câu, độ tự tin, độ đúng)]; cộng tỉ lệ câu · |độ đúng − độ tự tin|."""
    n = sum(g[0] for g in groups)
    return sum(k / n * abs(acc - conf) for k, conf, acc in groups)


def spec_decode_tokens(alpha, k):
    """Giải mã suy đoán (Leviathan và cộng sự, 2023): mô hình nhỏ đề xuất k từ tố, mỗi từ được chấp nhận với xác suất alpha độc lập.
    Số từ tố kỳ vọng sinh ra sau MỘT lần mô hình lớn kiểm: (1 − alpha^(k+1)) / (1 − alpha)."""
    return (1 - alpha ** (k + 1)) / (1 - alpha)


# ───────── AI agent (AGT): vòng lặp tác tử, công cụ, lập kế hoạch, bộ nhớ, đánh giá, chi phí, an toàn ─────────
def chain_success(p_step, steps):
    """Xác suất hoàn thành nhiệm vụ nhiều bước khi mỗi bước đúng độc lập với xác suất p_step."""
    return p_step ** steps


def chain_with_retry(p_step, steps, tries):
    """Mỗi bước được thử lại tối đa `tries` lần khi PHÁT HIỆN được lỗi (giả định phát hiện chắc chắn, các lần thử độc lập)."""
    return (1 - (1 - p_step) ** tries) ** steps


def check_args(args, schema):
    """Kiểm tham số theo lược đồ tối giản: schema = {tên: (kiểu, hàm kiểm)}. Trả (hợp lệ?, danh sách lỗi). Thiếu, thừa, sai kiểu đều là lỗi."""
    errs = []
    for k, (typ, ok) in schema.items():
        if k not in args:
            errs.append(f"thiếu {k}")
        elif not isinstance(args[k], typ) or isinstance(args[k], bool) and typ is int:
            errs.append(f"{k} sai kiểu")
        elif not ok(args[k]):
            errs.append(f"{k} ngoài miền")
    errs += [f"thừa {k}" for k in args if k not in schema]
    return not errs, errs


def dag_times(dur, deps):
    """Đồ thị phụ thuộc: dur = {bước: thời gian}, deps = {bước: [bước trước]}. Trả (tổng tuần tự, thời điểm xong khi chạy song song tối đa, đường găng)."""
    fin, prev = {}, {}
    order = []
    left = dict(deps)
    while left:
        ready = sorted(k for k, ds in left.items() if all(d in fin for d in ds))
        for k in ready:
            start = max((fin[d] for d in left[k]), default=0)
            prev[k] = max(left[k], key=lambda d: fin[d]) if left[k] else None
            fin[k] = start + dur[k]
            order.append(k)
            del left[k]
    end = max(fin, key=fin.get)
    path = [end]
    while prev[path[-1]]:
        path.append(prev[path[-1]])
    return sum(dur.values()), fin[end], path[::-1]


def turns_until_full(window, system, per_turn):
    """Số lượt hội thoại trước khi đầy ngữ cảnh: ⌊(cửa sổ − lời nhắc hệ thống) / mỗi lượt⌋."""
    return (window - system) // per_turn


def recall_after_rewrites(first, gain, rewrites):
    """Độ phủ sau mỗi lần viết lại truy vấn: mỗi lần tìm thêm `gain` phần của phần còn thiếu (giả định độc lập)."""
    miss = 1 - first
    return 1 - miss * (1 - gain) ** rewrites


def verifier_precision(p_correct, tpr, fpr):
    """Trong các câu bộ kiểm chứng NHẬN, tỉ lệ đúng (Bayes): p·tpr / (p·tpr + (1 − p)·fpr)."""
    return p_correct * tpr / (p_correct * tpr + (1 - p_correct) * fpr)


def best_of_n_verified(p_correct, tpr, fpr, n):
    """Sinh tối đa n câu, trả câu ĐẦU TIÊN được bộ kiểm chứng nhận. Trả (P(có câu được nhận), P(câu trả ra đúng | có câu được nhận))."""
    acc = p_correct * tpr + (1 - p_correct) * fpr
    p_any = 1 - (1 - acc) ** n
    return p_any, verifier_precision(p_correct, tpr, fpr)


def comm_channels(n, topology):
    """Số kênh một chiều: "full" mọi cặp n(n−1); "hub" qua một điều phối 2(n−1)."""
    return n * (n - 1) if topology == "full" else 2 * (n - 1)


def pass_at_k(p, k):
    """Ít nhất một lần thành công trong k lần độc lập."""
    return 1 - (1 - p) ** k


def pass_hat_k(p, k):
    """Thành công cả k lần (độ ổn định)."""
    return p ** k


def pass_at_k_unbiased(n, c, k):
    """Ước lượng không chệch pass@k từ n lần chạy có c lần đúng (Chen và cộng sự, 2021): 1 − C(n − c, k)/C(n, k)."""
    return 1 - math.comb(n - c, k) / math.comb(n, k) if n - c >= k else 1.0


def loop_tokens(start, grow, steps, cached_prefix=0.0):
    """Tổng từ tố đầu vào khi mỗi bước gửi lại toàn bộ ngữ cảnh (bắt đầu `start`, tăng `grow` mỗi bước).
    cached_prefix: phần từ tố được tính giá rẻ nhờ bộ nhớ đệm tiền tố, tính như phần trăm giá (0 = không đệm). Trả (tổng thô, tổng quy đổi)."""
    raw = sum(start + grow * i for i in range(steps))
    if not cached_prefix:
        return raw, raw
    eff = start  # bước đầu: chưa có gì trong bộ nhớ đệm
    for i in range(1, steps):
        prev = start + grow * (i - 1)
        eff += prev * cached_prefix + grow
    return raw, eff


AGT_POLICY = {"đọc trang": "chạy", "tìm kiếm": "chạy", "gửi thư": "hỏi", "chuyển tiền": "hỏi", "xoá dữ liệu": "cấm"}


def tool_gate(action, policy=AGT_POLICY):
    """Cổng quyền cho hành động của tác tử, KHÔNG phụ thuộc ai “ra lệnh” trong ngữ cảnh (người dùng hay nội dung trang web) — vì tác tử không
    phân biệt chắc chắn được. Hành động không có trong chính sách thì cấm (mặc định từ chối). Trả "chạy" / "hỏi" (chờ người dùng xác nhận) / "cấm"."""
    return policy.get(action, "cấm")


def workflow_vs_agent(p_fixed, n_fixed, p_agent, n_agent):
    """So độ tin cậy quy trình cố định (n_fixed bước, mỗi bước p_fixed) với tác tử (trung bình n_agent bước, mỗi bước p_agent)."""
    return p_fixed ** n_fixed, p_agent ** n_agent


def citation_check(claims, sources):
    """Kiểm trích dẫn: claims = [(câu trích, mã nguồn)], sources = {mã: văn bản}. Câu trích phải có NGUYÊN VĂN trong đúng nguồn được dẫn.
    Trả danh sách (mã nguồn, có trong nguồn?, nguồn có tồn tại?)."""
    return [(sid, sid in sources and quote in sources[sid], sid in sources) for quote, sid in claims]


# ───────── Robot tự hành (ROB): chuyển động, đo quãng đường, định vị, bản đồ, lập kế hoạch, điều khiển ─────────
def diff_drive(v_left, v_right, track):
    """Xe hai bánh vi sai: (v, ω, bán kính quay). track = khoảng cách hai bánh. Đi thẳng (ω = 0) thì bán kính vô hạn."""
    v = (v_left + v_right) / 2
    w = (v_right - v_left) / track
    return v, w, (v / w if w else math.inf)


def diff_drive_step(pose, v, w, h):
    """Một bước Euler của mô hình chuyển động: (x, y, θ) → (x + v·h·cos θ, y + v·h·sin θ, θ + ω·h)."""
    x, y, th = pose
    return x + v * h * math.cos(th), y + v * h * math.sin(th), th + w * h


def diff_drive_path(v, w, h, steps, pose=(0.0, 0.0, 0.0)):
    """Lặp diff_drive_step; trả tư thế cuối."""
    for _ in range(steps):
        pose = diff_drive_step(pose, v, w, h)
    return pose


def encoder_mm_per_tick(wheel_diam_m, ticks_per_rev):
    """Quãng đường mỗi xung của bộ mã hoá vòng quay (mm)."""
    return math.pi * wheel_diam_m / ticks_per_rev * 1000


def heading_drift(dist_m, err_deg):
    """Lệch ngang sau quãng đường thẳng dist_m khi hướng lệch err_deg độ."""
    return dist_m * math.sin(math.radians(err_deg))


def gauss_pdf(x, mu, sigma):
    """Mật độ phân phối chuẩn."""
    return math.exp(-(x - mu) ** 2 / (2 * sigma * sigma)) / (sigma * math.sqrt(2 * math.pi))


def beam_likelihood(z, true_d, sigma, w_hit=0.9, w_rand=0.1, z_max=10.0):
    """Mô hình đo khoảng cách hỗn hợp: w_hit·chuẩn(true_d, σ) + w_rand·đều(0, z_max) (Thrun–Burgard–Fox, mục 6.3, rút gọn hai thành phần)."""
    return w_hit * gauss_pdf(z, true_d, sigma) + w_rand / z_max


def hist_filter(belief, meas_like, move=0, p_exact=1.0):
    """Bộ lọc Bayes rời rạc trên hành lang vòng: dịch niềm tin `move` ô (đúng với xác suất p_exact, còn lại chia đều cho lệch ±1 ô),
    rồi nhân với khả năng đo meas_like và chuẩn hoá. Trả danh sách xác suất."""
    n = len(belief)
    if move:
        q = (1 - p_exact) / 2
        b = [0.0] * n
        for i, p in enumerate(belief):
            b[(i + move) % n] += p * p_exact
            b[(i + move - 1) % n] += p * q
            b[(i + move + 1) % n] += p * q
        belief = b
    post = [p * l for p, l in zip(belief, meas_like)]
    s = sum(post)
    return [p / s for p in post]


def ess(weights):
    """Kích thước mẫu hiệu dụng của bộ lọc hạt: 1 / Σ w² (trọng số đã chuẩn hoá)."""
    s = sum(weights)
    return 1 / sum((w / s) ** 2 for w in weights)


def motion_jacobian(theta, vh):
    """Jacobian của (x + vh·cos θ, y + vh·sin θ, θ) theo (x, y, θ)."""
    return [[1, 0, -vh * math.sin(theta)], [0, 1, vh * math.cos(theta)], [0, 0, 1]]


def logodds(p):
    return math.log(p / (1 - p))


def occ_update(p0, p_hit, hits, misses=0, p_miss=0.4):
    """Cập nhật ô lưới chiếm chỗ: log-odds cộng logit(p_hit) mỗi lần “bị chiếm”, logit(p_miss) mỗi lần “trống”, từ log-odds đầu logit(p0).
    Trả xác suất cuối."""
    l = logodds(p0) + hits * (logodds(p_hit) - logodds(p0)) + misses * (logodds(p_miss) - logodds(p0))
    return 1 / (1 + math.exp(-l))


def pose_graph_1d(odom, loops):
    """Đồ thị tư thế 1 chiều: x0 = 0 cố định; odom[i] = độ dời đo được từ x_i tới x_{i+1}; loops = [(i, j, độ dời đo từ x_i tới x_j)].
    Bình phương tối thiểu mọi ràng buộc bằng nhau trọng số. Trả [x1, …, xn]."""
    import numpy as np
    n = len(odom)
    rows, rhs = [], []
    for i, d in enumerate(odom):
        r = [0.0] * n
        if i > 0:
            r[i - 1] = -1
        r[i] = 1
        rows.append(r)
        rhs.append(d)
    for i, j, d in loops:
        r = [0.0] * n
        if i > 0:
            r[i - 1] = -1
        r[j - 1] += 1
        rows.append(r)
        rhs.append(d)
    return list(np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)[0])


def grid_cells(levels, dims):
    """Số ô của lưới đều: levels^dims."""
    return levels ** dims


def dwa_score(heading, clearance, speed, w=(0.4, 0.4, 0.2)):
    """Điểm cửa sổ động: tổng có trọng số (hướng về đích, khoảng trống, tốc độ), mỗi thành phần đã chuẩn hoá về [0, 1]."""
    return w[0] * heading + w[1] * clearance + w[2] * speed


def pure_pursuit(lookahead, lateral):
    """Độ cong lệnh của điểm nhìn trước: κ = 2·y / L² (Coulter 1992)."""
    return 2 * lateral / lookahead ** 2


def pinhole(X, Y, Z, f, cx, cy):
    """Chiếu điểm (X, Y, Z) (hệ camera, Z hướng ra trước) lên ảnh: (u, v) = (f·X/Z + cx, f·Y/Z + cy)."""
    return f * X / Z + cx, f * Y / Z + cy


def stop_distance(v, decel, t_react):
    """Quãng dừng: v·t_phản_ứng + v² / (2·a)."""
    return v * t_react + v * v / (2 * decel)


def occ_sequence(p0, p_hit, p_miss, events, clamp=None):
    """Chuỗi cập nhật log-odds cho một ô: events là chuỗi 'h' (thấy chiếm) / 'm' (thấy trống). clamp: chặn |log-odds| ≤ clamp sau mỗi bước.
    Trả xác suất cuối."""
    l, l0 = logodds(p0), logodds(p0)
    for e in events:
        l += (logodds(p_hit) if e == 'h' else logodds(p_miss)) - l0
        if clamp is not None:
            l = max(-clamp, min(clamp, l))
    return 1 / (1 + math.exp(-l))


def stereo_depth(f_px, baseline_m, disparity_px):
    """Độ sâu từ hai camera song song: Z = f·B / d (f tiêu cự điểm ảnh, B khoảng cách hai camera, d độ chênh vị trí điểm ảnh)."""
    return f_px * baseline_m / disparity_px


def max_safe_speed(sense_range, decel, t_react):
    """Tốc độ lớn nhất còn dừng kịp trong tầm phát hiện R: nghiệm dương của v·t + v²/(2a) = R, tức v = −a·t + √(a²t² + 2aR)."""
    return -decel * t_react + math.sqrt(decel * decel * t_react * t_react + 2 * decel * sense_range)


# ═══════════ DEN — Kỹ thuật dữ liệu ═══════════
def scan_bytes(rows, cols, bytes_per, layout="row", cols_used=None):
    """Số byte phải đọc: lưu theo hàng đọc mọi cột; lưu theo cột chỉ đọc các cột truy vấn dùng (bỏ qua nén, siêu dữ liệu)."""
    return rows * (cols if layout == "row" else cols_used) * bytes_per


def bloom_extra_reads(n_tables, fpr):
    """Kỳ vọng số lần đọc đĩa thừa khi tìm khoá KHÔNG tồn tại qua n tệp bảng, mỗi tệp có bộ lọc dương tính giả fpr."""
    return n_tables * fpr


def bloom_bits_per_key(fpr):
    """Số bit mỗi khoá tối ưu cho bộ lọc nhiều hàm băm: −ln p / (ln 2)², và số hàm băm tối ưu (bit/khoá)·ln 2."""
    m = -math.log(fpr) / math.log(2) ** 2
    return m, m * math.log(2)


def lsm_lookup(tables, key, memtable=None):
    """Đường đọc của cây gộp theo nhật ký: bộ đệm ghi trước, rồi các tệp bảng từ MỚI tới CŨ; giá trị None là bia mộ (đã xoá).
    tables: danh sách dict theo thứ tự cũ → mới. Trả (giá trị hoặc None, số tệp đã xem)."""
    if memtable and key in memtable:
        return memtable[key], 0
    seen = 0
    for t in reversed(tables):
        seen += 1
        if key in t:
            return t[key], seen
    return None, seen


def lsm_compact(tables):
    """Gộp các tệp bảng (cũ → mới): bản mới nhất thắng, bỏ hẳn khoá có bia mộ (None)."""
    out = {}
    for t in tables:
        out.update(t)
    return {k: v for k, v in out.items() if v is not None}


def partition_loads(keys, n_parts, part_fn):
    """Tỉ lệ lượt ghi mỗi phân vùng khi phân vùng bằng part_fn(key) → số 0..n_parts−1."""
    from collections import Counter
    c = Counter(part_fn(k) for k in keys)
    return [c.get(i, 0) / len(keys) for i in range(n_parts)]


def stable_hash(s):
    """Băm ổn định giữa các lần chạy (FNV-1a 32 bit) — hàm hash() của Python đổi theo mỗi tiến trình."""
    h = 2166136261
    for b in str(s).encode("utf-8"):
        h = ((h ^ b) * 16777619) % 2 ** 32
    return h


def graph_reach_bound(deg, hops):
    """Cận trên số đỉnh chạm tới sau đúng `hops` bước khi mỗi đỉnh có `deg` cạnh (không trừ trùng)."""
    return deg ** hops


def graph_reach(adj, start, hops):
    """Số đỉnh KHÁC NHAU cách start đúng tới `hops` bước (duyệt theo chiều rộng), không tính start."""
    seen, frontier = {start}, {start}
    for _ in range(hops):
        frontier = {v for u in frontier for v in adj.get(u, ())} - seen
        seen |= frontier
    return len(seen) - 1


def inverted_index(docs):
    """Chỉ mục ngược: từ → danh sách (mã văn bản, số lần xuất hiện), mã văn bản đánh từ 1."""
    idx = {}
    for i, d in enumerate(docs, 1):
        for t in dict.fromkeys(d):
            idx.setdefault(t, []).append((i, d.count(t)))
    return idx


def bm25_idf(n_docs, df):
    """IDF của BM25 (dạng Lucene, luôn dương): ln(1 + (N − n + 0,5)/(n + 0,5))."""
    return math.log(1 + (n_docs - df + 0.5) / (df + 0.5))


def bm25(query, docs, k1=1.2, b=0.75):
    """Điểm BM25 của từng văn bản (danh sách từ) cho truy vấn (danh sách từ) — Robertson & Zaragoza (2009)."""
    N = len(docs)
    avg = sum(map(len, docs)) / N
    out = []
    for d in docs:
        s = 0.0
        for t in query:
            tf = d.count(t)
            if tf:
                s += bm25_idf(N, sum(t in x for x in docs)) * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
        out.append(s)
    return out


def range_assign(n_parts, n_consumers):
    """Chia n phân vùng cho các thành viên nhóm tiêu thụ theo khoảng: mỗi người ⌊P/C⌋, P mod C người đầu thêm 1."""
    return [n_parts // n_consumers + (1 if i < n_parts % n_consumers else 0) for i in range(n_consumers)]


def replay_events(ckpt_period_s, crash_at_s, rate_per_s):
    """Số sự kiện phải xử lý lại khi sập ở crash_at_s với điểm kiểm tra mỗi ckpt_period_s giây (điểm cuối tại bội số gần nhất)."""
    return (crash_at_s % ckpt_period_s) * rate_per_s


def dual_write_sim(n, p_crash, seed=7, outbox=False):
    """Mô phỏng n đơn: ghi cơ sở dữ liệu rồi gửi sự kiện, sập giữa hai bước với xác suất p_crash.
    Không hộp thư đi: sự kiện mất. Có hộp thư đi: sự kiện nằm trong cùng giao dịch, bộ chuyển tiếp gửi lại → không mất, nhưng có thể trùng.
    Trả (số đơn mất sự kiện, số sự kiện gửi trùng)."""
    import random
    r = random.Random(seed)
    lost = dup = 0
    for _ in range(n):
        crash = r.random() < p_crash
        if not outbox:
            lost += crash
        else:
            dup += crash  # bộ chuyển tiếp sập SAU khi gửi, TRƯỚC khi đánh dấu đã gửi → gửi lại
    return lost, dup


def rowgroups_read(groups, lo, hi):
    """Số nhóm hàng phải đọc cho điều kiện lo ≤ x ≤ hi khi mỗi nhóm có thống kê nhỏ nhất–lớn nhất."""
    return sum(1 for g in groups if not (max(g) < lo or min(g) > hi))


def scd_report(scd2=True):
    """Kho dữ liệu nhỏ trên sqlite3: khách k1 chuyển Hà Nội → Đà Nẵng ngày 2026-03-01. Doanh thu theo (tháng, tỉnh).
    scd2=True: bảng chiều lưu lịch sử (khoảng hiệu lực); False: ghi đè (chỉ giữ dòng hiện tại)."""
    import sqlite3
    cn = sqlite3.connect(":memory:")
    cn.executescript("""CREATE TABLE dim_kh(sk INT, kh TEXT, tinh TEXT, tu TEXT, den TEXT);
INSERT INTO dim_kh VALUES (1,'k1','Hà Nội','2026-01-01','2026-03-01'),(2,'k1','Đà Nẵng','2026-03-01','9999-12-31');
CREATE TABLE fact(ngay TEXT, kh TEXT, tien INT);
INSERT INTO fact VALUES ('2026-02-10','k1',100),('2026-03-10','k1',200);""")
    cond = "f.ngay >= d.tu AND f.ngay < d.den" if scd2 else "d.den = '9999-12-31'"
    return cn.execute(f"SELECT substr(f.ngay,1,7), d.tinh, SUM(f.tien) FROM fact f JOIN dim_kh d ON d.kh = f.kh AND {cond} GROUP BY 1, 2 ORDER BY 1").fetchall()


def join_network_gb(big_gb, small_gb, machines, strategy):
    """Lượng dữ liệu gửi qua mạng khi nối: 'broadcast' gửi bảng nhỏ tới mọi máy khác; 'shuffle' băm lại cả hai bảng,
    mỗi dòng ở lại máy cũ với xác suất 1/machines."""
    if strategy == "broadcast":
        return small_gb * (machines - 1)
    return (big_gb + small_gb) * (machines - 1) / machines


def tiered_compaction_wa(n_flushes, fanout, wal=True):
    """Mô phỏng gộp theo bậc kích thước: mỗi lần xả ghi 1 đơn vị; khi có `fanout` tệp cùng bậc thì gộp thành một tệp bậc trên
    (ghi lại toàn bộ). Trả tổng số đơn vị đã ghi / số đơn vị đưa vào (khuếch đại ghi), cộng 1 cho nhật ký ghi trước nếu wal."""
    tiers = {}
    written = 0
    for _ in range(n_flushes):
        written += 1
        lvl, size = 0, 1
        tiers[lvl] = tiers.get(lvl, 0) + 1
        while tiers.get(lvl, 0) == fanout:
            tiers[lvl] = 0
            size *= fanout
            written += size
            lvl += 1
            tiers[lvl] = tiers.get(lvl, 0) + 1
    return written / n_flushes + (1 if wal else 0)


def btree_depth(n_keys, fanout):
    """Số tầng nhỏ nhất của cây B để chứa n_keys khoá khi mỗi nút có `fanout` con: nhỏ nhất d với fanout^d ≥ n_keys."""
    d, cap = 0, 1
    while cap < n_keys:
        cap *= fanout
        d += 1
    return d


# ═══════════ WEB — Web và di động ═══════════
def rtt_before_first_byte(rtt_ms, rounds=3):
    """Thời gian trước byte phản hồi đầu tiên khi mỗi bước (bắt tay giao vận, bắt tay mã hoá, yêu cầu) tốn một vòng khứ hồi."""
    return rtt_ms * rounds


def html_tree_stats(html):
    """Đếm số phần tử và độ sâu lớn nhất của cây phần tử dựng từ mã HTML (html.parser của thư viện chuẩn; bỏ qua thẻ rỗng như br, img)."""
    from html.parser import HTMLParser
    void = {"br", "img", "hr", "input", "meta", "link"}

    class P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.n = self.d = self.mx = 0

        def handle_starttag(self, tag, attrs):
            self.n += 1
            if tag not in void:
                self.d += 1
                self.mx = max(self.mx, self.d)
            else:
                self.mx = max(self.mx, self.d + 1)

        def handle_endtag(self, tag):
            if tag not in void:
                self.d -= 1
    p = P()
    p.feed(html)
    return p.n, p.mx


def box_width(content, padding, border, margin=0, sizing="content-box"):
    """Bề rộng hộp CSS chiếm trên trang (chưa tính lề ngoài nếu margin = 0). content-box: rộng = nội dung, cộng đệm và viền hai bên;
    border-box: rộng đã gồm đệm và viền."""
    if sizing == "border-box":
        return content + 2 * margin
    return content + 2 * padding + 2 * border + 2 * margin


def specificity(selector):
    """Độ ưu tiên (mã, lớp / thuộc tính / lớp giả, thẻ) của một bộ chọn CSS đơn giản: #id, .lop, [thuộc tính], :lớp giả, tên thẻ, tổ hợp bằng
    dấu cách hay > + ~. Không xử lý :is(), :not(), :where()."""
    import re
    s = re.sub(r"[>+~]", " ", selector)
    ids = len(re.findall(r"#[\w-]+", s))
    cls = len(re.findall(r"\.[\w-]+", s)) + len(re.findall(r"\[[^\]]*\]", s)) + len(re.findall(r"(?<!:):[\w-]+", s))
    s2 = re.sub(r"#[\w-]+|\.[\w-]+|\[[^\]]*\]|::?[\w-]+", " ", s)
    tags = len([t for t in s2.split() if t and t != "*"])
    return ids, cls, tags


def node_output(js, timeout=30):
    """Chạy mã JavaScript bằng Node thật, trả danh sách các từ đã in (None nếu không có Node)."""
    import subprocess
    try:
        return subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=timeout).stdout.split()
    except Exception:
        return None


def keyed_moves(old, new):
    """Số phần tử tối thiểu phải di chuyển khi so khớp danh sách có khoá: len − độ dài dãy con tăng dài nhất của vị trí cũ."""
    import bisect
    t = []
    for x in [old.index(k) for k in new if k in old]:
        i = bisect.bisect_left(t, x)
        t[i:i + 1] = [x]
    return len([k for k in new if k in old]) - len(t)


HTTP_METHODS = {"GET": (True, True), "HEAD": (True, True), "OPTIONS": (True, True), "PUT": (False, True), "DELETE": (False, True),
                "POST": (False, False), "PATCH": (False, False)}  # (an toàn, lũy đẳng) theo RFC 9110 mục 9.2.1–9.2.2


def offset_page(page, size, n_rows=30000, cursor=False):
    """sqlite3 thật: bảng id 1..n_rows có chỉ mục khoá chính. Trả (danh sách id của trang, số dòng bị bỏ qua).
    cursor=False: LIMIT size OFFSET (page−1)·size; cursor=True: WHERE id > id cuối trang trước."""
    import sqlite3
    cn = sqlite3.connect(":memory:")
    cn.execute("CREATE TABLE t(id INTEGER PRIMARY KEY, v)")
    cn.executemany("INSERT INTO t VALUES (?, ?)", ((i, i) for i in range(1, n_rows + 1)))
    skip = (page - 1) * size
    if cursor:
        rows = cn.execute("SELECT id FROM t WHERE id > ? ORDER BY id LIMIT ?", (skip, size)).fetchall()
        return [r[0] for r in rows], 0
    rows = cn.execute("SELECT id FROM t ORDER BY id LIMIT ? OFFSET ?", (size, skip)).fetchall()
    return [r[0] for r in rows], skip


def cache_fresh(age_s, max_age_s):
    """RFC 9111 mục 4.2: bản lưu còn tươi khi tuổi hiện tại nhỏ hơn thời gian tươi (max-age)."""
    return age_s < max_age_s


def pkce_challenge(verifier):
    """RFC 7636 mục 4.2, phương thức S256: base64url(SHA-256(verifier)) bỏ dấu = ở cuối."""
    import base64
    import hashlib
    return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode()


def load_seconds(n_bytes, bytes_per_s):
    return n_bytes / bytes_per_s


def wcag_luminance(hex6):
    """Độ chói tương đối theo WCAG 2.x (sRGB): kênh c ≤ 0,04045 thì c/12,92, ngược lại ((c + 0,055)/1,055)^2,4."""
    c = [int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def wcag_contrast(fg, bg):
    """Tỉ số tương phản (L sáng + 0,05) / (L tối + 0,05)."""
    a, b = wcag_luminance(fg), wcag_luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def frame_budget_ms(hz):
    return 1000 / hz


def lww_merge(a, b):
    """Ghi sau thắng: giữ nguyên giá trị có dấu thời gian lớn hơn. a, b = (thời điểm, giá trị)."""
    return a if a[0] >= b[0] else b


def old_version_share(p_update_per_week, weeks):
    """Tỉ lệ người dùng còn bản cũ sau `weeks` tuần khi mỗi tuần p người còn lại cập nhật (mô hình hình học, SỐ MINH HOẠ)."""
    return (1 - p_update_per_week) ** weeks


def api_retry_sim(n_requests, p_lost_response, idempotency_key=False, seed=1):
    """Khách gửi POST tạo đơn; phản hồi bị mất với xác suất p (máy chủ ĐÃ tạo đơn), khách gửi lại tới khi nhận phản hồi.
    Không khoá lũy đẳng: mỗi lần gửi lại tạo thêm một đơn. Có khoá: máy chủ nhớ khoá, trả lại kết quả cũ. Trả số đơn đã tạo."""
    import random
    r = random.Random(seed)
    created, seen = 0, set()
    for i in range(n_requests):
        while True:
            if idempotency_key:
                if i not in seen:
                    seen.add(i)
                    created += 1
            else:
                created += 1
            if r.random() >= p_lost_response:
                break
    return created


def offset_insert_anomaly(n=50, size=10, cursor=False):
    """Danh sách mới nhất trước (id giảm dần). Đọc trang 1, rồi một bản ghi mới được thêm, rồi đọc trang 2.
    Theo độ lệch: dòng cuối trang 1 xuất hiện lại ở đầu trang 2. Theo con trỏ (id < id cuối trang 1): không trùng.
    Trả danh sách id bị trùng giữa hai trang."""
    import sqlite3
    cn = sqlite3.connect(":memory:")
    cn.execute("CREATE TABLE t(id INTEGER PRIMARY KEY)")
    cn.executemany("INSERT INTO t VALUES (?)", ((i,) for i in range(1, n + 1)))
    p1 = [r[0] for r in cn.execute("SELECT id FROM t ORDER BY id DESC LIMIT ?", (size,))]
    cn.execute("INSERT INTO t VALUES (?)", (n + 1,))
    if cursor:
        p2 = [r[0] for r in cn.execute("SELECT id FROM t WHERE id < ? ORDER BY id DESC LIMIT ?", (p1[-1], size))]
    else:
        p2 = [r[0] for r in cn.execute("SELECT id FROM t ORDER BY id DESC LIMIT ? OFFSET ?", (size, size))]
    return sorted(set(p1) & set(p2))


def http_cache_decision(age_s, max_age_s, cached_etag, server_etag):
    """Bộ nhớ đệm HTTP rút gọn (RFC 9111 mục 4.2–4.3): còn tươi → dùng bản lưu, không hỏi máy chủ; đã cũ → gửi yêu cầu có điều kiện
    If-None-Match: thẻ khớp → 304 (không gửi lại thân), không khớp → 200 kèm thân mới."""
    if age_s < max_age_s:
        return "fresh"
    return 304 if cached_etag == server_etag else 200


# ═══════════ CLC — Điện toán đám mây ═══════════
def parallel_availability(a, n):
    """Độ sẵn sàng khi chạy song song n bản, mỗi bản sẵn sàng a, hỏng ĐỘC LẬP: 1 − (1 − a)^n."""
    return 1 - (1 - a) ** n


def subnet_plan(cidr, new_prefix, reserved=5):
    """Chia dải địa chỉ thành mạng con (ipaddress thật); trả (số mạng con, địa chỉ mỗi mạng, địa chỉ dùng được sau khi nhà cung cấp giữ `reserved`)."""
    import ipaddress
    subs = list(ipaddress.ip_network(cidr).subnets(new_prefix=new_prefix))
    return len(subs), subs[0].num_addresses, subs[0].num_addresses - reserved


def iam_eval(policies, action, resource):
    """Đánh giá chính sách kiểu “mặc định từ chối, từ chối tường minh thắng”: policies = [(hiệu lực 'allow'|'deny', tập thao tác hoặc {'*'},
    tài nguyên hoặc '*')]. Có deny khớp → 'deny'; không deny mà có allow khớp → 'allow'; không gì khớp → 'implicit-deny'."""
    match = lambda acts, r: (action in acts or "*" in acts) and (r == resource or r == "*")
    if any(e == "deny" and match(a, r) for e, a, r in policies):
        return "deny"
    if any(e == "allow" and match(a, r) for e, a, r in policies):
        return "allow"
    return "implicit-deny"


def expected_object_loss(n_objects, durability):
    """Kỳ vọng số đối tượng mất mỗi năm = n · (1 − độ bền năm)."""
    return n_objects * (1 - durability)


def breakeven_hours(upfront, hourly):
    return upfront / hourly


def faas_gb_seconds(invocations, seconds_each, memory_gb):
    return invocations * seconds_each * memory_gb


def faas_cost(invocations, seconds_each, memory_gb, price_per_gb_s, price_per_million_req):
    """Chi phí hàm theo sự kiện = GB-giây · đơn giá + số lần gọi / 10^6 · đơn giá mỗi triệu lần (SỐ MINH HOẠ, chưa trừ hạn mức miễn phí)."""
    return faas_gb_seconds(invocations, seconds_each, memory_gb) * price_per_gb_s + invocations / 1e6 * price_per_million_req


def worst_data_loss_minutes(snapshot_every_min, log_ship_every_min=None):
    """Lượng dữ liệu mất tối đa (phút) khi khôi phục: khoảng giữa hai lần đẩy nhật ký nếu có, nếu không thì giữa hai lần chụp nhanh."""
    return log_ship_every_min if log_ship_every_min else snapshot_every_min


def egress_cost(tb, price_per_gb, gb_per_tb=1024):
    return tb * gb_per_tb * price_per_gb


def envelope_rewrap_bytes(n_data_keys, key_bytes=32):
    """Xoay khoá chính trong mã hoá phong bì: chỉ mã hoá lại các khoá dữ liệu, không chạm dữ liệu."""
    return n_data_keys * key_bytes


def dr_standing_capacity(n_regions, strategy):
    """Dung lượng thường trực (bội số của tải đầy) cho khôi phục thảm hoạ: 'active-active' n vùng, mỗi vùng phải gánh 100% khi các vùng
    khác hỏng → n; 'warm' (vùng dự phòng chạy nhỏ, ví dụ 20%) → 1,2; 'pilot-light' (chỉ dữ liệu, máy tắt) ≈ 1; 'backup' → 1."""
    return {"active-active": float(n_regions), "warm": 1.2, "pilot-light": 1.0, "backup": 1.0}[strategy]


def active_active_capacity(n_regions, tolerate_failures=1):
    """Chủ động–chủ động trên n vùng, phải chịu được f vùng hỏng: mỗi vùng cần gánh 1/(n − f) tải đầy; tổng dung lượng thường trực n/(n − f)."""
    per = 1 / (n_regions - tolerate_failures)
    return per, n_regions * per


# ═══════════ BCH — Blockchain ═══════════
def block_hash(prev_hex, data):
    """Mã băm khối = SHA-256(mã khối trước | dữ liệu), dạng hex."""
    import hashlib
    return hashlib.sha256((prev_hex + "|" + data).encode("utf-8")).hexdigest()


def build_chain(datas, genesis_prev="0" * 64):
    """Trả danh sách mã băm đã lưu cho từng khối của chuỗi."""
    out, p = [], genesis_prev
    for d in datas:
        p = block_hash(p, d)
        out.append(p)
    return out


def first_bad_block(datas, stored, genesis_prev="0" * 64):
    """Kiểm chuỗi: tính lại mã từng khối từ dữ liệu và mã ĐÃ LƯU của khối trước; trả chỉ số (từ 0) của khối đầu tiên không khớp, hoặc None."""
    p = genesis_prev
    for i, d in enumerate(datas):
        if block_hash(p, d) != stored[i]:
            return i
        p = stored[i]
    return None


def merkle_levels(leaves):
    """Các tầng của cây Merkle nhị phân (số lá là lũy thừa của 2): tầng 0 là băm của lá, tầng cuối là gốc. Mỗi mã 32 byte."""
    import hashlib
    lv = [hashlib.sha256(x).digest() for x in leaves]
    levels = [lv]
    while len(lv) > 1:
        lv = [hashlib.sha256(lv[i] + lv[i + 1]).digest() for i in range(0, len(lv), 2)]
        levels.append(lv)
    return levels


def merkle_proof(levels, idx):
    """Bằng chứng thuộc về của lá idx: danh sách mã anh em từ dưới lên."""
    proof = []
    for lv in levels[:-1]:
        proof.append(lv[idx ^ 1])
        idx //= 2
    return proof


def merkle_verify(leaf, idx, proof, root):
    import hashlib
    h = hashlib.sha256(leaf).digest()
    for sib in proof:
        h = hashlib.sha256(h + sib).digest() if idx % 2 == 0 else hashlib.sha256(sib + h).digest()
        idx //= 2
    return h == root


def toy_rsa_sign(msg, n=3233, d=2753):
    """Chữ ký RSA ĐỒ CHƠI (n = 61 · 53): ký băm SHA-256 của thông điệp lấy dư n. Chỉ để minh hoạ — khoá thật dài 2048 bit trở lên."""
    import hashlib
    return pow(int(hashlib.sha256(msg.encode("utf-8")).hexdigest(), 16) % n, d, n)


def toy_rsa_verify(msg, sig, n=3233, e=17):
    import hashlib
    return pow(sig, e, n) == int(hashlib.sha256(msg.encode("utf-8")).hexdigest(), 16) % n


def utxo_select(coins, amount, fee):
    """Chọn đồng chưa tiêu từ lớn tới nhỏ tới khi đủ amount + fee; trả (đồng dùng, đầu ra người nhận, tiền thừa). Dùng số nguyên phần mười để tránh lỗi làm tròn."""
    need = round((amount + fee) * 10)
    used, tot = [], 0
    for c in sorted(coins, reverse=True):
        if tot >= need:
            break
        used.append(c)
        tot += round(c * 10)
    if tot < need:
        return None
    return used, amount, (tot - need) / 10


def pow_mine(header, zero_bits):
    """Thử nonce = 0, 1, 2, … tới khi SHA-256(header | nonce) có zero_bits bit đầu bằng 0; trả số lần thử."""
    import hashlib
    target = 1 << (256 - zero_bits)
    nonce = 0
    while True:
        if int.from_bytes(hashlib.sha256(header + b"|" + str(nonce).encode()).digest(), "big") < target:
            return nonce + 1
        nonce += 1


def nakamoto_catch_up(q, z):
    """Xác suất kẻ tấn công nắm tỉ lệ q sức tính đuổi kịp sau z khối xác nhận (Nakamoto 2008, mục 11)."""
    p = 1 - q
    if q >= p:
        return 1.0
    lam = z * q / p
    return 1 - sum(math.exp(-lam) * lam ** k / math.factorial(k) * (1 - (q / p) ** (z - k)) for k in range(z + 1))


def bft_tolerance(n):
    """Đồng thuận chịu lỗi Byzantine cần n ≥ 3f + 1: f = ⌊(n − 1)/3⌋; số phiếu chốt = n − f (hai nhóm n − f phiếu giao nhau ít nhất n − 2f ≥ f + 1 bên,
    nên luôn có một bên trung thực chung). Khi n = 3f + 1 đúng, n − f = 2f + 1."""
    f = (n - 1) // 3
    return f, n - f


def gas_fee_eth(gas, gwei):
    return gas * gwei * 1e-9


def reentrancy_vault(pool, deposit, checks_effects_interactions):
    """Mô phỏng KHÁI NIỆM lỗi gọi lại: kho có `pool` đơn vị, kẻ gửi `deposit`. Gửi tiền ra ngoài làm kích hoạt lại hàm rút (mô phỏng bên nhận gọi lại).
    Sai thứ tự (gửi trước, trừ số dư sau) → rút lặp tới cạn; đúng thứ tự (trừ trước) → chỉ rút đúng phần mình. Trả tổng rút được."""
    bal = {"x": deposit}
    state = {"pool": pool}

    def withdraw():
        amt = bal["x"]
        if amt <= 0 or state["pool"] < amt:
            return 0
        if checks_effects_interactions:
            bal["x"] = 0
            state["pool"] -= amt
            return amt + withdraw()   # bên nhận gọi lại: số dư đã về 0 nên không rút thêm
        state["pool"] -= amt
        got = amt + withdraw()        # bên nhận gọi lại TRƯỚC khi số dư bị trừ
        bal["x"] = 0
        return got
    return withdraw()


def chain_tps(block_bytes, tx_bytes, block_seconds):
    return block_bytes / tx_bytes / block_seconds


def median_oracle(values):
    s = sorted(values)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def exact_double_spend(q, z):
    """Xác suất CHÍNH XÁC kẻ tấn công (tỉ lệ q) rốt cuộc đuổi kịp sau z khối xác nhận, khi số khối kẻ tấn công đào được trong lúc chờ
    có phân phối nhị thức âm (không xấp xỉ Poisson): P = 1 − Σ_{k=0}^{z−1} C(k + z − 1, k)(p^z q^k − q^z p^k)
    (C. Grunspan, R. Pérez-Marco, Double spend races, 2018). Cao hơn công thức xấp xỉ của Nakamoto (2008)."""
    p = 1 - q
    if q >= p:
        return 1.0
    return 1 - sum(math.comb(k + z - 1, k) * (p ** z * q ** k - q ** z * p ** k) for k in range(z))


# ═══════════ DAN — Phân tích dữ liệu ═══════════
DAN_LOG = [("u1", "dang_nhap"), ("u1", "xem"), ("u2", "dang_nhap"), ("u2", "mua"), ("u3", "dang_nhap"), ("u4", "dang_nhap"), ("u4", "xem"),
           ("u5", "dang_nhap"), ("u6", "dang_nhap"), ("u6", "binh_luan")]


def dan_active(log, definition):
    """Số người dùng hoạt động theo hai định nghĩa: 'login' = có đăng nhập; 'action' = có ít nhất một thao tác khác đăng nhập."""
    if definition == "login":
        return len({u for u, e in log if e == "dang_nhap"})
    return len({u for u, e in log if e != "dang_nhap"})


def dan_db():
    """sqlite3 thật trong bộ nhớ: bảng don(id, cua_hang, tong), dong(don, sp, sl), dt(ngay, tien)."""
    import sqlite3
    cn = sqlite3.connect(":memory:")
    cn.executescript("""CREATE TABLE don(id INT, cua_hang TEXT, tong INT);
INSERT INTO don VALUES (1,'A',100),(2,'A',50);
CREATE TABLE dong(don INT, sp TEXT, sl INT);
INSERT INTO dong VALUES (1,'a',1),(1,'b',2),(1,'c',1),(2,'a',3);
CREATE TABLE dt(ngay INT, tien INT);
INSERT INTO dt VALUES (1,10),(2,30),(3,20),(4,40);""")
    return cn


def dan_sql(query, cn=None):
    """Chạy một câu truy vấn trên dan_db() (hoặc kết nối cho trước), trả danh sách bộ."""
    return (cn or dan_db()).execute(query).fetchall()


def weighted_mean(groups):
    """groups = [(số phần tử, trung bình nhóm)]: trung bình chung có trọng số."""
    return sum(n * m for n, m in groups) / sum(n for n, _ in groups)


def moving_average(xs, k):
    return [sum(xs[i - k + 1:i + 1]) / k for i in range(k - 1, len(xs))]


def mae(actual, forecast):
    return sum(abs(a - f) for a, f in zip(actual, forecast)) / len(actual)


def mape(actual, forecast):
    """Sai số phần trăm tuyệt đối trung bình; trả None khi có giá trị thực tế bằng 0 (không xác định)."""
    if any(a == 0 for a in actual):
        return None
    return sum(abs(a - f) / abs(a) for a, f in zip(actual, forecast)) / len(actual) * 100


def seasonal_naive(xs, season, h):
    """Dự báo ngây thơ theo mùa: giá trị h bước tới = giá trị cùng vị trí ở mùa gần nhất."""
    return [xs[len(xs) - season + (i % season)] for i in range(h)]


def top_share(values, frac):
    s = sorted(values, reverse=True)
    k = max(1, round(len(s) * frac))
    return sum(s[:k]) / sum(s)


def robust_z(xs, x):
    """Điểm bền vững: (x − trung vị) / (1,4826 · MAD) — 1,4826 làm MAD khớp độ lệch chuẩn khi dữ liệu chuẩn."""
    import statistics
    m = statistics.median(xs)
    mad_ = statistics.median([abs(v - m) for v in xs])
    return (x - m) / (1.4826 * mad_)


def z_score(xs, x):
    import statistics
    return (x - statistics.mean(xs)) / statistics.pstdev(xs)


def wilson(k, n, z=1.96):
    """Khoảng tin cậy Wilson (1927) cho tỉ lệ k/n."""
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def funnel(counts):
    """Tỉ lệ chuyển từng bước và toàn phễu (phần trăm)."""
    return [counts[i + 1] / counts[i] * 100 for i in range(len(counts) - 1)], counts[-1] / counts[0] * 100


def cohort_retention(cohorts):
    """cohorts = {nhóm: [số người kỳ 0, kỳ 1, …]} → {nhóm: [tỉ lệ còn lại kỳ 1, kỳ 2, …]} (phần trăm)."""
    return {c: [v / xs[0] * 100 for v in xs[1:]] for c, xs in cohorts.items()}


# ═══════════ EVT — Kiến trúc hướng sự kiện ═══════════
def point_to_point_links(n):
    return n * (n - 1) // 2


def consume_with_dlq(n, poison_ids, max_retry=None):
    """Tiêu thụ tuần tự n thông điệp của một phân vùng. Thông điệp độc luôn lỗi: không có kênh thư chết (max_retry None) thì kẹt tại đó;
    có thì thử max_retry lần rồi chuyển sang kênh thư chết. Trả (đã xử lý, nằm ở kênh thư chết, số lần thử tổng)."""
    done = dead = tries = 0
    for i in range(1, n + 1):
        if i in poison_ids:
            if max_retry is None:
                return done, dead, None
            tries += max_retry
            dead += 1
            continue
        done += 1
        tries += 1
    return done, dead, tries


def apply_versioned(updates, guard=True):
    """updates = [(phiên bản, giá trị)] theo thứ tự ĐẾN. guard: chỉ nhận phiên bản lớn hơn bản đang giữ. Trả (phiên bản, giá trị) cuối."""
    cur = (0, None)
    for v, val in updates:
        if not guard or v > cur[0]:
            cur = (v, val)
    return cur


def fold_events(events, start=0):
    """Ghi nguồn sự kiện: trạng thái = gấp các sự kiện (ở đây số dư tài khoản: mỗi sự kiện là một số cộng vào)."""
    s = start
    for e in events:
        s += e
    return s


def replay_cost(n_events, snapshot_every):
    """Số sự kiện tối đa phải phát lại sau ảnh chụp gần nhất."""
    return snapshot_every - 1 if snapshot_every and n_events >= snapshot_every else n_events


def saga_run(steps, fail_at):
    """steps = [(tên bước, tên bù trừ hoặc None)]; bước thứ fail_at (đếm từ 0) lỗi. Trả (các bước đã làm, các bù trừ chạy theo thứ tự)."""
    done = [s for s, _ in steps[:fail_at]]
    comp = [c for s, c in reversed(steps[:fail_at]) if c]
    return done, comp


def window_join(left, right, window):
    """Nối luồng–luồng: left = {khoá: thời điểm}, right = [(khoá, thời điểm)]; cặp khớp khi 0 ≤ t_right − t_left ≤ window."""
    return [(k, t) for k, t in right if k in left and 0 <= t - left[k] <= window]


def consumer_lag(in_rate, out_rate, seconds):
    return max(0, (in_rate - out_rate) * seconds)


def drain_seconds(backlog, in_rate, out_rate):
    return backlog / (out_rate - in_rate) if out_rate > in_rate else math.inf


def e2e_latency(seq):
    """Độ trễ đầu–cuối: seq = danh sách các khâu nối tiếp; mỗi khâu là một số (ms) hoặc một danh sách nhánh song song (lấy nhánh lâu nhất)."""
    return sum(max(x) if isinstance(x, (list, tuple)) else x for x in seq)


REQUIRED = object()


def read_event(event, schema):
    """Người nhận đọc sự kiện theo lược đồ của mình: schema = {trường: giá trị mặc định, hoặc REQUIRED}. Trường lạ bị bỏ qua.
    Thiếu trường bắt buộc → None (đọc hỏng)."""
    out = {}
    for f, d in schema.items():
        if f in event:
            out[f] = event[f]
        elif d is REQUIRED:
            return None
        else:
            out[f] = d
    return out


def schema_compat(old, new):
    """(tương thích ngược, tương thích xuôi): ngược = người nhận dùng lược đồ MỚI đọc được sự kiện viết theo lược đồ CŨ;
    xuôi = người nhận dùng lược đồ CŨ đọc được sự kiện viết theo lược đồ MỚI. Sự kiện mẫu: mọi trường của lược đồ người ghi đều có mặt."""
    sample = lambda s: {f: (1 if d is REQUIRED else d) for f, d in s.items()}
    return read_event(sample(old), new) is not None, read_event(sample(new), old) is not None


# ── CAS (tình huống chuyên gia) ──
def cas_inversion_sim(tasks, inherit, horizon=10000):
    """Mô phỏng lập lịch ưu tiên cố định, chiếm quyền, bước 1 ms, MỘT khoá loại trừ (CAS L04, đảo ngược ưu tiên).
    tasks: danh sách dict {name, prio (lớn = ưu tiên cao), release (ms), steps: [('cpu', n) | ('lock', n)]} — ('lock', n) = cần
    giữ khoá trong n ms. inherit=True: tác vụ đang giữ khoá nhận ưu tiên cao nhất của các tác vụ đang chờ khoá đó.
    Trả về (finish: {tên: mốc xong}, wait: {tên: số ms bị chặn vì khoá}, timeline: [tên chạy ở mỗi ms hoặc None])."""
    tasks = [dict(t, steps=[s for s in t["steps"] if s[1] > 0]) for t in tasks]       # bỏ bước dài 0 ms
    st = {t["name"]: {"i": 0, "left": t["steps"][0][1] if t["steps"] else 0, "done": not t["steps"]} for t in tasks}
    by = {t["name"]: t for t in tasks}
    holder, finish, wait, timeline = None, {t["name"]: t["release"] for t in tasks if not t["steps"]}, {t["name"]: 0 for t in tasks}, []
    for now in range(horizon):
        live = [n for n, t in by.items() if t["release"] <= now and not st[n]["done"]]
        if not live:
            if all(s["done"] for s in st.values()):
                break
            timeline.append(None)
            continue
        wants = lambda n: by[n]["steps"][st[n]["i"]][0] == "lock" and holder != n
        blocked = [n for n in live if wants(n) and holder is not None]
        for n in blocked:
            wait[n] += 1
        eff = {n: by[n]["prio"] for n in live}
        if inherit and holder in eff and blocked:
            eff[holder] = max([eff[holder]] + [by[n]["prio"] for n in blocked])
        ready = [n for n in live if n not in blocked]
        if not ready:
            timeline.append(None)
            continue
        run = max(ready, key=lambda n: (eff[n], -by[n]["release"]))
        s = st[run]
        if by[run]["steps"][s["i"]][0] == "lock" and holder is None:
            holder = run
        s["left"] -= 1
        timeline.append(run)
        if s["left"] == 0:
            if by[run]["steps"][s["i"]][0] == "lock":
                holder = None
            s["i"] += 1
            if s["i"] == len(by[run]["steps"]):
                s["done"], finish[run] = True, now + 1
            else:
                s["left"] = by[run]["steps"][s["i"]][1]
    return finish, wait, timeline


CAS_FLU = [1.0, 1.2, 1.5, 2.0, 2.6, 3.3, 4.0, 4.6, 5.0, 5.2, 5.1, 4.7, 4.1, 3.4, 2.8, 2.2, 1.8, 1.5, 1.3, 1.1]  # 20 tuần, số minh hoạ


def cas_spurious_fit(n_cand, seed=0, target=CAS_FLU, n_train=10):
    """CAS L10 — tái hiện “khớp quá mức” (Lazer 2014: 50 triệu cụm từ cho 1152 điểm): n_cand chuỗi ngẫu nhiên (bước ngẫu nhiên, numpy
    default_rng(seed)), mỗi chuỗi khớp thẳng y ≈ a·x + b trên n_train tuần đầu; chọn chuỗi có sai số tuyệt đối trung bình (MAE) nhỏ nhất
    trên tuần huấn luyện. Trả (MAE huấn luyện, MAE trên các tuần sau) của chuỗi được chọn."""
    import numpy as np
    T = np.array(target, dtype=float)
    C = np.random.default_rng(seed).normal(size=(n_cand, len(T))).cumsum(axis=1)
    best = None
    for c in C:
        a, b = np.polyfit(c[:n_train], T[:n_train], 1)
        e = float(np.mean(np.abs(a * c[:n_train] + b - T[:n_train])))
        if best is None or e < best[0]:
            best = (e, float(np.mean(np.abs(a * c[n_train:] + b - T[n_train:]))))
    return best


def cas_lag_mae(lag, target=CAS_FLU, n_train=10):
    """MAE của mô hình “dùng số đo thật trễ `lag` tuần” trên các tuần sau n_train (CAS L10, như dữ liệu CDC trễ ≈ 2 tuần)."""
    return sum(abs(target[t] - target[t - lag]) for t in range(n_train, len(target))) / (len(target) - n_train)


# ───────── Học tăng cường (RLN): mỗi hàm tính lại một con số đưa lên màn hình; tiền tố rln_ ─────────
# Quy ước MDP nhỏ: mdp[s][a] = [(xác_suất, phần_thưởng, s_kế), …]; s_kế = None là kết thúc (giá trị 0).
# Chính sách tất định: dict s → a; chính sách ngẫu nhiên: dict s → {a: xác suất}.
def rln_return(rewards, gamma):
    """Lợi nhuận chiết khấu G = r1 + γ·r2 + γ²·r3 + … (cộng xuôi)."""
    return sum(gamma ** k * r for k, r in enumerate(rewards))


def rln_returns_backward(rewards, gamma):
    """Mọi G_t tính NGƯỢC từ cuối: G_t = r_{t+1} + γ·G_{t+1}; trả về [G_0, G_1, …]."""
    out, g = [], 0.0
    for r in reversed(rewards):
        g = r + gamma * g
        out.append(g)
    return out[::-1]


def _rln_pi(pi, s):
    a = pi[s]
    return a if isinstance(a, dict) else {a: 1.0}


def rln_backup(mdp, V, s, a, gamma):
    """Một vế Bellman: Σ p·(r + γ·V(s′)) của hành động a ở s."""
    return sum(p * (r + gamma * (0.0 if s2 is None else V[s2])) for p, r, s2 in mdp[s][a])


def rln_eval_sweeps(mdp, pi, gamma, k, V0=None):
    """Đánh giá chính sách bằng k lượt quét đồng bộ từ V0 (mặc định 0); trả về danh sách V sau 0, 1, …, k lượt."""
    V = dict(V0) if V0 else {s: 0.0 for s in mdp}
    hist = [dict(V)]
    for _ in range(k):
        V = {s: sum(w * rln_backup(mdp, V, s, a, gamma) for a, w in _rln_pi(pi, s).items()) for s in mdp}
        hist.append(dict(V))
    return hist


def rln_eval(mdp, pi, gamma, tol=1e-13, max_iter=100000):
    """Giá trị chính xác (tới tol) của chính sách pi bằng quét lặp tới điểm bất động."""
    V = {s: 0.0 for s in mdp}
    for _ in range(max_iter):
        V2 = {s: sum(w * rln_backup(mdp, V, s, a, gamma) for a, w in _rln_pi(pi, s).items()) for s in mdp}
        if max(abs(V2[s] - V[s]) for s in mdp) < tol:
            return V2
        V = V2
    return V


def rln_greedy(mdp, V, gamma):
    """Cải thiện chính sách: ở mỗi s chọn a có vế Bellman lớn nhất (hoà thì giữ a đứng trước trong mdp[s])."""
    return {s: max(mdp[s], key=lambda a: rln_backup(mdp, V, s, a, gamma)) for s in mdp}


def rln_policy_iteration(mdp, pi0, gamma):
    """Lặp chính sách: trả về [(chính sách, V của nó), …] tới khi chính sách không đổi."""
    out, pi = [], dict(pi0)
    while True:
        V = rln_eval(mdp, pi, gamma)
        out.append((dict(pi), V))
        pi2 = rln_greedy(mdp, V, gamma)
        if all(rln_backup(mdp, V, s, pi2[s], gamma) <= rln_backup(mdp, V, s, pi[s], gamma) + 1e-12 for s in mdp):
            return out
        pi = pi2


def rln_value_iteration(mdp, gamma, k):
    """Lặp giá trị k lượt từ V = 0; trả về danh sách V sau 0, 1, …, k lượt."""
    V = {s: 0.0 for s in mdp}
    hist = [dict(V)]
    for _ in range(k):
        V = {s: max(rln_backup(mdp, V, s, a, gamma) for a in mdp[s]) for s in mdp}
        hist.append(dict(V))
    return hist


def rln_eps_greedy(Q, eps):
    """Xác suất chọn từng tay theo ε-tham lam (tay tốt nhất: hoà thì tay đứng trước)."""
    k, best = len(Q), max(range(len(Q)), key=lambda i: Q[i])
    return [(1 - eps) * (i == best) + eps / k for i in range(k)]


def rln_ucb(Q, N, t, c):
    """Điểm UCB của từng tay: Q(a) + c·√(ln t / N(a)) (Sutton & Barto, công thức 2.10); N(a) = 0 → vô cực."""
    return [math.inf if n == 0 else q + c * math.sqrt(math.log(t) / n) for q, n in zip(Q, N)]


def rln_incr_means(xs):
    """Trung bình cộng dồn Q_n+1 = Q_n + (r_n − Q_n)/n; trả về [Q sau 1, 2, … phần thưởng]."""
    q, out = 0.0, []
    for n, x in enumerate(xs, 1):
        q += (x - q) / n
        out.append(q)
    return out


def rln_ppo_clip(rho, A, eps=0.2):
    """Mục tiêu cắt của PPO cho một mẫu: min(ρ·A, clip(ρ, 1 − ε, 1 + ε)·A)."""
    return min(rho * A, max(1 - eps, min(rho, 1 + eps)) * A)


def rln_sigmoid(x):
    return 1 / (1 + math.exp(-x))


def rln_ess(ws):
    """Số mẫu hiệu dụng (Σw)² / Σw² của các trọng số quan trọng."""
    return sum(ws) ** 2 / sum(w * w for w in ws)


def rln_boat(policy, T=1000, finish_at=100, finish_reward=100, every=5):
    """Đua thuyền minh hoạ (RLN L11): về đích sau finish_at bước được finish_reward rồi hết lượt; quay vòng thì cứ `every` bước ăn 1 mốc."""
    if policy == "ve_dich":
        return finish_reward
    return sum(1 for t in range(1, T + 1) if t % every == 0)


# ── RLN, phần nhánh A (bài 4–8): hàm thêm đặt NGAY TRÊN dòng mốc này ──
def rln_batch_mc(episodes):
    """Monte Carlo theo lô: V(s) = trung bình lợi nhuận (không chiết khấu) sau MỖI lần ghé s. episodes = [[(s, r), …], …]
    (r là phần thưởng nhận khi rời s). Ví dụ 6.4 của Sutton & Barto."""
    tot, cnt = {}, {}
    for ep in episodes:
        g = 0.0
        for s, r in reversed(ep):
            g += r
            tot[s] = tot.get(s, 0.0) + g
            cnt[s] = cnt.get(s, 0) + 1
    return {s: tot[s] / cnt[s] for s in tot}


def rln_batch_td(episodes, gamma=1.0, alpha=0.01, sweeps=20000):
    """TD(0) theo lô: quét lặp lại toàn bộ dữ liệu, cộng dồn số gia rồi mới cập nhật, tới khi hội tụ (Sutton & Barto mục 6.3)."""
    V = {s: 0.0 for ep in episodes for s, _ in ep}
    for _ in range(sweeps):
        inc = {s: 0.0 for s in V}
        for ep in episodes:
            for i, (s, r) in enumerate(ep):
                nxt = V[ep[i + 1][0]] if i + 1 < len(ep) else 0.0
                inc[s] += alpha * (r + gamma * nxt - V[s])
        for s in V:
            V[s] += inc[s]
    return V


def rln_walk_episode(rng, n=5):
    """Một lượt bước ngẫu nhiên n trạng thái (Ví dụ 6.2): bắt đầu ở giữa, trái/phải 50%; ra mép phải thưởng 1, mép trái 0.
    Trả về [(trạng thái 0..n−1, phần thưởng), …]."""
    s, ep = n // 2, []
    while True:
        s2 = s + (1 if rng.random() < 0.5 else -1)
        r = 1.0 if s2 == n else 0.0
        ep.append((s, r))
        if s2 < 0 or s2 == n:
            return ep
        s = s2


def rln_td_walk(alpha, episodes, seed=0, n=5, v0=0.5):
    """TD(0) trực tuyến trên bước ngẫu nhiên; trả về sai số căn trung bình bình phương so với giá trị thật (k+1)/(n+1)."""
    rng = random.Random(seed)
    V = [v0] * n
    for _ in range(episodes):
        ep = rln_walk_episode(rng, n)
        for i, (s, r) in enumerate(ep):
            nxt = V[ep[i + 1][0]] if i + 1 < len(ep) else 0.0
            V[s] += alpha * (r + nxt - V[s])
    return math.sqrt(sum((V[k] - (k + 1) / (n + 1)) ** 2 for k in range(n)) / n)


def rln_cliff(method, episodes=500, alpha=0.5, eps=0.1, seed=0):
    """Đi men vách đá (Ví dụ 6.6): lưới 4 × 12, xuất phát (3, 0), đích (3, 11), vách (3, 1..10): −1 mỗi bước, rơi vách −100 và về
    xuất phát. method 'q' (học Q, lấy max) hoặc 'sarsa' (dùng hành động thật sẽ làm). Trả về (tổng thưởng mỗi lượt,
    số bước của đường tham lam học được, có rơi vách khi đi tham lam không, số lần rơi vách mỗi lượt)."""
    rng = random.Random(seed)
    acts = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    Q = {(i, j): [0.0] * 4 for i in range(4) for j in range(12)}

    def step(s, a):
        i, j = min(3, max(0, s[0] + acts[a][0])), min(11, max(0, s[1] + acts[a][1]))
        if i == 3 and 1 <= j <= 10:
            return (3, 0), -100.0
        return (i, j), -1.0

    def pick(s):
        if rng.random() < eps:
            return rng.randrange(4)
        q = Q[s]
        return q.index(max(q))

    sums, falls = [], []
    for _ in range(episodes):
        s, a, tot, nf = (3, 0), None, 0.0, 0
        a = pick(s)
        while s != (3, 11):
            s2, r = step(s, a)
            tot += r
            nf += r == -100.0
            a2 = pick(s2)
            if s2 == (3, 11):
                target = r
            elif method == "q":
                target = r + max(Q[s2])
            else:
                target = r + Q[s2][a2]
            Q[s][a] += alpha * (target - Q[s][a])
            s, a = s2, a2
        sums.append(tot)
        falls.append(nf)
    s, n, fell = (3, 0), 0, False
    while s != (3, 11) and n < 100:
        s2, r = step(s, Q[s].index(max(Q[s])))
        fell = fell or r == -100.0
        s, n = s2, n + 1
    return sums, n, fell, falls


def rln_max_bias(n_actions=3, noise=1.0):
    """Kỳ vọng của max các ước lượng khi mọi giá trị thật bằng 0 và mỗi ước lượng lệch ±noise đồng khả năng (liệt kê 2^n ca)."""
    combos = list(itertools.product((-noise, noise), repeat=n_actions))
    return sum(max(c) for c in combos) / len(combos)


def rln_adjacent_pairs(N, B):
    """Số cặp (trong lô B mẫu lấy đều, độc lập từ N bước) kỳ vọng là hai bước liền nhau: C(B, 2) · 2(N − 1) / N²."""
    return B * (B - 1) / 2 * 2 * (N - 1) / N ** 2


def rln_pg2(G1, G2, theta=0.0, b1=0.0, b2=0.0):
    """Chính sách 2 hành động π(a1) = σ(θ), π(a2) = 1 − σ(θ). Trả về (xác suất, mẫu ước lượng gradient (G − b)·d ln π / dθ
    của từng hành động, kỳ vọng, phương sai). d ln σ/dθ = 1 − σ; d ln(1 − σ)/dθ = −σ."""
    p = 1 / (1 + math.exp(-theta))
    probs = [p, 1 - p]
    xs = [(G1 - b1) * (1 - p), (G2 - b2) * (-p)]
    mean = sum(q * x for q, x in zip(probs, xs))
    var = sum(q * x * x for q, x in zip(probs, xs)) - mean ** 2
    return probs, xs, mean, var


def rln_pg2_true(G1, G2, theta=0.0):
    """Gradient thật của J(θ) = σ(θ)·G1 + (1 − σ(θ))·G2: σ(1 − σ)(G1 − G2)."""
    p = 1 / (1 + math.exp(-theta))
    return p * (1 - p) * (G1 - G2)


# ── mốc RLN-A ──

# ── RLN, phần nhánh B (bài 9–13): hàm thêm đặt NGAY TRÊN dòng mốc này ──
def rln_pref_steps(k, eta=1.0, rA=0.0, rB=0.0):
    """RLN L10: người chọn A hơn B; học thẳng hai điểm rA, rB bằng k bước giảm mất mát −ln σ(rA − rB), tốc độ eta.
    Đạo hàm theo rA là −(1 − σ(d)), theo rB là +(1 − σ(d)). Trả về [(d, σ(d), mất mát, 1 − σ(d))] trước mỗi bước và sau bước cuối."""
    out = []
    for _ in range(k + 1):
        d = rA - rB
        p = rln_sigmoid(d)
        out.append((d, p, -math.log(p), 1 - p))
        rA, rB = rA + eta * (1 - p), rB - eta * (1 - p)
    return out


def rln_race(policy, gamma=1.0, T=1000, finish_at=100, finish_reward=100, every=5, repeat_value=1.0):
    """RLN L11: mô phỏng TỪNG BƯỚC đua thuyền minh hoạ. "ve_dich": nhận finish_reward ở bước finish_at rồi hết lượt.
    "vong": quay vòng tới hết T bước, cứ `every` bước chạm lại một mốc; lần chạm đầu được 1, các lần sau được repeat_value.
    Phần thưởng ở bước t được nhân γ^(t−1). Trả về lợi nhuận chiết khấu."""
    g, hits = 0.0, 0
    for t in range(1, T + 1):
        r = 0.0
        if policy == "ve_dich":
            if t == finish_at:
                g += gamma ** (t - 1) * finish_reward
                break
        elif t % every == 0:
            r = 1.0 if hits == 0 else repeat_value
            hits += 1
        g += gamma ** (t - 1) * r
    return g


def rln_is_estimates(samples):
    """RLN L12: samples = [(trọng số w = π_mới/π_cũ, lợi nhuận G), …] từ nhật ký của chính sách cũ.
    Trả về (ước lượng thường Σw·G / n, ước lượng có trọng số Σw·G / Σw, số mẫu hiệu dụng (Σw)² / Σw²)."""
    sw = sum(w for w, _ in samples)
    swg = sum(w * g for w, g in samples)
    return swg / len(samples), (swg / sw if sw else 0.0), (rln_ess([w for w, _ in samples]) if sw else 0.0)


def rln_kl_reward(r, beta, p_new, p_ref):
    """RLN L10: phần thưởng đưa vào học tăng cường = r − β·ln(π_mới / π_gốc) cho một câu trả lời."""
    return r - beta * math.log(p_new / p_ref)


# ── mốc RLN-B ──


# ───────── Tính toán song song và GPU (PAR): mô phỏng từng bước — mỗi hàm trả về con số đưa lên màn hình ─────────
# Quy ước khoá: n = số lõi / số máy / số GPU; p = tỉ lệ thời gian song song được (như CSA bài 13); s = 1 − p.

def par_amdahl(p, n):
    """Amdahl: tăng tốc với n lõi khi tỉ lệ p của thời gian MỘT lõi song song được. Tính bằng mô phỏng thời gian: phần tuần tự
    chạy trên một lõi, phần song song chia đều cho n lõi."""
    t1 = 1.0
    tn = (1 - p) * t1 + max([p * t1 / n] * n)
    return t1 / tn


def par_gustafson(s, n):
    """Gustafson: s = tỉ lệ tuần tự đo trên máy n lõi (thời gian chạy song song lấy bằng 1). Máy một lõi cần s + (1 − s)·n."""
    return (s + (1 - s) * n) / (s + (1 - s))


def par_tree_sum(n):
    """Cộng n số theo cây cặp đôi, làm thật: trả về (số phép cộng = công việc T1, số tầng = đường găng T∞, tổng)."""
    vals, work, depth = list(range(1, n + 1)), 0, 0
    while len(vals) > 1:
        nxt = [vals[i] + vals[i + 1] for i in range(0, len(vals) - 1, 2)]
        work += len(nxt)
        if len(vals) % 2:
            nxt.append(vals[-1])
        vals, depth = nxt, depth + 1
    return work, depth, vals[0]


def par_greedy_tree_steps(n, procs):
    """Lịch tham lam cho cây cộng n số trên `procs` lõi: mỗi bước, mỗi lõi làm một phép cộng đã sẵn sàng (hai đầu vào đã có).
    Trả về số bước."""
    steps, level = 0, n          # level = số giá trị đang chờ được cộng
    while level > 1:
        adds = level // 2
        carry = level % 2
        while adds > 0:
            adds -= min(procs, adds)
            steps += 1
        level = level // 2 + carry
    return steps


def par_list_schedule(jobs, cores, order=None):
    """Phân việc động: lấy việc theo thứ tự `order` (mặc định như danh sách), mỗi việc vào lõi đang rảnh sớm nhất.
    Trả về danh sách tổng thời gian mỗi lõi."""
    load = [0] * cores
    for j in (jobs if order is None else order):
        load[load.index(min(load))] += j
    return load


def par_lpt(jobs, cores):
    """Việc dài làm trước: sắp giảm dần rồi phân việc động."""
    return par_list_schedule(jobs, cores, sorted(jobs, reverse=True))


def par_static_blocks(jobs, cores):
    """Chia tĩnh theo khối liền nhau, mỗi lõi cùng số việc. Trả về tổng thời gian mỗi lõi."""
    k = -(-len(jobs) // cores)
    return [sum(jobs[i * k:(i + 1) * k]) for i in range(cores)]


def par_cache_lines(addrs, line=64):
    """Tập các dòng bộ nhớ đệm (chỉ số dòng) mà các địa chỉ byte rơi vào."""
    return sorted({a // line for a in addrs})


def par_vector_split(n, width):
    """Vòng lặp n phần tử, mỗi lệnh vector xử lý `width` phần tử: đếm bằng cách đi từng lượt. Trả về (số lệnh vector, số lượt lẻ)."""
    i, vec = 0, 0
    while i + width <= n:
        i, vec = i + width, vec + 1
    return vec, n - i


def par_roofline(peak, bw, intensity):
    """Hiệu năng đạt được tối đa = min(đỉnh tính toán, băng thông × cường độ số học)."""
    return min(peak, bw * intensity)


def par_warp_passes(branch):
    """Một nhóm luồng chạy chung lệnh: mỗi nhánh khác nhau chạy một lượt riêng (các luồng nhánh khác tạm nghỉ).
    Trả về (số lượt, hiệu suất = số luồng làm việc có ích / (số lượt × số luồng))."""
    passes = [b for b in dict.fromkeys(branch)]
    useful = sum(sum(1 for x in branch if x == b) for b in passes)
    return len(passes), Fraction(useful, len(passes) * len(branch))


def par_transactions(stride, threads=32, word=4, seg=128):
    """Số đoạn bộ nhớ `seg` byte mà một nhóm `threads` luồng chạm tới khi luồng t đọc phần tử t·stride (mỗi phần tử `word` byte)."""
    return len({(t * stride * word) // seg for t in range(threads)})


def par_matmul_reads(n, b=None):
    """Đếm số phần tử đọc từ bộ nhớ chậm khi nhân hai ma trận n × n. b = None: ngây thơ, mỗi phép nhân–cộng đọc một phần tử A và
    một phần tử B. b: chia khối b × b, mỗi bộ ba khối (i, j, k) nạp một khối A và một khối B vào bộ nhớ nhanh (đếm theo vòng lặp)."""
    if b is None:
        return sum(2 * n for _ in range(n) for _ in range(n))
    nb, reads = n // b, 0
    for _ in range(nb):
        for _ in range(nb):
            for _ in range(nb):
                reads += 2 * b * b
    return reads


def par_ring_allreduce(vectors):
    """All-reduce vòng, làm thật: `vectors[i]` là vector của máy i, chia thành n mảnh bằng nhau. Pha 1 (rút gọn phân tán) n − 1 bước,
    pha 2 (gom lại) n − 1 bước; mỗi bước mỗi máy gửi một mảnh cho máy bên phải. Trả về (kết quả mỗi máy, số phần tử mỗi máy đã gửi,
    số bước)."""
    n = len(vectors)
    L = len(vectors[0])
    assert L % n == 0
    c = L // n
    chunks = [[list(v[k * c:(k + 1) * c]) for k in range(n)] for v in vectors]
    sent, steps = [0] * n, 0
    for s in range(n - 1):  # rút gọn phân tán
        msgs = [((i - s) % n, list(chunks[i][(i - s) % n])) for i in range(n)]
        for i, (k, data) in enumerate(msgs):
            j = (i + 1) % n
            chunks[j][k] = [a + b for a, b in zip(chunks[j][k], data)]
            sent[i] += c
        steps += 1
    for s in range(n - 1):  # gom lại: máy i giữ mảnh đầy đủ (i + 1) % n
        msgs = [((i + 1 - s) % n, list(chunks[i][(i + 1 - s) % n])) for i in range(n)]
        for i, (k, data) in enumerate(msgs):
            chunks[(i + 1) % n][k] = data
            sent[i] += c
        steps += 1
    return [sum(ch, []) for ch in chunks], sent, steps


def par_ps_bytes(n, size):
    """Máy chủ tham số: mỗi máy gửi `size` lên, nhận `size` về; máy chủ nhận tổng n·size qua đường của nó."""
    return {"server_in": n * size, "server_out": n * size, "worker_send": size}


def par_step_efficiency(compute, comm, overlap=0):
    """Hiệu suất mở rộng của một bước huấn luyện: thời gian tính / (thời gian tính + phần truyền thông KHÔNG chồng được)."""
    exposed = max(comm - overlap, 0)
    return compute / (compute + exposed)


# ── PAR, phần nhánh A (bài 2–6): hàm thêm đặt NGAY TRÊN dòng mốc này ──
def par_race_counts(times=2):
    """Hai luồng, mỗi luồng tăng x `times` lần bằng đọc–cộng–ghi (không khoá): duyệt MỌI cách xen kẽ, trả về {x cuối: số cách}."""
    ops = lambda t: [(t, k) for k in ("load", "add", "store") * times]
    out = {}
    for seq in _interleavings(ops("A"), ops("B")):
        x, reg = 0, {"A": 0, "B": 0}
        for t, k in seq:
            if k == "load": reg[t] = x
            elif k == "add": reg[t] += 1
            else: x = reg[t]
        out[x] = out.get(x, 0) + 1
    return out


def par_atomic_counts(times=2):
    """Như par_race_counts nhưng mỗi lần tăng là MỘT bước nguyên tử (không chen vào giữa được): trả về {x cuối: số cách}."""
    out = {}
    for seq in _interleavings([("A", "inc")] * times, [("B", "inc")] * times):
        x = 0
        for _ in seq:
            x += 1
        out[x] = out.get(x, 0) + 1
    return out


def par_reduce_seq(values):
    """Cộng dồn từng số theo thứ tự (một luồng), số thực máy."""
    acc = 0.0
    for v in values:
        acc = acc + v
    return acc


def par_reduce_tree(values):
    """Rút gọn theo cây cặp đôi (như nhiều luồng gộp tổng riêng), số thực máy."""
    vals = list(values)
    while len(vals) > 1:
        nxt = [vals[i] + vals[i + 1] for i in range(0, len(vals) - 1, 2)]
        if len(vals) % 2:
            nxt.append(vals[-1])
        vals = nxt
    return vals[0]


def par_shared_steps(threads, k, mode):
    """Số bước (mỗi phép tăng 1 bước) để `threads` luồng, mỗi luồng tăng k lần, ra tổng đúng:
    'atomic' = mọi lần tăng xếp hàng ở một biến chung (nối tiếp); 'reduce' = mỗi luồng k bước trên biến riêng, rồi gộp theo cây."""
    if mode == "atomic":
        return threads * k
    levels, m = 0, threads
    while m > 1:
        m, levels = (m + 1) // 2, levels + 1
    return k + levels


def par_static_cyclic(jobs, cores):
    """Chia tĩnh xen kẽ (vòng): việc i vào lõi i mod cores. Trả về tổng thời gian mỗi lõi."""
    load = [0] * cores
    for i, j in enumerate(jobs):
        load[i % cores] += j
    return load


def par_best_makespan(jobs, cores):
    """Thời gian hoàn thành NHỎ NHẤT có thể: thử MỌI cách gán việc vào lõi (chỉ dùng cho ví dụ nhỏ)."""
    best = None
    for assign in itertools.product(range(cores), repeat=len(jobs)):
        load = [0] * cores
        for j, c in zip(jobs, assign):
            load[c] += j
        m = max(load)
        best = m if best is None else min(best, m)
    return best


def par_dynamic_trace(jobs, cores, order=None):
    """Phân việc động, ghi vết: [(việc, lõi nhận, lúc bắt đầu)] theo thứ tự lấy việc; lõi rảnh sớm nhất (chỉ số nhỏ khi hoà) nhận việc."""
    load, trace = [0] * cores, []
    for j in (jobs if order is None else order):
        c = load.index(min(load))
        trace.append((j, c, load[c]))
        load[c] += j
    return trace


def par_line_transfers(addrs, rounds, line=64):
    """Mô hình huỷ bản sao khi ghi: luồng i chỉ ghi biến của nó ở địa chỉ addrs[i]; các luồng ghi xoay vòng (0, 1, …, n − 1) `rounds`
    vòng. Một lần ghi phải kéo dòng về (và huỷ bản sao ở lõi khác) khi lõi đó CHƯA giữ dòng ở trạng thái được ghi, tức người ghi
    trước đó trên dòng này là lõi khác hoặc chưa ai. Trả về (số lần kéo dòng, số lần ghi)."""
    owner, pulls, writes = {}, 0, 0
    for _ in range(rounds):
        for i, a in enumerate(addrs):
            ln = a // line
            if owner.get(ln) != i:
                pulls += 1
                owner[ln] = i
            writes += 1
    return pulls, writes


def par_vector_add(a, b, width):
    """Mô phỏng vòng c[i] = a[i] + b[i] đã vector hoá: mỗi lệnh vector cộng `width` cặp liền nhau, phần dư cộng từng phần tử.
    Trả về (c, số lệnh vector, số lượt vô hướng)."""
    n, c, i, vec, sca = len(a), [None] * len(a), 0, 0, 0
    while i + width <= n:
        c[i:i + width] = [x + y for x, y in zip(a[i:i + width], b[i:i + width])]
        i, vec = i + width, vec + 1
    while i < n:
        c[i] = a[i] + b[i]
        i, sca = i + 1, sca + 1
    return c, vec, sca


def par_recurrence(b, a0=0, width=None):
    """a[i] = a[i − 1] + b[i]. width=None: chạy đúng từng lượt. width=w: vector hoá NGÂY THƠ — mỗi khúc w lượt đọc a[i − 1] cũ
    (giá trị TRƯỚC khi khúc bắt đầu), như khi 8 làn cùng chạy một lúc. Trả về danh sách a[0..n]."""
    a = [a0] + [0] * len(b)
    if width is None:
        for i in range(1, len(b) + 1):
            a[i] = a[i - 1] + b[i - 1]
        return a
    for s in range(1, len(b) + 1, width):
        old = list(a)
        for i in range(s, min(s + width, len(b) + 1)):
            a[i] = old[i - 1] + b[i - 1]
    return a


def par_lane_sum(values, width):
    """Tổng đã vector hoá: `width` tổng riêng theo làn (làn k cộng phần tử k, k + w, …), cuối cùng gộp các làn từ trái sang phải."""
    lanes = [0.0] * width
    for i, v in enumerate(values):
        lanes[i % width] = lanes[i % width] + v
    acc = 0.0
    for x in lanes:
        acc = acc + x
    return acc


# ── mốc PAR-A ──

# ── PAR, phần nhánh B (bài 7–12): hàm thêm đặt NGAY TRÊN dòng mốc này ──
def par_ring_trace(vectors):
    """PAR L10 — vết của gộp toàn phần theo vòng (cùng thứ tự gửi như par_ring_allreduce): danh sách trạng thái các máy SAU mỗi bước,
    mỗi máy là danh sách các mảnh (mảnh = danh sách số). Bước 1 … n − 1: rút gọn phân tán; bước n … 2(n − 1): gom lại."""
    n = len(vectors)
    c = len(vectors[0]) // n
    ch = [[list(v[k * c:(k + 1) * c]) for k in range(n)] for v in vectors]
    states = []
    for s in range(n - 1):
        msgs = [((i - s) % n, list(ch[i][(i - s) % n])) for i in range(n)]
        for i, (k, d) in enumerate(msgs):
            j = (i + 1) % n
            ch[j][k] = [a + b for a, b in zip(ch[j][k], d)]
        states.append([[list(m) for m in mach] for mach in ch])
    for s in range(n - 1):
        msgs = [((i + 1 - s) % n, list(ch[i][(i + 1 - s) % n])) for i in range(n)]
        for i, (k, d) in enumerate(msgs):
            ch[(i + 1) % n][k] = d
        states.append([[list(m) for m in mach] for mach in ch])
    return states


def par_ring_time(n, size, bw, lat=0.0):
    """Thời gian gộp toàn phần theo vòng: 2(n − 1) bước nối tiếp, mỗi bước gửi một mảnh size/n qua mọi đường cùng lúc (băng thông bw
    mỗi đường) cộng độ trễ lat của bước đó."""
    return sum(lat + (size / n) / bw for _ in range(2 * (n - 1)))


def par_ps_time(n, size, bw, servers=1, lat=0.0):
    """Máy chủ tham số: `servers` máy chủ chia đều tham số; mỗi máy chủ nhận n · size/servers rồi gửi lại cùng lượng qua đường bw
    (nhận và gửi nối tiếp), mỗi pha một độ trễ lat."""
    per = n * size / servers
    return lat + per / bw + lat + per / bw


# ── mốc PAR-B ──


# ───────── Thị giác máy tính (CVI): mỗi hàm tính lại con số đưa lên màn hình — vòng lặp thuần, không gõ sẵn kết quả ─────────
# Quy ước: ảnh là danh sách hàng (list of list), chỉ số [hàng][cột]; hộp là (x1, y1, x2, y2) toạ độ liên tục (không cộng 1).
def cvi_frame_bytes(w, h, c=3, bits=8):
    """Dung lượng một khung chưa nén (byte): rộng · cao · số kênh · số bit mỗi kênh / 8."""
    return w * h * c * bits // 8


def cvi_xcorr2d(img, ker):
    """Tương quan chéo 'valid' (không lật bộ lọc) — cái mà thư viện học sâu gọi là tích chập."""
    H, W, k = len(img), len(img[0]), len(ker)
    return [[sum(img[i + a][j + b] * ker[a][b] for a in range(k) for b in range(k))
             for j in range(W - k + 1)] for i in range(H - k + 1)]


def cvi_conv2d(img, ker):
    """Tích chập đúng nghĩa toán học: lật bộ lọc 180 độ rồi tương quan chéo."""
    flipped = [row[::-1] for row in ker[::-1]]
    return cvi_xcorr2d(img, flipped)


def cvi_filter1d(xs, ker):
    """Tương quan chéo một chiều 'valid'."""
    k = len(ker)
    return [sum(xs[i + j] * ker[j] for j in range(k)) for i in range(len(xs) - k + 1)]


def cvi_otsu(pixels):
    """Vét mọi ngưỡng t (lớp 0: giá trị ≤ t). Trả về (t tốt nhất, [(t, w0, w1, mu0, mu1, phương sai giữa lớp)])."""
    vals = sorted(set(pixels))
    n, rows = len(pixels), []
    for t in vals[:-1]:
        a = [p for p in pixels if p <= t]
        b = [p for p in pixels if p > t]
        w0, w1 = len(a) / n, len(b) / n
        m0, m1 = sum(a) / len(a), sum(b) / len(b)
        rows.append((t, w0, w1, m0, m1, w0 * w1 * (m0 - m1) ** 2))
    best = max(rows, key=lambda r: r[5])
    return best[0], rows


def cvi_hist(pixels, levels):
    """Biểu đồ tần suất: số điểm ảnh ở mỗi mức 0 … levels − 1."""
    return [sum(1 for p in pixels if p == v) for v in range(levels)]


def cvi_equalize(pixels, levels):
    """Cân bằng biểu đồ: mức v → round((levels − 1) · tỉ lệ tích luỹ tới v). Trả về bảng ánh xạ."""
    h, n, acc, out = cvi_hist(pixels, levels), len(pixels), 0, []
    for v in range(levels):
        acc += h[v]
        out.append(round((levels - 1) * acc / n))
    return out


def cvi_project(K, X, Y, Z):
    """Chiếu điểm (X, Y, Z) (hệ camera) bằng ma trận nội K 3 × 3: [u·w, v·w, w] = K · [X, Y, Z]."""
    p = [sum(K[r][c] * v for c, v in enumerate((X, Y, Z))) for r in range(3)]
    return p[0] / p[2], p[1] / p[2]


def cvi_distort(x, y, k1, k2=0.0):
    """Méo hướng tâm trên toạ độ chuẩn hoá: x_méo = x · (1 + k1 r² + k2 r⁴), r² = x² + y²."""
    r2 = x * x + y * y
    s = 1 + k1 * r2 + k2 * r2 * r2
    return x * s, y * s


def cvi_rmse(obs, pred):
    """Sai số chiếu lại trung bình bình phương (căn), điểm ảnh."""
    return math.sqrt(sum((a - c) ** 2 + (b - d) ** 2 for (a, b), (c, d) in zip(obs, pred)) / len(obs))


def cvi_ssd_shift(img, r, c, dr, dc, half=1):
    """Tổng bình phương chênh lệch giữa cửa sổ (2·half + 1)² tâm (r, c) và cửa sổ dời (dr, dc)."""
    return sum((img[r + i + dr][c + j + dc] - img[r + i][c + j]) ** 2
               for i in range(-half, half + 1) for j in range(-half, half + 1))


def cvi_l2(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def cvi_match(descA, descB, thr=0.8):
    """Với mỗi mô tả của ảnh A: gần nhất, gần nhì trong B, tỉ số, giữ (tỉ số < thr). Trả về [(i, j, d1, d2, tỉ số, giữ)]."""
    out = []
    for i, a in enumerate(descA):
        ds = sorted((cvi_l2(a, b), j) for j, b in enumerate(descB))
        (d1, j), (d2, _) = ds[0], ds[1]
        out.append((i, j, d1, d2, d1 / d2, d1 / d2 < thr))
    return out


def cvi_ransac_iters(w, s, p=0.99):
    """Số lần thử N nhỏ nhất để xác suất gặp ít nhất một bộ s điểm toàn đúng ≥ p: (1 − wˢ)^N ≤ 1 − p."""
    N = 0
    while (1 - w ** s) ** N > 1 - p:
        N += 1
    return N


def cvi_lsq_line(pts):
    """Bình phương tối thiểu y = a·x + b."""
    n = len(pts)
    sx = sum(x for x, _ in pts); sy = sum(y for _, y in pts)
    sxx = sum(x * x for x, _ in pts); sxy = sum(x * y for x, y in pts)
    a = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    return a, (sy - a * sx) / n


def cvi_ransac_line(pts, thr):
    """RANSAC vét hết mọi cặp điểm (tất định): đường qua cặp nào có nhiều điểm trong (|y − ax − b| ≤ thr) nhất."""
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            (x1, y1), (x2, y2) = pts[i], pts[j]
            if x1 == x2:
                continue
            a = (y2 - y1) / (x2 - x1); b = y1 - a * x1
            inl = [k for k, (x, y) in enumerate(pts) if abs(y - a * x - b) <= thr]
            if best is None or len(inl) > len(best[2]):
                best = (a, b, inl)
    return best


def cvi_sad_costs(left, right, x, half, dmax):
    """Chi phí SAD khi so cửa sổ quanh cột x của hàng trái với cột x − d của hàng phải, d = 0 … dmax."""
    return [sum(abs(left[x + j] - right[x - d + j]) for j in range(-half, half + 1)) for d in range(dmax + 1)]


def cvi_receptive_field(layers):
    """Trường tiếp nhận sau một chồng lớp [(k, s)]: r ← r + (k − 1) · tích các bước nhảy trước đó."""
    r, jump = 1, 1
    for k, s in layers:
        r += (k - 1) * jump
        jump *= s
    return r


def cvi_out_size(n, k, p=0, s=1):
    """Cạnh đầu ra của tích chập: ⌊(n + 2p − k) / s⌋ + 1."""
    return (n + 2 * p - k) // s + 1


# bảy đoạn: a trên, b phải trên, c phải dưới, d dưới, e trái dưới, f trái trên, g giữa
CVI_SEG7 = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg"}


def cvi_seg7_transform(digit, how):
    """Xoay 180 độ ('rot180') hoặc lật ngang ('flip') chữ số bảy đoạn; trả về chữ số mới hoặc None nếu không còn là chữ số."""
    m = {"rot180": dict(a="d", b="e", c="f", d="a", e="b", f="c", g="g"),
         "flip": dict(a="a", b="f", c="e", d="d", e="c", f="b", g="g")}[how]
    segs = set(m[s] for s in CVI_SEG7[digit])
    return next((k for k, v in CVI_SEG7.items() if set(v) == segs), None)


def cvi_box_iou(A, B):
    """Giao trên hợp của hai hộp (x1, y1, x2, y2). Trả về (giao, hợp, IoU)."""
    iw = max(0, min(A[2], B[2]) - max(A[0], B[0]))
    ih = max(0, min(A[3], B[3]) - max(A[1], B[1]))
    inter = iw * ih
    union = (A[2] - A[0]) * (A[3] - A[1]) + (B[2] - B[0]) * (B[3] - B[1]) - inter
    return inter, union, inter / union


def cvi_nms(boxes, scores, thr=0.5):
    """Loại bỏ không cực đại tham lam: giữ hộp điểm cao nhất, bỏ mọi hộp có IoU > thr với nó, lặp lại. Trả về chỉ số giữ."""
    order = sorted(range(len(boxes)), key=lambda i: -scores[i])
    keep = []
    while order:
        i = order.pop(0)
        keep.append(i)
        order = [j for j in order if cvi_box_iou(boxes[i], boxes[j])[2] <= thr]
    return keep


def cvi_pr_curve(is_tp, n_gt):
    """is_tp: danh sách đúng/sai đã xếp theo điểm giảm dần. Trả về [(độ chuẩn xác, độ phủ)] sau mỗi phát hiện."""
    tp = fp = 0
    out = []
    for t in is_tp:
        tp += bool(t); fp += (not t)
        out.append((tp / (tp + fp), tp / n_gt))
    return out


def cvi_ap(is_tp, n_gt, mode="all"):
    """Độ chính xác trung bình: 'all' = diện tích dưới đường độ chuẩn xác nội suy (lấy max bên phải) theo độ phủ;
    '11' = trung bình độ chuẩn xác nội suy tại độ phủ 0; 0,1; …; 1 (PASCAL VOC 2007)."""
    pr = cvi_pr_curve(is_tp, n_gt)
    if mode == "11":
        return sum(max([p for p, r in pr if r >= t / 10] or [0]) for t in range(11)) / 11
    ap, prev_r = 0.0, 0.0
    for k, (p, r) in enumerate(pr):
        if r > prev_r:
            ap += (r - prev_r) * max(q for q, _ in pr[k:])
            prev_r = r
    return ap


def cvi_iou_dice(tp, fp, fn):
    """IoU = TP / (TP + FP + FN), Dice = 2TP / (2TP + FP + FN)."""
    return tp / (tp + fp + fn), 2 * tp / (2 * tp + fp + fn)


def cvi_mask_counts(pred, gt):
    """Đếm (TP, FP, FN, TN) trên hai mặt nạ 0/1 cùng kích thước."""
    tp = fp = fn = tn = 0
    for pr, gr in zip(pred, gt):
        for p, g in zip(pr, gr):
            tp += p and g; fp += p and not g; fn += (not p) and g; tn += (not p) and (not g)
    return tp, fp, fn, tn


def cvi_mix_acc(slices):
    """Độ chính xác chung từ các lát [(số ảnh hoặc tỉ trọng, độ chính xác)]."""
    return sum(n * a for n, a in slices) / sum(n for n, _ in slices)


def cvi_shortcut_sim(n, p_grass_cow=0.95, p_nograss_nocow=0.95, seed=0):
    """Mô phỏng tập ảnh: nửa có bò. Bò có cỏ với xác suất p, ảnh không bò không cỏ với xác suất p.
    Trả về (độ chính xác của luật 'có cỏ ⇒ bò' trên tập cùng phân bố, độ chính xác trên bò ở bãi biển (không cỏ))."""
    import random
    rng = random.Random(seed)
    ok = 0
    for _ in range(n):
        cow = rng.random() < 0.5
        grass = (rng.random() < p_grass_cow) if cow else (rng.random() >= p_nograss_nocow)
        ok += (grass == cow)
    rule = lambda has_grass: has_grass  # luật lối tắt: đoán "bò" khi và chỉ khi có cỏ
    beach = sum(rule(False) == True for _ in range(100))  # 100 ảnh bò thật trên bãi biển (không cỏ)
    return ok / n, beach / 100


# ── CVI, nhánh A (bài 4–7): hàm thêm đặt NGAY TRÊN dòng mốc này ──
# ── mốc CVI-A ──

# ── CVI, nhánh B (bài 8–11): hàm thêm đặt NGAY TRÊN dòng mốc này ──
def cvi_match_dets(dets, gts, thr=0.5):
    """Ghép tham lam (Russakovsky và cộng sự 2015, thuật toán 2): duyệt phát hiện theo điểm giảm dần, mỗi phát hiện lấy hộp thật
    CHƯA ghép có IoU ≥ thr lớn nhất → đúng; không có → sai. dets = [(điểm, hộp)], gts = [hộp]. Trả về [đúng/sai] theo thứ tự điểm."""
    free, out = set(range(len(gts))), []
    for s, b in sorted(dets, key=lambda d: -d[0]):
        cand = [(cvi_box_iou(b, gts[k])[2], k) for k in free if cvi_box_iou(b, gts[k])[2] >= thr]
        if cand:
            free.discard(max(cand)[1])
            out.append(True)
        else:
            out.append(False)
    return out


def cvi_ap101(is_tp, n_gt):
    """AP kiểu COCO: độ chuẩn xác nội suy (lấy max bên phải) đọc tại 101 mức độ phủ 0; 0,01; …; 1 rồi lấy trung bình."""
    pr = cvi_pr_curve(is_tp, n_gt)
    env = [max(p for p, _ in pr[k:]) for k in range(len(pr))]
    tot = 0.0
    for i in range(101):
        r = i / 100
        k = next((k for k, (_, rc) in enumerate(pr) if rc >= r - 1e-12), None)
        tot += env[k] if k is not None else 0.0
    return tot / 101


def cvi_xywh_to_xyxy(b):
    """Hộp (x, y, rộng, cao) — cách ghi của COCO — đổi sang (x1, y1, x2, y2)."""
    return (b[0], b[1], b[0] + b[2], b[1] + b[3])


# ── mốc CVI-B ──


# ══════════ IRS · Truy hồi thông tin và hệ gợi ý (tiền tố irs_) ══════════
# Vị trí đánh số từ 1. `rels` là danh sách 0/1 (hoặc mức liên quan) theo thứ tự hệ trả về.

def irs_prec_at_k(rels, k):
    """Độ chuẩn xác ở k kết quả đầu: số kết quả đúng trong k đầu chia k (rels: 0/1 theo thứ tự)."""
    return sum(1 for r in rels[:k] if r) / k


def irs_recall_at_k(rels, k, total_relevant):
    """Độ phủ ở k kết quả đầu: số kết quả đúng trong k đầu chia TỔNG số tài liệu đúng của câu hỏi (kể cả tài liệu hệ không trả)."""
    return sum(1 for r in rels[:k] if r) / total_relevant


def irs_rr(rels):
    """Hạng nghịch đảo: 1 chia vị trí của kết quả đúng đầu tiên; không có kết quả đúng → 0."""
    for i, r in enumerate(rels, 1):
        if r:
            return 1 / i
    return 0.0


def irs_mrr(lists):
    """Hạng nghịch đảo trung bình trên nhiều câu hỏi."""
    return sum(irs_rr(r) for r in lists) / len(lists)


def irs_dcg(gains, k=None, exp_gain=False):
    """DCG dạng phổ biến: tổng độ lợi chia log₂(vị trí + 1). exp_gain=True dùng độ lợi 2^rel − 1 (Burges và cộng sự 2005)."""
    g = gains[:k] if k else gains
    return sum(((2 ** x - 1) if exp_gain else x) / math.log2(i + 1) for i, x in enumerate(g, 1))


def irs_ndcg(gains, k=None, exp_gain=False, judged=None):
    """nDCG = DCG chia DCG của thứ tự lý tưởng. Thứ tự lý tưởng sắp giảm dần MỌI tài liệu đã chấm (`judged`, mặc định = gains)."""
    pool = sorted(judged if judged is not None else gains, reverse=True)
    ideal = irs_dcg(pool, k or len(gains), exp_gain)
    return irs_dcg(gains, k, exp_gain) / ideal if ideal else 0.0


def irs_dcg_jk(gains, b=2):
    """DCG dạng gốc Järvelin–Kekäläinen (TOIS 2002): vị trí i < b cộng nguyên độ lợi, từ i ≥ b cộng độ lợi chia log_b(i)."""
    return sum(x if i < b else x / math.log(i, b) for i, x in enumerate(gains, 1))


def irs_idf(n_docs, df):
    """Độ hiếm (dạng sách Manning–Raghavan–Schütze 2008): ln(N chia số tài liệu chứa từ)."""
    return math.log(n_docs / df)


def irs_tfidf(docs, vocab=None):
    """Vector TF-IDF của từng tài liệu (danh sách từ): trọng số = số lần xuất hiện · ln(N/df). Trả (vocab, [vector])."""
    vocab = vocab or sorted({t for d in docs for t in d})
    N = len(docs)
    df = {t: sum(t in d for d in docs) for t in vocab}
    return vocab, [[d.count(t) * (math.log(N / df[t]) if df[t] else 0.0) for t in vocab] for d in docs]


def irs_ivf_cost(n, n_lists, n_probe):
    """Số phép so khoảng cách của tìm theo cụm (chỉ mục tệp ngược): so với mọi tâm cụm, rồi duyệt n_probe cụm, mỗi cụm n/n_lists vector
    (giả sử các cụm đều nhau)."""
    return n_lists + n_probe * n / n_lists


def irs_rrf(rankings, k=60):
    """Hợp nhất thứ hạng nghịch đảo (Cormack, Clarke, Büttcher 2009): điểm(d) = Σ 1/(k + hạng của d trong từng danh sách).
    rankings: danh sách các danh sách mã tài liệu (hạng 1 đứng đầu). Trả dict mã → điểm."""
    s = {}
    for r in rankings:
        for i, d in enumerate(r, 1):
            s[d] = s.get(d, 0.0) + 1 / (k + i)
    return s


def irs_sqdist(a, b):
    """Bình phương khoảng cách Euclid giữa hai điểm."""
    return sum((x - y) ** 2 for x, y in zip(a, b))


def irs_ivf_search(points, labels, centroids, q, m):
    """Tìm láng giềng gần nhất theo cụm: so q với mọi tâm, chọn m cụm gần nhất, chỉ duyệt điểm của các cụm đó.
    Trả (chỉ số điểm gần nhất tìm được, số phép tính khoảng cách đã làm)."""
    near = sorted(range(len(centroids)), key=lambda j: irs_sqdist(q, centroids[j]))[:m]
    cand = [i for i, l in enumerate(labels) if l in near]
    best = min(cand, key=lambda i: irs_sqdist(q, points[i]))
    return best, len(centroids) + len(cand)


def irs_ivf_sim(n=5000, d=8, n_lists=70, probes=(1, 2, 4, 8), k=10, n_q=50, seed=0, blobs=40, iters=15):
    """Đo thật (numpy, hạt giống cố định) độ phủ ở k láng giềng và số phép so trung bình của tìm theo cụm trên dữ liệu gồm `blobs`
    đám điểm chuẩn. Tâm cụm học bằng K trung bình `iters` vòng. Trả [(m, độ phủ, số phép so trung bình)]."""
    import numpy as np
    rng = np.random.default_rng(seed)
    C = rng.normal(0, 3, (blobs, d))
    X = C[rng.integers(0, blobs, n)] + rng.normal(0, 1, (n, d))
    Q = C[rng.integers(0, blobs, n_q)] + rng.normal(0, 1, (n_q, d))
    cent = X[rng.choice(n, n_lists, replace=False)].copy()
    for _ in range(iters):
        a = ((X[:, None, :] - cent[None]) ** 2).sum(-1).argmin(1)
        for j in range(n_lists):
            if (a == j).any():
                cent[j] = X[a == j].mean(0)
    a = ((X[:, None, :] - cent[None]) ** 2).sum(-1).argmin(1)
    out = []
    for m in probes:
        rc = cost = 0
        for q in Q:
            true = set(np.argsort(((X - q) ** 2).sum(1))[:k].tolist())
            near = np.argsort(((cent - q) ** 2).sum(1))[:m]
            idx = np.where(np.isin(a, near))[0]
            cost += n_lists + len(idx)
            found = set(idx[np.argsort(((X[idx] - q) ** 2).sum(1))[:k]].tolist())
            rc += len(true & found) / k
        out.append((m, round(rc / n_q, 3), round(cost / n_q)))
    return out

# ── IRS, nhánh A (bài 5–8): hàm thêm đặt NGAY TRÊN dòng mốc này ──
def irs_pair_prob(o):
    """Xác suất mô hình đặt a trên b, theo hiệu điểm o = s_a − s_b (hàm logistic, Burges và cộng sự 2005)."""
    return 1 / (1 + math.exp(-o))


def irs_pair_loss(s_a, s_b):
    """Mất mát theo cặp khi a liên quan hơn b: ln(1 + e^−(s_a − s_b)) = −ln P(a trên b)."""
    return math.log(1 + math.exp(-(s_a - s_b)))


def irs_wrong_pairs(gains):
    """Số cặp xếp sai thứ tự: i đứng trước j mà mức liên quan của i nhỏ hơn của j."""
    return sum(1 for i in range(len(gains)) for j in range(i + 1, len(gains)) if gains[i] < gains[j])


def irs_mse(pred, true):
    """Sai số bình phương trung bình."""
    return sum((a - b) ** 2 for a, b in zip(pred, true)) / len(true)


def irs_cos_common(u, v):
    """Cosin chỉ trên các sản phẩm CẢ HAI người đã chấm (0 = chưa chấm); không có món chung → None."""
    pairs = [(a, b) for a, b in zip(u, v) if a and b]
    if not pairs:
        return None
    return sum(a * b for a, b in pairs) / math.sqrt(sum(a * a for a, _ in pairs) * sum(b * b for _, b in pairs))


def irs_knn_predict(sims, ratings):
    """Dự đoán = trung bình có trọng số độ tương tự của điểm láng giềng: Σ s·r / Σ |s|."""
    return sum(s * r for s, r in zip(sims, ratings)) / sum(abs(s) for s in sims)


def irs_mean_rated(r):
    """Trung bình các điểm đã chấm (bỏ số 0 = chưa chấm)."""
    xs = [x for x in r if x]
    return sum(xs) / len(xs)


def irs_mf_step(p, q, r, eta, lam=0.0):
    """Một bước cập nhật theo một lượt chấm (Koren, Bell, Volinsky 2009): e = r − p·q; p ← p + η(e·q − λp); q ← q + η(e·p − λq),
    cả hai dùng giá trị CŨ. Trả (p_mới, q_mới, e)."""
    e = r - sum(a * b for a, b in zip(p, q))
    pn = [a + eta * (e * b - lam * a) for a, b in zip(p, q)]
    qn = [b + eta * (e * a - lam * b) for a, b in zip(p, q)]
    return pn, qn, e


def irs_fit_user(qs, rs, eta, lam=0.0, epochs=2000, p0=None):
    """Chỉ học vector người dùng p (vector sản phẩm qs giữ cố định): lặp các lượt chấm rs, mỗi lượt p ← p + η(e·q − λp)."""
    p = list(p0 or [0.1] * len(qs[0]))
    for _ in range(epochs):
        for q, r in zip(qs, rs):
            e = r - sum(a * b for a, b in zip(p, q))
            p = [a + eta * (e * b - lam * a) for a, b in zip(p, q)]
    return p


def irs_neg_probs(counts, power=0.75):
    """Xác suất chọn mỗi sản phẩm làm mẫu âm: tần suất mũ `power` rồi chuẩn hoá (Mikolov và cộng sự 2013 dùng 3/4)."""
    w = [c ** power for c in counts]
    s = sum(w)
    return [x / s for x in w]


def irs_logq(score, p):
    """Hiệu chỉnh tần suất lấy mẫu (Yi và cộng sự 2019): điểm − ln p."""
    return score - math.log(p)

# ── mốc IRS-A ──

# ── IRS, nhánh B (bài 9–12): hàm thêm đặt NGAY TRÊN dòng mốc này ──
def irs_beta_mean(a, b):
    """Trung bình của phân phối Beta(a, b): a / (a + b)."""
    return a / (a + b)


def irs_beta_sd(a, b):
    """Độ lệch chuẩn của Beta(a, b): căn của ab / ((a + b)² (a + b + 1))."""
    return math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))


def irs_beta_post(a, b, clicks, shows):
    """Cập nhật niềm tin sau `shows` lần hiển thị có `clicks` lượt bấm: Beta(a + bấm, b + không bấm)."""
    return a + clicks, b + shows - clicks


def _irs_beta_logpdf(x, a, b):
    return (a - 1) * math.log(x) + (b - 1) * math.log(1 - x) + math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)


def irs_beta_p_beats(a1, b1, a2, b2, n=40000):
    """Xác suất một lần rút từ Beta(a1, b1) lớn hơn một lần rút độc lập từ Beta(a2, b2) — tích phân số trên lưới n điểm giữa:
    P = Σ f2(y) · (1 − F1(y)) Δy."""
    h = 1 / n
    xs = [(i + 0.5) * h for i in range(n)]
    f1 = [math.exp(_irs_beta_logpdf(x, a1, b1)) * h for x in xs]
    f2 = [math.exp(_irs_beta_logpdf(x, a2, b2)) * h for x in xs]
    tot, F1 = 0.0, 0.0
    for p1, p2 in zip(f1, f2):
        tot += p2 * (1 - F1 - p1 / 2)
        F1 += p1
    return tot


def irs_bandit_run(rates, steps, rule="thompson", seed=0, prior=(1, 1)):
    """Mô phỏng hiển thị một trong các sản phẩm mỗi lượt (tỉ lệ bấm thật `rates`), cập nhật Beta sau mỗi lượt.
    rule = "thompson" (rút một mẫu từ mỗi Beta, hiện mẫu lớn nhất) hoặc "greedy" (hiện trung bình lớn nhất). prior: một cặp (a, b) chung
    hoặc danh sách cặp cho từng sản phẩm. Trả số lần hiện mỗi sản phẩm."""
    import random
    rng = random.Random(seed)
    ab = [list(prior) for _ in rates] if isinstance(prior[0], (int, float)) else [list(x) for x in prior]
    shows = [0] * len(rates)
    for _ in range(steps):
        if rule == "thompson":
            score = [rng.betavariate(a, b) for a, b in ab]
        else:
            score = [a / (a + b) for a, b in ab]
        i = max(range(len(rates)), key=lambda j: score[j])
        shows[i] += 1
        if rng.random() < rates[i]:
            ab[i][0] += 1
        else:
            ab[i][1] += 1
    return shows


def irs_ips(clicks, prop, cap=None):
    """Lượt bấm điều chỉnh theo xác suất được nhìn thấy: bấm · (1/p); có `cap` thì trọng số bị cắt ở min(1/p, cap)."""
    w = 1 / prop
    return clicks * (min(w, cap) if cap is not None else w)


def irs_ips_spread(n, prop, rel, cap=None):
    """Ước lượng mức liên quan bằng trọng số nghịch đảo: (số bấm · w) / n với w = 1/p (hoặc min(1/p, cap)); số bấm ~ nhị thức(n, p · rel).
    Trả (kỳ vọng, độ lệch chuẩn) của ước lượng theo công thức nhị thức."""
    w = min(1 / prop, cap) if cap is not None else 1 / prop
    q = prop * rel
    return q * w, math.sqrt(q * (1 - q) / n) * w


def irs_propensity_swap(ctr_at_j, ctr_at_1):
    """Ước lượng xác suất được nhìn ở vị trí j (so với vị trí 1) bằng hoán đổi ngẫu nhiên (Joachims và cộng sự 2017): p_j / p_1 = CTR@j / CTR@1."""
    return ctr_at_j / ctr_at_1


def irs_mmr(rel, max_sim, lam):
    """Điểm MMR (Carbonell, Goldstein 1998): λ · liên quan − (1 − λ) · độ giống lớn nhất với các kết quả đã chọn."""
    return lam * rel - (1 - lam) * max_sim


def irs_mmr_select(rels, sim, lam, k):
    """Chọn k kết quả theo MMR, tham lam từng bước. rels: điểm liên quan; sim[i][j]: độ giống. Trả danh sách chỉ số theo thứ tự chọn."""
    chosen = []
    while len(chosen) < k:
        cand = [i for i in range(len(rels)) if i not in chosen]
        best = max(cand, key=lambda i: irs_mmr(rels[i], max((sim[i][j] for j in chosen), default=0.0), lam))
        chosen.append(best)
    return chosen


def irs_exposure(positions):
    """Mức được nhìn thấy của một nhóm: tổng chiết khấu 1/log₂(vị trí + 1) của các vị trí nhóm đó chiếm (cùng chiết khấu với DCG)."""
    return sum(1 / math.log2(i + 1) for i in positions)


def irs_feedback_loop(rates, shows0, days, total, explore=0.0, by="clicks"):
    """Vòng phản hồi (kỳ vọng, tất định) với hai sản phẩm tỉ lệ bấm thật `rates` = (A, B). Mỗi ngày hệ dồn (1 − explore) phần lượt hiển thị
    cho sản phẩm thắng hôm trước, phần explore chia đều. Thắng theo by="clicks" (tổng lượt bấm hôm trước) hoặc by="rate" (lượt bấm chia
    lượt hiện, cộng dồn từ đầu). Trả danh sách (hiện A, hiện B) theo ngày, ngày đầu = shows0."""
    hist = [tuple(shows0)]
    tot = [0.0, 0.0, 0.0, 0.0]          # hiện A, bấm A, hiện B, bấm B cộng dồn
    for _ in range(days - 1):
        sa, sb = hist[-1]
        ca, cb = sa * rates[0], sb * rates[1]
        tot = [tot[0] + sa, tot[1] + ca, tot[2] + sb, tot[3] + cb]
        if by == "rate":
            a_wins = (tot[1] / tot[0] if tot[0] else 0) >= (tot[3] / tot[2] if tot[2] else 0)
        else:
            a_wins = ca >= cb
        win, ex = total * (1 - explore), total * explore / 2
        hist.append((win + ex, ex) if a_wins else (ex, win + ex))
    return hist


def irs_latency(stages):
    """Tổng độ trễ tuần tự (ms) của các tầng: danh sách số mi li giây."""
    return sum(stages)


def irs_max_candidates(budget, fixed, per_item):
    """Số ứng viên tối đa tầng xếp hạng chịu được: (ngân sách − phần cố định) / chi phí mỗi ứng viên, làm tròn xuống."""
    return int(math.floor((budget - fixed) / per_item + 1e-9))   # + 1e-9: 60 / 0,05 trong số thực là 1199,99…


def irs_tail_any(p_slow, n):
    """Xác suất ít nhất một trong n mảnh chạy song song bị chậm, khi mỗi mảnh chậm độc lập với xác suất p_slow: 1 − (1 − p)^n."""
    return 1 - (1 - p_slow) ** n

# ── mốc IRS-B ──


# ───────── Tương tác người–máy (HCI): định luật Fitts, Hick–Hyman, KLM, Nielsen–Landauer, SUS, hình vuông Latin, chống lỗi ─────────
def hci_minutes_diff(h1, m1, h2, m2):
    """Số phút từ thời điểm h1:m1 tới h2:m2 trong cùng một ngày."""
    return (h2 * 60 + m2) - (h1 * 60 + m1)


def hci_mappings(n):
    """Số cách ghép 1-1 giữa n nút điều khiển và n thiết bị: n!."""
    return math.factorial(n)


def hci_fitts_id(D, W):
    """Độ khó theo dạng Shannon (MacKenzie 1992): ID = log₂(D/W + 1) (bit)."""
    return math.log2(D / W + 1)


def hci_fitts_time(D, W, a=0.1, b=0.15):
    """Thời gian trỏ tới đích theo định luật Fitts: T = a + b · log₂(D/W + 1) (giây)."""
    return a + b * math.log2(D / W + 1)


def hci_hick_time(n, b=0.2, a=0.0):
    """Thời gian chọn trong n mục quen thuộc có xác suất bằng nhau (Hick 1952): T = a + b · log₂(n + 1)."""
    return a + b * math.log2(n + 1)


def hci_hick_entropy(probs, b=0.2, a=0.0):
    """Thời gian chọn khi các mục có xác suất khác nhau (Hyman 1953): T = a + b · Σ p_i log₂(1/p_i + 1) hoặc entropy."""
    h = sum(-p * math.log2(p) for p in probs if p > 0)
    return a + b * h, h


def hci_chunks(s):
    """Đếm (tổng số ký tự không kể khoảng trắng, số cụm tách bằng khoảng trắng)."""
    return len(s.replace(" ", "").replace("-", "")), len(s.replace("-", " ").split())


HCI_KLM_WEIGHTS = {"K": 0.2, "P": 1.1, "B": 0.1, "H": 0.4, "M": 1.35}


def hci_klm_time(ops, weights=None):
    """Cộng thời gian chuỗi thao tác KLM (Card, Moran, Newell 1980). ops là chuỗi hoặc danh sách ký tự trong {K, P, B, H, M}."""
    w = weights or HCI_KLM_WEIGHTS
    return round(sum(w[ch] for ch in ops if ch in w), 4)


def hci_nielsen_found(n, lam=0.31):
    """Tỉ lệ vấn đề khả dụng phát hiện được với n người thử (Nielsen, Landauer 1993): 1 − (1 − λ)^n."""
    return 1 - (1 - lam) ** n


def hci_sus_score(answers):
    """Điểm SUS (Brooke 1996) từ 10 câu trả lời thang 1..5: câu lẻ cộng (x − 1), câu chẵn cộng (5 − x), nhân 2,5."""
    odd = sum(x - 1 for x in answers[0::2])
    even = sum(5 - x for x in answers[1::2])
    return (odd + even) * 2.5, odd, even


def hci_is_latin_square(rows):
    """Kiểm bảng `rows` (danh sách chuỗi hoặc bộ cùng độ dài n) có phải hình vuông Latin: mỗi hàng và mỗi cột chứa đủ n ký hiệu."""
    n = len(rows)
    if any(len(r) != n for r in rows):
        return False
    syms = sorted(set(rows[0]))
    if len(syms) != n:
        return False
    return all(sorted(r) == syms for r in rows) and all(sorted(rows[i][j] for i in range(n)) == syms for j in range(n))


def hci_wcag_target_ok(w, h, min_px=24):
    """Kiểm kích thước đích theo WCAG 2.2 tiêu chí 2.5.8 (tối thiểu 24 × 24 điểm ảnh CSS)."""
    return w >= min_px and h >= min_px


def hci_swiss_cheese_leak(rates):
    """Xác suất lỗi lọt qua mọi lớp bảo vệ độc lập: tích các tỉ lệ lọt của từng lớp."""
    p = 1.0
    for r in rates:
        p *= r
    return p


# ───────── Đồ hoạ máy tính (GFX): biến đổi thuần nhất, chiếu phối cảnh, raster hoá, bộ đệm độ sâu, chiếu sáng, mipmap, sRGB, dò tia ─────────
def gfx_frame_budget_ms(fps):
    """Ngân sách thời gian một khung hình (mi li giây) ở tốc độ `fps` khung mỗi giây."""
    return 1000.0 / fps


def gfx_pixels_per_sec(w, h, fps):
    """Tổng số điểm ảnh cần xuất mỗi giây ở độ phân giải w × h và tốc độ `fps`."""
    return w * h * fps


def gfx_rot2d(deg):
    """Ma trận quay 2D thuần nhất 3 × 3 quanh gốc một góc `deg` độ."""
    import numpy as np
    rad = math.radians(deg)
    c, s = round(math.cos(rad), 12), round(math.sin(rad), 12)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def gfx_trans2d(tx, ty):
    """Ma trận tịnh tiến 2D thuần nhất 3 × 3 theo (tx, ty)."""
    import numpy as np
    return np.array([[1.0, 0.0, float(tx)], [0.0, 1.0, float(ty)], [0.0, 0.0, 1.0]])


def gfx_apply2d(M, x, y):
    """Áp ma trận 3 × 3 cho điểm 2D (x, y, 1) và trả (x′, y′)."""
    import numpy as np
    v = M @ np.array([float(x), float(y), 1.0])
    return round(float(v[0]), 6), round(float(v[1]), 6)


def gfx_persp_project(x, y, z, f=1.0):
    """Chiếu phối cảnh điểm (x, y, z) lên mặt phẳng ảnh ở khoảng cách f: (f·x/z, f·y/z)."""
    return f * x / z, f * y / z


def gfx_persp_interp(z0, z1, u0, u1, t):
    """Nội suy thuộc tính u tại vị trí màn hình t ∈ [0, 1]: trả (nội suy có hiệu chỉnh phối cảnh theo 1/z, nội suy tuyến tính màn hình)."""
    inv_z = (1 - t) * (1 / z0) + t * (1 / z1)
    u_over_z = (1 - t) * (u0 / z0) + t * (u1 / z1)
    return u_over_z / inv_z, (1 - t) * u0 + t * u1


def gfx_ndc_to_pixel(x_ndc, width):
    """Đổi toạ độ thiết bị chuẩn hoá x ∈ [−1, 1] sang toạ độ màn hình [0, width]."""
    return (x_ndc + 1) / 2 * width


def gfx_barycentric(p, a, b, c):
    """Toạ độ trọng tâm (α, β, γ) của điểm p đối với tam giác (a, b, c)."""
    import numpy as np
    M = np.array([[a[0], b[0], c[0]], [a[1], b[1], c[1]], [1.0, 1.0, 1.0]], dtype=float)
    w = np.linalg.solve(M, np.array([float(p[0]), float(p[1]), 1.0]))
    return tuple(round(float(x), 6) for x in w)


def gfx_depth_norm(z, n, f):
    """Giá trị độ sâu chuẩn hoá d ∈ [0, 1] theo công thức chiếu phối cảnh: d = f(z − n) / (z(f − n))."""
    return f * (z - n) / (z * (f - n))


def gfx_depth_step(z, n, f, bits=24):
    """Khoảng cách độ sâu nhỏ nhất phân biệt được ở khoảng cách z với bộ đệm `bits` bit: Δz ≈ z²(f − n) / (f · n · 2^bits)."""
    return z * z * (f - n) / (f * n * (2 ** bits))


def gfx_lambert(n_vec, l_vec):
    """Cường độ khuếch tán Lambert: max(0, n · l) với hai vector đơn vị."""
    dot = sum(a * b for a, b in zip(n_vec, l_vec))
    return max(0.0, dot)


def gfx_blinn_spec(n_dot_h, s):
    """Phần bóng sáng Blinn–Phong: max(0, n · h)^s."""
    return max(0.0, n_dot_h) ** s


def gfx_bilinear(v00, v10, v01, v11, u, v):
    """Nội suy song tuyến tại (u, v) ∈ [0, 1]² giữa bốn giá trị góc ô."""
    return (1 - u) * (1 - v) * v00 + u * (1 - v) * v10 + (1 - u) * v * v01 + u * v * v11


def gfx_mipmap_stats(size):
    """Cho kết cấu vuông `size × size` (lũy thừa của 2): trả (số mức mipmap, tổng số điểm kết cấu mọi mức, tỉ lệ tăng thêm so với mức gốc)."""
    levels = int(math.log2(size)) + 1
    total = sum((size >> k) ** 2 for k in range(levels))
    base = size * size
    return levels, total, (total - base) / base


def gfx_srgb_to_linear(c):
    """Đổi giá trị sRGB c ∈ [0, 1] sang ánh sáng tuyến tính theo chuẩn IEC 61966-2-1."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def gfx_linear_to_srgb(x):
    """Đổi ánh sáng tuyến tính x ∈ [0, 1] sang giá trị sRGB theo chuẩn IEC 61966-2-1."""
    return 12.92 * x if x <= 0.0031308 else 1.055 * (x ** (1 / 2.4)) - 0.055


def gfx_srgb_blend_byte(b1, b2, alpha=0.5):
    """Trộn hai mức xám 8 bit (0..255) với tỉ lệ alpha: trả (trộn thẳng trên byte, trộn đúng trong không gian tuyến tính rồi mã hoá lại)."""
    naive = round((1 - alpha) * b1 + alpha * b2)
    l1, l2 = gfx_srgb_to_linear(b1 / 255.0), gfx_srgb_to_linear(b2 / 255.0)
    lin_mix = (1 - alpha) * l1 + alpha * l2
    correct = round(gfx_linear_to_srgb(lin_mix) * 255.0)
    return naive, correct


def gfx_ray_sphere(origin, direction, center, radius):
    """Giao của tia O + t·D (với D đơn vị) và mặt cầu tâm C bán kính r. Trả (biệt thức Δ, danh sách nghiệm thực t tăng dần)."""
    oc = [o - c for o, c in zip(origin, center)]
    a = sum(d * d for d in direction)
    b = 2.0 * sum(o * d for o, d in zip(oc, direction))
    c_val = sum(o * o for o in oc) - radius * radius
    disc = b * b - 4 * a * c_val
    if disc < 0:
        return disc, []
    sq = math.sqrt(disc)
    t1, t2 = (-b - sq) / (2 * a), (-b + sq) / (2 * a)
    return disc, sorted([round(t1, 6), round(t2, 6)])


def gfx_schlick_fresnel(cos_theta, F0=0.04):
    """Xấp xỉ Fresnel của Schlick (1994): F(θ) = F₀ + (1 − F₀)(1 − cos θ)^5."""
    return F0 + (1 - F0) * ((1 - cos_theta) ** 5)


def gfx_overdraw_fragments(w, h, overdraw):
    """Số mảnh phải tô khi khung hình w × h có độ tô đè trung bình `overdraw` lần."""
    return round(w * h * overdraw)
