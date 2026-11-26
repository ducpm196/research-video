"""Helper dùng chung cho nâng cấp AF2 Chặng 9–11 (305 bài): covers chuẩn xác, lab chạy thật, khối mã Python không lộ trước pause."""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import html
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))

import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402
import lv  # noqa: E402

PY_VENV_PYT = ROOT / "labs" / ".venv-pyt" / "Scripts" / "python.exe"
PY_VENV_ML = ROOT / "labs" / ".venv-ml" / "Scripts" / "python.exe"


def pick_runner(code: str) -> str:
    if re.search(r"^\s*(?:import|from)\s+(?:sklearn|scipy|torch)\b", code, re.M):
        return str(PY_VENV_ML)
    if re.search(r"^\s*(?:import|from)\s+(?:numpy|pandas|matplotlib|pytest)\b", code, re.M):
        return str(PY_VENV_PYT)
    return ak.VENV_PY


def pick_covers(spec: dict) -> list[tuple[int, str]]:
    """Ánh xạ fallback mục tiêu 1..n sang cảnh hợp lệ (ưu tiên tránh gán cứng 'practice' nếu mục tiêu là hiểu/phân tích)."""
    ex_ids = [s["id"] for s in spec["scenes"] if s.get("kind") == "example"]
    chk_ids = [s["id"] for s in spec["scenes"] if s.get("kind") == "check"]
    pool = ex_ids + chk_ids
    if not pool:
        pool = [s["id"] for s in spec["scenes"] if s.get("kind") in ("formula", "intuition")]
    nobj = len(spec.get("objectives") or [])
    cov = []
    for i in range(1, nobj):
        cov.append((i, pool[min(i - 1, len(pool) - 1)]))
    cov.append((max(1, nobj), "practice"))
    return cov


def has_screen_code(spec: dict) -> bool:
    for sc in spec["scenes"]:
        for st in sc.get("steps") or []:
            sh = st.get("show") or ""
            if '<div class="code"' in sh or "<div class='code'" in sh or "<pre" in sh:
                return True
    return False


def mask_output_format(lab_out: str) -> str:
    """Biến chuỗi đầu ra mẫu thành khuôn định dạng key=... không lộ đáp số (hỗ trợ ngoặc lồng và đơn vị ghép)."""
    units = ("m/s", "rad/s", "/s", "ms", "Hz", "dB", "km", "GB", "MB", "px", "V", "m", "x", "s", "%")
    out_lines = []
    for line in lab_out.strip().splitlines():
        res = []
        i, n = 0, len(line)
        while i < n:
            m = re.match(r"([A-Za-z0-9_]+=\s*)", line[i:])
            if not m:
                res.append(line[i])
                i += 1
                continue
            key_eq = m.group(1)
            j = i + len(key_eq)
            if j < n and line[j] in "(['\"":
                open_ch = line[j]
                close_ch = { "(": ")", "[": "]", "'": "'", '"': '"' }[open_ch]
                depth = 1 if open_ch in "([" else 0
                j += 1
                while j < n:
                    ch = line[j]
                    if open_ch in "'\"":
                        if ch == "\\" and j + 1 < n:
                            j += 2
                            continue
                        if ch == close_ch:
                            j += 1
                            break
                    else:
                        if ch == open_ch:
                            depth += 1
                        elif ch == close_ch:
                            depth -= 1
                            if depth == 0:
                                j += 1
                                break
                    j += 1
                val = line[i + len(key_eq):j]
            else:
                k = j
                while k < n and not line[k].isspace():
                    k += 1
                val = line[j:k]
                j = k
            suf = next((u for u in units if val.endswith(u) and len(val) > len(u)), "")
            res.append(key_eq + "..." + suf)
            i = j
        out_lines.append("".join(res))
    return "\n".join(out_lines)


def _strip_comments(code: str) -> str:
    return "\n".join(re.sub(r"#.*$", "", line) for line in code.splitlines())


def build_read_rows(code: str) -> list[list[str]]:
    """Sinh danh sách hàng 'viết trong mã -> đọc và hiểu là' bằng phân tích AST chính xác."""
    import ast_p1
    return ast_p1.build_read_rows(code)


