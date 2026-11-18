"""BNX L24 — JPA/Hibernate và Spring Data: mô hình tham chiếu của số câu SQL khi đọc quan hệ một–nhiều (tải lười: 1 + N;
nối kèm tải: 1), số dòng một phép nối trả về, độ trễ cộng dồn, số đối tượng một ngữ cảnh bền vững giữ. Chỉ thư viện chuẩn, không mạng.
Kiểm độc lập ở audit/bnx/ver/l24.py (chạy THẬT Hibernate 7.1.0.Final + H2, đếm bằng bộ đếm thống kê, và đếm lại bằng sqlite3 của Python)."""


def bnx_l24_lazy_sql(n):
    """Tải lười: 1 câu lấy n khách + mỗi khách đụng vào danh sách một câu."""
    return 1 + n


def bnx_l24_join_sql(n):
    """Nối kèm tải: một câu nối hai bảng, bất kể n."""
    return 1


def bnx_l24_rows_join(n, per):
    """Số dòng một câu nối trả về: mỗi khách xuất hiện một lần cho mỗi tài khoản."""
    return n * per


def bnx_l24_latency_ms(cau, ms_moi_cau):
    """Các câu chạy lần lượt: thời gian cộng dồn (số minh hoạ)."""
    return cau * ms_moi_cau


def bnx_l24_find_sql(lan_tim_cung_ma):
    """Tìm cùng một mã nhiều lần trong một phiên: chỉ lần đầu chạy SQL (ngữ cảnh bền vững đã giữ đối tượng)."""
    return 1 if lan_tim_cung_ma >= 1 else 0


def bnx_l24_entities_held(khach, tk_moi_khach):
    """Ngữ cảnh giữ mọi đối tượng đã tải: khách + khách × tài khoản mỗi khách."""
    return khach + khach * tk_moi_khach


def bnx_l24_khach_thay(khach, khach_khong_tk, kieu):
    """Số khách còn trong kết quả khi nối kèm tải: nối trong bỏ khách không có tài khoản, nối trái giữ."""
    return khach - khach_khong_tk if kieu == "trong" else khach
