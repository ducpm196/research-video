"""So bản chép GPU với bản chép CPU đã cache (cùng wav, cùng mô hình) trên mẫu câu từ các khoá đã xong.
Chạy: .venv/Scripts/python audit/perf/asr_gpu_eq.py int8_float16 120
Kết quả 2026-10-30 (RTX 2060): small giống hệt 77/120, TB 0,983; medium 95/120, TB 0,991. Xem tools/lv.py ASR_DEVICE."""
import sys, hashlib, random, time, difflib, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8"); sys.path.insert(0, "tools")
import lv
from vi_text import normalize
from faster_whisper import WhisperModel
ct = sys.argv[1]; N = int(sys.argv[2])
A = Path("out/_cache/asr"); pairs = []
wavs = sorted(Path("out/_cache/tts").glob("*.wav")); random.Random(7).shuffle(wavs)
for w in wavs:
    h = hashlib.sha256(w.read_bytes()).hexdigest()[:24]
    if (A / f"small_{h}.txt").exists() and (A / f"medium_{h}.txt").exists():
        pairs.append((w, h))
    if len(pairs) >= N: break
res = {}
for m in ("small", "medium"):
    model = WhisperModel(m, device="cuda", compute_type=ct); same = 0; rs = []; t0 = time.time(); diffs = []
    for w, h in pairs:
        s, _ = model.transcribe(lv.load_audio_16k(w), language="vi", beam_size=5, condition_on_previous_text=False)
        g = " ".join(x.text.strip() for x in s); c = (A / f"{m}_{h}.txt").read_text(encoding="utf-8")
        r = difflib.SequenceMatcher(None, normalize(c).split(), normalize(g).split()).ratio(); rs.append(r)
        same += g == c
        if r < 1: diffs.append((round(r, 3), c[:80], g[:80]))
    print(f"{m} {ct}: {len(pairs)} câu, {time.time()-t0:.0f}s, giống hệt {same}, tương đồng TB {sum(rs)/len(rs):.4f}, min {min(rs):.3f}")
    for d in sorted(diffs)[:4]: print("   ", d)
    del model
