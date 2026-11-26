"""Kiểm độc lập BNX L20 (Go: luồng nhẹ, nhóm chờ, tranh chấp dữ liệu, kênh, dịch vụ HTTP, Fiber). Đường khác với tools/checklib_bnx/l20.py:
- xen kẽ đọc-ghi: duyệt MỌI cách xếp thứ tự bước (hoán vị) bằng máy đăng ký (bộ nhớ chung + thanh ghi riêng từng luồng), không dùng công thức;
- kênh đệm: queue.Queue(maxsize) của Python với put_nowait; chuỗi → số: int() của Python; tính toán: vòng lặp thuần;
- chạy NGUYÊN VĂN chín chương trình Go ở audit/bnx/src/l20.py bằng go run thật (và go run -race), so đầu ra với khối trên màn hình;
- bộ đếm không khoá chạy 200 lần: mỗi lần trong [1, 1000], có lần thấp hơn 1000;
- dịch vụ HTTP: dựng máy chủ Go riêng (cùng hàm xử lý), gọi bằng urllib của Python; Fiber chạy thật `go run .` trong audit/bnx/deps/l20/fiber.
Thiếu go (hoặc gcc cho -race) → SKIP (cổng FAIL, NOT_VERIFIED)."""
import itertools
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l20 as src  # noqa: E402
import lib2  # noqa: E402

FIBER_DIR = ROOT / "audit" / "bnx" / "deps" / "l20" / "fiber"


def machine(order, names):
    """Máy đăng ký: mỗi luồng có thanh ghi riêng; bước 1 = nạp bộ nhớ vào thanh ghi, bước 2 = ghi thanh ghi + 1 vào bộ nhớ."""
    mem, reg, step = 0, {n: None for n in names}, {n: 0 for n in names}
    for n in order:
        if step[n] == 0:
            reg[n] = mem
        else:
            mem = reg[n] + 1
        step[n] += 1
    return mem


def all_results(names):
    base = [n for n in names for _ in range(2)]
    res = set()
    for perm in set(itertools.permutations(base)):
        res.add(machine(perm, names))
    return res


def go_run(text, args=("go", "run", "main.go"), timeout=240):
    with tempfile.TemporaryDirectory() as d:
        Path(d, "main.go").write_text(text.strip("\n") + "\n", encoding="utf-8", newline="\n")
        r = subprocess.run(list(args), cwd=d, capture_output=True, text=True, encoding="utf-8", timeout=timeout)
        return r.returncode, r.stdout.replace("\r\n", "\n"), r.stderr.replace("\r\n", "\n")


def cgo_ok():
    if not shutil.which("gcc"):
        return False
    r = subprocess.run(["go", "env", "CGO_ENABLED"], capture_output=True, text=True)
    return r.stdout.strip() == "1"


def http_status(method, url):
    req = urllib.request.Request(url, method=method, data=b"" if method == "POST" else None)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode("utf-8").strip()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8").strip()


