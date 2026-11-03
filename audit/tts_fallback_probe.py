"""Đánh giá giọng dự phòng so với vi-VN-NamMinhNeural: cao độ (F0 trung vị — nam ≈ 85–180 Hz), tốc độ (giây/từ) và độ khớp ASR
(faster-whisper small, cùng thước đo `lv.py asr`) trên 6 câu giảng mẫu của các khoá. In bảng; KHÔNG chọn giọng thay người dùng.
Chạy: .venv/Scripts/python audit/tts_fallback_probe.py → audit/tts_fallback/report.md (+ wav từng giọng để nghe)"""
import asyncio
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
import vi_text  # noqa: E402

OUT = ROOT / "audit" / "tts_fallback"; OUT.mkdir(parents=True, exist_ok=True)
PIPER = ROOT / "tools" / "vendor" / "piper"
SENT = ["Chào bạn, hôm nay ta học thuật toán sắp xếp.",
        "Tiến trình đầu tiên chờ 0 mi li giây, tiến trình thứ hai chờ 24 mi li giây.",
        "Vì mỗi bước chia đôi đoạn cần tìm, nên số bước tăng theo lô-ga-rít.",
        "Lỗi thứ nhất, nghĩ thêm bộ nhớ luôn giảm lỗi trang.",
        "Đáp án câu một, trung bình bằng 17 chia 3, khoảng 5 phẩy 67.",
        "Điều cần mang theo, hãy đo trước khi tối ưu."]


def f0_median(wav):
    with wave.open(str(wav)) as w:
        sr, x = w.getframerate(), np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    hop, n, f0 = int(sr * 0.01), int(sr * 0.04), []
    for i in range(0, len(x) - n, hop):
        fr = x[i:i + n] - x[i:i + n].mean()
        if np.sqrt((fr ** 2).mean()) < 300:      # bỏ khoảng lặng
            continue
        ac = np.correlate(fr, fr, "full")[n - 1:]
        lo, hi = int(sr / 400), int(sr / 60)
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.3 * ac[0]:                  # khung hữu thanh
            f0.append(sr / k)
    return float(np.median(f0)) if f0 else float("nan"), len(x) / sr


def to_wav(src, dst):
    subprocess.run([lv.ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", "24000", str(dst)], check=True)


async def edge(text, dst):
    import edge_tts
    mp3 = dst.with_suffix(".mp3")
    await edge_tts.Communicate(text, "vi-VN-NamMinhNeural", rate="-5%").save(str(mp3))
    to_wav(mp3, dst); mp3.unlink()


def piper(model, text, dst, speaker=None):
    from piper import PiperVoice, SynthesisConfig
    v = PiperVoice.load(str(model))
    cfg = SynthesisConfig(speaker_id=speaker) if speaker is not None else None
    tmp = dst.with_suffix(".raw.wav")
    with wave.open(str(tmp), "wb") as w:
        v.synthesize_wav(text, w, syn_config=cfg)
    to_wav(tmp, dst); tmp.unlink()


def main():
    from faster_whisper import WhisperModel
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    voices = {"edge NamMinh (chuẩn)": ("edge", None, None)}
    for onnx in sorted(PIPER.glob("*.onnx")):
        meta = json.loads(onnx.with_suffix(".onnx.json").read_text(encoding="utf-8"))
        ns = int(meta.get("num_speakers", 1))
        for s in (range(ns) if ns > 1 else [None]):
            voices[f"piper {onnx.stem}" + (f" #{s}" if s is not None else "")] = ("piper", onnx, s)
    rows = []
    for name, (kind, model, spk) in voices.items():
        # vòng 1: chỉ đo cao độ trên câu đầu; giọng F0 ≥ 165 Hz (không phải giọng nam) bỏ qua ASR
        d0 = OUT / "pitch_tmp.wav"
        asyncio.run(edge(SENT[0], d0)) if kind == "edge" else piper(model, SENT[0], d0, spk)
        if kind != "edge" and f0_median(d0)[0] >= 165:
            print(f"{name:42s} F0 {f0_median(d0)[0]:6.1f} Hz  (bỏ qua ASR)"); continue
        f0s, spw, sims = [], [], []
        for i, t in enumerate(SENT):
            dst = OUT / f"{name.replace(' ', '_').replace('#', 's').replace('(', '').replace(')', '')}_{i}.wav"
            try:
                asyncio.run(edge(t, dst)) if kind == "edge" else piper(model, t, dst, spk)
            except Exception as e:
                print(name, "LỖI", type(e).__name__, e); break
            f0, dur = f0_median(dst); f0s.append(f0); spw.append(dur / len(t.split()))
            hyp = " ".join(s.text for s in asr.transcribe(lv.load_audio_16k(dst), language="vi", beam_size=5)[0])
            sims.append(lv.similarity(vi_text.normalize(t), vi_text.normalize(hyp)) if hasattr(lv, "similarity")
                        else __import__("difflib").SequenceMatcher(None, vi_text.normalize(t).split(), vi_text.normalize(hyp).split()).ratio())
        if len(sims) == len(SENT):
            rows.append((name, np.nanmedian(f0s), np.mean(spw), np.mean(sims), min(sims)))
            print(f"{name:42s} F0 {rows[-1][1]:6.1f} Hz  {rows[-1][2]:.3f} s/từ  ASR TB {rows[-1][3]:.3f}  thấp nhất {rows[-1][4]:.3f}")
    md = ["| giọng | F0 trung vị (Hz) | giây/từ | ASR khớp TB | thấp nhất |", "|---|---|---|---|---|"]
    md += [f"| {n} | {a:.1f} | {b:.3f} | {c:.3f} | {d:.3f} |" for n, a, b, c, d in rows]
    (OUT / "report.md").write_text("\n".join(md) + f"\n\nchecked_at={lv.now()}\n", encoding="utf-8")
    print("→", OUT / "report.md")


main()
