"""(Bản GPU của audit/cs112/probe_terms.py cho khoá BNX, 2026-11-11: chỉ đổi thiết bị ASR sang cuda int8_float16 — production.md: cờ trên GPU ⊂ cờ CPU.)
Chọn cách viết cho TTS của từ ngoại / ký hiệu (SKILL Bước 4) — dùng cho CS112.
Mỗi cách viết × 4 ngữ cảnh × (small + medium) = 8 lần nghe. Văn bản gửi TTS KHÔNG qua lexicon.
Chấm: bản chép ASR (bỏ dấu, bỏ ký tự không phải chữ, chữ thường) chứa một khoá đích. Ngưỡng nhận: ≥ 7/8.
Đối chứng âm (một từ khác hẳn) phải KHÔNG đạt — nếu đạt thì phép thử không nói gì về từ đó (NOT_VERIFIED).
Chạy: .venv/Scripts/python audit/cs112/probe_terms.py audit/cs112/probes/<tên>.yaml
File yaml: {name, ctx: [4 câu có {}], terms: [{key, variants: [...], negative, keys: [...]}]}
Kết quả: audit/cs112/probes/<tên>.md (bảng) — audio lưu ở out/_probe/cs112/<tên>/."""
import asyncio
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
import edge_tts  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402

cfg = lv.load_yaml(sys.argv[1])
import os
D = Path(os.environ["FND_PROBE_DIR"]) / cfg["name"]
D.mkdir(parents=True, exist_ok=True)
VOICE, RATE = cfg.get("voice", "vi-VN-NamMinhNeural"), cfg.get("rate", "-5%")


def bare(t):
    t = "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn").replace("đ", "d")
    return re.sub(r"[^a-z]", "", t)


async def synth(t, p):
    for k in range(3):
        try:
            if not p.exists() or p.stat().st_size < 2000:
                await asyncio.wait_for(edge_tts.Communicate(t, VOICE, rate=RATE).save(str(p)), 60)
            if p.stat().st_size >= 2000:
                return
        except Exception:
            await asyncio.sleep(5 * (k + 1))
    print("TTS LỖI (không có âm thanh):", p.name, flush=True)  # FND: biến thể TTS không đọc được → điểm 0, không dừng cả mẻ


jobs = []
for term in cfg["terms"]:
    ctx = term.get("ctx") or cfg["ctx"]
    for vi, v in enumerate(term["variants"] + [term["negative"]]):
        for ci, c in enumerate(ctx):
            jobs.append((term["key"], vi, v, v == term["negative"], c.format(v), D / f"{re.sub(r'[^a-z0-9]', '', term['key'].lower())}_{vi}_{ci}.mp3"))  # giữ chữ số: sha1/sha256 từng ghi đè nhau


async def main():
    sem = asyncio.Semaphore(3)

    async def one(j):
        async with sem:
            await synth(j[4], j[5])
    await asyncio.gather(*[one(j) for j in jobs])
asyncio.run(main())
ms = {n: WhisperModel(n, device="cuda", compute_type="int8_float16") for n in ("small", "medium")}


def hear(n, p):
    segs, _ = ms[n].transcribe(lv.load_audio_16k(p), language="vi", beam_size=5, condition_on_previous_text=False)
    return " ".join(s.text.strip() for s in segs)


res = {}
for key, vi, v, neg, text, p in jobs:
    keys = [bare(k) for k in next(t["keys"] for t in cfg["terms"] if t["key"] == key)]
    hs = {n: (hear(n, p) if p.exists() and p.stat().st_size >= 2000 else "(TTS không đọc được)") for n in ms}
    hit = sum(any(k in bare(h) for k in keys) for h in hs.values())
    res.setdefault((key, v, neg), []).append((hit, text, hs))
lines = [f"# Dò phát âm `{cfg['name']}` (giọng {VOICE}, tốc độ {RATE}; small + medium; ngưỡng 7/8)", "",
         f"checked_at: {lv.now()}", "", "| từ | cách viết | điểm | đối chứng âm? | bản chép (small / medium) |", "|---|---|---|---|---|"]
for (key, v, neg), rows in res.items():
    tot = sum(h for h, _, _ in rows)
    heard = " ; ".join(f"{hs['small']} / {hs['medium']}" for _, _, hs in rows).replace("|", "/")
    lines.append(f"| {key} | «{v}» | {tot}/{2 * len(rows)} | {'ĐỐI CHỨNG' if neg else ''} | {heard[:600]} |")
    print(f"{key:12} «{v}» {tot}/{2 * len(rows)} {'(đối chứng âm)' if neg else ''}")
out = Path(sys.argv[1]).with_suffix(".md")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("→", out)
print("checked_at=" + lv.now())
