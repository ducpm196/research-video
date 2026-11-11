"""BNX L14 — DDD, cổng API và Open API: thùng token của cổng (phân số đúng, không lệch số thực), cận trên, ngày theo Thông tư 64."""
import datetime as _dt
from fractions import Fraction as _F


def bnx_l14_bucket(rate, cap, times):
    """Số yêu cầu được nhận: thùng đầy `cap` lúc 0, mỗi giây thêm `rate` thẻ (không quá `cap`), mỗi yêu cầu cần 1 thẻ."""
    tok, last, ok = _F(cap), _F(0), 0
    for t in times:
        t = _F(t)
        tok = min(_F(cap), tok + (t - last) * rate)
        last = t
        if tok >= 1:
            tok -= 1
            ok += 1
    return ok


def bnx_l14_bucket_trace(rate, cap, times):
    """[(chỉ số yêu cầu, số thẻ ngay trước yêu cầu, nhận?)] — để màn hình đọc từng bước."""
    tok, last, out = _F(cap), _F(0), []
    for i, t in enumerate(times):
        t = _F(t)
        tok = min(_F(cap), tok + (t - last) * rate)
        last = t
        ok = tok >= 1
        out.append((i, tok, ok))
        if ok:
            tok -= 1
    return out


def bnx_l14_accepted_idx(rate, cap, times):
    return [i for i, _, ok in bnx_l14_bucket_trace(rate, cap, times) if ok]


def bnx_l14_spread(n, seconds=1):
    """n yêu cầu rải đều trong `seconds` giây: thời điểm 0, s/n, 2s/n, …, (n−1)s/n."""
    return [_F(i * seconds, n) for i in range(n)]


def bnx_l14_bound(rate, cap, duration):
    """Cận trên số yêu cầu nhận được trong khoảng [0, duration]: phần nguyên của cap + rate·duration."""
    return int(_F(cap) + _F(rate) * _F(duration))


def bnx_l14_days(d1, d2):
    """Số ngày từ d1 tới d2, ngày dạng 'dd/mm/yyyy'."""
    p = lambda s: _dt.date(*reversed([int(x) for x in s.split("/")]))
    return (p(d2) - p(d1)).days


def bnx_l14_add_days(d, n):
    a = _dt.date(*reversed([int(x) for x in d.split("/")])) + _dt.timedelta(days=n)
    return f"{a.day:02d}/{a.month:02d}/{a.year}"


def bnx_l14_debit(balance, amount):
    """Gốc aggregate Tài khoản giữ bất biến số dư ≥ 0: trả (số dư sau, đã nhận?)."""
    if amount <= 0 or amount > balance:
        return balance, False
    return balance - amount, True
