"""BNX L25 — Giao dịch Spring và AOP: mô hình tham chiếu của luật hoàn tác mặc định, kết quả số dư/nhật ký của bốn ca, mức cô lập đọc lại,
số kết nối tối thiểu của bể khi có giao dịch riêng. Chỉ thư viện chuẩn, không mạng.
Kiểm độc lập ở audit/bnx/ver/l25.py (chạy THẬT Spring 7.0.10 + H2, JDBC thuần cho mức cô lập, bể kết nối tự viết cho phần quy mô)."""

_CHECKED = {"Exception", "IOException", "SQLException"}


def bnx_l25_rolls_back(loi, rollback_for=()):
    """Luật mặc định của Spring: lỗi không kiểm tra (lớp con RuntimeException) và Error hoàn tác; lỗi kiểm tra chốt, trừ khi khai rollbackFor."""
    if loi is None:
        return False
    if loi == "Error" or loi.endswith("Error"):
        return True
    if loi not in _CHECKED and loi.endswith("Exception"):
        return True
    return loi in rollback_for or ("Exception" in rollback_for and loi in _CHECKED)


def bnx_l25_balance(so_du, tru, hoan_tac):
    """Số dư sau một lần chuyển có lỗi: hoàn tác thì nguyên, chốt thì bị trừ."""
    return so_du if hoan_tac else so_du - tru


def bnx_l25_log_rows(lan_truyen):
    """Số dòng nhật ký còn sau khi nghiệp vụ hỏng: REQUIRED chung số phận (0), REQUIRES_NEW chốt riêng (1)."""
    return {"REQUIRED": 0, "REQUIRES_NEW": 1}[lan_truyen]


def bnx_l25_isolation_reread(muc, dau, tang):
    """Lần đọc thứ hai của A sau khi B cộng `tang` và chốt."""
    return dau + tang if muc == "READ_COMMITTED" else dau


def bnx_l25_pool_min(luong):
    """Hướng dẫn Spring: bể vượt số luồng đồng thời ít nhất 1 khi dùng REQUIRES_NEW."""
    return luong + 1


def bnx_l25_timeouts(luong, be):
    """Mọi luồng giữ giao dịch ngoài rồi xin giao dịch riêng: bể ≤ luồng thì không còn kết nối trống, mọi luồng hết giờ; bể > luồng thì không ai."""
    return luong if be <= luong else 0
