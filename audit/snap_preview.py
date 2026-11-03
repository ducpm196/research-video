"""Chụp khung từ preview.html (chưa cần dựng video) để xem bằng mắt: snap_preview.py OSY L02 [khung …] → audit/<khoá>/snap/<id>_<khung>.png
Không ghi khung → chụp khung cuối của mỗi cảnh."""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
course, lid = sys.argv[1].upper(), sys.argv[2]
want = [int(a) for a in sys.argv[3:]]
page = ROOT / "out" / course / lid / "preview.html"
dst = ROOT / "audit" / course.lower() / "snap"; dst.mkdir(parents=True, exist_ok=True)
with sync_playwright() as pw:
    br = pw.chromium.launch(channel="msedge")
    pg = br.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(page.as_uri()); pg.evaluate("document.body.classList.remove('preview')")
    frames = pg.evaluate("DATA.frames.map(f => f.scene_title)")
    if not want:
        want = [i for i in range(len(frames)) if i + 1 == len(frames) or frames[i + 1] != frames[i]]
    for i in want:
        pg.evaluate(f"renderFrame({i})"); pg.wait_for_timeout(250)
        out = dst / f"{lid}_{i:03d}.png"; pg.screenshot(path=str(out)); print(out)
    br.close()
