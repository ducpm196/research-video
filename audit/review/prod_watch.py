"""Theo dõi sản xuất: đọc audit/review/production_log.tsv (mỗi bài một dòng, do build_queue ghi) và log đang ghi dở.
In: bài đang dựng + bước hiện tại + đã chạy bao lâu; thống kê theo khoá (trung vị dựng / asr, số lần bị chặn, giọng);
số bài có đặc tả chưa dựng và thời gian ước tính còn lại (trung vị 10 bài gần nhất).
Chạy: .venv/Scripts/python audit/review/prod_watch.py"""
import csv
import re
import statistics as st
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
LOG = ROOT / "audit" / "review" / "production_log.tsv"

# bài đang dựng: log mới ghi gần nhất
logs = sorted((ROOT / "audit").glob("*/logs/L*.log"), key=lambda p: p.stat().st_mtime)
if logs:
    cur = logs[-1]
    age = time.time() - cur.stat().st_mtime
    lines = [l for l in cur.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
    step = next((l for l in reversed(lines) if l.startswith(("tts", "render", "build", "verify", "asr", "lint", "[FAIL]"))),
                lines[-1] if lines else "(chưa in gì)")
    print(f"Đang ghi: {cur.relative_to(ROOT)} — dòng cuối cách đây {age / 60:.1f} phút: {step[:150]}")

rows = list(csv.DictReader(LOG.open(encoding="utf-8"), delimiter="\t")) if LOG.exists() else []
if not rows:
    print("production_log.tsv chưa có dòng nào (hàng đợi bản 2026-10-30 trở đi mới ghi).")
else:
    # bài dựng lại có nhiều dòng: thống kê theo lần dựng CUỐI của mỗi bài
    by, last_of = {}, {(r["khoá"], r["bài"]): r for r in rows}
    for (c, _), r in last_of.items():
        by.setdefault(c, []).append(r)
    print(f"\n{'khoá':6} {'bài':>4} {'PASS':>4} {'dựng(tv)':>9} {'asr(tv)':>8} {'bị chặn':>7} {'dự phòng':>8}")
    for c, rs in by.items():
        ok = [r for r in rs if r["kết_quả"] == "PASS"]
        b = st.median(int(r["dựng_s"]) for r in rs)
        a = st.median(int(r["asr_s"]) for r in ok) if ok else 0
        blk = sum(int(r["số_lần_dựng"]) > 1 for r in rs)
        fb = sum(r["giọng"] == "dự phòng" for r in rs)
        print(f"{c:6} {len(rs):>4} {len(ok):>4} {b / 60:>8.1f}p {a / 60:>7.1f}p {blk:>7} {fb:>8}")
    # ước tính chỉ từ bài dựng MỚI (≥ một nửa số câu đọc mới); bài dựng lại lấy từ cache nhanh hơn nhiều, làm lệch ước tính
    def fresh(r):
        m = re.match(r"(\d+) câu \((\d+) mới", r["tts"])
        return bool(m) and int(m.group(2)) * 2 >= int(m.group(1))
    last = [r for r in rows if r["kết_quả"] == "PASS" and fresh(r)][-10:]
    per = st.median(int(r["dựng_s"]) + int(r["asr_s"]) for r in last) if last else None

    # bài có đặc tả mà chưa dựng
    todo = [f for c in sorted(p.name for p in (ROOT / "lessons").iterdir() if p.is_dir())
            for f in (ROOT / "lessons" / c).glob("L*_*.yaml")
            if not (ROOT / "out" / c.upper() / f.name.split("_")[0] / "build_report.json").exists()]
    if per:
        print(f"\nTrung vị 10 bài dựng mới gần nhất: {per / 60:.1f} phút/bài. Còn {len(todo)} bài có đặc tả chưa dựng "
              f"→ ước tính {len(todo) * per / 3600:.1f} giờ (chưa tính bài dựng lại).")
    print(f"Dòng cuối: {rows[-1]['kết_thúc']} {rows[-1]['khoá']} {rows[-1]['bài']} {rows[-1]['kết_quả']} — tts: {rows[-1]['tts'][:110]}")
