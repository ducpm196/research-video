"""BNX L15 — tình huống chuyên gia: ước lượng tải, ngân sách độ trễ, số lệnh cùng lúc (định luật Little). Số minh hoạ."""
from decimal import ROUND_HALF_UP as _HU
from decimal import Decimal as _D
from fractions import Fraction as _F

BNX_L15_SEC_PER_DAY = 24 * 60 * 60


def bnx_l15_tps(per_day, peak=1):
    """Giao dịch mỗi giây (phân số đúng): per_day / 86 400, nhân hệ số cao điểm."""
    return _F(per_day * peak, BNX_L15_SEC_PER_DAY)


def bnx_l15_round(x, nd=0):
    """Làm tròn nửa lên (kiểu viết tay), trả Decimal: bnx_l15_round(F(1000000, 86400), 1) == Decimal('11.6')."""
    q = _D(1).scaleb(-nd)
    return (_D(_F(x).numerator) / _D(_F(x).denominator)).quantize(q, rounding=_HU)


def bnx_l15_left(budget, parts):
    """Ngân sách độ trễ còn dư khi các chặng chạy nối tiếp."""
    return budget - sum(parts)


def bnx_l15_inflight(rate_per_s, ms):
    """Số việc đang xử lý cùng lúc = tốc độ đến × thời gian mỗi việc (định luật Little), thời gian tính bằng ms."""
    return _F(rate_per_s) * _F(ms, 1000)
