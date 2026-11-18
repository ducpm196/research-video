import lib2
from lib2 import *
from spoken_b import _spoken
from libj import jstep, nowrap
from labkit import write_lab, practice_scene

lib2.begin("L22")

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN ở audit/bnx/ver/l22.py và cổng screen_code).
#    Máy không có máy chủ AEM: các khối Python là MÔ PHỎNG theo tài liệu (audit/bnx/sources_l22.md), ghi rõ trên màn hình.
KHO_PY = """KHO = {"content": {"site": {"vi": {
    "home": {"jcr:primaryType": "nt:unstructured",
             "sling:resourceType": "site/components/page",
             "jcr:title": "Xin chào <script>alert(1)</script>"},
    "vay": {"jcr:primaryType": "nt:unstructured",
            "sling:resourceType": "site/components/page",
            "jcr:title": "Vay tiêu dùng"}}}}}
def nut(duong_dan):
    n = KHO
    for ten in duong_dan.strip("/").split("/"):
        n = n.get(ten) if isinstance(n, dict) else None
    return n if isinstance(n, dict) else None"""
KHO_RUN = """vi = nut("/content/site/vi")
print("nút con:", [k for k in vi if type(vi[k]) is dict])
print("thuộc tính:", sorted(nut("/content/site/vi/home")))
print(nut("/content/site/vi/home.html"))"""
KHO_OUT = """nút con: ['home', 'vay']
thuộc tính: ['jcr:primaryType', 'jcr:title', 'sling:resourceType']
None"""

TACH_PY = """def tach(url):
    cat = [i for i, c in enumerate(url) if c == "."] + [len(url)]
    co = [i for i in cat if nut(url[:i]) is not None]
    i = max(co) if co else cat[0]
    giua, gach, hau_to = url[i + 1:].partition("/")
    phan = giua.split(".") if giua else [None]
    return url[:i], phan[:-1], phan[-1], (gach + hau_to) or None"""
TACH_RUN = """for url in ["/content/site/vi/home.html",
            "/content/site/vi/home.in.a4.html",
            "/content/site/vi/home.html/phu/luc",
            "/content/site/vi/khong_co.html"]:
    print(tach(url))"""
TACH_OUT = """('/content/site/vi/home', [], 'html', None)
('/content/site/vi/home', ['in', 'a4'], 'html', None)
('/content/site/vi/home', [], 'html', '/phu/luc')
('/content/site/vi/khong_co', [], 'html', None)"""

CHON_PY = """MA_DUNG = ["/apps/site/components/page/page.html",
           "/apps/site/components/page/in.html",
           "/libs/site/components/page/page.html"]
def chon_tep(kieu, chon, mo_rong):
    duoi = ("" if mo_rong == "html" else "." + mo_rong) + ".html"
    ten = ["/".join(chon[:k]) for k in range(len(chon), 0, -1)]
    ten.append(kieu.split("/")[-1])
    for t in ten:
        for goc in ("/apps/", "/libs/"):
            tep = goc + kieu + "/" + t + duoi
            if tep in MA_DUNG:
                return tep"""
REQ_RUN = """for url in ["/content/site/vi/home.html", "/content/site/vi/vay.html",
            "/content/site/vi/home.in.a4.html"]:
    duong, chon, mo_rong, hau_to = tach(url)
    kieu = nut(duong)["sling:resourceType"]
    print(url.split("/")[-1], "->", chon_tep(kieu, chon, mo_rong))
print("kiểu:", kieu)"""
REQ_OUT = """home.html -> /apps/site/components/page/page.html
vay.html -> /apps/site/components/page/page.html
home.in.a4.html -> /apps/site/components/page/in.html
kiểu: site/components/page"""
CHECK_RUN = """MA_DUNG.remove("/apps/site/components/page/page.html")
print(chon_tep("site/components/page", [], "html"))
print(chon_tep("site/components/page", ["in"], "html"))
print(chon_tep("site/components/khac", [], "html"))"""
CHECK_OUT = """/libs/site/components/page/page.html
/apps/site/components/page/in.html
None"""

HTL_TXT = """<div data-sly-use.trang="com.vidu.site.TrangModel">
  <h1>${trang.tieuDe}</h1>
  <a href="${properties.lienKet}">Xem tiếp</a>
  <ul data-sly-list="${properties.mucCon}">
    <li>${item}</li>
  </ul>
</div>"""
THOAT_PY = r"""import re
MA = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}
def thoat(s):
    return "".join(MA.get(c, c) for c in s)
def dung(mau, thuoc_tinh):
    return re.sub(r"\$\{properties\.([\w:]+)\}",
                  lambda m: thoat(thuoc_tinh[m.group(1)]), mau)
mau = "<h1>${properties.jcr:title}</h1>"
print(dung(mau, nut("/content/site/vi/home")))
print(dung(mau, nut("/content/site/vi/vay")))"""
THOAT_OUT = """<h1>Xin chào &lt;script&gt;alert(1)&lt;/script&gt;</h1>
<h1>Vay tiêu dùng</h1>"""

MODEL_JAVA = """package com.vidu.site;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.annotations.Model;
import org.apache.sling.models.annotations.injectorspecific.*;
@Model(adaptables=Resource.class)
public class TrangModel {
    @ValueMapValue(name = "jcr:title")
    private String tieuDe;
    public String getTieuDe() { return tieuDe; }
}"""
MANIFEST = """Bundle-ManifestVersion: 2
Bundle-SymbolicName: com.vidu.site.core
Bundle-Version: 1.0.0
Import-Package: org.apache.sling.api.resource,
 org.apache.sling.models.annotations,
 org.apache.sling.models.annotations.injectorspecific
Sling-Model-Packages: com.vidu.site"""

GOI_PY = """DICH_VU = {}
class Goi:
    def __init__(self, ten, can, cap):
        self.ten, self.can, self.cap = ten, can, cap
        self.vet = ["INSTALLED"]
    def start(self, co_san):
        thieu = [p for p in self.can if p not in co_san]
        if thieu:
            raise RuntimeError(f"không phân giải được, thiếu {thieu}")
        self.vet += ["RESOLVED", "STARTING", "ACTIVE"]
        DICH_VU[self.cap] = self.ten"""
GOI_RUN = """g = Goi("site.core", ["org.apache.sling.api"], "TieuDe")
g.start({"org.apache.sling.api"})
print(" > ".join(g.vet), "|", DICH_VU)
g.vet += ["STOPPING", "RESOLVED"]
DICH_VU.pop(g.cap)
print(g.vet[-2:], "|", DICH_VU)
h = Goi("site.loi", ["com.vidu.thieu"], "X")
try:
    h.start({"org.apache.sling.api"})
except RuntimeError as loi:
    print(h.vet, loi)"""
GOI_OUT = """INSTALLED > RESOLVED > STARTING > ACTIVE | {'TieuDe': 'site.core'}
['STOPPING', 'RESOLVED'] | {}
['INSTALLED'] không phân giải được, thiếu ['com.vidu.thieu']"""

NOTE_SIM = "<span class='note'>(mô phỏng theo đặc tả công khai, không phải máy chủ AEM)</span>"
SIM = "mô phỏng theo đặc tả công khai, không phải máy chủ AEM"
SIM_T = "mô phỏng, không phải máy chủ AEM"        # bản ngắn cho tiêu đề khối mã (một dòng)
D = "<span>&#36;</span>"            # dấu đô la ngoài khối mã (tránh KaTeX coi là mở công thức)
# mẫu regex hiện trong bảng "viết trong mã" (chuỗi thô; dấu đô la viết bằng thực thể HTML để KaTeX không coi là công thức)
PAT_ROW = r'<code>r"\&#36;\{properties\.([\w:]+)\}"</code>'
PAT_TXT = r"<code>&#36;{properties.TÊN}</code>"
PAT_GRP = r"<code>([\w:]+)</code>"
TITLE = "Xin chào <script>alert(1)</script>"
TITLE_H = "Xin chào &lt;script&gt;alert(1)&lt;/script&gt;"                    # hiện tiêu đề thô trên màn hình
TITLE_E = "Xin chào &amp;lt;script&amp;gt;alert(1)&amp;lt;/script&amp;gt;"    # hiện tiêu đề ĐÃ thoát trên màn hình
PG = "site/components/page"
# 14 hàng không có tham số đường dẫn của bảng ví dụ trong tài liệu Apache Sling “URL decomposition” (giả định: có tài nguyên /a/b, không có con)
SLING_ROWS = [("/a/b", "/a/b", [], None, None, True), ("/a/b.html", "/a/b", [], "html", None, True),
              ("/a/b.s1.html", "/a/b", ["s1"], "html", None, True), ("/a/b.s1.s2.html", "/a/b", ["s1", "s2"], "html", None, True),
              ("/a/b/c/d", "/a/b/c/d", [], None, None, False), ("/a/c.html/s.txt", "/a/c", [], "html", "/s.txt", False),
              ("/a/b./c/d", "/a/b", [], None, "/c/d", True), ("/a/b.html/c/d", "/a/b", [], "html", "/c/d", True),
              ("/a/b.s1.html/c/d", "/a/b", ["s1"], "html", "/c/d", True), ("/a/b.s1.s2.html/c/d", "/a/b", ["s1", "s2"], "html", "/c/d", True),
              ("/a/b/c/d.s.txt", "/a/b/c/d", ["s"], "txt", None, False), ("/a/b.html/c/d.s.txt", "/a/b", [], "html", "/c/d.s.txt", True),
              ("/a/b.s1.html/c/d.s.txt", "/a/b", ["s1"], "html", "/c/d.s.txt", True),
              ("/a/b.s1.s2.html/c/d.s.txt", "/a/b", ["s1", "s2"], "html", "/c/d.s.txt", True)]



