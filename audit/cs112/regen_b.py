"""Phần B (L17, L18, L21, L23, L24, L25, L26): bài sinh từ mẫu audit/cs112/src/*.tpl.yaml + hình một dòng.
extract: trích hình từ bài ĐANG CÓ ra audit/cs112/fig/<Lxx>_<TÊN>.svg (căn từng dòng; chấp nhận mẫu có thêm dòng
asr_reviewed mà bài chưa có). gen: ghép lại mẫu + hình bằng fill_tpl.py (dùng lại regen_a.gen).
Dùng: .venv/Scripts/python -B audit/cs112/regen_b.py extract|gen L17 [L18 …]"""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import regen_a

regen_a.TPL.update({
    "L17": "L17_lap_lich", "L18": "L18_qhd", "L21": "L21_qhtt", "L23": "L23_sap_xep_nhanh",
    "L24": "L24_duong_di_ngan_nhat", "L25": "L25_cay_khung_nho_nhat", "L26": "L26_p_np_quy_dan",
})


def extract(lid):
    tpl = regen_a.rd(regen_a.SRC / (regen_a.TPL[lid] + ".tpl.yaml")).split("\n")
    les = regen_a.rd(regen_a.lesson_path(lid)).split("\n")
    sm = difflib.SequenceMatcher(None, tpl, les, autojunk=False)
    names = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or tag == "delete":
            continue
        assert tag == "replace" and i2 - i1 == j2 - j1, f"{lid}: khác biệt ngoài hình ở dòng mẫu {i1 + 1}"
        for a, b in zip(tpl[i1:i2], les[j1:j2]):
            parts = re.split(r"\{\{([A-Za-z0-9_]+)\}\}", a)
            rx = "^" + "".join(re.escape(p) if k % 2 == 0 else "(.*)" for k, p in enumerate(parts)) + "$"
            m = re.match(rx, b)
            assert m, f"{lid}: dòng hình không khớp mẫu"
            for n, svg in zip(parts[1::2], m.groups()):
                (regen_a.FIG / f"{lid}_{n}.svg").write_text(svg, encoding="utf-8", newline="")
                names.append(n)
    print(lid, "trích", len(names), "hình:", names)


def gen(lid):
    regen_a.gen(lid)
    p = regen_a.lesson_path(lid)
    crlf, lf = bytes([13, 10]), bytes([10])
    p.write_bytes(p.read_bytes().replace(crlf, lf))  # giữ LF như các bài khác


if __name__ == "__main__":
    cmd, ids = sys.argv[1], sys.argv[2:]
    for i in ids:
        (extract if cmd == "extract" else gen)(i)
