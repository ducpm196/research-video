"""Liệt kê các step có `focus` dạng "khối.dòng" trỏ vào một KHỐI MÃ, kèm dòng mã được trỏ, để người đọc xác nhận câu
lời đọc nói đúng dòng đó. Dùng sau khi sửa khối mã (thêm/bớt dòng làm lệch chỉ số dòng mà lint không bắt, vì lint chỉ
đếm số mục focus = số câu). Chạy: python -B audit/review/screen_code/focus_code_lines.py <tệp bài> [...]"""
import pathlib, re, sys
from html.parser import HTMLParser

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
import lv  # noqa: E402
import screen_code as sc  # noqa: E402


def top_blocks(show):
    """Khối cấp cao nhất như lv tách (dùng chính lv nếu có hàm), trả list html."""
    if hasattr(lv, "split_blocks"):
        return lv.split_blocks(show)
    return None


for f in sys.argv[1:]:
    spec = yaml.safe_load(open(f, encoding="utf-8"))
    for scn in spec.get("scenes") or []:
        for ti, st in enumerate(scn.get("steps") or []):
            foc = st.get("focus") or []
            dotted = [x for x in foc if isinstance(x, str) and re.fullmatch(r"\d+\.\d+", x)]
            show = st.get("show") or ""
            if not dotted or ("class=\"code" not in show and "<pre" not in show):
                continue
            sents = lv.sentences(st.get("say", ""))
            p = sc._Blocks()
            p.feed(show)
            p.close()
            print(f"== {f} [{scn.get('id')} step {ti}] focus={foc}")
            for i, x in enumerate(foc):
                s = sents[i] if i < len(sents) else "?"
                print(f"   câu {i + 1} → {x}: {s[:110]}")
            for bi, b in enumerate(p.blocks):
                for li, line in enumerate(b, 1):
                    print(f"      khối mã {bi} dòng {li}: {line[:100]}")