def _legacy_build_read_rows(code: str) -> list[list[str]]:

    # 1. Import cụ thể
    imports = []
    for m in re.finditer(r"^\s*import\s+([A-Za-z0-9_.,\s]+?)(?:\s+as\s+\w+)?$", clean, re.M):
        for mod in m.group(1).split(","):
            mod = mod.strip().split()[0]
            if mod and mod not in imports:
                imports.append(mod)
    from_imports = re.findall(r"^\s*from\s+(\S+)\s+import\s+([^\n]+)", clean, re.M)
    mod_desc = {
        "math": "Nạp thư viện toán học chuẩn (lô-ga-rít, căn, lượng giác…)",
        "random": "Nạp thư viện sinh số ngẫu nhiên theo hạt giống",
        "hashlib": "Nạp thư viện tính mã băm (như SHA-256)",
        "sqlite3": "Nạp thư viện chạy truy vấn SQL trong bộ nhớ",
        "heapq": "Nạp hàng đợi ưu tiên lấy phần tử nhỏ nhất",
        "re": "Nạp thư viện biểu thức chính quy khớp mẫu chuỗi",
        "datetime": "Nạp thư viện xử lý ngày giờ",
    }
    for mod in imports:
        rows.append([f"<code>import {mod}</code>", mod_desc.get(mod, f"Nạp thư viện chuẩn {mod}")])
    for pkg, names in from_imports:
        clean_names = ", ".join(n.strip().split()[0] for n in names.split(","))
        desc = f"Lấy công cụ <code>{clean_names}</code> từ thư viện <code>{pkg}</code>"
        if "Fraction" in clean_names:
            desc = "Dùng phân số chính xác <code>Fraction(tu, mau)</code>"
        elif "deque" in clean_names:
            desc = "Hàng đợi hai đầu lấy/thêm đầu cuối nhanh"
        elif "Counter" in clean_names:
            desc = "Bộ đếm tần suất từng phần tử tự động"
        rows.append([f"<code>from {pkg} import {clean_names}</code>", desc])

    # 2. Hàm / lambda
    if re.search(r"^\s*def\s+\w+", clean, re.M):
        rows.append(["<code>def ham(...): ... return</code>", "Định nghĩa hàm xử lý riêng và trả kết quả về"])
    if re.search(r"\blambda\b", clean):
        rows.append(["<code>lambda x: bieu_thuc</code>", "Hàm viết gọn một dòng nhận đầu vào bên trái dấu hai chấm"])

    # 3. Vòng lặp / comprehension / điều kiện / hàm ẩn danh
    if re.search(r"^\s*#", clean, re.M) or "  #" in clean:
        rows.append(["<code># ghi chú</code>", "Phần chú thích giải thích bằng lời sau dấu <code>#</code>, Python bỏ qua khi chạy"])
    if re.search(r"\[[^\]]*\bfor\b[^\]]*\bin\b[^\]]*\]", clean):
        rows.append(["<code>[bt for x in ds if dk]</code>", "Tạo nhanh danh sách mới bằng vòng lặp (có thể lọc theo <code>if</code>)"])
    elif re.search(r"\[[^\]\n,]+(?:,[^\]\n]+)+\]", clean):
        rows.append(["<code>[a, b, ...]</code>", "Danh sách ngoặc vuông chứa nhiều phần tử có thứ tự (chỉ số bắt đầu từ 0)"])
    if re.search(r"\bfor\s+[^:\n]+\s+in\b", clean) and re.search(r"\brange\(", clean):
        rows.append(["<code>for i in range(n):</code>", "Lặp <code>n</code> lần qua dãy số nguyên từ <code>0</code> tới <code>n-1</code>"])
    elif re.search(r"\bfor\s+[^:\n]+\s+in\b", clean):
        rows.append(["<code>for x in ds:</code>", "Lặp lần lượt qua từng phần tử trong dãy hoặc bảng"])
    if re.search(r"\bsum\([^)\n]*\bfor\b[^)\n]*\bin\b", clean) or re.search(r"\ball\([^)\n]*\bfor\b[^)\n]*\bin\b", clean):
        rows.append(["<code>sum(bt for x in ds) / all(...)</code>", "Cộng dồn hoặc kiểm đúng mọi phần tử theo biểu thức lặp một dòng"])
    if re.search(r"\bwhile\b", clean):
        br = " (dừng ngay khi gặp <code>break</code>)" if re.search(r"\bbreak\b", clean) else ""
        rows.append(["<code>while True / dk:</code>", f"Lặp liên tục cho tới khi điều kiện sai{br}"])
    elif re.search(r"\bbreak\b", clean):
        rows.append(["<code>break</code>", "Thoát sớm khỏi vòng lặp ngay khi đã tìm thấy đáp án"])
    if re.search(r"[^\s]+\s+\bif\b[^:\n]+\belse\b\s+[^\s]+", clean):
        rows.append(["<code>A if dk else B</code>", "Chọn giá trị A khi điều kiện đúng, ngược lại chọn giá trị B"])
    if re.search(r"^\s*(?:if|elif|else)\b.*:", clean, re.M):
        rows.append(["<code>if / elif / else:</code>", "Rẽ nhánh kiểm tra điều kiện đúng hay sai trước khi thực thi"])
    if ";" in clean:
        rows.append(["<code>lenh_1; lenh_2</code>", "Dấu chấm phẩy ngăn nhiều câu lệnh ngắn gộp trên cùng một dòng"])

    # 4. Cấu trúc dữ liệu & phương thức phổ biến
    if "deque" in clean or ".popleft(" in clean:
        rows.append(["<code>deque / .popleft()</code>", "Hàng đợi hai đầu: lấy phần tử ở đầu ra nhanh cho tìm kiếm theo chiều rộng"])
    if re.search(r"sqlite3|\.execute\(", clean):
        rows.append(["<code>sqlite3 / .execute(...)</code>", "Chạy câu truy vấn SQL trong bộ nhớ và lấy dòng kết quả (<code>fetchone/fetchall</code>)"])
    if re.search(r"hashlib|\.hexdigest\(", clean):
        rows.append(["<code>.encode().hexdigest()</code>", "Chuyển chữ thành byte UTF-8 rồi băm SHA-256 ra chuỗi thập lục phân"])
    elif ".encode(" in clean:
        rows.append(["<code>s.encode()</code>", "Chuyển chuỗi chữ sang dãy byte trước khi đưa vào hàm băm"])
    if ".startswith(" in clean:
        rows.append(["<code>s.startswith('00')</code>", "Kiểm tra chuỗi có mở đầu đúng bằng tiền tố yêu cầu hay không"])
    if re.search(r"random\.Random\(", clean):
        rows.append(["<code>random.Random(42)</code>", "Tạo bộ sinh số ngẫu nhiên cố định theo hạt giống để chạy lại y hệt"])
    if re.search(r"\{[^}\n]+:[^}\n]+\}", clean) or ".items()" in clean or ".values()" in clean or "dict(" in clean:
        rows.append(["<code>{k: v} / dict(...)</code>", "Từ điển ánh xạ cặp khoá–giá trị (tra cứu nhanh bằng <code>d[k]</code>)"])
    elif re.search(r"\{[^}:,\n]+(?:,[^}:,\n]+)*\}|set\(", clean) or ".add(" in clean:
        rows.append(["<code>{a, b} / set() / .add()</code>", "Tập hợp các phần tử không trùng lặp (hỗ trợ kiểm tập con <code>&lt;=</code>)"])
    if ".append(" in clean:
        rows.append(["<code>ds.append(x)</code>", "Thêm một phần tử <code>x</code> vào cuối danh sách <code>ds</code>"])
    if ".join(" in clean:
        rows.append(['<code>",".join(ds)</code>', "Ghép các chuỗi trong danh sách thành một chuỗi nối bằng dấu phẩy"])
    if re.search(r"sorted\([^)\n]*key=", clean):
        rows.append(["<code>sorted(ds, key=...)</code>", "Sắp xếp theo tiêu chí tuỳ chọn (<code>reverse=True</code> là giảm dần)"])

    # 5. Các hàm chuẩn thật sự có trong code
    math_calls = sorted(set(re.findall(r"\bmath\.(\w+)\(", clean)))
    if math_calls:
        m_map = {
            "log": "lô-ga-rít tự nhiên ln", "log10": "lô-ga-rít cơ số 10", "log2": "cơ số 2",
            "log1p": "ln(1+x)", "exp": "e mũ", "sqrt": "căn bậc hai",
            "ceil": "làm tròn lên", "floor": "làm tròn xuống",
            "hypot": "căn tổng bình phương", "comb": "tổ hợp", "factorial": "giai thừa",
            "radians": "đổi độ sang ra-đi-an", "sin": "sin", "cos": "cos",
        }
        m_txt = ", ".join(m_map.get(c, c) for c in math_calls)
        rows.append([f"<code>math.{', math.'.join(math_calls)}</code>", f"Gọi hàm toán học: {m_txt}"])

    builtins_present = [fn for fn in ("sum", "len", "max", "min", "abs", "round", "sorted", "all", "any", "list", "range", "pow", "hex")
                        if re.search(rf"\b{fn}\(", clean) and not (fn == "range" and re.search(r"\bfor\s+[^:\n]+\s+in\s+range\(", clean))]
    if "range" in builtins_present and "list" in builtins_present and "list(range(" in clean:
        builtins_present = [fn for fn in builtins_present if fn not in ("list", "range")]
        rows.append(["<code>list(range(n))</code>", "Tạo danh sách số nguyên từ <code>0</code> đến <code>n-1</code>"])
    if "sorted" in builtins_present and re.search(r"sorted\([^)\n]*key=", clean):
        builtins_present.remove("sorted")
    if builtins_present:
        b_map = {"sum": "tổng", "len": "độ dài", "max": "lớn nhất", "min": "nhỏ nhất",
                 "abs": "trị tuyệt đối", "round": "làm tròn", "sorted": "sắp xếp",
                 "all": "mọi phần tử đúng", "any": "có ít nhất 1 đúng",
                 "list": "ép sang danh sách", "range": "dãy số nguyên",
                 "pow": "lũy thừa (hỗ trợ lấy dư)", "hex": "đổi sang chuỗi thập lục phân 0x"}
        for i in range(0, len(builtins_present), 4):
            chunk_fn = builtins_present[i:i + 4]
            rows.append([
                "<code>" + " / ".join(f"{fn}(...)" for fn in chunk_fn) + "</code>",
                "Hàm dựng sẵn: " + ", ".join(b_map[fn] for fn in chunk_fn),
            ])

    if re.search(r"\bzip\(", clean):
        rows.append(["<code>zip(a, b)</code>", "Ghép từng cặp phần tử cùng vị trí giữa hai dãy"])
    if re.search(r"\benumerate\(", clean):
        rows.append(["<code>enumerate(ds)</code>", "Lặp lấy đồng thời số thứ tự (từ 0) và giá trị"])
    if re.search(r"\bint\([^)\n]*(?:==|!=|<=|>=|<|>|\bin\b|\band\b|\bor\b|\bnot\b)", clean):
        rows.append(["<code>int(dieu_kien)</code>", "Đổi Đúng/Sai thành số 1 hoặc 0 để chấm điểm"])
    elif re.search(r"\bint\(", clean):
        rows.append(["<code>int(x)</code>", "Ép giá trị về số nguyên (cắt phần lẻ thập phân)"])

    # 6. Toán tử đặc biệt, truy cập chỉ số & dấu phân cách số lớn
    ops = []
    if re.search(r"^\s*[A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*\s*=(?![=])", clean, re.M):
        ops.append(("=", "gán giá trị vào biến"))
    if "**" in clean:
        ops.append(("**", "lũy thừa"))
    if "//" in clean:
        ops.append(("//", "chia lấy phần nguyên"))
    if re.search(r"(?<![\"'{%])\s*%(?!=)\s*(?![\"'}:])", clean):
        ops.append(("%", "chia lấy phần dư"))
    if "+=" in clean or "-=" in clean:
        if "+=" in clean:
            ops.append(("+=", "cộng dồn vào biến"))
        if "-=" in clean:
            ops.append(("-=", "trừ bớt tại chỗ"))
    if re.search(r"==|!=|>=|<=", clean):
        ops.append(("== / != / &gt;= / &lt;=", "so sánh hai giá trị trả về Đúng hoặc Sai"))
    if "<<" in clean or ">>" in clean:
        ops.append(("&lt;&lt; / &gt;&gt;", "dịch bit trái / phải"))
    if ops:
        rows.append([
            "<code>" + ", ".join(k for k, _ in ops) + "</code>",
            "Toán tử: " + ", ".join(f"{html.unescape(k)} là {v}" for k, v in ops),
        ])
    if re.search(r"\b\d+(?:\.\d+)?[eE][+-]?\d+\b", clean):
        rows.append(["<code>1e-9 / 1e6</code>", "Ký hiệu khoa học nhân với lũy thừa của 10 (<code>1e-9</code> = 10⁻⁹, <code>1e6</code> = 10⁶)"])
    if re.search(r"[A-Za-z_]\w*\[(?:[^\]\n:]+|-?\d*:-?\d*)\]", clean):
        rows.append(["<code>ds[i] / ds[:k]</code>", "Lấy phần tử ở vị trí <code>i</code> (từ 0) hoặc <code>k</code> phần tử đầu"])
    if re.search(r"\b\d+_\d+\b", clean):
        rows.append(["<code>100_000</code>", "Dấu gạch dưới tách hàng nghìn cho dễ đọc số lớn (bằng 100000)"])

    # 7. Định dạng chuỗi print chính xác
    fmts = sorted(set(re.findall(r":(\.\d+[fFe%]|\d+f)", clean)))
    if fmts:
        f_show = ", ".join(f"{{{f}}}" if not f.startswith(":") else f"{{x{f}}}" for f in fmts[:3])
        f_desc = ", ".join(
            f"làm tròn {m.group(1)} chữ số" if (m := re.match(r"\.(\d+)f", f))
            else ("ký hiệu khoa học" if "e" in f.lower() else f"định dạng {f}")
            for f in fmts[:3]
        )
        rows.append([f'<code>f"...{f_show}..."</code>', f"Chèn giá trị vào chuỗi theo chuẩn ({f_desc})"])
    elif re.search(r"\bf[\"']", clean):
        rows.append(['<code>f"...{bien}..."</code>', "Nhúng trực tiếp giá trị của biến vào chuỗi kết quả"])

    if re.search(r"\bprint\(", clean):
        rows.append(["<code>print(...)</code>", "In từng dòng kết quả ra màn hình để kiểm khớp đáp án"])

    if not rows:
        rows.append(["<code>print(...)</code>", "Tính biểu thức và in dòng kết quả ra màn hình"])
    return rows


