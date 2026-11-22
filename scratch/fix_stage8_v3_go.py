"""Comprehensive v3 -> GO fix script for all 8 Stage 8 courses (114 lessons)."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
import yaml

os.environ.setdefault("PYTHONUTF8", "1")
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit/s9_11"))
import lv  # noqa: E402
import ast_p1  # noqa: E402


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


def append_to_step(rel: str, scene_id: str, note_html: str, note_say: str, marker: str) -> None:
    """Append `note_html` to the last step's `show:` in `scene_id` and `note_say` to its `say:`, recomputing `focus:` via lv."""
    p = _res(rel)
    txt = p.read_text(encoding="utf-8")
    if note_html[:35] in txt:
        return
    d = yaml.safe_load(txt)
    sc = next(s for s in d["scenes"] if s["id"] == scene_id)
    last = sc["steps"][-1]
    old_show = str(last.get("show", ""))
    old_say = str(last.get("say", ""))

    # Recompute exact focus target block using lv helpers
    # First get total blocks before this step (taking `clear:` into account)
    blocks_before = []
    for st in sc["steps"][:-1]:
        if st.get("clear"):
            blocks_before = []
        if st.get("show"):
            blocks_before.append(lv.html_units(str(st["show"])))

    if last.get("clear"):
        blocks_before = []
    new_show = old_show.rstrip("\n") + "\n" + note_html
    units_in_last = lv.html_units(new_show)
    if note_html.startswith("<p class=\"note\">") and "<table" not in old_show and not blocks_before:
        blk_target = len(units_in_last)
    elif len(blocks_before) > 0:
        # `focus` without B prefix targets last block (the current step's show)
        blk_target = len(units_in_last)
    else:
        blk_target = len(units_in_last)

    old_n_sents = len(lv.sentences(old_say))
    new_say = old_say.rstrip() + " " + note_say.strip()
    new_n_sents = len(lv.sentences(new_say))
    n_add = max(0, new_n_sents - old_n_sents)

    # Locate the exact `say:` line in the file matching `scene_id` + last step
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
    assert say_idx is not None, f"Could not find say: for {rel} #{scene_id} ({key_prefix!r})"

    # Insert note_html at end of `show:` block right before metadata keys / focus / say
    show_start = None
    show_end = None
    for j in range(say_idx - 1, -1, -1):
        ls = lines[j].lstrip()
        if ls.startswith(("focus:", "introduces:", "notation_note:", "forward_ref:", "pause:", "clear:", "- ")):
            # Skip focus list items (`- 1`, `- '1.2'`)
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
    assert show_start is not None and show_end is not None, f"show bounds not found in {rel} #{scene_id}"

    show_line = lines[show_start].lstrip()
    if show_line.startswith(("show: |", "show: >-", "- show: |", "- show: >-")):
        indent_html = " " * (len(lines[show_end - 1]) - len(lines[show_end - 1].lstrip()))
        lines[show_end - 1] = lines[show_end - 1].rstrip("\r\n") + "\n" + indent_html + note_html + "\n"
    else:
        # Single-line quoted/plain show: convert cleanly to multiline `show: |`
        lead = len(lines[show_start]) - len(lines[show_start].lstrip())
        prefix = "- " if show_line.startswith("- ") else ""
        indent_key = " " * lead
        body_indent = " " * (lead + len(prefix) + 2)
        lines[show_start] = f"{indent_key}{prefix}show: |\n{body_indent}{old_show.strip()}\n{body_indent}{note_html}\n"

    # Update `say:` cleanly using YAML double/plain escaping (preserving single-line format cleanly)
    indent_say = " " * (len(lines[say_idx]) - len(lines[say_idx].lstrip()))
    safe_say = yaml.safe_dump({"s": new_say}, allow_unicode=True, width=100000).splitlines()[0][3:]
    lines[say_idx] = f"{indent_say}say: {safe_say}\n"

    # Update `focus:` if present in last step
    for j in range(say_idx - 1, show_start, -1):
        if lines[j].lstrip().startswith("focus:"):
            foc_line = lines[j].lstrip()
            if "[" in foc_line:
                # Inline list e.g. `focus: [1, 2]`
                arr = list(last["focus"]) + [blk_target] * n_add
                indent_f = " " * (len(lines[j]) - len(lines[j].lstrip()))
                lines[j] = f"{indent_f}focus: {arr}\n"
            else:
                end = j + 1
                while end < say_idx and lines[end].lstrip().startswith("- "):
                    end += 1
                indent_f = " " * (len(lines[end - 1]) - len(lines[end - 1].lstrip()))
                lines = lines[:end] + [f"{indent_f}- {blk_target}\n"] * n_add + lines[end:]
            break

    p.write_text("".join(lines), encoding="utf-8")


def add_practice_rows(rel: str, extra_rows: list[tuple[str, str]]) -> None:
    """Append extra `[<code>...</code>, desc]` rows to the last reading-code table before reference code."""
    p = _res(rel)
    txt = p.read_text(encoding="utf-8")
    row_html = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in extra_rows)
    if all(k in txt for k, _ in extra_rows):
        return
    # Add into the LAST `viết trong mã` table
    marker = "viết trong mã</th><th>đọc và hiểu là</th></tr>"
    idx = txt.rfind(marker)
    assert idx != -1, f"reading-code table not found in {rel}"
    close_tbl = txt.find("</table>", idx)
    assert close_tbl != -1, f"</table> not found in {rel}"
    new_rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in extra_rows if k not in txt[idx:close_tbl])
    p.write_text(txt[:close_tbl] + new_rows + txt[close_tbl:], encoding="utf-8")


def set_covers(rel: str, pairs: list[tuple[int, str]]) -> None:
    p = _res(rel)
    txt = p.read_text(encoding="utf-8")
    idx = txt.find("\ncovers:\n")
    assert idx != -1, f"covers: missing in {rel}"
    cov = ["covers:\n"] + [f"- objective: {o}\n  scene: {s}\n" for o, s in pairs]
    p.write_text(txt[: idx + 1] + "".join(cov), encoding="utf-8")


def replace_pairs(rel: str, pairs: list[tuple[str, str]]) -> None:
    p = _res(rel)
    txt = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in txt:
            txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")


# 1. Remove ALL non-code `" vs "` in Stage 8 lessons & labs/de.md
for c in ("dan", "dsc", "mlo", "evt", "den", "cld", "clc", "sar"):
    for p in sorted(list((ROOT / f"lessons/{c}").glob("L*.yaml")) + list((ROOT / f"labs/{c}").glob("L*/de.md"))):
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        changed = False
        for i, l in enumerate(lines):
            if " vs " in l and "<code>" not in l and "<div>" not in l:
                lines[i] = l.replace(" vs ", " so với ")
                changed = True
        if changed:
            p.write_text("".join(lines), encoding="utf-8")

