"""BNX L18 — Kiểm thử Java với JUnit 5 và Mockito: hàm phí ba nhánh (số minh hoạ), bốn ca kiểm, đối tượng giả đếm lời gọi, giờ chốt.
Chỉ thư viện chuẩn, không mạng. Kiểm độc lập ở audit/bnx/ver/l18.py (chạy thật JUnit Platform 1.14.4 + Mockito 5.24.0 trên JDK 21)."""

_FREE_BELOW = 500_000      # dưới mốc này: miễn phí
_HIGH_FROM = 10_000_000    # từ mốc này trở lên: phí cao
_FEE_MID, _FEE_HIGH = 5_000, 5_500


def bnx_jt_fee(amount, bug=False):
    """Phí chuyển tiền (số minh hoạ). bug=True: mã trên màn hình viết nhầm `<=` ở mốc 10 triệu."""
    if amount < _FREE_BELOW:
        return 0
    if amount < _HIGH_FROM or (bug and amount == _HIGH_FROM):
        return _FEE_MID
    return _FEE_HIGH


def bnx_jt_fee_branches():
    """Số nhánh của hàm phí = số giá trị trả về khác đường đi: hai mốc cắt trục số thành ba khoảng."""
    return len((_FREE_BELOW, _HIGH_FROM)) + 1


def bnx_jt_fee_cases():
    """Bốn ca kiểm của PhiTest: (tên, số tiền, giá trị mong đợi theo đề)."""
    return [("mienPhi", 200_000, 0), ("phiVua", 2_000_000, 5_000), ("phiCao", 50_000_000, 5_500), ("bien", 10_000_000, 5_500)]


def bnx_jt_fee_run(bug=True):
    """Chạy bốn ca trên hàm phí: (số ca đạt, số ca trượt, [(tên, mong đợi, nhận)] của ca trượt)."""
    bad = [(n, want, bnx_jt_fee(a, bug)) for n, a, want in bnx_jt_fee_cases() if bnx_jt_fee(a, bug) != want]
    return len(bnx_jt_fee_cases()) - len(bad), len(bad), bad


def bnx_jt_transfer(amount, accept=True, bug=False):
    """Dịch vụ chuyển tiền gọi cổng thanh toán với (tài khoản, số tiền + phí). Cổng là đối tượng giả ghi lại lời gọi.
    Trả (phí hoặc 'lỗi' khi cổng từ chối, danh sách lời gọi)."""
    calls = []

    def gate(acc, total):
        calls.append((acc, total))
        return accept

    fee = bnx_jt_fee(amount, bug)
    if not gate("TK01", amount + fee):
        return "lỗi", calls
    return fee, calls


def bnx_jt_before_cutoff(hour, minute, cutoff_hour=22):
    """Lệnh trước giờ chốt (22 giờ, số minh hoạ) thì tính trong ngày."""
    return hour * 60 + minute < cutoff_hour * 60


def bnx_jt_suite_ms(n_fake, n_real, fake_ms=10, real_ms=2000):
    """Thời gian chạy bộ ca kiểm (mili giây, số minh hoạ): ca dùng đối tượng giả và ca gọi cổng thử thật."""
    return n_fake * fake_ms + n_real * real_ms
