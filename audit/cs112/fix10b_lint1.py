"""fix10 CS112: sửa lỗi lint E52 sau đợt thêm định nghĩa (L15: dùng \cdots thay \dots; L18: introduces bigTheta + focus câu cuối). Chạy một lần."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, tpl, regen  # noqa

edit(lesson("L15"), "$n! = n \cdot (n - 1) \cdot \dots \cdot 1$", "$n! = n \cdot (n - 1) \cdot (n - 2) \cdots 1$")
edit(tpl("L18"), '        focus: [["1.1", "1.2"], "1.3", ["2.1", "2.2"], "2.3", 0]', '        focus: [["1.1", "1.2"], "1.3", ["2.1", "2.2"], "2.3", 3]\n        introduces: [bigTheta]')
regen("L18")