# ── AF2 (nhánh B): cảnh quy mô + lab. Chương trình chạy THẬT lúc import (đệm ở audit/bnx/progcache/L22.json); vẫn là MÔ PHỎNG kho, không phải máy chủ AEM ──
QUYMO = prog("QuyMo", r'''
PAGE = "site/components/page"
def lap_kho(n):
    vi = {}
    for i in range(n):
        loai = PAGE if i % 100 == 0 else "site/components/tin"
        vi[f"t{i}"] = {"sling:resourceType": loai}
    return {"content": {"site": {"vi": vi}}}
def duyet(nut):
    thay, khop = 1, 0
    for k, v in nut.items():
        if isinstance(v, dict):
            t, c = duyet(v)
            thay, khop = thay + t, khop + c
        elif k == "sling:resourceType" and v == PAGE:
            khop += 1
    return thay, khop
for n in (10, 1_000, 100_000):
    kho = lap_kho(n)
    chi_muc = {}
    for ten, nut in kho["content"]["site"]["vi"].items():
        chi_muc.setdefault(nut["sling:resourceType"], []).append(ten)
    thay, khop = duyet(kho)
    print(n, "trang: duyet", thay, "nut, khop", khop, "| chi muc doc", len(chi_muc[PAGE]), "nut")
''', lang="python", claims=["tìm nút theo thuộc tính không chỉ mục: duyệt n + 4 nút (14; 1 004; 100 004), khớp 1 trên 100; có chỉ mục chỉ đọc đúng số nút khớp (1; 10; 1 000)"])

LAB_PY = r'''
KHO = {"content": {"bank": {"en": {
    "the": {"sling:resourceType": "bank/components/card"},
    "vay": {"sling:resourceType": "bank/components/loan"}}}}}
TEP = ["/apps/bank/components/card/card.html",
       "/apps/bank/components/card/print.html",
       "/libs/bank/components/loan/loan.html"]
def nut(duong):
    n = KHO
    for ten in duong.strip("/").split("/"):
        n = n.get(ten) if isinstance(n, dict) else None
    return n
def xu_ly(url):
    duong, _, phan = url.partition(".")
    khuc = phan.split(".")
    chon = khuc[0] if len(khuc) > 1 else None
    n = nut(duong)
    if n is None:
        return "KHONG CO TAI NGUYEN"
    kieu = n["sling:resourceType"]
    for ten in ([chon] if chon else []) + [kieu.split("/")[-1]]:
        for goc in ("/apps/", "/libs/"):
            tep = goc + kieu + "/" + ten + ".html"
            if tep in TEP:
                return tep
    return "KHONG CO TEP DUNG"
for url in ["/content/bank/en/the.html", "/content/bank/en/the.print.html",
            "/content/bank/en/vay.html", "/content/bank/en/vay.print.html",
            "/content/bank/en/thieu.html"]:
    print(url.split("/")[-1], "->", xu_ly(url))
'''
LAB = prog("LabL22", LAB_PY, lang="python", kind="run")
LAB_DE = """# Lab BNX L22 — Từ đường dẫn tới tệp dựng (mô phỏng, không cần máy chủ AEM)

Máy bạn không có máy chủ AEM, nên ta mô phỏng bằng Python (số liệu và tên là số minh hoạ, khác ví dụ trong bài). Kho nội dung và danh sách tệp dựng cho sẵn:

```python
KHO = {"content": {"bank": {"en": {
    "the": {"sling:resourceType": "bank/components/card"},
    "vay": {"sling:resourceType": "bank/components/loan"}}}}}
TEP = ["/apps/bank/components/card/card.html",
       "/apps/bank/components/card/print.html",
       "/libs/bank/components/loan/loan.html"]
```

Viết `mau.py` (chép hai khai báo trên vào đầu tệp, rồi viết tiếp). Với mỗi địa chỉ trong danh sách bên dưới:

1. Tách địa chỉ tại dấu chấm đầu tiên: phần trước là đường dẫn tài nguyên (tên nút không có dấu chấm); phần sau chia theo dấu chấm, khúc cuối là phần mở rộng, khúc trước (nếu có) là **bộ chọn** (chỉ có tối đa một).
2. Đi từ gốc `KHO` xuống theo từng tên của đường dẫn để tìm nút. Không có nút thì kết quả là `KHONG CO TAI NGUYEN`.
3. Đọc `sling:resourceType` của nút. Tên ứng viên: bộ chọn (nếu có) rồi tới khúc cuối của kiểu tài nguyên. Với mỗi tên, thử `/apps/<kiểu>/<tên>.html` rồi `/libs/<kiểu>/<tên>.html`; tệp đầu tiên nằm trong `TEP` thì chọn. Không có tệp nào thì kết quả là `KHONG CO TEP DUNG`.

Địa chỉ: `/content/bank/en/the.html`, `/content/bank/en/the.print.html`, `/content/bank/en/vay.html`, `/content/bank/en/vay.print.html`, `/content/bank/en/thieu.html`.

In mỗi địa chỉ một dòng dạng `<tên cuối của địa chỉ> -> <kết quả>`, ví dụ `the.html -> /apps/...`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L22 mau.py`.
"""