# 2. Text / Lab / Code / Spelling / Recap direct fixes
DIRECT_REPLACES = {
    "lessons/dan/L06_chuoi_thoi_gian.yaml": [("hòa hợp", "hoà hợp"), ("hòa ", "hoà "), ("hòa,", "hoà,")],
    "lessons/dsc/L03_du_lieu_thieu.yaml": [
        ("(< 1 giây)", "(&lt; 1 giây)"),
        ("Ở hai mức quy mô, dãy 6 số thiếu 2 ô làm phương sai tụt còn 0 phẩy 6 lần. Trên bảng 1 triệu dòng thiếu 30 phần trăm, điền trung bình chạy xong trong 1 giây nhưng làm phương sai tụt còn 0 phẩy 7 lần.", ""),
        ("xóa ", "xoá "), ("Xóa ", "Xoá "),
    ],
    "lessons/dsc/L04_thong_ke_ben_vung.yaml": [("hóa đơn", "hoá đơn"), ("xóa ", "xoá "), ("Xóa ", "Xoá ")],
    "lessons/dsc/L13_rieng_tu_dao_duc.yaml": [
        ('\n      <p class="note">Bảng 4 dòng đạt 2-ẩn danh trong dưới 1 mi-li-giây; trên 10 triệu hồ sơ y tế 20 cột, ẩn danh hoá tốn thời gian sắp xếp hơn và nhiều cột định danh buộc phải gộp nhóm thô hơn.</p>', ""),
        ('\n      <p class="note">Bảng 4 dòng đạt 2-ẩn danh dưới 1 mi-li-giây; trên 10 triệu hồ sơ 20 cột, ẩn danh hoá tốn nhiều thời gian sắp xếp hơn và phải gộp nhóm thô hơn.</p>', ""),
        (" Ở hai mức quy mô, bảng 4 dòng đạt 2 ẩn danh trong dưới 1 mi li giây. Trên 10 triệu hồ sơ y tế 20 cột, ẩn danh hoá tốn thời gian sắp xếp hơn và nhiều cột định danh buộc phải gộp nhóm thô hơn.", ""),
        ("    - 1\n    - '1.2'\n    - '1.3'\n    - 2\n    - 2", "    - 1\n    - '1.2'\n    - '1.3'"),
        ("xóa ", "xoá "), ("Xóa ", "Xoá "),
    ],
    "lessons/dsc/L08_thu_nghiem_ab.yaml": [
        ("gấp 25 lần nhưng nhìn trộm vẫn báo giả.",
         "tới 356 nghìn 335 khách mỗi nhóm, tốn gấp khoảng 24 lần thời gian chạy thử nghiệm, còn nhìn trộm 10 lần trên nhóm 1 nghìn khách vẫn gây báo giả 18 phẩy 9 phần trăm."),
    ],
    "lessons/dsc/L10_ro_ri_du_lieu.yaml": [
        ("tạo độ đúng ảo hơn 80 phần trăm.", "tạo độ đúng ảo tới 88 phẩy 9 phần trăm."),
    ],
    "lessons/dsc/L11_ti_le_nen.yaml": [
        ("- id: cost\n  kind: concept\n", "- id: cost\n  kind: example\n"),
    ],
    "labs/dsc/L01/de.md": [
        ("`30°C / 15°C = 2.0x`", "`30°C` và `15°C`"),
    ],
    "labs/dsc/L15/de.md": [
        ("căn(0.8558^2 + round(2*800/(2817131/2), 5)) - 0.8558",
         "giữa ngưỡng gốc `0.8558` và biên độ ước lượng từ `800` tham số trộn trên một nửa tập `2 817 131` dòng (làm tròn phần phương sai phụ `5` chữ số trước khi khai căn)"),
    ],
    "labs/mlo/L01/de.md": [
        ("trong `random.Random(seed).sample(range(12), 5)`",
         "với bộ sinh giả ngẫu nhiên có hạt giống riêng trong thư viện chuẩn `random` để rút ngẫu nhiên `5` phần tử không lặp từ dãy `0..11`"),
    ],
    "labs/mlo/L06/de.md": [
        ("`first_wait_ms=<số nguyên> single_rps=<số nguyên> batch_rps=<số nguyên>`",
         "`first_wait_ms=<số nguyên> single_rps=<số nguyên làm tròn bằng round> batch_rps=<số nguyên làm tròn bằng round>`"),
    ],
    "labs/mlo/L09/de.md": [
        ("`top-2`", "`top-2`, nếu hoà điểm ưu tiên mục có chỉ số nhỏ hơn"),
    ],
    "labs/mlo/L10/de.md": [
        ("công thức trung bình bình phương hiệu `(p - y)^2`",
         "trung bình của bình phương độ lệch giữa xác suất dự đoán và nhãn thật"),
    ],
    "labs/mlo/L14/de.md": [
        ("`4 * 3 * 2` tổ hợp cấu hình triển khai",
         "tổ hợp từ `4` họ đặc trưng, `3` mức tài nguyên và `2` vùng triển khai"),
    ],
    "lessons/mlo/L03_kiem_thu_he_ml.yaml": [("mất < 1 ms", "mất &lt; 1 ms")],
    "lessons/mlo/L13_bao_mat_he_ml.yaml": [("(< 5%)", "(&lt; 5%)")],
    "labs/evt/L00/de.md": [
        ("điểm–điểm `N*(N-1)//2` so với qua 1 kênh sự kiện trung tâm `N`",
         "điểm–điểm nối từng cặp trong `N` dịch vụ so với nối qua 1 kênh sự kiện trung tâm"),
    ],
    "lessons/evt/L00_su_kien_va_lenh.yaml": [
        ("liên kết điểm–điểm theo N*(N-1)/2 xuống N kết nối",
         "số đường nối giữa từng cặp dịch vụ so với gom qua 1 kênh sự kiện trung tâm"),
    ],
    "labs/evt/L04/de.md": [
        ("dựng lại số dư qua ảnh chụp", "dựng lại số dư qua ảnh chụp trạng thái (snapshot)"),
    ],
    "labs/evt/L05/de.md": [
        ("(`tồn / tốc độ ghi`)", "(lượng tồn chia cho nhịp ghi mỗi giây)"),
    ],
    "labs/evt/L09/de.md": [
        ("So sánh ước lượng sai (quên dòng mới) với thời gian đuổi kịp thực tế.",
         "So sánh ước lượng sai (quên dòng mới) với thời gian đuổi kịp thực tế (làm tròn 1 chữ số thập phân)."),
    ],
    "lessons/evt/L10_quan_sat.yaml": [
        ("(A → max(B, C) → D = 90 ms)", "[A → nhánh chậm nhất giữa B, C → D = 90 ms]"),
    ],
    "lessons/evt/L11_hanh_trinh_nhat_ky_su_kien.yaml": [
        ("mỗi ngày ghi 1 TB, muốn chịu 1 máy hỏng.</p>",
         "mỗi ngày ghi 1 TB (quy ước 1 TB = 1 000 GB), muốn chịu 1 máy hỏng.</p>"),
        ("      focus:\n      - 1\n      - 1\n      say: Điều cần mang theo, mỗi thực hành tốt là câu trả lời cho một điểm nghẽn ở một quy mô cụ thể. Hệ này thắng nhờ một ý đơn giản, nhật ký có vị trí, và cuối cùng áp chính ý đó cho bản thân nó.",
         "      focus:\n      - 1\n      - 1\n      - 2\n      - 2\n      say: Điều cần mang theo, mỗi thực hành tốt là câu trả lời cho một điểm nghẽn ở một quy mô cụ thể. Hệ này thắng nhờ một ý đơn giản, nhật ký có vị trí, và cuối cùng áp chính ý đó cho bản thân nó. Ở hai mức quy mô, hệ nhỏ 1 nghìn tin mỗi giây chỉ cần một cụm gọn nhẹ. Tới 1 tỉ tin mỗi ngày cần gom lô năm mươi tin, còn lên 800 tỉ tin mỗi ngày mới phải tách cụm nhiều tầng và đếm kiểm từng chặng."),
    ],
    "labs/cld/L05/de.md": [
        ("số lượng bản mong muốn (`desired`) và đang chạy (`running`)",
         "số bản mong muốn (`desired`, tức số bản khai báo cần có) và đang chạy (`running`)"),
    ],
    "labs/cld/L09/de.md": [
        ("so với (P2C)", "so với chọn tốt hơn trong hai ngẫu nhiên (Power of Two Choices, viết tắt P2C)"),
        ("hai bước ngẫu nhiên (P2C)", "chọn tốt hơn trong hai ngẫu nhiên (Power of Two Choices, P2C)"),
    ],
    "labs/cld/L15/de.md": [
        ("ở điểm giữa `25%` (`2 500` máy)", "ở điểm giữa `25%`"),
        ("cửa sổ cập nhật lớn `14 400` phút (tỉ lệ `0.07%`)", "cửa sổ cập nhật lớn `14 400` phút"),
    ],
    "lessons/cld/L15_hanh_trinh_borg_kubernetes.yaml": [
        ("    focus:\n    - 1\n    - 1\n    say: Điều cần mang theo, mỗi thực hành tốt là câu trả lời cho một điểm nghẽn ở một quy mô cụ thể. Trước khi áp dụng, hãy hỏi điểm nghẽn đó đã xuất hiện ở hệ của mình chưa, và đo được bằng con số nào.",
         "    focus:\n    - 1\n    - 1\n    - 2\n    - 2\n    say: Điều cần mang theo, mỗi thực hành tốt là câu trả lời cho một điểm nghẽn ở một quy mô cụ thể. Trước khi áp dụng, hãy hỏi điểm nghẽn đó đã xuất hiện ở hệ của mình chưa, và đo được bằng con số nào. Ở hai mức quy mô, nhóm nhỏ vài dịch vụ chưa cần bộ điều khiển phức tạp. Trên cụm 10 nghìn máy kiểu Borg dùng chung tiết kiệm 20 tới 30 phần trăm máy, còn tách cụm riêng cho nhóm 200 máy cần thêm máy dự phòng để đổi lấy cách ly lỗi."),
    ],
    "lessons/clc/L00_dam_may_la_gi.yaml": [
        ("dù thuê hạ tầng (3 lớp tự quản), nền tảng (2 lớp) hay phần mềm (1 lớp)",
         "dù thuê hạ tầng (4 lớp tự quản trên phần cứng), nền tảng (2 lớp) hay phần mềm (1 lớp)"),
    ],
    "labs/clc/L00/de.md": [
        ("ở hạ tầng như dịch vụ (`IaaS`: 4 lớp trên phần cứng), nền tảng như dịch vụ (`PaaS`: 2 lớp trên cùng), hàm theo sự kiện (`FaaS`: 2 lớp hàm & dữ liệu), phần mềm như dịch vụ (`SaaS`: 1 lớp dữ liệu) và mức chênh lệch giữa `IaaS` với `SaaS`.",
         "cho bốn mô hình: hạ tầng như dịch vụ (`IaaS`: khách hàng tự quản các lớp phía trên phần cứng), nền tảng như dịch vụ (`PaaS`: chỉ tự quản mã ứng dụng và dữ liệu), hàm theo sự kiện (`FaaS`: chỉ tự quản mã hàm ở lớp ứng dụng và dữ liệu), phần mềm như dịch vụ (`SaaS`: chỉ tự quản lớp dữ liệu), rồi tính mức chênh lệch số lớp giữa `IaaS` và `SaaS`."),
    ],
    "labs/clc/L03/de.md": [
        ("Kiểm thử 3 trường hợp trên bộ quyền cụ thể.",
         "Kiểm thử 3 trường hợp trên hai bộ quyền `p_ro = [('Allow', {'s3:GetObject'})]` và `p_mix = [('Allow', {'*'}), ('Deny', {'ec2:TerminateInstances'})]`: kiểm tra `'s3:GetObject'` với `p_ro` (`read_allow`), `'ec2:TerminateInstances'` với `p_mix` (`terminate_deny`) và `'iam:PassRole'` với `p_ro` (`unmatched_default`)."),
    ],
    "labs/clc/L12/de.md": [
        ("từ `09:37` tới `13:54` (`257` phút).", "từ `09:37` tới `13:54` cùng ngày."),
    ],
    "lessons/clc/L12_hanh_trinh_luu_tru_doi_tuong.yaml": [
        ("    focus:\n    - 1\n    - 1\n    say: Điều cần mang theo, ở quy mô lớn, thứ hay hỏng nhất không phải máy mà là việc hiếm khi làm, như khởi động lại toàn bộ hay lệnh gỡ hàng loạt. Hãy cho công cụ tự chặn, và thử khôi phục ở đúng quy mô hiện tại.",
         "    focus:\n    - 1\n    - 1\n    - 2\n    - 2\n    say: Điều cần mang theo, ở quy mô lớn, thứ hay hỏng nhất không phải máy mà là việc hiếm khi làm, như khởi động lại toàn bộ hay lệnh gỡ hàng loạt. Hãy cho công cụ tự chặn, và thử khôi phục ở đúng quy mô hiện tại. Ở hai mức quy mô, năm 2006 hệ khởi đầu với 800 triệu đối tượng và sự cố 257 phút năm 2017 buộc phải dựng rào chắn. Tới quy mô 200 nghìn tỉ đối tượng năm 2022, mọi công cụ vận hành đều phải có ngưỡng tự chặn và diễn tập đúng cỡ thật."),
    ],
    "labs/sar/L06/de.md": [
        ("và tỉ số thời gian gián đoạn giữa nối tiếp với song song.",
         "và tỉ số thời gian gián đoạn giữa nối tiếp với song song theo công thức `(1 - series) / (1 - parallel)` (làm tròn tới số nguyên gần nhất bằng `round`)."),
    ],
    "labs/sar/L07/de.md": [
        ("Mô phỏng từng giây trong `4` giây (`0..4` s) nhận tổng `3 200` yêu cầu dồn vào (`800` yêu cầu/s ở 4 đợt, kiểm tra lượng token khả dụng tích lũy theo quy tắc thùng token),",
         "Mô phỏng theo 5 mốc `t = 0..4`: tại `t = 0` lấy ngay lượng token sẵn có trong thùng cho lượt khởi đầu, sau đó ở mỗi giây `t = 1..4` nạp thêm `rate = 15` token rồi tiếp nhận từ đợt `800` yêu cầu/giây trên tổng lưu lượng chuẩn `3 200` yêu cầu,"),
    ],
    "labs/sar/L09/de.md": [
        (", xác nhận số dư cuối cùng còn `275`.", ", rồi in số lần thử, số lần ghi nhận đúng một lần và số dư cuối cùng."),
    ],
    "labs/sar/L10/de.md": [
        ("độ trễ truyền một chiều `36 ms` (vòng khứ hồi `RTT = 2 * 36 = 72 ms`).",
         "độ trễ truyền một chiều `36 ms` (lưu ý khứ hồi `RTT` đi và về gồm hai lượt truyền)."),
    ],
    "labs/sar/L11/de.md": [
        ("có bảng `invoices(amt INT)` chứa giá trị `950`, bật chế độ chỉ đọc (`PRAGMA query_only = ON`). Kiểm chứng lệnh đọc `SELECT` trả về đúng `950`, còn lệnh `DELETE` ném ngoại lệ `OperationalError` để khoanh vùng thiệt hại.",
         "tạo một bảng hoá đơn chứa số tiền `950`, sau đó bật chế độ chỉ đọc (read-only pragma) của SQLite. Kiểm chứng lệnh đọc vẫn lấy ra đúng số tiền `950` (`read_allowed = 1`), còn lệnh xoá bị chặn ném ngoại lệ lỗi vận hành (`write_blocked = 1`), qua đó chứng minh phạm vi thiệt hại đã được khoanh vùng (`blast_contained = 1`)."),
    ],
    "labs/sar/L13/de.md": [
        ("mỗi bài `250 byte` (`200 GB/ngày`),", "mỗi bài `250 byte` (tính theo `1 GB = 10^9 byte`),"),
    ],
}

