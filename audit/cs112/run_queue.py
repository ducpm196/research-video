"""Hàng đợi chạy nền cho CS112 — một tiến trình duy nhất để các bước nặng (ASR) không tranh CPU.
Mỗi mục: "probe:<yaml>" | "build:<lesson.yaml>" | "asr:<lesson.yaml>". Ghi log vào out/CS112/_queue.log.
Khi TTS bị chặn (dịch vụ giới hạn tần suất / hết hạn mức): CHỜ 1 GIỜ rồi thử lại (yêu cầu người dùng 2026-10-27:
không thử lại mỗi phút), tối đa 6 lần. Chạy: .venv/Scripts/python -u audit/cs112/run_queue.py <mục> <mục> ..."""
import datetime
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
LOG = ROOT / "out" / "CS112" / "_queue.log"
WAIT = 3600


def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(args, tag):
    r = subprocess.run([PY, "-u"] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    (ROOT / "out" / "CS112" / f"_q_{tag}.log").write_text(out, encoding="utf-8")
    return r.returncode, out


for item in sys.argv[1:]:
    kind, path = item.split(":", 1)
    tag = f"{kind}_{Path(path).stem.split('_')[0]}"
    for attempt in range(7):
        if kind == "probe":
            rc, out = run(["audit/cs112/probe_terms.py", path], tag)
            blocked = "BLOCKED" in out
        elif kind == "build":
            rc, out = run(["tools/lv.py", "build", path], tag)
            blocked = "tts BLOCKED" in out
        else:
            rc, out = run(["tools/lv.py", "asr", path], tag)
            blocked = False
        summary = " | ".join(l for l in out.splitlines() if any(k in l for k in ("verify:", "build dừng", "[FAIL] render", "asr:", "tts:", "BLOCKED", "→ audit")))
        log(f"{item} rc={rc} {summary[:400]}")
        if blocked and attempt < 6:
            log(f"{item}: TTS bị chặn — chờ {WAIT // 60} phút rồi thử lại (lần {attempt + 2})")
            time.sleep(WAIT)
            continue
        break
log("QUEUE DONE")
