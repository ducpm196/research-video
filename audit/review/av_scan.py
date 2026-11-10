# Chuyển từ scratchpad phiên 7f725234 (2026-11-09) vào kho 2026-11-10 để dùng lại. Dùng: .venv/Scripts/python -B audit/review/av_scan.py [out.tsv]
"""Quét mọi out/<KHOÁ>/<Lxx>/<Lxx>.mp4: độ dài luồng hình và luồng tiếng (ffmpeg -c copy -f null), timeline trong build_report,
codec/độ phân giải. In TSV + tóm tắt: lệch hình−tiếng, lệch container−timeline (ngưỡng verify 0,5 s)."""
import json, re, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("D:/research-video")
FF = str(ROOT / ".venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
TIME = re.compile(r"time=(\d+):(\d+):([\d.]+)")
DUR = re.compile(r"Duration: (\d+):(\d+):([\d.]+)")
def secs(m): return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
def stream_len(mp4, sel):
    r = subprocess.run([FF, "-hide_banner", "-i", str(mp4), "-map", f"0:{sel}", "-c", "copy", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    ms = list(TIME.finditer(r.stderr))
    return (secs(ms[-1]) if ms else None), r.stderr
rows = []
for rep in sorted(ROOT.glob("out/*/L*/build_report.json")):
    d = rep.parent; mp4 = d / f"{d.name}.mp4"
    if d.parent.name.startswith("_") or not mp4.exists():
        continue
    tl = json.loads(rep.read_text(encoding="utf-8")).get("timeline_seconds")
    v, info = stream_len(mp4, "v"); a, _ = stream_len(mp4, "a")
    m = DUR.search(info); cont = secs(m) if m else None
    ok = all(s in info for s in ("Video: h264", "Audio: aac", "1920x1080"))
    rows.append((d.parent.name, d.name, tl, cont, v, a, ok))
out = Path(sys.argv[1]) if len(sys.argv) > 1 else None
lines = ["course\tlesson\ttimeline\tcontainer\tvideo\taudio\tv_minus_a\tcont_minus_tl\tformat_ok"]
for c, l, tl, cont, v, a, ok in rows:
    va = None if v is None or a is None else round(v - a, 3)
    ct = None if cont is None or tl is None else round(cont - tl, 3)
    lines.append(f"{c}\t{l}\t{tl}\t{cont}\t{v}\t{a}\t{va}\t{ct}\t{ok}")
if out:
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
va = [float(x.split("\t")[6]) for x in lines[1:] if x.split("\t")[6] != "None"]
ct = [float(x.split("\t")[7]) for x in lines[1:] if x.split("\t")[7] != "None"]
print(f"video: {len(rows)} | format sai: {sum(1 for r in rows if not r[6])} | thiếu số đo: {len(rows) - len(va)}")
print(f"hình−tiếng: max {max(va):.3f}s, min {min(va):.3f}s, >0,3s: {sum(1 for x in va if x > 0.3)}, >0,5s: {sum(1 for x in va if x > 0.5)}")
print(f"container−timeline: max |Δ| {max(abs(x) for x in ct):.3f}s, >0,5s: {sum(1 for x in ct if abs(x) > 0.5)}")
for x in lines[1:]:
    f = x.split("\t")
    if f[8] != "True" or (f[6] != "None" and float(f[6]) > 0.3) or (f[7] != "None" and abs(float(f[7])) > 0.5):
        print("  ", x)