def build():
    write_lab("BNX", "L22", LAB_DE, "py", LAB_PY, LAB.out)
    hook = sc("hook", "hook", "9 giờ sáng, biên tập viên sửa tiêu đề trang vay: không ai triển khai lại mã", [
        st(f"""<p>Trang web giới thiệu sản phẩm của một ngân hàng chạy trên <b>Adobe Experience Manager (AEM)</b>, một hệ quản trị nội dung. 9 giờ sáng, biên tập viên sửa tiêu đề trang chủ. Trang đổi ngay trên máy soạn (author), dù <b>không ai triển khai lại mã</b> và trên đĩa có <b>0</b> tệp HTML của trang đó; khách chỉ thấy sau khi nội dung được đăng (publish) sang máy đăng.</p>
<div class="box key">Lỡ tay, người đó gõ vào tiêu đề chuỗi <code>{TITLE_H}</code>. Trình duyệt của khách có chạy đoạn mã lạ đó không? Và <b>2</b> trang khác nhau làm sao dùng chung <b>1</b> tệp dựng? Khi kho có hàng trăm nghìn trang, việc tìm nào sẽ chậm trước?</div>
{NOTE_SIM}""",
           """Chào bạn, trang web giới thiệu sản phẩm của một ngân hàng chạy trên một hệ quản trị nội dung. Chín giờ sáng, biên tập viên sửa tiêu đề trang chủ và trang đổi ngay, dù không ai triển khai lại mã. Lỡ tay, người đó gõ vào tiêu đề một đoạn mã lạ, vậy trình duyệt của khách có chạy nó không? Hai trang khác nhau dùng chung một tệp dựng bằng cách nào, và khi kho lớn thì việc tìm nào chậm trước? Bài này chỉ là mô phỏng.""",
           focus=[1, 2, 2, 2, 3, 3], introduces=["bnx_aem"]),
    ], checks=[f"alg.bnx_l22_resolve('/content/site/vi/home.html')[2] == alg.bnx_l22_resolve('/content/site/vi/vay.html')[2] == '/apps/{PG}/page.html'",
               "len({alg.bnx_l22_resolve(u)[2] for u in ('/content/site/vi/home.html', '/content/site/vi/vay.html')}) == 1",
               f"alg.bnx_l22_props('/content/site/vi/home')['jcr:title'] == {TITLE!r}"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Cây", "mỗi nút có một nút cha và có thể có nhiều nút con; đi từ gốc xuống theo tên", "thư mục trên máy: ổ đĩa → thư mục → thư mục con"],
                  ["② Đường dẫn và phần mở rộng", "dãy tên nối bằng dấu gạch chéo; phần sau dấu chấm cuối cho biết dạng muốn nhận", "/content/site/vi/home.html: 4 cấp, phần mở rộng html"],
                  ["③ Ký tự đặc biệt của HTML", "dấu &lt; mở một thẻ; muốn hiện nó như chữ thường phải viết thành &amp;lt;", "&lt;b&gt; có 3 ký tự, 2 ký tự đặc biệt; thoát xong dài 3 + 2 × 3 = 9 ký tự"],
                  ["④ Máy trạng thái", "một vật chỉ ở một trạng thái tại một lúc, và chỉ đi theo các bước cho phép", "đèn giao thông: xanh → vàng → đỏ"]]),
           """Trước hết ta cần hiểu bốn điều. Cây là cấu trúc mà mỗi nút có một nút cha và nhiều nút con, giống thư mục trên máy. Đường dẫn là dãy tên nối bằng dấu gạch chéo, phần sau dấu chấm cuối là phần mở rộng. Dấu nhỏ hơn mở một thẻ, nên muốn hiện nó như chữ thường thì phải viết thành một mã bốn ký tự. Máy trạng thái chỉ ở một trạng thái tại một lúc và chỉ đi theo các bước cho phép.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
    ], checks=["alg.bnx_l22_depth('/content/site/vi/home') == 4",
               "alg.bnx_l22_escape('<b>') == '&lt;b&gt;' and alg.bnx_l22_escaped_count('<b>') == 2",
               "len(alg.bnx_l22_escape('<b>')) == 3 + 2 * 3 == 9",
               "alg.bnx_l22_bundle_step('INSTALLED', 'start') is None"])

    sym = sc("sym", "symbol", "Giải mã từ ngữ và sáu trạng thái của gói", [
        st(table(["từ", "nghĩa"],
                 [["JCR (Java Content Repository)", "kho nội dung dạng cây. Mỗi mục là <b>nút</b> hoặc <b>thuộc tính</b>; nội dung thật nằm trong giá trị của thuộc tính"],
                  ["jcr:primaryType", "thuộc tính bắt buộc, giữ tên kiểu nút chính; <code>nt:unstructured</code> cho phép nút con và thuộc tính tên bất kỳ"],
                  ["Sling, tài nguyên (resource)", "tầng nhận yêu cầu web: đổi đường dẫn thành một tài nguyên trong kho"],
                  ["sling:resourceType", "thuộc tính ghi <b>kiểu tài nguyên</b>; Sling dùng nó để tìm tệp dựng (script). AEM thật: nút trang có kiểu <code>cq:Page</code>, và thuộc tính này nằm ở nút con <code>jcr:content</code> giữ nội dung của trang; bài gộp hai nút cho gọn"]]),
           """Bảng này giải mã các từ của bài. Một là kho nội dung dạng cây gồm nút và thuộc tính. Hai là tầng nhận yêu cầu web, đổi đường dẫn thành tài nguyên rồi dùng kiểu tài nguyên để tìm tệp dựng.""",
           focus=[0, ["1.2", "1.3"], ["1.4", "1.5"]],
           introduces=["bnx_jcr", "bnx_sling"]),
        st(table(["từ", "nghĩa"],
                 [["selector, extension", "các khúc giữa tên tài nguyên và phần mở rộng (home<b>.in.a4</b>.html); phần mở rộng là khúc cuối"],
                  ["HTL (HTML Template Language)", f"ngôn ngữ khuôn mẫu: biểu thức <code>{D}{{…}}</code> và các thuộc tính <code>data-sly-*</code>"],
                  ["OSGi, bundle, service", "khung mô-đun của Java: mã đóng thành <b>gói</b> (bundle) có vòng đời; gói đăng ký <b>dịch vụ</b> cho gói khác dùng"]]),
           """Ba là ngôn ngữ khuôn mẫu viết tệp dựng, và bộ chọn là các khúc nằm giữa tên tài nguyên và phần mở rộng. Bốn là khung mô-đun của Java, đóng mã thành gói có vòng đời, và gói đăng ký dịch vụ cho gói khác dùng.""",
           focus=["1.2", "1.3", "1.4"], clear=True,
           introduces=["bnx_htl", "bnx_osgi"]),
        st(table(["trạng thái của gói (bundle)", "nghĩa theo đặc tả OSGi Core 8"],
                 [["INSTALLED", "gói đã được cài thành công"],
                  ["RESOLVED", "mọi lớp Java gói cần đều có; gói sẵn sàng được khởi động, hoặc vừa dừng"],
                  ["STARTING", "gói đang được khởi động"],
                  ["ACTIVE", "gói đã kích hoạt xong và đang chạy"],
                  ["STOPPING", "gói đang được dừng"],
                  ["UNINSTALLED", "gói đã bị gỡ; không chuyển sang trạng thái nào khác được nữa"]]),
           """Một gói có sáu trạng thái: đã cài, đã phân giải, đang khởi động, đang chạy, đang dừng và đã gỡ. Đã phân giải nghĩa là mọi lớp Java gói cần đều có. Đã gỡ là trạng thái cuối.""",
           clear=True),
    ], checks=["alg.bnx_l22_props('/content/site/vi/home')['jcr:primaryType'] == 'nt:unstructured'",
               "alg.bnx_l22_split('/content/site/vi/home.in.a4.html')[1:3] == (['in', 'a4'], 'html')",
               "len({s for s in ('INSTALLED', 'RESOLVED', 'STARTING', 'ACTIVE', 'STOPPING', 'UNINSTALLED') if alg.bnx_l22_bundle_step(s, 'x') is None}) == 6",
               "all(alg.bnx_l22_bundle_step('UNINSTALLED', e) is None for e in ('resolve', 'start', 'started', 'stop', 'stopped', 'uninstall'))"])

    intu = sc("intuition", "intuition", "Hình dung: đường đi của một yêu cầu, và vòng đời của một gói", [
        st(svg(1500, 500,
               panel(20, 20, 520, 400, "Kho nội dung (JCR): cây nút", C_BLUE),
               box(200, 80, 160, 46, "content", C_GRAY, size=20, bold=True),
               box(200, 146, 160, 46, "site", C_GRAY, size=20, bold=True),
               box(200, 212, 160, 46, "vi", C_GRAY, size=20, bold=True),
               box(50, 290, 215, 110, ["home", "sling:resourceType =", PG], C_AMBER, size=17, bold=True),
               box(295, 290, 215, 110, ["vay", "sling:resourceType =", PG], C_AMBER, size=17, bold=True),
               arrow(280, 126, 280, 143), arrow(280, 192, 280, 209), arrow(250, 258, 180, 286), arrow(310, 258, 385, 286),
               panel(590, 20, 890, 400, "Sling: từ đường dẫn tới trang", C_GREEN),
               box(615, 80, 400, 56, "/content/site/vi/home.html", C_GRAY, size=21, bold=True),
               box(615, 180, 400, 80, ["① tách: tài nguyên /content/site/vi/home", "phần mở rộng html"], C_BLUE, size=19),
               box(615, 310, 400, 80, ["② đọc thuộc tính của nút home", "sling:resourceType"], C_AMBER, size=19),
               arrow(815, 136, 815, 176), arrow(815, 260, 815, 306),
               box(1070, 180, 390, 80, ["③ chọn tệp dựng theo KIỂU", f"/apps/{PG}/page.html"], C_PURPLE, size=17, bold=True),
               box(1070, 310, 390, 80, ["④ tệp HTL đọc thuộc tính,", "tự thoát ký tự, trả trang về"], C_GREEN, size=19),
               arrow(1015, 350, 1040, 350), arrow(1040, 350, 1040, 220, dash=True), arrow(1040, 220, 1066, 220), arrow(1265, 260, 1265, 306),
               arrow(540, 340, 611, 345, "#d97706"),
               txt(750, 470, "Trang là dữ liệu trong kho; mã dựng được chọn theo kiểu tài nguyên, không theo đường dẫn", 24, "middle", "#1f2937", True)),
           """Hình này là đường đi của một yêu cầu. Bên trái là kho nội dung, hai nút trang mang cùng một kiểu tài nguyên. Bên phải, tầng nhận yêu cầu tách đường dẫn, đọc kiểu của nút rồi chọn tệp dựng theo kiểu đó, nên mã dựng chọn theo kiểu, không theo đường dẫn."""),
        st(svg(1500, 500,
               panel(20, 20, 1000, 400, "Vòng đời của một gói OSGi (bundle)", C_BLUE),
               box(50, 110, 190, 80, ["INSTALLED", "đã cài"], C_GRAY, size=20, bold=True),
               box(300, 110, 190, 80, ["RESOLVED", "đã phân giải"], C_AMBER, size=20, bold=True),
               box(550, 110, 190, 80, ["STARTING", "đang khởi động"], C_GRAY, size=20, bold=True),
               box(800, 110, 190, 80, ["ACTIVE", "đang chạy"], C_GREEN, size=20, bold=True),
               arrow(240, 150, 296, 150), arrow(490, 150, 546, 150), arrow(740, 150, 796, 150),
               txt(270, 100, "đủ gói", 18, "middle", "#475569"), txt(520, 100, "start", 18, "middle", "#475569"),
               box(550, 290, 190, 80, ["STOPPING", "đang dừng"], C_GRAY, size=20, bold=True),
               arrow(895, 190, 745, 325), arrow(546, 325, 420, 194),
               txt(880, 280, "stop", 18, "middle", "#475569"),
               box(50, 290, 190, 80, ["UNINSTALLED", "đã gỡ"], C_RED, size=20, bold=True),
               arrow(145, 190, 145, 286), arrow(330, 190, 235, 290),
               txt(130, 245, "gỡ", 18, "end", "#475569"), txt(300, 255, "gỡ", 18, "start", "#475569"),
               txt(260, 405, "thiếu gói phụ thuộc: start báo lỗi, gói kẹt ở INSTALLED", 19, "start", "#dc2626", True),
               panel(1070, 20, 410, 400, "Sổ đăng ký dịch vụ", C_GREEN),
               box(1100, 110, 350, 80, ["gói ACTIVE đăng ký", "dịch vụ"], C_GREEN, size=20, bold=True),
               box(1100, 240, 350, 110, ["gói dừng: dịch vụ của nó", "tự động bị gỡ khỏi sổ"], C_RED, size=20),
               arrow(990, 150, 1096, 150, "#16a34a"),
               txt(750, 470, "RESOLVED là đủ điều kiện chạy, chưa phải đang chạy; chỉ ACTIVE mới cung cấp dịch vụ", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là vòng đời của một gói. Đủ gói phụ thuộc thì gói sang đã phân giải, lệnh khởi động đưa nó tới đang chạy và gói mới đăng ký dịch vụ, còn lệnh dừng đưa gói về đã phân giải."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: kho, đường dẫn, tệp dựng, khuôn mẫu, gói", [
        st(table(["viết trong mã Python", "nghĩa"],
                 [["<code>n.get(ten)</code>, <code>isinstance(n, dict)</code>, <code>type(n) is dict</code>", "lấy giá trị theo khoá, không có thì rỗng; kiểm n có phải một bảng tra không (hai cách viết cùng ý)"],
                  ["<code>s.partition(\"/\")</code>, <code>s.split(\".\")</code>", "tách chuỗi tại dấu đầu thành ba phần: trước, dấu, sau / cắt chuỗi thành danh sách theo dấu chấm"],
                  ["<code>re.sub(mẫu, lambda m: …, s)</code>", "thay mọi chỗ khớp mẫu trong s bằng kết quả của một hàm nhỏ (lambda) nhận phần khớp m"]]),
           """Trước khi đọc mã, ta nhắc vài cú pháp Python vì mã dùng chúng liên tục. Có hàm lấy giá trị theo khoá, hai hàm cắt chuỗi, và hàm thay chữ nhận một hàm nhỏ.""", clear=True),
        st(code(KHO_PY, f"Bước 1. Kho nội dung là một cây ({SIM_T})"),
           """Bước một, ta mô phỏng kho nội dung bằng từ điển Python lồng nhau, vì kho thật cũng là một cây. Giá trị là từ điển thì là nút con, là chuỗi thì là thuộc tính.""",
           focus=[1, "2.2"], clear=True),
        st(code(KHO_RUN) + out(KHO_OUT, "Làm thử — kết quả chạy thật của mô phỏng"),
           """Làm thử, nút cấp ba có hai nút con, và nút trang chủ có ba thuộc tính. Đường dẫn có cả phần mở rộng thì không phải nút nào trong kho, nên phải tách nó trước khi tìm.""",
           focus=["3.1", "3.3"], clear=True),
        jstep([(("<code>[i for i, c in enumerate(url) if c == \".\"] + [len(url)]</code>", "danh sách sinh sẵn: lặp từng cặp (số thứ tự i, ký tự c) của url, giữ i khi c là dấu chấm; <code>+ […]</code> nối thêm một phần tử cuối", "Danh sách sinh sẵn lặp từng ký tự kèm số thứ tự, giữ lại vị trí các dấu chấm, rồi nối thêm vị trí cuối chuỗi."), "với <code>\"a.b\"</code> ra <code>[1, 3]</code>", ""),
               (("<code>url[:i]</code>, <code>url[i + 1:]</code>, <code>phan[:-1]</code>, <code>phan[-1]</code>", "cắt lát: <code>[:i]</code> là i phần tử đầu; <code>[i + 1:]</code> từ vị trí i + 1 tới hết; <code>[-1]</code> là phần tử cuối; <code>[:-1]</code> là mọi phần tử trừ cuối", "Cắt lát lấy một đoạn của chuỗi hay danh sách, và số âm đếm từ cuối về."), "<code>\"abcd\"[:2]</code> ra <code>ab</code>; <code>[1, 2, 3][-1]</code> ra <code>3</code>", ""),
               (("<code>i = max(co) if co else cat[0]</code>", "biểu thức điều kiện: i là số lớn nhất của <code>co</code> nếu <code>co</code> không rỗng, ngược lại là <code>cat[0]</code>", "Biểu thức điều kiện cho giá trị đầu nếu danh sách không rỗng, ngược lại cho giá trị sau."), "<code>1 if [5] else 0</code> ra <code>1</code>", ""),
               (("<code>giua, gach, hau_to = s.partition(\"/\")</code>", "gán ba phần của kết quả vào ba tên, theo thứ tự", "Một lệnh gán ba phần của kết quả vào ba tên theo thứ tự."), "<code>a, b, c = (1, 2, 3)</code> thì b là 2", "")]),
        st(code(TACH_PY, f"Bước 2. Tách đường dẫn theo cách của Sling ({SIM_T})"),
           """Bước hai là tách đường dẫn. Vì tên nút có thể chứa dấu chấm, nên hàm giữ điểm cắt xa nhất mà phần đầu là nút có thật. Phần còn lại chia theo dấu chấm: khúc cuối là phần mở rộng, các khúc trước là bộ chọn.""",
           focus=[1, "2.3", "2.6"], clear=True),
        st(code(TACH_RUN) + out(TACH_OUT, "Làm thử — kết quả chạy thật của mô phỏng"),
           """Làm thử với bốn đường dẫn, có bộ chọn, có hậu tố, và một đường dẫn trỏ tới nút không có nên cắt ở dấu chấm đầu tiên.""",
           focus=["1.1", "3.1", "3.3"], clear=True),
        st(code(CHON_PY, f"Bước 3. Chọn tệp dựng theo kiểu tài nguyên ({SIM_T})"),
           """Bước ba là chọn tệp dựng. Ta thử tên theo bộ chọn trước, rồi tới khúc cuối của kiểu tài nguyên. Mỗi tên tìm ở thư mục dự án trước, rồi mới tới thư mục sản phẩm.""",
           focus=[1, "2.5", "2.9"], clear=True),
        st(code(REQ_RUN) + out(REQ_OUT, "Làm thử — kết quả chạy thật của mô phỏng"),
           """Làm thử, hai trang khác đường dẫn nhưng cùng kiểu tài nguyên nên dùng chung một tệp dựng. Thêm bộ chọn vào trang chủ thì tệp mang tên bộ chọn được dùng thay.""",
           focus=["1.3", "3.3"], clear=True),
        st(code(HTL_TXT, "Bước 4. Tệp dựng HTL (đối chiếu đặc tả, không chạy; lienKet và mucCon là thuộc tính giả định)")
           + table(["phần", "nghĩa theo đặc tả HTL"],
                   [["data-sly-use.trang", "khởi tạo phần logic và đặt tên là trang để khuôn mẫu dùng"],
                    [f"{D}{{trang.tieuDe}}", "biểu thức; ở giữa thẻ thì tự thoát theo ngữ cảnh text"],
                    [f"href=\"{D}{{…}}\"", "tự xử lý theo ngữ cảnh uri: địa chỉ không hợp lệ thì không in gì"],
                    ["data-sly-list", "lặp nội dung của thẻ cho từng phần tử, tên mặc định là item"]]),
           """Bước bốn, đây là tệp dựng viết bằng ngôn ngữ khuôn mẫu, ta chỉ đọc đối chiếu vì máy này không chạy được nó. Biểu thức giữa thẻ tự thoát ký tự theo ngữ cảnh văn bản, còn trong địa chỉ thì được kiểm.""",
           focus=[1, "3.2", "3.3", "3.4"], clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>MA.get(c, c)</code>", "lấy giá trị đổi của <code>c</code> trong bảng <code>MA</code>; không có thì giữ nguyên <code>c</code> (đối số thứ hai là giá trị mặc định)"],
                  ["<code>\"\".join(… for c in s)</code>", "ghép các ký tự đã đổi lại thành một chuỗi"],
                  [PAT_ROW, "mẫu tìm đúng chữ " + PAT_TXT + ": các ký tự có dấu gạch chéo ngược đứng trước là ký tự thật, " + PAT_GRP + " bắt phần TÊN gồm chữ, số, gạch dưới hoặc hai chấm"],
                  ["<code>m.group(1)</code>", "phần nằm trong cặp ngoặc tròn thứ nhất của mẫu, tức TÊN"]]),
           """Mã tự thoát có bốn chỗ cần biết. Hàm lấy hai đối số nên giữ nguyên ký tự nếu bảng không có. Mẫu tìm đúng cụm có dấu đô la, và phần trong ngoặc tròn là tên thuộc tính, lấy ra bằng số một.""", clear=True),
        st(code(THOAT_PY, f"Bước 4 (tiếp). Tự thoát ký tự ở ngữ cảnh text ({SIM_T})") + out(THOAT_OUT),
           """Để thấy việc tự thoát, ta mô phỏng nó, và bảng đổi bốn ký tự đặc biệt thành mã vô hại. Kết quả chạy thật cho thấy đoạn mã lạ trong tiêu đề đã thành chữ thường, nên trình duyệt chỉ hiện nó ra chứ không chạy.""",
           focus=["2.2", "4.1"], clear=True),
        st(table(["ngữ cảnh (context)", "dùng khi", "HTL làm gì (theo đặc tả)"],
                 [["text", "mặc định cho nội dung giữa các thẻ", "mã hoá mọi ký tự đặc biệt của HTML"],
                  ["attribute", "mặc định cho giá trị thuộc tính", "mã hoá mọi ký tự đặc biệt của HTML"],
                  ["uri", "liên kết và đường dẫn (href, src)", "kiểm địa chỉ; không hợp lệ thì không in gì"],
                  ["html", "cần in ra thẻ một cách an toàn", "lọc bỏ các thẻ nguy hiểm"],
                  ["unsafe", "khi mọi ngữ cảnh khác đều quá chặt", "tắt hẳn việc thoát ký tự và bảo vệ; nên dễ bị XSS (kẻ gian cài đoạn lệnh chạy trong trình duyệt người xem)"]])
           + f"<span class='note'>Ghi đè bằng tuỳ chọn context, ví dụ <code>{D}{{properties.jcr:title @ context='text'}}</code>.</span>",
           """Có năm ngữ cảnh hay gặp. Văn bản và thuộc tính mã hoá mọi ký tự đặc biệt, còn địa chỉ thì được kiểm. Lọc thẻ giữ thẻ lành, và ngữ cảnh cuối tắt hẳn bảo vệ nên chỉ dùng khi hiểu rõ rủi ro.""",
           focus=["1.2", "1.3", "1.4", "1.5"], clear=True, introduces=["bnx_xss"]),
        jstep([(("<code>package com.vidu.site;</code>, <code>public class TrangModel { … }</code>", "<code>package</code>: lớp nằm ở thư mục com/vidu/site; <code>class</code>: khai một lớp, phần thân giữa cặp ngoặc nhọn; <code>public</code>: nơi khác dùng được", "Câu gói ghi thư mục chứa lớp, và khai lớp mở một khối có phần thân giữa cặp ngoặc nhọn."), "", ""),
               (("<code>import org.apache.sling…*;</code>", "lấy lớp của thư viện về dùng; dấu <code>*</code> lấy mọi lớp của gói đó", "Câu nhập lấy lớp của thư viện về dùng, và dấu sao lấy mọi lớp của gói."), "<code>import java.util.*;</code>", ""),
               (("<code>@Model(…)</code>, <code>@ValueMapValue(…)</code>", "chú thích bắt đầu bằng <code>@</code>: dán nhãn cho lớp hay trường ngay sau nó để thư viện đọc; tự nó không chạy gì", "Chú thích bắt đầu bằng dấu a còng, dán nhãn cho lớp hay trường ngay sau nó để thư viện đọc, và tự nó không chạy gì."), "", ""),
               (("<code>private String tieuDe;</code>, <code>public String getTieuDe() { return tieuDe; }</code>", "trường chuỗi <code>tieuDe</code> chỉ mã trong lớp này dùng được; hàm công khai <code>getTieuDe()</code> trả giá trị trường ra ngoài", "Trường riêng tư chỉ mã trong lớp dùng được, còn hàm công khai trả giá trị trường ra ngoài."), "", "")], intro="Trước khi đọc mã Java, ta cần bốn ký hiệu, vì mã dùng chúng."),
        st(code(MODEL_JAVA, "Bước 5. Lớp mô hình Sling Model (biên dịch được; chưa chạy trong máy chủ)")
           + "<p class='note'><code>@Model(adaptables=Resource.class)</code>: nhãn (annotation) báo lớp này tạo được từ một tài nguyên; <code>@ValueMapValue(name = \"jcr:title\")</code>: nhãn báo gán thuộc tính <code>jcr:title</code> vào biến ngay dưới. Quy ước: khuôn mẫu viết <code>&#36;{trang.tieuDe}</code> thì máy gọi hàm <code>getTieuDe()</code> của lớp (chữ <code>get</code> cộng tên thuộc tính viết hoa chữ đầu).</p>",
           """Bước năm là phần Java: lớp mô hình đọc thuộc tính tiêu đề. Khuôn mẫu viết tên thuộc tính, còn máy gọi hàm lấy giá trị cùng tên của lớp, nên logic nằm ở Java còn khuôn mẫu chỉ lo hiển thị.""",
           focus=[1, 2], clear=True),
        st(code(MANIFEST, "Tệp khai báo của gói chứa lớp đó (MANIFEST.MF)"),
           """Lớp này nằm trong một gói, nên tệp khai báo của gói ghi tên, phiên bản và các gói Java nó cần nhập. Trong khai báo này, thiếu dòng cuối thì lớp mô hình không được đăng ký.""",
           focus=[1, "2.7"], clear=True),
        jstep([(("<code>class Goi:</code>, <code>def __init__(self, …)</code>", "khai một lớp, khuôn tạo đối tượng; <code>__init__</code> chạy lúc tạo, <code>self</code> là chính đối tượng đó", "Lớp là khuôn tạo đối tượng, hàm tạo chạy lúc tạo, và tên chính nó chỉ đối tượng đang tạo."), "", ""),
               (("<code>self.ten, self.can, self.cap = ten, can, cap</code>", "gán ba giá trị vào ba trường của đối tượng một lúc, theo thứ tự", "Một lệnh gán ba giá trị vào ba trường của đối tượng theo thứ tự."), "", ""),
               (("<code>self.vet += [\"A\", \"B\"]</code>", "<code>+=</code> với danh sách: nối các phần tử vào cuối danh sách <code>self.vet</code>", "Dấu cộng bằng với danh sách nối thêm các phần tử vào cuối danh sách."), "<code>x = [1]; x += [2, 3]</code> thì x là <code>[1, 2, 3]</code>", ""),
               (("<code>raise RuntimeError(…)</code>, <code>try: … except RuntimeError as loi:</code>", "<code>raise</code>: ném lỗi, việc đang làm dừng; <code>try</code>/<code>except</code>: thử chạy, gặp lỗi loại đó thì chạy khối <code>except</code>, lỗi gán vào tên <code>loi</code>", "Lệnh ném lỗi dừng việc đang làm, còn khối thử và khối bắt lỗi chạy phần xử lý khi gặp lỗi loại đã nêu."), "", "")]),
        st(code(GOI_PY, f"Bước 6. Vòng đời của gói và sổ dịch vụ ({SIM_T})"),
           """Bước sáu, ta mô phỏng vòng đời của gói. Vì thiếu gói cần thì gói đứng ở trạng thái đã cài, còn đủ thì đi tới đang chạy và chỉ lúc đó mới ghi dịch vụ vào sổ.""",
           focus=[1, "2.5"], clear=True),
        st(code(GOI_RUN) + out(GOI_OUT, "Làm thử — kết quả chạy thật của mô phỏng"),
           """Làm thử, gói thứ nhất đang chạy và có một dịch vụ, khi dừng thì dịch vụ bị gỡ nên sổ trống. Gói thứ hai thiếu một gói cần nên chỉ ở trạng thái đã cài.""",
           focus=["3.1", "3.3"], clear=True),
    ], checks=["sorted(k for k, v in alg.bnx_l22_repo().items() if k.startswith('/content/site/vi/')) == ['/content/site/vi/home', '/content/site/vi/vay']",
               "sorted(alg.bnx_l22_props('/content/site/vi/home')) == ['jcr:primaryType', 'jcr:title', 'sling:resourceType'] and alg.bnx_l22_props('/content/site/vi/home.html') is None",
               "alg.bnx_l22_split('/content/site/vi/home.html') == ('/content/site/vi/home', [], 'html', None, True)",
               "alg.bnx_l22_split('/content/site/vi/home.in.a4.html') == ('/content/site/vi/home', ['in', 'a4'], 'html', None, True)",
               "alg.bnx_l22_split('/content/site/vi/home.html/phu/luc') == ('/content/site/vi/home', [], 'html', '/phu/luc', True)",
               "alg.bnx_l22_split('/content/site/vi/khong_co.html') == ('/content/site/vi/khong_co', [], 'html', None, False)",
               f"alg.bnx_l22_script('{PG}', [], 'html') == '/apps/{PG}/page.html'",
               f"alg.bnx_l22_resolve('/content/site/vi/vay.html') == ('/content/site/vi/vay', '{PG}', '/apps/{PG}/page.html')",
               f"alg.bnx_l22_resolve('/content/site/vi/home.in.a4.html')[2] == '/apps/{PG}/in.html'",
               f"alg.bnx_l22_escape({TITLE!r}) == 'Xin chào &lt;script&gt;alert(1)&lt;/script&gt;'",
               "alg.bnx_l22_escape('Vay tiêu dùng') == 'Vay tiêu dùng' and alg.bnx_l22_escape('&lt;') == '&amp;lt;'",
               "alg.bnx_l22_bundle_trace(['org.apache.sling.api'], {'org.apache.sling.api'}) == ['INSTALLED', 'RESOLVED', 'STARTING', 'ACTIVE']",
               "alg.bnx_l22_bundle_trace(['com.vidu.thieu'], {'org.apache.sling.api'}) == ['INSTALLED']",
               "alg.bnx_l22_bundle_step(alg.bnx_l22_bundle_step('ACTIVE', 'stop'), 'stopped') == 'RESOLVED'"])

    ex = sc("example", "example", "Ví dụ một yêu cầu, từng phép tính", [
        st(f"""<p>Yêu cầu: <code>/content/site/vi/home.html</code> {NOTE_SIM}</p>
