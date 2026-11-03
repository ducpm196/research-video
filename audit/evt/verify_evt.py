"""Kiểm độc lập mọi khẳng định của khoá EVT — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Kết nối: đếm cặp bằng itertools. Lược đồ: mã hoá/giải mã JSON thật với bộ đọc tự cài. Kênh thư chết, tồn đọng, xả, đuổi kịp: mô phỏng từng giây (từng ngày).
Phiên bản: mọi hoán vị thứ đến. Gấp: itertools.accumulate. Giao dịch dài: máy trạng thái tự cài có nhật ký. Nối cửa sổ: vòng lặp đôi. Độ trễ: mô phỏng
sự kiện rời rạc theo thời điểm hoàn thành. Chạy: .venv/Scripts/python audit/evt/verify_evt.py"""
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: đếm cặp ──
pairs = lambda n: len(list(itertools.combinations(range(n), 2)))
rec("L00", pairs(10) == 45 == alg.point_to_point_links(10) and pairs(11) - pairs(10) == 10 and pairs(6) == 15,
    "itertools: 10 dịch vụ 45 cặp, thêm thứ 11 thêm 10; 6 dịch vụ 15")


# ── L01: JSON thật + bộ đọc tự cài ──
def decode(raw, schema):
    obj = json.loads(raw)
    out = {}
    for f, (req, d) in schema.items():
        if f in obj:
            out[f] = obj[f]
        elif req:
            raise KeyError(f)
        else:
            out[f] = d
    return out


def compat(old, new):
    def ok(writer, reader):
        raw = json.dumps({f: (1 if req else d) for f, (req, d) in writer.items()})
        try:
            decode(raw, reader)
            return True
        except KeyError:
            return False
    return ok(old, new), ok(new, old)


V1 = {"ma": (True, None), "tien": (True, None)}
cases = [({**V1, "ghi_chu": (False, "")}, (True, True)), ({**V1, "kenh": (True, None)}, (False, True)),
         ({"ma": (True, None)}, (True, False)), ({**V1, "kenh": (False, "web")}, (True, True))]
Rq = alg.REQUIRED
conv = lambda s: {f: (Rq if req else d) for f, (req, d) in s.items()}
rec("L01", all(compat(V1, n) == exp == alg.schema_compat(conv(V1), conv(n)) for n, exp in cases)
    and compat({**V1, "ghi_chu": (False, "")}, V1) == (True, True), "JSON thật: thêm tuỳ chọn hai chiều; thêm bắt buộc chỉ xuôi; xoá bắt buộc chỉ ngược; thêm có mặc định hai chiều")


# ── L02: mô phỏng người tiêu thụ từng lần thử ──
def sim_dlq(n, poison, k=None, cap=100000):
    i, done, dlq, tries = 1, 0, 0, 0
    while i <= n and tries < cap:
        attempts = 0
        while True:
            tries += 1
            attempts += 1
            if i not in poison:
                done += 1
                break
            if k is not None and attempts >= k:
                dlq += 1
                break
            if tries >= cap:
                return done, dlq, None
        i += 1
    return done, dlq, tries


rec("L02", sim_dlq(1000, {10}, 3) == (999, 1, 1002) == alg.consume_with_dlq(1000, {10}, 3) and sim_dlq(1000, {10})[:2] == (9, 0) and sim_dlq(1000, {10})[2] is None
    and sim_dlq(500, {7, 300}, 5) == (498, 2, 508) == alg.consume_with_dlq(500, {7, 300}, 5) and sim_dlq(500, {7, 300})[:2] == (6, 0),
    "mô phỏng: kẹt ở 9; thử 3 lần → 999 + 1, 1002 lần thử; câu hỏi 498, 2, 508; không kênh thư chết kẹt ở 6")


# ── L03: mọi hoán vị thứ đến ──
ups = [(1, "A"), (2, "B"), (3, "C")]
guard_ok = all(alg.apply_versioned(list(p)) == (3, "C") for p in itertools.permutations(ups + [(3, "C")]))
blind_wrong = sum(alg.apply_versioned(list(p), guard=False) != (3, "C") for p in itertools.permutations(ups))
rec("L03", guard_ok and blind_wrong == 4 and alg.apply_versioned([(1, 'A'), (3, 'C'), (2, 'B')], guard=False) == (2, "B")
    and alg.apply_versioned([(2, 'X'), (1, 'W'), (4, 'Z'), (3, 'Y')]) == (4, "Z"),
    "mọi hoán vị (kể cả trùng): có phiên bản luôn giữ C; ghi đè mù sai ở 4/6 thứ tự; câu hỏi Z")

