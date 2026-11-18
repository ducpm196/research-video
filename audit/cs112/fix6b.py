"""fix6 CS112 L15–L29 (2026-11-16): công cụ vá bài/mẫu theo chuẩn P1 chặt.
- edit(path, old, new): thay đúng một chỗ (kiểm duy nhất), giữ kiểu xuống dòng (LF hay CRLF) của tệp.
- patch_cham(path): chân trang chấm bài có giải thích lệnh `bash labs/cham.sh …` tại chỗ + lời đọc thêm một câu.
- wc(path): số từ lời đọc.
Bài sinh từ mẫu (L17, L18, L21, L23–L26): vá MẪU `audit/cs112/src/*.tpl.yaml` rồi `regen_b.py gen`.
Dùng: .venv/Scripts/python -B audit/cs112/fix6b.py cham <tệp .yaml> [...]"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]


def rd(p):
    b = Path(p).read_bytes().decode("utf-8")
    return b.replace("\r\n", "\n"), "\r\n" in b


def wr(p, t, crlf):
    Path(p).write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))


def edit(path, old, new):
    t, crlf = rd(path)
    n = t.count(old)
    assert n == 1, f"{Path(path).name}: cần đúng 1 chỗ, thấy {n}: {old[:70]!r}"
    wr(path, t.replace(old, new), crlf)


def lesson(lid):
    return next((ROOT / "lessons" / "cs112").glob(lid + "_*.yaml"))


def tpl(lid):
    import regen_a
    import regen_b  # noqa: F401  (cập nhật bảng tên mẫu)
    return regen_a.SRC / (regen_a.TPL[lid] + ".tpl.yaml")


def regen(lid):
    """sinh lại bài từ mẫu đã vá (fill_tpl + hình một dòng); giữ LF như regen_b"""
    import regen_a
    import regen_b
    regen_b.gen(lid)


def clear_next(path, snippet):
    """thêm `clear: true` cho step đứng ngay sau step có lời đọc chứa `snippet` (để bảng đọc mã không đè lên nội dung sau)"""
    t, crlf = rd(path)
    assert t.count(snippet) == 1, f"{Path(path).name}: snippet phải duy nhất ({t.count(snippet)}): {snippet[:60]!r}"
    i = t.index(snippet)
    nl = chr(10)
    j = t.index(nl + "      - ", i)
    nxt = t[j + 1:j + 60]
    assert nxt.startswith("      - show: |") or nxt.startswith("      - clear: true"), nxt
    if nxt.startswith("      - clear: true"):
        return
    t = t[:j + 1] + "      - clear: true" + nl + "        show: |" + t[j + 1 + len("      - show: |"):]
    wr(path, t, crlf)


def ensure_clear(path, marker):
    """đảm bảo step có chữ `marker` trong phần show bắt đầu bằng `- clear: true` (mọi lần xuất hiện)"""
    t, crlf = rd(path)
    nl = chr(10)
    pos, n = 0, 0
    while True:
        i = t.find(marker, pos)
        if i < 0:
            break
        j = t.rfind(nl + "      - ", 0, i)
        head = t[j + 1:j + 60]
        if head.startswith("      - show: |"):
            t = t[:j + 1] + "      - clear: true" + nl + "        show: |" + t[j + 1 + len("      - show: |"):]
            n += 1
        pos = i + len(marker) + 30
    wr(path, t, crlf)
    return n


OLD_TAIL = " — in <b>ĐÚNG</b> khi trùng.</p>"
SAY_OLD = re.compile(
    r"Bạn chạy chương trình của mình rồi so từng dòng\. Nếu muốn chấm bằng máy, dùng lệnh ở dưới màn hình, "
    r"lệnh in chữ ĐÚNG khi đầu ra trùng(, hoặc chỉ ra dòng nào khác)?\.")
SAY_NEW = ("Bạn chạy chương trình của mình rồi so từng dòng với màn hình. "
           "Muốn chấm bằng máy, gõ lệnh ở chân màn hình: nó chạy tệp chấm bài, kèm khoá học, mã bài và tên tệp của bạn. "
           "Lệnh in chữ ĐÚNG khi mọi dòng trùng, hoặc chỉ ra dòng nào khác.")


def patch_cham(path):
    p = Path(path)
    t, crlf = rd(p)
    if "là tệp chấm bài" in t:
        print(p.name, "đã vá")
        return
    m = re.search(r"<code>bash labs/cham\.sh (CS112 L\d\d [A-Za-z0-9_.]+)</code>" + re.escape(OLD_TAIL), t)
    assert m, f"{p.name}: không thấy dòng chấm bài cũ"
    args = m.group(1)
    new_tail = (f" — <code>bash</code> chạy một tệp lệnh; <code>labs/cham.sh</code> là tệp chấm bài; "
                f"<code>{args}</code> là khoá, bài và tên tệp của bạn. In <b>ĐÚNG</b> khi mọi dòng đầu ra trùng với kết quả mong đợi.</p>")
    t = t[:m.end() - len(OLD_TAIL)] + new_tail + t[m.end():]
    i = m.start()
    j = t.index("        say: ", i)
    k = t.index("\n", j)
    say_line = t[j:k]
    assert SAY_OLD.search(say_line), f"{p.name}: lời đọc chân trang khác mẫu"
    say_new = SAY_OLD.sub(lambda _: SAY_NEW, say_line)
    fa = t.rindex("        focus: [", i, j)
    fb = t.index("\n", fa)
    foc = t[fa:fb]
    mm = re.match(r"        focus: \[(.*)\]$", foc)
    items = [x.strip() for x in mm.group(1).split(",")]
    items.append(items[-1])
    foc_new = "        focus: [" + ", ".join(items) + "]"
    t = t[:fa] + foc_new + t[fb:j] + say_new + t[k:]
    wr(p, t, crlf)
    print(p.name, "đã vá chân trang;", foc.strip(), "->", foc_new.strip())


if __name__ == "__main__":
    cmd, files = sys.argv[1], sys.argv[2:]
    for f in files:
        if cmd == "cham":
            patch_cham(f)