for rel, pairs in DIRECT_REPLACES.items():
    replace_pairs(rel, pairs)

# 3. Handle `EVT L11 recap#1` whitespace cleanly (YAML indent 4 or 6)
p_evt11 = ROOT / "lessons/evt/L11_hanh_trinh_nhat_ky_su_kien.yaml"
t_evt11 = p_evt11.read_text(encoding="utf-8")
old_e11 = "    focus:\n    - 1\n    - 1\n    say: Điều cần mang theo, mỗi thực hành tốt là câu trả lời cho một điểm nghẽn ở một quy mô cụ thể. Hệ này thắng nhờ một ý đơn giản, nhật ký có vị trí, và cuối cùng áp chính ý đó cho bản thân nó."
new_e11 = "    focus:\n    - 1\n    - 1\n    - 2\n    - 2\n    say: Điều cần mang theo, mỗi thực hành tốt là câu trả lời cho một điểm nghẽn ở một quy mô cụ thể. Hệ này thắng nhờ một ý đơn giản, nhật ký có vị trí, và cuối cùng áp chính ý đó cho bản thân nó. Ở hai mức quy mô, hệ nhỏ 1 nghìn tin mỗi giây chỉ cần một cụm gọn nhẹ. Tới 1 tỉ tin mỗi ngày cần gom lô năm mươi tin, còn lên 800 tỉ tin mỗi ngày mới phải tách cụm nhiều tầng và đếm kiểm từng chặng."
if old_e11 in t_evt11:
    p_evt11.write_text(t_evt11.replace(old_e11, new_e11), encoding="utf-8")

# 4. Sync `DSC L00` practice[2] (ast_p1) + practice[3] (loi_giai.py)
dsc00_p = ROOT / "lessons/dsc/L00_quy_trinh.yaml"
dsc00_s = dsc00_p.read_text(encoding="utf-8")
old_d00_code = '<div>obs_diff = (seen_cnt / seen_n) - (unseen_cnt / unseen_n)</div><div>print(f"obs_diff={obs_diff:.2f} needs_randomization=1")</div></div>'
new_d00_code = '<div>is_observational = 1</div><div>obs_diff = (seen_cnt / seen_n) - (unseen_cnt / unseen_n)</div><div>print(f"obs_diff={obs_diff:.2f} needs_randomization={int(is_observational == 1)}")</div></div>'
if old_d00_code in dsc00_s:
    dsc00_s = dsc00_s.replace(old_d00_code, new_d00_code)
    dsc00_p.write_text(dsc00_s, encoding="utf-8")
add_practice_rows("lessons/dsc/L00_quy_trinh.yaml", [
    ("<code>== / !=</code>", "So sánh hai vế, kiểm tra rỗng bằng <code>is None</code> hoặc kẹp khoảng trả về Đúng/Sai"),
    ("<code>int(x)</code>", "Chuyển giá trị sang số nguyên (chẳng hạn đổi True/False thành 1/0)"),
])

# 5. Add extra library/SQLite tokens to `practice` reading-code tables (P1)
PRACTICE_ROWS = {
    "lessons/dan/L02_noi_nhan_dong.yaml": [
        ("<code>sqlite3 / .connect(':memory:')</code>", "Mở cơ sở dữ liệu SQLite tạm chạy thẳng trên bộ nhớ (RAM)"),
        ("<code>CREATE TABLE / INSERT INTO / .executescript() / .fetchone()</code>", "Câu lệnh SQL tạo bảng, chèn dòng dữ liệu, chạy nhiều lệnh SQL và lấy 1 dòng kết quả"),
    ],
    "lessons/dan/L03_ham_cua_so.yaml": [
        ("<code>sqlite3 / .connect(':memory:')</code>", "Mở cơ sở dữ liệu SQLite tạm chạy thẳng trên bộ nhớ (RAM)"),
        ("<code>CREATE TABLE / INSERT INTO / .executemany() / .fetchall()</code>", "Câu lệnh SQL tạo bảng, chèn hàng loạt dòng dữ liệu và lấy toàn bộ dòng kết quả"),
    ],
    "lessons/den/L10_hop_thu_di.yaml": [
        ("<code>sqlite3 / .connect(':memory:')</code>", "Mở cơ sở dữ liệu SQLite tạm chạy trên bộ nhớ (RAM)"),
        ("<code>CREATE TABLE / INSERT INTO / SELECT / ROLLBACK</code>", "Câu lệnh SQL tạo bảng, chèn dòng, truy vấn và huỷ giao dịch hoàn tác trạng thái"),
    ],
    "lessons/den/L12_kho_du_lieu.yaml": [
        ("<code>sqlite3 / .connect(':memory:')</code>", "Mở cơ sở dữ liệu SQLite tạm chạy trên bộ nhớ (RAM)"),
        ("<code>CREATE TABLE / INSERT INTO / SELECT / BETWEEN</code>", "Câu lệnh SQL tạo bảng, chèn dòng, truy vấn và lọc giá trị nằm trong khoảng ngày"),
    ],
    "lessons/clc/L02_mang_ao.yaml": [
        ("<code>ipaddress / IPv4Network</code>", "Thư viện chuẩn xử lý mạng IPv4 từ ký hiệu dải mạng CIDR"),
        ("<code>.subnets(new_prefix=...) / .num_addresses</code>", "Chia dải mạng cha thành các mạng con có tiền tố mới và đếm số địa chỉ mỗi mạng con"),
    ],
    "lessons/sar/L05_phan_manh.yaml": [
        ("<code>math.ceil(x)</code>", "Làm tròn lên số nguyên gần nhất sao cho đủ chỗ chứa không bị thiếu nút"),
    ],
    "lessons/sar/L09_luy_dang.yaml": [
        ("<code>sqlite3 / .connect(':memory:') / PRIMARY KEY</code>", "Mở cơ sở dữ liệu SQLite tạm và đặt cột khoá chính duy nhất chống chèn trùng"),
        ("<code>CREATE TABLE / INSERT INTO / SELECT / UPDATE</code>", "Câu lệnh SQL tạo bảng, chèn dữ liệu, truy vấn kiểm tra và cập nhật số dư"),
        ("<code>IntegrityError / try / except / .fetchone()</code>", "Bắt ngoại lệ vi phạm khoá duy nhất trong khối <code>try/except</code> và đọc 1 dòng kết quả"),
    ],
    "lessons/sar/L11_kien_truc_an_toan.yaml": [
        ("<code>sqlite3 / PRAGMA query_only</code>", "Mở SQLite và bật cờ <code>PRAGMA query_only</code> khoá kết nối sang chế độ chỉ đọc"),
        ("<code>CREATE TABLE / INSERT INTO / SELECT / DELETE</code>", "Câu lệnh SQL tạo bảng hoá đơn, chèn dữ liệu, truy vấn đọc và thử lệnh xoá"),
        ("<code>OperationalError / try / except / .fetchone()</code>", "Bắt ngoại lệ lỗi thao tác khi kết nối chỉ đọc chặn ghi và đọc 1 dòng kết quả"),
    ],
}
for rel, rows in PRACTICE_ROWS.items():
    add_practice_rows(rel, rows)