def _atomic_write_text(path: Path, text: str, retries: int = 16, delay: float = 0.35) -> None:
    """Write via sibling temp file + os.replace with retries to avoid Windows Errno 22 locks."""
    import os
    import time
    tmp = path.with_suffix(path.suffix + ".tmp")
    for idx in range(retries):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            os.replace(tmp, path)
            return
        except OSError:
            if idx == retries - 1:
                raise
            time.sleep(delay)


def sync_practice_run_blocks(course: str, lid: str, sol_code: str, lab_out: str | None = None):
    """Đánh dấu khối lời giải tham khảo trong practice là runnable để screen_code.py chạy kiểm chứng thực sự."""
    led_p = ROOT / "audit" / "review" / "screen_code" / f"{course.upper()}.yaml"
    if not led_p.is_file():
        return
    if lab_out is None:
        exp_p = ROOT / "labs" / course.upper() / lid / "mong_doi.txt"
        lab_out = exp_p.read_text(encoding="utf-8") if exp_p.is_file() else ""
    doc = yaml.safe_load(led_p.read_text(encoding="utf-8"))
    blocks = doc.get("blocks") or {}
    actual = ak.sc_mod.all_blocks(course.upper())
    changed = False
    for k, txt in actual.items():
        parts = k.split()
        if parts[1] == lid and parts[2] == "practice":
            if txt.strip() == sol_code.strip():
                sha = ak.sc_mod.digest(txt)
                blocks[k] = {
                    "sha": sha,
                    "kind": "run",
                    "lang": "python",
                    "expect_stdout": lab_out.strip() + "\n",
                }
                changed = True
    if changed:
        doc["blocks"] = blocks
        _atomic_write_text(led_p, up.dump_yaml(doc))


