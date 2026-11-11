"""BNX L02 — Protocol Buffers bằng tay (khoá trường, varint, chuỗi) và hạn chót qua chuỗi lời gọi. Chỉ thư viện chuẩn."""
import json as _json


def bnx_pb_varint(n):
    """Số nguyên không âm → byte varint (7 bit mỗi byte, byte thấp trước, bit 8 = còn byte sau)."""
    if n < 0:
        raise ValueError("chỉ mã số không âm")
    out = bytearray()
    while n >= 0x80:
        out.append((n % 128) + 128)
        n //= 128
    out.append(n)
    return bytes(out)


def bnx_pb_key(num, wire):
    """Khoá trường = (số hiệu << 3) | kiểu dây, viết bằng phép nhân để khác cách viết trong bài."""
    return num * 8 + wire


def bnx_pb_field(num, wire, value):
    """Một trường đã mã hoá: kiểu 0 (VARINT) mang số nguyên; kiểu 2 (LEN) mang byte/chuỗi: độ dài rồi byte."""
    if wire == 0:
        return bnx_pb_varint(bnx_pb_key(num, 0)) + bnx_pb_varint(value)
    if wire == 2:
        b = value.encode("utf-8") if isinstance(value, str) else bytes(value)
        return bnx_pb_varint(bnx_pb_key(num, 2)) + bnx_pb_varint(len(b)) + b
    raise ValueError("bài chỉ dùng kiểu 0 và 2")


def _read_varint(buf, i):
    n, mul = 0, 1
    while True:
        b = buf[i]
        i += 1
        n += (b % 128) * mul
        mul *= 128
        if b < 128:
            return n, i


def bnx_pb_decode(buf):
    """Byte → {số hiệu: giá trị} (kiểu 0 → int, kiểu 2 → bytes)."""
    i, out = 0, {}
    while i < len(buf):
        key, i = _read_varint(buf, i)
        num, wire = key // 8, key % 8
        if wire == 0:
            out[num], i = _read_varint(buf, i)
        elif wire == 2:
            ln, i = _read_varint(buf, i)
            out[num], i = bytes(buf[i:i + ln]), i + ln
        else:
            raise ValueError(f"kiểu dây {wire} không có trong bài")
    return out


def bnx_pb_named(buf, names):
    """Giải mã rồi gắn tên theo bảng {số hiệu: tên} của một bản .proto."""
    return {names[k]: v for k, v in bnx_pb_decode(buf).items() if k in names}


def bnx_json_len(obj):
    """Số byte của JSON gọn (không dấu cách) mã UTF-8."""
    return len(_json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def bnx_deadline_chain(budget_ms, costs_ms, propagate=True):
    """Chuỗi dịch vụ gọi nối nhau, mỗi dịch vụ cần costs_ms[k] ms. propagate=True: mỗi dịch vụ nhận THỜI GIAN CÒN LẠI;
    False: mỗi dịch vụ tự đặt lại budget_ms. Trả [(trạng thái, ms còn lại khi bắt đầu)] và dừng ở dịch vụ hết giờ đầu tiên
    (propagate=True); với False trả cả chuỗi và trạng thái 'xong' kể cả khi người gọi đầu đã bỏ cuộc."""
    out, used = [], 0
    for c in costs_ms:
        left = budget_ms - used if propagate else budget_ms
        if c > left:
            out.append(("hết giờ", left))
            return out
        out.append(("xong", left))
        used += c
    return out


def bnx_deadline_wasted(budget_ms, costs_ms):
    """Khi mỗi dịch vụ đặt lại hạn: số ms chuỗi còn chạy sau lúc người gọi đầu đã bỏ cuộc (0 nếu kịp)."""
    return max(0, sum(costs_ms) - budget_ms)
