"""Clean up the 8 misplaced note insertions from the first pre-fix run + 4 DSC lint items."""
import ast
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

# 1. Strip any occurrence of our ENRICH_S8 notes & appended say/focus in the 8 files that had wrong placement
src = (ROOT / "scratch/fix_stage8_v3_go.py").read_text("utf-8")
tree = ast.parse(src)
enrich_list = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "ENRICH_S8" for t in node.targets):
        enrich_list = ast.literal_eval(node.value)

EIGHT = {
    "lessons/dan/L02_noi_nhan_dong.yaml",
    "lessons/dan/L03_ham_cua_so.yaml",
    "lessons/dan/L12_hanh_trinh_thu_nghiem_ab.yaml",
    "lessons/dan/L07_du_bao_co_so.yaml",
    "lessons/dan/L11_bang_dieu_khien.yaml",
    "lessons/dsc/L03_du_lieu_thieu.yaml",
    "lessons/dsc/L12_dien_giai_hoi_quy.yaml",
    "lessons/mlo/L08_giam_sat_troi.yaml",
}

for rel, sid, n_html, n_say, _ in enrich_list:
    if rel not in EIGHT:
        continue
    p = ROOT / rel
    lines = p.read_text("utf-8").splitlines(keepends=True)
    # Remove any line containing first 30 chars of note or old alpha/DAN L11 variant
    prefixes = [n_html[:30], '<p class="note"><b>Thiết kế cảnh báo ít báo động giả:', '<p class="note"><b>Ngưỡng ý nghĩa thống kê']
    lines = [l for l in lines if not any(pf in l for pf in prefixes)]
    txt = "".join(lines)
    # Strip appended n_say (or old DAN L11 say) + 1 trailing focus item from target scene
    old_says = [n_say.strip(), "Để thiết kế cảnh báo ít báo động giả, hãy đặt ngưỡng đủ rộng và đòi hỏi vi phạm lặp qua hai kỳ liên tiếp nhằm lọc nhiễu."]
    for osay in old_says:
        if osay in txt:
            txt = txt.replace(" " + osay, "").replace(osay, "")
            # Pop the last focus item added on that target scene's last step if present
            d = yaml.safe_load(txt)
            sc = next(s for s in d["scenes"] if s["id"] == sid)
            st = sc["steps"][-1]
            # Let exact step lint count be synced cleanly below if needed
    p.write_text(txt, encoding="utf-8")

# 2. Exact focus restoration on the 8 target scenes + DSC L03/08/12/13
def fix_step_focus(rel: str, sid: str, idx: int, new_foc):
    p = ROOT / rel
    lines = p.read_text("utf-8").splitlines(keepends=True)
    d = yaml.safe_load("".join(lines))
    sc = next(s for s in d["scenes"] if s["id"] == sid)
    st = sc["steps"][idx]
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
    assert say_i is not None, f"missing {rel} {sid}[{idx}]"
    for j in range(say_i - 1, max(-1, say_i - 25), -1):
        if lines[j].lstrip().startswith("focus:"):
            end = j + 1
            while end < say_i and lines[end].lstrip().startswith("- "):
                end += 1
            indent = " " * (len(lines[j]) - len(lines[j].lstrip()))
            if new_foc is None:
                lines = lines[:j] + lines[end:]
            else:
                item_indent = indent + "- "
                repl = [f"{indent}focus:\n"] + [f"{item_indent}{x!r}\n" if isinstance(x, str) else f"{item_indent}{x}\n" for x in new_foc]
                lines = lines[:j] + repl + lines[end:]
            break
    p.write_text("".join(lines), encoding="utf-8")

fix_step_focus("lessons/dan/L02_noi_nhan_dong.yaml", "sym", 0, [1, "1.2", "1.3", "1.4", 2, 2])
fix_step_focus("lessons/dan/L03_ham_cua_so.yaml", "check", 0, [0, "1.2", "1.3", "1.3", "1.4"])
fix_step_focus("lessons/dan/L07_du_bao_co_so.yaml", "check", 0, [0, "1.2", "1.3", "1.4"])
fix_step_focus("lessons/dan/L11_bang_dieu_khien.yaml", "check", 0, [0, "1.2", "1.2", "1.3", 2, 2])
fix_step_focus("lessons/dan/L12_hanh_trinh_thu_nghiem_ab.yaml", "sym", 0, [1, "1.2", "1.3", "1.4", "1.5", "1.6"])
fix_step_focus("lessons/dsc/L03_du_lieu_thieu.yaml", "check", 1, [1, 1, 2])
fix_step_focus("lessons/dsc/L12_dien_giai_hoi_quy.yaml", "example", 2, ["1.4", 2])
fix_step_focus("lessons/dsc/L12_dien_giai_hoi_quy.yaml", "example", 3, None)
fix_step_focus("lessons/mlo/L08_giam_sat_troi.yaml", "check", 0, [1, "1.2", "1.2", "1.3", "1.4"])

# 3. Fix DSC L08 recap.1 long sentence & focus
p8 = ROOT / "lessons/dsc/L08_thu_nghiem_ab.yaml"
s8 = p8.read_text("utf-8")
old_r8 = "Giảm mức cần thấy xuống 5 lần đẩy cỡ mẫu lên tới 356 nghìn 335 khách mỗi nhóm, tốn gấp khoảng 24 lần thời gian chạy thử nghiệm, còn nhìn trộm 10 lần trên nhóm 1 nghìn khách vẫn gây báo giả 18 phẩy 9 phần trăm."
new_r8 = "Giảm mức cần thấy xuống 5 lần đẩy cỡ mẫu lên tới 356 nghìn 335 khách mỗi nhóm, tốn gấp khoảng 24 lần thời gian chạy thử nghiệm. Nhìn trộm 10 lần trên nhóm 1 nghìn khách vẫn gây báo giả 18 phẩy 9 phần trăm."
assert old_r8 in s8
p8.write_text(s8.replace(old_r8, new_r8), encoding="utf-8")
fix_step_focus("lessons/dsc/L08_thu_nghiem_ab.yaml", "recap", 1, [1, 2, 2, 2])

# 4. Fix DSC L13 check.0 focus + add ~45 words to DSC L13 recap.0 (`w=1636 -> ~1685`)
fix_step_focus("lessons/dsc/L13_rieng_tu_dao_duc.yaml", "check", 0, [0, "1.2", "1.3"])
p13 = ROOT / "lessons/dsc/L13_rieng_tu_dao_duc.yaml"
s13 = p13.read_text("utf-8")
extra_rec13 = " Luôn rà soát cả cột thời gian lẫn địa điểm trước khi xuất bảng tổng hợp, vì sự kết hợp nhiều trường thô nhỏ lẻ vẫn có thể làm hẹp kích thước từng nhóm ẩn danh xuống dưới ngưỡng bảo vệ an toàn."
if extra_rec13.strip() not in s13:
    target_rec = "Khi số cột tăng thêm, luôn chạy kiểm thử kích thước nhóm trước khi phát hành bảng công khai."
    assert target_rec in s13
    p13.write_text(s13.replace(target_rec, target_rec + extra_rec13), encoding="utf-8")

print("REPAIRED 8 FILES + DSC L03/08/12/13 CLEANLY!", flush=True)
