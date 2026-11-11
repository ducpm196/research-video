"""Kiểm độc lập BNX L09 (Couchbase) bằng đường KHÁC checklib: (1) chạy nguyên văn các khối Python trên màn hình bằng tiến trình riêng;
(2) CRC32 tự cài theo từng bit (không dùng zlib), thùng ảo bằng phép AND 1023; kho CAS viết lại kiểu khác (vòng thử lại tổng quát);
liệt kê thứ tự bằng đệ quy thay cho permutations; giờ hết hạn bằng datetime; (3) đối chiếu alg.bnx_*. Không chạy Couchbase thật."""
import datetime as dt
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l09  # noqa: E402


def run_py(code):
    p = subprocess.run([sys.executable, "-X", "utf8", "-I", "-c", code], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout


def crc32_bitwise(data):
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (0xEDB88320 if crc & 1 else 0)
    return crc ^ 0xFFFFFFFF


class CasStore:
    """Kho kiểu khác: lưu (giá trị, phiên bản) trong một bộ, ghi bằng compare_and_set trả True/False."""

    def __init__(self, v, ver):
        self.state = (v, ver)

    def compare_and_set(self, expect_ver, new_v):
        v, ver = self.state
        if ver != expect_ver:
            return False
        self.state = (new_v, ver + 1)
        return True


def story(start, ver, adds, use_cas):
    s = CasStore(start, ver)
    snaps = {p: s.state for p, _ in adds}          # mọi tiến trình đọc trước
    rejected = []
    for p, a in adds:
        v0, ver0 = snaps[p]
        if not use_cas:
            s.state = (v0 + a, s.state[1] + 1)      # ghi đè mù
            continue
        while not s.compare_and_set(ver0, v0 + a):  # vòng thử lại: đọc lại rồi ghi
            rejected.append(p)
            v0, ver0 = s.state
    return s.state, rejected


def orders(counts, prefix=()):
    if not any(counts.values()):
        yield prefix
        return
    for p in sorted(counts):
        if counts[p]:
            counts[p] -= 1
            yield from orders(counts, prefix + (p,))
            counts[p] += 1


def finals(use_cas):
    out = set()
    od = list(orders({"P1": 2, "P2": 2}))
    for o in od:
        s, seen = CasStore(100, 7), {}
        for p in o:
            if p not in seen:
                seen[p] = s.state
                continue
            v0, ver0 = seen[p]
            add = {"P1": 50, "P2": 30}[p]
            if use_cas:
                while not s.compare_and_set(ver0, v0 + add):
                    v0, ver0 = s.state
            else:
                s.state = (v0 + add, s.state[1] + 1)
        out.add(s.state[0])
    return len(od), sorted(out)


def run(rec):
    L = "L09"
    # (1) mã trên màn hình chạy thật
    for name, pre in (("KEY", ""), ("USE", l09.STORE_PY), ("INTER", "")):
        rc, so = run_py(pre + getattr(l09, name + "_PY"))
        rec(L, rc == 0 and so.strip() == getattr(l09, name + "_OUT").strip(), f"khối {name}_PY chạy rc={rc}, đầu ra thật = hằng {name}_OUT trên màn hình")

    # (2a) CRC32 tự cài từng bit, thùng ảo = AND 1023 (10 bit cuối)
    h = crc32_bitwise(l09.KEY.encode())
    rec(L, h == 2170508415 == alg.bnx_crc32(l09.KEY), f"CRC32 từng bit của {l09.KEY} = {h} (khớp alg.bnx_crc32)")
    vb = ((h >> 16) & 0x7FFF) & (1024 - 1)        # đúng biểu thức của KeyValueLocator.partitionForKey (Java SDK)
    vb128 = ((h >> 16) & 0x7FFF) & (128 - 1)
    rec(L, vb == 351 == alg.bnx_vbucket(l09.KEY) and vb128 == 95 == alg.bnx_vbucket(l09.KEY, 128)
        and h // 65536 == 33119 and 1024 // 4 == 256 and 256 <= vb <= 511,
        "thùng ảo theo phép bit của thư viện Java: 1024 thùng → 351, 128 thùng → 95 (khớp alg.bnx_vbucket viết bằng phép chia); 351 ở máy 2 (256–511)")
    q1 = ((10 ** 9 >> 16) & 0x7FFF) & 1023
    rec(L, q1 == 922 == alg.bnx_vbucket_of_crc(10 ** 9) and 10 ** 9 // 65536 == 15258, "đố câu 1: CRC32 = 1 000 000 000 → 15 258 → thùng 922")

    # (2b) CAS: kho kiểu khác + vòng thử lại tổng quát
    st, rej = story(100, 7, (("P1", 50), ("P2", 30)), True)
    st0, _ = story(100, 7, (("P1", 50), ("P2", 30)), False)
    ref = alg.bnx_cas_story()
    rec(L, st == (180, 9) == ref[:2] and rej == ["P2"] and ref[2][1] == ("P2", "từ chối"),
        "có CAS: P1 ghi, P2 bị từ chối đúng một lần, đọc lại rồi ghi → 180, CAS 9 (mô phỏng), khớp alg.bnx_cas_story")
    rec(L, st0[0] == 130 == alg.bnx_cas_story(use_cas=False)[0] and st[0] - st0[0] == 50,
        "không CAS: ghi đè còn 130, mất 50 điểm")
    q, _ = story(200, 12, (("P1", -40), ("P2", 25)), True)
    q0, _ = story(200, 12, (("P1", -40), ("P2", 25)), False)
    rec(L, q[0] == 185 and q0[0] == 225 and alg.bnx_cas_story(200, 12, (("P1", -40), ("P2", 25)))[:2] == (185, 14),
        "đố câu 2: có CAS 185, không CAS 225")

    # (2c) mọi thứ tự, liệt kê đệ quy
    rec(L, finals(True) == (6, [180]) == alg.bnx_interleavings(True) and finals(False) == (6, [130, 150, 180]) == alg.bnx_interleavings(False),
        "đệ quy 6 thứ tự: có CAS luôn 180; không CAS ∈ {130, 150, 180}")

    # (2d) hạn sống bằng datetime; quy tắc ghi lại mất hạn sống (nguồn [CB3])
    t = dt.datetime(2026, 1, 5, 9, 0, 0) + dt.timedelta(seconds=1800)
    rec(L, (t.hour, t.minute, t.second) == (9, 30, 0) == alg.bnx_clock_add(9, 0, 0, 1800), "9:00:00 + 1800 giây = 9:30:00")
    rec(L, alg.bnx_ttl_after_mutation(1800, False) == 0 and alg.bnx_ttl_after_mutation(1800, True) == 1800
        and alg.bnx_ttl_after_mutation(1800, False, True) == 1800, "ghi không đặt hạn sống → 0; đặt lại hoặc preserve_expiry → giữ")

    # (3) bài sinh ra
    cur = next(x for x in yaml.safe_load((ROOT / "curriculum" / "bnx.yaml").read_text(encoding="utf-8"))["lessons"] if x["id"] == L)
    spec = yaml.safe_load(next((ROOT / "lessons" / "bnx").glob(f"{L}_*.yaml")).read_text(encoding="utf-8"))
    shows = " ".join(s_["show"] for sc_ in spec["scenes"] for s_ in sc_["steps"])
    rec(L, spec["title"].endswith(cur["title"]) and spec["objectives"] == cur["objectives"], "tiêu đề và mục tiêu chép nguyên văn giáo án")
    rec(L, all(x in shows for x in ("CAS = 7", "từ chối", "100 + 50 + 30 = 180", "số minh hoạ")),
        "ví dụ giáo án có trên màn hình: CAS = 7, P2 bị từ chối, đọc lại rồi ghi, 100 + 50 + 30 = 180, ghi số minh hoạ")
