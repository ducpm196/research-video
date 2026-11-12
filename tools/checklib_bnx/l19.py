"""BNX L19 — Redis nâng cao: khe băm của cụm (CRC16 XMODEM mod 16384, thẻ băm), chia khe cho các nút, khoá SET NX EX có mã chủ khoá,
khử trùng theo mã giao dịch có hạn, danh sách đen mã truy cập. Chỉ thư viện chuẩn, không mạng, không Docker.
Kiểm độc lập ở audit/bnx/ver/l19.py (CRC tính từng bit, Redis 8.10.3 thật trong Docker)."""

_L19_SLOTS = 16384


def _l19_table():
    t = []
    for i in range(256):
        c = i << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
        t.append(c)
    return t


_L19_T = _l19_table()


def bnx_l19_crc16(data):
    """CRC16 XMODEM (đa thức 0x1021, khởi đầu 0, không đảo bit) — tra bảng 256 ô. data: bytes hoặc str."""
    if isinstance(data, str):
        data = data.encode()
    c = 0
    for b in data:
        c = ((c << 8) & 0xFFFF) ^ _L19_T[((c >> 8) ^ b) & 0xFF]
    return c


def bnx_l19_hashed_part(key):
    """Phần của khoá được đem băm: nếu có '{' rồi '}' bên phải và giữa có ít nhất 1 ký tự thì chỉ băm phần giữa (thẻ băm)."""
    s = key.find("{")
    if s >= 0:
        e = key.find("}", s + 1)
        if e > s + 1:
            return key[s + 1:e]
    return key


def bnx_l19_slot(key):
    return bnx_l19_crc16(bnx_l19_hashed_part(key)) % _L19_SLOTS


def bnx_l19_ranges(n=3):
    """Cách redis-cli --cluster create chia 16384 khe cho n nút chính (đã thấy thật với n = 3: 0–5460, 5461–10922, 10923–16383)."""
    per, out, first, cur = _L19_SLOTS / n, [], 0, 0.0
    for i in range(n):
        last = _L19_SLOTS - 1 if i == n - 1 else int(cur + per - 1 + 0.5)
        out.append((first, last))
        first, cur = last + 1, cur + per
    return out


def bnx_l19_node(slot, n=3):
    """Số thứ tự (từ 1) của nút giữ khe."""
    for i, (a, b) in enumerate(bnx_l19_ranges(n), 1):
        if a <= slot <= b:
            return i
    raise ValueError(slot)


def bnx_l19_node_of_key(key, n=3):
    return bnx_l19_node(bnx_l19_slot(key), n)


def bnx_l19_same_slot(*keys):
    return len({bnx_l19_slot(k) for k in keys}) == 1


def bnx_l19_set_nx_ex(times, ttl):
    """Gửi cùng một lệnh SET khoá NX EX ttl ở các giây `times` (tăng dần): trả danh sách 'OK' / None như Redis.
    Khoá hết hạn đúng lúc đồng hồ chạm (lúc đặt + ttl)."""
    exp, out = None, []
    for t in times:
        if exp is not None and t < exp:
            out.append(None)
        else:
            exp = t + ttl
            out.append("OK")
    return out


def bnx_l19_processed(times, ttl):
    """Số lần yêu cầu được XỬ LÝ (không bị khử trùng) khi bên gửi gửi cùng mã giao dịch ở các giây `times`."""
    return sum(1 for x in bnx_l19_set_nx_ex(times, ttl) if x == "OK")


def bnx_l19_bl_ttl(exp, now):
    """Hạn của mục danh sách đen = thời gian còn lại của mã truy cập (0 nếu mã đã hết hạn: không cần ghi)."""
    return max(0, exp - now)


def bnx_l19_lock_story(ttl, pause, owner_check=True):
    """A lấy khoá ở giây 0 (hạn ttl), dừng tới giây `pause` rồi làm việc và nhả khoá; B xin khoá ngay khi khoá của A hết hạn.
    Trả (số người cùng làm việc ở giây pause, kết quả lệnh nhả của A: 0 = không xoá gì, 1 = xoá mất khoá — của B nếu B đang giữ)."""
    holder, exp = "A", ttl
    if pause >= exp:
        holder, exp = "B", exp + ttl           # B lấy được khoá lúc khoá A hết hạn
    working = 2 if holder == "B" else 1          # A tỉnh dậy vẫn làm việc
    if owner_check:
        released = 1 if holder == "A" else 0
    else:
        released = 1                             # DEL thẳng: xoá bất kể khoá của ai
    return working, released


def bnx_l19_overrun(ttl, pause):
    return max(0, pause - ttl)
