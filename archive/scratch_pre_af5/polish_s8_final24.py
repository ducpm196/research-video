"""Fix final 24 lint/E51/warn items across Stage 8 so 114/114 pass lv.lint 0 FAIL 0 WARN."""
import os
import re
import sys
from pathlib import Path
import yaml

os.environ.setdefault("PYTHONUTF8", "1")
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scratch"))
import lv  # noqa: E402

def _res(rel: str) -> Path:
    p = ROOT / rel
    if p.exists():
        return p
    if rel.startswith("lessons/") and rel.endswith(".yaml"):
        lid = Path(rel).name[:4]
        hits = sorted((ROOT / Path(rel).parent).glob(f"{lid}*.yaml"))
        if hits:
            return hits[0]
    raise FileNotFoundError(rel)


def set_covers(rel: str, pairs: list[tuple[int, str]]) -> None:
    p = _res(rel)
    txt = p.read_text(encoding="utf-8")
    idx = txt.find("\ncovers:\n")
    assert idx != -1, f"covers: missing in {rel}"
    cov = ["covers:\n"] + [f"- objective: {o}\n  scene: {s}\n" for o, s in pairs]
    p.write_text(txt[: idx + 1] + "".join(cov), encoding="utf-8")


def append_to_step(rel: str, scene_id: str, note_html: str, note_say: str, marker: str) -> None:
    p = _res(rel)
    txt = p.read_text(encoding="utf-8")
    if note_html[:35] in txt:
        return
    d = yaml.safe_load(txt)
    sc = next(s for s in d["scenes"] if s["id"] == scene_id)
    last = sc["steps"][-1]
    old_show = str(last.get("show", ""))
    old_say = str(last.get("say", ""))
    new_show = old_show.rstrip("\n") + "\n" + note_html
    blk_target = len(lv.html_units(new_show))
    n_add = max(0, len(lv.sentences(old_say.rstrip() + " " + note_say.strip())) - len(lv.sentences(old_say)))
    new_say = old_say.rstrip() + " " + note_say.strip()

    lines = txt.splitlines(keepends=True)
    in_scene = False
    say_idx = None
    key_prefix = old_say.strip()[:40]
    for i, line in enumerate(lines):
        if re.match(rf"^\s*-\s+id:\s+{re.escape(scene_id)}\b", line):
            in_scene = True
        elif in_scene and re.match(r"^\s*-\s+id:\s+\w+", line):
            in_scene = False
        if in_scene and line.lstrip().startswith("say:") and key_prefix in line:
            say_idx = i
    assert say_idx is not None, f"Could not find say: for {rel} #{scene_id}"
    show_start = show_end = None
    for j in range(say_idx - 1, -1, -1):
        ls = lines[j].lstrip()
        if ls.startswith(("focus:", "introduces:", "notation_note:", "forward_ref:", "pause:", "clear:", "- ")):
            if ls.startswith("- show:"):
                show_start = j
                if show_end is None:
                    show_end = say_idx
                break
            if ls.startswith("- "):
                show_end = j
                continue
            show_end = j
        elif ls.startswith("show:"):
            show_start = j
            if show_end is None:
                show_end = say_idx
            break
    assert show_start is not None and show_end is not None
    show_line = lines[show_start].lstrip()
    if show_line.startswith(("show: |", "show: >-", "- show: |", "- show: >-")):
        indent_html = " " * (len(lines[show_end - 1]) - len(lines[show_end - 1].lstrip()))
        lines[show_end - 1] = lines[show_end - 1].rstrip("\r\n") + "\n" + indent_html + note_html + "\n"
    else:
        lead = len(lines[show_start]) - len(lines[show_start].lstrip())
        prefix = "- " if show_line.startswith("- ") else ""
        lines[show_start] = f"{' '*lead}{prefix}show: |\n{' '*(lead+len(prefix)+2)}{old_show.strip()}\n{' '*(lead+len(prefix)+2)}{note_html}\n"
    indent_say = " " * (len(lines[say_idx]) - len(lines[say_idx].lstrip()))
    safe_say = yaml.safe_dump({"s": new_say}, allow_unicode=True, width=100000).splitlines()[0][3:]
    lines[say_idx] = f"{indent_say}say: {safe_say}\n"
    for j in range(say_idx - 1, show_start, -1):
        if lines[j].lstrip().startswith("focus:"):
            end = j + 1
            while end < say_idx and lines[end].lstrip().startswith("- "):
                end += 1
            indent_f = " " * (len(lines[end - 1]) - len(lines[end - 1].lstrip()))
            lines = lines[:end] + [f"{indent_f}- {blk_target}\n"] * n_add + lines[end:]
            break
    p.write_text("".join(lines), encoding="utf-8")

