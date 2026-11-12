"""Kiểm độc lập BNX L22 (AEM: JCR, Sling, HTL, OSGi). MÁY KHÔNG CÓ MÁY CHỦ AEM: mọi cơ chế trong bài là MÔ PHỎNG theo tài liệu
(audit/bnx/sources_l22.md). Đường khác với tools/checklib_bnx/l22.py:
- chạy NGUYÊN VĂN các khối Python hiện trên màn hình (hằng ở audit/bnx/src/l22.py) bằng exec, so đầu ra với khối "Kết quả chạy thật";
- bảng 14 hàng của Apache Sling “URL decomposition” gõ lại ở đây như văn bản của tài liệu (dấu "-" = null), là chuẩn đối chiếu cho
  (a) hàm tách trên màn hình (chạy với kho {/a/b}), (b) alg.bnx_l22_split, (c) một hàm tách thứ ba viết khác (duyệt nút theo độ dài giảm dần);
- thoát ký tự: so với html.escape(quote=True) của thư viện chuẩn; HTL_TXT phân tích bằng ElementTree (là XML đúng cú pháp);
- Java: lớp TrangModel BIÊN DỊCH THẬT bằng javac với tệp jar Apache Sling tải từ Maven Central (audit/bnx/deps/l22, có sha256),
  rồi đọc chú thích bằng phản chiếu; MANIFEST phân tích (dòng nối tiếp); khớp gói/Import-Package/Sling-Model-Packages với mã Java;
- máy trạng thái gói: viết lại theo bảng (trạng thái, sự kiện) khác với mã bài.
KHÔNG kiểm được (NOT_VERIFIED, chỉ theo tài liệu): HTL chạy trong máy chủ, Sling Model nạp thuộc tính thật, bộ mã hoá của HTL thật,
OSGi framework thật. Thiếu jar hoặc javac → SKIP (cổng FAIL)."""
import contextlib
import hashlib
import html
import io
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l22 as src  # noqa: E402

DEPS = ROOT / "audit" / "bnx" / "deps" / "l22"
JARS = {"org.apache.sling.api-3.0.2.jar": "8b8b14abc3f273e35f5622152f83aa20951ed012c266b690d9a1487ab799ebae",
        "org.apache.sling.models.api-2.0.0.jar": "d7bbd7449c5cc2ba58ca055c0d96c67221d6cfe4ca03aa559b29094510b152f8"}

# Bảng ví dụ của Apache Sling “URL decomposition” (đọc 2026-11-12), giả định có tài nguyên /a/b, không có con. 14 hàng không tham số.
DOC_TABLE = """/a/b | /a/b | - | - | - | yes
/a/b.html | /a/b | - | html | - | yes
/a/b.s1.html | /a/b | s1 | html | - | yes
/a/b.s1.s2.html | /a/b | s1.s2 | html | - | yes
/a/b/c/d | /a/b/c/d | - | - | - | no
/a/c.html/s.txt | /a/c | - | html | /s.txt | no
/a/b./c/d | /a/b | - | - | /c/d | yes
/a/b.html/c/d | /a/b | - | html | /c/d | yes
/a/b.s1.html/c/d | /a/b | s1 | html | /c/d | yes
/a/b.s1.s2.html/c/d | /a/b | s1.s2 | html | /c/d | yes
/a/b/c/d.s.txt | /a/b/c/d | s | txt | - | no
/a/b.html/c/d.s.txt | /a/b | - | html | /c/d.s.txt | yes
/a/b.s1.html/c/d.s.txt | /a/b | s1 | html | /c/d.s.txt | yes
/a/b.s1.s2.html/c/d.s.txt | /a/b | s1.s2 | html | /c/d.s.txt | yes"""


def doc_rows():
    rows = []
    for line in DOC_TABLE.split("\n"):
        u, p, s, e, x, f = [c.strip() for c in line.split("|")]
        rows.append((u, p, s.split(".") if s != "-" else [], None if e == "-" else e, None if x == "-" else x, f == "yes"))
    return rows


def run_py(*parts):
    """Chạy NGUYÊN VĂN các đoạn mã (nối lại) trong một không gian tên mới; trả (stdout, không gian tên)."""
    ns = {"__name__": "man_hinh"}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile("\n".join(parts), "<man_hinh>", "exec"), ns)
    return buf.getvalue(), ns


def same(got, want):
    return got.strip("\n") == want.strip("\n")


