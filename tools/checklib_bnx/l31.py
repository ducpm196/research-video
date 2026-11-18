"""BNX L31 — Quan sát hệ thống: mô hình tham chiếu của dựng đường đi từ nhật ký (mã tương quan), chi phí chỉ mục đảo (đếm dòng), tỉ lệ lỗi, tốc độ đốt ngân sách
lỗi, số chuỗi và dung lượng văn bản chỉ số theo nhãn. Chỉ thư viện chuẩn, không mạng, không Docker. Kiểm độc lập ở audit/bnx/ver/l31.py
(chạy THẬT Python, Java, Prometheus 3.16.0 qua ảnh Docker chính thức)."""
from fractions import Fraction


def bnx_l31_demo():
    """Sáu dòng nhật ký của ví dụ (đồng hồ giả: 1000, 1007, … mili giây)."""
    return [(1000, "cong", "a1", "nhan"), (1007, "cong", "b2", "nhan"), (1014, "tt", "a1", "tru-tien"),
            (1021, "tt", "b2", "doc-so-du"), (1028, "sc", "a1", "loi"), (1035, "cong", "a1", "tra")]


def bnx_l31_path(events, cid):
    """Lọc theo cid, sắp theo t: trả (danh sách 'dv:ev', thời gian từ đầu tới cuối ms)."""
    dong = sorted((e for e in events if e[2] == cid), key=lambda e: e[0])
    return [f"{e[1]}:{e[3]}" for e in dong], dong[-1][0] - dong[0][0]


def bnx_l31_index(n):
    """n dòng; dòng i thuộc dịch vụ i % 5 (2 = sc); ERROR khi i % 1000 ∈ {7, 8}. Trả (số dòng ERROR của sc, số dòng ERROR, n)."""
    err = sum(1 for i in range(n) if i % 1000 in (7, 8))
    khop = sum(1 for i in range(n) if i % 1000 in (7, 8) and i % 5 == 2)
    return khop, err, n


def bnx_l31_ratio(loi, tong):
    return loi / tong


def bnx_l31_burn(ty_le, slo):
    """Tốc độ đốt = tỉ lệ lỗi / (1 − SLO), tính bằng Fraction để khỏi sai số thập phân."""
    return float(Fraction(str(ty_le)) / (1 - Fraction(str(slo))))


def bnx_l31_days(burn, ky=30):
    """Số ngày cạn ngân sách của kỳ `ky` ngày với tốc độ đốt `burn` không đổi."""
    return ky / burn


def bnx_l31_budget_min(slo, phut=43200):
    return float(phut * (1 - Fraction(str(slo))))


def bnx_l31_exposition(nguoi):
    """Văn bản chỉ số như XuatChiSo.java: trả (số dòng chỉ số không phải chú thích, số byte)."""
    duong, ma, so = ["/chuyen", "/so-du"], ["200", "500"], [[980, 20], [4990, 10]]
    s = "# HELP http_requests_total So yeu cau da nhan.\n# TYPE http_requests_total counter\n"
    for d in range(2):
        for c in range(2):
            nhan = f'route="{duong[d]}",code="{ma[c]}"'
            if nguoi == 0:
                s += "http_requests_total{" + nhan + "} " + str(so[d][c]) + "\n"
            else:
                for u in range(1, nguoi + 1):
                    s += "http_requests_total{" + nhan + f',user="u{u}"' + "} 1\n"
    s += "# TYPE dang_xu_ly gauge\ndang_xu_ly 3\n"
    return sum(1 for l in s.split("\n") if l and not l.startswith("#")), len(s.encode())
