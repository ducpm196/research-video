"""BNX L33 — Hệ cũ: Servlet, JSP, Tomcat, JBoss. Mô hình tham chiếu của bể luồng: số lượt chờ (n yêu cầu cùng lúc, L luồng) và thông lượng tối đa
(L luồng, mỗi yêu cầu t giây). Chỉ thư viện chuẩn, không mạng, không Docker. Kiểm độc lập ở audit/bnx/ver/l33.py (chạy THẬT Tomcat nhúng 10.1.61)."""
import math


def bnx_l33_waves(n, luong):
    """Số lượt xử lý khi n yêu cầu cùng lúc và bể `luong` luồng: ⌈n / luong⌉."""
    return math.ceil(n / luong)


def bnx_l33_throughput(luong, t):
    """Thông lượng tối đa mỗi giây của bể `luong` luồng khi mỗi yêu cầu mất t giây."""
    return luong / t
