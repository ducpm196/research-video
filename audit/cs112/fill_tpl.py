"""Điền hình sinh bằng máy vào bài: fill_tpl.py audit/cs112/src/Lxx.tpl.yaml lessons/cs112/Lxx_….yaml TEN=audit/cs112/hinh.svg …
Mỗi “{{TEN}}” trong tệp mẫu được thay bằng nội dung một dòng của tệp hình (hình không vẽ tay — sinh từ dữ liệu, xem *_svg.py).
Không ghi đè nếu còn “{{” chưa thay."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
t = src.read_text(encoding="utf-8")
for kv in sys.argv[3:]:
    k, f = kv.split("=", 1)
    svg = Path(f).read_text(encoding="utf-8").strip()
    assert "\n" not in svg, f"{f}: hình phải là một dòng"
    assert "{{" + k + "}}" in t, f"mẫu không có {{{{{k}}}}}"
    t = t.replace("{{" + k + "}}", svg)
assert "{{" not in t, "còn chỗ chưa điền: " + t[t.index("{{"):t.index("{{") + 20]
dst.write_text(t, encoding="utf-8")
print("→", dst)
