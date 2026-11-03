"""Thêm `clear: true` cho một step (bắt đầu bảng mới) khi nội dung tràn khung: add_clear.py lessons/…/Lxx.yaml cảnh.step …
Tìm dòng `say:` thứ k của bài (k = vị trí step), lùi lên dòng mở step “      - …”, chèn clear; đọc lại bài và kiểm."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools")); sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
p = Path(sys.argv[1])
for key in sys.argv[2:]:
    sp = lv.load_spec(p)
    keys = [f"{sc['id']}.{k}" for sc in sp["scenes"] for k, _ in enumerate(sc["steps"])]
    lines = p.read_text(encoding="utf-8").split("\n")
    says = [i for i, ln in enumerate(lines) if ln.startswith("        say:")]
    i = says[keys.index(key)]
    while not lines[i].startswith("      - "):
        i -= 1
    assert "clear:" not in lines[i]
    lines[i] = "      - clear: true\n        " + lines[i][8:]
    p.write_text("\n".join(lines), encoding="utf-8")
    st = {f"{sc['id']}.{k}": s for sc in lv.load_spec(p)["scenes"] for k, s in enumerate(sc["steps"])}[key]
    assert st.get("clear") is True and st.get("say"), key
    print(p.name[:3], key, "→ clear: true")
