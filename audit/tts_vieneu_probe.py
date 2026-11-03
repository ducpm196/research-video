"""Đo các giọng NAM miền BẮC của VieNeu so với vi-VN-NamMinhNeural, cùng thước đo audit/tts_fallback_probe.py:
F0 trung vị, giây/từ, độ khớp ASR (faster-whisper small + medium — như `lv.py asr`) trên 6 câu giảng mẫu. Chỉ đo, không chọn thay người dùng.
Chạy: .venv/Scripts/python audit/tts_vieneu_probe.py → audit/tts_fallback/vieneu_report.md"""
import asyncio
import difflib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "audit"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
import vi_text  # noqa: E402
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("fp", ROOT / "audit" / "tts_fallback_probe.py")
src = (ROOT / "audit" / "tts_fallback_probe.py").read_text(encoding="utf-8").replace("\nmain()\n", "\n")
fp = {"__file__": str(ROOT / "audit" / "tts_fallback_probe.py"), "__name__": "fp"}; exec(compile(src, "tts_fallback_probe.py", "exec"), fp)
SENT, f0_median, to_wav, edge = fp["SENT"], fp["f0_median"], fp["to_wav"], fp["edge"]
OUT = ROOT / "audit" / "tts_fallback"
VOICES = ["Minh Đức", "Phạm Tuyên", "Hải Đăng", "Quốc Tuấn", "Xuân Vĩnh", "Thanh Bình", "Thiện Minh"]


def main():
    jobs = [{"text": t, "voice": v, "out": str(OUT / f"vieneu_{v.replace(' ', '_')}_{i}.raw.wav")} for v in VOICES for i, t in enumerate(SENT)]
    r = subprocess.run([str(ROOT / ".venv-tts" / "Scripts" / "python.exe"), str(ROOT / "tools" / "tts_vieneu.py")],
                       input=json.dumps(jobs, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8")
    print("\n".join(l for l in r.stdout.splitlines() if l.startswith("FAIL")) or "vieneu: tổng hợp xong")
    names = {"edge NamMinh (chuẩn)": [OUT / f"edgeref_{i}.wav" for i in range(len(SENT))]}
    for i, t in enumerate(SENT):
        for k in range(3):
            try:
                asyncio.run(edge(t, names["edge NamMinh (chuẩn)"][i])); break
            except Exception as e:
                print("edge lần", k + 1, type(e).__name__)
    for v in VOICES:
        names[f"vieneu {v}"] = []
        for i in range(len(SENT)):
            raw = OUT / f"vieneu_{v.replace(' ', '_')}_{i}.raw.wav"; dst = raw.with_name(raw.name.replace(".raw", ""))
            if raw.exists():
                to_wav(raw, dst); raw.unlink()
            names[f"vieneu {v}"].append(dst)
    from faster_whisper import WhisperModel
    models = {m: WhisperModel(m, device="cpu", compute_type="int8") for m in ("small", "medium")}
    rows = []
    for name, files in names.items():
        if not all(f.exists() for f in files):
            print(name, "thiếu tệp — bỏ"); continue
        f0s, spw, sims = [], [], {m: [] for m in models}
        for t, f in zip(SENT, files):
            f0, dur = f0_median(f); f0s.append(f0); spw.append(dur / len(t.split()))
            for m, mod in models.items():
                hyp = " ".join(s.text for s in mod.transcribe(lv.load_audio_16k(f), language="vi", beam_size=5)[0])
                sims[m].append(difflib.SequenceMatcher(None, vi_text.normalize(t).split(), vi_text.normalize(hyp).split()).ratio())
        best = [max(a, b) for a, b in zip(sims["small"], sims["medium"])]
        rows.append((name, sorted(f0s)[len(f0s) // 2], sum(spw) / len(spw), sum(sims["small"]) / len(SENT), sum(sims["medium"]) / len(SENT),
                     sum(best) / len(SENT), min(best)))
        print(f"{name:26s} F0 {rows[-1][1]:6.1f}  {rows[-1][2]:.3f} s/từ  small {rows[-1][3]:.3f}  medium {rows[-1][4]:.3f}  "
              f"tốt hơn {rows[-1][5]:.3f}  thấp nhất {rows[-1][6]:.3f}", flush=True)
    md = ["| giọng | F0 (Hz) | giây/từ | ASR small | ASR medium | max(small, medium) TB | thấp nhất |", "|---|---|---|---|---|---|---|"]
    md += [f"| {r_[0]} | {r_[1]:.1f} | {r_[2]:.3f} | {r_[3]:.3f} | {r_[4]:.3f} | {r_[5]:.3f} | {r_[6]:.3f} |" for r_ in rows]
    (OUT / "vieneu_report.md").write_text("\n".join(md) + f"\n\ncâu đo: {SENT}\nchecked_at={lv.now()}\n", encoding="utf-8")
    print("→", OUT / "vieneu_report.md")


main()
