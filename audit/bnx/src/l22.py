from lib import *

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


def build():
    hook = sc("hook", "hook", "9 giờ sáng, biên tập viên sửa tiêu đề trang vay: không ai triển khai lại mã", [
        st(f"""<p>Trang web giới thiệu sản phẩm của một ngân hàng chạy trên <b>Adobe Experience Manager (AEM)</b>. 9 giờ sáng, biên tập viên sửa tiêu đề trang chủ. Trang đổi ngay trên máy soạn (author), dù <b>không ai triển khai lại mã</b> và trên đĩa có <b>0</b> tệp HTML của trang đó; khách chỉ thấy sau khi nội dung được đăng (publish) sang máy đăng.</p>
<div class="box key">Lỡ tay, người đó gõ vào tiêu đề chuỗi <code>{TITLE_H}</code>. Trình duyệt của khách có chạy đoạn mã lạ đó không? Và <b>2</b> trang khác nhau làm sao dùng chung <b>1</b> tệp dựng?</div>
{NOTE_SIM}""",
           """Chào bạn, trang web giới thiệu sản phẩm của một ngân hàng chạy trên một hệ quản trị nội dung, tên của nó đang hiện trên màn hình.
           Chín giờ sáng, biên tập viên sửa tiêu đề trang chủ, và trang đổi ngay trên máy soạn, dù không ai triển khai lại mã và trên đĩa không có tệp nào của trang đó.
           Lỡ tay, người đó gõ vào tiêu đề một đoạn mã lạ, vậy trình duyệt của khách có chạy đoạn mã đó không? Và hai trang khác nhau làm sao dùng chung một tệp dựng?
           Máy ta không có máy chủ thật nên bài là mô phỏng theo đặc tả công khai, và khách chỉ thấy trang sau khi nội dung được đăng sang máy đăng.""",
           focus=[1, 1, 2, 2, 3]),
        st(table(["câu hỏi", "phần trả lời trong bài"],
                 [["trang nằm ở đâu nếu không phải tệp trên đĩa", "kho nội dung JCR: cây gồm nút và thuộc tính"],
                  ["từ đường dẫn tới mã dựng trang bằng cách nào", "Sling: tách đường dẫn, tìm tài nguyên, đọc kiểu tài nguyên, chọn tệp dựng"],
                  ["vì sao đoạn mã lạ trong tiêu đề không chạy", "HTL tự thoát ký tự theo ngữ cảnh"],
                  ["mã Java của dự án được nạp và chạy thế nào", "gói OSGi có vòng đời; chỉ gói đang chạy mới cung cấp dịch vụ"]]),
           """Bài này trả lời bốn câu hỏi. Trang nằm ở đâu nếu không phải tệp trên đĩa. Từ đường dẫn tới mã dựng trang bằng cách nào.
           Vì sao đoạn mã lạ trong tiêu đề không chạy. Và mã Java của dự án được nạp và chạy thế nào.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ], checks=[f"alg.bnx_l22_resolve('/content/site/vi/home.html')[2] == alg.bnx_l22_resolve('/content/site/vi/vay.html')[2] == '/apps/{PG}/page.html'",
               "len({alg.bnx_l22_resolve(u)[2] for u in ('/content/site/vi/home.html', '/content/site/vi/vay.html')}) == 1",
               f"alg.bnx_l22_props('/content/site/vi/home')['jcr:title'] == {TITLE!r}"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Cây", "mỗi nút có một nút cha và có thể có nhiều nút con; đi từ gốc xuống theo tên", "thư mục trên máy: ổ đĩa → thư mục → thư mục con"],
                  ["② Đường dẫn và phần mở rộng", "dãy tên nối bằng dấu gạch chéo; phần sau dấu chấm cuối cho biết dạng muốn nhận", "/content/site/vi/home.html: 4 cấp, phần mở rộng html"],
                  ["③ Ký tự đặc biệt của HTML", "dấu &lt; mở một thẻ; muốn hiện nó như chữ thường phải viết thành &amp;lt;", "&lt;b&gt; là thẻ in đậm; &amp;lt;b&amp;gt; hiện ra đúng ba ký tự &lt;b&gt;"],
                  ["④ Máy trạng thái", "một vật chỉ ở một trạng thái tại một lúc, và chỉ đi theo các bước cho phép", "đèn giao thông: xanh → vàng → đỏ"]]),
           """Trước hết ta cần hiểu bốn điều. Cây là cấu trúc mà mỗi nút có một nút cha và có thể có nhiều nút con, giống thư mục trên máy.
           Đường dẫn là dãy tên nối bằng dấu gạch chéo, còn phần sau dấu chấm cuối là phần mở rộng, cho biết dạng muốn nhận.
           Trong trang web, dấu nhỏ hơn mở một thẻ, nên muốn hiện nó như chữ thường thì phải viết thành một mã bốn ký tự.
           Máy trạng thái là một vật chỉ ở một trạng thái tại một lúc, và chỉ đi theo các bước cho phép, giống đèn giao thông.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st("""<div class="box"><b>Ví dụ số.</b> Đường dẫn <code>/content/site/vi/home</code> có <b>4</b> cấp: content → site → vi → home.
<br>Chuỗi <code>&lt;b&gt;</code> có <b>2</b> ký tự đặc biệt; sau khi thoát thành <code>&amp;lt;b&amp;gt;</code>, dài <b>3 + 2 × 3 = 9</b> ký tự.</div>""",
           """Một ví dụ số. Đường dẫn đang hiện có bốn cấp, đi từ nút gốc qua ba nút trung gian tới nút cuối.
           Chuỗi thẻ in đậm dài ba ký tự, trong đó có hai ký tự đặc biệt. Vì mỗi ký tự đặc biệt dài thêm ba ký tự khi thoát, nên chuỗi sau khi thoát dài chín ký tự."""),
    ], checks=["alg.bnx_l22_depth('/content/site/vi/home') == 4",
               "alg.bnx_l22_escape('<b>') == '&lt;b&gt;' and alg.bnx_l22_escaped_count('<b>') == 2",
               "len(alg.bnx_l22_escape('<b>')) == 3 + 2 * 3 == 9",
               "alg.bnx_l22_bundle_step('INSTALLED', 'start') is None"])

    sym = sc("sym", "symbol", "Giải mã từ ngữ và sáu trạng thái của gói", [
        st(table(["từ", "nghĩa"],
                 [["AEM (Adobe Experience Manager)", "hệ quản trị nội dung trang web; bài này chỉ dạy bốn nền móng bên dưới nó"],
                  ["JCR (Java Content Repository)", "kho nội dung dạng cây. Mỗi mục là <b>nút</b> hoặc <b>thuộc tính</b>; nội dung thật nằm trong giá trị của thuộc tính"],
                  ["jcr:primaryType", "thuộc tính bắt buộc, giữ tên kiểu nút chính; <code>nt:unstructured</code> cho phép nút con và thuộc tính tên bất kỳ"],
                  ["Sling, tài nguyên (resource)", "tầng nhận yêu cầu web: đổi đường dẫn thành một tài nguyên trong kho"]]),
           """Bảng này giải mã các từ của bài. Tên đầu tiên là hệ quản trị nội dung trang web, và bài chỉ dạy bốn nền móng bên dưới nó.
           Nền móng thứ nhất là kho nội dung dạng cây, mỗi mục là nút hoặc thuộc tính, và nội dung thật nằm trong giá trị của thuộc tính.
           Mỗi nút có một thuộc tính bắt buộc giữ tên kiểu nút chính, và kiểu đang hiện cho phép nút con và thuộc tính tên bất kỳ.
           Nền móng thứ hai là tầng nhận yêu cầu web, nó đổi đường dẫn thành một tài nguyên trong kho.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st(table(["từ", "nghĩa"],
                 [["sling:resourceType", "thuộc tính ghi <b>kiểu tài nguyên</b>; Sling dùng nó để tìm tệp dựng (script). AEM thật: nút trang là <code>cq:Page</code>, thuộc tính này nằm ở nút con <code>jcr:content</code>; bài gộp hai nút cho gọn"],
                  ["selector, extension", "các khúc giữa tên tài nguyên và phần mở rộng (home<b>.in.a4</b>.html); phần mở rộng là khúc cuối"],
                  ["HTL (HTML Template Language)", f"ngôn ngữ khuôn mẫu: biểu thức <code>{D}{{…}}</code> và các thuộc tính <code>data-sly-*</code>"],
                  ["OSGi, bundle, service", "khung mô-đun của Java: mã đóng thành <b>gói</b> (bundle) có vòng đời; gói đăng ký <b>dịch vụ</b> cho gói khác dùng"]]),
           """Bảng tiếp theo cho bốn từ còn lại. Thuộc tính kiểu tài nguyên là thứ tầng này dùng để tìm tệp dựng, và ở hệ thật nó nằm ở nút con của nút trang, còn bài gộp hai nút cho gọn.
           Bộ chọn là các khúc nằm giữa tên tài nguyên và phần mở rộng, còn phần mở rộng là khúc cuối.
           Nền móng thứ ba là ngôn ngữ khuôn mẫu, gồm biểu thức trong ngoặc nhọn và các thuộc tính đặc biệt của thẻ.
           Nền móng thứ tư là khung mô-đun của Java, nơi mã đóng thành gói có vòng đời, và gói đăng ký dịch vụ cho gói khác dùng.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
        st(table(["trạng thái của gói (bundle)", "nghĩa theo đặc tả OSGi Core 8"],
                 [["INSTALLED", "gói đã được cài thành công"],
                  ["RESOLVED", "mọi lớp Java gói cần đều có; gói sẵn sàng được khởi động, hoặc vừa dừng"],
                  ["STARTING", "gói đang được khởi động"],
                  ["ACTIVE", "gói đã kích hoạt xong và đang chạy"],
                  ["STOPPING", "gói đang được dừng"],
                  ["UNINSTALLED", "gói đã bị gỡ; không chuyển sang trạng thái nào khác được nữa"]]),
           """Một gói có sáu trạng thái. Trạng thái thứ nhất là đã cài thành công.
           Trạng thái thứ hai là đã phân giải, nghĩa là mọi lớp Java gói cần đều có, nên gói sẵn sàng được khởi động, hoặc vừa dừng.
           Trạng thái thứ ba là đang khởi động. Trạng thái thứ tư là đang chạy, tức gói đã kích hoạt xong.
           Trạng thái thứ năm là đang dừng. Trạng thái thứ sáu là đã gỡ, và từ đó gói không chuyển sang trạng thái nào khác được nữa.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"], clear=True),
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
           """Hình này là đường đi của một yêu cầu. Bên trái là kho nội dung, một cây nút, trong đó hai nút trang ở dưới cùng mang cùng một kiểu tài nguyên.
           Bên phải, tầng nhận yêu cầu tách đường dẫn thành đường dẫn tài nguyên và phần mở rộng, rồi đọc thuộc tính kiểu tài nguyên của nút tìm được.
           Từ kiểu đó nó chọn tệp dựng, và tệp dựng đọc thuộc tính của nút, tự thoát ký tự, rồi trả trang về.
           Vì vậy trang là dữ liệu trong kho, còn mã dựng được chọn theo kiểu tài nguyên, không theo đường dẫn."""),
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
           """Hình thứ hai là vòng đời của một gói. Gói vừa cài ở trạng thái đã cài, và khi đủ mọi gói phụ thuộc thì sang trạng thái đã phân giải.
           Lệnh khởi động đưa gói qua trạng thái đang khởi động rồi tới đang chạy, và lúc đó gói mới đăng ký dịch vụ vào sổ ở bên phải.
           Lệnh dừng đưa gói qua trạng thái đang dừng rồi quay về đã phân giải, và dịch vụ của nó tự động bị gỡ khỏi sổ.
           Gói ở đã cài hay đã phân giải đều gỡ được. Nếu thiếu gói phụ thuộc thì gói kẹt ở trạng thái đã cài. Vì vậy đã phân giải mới là đủ điều kiện chạy, chưa phải đang chạy."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: kho, đường dẫn, tệp dựng, khuôn mẫu, gói", [
        st(code(KHO_PY, f"Bước 1. Kho nội dung là một cây ({SIM_T})"),
           """Bước một, ta mô phỏng kho nội dung bằng một từ điển Python lồng nhau, vì kho thật cũng là một cây.
           Giá trị nào là từ điển thì là nút con, giá trị nào là chuỗi thì là thuộc tính.
           Hàm tìm nút đi từ gốc xuống theo từng tên trong đường dẫn, và trả về rỗng nếu không có nút như vậy.""",
           focus=[1, "2.2", "2.8"]),
        st(code(KHO_RUN) + out(KHO_OUT, "Làm thử — kết quả chạy thật của mô phỏng"),
           """Làm thử, nút cấp ba có hai nút con là hai trang. Nút trang chủ có ba thuộc tính: kiểu nút chính, tiêu đề và kiểu tài nguyên.
           Còn đường dẫn có cả phần mở rộng thì không phải nút nào trong kho, nên hàm trả về rỗng. Vì vậy phải tách đường dẫn trước khi tìm.""",
           focus=["3.1", "3.2", "3.3", "3.3"], clear=True),
        st(code(TACH_PY, f"Bước 2. Tách đường dẫn theo cách của Sling ({SIM_T})"),
           """Bước hai là tách đường dẫn. Vì tên nút có thể chứa dấu chấm, nên nhìn chuỗi thôi thì không biết đường dẫn tài nguyên kết thúc ở đâu.
           Do đó hàm thử cắt tại từng dấu chấm và tại cuối chuỗi, rồi giữ điểm cắt xa nhất mà phần đầu là một nút có thật.
           Phần còn lại, tính tới dấu gạch chéo kế tiếp, được chia theo dấu chấm: khúc cuối là phần mở rộng, các khúc trước là bộ chọn.
           Phần từ dấu gạch chéo đó trở đi là hậu tố.""",
           focus=[1, 1, "2.3", "2.6", "2.7"], clear=True),
        st(code(TACH_RUN) + out(TACH_OUT, "Làm thử — kết quả chạy thật của mô phỏng"),
           """Làm thử với bốn đường dẫn. Đường dẫn thứ nhất cho đường dẫn tài nguyên là nút trang chủ, không có bộ chọn, và phần mở rộng trang.
           Đường dẫn thứ hai có thêm hai bộ chọn. Đường dẫn thứ ba có hậu tố nằm sau phần mở rộng.
           Đường dẫn thứ tư trỏ tới nút không có, nên hàm cắt ở dấu chấm đầu tiên, và bảng của đặc tả ghi trường hợp này là không có tài nguyên.""",
           focus=["1.1", "3.1", "3.2", "3.3", "3.4"], clear=True),
        st(code(CHON_PY, f"Bước 3. Chọn tệp dựng theo kiểu tài nguyên ({SIM_T})"),
           """Bước ba là chọn tệp dựng. Danh sách đầu là ba tệp dựng đang có, hai tệp của dự án và một tệp của sản phẩm.
           Tên tệp ứng viên lấy từ bộ chọn trước, rồi tới khúc cuối của kiểu tài nguyên, vì tệp khớp nhiều bộ chọn hơn thì được ưu tiên.
           Phần mở rộng trang được lược khỏi tên tệp, còn phần mở rộng khác thì phải ghi vào tên.
           Với mỗi tên, hàm tìm ở thư mục của dự án trước, rồi mới tới thư mục của sản phẩm.""",
           focus=[1, "2.1", "2.6", "2.5", "2.9"], clear=True),
        st(code(REQ_RUN) + out(REQ_OUT, "Làm thử — kết quả chạy thật của mô phỏng"),
           """Làm thử, ta ghép ba hàm: tách đường dẫn, tìm nút, đọc kiểu tài nguyên, rồi chọn tệp.
           Hai trang khác đường dẫn nhưng cùng kiểu tài nguyên, nên cùng dùng một tệp dựng.
           Cũng trang chủ đó, nhưng thêm bộ chọn, thì tệp dựng mang tên bộ chọn được dùng thay.""",
           focus=["1.3", "3.2", "3.3"], clear=True),
        st(code(HTL_TXT, "Bước 4. Tệp dựng HTL (đối chiếu đặc tả, không chạy; lienKet và mucCon là thuộc tính giả định)")
           + table(["phần", "nghĩa theo đặc tả HTL"],
                   [["data-sly-use.trang", "khởi tạo phần logic và đặt tên là trang để khuôn mẫu dùng"],
                    [f"{D}{{trang.tieuDe}}", "biểu thức; ở giữa thẻ thì tự thoát theo ngữ cảnh text"],
                    [f"href=\"{D}{{…}}\"", "tự xử lý theo ngữ cảnh uri: địa chỉ không hợp lệ thì không in gì"],
                    ["data-sly-list", "lặp nội dung của thẻ cho từng phần tử, tên mặc định là item"]])
           ,
           """Bước bốn, đây là một tệp dựng viết bằng ngôn ngữ khuôn mẫu. Ta chỉ đọc và đối chiếu với đặc tả, vì máy này không chạy được nó, và hai thuộc tính liên kết với danh sách là giả định, nút mẫu không có.
           Thuộc tính đầu tiên khởi tạo phần logic viết bằng Java, và đặt cho nó một tên để khuôn mẫu dùng.
           Biểu thức nằm giữa thẻ thì tự được thoát ký tự theo ngữ cảnh văn bản.
           Biểu thức nằm trong địa chỉ liên kết thì được kiểm theo ngữ cảnh địa chỉ, và địa chỉ không hợp lệ thì không in gì.
           Thuộc tính cuối lặp nội dung của thẻ cho từng phần tử của danh sách, với tên mặc định cho mỗi phần tử.""",
           focus=[1, 1, "3.2", "3.3", "3.4", "3.5"], clear=True),
        st(code(THOAT_PY, f"Bước 4 (tiếp). Tự thoát ký tự ở ngữ cảnh text ({SIM_T})") + out(THOAT_OUT),
           """Để thấy việc tự thoát, ta mô phỏng nó. Bảng đầu tiên đổi bốn ký tự đặc biệt thành mã vô hại, và hàm thoát duyệt từng ký tự nên không bao giờ thoát hai lần.
           Hàm dựng thay mỗi biểu thức bằng giá trị thuộc tính đã thoát.
           Kết quả chạy thật cho thấy đoạn mã lạ trong tiêu đề trang chủ đã thành chữ thường, nên trình duyệt chỉ hiện nó ra chứ không chạy.
           Tiêu đề trang vay không có ký tự đặc biệt nên giữ nguyên.""",
           focus=[1, "2.2", "2.5", "4.1", "4.2"], clear=True),
        st(table(["ngữ cảnh (context)", "dùng khi", "HTL làm gì (theo đặc tả)"],
                 [["text", "mặc định cho nội dung giữa các thẻ", "mã hoá mọi ký tự đặc biệt của HTML"],
                  ["attribute", "mặc định cho giá trị thuộc tính", "mã hoá mọi ký tự đặc biệt của HTML"],
                  ["uri", "liên kết và đường dẫn (href, src)", "kiểm địa chỉ; không hợp lệ thì không in gì"],
                  ["html", "cần in ra thẻ một cách an toàn", "lọc bỏ các thẻ nguy hiểm"],
                  ["unsafe", "khi mọi ngữ cảnh khác đều quá chặt", "tắt hẳn việc thoát ký tự và bảo vệ"]])
           + f"<span class='note'>Ghi đè bằng tuỳ chọn context, ví dụ <code>{D}{{properties.jcr:title @ context='text'}}</code>.</span>",
           """Bảng này là năm ngữ cảnh hay gặp. Ngữ cảnh văn bản là mặc định cho nội dung giữa các thẻ, và mã hoá mọi ký tự đặc biệt.
           Ngữ cảnh thuộc tính là mặc định cho giá trị thuộc tính, cũng mã hoá mọi ký tự đặc biệt.
           Ngữ cảnh địa chỉ dùng cho liên kết, nó kiểm địa chỉ và không in gì nếu địa chỉ không hợp lệ.
           Ngữ cảnh thứ tư dùng khi cần in ra thẻ, và nó lọc bỏ các thẻ nguy hiểm.
           Ngữ cảnh cuối tắt hẳn việc thoát ký tự và bảo vệ, nên chỉ dùng khi hiểu rõ rủi ro. Người viết có thể ghi đè ngữ cảnh bằng một tuỳ chọn trong biểu thức.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", 2], clear=True),
        st(code(MODEL_JAVA, "Bước 5. Lớp mô hình Sling Model (biên dịch được; chưa chạy trong máy chủ)"),
           """Bước năm là phần Java. Lớp mô hình mang chú thích cho biết nó tạo từ một tài nguyên, và trường tiêu đề đọc thuộc tính tiêu đề, tên ghi ngay trong chú thích, khớp với nút mẫu.
           Vì vậy logic nằm ở Java, còn khuôn mẫu chỉ lo hiển thị.""",
           focus=[1, 2, 2], clear=True),
        st(code(MANIFEST, "Tệp khai báo của gói chứa lớp đó (MANIFEST.MF)"),
           """Lớp này nằm trong một gói, và tệp khai báo của gói ghi tên gói, phiên bản, và các gói Java nó cần nhập từ gói khác.
           Dòng cuối liệt kê gói Java chứa các lớp mô hình, vì thiếu dòng đó thì lớp mô hình không được đăng ký.""",
           focus=[2, "2.7"], clear=True),
        st(code(GOI_PY, f"Bước 6. Vòng đời của gói và sổ dịch vụ ({SIM_T})"),
           """Bước sáu, ta mô phỏng vòng đời của gói. Mỗi gói nhớ tên, các gói nó cần, dịch vụ nó cấp, và vết các trạng thái đã qua, bắt đầu từ đã cài.
           Khi khởi động, nếu thiếu gói cần thì việc phân giải thất bại và hàm báo lỗi, nên gói đứng nguyên ở trạng thái đã cài.
           Nếu đủ, gói đi qua đã phân giải, đang khởi động, rồi đang chạy, và chỉ lúc đó mới ghi dịch vụ của mình vào sổ.""",
           focus=[1, "2.5", "2.9", "2.10"], clear=True),
        st(code(GOI_RUN) + out(GOI_OUT, "Làm thử — kết quả chạy thật của mô phỏng"),
           """Làm thử, gói thứ nhất có đủ gói cần, nên vết của nó đi từ đã cài, qua đã phân giải và đang khởi động, tới đang chạy, và sổ có một dịch vụ.
           Khi dừng, ta ghi thêm trạng thái đang dừng rồi đã phân giải, và gỡ dịch vụ khỏi sổ, nên sổ trống, vì dịch vụ của gói dừng bị gỡ.
           Gói thứ hai thiếu một gói cần, nên vết của nó chỉ có trạng thái đã cài, kèm thông báo thiếu gói nào.""",
           focus=["3.1", "3.2", "3.3"], clear=True),
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
           """Ta làm trọn một yêu cầu, tới trang chủ. Phép tính thứ nhất là tách. Chuỗi có một dấu chấm, nên có hai chỗ cắt để thử.
           Cắt ở cuối chuỗi thì không có nút nào mang tên đó. Cắt ở dấu chấm thì phần đầu là một nút có thật.
           Vậy đường dẫn tài nguyên là nút trang chủ, không có bộ chọn, và phần mở rộng là phần mở rộng trang."""),
        st("<p><b>② Tìm nút.</b> Dùng đường dẫn tài nguyên ở phép ①: đi <b>4</b> cấp content → site → vi → home. Nút home có <b>3</b> thuộc tính:</p>"
           + table(["thuộc tính của nút home", "giá trị"],
                   [["jcr:primaryType", "nt:unstructured"], ["jcr:title", TITLE_H], ["sling:resourceType", PG]]),
           """Phép tính thứ hai dùng lại đường dẫn tài nguyên vừa tách. Đi bốn cấp từ gốc thì tới nút trang chủ, và nút này có ba thuộc tính."""),
        st(f"""<div class="box"><b>③ Đọc kiểu.</b> Trong 3 thuộc tính ở phép ②: <code>sling:resourceType = {PG}</code>. Khúc cuối của kiểu là <b>page</b>.</div>""",
           """Phép tính thứ ba đọc thuộc tính kiểu tài nguyên trong ba thuộc tính đó. Giá trị của nó là một đường dẫn tương đối gồm ba khúc, và khúc cuối sẽ thành tên tệp.""",
           clear=True),
        st("<p><b>④ Chọn tệp.</b> Không có selector, phần mở rộng html được lược → tên tệp <b>page.html</b> (khúc cuối của kiểu ở phép ③).</p>"
           + table(["thứ tự tìm", "tệp ứng viên", "kết quả"],
                   [["1", f"/apps/{PG}/page.html", "có → chọn, dừng"], ["2", f"/libs/{PG}/page.html", "không cần xem tới"]]),
           """Phép tính thứ tư chọn tệp. Vì không có bộ chọn và phần mở rộng trang được lược, nên tên tệp là khúc cuối của kiểu ghép với đuôi của tệp khuôn mẫu.
           Tìm ở thư mục của dự án trước thì thấy ngay, nên dừng, không cần xem thư mục của sản phẩm.""",
           clear=True),
        st(f"""<div class="box"><b>⑤ Dựng.</b> Tệp page.html in tiêu đề của nút ở phép ②. Tiêu đề dài <b>34</b> ký tự, có <b>4</b> ký tự đặc biệt (2 dấu &lt;, 2 dấu &gt;); mỗi ký tự thành 4 ký tự:
<br><code>{TITLE_E}</code> dài <b>34 + 4 × 3 = 46</b> ký tự → trình duyệt hiện chữ, <span class="hl">không chạy mã</span>.
<br><span class="note">46 tính theo hàm mô phỏng chỉ thoát 4 ký tự &amp; &lt; &gt; ", không đo từ máy chủ thật.</span></div>
<div class="box key">Phần Java phía sau nằm trong một gói OSGi đã đi qua <b>INSTALLED → RESOLVED → ACTIVE</b> (qua STARTING trong chốc lát).</div>""",
           """Phép tính thứ năm là dựng trang. Tệp dựng in tiêu đề của nút, dài ba mươi tư ký tự, trong đó có bốn ký tự đặc biệt.
           Vì mỗi ký tự đặc biệt thành bốn ký tự, nên chuỗi sau khi thoát dài bốn mươi sáu ký tự, và trình duyệt chỉ hiện chữ, không chạy mã.
           Con số này tính theo hàm mô phỏng, không đo từ máy chủ thật.
           Còn phần Java phía sau nằm trong một gói đã đi qua ba trạng thái: đã cài, đã phân giải, rồi đang chạy.""",
           focus=[1, 1, 1, 1, 2], clear=True),
    ], checks=["'/content/site/vi/home.html'.count('.') == 1 and alg.bnx_l22_props('/content/site/vi/home.html') is None",
               "alg.bnx_l22_split('/content/site/vi/home.html')[:3] == ('/content/site/vi/home', [], 'html')",
               "alg.bnx_l22_depth(alg.bnx_l22_split('/content/site/vi/home.html')[0]) == 4 and len(alg.bnx_l22_props('/content/site/vi/home')) == 3",
               f"alg.bnx_l22_props('/content/site/vi/home')['sling:resourceType'] == '{PG}' and '{PG}'.split('/')[-1] == 'page'",
               f"alg.bnx_l22_resolve('/content/site/vi/home.html')[2] == '/apps/{PG}/page.html'",
               f"len({TITLE!r}) == 34 and alg.bnx_l22_escaped_count({TITLE!r}) == 4 and len(alg.bnx_l22_escape({TITLE!r})) == 34 + 4 * 3 == 46",
               "[s for s in alg.bnx_l22_bundle_trace([], set()) if s != 'STARTING'] == ['INSTALLED', 'RESOLVED', 'ACTIVE']"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: gỡ một tệp dựng, và so với bảng ví dụ của Apache Sling", [
        st(code(CHECK_RUN, f"Gỡ tệp page.html của dự án rồi hỏi lại ({SIM_T})") + out(CHECK_OUT),
           """Kiểm bằng đường khác. Nếu đúng là tìm ở thư mục của dự án trước, thì khi gỡ tệp ở đó, tệp của sản phẩm phải được dùng thay.
           Kết quả chạy thật đúng như vậy ở lần hỏi thứ nhất. Lần hỏi thứ hai có bộ chọn, nên vẫn ra tệp mang tên bộ chọn của dự án.
           Lần hỏi thứ ba dùng một kiểu tài nguyên không có tệp dựng nào, nên hàm trả về rỗng.""",
           focus=[1, "2.1", "4.1", "4.2", "4.3"]),
        st(table(["đường dẫn (bảng của Apache Sling, giả định có tài nguyên /a/b)", "tài nguyên", "selector", "mở rộng", "hậu tố"],
                 [["/a/b.s1.s2.html", "/a/b", "s1.s2", "html", "không"],
                  ["/a/b.html/c/d", "/a/b", "không", "html", "/c/d"],
                  ["/a/b/c/d.s.txt", "/a/b/c/d (không có)", "s", "txt", "không"],
                  ["/a/b.s1.html/c/d.s.txt", "/a/b", "s1", "html", "/c/d.s.txt"]])
           + "<span class='note'>Bảng ví dụ của Apache Sling có 14 hàng không dùng tham số đường dẫn; hàm tách của bài cho đúng cả <b>14</b> hàng.</span>",
           """Đường kiểm thứ hai là so với bảng ví dụ của chính nhóm làm ra tầng phân giải đường dẫn, với giả định chỉ có một tài nguyên.
           Hàng thứ nhất có hai bộ chọn. Hàng thứ hai có hậu tố sau phần mở rộng.
           Hàng thứ ba trỏ tới nút không có, nên đường dẫn tài nguyên chỉ được cắt ở dấu chấm đầu tiên. Hàng thứ tư có cả bộ chọn lẫn hậu tố chứa dấu chấm.
           Bảng đó có mười bốn hàng không dùng tham số đường dẫn, và hàm tách của bài cho đúng cả mười bốn hàng.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", 2], clear=True),
    ], checks=[f"alg.bnx_l22_script('{PG}', [], 'html', ['/apps/{PG}/in.html', '/libs/{PG}/page.html']) == '/libs/{PG}/page.html'",
               f"alg.bnx_l22_script('{PG}', ['in'], 'html', ['/apps/{PG}/in.html', '/libs/{PG}/page.html']) == '/apps/{PG}/in.html'",
               "alg.bnx_l22_script('site/components/khac', [], 'html') is None",
               f"sum(alg.bnx_l22_split(u, ['/a', '/a/b']) == (p, s, e, x, f) for u, p, s, e, x, f in {SLING_ROWS!r}) == 14",
               "alg.bnx_l22_split('/a/b/c/d.s.txt', ['/a', '/a/b']) == ('/a/b/c/d', ['s'], 'txt', None, False)"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ mỗi trang là một tệp HTML trên đĩa, và Sling chọn mã dựng theo <b>đường dẫn</b>.
<br><span class="note">Đúng: trang là dữ liệu trong kho nội dung (nút và thuộc tính). Đường dẫn chỉ để tìm tài nguyên; mã dựng được chọn theo <b>sling:resourceType</b>. Vì vậy 2 trang khác đường dẫn dùng chung 1 tệp page.html.</span></div>""",
           """Lỗi thứ nhất, của người mới, là nghĩ mỗi trang là một tệp trên đĩa, và mã dựng được chọn theo đường dẫn.
           Thật ra trang là dữ liệu trong kho nội dung. Đường dẫn chỉ để tìm tài nguyên, còn mã dựng được chọn theo kiểu tài nguyên, nên hai trang khác đường dẫn dùng chung một tệp dựng."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Cài gói xong, thấy không báo lỗi là yên tâm. Thật ra gói đang ở <b>INSTALLED</b> vì một gói trong Import-Package không có: việc phân giải thất bại, lệnh start ném BundleException, <b>không dịch vụ nào</b> được đăng ký.
<br><span class="note">Cách chữa: sau mỗi lần triển khai, đọc trạng thái từng gói. INSTALLED: tìm gói phụ thuộc còn thiếu. RESOLVED: gói đủ điều kiện nhưng chưa chạy. Chỉ <b>ACTIVE</b> mới cung cấp dịch vụ, nhưng ACTIVE chưa đủ: thành phần khai báo kiểu DS còn thiếu tham chiếu thì chưa đăng ký dịch vụ (OSGi Compendium §112.3); xem cả mục thành phần trong bảng điều khiển.</span></div>
<div class="box warn"><b>Cùng giai đoạn.</b> Sửa thẳng tệp dựng trong <code>/libs</code>. Nhánh này thay đổi mỗi khi nâng cấp, vá nóng hoặc cài gói tính năng, nên chỗ sửa có thể mất. Đúng: dựng lại cấu trúc tương ứng dưới <code>/apps</code>, vì <code>/apps</code> được tìm trước.</div>""",
           """Lỗi thứ hai, của người đã đi làm, hay gặp lúc mới dựng hệ thống. Cài gói xong, thấy không báo lỗi là yên tâm.
           Thật ra gói đang kẹt ở trạng thái đã cài, vì một gói nó cần nhập không có, nên việc phân giải thất bại và không dịch vụ nào được đăng ký.
           Cách chữa là sau mỗi lần triển khai, đọc trạng thái từng gói. Đã cài thì tìm gói phụ thuộc còn thiếu, đã phân giải thì gói chưa chạy, chỉ đang chạy mới có dịch vụ, mà vẫn chưa đủ nếu thành phần còn thiếu tham chiếu.
           Cũng ở giai đoạn này, có người sửa thẳng tệp dựng trong thư mục của sản phẩm.
           Nhánh đó thay đổi mỗi khi nâng cấp hay vá nóng, nên chỗ sửa có thể mất. Cách đúng là dựng lại cấu trúc tương ứng ở thư mục của dự án, vì nơi đó được tìm trước.""",
           focus=[1, 1, 1, 1, 1, 2, 2, 2], clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng và kho lớn dần).</b> Viết truy vấn tìm mọi nút theo một thuộc tính mà không có chỉ mục cho nó. Theo hướng dẫn của Apache Jackrabbit Oak, không có chỉ mục thì kho bị <b>duyệt qua</b>, và nhật ký ghi cảnh báo dạng “Traversed 10000 nodes with filter …”.
<br><span class="note">Kho mẫu của bài: tìm nút có kiểu site/components/page phải đọc cả <b>5</b> nút để ra <b>2</b> nút khớp. Kho thật có hàng triệu nút thì số nút phải đọc tăng theo. Cách chữa: tạo chỉ mục cho thuộc tính được truy vấn, và theo dõi cảnh báo đó trong nhật ký.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, lộ ra khi tải tăng và kho lớn dần. Đó là viết truy vấn tìm nút theo một thuộc tính mà không có chỉ mục cho nó.
           Theo hướng dẫn của nhóm làm ra kho nội dung, không có chỉ mục thì kho bị duyệt qua từng nút, và nhật ký ghi cảnh báo đã duyệt mười nghìn nút.
           Trong kho mẫu của bài, tìm nút theo kiểu tài nguyên phải đọc cả năm nút để ra hai nút khớp, và kho thật càng lớn thì số nút phải đọc càng tăng.
           Cách chữa là tạo chỉ mục cho thuộc tính được truy vấn, và theo dõi cảnh báo đó trong nhật ký.""",
           clear=True),
    ], checks=["len({alg.bnx_l22_resolve(u)[0] for u in ('/content/site/vi/home.html', '/content/site/vi/vay.html')}) == 2 and len({alg.bnx_l22_resolve(u)[2] for u in ('/content/site/vi/home.html', '/content/site/vi/vay.html')}) == 1",
               "alg.bnx_l22_bundle_trace(['p.q'], set())[-1] == 'INSTALLED' and not alg.bnx_l22_serves('INSTALLED')",
               "not alg.bnx_l22_serves('RESOLVED') and alg.bnx_l22_serves('ACTIVE')",
               f"alg.bnx_l22_script('{PG}', [], 'html').startswith('/apps/')",
               f"alg.bnx_l22_scan_cost('{PG}') == (5, 2)"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề (dùng kho mẫu và ba tệp dựng của bài)"],
                 [["1", "Yêu cầu /content/site/vi/vay.in.a4.html: đường dẫn tài nguyên, selector, phần mở rộng là gì? Tệp dựng nào được chọn?"],
                  ["2", "Gói A cần nhập gói p.q, nhưng không gói nào đang cài cung cấp p.q. Gọi start thì A ở trạng thái nào, có dịch vụ không? Gói B đang ACTIVE bị stop thì về trạng thái nào?"],
                  ["3", f"Quyết định: biên tập viên muốn chữ <b>in đậm</b> trong tiêu đề, nên nhập cả thẻ. Chọn <code>context='html'</code> hay <code>context='unsafe'</code> cho biểu thức in tiêu đề?"]]),
           """Đến lượt bạn. Câu một, với yêu cầu đang hiện, đường dẫn tài nguyên, bộ chọn và phần mở rộng là gì, và tệp dựng nào được chọn?
           Câu hai, gói A cần nhập một gói Java mà không gói nào đang cài cung cấp. Gọi lệnh khởi động thì gói A ở trạng thái nào, có dịch vụ không? Còn gói B đang chạy mà bị dừng thì về trạng thái nào?
           Câu ba, biên tập viên muốn chữ in đậm trong tiêu đề nên nhập cả thẻ. Nên chọn ngữ cảnh lọc thẻ nguy hiểm, hay ngữ cảnh tắt hẳn bảo vệ? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st(f"""<div class="box"><b>Câu 1.</b> Cắt ở dấu chấm đầu tiên thì <code>/content/site/vi/vay</code> là nút có thật → đường dẫn tài nguyên. Phần còn lại <code>in.a4.html</code>: selector <b>in, a4</b>; phần mở rộng <b>html</b>.
<br>Kiểu của nút vay: {PG}. Tên ứng viên: in/a4.html (không có) → <b>in.html</b> (có ở /apps) → chọn <code>/apps/{PG}/in.html</code>.</div>""",
           """Đáp án câu một. Cắt ở dấu chấm đầu tiên thì phần đầu là nút trang vay có thật, nên đó là đường dẫn tài nguyên. Phần còn lại cho hai bộ chọn và phần mở rộng trang.
           Nút trang vay có cùng kiểu tài nguyên với trang chủ. Tên ứng viên khớp cả hai bộ chọn thì không có, nên tới tên khớp bộ chọn đầu, và tệp đó có ở thư mục của dự án."""),
        st("""<div class="box"><b>Câu 2.</b> Thiếu p.q → không phân giải được → start báo lỗi, gói A đứng ở <b>INSTALLED</b>, <b>0</b> dịch vụ.
<br>Gói B: ACTIVE → STOPPING → <b>RESOLVED</b>; dịch vụ của B bị gỡ khỏi sổ.</div>""",
           """Đáp án câu hai. Thiếu gói cần nhập thì không phân giải được, nên lệnh khởi động báo lỗi, gói A đứng ở trạng thái đã cài và không có dịch vụ nào.
           Gói B đi từ đang chạy, qua đang dừng, về đã phân giải, và dịch vụ của nó bị gỡ khỏi sổ."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["context='html'", "thẻ in đậm vẫn hiện; thẻ nguy hiểm bị lọc bỏ", "một số thẻ biên tập viên muốn có thể bị lọc; phải thử trước"],
                  ["context='unsafe'", "nhập gì hiện nấy, không phải thử", "tắt hẳn bảo vệ: một đoạn mã lạ trong tiêu đề sẽ chạy trên máy khách"]]),
           """Đáp án câu ba. Ngữ cảnh lọc thẻ vẫn cho thẻ in đậm hiện ra, mà thẻ nguy hiểm bị lọc bỏ. Đổi lại, một số thẻ biên tập viên muốn có thể bị lọc, nên phải thử trước.
           Ngữ cảnh tắt bảo vệ thì nhập gì hiện nấy, nhưng một đoạn mã lạ trong tiêu đề sẽ chạy trên máy của khách.
           Vì trang ngân hàng không được phép chạy mã lạ, nên chọn ngữ cảnh lọc thẻ."""),
    ], checks=["alg.bnx_l22_split('/content/site/vi/vay.in.a4.html') == ('/content/site/vi/vay', ['in', 'a4'], 'html', None, True)",
               f"alg.bnx_l22_resolve('/content/site/vi/vay.in.a4.html') == ('/content/site/vi/vay', '{PG}', '/apps/{PG}/in.html')",
               "alg.bnx_l22_bundle_trace(['p.q'], {'x.y'}) == ['INSTALLED'] and not alg.bnx_l22_serves(alg.bnx_l22_bundle_trace(['p.q'], {'x.y'})[-1])",
               "[alg.bnx_l22_bundle_step('ACTIVE', 'stop'), alg.bnx_l22_bundle_step('STOPPING', 'stopped')] == ['STOPPING', 'RESOLVED']"])

    rec = sc("recap", "recap", "Chuỗi logic, góc phỏng vấn & tư duy cần mang theo", [
        st(chain("JCR: trang là nút và thuộc tính", "Sling: đường dẫn → tài nguyên", "sling:resourceType → tệp dựng, /apps trước /libs", "HTL: tự thoát theo ngữ cảnh", "Sling Model: logic ở Java", "OSGi: chỉ ACTIVE mới có dịch vụ"),
           """Tổng kết chuỗi logic. Trang là nút và thuộc tính trong kho nội dung. Tầng nhận yêu cầu đổi đường dẫn thành tài nguyên.
           Kiểu tài nguyên quyết định tệp dựng, và thư mục của dự án được tìm trước thư mục của sản phẩm.
           Ngôn ngữ khuôn mẫu tự thoát ký tự theo ngữ cảnh, còn logic nằm ở lớp mô hình viết bằng Java.
           Lớp đó sống trong một gói, và chỉ gói đang chạy mới cung cấp dịch vụ.""",
           focus=[0, "1.1", "1.3", "1.5", "1.7", "1.11"]),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["Một yêu cầu tới trang AEM được xử lý thế nào?", "Sling tách đường dẫn, tìm tài nguyên trong JCR, đọc sling:resourceType (AEM: nút cq:Page, thuộc tính ở nút con jcr:content), chọn tệp dựng HTL (tìm /apps trước /libs)"],
                  ["Sling Model và HTL chia việc ra sao?", "Sling Model là lớp Java gắn @Model(adaptables=Resource.class), nạp thuộc tính của tài nguyên; HTL gọi nó bằng data-sly-use và chỉ lo hiển thị, tự thoát theo ngữ cảnh"],
                  ["Gói OSGi triển khai xong mà không chạy, bạn xem gì?", "trạng thái gói: INSTALLED là chưa phân giải được, thường do thiếu gói trong Import-Package; RESOLVED là chưa chạy; chỉ ACTIVE mới đăng ký dịch vụ, và thành phần DS thiếu tham chiếu thì ACTIVE vẫn chưa có dịch vụ"]])
           + "<p><span class='note'>Trả lời bằng cơ chế; không nêu số liệu của dự án hay tổ chức thật. Bài này là mô phỏng theo đặc tả công khai, không thay cho việc thực hành trên máy chủ AEM.</span></p>",
           """Đây là ba câu người phỏng vấn hay hỏi về dòng này trên hồ sơ xin việc. Hỏi một yêu cầu tới trang được xử lý thế nào, thì trả lời theo bốn bước: tách đường dẫn, tìm tài nguyên, đọc kiểu tài nguyên, chọn tệp dựng.
           Hỏi lớp mô hình và khuôn mẫu chia việc ra sao, thì trả lời lớp mô hình nạp thuộc tính của tài nguyên, còn khuôn mẫu gọi nó và chỉ lo hiển thị.
           Hỏi gói triển khai xong mà không chạy thì xem gì, thì trả lời xem trạng thái gói, tìm gói phụ thuộc còn thiếu, rồi xem thành phần của gói có đủ tham chiếu chưa.
           Hãy trả lời bằng cơ chế, và nhớ rằng bài này là mô phỏng, không thay cho việc thực hành trên máy chủ thật.""",
           focus=[0, "1.2", "1.3", "1.4", 2], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> gặp một hệ lớn, hỏi ba điều: <b>dữ liệu</b> nằm ở đâu, <b>luật nào</b> chọn mã để chạy, và mã đó đang ở <b>trạng thái</b> nào.</div>""",
           """Điều cần mang theo. Gặp một hệ lớn, hãy hỏi ba điều: dữ liệu nằm ở đâu, luật nào chọn mã để chạy, và mã đó đang ở trạng thái nào.""",
           clear=True),
        st("""<p class='small'>Bài sau: huấn luyện rừng cô lập để tìm giao dịch lạ, rồi xuất mô hình sang ONNX Runtime.</p>""",
           """Ở bài sau, ta huấn luyện một rừng cô lập để tìm giao dịch lạ, rồi xuất mô hình và chấm điểm giao dịch bằng ONNX Runtime.""",
           forward_ref=True),
    ], checks=[f"alg.bnx_l22_resolve('/content/site/vi/home.html') == ('/content/site/vi/home', '{PG}', '/apps/{PG}/page.html')",
               "alg.bnx_l22_serves('ACTIVE') and not alg.bnx_l22_serves('RESOLVED')"])
    return lesson("L22", "aem_jcr_sling_htl_osgi",
                  "Bài 22 — Adobe Experience Manager: JCR, Sling phân giải đường dẫn, thành phần HTL và gói OSGi",
                  "curriculum/bnx.yaml L22; audit/bnx/verify_bnx.py L22; audit/bnx/sources_l22.md (đọc 2026-11-12): Apache Sling “URL decomposition”, "
                  "“Servlets and Scripts”, “Scripting”, “Sling Models”; “Resources”; đặc tả HTL (github.com/adobe/htl-spec); "
                  "OSGi Core Release 8 chương Life Cycle, Module, Service; JCR 2.0 (JSR 283) chương 3 Repository Model; Apache Jackrabbit Oak “Query Engine”; "
                  "Adobe AEM 6.5 “Overlays”. Máy không có máy chủ AEM: cơ chế dạy bằng mô phỏng Python theo tài liệu; mã HTL, Java, MANIFEST chỉ đọc đối chiếu",
                  ["Đọc một cây nội dung JCR gồm nút và thuộc tính",
                   "Lần theo cách Sling đổi một đường dẫn thành tài nguyên rồi chọn tệp dựng trang",
                   "Đọc một đoạn HTL và nói vì sao nó tự thoát ký tự theo ngữ cảnh",
                   "Kể vòng đời của một gói OSGi và vai trò của dịch vụ"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
