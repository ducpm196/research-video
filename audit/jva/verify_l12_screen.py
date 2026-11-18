"""Kiểm L12 theo cách người học làm: GHÉP NGUYÊN VĂN các phần mã trên màn hình (cảnh `tep`) thành So.java, rồi áp đúng các chỉnh sửa
ghi ở chữ nhỏ của cảnh `pitfalls` (Lỗi 1, 3, 4), biên dịch + chạy THẬT và so với những gì màn hình chiếu, kể cả số dòng trong dấu vết.
(Vòng 2, 2026-11-14: màn hình từng hứa "đúng các số dòng ấy" nhưng các phần ghép lại ra số dòng lệch vì thiếu dòng trống.)
Được gọi từ verify_jva.py; không chạy riêng."""
import html
import re
import subprocess
import tempfile
from pathlib import Path


def screen_blocks(show):
    """Các khối mã trên màn hình (`<div class="code">…</div>`): mỗi khối = danh sách dòng chữ thật (bỏ thẻ, giải mã HTML)."""
    res = []
    for body in re.findall(r'<div class="code">((?:<div>.*?</div>)*)</div>', show, flags=re.S):
        lines = []
        for d in re.findall(r"<div>(.*?)</div>", body, flags=re.S):
            t = html.unescape(re.sub(r"<[^>]+>", "", d))
            lines.extend(x.rstrip() for x in t.split("\n"))
        res.append(lines)
    return res


def run_java(javac, name, code):
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / f"{name}.java").write_text(code + "\n", encoding="utf-8")
        c = subprocess.run(javac + ["-d", d, f"{name}.java"], capture_output=True, text=True, cwd=d, encoding="utf-8", errors="replace")
        if c.returncode != 0:
            return None, None, c.stderr
        r = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", d, name], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60, cwd=d)
        return r.stdout, r.stderr, ""


def nonblank(s):
    return [x.strip() for x in s.replace("\r\n", "\n").split("\n") if x.strip()]


def edit(src, cls, bug=False, drop_kiem=False, tail_kiem=False, drop_guard=False, one_lenh=False):
    """Các chỉnh sửa người học làm theo chữ nhỏ trên màn hình, áp lên So.java đã ghép."""
    lines = src.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "public class So {":
            ln = ln.replace("So", cls)
        if bug and "b + l.tien()" in ln:
            ln = ln.replace("b + l.tien()", "a + l.tien()")
        if drop_kiem and ln.strip().startswith("kiem();"):
            i += 1
            continue
        if drop_guard and "if (l.tu().equals(l.den())) {" in ln:
            i += 3
            continue
        if one_lenh and ln.strip().startswith("ds.add(new Lenh("):
            while lines[i].strip().startswith("ds.add(new Lenh("):
                i += 1
            out.append('        ds.add(new Lenh("A", "A", 100000));')
            continue
        out.append(ln)
        if tail_kiem and ln.strip() == 'System.out.println("Tong " + so.tong());':
            out.append("        so.kiem();")
        i += 1
    return "\n".join(out)


def check(spec, programs, javac):
    """Trả về danh sách (đạt?, mô tả)."""
    res = []
    sc = {s_["id"]: s_ for s_ in spec["scenes"]}
    so_prog = next(p for p in programs if p["lesson"] == "L12" and p["name"] == "So")
    parts = [screen_blocks(st_["show"])[0] for st_ in sc["tep"]["steps"]]
    asm = "\n".join("\n".join(pt) for pt in parts)
    want_src = "\n".join(x.rstrip() for x in so_prog["code"].split("\n"))
    same = asm == want_src
    res.append((same, f"{len(parts)} phần trên màn hình ghép nguyên văn = So.java đầy đủ ({len(asm.splitlines())} dòng)" if same
                else f"ghép {len(asm.splitlines())} dòng khác tệp {len(want_src.splitlines())} dòng"))
    so_out, _, cerr = run_java(javac, "So", asm)
    res.append((so_out is not None and nonblank(so_out) == nonblank(so_prog["out"]),
                "So.java ghép chạy ra đúng kết quả trên màn hình" + (f" ({cerr[:200]})" if cerr else "")))
    pit = sc["pitfalls"]["steps"]
    for idx, cls, kw in [(0, "SoLoi", dict(bug=True)),
                         (5, "CuoiNgay", dict(bug=True, drop_kiem=True, tail_kiem=True)),
                         (6, "TuChuyen", dict(drop_guard=True, one_lenh=True))]:
        shown = [x.strip() for blk in screen_blocks(pit[idx]["show"])[-1:] for ln in blk for x in ln.split("\n") if x.strip()]
        o, e, cerr = run_java(javac, cls, edit(asm, cls, **kw))
        if o is None:
            res.append((False, f"{cls}: không biên dịch được: {cerr[:200]}"))
            continue
        real = nonblank(o) + nonblank(e)
        res.append((real == shown, f"{cls}: ghép + chỉnh sửa theo chữ nhỏ cho kết quả và dấu vết khớp màn hình ({len(real)} dòng)"
                    if real == shown else f"{cls}: LỆCH. chạy thật {real!r}; màn hình {shown!r}"))
    return res