# 6. Move `DEN L00..L14` `Hai mức quy mô` from hook#0 -> recap#1 cleanly
for p in sorted((ROOT / "lessons/den").glob("L*.yaml")):
    txt = p.read_text(encoding="utf-8")
    d = yaml.safe_load(txt)
    hook0 = d["scenes"][0]["steps"][0]
    recap = next(s for s in d["scenes"] if s["id"] == "recap")
    rec1 = recap["steps"][1]
    if "Hai mức quy mô:" in str(rec1.get("show", "")):
        continue
    m = re.search(r'<p class="note"><b>Hai mức quy mô:</b>.*?</p>', str(hook0.get("show", "")), re.DOTALL)
    assert m, f"Hai mức quy mô not found in hook#0 of {p.name}"
    note_tag = m.group(0)

    # Remove note_tag from hook#0.show
    new_hook_show = str(hook0["show"]).replace("\n" + note_tag, "").replace(note_tag, "")
    n_units_hook = len(lv.html_units(new_hook_show))
    old_hook_foc = hook0.get("focus") or []
    new_hook_foc = [x if not (isinstance(x, int) and x > n_units_hook) else n_units_hook for x in old_hook_foc]

    # Add note_tag to rec1.show and compute exact rec1.focus
    new_rec_show = str(rec1["show"]).rstrip() + "\n" + note_tag + "\n"
    n_sents_rec = len(lv.sentences(str(rec1["say"])))
    # Check if rec1.show block 1 is box key and block 2 is Hai muc quy mo
    # First sentence (1 or 2 sentences until "Hai mức quy mô" mention) maps to block 1, remaining to block 2
    rec_sents = lv.sentences(str(rec1["say"]))
    split_idx = None
    for idx_s, sent in enumerate(rec_sents):
        if "hai mức quy mô" in sent.lower() or "quy mô" in sent.lower() and idx_s >= 1:
            split_idx = idx_s
            break
    if split_idx is None:
        split_idx = 1
    new_rec_foc = [1] * split_idx + [2] * (n_sents_rec - split_idx)

    # Apply edits to raw text safely via exact YAML line replacement
    lines = txt.splitlines(keepends=True)
    # 6a. Replace hook0 focus + remove note_tag
    txt2 = txt.replace("\n" + note_tag, "").replace(note_tag, "")
    if old_hook_foc:
        # Update hook0 focus block in lines
        # Re-read first `focus:` occurrence before `say:`
        lines2 = txt2.splitlines(keepends=True)
        for idx_l, ln in enumerate(lines2):
            if ln.lstrip().startswith("focus:") and idx_l < 120:
                end = idx_l + 1
                while end < len(lines2) and lines2[end].lstrip().startswith("- "):
                    end += 1
                indent_f = " " * (len(lines2[idx_l]) - len(lines2[idx_l].lstrip()))
                item_indent = indent_f + "- "
                if end > idx_l + 1:
                    item_indent = " " * (len(lines2[idx_l + 1]) - len(lines2[idx_l + 1].lstrip())) + "- "
                repl_f = [f"{indent_f}focus:\n"] + [f"{item_indent}{x}\n" for x in new_hook_foc]
                lines2 = lines2[:idx_l] + repl_f + lines2[end:]
                break
        txt2 = "".join(lines2)

    # 6b. Append note_tag + focus into recap#1
    old_rec_box_match = re.search(r'(<div class="box key">.*?</div>)', str(rec1["show"]), re.DOTALL)
    assert old_rec_box_match, f"box key missing in {p.name}"
    box_str = old_rec_box_match.group(1)
    idx_rec = txt2.rfind("- id: recap")
    assert idx_rec != -1
    idx_box = txt2.find(box_str, idx_rec)
    assert idx_box != -1, f"box_str not found in recap of {p.name}"
    # Find line indent at box_str
    line_start = txt2.rfind("\n", 0, idx_box) + 1
    box_indent = " " * (idx_box - line_start)
    after_box = idx_box + len(box_str)
    # Find next `say:` after idx_box to insert `focus:` right before `say:`
    idx_say_rec = txt2.find("\n", after_box)
    # Insert note_tag after box_str
    txt2 = txt2[:after_box] + "\n" + box_indent + note_tag + txt2[after_box:]
    idx_say_rec = txt2.find("say:", idx_box)
    line_say_start = txt2.rfind("\n", 0, idx_say_rec) + 1
    say_indent = " " * (idx_say_rec - line_say_start)
    foc_yaml = f"{say_indent}focus:\n" + "".join(f"{say_indent}- {x}\n" for x in new_rec_foc)
    txt2 = txt2[:line_say_start] + foc_yaml + txt2[line_say_start:]
    p.write_text(txt2, encoding="utf-8")

