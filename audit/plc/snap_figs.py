"""Chụp các hình audit/plc/fig/*.svg (hoặc tên chỉ định) thành PNG để xem bằng mắt: snap_figs.py [tên …] → audit/plc/snap/fig_<tên>.png"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
fig = ROOT / "audit" / "plc" / "fig"; dst = ROOT / "audit" / "plc" / "snap"; dst.mkdir(parents=True, exist_ok=True)
names = sys.argv[1:] or sorted(p.stem for p in fig.glob("*.svg"))
css = (ROOT / "tools" / "vendor" / "node_modules" / "katex" / "dist" / "katex.min.css").as_uri()
with sync_playwright() as pw:
    br = pw.chromium.launch(channel="msedge")
    pg = br.new_page(viewport={"width": 900, "height": 600})
    for n in names:
        svg = (fig / f"{n}.svg").read_text(encoding="utf-8")
        pg.set_content(f'<html><head><link rel="stylesheet" href="{css}"></head><body style="margin:20px;background:#fffbeb;'
                       f'font-family:Segoe UI">{svg}</body></html>')
        pg.wait_for_timeout(200)
        out = dst / f"fig_{n}.png"; pg.locator("svg").first.screenshot(path=str(out)); print(out)
    br.close()
