"""Kiểm độc lập BNX L08 (Elasticsearch) bằng đường KHÁC checklib: (1) chạy nguyên văn các khối Python trên màn hình bằng tiến trình
riêng và so đầu ra với hằng *_OUT; (2) tính lại bằng vòng lặp thuần / phép trừ lặp / mô phỏng sự kiện; (3) đối chiếu alg.bnx_*.
Không chạy Elasticsearch thật (hành vi sản phẩm lấy từ nguồn sources.md [ES1]–[ES4], ghi NOT_VERIFIED ở sổ mã)."""
import binascii
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l08  # noqa: E402


def run_py(code):
    p = subprocess.run([sys.executable, "-X", "utf8", "-I", "-c", code], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout


def mod_by_subtraction(h, n):
    while h >= n:
        h -= n
    return h


def run(rec):
    L = "L08"
    # (1) mã trên màn hình chạy thật, đầu ra khớp hằng hiển thị
    for name in ("INV", "ROUTE", "CRC", "REFRESH"):
        rc, so = run_py(getattr(l08, name + "_PY"))
        rec(L, rc == 0 and so.strip() == getattr(l08, name + "_OUT").strip(), f"khối {name}_PY chạy rc={rc}, đầu ra thật = hằng {name}_OUT trên màn hình")

    # (2a) chỉ mục ngược: quét thô từng (từ, bản ghi) không dùng dict lồng
    docs = l08.DOCS
    words = sorted({w for t in docs.values() for w in t.split()})
    brute = {w: [d for d in sorted(docs) if w in docs[d].split()] for w in words}
    rec(L, brute == alg.bnx_inverted_index(docs), f"chỉ mục ngược quét thô = alg.bnx_inverted_index ({len(words)} từ)")
    rec(L, (brute["tiền"], brute["chuyển"], brute["napas"]) == (["d1", "d2", "d3", "d4"], ["d1", "d3"], ["d1"])
        and sorted(set(brute["chuyển"]) & set(brute["napas"])) == ["d1"] == alg.bnx_search_and(docs, "chuyển", "napas"),
        "tiền → 4 bản ghi, chuyển → d1 d3, napas → d1, giao = [d1]")

    # (2b) định tuyến: phép trừ lặp thay cho %
    rec(L, mod_by_subtraction(17, 3) == 2 == alg.bnx_shard(17, 3) and mod_by_subtraction(17, 4) == 1 == alg.bnx_shard(17, 4),
        "17 mod 3 = 2, 17 mod 4 = 1 (trừ lặp)")
    copies = [f"P{i}" for i in range(3)] + [f"R{i}" for i in range(3)]
    rec(L, len(copies) == 6 == alg.bnx_total_shards(3, 1), "liệt kê P0..P2, R0..R2 = 6 mảnh = alg.bnx_total_shards(3, 1)")
    keep = sum(1 for h in range(1200) if mod_by_subtraction(h, 3) == mod_by_subtraction(h, 4))
    rec(L, keep == 300 and Fraction(keep, 1200) == Fraction(1, 4) == alg.bnx_keep_cycle(3, 4)[2] and alg.bnx_keep_cycle(3, 4)[:2] == (3, 12),
        f"1200 giá trị băm liên tiếp (100 vòng): {keep} giữ mảnh = 25% = 3/12 (alg.bnx_keep_cycle)")
    rec(L, (1200000 - 1200000 * keep // 1200) == 900000 == (1 - alg.bnx_keep_cycle(3, 4)[2]) * 1200000,
        "75% của 1 200 000 = 900 000 bản ghi phải chuyển")

    # (2c) băm thật bằng binascii.crc32 (cài đặt khác zlib.crc32)
    ids = [f"tx{i}" for i in range(1, 1201)]
    s = sum(binascii.crc32(d.encode()) % 3 == binascii.crc32(d.encode()) % 4 for d in ids)
    rec(L, s == 315 == alg.bnx_crc_keep(1200, 3, 4) and f"{s} / 1200 = {round(s / 1200, 3)}" in l08.CRC_OUT,
        f"binascii.crc32 trên tx1..tx1200: {s} giữ mảnh (≈ 26%), khớp alg.bnx_crc_keep và đầu ra màn hình")
    rec(L, all((binascii.crc32(d.encode()) % 6) % 3 == binascii.crc32(d.encode()) % 3 for d in ids) and alg.bnx_split_ok(3, 2),
        "tách 3 → 6: mảnh mới mod 3 = mảnh cũ với mọi mã (split theo bội số)")

    # (2d) làm tươi: mô phỏng sự kiện theo danh sách thời điểm làm tươi tường minh
    refreshes, visible, found = [1.0, 2.0], set(), []
    events = sorted([(0.0, "ghi", "d1"), (0.5, "tìm", None), (1.0, "làm tươi", None), (1.2, "tìm", None)], key=lambda e: e[0])
    buf = []
    for t, kind, d in events:
        if kind == "ghi":
            buf.append(d)
        elif kind == "làm tươi" and t in refreshes:
            visible |= set(buf)
            buf = []
        elif kind == "tìm":
            found.append(len(visible))
    rec(L, found == [0, 1] == alg.bnx_refresh_sim([(0, "d1")], [0.5, 1.2]), "mô phỏng sự kiện: tìm lúc 0,5 s thấy 0, lúc 1,2 s thấy 1")

    # (2e) đáp án đố
    keep56 = sum(1 for h in range(300) if h % 5 == h % 6)
    rec(L, len([1 for _ in range(5) for _ in range(3)]) == 15 == alg.bnx_total_shards(5, 2)
        and (mod_by_subtraction(23, 5), mod_by_subtraction(23, 6)) == (3, 5)
        and Fraction(keep56, 300) == Fraction(1, 6) == alg.bnx_keep_cycle(5, 6)[2] and round(100 * keep56 / 300) == 17,
        "đố: 5·(1+2) = 15; 23 mod 5 = 3, mod 6 = 5; giữ mảnh 5→6 = 1/6 ≈ 17%")

    # (3) bài sinh ra: tiêu đề, mục tiêu nguyên văn giáo án; số trong ví dụ giáo án có trên màn hình
    cur = next(x for x in yaml.safe_load((ROOT / "curriculum" / "bnx.yaml").read_text(encoding="utf-8"))["lessons"] if x["id"] == L)
    spec = yaml.safe_load(next((ROOT / "lessons" / "bnx").glob(f"{L}_*.yaml")).read_text(encoding="utf-8"))
    shows = " ".join(s_["show"] for sc_ in spec["scenes"] for s_ in sc_["steps"])
    rec(L, spec["title"].endswith(cur["title"]) and spec["objectives"] == cur["objectives"], "tiêu đề và mục tiêu chép nguyên văn giáo án")
    rec(L, all(x in shows for x in ("3 mảnh chính", "1 bản sao", "\\hl{6}", "17 \\text{ mod } 3", "\\frac{3}{12}", "25\\%", "tạo chỉ mục mới")),
        "các số của ví dụ giáo án (3 chính, 1 bản sao, 6, mod 3, 3/12 = 25%, tạo chỉ mục mới) có trên màn hình")
