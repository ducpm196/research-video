"""BNX L35 — Vận hành và tài liệu: ngân sách ngừng theo SLA, độ sẵn sàng của chuỗi dịch vụ nối tiếp, phần vượt ngân sách. Dùng Decimal/Fraction (thư viện chuẩn).
Kiểm độc lập ở audit/bnx/ver/l35.py (chạy lại Python thật; tính lại bằng phân số và bằng đếm từng phút)."""
from decimal import Decimal


def bnx_l35_budget(ti_le, ngay):
    """Ngân sách ngừng (phút) = ngày × 24 × 60 × (100 − tỉ lệ %) : 100. ti_le là chuỗi như '99.9'. Trả số thực (làm tròn 6 chữ số)."""
    return round(float(Decimal(ngay) * 24 * 60 * (100 - Decimal(ti_le)) / 100), 6)


def bnx_l35_chain(cac_ti_le, nd=6):
    """Độ sẵn sàng chung của các dịch vụ nối tiếp (dạng 0–1, chuỗi như '0.999'): tích, làm tròn nd chữ số."""
    p = Decimal(1)
    for x in cac_ti_le:
        p *= Decimal(x)
    return round(float(p), nd)


def bnx_l35_over(da_dung, ngan_sach):
    """Số phút vượt ngân sách (0 nếu còn trong ngân sách)."""
    return round(max(0.0, float(Decimal(str(da_dung)) - Decimal(str(ngan_sach)))), 6)
