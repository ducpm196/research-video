"""Công cụ soạn bài: chạy thử một phiên và in đầu ra thật từng bước để chép vào cmd(...).
Dùng: .venv/Scripts/python audit/fnd/explore.py <tệp.py>   — tệp định nghĩa FILES = {…} và STEPS = ["lệnh", …]."""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")
from runner import run_session  # noqa: E402

ns = {}
exec(Path(sys.argv[1]).read_text(encoding="utf-8"), ns)
got, err, R = run_session(ns.get("FILES", {}), ns["STEPS"])
if got is None:
    print("LỖI", err)
else:
    for i, a in enumerate(ns["STEPS"]):
        print(f"--- [{i}] $ {a}")
        print(repr(got.get(i, "<<không có>>")))
shutil.rmtree(R, ignore_errors=True)
