"""BNX L16 — Đa luồng Java nâng cao: bể luồng cố định, hàng đợi có giới hạn, ghép lời gọi song song, chia để trị.
Mô hình tính (không đo thời gian thật): bể n luồng nhận việc theo thứ tự gửi, luồng rảnh sớm nhất lấy việc đầu hàng.
Chỉ thư viện chuẩn. Kiểm độc lập ở audit/bnx/ver/l16.py (mô phỏng từng mili giây, công thức đóng, chạy thật javac/java)."""
import heapq as _hq


def bnx_pool_rounds(n_tasks, n_threads):
    """Số lượt khi mọi việc dài bằng nhau: làm tròn lên của n_tasks / n_threads."""
    return -(-n_tasks // n_threads)


def bnx_pool_schedule(durations, n_threads):
    """[(bắt đầu, kết thúc)] của từng việc, theo thứ tự gửi; mọi việc gửi ở thời điểm 0."""
    free = [0] * n_threads
    _hq.heapify(free)
    res = []
    for d in durations:
        t = _hq.heappop(free)
        res.append((t, t + d))
        _hq.heappush(free, t + d)
    return res


def bnx_pool_makespan(durations, n_threads):
    """Thời điểm việc cuối cùng xong (thời gian chờ cả lô)."""
    return max(e for _, e in bnx_pool_schedule(durations, n_threads))


def bnx_work_total(durations):
    """Tổng công việc (mili giây luồng): không đổi dù chạy bao nhiêu luồng."""
    return sum(durations)


def bnx_finish_order(calls, n_threads):
    """calls = [(tên, ms)] theo thứ tự gửi → tên theo thứ tự xong."""
    sch = bnx_pool_schedule([ms for _, ms in calls], n_threads)
    return [calls[i][0] for i in sorted(range(len(calls)), key=lambda i: (sch[i][1], i))]


def bnx_pool_admit(n_tasks, n_threads, queue_cap):
    """Gửi liền n_tasks việc chưa việc nào xong, bể n_threads luồng (core = max), hàng đợi queue_cap chỗ:
    (số việc được nhận, số việc bị từ chối)."""
    ok = min(n_tasks, n_threads + queue_cap)
    return ok, n_tasks - ok


def bnx_pool_throughput(n_threads, task_ms):
    """Số việc bể xử lý được mỗi giây."""
    return n_threads * 1000 // task_ms


def bnx_queue_backlog(arrive_per_s, n_threads, task_ms, seconds):
    """Số việc nằm chờ sau `seconds` giây khi hàng đợi không giới hạn."""
    return max(0, arrive_per_s - bnx_pool_throughput(n_threads, task_ms)) * seconds


def bnx_fj_leaves(lo, hi, threshold):
    """Số việc lá khi chia đôi đoạn [lo, hi] tại (lo + hi) // 2 tới khi số phần tử ≤ threshold."""
    if hi - lo + 1 <= threshold:
        return 1
    mid = (lo + hi) // 2
    return bnx_fj_leaves(lo, mid, threshold) + bnx_fj_leaves(mid + 1, hi, threshold)


def bnx_fj_sum(lo, hi, threshold):
    """Tổng lo..hi tính đúng theo cây chia đôi (lá cộng bằng công thức cấp số cộng)."""
    if hi - lo + 1 <= threshold:
        return (lo + hi) * (hi - lo + 1) // 2
    mid = (lo + hi) // 2
    return bnx_fj_sum(lo, mid, threshold) + bnx_fj_sum(mid + 1, hi, threshold)


def bnx_fj_depth(n, threshold):
    """Số lần chia đôi tới khi n / 2^k ≤ threshold."""
    k = 0
    while n > threshold * 2 ** k:
        k += 1
    return k


def bnx_gauss(n):
    return n * (n + 1) // 2


def bnx_shared_order(io_ms, n_threads, shared):
    """Các việc chờ vào ra (io_ms, gửi trước) rồi một việc tính ~0 ms. shared=True: cùng một bể n_threads luồng;
    False: việc tính có bể riêng. Trả (thứ tự xong, thời điểm việc tính bắt đầu)."""
    sch = bnx_pool_schedule(list(io_ms) + ([0] if shared else []), n_threads)
    ev = [(sch[i][1], 0, f"chờ {ms}") for i, ms in enumerate(io_ms)]
    start = sch[-1][0] if shared else 0
    ev.append((start, 1, "tính"))   # việc tính chỉ bắt đầu sau khi một luồng vừa rảnh
    return [n for _, _, n in sorted(ev)], start
