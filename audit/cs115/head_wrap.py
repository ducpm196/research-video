"""Kiểm dòng đầu trang / tiêu đề phân cảnh có xuống 2 dòng không, trên preview.html đã dựng (không dựng lại video):
mở trang, hiện khung đầu của mỗi phân cảnh, đo chiều cao như phép kiểm headWrap trong player.html.
Chạy: head_wrap.py CS115 [L11 …]   (không ghi tên bài = mọi bài của khoá)"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
course, ids = sys.argv[1], sys.argv[2:]
ids = ids or sorted(p.name for p in (ROOT / "out" / course).glob("L??"))
JS = """() => { const w = el => el.offsetHeight > 1.9 * parseFloat(getComputedStyle(el).fontSize);
  return [w(document.querySelector('header .lesson')), w(document.getElementById('sceneTitle'))]; }"""
bad = 0
with sync_playwright() as pw:
    br = pw.chromium.launch(channel="msedge")
    pg = br.new_page(viewport={"width": 1920, "height": 1080})
    for lid in ids:
        pg.goto((ROOT / "out" / course / lid / "preview.html").as_uri())
        frames = pg.evaluate("DATA.frames.map(f => f.scene_title)")
        seen = set()
        for i, s in enumerate(frames):
            if s in seen:
                continue
            seen.add(s)
            pg.evaluate(f"window.renderFrame ? window.renderFrame({i}) : render({i})")
            head, scene = pg.evaluate(JS)
            if head or scene:
                bad += 1
                print(f"[FAIL] {lid} khung {i} ({s}): " + ("dòng đầu trang 2 dòng " if head else "") + ("tiêu đề phân cảnh 2 dòng" if scene else ""))
                if head:
                    break
    br.close()
print(f"{course}: {len(ids)} bài, {bad} chỗ xuống dòng")