def split3(url, paths):
    """Hàm tách thứ ba: chọn nút DÀI NHẤT mà url bằng nó hoặc nó cộng một dấu chấm; phần dư tách bằng biểu thức chính quy."""
    best = None
    for p in sorted(paths, key=len, reverse=True):
        if url == p or url.startswith(p + "."):
            best = p
            break
    found = best is not None
    if best is None:
        best = url[:url.index(".")] if "." in url else url
    rest = url[len(best):]
    m = re.match(r"^(?:\.([^/]*))?(/.*)?$", rest)
    mid, suffix = m.group(1), m.group(2)
    parts = mid.split(".") if mid else []
    return best, parts[:-1], (parts[-1] if parts else None), suffix, found


# ── máy trạng thái gói viết lại theo bảng (trạng thái, sự kiện) khác mã bài
OSGI = {("INSTALLED", "resolve"): "RESOLVED", ("RESOLVED", "start"): "STARTING", ("STARTING", "started"): "ACTIVE",
        ("ACTIVE", "stop"): "STOPPING", ("STOPPING", "stopped"): "RESOLVED", ("INSTALLED", "uninstall"): "UNINSTALLED",
        ("RESOLVED", "uninstall"): "UNINSTALLED"}
STATES = ["INSTALLED", "RESOLVED", "STARTING", "ACTIVE", "STOPPING", "UNINSTALLED"]
EVENTS = ["resolve", "start", "started", "stop", "stopped", "uninstall"]


def parse_manifest(text):
    """Đầu mục MANIFEST: dòng bắt đầu bằng một dấu cách nối vào dòng trước (đặc tả JAR)."""
    lines = []
    for l in text.strip("\n").split("\n"):
        if l.startswith(" ") and lines:
            lines[-1] += l[1:]
        else:
            lines.append(l)
    return {k: v.strip() for k, v in (l.split(":", 1) for l in lines)}


