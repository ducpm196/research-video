"""Hạ tầng sửa vòng 4 (fix6, 2026-11-16) cho DMS L00–L10: bảng "viết trong mã -> đọc là -> ví dụ" đặt NGAY TRƯỚC khối mã,
và dòng giải thích chân trang chấm bài. Dùng cùng af2lib (không sửa af2lib để không đụng L11–L20)."""
import html as _h
import re

from af2lib import step, practice  # noqa: F401

_SENT = re.compile(r"(?<=[.!?…])\s+(?=[^\s])")


def n_sent(say):
    return len([s for s in _SENT.split(" ".join(str(say).split())) if s.strip()])


def C(s):
    """một mẩu mã nội dòng (đã thoát HTML)"""
    return "<code>" + _h.escape(s) + "</code>"


def read_table(rows, head=("viết trong mã", "đọc là", "ví dụ")):
    """rows: (mã, cách đọc [HTML], ví dụ [HTML]); cột mã được thoát HTML và đặt trong <code>."""
    t = '<table class="t"><tr>' + "".join(f"<th>{x}</th>" for x in head) + "</tr>"
    for code, reading, ex in rows:
        t += f"<tr><td>{C(code)}</td><td>{reading}</td><td>{ex}</td></tr>"
    return t + "</table>"


def read_step(rows, intro, says, clear=True, note=None):
    """step có bảng đọc mã: một câu mở (focus tiêu đề bảng) + đúng một câu cho mỗi hàng (focus hàng đó).
    note: HTML thêm sau bảng (không có câu riêng; gắn vào câu mở)."""
    assert len(rows) == len(says), (len(rows), len(says))
    for s in [intro] + list(says):
        assert n_sent(s) == 1, s
    show = read_table(rows) + (note or "")
    focus = ["1.1"] + [f"1.{i + 2}" for i in range(len(rows))]
    return step(show, " ".join([intro] + list(says)), focus=focus, clear=clear)


def hint_parts(box_html, box_say, rows, says, intro=None):
    """gợi ý của cảnh Tự làm: hộp gợi ý (khối 1) + bảng đọc mã (khối 2); trả (html, say, focus)."""
    assert len(rows) == len(says)
    html = box_html + read_table(rows)
    parts = [box_say] + ([intro] if intro else []) + list(says)
    nb = n_sent(box_say)
    focus = [1] * nb + (["2.1"] if intro else []) + [f"2.{i + 2}" for i in range(len(rows))]
    for s in ([intro] if intro else []) + list(says):
        assert n_sent(s) == 1, s
    return html, " ".join(parts), focus


CHAM_SAY = ("Đây là kết quả mong đợi. Bạn chạy chương trình của mình rồi so từng dòng với màn hình. "
            "Muốn chấm bằng máy, gõ lệnh ở chân màn hình: nó chạy tệp chấm bài, kèm khoá học, mã bài và tên tệp của bạn. "
            "Lệnh in chữ ĐÚNG khi mọi dòng trùng, hoặc chỉ ra dòng nào khác.")


def patch_cham(prac, lid, filename):
    """thay dòng chân trang của cảnh practice (step 2) bằng dòng có giải thích và lời đọc 4 câu"""
    st = prac["steps"][1]
    cmd = f"bash labs/cham.sh DMS {lid} {filename}"
    old = f'<p class="note">Chấm bằng Git Bash: <code>{_h.escape(cmd)}</code> — in <b>ĐÚNG</b> khi trùng.</p>'
    assert old in st["show"], "không thấy dòng chân trang cũ"
    new = (f'<p class="note">Chấm bằng Git Bash: <code>{_h.escape(cmd)}</code> — <code>bash</code> chạy một tệp lệnh; '
           f'<code>labs/cham.sh</code> là tệp chấm bài; <code>DMS {lid} {filename}</code> là khoá, bài và tên tệp của bạn. '
           'In <b>ĐÚNG</b> khi mọi dòng đầu ra trùng với kết quả mong đợi.</p>')
    st["show"] = st["show"].replace(old, new)
    st["say"] = CHAM_SAY
    assert n_sent(CHAM_SAY) == 4
    st["focus"] = [2, 2, 3, 3]
    return prac


def read_steps(rows, intro, says, split, note=None, intro2="Tiếp theo là các ký hiệu còn lại."):
    """như read_step nhưng tách thành hai step (hàng [:split] và [split:]) để bảng không tràn khung (render: 'nội dung TRÀN bảng')."""
    a = read_step(rows[:split], intro, says[:split], note=note)
    b = read_step(rows[split:], intro2, says[split:])
    return [a, b]


def add_read_step(prac, rows, intro, says, note=None):
    """thêm một step bảng đọc mã vào CUỐI cảnh Tự làm (sau gợi ý), có clear: true (fix12: cú pháp chỉ ở de.md phải hiện trên màn hình)"""
    prac["steps"].append(read_step(rows, intro, says, clear=True, note=note))
    return prac
