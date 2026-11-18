"""BNX L30 — Chịu lỗi bằng mã: mô hình tham chiếu của thử lại có lùi (tổng thời gian chờ), cầu dao ba trạng thái với đồng hồ giả, xô token, hệ số khuếch đại
tải khi thử lại. Chỉ thư viện chuẩn, không mạng. Kiểm độc lập ở audit/bnx/ver/l30.py (chạy THẬT Java: bản tự cài và Resilience4j 2.3.0)."""


def bnx_l30_retry(hong, toi_da, goc):
    """Dịch vụ hỏng `hong` lần đầu. Trả (kết quả, tổng chờ ms): chờ goc·2^(lần−1) sau mỗi lần hỏng, trừ lần cuối."""
    cho = 0
    for lan in range(1, toi_da + 1):
        if lan > hong:
            return ("ok", lan, cho)
        if lan == toi_da:
            return ("that bai", toi_da, cho)
        cho += goc * 2 ** (lan - 1)


def bnx_l30_breaker(thoi_diem, hong_toi, nguong=3, cho=1000):
    """Cầu dao ba trạng thái. thoi_diem: danh sách ms gọi; dịch vụ hỏng khi ms ≤ hong_toi. Trả (số cuộc gọi thật, số cuộc bị chặn, trạng thái cuối)."""
    s = {"t": "DONG", "hong": 0, "mo": 0}
    that = chan = 0
    for ms in thoi_diem:
        if s["t"] == "MO":
            if ms - s["mo"] < cho:
                chan += 1
                continue
            s["t"] = "NUA_MO"
        tot = ms > hong_toi
        that += 1
        if s["t"] == "NUA_MO":
            s.update(t="DONG", hong=0) if tot else s.update(t="MO", mo=ms)
        elif tot:
            s["hong"] = 0
        else:
            s["hong"] += 1
            if s["hong"] >= nguong:
                s.update(t="MO", mo=ms)
    return that, chan, s["t"]


def bnx_l30_bucket(dung_tich, nap_moi_giay, dot):
    """Xô token. dot: [(ms, số yêu cầu cùng lúc)]. Trả danh sách số yêu cầu được nhận ở mỗi đợt."""
    thung, truoc, kq = float(dung_tich), 0, []
    for ms, n in dot:
        thung = min(dung_tich, thung + (ms - truoc) / 1000.0 * nap_moi_giay)
        truoc = ms
        ok = 0
        for _ in range(n):
            if thung >= 1:
                thung -= 1
                ok += 1
        kq.append(ok)
    return kq


def bnx_l30_retry_load(n, so_lan_thu_lai):
    """Mọi yêu cầu đều hỏng: mỗi yêu cầu thành 1 + r cuộc gọi tới dịch vụ."""
    return n * (1 + so_lan_thu_lai)


def bnx_l30_vach_qua(cho, giu_giay):
    """Vách ngăn `cho` chỗ, mỗi cuộc giữ tối đa `giu_giay` giây: số yêu cầu mỗi giây tối đa qua được (định luật Little: chỗ / thời gian giữ)."""
    return cho / giu_giay


def bnx_l30_luong_cho(yeu_cau_moi_giay, giu_giay):
    """Số luồng đang chờ cùng lúc nếu mỗi cuộc gọi treo `giu_giay` giây."""
    return yeu_cau_moi_giay * giu_giay
