"""BNX L34 — Hệ thống phê duyệt tín dụng: máy trạng thái hồ sơ, người có quyền duyệt theo TỔNG dư nợ, số dòng phải đọc khi tra lịch sử (có/không chỉ mục).
Mọi ngưỡng là số minh hoạ của bài. Chỉ thư viện chuẩn, không mạng. Kiểm độc lập ở audit/bnx/ver/l34.py (chạy THẬT Python + sqlite: máy trạng thái, đồng ý, đếm dòng đọc)."""

CANH = {("KHOI_TAO", "THAM_DINH"), ("THAM_DINH", "CHAM_DIEM"), ("THAM_DINH", "TU_CHOI"), ("CHAM_DIEM", "CHO_DUYET"),
        ("CHO_DUYET", "DA_DUYET"), ("CHO_DUYET", "TU_CHOI"), ("DA_DUYET", "GIAI_NGAN")}

BAC = {"CN": [(100, "chuyen vien"), (500, "truong phong"), (None, "hoi dong")],
       "DN": [(2000, "truong phong"), (10000, "giam doc khoi"), (None, "hoi dong")]}
HANG = {"chuyen vien": 1, "truong phong": 2, "giam doc khoi": 3, "hoi dong": 4}


def bnx_l34_hop_le(tu, den):
    """Cạnh (tu → den) có trong bảng cho phép không."""
    return (tu, den) in CANH


def bnx_l34_nguoi_duyet(loai, du_no, moi):
    """(tổng, vai trò cần) theo bậc của loại hồ sơ, tính trên TỔNG dư nợ hiện có + khoản mới (triệu đồng)."""
    tong = du_no + moi
    for tran, vai in BAC[loai]:
        if tran is None or tong <= tran:
            return tong, vai


def bnx_l34_duoc_duyet(nguoi_tao, nguoi_duyet, vai_duyet, can):
    """Khác người tạo và hạng vai trò đủ cao."""
    return nguoi_tao != nguoi_duyet and HANG[vai_duyet] >= HANG[can]


def bnx_l34_doc(n, co_chi_muc, moi_khach=5):
    """Số dòng phải đọc để lấy các dòng của MỘT khách: quét toàn bảng đọc n dòng; có chỉ mục chỉ đọc các dòng của khách."""
    return moi_khach if co_chi_muc else n


def bnx_l34_con_han(het_han, ngay):
    """Đồng ý còn hiệu lực khi ngày hết hạn >= ngày tra (chuỗi ISO so theo thứ tự chữ cái)."""
    return het_han >= ngay


def bnx_l34_canh():
    """Tập cạnh (từ, đến) được phép."""
    return set(CANH)
