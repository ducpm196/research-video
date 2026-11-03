"""Ghép 4 khung bất kỳ của CS115 (1920×1080) thành ảnh 2×2 để xem nhanh: sheet.py ten L11:0 L23:0 L39:0 L21:0
→ audit/cs115/sheets/ten.png. Chỉ để duyệt bố cục; chữ nhỏ vẫn mở khung gốc."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
name, picks = sys.argv[1], sys.argv[2:6]
sheet = Image.new("RGB", (1920, 1080), "white")
for k, s in enumerate(picks):
    lid, i = s.split(":")
    c, lid = (lid.split("/") if "/" in lid else ("CS115", lid))
    im = Image.open(ROOT / "out" / c / lid / "frames" / f"{int(i):05d}.png").convert("RGB").resize((960, 540))
    ImageDraw.Draw(im).rectangle((0, 520, 110, 540), fill="black")
    ImageDraw.Draw(im).text((4, 524), f"{lid} #{i}", fill="yellow")
    sheet.paste(im, ((k % 2) * 960, (k // 2) * 540))
out = ROOT / "audit" / "cs115" / "sheets" / f"{name}.png"
out.parent.mkdir(exist_ok=True)
sheet.save(out)
print(out)