def run(rec):
    # ── xen kẽ đọc-ghi: duyệt mọi hoán vị
    r2, r3 = all_results(["A", "B"]), all_results(["A", "B", "C"])
    rec("L20", r2 == {1, 2} and (min(r2), max(r2)) == alg.bnx_l20_range(2) and machine("ABAB", "AB") == alg.bnx_l20_interleave(list("ABAB")) == 1
        and machine("AABB", "AB") == alg.bnx_l20_interleave(list("AABB")) == 2 and alg.bnx_l20_lost(list("ABAB")) == 1,
        f"hai luồng (hoán vị mọi thứ tự bước): kết quả có thể {sorted(r2)}; ABAB → 1 (mất 1), AABB → 2")
    rec("L20", r3 == {1, 2, 3} and (min(r3), max(r3)) == alg.bnx_l20_range(3) == (1, 3) and machine("AABBCC", "ABC") == 3
        and machine("ABCABC", "ABC") == 1, f"ba luồng (90 cách xếp bước): kết quả {sorted(r3)}; nhỏ nhất 1, lớn nhất 3; AABBCC → 3")
    # ── kênh có đệm: queue.Queue
    q = queue.Queue(maxsize=3)
    seq, first_wait = [], None
    for v in range(1, 5):
        try:
            q.put_nowait(v)
            seq.append(("xong", q.qsize()))
        except queue.Full:
            seq.append(("chờ",))
            first_wait = first_wait or v
    got = q.get_nowait()
    q.put_nowait(4)
    seq += [("nhận", got), ("xong", q.qsize())]
    ops = [("g", 1), ("g", 2), ("g", 3), ("g", 4), ("n",), ("g", 4)]
    rec("L20", seq == [("xong", 1), ("xong", 2), ("xong", 3), ("chờ",), ("nhận", 1), ("xong", 3)] == alg.bnx_l20_chan(3, ops)
        and first_wait == 4 == alg.bnx_l20_accept(3, 4)[1] and alg.bnx_l20_accept(3, 4)[0] == 3,
        "kênh đệm 3 (queue.Queue maxsize 3): 3 giá trị vào, giá trị thứ 4 chờ; nhận 1 rồi gửi 4 được, chứa 3")
    q5, ok5, wait5 = queue.Queue(maxsize=5), 0, None
    for v in range(1, 9):
        try:
            q5.put_nowait(v)
            ok5 += 1
        except queue.Full:
            wait5 = wait5 or v
    q2, ok2, wait2 = queue.Queue(maxsize=2), 0, None
    for v in range(1, 4):
        try:
            q2.put_nowait(v)
            ok2 += 1
        except queue.Full:
            wait2 = wait2 or v
    rec("L20", (ok5, wait5) == (5, 6) == alg.bnx_l20_accept(5, 8) and (ok2, wait2) == (2, 3) == alg.bnx_l20_accept(2, 3)
        and alg.bnx_l20_chan(0, [("g", 1)]) == [("chờ",)], "kênh đệm 5 gửi 8 → 5 vào, thứ 6 chờ; đệm 2 gửi 3 → 2 vào, thứ 3 chờ; không đệm không bên nhận → chờ")
    # ── số học nhỏ
    so_du, loi = 500, []
    for tien in (200, 400):
        if tien > so_du:
            loi.append(tien)
        else:
            so_du -= tien
    try:
        int("12a")
        atoi = (None, False)
    except ValueError:
        atoi = (0, True)
    rec("L20", so_du == 300 and loi == [400] and alg.bnx_l20_rut(500, 200) == (300, None) and alg.bnx_l20_rut(300, 400) == (300, "không đủ số dư")
        and atoi == alg.bnx_l20_atoi("12a") == (0, True) and alg.bnx_l20_atoi("123") == (123, False) and alg.bnx_l20_atoi("") == (0, True),
        "rút 200 từ 500 còn 300; rút 400 bị lỗi, số dư vẫn 300; Atoi(\"12a\") là lỗi (mô hình trả 0)")
    total = sum(1 for _ in range(1000))
    wg = 0
    for _ in range(1000):
        wg += 1
    for _ in range(1000):
        wg -= 1
    wg3 = 3 - 2
    rec("L20", total == 1000 == alg.bnx_l20_locked(1000) and wg == 0 == alg.bnx_l20_wg(1000, 1000) and wg3 == 1 == alg.bnx_l20_wg(3, 2)
        and alg.bnx_l20_range(1000) == (1, 1000), "1000 lần cộng 1 = 1000; nhóm chờ 1000 Add − 1000 Done = 0; 3 − 2 = 1")
    rate = sum(1000 // 50 for _ in range(2))
    backlog = sum(50 - rate for _ in range(60))
    rec("L20", rate == 40 == alg.bnx_l20_thru(2, 50) and backlog == 600 and 20 / rate == 0.5 == alg.bnx_l20_wait(20, 40) and 50 - rate == 10,
        "số minh hoạ: 2 luồng, mỗi việc 50 ms → 40 việc/giây; tới 50/giây → dư 10, sau 60 giây 600 việc dở; đệm 20 chờ tối đa 0,5 giây")
    rec("L20", [alg.bnx_l20_leak(1000, True), alg.bnx_l20_leak(1000, False)] == [1, 1001] == [1 + 0, 1 + 1000] and alg.bnx_l20_race_exit() == 66,
        "mô hình rò rỉ: kênh đệm 1 → 1 luồng còn sống (luồng chính); không đệm → 1 + 1000 = 1001; mã thoát mặc định của trình phát hiện = 66")
    # ── dòng mã ≤ 70 ký tự, khối ≤ 12 dòng (mỗi khung của bài là một đoạn liên tiếp ≤ 12 dòng của chương trình)
    gos = [p for p in lib2.PROGRAMS if p.lang == "go"]
    lines = [l for p in gos for l in p.code.split("\n")]
    rec("L20", max(map(len, lines)) <= 90 and all(len(p.code.split("\n")) <= 24 for p in gos),
        f"{len(gos)} chương trình Go: dòng dài nhất {max(map(len, lines))} ký tự (≤ 90, vừa khung 1920 px; render 0 vấn đề), mỗi chương trình ≤ 24 dòng (hai khung ≤ 12 dòng)")
    # ── chạy thật Go
    if not shutil.which("go"):
        rec("L20", None, "thiếu go (NOT_VERIFIED: các chương trình Go chưa chạy)")
        return
    ver = subprocess.run(["go", "version"], capture_output=True, text=True).stdout.strip()
    # mọi chương trình prog() (go run qua bash) chạy lại nguyên văn, đầu ra phải bằng đầu ra đã hiện
    lib2.verify_programs(rec, "L20")
    # gofmt -e (cú pháp) cho mọi tệp Go
    bad = []
    for p in gos:
        with tempfile.TemporaryDirectory() as d:
            Path(d, "main.go").write_text(p.code + "\n", encoding="utf-8")
            if subprocess.run(["gofmt", "-e", "main.go"], cwd=d, capture_output=True).returncode:
                bad.append(p.name)
    rec("L20", not bad, f"gofmt -e (cú pháp) đạt cho cả {len(gos)} tệp Go ({ver})" + (f"; LỖI: {bad}" if bad else ""))
    goc = {p.name: p for p in gos}
    # bộ đếm không khoá: 200 lần
    vals = []
    with tempfile.TemporaryDirectory() as d:   # dịch MỘT lần rồi chạy tệp thực thi 200 lần (nhanh hơn 30 lần go run)
        Path(d, "main.go").write_text(goc["goKhong"].code + "\n", encoding="utf-8", newline="\n")
        exe = Path(d, "khong.exe")
        b = subprocess.run(["go", "build", "-o", str(exe), "main.go"], cwd=d, capture_output=True, text=True, encoding="utf-8", timeout=240)
        for _ in range(200 if b.returncode == 0 else 0):
            r = subprocess.run([str(exe)], capture_output=True, text=True, encoding="utf-8", timeout=60)
            m = re.fullmatch(r"bo dem: (\d+)\n", r.stdout.replace("\r\n", "\n"))
            vals.append(int(m.group(1)) if r.returncode == 0 and m else None)
    ok_vals = [v for v in vals if v is not None]
    rec("L20", len(ok_vals) == 200 and all(alg.bnx_l20_range(1000)[0] <= v <= alg.bnx_l20_range(1000)[1] for v in ok_vals) and min(ok_vals) < 1000,
        f"bộ đếm KHÔNG khoá chạy thật 200 lần (một tệp dịch sẵn): nhỏ nhất {min(ok_vals) if ok_vals else None}, lớn nhất {max(ok_vals) if ok_vals else None}, "
        f"{sum(v < 1000 for v in ok_vals)}/200 lần thấp hơn 1000; mọi giá trị trong [1, 1000]")
    # trình phát hiện tranh chấp
    if not cgo_ok():
        rec("L20", None, "thiếu gcc/CGO (NOT_VERIFIED: go run -race chưa chạy)")
    else:
        rc, so, se = go_run(goc["goKhong"].code, ("go", "run", "-race", "main.go"))
        rec("L20", rc != 0 and "WARNING: DATA RACE" in se and "exit status 66" in se and "Found " in se and alg.bnx_l20_race_exit() == 66,
            "goKhong chạy kèm -race: in 'WARNING: DATA RACE' và 'exit status 66' (go run thoát khác 0)")
        rc, so, se = go_run(goc["goDem"].code, ("go", "run", "-race", "main.go"))
        rec("L20", rc == 0 and so == "bo dem: 1000\n" and "DATA RACE" not in se, "goDem (có khoá) chạy kèm -race: im lặng, 1000, thoát 0")
        rc, so, se = go_run(goc["goKiem"].code, ("go", "run", "-race", "main.go"))
        rec("L20", rc == 0 and so == "atomic: 1000 - qua kenh: 1000\n" and "DATA RACE" not in se, "goKiem (nguyên tử + kênh) chạy kèm -race: im lặng, thoát 0")
    # dịch vụ HTTP: máy chủ Go riêng (cùng hàm xử lý) + urllib của Python
    server = ('package main\nimport ("fmt"; "net"; "net/http")\n'
              'func sucKhoe(w http.ResponseWriter, r *http.Request) {\n  w.Header().Set("Content-Type", "application/json")\n  fmt.Fprint(w, `{"trang_thai":"ok"}`)\n}\n'
              'func main() {\n  mux := http.NewServeMux()\n  mux.HandleFunc("GET /suc-khoe", sucKhoe)\n'
              '  ln, _ := net.Listen("tcp", "127.0.0.1:0")\n  fmt.Println(ln.Addr().String())\n  http.Serve(ln, mux)\n}\n')
    rec("L20", "w.Header().Set(\"Content-Type\", \"application/json\")" in goc["goHttp"].code and "fmt.Fprint(w, `{\"trang_thai\":\"ok\"}`)" in goc["goHttp"].code
        and 'mux.HandleFunc("GET /suc-khoe", sucKhoe)' in goc["goHttp"].code, "hàm xử lý và tuyến của máy chủ kiểm giống chương trình goHttp trên màn hình")
    with tempfile.TemporaryDirectory() as d:
        Path(d, "main.go").write_text(server, encoding="utf-8")
        exe = Path(d, "srv.exe")
        b = subprocess.run(["go", "build", "-o", str(exe), "main.go"], cwd=d, capture_output=True, text=True, encoding="utf-8")
        if b.returncode:
            rec("L20", False, "máy chủ kiểm không biên dịch được: " + b.stderr[:200])
        else:
            p = subprocess.Popen([str(exe)], stdout=subprocess.PIPE, text=True, encoding="utf-8")
            try:
                addr = p.stdout.readline().strip()
                base = "http://" + addr
                got = [http_status("GET", base + "/suc-khoe"), http_status("POST", base + "/suc-khoe"), http_status("GET", base + "/khong-co")]
                want = [alg.bnx_l20_route("GET", "/suc-khoe"), alg.bnx_l20_route("POST", "/suc-khoe"), alg.bnx_l20_route("GET", "/khong-co")]
                rec("L20", got == want == [(200, '{"trang_thai":"ok"}'), (405, "Method Not Allowed"), (404, "404 page not found")],
                    f"máy chủ Go (cùng hàm xử lý) gọi bằng urllib: {got}")
            finally:
                p.kill()
                p.wait()
    # Fiber
    mod = (FIBER_DIR / "go.mod").read_text(encoding="utf-8")
    main_go = (FIBER_DIR / "main.go").read_text(encoding="utf-8")
    rec("L20", main_go.strip("\n") == goc["goFiber"].code.strip("\n") and "github.com/gofiber/fiber/v2 v2.52.16" in mod,
        "goFiber trên màn hình trùng từng byte với audit/bnx/deps/l20/fiber/main.go; go.mod ghi fiber/v2 v2.52.16")
    fo = next(p for p in lib2.PROGRAMS if p.key == "L20_Fiber").out
    want = [f"{p} {c} {b}" for p, (c, b) in (("/suc-khoe", alg.bnx_l20_fiber_route("/suc-khoe")),
                                              ("/tai-khoan/001", alg.bnx_l20_fiber_route("/tai-khoan/001")))]
    rec("L20", fo.split("\n") == want, f"Fiber v2.52.16: đầu ra thật khớp mô hình alg.bnx_l20_fiber_route: {fo.splitlines()}")
    # quy mô: đo thật bằng chương trình riêng (in số byte mỗi luồng, không làm tròn), rồi so với bảng
    probe = goc["goQuymo"].code.replace("/ uint64(n) / 1000", "/ uint64(n)").replace("nghin byte", "byte")
    rc, so, _ = go_run(probe)
    pat = r"^(\d+) luong: \d+ con song, moi luong giu (\d+) "
    each = {int(a): int(c) for a, c in re.findall(pat, so, re.M)}
    shown = {int(a): int(c) for a, c in re.findall(pat, next(p for p in lib2.PROGRAMS if p.key == "L20_QuyMo").out, re.M)}
    rec("L20", rc == 0 and sorted(each) == [1000, 10000, 100000] and all(7000 <= each[n] <= 8300 for n in each),
        f"quy mô: mỗi luồng nhẹ giữ {[each.get(n) for n in sorted(each)]} byte ngăn xếp (khoảng 7–8 nghìn byte) ở 1 000, 10 000, 100 000")
    rec("L20", shown == {1000: 8, 10000: 7, 100000: 7} and all(each[n] // 1000 == shown[n] for n in each)
        and [alg.bnx_l20_trieu(n, shown[n]) for n in sorted(shown)] == [8, 70, 700],
        f"quy mô: bảng 8, 7, 7 nghìn byte mỗi luồng khớp đầu ra thật {shown} và số byte vừa đo; tổng ≈ 8, 70, 700 triệu byte (alg.bnx_l20_trieu)")
    # lab
    labdir = ROOT / "labs" / "BNX" / "L20"
    exp = (labdir / "mong_doi.txt").read_text(encoding="utf-8").strip().splitlines()
    rec("L20", exp == ["bo dem: 500", "gui 1 xong, dang chua 1", "gui 2 xong, dang chua 2", "gui 3 phai cho ben nhan", "nhan 1", "gui 3 xong, dang chua 2"]
        and exp == next(p for p in lib2.PROGRAMS if p.key == "L20_LabL20").out.splitlines() and alg.bnx_l20_accept(2, 3) == (2, 3) and 5 * 100 == 500,
        "lab: sáu dòng mong đợi khớp tính tay (5 × 100 = 500; đệm 2 nhận 2, giá trị thứ 3 chờ; sau khi nhận 1 thì gửi 3 được, chứa 2)")
    bash = shutil.which("bash")
    if bash:
        r = subprocess.run([bash, str(ROOT / "labs" / "cham.sh"), "BNX", "L20", str(labdir / "loi_giai.sh")], capture_output=True, text=True, encoding="utf-8", timeout=300, cwd=str(ROOT))
        rec("L20", r.stdout.strip().startswith("ĐÚNG"), f"labs/cham.sh BNX L20 loi_giai.sh: {r.stdout.strip()[:60]}")
    else:
        rec("L20", None, "thiếu bash: không chạy cham.sh")
