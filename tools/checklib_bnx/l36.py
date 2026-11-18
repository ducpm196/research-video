"""BNX L36 — Phỏng vấn thiết kế hệ thống (trung tâm thanh toán, hệ thống tín dụng): ước lượng tải ở ×1, ×100, ×10 000, số lệnh lệch cần đối soát, khoá lũy đẳng.
Mọi số đầu vào (khách, giao dịch, hệ số đỉnh, sức một nút) là số minh hoạ của bài. Chỉ thư viện chuẩn, không mạng.
Kiểm độc lập ở audit/bnx/ver/l36.py (chạy THẬT Python + sqlite; tính lại bằng Fraction)."""
import math


def bnx_l36_gd(khach, gd_khach, he_so):
    """Giao dịch mỗi ngày."""
    return khach * he_so * gd_khach


def bnx_l36_tb(khach, gd_khach, he_so):
    """Giao dịch mỗi giây, trung bình (86 400 giây một ngày), làm tròn 1 chữ số."""
    return round(bnx_l36_gd(khach, gd_khach, he_so) / 86400, 1)


def bnx_l36_dinh(khach, gd_khach, he_so, he_so_dinh):
    """Giao dịch mỗi giây ở đỉnh = trung bình × hệ số đỉnh, làm tròn số nguyên."""
    return round(bnx_l36_gd(khach, gd_khach, he_so) / 86400 * he_so_dinh)


def bnx_l36_gb(khach, gd_khach, he_so, byte):
    """Gigabyte mỗi ngày (1 GB = 10^9 byte), làm tròn 1 chữ số."""
    return round(bnx_l36_gd(khach, gd_khach, he_so) * byte / 10 ** 9, 1)


def bnx_l36_nut(khach, gd_khach, he_so, he_so_dinh, suc_nut):
    """Số nút ghi = làm tròn LÊN (giao dịch đỉnh : sức một nút)."""
    return math.ceil(bnx_l36_gd(khach, gd_khach, he_so) / 86400 * he_so_dinh / suc_nut)


def bnx_l36_lech(n, chu_ky=500):
    """Số lệnh lệch khi cứ chu_ky lệnh thì 1 lệnh hỏng bước ghi có (lệnh thứ chu_ky − 1, 2·chu_ky − 1, … tính từ 0)."""
    return n // chu_ky


def bnx_l36_gio(lech, phut=10):
    """Giờ xử lý tay nếu mỗi lệch mất `phut` phút, làm tròn 1 chữ số."""
    return round(lech * phut / 60, 1)
