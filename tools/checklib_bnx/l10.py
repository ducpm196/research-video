"""BNX L10 — Kafka nén nhật ký (bia mộ), kiểm lược đồ BACKWARD (giản lược), sàn chủ đề RabbitMQ (* và #). Chỉ thư viện chuẩn."""

def bnx_l10_log():
    """8 bản ghi của 3 khoá (VER BNX:L10)."""
    return [("A", 100), ("B", 200), ("A", 150), ("C", 50), ("B", 180), ("A", 120), ("C", 75), ("B", 260)]


def bnx_compact(log, drop_tombstones=True):
    """Giữ bản cuối của mỗi khoá, giữ nguyên offset. Bia mộ (giá trị None): drop_tombstones=False → còn giữ bia mộ (trong
    thời gian delete.retention.ms); True → khoá biến mất hẳn (sau thời gian đó). Trả [(offset, khoá, giá trị)] theo offset."""
    last = {}
    for off, (k, v) in enumerate(log):
        last[k] = (off, v)
    return sorted((off, k, v) for k, (off, v) in last.items() if v is not None or not drop_tombstones)


def bnx_topic_match(pattern, key):
    """Khớp khoá định tuyến (các từ nối bằng dấu chấm) với mẫu liên kết: * đúng một từ, # không hoặc nhiều từ."""
    p, k = pattern.split("."), key.split(".")

    def m(i, j):
        if i == len(p):
            return j == len(k)
        if p[i] == "#":
            return any(m(i + 1, t) for t in range(j, len(k) + 1))
        return j < len(k) and p[i] in ("*", k[j]) and m(i + 1, j + 1)
    return m(0, 0)


def bnx_route(bindings, key):
    """bindings: [(hàng đợi, mẫu)]. Trả danh sách hàng đợi nhận (mỗi hàng đợi một lần dù khớp nhiều mẫu)."""
    out = []
    for q, pat in bindings:
        if bnx_topic_match(pat, key) and q not in out:
            out.append(q)
    return out


def bnx_backward_ok(new, old):
    """Giản lược quy tắc BACKWARD: bên đọc dùng lược đồ mới đọc được dữ liệu ghi bằng lược đồ cũ khi mọi trường MỚI có giá trị
    mặc định (bỏ trường thì được). new/old: {tên trường: có mặc định?}. Trả (được?, [trường gây lỗi])."""
    bad = [f for f, has_default in new.items() if f not in old and not has_default]
    return len(bad) == 0, bad


def bnx_ms_to_hours(ms):
    return ms / 3_600_000
