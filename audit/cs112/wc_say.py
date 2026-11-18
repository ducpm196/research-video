"""Đếm từ lời đọc (say) từng bài CS112: wc_say.py L15 L16 ... ; cảnh báo câu ngoài 4..38 từ (E?), số có dấu cách nhóm."""
import re
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
for lid in sys.argv[1:]:
    p = next((ROOT / "lessons" / "cs112").glob(lid + "_*.yaml"))
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    tot = 0
    bad = []
    for sc in d["scenes"]:
        for i, st in enumerate(sc.get("steps") or []):
            s = st.get("say") or ""
            tot += len(s.split())
            for sent in re.split(r"(?<=[.!?])\s+", s.strip()):
                n = len(sent.split())
                if sent and (n < 4 or n > 38):
                    bad.append((sc["id"], i, n, sent[:60]))
    print(lid, tot, "từ", len(bad), "câu ngoài 4..38:", bad[:5])
