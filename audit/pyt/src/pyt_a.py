"""Hàm dùng chung cho nửa A của khoá PYT (L00–L06), tránh sửa lib.py dùng chung với nửa B.
t2(sec): như lib.t_show nhưng làm tròn 2 chữ số có nghĩa (1 chữ số làm lệch tỉ lệ: 1,4 s và 0,92 s thành '1 s' và '900 ms')."""
from lib import sig, vi_num


def t2(sec):
    """Số giây → (chữ trên màn hình, chữ đọc) với 2 chữ số có nghĩa: ('≈ 1,4 s', 'khoảng một phẩy bốn giây')."""
    if sec < 1e-6:
        v, u, uv = sig(sec * 1e9, 2), "ns", "phần tỉ giây"
    elif sec < 1e-3:
        v, u, uv = sig(sec * 1e6, 2), "µs", "phần triệu giây"
    elif sec < 1:
        v, u, uv = sig(sec * 1e3, 2), "ms", "phần nghìn giây"
    elif sec < 60:
        v, u, uv = sig(sec, 2), "s", "giây"
    elif sec < 3600:
        v, u, uv = sig(sec / 60, 2), "phút", "phút"
    elif sec < 86400:
        v, u, uv = sig(sec / 3600, 2), "giờ", "giờ"
    else:
        v, u, uv = sig(sec / 86400, 2), "ngày", "ngày"
    return f"≈ {str(v).replace('.', ',')} {u}", f"khoảng {vi_num(v)} {uv}"


def val2(sec):
    """Giá trị số (giây) đúng như chữ t2 hiện ra, để tính tỉ lệ khớp với số trên màn hình."""
    if sec < 1e-6:
        return sig(sec * 1e9, 2) * 1e-9
    if sec < 1e-3:
        return sig(sec * 1e6, 2) * 1e-6
    if sec < 1:
        return sig(sec * 1e3, 2) * 1e-3
    return sig(sec, 2)
