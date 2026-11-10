"""Lỗi cấy cho cổng screen_code (AC3): mỗi ca dựng một khối + mục sổ TRONG BỘ NHỚ (không đụng kho) và đòi cổng
cho đúng kết luận. Ca dương (phải PASS) đi kèm để chứng minh nhánh kiểm chạy thật chứ không FAIL vì lỗi môi trường.
Chạy: .venv/Scripts/python -B audit/review/screen_code/negative_controls.py   (thoát 1 nếu một ca ra kết luận sai)"""
import datetime, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.stdout.reconfigure(encoding="utf-8")
import screen_code as sc  # noqa: E402

TA = "class TaiKhoan:\n    def __init__(self, so_du=0):\n        self._so_du = so_du\n    def rut(self, x):\n        self._so_du -= x"
CASES = [
    # (tên, {khoá: văn bản}, {khoá: mục (không cần sha — tự điền)}, khoá cần xét, kết luận mong đợi)
    ("python cú pháp: class một dòng (SDP L04 cũ)", {"K": "class CaPhe:   def gia(self): return 30"},
     {"K": dict(kind="run", lang="python", no_claim_reason="t")}, "K", False),
    ("python thiếu hàm nap (SDP L02 cũ)", {"K": TA},
     {"K": dict(kind="run", lang="python", post="a = TaiKhoan(200); a.nap(50); assert a._so_du == 250")}, "K", False),
    ("python sai kết quả", {"K": "x = 0.1 + 0.2"}, {"K": dict(kind="run", lang="python", post="assert x == 0.3")}, "K", False),
    ("python đúng kết quả (dương)", {"K": "x = 0.1 + 0.2"},
     {"K": dict(kind="run", lang="python", post="assert abs(x - 0.3) < 1e-12")}, "K", True),
    ("run không có khẳng định", {"K": "x = 1"}, {"K": dict(kind="run", lang="python")}, "K", False),
    ("pseudo thiếu reason", {"K": "nếu x lớn thì dừng"}, {"K": dict(kind="pseudo")}, "K", False),
    ("other thiếu read_check", {"K": "FROM python:3.12"}, {"K": dict(kind="other", lang="dockerfile", reason="r")}, "K", False),
    ("fragment không thuộc nguồn", {"H": "a = 1\nb = 2\nc = 3", "F": "b = 2\nd = 4"},
     {"H": dict(kind="run", lang="python", no_claim_reason="t"), "F": dict(kind="fragment", within="H", reason="r")},
     "F", False),
    ("fragment thuộc nguồn (dương)", {"H": "def f():\n    a = 1\n    b = 2\n    return a + b", "F": "a = 1\nb = 2"},
     {"H": dict(kind="run", lang="python", post="assert f() == 3"), "F": dict(kind="fragment", within="H", reason="r")},
     "F", True),
    ("output sai so với chạy thật", {"H": "print(1 + 1)", "O": "3"},
     {"H": dict(kind="run", lang="python", expect_stdout="2"), "O": dict(kind="output", of="H", reason="r")}, "O", False),
    ("output là chuỗi con của dòng thật (5 vs 50000)", {"H": "print('So du: 50000 dong')", "O": "So du: 5"},
     {"H": dict(kind="run", lang="python", expect_stdout="So du: 50000 dong"), "O": dict(kind="output", of="H", reason="r")},
     "O", False),
    ("output lược bằng … (dương)", {"H": "print('Cannot invoke X because Y is null')", "O": "Cannot invoke X …"},
     {"H": dict(kind="run", lang="python", expect_stdout="Cannot invoke X because Y is null"),
      "O": dict(kind="output", of="H", reason="r")}, "O", True),
    ("output cắt cụt KHÔNG có … ", {"H": "print('Cannot invoke X because Y is null')", "O": "Cannot invoke X"},
     {"H": dict(kind="run", lang="python", expect_stdout="Cannot invoke X because Y is null"),
      "O": dict(kind="output", of="H", reason="r")}, "O", False),
    ("stderr dòng lược bằng … khớp cả dòng (dương)", {"K": "raise ValueError('A because B')"},
     {"K": dict(kind="run", lang="python", expect_exception="ValueError",
                expect_stderr_contains="ValueError: A …")}, "K", True),
    ("stderr dòng lược bằng … nhưng sai chữ", {"K": "raise ValueError('A because B')"},
     {"K": dict(kind="run", lang="python", expect_exception="ValueError",
                expect_stderr_contains="ValueError: C …")}, "K", False),
    ("output đúng (dương)", {"H": "print(1 + 1)", "O": "2"},
     {"H": dict(kind="run", lang="python", expect_stdout="2"), "O": dict(kind="output", of="H", reason="r")}, "O", True),
    ("sqlite sai số dòng", {"K": "SELECT COUNT(*) FROM t;"},
     {"K": dict(kind="run", lang="sqlite", prelude="CREATE TABLE t(x); INSERT INTO t VALUES (1),(2);",
                prelude_reason="dữ liệu bài", expect_stdout="3")}, "K", False),
    ("sqlite đúng (dương)", {"K": "SELECT COUNT(*) FROM t;"},
     {"K": dict(kind="run", lang="sqlite", prelude="CREATE TABLE t(x); INSERT INTO t VALUES (1),(2);",
                prelude_reason="dữ liệu bài", expect_stdout="2")}, "K", True),
    ("prelude thiếu lý do", {"K": "print(y)"},
     {"K": dict(kind="run", lang="python", prelude="y = 1", expect_stdout="1")}, "K", False),
    ("C cú pháp sai (thiếu ;)", {"K": "int x = 5\nx++;"},
     {"K": dict(kind="syntax", lang="c", c_wrap="void f(void) {\n{CODE}\n}")}, "K", False),
    ("C cú pháp đúng (dương)", {"K": "int x = 5;\nx++;"},
     {"K": dict(kind="syntax", lang="c", c_wrap="void f(void) {\n{CODE}\n}")}, "K", True),
    ("C có chú thích // và /* */ (dương)", {"K": "int x = 5;   // năm\n/* tăng */ x++;"},
     {"K": dict(kind="syntax", lang="c", c_wrap="void f(void) {\n{CODE}\n}")}, "K", True),
    ("C: // nằm trong chuỗi không bị coi là chú thích → thiếu ; vẫn bắt", {"K": 'char *s = "a//b"\nint y = 1;'},
     {"K": dict(kind="syntax", lang="c", c_wrap="void f(void) {\n{CODE}\n}")}, "K", False),
    ("python in tiếng Việt (dương)", {"K": 'print("số dư âm")'},
     {"K": dict(kind="run", lang="python", expect_stdout="số dư âm")}, "K", True),
    ("node sai kết quả", {"K": "console.log(1 + '1');"},
     {"K": dict(kind="run", lang="node", expect_stdout="2")}, "K", False),
    ("node đúng (dương)", {"K": "console.log(1 + '1');"},
     {"K": dict(kind="run", lang="node", expect_stdout="11")}, "K", True),
    ("go cú pháp sai", {"K": "if x == 0 {"},
     {"K": dict(kind="syntax", lang="go", go_wrap="package main\nfunc main() {\nx := 0\n{CODE}\n}")}, "K", False),
    ("java lỗi biên dịch đúng như bài nói (dương)", {"K": "public class Main { void f() { int x = 1 } }"},
     {"K": dict(kind="run", lang="java", expect_compile_error="';' expected")}, "K", True),
    ("java chạy ra khác bài nói", {"K": "public class Main { public static void main(String[] a) { System.out.println(7 / 2); } }"},
     {"K": dict(kind="run", lang="java", expect_stdout="3.5")}, "K", False),
]


def main():
    bad = 0
    for name, blocks, reg, key, want in CASES:
        for k, e in reg.items():
            e["sha"] = sc.digest(blocks[k])
        ok, msg, _, _ = sc.Gate(blocks, reg).check(key)
        # ca âm chỉ tính ĐÚNG khi FAIL vì lỗi thật, không vì môi trường thiếu công cụ (NOT_VERIFIED)
        good = ok == want and not msg.startswith("NOT_VERIFIED")
        bad += not good
        print(f"{'ĐÚNG' if good else 'SAI '}  {name}: cổng {'PASS' if ok else 'FAIL'} (mong {'PASS' if want else 'FAIL'}) — {msg[:110]}")
    # STALE: đổi chữ sau khi ghim — kiểm bằng chính hàm so sha của cổng
    t0, t1 = "x = 1", "x = 2"
    stale_caught = sc.digest(t0) != sc.digest(t1)
    bad += not stale_caught
    print(f"{'ĐÚNG' if stale_caught else 'SAI '}  đổi chữ sau khi ghim → sha lệch (STALE)")
    print(f"negative_controls: {len(CASES) + 1 - bad}/{len(CASES) + 1} ca đúng kết luận")
    print("checked_at=" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
