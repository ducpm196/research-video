"""Phép chia CRC dạng chia dài, căn cột bằng phông đơn cách — sinh từ vết của alg.crc_remainder (không gõ tay).
Mỗi bước: dòng đa thức sinh đặt dưới bit 1 đứng đầu, rồi dòng kết quả XOR. Chạy → audit/net/fig/crc_*.html (một dòng mỗi tệp)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402


def sp(n):
    return "&nbsp;" * n


def division(data, gen, show_steps=None):
    k = len(gen) - 1
    rem, trace = alg.crc_remainder(data, gen)
    rows = [f'<div>{data}<span style="color:#9ca3af">{"0" * k}</span>&nbsp;&nbsp;(nối {k} số 0)</div>']
    steps = trace if show_steps is None else trace[:show_steps]
    for n, (i, after) in enumerate(steps, 1):
        rows.append(f'<div style="color:#d97706">{sp(i)}{gen}&nbsp;&nbsp;(XOR bước {n})</div>')
        lead = len(after) - len(after.lstrip("0"))
        shown = sp(lead) + after[lead:] if lead < len(after) else sp(len(after))
        rows.append(f'<div>{shown}</div>')
    if show_steps is not None and show_steps < len(trace):
        rows.append(f'<div style="color:#6b7280">… còn {len(trace) - show_steps} bước XOR nữa …</div>')
    rows.append(f'<div><b>phần dư = {rem}</b></div>')
    return '<div class="code">' + "".join(rows) + "</div>", rem, len(trace)


if __name__ == "__main__":
    fig = ROOT / "audit" / "net" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    main, rem, n = division("11010011101100", "1011", show_steps=3)
    assert rem == "100" and n == 9
    quiz, rem2, n2 = division("101110", "1001")
    assert rem2 == "011" and n2 == 4
    (fig / "crc_main.html").write_text(main, encoding="utf-8")
    (fig / "crc_quiz.html").write_text(quiz, encoding="utf-8")
    print("crc_main (3/9 bước), crc_quiz (4 bước) →", fig)
