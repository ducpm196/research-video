"""fix10 CS112: bỏ từ Latin (Git Bash, Windows) khỏi lời đọc bước Git Bash; dùng LaTeX cho ∑ ở L16. Chạy một lần."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, tpl, regen  # noqa

TPL = {"L17", "L18", "L21", "L23", "L24", "L25", "L26"}
OLD = "Git Bash là cửa sổ gõ lệnh trên Windows, mở bằng chuột phải trong thư mục bài làm. Gõ lệnh đầu để chạy chương trình, lệnh sau để chấm, lệnh chấm in chữ ĐÚNG khi mọi dòng khớp."
NEW = "Lệnh được gõ trong một cửa sổ dòng lệnh, mở bằng chuột phải trong thư mục bài làm. Lệnh đầu chạy chương trình, lệnh sau chấm bài, và in chữ ĐÚNG khi mọi dòng khớp."
for n in range(15, 30):
    lid = f"L{n}"
    edit(tpl(lid) if lid in TPL else lesson(lid), OLD, NEW)
edit(lesson("L16"), "(∑ = cộng lại mọi số hạng: $p_1x_1 + p_2x_2 + p_3x_3$)", "($\sum$ = cộng lại mọi số hạng: $p_1x_1 + p_2x_2 + p_3x_3$)")
for lid in sorted(TPL):
    regen(lid)
