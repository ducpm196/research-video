"""Kiểm độc lập mọi khẳng định của khoá PLC — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Từ vựng: ôtômat viết tay đọc từng ký tự (không dùng re). Cú pháp, kết hợp, ưu tiên: bộ phân tích `ast` của chính Python.
Phạm vi tĩnh: chạy mã Python thật; phạm vi động: mô phỏng ngăn xếp lời gọi. Hợp nhất: thuật toán Robinson với phép hợp thế.
Đánh dấu–quét: BFS (checklib dùng DFS). Máy ngăn xếp: so với eval của Python. Gấp hằng số: so với bộ tối ưu của trình biên dịch
CPython (hằng số trong co_consts). JavaScript: chạy Node thật. Java: javac/java/javap thật (L05d–f, L09e, L10b; thêm 2026-11-09). C/C++: không có trình biên dịch
trên máy → NOT_VERIFIED, ghi rõ.
Chạy: .venv/Scripts/python audit/plc/verify_plc.py → PASS/FAIL từng dòng và tổng."""
import ast
import shutil
import struct
import subprocess
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00, L01: ôtômat viết tay ──
def lex2(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            out.append(("SO", s[i:j]))
            i = j
        elif c.isalpha() or c == "_":
            j = i
            while j < len(s) and (s[j].isalnum() or s[j] == "_"):
                j += 1
            w = s[i:j]
            out.append(("KHOA" if w in {"if", "while", "return", "def"} else "TEN", w))
            i = j
        elif s[i:i + 2] in ("==", "<=", ">="):
            out.append(("PHEP", s[i:i + 2]))
            i += 2
        elif c in "+-*/=<>()":
            out.append(("PHEP", c))
            i += 1
        else:
            out.append(("LOI", c))
            i += 1
    return out


for src in ["x1 = 42+y", "if x1<=10", "ifx", "if", "x-1", "count2>=c", "while1 = 2", "x = 3 @ 4", "x = = 3", "total = price * 3"]:
    rec("L01", lex2(src) == alg.lex(src), f"từ tố của “{src}”: {[t for _, t in lex2(src)]}")
rec("L00a", len(lex2("total = price * 3")) == 5 and ("LOI", "@") in lex2("x = 3 @ 4"), "5 từ tố; “@” lỗi từ vựng")


# ── L02, L03: cây của chính Python ──
def py_tree(src):
    def conv(n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.Name):
            return n.id
        op = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}[type(n.op)]
        return (op, conv(n.left), conv(n.right))
    return conv(ast.parse(src, mode="eval").body)


for src in ["1+2*3", "(1+2)*3", "8-3-2", "16/4/2", "2*3+4*5", "2*(3+4)", "20/5/2", "(8-3)*2", "x*(y+2)"]:
    rec("L02", py_tree(src) == alg.parse_expr(src), f"cây của “{src}” = cây của bộ phân tích Python: {alg.ast_str(py_tree(src))}")
vals = {"1+2*3": 7, "(1+2)*3": 9, "8-3-2": 3, "2*3+4*5": 26, "2*(3+4)": 14, "(8-3)*2": 10}
rec("L02a", all(eval(k) == v == alg.ast_eval(alg.parse_expr(k)) for k, v in vals.items()), "giá trị 7, 9, 3, 26, 14, 10")
rec("L03a", alg.ast_eval(alg.parse_expr("8-3-2", "right")) == 8 - (3 - 2) == 7 and alg.ast_eval(alg.parse_expr("16/4/2", "right")) == 16 // (4 // 2) == 8,
    "kết hợp phải: 7 và 8")
