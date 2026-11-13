"""Bổ sung sổ `audit/review/screen_code/JVA.yaml` sau `screen_code.py gen-jva`: các khối KHÔNG phải mã Java (lệnh Git Bash, thông báo
lỗi nhiều dòng, ...) mà gen-jva báo "CHƯA KHỚP" được khai tay (`hand: true`) theo bảng HAND dưới đây, khoá bằng NGUYÊN VĂN khối.
Dùng: .venv/Scripts/python -B audit/jva/screen_hand.py   (chạy ngay sau gen-jva; in các khối còn thiếu luật)"""
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.stdout.reconfigure(encoding="utf-8")
import screen_code as sc  # noqa: E402

REG = ROOT / "audit" / "review" / "screen_code" / "JVA.yaml"
BASH_SYNTAX = {"kind": "syntax", "lang": "bash"}


def out_of_src(lesson, text, reg):
    """Thông báo javac nhiều dòng (dòng đầu dạng `Tên.java:N: error: …`) → output `of` nguồn lỗi biên dịch cùng tên."""
    m = re.match(r"(\w+)\.java:\d+: error:", text)
    if not m:
        return None
    for k, v in (reg.get("sources") or {}).items():
        if k.startswith(f"{lesson}_") and v.get("java_class") == m.group(1) and v.get("expect_compile_error"):
            return {"kind": "output", "of": f"src:JVA:{k}", "reason": f"thông báo javac của chương trình {m.group(1)}"}
    return None


# văn bản khối (nguyên văn) → mục sổ. Giá trị là dict, hoặc hàm (lesson, key, blocks, reg) → dict.
def after(text_prev, **extra):
    """Khối chạy tiếp lệnh trước: nối văn bản đã ghim của khối `text_prev` cùng bài làm prelude."""
    def f(lesson, key, blocks, reg):
        for k, t in blocks.items():
            if k.split()[1] == lesson and t == text_prev:
                return dict({"kind": "run", "lang": "bash", "prelude_keys": [k]}, **extra)
        raise KeyError(text_prev)
    return f


PHI_CMD = "javac PhiArgs.java\njava PhiArgs 499999\njava PhiArgs 500000\njava PhiArgs 10000000\njava PhiArgs"
PHI_OUT = "499999 -> phi 0\n500000 -> phi 2200\n10000000 -> phi 5500\n500000 -> phi 2200"
RUT_CMD = 'javac RutNhap.java\necho "300000 500000" | java RutNhap\necho "800000 500000" | java RutNhap'
RUT_OUT = "Khong du tien\nDa rut, con 300000"


ARGS_CMD = "javac TongArgs.java\njava TongArgs 7000000 4000000 9000000\njava TongArgs 1500000 2500000\njava TongArgs"
ARGS_OUT = "3 lenh, tong 20000000\n2 lenh, tong 4000000\n0 lenh, tong 0"
NHAP_CMD = 'javac TongNhap.java\necho "1200000 800000 500000 2500000" | java TongNhap'
NHAP_OUT = "4 lenh, tong 5000000"


def run_cmd(files, expect, claims=None, **extra):
    """Khối lệnh Git Bash chạy thật: `files` = {tên tệp: nguồn} ghi vào thư mục chạy; khẳng định = đầu ra chuẩn."""
    return dict({"kind": "run", "lang": "bash", "files": files, "expect_stdout": expect,
                 "claims": claims or ["kết quả chạy hiện ngay dưới khối lệnh"]}, **extra)


def of_cmd(cmd_text):
    """Khối kết quả đứng sau một khối lệnh: output `of` khối lệnh đó (so từng dòng với đầu ra thật)."""
    def f(lesson, key, blocks, reg):
        for k, t in blocks.items():
            if k.split()[1] == lesson and t == cmd_text:
                return {"kind": "output", "of": k, "reason": "kết quả thật của khối lệnh ngay trên"}
        raise KeyError(cmd_text)
    return f


def io_programs():
    """Chương trình đọc bàn phím (lib.PROGRAMS_IO): gen-jva không thấy; ta thêm NGUỒN chỉ-biên-dịch để khối mã là đoạn trích của nó."""
    sys.path[:0] = [str(ROOT / "audit" / "jva"), str(ROOT / "audit" / "jva" / "src")]
    import importlib
    import lib
    for f in sorted((ROOT / "audit/jva/src").glob("l*.py")):
        lib.begin(f.stem.upper())
        importlib.import_module(f.stem).build()
    return lib.PROGRAMS_IO


def io_rule(lesson, text, ios, reg):
    frag = sc._dedent_lines(text)
    for pr in ios:
        if pr["lesson"] != lesson:
            continue
        name = f"{lesson}_{pr['name']}"
        hl = pr["code"].split("\n")
        if any(sc._dedent_lines("\n".join(hl[i:i + len(frag)])) == frag for i in range(len(hl) - len(frag) + 1)):
            return {"kind": "fragment", "within": f"src:JVA:{name}", "reason": f"dãy dòng của chương trình {pr['name']} (đọc bàn phím; nguồn chỉ biên dịch)"}
    return None