# 1. DSC L08 recap.1 focus (`focus` sits below `say:` in L08)
p8 = ROOT / "lessons/dsc/L08_thu_nghiem_ab.yaml"
s8 = p8.read_text("utf-8")
old_f8 = "    focus:\n    - 1\n    - 2\n    - 2\n  - clear: true"
new_f8 = "    focus:\n    - 1\n    - 2\n    - 2\n    - 2\n  - clear: true"
assert old_f8 in s8
p8.write_text(s8.replace(old_f8, new_f8), "utf-8")

# 2. DSC L12 example.2 & example.3 focus
p12 = ROOT / "lessons/dsc/L12_dien_giai_hoi_quy.yaml"
s12 = p12.read_text("utf-8")
old_e2 = "    say: Bước ba, với r bằng 0 phẩy 99,"
new_e2 = "    focus:\n    - '1.4'\n    - 2\n    say: Bước ba, với r bằng 0 phẩy 99,"
assert old_e2 in s12
s12 = s12.replace(old_e2, new_e2)
old_e3 = "    say: Bước bốn, lưu ý tổng b 1 cộng b 2 vẫn ổn định,"
new_e3 = "    focus:\n    - 1\n    - 1\n    - 2\n    say: Bước bốn, lưu ý tổng b 1 cộng b 2 vẫn ổn định,"
assert old_e3 in s12
s12 = s12.replace(old_e3, new_e3)
p12.write_text(s12, "utf-8")

# 3. DSC L13 recap.0 long sentence split
p13 = ROOT / "lessons/dsc/L13_rieng_tu_dao_duc.yaml"
s13 = p13.read_text("utf-8")
old_r13 = "Luôn rà soát cả cột thời gian lẫn địa điểm trước khi xuất bảng tổng hợp, vì sự kết hợp nhiều trường thô nhỏ lẻ vẫn có thể làm hẹp kích thước từng nhóm ẩn danh xuống dưới ngưỡng bảo vệ an toàn."
new_r13 = "Luôn rà soát cả cột thời gian lẫn địa điểm trước khi xuất bảng tổng hợp. Nhiều trường thô nhỏ lẻ ghép lại vẫn có thể làm hẹp kích thước từng nhóm xuống dưới ngưỡng an toàn."
assert old_r13 in s13
p13.write_text(s13.replace(old_r13, new_r13), "utf-8")

# 4. CLD L09 example.3 sentence split + extra focus `- 2`
p_cld9 = ROOT / "lessons/cld/L09_can_bang_tai.yaml"
s_c9 = p_cld9.read_text("utf-8")
old_c9 = "So sánh ba thuật toán, vòng tròn dễ lệch khi yêu cầu nặng nhẹ khác nhau, ít kết nối nhất chính xác nhưng tốn trạng thái, còn chọn tốt hơn trong hai gọn nhẹ mà hiệu quả cao."
new_c9 = "So sánh ba thuật toán, vòng tròn dễ lệch khi yêu cầu nặng nhẹ khác nhau. Ít kết nối nhất chính xác nhưng tốn trạng thái, còn chọn tốt hơn trong hai gọn nhẹ mà hiệu quả cao."
assert old_c9 in s_c9
s_c9 = s_c9.replace(old_c9, new_c9)
# Also add one `- 2` at end of example.3 focus
d_c9 = yaml.safe_load(s_c9)
sc_ex = next(s for s in d_c9["scenes"] if s["id"] == "example")
st_last = sc_ex["steps"][-1]
if len(st_last["focus"]) < len(lv.sentences(st_last["say"])):
    lines_c9 = s_c9.splitlines(keepends=True)
    key = "So sánh ba thuật toán"
    for i, l in enumerate(lines_c9):
        if l.lstrip().startswith("say:") and key in l:
            # Find preceding focus list item
            j = i - 1
            while j > 0 and lines_c9[j].lstrip().startswith("- "):
                j -= 1
            if lines_c9[j].lstrip().startswith("focus:"):
                indent = " " * (len(lines_c9[i - 1]) - len(lines_c9[i - 1].lstrip()))
                lines_c9.insert(i, f"{indent}- 2\n")
            break
    s_c9 = "".join(lines_c9)
p_cld9.write_text(s_c9, "utf-8")

