"""BNX L07 — mô hình thuần Python: phân vùng theo tháng và cắt tỉa phân vùng, lọc JSON (hàng đợi, chia mảnh đã chuyển sang l38.py).
Không gọi cơ sở dữ liệu. Bộ kiểm audit/bnx/ver/l07.py chạy THẬT trên Oracle (bnx-ora) rồi so với các hàm này."""
import calendar as _cal
import datetime as _dt
import json as _json


def bnx_l07_days(lo, hi):
    """Số ngày trong [lo, hi) — lo, hi là chuỗi 'YYYY-MM-DD'."""
    return (_dt.date.fromisoformat(hi) - _dt.date.fromisoformat(lo)).days


def bnx_l07_month_days(y, m):
    return _cal.monthrange(y, m)[1]


def bnx_l07_load(n_rows, per_day=10, start="2025-01-01"):
    """Dữ liệu nạp: dòng thứ r (từ 1) có ngày = start + (r − 1) // per_day. Trả danh sách ngày."""
    d0 = _dt.date.fromisoformat(start)
    return [d0 + _dt.timedelta(days=(r - 1) // per_day) for r in range(1, n_rows + 1)]


def bnx_l07_partitions(dates, first_bound="2025-02-01"):
    """Phân vùng theo khoảng một tháng: phân vùng đầu chứa ngày < first_bound, mỗi tháng sau một phân vùng tự sinh.
    Trả số phân vùng (đếm các tháng khác nhau, gộp mọi tháng trước mốc đầu vào phân vùng 1)."""
    b = _dt.date.fromisoformat(first_bound)
    keys = {("p1",) if d < b else (d.year, d.month) for d in dates}
    return len(keys)


def bnx_l07_position(d, first_bound="2025-02-01"):
    """Vị trí phân vùng (từ 1) của một ngày, khi phân vùng đầu kết thúc ở first_bound và mỗi phân vùng sau dài một tháng."""
    d, b = _dt.date.fromisoformat(d), _dt.date.fromisoformat(first_bound)
    if d < b:
        return 1
    return 2 + (d.year - b.year) * 12 + (d.month - b.month)


def bnx_l07_prune(lo, hi):
    """Điều kiện ngay >= lo AND ngay < hi: (Pstart, Pstop) = vị trí phân vùng của lo và của ngày cuối cùng < hi."""
    last = (_dt.date.fromisoformat(hi) - _dt.timedelta(days=1)).isoformat()
    return bnx_l07_position(lo), bnx_l07_position(last)


def bnx_l07_count(dates, lo, hi):
    a, b = _dt.date.fromisoformat(lo), _dt.date.fromisoformat(hi)
    n = 0
    for d in dates:
        if a <= d < b:
            n += 1
    return n


def bnx_l07_max_partitions():
    """Giới hạn số phân vùng của một bảng theo Oracle Database Reference, “Logical Database Limits”: 1024K − 1."""
    return 1024 * 1024 - 1


def bnx_l07_json_ids(docs, field, threshold):
    """docs: {id: chuỗi}. Chuỗi không phải JSON hợp lệ thì bị ràng buộc IS JSON từ chối (không vào bảng).
    Trả (các id được nhận, các id có field > threshold)."""
    ok, hit = [], []
    for i, s in docs.items():
        try:
            v = _json.loads(s)
        except ValueError:
            continue
        ok.append(i)
        if isinstance(v.get(field), (int, float)) and v[field] > threshold:
            hit.append(i)
    return ok, hit


def bnx_l07_month_rows(per_day, month, year=2025):
    """Số dòng của một tháng khi mỗi ngày nạp per_day dòng (công thức đóng): số ngày của tháng × per_day."""
    return bnx_l07_month_days(year, month) * per_day
