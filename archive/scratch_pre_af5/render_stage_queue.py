"""Hàng đợi tuần tự render MP4 + ASR theo danh sách khoá học (ví dụ: RBM ESY ROB GFX BCH).
Chỉ build lại bài nào STALE/chưa build (theo lv.verify / build_report), sau đó chạy ASR nếu cần.
Khi gặp `tts BLOCKED`: chờ 60 phút tối đa 6 lần (giữ an toàn cho dịch vụ TTS)."""
import io
import subprocess
import sys
import time
import datetime
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
LOG_DIR = ROOT / "out" / "_queue_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
WAIT = 3600


def log(log_file: Path, msg: str) -> None:
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def needs_build(yp: Path) -> bool:
    sp = lv.load_spec(yp)
    od = ROOT / "out" / yp.parent.name.upper() / sp["id"]
    rep = od / "build_report.json"
    mp4 = od / f"{sp['id']}.mp4"
    if not rep.exists() or not mp4.exists():
        return True
    import json
    b = json.loads(rep.read_text(encoding="utf-8"))
    if b.get("spec_sha256") != lv.spec_digest(sp):
        return True
    with redirect_stdout(io.StringIO()):
        frames = lv.build_frames(sp)
    if b.get("tts_sha256") != lv.tts_digest(frames):
        return True
    return False


def main() -> None:
    args = [a.upper() for a in sys.argv[1:] if not a.startswith("-")]
    force = "--force" in sys.argv[1:]
    courses = args or []
    assert courses, "Usage: python -u scratch/render_stage_queue.py COURSE1 [COURSE2 ...] [--force]"
    tag = "_".join(courses)
    log_file = LOG_DIR / f"queue_{tag}.log"
    targets = []
    for c in courses:
        for yp in sorted((ROOT / "lessons" / c.lower()).glob("L??_*.yaml")):
            if force or needs_build(yp):
                targets.append((c, yp))
    log(log_file, f"START queue {courses}: {len(targets)} lessons need build+asr")
    failed = []
    for idx, (c, yp) in enumerate(targets, 1):
        rel = yp.relative_to(ROOT).as_posix()
        log(log_file, f"[{idx}/{len(targets)}] BUILD {rel}")
        ok = False
        for attempt in range(7):
            r = subprocess.run([PY, "-u", "tools/lv.py", "build", rel], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
            out = (r.stdout or "") + (r.stderr or "")
            if r.returncode == 0:
                last_lines = " | ".join(out.splitlines()[-3:])
                log(log_file, f"  BUILD OK: {last_lines[:250]}")
                ok = True
                break
            blocked = "tts BLOCKED" in out
            log(log_file, f"  BUILD FAIL rc={r.returncode} blocked={blocked}: {out[-240:].strip()}")
            if blocked and attempt < 6:
                log(log_file, f"  TTS blocked — sleeping {WAIT // 60}m (retry {attempt + 2})")
                time.sleep(WAIT)
                continue
            break
        if not ok:
            failed.append(("build", rel))
            continue
        r2 = subprocess.run([PY, "-u", "tools/lv.py", "asr", rel], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        out2 = (r2.stdout or "") + (r2.stderr or "")
        asr_tail = " | ".join(out2.splitlines()[-2:])
        log(log_file, f"  ASR rc={r2.returncode}: {asr_tail[:250]}")
        if r2.returncode != 0:
            failed.append(("asr", rel))
    log(log_file, f"DONE queue {courses}: failed={len(failed)} {failed}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