<div class="box"><b>① Tách.</b> Chuỗi có <b>1</b> dấu chấm. Thử cắt ở cuối chuỗi: không có nút tên home.html. Thử cắt ở dấu chấm: nút <code>/content/site/vi/home</code> có thật.
<br>→ đường dẫn tài nguyên <code>/content/site/vi/home</code>, <b>0</b> selector, phần mở rộng <b>html</b>.</div>""",
           """Ta làm trọn một yêu cầu tới trang chủ. Phép tính thứ nhất là tách: cắt ở dấu chấm thì phần đầu là nút có thật, nên không có bộ chọn."""),
        st("<p><b>② Tìm nút.</b> Dùng đường dẫn tài nguyên ở phép ①: đi <b>4</b> cấp content → site → vi → home. Nút home có <b>3</b> thuộc tính:</p>"
           + table(["thuộc tính của nút home", "giá trị"],
                   [["jcr:primaryType", "nt:unstructured"], ["jcr:title", TITLE_H], ["sling:resourceType", PG]]),
           """Phép tính thứ hai đi bốn cấp từ gốc tới nút trang chủ, và nút này có ba thuộc tính."""),
        st(f"""<div class="box"><b>③ Đọc kiểu.</b> Trong 3 thuộc tính ở phép ②: <code>sling:resourceType = {PG}</code>. Khúc cuối của kiểu là <b>page</b>.</div>""",
           """Phép tính thứ ba đọc thuộc tính kiểu tài nguyên, giá trị gồm ba khúc và khúc cuối sẽ thành tên tệp.""",
           clear=True),
        st("<p><b>④ Chọn tệp.</b> Không có selector, phần mở rộng html được lược → tên tệp <b>page.html</b> (khúc cuối của kiểu ở phép ③).</p>"
           + table(["thứ tự tìm", "tệp ứng viên", "kết quả"],
                   [["1", f"/apps/{PG}/page.html", "có → chọn, dừng"], ["2", f"/libs/{PG}/page.html", "không cần xem tới"]]),
           """Phép tính thứ tư chọn tệp. Không có bộ chọn nên tên tệp là khúc cuối của kiểu, và tìm ở thư mục của dự án thì thấy ngay.""",
           clear=True),
        st(f"""<div class="box"><b>⑤ Dựng.</b> Tệp page.html in tiêu đề của nút ở phép ②. Tiêu đề dài <b>34</b> ký tự, có <b>4</b> ký tự đặc biệt (2 dấu &lt;, 2 dấu &gt;); mỗi ký tự thành 4 ký tự:
