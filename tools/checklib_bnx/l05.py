"""BNX L05 — mTLS: quyết định của máy chủ khi đòi chứng chỉ khách (có chứng chỉ? nơi cấp được tin? còn hạn?) và lịch xoay vòng.
Chỉ thư viện chuẩn; phép bắt tay THẬT (openssl + Python ssl) ở audit/bnx/ver/l05.py."""
import datetime as _dt

# lý do máy chủ ghi khi từ chối, đúng chuỗi in ra trong lần chạy thật (Python 3.13, OpenSSL 3.0)
bnx_l05_server_reason = {"none": "PEER_DID_NOT_RETURN_A_CERTIFICATE", "ca": "unable to get local issuer certificate",
                         "expired": "certificate has expired"}
bnx_l05_client_alert = {"none": "TLSV13_ALERT_CERTIFICATE_REQUIRED", "ca": "TLSV1_ALERT_UNKNOWN_CA", "expired": "SSLV3_ALERT_CERTIFICATE_EXPIRED"}


def bnx_mtls_decision(cert, trusted, now):
    """cert = None hoặc {"cn", "issuer", "not_before", "not_after"} (datetime); trusted = tập nơi cấp máy chủ tin.
    Thứ tự như OpenSSL: không có chứng chỉ → 'none'; nơi cấp không được tin → 'ca'; ngoài hạn → 'expired'; còn lại 'ok'."""
    if cert is None:
        return "none"
    if cert["issuer"] not in trusted:
        return "ca"
    if not (cert["not_before"] <= now <= cert["not_after"]):
        return "expired"
    return "ok"


def bnx_l05_cases(now):
    d = _dt.datetime
    ok = {"cn": "thanh_toan", "issuer": "ca1", "not_before": now - _dt.timedelta(days=1), "not_after": now + _dt.timedelta(days=89)}
    la = dict(ok, cn="la_mat", issuer="ca2")
    cu = {"cn": "het_han", "issuer": "ca1", "not_before": d(2025, 1, 1), "not_after": d(2025, 4, 1)}
    return [bnx_mtls_decision(c, {"ca1"}, now) for c in (None, la, cu, ok)]


def bnx_days_between(a, b):
    """Số ngày từ ngày a tới ngày b (chuỗi YYYY-MM-DD)."""
    return (_dt.date.fromisoformat(b) - _dt.date.fromisoformat(a)).days


def bnx_add_days(a, n):
    return (_dt.date.fromisoformat(a) + _dt.timedelta(days=n)).isoformat()


def bnx_rotate_day(validity_days, num=2, den=3):
    """Xoay vòng khi đã dùng num/den thời hạn (số minh hoạ của bài: 2/3)."""
    return validity_days * num // den


def bnx_rotations_per_year(validity_days, days_per_year=365):
    """Số lần đổi mỗi năm khi xoay ở 2/3 thời hạn (quy tắc của bài): 30 ngày → xoay mỗi 20 ngày → 365 // 20 = 18."""
    return days_per_year // bnx_rotate_day(validity_days)


def bnx_leak_window(validity_days, leak_day):
    """Khoá riêng lộ ở ngày leak_day, không thu hồi: chứng chỉ còn dùng được bao nhiêu ngày."""
    return max(0, validity_days - leak_day)