# 7. Enrich `P1` terms and `covers:` pedagogical notes cleanly via `append_to_step`!
ENRICH_S8 = [
    # DAN
    ("lessons/dan/L02_noi_nhan_dong.yaml", "sym",
     '<p class="note"><b>Ghi chú thuật ngữ:</b> quan hệ <b>1–N</b> (một–nhiều) nghĩa là một dòng bảng cha khớp nhiều dòng bảng con; trong Python, <code>sqlite3.connect(\':memory:\')</code> mở cơ sở dữ liệu tạm ngay trong bộ nhớ (<b>RAM</b>).</p>',
     "Về thuật ngữ thực hành, quan hệ một nhiều nghĩa là một đơn khớp nhiều dòng, và cờ mở cơ sở dữ liệu tạm chạy ngay trong bộ nhớ RAM.",
     "Ghi chú thuật ngữ:"),
    ("lessons/dan/L03_ham_cua_so.yaml", "check",
     '<p class="note"><b>Chọn hàm xếp hạng khi đồng hạng:</b> cùng giá trị có thể cho số thứ tự khác nhau với <code>ROW_NUMBER()</code>, cùng hạng và nhảy bậc với <code>RANK()</code>, hoặc cùng hạng không nhảy bậc với <code>DENSE_RANK()</code>.</p>',
     "Khi có giá trị bằng nhau, chọn đánh số thứ tự liên tiếp, xếp cùng hạng có nhảy bậc hay cùng hạng không nhảy bậc tuỳ bài toán.",
     "Chọn hàm xếp hạng"),
    ("lessons/dan/L04_nhom_nguoi_dung.yaml", "sym",
     '<p class="note"><b>Ghi chú thuật ngữ:</b> tỉ lệ giữ chân theo nhóm đồng kỳ gọi tắt tiếng Anh là <b>cohort retention</b>; các cột <b>T1</b>, <b>T2</b> ký hiệu tháng thứ nhất và tháng thứ hai kể từ lúc đăng ký.</p>',
     "Tỉ lệ giữ chân theo nhóm đăng ký cùng kỳ được ghi theo từng kỳ T1, T2 sau tháng đầu.",
     "cohort retention"),
    ("lessons/dan/L12_hanh_trinh_thu_nghiem_ab.yaml", "sym",
     '<p class="note"><b>Ngưỡng ý nghĩa thống kê (alpha):</b> bài dùng mức alpha bằng 0,025 mỗi nhánh (ứng với mức lỗi loại một hai phía 0,05).</p>',
     "Bài còn dùng ký hiệu chữ Hy Lạp an-pha làm ngưỡng mức ý nghĩa, với giá trị không phẩy không hai lăm.",
     "Ngưỡng ý nghĩa thống kê (alpha)"),
    ("lessons/dan/L07_du_bao_co_so.yaml", "check",
     '<p class="note"><b>Chọn thước đo sai số:</b> dùng <b>MAE</b> khi cần đọc sai số theo đúng đơn vị doanh số hoặc khi có giá trị gần 0; chỉ dùng <b>MAPE</b> khi cần tỉ lệ phần trăm và các giá trị thật đều dương lớn.</p>',
     "Khi chọn thước đo sai số, ưu tiên sai số tuyệt đối trung bình để giữ nguyên đơn vị, còn phần trăm sai số chỉ dùng khi mẫu số đủ lớn khác không.",
     "Chọn thước đo sai số:"),
    ("lessons/dan/L11_bang_dieu_khien.yaml", "check",
     '<p class="note"><b>Biểu đồ chuẩn và cảnh báo ít báo động giả:</b> vẽ biểu đồ cột giữ trục tung bắt đầu từ 0 để tránh phóng đại; thiết kế cảnh báo kết hợp ngưỡng chênh đủ lớn qua hai kỳ liên tiếp nhằm lọc nhiễu.</p>',
     "Để vẽ biểu đồ không phóng đại cần giữ trục tung từ 0, đồng thời đặt ngưỡng cảnh báo đủ rộng qua hai kỳ liên tiếp nhằm lọc báo động giả.",
     "Biểu đồ chuẩn và cảnh báo"),
    # DSC
    ("lessons/dsc/L02_du_lieu_gon_noi_bang.yaml", "sym",
     '<p class="note"><b>Quan hệ nhiều–nhiều (N–M) và tích Đề-các:</b> khi nối hai bảng qua cột có khoá lặp ở cả hai bên (nhiều–nhiều, N–M), phép nối tạo ra <b>tích Đề-các</b> khiến số dòng nhân bội ngoài ý muốn.</p>',
     "Quan hệ nhiều nhiều xảy ra khi hai bảng đều trùng khoá, làm phép nối sinh ra tích Đề các nhân bội số dòng.",
     "tích Đề-các"),
    ("lessons/dsc/L03_du_lieu_thieu.yaml", "check",
     '<p class="note"><b>Chọn cách xử lý phù hợp:</b> chỉ xoá dòng khi dữ liệu thiếu hoàn toàn ngẫu nhiên với tỉ lệ nhỏ; khi thiếu có nguyên nhân, giữ riêng một cờ báo thiếu hoặc dùng mô hình tự xử lý giá trị trống thay vì điền trung bình chung.</p>',
     "Khi chọn cách xử lý dữ liệu thiếu, chỉ bỏ dòng lúc thiếu hoàn toàn ngẫu nhiên, còn lại hãy giữ cờ báo thiếu hoặc điền theo từng nhóm.",
     "Chọn cách xử lý phù hợp:"),
    ("lessons/dsc/L06_tuong_quan.yaml", "sym",
     '<p class="note"><b>Hệ số tương quan Pearson ($r$):</b> thước đo tương quan tuyến tính $r$ trình bày ở trên gọi đầy đủ là <b>hệ số tương quan Pearson</b>.</p>',
     "Thước đo tương quan tuyến tính chữ r này mang tên gọi đầy đủ là hệ số tương quan Pi-ơ-sơn.",
     "Pearson"),
    ("lessons/dsc/L06_tuong_quan.yaml", "example",
     '<p class="note"><b>Đọc đúng hệ số $r$:</b> dấu cho biết chiều tăng giảm cùng hay ngược, độ lớn gần $\\pm 1$ cho thấy bám sát đường thẳng, còn $r = 0$ chỉ nghĩa là không có xu hướng đường thẳng chứ không chứng minh hai biến độc lập.</p>',
     "Đọc đúng hệ số tương quan cần xem cả chiều dấu lẫn độ khít đường thẳng, và giá trị không chỉ nói không có quan hệ tuyến tính.",
     "Đọc đúng hệ số $r$:"),
    ("lessons/dsc/L09_kiem_dinh_nhieu_lan.yaml", "sym",
     '<p class="note"><b>Xác suất sai lầm toàn họ (FWER):</b> tỉ lệ có ít nhất một kết quả giả trong nhiều lần kiểm đồng thời gọi tắt là <b>FWER</b> (Family-Wise Error Rate).</p>',
     "Xác suất gặp ít nhất một báo giả trong cả loạt kiểm định được viết tắt theo tiếng Anh là FWER.",
     "FWER"),
    ("lessons/dsc/L11_ti_le_nen.yaml", "sym",
     '<p class="note"><b>Giá trị dự đoán dương (PPV):</b> tỉ lệ người thật sự mắc bệnh trong nhóm có kết quả dương tính gọi tắt tiếng Anh là <b>PPV</b> (Positive Predictive Value).</p>',
     "Giá trị dự đoán dương được viết tắt trong thực hành bằng ba chữ cái tiếng Anh là P P V.",
     "PPV"),
    ("lessons/dsc/L12_dien_giai_hoi_quy.yaml", "example",
     '<p class="note"><b>Cách đọc một hệ số hồi quy:</b> hệ số $b_j$ là mức thay đổi trung bình của biến kết quả khi biến $X_j$ tăng thêm 1 đơn vị trong điều kiện giữ nguyên các biến còn lại — chỉ nêu tương quan quan sát, không mặc định là nhân quả.</p>',
     "Để đọc đúng một hệ số hồi quy, hãy nói là mức đổi trung bình khi giữ nguyên các biến khác, chứ không tự suy thành quan hệ nhân quả.",
     "Cách đọc một hệ số hồi quy:"),
    # MLO
    ("lessons/mlo/L02_quan_ly_du_lieu.yaml", "sym",
     '<p class="note"><b>Đơn vị lưu trữ lớn:</b> <b>1 TB</b> (terabyte) bằng 1 000 GB, và <b>1 petabyte</b> bằng 1 000 TB (tương đương một triệu GB).</p>',
     "Về đơn vị dung lượng, một tê-ra-bai bằng một nghìn ghi-ga-bai, còn một pê-ta-bai gấp một nghìn tê-ra-bai.",
     "petabyte"),
    ("lessons/mlo/L03_kiem_thu_he_ml.yaml", "sym",
     '<p class="note"><b>Tích hợp liên tục (CI):</b> quy trình tự động chạy toàn bộ kiểm thử dữ liệu và mô hình mỗi khi gộp mã mới gọi là <b>CI</b> (Continuous Integration).</p>',
     "Quy trình chạy kiểm thử tự động mỗi lần gộp mã mới thường được viết tắt là C I.",
     "Continuous Integration"),
    ("lessons/mlo/L06_phuc_vu_mo_hinh.yaml", "sym",
     '<p class="note"><b>Nhịp tải req/s:</b> số yêu cầu hệ phải phục vụ trong một giây viết tắt là <b>req/s</b> (requests per second).</p>',
     "Nhịp yêu cầu phục vụ mỗi giây thường viết gọn trên biểu đồ và đề bài là số yêu cầu trên giây.",
     "req/s"),
    ("lessons/mlo/L06_phuc_vu_mo_hinh.yaml", "example",
     '<p class="note"><b>Chọn theo lô hay trực tuyến:</b> dự đoán trước theo lô khi người dùng chưa cần kết quả ngay (ví dụ gợi ý qua đêm) để tối đa hoá thông lượng; dùng phục vụ trực tuyến khi phải trả lời ngay trong vài chục mi-li-giây theo ngữ cảnh hiện tại.</p>',
     "Để chọn đúng, hãy dự đoán trước theo lô khi không cần kết quả tức thì, và chạy trực tuyến khi phải phản hồi ngay theo ngữ cảnh mới nhất.",
     "Chọn theo lô hay trực tuyến:"),
    ("lessons/mlo/L07_phat_hanh_mo_hinh.yaml", "example",
     '<p class="note"><b>Chạy song song không ảnh hưởng người dùng (chạy bóng):</b> gửi bản sao lưu lượng thật vào mô hình mới để đo độ trễ và phân phối dự đoán nhưng vẫn trả đáp án của mô hình cũ cho khách trước khi mở thử nghiệm A/B.</p>',
     "Trước khi mở cho người dùng, chạy bóng gửi bản sao lưu lượng vào mô hình mới để đo độ trễ mà không làm ảnh hưởng kết quả trả về.",
     "chạy bóng"),
    ("lessons/mlo/L08_giam_sat_troi.yaml", "check",
     '<p class="note"><b>Chọn đặc trưng và ngưỡng cảnh báo:</b> ưu tiên theo dõi chỉ số ổn định quần thể trên các đặc trưng có trọng số ảnh hưởng cao nhất, với ngưỡng trôi nhẹ 0,10 và báo động chuyển lệch đáng kể từ <b>0,25</b> trở lên.</p>',
     "Khi chọn đặc trưng và ngưỡng, hãy ưu tiên những biến có ảnh hưởng mạnh nhất và đặt mức cảnh báo lệch đáng kể từ không phẩy hai lăm.",
     "Chọn đặc trưng và ngưỡng cảnh báo:"),
    ("lessons/mlo/L13_bao_mat_he_ml.yaml", "sym",
     '<p class="note"><b>Giao diện dịch vụ (API):</b> điểm mở cho phép ứng dụng bên ngoài gửi yêu cầu tới mô hình gọi là <b>API</b> (giao diện lập trình ứng dụng).</p>',
     "Cổng tiếp nhận yêu cầu dự đoán từ ứng dụng bên ngoài được gọi là giao diện dịch vụ A P I.",
     "API"),
    ("lessons/mlo/L14_hanh_trinh_no_ky_thuat.yaml", "stage4",
     '<p class="note"><b>Chọn mức đầu tư cho đội của bạn:</b> đội nhỏ một sản phẩm chỉ cần kiểm thử dữ liệu chuẩn và nhật ký theo dõi gọn nhẹ; chỉ đầu tư nền tảng đặc trưng dùng chung và huấn luyện lại tự động khi có nhiều nhóm dùng chung dữ liệu và vòng đời triển khai liên tục.</p>',
     "Ở quy mô đội của chính bạn, chỉ đầu tư hạ tầng đặc trưng dùng chung khi nhiều đội cùng chia sẻ dữ liệu, còn đội nhỏ hãy ưu tiên kiểm thử sạch và gọn.",
     "Chọn mức đầu tư cho đội của bạn:"),
    # EVT
    ("lessons/evt/L00_su_kien_va_lenh.yaml", "sym",
     '<p class="note"><b>Hai kiểu nối mạng dịch vụ:</b> nối trực tiếp cặp đôi gọi là điểm–điểm (<b>P2P</b>); phát qua một kênh chung ở giữa gọi là kênh sự kiện trung tâm (<b>bus</b>).</p>',
     "Trong kiến trúc, nối thẳng từng cặp dịch vụ gọi tắt là P2P, còn kênh sự kiện ở giữa gọi là bus.",
     "P2P"),
    ("lessons/evt/L01_luoc_do_su_kien.yaml", "check",
     '<p class="note"><b>Chọn thứ tự triển khai:</b> với tương thích ngược nâng bên nhận trước để đọc được cả cũ lẫn mới; với tương thích xuôi nâng bên phát trước để bên nhận cũ bỏ qua trường lạ an toàn.</p>',
     "Về thứ tự triển khai, tương thích ngược thì nâng cấp người nhận trước, còn tương thích xuôi thì nâng cấp người gửi trước.",
     "Chọn thứ tự triển khai:"),
    ("lessons/evt/L02_kenh_thu_chet.yaml", "check",
     '<p class="note"><b>Thiết kế quy trình xử lý lại:</b> gắn lý do lỗi, số lần đã thử và khoá sự kiện gốc vào kênh thư chết, rồi chỉ phát lại sang luồng chính sau khi đã vá lỗi ở dịch vụ tiêu thụ.</p>',
     "Khi thiết kế kênh thư chết, luôn giữ lại dữ liệu gốc cùng số lần thử và chỉ cho phát lại sau khi đã vá xong nguyên nhân lỗi.",
     "Thiết kế quy trình xử lý lại:"),
    ("lessons/evt/L03_thu_tu_va_phien_ban.yaml", "example",
     '<p class="note"><b>Chọn khoá phân vùng đúng:</b> đặt khoá theo thực thể cần giữ thứ tự (ví dụ <code>order_id</code>) thay vì dùng một giá trị cố định hay chuỗi ngẫu nhiên làm mất thứ tự hoặc nghẽn một phân vùng.</p>',
     "Chọn đúng khoá phân vùng là gắn với mã thực thể cần giữ thứ tự như mã đơn hàng, tránh dùng khoá hằng số hay ngẫu nhiên.",
     "Chọn khoá phân vùng đúng:"),
    ("lessons/evt/L06_giao_dich_dai.yaml", "check",
     '<p class="note"><b>So sánh điều phối với biên đạo:</b> điều phối tập trung dễ nhìn toàn luồng qua một bộ điều khiển nhưng cần quản lý trạng thái trung tâm; biên đạo phi tập trung giảm điểm nghẽn nhưng khó lần dấu khi chuỗi dài nhiều bước.</p>',
     "Khi so sánh hai cách, điều phối tập trung dễ theo dõi toàn luồng tại một chỗ, còn biên đạo tránh được điểm điều khiển trung tâm nhưng khó truy vết hơn.",
     "So sánh điều phối với biên đạo:"),
    ("lessons/evt/L09_tai_xu_ly.yaml", "example",
     '<p class="note"><b>So sánh kiến trúc hai đường với một đường phát lại:</b> giữ hai nhánh lô và luồng riêng tốn công bảo trì hai bộ mã dễ lệch số, còn gom về một luồng kèm nhật ký giữ lại chỉ dùng một đường mã cho cả dữ liệu mới và phát lại.</p>',
     "So sánh hai cách tổ chức, gộp về một luồng phát lại giúp tránh viết và đối chiếu hai bộ mã song song như kiến trúc hai nhánh.",
     "So sánh kiến trúc hai đường với một đường phát lại:"),
    ("lessons/evt/L09_tai_xu_ly.yaml", "check",
     '<p class="note"><b>Chọn thời gian giữ nhật ký:</b> đặt hạn lưu lớn hơn cửa sổ sửa lỗi nghiệp vụ dài nhất cộng thêm thời gian phát lại và kiểm tra sai số, tránh xoá mất mốc đầu trước khi phát hiện hỏng.</p>',
     "Khi chọn thời gian giữ nhật ký, hãy đặt dài hơn quãng thời gian phát hiện lỗi cộng thời gian chạy lại hoàn tất.",
     "Chọn thời gian giữ nhật ký:"),
    ("lessons/evt/L11_hanh_trinh_nhat_ky_su_kien.yaml", "stage5",
     '<p class="note"><b>Chọn thực hành hợp quy mô mình:</b> hệ lưu lượng vài nghìn tin mỗi giây dùng tốt một cụm gọn với bản sao cơ bản; chỉ đầu tư phân tầng cụm và lược bỏ điều phối ngoài khi sản lượng vọt lên hàng trăm nghìn tin mỗi giây.</p>',
     "Để chọn thực hành hợp quy mô riêng, chỉ chia tách nhiều cụm phức tạp khi sản lượng vượt quá ngưỡng một cụm đơn chịu được.",
     "Chọn thực hành hợp quy mô mình:"),
    # DEN
    ("lessons/den/L08_nhat_ky_su_kien.yaml", "check",
     '<p class="note"><b>Chọn thời điểm ghi nhận vị trí đọc:</b> chỉ ghi vị trí sau khi đã xử lý và lưu kết quả xuống đích (và làm hàm xử lý lũy đẳng) để tránh mất sự kiện nếu máy đọc sập giữa chừng.</p>',
     "Khi chọn thời điểm ghi nhận vị trí đọc, luôn ghi sau lúc lưu kết quả xong để không bị mất tin khi dịch vụ tắt đột ngột.",
     "Chọn thời điểm ghi nhận vị trí đọc:"),
    ("lessons/den/L12_kho_du_lieu.yaml", "sym",
     '<p class="note"><b>Chiều thay đổi chậm (SCD):</b> cách bảng chiều cập nhật hoặc lưu lại lịch sử các thuộc tính theo thời gian gọi là <b>SCD</b> (Slowly Changing Dimension).</p>',
     "Các chiến lược cập nhật hoặc lưu lịch sử thay đổi cho bảng chiều được gọi tên theo thuật ngữ SCD.",
     "SCD"),
    ("lessons/den/L12_kho_du_lieu.yaml", "example",
     '<p class="note"><b>Thiết kế lược đồ hình sao:</b> đặt một bảng sự kiện ở trung tâm chứa các thước đo định lượng, nối ra các bảng chiều chứa ngữ cảnh để báo cáo tổng hợp nhanh và dễ mở rộng.</p>',
     "Khi thiết kế lược đồ hình sao, ta gom các con số đo ở bảng trung tâm và tách thông tin mô tả ra các bảng chiều xung quanh.",
     "Thiết kế lược đồ hình sao:"),
    ("lessons/den/L12_kho_du_lieu.yaml", "check",
     '<p class="note"><b>Chọn độ mịn của bảng sự kiện:</b> cố định mỗi dòng ứng với đơn vị sự kiện nhỏ nhất không tách thêm được (chẳng hạn từng dòng hàng bán) trước khi nối sang mọi bảng chiều.</p>',
     "Để chọn độ mịn cho bảng sự kiện, hãy chọn mức chi tiết nhỏ nhất cần phân tích và giữ đồng nhất trên toàn bảng.",
     "Chọn độ mịn của bảng sự kiện:"),
    # CLD
    ("lessons/cld/L03_giao_tiep_san_sang.yaml", "example",
     '<p class="note"><b>So sánh gọi đồng bộ và gửi thông điệp:</b> gọi đồng bộ trả kết quả ngay nhưng ghép chặt độ sẵn sàng theo phép nhân nối tiếp; gửi thông điệp bất đồng bộ qua hàng đợi chịu được dịch vụ đích tạm nghỉ khi chưa cần trả lời tức thì.</p>',
     "Khi so sánh hai kiểu giao tiếp, gọi đồng bộ gắn chặt sinh tử các mắt xích liên tiếp, còn gửi thông điệp giúp tách nhịp chờ khi có thể trễ.",
     "So sánh gọi đồng bộ và gửi thông điệp:"),
    ("lessons/cld/L08_cap_nhat_cuon_chieu.yaml", "check",
     '<p class="note"><b>So sánh ba chiến lược phát hành:</b> cuốn chiếu tiết kiệm máy nhưng trộn hai phiên bản; xanh–lam chuyển tức thì tốn gấp đôi tài nguyên tạm; phát hành thử kiểm tra trước trên phần trăm khách nhỏ.</p>',
     "So sánh ba cách, cuốn chiếu tiết kiệm tài nguyên nhất, xanh lam tốn gấp đôi máy nhưng quay lui tức thì, còn phát hành thử giảm rủi ro trên nhóm nhỏ.",
     "So sánh ba chiến lược phát hành:"),
    ("lessons/cld/L09_can_bang_tai.yaml", "example",
     '<p class="note"><b>So sánh ba thuật toán chia tải:</b> vòng tròn chia đều mù độ trễ; ít kết nối nhất theo dõi sát tải hiện thời nhưng cần trạng thái tập trung; chọn tốt hơn trong hai đạt cân bằng tốt khi nhiều bộ chia tải chạy song song.</p>',
     "So sánh ba thuật toán, vòng tròn dễ lệch khi yêu cầu nặng nhẹ khác nhau, ít kết nối nhất chính xác nhưng tốn trạng thái, còn chọn tốt hơn trong hai gọn nhẹ mà hiệu quả cao.",
     "So sánh ba thuật toán chia tải:"),
    # CLC
    ("lessons/clc/L01_vung_sanz_sang.yaml", "sym",
     '<p class="note"><b>Ký hiệu vùng sẵn sàng (AZ):</b> mỗi cụm trung tâm dữ liệu tách biệt về điện, mạng và làm mát trong một vùng gọi tắt tiếng Anh là <b>AZ</b> (Availability Zone).</p>',
     "Mỗi khu vực trung tâm dữ liệu độc lập về điện và mạng được gọi là vùng sẵn sàng, viết tắt là A Z.",
     "Availability Zone"),
    ("lessons/clc/L02_mang_ao.yaml", "sym",
     '<p class="note"><b>Thuật ngữ mạng đám mây:</b> mạng riêng biệt lập gọi là <b>VPC</b> (Virtual Private Cloud), chia nhỏ thành các mạng con (<b>subnet</b>) đánh địa chỉ theo giao thức mạng <b>IP</b>.</p>',
     "Trên đám mây, mạng riêng ảo gọi là VPC, chia nhỏ thành các mạng con theo địa chỉ IP.",
     "Virtual Private Cloud"),
    ("lessons/clc/L03_phan_quyen.yaml", "sym",
     '<p class="note"><b>Từ khoá phân quyền IAM:</b> hệ thống quản lý danh tính và quyền viết tắt là <b>IAM</b>; hai hiệu lực quy tắc là cho phép (<b>Allow</b>) và từ chối (<b>Deny</b>).</p>',
     "Hệ thống phân quyền đám mây gọi tắt là IAM, trong đó hai nhãn quy tắc chính là cho phép và từ chối.",
     "Allow"),
    ("lessons/clc/L04_luu_tru.yaml", "example",
     '<p class="note"><b>Chọn loại lưu trữ:</b> tệp tĩnh lớn hay ảnh dùng kho đối tượng để mở rộng rẻ; cơ sở dữ liệu đòi hỏi độ trễ thấp dùng đĩa khối gắn máy ảo; nhiều máy cùng đọc ghi một cây thư mục dùng lưu trữ tệp chung.</p>',
     "Để chọn đúng loại lưu trữ, dùng kho đối tượng cho tệp lớn truy cập qua web, đĩa khối cho cơ sở dữ liệu cần nhanh, và hệ tệp chung khi nhiều máy dùng chung.",
     "Chọn loại lưu trữ:"),
    ("lessons/clc/L05_may_ao_chi_phi.yaml", "sym",
     '<p class="note"><b>Các gói thuê và đơn vị tiền:</b> gói trả linh hoạt theo nhu cầu là <b>On-Demand</b>, gói cam kết 1–3 năm là <b>Reserved</b>, tính cước theo đơn vị đô la Mỹ (<b>USD</b>).</p>',
     "Hai gói thuê phổ biến là trả theo nhu cầu linh hoạt và đặt trước có cam kết thời hạn, thường niêm yết theo đồng đô la Mỹ.",
     "On-Demand"),
    ("lessons/clc/L06_ham_theo_su_kien.yaml", "sym",
     '<p class="note"><b>Mô hình không cần quản máy chủ (serverless):</b> cách chạy hàm theo sự kiện trả tiền từng lượt không tự vận hành máy chủ gọi chung là <b>serverless</b>.</p>',
     "Cách vận hành hàm không phải tự quản lý máy chủ nền tảng thường được gọi theo thuật ngữ là serverless.",
     "serverless"),
    ("lessons/clc/L07_csdl_duoc_quan_ly.yaml", "sym",
     '<p class="note"><b>Ảnh chụp nhanh và nhật ký ghi trước:</b> bản sao toàn bộ ổ đĩa tại một mốc là ảnh chụp (<b>snapshot</b>); nhật ký ghi mọi thay đổi liên tục giữa các lần chụp là <b>WAL</b> (Write-Ahead Log).</p>',
     "Bản sao định kỳ toàn bộ đĩa là ảnh chụp nhanh, còn nhật ký ghi liên tiếp từng thay đổi giúp khôi phục theo từng giây viết tắt là WAL.",
     "Write-Ahead Log"),
    ("lessons/clc/L08_chi_phi_mang_cdn.yaml", "sym",
     '<p class="note"><b>Lưu lượng ra và mạng phân phối nội dung:</b> cước truyền dữ liệu rời khỏi vùng đám mây là cước ra (<b>Egress</b>), tính bằng đồng <b>USD</b>; lớp máy đệm đặt gần người dùng giúp giảm cước ra gọi là <b>CDN</b>.</p>',
     "Cước đẩy dữ liệu rời đám mây ra internet gọi là cước ra, giảm tải hiệu quả bằng mạng phân phối nội dung gần người dùng CDN.",
     "Egress"),
    ("lessons/clc/L09_ma_hoa_khoa.yaml", "sym",
     '<p class="note"><b>Dịch vụ quản lý khoá (KMS):</b> dịch vụ chuyên cất giữ khoá chính ngoài máy chủ dữ liệu gọi tắt là <b>KMS</b>; đơn vị kích thước dữ liệu mẫu là kilôbai (<b>KB</b> = 1 024 byte).</p>',
     "Dịch vụ quản lý khoá tách biệt nơi cất giữ khoá gốc gọi tắt là KMS.",
     "KMS"),
    ("lessons/clc/L10_khoi_phuc_tham_hoa.yaml", "sym",
     '<p class="note"><b>Ký hiệu mô hình dự phòng:</b> mô hình hai vùng cùng nhận tải gọi là chủ động–chủ động (<b>Active-Active</b>) tính theo lưu lượng <b>req/s</b> (yêu cầu mỗi giây); còn mô hình chừa sẵn ít nhất 1 phần dự phòng gọi là <b>N+1</b>.</p>',
     "Hai mô hình dự phòng hay dùng là hai vùng chạy song song theo nhịp yêu cầu mỗi giây, và cách chừa sẵn ít nhất một máy dự phòng.",
     "Active-Active"),
    ("lessons/clc/L11_tong_hop_di_chuyen.yaml", "sym",
     '<p class="note"><b>Nhắc lại ký hiệu kiến trúc:</b> phân tách tối thiểu qua hai vùng sẵn sàng (<b>AZ</b>) để loại bỏ điểm hỏng đơn lẻ duy nhất (<b>SPOF</b>, Single Point of Failure).</p>',
     "Một hệ kiến trúc tốt luôn tránh điểm hỏng đơn lẻ có thể làm sập cả hệ thống nhờ trải ra ít nhất hai vùng sẵn sàng.",
     "SPOF"),
    ("lessons/clc/L12_hanh_trinh_luu_tru_doi_tuong.yaml", "stage5",
     '<p class="note"><b>Chọn cách bảo vệ và chỗ đặt trạng thái:</b> với kho vừa cần đồng bộ cao mà kích thước bảng chỉ mục chưa quá lớn, chọn một dịch vụ quản lý trạng thái nhất quán mạnh và đặt mọi lệnh xoá hoặc sửa cấu hình hàng loạt sau bước rào chắn hai lớp cùng diễn tập đúng quy mô.</p>',
     "Khi chọn cách bảo vệ cho quy mô riêng, đặt các lệnh gỡ hàng loạt sau ngưỡng tự chặn và dùng kho nhất quán mạnh cho bảng siêu dữ liệu cốt lõi.",
     "Chọn cách bảo vệ và chỗ đặt trạng thái:"),
    # SAR
    ("lessons/sar/L00_thuoc_tinh_chat_luong.yaml", "sym",
     '<p class="note"><b>Thuật ngữ viết tắt độ trễ:</b> phân vị thứ 95 và 99 của độ trễ gọi tắt là <b>P95</b>, <b>P99</b>; mục tiêu cam kết chất lượng dịch vụ gọi là <b>SLO</b> (Service Level Objective).</p>',
     "Các mốc phần trăm đuôi chậm như 95 hay 99 gọi tắt là P95 và P99, còn cam kết mục tiêu phục vụ gọi là SLO.",
     "SLO"),
    ("lessons/sar/L01_ghi_quyet_dinh.yaml", "sym",
     '<p class="note"><b>Thuật ngữ quyết định kiến trúc:</b> bản ghi quyết định kiến trúc viết tắt là <b>ADR</b>; hệ quản trị cơ sở dữ liệu quan hệ chuẩn giao dịch <b>ACID</b> gọi tắt là <b>RDBMS</b>.</p>',
     "Bản ghi quyết định viết tắt là A D R, còn hệ cơ sở dữ liệu quan hệ bảo đảm toàn vẹn giao dịch gọi tắt là RDBMS.",
     "RDBMS"),
    ("lessons/sar/L02_uoc_luong_suc_tai.yaml", "sym",
     '<p class="note"><b>Đơn vị lưu lượng:</b> lượng người dùng hoạt động mỗi ngày là <b>DAU</b> (Daily Active Users), và số truy vấn phục vụ mỗi giây là <b>QPS</b> (Queries Per Second).</p>',
     "Hai chỉ số sức tải thường tính trước khi chọn máy là số người dùng hằng ngày và lượng truy vấn trên giây.",
     "DAU"),
    ("lessons/sar/L03_tac_viec_thanh_phan.yaml", "sym",
     '<p class="note"><b>Giao diện và chiều gọi dịch vụ:</b> tầng giao diện người dùng gọi tắt là <b>UI</b>; bên phát yêu cầu gọi là bên gọi (<b>caller</b>) và bên phục vụ là bên được gọi (<b>callee</b>).</p>',
     "Tầng hiển thị giao diện gọi tắt là U I, còn hai đầu mối trao đổi giữa hai dịch vụ là bên gọi và bên nhận.",
     "callee"),
    ("lessons/sar/L04_bo_nho_dem.yaml", "sym",
     '<p class="note"><b>Bộ nhớ đệm nhanh (Cache):</b> lớp lưu tạm kết quả gần bộ xử lý để tăng tốc truy xuất gọi bằng tiếng Anh là <b>Cache</b>.</p>',
     "Trong kiến trúc thực tế, bộ nhớ đệm tăng tốc truy cập hay được ghi thẳng là két.",
     "Cache"),
    ("lessons/sar/L04_bo_nho_dem.yaml", "check",
     '<p class="note"><b>Chọn chiến lược ghi và thời gian sống:</b> chọn ghi xuyên qua khi cần dữ liệu an toàn tức thì, chỉ dùng ghi trễ khi chịu rủi ro mất vài giây cuối; luôn cộng thêm khoảng lệch ngẫu nhiên vào thời gian sống (TTL) để tránh hết hạn đồng loạt.</p>',
     "Khi chọn chiến lược ghi, ưu tiên an toàn bằng ghi xuyên qua nếu mất dữ liệu không cho phép, và luôn rải lệch thời gian sống để tránh sập đồng loạt.",
     "Chọn chiến lược ghi và thời gian sống:"),
    ("lessons/sar/L05_phan_manh.yaml", "sym",
     '<p class="note"><b>Ký hiệu phân mảnh:</b> hệ số sao chép số bản dữ liệu gọi tắt là <b>RF</b> (Replication Factor), còn mỗi phần dữ liệu chia nhỏ đặt trên từng cụm là một mảnh (<b>shard</b>).</p>',
     "Hệ số nhân bản dữ liệu viết tắt là R F, còn từng lát dữ liệu khi chia tách gọi là các mảnh.",
     "Replication Factor"),
    ("lessons/sar/L05_phan_manh.yaml", "example",
     '<p class="note"><b>Chọn khoá phân mảnh tránh điểm nóng:</b> chọn khoá có lực lượng lớn và phân bố đều theo luồng ghi như mã giao dịch hoặc mã người dùng băm, tránh chọn mã quốc gia hay ngày tạo khiến mọi lượt ghi dồn về một mảnh.</p>',
     "Để chọn khoá phân mảnh đúng, tìm trường có độ phân tán đều theo lượt ghi thay vì gộp hết vào một mã quốc gia hoặc ngày hôm nay.",
     "Chọn khoá phân mảnh tránh điểm nóng:"),
    ("lessons/sar/L08_hang_doi_bat_dong_bo.yaml", "sym",
     '<p class="note"><b>Thuật ngữ hàng đợi:</b> lượng công việc tồn đọng chưa xử lý kịp là <b>backlog</b>, và quá trình rút hết phần tồn đó về không khi lưu lượng hạ xuống gọi là xả hàng đợi (<b>drain</b>).</p>',
     "Phần việc ứ đọng trong hàng đợi gọi là tồn đọng, và giai đoạn dọn sạch lượng ứ đọng này gọi là xả hàng đợi.",
     "backlog"),
    ("lessons/sar/L09_luy_dang.yaml", "sym",
     '<p class="note"><b>Ngữ cảnh thực hành SQLite:</b> dùng cơ sở dữ liệu nhúng gọn <b>SQLite</b> lưu bảng sổ cái <b>ledger</b> và bảng khoá lũy đẳng <b>idem</b> chống xử lý trùng một yêu cầu (<b>req</b>).</p>',
     "Trong bài thực hành dùng cơ sở dữ liệu gọn nhẹ S Q Lite với hai bảng sổ cái và khoá chống lặp mỗi yêu cầu.",
     "ledger"),
    ("lessons/sar/L10_nhat_quan_da_vung.yaml", "sym",
     '<p class="note"><b>Thời gian khứ hồi (RTT):</b> tổng thời gian gửi một gói tin đi và nhận phản hồi quay về gọi là <b>RTT</b> (Round-Trip Time).</p>',
     "Khoảng thời gian gửi yêu cầu đi và nhận tin xác nhận quay về được đo bằng thời gian khứ hồi RTT.",
     "Round-Trip Time"),
    ("lessons/sar/L10_nhat_quan_da_vung.yaml", "check",
     '<p class="note"><b>Chọn mức nhất quán theo từng loại dữ liệu:</b> bắt buộc nhất quán mạnh qua đa số với tiền tệ, tồn kho hay quyền bảo mật; dùng nhất quán cuối cùng nhanh cho lượt thích, bộ đếm xem hay trạng thái ít nhạy cảm.</p>',
     "Khi chọn mức nhất quán, dữ liệu tiền bạc và tồn kho buộc phải chờ đa số đồng bộ, còn lượt thích hay bộ đếm chỉ cần nhất quán cuối cùng.",
     "Chọn mức nhất quán theo từng loại dữ liệu:"),
    ("lessons/sar/L11_kien_truc_an_toan.yaml", "sym",
     '<p class="note"><b>Chỉ lệnh chỉ đọc trên SQLite:</b> cơ sở dữ liệu nhúng <b>SQLite</b> hỗ trợ câu lệnh cấu hình <b>PRAGMA</b> để khoá kết nối ở chế độ chỉ đọc an toàn cho báo cáo.</p>',
     "Trên cơ sở dữ liệu S Q Lite, ta dùng chỉ lệnh cấu hình để khoá cứng quyền chỉ đọc cho tài khoản tra cứu.",
     "PRAGMA"),
    ("lessons/sar/L12_thiet_ke_tong_hop.yaml", "sym",
     '<p class="note"><b>Nhắc lại đơn vị QPS:</b> số yêu cầu hệ thống phục vụ trong mỗi giây viết tắt là <b>QPS</b> (Queries Per Second).</p>',
     "Khi trình bày ước lượng lưu lượng thiết kế, đơn vị truy vấn mỗi giây được viết tắt là Q P S.",
     "QPS"),
    ("lessons/sar/L13_hanh_trinh_twitter.yaml", "stage5",
     '<p class="note"><b>Chọn giữa thêm máy và tách dịch vụ:</b> khi lưu lượng và đội kỹ thuật còn nhỏ, tăng máy hoặc thêm bộ nhớ đệm trước; chỉ tách nhỏ thành các dịch vụ độc lập khi ranh giới dữ liệu đã rõ và một điểm nghẽn riêng buộc phải mở rộng theo tỷ lệ khác biệt.</p>',
     "Khi cân nhắc mở rộng cho hệ của mình, hãy thêm máy hoặc tối ưu bộ nhớ đệm trước khi tách dịch vụ nhỏ gây gánh nặng vận hành.",
     "Chọn giữa thêm máy và tách dịch vụ:"),
]