<br><code>{TITLE_E}</code> dài <b>34 + 4 × 3 = 46</b> ký tự → trình duyệt hiện chữ, <span class="hl">không chạy mã</span>.
<br><span class="note">46 tính theo hàm mô phỏng chỉ thoát 4 ký tự &amp; &lt; &gt; ", không đo từ máy chủ thật.</span></div>
<div class="box key">Phần Java phía sau nằm trong một gói OSGi đã đi qua <b>INSTALLED → RESOLVED → ACTIVE</b> (qua STARTING trong chốc lát).</div>""",
           """Phép tính thứ năm dựng trang: tiêu đề dài ba mươi bốn ký tự có bốn ký tự đặc biệt, mỗi ký tự thành bốn ký tự. Nên chuỗi sau khi thoát dài bốn mươi sáu, theo mô phỏng.""",
           clear=True),
    ], checks=["'/content/site/vi/home.html'.count('.') == 1 and alg.bnx_l22_props('/content/site/vi/home.html') is None",
               "alg.bnx_l22_split('/content/site/vi/home.html')[:3] == ('/content/site/vi/home', [], 'html')",
               "alg.bnx_l22_depth(alg.bnx_l22_split('/content/site/vi/home.html')[0]) == 4 and len(alg.bnx_l22_props('/content/site/vi/home')) == 3",
               f"alg.bnx_l22_props('/content/site/vi/home')['sling:resourceType'] == '{PG}' and '{PG}'.split('/')[-1] == 'page'",
               f"alg.bnx_l22_resolve('/content/site/vi/home.html')[2] == '/apps/{PG}/page.html'",
               f"len({TITLE!r}) == 34 and alg.bnx_l22_escaped_count({TITLE!r}) == 4 and len(alg.bnx_l22_escape({TITLE!r})) == 34 + 4 * 3 == 46",
               "[s for s in alg.bnx_l22_bundle_trace([], set()) if s != 'STARTING'] == ['INSTALLED', 'RESOLVED', 'ACTIVE']"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: gỡ một tệp dựng, và so với bảng ví dụ của Apache Sling", [
        st(code(CHECK_RUN, f"Gỡ tệp page.html của dự án rồi hỏi lại ({SIM_T})") + out(CHECK_OUT),
           """Kiểm bằng đường khác: nếu đúng là tìm ở thư mục của dự án trước, thì khi gỡ tệp ở đó, tệp của sản phẩm phải được dùng thay, và kết quả chạy thật đúng vậy. Kiểu không có tệp dựng nào thì hàm trả về rỗng.""",
           focus=[1, "4.1", "4.3"]),
        st(table(["đường dẫn (bảng của Apache Sling, giả định có tài nguyên /a/b)", "tài nguyên", "selector", "mở rộng", "hậu tố"],
                 [["/a/b.s1.s2.html", "/a/b", "s1.s2", "html", "không"],
                  ["/a/b.html/c/d", "/a/b", "không", "html", "/c/d"],
                  ["/a/b/c/d.s.txt", "/a/b/c/d (không có)", "s", "txt", "không"],
                  ["/a/b.s1.html/c/d.s.txt", "/a/b", "s1", "html", "/c/d.s.txt"]])
           + "<p style='margin-top:14px'><span class='note'>Bảng ví dụ của Apache Sling có 14 hàng không dùng tham số đường dẫn (cặp tên=giá trị sau dấu chấm phẩy); hàm tách của bài cho đúng cả <b>14</b> hàng.</span></p>",
           """Đường kiểm thứ hai là bảng ví dụ của chính nhóm làm ra tầng phân giải đường dẫn, nên đáng tin hơn tự đoán. Bảng đó có mười bốn hàng, hàm tách của bài cho đúng cả mười bốn.""",
           focus=[0, 2], clear=True),
    ], checks=[f"alg.bnx_l22_script('{PG}', [], 'html', ['/apps/{PG}/in.html', '/libs/{PG}/page.html']) == '/libs/{PG}/page.html'",
               f"alg.bnx_l22_script('{PG}', ['in'], 'html', ['/apps/{PG}/in.html', '/libs/{PG}/page.html']) == '/apps/{PG}/in.html'",
               "alg.bnx_l22_script('site/components/khac', [], 'html') is None",
               f"sum(alg.bnx_l22_split(u, ['/a', '/a/b']) == (p, s, e, x, f) for u, p, s, e, x, f in {SLING_ROWS!r}) == 14",
               "alg.bnx_l22_split('/a/b/c/d.s.txt', ['/a', '/a/b']) == ('/a/b/c/d', ['s'], 'txt', None, False)"])

    quymo = sc("quymo", "example", "Khi kho lớn dần: tìm theo thuộc tính có và không có chỉ mục", [
        st(QUYMO.show(lines=(1, 7), title=f"QuyMo.py (trích): dựng kho n trang, cứ 100 trang có 1 trang kiểu page ({SIM_T})"),
           """Ta đo khi kho lớn dần. Hàm dựng kho có n trang, cứ một trăm trang thì có một trang mang kiểu trang, còn lại là kiểu tin, và đây là mô phỏng.""",
           clear=True),
        st(QUYMO.show(lines=(8, 16), title="QuyMo.py (tiếp): duyệt qua mọi nút để tìm theo thuộc tính"),
           """Hàm duyệt đếm mọi nút nó đi qua và mọi nút khớp kiểu trang, vì không có chỉ mục thì kho chỉ còn cách xem từng nút.""",
           clear=True),
        st(QUYMO.show(lines=(17, 23), title="QuyMo.py (hết): so duyệt với chỉ mục, ở 10, 1 000 và 100 000 trang") + QUYMO.out_html(),
           """Chỉ mục ở đây là một từ điển ghi sẵn kiểu nào có những trang nào. Kết quả chạy thật: duyệt đi qua mười bốn, một nghìn không trăm bốn, rồi một trăm nghìn không trăm bốn nút, còn chỉ mục chỉ đọc đúng số nút khớp.""",
           focus=[1, "2.2"], clear=True),
        st(table(["số trang N", "nút phải duyệt (không chỉ mục)", "nút khớp", "nút đọc qua chỉ mục", "bước tra đường dẫn một trang (mô phỏng)"],
                 [[nowrap("10 (×1)"), "14", "1", "1", "4"],
                  [nowrap("1 000 (×100)"), "1 004", "10", "10", "4"],
                  [nowrap("100 000 (×10 000)"), "100 004", "1 000", "1 000", "4"]]),
           """Bảng cho thấy hai cách tăng khác nhau. Trong mô phỏng, tra một đường dẫn luôn bốn bước, còn kho thật phụ thuộc số con của mỗi nút. Truy vấn không chỉ mục đọc số nút tăng thẳng theo kho, còn chỉ mục thì đọc đúng số nút khớp.""",
           focus=[0, "1.2", "1.3"], clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["duyệt toàn kho", "không cần chuẩn bị, luôn đúng", "số nút đọc tăng thẳng theo kho", "kho nhỏ, truy vấn hiếm"],
                  ["tạo chỉ mục cho thuộc tính", "chỉ đọc đúng số nút khớp", "mỗi lần ghi phải cập nhật chỉ mục, tốn thêm chỗ chứa; phải khai trước đúng thuộc tính", "thuộc tính được truy vấn thường xuyên"],
                  ["thu hẹp phạm vi, chỉ tìm dưới một nhánh", "duyệt ít nút hơn", "không thấy nút nằm ngoài nhánh", "biết trước nội dung nằm ở nhánh nào"]]),
           """Ta phải chọn và chấp nhận đánh đổi. Duyệt toàn kho không cần chuẩn bị nhưng chậm theo kho. Chỉ mục đổi chi phí đọc lấy chi phí ghi và chỗ chứa, còn thu hẹp phạm vi thì bỏ sót nút ngoài nhánh.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l22_scale(10) == (14, 1, 1) and alg.bnx_l22_scale(1000) == (1004, 10, 10) and alg.bnx_l22_scale(100000) == (100004, 1000, 1000)",
               "alg.bnx_l22_depth('/content/site/vi/home') == 4",
               "1000 // 10 == 100000 // 1000 == 100 and 100000 // 10 == 10000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ mỗi trang là một tệp HTML trên đĩa, và Sling chọn mã dựng theo <b>đường dẫn</b>.
