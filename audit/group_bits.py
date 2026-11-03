"""Nhóm dãy bit dài trong LỜI ĐỌC thành từng 4 bit, ngắt bằng dấu phẩy, tính từ bên phải (như khi đổi sang hệ 16):
“1 1 1 1 0 1 0 0” → “1 1 1 1, 0 1 0 0”; “1 1 0 1 1 1 1” → “1 1 0, 1 1 1 1”.
Lý do (OBSERVED, CSA L01/L02 asr 2026-10-28): dãy ≥ 5 chữ số 0/1 đọc liền, ASR gộp thành số và chép thiếu/sai chữ số
(“0 0 0 0 0 1 0 1” → “0000001”), nên không kiểm được TTS có đọc đủ; nhóm 4 bit cũng là cách đọc chuẩn cho người học.
Chỉ đổi trường `say`, không đổi màn hình. Chạy: group_bits.py lessons/csa/L01_….yaml …  (in từng dòng đổi)"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
# Khớp THAM LAM cả dãy chữ số 0/1 cách nhau đúng một dấu cách; dãy < 5 chữ số để nguyên. KHÔNG dùng lookahead cấm dấu phẩy:
# bản đầu có “(?![\d,])” làm dãy đứng trước dấu phẩy bị cắt ngắn (“1 1 1 1 1 0 1 1,” → “1 1 1, 1 1 0 1 1”) — lỗi thật 2026-10-28.
RUN = re.compile(r"\b[01](?: [01])+\b")


def group(m):
    bits = m.group(0).split(" ")
    if len(bits) < 5:
        return m.group(0)
    head = len(bits) % 4
    parts = ([bits[:head]] if head else []) + [bits[i:i + 4] for i in range(head, len(bits), 4)]
    return ", ".join(" ".join(p) for p in parts)


DRY = "--dry" in sys.argv
for f in [a for a in sys.argv[1:] if a != "--dry"]:
    p = Path(f); lines = p.read_text(encoding="utf-8").split("\n"); n = 0
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("say:"):
            new = RUN.sub(group, ln)
            if new != ln:
                print(f"{p.name}:{i + 1}\n  - {ln.strip()}\n  + {new.strip()}"); lines[i] = new; n += 1
    if not DRY:
        p.write_text("\n".join(lines), encoding="utf-8")
    print(f"{p.name}: {n} dòng đổi")
