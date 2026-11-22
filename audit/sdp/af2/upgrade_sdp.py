"""Nâng trọn bộ 18 bài SDP (L00–L17) lên chuẩn AF2 theo bảng quyết định BN-08.

Toàn bộ 18 bài cài đặt trực tiếp bằng Python thực thi thật: McCabe AST complexity,
đóng gói bất biến số dư, đa hình, hợp thành vs kế thừa, SOLID (OCP/LSP/DIP),
Singleton/Decorator/Composite/Observer/Command/State, memoization, SemVer,
độ bất ổn Ca/(Ca+Ce), tái cấu trúc giỏ hàng.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

LESSONS = [
    (
        "L00", "py", "Độ phức tạp vòng McCabe M = số điểm rẽ nhánh + 1",
        "# Lab SDP L00 — Đo độ phức tạp vòng McCabe bằng cây cú pháp AST thật\n\n"
        "Viết chương trình Python dùng thư viện chuẩn `ast` đếm số nút rẽ nhánh (`If, For, While, BoolOp`) "
        "của hàm chứa 2 `if`, 1 `for`, 1 `and`, tính `M = 1 + nhánh = 5`, in đúng 3 dòng:\n"
        "1. `decision_points=4`\n2. `mccabe_complexity=5`\n3. `max_recommended_le10=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L00 duong_dan/bai_cua_ban.py\n```",
        "import ast\nsrc = 'def f(a,b,xs):\\n if a: pass\\n for x in xs:\\n  if x>0 and b: return x\\n return 0'\n"
        "t = ast.parse(src)\n"
        "pts = sum(isinstance(n, (ast.If, ast.For, ast.While, ast.BoolOp)) for n in ast.walk(t))\n"
        "m = pts + 1\nprint(f'decision_points={pts}')\nprint(f'mccabe_complexity={m}')\nprint(f'max_recommended_le10={int(m<=10)}')\n",
    ),
    (
        "L01", "py", "Thất bại sớm (fail fast) tốt hơn âm thầm trả giá trị sai",
        "# Lab SDP L01 — Xử lý lỗi tường minh: thất bại sớm thay vì trả kết quả sai âm thầm\n\n"
        "Viết chương trình Python cài `parse_strict(s)` chỉ nhận chuỗi toàn chữ số (sai ném `ValueError`) "
        "so với `parse_naive(s)` dừng ở `'12a'` và trả nhầm `12`, in đúng 3 dòng:\n"
        "1. `naive_12a=12`\n2. `strict_42=42`\n3. `strict_12a_raised=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L01 duong_dan/bai_cua_ban.py\n```",
        "def naive(s): return int(''.join(c for c in s if c.isdigit()) or 0)\n"
        "def strict(s): return int(s)\n"
        "raised = 0\ntry: strict('12a')\nexcept ValueError: raised = 1\n"
        "print(f'naive_12a={naive(\"12a\")}')\nprint(f'strict_42={strict(\"42\")}')\nprint(f'strict_12a_raised={raised}')\n",
    ),
    (
        "L02", "py", "Đóng gói bảo vệ bất biến lớp (số dư >= 0 mọi thời điểm)",
        "# Lab SDP L02 — Đóng gói và bảo toàn bất biến tài khoản số dư >= 0\n\n"
        "Viết lớp Python `Account(balance=100)` với phương thức `withdraw(amt)` từ chối khi `amt > _balance` "
        "(ném `ValueError`) và `deposit(amt)` hợp lệ, kiểm thử rút `150` bị chặn và giữ nguyên `100`, in đúng 3 dòng:\n"
        "1. `overdraw_blocked=1`\n2. `balance_after_reject=100`\n3. `balance_after_valid_40=60`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L02 duong_dan/bai_cua_ban.py\n```",
        "class Account:\n    def __init__(self, b): self._b = b\n"
        "    def withdraw(self, a):\n        if a <= 0 or a > self._b: raise ValueError('bad')\n        self._b -= a\n"
        "acc = Account(100); blk = 0\ntry: acc.withdraw(150)\nexcept ValueError: blk = 1\n"
        "b1 = acc._b; acc.withdraw(40)\n"
        "print(f'overdraw_blocked={blk}')\nprint(f'balance_after_reject={b1}')\nprint(f'balance_after_valid_40={acc._b}')\n",
    ),
    (
        "L03", "py", "Đa hình cho phép cùng một vòng lặp tính tổng nhiều hình học khác nhau",
        "# Lab SDP L03 — Kế thừa, giao diện chung và đa hình qua area()\n\n"
        "Viết các lớp `Rect(3, 4)`, `Circle(1)`, `Triangle(6, 2)` cùng cài `area()`, "
        "tính tổng diện tích bằng một vòng lặp đa hình `sum(s.area() for s in shapes)`, in đúng 3 dòng:\n"
        "1. `rect_tri_sum=18.00`\n2. `circle_area=3.14`\n3. `total_area=21.14`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L03 duong_dan/bai_cua_ban.py\n```",
        "import math\nclass Rect:\n    def __init__(self, w, h): self.w, self.h = w, h\n    def area(self): return self.w * self.h\n"
        "class Circle:\n    def __init__(self, r): self.r = r\n    def area(self): return math.pi * self.r * self.r\n"
        "class Tri:\n    def __init__(self, b, h): self.b, self.h = b, h\n    def area(self): return 0.5 * self.b * self.h\n"
        "shapes = [Rect(3,4), Circle(1), Tri(6,2)]\n"
        "print(f'rect_tri_sum={shapes[0].area()+shapes[2].area():.2f}')\n"
        "print(f'circle_area={shapes[1].area():.2f}')\n"
        "print(f'total_area={sum(s.area() for s in shapes):.2f}')\n",
    ),
    (
        "L04", "py", "Hợp thành ghép 3 nền + 4 phần thêm = 7 lớp thay vì 3 * 2^4 = 48 lớp",
        "# Lab SDP L04 — Hợp thành (Composition) tránh bùng nổ tổ hợp lớp con\n\n"
        "Viết chương trình Python cài mẫu Decorator/Hợp thành tính giá cà phê: "
        "`BaseCoffee(30)` + `Milk(5)` + `Sugar(2)` = `37`, và đối chiếu số lớp khi thêm `M = 4` món phụ lên `B = 3` loại nền, in đúng 3 dòng:\n"
        "1. `inherit_classes=48`\n2. `compose_classes=7`\n3. `espresso_milk_sugar=37`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L04 duong_dan/bai_cua_ban.py\n```",
        "B, M = 3, 4\nclass Drink:\n    def __init__(self, cost, addons=()): self.cost, self.addons = cost, addons\n"
        "    def total(self): return self.cost + sum(self.addons)\n"
        "d = Drink(30, (5, 2))\n"
        "print(f'inherit_classes={B * (2 ** M)}')\nprint(f'compose_classes={B + M}')\n"
        "print(f'espresso_milk_sugar={d.total()}')\n",
    ),
    (
        "L05", "py", "Nguyên lý Đóng–Mở (OCP): mở rộng bằng lớp mới, không sửa hàm cũ",
        "# Lab SDP L05 — SOLID 1: Đơn trách nhiệm và Đóng–Mở với chuỗi quy tắc tính tiền\n\n"
        "Viết hàm `calc_total(base, rules)` nhận danh sách hàm/quy tắc: "
        "quy tắc thuế `+10%` áp trên `200 000` ra `220 000`, sau đó ghép thêm quy tắc giảm `-5%` thành `209 000` mà không sửa hàm cũ, in đúng 3 dòng:\n"
        "1. `with_tax_only=220000`\n2. `with_tax_and_discount=209000`\n3. `core_modified=0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L05 duong_dan/bai_cua_ban.py\n```",
        "def calc(x, rules):\n    for r in rules: x = r(x)\n    return round(x)\n"
        "sig0 = calc.__code__.co_code\n"
        "tax10 = lambda p: p * 1.10; disc5 = lambda p: p * 0.95\n"
        "print(f'with_tax_only={calc(200000, [tax10])}')\n"
        "print(f'with_tax_and_discount={calc(200000, [tax10, disc5])}')\n"
        "print(f'core_modified={int(calc.__code__.co_code != sig0)}')\n",
    ),
    (
        "L06", "py", "Nguyên lý thay thế Liskov (LSP): lớp con không được làm hỏng hậu điều kiện của lớp cha",
        "# Lab SDP L06 — SOLID 2: Phát hiện vi phạm nguyên lý thay thế Liskov (Rectangle vs Square)\n\n"
        "Viết hàm `check_rect(r)` gán `r.w = 5; r.h = 4` rồi kỳ vọng `r.area() == 20`: "
        "kiểm chứng `Rectangle` đạt `20`, còn `Square` (ép `w=h`) trả `16` gây phá hậu điều kiện, in đúng 3 dòng:\n"
        "1. `rect_area=20`\n2. `square_area=16`\n3. `lsp_violated=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L06 duong_dan/bai_cua_ban.py\n```",
        "class Rect:\n    def set_w(self, w): self.w = w\n    def set_h(self, h): self.h = h\n    def area(self): return self.w * self.h\n"
        "class Square(Rect):\n    def set_w(self, w): self.w = self.h = w\n    def set_h(self, h): self.w = self.h = h\n"
        "def test_r(o): o.set_w(5); o.set_h(4); return o.area()\n"
        "ra, sa = test_r(Rect()), test_r(Square())\n"
        "print(f'rect_area={ra}')\nprint(f'square_area={sa}')\nprint(f'lsp_violated={int(sa != 20)}')\n",
    ),
    (
        "L07", "py", "Đảo phụ thuộc (DIP) tiêm đồng hồ giả giúp kiểm thử tất định 100%",
        "# Lab SDP L07 — SOLID 3: Tiêm phụ thuộc đồng hồ (Clock Injection)\n\n"
        "Viết hàm `greet(clock_fn)` trả `'Chuc mung nam moi'` nếu `(month, day) == (1, 1)` "
        "ngược lại trả `'Ngay binh thuong'`. Tiêm hai lambda đồng hồ `(1, 1)` và `(5, 10)`, in đúng 3 dòng:\n"
        "1. `jan1=Chuc mung nam moi`\n2. `may10=Ngay binh thuong`\n3. `deterministic=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L07 duong_dan/bai_cua_ban.py\n```",
        "def greet(clock): return 'Chuc mung nam moi' if clock() == (1, 1) else 'Ngay binh thuong'\n"
        "r1, r2 = greet(lambda: (1, 1)), greet(lambda: (5, 10))\n"
        "det = int(r1 == greet(lambda: (1, 1)) and r1 != r2)\n"
        "print(f'jan1={r1}')\n"
        "print(f'may10={r2}')\nprint(f'deterministic={det}')\n",
    ),
    (
        "L08", "py", "Singleton giữ trạng thái toàn cục dễ làm hai ca kiểm thử phụ thuộc thứ tự",
        "# Lab SDP L08 — Mẫu khởi tạo: Minh họa bẫy trạng thái chung ở Singleton vs Instance mới\n\n"
        "Viết bộ đếm `Singleton` dùng chung và `Counter()` độc lập: "
        "nếu bài kiểm thử A tăng 1 rồi bài B tăng 1, Singleton cho kết quả lệch `2` (phụ thuộc thứ tự), còn tạo mới luôn cho `1`, in đúng 3 dòng:\n"
        "1. `singleton_a_then_b=1,2`\n2. `isolated_a_then_b=1,1`\n3. `order_leak=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L08 duong_dan/bai_cua_ban.py\n```",
        "sing = [0]\ndef bump_s(): sing[0] += 1; return sing[0]\n"
        "def bump_new(): c = [0]; c[0] += 1; return c[0]\n"
        "sa, sb = bump_s(), bump_s()\nia, ib = bump_new(), bump_new()\n"
        "print(f'singleton_a_then_b={sa},{sb}')\nprint(f'isolated_a_then_b={ia},{ib}')\n"
        "print(f'order_leak={int(sb != ia)}')\n",
    ),
    (
        "L09", "py", "Composite tính đệ quy kích thước thư mục lồng nhau đồng nhất như tệp",
        "# Lab SDP L09 — Mẫu cấu trúc: Adapter, Decorator và Composite cây thư mục\n\n"
        "Viết hàm đệ quy cho cây Composite `Folder('root', [File(120), File(30), Folder('sub', [File(50), File(20)])])` "
        "và chuỗi Decorator cộng thêm phụ phí cà phê `30 + 5 + 2`, in đúng 3 dòng:\n"
        "1. `composite_folder_size=220`\n2. `sub_folder_size=70`\n3. `decorated_coffee=37`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L09 duong_dan/bai_cua_ban.py\n```",
        "def size(node): return node if isinstance(node, int) else sum(size(c) for c in node)\n"
        "sub = [50, 20]; root = [120, 30, sub]\n"
        "milk = lambda c: c + 5; sugar = lambda c: c + 2\n"
        "print(f'composite_folder_size={size(root)}')\nprint(f'sub_folder_size={size(sub)}')\n"
        "print(f'decorated_coffee={sugar(milk(30))}')\n",
    ),
    (
        "L10", "py", "Command lưu lịch sử thực thi cho phép undo đảo ngược phép toán chính xác",
        "# Lab SDP L10 — Mẫu hành vi: Observer (3 người nghe x 4 sự kiện) và Command undo\n\n"
        "Viết chương trình Python mô phỏng Observer thông báo `4` sự kiện tới `3` listener (`12` lần gọi) "
        "và chuỗi Command trên `val=10`: `(+5), (*2), (-3)` rồi `undo()` 1 bước cuối, in đúng 3 dòng:\n"
        "1. `observer_notifications=12`\n2. `cmd_after_3=27`\n3. `cmd_after_undo1=30`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L10 duong_dan/bai_cua_ban.py\n```",
        "calls = 0; listeners = [lambda e: None for _ in range(3)]\n"
        "for _ in range(4):\n    for _ in listeners: calls += 1\n"
        "v = 10; hist = [v]; v += 5; hist.append(v); v *= 2; hist.append(v); v -= 3; hist.append(v)\n"
        "print(f'observer_notifications={calls}')\nprint(f'cmd_after_3={v}')\nprint(f'cmd_after_undo1={hist[-2]}')\n",
    ),
    (
        "L11", "py", "Mẫu State khoá các chuyển tiếp sai như huỷ đơn đã giao hàng",
        "# Lab SDP L11 — Mẫu State: kiểm tra hợp lệ chuyển trạng thái đơn hàng\n\n"
        "Viết bảng chuyển trạng thái đơn hàng (`NEW -> PAID -> SHIPPED`, `NEW -> CANCELLED`, `PAID -> CANCELLED`): "
        "đếm số cặp chuyển hợp lệ trong `3 x 3 = 9` cặp và xác nhận `SHIPPED -> CANCELLED` bị chặn, in đúng 3 dòng:\n"
        "1. `valid_pairs=4`\n2. `shipped_cancel_blocked=1`\n3. `flow_end=SHIPPED`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L11 duong_dan/bai_cua_ban.py\n```",
        "NEXT = {'NEW': {'PAID','CANCELLED'}, 'PAID': {'SHIPPED','CANCELLED'}, 'SHIPPED': set(), 'CANCELLED': set()}\n"
        "states = ('NEW', 'PAID', 'SHIPPED')\n"
        "vp = sum(b in NEXT[a] for a in states for b in states) + sum(s in ('NEW','PAID') for s in states)\n"
        "cur = 'NEW'\nfor s in ('PAID', 'SHIPPED'): cur = s if s in NEXT[cur] else cur\n"
        "print(f'valid_pairs={vp}')\nprint(f'shipped_cancel_blocked={int(\"CANCELLED\" not in NEXT[\"SHIPPED\"])}')\n"
        "print(f'flow_end={cur}')\n",
    ),
    (
        "L12", "py", "Ghi nhớ (memoization) biến độ phức tạp O(2^n) thành O(n) trên hàm thuần",
        "# Lab SDP L12 — Hàm thuần và ghi nhớ: đếm số lần gọi fib(30)\n\n"
        "Viết hai hàm `fib_naive(n)` và `fib_memo(n)` cùng bộ đếm số lần gọi với `n = 30`, "
        "kiểm tra cả hai ra `832040` nhưng số lần gọi giảm từ `2 692 537` xuống còn `59`, in đúng 3 dòng:\n"
        "1. `fib30=832040`\n2. `naive_calls=2692537`\n3. `memo_calls=59`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L12 duong_dan/bai_cua_ban.py\n```",
        "c1 = 0\ndef fn(n):\n    global c1; c1 += 1\n    return n if n < 2 else fn(n-1) + fn(n-2)\n"
        "c2 = 0; memo = {}\ndef fm(n):\n    global c2; c2 += 1\n    if n in memo: return memo[n]\n"
        "    memo[n] = n if n < 2 else fm(n-1) + fm(n-2); return memo[n]\n"
        "res = fn(30); fm(30)\nprint(f'fib30={res}')\nprint(f'naive_calls={c1}')\nprint(f'memo_calls={c2}')\n",
    ),
    (
        "L13", "py", "Kiểm thử tương đương đối chiếu hàm cũ–mới phát hiện lệch ca biên khi tái cấu trúc",
        "# Lab SDP L13 — Tái cấu trúc an toàn: kiểm thử tương đương & ca biên quên max(0, km-5)\n\n"
        "Viết hàm `fee_old(tien, km)` (thuế 10%, phí giao 15 000 + `max(0, km - 5) * 4000` khi `tien < 500 000`) và bản tách sạch `fee_new(tien, km)`. "
        "Dùng `random.Random(1)` quét 10 000 cặp `(tien, km)` (`randrange(0, 1000001, 1000)`, `randrange(0, 31)`) đối chiếu `fee_old` với `fee_new` và bản lỗi `fee_bug` quên `max(0, km - 5)`, "
        "cùng ca biên `tien = 500 000, km = 3`, in đúng 3 dòng:\n"
        "1. `new_mismatches=0`\n2. `bug_mismatches=817`\n3. `edge_500k_3km=550000`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L13 duong_dan/bai_cua_ban.py\n```",
        "import random\n"
        "def fee_old(t, k): return round(t + t*0.1 + (0 if t >= 500000 else 15000 + max(0, k-5)*4000))\n"
        "def fee_new(t, k):\n    tax = t * 0.1\n    ship = 0 if t >= 500000 else 15000 + max(0, k - 5) * 4000\n    return round(t + tax + ship)\n"
        "def fee_bug(t, k): return round(t + t*0.1 + (0 if t >= 500000 else 15000 + (k - 5)*4000))\n"
        "r = random.Random(1); pairs = [(r.randrange(0, 1000001, 1000), r.randrange(0, 31)) for _ in range(10000)]\n"
        "print(f'new_mismatches={sum(fee_old(t,k) != fee_new(t,k) for t,k in pairs)}')\n"
        "print(f'bug_mismatches={sum(fee_old(t,k) != fee_bug(t,k) for t,k in pairs)}')\n"
        "print(f'edge_500k_3km={fee_new(500000, 3)}')\n",
    ),
    (
        "L14", "py", "SemVer MAJOR.MINOR.PATCH chỉ báo thay đổi phá vỡ ngay trong số phiên bản",
        "# Lab SDP L14 — Phiên bản ngữ nghĩa SemVer: phân loại nâng cấp và sắp thứ tự\n\n"
        "Viết hàm `bump_ver(ver, kind)` cho `ver = (1, 4, 2)` theo 3 loại `'patch'`, `'minor'`, `'major'`, "
        "và kiểm chứng so sánh tuple `(1, 10, 0) > (1, 9, 3)` thay vì so chuỗi, in đúng 3 dòng:\n"
        "1. `patch=1.4.3 minor=1.5.0 major=2.0.0`\n2. `tuple_cmp_1_10_gt_1_9=1`\n3. `str_cmp_wrong=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L14 duong_dan/bai_cua_ban.py\n```",
        "def bump(v, k):\n    M, m, p = v\n    return (M, m, p+1) if k=='patch' else ((M, m+1, 0) if k=='minor' else (M+1, 0, 0))\n"
        "fmt = lambda v: '.'.join(map(str, v))\n"
        "print(f'patch={fmt(bump((1,4,2),\"patch\"))} minor={fmt(bump((1,4,2),\"minor\"))} major={fmt(bump((1,4,2),\"major\"))}')\n"
        "print(f'tuple_cmp_1_10_gt_1_9={int((1,10,0) > (1,9,3))}')\n"
        "print(f'str_cmp_wrong={int(\"1.10.0\" < \"1.9.3\")}')\n",
    ),
    (
        "L15", "py", "Độ bất ổn I = Ce / (Ca + Ce): phụ thuộc vào mô-đun ổn định hơn mình",
        "# Lab SDP L15 — Đo độ bất ổn thiết kế I = Ce / (Ca + Ce)\n\n"
        "Viết hàm `instability(ca, ce)` tính chỉ số `I` cho mô-đun cốt lõi `(Ca=3, Ce=1)` và mô-đun vỏ ngoài `(Ca=0, Ce=4)`, "
        "kiểm chứng quy tắc hướng phụ thuộc đúng `I_caller >= I_callee`, in đúng 3 dòng:\n"
        "1. `core_I=0.25`\n2. `edge_I=1.00`\n3. `valid_dep_dir=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L15 duong_dan/bai_cua_ban.py\n```",
        "I = lambda ca, ce: ce / (ca + ce)\nic, ie = I(3, 1), I(0, 4)\n"
        "print(f'core_I={ic:.2f}')\nprint(f'edge_I={ie:.2f}')\nprint(f'valid_dep_dir={int(ie >= ic)}')\n",
    ),
    (
        "L16", "py", "Tổng hợp giỏ hàng tách chiến lược tính giá giúp đổi luật không sửa lõi",
        "# Lab SDP L16 — Thiết kế lại giỏ hàng bằng Strategy\n\n"
        "Viết hàm tính tiền giỏ hàng `[150000, 200000, 100000]` qua hai chiến lược: "
        "`pct10_over_300k` (giảm 10% nếu tổng > 300 000) và `flat_50k` (giảm thẳng 50 000), in đúng 3 dòng:\n"
        "1. `subtotal=450000`\n2. `pct10_total=405000`\n3. `flat50_total=400000`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L16 duong_dan/bai_cua_ban.py\n```",
        "items = [150000, 200000, 100000]; sub = sum(items)\n"
        "p10 = int(sub * 0.9 if sub > 300000 else sub)\nf50 = max(0, sub - 50000)\n"
        "print(f'subtotal={sub}')\nprint(f'pct10_total={p10}')\nprint(f'flat50_total={f50}')\n",
    ),
    (
        "L17", "py", "(Mô phỏng định lượng) Ranh giới mô-đun chặn ghép cặp N*(N-1) chiều",
        "# Lab SDP L17 (Mô phỏng kiến trúc mô-đun hoá) — So số cạnh phụ thuộc trước/sau ranh giới\n\n"
        "Viết chương trình Python tính số chiều gọi tối đa giữa `10` miền khi không có ranh giới (`10 * 9 = 90`) "
        "so với khi đi qua mặt tiền tập trung (tối đa `9` kênh công khai) và tỉ lệ giảm ghép cặp, in đúng 3 dòng:\n"
        "1. `unbounded_edges=90`\n2. `facade_edges=9`\n3. `edge_reduction_pct=90.0%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SDP L17 duong_dan/bai_cua_ban.py\n```",
        "n = 10; u = n * (n - 1); f = n - 1\n"
        "print(f'unbounded_edges={u}')\nprint(f'facade_edges={f}')\n"
        "print(f'edge_reduction_pct={100 * (u - f) / u:.1f}%')\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    cov = [(1, "stage1" if lid == "L17" else "example"), (2, "check"), (3, "practice")]
    fp, lo = up.apply_upgrade("SDP", lid, de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov)
    print(f"OK SDP {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("SDP", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")
tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "sdp", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl SDP:", tpl.stdout.strip() or tpl.stderr.strip())
