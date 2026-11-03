"""In các bước mà `focus` lệch số câu (hoặc bước dày chữ thiếu focus), kèm từng câu đánh số và các phần của khối,
để người soạn đặt focus đúng (lint E31/E32). Chạy: .venv/Scripts/python audit/cs112/focus_help.py lessons/cs112/Lxx_*.yaml"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

spec = lv.load_spec(sys.argv[1])
for sc in spec["scenes"]:
    for ki, st in enumerate(sc["steps"]):
        sents = lv.sentences(st.get("say") or "")
        foc = st.get("focus")
        units = lv.html_units(str(st.get("show", ""))) if st.get("show") else []
        if (foc is not None and len(foc) != len(sents)) or (foc is None and len(units) >= 3 and len(sents) >= 3):
            print(f"== {sc['id']}.{ki}: {len(sents)} câu, focus hiện có {foc}")
            print("   phần của khối: " + ", ".join(f"{i + 1}:{u['tag']}({len(u['kids'])})" for i, u in enumerate(units)))
            for j, s in enumerate(sents, 1):
                print(f"   {j}. {s[:110]}")