HAND = {
    PHI_CMD: run_cmd({"PhiArgs.java": "src:JVA:L03_PhiArgs"}, PHI_OUT),
    PHI_OUT: of_cmd(PHI_CMD),
    RUT_CMD: run_cmd({"RutNhap.java": "src:JVA:L03_RutNhap"}, RUT_OUT),
    RUT_OUT: of_cmd(RUT_CMD),
    ARGS_CMD: run_cmd({"TongArgs.java": "src:JVA:L04_TongArgs"}, ARGS_OUT),
    ARGS_OUT: of_cmd(ARGS_CMD),
    NHAP_CMD: run_cmd({"TongNhap.java": "src:JVA:L04_TongNhap"}, NHAP_OUT),
    NHAP_OUT: of_cmd(NHAP_CMD),
    "javac -version": {"kind": "run", "lang": "bash", "claims": ["lệnh in ra số phiên bản, ví dụ javac 21.0.2"],
                       "post": 'v=$(javac -version 2>&1); [[ $v =~ ^javac\\ ([0-9]+) ]] && [ "${BASH_REMATCH[1]}" -ge 21 ]'},
    "mkdir -p ~/hoc/jva\ncd ~/hoc/jva\npwd\nls": BASH_SYNTAX,
    "javac Chao.java": {"kind": "run", "lang": "bash", "files": {"Chao.java": "src:JVA:L00_Chao"},
                        "claims": ["không có lỗi thì không in gì, và trong thư mục xuất hiện thêm tệp Chao.class"],
                        "expect_stdout": "", "post": "test -f Chao.class"},
    "java Chao": after("javac Chao.java", files={"Chao.java": "src:JVA:L00_Chao"},
                       claims=["khối kết quả ngay sau: Chao ban! / So du: 100000 dong"],
                       expect_stdout="Chao ban!\nSo du: 100000 dong"),
    "cd ~\njavac Chao.java": BASH_SYNTAX,
    'jshell> int soLenh = 100\nsoLenh ==> 100\njshell> soLenh * 3\n$2 ==> 300\njshell> long lon = 3000000000L\nlon ==> 3000000000\n'
    'jshell> 1 + 2 + "A"\n$4 ==> "3A"': {
        "kind": "output", "reason": "phiên jshell thật (JDK 21.0.13): các dòng gõ vào và giá trị máy in, đã chạy và so từng dòng"},
    "error: file not found: Chao.java\nUsage: javac <options> <source files>\nuse --help for a list of possible options": {
        "kind": "output", "reason": "đầu ra thật của javac khi tệp không có trong thư mục đang đứng (đã chạy bằng JDK 21.0.13)"},
}


def main():
    subprocess.run([sys.executable, "-B", str(ROOT / "audit" / "review" / "screen_code.py"), "gen-jva"], check=True,
                   capture_output=True)
    blocks = sc.all_blocks("JVA")
    reg = yaml.safe_load(REG.read_text(encoding="utf-8"))
    bl = reg["blocks"]
    for k in [k for k in bl if k not in blocks]:     # mục tay mồ côi
        del bl[k]
    ios = io_programs()
    reg.setdefault("sources", {})
    for pr in ios:
        reg["sources"][f"{pr['lesson']}_{pr['name']}"] = {"lang": "java", "java_class": pr["name"], "kind": "syntax", "code": pr["code"]}
    todo = []
    for k, t in blocks.items():
        if k in bl and bl[k].get("sha") == sc.digest(t):
            continue
        lesson = k.split()[1]
        rule = HAND.get(t) or out_of_src(lesson, t, reg) or io_rule(lesson, t, ios, reg)
        if callable(rule):
            rule = rule(lesson, k, blocks, reg)
        if rule is None:
            todo.append(k)
            bl.pop(k, None)
            continue
        e = {"sha": sc.digest(t)}
        e.update(rule)
        e["hand"] = True
        bl[k] = e
    hdr = ("# Sổ mã trên màn hình khoá JVA — SINH bằng `screen_code.py gen-jva` từ audit/jva/src (lib.PROGRAMS).\n"
           "# Mục `hand: true` (khối không khớp chương trình nào) do audit/jva/screen_hand.py điền; được giữ qua các lần sinh lại.\n")
    REG.write_text(hdr + yaml.safe_dump(reg, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8", newline="\n")
    print(f"screen_hand: {len(bl)} mục; còn thiếu luật: {len(todo)}")
    for k in todo:
        print("  THIẾU", k, "|", repr(blocks[k][:100]))


if __name__ == "__main__":
    main()