<br><span class="note">Đúng: trang là dữ liệu trong kho nội dung (nút và thuộc tính). Đường dẫn chỉ để tìm tài nguyên; mã dựng được chọn theo <b>sling:resourceType</b>. Vì vậy 2 trang khác đường dẫn dùng chung 1 tệp page.html.</span></div>""",
           """Lỗi thứ nhất, của người mới, là nghĩ mỗi trang là một tệp trên đĩa và mã dựng chọn theo đường dẫn. Thật ra trang là dữ liệu trong kho, và mã dựng chọn theo kiểu tài nguyên."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Cài gói xong, thấy không báo lỗi là yên tâm. Thật ra gói đang ở <b>INSTALLED</b> vì một gói trong Import-Package (dòng khai các gói Java mà gói này cần nhập từ gói khác) không có: việc phân giải thất bại, lệnh start ném BundleException (lỗi OSGi báo gói không chạy được), <b>không dịch vụ nào</b> được đăng ký.
<br><span class="note">Cách chữa: sau mỗi lần triển khai, đọc trạng thái từng gói. INSTALLED: tìm gói phụ thuộc còn thiếu. RESOLVED: gói đủ điều kiện nhưng chưa chạy. Chỉ <b>ACTIVE</b> mới cung cấp dịch vụ, nhưng ACTIVE chưa đủ: thành phần khai báo kiểu DS (Declarative Services: Java khai báo bằng chú thích, OSGi tự nối các dịch vụ lại) còn thiếu tham chiếu thì chưa đăng ký dịch vụ (OSGi Compendium §112.3); xem cả mục thành phần trong bảng điều khiển.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là cài gói xong thấy không báo lỗi thì yên tâm, trong khi gói kẹt ở đã cài vì thiếu một gói cần nhập. Cách chữa là sau mỗi lần triển khai đọc trạng thái từng gói, vì chỉ đang chạy mới có dịch vụ.""",
           clear=True, introduces=["bnx_ds"]),
        st("<p><b>Cùng giai đoạn.</b> Sửa thẳng tệp dựng trong <code>/libs</code>: chỗ sửa có thể mất khi nâng cấp hay vá nóng.</p>"
           + table(["nhánh", "thuộc về", "khi nâng cấp sản phẩm"],
                   [["<code>/libs</code>", "sản phẩm", "bị thay, chỗ sửa mất"],
                    ["<code>/apps</code>", "dự án của bạn", "giữ nguyên, được tìm trước"]]),
           """Còn một lỗi cùng giai đoạn là sửa thẳng thư mục của sản phẩm. Nhánh này đổi mỗi khi nâng cấp nên chỗ sửa có thể mất, vì vậy hãy dựng lại ở thư mục của dự án, nơi được tìm trước.""",
           clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc kho lớn dần).</b> Viết truy vấn tìm mọi nút theo một thuộc tính mà không có chỉ mục cho nó. Theo hướng dẫn của Apache Jackrabbit Oak (bộ máy kho nội dung của AEM), không có chỉ mục thì kho bị <b>duyệt qua</b>, và nhật ký ghi cảnh báo dạng “Traversed 10000 nodes with filter …”.
<br><span class="note">Kho mẫu của bài: tìm nút có kiểu site/components/page phải đọc cả <b>6</b> nút (5 nút dưới gốc và nút gốc, như hàm <code>duyet</code> ở phần đo) để ra <b>2</b> nút khớp; phần đo ở trên cho thấy 100 004 nút ở 100 000 trang. Cách chữa: tạo chỉ mục cho thuộc tính được truy vấn, và theo dõi cảnh báo đó trong nhật ký.</span></div>""",
           """Lỗi thứ ba lộ ra khi kho lớn dần: truy vấn theo một thuộc tính không có chỉ mục thì kho bị duyệt qua từng nút. Cách chữa là tạo chỉ mục cho thuộc tính được truy vấn.""",
           clear=True),
    ], checks=["len({alg.bnx_l22_resolve(u)[0] for u in ('/content/site/vi/home.html', '/content/site/vi/vay.html')}) == 2 and len({alg.bnx_l22_resolve(u)[2] for u in ('/content/site/vi/home.html', '/content/site/vi/vay.html')}) == 1",
               "alg.bnx_l22_bundle_trace(['p.q'], set())[-1] == 'INSTALLED' and not alg.bnx_l22_serves('INSTALLED')",
               "not alg.bnx_l22_serves('RESOLVED') and alg.bnx_l22_serves('ACTIVE')",
               f"alg.bnx_l22_script('{PG}', [], 'html').startswith('/apps/')",
               f"alg.bnx_l22_scan_cost('{PG}') == (5, 2) and 5 + 1 == 6"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề (dùng kho mẫu và ba tệp dựng của bài)"],
                 [["1", "Yêu cầu /content/site/vi/vay.in.a4.html: đường dẫn tài nguyên, selector, phần mở rộng là gì? Tệp dựng nào được chọn?"],
                  ["2", "Gói A cần nhập gói p.q, nhưng không gói nào đang cài cung cấp p.q. Gọi start thì A ở trạng thái nào, có dịch vụ không? Gói B đang ACTIVE bị stop thì về trạng thái nào?"],
                  ["3", f"Quyết định: biên tập viên muốn chữ <b>in đậm</b> trong tiêu đề, nên nhập cả thẻ. Chọn <code>context='html'</code> hay <code>context='unsafe'</code> cho biểu thức in tiêu đề?"]]),
           """Đến lượt bạn. Câu một, với yêu cầu đang hiện, đường dẫn tài nguyên, bộ chọn và tệp dựng là gì? Câu hai, gói A cần nhập một gói Java mà không gói nào cung cấp, gọi khởi động thì A ở trạng thái nào? Câu ba, muốn chữ in đậm thì chọn ngữ cảnh nào? Hãy dừng video và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4"], pause=25),
        st(f"""<div class="box"><b>Câu 1.</b> Cắt ở dấu chấm đầu tiên thì <code>/content/site/vi/vay</code> là nút có thật → đường dẫn tài nguyên. Phần còn lại <code>in.a4.html</code>: selector <b>in, a4</b>; phần mở rộng <b>html</b>.
