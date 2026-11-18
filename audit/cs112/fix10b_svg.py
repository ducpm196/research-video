"""fix10 CS112: sửa hình SVG L25 (hợp–tìm) và L26 (Venn P/NP) — nhãn không đè nút/viền, không ra ngoài khung. Chạy một lần."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit  # noqa

D = Path(__file__).resolve().parent
# ---- L25 dsu_svg.py
f = D / "dsu_svg.py"
edit(f, 'def label(x, y, s, size=22, fill="#374151", bold=False):\n    w = \' font-weight="700"\' if bold else ""\n    return f\'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{fill}"{w}>{s}</text>\'',
     'def label(x, y, s, size=22, fill="#374151", bold=False):\n    """s có thể là danh sách dòng (mỗi dòng cách 26 px) để nhãn không rộng quá cột"""\n    w = \' font-weight="700"\' if bold else ""\n    lines = [s] if isinstance(s, str) else s\n    return "".join(f\'<text x="{x}" y="{y + 26 * k}" font-size="{size}" text-anchor="middle" fill="{fill}"{w}>{t}</text>\' for k, t in enumerate(lines))')
edit(f, 'width="1000" height="520" viewBox="0 0 1000 520"', 'width="1000" height="590" viewBox="0 0 1000 590"')
edit(f, 'out.append(label(210, 215, "trước: nhóm {1, 2, 3} (3 nút) và nhóm {4, 5} (2 nút)", 21))',
     'out.append(label(210, 222, ["trước: nhóm {1, 2, 3} (3 nút)", "và nhóm {4, 5} (2 nút)"], 21))')
edit(f, 'out.append(label(750, 215, "sau union(3, 5): gốc nhóm nhỏ (4) gắn vào gốc nhóm lớn (1)", 21))',
     'out.append(label(750, 222, ["sau union(3, 5): gốc nhóm nhỏ (4)", "gắn vào gốc nhóm lớn (1)"], 21))')
edit(f, 'out.append(label(210, 505, "chuỗi 5 → 4 → 3 → 2 → 1: tìm gốc từ 5 tốn 4 bước", 21))',
     'out.append(label(210, 545, ["chuỗi 5 → 4 → 3 → 2 → 1:", "tìm gốc từ 5 tốn 4 bước"], 21))')
edit(f, 'out.append(label(750, 505, "sau find(5) có nén đường: mọi nút trỏ thẳng về gốc 1", 21))',
     'out.append(label(750, 545, ["sau find(5) có nén đường:", "mọi nút trỏ thẳng về gốc 1"], 21))')
# ---- L26 pnp_svg.py
f = D / "pnp_svg.py"
edit(f, 'txt(500, 56, "NP: kiểm được chứng chỉ nhanh", 28, True, "#2563eb"),', 'txt(500, 82, "NP: kiểm được chứng chỉ nhanh", 26, True, "#2563eb"),')
edit(f, 'txt(260, 175, "P", 40, True, "#059669"), txt(260, 212, "giải được nhanh", 24), txt(260, 242, "sắp xếp, đường ngắn nhất", 22),',
     'txt(260, 160, "P", 40, True, "#059669"), txt(260, 195, "giải được nhanh", 24), txt(260, 224, "sắp xếp,", 22), txt(260, 250, "đường ngắn nhất", 22),')
edit(f, 'txt(730, 160, "NP-đầy đủ", 32, True, "#d97706"), txt(730, 200, "phủ đỉnh, tổng tập con,", 22), txt(730, 230, "người du lịch (quyết định)", 22),',
     'txt(730, 150, "NP-đầy đủ", 32, True, "#d97706"), txt(730, 187, "phủ đỉnh, tổng tập con,", 22), txt(730, 215, "người du lịch", 22), txt(730, 243, "(quyết định)", 22),')