# ── L04: accumulate + ảnh chụp thật ──
ev = [100, -30, 50, -20]
rng_ev = [((i * 7919) % 201) - 100 for i in range(10**6)]
snap = {i: s for i, s in enumerate(itertools.accumulate(rng_ev), 1) if i % 1000 == 0}
worst = max(n - max((k for k in snap if k <= n), default=0) for n in range(10**6 - 2000, 10**6 + 1))
rec("L04", list(itertools.accumulate(ev)) == [100, 70, 120, 100] and worst == 999 == alg.replay_cost(10**6, 1000)
    and snap[10**6] == sum(rng_ev) and list(itertools.accumulate([200, -50, -80, 30, 80]))[-2:] == [100, 180] and alg.replay_cost(50000, 500) == 499,
    "accumulate: 100, 70, 120, 100; ảnh chụp mỗi 1000 → phát lại tối đa 999; ảnh khớp tổng; bù trừ 80 → 180; câu hỏi 499")


# ── L05, L08: mô phỏng từng giây ──
def sim_backlog(inp, out, secs, backlog=0):
    for _ in range(secs):
        backlog = max(0, backlog + inp - out)
    return backlog


def sim_drain(backlog, inp, out):
    t = 0
    while backlog > 0:
        backlog = max(0, backlog + inp - out)
        t += 1
    return t


def oldest_age(inp, out, secs):
    processed = out * secs
    return secs - processed / inp


rec("L05", sim_backlog(500, 400, 600) == 60000 == alg.consumer_lag(500, 400, 600) and sim_drain(60000, 0, 400) == 150
    and sim_backlog(800, 600, 300) == 60000 and sim_drain(60000, 0, 600) == 100,
    "mô phỏng giây: 60 000 sau 10 phút; dừng ghi → đuổi kịp 150 s; câu hỏi 60 000, 100 s")
rec("L08", sim_backlog(1200, 1000, 3600) == 720000 and sim_drain(720000, 1200, 1500) == 2400 == alg.drain_seconds(720000, 1200, 1500)
    and oldest_age(1200, 1000, 3600) == 600 and 720000 / 1500 == 480 and sim_backlog(500, 400, 1800) == 180000 and sim_drain(180000, 500, 600) == 1800
    and oldest_age(500, 400, 1800) == 360, "mô phỏng giây: tồn 720 000, sự kiện cũ nhất chờ 600 s, xả 2400 s (không phải 480); câu hỏi 180 000, 360 s, 1800 s")


# ── L06: máy trạng thái có nhật ký ──
def run_saga(steps, fail_name):
    log, undo = [], []
    for name, comp in steps:
        if name == fail_name:
            log.append(("lỗi", name))
            while undo:
                log.append(("bù", undo.pop()))
            break
        log.append(("làm", name))
        if comp:
            undo.append(comp)
    return [n for a, n in log if a == "làm"], [n for a, n in log if a == "bù"]


S1 = [("giữ hàng", "nhả hàng"), ("trừ tiền", "hoàn tiền"), ("giao", None)]
S2 = [("đặt phòng", "huỷ phòng"), ("đặt vé", "huỷ vé"), ("trừ tiền", "hoàn tiền"), ("gửi thư", None)]
rec("L06", run_saga(S1, "giao") == alg.saga_run(S1, 2) == (["giữ hàng", "trừ tiền"], ["hoàn tiền", "nhả hàng"]) and run_saga(S2, "trừ tiền") == alg.saga_run(S2, 2) == (["đặt phòng", "đặt vé"], ["huỷ vé", "huỷ phòng"]),
    "máy trạng thái: bù trừ hoàn tiền rồi nhả hàng; câu hỏi huỷ vé rồi huỷ phòng")


# ── L07: vòng lặp đôi ──
def join2(imps, clicks, w):
    return [(k, t) for k, t in clicks for k2, t2 in imps if k == k2 and 0 <= t - t2 <= w]


