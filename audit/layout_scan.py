"""Quét lỗi bố cục trên preview.html của MỌI khung (không cần dựng video): sinh lại preview từ bài, mở bằng trình duyệt, gọi
renderFrame(i) rồi layoutIssues() (player.html) — chồng phần, công thức tràn, viền nhấn đè chữ. In tổng theo loại và các khung lỗi.
Chạy: layout_scan.py CS115 [L01 …] [--no-preview]  → audit/layout_<khoá>.tsv (bài, khung, lỗi)"""
import subprocess
import sys
from collections import Counter
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
course = sys.argv[1]
ids = [a for a in sys.argv[2:] if a.startswith("L")]
lessons = sorted((ROOT / "lessons" / course.lower()).glob("L??_*.yaml"))
lessons = [p for p in lessons if not ids or p.name[:3] in ids]
if "--no-preview" not in sys.argv:
    for p in lessons:
        subprocess.run([str(ROOT / ".venv" / "Scripts" / "python.exe"), str(ROOT / "tools" / "lv.py"), "preview", str(p)],
                       cwd=ROOT, capture_output=True)
rows, kinds, frames_total, frames_bad = [], Counter(), 0, 0
with sync_playwright() as pw:
    br = pw.chromium.launch(channel="msedge")
    pg = br.new_page(viewport={"width": 1920, "height": 1080})
    for p in lessons:
        lid = p.name[:3]
        pg.goto((ROOT / "out" / course / lid / "preview.html").as_uri())
        pg.evaluate("document.body.classList.remove('preview')")
        n = pg.evaluate("DATA.frames.length")
        for i in range(n):
            st = pg.evaluate(f"renderFrame({i})")
            iss = list(st.get("layout") or []) + (["tràn-bảng: nội dung vượt khung"] if st["overflow"] else []) \
                + (["phụ-đề: tràn"] if st["capOverflow"] else []) + (["tiêu-đề: xuống dòng"] if st.get("headWrap") else [])
            frames_total += 1
            if iss:
                frames_bad += 1
                for s in iss:
                    kinds[s.split(":")[0]] += 1
                    rows.append(f"{lid}\t{i}\t{s}")
    br.close()
out = ROOT / "audit" / f"layout_{course}.tsv"
out.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"{course}: {len(lessons)} bài, {frames_total} khung, {frames_bad} khung có lỗi bố cục; theo loại: {dict(kinds)} → {out}")
