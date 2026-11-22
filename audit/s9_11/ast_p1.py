"""Phân tích AST + tokenize chính xác cho bảng hướng dẫn đọc mã Python (P1)."""
from __future__ import annotations

import ast
import html
import io
import tokenize


def build_read_rows(code: str) -> list[list[str]]:
    """Sinh các dòng `[<code>cú pháp</code>, giải thích HTML tiếng Việt]` khớp 100% mã thật."""
    rows: list[list[str]] = []
    seen: set[str] = set()

    def add(tok_html: str, desc: str) -> None:
        if tok_html not in seen:
            seen.add(tok_html)
            rows.append([tok_html, desc])

    tree = ast.parse(code)
    nodes = list(ast.walk(tree))
    toks = list(tokenize.generate_tokens(io.StringIO(code).readline))

    has_comment = any(t.type == tokenize.COMMENT for t in toks)
    has_semi = any(t.type == tokenize.OP and t.string == ";" for t in toks)
    num_strs = [t.string for t in toks if t.type == tokenize.NUMBER]
    has_num_under = any("_" in s for s in num_strs)
    has_sci = any(("e" in s.lower() and not s.lower().startswith("0x")) for s in num_strs)
    has_hex_lit = any(s.lower().startswith("0x") for s in num_strs)

    imports: set[str] = set()
    from_imports: dict[str, set[str]] = {}
    calls: set[str] = set()
    methods: set[str] = set()
    has_default_fn = False
    has_default_lam = False
    has_multi_lam = False
    has_unpack_assign = False
    has_unpack_for = False
    has_discard = False
    has_starred = False
    has_class = False
    has_list = False
    has_list_repeat = False
    has_nested_lc = False
    has_lc_filter = False
    has_lc = False
    has_gen = False
    has_tuple = False
    has_set = False
    has_dict = False
    has_2d_sub = False
    has_neg_sub = False
    has_slice = False
    has_step_slice = False
    has_sub = False
    has_bytes = False
    bool_consts: set[object] = set()
    has_and = False
    has_or = False
    has_not = False
    has_in = False
    has_not_in = False
    has_ltgt = False
    has_eq = False
    has_chained_cmp = False
    has_bit_op = False
    has_bitor = False
    has_is_none = False
    has_dict_unpack = False
    has_reverse_kw = False
    has_aug_bit = False
    has_aug_arith = False
    has_pow = False
    has_floordiv = False
    has_mod = False
    has_if_truthy = False
    has_ternary = False
    f_specs: list[str] = []
    has_repr_fmt = False
    has_fstr = False
    has_print_multi = False
    has_int16 = False
    has_key_kw = False

    def _call_name(fn: ast.AST) -> str:
        if isinstance(fn, ast.Name):
            return fn.id
        if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name):
            return f"{fn.value.id}.{fn.attr}"
        return ""

    # Track RHS values of parallel tuple assignment so `a, b = 1, 2` isn't mislabeled as tuple literal
    parallel_rhs_ids: set[int] = set()
    for n in nodes:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Tuple) and isinstance(n.value, ast.Tuple):
            parallel_rhs_ids.add(id(n.value))

    for n in nodes:
        if isinstance(n, ast.Import):
            for a in n.names:
                imports.add(a.name)
        elif isinstance(n, ast.ImportFrom) and n.module:
            from_imports.setdefault(n.module, set()).update(a.name for a in n.names)
        elif isinstance(n, ast.ClassDef):
            has_class = True
        elif isinstance(n, ast.FunctionDef):
            if n.args.defaults or n.args.kw_defaults:
                has_default_fn = True
        elif isinstance(n, ast.Lambda):
            if len(n.args.args) >= 2:
                has_multi_lam = True
            if n.args.defaults:
                has_default_lam = True
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, (ast.Tuple, ast.List)):
                    has_unpack_assign = True
                for sub in ast.walk(t):
                    if isinstance(sub, ast.Name) and sub.id == "_":
                        has_discard = True
        elif isinstance(n, (ast.For, ast.comprehension)):
            if isinstance(n.target, (ast.Tuple, ast.List)):
                has_unpack_for = True
            for sub in ast.walk(n.target):
                if isinstance(sub, ast.Name) and sub.id == "_":
                    has_discard = True
        elif isinstance(n, ast.Starred):
            has_starred = True
        elif isinstance(n, ast.List):
            has_list = True
        elif isinstance(n, ast.ListComp):
            has_lc = True
            if len(n.generators) >= 2 or any(isinstance(x, ast.ListComp) for x in ast.walk(n.elt)):
                has_nested_lc = True
            if any(g.ifs for g in n.generators):
                has_lc_filter = True
        elif isinstance(n, ast.GeneratorExp):
            has_gen = True
            if any(g.ifs for g in n.generators):
                has_lc_filter = True
        elif isinstance(n, ast.Tuple):
            if isinstance(n.ctx, ast.Load) and id(n) not in parallel_rhs_ids:
                has_tuple = True
        elif isinstance(n, ast.Set):
            has_set = True
        elif isinstance(n, ast.Dict):
            has_dict = True
            if any(k is None for k in n.keys):
                has_dict_unpack = True
        elif isinstance(n, ast.Subscript):
            has_sub = True
            if isinstance(n.value, ast.Subscript):
                has_2d_sub = True
            if isinstance(n.slice, ast.Slice):
                has_slice = True
                if n.slice.step is not None:
                    has_step_slice = True
            elif isinstance(n.slice, ast.UnaryOp) and isinstance(n.slice.op, ast.USub):
                has_neg_sub = True
        elif isinstance(n, ast.Constant):
            if isinstance(n.value, (bytes, bytearray)):
                has_bytes = True
            elif n.value is True or n.value is False or n.value is None:
                bool_consts.add(n.value)
        elif isinstance(n, ast.BoolOp):
            if isinstance(n.op, ast.And):
                has_and = True
            elif isinstance(n.op, ast.Or):
                has_or = True
        elif isinstance(n, ast.UnaryOp):
            if isinstance(n.op, ast.Not):
                has_not = True
            elif isinstance(n.op, ast.Invert):
                has_bit_op = True
        elif isinstance(n, ast.BinOp):
            if isinstance(n.op, ast.Pow):
                has_pow = True
            elif isinstance(n.op, ast.FloorDiv):
                has_floordiv = True
            elif isinstance(n.op, ast.Mod):
                has_mod = True
            elif isinstance(n.op, ast.BitOr):
                has_bitor = True
            elif isinstance(n.op, (ast.BitAnd, ast.BitXor, ast.LShift, ast.RShift)):
                has_bit_op = True
            elif isinstance(n.op, ast.Mult) and (isinstance(n.left, ast.List) or isinstance(n.right, ast.List)):
                has_list_repeat = True
        elif isinstance(n, ast.AugAssign):
            if isinstance(n.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift)):
                has_aug_bit = True
            else:
                has_aug_arith = True
        elif isinstance(n, ast.Compare):
            if len(n.ops) >= 2:
                has_chained_cmp = True
            for op in n.ops:
                if isinstance(op, ast.In):
                    has_in = True
                elif isinstance(op, ast.NotIn):
                    has_not_in = True
                elif isinstance(op, (ast.Lt, ast.Gt, ast.LtE, ast.GtE)):
                    has_ltgt = True
                elif isinstance(op, (ast.Eq, ast.NotEq)):
                    has_eq = True
                elif isinstance(op, (ast.Is, ast.IsNot)):
                    has_is_none = True
        elif isinstance(n, ast.If):
            if isinstance(n.test, ast.Name):
                has_if_truthy = True
        elif isinstance(n, ast.IfExp):
            has_ternary = True
        elif isinstance(n, ast.JoinedStr):
            has_fstr = True
        elif isinstance(n, ast.FormattedValue):
            if n.conversion == ord("r"):
                has_repr_fmt = True
            if isinstance(n.format_spec, ast.JoinedStr):
                spec_txt = "".join(
                    v.value for v in n.format_spec.values if isinstance(v, ast.Constant) and isinstance(v.value, str)
                )
                if spec_txt and spec_txt not in f_specs:
                    f_specs.append(spec_txt)
        elif isinstance(n, ast.Call):
            cn = _call_name(n.func)
            if cn:
                calls.add(cn)
            if any(kw.arg is None for kw in n.keywords):
                has_dict_unpack = True
            if isinstance(n.func, ast.Attribute):
                methods.add(n.func.attr)
            if cn == "int" and len(n.args) >= 2:
                has_int16 = True
            if cn == "print" and len(n.args) >= 2:
                has_print_multi = True
            if any(kw.arg == "key" for kw in n.keywords):
                has_key_kw = True
            if any(kw.arg == "reverse" for kw in n.keywords):
                has_reverse_kw = True
            if any(kw.arg == "default" for kw in n.keywords):
                calls.add("_kw_default")

    if has_comment:
        add("<code># ...</code>", "Dòng chú thích giải nghĩa cho người đọc, máy bỏ qua khi chạy")
    if "math" in imports or "math" in from_imports:
        math_fns = [fn for fn in ("acos", "atan2", "ceil", "cos", "sin", "degrees", "hypot", "exp", "factorial", "log", "log2", "sqrt")
                    if f"math.{fn}" in calls or fn in from_imports.get("math", set())]
        if math_fns:
            fn_txt = ", ".join(math_fns)
            add(f"<code>math ({html.escape(fn_txt)})</code>",
                "Nạp hàm toán học chuẩn (lượng giác, hàm ngược góc, đổi radian ra độ, lôgarit, lũy thừa)")
        else:
            add("<code>import math</code>", "Nạp thư viện toán học chuẩn để dùng hàm sẵn có")
    if "heapq" in imports or "heapq" in from_imports:
        add("<code>heapq.heappush / heappop</code>", "Hàng đợi ưu tiên luôn lấy ra phần tử có chi phí nhỏ nhất trước")
    if "hashlib" in imports or "hashlib.sha256" in calls:
        add("<code>hashlib.sha256(...)</code>", "Hàm băm mật mã SHA-256 biến chuỗi byte thành mã băm 256 bit")
    if "datetime" in imports:
        add("<code>import datetime as dt</code>", "Nạp thư viện ngày tháng để cộng trừ ngày chính xác theo lịch")
    if "re" in imports:
        add("<code>re.compile(...) / .fullmatch(s)</code>", "Biên dịch biểu thức chính quy rồi kiểm tra toàn chuỗi có khớp hay không")
    if "deque" in from_imports.get("collections", set()) or "deque" in calls:
        add("<code>collections.deque(..., maxlen=k)</code>", "Hàng đợi hai đầu giữ tối đa <code>k</code> phần tử (thêm/bớt nhanh ở hai đầu)")

    if has_class:
        add("<code>class ... / def __init__(self, ...):</code>",
            "Định nghĩa kiểu đối tượng mới; hàm <code>__init__</code> khởi tạo trạng thái ban đầu (<code>self</code> chỉ chính đối tượng đó)")
    if any(isinstance(n, ast.FunctionDef) for n in nodes):
        sig = "def ham(x, mac_dinh=1):" if has_default_fn else "def ham(...): ... return"
        desc = ("Định nghĩa hàm dùng lại (<code>mac_dinh=1</code> là giá trị mặc định nếu không truyền), <code>return</code> trả kết quả"
                if has_default_fn else "Định nghĩa hàm xử lý riêng và dùng <code>return</code> trả kết quả về")
        add(f"<code>{sig}</code>", desc)
    if any(isinstance(n, ast.Lambda) for n in nodes):
        if has_default_lam:
            add("<code>lambda x, k=1.0: ...</code>", "Hàm viết gọn trên một dòng (có tham số mặc định khi gọi thiếu)")
        elif has_multi_lam:
            add("<code>lambda x, y: ...</code>", "Hàm viết gọn nhận nhiều đối số trực tiếp trên một dòng")
        else:
            add("<code>lambda x: ...</code>", "Hàm viết gọn một dòng (nhận đầu vào <code>x</code>, trả ngay kết quả sau dấu <code>:</code>)")

    if has_unpack_assign or has_unpack_for:
        ex = "for a, b in ds:" if has_unpack_for else "a, b = ..."
        add(f"<code>{html.escape(ex)}</code>", "Giải nén nhiều giá trị cùng lúc vào các tên biến tương ứng theo thứ tự")
    if has_discard:
        add("<code>_</code>", "Biến bỏ qua (dùng khi đếm số vòng lặp hoặc giải nén phần tử không cần tới)")
    if has_starred:
        add("<code>f(*bo)</code>", "Toán tử <code>*</code> bung các phần tử của bộ/danh sách thành từng đối số rời")
    if has_hex_lit or has_int16:
        tok = "0xA5 / int(s, 16)" if (has_hex_lit and has_int16) else ("0xA5" if has_hex_lit else "int(s, 16)")
        add(f"<code>{tok}</code>", "Số nguyên viết ở hệ cơ số 16 (hexa) hoặc chuyển chuỗi hệ 16 sang số nguyên")
    if has_bytes or "encode" in methods or "decode" in methods or "bytes" in calls:
        add("<code>b'...' / bytes() / .encode() / .decode()</code>", "Chuỗi byte thô, kiểu dữ liệu byte và phép đổi qua lại với chữ")
    if has_num_under or has_sci:
        parts = []
        if has_num_under:
            parts.append("1_000_000")
        if has_sci:
            parts.append("1e-9 / 1e6")
        add(f"<code>{' ; '.join(parts)}</code>", "Dấu <code>_</code> giúp dễ đọc số lớn (không đổi giá trị); <code>1e-9</code>/<code>1e6</code> là lũy thừa của 10")

    if has_nested_lc or has_lc or has_gen:
        if has_nested_lc:
            add("<code>[[... for ...] for ...]</code>", "Tạo danh sách lồng nhau (bảng 2 chiều) bằng hai vòng <code>for</code> viết gọn")
        elif has_lc_filter:
            add("<code>[bt for x in ds if đk]</code>", "Lọc phần tử thoả điều kiện <code>đk</code> rồi tính giá trị mới")
        elif has_lc:
            add("<code>[bt for x in ds]</code>", "Duyệt qua từng phần tử <code>x</code> trong <code>ds</code> để tạo danh sách mới")
        else:
            add("<code>(bt for x in ds)</code>", "Biểu thức sinh tuần tự từng phần tử <code>x</code> (thường truyền vào <code>sum(...)</code>)")
    if has_list or has_list_repeat:
        tok = "[a, b] / [x] * N" if has_list_repeat else "[a, b, ...]"
        desc = "Danh sách theo thứ tự; <code>[x] * N</code> lặp thành danh sách dài <code>N</code> phần tử" if has_list_repeat else "Danh sách nhiều phần tử theo thứ tự (lấy phần tử thứ <code>i</code> bằng <code>ds[i]</code>, đếm từ <code>0</code>)"
        add(f"<code>{tok}</code>", desc)
    if has_tuple or "tuple" in calls:
        add("<code>(a, b) / tuple(...)</code>", "Bộ giá trị cố định đóng gói theo thứ tự (không thay đổi sau khi tạo)")
    if has_set or "set" in calls or "add" in methods or "frozenset" in calls:
        tok = "frozenset(...) / {a, b}" if "frozenset" in calls else "{a, b} / set() / .add()"
        add(f"<code>{tok}</code>", "Tập hợp giữ các phần tử duy nhất (hỗ trợ kiểm tra thuộc <code>in</code> rất nhanh)")
    if has_dict or "dict" in calls or "get" in methods:
        tok = "{**a, **b} / {k: v}" if has_dict_unpack else "{k: v} / .get(k, mac_dinh)"
        desc = "Giải nén các cặp khoá–giá trị vào từ điển mới (khoá sau ghi đè khoá trước)" if has_dict_unpack else "Từ điển ánh xạ cặp khoá–giá trị (<code>.get</code> trả giá trị mặc định nếu thiếu khoá)"
        add(f"<code>{tok}</code>", desc)
    if has_2d_sub or has_step_slice or has_slice or has_neg_sub:
        toks = []
        if has_2d_sub:
            toks.append("M[i][j]")
        if has_neg_sub:
            toks.append("ds[-1]")
        if has_step_slice:
            toks.append("ds[1::2]")
        elif has_slice:
            toks.append("ds[a:b]")
        add(f"<code>{' / '.join(toks)}</code>", "Truy cập ô hàng <code>i</code> cột <code>j</code>, phần tử cuối <code>[-1]</code>, hoặc cắt lát danh sách/chuỗi")
    elif has_sub:
        add("<code>ds[i]</code>", "Lấy phần tử ở vị trí <code>i</code> (đếm từ <code>0</code>)")

    if bool_consts or has_and or has_or or has_not or has_in or has_not_in or has_if_truthy or has_ternary:
        btoks = []
        if bool_consts:
            btoks.append("/".join(str(x) for x in sorted(bool_consts, key=str)))
        if has_and or has_or or has_not:
            btoks.append(" ".join(x for x, f in (("and", has_and), ("or", has_or), ("not", has_not)) if f))
        if has_in or has_not_in:
            btoks.append("not in" if has_not_in else "in")
        if has_if_truthy:
            btoks.append("if ds:")
        if has_ternary:
            btoks.append("A if đk else B")
        add(f"<code>{html.escape(' ; '.join(btoks))}</code>",
            "Giá trị logic (<code>True/False/None</code>), phép logic (<code>and/or/not</code>), kiểm tra thuộc tập/rỗng hoặc rẽ nhánh gọn")
    if has_chained_cmp or has_ltgt or has_eq or has_is_none:
        cmps = []
        if has_chained_cmp:
            cmps.append("0 <= x < n")
        if has_ltgt:
            cmps.append("< / <= / > / >=")
        if has_eq:
            cmps.append("== / !=")
        if has_is_none:
            cmps.append("is None / is not None")
        add(f"<code>{html.escape(' ; '.join(cmps))}</code>",
            "So sánh hai vế, kiểm tra rỗng bằng <code>is None</code> hoặc kẹp khoảng trả về Đúng/Sai")
    if has_bitor and not has_bit_op and not has_aug_bit and not has_hex_lit and (has_set or "set" in calls or "frozenset" in calls):
        add("<code>A | B</code>", "Phép hợp hai tập hợp (lấy mọi phần tử thuộc ít nhất một trong hai tập)")
    elif has_bit_op or has_bitor or has_aug_bit:
        add("<code>&amp; / | / ^ / ~ / &lt;&lt; / &gt;&gt; / |=</code>", "Phép toán thao tác từng bit nhị phân và cập nhật thanh ghi/mặt nạ bit")
    if has_pow or has_floordiv or has_mod:
        ops = " ".join(x for x, f in (("**", has_pow), ("//", has_floordiv), ("%", has_mod)) if f)
        add(f"<code>{ops}</code>", "<code>**</code> là lũy thừa; <code>//</code> là chia lấy nguyên; <code>%</code> là chia lấy phần dư")
    if has_aug_arith:
        add("<code>+= / -= / *=</code>", "Cộng dồn, trừ bớt hoặc nhân trực tiếp vào biến hiện có")

    extra_calls = []
    for k, label in (
        ("zip", "zip(a, b)"),
        ("enumerate", "enumerate(ds)"),
        ("range", "range(...)"),
        ("sorted", "sorted(...)"),
        ("min", "min(...)"),
        ("max", "max(...)"),
        ("all", "all(...)"),
        ("any", "any(...)"),
        ("round", "round(x, n)"),
        ("bin", "bin(n)"),
        ("format", "format(m, ...)"),
        ("tuple", "tuple(...)"),
        ("bool", "bool(x)"),
        ("int", "int(x)"),
        ("hex", "hex(n)"),
        ("len", "len(ds)"),
        ("sum", "sum(...)"),
        ("abs", "abs(x)"),
    ):
        if k in calls and label not in seen:
            extra_calls.append(label)
    if has_key_kw:
        extra_calls.append("key=...")
    if has_reverse_kw:
        extra_calls.append("reverse=True")
    if "_kw_default" in calls:
        extra_calls.append("default=...")
    for m in ("popleft", "pop", "append", "extend", "insert", "remove", "items", "keys", "values", "join", "split", "strip", "lower", "upper", "replace", "count", "union", "sample", "random", "startswith", "endswith", "fullmatch"):
        if m in methods:
            extra_calls.append(f".{m}()")
    if "isinstance" in calls:
        add("<code>isinstance(x, kieu)</code>",
            "Kiểm tra giá trị <code>x</code> có thuộc kiểu dữ liệu cho trước không (trả về Đúng/Sai)")
    if "isdigit" in methods:
        add("<code>.isdigit()</code>",
            "Kiểm tra chuỗi ký tự có chỉ gồm toàn chữ số 0–9 hay không (trả về Đúng/Sai)")
    if extra_calls:
        add(f"<code>{html.escape(', '.join(extra_calls[:7]))}</code>",
            "Hàm/phương thức dựng sẵn thường dùng (sắp xếp, cực trị, ghép đôi, đánh chỉ số, làm tròn, lấy/thêm phần tử)")

    add("<code>= / + / - / * / /</code>",
        "Phép gán <code>=</code> đặt giá trị vào biến; <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code> là cộng, trừ, nhân, chia")

    if has_semi:
        add("<code>;</code>", "Dấu chấm phẩy ngăn cách hai lệnh ngắn viết trên cùng một dòng")
    if has_fstr:
        spec_show = ", ".join(f"{{:{s}}}" if not s.startswith(":") else f"{{{s}}}" for s in f_specs[:3])
        if has_repr_fmt:
            spec_show = (spec_show + ", " if spec_show else "") + "{x!r}"
        tok = f'f"...{spec_show}..."' if spec_show else 'f"...{ten_bien}..."'
        add(f"<code>{html.escape(tok)}</code>",
            "Chuỗi định dạng chèn giá trị biến vào văn bản (<code>:.2f</code> làm tròn 2 chữ số; <code>!r</code> giữ nguyên dấu nháy)")
    if "print" in calls:
        tok = "print(a, b)" if has_print_multi else "print(...)"
        desc = "In nhiều phần liên tiếp cách nhau bằng dấu cách để ghép trọn 1 dòng đáp án" if has_print_multi else "In từng dòng kết quả ra màn hình để kiểm khớp đáp án"
        add(f"<code>{tok}</code>", desc)

    return rows