# 5. SAR L13 E38 "tỷ" -> "tỉ"
p_s13 = ROOT / "lessons/sar/L13_hanh_trinh_twitter.yaml"
s_s13 = p_s13.read_text("utf-8")
s_s13 = s_s13.replace("tỷ lệ", "tỉ lệ").replace("Tỷ lệ", "Tỉ lệ").replace(" tỷ ", " tỉ ")
p_s13.write_text(s_s13, "utf-8")

# 6. Replace raw foreign acronyms inside `say:` in those 11 Stage 8 lessons with natural Vietnamese
SAY_CLEAN = {
    "lessons/dsc/L09_kiem_dinh_nhieu_lan.yaml": [("FWER.", "tỉ lệ sai toàn họ.")],
    "lessons/evt/L00_su_kien_va_lenh.yaml": [("gọi là bus.", "gọi là kênh sự kiện dùng chung.")],
    "lessons/den/L12_kho_du_lieu.yaml": [("thuật ngữ SCD.", "thuật ngữ chiều thay đổi chậm.")],
    "lessons/clc/L02_mang_ao.yaml": [("gọi là VPC, chia nhỏ", "gọi là mạng riêng biệt lập, chia nhỏ")],
    "lessons/clc/L06_ham_theo_su_kien.yaml": [("là serverless.", "là hàm không tự quản máy chủ.")],
    "lessons/clc/L07_csdl_duoc_quan_ly.yaml": [("viết tắt là WAL.", "gọi là nhật ký ghi trước.")],
    "lessons/clc/L08_chi_phi.yaml": [("người dùng CDN.", "người dùng gần đó.")],
    "lessons/clc/L09_ma_hoa_phong_bi.yaml": [("gọi tắt là KMS.", "gọi là dịch vụ quản lý khoá.")],
    "lessons/sar/L00_thuoc_tinh_chat_luong.yaml": [("gọi là SLO.", "gọi là mục tiêu mức phục vụ.")],
    "lessons/sar/L01_ghi_quyet_dinh.yaml": [("gọi tắt là RDBMS.", "gọi là hệ cơ sở dữ liệu quan hệ.")],
    "lessons/sar/L09_luy_dang.yaml": [("S Q Lite", "cơ sở dữ liệu gọn nhẹ")],
    "lessons/sar/L10_nhat_quan_da_vung.yaml": [("khứ hồi RTT.", "khứ hồi hai lượt.")],
    "lessons/sar/L11_kien_truc_an_toan.yaml": [("S Q Lite", "cơ sở dữ liệu gọn nhẹ")],
}
for rel, pairs in SAY_CLEAN.items():
    p = ROOT / rel
    s = p.read_text("utf-8")
    for old, new in pairs:
        assert old in s, f"{old!r} missing in {rel}"
        s = s.replace(old, new)
    p.write_text(s, "utf-8")

