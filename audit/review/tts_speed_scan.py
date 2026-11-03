"""Quét câu TTS nghi bị CẮT CỤT trong mọi bài đã dựng: giây/từ thấp bất thường.
Lỗi thật AIF L08 khung 31 (2026-10-30): câu 9 từ chỉ 0,175 s/từ, cả small và medium chỉ nghe “Câu 2. Tri thức gồm áp/án” —
âm thanh cụt mà vẫn vượt ngưỡng chặn MIN_SEC_PER_WORD = 0,15 của lv.py (đặt theo L05: 0,045 s/từ). Trung vị kho ≈ 0,35 s/từ.
Câu bị nghi = s/từ < NGƯỠNG; in kèm bản chép ASR (cache) để phân định: chép đủ câu → đọc nhanh nhưng đủ; chép thiếu đuôi → cụt.
Chạy: .venv/Scripts/python audit/review/tts_speed_scan.py [ngưỡng=0.22] [khoá …]"""
import hashlib
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

args = sys.argv[1:]
thr = float(args.pop(0)) if args and args[0].replace(".", "", 1).isdigit() else 0.22
courses = [c.lower() for c in args] or sorted(p.name for p in (ROOT / "lessons").iterdir() if p.is_dir())
A = ROOT / "out" / "_cache" / "asr"
hits = n = 0
for c in courses:
    for f in sorted((ROOT / "lessons" / c).glob("L*_*.yaml")):
        lid = f.name.split("_")[0]
        if not (ROOT / "out" / c.upper() / lid / "build_report.json").exists():
            continue
        spec = lv.load_spec(f)
        with redirect_stdout(io.StringIO()):
            frames = lv.build_frames(spec)
        for i, fr in enumerate(frames):
            w = lv.tts_key(fr)
            if not w.exists():
                continue
            words = len(fr["tts"].replace("-", " ").split())
            n += 1
            if words < 4:
                continue  # câu rất ngắn: thời lượng bị khoảng lặng đầu/cuối chi phối, không so được
            spw = lv.wav_seconds(w) / words
            if spw < thr:
                hits += 1
                h = hashlib.sha256(w.read_bytes()).hexdigest()[:24]
                heard = [(A / f"{m}_{h}.txt").read_text(encoding="utf-8") for m in ("small", "medium") if (A / f"{m}_{h}.txt").exists()]
                print(f"{c.upper()} {lid} khung {i}: {spw:.3f} s/từ ({words} từ) | {fr['tts']}\n    nghe: {' || '.join(heard) or '(chưa có bản chép)'}")
print(f"\ntts_speed_scan: {n} câu, {hits} câu < {thr} s/từ", file=sys.stderr)