<br>Kiểu của nút vay: {PG}. Tên ứng viên: in/a4.html (không có) → <b>in.html</b> (có ở /apps) → chọn <code>/apps/{PG}/in.html</code>.</div>""",
           """Đáp án câu một: nút trang vay là đường dẫn tài nguyên, và hai bộ chọn là in và a bốn. Tên khớp bộ chọn đầu có ở thư mục của dự án, nên tệp được chọn là tệp in của dự án."""),
        st("""<div class="box"><b>Câu 2.</b> Thiếu p.q → không phân giải được → start báo lỗi, gói A đứng ở <b>INSTALLED</b>, <b>0</b> dịch vụ.
<br>Gói B: ACTIVE → STOPPING → <b>RESOLVED</b>; dịch vụ của B bị gỡ khỏi sổ.</div>""",
           """Đáp án câu hai: thiếu gói cần nhập thì không phân giải được, nên gói A đứng ở đã cài và không có dịch vụ. Gói B đi từ đang chạy qua đang dừng về đã phân giải, và dịch vụ của nó bị gỡ khỏi sổ."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["context='html'", "thẻ in đậm vẫn hiện; thẻ nguy hiểm bị lọc bỏ", "một số thẻ biên tập viên muốn có thể bị lọc; phải thử trước"],
                  ["context='unsafe'", "nhập gì hiện nấy, không phải thử", "tắt hẳn bảo vệ: một đoạn mã lạ trong tiêu đề sẽ chạy trên máy khách"]]),
           """Đáp án câu ba: ngữ cảnh lọc thẻ cho thẻ in đậm hiện ra mà lọc bỏ thẻ nguy hiểm, đổi lại phải thử. Ngữ cảnh tắt bảo vệ cho mã lạ chạy trên máy khách, nên trang ngân hàng chọn lọc thẻ.""",
           focus=["1.2", "1.3"]),
    ], checks=["alg.bnx_l22_split('/content/site/vi/vay.in.a4.html') == ('/content/site/vi/vay', ['in', 'a4'], 'html', None, True)",
               f"alg.bnx_l22_resolve('/content/site/vi/vay.in.a4.html') == ('/content/site/vi/vay', '{PG}', '/apps/{PG}/in.html')",
               "alg.bnx_l22_bundle_trace(['p.q'], {'x.y'}) == ['INSTALLED'] and not alg.bnx_l22_serves(alg.bnx_l22_bundle_trace(['p.q'], {'x.y'})[-1])",
               "[alg.bnx_l22_bundle_step('ACTIVE', 'stop'), alg.bnx_l22_bundle_step('STOPPING', 'stopped')] == ['STOPPING', 'RESOLVED']"])

    lab_pr = practice_scene(sc, "Tự làm: từ địa chỉ tới tệp dựng trong một kho nhỏ", practice_steps2(
        st, "BNX", "L22",
        """<p><b>Đề</b> (mô phỏng, không phải máy chủ AEM): kho <code>KHO</code> có hai trang <code>the</code> (kiểu <code>bank/components/card</code>) và <code>vay</code> (kiểu <code>bank/components/loan</code>); ba tệp dựng trong <code>TEP</code>. Viết <code>mau.py</code>: với 5 địa chỉ trong <code>de.md</code>:</p>
<ol><li>tách tại dấu chấm đầu: đường dẫn tài nguyên, bộ chọn (nếu có), phần mở rộng</li><li>tìm nút trong <code>KHO</code> (không có → <code>KHONG CO TAI NGUYEN</code>)</li><li>chọn tệp: tên bộ chọn rồi khúc cuối của kiểu; <code>/apps</code> trước <code>/libs</code></li></ol>
<p class="note">Kho, danh sách tệp và 5 địa chỉ nằm ở <code>de.md</code>; in <code>&lt;tên cuối&gt; -&gt; &lt;kết quả&gt;</code> mỗi địa chỉ một dòng.</p>""",
        """Bây giờ tới phần bạn tự làm, vẫn là mô phỏng. Cho một kho có hai trang và ba tệp dựng, hãy viết chương trình xử lý năm địa chỉ: tách đường dẫn và bộ chọn, tìm nút, rồi chọn tệp dựng, thư mục của dự án trước.""",
        LAB.out, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>duong, _, phan = url.partition(".")</code> tách tại dấu chấm đầu; <code>phan.split(".")</code> cho các khúc, khúc cuối là phần mở rộng. Danh sách tên ứng viên: bộ chọn (nếu có) rồi <code>kieu.split("/")[-1]</code>.
Lời giải ở <code>labs/BNX/L22/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, tách địa chỉ tại dấu chấm đầu tiên rồi chia phần sau theo dấu chấm. Tên ứng viên là bộ chọn nếu có, rồi khúc cuối của kiểu tài nguyên. Lời giải chỉ mở sau khi đã thử.""", pause=120), "BNX", "L22")

    rec = sc("recap", "recap", "Chuỗi logic, góc phỏng vấn & tư duy cần mang theo", [
        st(chain("JCR: trang là nút và thuộc tính", "Sling: đường dẫn → tài nguyên", "sling:resourceType → tệp dựng, /apps trước /libs", "HTL: tự thoát theo ngữ cảnh", "Sling Model: logic ở Java", "OSGi: chỉ ACTIVE mới có dịch vụ"),
           """Tổng kết: trang là nút và thuộc tính trong kho, đường dẫn đổi thành tài nguyên, và kiểu tài nguyên quyết định tệp dựng. Khuôn mẫu tự thoát ký tự theo ngữ cảnh, còn gói chỉ có dịch vụ khi đang chạy.""",
           focus=[0, "1.3", "1.5", "1.7"]),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["Một yêu cầu tới trang AEM được xử lý thế nào?", "Sling tách đường dẫn, tìm tài nguyên trong JCR, đọc sling:resourceType (AEM: nút cq:Page, thuộc tính ở nút con jcr:content), chọn tệp dựng HTL (tìm /apps trước /libs)"],
                  ["Sling Model và HTL chia việc ra sao?", "Sling Model là lớp Java gắn @Model(adaptables=Resource.class), nạp thuộc tính của tài nguyên; HTL gọi nó bằng data-sly-use và chỉ lo hiển thị, tự thoát theo ngữ cảnh"],
                  ["Gói OSGi triển khai xong mà không chạy, bạn xem gì?", "trạng thái gói: INSTALLED là chưa phân giải được, thường do thiếu gói trong Import-Package; RESOLVED là chưa chạy; chỉ ACTIVE mới đăng ký dịch vụ, và thành phần DS thiếu tham chiếu thì ACTIVE vẫn chưa có dịch vụ"]])
           + "<p><span class='note'>Trả lời bằng cơ chế; không nêu số liệu của dự án hay tổ chức thật. Bài này là mô phỏng theo đặc tả công khai, không thay cho việc thực hành trên máy chủ AEM.</span></p>",
           """Người phỏng vấn hay hỏi: một yêu cầu tới trang được xử lý thế nào, lớp mô hình và khuôn mẫu chia việc ra sao, và gói xong mà không chạy thì xem gì.""",
           focus=[1, 1], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> gặp một hệ lớn, hỏi ba điều: <b>dữ liệu</b> nằm ở đâu, <b>luật nào</b> chọn mã để chạy, và mã đó đang ở <b>trạng thái</b> nào. Rồi hỏi thêm: truy vấn này còn rẻ khi dữ liệu lớn gấp trăm lần không?</div>
<p class='small'>Bài sau: huấn luyện rừng cô lập để tìm giao dịch lạ, rồi đưa mô hình ra chạy ở nơi khác.</p>""",
           """Điều cần mang theo: gặp một hệ lớn, hỏi dữ liệu nằm ở đâu, luật nào chọn mã để chạy, mã ở trạng thái nào, và truy vấn còn rẻ khi dữ liệu gấp trăm lần không. Bài sau ta huấn luyện một rừng cô lập để tìm giao dịch lạ.""",
           clear=True, forward_ref=True),
    ], checks=[f"alg.bnx_l22_resolve('/content/site/vi/home.html') == ('/content/site/vi/home', '{PG}', '/apps/{PG}/page.html')",
               "alg.bnx_l22_serves('ACTIVE') and not alg.bnx_l22_serves('RESOLVED')"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L22", "aem_jcr_sling_htl_osgi",
                  "Bài 22 — Adobe Experience Manager: JCR, Sling phân giải đường dẫn, thành phần HTL và gói OSGi",
                  "curriculum/bnx.yaml L22; audit/bnx/verify_bnx.py L22; audit/bnx/sources_l22.md (đọc 2026-11-12): Apache Sling “URL decomposition”, "
                  "“Servlets and Scripts”, “Scripting”, “Sling Models”; “Resources”; đặc tả HTL (github.com/adobe/htl-spec); "
                  "OSGi Core Release 8 chương Life Cycle, Module, Service; JCR 2.0 (JSR 283) chương 3 Repository Model; Apache Jackrabbit Oak “Query Engine”; "
                  "Adobe AEM 6.5 “Overlays”. Máy không có máy chủ AEM: cơ chế dạy bằng mô phỏng Python theo tài liệu; mã HTL, Java, MANIFEST chỉ đọc đối chiếu; "
                  "quy mô và lab: Python chạy thật (mô phỏng, audit/bnx/progcache/L22.json)",
                  ["Đọc một cây nội dung JCR gồm nút và thuộc tính",
                   "Lần theo cách Sling đổi một đường dẫn thành tài nguyên rồi chọn tệp dựng trang",
                   "Đọc một đoạn HTL và nói vì sao nó tự thoát ký tự theo ngữ cảnh",
                   "Kể vòng đời của một gói OSGi và vai trò của dịch vụ",
                   "So sánh số nút phải đọc khi tìm theo thuộc tính có và không có chỉ mục ở 10, 1 000 và 100 000 trang",
                   "Tìm tài nguyên và tệp dựng cho một địa chỉ trong một kho nhỏ bằng mã Python"],
                  scenes,
                  covers=[(1, "formula"), (2, "example"), (3, "formula"), (4, "formula"), (5, "quymo"), (6, "practice")])
