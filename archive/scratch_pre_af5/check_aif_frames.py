import json
from pathlib import Path
ROOT = Path(r"D:\research-video")
dec = json.JSONDecoder()
for c, lid, fidx in [("CVI", "L08", 99), ("CVI", "L09", 90), ("CVI", "L12", 116)]:
    html = (ROOT / "out" / c / lid / "preview.html").read_text(encoding="utf-8")
    pos = html.find("DATA = ")
    pos = html.find("{", html.find("DATA=") if pos < 0 else pos)
    data, _ = dec.raw_decode(html, pos)
    fr = data["frames"][fidx]
    print(f"=== {c} {lid} frame {fidx} / {len(data['frames'])} scene={fr.get('scene_title')} kind={fr.get('kind')} ===")
    for b in fr.get("blocks", []):
        print("  BLK:", b[:1200])
