"""Rà mọi bài của mọi khoá: tham chiếu “bài N” so với lộ trình (lỗi thật 2026-10-29: CS115 L00 ghi “bài 34–43: mở rộng”,
bỏ sót L44). Bắt: (R1) đầu mút khoảng “bài a–b”/“bài a đến (bài) b” không có trong lộ trình; (R2) bản đồ khoá học (một cảnh
nhắc ≥ 60% số bài) không phủ đủ mọi bài 1..max; (R3) bài không có bài kế tiếp mà vẫn nói “bài sau/tiếp theo”; (R4) “bài cuối”
/“hết khoá”/“kết thúc khoá” ở bài không phải bài số lớn nhất (trừ khi nói rõ “của phần …”); (R5) “khoá (học) có/gồm N bài” sai
số bài. Chạy: .venv/Scripts/python audit/review/check_course_refs.py [khoá …]"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

DASH = r"\s*(?:–|-|—|đến|tới)\s*(?:bài\s+)?"
RANGE = re.compile(r"\b[Bb]ài\s+(\d+)" + DASH + r"(\d+)\b")
SINGLE = re.compile(r"\b[Bb]ài\s+(\d+)\b")
# “bài 12–15 và 17”, “bài 1–5; bài 16”: số đứng sau “và/,” ngay sau một tham chiếu
TAIL = re.compile(r"\b[Bb]ài\s+\d+(?:" + DASH + r"\d+)?((?:\s*(?:,|và|hoặc)\s*(?:bài\s+)?\d+(?:" + DASH + r"\d+)?)+)")


def covered(text):
    s = set()
    for m in RANGE.finditer(text):
        a, b = int(m.group(1)), int(m.group(2))
        if a < b:
            s.update(range(a, b + 1))
    for m in SINGLE.finditer(text):
        s.add(int(m.group(1)))
    for m in TAIL.finditer(text):
        for part in re.finditer(r"(\d+)(?:" + DASH + r"(\d+))?", m.group(1)):
            a = int(part.group(1))
            b = int(part.group(2) or a)
            s.update(range(a, b + 1))
    return s


def plain(st):
    return str(st.get("say", "")) + " \n " + re.sub(r"<[^>]+>", " ", str(st.get("show", "")))


def check(path):
    spec = lv.load_spec(path)
    cur, known = lv.lesson_numbers(spec)
    out = []
    if cur is None or not known:
        return out
    mx = max(known)
    lessons = set(k for k in known if k > 0)
    scene_cov = {}
    for si, sc, ki, st in lv.iter_steps(spec):
        where = f"{sc.get('id', si)}.{ki}"
        t = plain(st)
        for m in RANGE.finditer(t):
            for n in (int(m.group(1)), int(m.group(2))):
                if n not in known:
                    out.append(("R1", where, f"khoảng “{m.group(0)}” trỏ tới bài {n} không có trong lộ trình (max {mx})"))
        scene_cov.setdefault(sc.get("id", si), set()).update(covered(t))
        say = str(st.get("say", ""))
        if (cur + 1) not in known and re.search(r"(?<![Cc]ác )\b[Bb]ài (?:sau|tiếp theo)\b", re.sub(r"[Hh]ẹn gặp", "", say)):
            out.append(("R3", where, f"bài {cur} không có bài kế tiếp trong lộ trình mà vẫn nhắc “bài sau/tiếp theo”"))
        if re.search(r"[Hh]ẹn gặp bạn ở bài (tiếp theo|sau)", say) and (cur + 1) not in known:
            out.append(("R3", where, f"“hẹn gặp ở bài tiếp theo” ở bài {cur} — không còn bài kế tiếp"))
        # “hết khoá” cũng là thuật ngữ khoá dữ liệu (DBS L13, DSY L06: giữ khoá tới hết giao dịch) → chỉ xét “hết khoá học”.
        # Bài áp cuối giới thiệu “bài sau, bài cuối của khoá” là ĐÚNG (CSA L14, DMS L18, OSY L13 — báo nhầm 2026-10-31).
        for m in re.finditer(r"\b(bài cuối|hết khoá học|kết thúc khoá|khép lại khoá)\b[^.]{0,40}", say + " " + t, re.I):
            fwd = cur == mx - 1 and m.group(1).lower() == "bài cuối" and st.get("forward_ref")
            if cur != mx and not fwd and not re.search(r"phần|chặng|nhóm", m.group(0)):
                out.append(("R4", where, f"“{m.group(0)[:60]}” nhưng bài {cur} không phải bài cuối (max {mx})"))
        for m in re.finditer(r"\bkhoá(?: học)?(?: này)? (?:có|gồm) (\d+) bài\b", t):
            if int(m.group(1)) not in (len(known), len(lessons)):
                out.append(("R5", where, f"“{m.group(0)}” nhưng lộ trình có {len(known)} bài ({len(lessons)} không kể bài 0)"))
    for scid, cov in scene_cov.items():
        if len(cov & lessons) >= 0.6 * len(lessons) and len(lessons) >= 5:
            miss = sorted(lessons - cov - {cur})   # bản đồ nằm trong chính bài cur không cần tự liệt kê mình (AIF L13)
            if miss:
                out.append(("R2", scid, f"bản đồ khoá học phủ {len(cov & lessons)}/{len(lessons)} bài, thiếu: {miss}"))
    return out


courses = [c.lower() for c in sys.argv[1:]] or sorted(p.name for p in (ROOT / "lessons").iterdir() if p.is_dir())
total = 0
for c in courses:
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        for code, where, msg in check(p):
            total += 1
            print(f"{code} {c.upper()} {p.stem[:3]} {where}: {msg}")
print(f"\ncheck_course_refs: {total} vấn đề")
sys.exit(1 if total else 0)