imps = [("a", 0), ("b", 1), ("c", 2), ("d", 3), ("e", 4)]
clk = [("a", 3), ("b", 13), ("d", 10)]
rec("L07", join2(imps, clk, 10) == alg.window_join(dict(imps), clk, 10) == [("a", 3), ("d", 10)] and len(join2(imps, clk, 15)) == 3
    and join2([("x", 5), ("y", 8)], [("x", 4), ("x", 9), ("y", 20), ("z", 9)], 10) == [("x", 9)] and 2 / 5 == 0.4,
    "vòng lặp đôi: 2 cặp (12 phút bị loại), cửa sổ 15 thì 3; câu hỏi chỉ x lúc 9; tỉ lệ 40%")


# ── L09: mô phỏng từng ngày (bước 0,5 ngày) ──
def catch_up(backlog_days, k, step=0.5):
    pos, now, t = 0.0, backlog_days, 0.0
    while pos < now - 1e-9:
        pos += k * step
        now += step
        t += step
    return t


rec("L09", catch_up(30, 5) == 7.5 == alg.drain_seconds(30, 1, 5) and 30 / 5 == 6 and catch_up(30, 2) == 30 and catch_up(14, 3) == 7 == alg.drain_seconds(14, 1, 3),
    "mô phỏng ngày: 30 ngày gấp 5 → 7,5 ngày (6 chỉ là phần tồn); gấp 2 → 30 ngày; câu hỏi 14 ngày gấp 3 → 7")


# ── L10: mô phỏng thời điểm hoàn thành ──
def finish_time(seq):
    t = 0
    for stage in seq:
        branches = stage if isinstance(stage, list) else [stage]
        t = max(t + b for b in branches)
    return t


rec("L10", finish_time([10, [20, 50], 30]) == 90 == alg.e2e_latency([10, [20, 50], 30]) and sum([10, 20, 50, 30]) == 110
    and finish_time([10, [5, 50], 30]) == 90 and finish_time([10, [20, 30], 30]) == 70 and finish_time([5, [15, 40, 25], 10, [8, 12]]) == 67,
    "thời điểm hoàn thành: 90 ms (không phải 110); sửa B không đổi, sửa C còn 70; câu hỏi 67")

# ── L11: bài hành trình — tính lại bằng đường khác (đếm giây, đếm ngày theo lịch, liệt kê nút còn sống) ──
import datetime  # noqa: E402

day_s = 24 * 60 * 60
avg11 = 10**9 / day_s
avg15 = 800 * 10**9 / day_s
kept = lambda n, dead: n - dead >= n // 2 + 1  # còn đủ đa số?
survive = lambda n: max(k for k in range(n + 1) if kept(n, k))
days = sum(1 for k in range((datetime.date(2025, 3, 18) - datetime.date(2019, 10, 30)).days))
cal = sum(366 if (y % 4 == 0 and (y % 100 or y % 400 == 0)) else 365 for y in range(2020, 2025)) + \
    (datetime.date(2025, 3, 18) - datetime.date(2024, 10, 30)).days
rec("L11", round(avg11) == 11574 and abs(11574 * day_s - 10**9) < day_s
    and sum([200] * 400_000) * 8 == 640_000_000 and 400_000 / 50_000 == 8
    and [f + 1 for f in (1, 2)] == [2, 3] and [2 * f + 1 for f in (1, 2)] == [3, 5]
    and round(avg15 / 1e6, 2) == 9.26 and round(13e6 / avg15, 1) == 1.4 and round(650 / 175, 1) == 3.7
    and abs(175e12 / 800e9 - 2.75e9 / 13e6) < 10
    and [survive(n) for n in (3, 4, 5)] == [1, 1, 2]
    and days == cal == 1966 and 1_000_000 // 2_000 == 500
    and round(1000 * 1000 * day_s * 7 * 2 / 1e9, 1) == 1209.6 and round(1000 * 1000 * day_s * 30 * 2 / 1e9, 1) == 5184.0,
    "1 tỉ tin/ngày ≈ 11 574/giây; gộp 50 gấp 8, 640 triệu bit/giây; F + 1 so với 2F + 1; 800 tỉ/ngày ≈ 9,26 triệu/giây, đỉnh 1,4 lần, đọc 3,7 lần; "
    "cỡ tin hai đường ≈ 219/212 byte; đa số 3→1, 4→1, 5→2; 30/10/2019 → 18/3/2025 = 1966 ngày (lịch năm nhuận); quiz 1209,6 / 5184 GB")

bad = [c for c, ok in R if not ok]
print(f"\nverify_evt: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
