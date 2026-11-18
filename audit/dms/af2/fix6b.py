"""Hạ tầng sửa vòng 4, đợt B (fix6b, 2026-11-16) cho DMS L11–L20: dùng lại fix6lib (bảng đọc mã, chân trang chấm bài)
và thêm `asr_keep`: khôi phục mục `asr_reviewed` thêm tay sau AF2 (không có trong base/) khi sinh lại bài từ script.
Mục nằm ở audit/dms/af2/fix6b_asr_keep/Lnn.json (trích nguyên văn từ bài/mẫu trước khi sinh lại)."""
import json
from pathlib import Path

from fix6lib import *  # noqa
from af2lib import BASE  # noqa

KEEP = Path(__file__).resolve().parent / "fix6b_asr_keep"


def asr_entries(lid):
    p = KEEP / f"{lid}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def asr_lines(lid):
    return "".join('  - {sentence: %s, reason: %s}\n' % (json.dumps(e["sentence"], ensure_ascii=False), json.dumps(e["reason"], ensure_ascii=False))
                   for e in asr_entries(lid))


def asr_keep(lid):
    """tuple `repl` cho apply(): thêm các mục asr_reviewed đã giữ vào bản gốc (dạng `asr_reviewed: []` hoặc `asr_reviewed:`)"""
    es = asr_lines(lid)
    if not es:
        return []
    f = next(BASE.glob(f"{lid}_*.yaml"))
    t = f.read_text(encoding="utf-8")
    if "\nasr_reviewed: []" in t:
        return [("asr_reviewed: []", "asr_reviewed:\n" + es.rstrip("\n"))]
    return [("asr_reviewed:\n", "asr_reviewed:\n" + es)]


def hint_parts2(box_html, main_say, rows, says, tail_say, intro=None):
    """như hint_parts nhưng câu kết ("Lời giải nằm trong thư mục…") nói SAU các hàng của bảng; trả (html, say, focus)"""
    assert len(rows) == len(says)
    for s in ([intro] if intro else []) + list(says):
        assert n_sent(s) == 1, s
    html = box_html + read_table(rows)
    parts = [main_say] + ([intro] if intro else []) + list(says) + [tail_say]
    focus = [1] * n_sent(main_say) + (["2.1"] if intro else []) + [f"2.{i + 2}" for i in range(len(rows))] + [1] * n_sent(tail_say)
    return html, " ".join(parts), focus


from fix6lib import read_steps as _read_steps  # noqa: E402

INTRO2 = "Tiếp theo là các ký hiệu còn lại nữa."


def read_steps(rows, intro, says, split=3, note=None, intro2=INTRO2):
    """bảng > 4 hàng tách thành hai step liên tiếp (render: 'TRÀN bảng'); trả list step. Dùng flat() khi ghép vào cảnh."""
    return _read_steps(rows, intro, says, split, note=note, intro2=intro2)


def flat(*items):
    out = []
    for x in items:
        out.extend(x if isinstance(x, list) else [x])
    return out


def hint_steps2(box_html, main_say, rows, says, tail_say, tail_html, split=3, intro2=INTRO2):
    """gợi ý có bảng > 4 hàng: step A = hộp + bảng hàng [:split]; step B (clear) = bảng hàng còn lại + dòng lời giải. Trả [A, B] (mỗi phần tử là dict step)."""
    assert len(rows) == len(says)
    for s in [intro2] + list(says):
        assert n_sent(s) == 1, s
    nb = n_sent(main_say)
    a = step(box_html + read_table(rows[:split]), " ".join([main_say] + list(says[:split])),
             focus=[1] * nb + [f"2.{i + 2}" for i in range(split)], clear=True)
    nt = n_sent(tail_say)
    b = step(read_table(rows[split:]) + tail_html, " ".join([intro2] + list(says[split:]) + [tail_say]),
             focus=["1.1"] + [f"1.{i + 2}" for i in range(len(rows) - split)] + [2] * nt, clear=True)
    return [a, b]


import fix6lib as _f6  # noqa: E402

GIT_BASH = ("Git Bash là cửa sổ gõ lệnh trên Windows (đi kèm Git for Windows): vào thư mục bài làm, bấm chuột phải vào chỗ trống, "
            "chọn <b>Open Git Bash here</b>. ")


def patch_cham(prac, lid, filename):
    """fix12: như fix6lib.patch_cham, thêm ĐẦU ghi chú câu giải nghĩa Git Bash (chỉ đổi `show`, không đổi `say`)"""
    _f6.patch_cham(prac, lid, filename)
    st = prac["steps"][1]
    marker = '<p class="note">Chấm bằng Git Bash:'
    assert st["show"].count(marker) == 1
    st["show"] = st["show"].replace(marker, '<p class="note">' + GIT_BASH + 'Chấm bằng Git Bash:')
    return prac