def run(rec):
    # ── 1. Chạy nguyên văn các khối Python trên màn hình
    o, ns = run_py(src.KHO_PY, src.KHO_RUN)
    rec("L22", same(o, src.KHO_OUT) and ns["nut"]("/content/site/vi/home.html") is None,
        "khối kho JCR (từ điển lồng nhau) chạy nguyên văn: 2 nút con home, vay; 3 thuộc tính; đường dẫn có phần mở rộng không phải nút → None")
    o, ns = run_py(src.KHO_PY, src.TACH_PY, src.TACH_RUN)
    rec("L22", same(o, src.TACH_OUT), "khối tách đường dẫn chạy nguyên văn với bốn đường dẫn, đầu ra khớp khối trên màn hình")
    o, ns = run_py(src.KHO_PY, src.TACH_PY, src.CHON_PY, src.REQ_RUN)
    rec("L22", same(o, src.REQ_OUT) and ns["kieu"] == src.PG,
        "khối chọn tệp dựng: home.html và vay.html (khác đường dẫn) cùng /apps/site/components/page/page.html; thêm .in.a4 → in.html; khớp màn hình")
    o, _ = run_py(src.CHON_PY, src.CHECK_RUN)
    rec("L22", same(o, src.CHECK_OUT), "gỡ page.html của dự án → /libs; có selector in → vẫn in.html; kiểu lạ → None (khớp khối kiểm)")
    o, ns = run_py(src.KHO_PY, src.THOAT_PY)
    rec("L22", same(o, src.THOAT_OUT), "khối tự thoát ký tự chạy nguyên văn: tiêu đề có <script> thành &lt;script&gt;…, tiêu đề vay giữ nguyên")
    o, ns = run_py(src.GOI_PY, src.GOI_RUN)
    rec("L22", same(o, src.GOI_OUT) and ns["DICH_VU"] == {},
        "khối vòng đời gói chạy nguyên văn: INSTALLED > RESOLVED > STARTING > ACTIVE, sổ có 1 dịch vụ; sau dừng sổ trống; gói thiếu phụ thuộc kẹt INSTALLED")

    # ── 2. Bảng 14 hàng của Apache Sling
    rows = doc_rows()
    rec("L22", len(rows) == 14 == len(src.SLING_ROWS) and [(u, p, s, e, x, f) for u, p, s, e, x, f in rows] == list(src.SLING_ROWS),
        "bảng Apache Sling gõ lại từ tài liệu: đúng 14 hàng và trùng SLING_ROWS của bài (kể cả cột có tài nguyên hay không)")
    _, nsr = run_py(src.KHO_PY, src.TACH_PY)
    nsr["KHO"] = {"a": {"b": {}}}                       # tài nguyên /a/b, không có con; nut() của khối dùng KHO toàn cục
    exist = ["/a", "/a/b"]                              # cả /a cũng là nút (cha của /a/b)
    ok_screen = ok_alg = ok_third = 0
    for u, p, s, e, x, f in rows:
        t = nsr["tach"](u)
        ok_screen += t == (p, s, e, x)
        ok_alg += alg.bnx_l22_split(u, exist) == (p, s, e, x, f)
        ok_third += split3(u, exist) == (p, s, e, x, f)
    rec("L22", ok_screen == ok_alg == ok_third == 14,
        f"14 hàng: hàm tách TRÊN MÀN HÌNH {ok_screen}/14, alg.bnx_l22_split {ok_alg}/14, hàm tách viết khác {ok_third}/14 khớp bảng của tài liệu")
    dots = {u: u.count(".") for u in ("/content/site/vi/home.html", "/content/site/vi/home.in.a4.html")}
    rec("L22", dots["/content/site/vi/home.html"] == 1 and len("/content/site/vi/home.in.a4.html".split("/home")[1].strip(".").split(".")) == 3,
        "ví dụ ①: /content/site/vi/home.html có đúng 1 dấu chấm; home.in.a4.html có 3 khúc sau tên (in, a4, html)")
    # ba URL của bài qua cả ba đường
    repo = {"/content", "/content/site", "/content/site/vi", "/content/site/vi/home", "/content/site/vi/vay"}
    urls = ["/content/site/vi/home.html", "/content/site/vi/home.in.a4.html", "/content/site/vi/home.html/phu/luc",
            "/content/site/vi/khong_co.html", "/content/site/vi/vay.in.a4.html"]
    _, nst = run_py(src.KHO_PY, src.TACH_PY)
    agree = all(nst["tach"](u) == split3(u, repo)[:4] == alg.bnx_l22_split(u)[:4] for u in urls)
    rec("L22", agree, "5 đường dẫn của bài: hàm tách trên màn hình = hàm tách viết khác = alg.bnx_l22_split")

    # ── 3. Chọn tệp dựng, số nút phải đọc
    _, nsc = run_py(src.CHON_PY)
    cases = [(PG := src.PG, [], "html"), (PG, ["in"], "html"), (PG, ["in", "a4"], "html"), (PG, [], "txt"), ("site/components/khac", [], "html")]
    rec("L22", all(nsc["chon_tep"](*c) == alg.bnx_l22_script(*c) for c in cases)
        and alg.bnx_l22_script(PG, ["in", "a4"], "html") == f"/apps/{PG}/in.html" and alg.bnx_l22_script(PG, [], "txt") is None,
        "chon_tep trên màn hình = alg.bnx_l22_script cho 5 ca; selector in.a4 → in.html; .txt không có tệp → None")
    nodes = []
    stack = [("", nst["KHO"])]
    while stack:                                        # duyệt cây KHO, đếm nút (không tính gốc) và nút có kiểu page
        pth, node = stack.pop()
        for k, v in node.items():
            if isinstance(v, dict):
                nodes.append((pth + "/" + k, v))
                stack.append((pth + "/" + k, v))
    hit = sum(1 for _, v in nodes if v.get("sling:resourceType") == src.PG)
    rec("L22", (len(nodes), hit) == (5, 2) == alg.bnx_l22_scan_cost(src.PG)
        and {p for p, _ in nodes} == repo, "kho mẫu có 5 nút, 2 nút kiểu page; không chỉ mục thì phải đọc cả 5 để ra 2 (duyệt cây khác alg)")

    # ── 4. Thoát ký tự
    title = src.TITLE
    esc = html.escape(title, quote=True)
    rec("L22", len(title) == 34 and sum(c in '&<>"' for c in title) == 4 and len(esc) == 46 == 34 + 4 * 3
        and esc == alg.bnx_l22_escape(title) and esc == src.TITLE_H and html.unescape(src.TITLE_E) == esc,
        "tiêu đề dài 34, 4 ký tự đặc biệt, thoát thành 46 = 34 + 4·3 (html.escape của thư viện chuẩn cho cùng chuỗi); chuỗi hiện trên màn hình khớp")
    _, nsz = run_py(src.KHO_PY, src.THOAT_PY)
    samples = ["<b>", "a&b", 'say "hi"', "&lt;", "Vay tiêu dùng", "<<>>", ""]
    rec("L22", all(nsz["thoat"](s) == html.escape(s, quote=True) == alg.bnx_l22_escape(s) for s in samples)
        and len(html.escape("<b>", quote=True)) == 9 == 3 + 2 * 3 and nsz["thoat"]("&lt;") == "&amp;lt;",
        "hàm thoat trên màn hình = html.escape = alg cho 7 chuỗi; '<b>' → 9 ký tự = 3 + 2·3; '&lt;' không bị bỏ sót (thành &amp;lt;)")

    # ── 5. HTL phân tích được (cú pháp XML) và khớp với mã Java
    root = ET.fromstring(src.HTL_TXT)
    use = root.attrib.get("data-sly-use.trang")
    h1, a, ul = root.find("h1"), root.find("a"), root.find("ul")
    rec("L22", root.tag == "div" and use == "com.vidu.site.TrangModel" and h1.text == "${trang.tieuDe}"
        and a.attrib["href"] == "${properties.lienKet}" and ul.attrib["data-sly-list"] == "${properties.mucCon}"
        and ul.find("li").text == "${item}", "HTL_TXT là XML đúng cú pháp: data-sly-use.trang, ${trang.tieuDe}, href, data-sly-list, ${item}")
    jt = src.MODEL_JAVA
    pkg = re.search(r"^package ([\w.]+);", jt, re.M).group(1)
    cls = re.search(r"public class (\w+)", jt).group(1)
    getter = "get" + "tieuDe"[0].upper() + "tieuDe"[1:]            # HTL: ${trang.tieuDe} → getter getTieuDe (đặc tả HTL 4.3)
    rec("L22", f"{pkg}.{cls}" == use and f"String {getter}()" in jt and "@ValueMapValue" in jt and "@Model(adaptables=Resource.class)" in jt,
        f"HTL gọi {use}: khớp gói {pkg} + lớp {cls}; biểu thức trang.tieuDe ↔ getter {getter}() có trong lớp")
    # mô hình đọc thuộc tính tên gì? phải là thuộc tính CÓ trong nút mẫu (không để mô hình đọc "tieuDe" khi nút chỉ có jcr:title)
    prop = re.search(r'@ValueMapValue\(name = "([^"]+)"\)', jt)
    home = alg.bnx_l22_props("/content/site/vi/home")
    rec("L22", prop is not None and prop.group(1) in home and "jcr:title" in src.KHO_PY and prop.group(1) == "jcr:title",
        f"@ValueMapValue đọc thuộc tính {prop.group(1) if prop else None!r}: có trong nút mẫu home ({sorted(home)}); cùng thuộc tính mà mô phỏng HTL dùng")
    mf = parse_manifest(src.MANIFEST)
    imports = sorted(re.findall(r"^import ([\w.]+)\.(?:\w+|\*);", jt, re.M))
    imp_hdr = sorted(x.strip() for x in mf["Import-Package"].split(","))
    rec("L22", mf["Bundle-ManifestVersion"] == "2" and mf["Bundle-SymbolicName"] == "com.vidu.site.core"
        and re.fullmatch(r"\d+\.\d+\.\d+", mf["Bundle-Version"]) and mf["Sling-Model-Packages"] == pkg and imp_hdr == imports,
        f"MANIFEST: ManifestVersion 2, tên có, phiên bản dạng a.b.c, Sling-Model-Packages = {pkg}, Import-Package = đúng {len(imports)} gói Java nhập")

    # ── 6. Máy trạng thái gói
    def trace(needs, avail):
        st, tr = "INSTALLED", ["INSTALLED"]
        if any(n not in avail for n in needs):
            return tr
        for ev in ("resolve", "start", "started"):
            st = OSGI[(st, ev)]
            tr.append(st)
        return tr
    good = trace(["org.apache.sling.api"], {"org.apache.sling.api"})
    rec("L22", good == ["INSTALLED", "RESOLVED", "STARTING", "ACTIVE"] == alg.bnx_l22_bundle_trace(["org.apache.sling.api"], {"org.apache.sling.api"})
        and trace(["com.vidu.thieu"], {"org.apache.sling.api"}) == ["INSTALLED"] == alg.bnx_l22_bundle_trace(["com.vidu.thieu"], set()),
        "gói đủ phụ thuộc: INSTALLED→RESOLVED→STARTING→ACTIVE; thiếu → kẹt INSTALLED (máy trạng thái viết theo bảng, khớp alg)")
    mism = [(s, e) for s in STATES for e in EVENTS if OSGI.get((s, e)) != alg.bnx_l22_bundle_step(s, e)]
    rec("L22", not mism and all(OSGI.get(("UNINSTALLED", e)) is None for e in EVENTS) and len(STATES) == 6,
        f"36 cặp (6 trạng thái × 6 sự kiện): bảng độc lập khớp alg ({len(mism)} lệch); UNINSTALLED không đi đâu được nữa; có 6 trạng thái")
    st = "INSTALLED"
    for ev in ("resolve", "start", "started", "stop", "stopped"):
        st = OSGI[(st, ev)]
    rec("L22", st == "RESOLVED" and [s for s in STATES if alg.bnx_l22_serves(s)] == ["ACTIVE"]
        and alg.bnx_l22_bundle_trace([], set()) == ["INSTALLED", "RESOLVED", "STARTING", "ACTIVE"],
        "start rồi stop về RESOLVED; chỉ ACTIVE cung cấp dịch vụ (quy tắc của bài, suy từ tài liệu OSGi: xem sources_l22.md)")

    # ── 7. Java thật: biên dịch TrangModel với jar Apache Sling, đọc chú thích
    missing = [n for n in JARS if not (DEPS / n).exists()]
    if missing or not (shutil.which("javac") and shutil.which("java")):
        rec("L22", None, f"thiếu javac/java hoặc jar {missing} (NOT_VERIFIED: lớp Sling Model chưa biên dịch)")
    else:
        bad = [n for n, h in JARS.items() if hashlib.sha256((DEPS / n).read_bytes()).hexdigest() != h]
        rec("L22", not bad, f"sha256 của {len(JARS)} tệp jar ở audit/bnx/deps/l22 khớp README ({'đúng' if not bad else bad})")
        cp = str(DEPS / "*")
        probe = """import java.util.*;
import org.apache.sling.models.annotations.Model;
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;
public class Probe {
  public static void main(String[] a) throws Exception {
    Class<?> c = Class.forName("com.vidu.site.TrangModel");
    Model m = c.getAnnotation(Model.class);
    System.out.println(Arrays.toString(m.adaptables()));
    System.out.println(c.getDeclaredField("tieuDe").isAnnotationPresent(ValueMapValue.class));
    System.out.println(c.getMethod("getTieuDe").getReturnType().getSimpleName());
  }
}
"""
        with tempfile.TemporaryDirectory() as d:
            Path(d, "TrangModel.java").write_text(src.MODEL_JAVA.strip("\n") + "\n", encoding="utf-8")
            Path(d, "Probe.java").write_text(probe, encoding="utf-8")
            r = subprocess.run(["javac", "-encoding", "UTF-8", "-proc:none", "-cp", cp, "-d", d + "/out", "TrangModel.java", "Probe.java"],
                               cwd=d, capture_output=True, text=True, encoding="utf-8")
            ok_c = r.returncode == 0 and Path(d, "out", "com", "vidu", "site", "TrangModel.class").exists()
            rec("L22", ok_c, "TrangModel.java (nguyên văn khối Bước 5) biên dịch bằng javac với org.apache.sling.api 3.0.2 và models.api 2.0.0"
                + ("" if ok_c else ": " + r.stderr[:200]))
            if ok_c:
                r = subprocess.run(["java", "-cp", d + "/out" + ";" + cp if sys.platform == "win32" else d + "/out:" + cp, "Probe"],
                                   capture_output=True, text=True, encoding="utf-8", timeout=120)
                lines = r.stdout.replace("\r\n", "\n").strip().split("\n")
                rec("L22", r.returncode == 0 and lines == ["[interface org.apache.sling.api.resource.Resource]", "true", "String"],
                    f"phản chiếu: @Model(adaptables=Resource.class), trường tieuDe có @ValueMapValue, getTieuDe() trả String ({lines})")
    # ── 8. Mã trên màn hình: ≤ 12 dòng, dòng ≤ 70 ký tự
    consts = [src.KHO_PY, src.KHO_RUN, src.KHO_OUT, src.TACH_PY, src.TACH_RUN, src.TACH_OUT, src.CHON_PY, src.REQ_RUN, src.REQ_OUT,
              src.CHECK_RUN, src.CHECK_OUT, src.HTL_TXT, src.THOAT_PY, src.THOAT_OUT, src.MODEL_JAVA, src.MANIFEST, src.GOI_PY,
              src.GOI_RUN, src.GOI_OUT]
    ls = [len(c.strip("\n").split("\n")) for c in consts]
    wid = max(len(l) for c in consts for l in c.strip("\n").split("\n"))
    rec("L22", max(ls) <= 12 and wid <= 70, f"khối mã dài nhất {max(ls)} dòng (≤ 12), dòng rộng nhất {wid} ký tự (≤ 70)")
