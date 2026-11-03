"""Bảng vết thay trang cho OSY L10 — sinh HTML một dòng từ mô phỏng (cùng logic với tools/checklib.page_faults), không gõ tay.
Mỗi cột = một lần tham chiếu; các dòng = nội dung khung SAU lần đó; dòng cuối đánh dấu ● (chấm đỏ) nếu lỗi trang. Kiểm: số ● = page_faults.
Chạy: .venv/Scripts/python audit/osy/pagetrace.py → audit/osy/fig/trace_*.html"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib  # noqa: E402


def trace(ref, frames, policy):
    slots, order, cols = [None] * frames, [], []   # slots: nội dung từng khung (giữ vị trí); order: thứ tự để chọn nạn nhân
    for i, p in enumerate(ref):
        fault = p not in slots
        if not fault:
            if policy == "LRU":
                order.remove(p); order.append(p)
        else:
            if None in slots:
                slots[slots.index(None)] = p
            else:
                if policy == "OPT":
                    fut = ref[i + 1:]
                    v = max(slots, key=lambda q: fut.index(q) if q in fut else 10 ** 9)
                else:
                    v = order[0]
                order.remove(v); slots[slots.index(v)] = p
            order.append(p)
        cols.append((p, list(slots), fault))
    assert sum(f for _, _, f in cols) == checklib.page_faults(ref, frames, policy)
    return cols


def html(cols):
    n = len(cols[0][1])
    h = ['<table class="t trace"><tr><th>tham chiếu</th>' + "".join(f"<th>{p}</th>" for p, _, _ in cols) + "</tr>"]
    for k in range(n):
        h.append(f"<tr><td>khung {k + 1}</td>" + "".join(f"<td>{'' if s[k] is None else s[k]}</td>" for _, s, _ in cols) + "</tr>")
    h.append('<tr><td>lỗi</td>' + "".join(f"<td>{'<b class=&quot;red&quot;>●</b>' if f else ''}</td>" for _, _, f in cols) + "</tr></table>")
    return "".join(h).replace("&quot;", '"')


if __name__ == "__main__":
    fig = ROOT / "audit" / "osy" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    R = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    for name, (n, pol) in {"fifo3": (3, "FIFO"), "fifo4": (4, "FIFO"), "lru3": (3, "LRU"), "opt3": (3, "OPT")}.items():
        cols = trace(R, n, pol)
        (fig / f"trace_{name}.html").write_text(html(cols), encoding="utf-8")
        print(name, sum(f for *_, f in cols))
