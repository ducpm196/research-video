"""Kiểm độc lập BNX L17 (Spring Security và Spring Cloud). Đường khác với tools/checklib_bnx/l17.py:
- CHẠY THẬT Spring Security 7.1.2 (jar ở audit/bnx/deps/l17, so sha256 với README trước khi chạy): CauHinh.java + ChayThu.java NGUYÊN VĂN,
  đầu ra phải bằng OUT_SPRING từng ký tự, hai lần; thứ tự 14 trạm và 7 mã trạng thái đối chiếu với mô hình alg.bnx_l17_*;
- kiểm NGƯỢC nguyên nhân 403 của POST: cấu hình sửa (tắt CSRF) thì POST không mã phải nhận 401, không còn 403;
- chia tải: Java thuần ChiaTai.java chạy thật; Python đếm bằng bộ đếm tăng dần (không dùng divmod của alg);
- cận trên yêu cầu lỗi: mô phỏng từng giây với bộ đếm xoay vòng thật, đối chiếu công thức rate · giây : bản;
- PY_CHECK chạy thật bằng Python; các khối YAML Y_* phân tích bằng yaml.safe_load.
Thiếu jar / sha256 sai / javac / java → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import ast
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import importlib.util  # noqa: E402
import l17 as src  # noqa: E402

_sp = importlib.util.spec_from_file_location('bnx_l17_ref', ROOT / 'tools' / 'checklib_bnx' / 'l17.py')
REF = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(REF)
DEPS = ROOT / "audit" / "bnx" / "deps" / "l17"
SHA = {  # đúng bảng ở audit/bnx/deps/l17/README.md
    "commons-logging-1.3.5.jar": "6d7a744e4027649fbb50895df9497d109f98c766a637062fe8d2eabbb3140ba4",
    "jakarta.servlet-api-6.1.0.jar": "8a31f465f3593bf2351531a5c952014eb839da96a605b5825b93dd54714c48c4",
    "jspecify-1.0.1.jar": "070d75f261fe4c5b8202508366715f7f2d4660f88c8ef7e6d3575e48c9683b66",
    "micrometer-commons-1.17.2.jar": "af8c85e879025ce30c381e6810e14c4f52b4150894e36c815860d14763271348",
    "micrometer-observation-1.17.2.jar": "d3ff53cfa0532dc1af0de349073f9aeb985e01f4b88c1d904350178805859695",
    "nimbus-jose-jwt-10.9.1.jar": "33152ea83ec50d22706fdaf3b07acbcd716f9a68edcabdd7c4d02843cbdcdcf6",
    "spring-aop-7.0.10.jar": "babf50a645f4f788e1267078cf891e472f657cabf65518055cf5214220574e3f",
    "spring-beans-7.0.10.jar": "bd67c6fc887afa30cbcb489ff4f82bf19f818e79ab1cf1bef98dff8a289108ec",
    "spring-context-7.0.10.jar": "f0065166b6a5101a871ab8702d6c4011cf39faed370a64e7ef14a3ad2bf2a99a",
    "spring-core-7.0.10.jar": "a236f31a7c07e3a1a8e7839ec5c0d47b5cc75709132db50416d5dad320341f12",
    "spring-expression-7.0.10.jar": "12067b66548f7613fa8938ca6051a6d1dd8c397bf478e0bb1adb9936358ec81d",
    "spring-security-config-7.1.2.jar": "826af4e79495d54b761a5f0313774a07d36359e83dd5518d57d69bacd7bbf478",
    "spring-security-core-7.1.2.jar": "39df3dc77436d3e9308f89056c1a42605e08f0ad9ad208f7e34c4b16102886e1",
    "spring-security-crypto-7.1.2.jar": "4aaa60bb612d5fece004c07f893b3a8d707c207bbd8585d10e0015b5301cd864",
    "spring-security-oauth2-core-7.1.2.jar": "aa50c141cb303bae1b87d761f9459930d75af280c43e80b7488d50e62dd1e216",
    "spring-security-oauth2-jose-7.1.2.jar": "e956dcaf0342699b967b5ca301d628d0808e97c7e6614b822fe832f6eba762dc",
    "spring-security-oauth2-resource-server-7.1.2.jar": "a154ce053da747c0be4144794cf2bd835b6cd56e09d1b4b2a62dfdcda6d273fb",
    "spring-security-web-7.1.2.jar": "fc36d37695462dbe4fb32bd6820043afbf83ebcffce4974929bf79a29fcb5e73",
    "spring-test-7.0.10.jar": "73c18292b63e814c415c1c470fcc47be1e21442b80ee31a0bcd949e53d0c49bd",
    "spring-web-7.0.10.jar": "76ddb03d236547f6852def8cb303e1cf2cd2c1954dec5bf2abd87d11b89dfee7",
}
CASES = ["A", "B", "C", "D", "E", "F", "G"]


def ls(text):
    return text.strip(chr(10)).split(chr(10))


def line_match(want, got):
    rx = re.compile("^" + ".*".join(re.escape(p) for p in want.strip().split("…")) + "$")
    return bool(rx.match(got.strip()))


def screen_matches(screen, actual):
    """Mỗi dòng khác rỗng trên màn hình (… = đoạn lược) khớp CẢ MỘT dòng đầu ra thật, đúng thứ tự."""
    lines, pos = actual.replace("\r\n", "\n").split("\n"), 0
    for w in [x for x in screen.strip("\n").split("\n") if x.strip()]:
        while pos < len(lines) and not line_match(w, lines[pos]):
            pos += 1
        if pos == len(lines):
            return False
        pos += 1
    return True


def run_spring(cfg, runner):
    """Biên dịch + chạy CauHinh/ChayThu với jar thật; trả (mã thoát, stdout) hoặc (mã, lỗi biên dịch)."""
    with tempfile.TemporaryDirectory() as d:
        dp = Path(d)
        (dp / "lib").mkdir()
        for j in SHA:
            shutil.copy(DEPS / j, dp / "lib" / j)
        (dp / "CauHinh.java").write_text(cfg.strip("\n") + "\n", encoding="utf-8", newline="\n")
        (dp / "ChayThu.java").write_text(runner.strip("\n") + "\n", encoding="utf-8", newline="\n")
        r = subprocess.run(["javac", "-encoding", "UTF-8", "-cp", "lib/*", "-d", "out", "CauHinh.java", "ChayThu.java"], cwd=d,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
        if r.returncode:
            return r.returncode, r.stderr
        r = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-cp", "out" + os.pathsep + "lib/*", "ChayThu"], cwd=d,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
        return r.returncode, r.stdout.replace("\r\n", "\n")


def run_plain(code, cls):
    with tempfile.TemporaryDirectory() as d:
        Path(d, cls + ".java").write_text(code.strip("\n") + "\n", encoding="utf-8")
        r = subprocess.run(["javac", "-encoding", "UTF-8", "-d", d, cls + ".java"], cwd=d, capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        if r.returncode:
            return r.returncode, r.stderr
        r = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-cp", d, cls], cwd=d, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=120)
        return r.returncode, r.stdout.replace("\r\n", "\n")


def parse(out):
    """Tách đầu ra thật: danh sách trạm (thứ tự) và, mỗi ca, (có qua trạm quan sát, tới dịch vụ, mã trạng thái, đầu mục)."""
    chain, cases, cur = [], {}, None
    for ln in out.split("\n"):
        m = re.match(r"^(\d+) (\w+)$", ln)
        if m:
            chain.append((int(m.group(1)), m.group(2)))
            continue
        m = re.match(r"^([A-H])\. ", ln)
        if m:
            cur = m.group(1)
            cases[cur] = {"obs": False, "svc": False, "st": None, "hdr": ""}
            continue
        if cur is None:
            continue
        s = ln.strip()
        if s == "qua trạm quan sát":
            cases[cur]["obs"] = True
        elif s == "tới dịch vụ":
            cases[cur]["svc"] = True
        elif s.startswith("mã trạng thái "):
            cases[cur]["st"] = int(s.split()[-1])
        elif s:
            cases[cur]["hdr"] = s
    return chain, cases


def round_robin_counter(health, n):
    """Bộ đếm tăng dần (không divmod): yêu cầu thứ k tới bản khoẻ thứ k mod số bản khoẻ."""
    alive = [i for i, h in enumerate(health) if h]
    cnt = Counter()
    for k in range(n):
        cnt[alive[k % len(alive)]] += 1
    return [cnt[i] for i in range(len(health))]


def lost_by_simulation(rate, total, seconds):
    """Từng giây, từng yêu cầu: bản chết là bản số 0 trong vòng xoay; đếm yêu cầu rơi vào nó."""
    k = lost = 0
    for _ in range(seconds):
        for _ in range(rate):
            if k % total == 0:
                lost += 1
            k += 1
    return lost


def run(rec):
    # ── phần không cần công cụ ──
    for h, n, want in (([True, False, True], 100, [50, 0, 50]), ([True] * 3, 100, [34, 33, 33]), ([True, True], 6, [3, 3]),
                       ([True, False, True, True], 90, [30, 0, 30, 30]), ([True, False, False, True], 90, [45, 0, 0, 45])):
        rec("L17", round_robin_counter(h, n) == want == alg.bnx_l17_round_robin(h, n),
            f"chia xoay vòng {n} yêu cầu cho {sum(h)}/{len(h)} bản khoẻ: bộ đếm tăng dần = alg = {want}")
    rec("L17", 100 // 2 == 50 and 3 - 1 == 2 and 90 // 3 == 30 and 90 // 2 == 45 and 45 / 30 == 1.5, "phép chia: 100:2 = 50; 90:3 = 30; 90:2 = 45; 45/30 = 1,5")
    l45, l37 = lost_by_simulation(100, 3, 45), lost_by_simulation(100, 3, 37)
    rec("L17", l45 == 1500 == alg.bnx_l17_lost(100, 3, 45) and l37 == 1234 == -(-100 * 37 // 3) and alg.bnx_l17_lost(100, 3, 37) == 1233
        and alg.bnx_l17_stale_window(10, 35) == 45 and alg.bnx_l17_stale_window(2, 35) == 37 and 10 - 2 == 8 and 5 == 10 // 2,
        f"câu 3 (số minh hoạ): mô phỏng từng yêu cầu cho {l45} lỗi trong 45 giây (= 1500) và {l37} trong 37 giây (công thức 100·37:3 = 1233,3, cận trên làm tròn lên = 1234 = số bài nói)")
    rec("L17", alg.bnx_l17_authorities("so_du han_muc") == ["SCOPE_" + s for s in "so_du han_muc".split()] and len("so_du han_muc".split()) == 2,
        "scope 'so_du han_muc' → 2 quyền SCOPE_so_du, SCOPE_han_muc")
    # khối YAML chép từ tài liệu: phân tích thật, kiểm đúng điều bài nói
    rs = yaml.safe_load(src.Y_RS)
    gw = yaml.safe_load(src.Y_GW)
    cf = yaml.safe_load(src.Y_CIPHER)
    route = gw["spring"]["cloud"]["gateway"]["server"]["webflux"]["routes"][0]
    rec("L17", rs["spring"]["security"]["oauth2"]["resourceserver"]["jwt"]["issuer-uri"].startswith("https://")
        and route["uri"].startswith("lb://") and route["predicates"] == ["Path=/service/**"]
        and cf["spring"]["datasource"]["password"].startswith("{cipher}")
        and yaml.safe_load(src.Y_CONSUL)["spring"]["cloud"]["consul"]["discovery"]["healthCheckInterval"] == "15s",
        "Y_RS/Y_GW/Y_CIPHER/Y_CONSUL phân tích được; issuer-uri https, uri lb://, Path, tiền tố {cipher} (đối chiếu sources_l17.md; KHÔNG chạy các cấu hình này)")
    shown = [ls(src.J_CFG)[11:37], ls(src.J_RUN)[18:51], ls(src.SH_RUN)[3:5]]
    shown += [ls(c) for c in (src.J_LB, src.PY_CHECK, src.Y_RS, src.Y_GW, src.Y_CIPHER, src.OUT_CHAIN, src.OUT_A, src.OUT_B,
                              src.OUT_C, src.OUT_D, src.OUT_E, src.OUT_FG, src.OUT_LB, src.OUT_CHECK)]
    lines = [ln for blk in shown for ln in blk]
    rec("L17", max(map(len, lines)) <= 70, f"dòng mã/đầu ra HIỆN trên màn hình dài nhất {max(map(len, lines))} ký tự (≤ 70; các dòng import ở đầu CauHinh.java không hiện)")

    # ── Python thật: bảng quyết định trên màn hình ──
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", src.PY_CHECK], capture_output=True, text=True, encoding="utf-8")
    rec("L17", r.returncode == 0 and r.stdout.replace("\r\n", "\n") == src.OUT_CHECK.strip("\n") + "\n",
        "PY_CHECK chạy thật (Python): [401, 401, 403, 200, 401] và 50 [34, 33, 33] khớp NGUYÊN VĂN màn hình")

    # ── Java ──
    if not (shutil.which("javac") and shutil.which("java")):
        rec("L17", None, "NOT_VERIFIED: thiếu javac/java (Spring Security và mô phỏng chia tải chưa chạy)")
        return
    rc, so = run_plain(src.J_LB, "ChiaTai")
    rec("L17", rc == 0 and so == src.OUT_LB.strip("\n") + "\n" and "{bản 1=34, bản 2=33, bản 3=33}" in so and "{bản 1=50, bản 3=50}" in so,
        "ChiaTai.java (mô phỏng Java thuần) chạy thật: ba bản khoẻ 34/33/33; bản 2 trượt 50/50; khớp màn hình")
    miss = [j for j in SHA if not (DEPS / j).exists()]
    if miss:
        rec("L17", None, f"NOT_VERIFIED: thiếu {len(miss)} jar ở audit/bnx/deps/l17 (đầu tiên: {miss[0]}); tải lại theo README.md — Spring Security chưa chạy")
        return
    bad = [j for j, h in SHA.items() if hashlib.sha256((DEPS / j).read_bytes()).hexdigest() != h]
    if bad:
        rec("L17", False, f"sha256 sai: {bad}")
        return
    rec("L17", True, f"{len(SHA)} jar ở deps/l17 đúng sha256 trong README")
    readme = (DEPS / "README.md").read_text(encoding="utf-8")
    rec("L17", all(h in readme for h in SHA.values()), "sha256 trong ver/l17.py trùng bảng README.md")

    outs = [run_spring(src.J_CFG, src.J_RUN) for _ in range(2)]
    want = src.OUT_SPRING.strip("\n") + "\n"
    rec("L17", all(rc == 0 and so == want for rc, so in outs),
        "Spring Security 7.1.2 THẬT: CauHinh.java + ChayThu.java nguyên văn chạy 2 lần, đầu ra khớp OUT_SPRING từng ký tự"
        + ("" if outs[0][0] == 0 else f" — LỖI: {outs[0][1][:200]}"))
    rc, so = outs[0]
    if rc != 0:
        return
    chain, cases = parse(so)
    rec("L17", [n for _, n in chain] == REF.BNX_L17_CHAIN and [i for i, _ in chain] == list(range(1, 15)) and len(chain) == alg.bnx_l17_chain_len() == 14,
        "14 trạm in ra từ FilterChainProxy.getFilters đúng thứ tự và đúng tên với mô hình alg (BNX_L17_CHAIN)")
    for nm in ("CsrfFilter", "BearerTokenAuthenticationFilter", "TramQuanSat", "ExceptionTranslationFilter", "AuthorizationFilter"):
        rec("L17", dict((n, i) for i, n in chain)[nm] == alg.bnx_l17_pos(nm), f"vị trí trạm {nm} = {alg.bnx_l17_pos(nm)} (đầu ra thật = alg)")
    tok = {"A": (None, "GET"), "B": (src.T_GIA, "GET"), "C": (src.T_AN, "GET"), "D": (src.T_BINH, "GET"), "E": (src.T_CU, "GET"),
           "F": (None, "POST"), "G": (src.T_BINH, "POST")}
    allok = True
    for c in CASES:
        t, method = tok[c]
        model = alg.bnx_l17_trace(method, (ast.literal_eval(t) if t else None), "han_muc")
        real = cases[c]
        allok &= (real["st"], real["obs"], real["svc"]) == (model[0], model[2], model[3])
    rec("L17", allok and [cases[c]["st"] for c in CASES] == [401, 401, 403, 200, 401, 403, 200],
        "bảy ca chạy thật: mã trạng thái, đi qua trạm quan sát, tới dịch vụ — đều khớp alg.bnx_l17_trace; = 401, 401, 403, 200, 401, 403, 200")
    rec("L17", cases["A"]["st"] == 401 and cases["C"]["st"] == 403 and cases["D"]["st"] == 200 and cases["A"]["obs"] and cases["C"]["obs"]
        and not cases["B"]["obs"] and not cases["E"]["obs"] and not cases["F"]["obs"],
        "ví dụ giáo án: không mã 401; mã thật thiếu quyền 403; đủ quyền 200. Mã hỏng và lệnh POST thiếu mã không tới trạm quan sát (dừng trước trạm 9)")
    rec("L17", "insufficient_scope" in cases["C"]["hdr"] and "Invalid signature" in cases["B"]["hdr"] and "Jwt expired at 2023-11-14T22:13:20Z" in cases["E"]["hdr"]
        and cases["A"]["hdr"].startswith("Bearer resource_metadata="),
        "đầu mục WWW-Authenticate thật: A resource_metadata; B Invalid signature; C insufficient_scope; E hết hạn 2023-11-14T22:13:20Z")
    import datetime
    rec("L17", datetime.datetime.fromtimestamp(1700000000, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") == "2023-11-14T22:13:20Z",
        "1700000000 (exp của mã cũ) = 2023-11-14T22:13:20Z (tính bằng Python)")
    parts = {"OUT_CHAIN": src.OUT_CHAIN, "OUT_A": src.OUT_A, "OUT_B": src.OUT_B, "OUT_C": src.OUT_C, "OUT_D": src.OUT_D, "OUT_E": src.OUT_E, "OUT_FG": src.OUT_FG}
    bad = [k for k, v in parts.items() if not screen_matches(v, so)]
    rec("L17", not bad, "mọi đoạn đầu ra trên màn hình (OUT_CHAIN, A–E, F–G) khớp từng dòng, đúng thứ tự, với đầu ra thật" + (f" — LỆCH: {bad}" if bad else ""))

    # ── kiểm ngược nguyên nhân 403 của POST: tắt CSRF thì POST không mã phải nhận 401 ──
    cfg2 = src.J_CFG.replace("    http.oauth2ResourceServer(", "    http.csrf(c -> c.disable());\n    http.oauth2ResourceServer(")
    runner2 = src.J_RUN
    rc2, so2 = run_spring(cfg2, runner2)
    if rc2 != 0:
        rec("L17", False, f"cấu hình tắt CSRF không chạy được: {so2[:200]}")
    else:
        ch2, cs2 = parse(so2)
        rec("L17", cs2["F"]["st"] == 401 and cs2["G"]["st"] == 200 and cs2["A"]["st"] == 401 and "CsrfFilter" not in [n for _, n in ch2],
            "kiểm ngược: tắt CSRF thì POST không mã nhận 401 (không còn 403), POST đủ quyền vẫn 200, chuỗi mất CsrfFilter → thủ phạm 403 của ca F là CsrfFilter")
    # ── LF2 (F12): POST mang mã ký sai (ca H) phải nhận 401, không phải 403 của CsrfFilter; chỉ chạy ở bộ kiểm, KHÔNG hiện trên màn hình ──
    runner3 = src.J_RUN.replace('    thu("G. lệnh POST, đủ quyền", "POST", binh);',
                                '    thu("G. lệnh POST, đủ quyền", "POST", binh);\n    thu("H. lệnh POST, mã ký bằng khoá khác", "POST", gia);')
    assert runner3 != src.J_RUN
    rc3, so3 = run_spring(src.J_CFG, runner3)
    if rc3 != 0:
        rec("L17", False, f"biến thể có ca H không chạy được: {so3[:200]}")
    else:
        _, cs3 = parse(so3)
        rec("L17", cs3["H"]["st"] == 401 and not cs3["H"]["obs"] and "Invalid signature" in cs3["H"]["hdr"] and cs3["F"]["st"] == 403,
            "LF2 F12: lệnh POST mang mã ký sai nhận 401 (trạm đọc mã trả, không qua trạm 9), còn POST không mã nhận 403 — yêu cầu có đầu mục mã không bị CsrfFilter chặn với cấu hình này (bài không khẳng định cơ chế)")
    # ── kiểm ngược thứ tự: mã hỏng dừng ở trạm đọc mã ──
    rec("L17", alg.bnx_l17_pos("BearerTokenAuthenticationFilter") < alg.bnx_l17_pos("TramQuanSat") < alg.bnx_l17_pos("AuthorizationFilter")
        and not cases["B"]["obs"] and cases["C"]["obs"], "trạm 8 < trạm 9 < trạm 14; mã hỏng không tới trạm 9, mã tốt tới trạm 9 (quan sát thật)")
