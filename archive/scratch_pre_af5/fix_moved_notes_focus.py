"""Cleanly move the 5 stray ENRICH notes in LLM/RLN/CVI into their actual spoken target steps, remove duplicates in CVI L05/L10, and fix focus[-1] in AIF L14 & CLD L09."""
import re
import subprocess
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def fix_final_focus(rel: str, sid: str, ki: int, new_last: int) -> None:
    p = ROOT / rel
    lines = p.read_text("utf-8").splitlines(keepends=True)
    d = yaml.safe_load("".join(lines))
    sc = next(s for s in d["scenes"] if s["id"] == sid)
    st = sc["steps"][ki]
    key = st["say"].strip()[:40]
    in_s = False
    say_i = None
    for i, l in enumerate(lines):
        if re.match(rf"^\s*-\s+id:\s+{re.escape(sid)}\b", l):
            in_s = True
        elif in_s and re.match(r"^\s*-\s+id:\s+\w+", l):
            in_s = False
        if in_s and l.lstrip().startswith("say:") and key in l:
            say_i = i
    assert say_i is not None, f"say not found: {rel} {sid}[{ki}]"
    # find focus block immediately before say_i
    j = say_i - 1
    while j > 0 and lines[j].lstrip().startswith("- "):
        j -= 1
    assert lines[j].lstrip().startswith("focus:"), f"focus not found before line {say_i} in {rel}"
    indent_item = " " * (len(lines[say_i - 1]) - len(lines[say_i - 1].lstrip()))
    lines[say_i - 1] = f"{indent_item}- {new_last}\n"
    p.write_text("".join(lines), encoding="utf-8")


def move_note(rel: str, src_pfx: str, dst_sid: str) -> None:
    p = ROOT / rel
    lines = p.read_text("utf-8").splitlines(keepends=True)
    # 1. Remove matching `<p class="note">...src_pfx...` line from wherever it currently sits
    removed_line = None
    new_lines = []
    for l in lines:
        if src_pfx in l and '<p class="note">' in l:
            removed_line = l.strip()
        else:
            new_lines.append(l)
    assert removed_line is not None, f"note not found: {src_pfx} in {rel}"
    txt = "".join(new_lines)

    # 2. Insert removed_line at end of `show:` of last step in `dst_sid`, and fix its last `focus:` index
    d = yaml.safe_load(txt)
    sc = next(s for s in d["scenes"] if s["id"] == dst_sid)
    st = sc["steps"][-1]
    new_show = str(st["show"]).rstrip() + "\n" + removed_line
    target_blk = len(lv.html_units(new_show))
    key = st["say"].strip()[:40]

    lines2 = txt.splitlines(keepends=True)
    in_s = False
    say_i = None
    for i, l in enumerate(lines2):
        if re.match(rf"^\s*-\s+id:\s+{re.escape(dst_sid)}\b", l):
            in_s = True
        elif in_s and re.match(r"^\s*-\s+id:\s+\w+", l):
            in_s = False
        if in_s and l.lstrip().startswith("say:") and key in l:
            say_i = i
    assert say_i is not None, f"dst say not found in {rel} {dst_sid}"

    # find focus or say_i right above say_i -> insert removed_line right before focus/introduces/say
    ins_at = say_i
    for j in range(say_i - 1, -1, -1):
        ls = lines2[j].lstrip()
        if ls.startswith(("focus:", "introduces:", "notation_note:", "forward_ref:", "pause:", "clear:")):
            ins_at = j
        elif ls.startswith("- ") and not ls.startswith("- show"):
            ins_at = j
        else:
            break
    indent_html = " " * (len(lines2[ins_at - 1]) - len(lines2[ins_at - 1].lstrip()))
    lines2[ins_at - 1] = lines2[ins_at - 1].rstrip("\r\n") + "\n" + indent_html + removed_line + "\n"
    p.write_text("".join(lines2), encoding="utf-8")
    fix_final_focus(rel, dst_sid, len(sc["steps"]) - 1, target_blk)