rec("L03b", eval("2**3**2") == 512 and eval("(2**3)**2") == 64 and eval("2**2**3") == 256, "luỹ thừa kết hợp phải: 512, 256")
rec("L03c", -7 // 2 == -4 and int(-7 / 2) == -3 and alg.ast_eval(("/", -7, 2)) == -3, "−7 chia nguyên 2: làm tròn xuống −4, về 0 −3")

# ── L04: phạm vi ──
env = {}
exec("x = 1\ndef f(): return x\ndef g():\n    x = 2\n    return f()\nr = g()\n", env)
rec("L04a", env["r"] == 1 == alg.scope_lookup("static"), "Python thật (tĩnh): g() = 1")


def dyn(gx, lx):
    stack = [{"x": gx}]

    def f():
        for fr in reversed(stack):
            if "x" in fr:
                return fr["x"]

    def g():
        stack.append({"x": lx})
        v = f()
        stack.pop()
        return v
    return g()


rec("L04b", dyn(1, 2) == 2 == alg.scope_lookup("dynamic") and dyn(5, 7) * 2 == 14, "mô phỏng phạm vi động: 2; quiz 14")
env = {}
exec("a = 5\ndef p(): return a * 2\ndef q():\n    a = 7\n    return p()\nr = q()\n", env)
rec("L04c", env["r"] == 10, "quiz tĩnh (Python thật): 10")
rec("L04d", alg.shadow_late() == 21 and alg.unbound_local() == "UnboundLocalError", "chọn biến: 21; gán sau đọc → UnboundLocalError")

# ── L05: kiểu ──
node = shutil.which("node")
if node:
    out = subprocess.run([node, "-e", 'console.log(JSON.stringify(["3"+1, "3"*2, "5"-2]))'], capture_output=True, text=True).stdout.strip()
    rec("L05a", out == '["31",6,3]', f"Node thật: \"3\"+1, \"3\"*2, \"5\"-2 → {out}")
else:
    print("NOT_VERIFIED L05a — không có Node")
rec("L05b", alg.py_add_error("3", 1) == "TypeError", "Python: \"3\" + 1 → TypeError khi chạy")
rec("L05c", struct.unpack("<I", struct.pack("<f", 1.0))[0] == 0x3F800000 == 1065353216, "bit của 1.0f đọc như số nguyên 32 bit = 1065353216")
# Java thật (JDK trên PATH, thêm 2026-11-09 đợt C): biên dịch trong thư mục tạm, đọc thông báo javac / chạy java / đọc javap.
import tempfile  # noqa: E402

javac, java, javap = shutil.which("javac"), shutil.which("java"), shutil.which("javap")


def jrun(files, main=None, javap_cls=None):
    """Biên dịch {tên tệp: mã}; trả (mã thoát javac, stderr javac, stdout java hoặc javap)."""
    with tempfile.TemporaryDirectory() as d:
        for n, s in files.items():
            (Path(d) / n).write_text(s, encoding="utf-8")
        c = subprocess.run([javac, *files], cwd=d, capture_output=True, text=True)
        out = ""
        if c.returncode == 0 and main:
            out = subprocess.run([java, "-cp", d, main], capture_output=True, text=True).stdout
        if c.returncode == 0 and javap_cls:
            out = subprocess.run([javap, "-c", "-v", "-cp", d, javap_cls], capture_output=True, text=True).stdout
        return c.returncode, c.stderr, out


if javac and java and javap:
    rc, err, _ = jrun({"A.java": 'public class A { public static void main(String[] a) { int x = "3" + 1; } }'})
    rec("L05d", rc != 0 and "incompatible types: String cannot be converted to int" in err, "javac: int x = \"3\" + 1; → lỗi biên dịch (JLS §5.2)")
    rc, _, out = jrun({"B.java": 'public class B { public static void main(String[] a) { System.out.println("3" + 1); } }'}, main="B")
    rec("L05e", rc == 0 and out.strip() == "31", "java: \"3\" + 1 → \"31\" (đổi số thành chuỗi, JLS §15.18.1)")
    bad = [jrun({"C.java": 'public class C { Object x = "%s" %s 2; }' % (s, op)})[1] for s, op in (("3", "*"), ("5", "-"))]
    rec("L05f", all("bad operand types" in e for e in bad), "javac: \"3\" * 2 và \"5\" - 2 → lỗi biên dịch (không tự đổi chuỗi thành số)")
    rc, _, out = jrun({"S.java": "import java.util.*;\npublic class S {\n static void them(List<Integer> ds){ ds.add(1); }\n"
                       " static void ganLai(List<Integer> ds){ ds = new ArrayList<>(List.of(9)); }\n"
                       " static void doiCho(Integer p, Integer q){ Integer t = p; p = q; q = t; }\n"
                       " public static void main(String[] x){ List<Integer> a = new ArrayList<>(List.of(0)); them(a);\n"
                       "  List<Integer> b = new ArrayList<>(List.of(0)); ganLai(b); Integer p = 1, q = 2; doiCho(p, q);\n"
                       "  System.out.println(a + \" \" + b + \" \" + p + \",\" + q); } }"}, main="S")
    rec("L09e", out.strip() == "[0, 1] [0] 1,2", f"Java chia sẻ đối tượng: sửa thấy, gán lại không, hoán đổi không → {out.strip()}")
    rc, _, out = jrun({"M.java": "public class M {\n static int trai(int a,int b,int c,int d){ return ((a+b)+c)+d; }\n"
                       " static int phai(int a,int b,int c,int d){ return a+(b+(c+d)); }\n}"}, javap_cls="M")
    import re as _re  # noqa: E402
    st = _re.findall(r"static int (\w+)\(.*?stack=(\d+)", out, _re.S)
    rec("L10b", st == [("trai", "2"), ("phai", "4")], f"máy ảo Java: hàm khai độ cao tối đa (max_stack, JVMS §4.7.3): lệch trái 2, lệch phải 4 → {st}")
else:
    print("NOT_VERIFIED L05d/L05e/L05f/L09e/L10b — không có javac/java/javap trên máy")


# ── L06: hợp nhất Robinson ──
def subst(t, s):
    if isinstance(t, str) and t in s:
        return subst(s[t], s)
    if isinstance(t, tuple):
        return (t[0],) + tuple(subst(x, s) for x in t[1:])
    return t


def occurs(v, t):
    return t == v or (isinstance(t, tuple) and any(occurs(v, x) for x in t[1:]))


def robinson(pairs):
    s = {}
    work = list(pairs)
    while work:
        a, b = work.pop()
        a, b = subst(a, s), subst(b, s)
        if a == b:
            continue
        if isinstance(b, str) and b.startswith("'") and not (isinstance(a, str) and a.startswith("'")):
            a, b = b, a
        if isinstance(a, str) and a.startswith("'"):
            if occurs(a, b):
                return None
            s = {k: subst(v, {a: b}) for k, v in s.items()}
            s[a] = b
        elif isinstance(a, tuple) and isinstance(b, tuple) and a[0] == b[0]:
            work += list(zip(a[1:], b[1:]))
        else:
            return None
    return s


def same(s1, s2, vars_):
    return (s1 is None and s2 is None) or (s1 is not None and s2 is not None and all(subst(v, s1) == alg.resolve(v, s2) for v in vars_))


cases = [((("->", "'a", "bool"), ("->", "int", "'r")), ["'a", "'r"]), ((("->", "'a", "int"), ("->", "bool", "'c")), ["'a", "'c"]),
         ((("->", "int", "int"), ("->", "int", "bool")), []), (("'a", ("->", "'a", "'b")), ["'a"]), (("int", "bool"), [])]
for (x, y), vs in cases:
    rec("L06", same(robinson([(x, y)]), alg.unify(x, y), vs), f"hợp nhất {x} với {y}")
s = robinson([("'a", "int"), ("'b", "int")])
rec("L06a", subst(("->", "'a", "'b"), s) == ("->", "int", "int"), "nhan_doi : int → int")

# ── L07: bao đóng (Python thật) ──
rec("L07a", alg.late_binding() == ([2, 2, 2], [0, 1, 2]) and [f() for f in [lambda: i for i in range(3)]] == [2, 2, 2], "bắt muộn [2,2,2]; sửa [0,1,2]")
c1, c2 = alg.make_counter(), alg.make_counter()
rec("L07b", [c1(), c1(), c1(), c2()] == [1, 2, 3, 1], "hai bộ đếm 1,2,3 và 1")
rec("L07c", (lambda mk: (mk(5)(3), mk(10)(mk(5)(1))))(lambda n: lambda x: x + n) == (8, 16), "quiz 8, 16")


# ── L08: BFS + đếm tham chiếu dây chuyền viết lại ──
def bfs_live(h, roots):
    seen, q = set(roots), deque(roots)
    while q:
        v = q.popleft()
        for w in h[v]:
            if w not in seen:
                seen.add(w)
                q.append(w)
    return seen


def rc_free(h, roots):
    cnt = {k: 0 for k in h}
    for vs in h.values():
        for w in vs:
            cnt[w] += 1
    for r in roots:
        cnt[r] += 1
    alive = set(h)
    changed = True
    while changed:
        changed = False
        for k in list(alive):
            if cnt[k] == 0:
                alive.discard(k)
                for w in h[k]:
                    cnt[w] -= 1
                changed = True
    return set(h) - alive


H1 = {"A": ["B"], "B": ["C"], "C": [], "D": ["E"], "E": ["D"]}
H2 = {"R": ["X"], "X": ["Y"], "Y": ["X"], "Z": ["W"], "W": []}
rec("L08a", bfs_live(H1, ["A"]) == alg.mark_sweep(H1, ["A"])[0] == {"A", "B", "C"}, "sống A, B, C; rác D, E")
rec("L08b", rc_free(H1, ["A"]) == alg.refcount_free(H1, ["A"]) == set(), "đếm tham chiếu không thu hồi vòng D ↔ E")
rec("L08c", set(H2) - bfs_live(H2, ["R"]) == {"Z", "W"} == rc_free(H2, ["R"]) == alg.refcount_free(H2, ["R"]), "quiz: cả hai thu hồi Z, W")

# ── L09 ──
d = alg.sharing_demo()
rec("L09a", d["them"] == [0, 1] and d["gan_lai"] == [0] and d["doi_cho"] == (1, 2), "sửa thấy, gán lại không, hoán đổi không")
rec("L09b", d["bad"] == ([1, 2], [1, 2]) and d["bad_same"] and d["good"] == ([1], [2]), "mặc định danh sách dùng chung; sửa bằng None")
m = {"k": 1}


def doi(x):
    x["k"] = 2


def thay(x):
    x = {"k": 3}  # noqa: F841


doi(m)
thay(m)
rec("L09c", m["k"] == 2, "quiz: m[\"k\"] = 2")
print("NOT_VERIFIED L09d — C++ hoán đổi qua int& : không có trình biên dịch C++ trên máy (chuẩn C++ [dcl.ref])")

# ── L10: máy ngăn xếp so với eval ──
for src, envv in [("1+2*3", {}), ("7-2", {}), ("(8-3)*2", {}), ("x*(y+2)", {"x": 3, "y": 4})]:
    rec("L10", alg.stack_vm(alg.stack_gen(alg.parse_expr(src)), envv) == [eval(src, {}, envv)], f"máy ngăn xếp “{src}” = eval = {eval(src, {}, envv)}")
code = alg.stack_gen(alg.parse_expr("1+2*3"))
depth = [sum(1 if c[0] in ("push", "load") else -1 for c in code[:k + 1]) for k in range(len(code))]
rec("L10a", depth == [1, 2, 3, 2, 1] and [len(s) for s in alg.stack_vm(code, trace=True)[1]] == depth, "độ cao ngăn xếp 1,2,3,2,1 — cuối còn 1")

# ── L11: bộ tối ưu của CPython ──
consts = compile("2*3+x", "<s>", "eval").co_consts
rec("L11a", 6 in consts and alg.const_fold(alg.parse_expr("2*3+x")) == ("+", 6, "x"), f"CPython cũng gấp 2*3 → 6 (co_consts = {consts})")
consts2 = compile("x+2+3", "<s>", "eval").co_consts
rec("L11b", 5 not in consts2 and alg.const_fold(alg.parse_expr("x+2+3")) == ("+", ("+", "x", 2), 3), f"x+2+3 không gấp (co_consts = {consts2})")
rec("L11c", (0.1 + 0.2) + 0.3 == 0.6000000000000001 and 0.1 + (0.2 + 0.3) == 0.6, "số thực không kết hợp")
rec("L11d", 21 in compile("(1+2)*(3+4)", "<s>", "eval").co_consts and alg.const_fold(alg.parse_expr("4*5-x*2")) == ("-", 20, ("*", "x", 2)), "quiz: 21; (− 20 (* x 2))")
print("NOT_VERIFIED L11e — C: if (x + 1 > x) bị gấp thành đúng khi tối ưu: không có trình biên dịch C trên máy (C17 §6.5¶5)")

# ── L12 ──
from functools import reduce  # noqa: E402
rec("L12a", reduce(lambda a, b: a + b, (x * x for x in range(1, 7) if x % 2 == 0), 0) == 56, "tổng bình phương số chẵn 1..6 = 56")
rec("L12b", reduce(lambda a, b: a * b, (x for x in range(1, 6) if x % 2), 1) == 15, "tích số lẻ 1..5 = 15")
t = ([1], 2)
t[0].append(3)
rec("L12c", t == ([1, 3], 2), "bộ chứa danh sách vẫn bị sửa bên trong")
l0 = (1, (2, None))
a, b = (9, l0), (8, l0)
nodes = {id(a), id(b), id(l0), id(l0[1])}
rec("L12d", len(nodes) == 4 and a[1] is b[1], "4 nút; phần đuôi dùng chung")

# ── L13: hành trình an toàn bộ nhớ — tính lại bằng đường khác (đếm thẳng, mô phỏng, phân số đúng) ──
import itertools  # noqa: E402
import math  # noqa: E402
from fractions import Fraction  # noqa: E402
rec("L13a", sum(1 for c in itertools.product((0, 1), repeat=3) if sum(c) == 3) == 1
    and sum(1 for c in itertools.product((0, 1), repeat=3) if sum(c) <= 2) == 7, "quy tắc hai trên ba: 8 tổ hợp, 1 bị cấm, 7 được phép (liệt kê)")
rec("L13b", round(float(Fraction(130 - 5, 130)) * 100, 1) == 96.2, "Chromium 3/2019: 125/130 ≈ 96,2% do hỏng bộ nhớ")
rec("L13c", round(float(1 - Fraction(85, 223)) * 100, 1) == 61.9 and round(85 / 0.35) == 243 and abs(85 / 0.35 - 20 * 12) < 5
    and round(223 / 0.76) == 293, "Android 2019→2022: giảm 61,9%; tổng 2022 ≈ 243 ≈ 20 mỗi tháng nhân 12")
# mô phỏng từng năm (bước 1/1000 năm) sự sống sót theo hàm mũ, tuổi thọ trung bình 2,5 năm → tỉ số mật độ sau 5 năm
_s, _dt = 1.0, 1e-4
for _ in range(int(5 / _dt)):
    _s -= _s * _dt / 2.5
rec("L13d", round(1 / _s, 1) == 7.4 and round(math.e ** 2, 2) == 7.39 and round(2 ** (5 / (2.5 * math.log(2))), 2) == 7.39,
    f"giảm theo cấp số nhân, tuổi thọ 2,5 năm: mã 5 năm tuổi ít lỗi hơn {1 / _s:.2f} lần (AN24: 7,4x)")
rec("L13e", round(5 / math.log(3.4), 1) == 4.1, "3,4x sau 5 năm ứng với tuổi thọ trung bình ≈ 4,1 năm")
rec("L13f", Fraction(1, 5) == Fraction(2, 10) and Fraction(1000) / Fraction(1, 5) == 5000 and 5_000_000 * 4 // 100 == 200_000
    and Fraction(1, 1000) * 10 ** 6 == 1000, "Rust 0,2 mỗi triệu dòng; C/C++ 1 mỗi nghìn dòng = 1000 mỗi triệu → 5000 lần; 4% của 5 triệu = 200 000")
_old, _tot = [100 / 2 ** k for k in range(4)], [round(100 / 2 ** k + 20 * k) for k in range(4)]
rec("L13g", _old == [100, 50, 25, 12.5] and _tot == [100, 70, 65, 72] and 1_500_000 // 1000 == 1500,
    "khoá vòi (số minh hoạ): mã cũ 100→12,5, có thêm 20 lỗi mới mỗi năm thì tổng 100, 70, 65, 72; cận trên 1500")
rec("L13h", 200_000 // 1000 == 200 and round(200 / math.e ** 2) == 27 and 20_000 // 1000 == 20, "quiz: 20 lỗ hổng mới mỗi năm; mã cũ 5 năm còn ≈ 27")

n_ok = sum(ok for _, ok in R)
print(f"\n{n_ok}/{len(R)} PASS")
sys.exit(0 if n_ok == len(R) else 1)