def upgrade_lesson(
    course: str,
    lid: str,
    hint: str,
    de_md: str,
    sol_code: str,
    add_code_if_missing: bool = True,
    covers: list[tuple[int, str]] | None = None,
    force_code: bool = False,
):
    """Nâng cấp 1 bài chuẩn AF2 (idempotent):
    - Giao đề + khuôn định dạng đầu ra + lệnh chấm + `pause: 30` TRƯỚC.
    - Hiện `mong_doi.txt` SAU `pause`.
    - Khi bài chưa có khối mã Python ở thân bài (hoặc force_code=True): hiện bảng giải thích cú pháp khớp 100% mã thật
      và khối `Lời giải tham khảo` SAU `pause` + `mong_doi.txt` (tuyệt đối không lộ trước pause).
    """
    sol_code = sol_code.strip("\n") + "\n"
    spec_path = up._lesson_path(course, lid)
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))

    non_prac = [s for s in spec["scenes"] if s["id"] != "practice"]
    orig_had_code = any(
        '<div class="code"' in (st.get("show") or "")
        or "<div class='code'" in (st.get("show") or "")
        or "<pre" in (st.get("show") or "")
        for sc in non_prac
        for st in sc.get("steps") or []
    )

    spec_clean = dict(spec, scenes=non_prac)
    cov = covers if covers is not None else pick_covers(spec_clean)

    lab_out = up.grade_and_write_lab(course, lid, de_md, "py", sol_code)

    spec["scenes"] = non_prac
    _cleaned_yaml = up.dump_yaml(spec)
    _atomic_write_text(spec_path, _cleaned_yaml)
    _base_file = ROOT / "audit" / course.lower() / "af2" / "base" / f"{lid}.yaml"
    _base_file.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(_base_file, _cleaned_yaml)

    fp, _ = up.apply_upgrade(course, lid, de_md=de_md, ext="py", sol_code=sol_code, de_hint=hint, covers=cov)

    spec2 = yaml.safe_load(fp.read_text(encoding="utf-8"))
    prac = [s for s in spec2["scenes"] if s["id"] == "practice"][0]

    # Step 0: Đề bài + khuôn định dạng + lệnh chấm (kèm chú thích tiếng Việt) + pause: 30
    out_fmt = mask_output_format(lab_out)
    step0_html = ak.table(
        [f"Thực hành {course}:{lid}", "Hướng dẫn tự làm và tự chấm trên máy"],
        [
            ["<b>Đề bài</b>", f"Mở tệp <code>labs/{course}/{lid}/de.md</code>, tự viết chương trình <b>Python</b>"],
            ["<b>Nhiệm vụ</b>", html.escape(hint)],
            ["<b>Khuôn đầu ra cần in</b>", f"<code>{html.escape(out_fmt).replace(chr(10), '<br/>')}</code>"],
            ["<b>Lệnh tự chấm</b>", f"<code>bash labs/cham.sh {course} {lid} duong_dan/bai_cua_ban.py</code><br/><i>(chạy trình dòng lệnh <code>bash</code> gọi công cụ so khớp từng dòng đầu ra với đáp án)</i>"],
        ],
    )
    step0 = ak.st_auto(
        step0_html,
        "Bây giờ đến phần bạn tự thực hành và chấm thật trên máy. "
        "Hãy mở tệp đề bài, đọc kỹ dữ liệu vào cùng khuôn đầu ra cần in, tự viết chương trình rồi gõ lệnh dòng lệnh để tự chấm trước khi xem kết quả.",
        clear=True,
        pause=30,
    )
    step1 = ak.st_auto(
        ak.out_block(lab_out, f"Kết quả mong đợi cần khớp ({len(lab_out.splitlines())} dòng)"),
        "Đây là kết quả mong đợi khi chạy đúng bài làm, dùng để bạn đối chiếu từng dòng trên máy của mình.",
        clear=True,
    )

    new_steps = [step0, step1]
    if add_code_if_missing and (force_code or not orig_had_code):
        read_rows = build_read_rows(sol_code)
        for idx in range(0, len(read_rows), 5):
            chunk = read_rows[idx: idx + 5]
            part = "" if len(read_rows) <= 5 else f" (phần {idx // 5 + 1})"
            new_steps.append(
                ak.st_auto(
                    ak.table(["viết trong mã", "đọc và hiểu là"], chunk),
                    f"Bảng này giải thích từng ký hiệu dùng trong lời giải tham khảo{part} để bạn tự đối chiếu cách viết.",
                    clear=True,
                )
            )
        disp_code = sol_code.strip()
        new_steps.append(
            ak.st_auto(
                ak.code_block(disp_code, f"Lời giải tham khảo {course}:{lid} bằng Python (chỉ xem sau khi tự thử)"),
                "Cuối cùng là lời giải tham khảo bằng mã lệnh chạy ra đúng kết quả trên để bạn đối chiếu lại sau khi đã tự làm.",
                clear=True,
            )
        )

    prac["steps"] = new_steps
    _atomic_write_text(fp, up.dump_yaml(spec2))
    res = lv.lint(lv.load_spec(fp))
    if res.errors or res.warnings:
        raise RuntimeError(f"lint {fp.name} thất bại:\nE={res.errors}\nW={res.warnings}")

    return fp
