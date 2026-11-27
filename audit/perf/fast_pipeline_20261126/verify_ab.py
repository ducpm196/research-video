
"""So hai bản dựng của CÙNG một bài (A: lv.py, B: lv_fast.py): luồng, âm thanh, phụ đề, khung PNG, từng mốc chuyển slide.
Dùng: .venv/Scripts/python -B audit/perf/fast_pipeline_20261126/verify_ab.py <thư mục bài A> <thư mục bài B> <Lxx>"""
import sys, subprocess, json, re, hashlib
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode=True
import ctypes
def _idle():  # ưu tiên thấp nhất của Windows (tiến trình con thừa hưởng) để không giành CPU với hàng dựng đang chạy
    k = ctypes.windll.kernel32; k.GetCurrentProcess.restype = ctypes.c_void_p
    k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]; k.SetPriorityClass(k.GetCurrentProcess(), 0x40)
_idle()
import numpy as np
from PIL import Image
from pathlib import Path
FF = r"D:/research-video/.venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
A, B = Path(sys.argv[1]), Path(sys.argv[2]); lid = sys.argv[3]
W, H = 480, 270
def info(p):
    return subprocess.run([FF, "-hide_banner", "-i", str(p)], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
def stream_len(p, sel):
    r = subprocess.run([FF, "-hide_banner", "-i", str(p), "-map", "0:" + sel, "-c", "copy", "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = list(re.finditer(r"time=(\d+):(\d+):([\d.]+)", r.stderr))[-1]
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
def audio_md5(p):
    return subprocess.run([FF, "-v", "error", "-i", str(p), "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()
def decode_errors(p):
    r = subprocess.run([FF, "-v", "error", "-i", str(p), "-f", "null", "-"], capture_output=True, text=True, errors="replace")
    return r.returncode, r.stderr.strip()[:300]
for name, d in (("A lv.py", A), ("B lv_fast", B)):
    p = d / (lid + ".mp4"); i = info(p)
    v = re.search(r"Video: (.*)", i)[1]; a = re.search(r"Audio: (.*)", i)[1]
    print(f"--- {name}: {p.stat().st_size/1e6:.2f} MB | " + re.search(r"Duration: [^,]+", i)[0])
    print("   hình:", v[:150]); print("   tiếng:", a[:90])
    vl, al = stream_len(p, "v"), stream_len(p, "a")
    rep = json.loads((d / "build_report.json").read_text(encoding="utf-8"))
    print(f"   luồng hình {vl:.3f}s, tiếng {al:.3f}s, hình-tiếng {vl-al:+.3f}s, timeline {rep['timeline_seconds']}s | giải mã toàn tệp rc/err: {decode_errors(p)}")
    print("   spec_sha", rep["spec_sha256"][:12], "tts_sha", rep["tts_sha256"][:12], "frames", rep["frames"], "encoder", rep.get("video_encoder", "(không ghi)"))
print("âm thanh AAC giống từng byte:", audio_md5(A/(lid+".mp4")) == audio_md5(B/(lid+".mp4")))
for f in (lid + ".srt", "chapters.txt", "_frames.txt"):
    print(f, "giống từng byte:", (A/f).read_bytes() == (B/f).read_bytes())
pa, pb = sorted((A/"frames").glob("*.png")), sorted((B/"frames").glob("*.png"))
same = sum(x.read_bytes() == y.read_bytes() for x, y in zip(pa, pb))
print(f"khung PNG: {len(pa)} vs {len(pb)}, giống từng byte {same}")
# mốc chuyển slide
durs = [float(l.split()[1]) for l in (B/"_frames.txt").read_text().splitlines() if l.startswith("duration")]
t0 = np.concatenate([[0], np.cumsum(durs)])
refs = [np.asarray(Image.open(p).convert("L").resize((W, H), Image.BILINEAR), dtype=np.int16) for p in pb]
dist = [float(np.abs(refs[k] - refs[k-1]).mean()) for k in range(1, len(refs))]
def classify(p, fps):
    proc = subprocess.Popen([FF, "-v", "error", "-i", str(p), "-map", "0:v", "-vf", f"scale={W}:{H}:flags=bilinear,format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    labels = []; cur = 0; n = 0
    while True:
        buf = proc.stdout.read(W * H)
        if len(buf) < W * H: break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W).astype(np.int16)
        t = n / fps
        near = int(np.searchsorted(t0, t, side="right")) - 1
        cands = [c for c in (near - 1, near, near + 1) if 0 <= c < len(refs)]
        scores = {c: float(np.abs(fr - refs[c]).mean()) for c in cands}
        best = min(scores, key=scores.get)
        labels.append((t, best, scores[best], near)); n += 1
    proc.wait()
    return labels
for name, d, fps in (("A", A, 30), ("B", B, 10)):
    lab = classify(d / (lid + ".mp4"), fps)
    # mốc quan sát được: khung video đầu tiên khớp slide k (k>=1)
    first = {}
    for t, best, sc, near in lab: first.setdefault(best, t)
    errs = []; undetectable = 0; missing = []
    for k in range(1, len(refs)):
        if dist[k-1] < 0.05: undetectable += 1; continue
        if k not in first: missing.append(k); continue
        errs.append(first[k] - t0[k])
    errs = np.array(errs)
    wrong_far = sum(1 for t, best, sc, near in lab if best != near and min(abs(t - t0[near]), abs(t - t0[min(near+1, len(t0)-1)])) > 0.2 and 0 <= near < len(refs) and (best == 0 or dist[best-1] >= 0.05))
    print(f"{name} ({fps} fps): {len(lab)} khung video | mốc đo được {len(errs)}/{len(refs)-1} (không phân biệt được {undetectable}, thiếu {missing}) | lệch mốc: min {errs.min():+.3f}s, max {errs.max():+.3f}s, |lệch| trung bình {np.abs(errs).mean():.3f}s | khung sai slide cách mốc >0,2 s: {wrong_far} | sai khác pixel TB {np.mean([s for _,_,s,_ in lab]):.3f}/255")