for rel, sid, n_html, n_say, marker in ENRICH_S8:
    append_to_step(rel, sid, n_html, n_say, marker)

# 8. Set ALL cleaned `covers:` mappings across Stage 8 flagged lessons
COVERS_S8 = {
    "lessons/dan/L06_chuoi_thoi_gian.yaml": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "lessons/dan/L08_phan_khuc.yaml": [(1, "example"), (2, "sym"), (3, "sym")],
    "lessons/dan/L11_bang_dieu_khien.yaml": [(1, "example"), (2, "check"), (3, "check")],
    "lessons/dsc/L06_tuong_quan.yaml": [(1, "example"), (2, "intuition"), (3, "example")],
    "lessons/dsc/L09_kiem_dinh_nhieu_lan.yaml": [(1, "example"), (2, "example"), (3, "sym")],
    "lessons/dsc/L11_ti_le_nen.yaml": [(1, "example"), (2, "pitfalls"), (3, "cost")],
    "lessons/dsc/L13_rieng_tu_dao_duc.yaml": [(1, "pitfalls"), (2, "example"), (3, "pitfalls")],
    "lessons/mlo/L01_tai_lap.yaml": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "lessons/mlo/L03_kiem_thu_he_ml.yaml": [(1, "sym"), (2, "example"), (3, "check")],
    "lessons/mlo/L12_the_mo_hinh_cong_bang.yaml": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "lessons/mlo/L13_bao_mat_he_ml.yaml": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "lessons/mlo/L14_hanh_trinh_no_ky_thuat.yaml": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (2, "check"), (3, "stage4")],
    "lessons/evt/L02_kenh_thu_chet.yaml": [(1, "example"), (2, "sym"), (3, "check")],
    "lessons/evt/L04_ghi_nguon_su_kien.yaml": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "lessons/evt/L05_tach_ghi_doc.yaml": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "lessons/evt/L06_giao_dich_dai.yaml": [(1, "example"), (2, "example"), (2, "check"), (3, "check")],
    "lessons/evt/L09_tai_xu_ly.yaml": [(1, "example"), (2, "check"), (3, "check")],
    "lessons/evt/L10_quan_sat.yaml": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "lessons/evt/L11_hanh_trinh_nhat_ky_su_kien.yaml": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5")],
    "lessons/den/L08_nhat_ky_su_kien.yaml": [(1, "example"), (2, "check"), (3, "check")],
    "lessons/den/L12_kho_du_lieu.yaml": [(1, "example"), (2, "check"), (3, "check")],
    "lessons/cld/L02_anh_tai_lap.yaml": [(1, "intuition"), (2, "check"), (3, "pitfalls")],
    "lessons/cld/L09_can_bang_tai.yaml": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "lessons/cld/L13_cau_hinh_bi_mat.yaml": [(1, "sym"), (2, "sym"), (3, "pitfalls")],
    "lessons/clc/L00_dam_may_la_gi.yaml": [(1, "sym"), (2, "sym"), (3, "example")],
    "lessons/clc/L05_may_ao_chi_phi.yaml": [(1, "example"), (2, "pitfalls"), (3, "pitfalls")],
    "lessons/clc/L06_ham_theo_su_kien.yaml": [(1, "example"), (2, "sym"), (3, "practice")],
    "lessons/clc/L07_csdl_duoc_quan_ly.yaml": [(1, "sym"), (2, "example"), (3, "sym")],
    "lessons/clc/L10_khoi_phuc_tham_hoa.yaml": [(1, "intuition"), (2, "example"), (3, "pitfalls")],
    "lessons/clc/L11_tong_hop_di_chuyen.yaml": [(1, "example"), (2, "sym"), (3, "pitfalls")],
    "lessons/clc/L12_hanh_trinh_luu_tru_doi_tuong.yaml": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "stage5"), (3, "stage5")],
    "lessons/sar/L01_ghi_quyet_dinh.yaml": [(1, "example"), (2, "sym"), (3, "pitfalls")],
    "lessons/sar/L05_phan_manh.yaml": [(1, "example"), (2, "sym"), (3, "example")],
    "lessons/sar/L06_do_san_sang.yaml": [(1, "example"), (2, "sym"), (3, "pitfalls")],
    "lessons/sar/L12_thiet_ke_tong_hop.yaml": [(1, "example"), (2, "check"), (3, "prereq")],
    "lessons/sar/L13_hanh_trinh_twitter.yaml": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "stage5"), (3, "stage5")],
}
for rel, cov in COVERS_S8.items():
    set_covers(rel, cov)

# 9. Quick Stage 8 check across ALL 114 lessons (`>=1650w`, `0` 'càng', `0` ' vs ', `lv.lint` E/W = 0)
bad = []
for c in ("dan", "dsc", "mlo", "evt", "den", "cld", "clc", "sar"):
    for p in sorted((ROOT / f"lessons/{c}").glob("L*.yaml")):
        txt = p.read_text(encoding="utf-8")
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
print(f"STAGE 8 ALL 114 LESSONS LINT FAILURES: {len(bad)}", flush=True)
assert not bad, f"Stage 8 issues remain: {bad}"
print("STAGE 8 V3->GO PATCHES + 114-LESSON LINT 100% PASS!", flush=True)
