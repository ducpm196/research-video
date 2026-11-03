# CAS L09 — Heartbleed. Đường KHÁC `checks`: dựng bản ghi thật bằng bytes + struct (2 byte độ dài kiểu mạng), chạy một bộ đọc an toàn
# theo đúng các phép kiểm của bản vá 1.0.1g / RFC 6520 §4 trên mọi giá trị khai báo; số ngày bằng datetime; sympy giải bất đẳng thức.
import datetime as dt
import struct

import sympy as sp

MAX_PLAIN = 2 ** 14                                   # RFC 6520: tin không vượt 2^14 byte


def make_record(declared, payload=b"A", pad=16):      # bản ghi minh hoạ (phòng thủ): loại 1 byte, độ dài khai báo, dữ liệu, đệm
    return bytes([1]) + struct.pack(">H", declared) + payload + bytes(pad)


def safe_reply(rec):                                  # trả None = bỏ qua lặng lẽ
    if 1 + 2 + 16 > len(rec):
        return None
    n = struct.unpack(">H", rec[1:3])[0]
    if 1 + 2 + n + 16 > len(rec):
        return None
    if 1 + 2 + n + 16 > MAX_PLAIN:
        return None
    return rec[3:3 + n]


r20 = make_record(1)
rec("L09a", len(r20) == 20 and safe_reply(r20) == b"A", "bản ghi 20 byte, khai 1: nhận, trả đúng 1 byte")
rec("L09b", safe_reply(make_record(65535)) is None and 1 + 2 + 65535 + 16 == 65554, "khai 65 535 trên bản ghi 20 byte: bỏ (65 554 > 20)")
acc = [n for n in range(2 ** 16) if safe_reply(bytes([1]) + struct.pack(">H", n) + b"A" + bytes(16)) is not None]
rec("L09c", acc == [0, 1] and 2 ** 16 - len(acc) == 65534, "thử hết 65 536 giá trị: chỉ 0 và 1 được nhận; 65 534 bị bỏ")
n, L = sp.symbols("n L", integer=True)
sol = sp.solve(sp.Le(1 + 2 + n + 16, 16384), n)
rec("L09d", sp.Le(n, 16365).equals(sol) or str(sol) == "(-oo < n) & (n <= 16365)", "n lớn nhất trong giới hạn 2^14: 16 365")
rec("L09e", safe_reply(bytes(18)) is None and safe_reply(make_record(0, b"")) == b"", "bản ghi < 19 byte bị bỏ; 19 byte với n = 0 nhận")
rec("L09f", (dt.date(2014, 4, 7) - dt.date(2012, 3, 14)).days == 754 and 2 ** 16 - 1 == 65535, "1.0.1 (14/3/2012) → 1.0.1g (7/4/2014): 754 ngày")
q = lambda declared, real: 2 + declared <= real
rec("L09g", not q(300, 50) and max(d for d in range(2 ** 16) if q(d, 50)) == 48, "quiz: 2 + 300 > 50 bỏ; lớn nhất 48")
