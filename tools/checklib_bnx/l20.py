"""BNX L20 — Go cho backend: lỗi là giá trị trả về, luồng nhẹ + nhóm chờ, tranh chấp dữ liệu, kênh có đệm / không đệm,
dịch vụ HTTP nhỏ. Mô hình tính thuần Python (không chạy Go, không mạng). Chỉ thư viện chuẩn.
Kiểm độc lập ở audit/bnx/ver/l20.py (duyệt mọi cách xen kẽ, luồng Python thật, queue.Queue, chạy thật go run / go run -race)."""
import json as _json


def bnx_l20_rut(so_du, so_tien):
    """Hàm rut của bài: (số dư sau, lỗi). Không đủ tiền → số dư giữ nguyên, lỗi là chuỗi; đủ → lỗi None (nil)."""
    if so_tien > so_du:
        return so_du, "không đủ số dư"
    return so_du - so_tien, None


def bnx_l20_wg(n_add, n_done):
    """Bộ đếm việc của nhóm chờ sau n_add lần Add(1) và n_done lần Done. Wait trở về khi và chỉ khi bằng 0."""
    return n_add - n_done


def bnx_l20_locked(n_goroutines, per=1):
    """Bộ đếm khi mỗi lần tăng nằm trọn trong khoá: không lần tăng nào bị mất."""
    return n_goroutines * per


def bnx_l20_interleave(order):
    """Tăng bộ đếm KHÔNG khoá. Mỗi luồng làm hai bước: đọc rồi ghi (giá trị đã đọc + 1). `order` là dãy tên luồng theo thứ tự
    bước chạy (mỗi tên xuất hiện đúng 2 lần: lần đầu là đọc, lần sau là ghi). Trả giá trị cuối của bộ đếm (bắt đầu từ 0)."""
    dem, da_doc = 0, {}
    for t in order:
        if t not in da_doc:
            da_doc[t] = dem
        else:
            dem = da_doc[t] + 1
    return dem


def bnx_l20_lost(order):
    """Số lần tăng bị mất của một cách xen kẽ."""
    return len(set(order)) - bnx_l20_interleave(order)


def bnx_l20_range(n_goroutines):
    """(nhỏ nhất, lớn nhất) bộ đếm có thể ra khi n luồng, mỗi luồng tăng một lần không khoá, theo mô hình đọc rồi ghi."""
    return (1 if n_goroutines else 0), n_goroutines


def bnx_l20_chan(cap, ops):
    """Kênh sức chứa cap (0 = không đệm, không có bên nhận đang chờ). ops: ('g', v) thử gửi không chờ, ('n',) nhận.
    Trả danh sách kết quả: ('xong', đang chứa) | ('chờ',) cho gửi; ('nhận', v) cho nhận."""
    buf, res = [], []
    for op in ops:
        if op[0] == "g":
            if len(buf) < cap:
                buf.append(op[1])
                res.append(("xong", len(buf)))
            else:
                res.append(("chờ",))
        else:
            res.append(("nhận", buf.pop(0)))
    return res


def bnx_l20_accept(cap, n_send):
    """Gửi liền n_send giá trị vào kênh đệm cap, không ai nhận: (số giá trị vào được, thứ tự của giá trị đầu tiên phải chờ | None)."""
    ok = min(cap, n_send)
    return ok, (ok + 1 if n_send > cap else None)


def bnx_l20_route(method, path):
    """Dịch vụ của bài: tuyến "GET /suc-khoe". Trả (mã trạng thái, thân)."""
    if path == "/suc-khoe":
        if method == "GET":
            return 200, _json.dumps({"trang_thai": "ok"}, separators=(",", ":"))
        return 405, "Method Not Allowed"
    return 404, "404 page not found"


def bnx_l20_fiber_route(path):
    """Hai tuyến Fiber của bài: /suc-khoe và /tai-khoan/:so (tham số đường dẫn)."""
    if path == "/suc-khoe":
        return 200, _json.dumps({"trang_thai": "ok"}, separators=(",", ":"))
    parts = path.strip("/").split("/")
    if len(parts) == 2 and parts[0] == "tai-khoan" and parts[1]:
        return 200, _json.dumps({"so": parts[1]}, separators=(",", ":"))
    return 404, "Cannot GET " + path


def bnx_l20_atoi(s):
    """strconv.Atoi rút gọn cho số không dấu: (giá trị, có lỗi). Lỗi → giá trị 0 (giá trị không của kiểu int)."""
    if s and all(c in "0123456789" for c in s):
        return int(s), False
    return 0, True


def bnx_l20_leak(n_requests, buffered):
    """Mỗi yêu cầu sinh một luồng nhẹ gửi kết quả vào kênh riêng; bên nhận đã bỏ đi vì hết hạn chờ.
    Kênh không đệm → luồng gửi kẹt mãi; kênh đệm 1 → gửi xong rồi kết thúc. Trả số luồng nhẹ đang sống (kể cả luồng chính)."""
    return 1 + (0 if buffered else n_requests)


def bnx_l20_race_exit():
    """Mã thoát mặc định của chương trình chạy kèm trình phát hiện tranh chấp khi thấy tranh chấp (go.dev/doc/articles/race_detector, tuỳ chọn exitcode)."""
    return 66


def bnx_l20_thru(workers, ms_per_job):
    """Số việc xử lý được mỗi giây của `workers` luồng nhẹ làm việc, mỗi việc `ms_per_job` mili giây."""
    return workers * 1000 // ms_per_job


def bnx_l20_wait(cap, per_sec):
    """Thời gian chờ nhiều nhất (giây) của việc xếp cuối trong kênh đệm `cap` khi xử lý `per_sec` việc mỗi giây."""
    return cap / per_sec
