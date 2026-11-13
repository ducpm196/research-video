"""G-LEGAL (plan AF2): mọi số hiệu văn bản pháp lý trong lessons/, interview/, curriculum/ phải có mục trong audit/legal/registry.yaml;
văn bản HET_HIEU_LUC hoặc SUA_DOI hoặc CHUA_KIEM không được dẫn trơn: dòng chứa số hiệu (±400 ký tự) phải có cụm
"hết hiệu lực" | "thay bằng" | "thay thế" | "sửa đổi" | "cần kiểm lại" | "chưa kiểm" | "đã bị" | "luật cũ" | "trước 1/7/2026" | "NOT_VERIFIED".
Dùng: .venv/Scripts/python -B audit/review/check_legal.py [--strict]   (--strict: CHUA_KIEM cũng là FAIL)"""
import re, sys
from pathlib import Path
import yaml
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
reg = yaml.safe_load((ROOT / "audit/legal/registry.yaml").read_text(encoding="utf-8"))["docs"]
strict = "--strict" in sys.argv
NUM = re.compile(r"\b(\d{1,3}/\d{4}/(?:QH\d+|NĐ-CP|TT-[A-Z]+|QĐ-[A-Z]+|NQ-CP)|\d{1,3}/VBHN-[A-Z]+)")
HEDGE = re.compile(r"hết hiệu lực|thay bằng|thay thế|thay Nghị định|thay luật|thay Luật|sửa đổi|sửa bởi|cần kiểm lại|chưa kiểm|đã bị|luật cũ|trước 1/7/2026|NOT_VERIFIED|kiểm lại văn bản", re.I)
files = [p for d in ("lessons", "interview", "curriculum") for p in (ROOT / d).rglob("*") if p.suffix in (".yaml", ".md") and not p.name.startswith("HANDOVER")]   # HANDOVER*: nhật ký lịch sử
bad = n = 0
unknown, flagged = {}, {}
for f in files:
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in NUM.finditer(t):
        n += 1
        k = m.group(1)
        if k not in reg:
            unknown.setdefault(k, set()).add(f.relative_to(ROOT).as_posix())
            continue
        st = reg[k]["status"]
        if st == "HIEU_LUC":
            continue
        if st == "CHUA_KIEM" and not strict:
            continue
        if f.relative_to(ROOT).as_posix() in (reg[k].get("historical_ok") or []):
            continue                                    # bài hành trình kể đúng lịch sử văn bản (ghi trong sổ)
        ctx = t[max(0, m.start() - 400): m.end() + 400]
        if not HEDGE.search(ctx):
            flagged.setdefault((k, st), set()).add(f.relative_to(ROOT).as_posix())
for k, fs in sorted(unknown.items()):
    print(f"FAIL {k}: không có trong registry — {sorted(fs)[:3]}"); bad += 1
for (k, st), fs in sorted(flagged.items()):
    print(f"FAIL {k} [{st}] dẫn trơn, không ghi chú hiệu lực — {sorted(fs)[:4]}"); bad += 1
chua = [k for k, v in reg.items() if v["status"] == "CHUA_KIEM"]
print(f"check_legal: {n} lượt dẫn, {len(reg)} văn bản trong sổ ({len(chua)} CHUA_KIEM: {chua}), {bad} FAIL")
sys.exit(1 if bad else 0)
