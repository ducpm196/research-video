"""Tổng hợp giọng bằng VieNeu-TTS (Apache-2.0, chạy cục bộ trên CPU) — chạy bằng .venv-tts/Scripts/python (môi trường riêng,
không đụng gói đã ghim của .venv). Đọc danh sách việc JSON từ stdin: [{"text": …, "voice": "Phạm Tuyên", "out": "…wav", "speed": 1.0}],
ghi mỗi “out” một tệp wav, in “OK <out>” hoặc “FAIL <out> <lỗi>” mỗi dòng. `--list` in các giọng có sẵn."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")
from vieneu import Vieneu  # noqa: E402

tts = Vieneu()
if "--list" in sys.argv:
    for label, vid in tts.list_preset_voices():
        print(label, "|", vid)
    sys.exit(0)
for job in json.load(sys.stdin):
    try:
        kw = {"voice": job["voice"]}
        audio = tts.infer(job["text"], **kw)
        tts.save(audio, job["out"])
        print("OK", job["out"], flush=True)
    except Exception as e:  # một câu lỗi không huỷ cả lượt
        print("FAIL", job["out"], type(e).__name__, str(e)[:200], flush=True)