def remove_note_in_scene(rel: str, src_pfx: str, src_sid: str) -> None:
    p = ROOT / rel
    lines = p.read_text("utf-8").splitlines(keepends=True)
    in_s = False
    removed = 0
    new_lines = []
    for l in lines:
        if re.match(rf"^\s*-\s+id:\s+{re.escape(src_sid)}\b", l):
            in_s = True
        elif in_s and re.match(r"^\s*-\s+id:\s+\w+", l):
            in_s = False
        if in_s and src_pfx in l and '<p class="note">' in l:
            removed += 1
            continue
        new_lines.append(l)
    assert removed > 0, f"note not found in {rel} #{src_sid}: {src_pfx}"
    p.write_text("".join(new_lines), encoding="utf-8")


# Apply exact 5 moves + 2 scene-scoped duplicate removals + 2 final focus fixes
move_note("lessons/llm/L01_ngram_do_hon_loan.yaml", "<b>Quy tắc so sánh mô hình đúng:</b>", "check")
move_note("lessons/rln/L00_loi_nhuan_chiet_khau.yaml", "<b>Chọn $\\gamma$ và cạm bẫy cộng hằng số:</b>", "check")
move_note("lessons/rln/L11_khai_thac_phan_thuong.yaml", "<b>Thiết kế phần thưởng an toàn:</b>", "check")
move_note("lessons/cvi/L00_anh_so.yaml", "<b>Số mức màu của kênh:</b>", "formula")
move_note("lessons/cvi/L06_do_sau_hai_camera.yaml", "<b>Chọn thông số cho bài đo thực tế:</b>", "check")

remove_note_in_scene("lessons/cvi/L05_ransac.yaml", "<b>Đánh đổi chi phí:</b>", "example")
remove_note_in_scene("lessons/cvi/L10_dich_chuyen_mien.yaml", "<b>Quy tắc lập tập kiểm tra:</b>", "example")

fix_final_focus("lessons/aif/L14_hanh_trinh_may_choi_co.yaml", "stage5", 1, 3)
fix_final_focus("lessons/cld/L09_can_bang_tai.yaml", "example", 3, 3)

TOUCHED = [
    "lessons/llm/L01_ngram_do_hon_loan.yaml",
    "lessons/rln/L00_loi_nhuan_chiet_khau.yaml",
    "lessons/rln/L11_khai_thac_phan_thuong.yaml",
    "lessons/cvi/L00_anh_so.yaml",
    "lessons/cvi/L05_ransac.yaml",
    "lessons/cvi/L06_do_sau_hai_camera.yaml",
    "lessons/cvi/L10_dich_chuyen_mien.yaml",
    "lessons/aif/L14_hanh_trinh_may_choi_co.yaml",
    "lessons/cld/L09_can_bang_tai.yaml",
]
for rel in TOUCHED:
    print(">>> LINT", rel, flush=True)
    r = subprocess.run([PY, "-B", "tools/lv.py", "lint", rel], cwd=ROOT)
    assert r.returncode == 0, f"lint failed: {rel}"

for c in ("LLM", "RLN", "CVI", "AIF", "CLD"):
    subprocess.run([PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"], cwd=ROOT, check=True)
    subprocess.run([PY, "-B", "audit/review/screen_code.py", "check", "--course", c], cwd=ROOT, check=True)

for c in ("LLM", "RLN", "CVI"):
    subprocess.run([PY, "-B", "-u", "audit/layout_scan.py", c], cwd=ROOT, check=True)
    tsv = ROOT / f"audit/layout_{c}.tsv"
    assert not tsv.read_text("utf-8").strip(), f"layout errors in {c}"

print("ALL MOVED NOTES + FOCUS + LINT + LAYOUT_SCAN 100% PASS!", flush=True)
