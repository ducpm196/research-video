"""Bằng chứng cho câu ASR gắn cờ có DÃY CHỮ SỐ (bit, hệ 16, số liệu): so dãy chữ số của lời đọc kỳ vọng với dãy chữ số trong bản chép
của small và medium (bỏ dấu cách, dấu phẩy; “không”, “một”… đọc rời cũng đổi về chữ số). Trùng hoàn toàn ở ít nhất một mô hình →
TTS đã đọc đủ và đúng thứ tự mọi chữ số (ASR chỉ gộp chữ số thành số). In bảng; không tự ghi gì.
Chạy: .venv/Scripts/python audit/asr_digits.py CSA L01 L06 …"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
W = {"không": "0", "một": "1", "hai": "2", "ba": "3", "bốn": "4", "năm": "5", "sáu": "6", "bảy": "7", "tám": "8", "chín": "9"}


def digits(s):
    s = s.lower()
    s = re.sub(r"\b(" + "|".join(W) + r")\b", lambda m: W[m.group(1)], s)
    return "".join(ch for ch in s if ch.isdigit())


def rows(course, lid):
    rep = (ROOT / "out" / course / lid / "asr_report.md").read_text(encoding="utf-8")
    full = rep.split("## Tham khảo")[0]
    out = []
    for line in full.splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 8 and c[0].isdigit():
            out.append(c)
    return out, rep


course = sys.argv[1].upper()
for lid in sys.argv[2:]:
    rs, rep = rows(course, lid)
    for c in rs:
        exp = c[2]
        if not re.search(r"\d", exp):
            continue
        heard = [c[3]]   # cột “nghe được” (asr_report chỉ lưu một bản chép)
        ok = any(digits(h) == digits(exp) for h in heard)
        print(f"{lid} | {'KHỚP SỐ' if ok else 'LỆCH SỐ'} | kỳ vọng {digits(exp)} | nghe {' / '.join(digits(h) for h in heard)} | {exp[:80]}")
