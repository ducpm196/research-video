"""BNX L28 — PostgreSQL, MongoDB, MySQL so với Oracle và SQL Server: mô hình tham chiếu của số dòng bị loại khi quét tuần tự so với chỉ mục,
rút tiền có điều kiện (nguyên tử) so với đọc rồi ghi (ghi đè). Chỉ thư viện chuẩn, không mạng.
Kiểm độc lập ở audit/bnx/ver/l28.py (chạy THẬT PostgreSQL 17, MongoDB 8, MySQL 8.4 bằng ảnh Docker chính thức, Oracle/SQL Server trong container có sẵn)."""


def bnx_l28_removed(n, co_chi_muc):
    """Truy vấn bằng đúng một giá trị duy nhất: quét tuần tự đọc hết n dòng và loại n − 1 dòng; quét theo chỉ mục không loại dòng nào."""
    return 0 if co_chi_muc else n - 1


def bnx_l28_withdraw(so_du, cac_lan_rut):
    """Rút có điều kiện (chỉ trừ khi còn đủ): trả (danh sách 1/0 từng lần, số dư cuối). Mỗi lần kiểm và trừ trong MỘT bước nguyên tử."""
    ok = []
    for r in cac_lan_rut:
        if so_du >= r:
            so_du -= r
            ok.append(1)
        else:
            ok.append(0)
    return ok, so_du


def bnx_l28_lost_update(so_du, rut_a, rut_b):
    """Đọc rồi ghi không điều kiện: hai bên cùng đọc so_du, mỗi bên ghi so_du − số rút của mình; bên ghi sau thắng.
    Trả (số dư cuối, số tiền đã chi ra mà không bị trừ)."""
    cuoi = so_du - rut_b
    return cuoi, rut_a + rut_b - (so_du - cuoi)


def bnx_l28_sql_update(so_du, rut):
    """UPDATE tk SET so_du = so_du - rut WHERE id = 1 AND so_du >= rut: (số dòng bị sửa, số dư mới)."""
    return (1, so_du - rut) if so_du >= rut else (0, so_du)
