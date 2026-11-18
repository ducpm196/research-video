"""BNX L12 — Ví điện tử và nộp thuế điện tử: hàm tham chiếu cho `checks:` (chỉ thư viện chuẩn).
Nguồn: [ND52] tài khoản đảm bảo thanh toán không thấp hơn tổng số dư ví; [TT40] 100 triệu đồng/tháng (thứ cấp);
[TT41] một số giao dịch tới 300 triệu đồng/tháng; [TT19] số tham chiếu chứng từ nộp ngân sách — xem audit/bnx/sources.md.
Mọi số tiền là số minh hoạ."""


def bnx_wallet_run(escrow, wallets, journal, cust=None):
    """Chạy nhật ký ví. journal: ("nap", ví, tiền) | ("rut", ví, tiền) | ("chuyen", ví_đi, ví_đến, tiền).
    Trả (tài khoản đảm bảo, dict ví, dict tài khoản khách tại ngân hàng, danh sách bút toán ngân hàng (nợ, có, tiền))."""
    w = dict(wallets)
    c = dict(cust or {})
    bank = []
    for ev in journal:
        kind = ev[0]
        if kind == "nap":
            _, k, amt = ev
            w[k] += amt
            escrow += amt
            c[k] = c.get(k, 0) - amt
            bank.append((f"tiền gửi khách {k}", "đảm bảo thanh toán", amt))
        elif kind == "rut":
            _, k, amt = ev
            if w[k] < amt:
                raise ValueError("ví không đủ tiền")
            w[k] -= amt
            escrow -= amt
            c[k] = c.get(k, 0) + amt
            bank.append(("đảm bảo thanh toán", f"tiền gửi khách {k}", amt))
        elif kind == "chuyen":
            _, a, b, amt = ev
            if w[a] < amt:
                raise ValueError("ví không đủ tiền")
            w[a] -= amt
            w[b] += amt
        else:
            raise ValueError(kind)
    return escrow, w, c, bank


def bnx_invariant(escrow, wallets):
    """Bất biến cuối ngày ([ND52]): tài khoản đảm bảo không thấp hơn tổng số dư ví. Trả (đạt?, tổng ví, phần dư/thiếu)."""
    tot = sum(wallets.values()) if isinstance(wallets, dict) else sum(wallets)
    return escrow >= tot, tot, escrow - tot


def bnx_monthly_limit(txs, limit):
    """Cộng dồn giao dịch trong tháng; giao dịch làm tổng vượt hạn mức bị từ chối (không cộng). Trả [(tiền, nhận?, đã dùng)]."""
    used, out = 0, []
    for t in txs:
        if used + t > limit:
            out.append((t, False, used))
        else:
            used += t
            out.append((t, True, used))
    return out


def bnx_tax_recon(bank, treasury):
    """Đối soát theo số tham chiếu: bank, treasury là dict {số tham chiếu: tiền}.
    Trả dict: khop, chua_sang (ngân hàng có, phía Kho bạc chưa có), lech_tien, thua (phía Kho bạc có, ngân hàng không)."""
    r = {"khop": [], "chua_sang": [], "lech_tien": [], "thua": []}
    for k in sorted(bank):
        if k not in treasury:
            r["chua_sang"].append(k)
        elif treasury[k] != bank[k]:
            r["lech_tien"].append(k)
        else:
            r["khop"].append(k)
    r["thua"] = sorted(k for k in treasury if k not in bank)
    return r


# ── Nâng AF2 (WP4, 2026-11-14): quy mô đối soát và lab ──
def bnx_l12_scan_cmp(n):
    """Đối soát bằng vòng lặp lồng: chứng từ thứ i của ngân hàng nằm ở vị trí i của danh sách Kho bạc nên cần i + 1 phép so sánh;
    tổng 1 + 2 + … + n = n(n+1)/2."""
    return n * (n + 1) // 2


def bnx_l12_lookup_cmp(n):
    """Đối soát bằng bảng tra: mỗi chứng từ tra đúng một lần."""
    return n


def bnx_l12_time_s(phep, ns_moi_phep):
    """Thời gian chờ (giây) nếu mỗi phép mất ns_moi_phep nano giây (số minh hoạ)."""
    return round(phep * ns_moi_phep / 1e9, 9)


def bnx_l12_lab():
    """Lab L12: chạy lại nhật ký có lệnh rút bị từ chối vì ví không đủ tiền. Trả (ví, tổng ví, tài khoản đảm bảo, đạt?)."""
    escrow, w = 250_000, {"X": 0, "Y": 250_000, "Z": 0}
    for ev in [("nap", "X", 3_000_000), ("chuyen", "X", "Z", 1_200_000), ("rut", "Z", 400_000), ("nap", "Y", 500_000),
               ("rut", "Y", 2_000_000), ("chuyen", "Z", "Y", 300_000)]:
        if ev[0] == "rut" and w[ev[1]] < ev[2]:
            continue
        escrow, w, _, _ = bnx_wallet_run(escrow, w, [ev])
    tot = sum(w.values())
    return w, tot, escrow, escrow >= tot
