"""BNX L38 — mô hình thuần Python: hàng đợi có giao dịch, số ô phải đọc khi lưu theo hàng và theo cột, lệnh chuyển xuyên mảnh.
Không gọi cơ sở dữ liệu. Bộ kiểm audit/bnx/ver/l38.py chạy THẬT trên Oracle (bnx-ora) rồi so với các hàm này."""


def bnx_l38_queue(ops):
    """Hàng đợi có giao dịch: ('enq', x) gửi tạm, ('deq',) nhận tạm phần tử đầu, ('commit',) chốt, ('rollback',) huỷ mọi việc chưa chốt.
    Trả (các thông điệp đã nhận và chốt, số thông điệp còn trong hàng đợi)."""
    q, pend_enq, pend_deq, got = [], [], [], []
    for op in ops:
        if op[0] == "enq":
            pend_enq.append(op[1])
        elif op[0] == "deq":
            avail = [x for x in q if x not in pend_deq]
            if avail:
                pend_deq.append(avail[0])
        elif op[0] == "commit":
            q += pend_enq
            for x in pend_deq:
                q.remove(x)
                got.append(x)
            pend_enq, pend_deq = [], []
        elif op[0] == "rollback":
            pend_enq, pend_deq = [], []
    return got, len(q)


def bnx_l38_shard(acc, n):
    """Quy tắc chia mảnh MINH HOẠ của bài: mảnh = mã tài khoản chia lấy dư cho n (không phải cách Oracle chia)."""
    return acc % n


def bnx_l38_cells(n_rows, n_cols, layout):
    """Số ô phải đọc để cộng MỘT cột: lưu theo hàng đọc cả dòng (n_rows × n_cols ô), lưu theo cột chỉ đọc một cột (n_rows ô). Mô hình đếm, không đo thời gian."""
    if layout == "hang":
        return n_rows * n_cols
    if layout == "cot":
        return n_rows
    raise ValueError(layout)


def bnx_l38_cross(n_acc, n_shards):
    """(số cặp chuyển có thứ tự, số cặp xuyên mảnh) với mã 0..n_acc-1, mảnh = mã mod n_shards. Đếm theo cỡ từng lớp dư (công thức),
    khác cách đếm từng cặp của chương trình trên màn hình."""
    sizes = [len([a for a in range(n_acc) if a % n_shards == r]) for r in range(n_shards)]
    total = n_acc * (n_acc - 1)
    same = sum(s * (s - 1) for s in sizes)
    return total, total - same


def bnx_l38_moved(n_acc, old, new):
    """Số tài khoản đổi mảnh khi số mảnh đổi từ old sang new (chia lấy dư)."""
    return sum(1 for a in range(n_acc) if a % old != a % new)
