"""Chèn một khối HAND vào audit/dms/asr_review_dms.py trước mốc CSA L03. Dùng: ins_hand.py <tệp khối> <nhãn không được trùng>."""
import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
p = pathlib.Path("audit/dms/asr_review_dms.py")
t = p.read_text(encoding="utf-8")
m = "    # ── CSA L03 dựng lại (2026-10-29) ──"
add = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
assert t.count(m) == 1, "mốc không duy nhất"
assert sys.argv[2] not in t, "khối đã có"
p.write_text(t.replace(m, add + m), encoding="utf-8")
print("ok")
