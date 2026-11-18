"""BNX L29 — CQRS và Event Sourcing cho sổ tiền: mô hình tham chiếu của phát lại sự kiện (số dư = tổng có dấu) và số sự kiện phải đọc khi có/không bản chụp.
Chỉ thư viện chuẩn, không mạng. Kiểm độc lập ở audit/bnx/ver/l29.py (chạy THẬT Python + sqlite: trigger chặn sửa/xoá, phát lại, bù, đọc trễ; đếm bằng SQL)."""


def bnx_l29_replay(su_kien, so_du=0):
    """Phát lại: NAP cộng, RUT trừ, theo thứ tự."""
    for loai, tien in su_kien:
        so_du += tien if loai == "NAP" else -tien
    return so_du


def bnx_l29_events_to_read(n, k):
    """Số sự kiện phải đọc để dựng số dư tại sự kiện thứ n: không bản chụp (k = 0) thì n; cứ k sự kiện một bản chụp thì n mod k."""
    return n if k == 0 else n % k