# 7. Enrich 6 `AF2_DO_SCENES` targets & update `covers:` so `lv.lint E51` AND `v3` semantics pass!
MORE_ENRICH = [
    ("lessons/mlo/L03_kiem_thu_he_ml.yaml", "example",
     '<p class="note"><b>Kiểm thử lược đồ và phân bố dữ liệu:</b> luôn khẳng định đủ cột đúng kiểu, giá trị hợp lệ (như tuổi trong khoảng cho phép) và độ lệch phân bố chưa vượt ngưỡng trước khi chấm điểm hành vi.</p>',
     "Trước khi kiểm thử hành vi, cần viết kiểm thử lược đồ kiểm tra đủ cột, đúng miền giá trị và phân bố không lệch bất thường.",
     "Kiểm thử lược đồ và phân bố dữ liệu:"),
    ("lessons/mlo/L12_the_mo_hinh_cong_bang.yaml", "example",
     '<p class="note"><b>Viết thẻ mô hình minh bạch:</b> ghi rõ mục tiêu sử dụng, nguồn dữ liệu, chỉ số tổng kèm bảng tách riêng theo từng nhóm người dùng và các giới hạn không được phép triển khai.</p>',
     "Khi viết thẻ mô hình, hãy ghi rõ mục tiêu dùng, chỉ số tách theo từng nhóm người dùng chứ không chỉ để một con số chung.",
     "Viết thẻ mô hình minh bạch:"),
    ("lessons/mlo/L13_bao_mat_he_ml.yaml", "check",
     '<p class="note"><b>Biện pháp phòng thủ chuỗi cung ứng:</b> kiểm soát nguồn dữ liệu đầu vào, đặt giới hạn tốc độ truy vấn API và luôn kiểm mã băm SHA cùng chữ ký gói trước khi tải trọng số.</p>',
     "Bên cạnh kiểm thử tấn công, cần kiểm soát nguồn dữ liệu, giới hạn truy vấn và xác minh mã băm cùng chữ ký trước khi chạy mô hình.",
     "Biện pháp phòng thủ chuỗi cung ứng:"),
    ("lessons/evt/L04_ghi_nguon_su_kien.yaml", "check",
     '<p class="note"><b>Sửa sai bằng sự kiện bù trừ:</b> khi phát hiện giao dịch hạch toán nhầm, phát thêm một sự kiện điều chỉnh đối xứng để tổng gấp ra số dư đúng thay vì xoá sửa dòng cũ trong nhật ký.</p>',
     "Khi cần sửa sai sót trên dữ liệu bất biến, ta thêm sự kiện bù trừ mới thay vì sửa lịch sử cũ rồi kiểm lại phép gấp.",
     "Sửa sai bằng sự kiện bù trừ:"),
    ("lessons/evt/L05_tach_ghi_doc.yaml", "example",
     '<p class="note"><b>Dựng mô hình đọc từ dòng sự kiện:</b> bộ chiếu đọc tuần tự từng sự kiện từ nhật ký để cập nhật bảng tra cứu tối ưu sẵn cho các câu truy vấn đọc nhanh.</p>',
     "Bộ chiếu đọc tuần tự sự kiện để dựng riêng mô hình đọc nhanh tách biệt với luồng ghi.",
     "Dựng mô hình đọc từ dòng sự kiện:"),
    ("lessons/evt/L10_quan_sat.yaml", "check",
     '<p class="note"><b>Mốc đo độ trễ đúng:</b> lấy hiệu từ thời điểm sự kiện thật sự phát sinh gắn trên thông điệp tới khi hoàn tất xử lý thay vì chỉ đo thời điểm từng dịch vụ nhận được tin.</p>',
     "Luôn đo độ trễ kể từ thời điểm sự kiện phát sinh ban đầu thay vì thời điểm khâu cuối nhận được thông điệp.",
     "Mốc đo độ trễ đúng:"),
]
for rel, sid, nh, ns, mk in MORE_ENRICH:
    append_to_step(rel, sid, nh, ns, mk)

set_covers("lessons/mlo/L03_kiem_thu_he_ml.yaml", [(1, "example"), (2, "example"), (3, "check")])
set_covers("lessons/mlo/L12_the_mo_hinh_cong_bang.yaml", [(1, "example"), (2, "example"), (3, "pitfalls")])
set_covers("lessons/mlo/L13_bao_mat_he_ml.yaml", [(1, "sym"), (2, "example"), (3, "check")])
set_covers("lessons/evt/L04_ghi_nguon_su_kien.yaml", [(1, "example"), (2, "check"), (3, "check")])
set_covers("lessons/evt/L05_tach_ghi_doc.yaml", [(1, "example"), (2, "example"), (3, "pitfalls")])
set_covers("lessons/evt/L10_quan_sat.yaml", [(1, "sym"), (2, "example"), (3, "check")])

# 8. Final verify across ALL 114 Stage 8 lessons (`>= 1650w`, `0` 'càng', `0` E/W lint)
bad = []
for c in ("dan", "dsc", "mlo", "evt", "den", "cld", "clc", "sar"):
    for p in sorted((ROOT / f"lessons/{c}").glob("L*.yaml")):
        txt = p.read_text("utf-8")
        d = yaml.safe_load(txt)
        w = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc["steps"])
        cang = sum(
            len(re.findall(r"\bcàng\b", str(st.get(k) or ""), re.I))
            for sc in d["scenes"] for st in sc["steps"] for k in ("show", "say")
        ) + sum(len(re.findall(r"\bcàng\b", str(o), re.I)) for o in d.get("objectives", []))
        res = lv.lint(d, quiet=True)
        if w < 1650 or cang > 0 or res.errors or res.warnings:
            print(f"FAIL {c.upper()} {d['id']}: w={w} cang={cang} E={res.errors} W={res.warnings}", flush=True)
            bad.append((c.upper(), d["id"], w, cang, res.errors, res.warnings))
print(f"STAGE 8 ALL 114 LESSONS FINAL LINT FAILURES: {len(bad)}", flush=True)
assert not bad, f"Stage 8 still has issues: {bad}"
print("STAGE 8 114/114 LINT 0 FAIL 0 WARN 100% PASS!", flush=True)
