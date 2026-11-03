"""Ghép 4 khung (1920×1080) thành một ảnh 2×2 cỡ 1920×1080 để xem bằng mắt nhanh hơn (SKILL Bước 6) — chỉ để duyệt bố cục;
chữ nhỏ (chỉ số, số mũ) vẫn phải mở khung gốc. Chạy: contact_sheet.py L15 0 8 15 19 → out/CS112/L15/sheet_0_8_15_19.png"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
lid, idx = sys.argv[1], [int(x) for x in sys.argv[2:6]]
d = ROOT / "out" / (sys.argv[6] if len(sys.argv) > 6 else "CS112") / lid
sheet = Image.new("RGB", (1920, 1080), "white")
for k, i in enumerate(idx):
    im = Image.open(d / "frames" / f"{i:05d}.png").convert("RGB").resize((960, 540))
    ImageDraw.Draw(im).text((8, 8), f"{lid} #{i}", fill="red")
    sheet.paste(im, ((k % 2) * 960, (k // 2) * 540))
out = d / f"sheet_{'_'.join(map(str, idx))}.png"
sheet.save(out)
print(out)
