import lib2
from lib2 import *
from libj import jstep, nowrap, JROW

BS = chr(92)


def R(k, say):
    """Hàng của khuôn libj.JROW với lời đọc rút gọn (bài này nhiều bảng, giữ lời đọc ≤ 2300 từ)."""
    return (JROW[k][0], JROW[k][1], say)


# ── Mã hiện trên màn hình (audit/bnx/screen/l17.yaml, audit/bnx/ver/l17.py chạy NGUYÊN VĂN) ──
# J_CFG + J_RUN: Spring Security 7.1.2 THẬT (jar ở audit/bnx/deps/l17, tải từ Maven Central), chạy bằng SH_RUN, không cần máy chủ web:
#   yêu cầu giả của spring-test (MockHttpServletRequest) đi qua đúng chuỗi bộ lọc mà Spring Security dựng.
# J_LB: MÔ PHỎNG Java thuần của sổ đăng ký + chia tải xoay vòng (không phải Spring Cloud). PY_CHECK: bảng quyết định viết tay.
# Y_*: cấu hình chép từ tài liệu chính thức (audit/bnx/sources_l17.md), KHÔNG chạy trên máy này.
J_CFG = r'''
import static java.nio.charset.StandardCharsets.UTF_8;
import jakarta.servlet.*;
import java.io.IOException;
import javax.crypto.spec.SecretKeySpec;
import org.springframework.context.annotation.*;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.*;
import org.springframework.security.config.annotation.web.configuration.*;
import org.springframework.security.oauth2.jwt.*;
import org.springframework.security.oauth2.server.resource.web.authentication.*;
import org.springframework.security.web.SecurityFilterChain;
@Configuration
@EnableWebSecurity
public class CauHinh {
  static final String KHOA = "khoa-hoc-tap-chi-dai-32-byte-001";
  @Bean
  SecurityFilterChain chuoi(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(q -> q
        .requestMatchers("/han-muc").hasAuthority("SCOPE_han_muc")
        .anyRequest().authenticated());
    http.oauth2ResourceServer(m -> m.jwt(Customizer.withDefaults()));
    http.addFilterAfter(new TramQuanSat(),
        BearerTokenAuthenticationFilter.class);
    return http.build();
  }
  @Bean
  JwtDecoder giaiMa() {                // kiểm chữ ký bằng khoá chung
    var khoa = new SecretKeySpec(KHOA.getBytes(UTF_8), "HmacSHA256");
    return NimbusJwtDecoder.withSecretKey(khoa).build();
  }
  static class TramQuanSat implements Filter {   // trạm quan sát
    public void doFilter(ServletRequest q, ServletResponse d,
        FilterChain c) throws IOException, ServletException {
      System.out.println("  qua trạm quan sát");
      c.doFilter(q, d);
    }
  }
}
'''

J_RUN = r'''
import static java.nio.charset.StandardCharsets.UTF_8;
import jakarta.servlet.Filter;
import java.util.Base64;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import org.springframework.mock.web.*;
import org.springframework.security.web.FilterChainProxy;
import org.springframework.web.context.support.*;
public class ChayThu {
  static Filter chuoi;
  static String ky(String than, String khoa) throws Exception {
    var b = Base64.getUrlEncoder().withoutPadding();
    String p = b.encodeToString("{\"alg\":\"HS256\"}".getBytes(UTF_8))
        + "." + b.encodeToString(than.getBytes(UTF_8));
    Mac m = Mac.getInstance("HmacSHA256");
    m.init(new SecretKeySpec(khoa.getBytes(UTF_8), "HmacSHA256"));
    return p + "." + b.encodeToString(m.doFinal(p.getBytes(UTF_8)));
  }
  static void thu(String ten, String pt, String ma) throws Exception {
    System.out.println(ten);
    var q = new MockHttpServletRequest(pt, "/han-muc");
    if (ma != null) q.addHeader("Authorization", "Bearer " + ma);
    var d = new MockHttpServletResponse();
    chuoi.doFilter(q, d,
        (x, y) -> System.out.println("  tới dịch vụ"));
    System.out.println("  mã trạng thái " + d.getStatus());
    String h = d.getHeader("WWW-Authenticate");
    if (h != null) System.out.println("  " + h);
  }
  public static void main(String[] a) throws Exception {
    var ctx = new AnnotationConfigWebApplicationContext();
    ctx.setServletContext(new MockServletContext());
    ctx.register(CauHinh.class);
    ctx.refresh();
    chuoi = ctx.getBean("springSecurityFilterChain", Filter.class);
    int i = 0;
    for (Filter f : ((FilterChainProxy) chuoi).getFilters("/han-muc"))
      System.out.println(++i + " " + f.getClass().getSimpleName());
    String k = CauHinh.KHOA, han = ",\"exp\":4102444800}";
    String an = ky("{\"scope\":\"so_du\"" + han, k);
    String binh = ky("{\"scope\":\"so_du han_muc\"" + han, k);
    String gia = ky("{\"scope\":\"han_muc\"" + han,
        "khoa-cua-ke-gian-dai-32-byte-002");
    String cu = ky("{\"scope\":\"han_muc\",\"exp\":1700000000}", k);
    thu("A. không mang mã", "GET", null);
    thu("B. mã ký bằng khoá khác", "GET", gia);
    thu("C. mã thật, thiếu quyền", "GET", an);
    thu("D. mã thật, đủ quyền", "GET", binh);
    thu("E. mã thật, đã hết hạn", "GET", cu);
    thu("F. lệnh POST, không mang mã", "POST", null);
    thu("G. lệnh POST, đủ quyền", "POST", binh);
  }
}
'''

SH_RUN = r'''
D=/d/research-video/audit/bnx/deps/l17
ls $D/spring-security-web-7.1.2.jar >/dev/null 2>&1 || { echo "NOT_VERIFIED: thiếu jar" >&2; exit 97; }
mkdir -p lib && cp $D/*.jar lib/
javac -encoding UTF-8 -cp "lib/*" -d out CauHinh.java ChayThu.java
java -Dstdout.encoding=UTF-8 -cp "out;lib/*" ChayThu
'''

J_LB = r'''
import java.util.*;
public class ChiaTai {   // MÔ PHỎNG, không phải Spring Cloud
  record Ban(String ten, boolean khoe) { }
  static Map<String, Integer> chia(List<Ban> so, int n) {
    List<Ban> song = so.stream().filter(Ban::khoe).toList();
    Map<String, Integer> dem = new TreeMap<>();
    for (int i = 0; i < n; i++) {
      Ban b = song.get(i % song.size());   // xoay vòng
      dem.merge(b.ten(), 1, Integer::sum);
    }
    return dem;
  }
  public static void main(String[] a) {
    List<Ban> so = List.of(new Ban("bản 1", true),
        new Ban("bản 2", true), new Ban("bản 3", true));
    System.out.println("ba bản khoẻ: " + chia(so, 100));
    so = List.of(new Ban("bản 1", true),
        new Ban("bản 2", false), new Ban("bản 3", true));
    System.out.println("bản 2 trượt: " + chia(so, 100));
  }
}
'''

PY_CHECK = r'''
def kiem(ma, quyen_can):
    if ma is None:
        return 401                     # chưa biết bạn là ai
    if not ma["chu_ky_dung"] or ma["het_han"]:
        return 401                     # mã không tin được
    if quyen_can not in ma["quyen"]:
        return 403                     # biết rồi nhưng không cho
    return 200
an = {"chu_ky_dung": True, "het_han": False, "quyen": ["so_du"]}
binh = dict(an, quyen=["so_du", "han_muc"])
gia, cu = dict(binh, chu_ky_dung=False), dict(binh, het_han=True)
print([kiem(m, "han_muc") for m in (None, gia, an, binh, cu)])
print(100 // 2, [len(range(i, 100, 3)) for i in range(3)])
'''

Y_RS = r'''
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://idp.example.com/issuer
'''

Y_GW = r'''
spring:
  cloud:
    gateway:
      server:
        webflux:
          routes:
          - id: myRoute
            uri: lb://service
            predicates:
            - Path=/service/**
'''

Y_CONSUL = r'''
spring:
  cloud:
    consul:
      discovery:
        healthCheckInterval: 15s
'''

Y_CIPHER = r'''
spring:
  datasource:
    username: dbuser
    password: '{cipher}FKSAJDFGYOS8F7GLHAKERGFHLSAJ'
'''

# Đầu ra THẬT, đầy đủ, của SH_RUN (Spring Security 7.1.2, Spring Framework 7.0.10, Temurin JDK 21.0.13, Windows 11, 2026-11-11; 3 lần chạy giống nhau)
OUT_SPRING = r'''
1 DisableEncodeUrlFilter
2 WebAsyncManagerIntegrationFilter
3 SecurityContextHolderFilter
4 HeaderWriterFilter
5 CsrfFilter
6 LogoutFilter
7 OAuth2ProtectedResourceMetadataFilter
8 BearerTokenAuthenticationFilter
9 TramQuanSat
10 RequestCacheAwareFilter
11 SecurityContextHolderAwareRequestFilter
12 AnonymousAuthenticationFilter
13 ExceptionTranslationFilter
14 AuthorizationFilter
A. không mang mã
  qua trạm quan sát
  mã trạng thái 401
  Bearer resource_metadata="http://localhost/.well-known/oauth-protected-resource"
B. mã ký bằng khoá khác
  mã trạng thái 401
  Bearer error="invalid_token", error_description="An error occurred while attempting to decode the Jwt: Signed JWT rejected: Invalid signature", error_uri="https://tools.ietf.org/html/rfc6750#section-3.1", resource_metadata="http://localhost/.well-known/oauth-protected-resource"
C. mã thật, thiếu quyền
  qua trạm quan sát
  mã trạng thái 403
  Bearer error="insufficient_scope", error_description="The request requires higher privileges than provided by the access token.", error_uri="https://tools.ietf.org/html/rfc6750#section-3.1"
D. mã thật, đủ quyền
  qua trạm quan sát
  tới dịch vụ
  mã trạng thái 200
E. mã thật, đã hết hạn
  mã trạng thái 401
  Bearer error="invalid_token", error_description="An error occurred while attempting to decode the Jwt: Jwt expired at 2023-11-14T22:13:20Z", error_uri="https://tools.ietf.org/html/rfc6750#section-3.1", resource_metadata="http://localhost/.well-known/oauth-protected-resource"
F. lệnh POST, không mang mã
  mã trạng thái 403
G. lệnh POST, đủ quyền
  qua trạm quan sát
  tới dịch vụ
  mã trạng thái 200
'''

# Các đoạn hiện trên màn hình: dòng dài cắt bằng "…" (cổng screen_code so từng dòng với OUT_SPRING, đúng thứ tự)
OUT_CHAIN = """
1 DisableEncodeUrlFilter
…
5 CsrfFilter
…
8 BearerTokenAuthenticationFilter
9 TramQuanSat
…
12 AnonymousAuthenticationFilter
13 ExceptionTranslationFilter
14 AuthorizationFilter
"""
OUT_A = """
A. không mang mã
  qua trạm quan sát
  mã trạng thái 401
  Bearer resource_metadata=…
"""
OUT_B = """
B. mã ký bằng khoá khác
  mã trạng thái 401
  Bearer error="invalid_token", …Invalid signature…
"""
OUT_C = """
C. mã thật, thiếu quyền
  qua trạm quan sát
  mã trạng thái 403
  Bearer error="insufficient_scope", …
"""
OUT_D = """
D. mã thật, đủ quyền
  qua trạm quan sát
  tới dịch vụ
  mã trạng thái 200
"""
OUT_E = """
E. mã thật, đã hết hạn
  mã trạng thái 401
  Bearer error="invalid_token", …Jwt expired at 2023-11-14T22:13:20Z…
"""
OUT_FG = """
F. lệnh POST, không mang mã
  mã trạng thái 403
G. lệnh POST, đủ quyền
  qua trạm quan sát
  tới dịch vụ
  mã trạng thái 200
"""
OUT_LB = """
ba bản khoẻ: {bản 1=34, bản 2=33, bản 3=33}
bản 2 trượt: {bản 1=50, bản 3=50}
"""
OUT_CHECK = """
[401, 401, 403, 200, 401]
50 [34, 33, 33]
"""

from l16 import _spoken  # noqa: E402  (ghép câu quá ngắn vào câu bên cạnh, giữ focus)

T_NONE = "None"
T_AN = "{'sig': True, 'expired': False, 'scopes': ['so_du']}"
T_BINH = "{'sig': True, 'expired': False, 'scopes': ['so_du', 'han_muc']}"
T_GIA = "{'sig': False, 'expired': False, 'scopes': ['han_muc']}"
T_CU = "{'sig': True, 'expired': True, 'scopes': ['han_muc']}"


# ── AF2 (WP4, 2026-11-14): cảnh quy mô + Tự làm ──
lib2.begin("L17")
P_CT = prog("ChiaTai", J_LB, lang="java", claims=["ba bản khoẻ: 100 yêu cầu chia 34, 33, 33", "bản 2 trượt: bản 1 và bản 3 mỗi bản 50"])

J_QUYMO = r'''
public class CuaSoLoi {  // MÔ PHỎNG, không phải Spring Cloud
  static long loi(long tocDo, int giay, int soBan) {
    long roi = 0;
    for (long i = 0; i < tocDo * giay; i++)
      if (i % soBan == 0) roi++;     // bản số 0 đã chết, vẫn trong danh sách
    return roi;
  }
  public static void main(String[] a) {
    for (long r : new long[] {100, 10_000, 1_000_000})
      System.out.println(r + " yeu cau/giay, 45 giay: "
          + loi(r, 45, 3) + " loi");
  }
}
'''
P_QUYMO = prog("CuaSoLoi", J_QUYMO, lang="java", timeout=120,
               claims=["3 bản, 1 bản chết còn trong danh sách 45 giây: 1 500; 150 000; 15 000 000 yêu cầu lỗi ở 100; 10 000; 1 000 000 yêu cầu mỗi giây (mô phỏng)"])

# Lab (số liệu khác ví dụ): đường /chuyen-tien đòi quyền chuyen_tien; 6 ca; 250 yêu cầu chia cho 3 bản khoẻ trong 4 bản
LAB_PY = r'''
def kiem(ma, duong):
    if ma is None:
        return 401
    if not ma["chu_ky_dung"] or ma["het_han"]:
        return 401
    if duong == "/chuyen-tien" and "chuyen_tien" not in ma["quyen"]:
        return 403
    return 200


an = {"chu_ky_dung": True, "het_han": False, "quyen": ["so_du"]}
binh = dict(an, quyen=["so_du", "chuyen_tien"])
gia = dict(binh, chu_ky_dung=False)
cu = dict(binh, het_han=True)
ca = [(None, "/so-du"), (gia, "/so-du"), (cu, "/chuyen-tien"),
      (an, "/so-du"), (an, "/chuyen-tien"), (binh, "/chuyen-tien")]
for i, (ma, duong) in enumerate(ca, 1):
    print(f"ca {i}: {kiem(ma, duong)}")

ban = {"b1": True, "b2": False, "b3": True, "b4": True}
khoe = [t for t, ok in ban.items() if ok]
dem = {t: 0 for t in khoe}
for i in range(250):
    dem[khoe[i % len(khoe)]] += 1
print(" ".join(f"{t}={n}" for t, n in dem.items()))
'''
LAB_OUT = """ca 1: 401
ca 2: 401
ca 3: 401
ca 4: 200
ca 5: 403
ca 6: 200
b1=84 b3=83 b4=83"""

LAB_DE = """# Lab BNX L17 — Bảng quyết định 401/403 và chia xoay vòng cho các bản khoẻ

Viết `mau.py` (Python, không cần cài thêm gì). Đây là **mô hình Python** của bảng quyết định và phép chia tải, không chạy Spring. Số liệu là số minh hoạ.

**Phần 1 — bảng quyết định.** Hàm `kiem(ma, duong)` trả về mã trạng thái, theo luật: đường `/chuyen-tien` đòi quyền `chuyen_tien`, mọi đường khác chỉ cần đã xác thực.
`ma` là `None` (không mang mã) hoặc một từ điển `{"chu_ky_dung": bool, "het_han": bool, "quyen": [...]}`. Luật theo thứ tự: không mã → 401; chữ ký sai hoặc đã hết hạn → 401;
đường `/chuyen-tien` mà `quyen` thiếu `chuyen_tien` → 403; còn lại → 200.
Dựng 4 mã: `an` (chữ ký đúng, còn hạn, quyền `["so_du"]`), `binh` (như `an` nhưng quyền `["so_du", "chuyen_tien"]`), `gia` (như `binh` nhưng chữ ký sai), `cu` (như `binh` nhưng đã hết hạn).
Rồi gọi hàm cho 6 ca theo thứ tự: (không mã, `/so-du`), (`gia`, `/so-du`), (`cu`, `/chuyen-tien`), (`an`, `/so-du`), (`an`, `/chuyen-tien`), (`binh`, `/chuyen-tien`), in `ca <i>: <mã trạng thái>`.

**Phần 2 — chia xoay vòng.** Có 4 bản dịch vụ `b1, b2, b3, b4`, trong đó `b2` trượt kiểm sức khoẻ. Chia **250 yêu cầu** xoay vòng chỉ cho các bản khoẻ
(yêu cầu thứ i, đếm từ 0, giao cho bản khoẻ thứ i chia lấy dư cho số bản khoẻ). In một dòng `b1=<n> b3=<n> b4=<n>`.

In đúng 7 dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh BNX L17 mau.py`.
"""


def build():
    hook = sc("hook", "hook", "Ba yêu cầu tới cùng một địa chỉ: 401, 403 và 200", [
        st("""<p>Dịch vụ hạn mức của một ngân hàng nhận <b>ba yêu cầu</b> tới cùng một địa chỉ <code>/han-muc</code>:</p>
<div class="box key">Không mang mã truy cập: bị chặn, nhận <b>401</b>. Có mã hợp lệ nhưng thiếu quyền: nhận <b>403</b>. Đủ quyền: nhận <b>200</b>.<br>Ai chặn, chặn ở đâu, và vì sao hai lần từ chối mang hai con số khác nhau?</div>
<p>Dịch vụ chạy <b>ba bản</b> giống nhau; một bản trượt kiểm sức khoẻ thì 100 yêu cầu chia cho 2 bản còn lại, mỗi bản <b>50</b>.</p>""",
           """Chào bạn, dịch vụ hạn mức nhận ba yêu cầu tới cùng một địa chỉ. Không mang mã thì nhận bốn trăm lẻ một, mã hợp lệ nhưng thiếu quyền thì bốn trăm lẻ ba, đủ quyền thì hai trăm. Vì sao hai lần từ chối mang hai con số khác nhau? Dịch vụ chạy ba bản, một bản trượt thì một trăm yêu cầu chia hai bản còn lại, mỗi bản năm mươi.""",
           focus=[1, 1, 1, 2]),
    ], checks=[f"alg.bnx_l17_status('GET', {T_NONE}, 'han_muc') == 401", f"alg.bnx_l17_status('GET', {T_AN}, 'han_muc') == 403",
               f"alg.bnx_l17_status('GET', {T_BINH}, 'han_muc') == 200",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]", "sum([True, False, True]) == 3 - 1 == 2"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① mã truy cập", "chuỗi có <b>chữ ký</b> (dãy ký tự tính từ nội dung và khoá bí mật; sửa nội dung thì lệch) do máy chủ cấp mã; mang hạn dùng, <b>phạm vi quyền</b> (scope)", "scope <code>so_du han_muc</code>: 2 quyền"],
                  ["② mã trạng thái", "con số máy chủ trả về cho mỗi yêu cầu", "200: xong; 401: chưa xác thực; 403: bị cấm"],
                  ["③ bean", "đối tượng do Spring tạo và giữ; khai bằng nhãn <code>@Bean</code>", "một bean giữ luật bảo mật, một bean kiểm chữ ký"],
                  ["④ bản dịch vụ", "một tiến trình đang chạy của cùng một dịch vụ; nhiều bản để chịu tải và chịu lỗi", "3 bản, 1 bản hỏng: còn 3 − 1 = 2 bản phục vụ"],
                  ["⑤ xác thực và phân quyền", "xác thực: biết người gọi là ai; phân quyền: xét người đó có được làm việc này không", "mã hỏng là lỗi xác thực; mã tốt mà thiếu quyền là lỗi phân quyền"]]),
           """Trước hết ta cần hiểu năm điều. Mã truy cập là chuỗi có chữ ký, tức dãy ký tự tính từ nội dung và khoá bí mật, nên sửa nội dung là chữ ký lệch; mã còn mang hạn dùng và phạm vi quyền. Mã trạng thái: hai trăm là xong, bốn trăm lẻ một là chưa xác thực, bốn trăm lẻ ba là bị cấm. Bản dịch vụ là một tiến trình đang chạy. Xác thực là biết ai gọi, phân quyền là xét có được làm không."""),
        st("""<p>Làm thử: 3 bản đăng ký, 1 bản hỏng, 100 yêu cầu chia đều.</p>
$$3 - 1 = 2 \\text{ bản}; \\qquad 100 : 2 = \\hl{50} \\text{ yêu cầu mỗi bản}; \\qquad \\text{còn đủ 3 bản thì } 100 = 34 + 33 + 33$$""",
           """Làm thử với ba bản đăng ký, một bản hỏng: còn hai bản nên một trăm yêu cầu chia mỗi bản năm mươi. Đủ ba bản thì chia ra ba mươi tư, ba mươi ba, ba mươi ba.""", clear=True),
    ], checks=["alg.bnx_l17_authorities('so_du han_muc') == ['SCOPE_so_du', 'SCOPE_han_muc']",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]",
               "alg.bnx_l17_round_robin([True, True, True], 100) == [34, 33, 33]", "sum(alg.bnx_l17_round_robin([True] * 3, 100)) == 100"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên trong Spring Security", "nghĩa"],
                 [["Filter, SecurityFilterChain", "<b>bộ lọc</b> là một trạm: nhận yêu cầu, làm một việc, rồi chuyển tiếp hoặc trả lời luôn; <b>chuỗi bộ lọc</b> là danh sách trạm có thứ tự"],
                  ["BearerTokenAuthenticationFilter", "<b>trạm đọc mã</b>: lấy mã truy cập trong yêu cầu và kiểm nó"],
                  ["AuthorizationFilter, ExceptionTranslationFilter", "<b>trạm kiểm quyền</b> so quyền với luật của đường dẫn; <b>trạm dịch lỗi</b> đổi lỗi của nó thành 401 hoặc 403"],
                  ["SCOPE_han_muc", "quyền sinh từ phạm vi <code>han_muc</code> trong mã; tiền tố <code>SCOPE_</code> do Spring thêm"]]),
           """Bảng này giải mã tên của phần bảo mật. Bộ lọc là một trạm, chuỗi bộ lọc là danh sách trạm có thứ tự. Trạm đọc mã kiểm mã, trạm kiểm quyền so quyền với luật, trạm dịch lỗi đổi lỗi thành mã trạng thái.""", clear=True),
        st(table(["tên trong Spring Cloud", "nghĩa"],
                 [["Spring Cloud Gateway", "<b>cổng</b>: cửa vào chung, nhận yêu cầu rồi chuyển tới đúng dịch vụ"],
                  ["Consul", "<b>sổ đăng ký dịch vụ</b>: mỗi bản tự ghi tên, địa chỉ; sổ kiểm sức khoẻ từng bản"],
                  ["<code>lb://ten-dich-vu</code>", "địa chỉ theo <b>tên</b>: cổng tra sổ lấy các bản rồi chia tải (load balance)"],
                  ["Spring Cloud Config", "<b>cấu hình tập trung</b>: một máy chủ giữ cấu hình cho mọi dịch vụ"]]),
           """Cổng là cửa vào chung, sổ đăng ký là nơi mỗi bản tự ghi tên và được kiểm sức khoẻ. Địa chỉ theo tên khiến cổng tra sổ rồi chia tải, còn cấu hình tập trung giữ cấu hình chung.""", clear=True, introduces=['bnx_consul']),
    ], checks=["alg.bnx_l17_authorities('han_muc') == ['SCOPE_han_muc']"])

    def tram(i, col=C_GRAY, bold=False):
        return box(40 + (i - 1) * 100, 80, 90, 70, str(i), col, 26, bold)

    def nhan(i, s):
        return txt(85 + (i - 1) * 100, 185, s, 20)

    intu = sc("intuition", "intuition", "Hình dung: chuỗi trạm trước dịch vụ, và cổng trước các bản", [
        st(svg(1500, 500,
               txt(750, 40, "14 trạm của chuỗi bộ lọc đứng trước dịch vụ (thứ tự in ra từ lần chạy thật)", 26, "middle", "#1f2937", True),
               "".join(tram(i) for i in (1, 2, 3, 4, 6, 7, 10, 11, 12)),
               tram(5, C_AMBER), tram(8, C_BLUE, True), tram(9, C_GRAY), tram(13, C_PURPLE, True), tram(14, C_GREEN, True),
               nhan(5, "chống giả mạo"), nhan(8, "đọc mã"), nhan(9, "quan sát"), nhan(13, "dịch lỗi"), nhan(14, "kiểm quyền"),
               arrow(1385, 215, 1385, 262), box(1270, 265, 200, 60, "dịch vụ", C_GREEN, 24, True),
               txt(60, 270, "không mang mã: qua trạm 8, trạm 14 ném lỗi, trạm 13 trả 401", 24, "start", "#dc2626"),
               txt(60, 320, "mã hỏng (sai chữ ký, hết hạn): trạm 8 trả 401 ngay, không đi tiếp", 24, "start", "#dc2626"),
               txt(60, 370, "mã tốt, thiếu quyền: trạm 14 ném lỗi, trạm 13 trả 403", 24, "start", "#d97706"),
               txt(60, 420, "mã tốt, đủ quyền: qua cả 14 trạm, tới dịch vụ, 200", 24, "start", "#16a34a"),
               txt(750, 475, "Xác thực (trạm 8) đứng trước phân quyền (trạm 14): phải biết ai gọi rồi mới xét cho hay không", 24, "middle", "#1f2937", True)),
           """Hình này là mười bốn trạm của chuỗi bộ lọc. Không mang mã thì trạm mười ba trả bốn trăm lẻ một, mã hỏng thì trạm tám trả bốn trăm lẻ một ngay, mã tốt mà thiếu quyền thì trạm mười ba trả bốn trăm lẻ ba."""),
        st(svg(1500, 550,
               txt(750, 40, "Spring Cloud: cổng tra sổ đăng ký rồi chia tải cho các bản khoẻ", 26, "middle", "#1f2937", True),
               box(40, 230, 220, 70, ["ứng dụng", "khách"], C_GRAY, 22),
               box(420, 220, 280, 90, ["cổng", "Spring Cloud Gateway"], C_BLUE, 22, True),
               arrow(265, 265, 415, 265, "#475569", "100 yêu cầu", 20),
               box(400, 70, 320, 80, ["sổ đăng ký dịch vụ", "Consul"], C_PURPLE, 22, True),
               arrow(560, 216, 560, 156, "#475569"), txt(575, 192, "tra sổ", 20, "start"),
               box(1080, 80, 360, 70, "bản 1: khoẻ, nhận 50", C_GREEN, 22),
               box(1080, 230, 360, 70, "bản 2: trượt, nhận 0", C_RED, 22),
               box(1080, 380, 360, 70, "bản 3: khoẻ, nhận 50", C_GREEN, 22),
               arrow(705, 245, 1075, 125), arrow(705, 285, 1075, 410),
               arrow(725, 95, 1075, 95, "#9333ea", "kiểm sức khoẻ định kỳ", 20, True),
               box(400, 400, 320, 80, ["máy chủ cấu hình", "Spring Cloud Config"], C_AMBER, 22, True),
               arrow(560, 396, 560, 316, "#d97706", None, 20, True), txt(575, 365, "cấu hình", 20, "start"),
               txt(750, 535, "Nếu sổ chỉ trả bản khoẻ: bản 2 trượt bị loại, 100 : 2 = 50 mỗi bản", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là Spring Cloud. Khách chỉ biết cổng, cổng tra sổ đăng ký rồi chia xoay vòng cho các bản khoẻ, nên bản hai trượt bị loại và mỗi bản nhận năm mươi. Máy chủ cấu hình giữ cấu hình chung."""),
    ], checks=["alg.bnx_l17_chain_len() == 14", "alg.bnx_l17_pos('CsrfFilter') == 5", "alg.bnx_l17_pos('BearerTokenAuthenticationFilter') == 8",
               "alg.bnx_l17_pos('TramQuanSat') == 9", "alg.bnx_l17_pos('ExceptionTranslationFilter') == 13",
               "alg.bnx_l17_pos('AuthorizationFilter') == 14",
               f"alg.bnx_l17_trace('GET', {T_NONE}, 'han_muc') == (401, 'ExceptionTranslationFilter', True, False)",
               f"alg.bnx_l17_trace('GET', {T_GIA}, 'han_muc') == (401, 'BearerTokenAuthenticationFilter', False, False)",
               f"alg.bnx_l17_trace('GET', {T_CU}, 'han_muc')[:2] == (401, 'BearerTokenAuthenticationFilter')",
               f"alg.bnx_l17_trace('GET', {T_AN}, 'han_muc') == (403, 'ExceptionTranslationFilter', True, False)",
               f"alg.bnx_l17_trace('GET', {T_BINH}, 'han_muc') == (200, None, True, True)",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]"])

    form = sc("formula", "formula", "Suy ra từng bước: từ một trạm tới cả hệ thống", [
        st("""<p><b>Bước 1.</b> Bảo mật có nhiều việc khác nhau, gộp vào một chỗ thì khó thay từng phần, nên Spring Security chia thành <b>chuỗi trạm có thứ tự</b>. Thứ tự là luật: trạm xác thực phải đứng <b>trước</b> trạm phân quyền.</p>
<p>Làm thử: trạm đọc mã ở vị trí 8, trạm kiểm quyền ở vị trí 14.</p>
$$8 < 14 \\;\\Rightarrow\\; \\text{khi tới trạm kiểm quyền, đã biết người gọi là ai (hoặc biết là vô danh)}$$""",
           """Bước một, bảo mật chia thành chuỗi trạm có thứ tự để thay được từng phần, và trạm đọc mã ở vị trí tám phải đứng trước trạm kiểm quyền ở vị trí mười bốn.""",
           clear=True),
        st("""<p><b>Bước 2.</b> Trạm đọc mã chỉ lo <b>xác thực</b>: mã hỏng thì trả <b>401</b> ngay; không có mã thì cho đi tiếp như <b>khách vô danh</b>. Trạm kiểm quyền (14) chỉ biết ném lỗi từ chối; trạm dịch lỗi (13) bọc ngoài, hỏi người gọi đã xác thực chưa.</p>"""
           + table(["người gọi", "ai trả lời", "mã"],
                   [["không mang mã (vô danh)", "trạm dịch lỗi (13)", "<b>401</b>: chưa biết bạn là ai"],
                    ["mã sai chữ ký hoặc hết hạn", "trạm đọc mã (8)", "<b>401</b>: mã không tin được"],
                    ["mã tốt, thiếu quyền", "trạm dịch lỗi (13)", "<b>403</b>: biết rồi nhưng không cho"]]),
           """Bước hai, trạm đọc mã chỉ lo xác thực: mã hỏng thì trả bốn trăm lẻ một vì không tin được, không có mã thì cho đi tiếp như khách vô danh. Trạm dịch lỗi hỏi người gọi đã xác thực chưa: vô danh thì bốn trăm lẻ một, đã xác thực mà thiếu quyền thì bốn trăm lẻ ba.""",
           focus=[1, 1, 2, 2], clear=True),
        st("""<p><b>Bước 3.</b> Dịch vụ tự kiểm mã, không hỏi lại máy chủ cấp mã mỗi lần, nên cần <b>khoá để kiểm chữ ký</b>. Khai địa chỉ máy chủ cấp mã, dịch vụ tự lấy <b>khoá công khai</b> ở đó (khoá chỉ để kiểm chữ ký, ai cũng biết được; chỉ <b>khoá riêng</b> của máy chủ cấp mã mới ký được): dịch vụ như thế gọi là <b>máy chủ tài nguyên</b>.</p>"""
           + code(Y_RS, "application.yml (chép từ hướng dẫn của Spring Security, không chạy trên máy này)")
           + """<p>Làm thử: scope <code>so_du han_muc</code> cho 2 quyền <code>SCOPE_so_du</code>, <code>SCOPE_han_muc</code>. Mặc định chỉ kiểm nơi cấp và hạn.</p>""",
           """Bước ba, dịch vụ tự kiểm mã nên cần khoá kiểm chữ ký. Dòng cuối khai địa chỉ máy chủ cấp mã để dịch vụ tự lấy khoá công khai, vì chỉ khoá riêng mới ký được. Dịch vụ như thế gọi là máy chủ tài nguyên.""",
           focus=[1, "3.6", 1, 4], clear=True),
        jstep([(R("yflow", "Trong YAML, dòng bắt đầu bằng gạch ngang là một phần tử của danh sách."), "<code>routes:</code> rồi <code>- id: myRoute</code>: một tuyến trong danh sách", ""),
               (("<code>uri: lb://service</code>, <code>- Path=/service/**</code>", "<code>lb://service</code>: địa chỉ theo tên dịch vụ, cổng tra sổ rồi chia tải; <code>Path=/service/**</code>: khớp mọi đường dẫn bắt đầu bằng <code>/service/</code>", "Địa chỉ theo tên để cổng tra sổ rồi chia tải, điều kiện khớp mọi đường dẫn cùng đầu."), "", "")]),
        st("""<p><b>Bước 4.</b> Địa chỉ các bản thay đổi liên tục, nên cổng ghi <b>tên dịch vụ</b> rồi tra sổ lấy các bản khoẻ; yêu cầu thứ $i$ giao cho bản thứ $i$ chia lấy dư cho số bản khoẻ.</p>"""
           + code(Y_GW, "application.yml của cổng (theo hướng dẫn của Spring Cloud Gateway, không chạy ở đây)"),
           """Bước bốn, địa chỉ các bản thay đổi liên tục, nên cổng ghi tên dịch vụ rồi tra sổ lấy các bản khoẻ. Yêu cầu thứ i giao cho bản thứ i chia lấy dư cho số bản khoẻ.""",
           clear=True),
        st("""<p>Làm thử: yêu cầu số chẵn về bản đầu, yêu cầu số lẻ về bản sau.</p>
$$6 \\text{ yêu cầu}, 2 \\text{ bản khoẻ}: \\quad 6 : 2 = \\hl{3} \\text{ yêu cầu mỗi bản}$$""",
           """Làm thử với hai bản khoẻ, sáu yêu cầu thì các yêu cầu số chẵn về bản đầu, số lẻ về bản sau, nên mỗi bản nhận ba yêu cầu.""",
           clear=True),
        st(table(["mảnh của Spring Cloud", "giữ gì", "vì sao cần"],
                 [["cổng", "luật định tuyến: đường dẫn nào về dịch vụ nào", "khách chỉ cần biết một địa chỉ"],
                  ["sổ đăng ký dịch vụ", "tên, địa chỉ và sức khoẻ của từng bản", "bản thêm vào hay chết đi, không ai phải sửa cấu hình"],
                  ["cấu hình tập trung", "cấu hình của mọi dịch vụ ở một nơi", "đổi một chỗ, không sửa từng bản"]]),
           """Bước năm, cổng giữ luật định tuyến, sổ đăng ký giữ sức khoẻ từng bản nên thêm hay mất bản không ai sửa cấu hình, và cấu hình tập trung cho đổi một chỗ.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l17_pos('BearerTokenAuthenticationFilter') == 8 < alg.bnx_l17_pos('AuthorizationFilter') == 14",
               "alg.bnx_l17_pos('ExceptionTranslationFilter') == 13",
               f"alg.bnx_l17_trace('GET', {T_NONE}, 'han_muc')[2] is True and alg.bnx_l17_trace('GET', {T_GIA}, 'han_muc')[2] is False",
               f"alg.bnx_l17_status('GET', {T_GIA}, 'han_muc') == 401 and alg.bnx_l17_status('GET', {T_CU}, 'han_muc') == 401",
               f"alg.bnx_l17_status('GET', {T_NONE}, 'han_muc') == 401 and alg.bnx_l17_status('GET', {T_AN}, 'han_muc') == 403",
               "len(alg.bnx_l17_authorities('so_du han_muc')) == 2",
               "alg.bnx_l17_round_robin([True, True], 6) == [3, 3]", "[i % 2 for i in range(6)] == [0, 1, 0, 1, 0, 1]"])

    ex = sc("example", "example", "Ví dụ chạy thật Spring Security, từng phép tính", [
        st(code(J_CFG, "CauHinh.java (1/4): các lệnh nhập thư viện, gõ đủ từng dòng", lines=(1, 11))
           + """<p class="note"><code>@Configuration</code> đánh dấu lớp khai báo bean; <code>@EnableWebSecurity</code> bật bảo mật web; <code>q -&gt; …</code> là một hàm nhỏ không tên.</p>""",
           """Tệp cấu hình mở đầu bằng các lệnh nhập thư viện, gõ lại đúng từng dòng.""", clear=True),
        jstep([(R("class", "Lớp là khối chứa hàm và dữ liệu giữa cặp ngoặc nhọn."), "<code>public class CauHinh { … }</code>", ""),
               (("<code>SecurityFilterChain chuoi(HttpSecurity http) throws Exception</code>", "hàm tên <code>chuoi</code>: nhận <code>http</code>, trả về chuỗi bộ lọc; <code>throws Exception</code>: có thể ném lỗi", "Hàm nhận cấu hình bảo mật, trả về chuỗi bộ lọc, có thể ném lỗi."), "kiểu trả về đứng trước tên hàm", ""),
               ]),
        st(code(J_CFG, "CauHinh.java (2/4): luật bảo mật của dịch vụ hạn mức", lines=(12, 21)),
           """Ta chạy thật bộ khung bảo mật của Spring bản bảy chấm một. Hàm có nhãn khai chuỗi bộ lọc: đường dẫn hạn mức đòi quyền hạn mức, đường khác chỉ cần đã xác thực.""", clear=True),
        st(code(J_CFG, "CauHinh.java (3/4): trạm quan sát và bộ kiểm chữ ký", lines=(22, 30))
           + """<p class="note">Bài thử dùng <b>khoá chung</b> của hai bên cho gọn; cấu hình thật ở bước ba (<code>issuer-uri</code>) lấy <b>khoá công khai</b> nên không phải giữ bí mật khoá kiểm.</p>""",
           """Ta chèn một trạm quan sát ngay sau trạm đọc mã, và khai bộ kiểm chữ ký bằng khoá chung. Chữ ký tính bằng mã băm có khoá, mà mã băm là dãy ký tự ngắn sinh từ dữ liệu.""", clear=True, introduces=["bnx_ma_bam"]),
        jstep([(R("impl", "Lớp cam kết có đủ các hàm mà giao diện liệt kê."), "<code>static class TramQuanSat implements Filter</code>", ""),
               (("<code>public void doFilter(ServletRequest q, ServletResponse d, FilterChain c) throws IOException, ServletException</code>", "hàm của trạm: nhận yêu cầu <code>q</code>, trả lời <code>d</code> và phần chuỗi còn lại <code>c</code>; <code>throws</code> liệt kê hai loại lỗi có thể ném; <code>c.doFilter(q, d)</code> chuyển yêu cầu sang trạm sau", "Hàm của trạm nhận yêu cầu, rồi lệnh chuyển tiếp đẩy yêu cầu sang trạm sau."), "trạm in một câu rồi gọi <code>c.doFilter</code>", "")]),
        st(code(J_CFG, "CauHinh.java (4/4): trạm quan sát chỉ in một câu rồi chuyển tiếp", lines=(31, 38)),
           """Trạm quan sát chỉ in một câu rồi chuyển tiếp, nên yêu cầu nào không in câu này đã bị chặn từ trạm đọc mã trở về trước.""", clear=True),
        st(code(J_RUN, "ChayThu.java (1/6): nhập thư viện, mở lớp, khai biến giữ chuỗi bộ lọc", lines=(1, 10))
           + """<p class="note"><code>Base64</code> (base64url): viết byte thành ký tự chữ và số an toàn trong đường dẫn.</p>""",
           """Tệp chạy thử nhập thư viện, mở lớp và khai biến giữ chuỗi bộ lọc dùng chung.""", clear=True, introduces=["bnx_base64url"]),
        jstep([(("<code>static String ky(String than, String khoa) throws Exception</code>", "hàm tên <code>ky</code>: trả về một chuỗi chữ, nhận hai chuỗi là phần thân và khoá", "Hàm ký trả về chuỗi chữ, nhận phần thân và khoá."), "<code>ky(…)</code> cho ra mã truy cập", ""),
               (("<code>var b = Base64.getUrlEncoder().withoutPadding();</code>", "<code>var</code>: để máy tự suy ra kiểu của biến từ vế phải", "Biến không ghi kiểu thì máy suy ra kiểu từ vế phải."), "<code>b</code> là bộ đổi byte sang chữ", ""),
               (('<code>"{' + BS + '"alg' + BS + '":' + BS + '"HS256' + BS + '"}"</code>', "trong chuỗi Java, dấu gạch ngược đặt trước dấu nháy kép để nháy đó là chữ thường, không kết thúc chuỗi", "Gạch ngược trước dấu nháy kép làm nháy đó thành chữ thường trong chuỗi."), '<code>{"alg":"HS256"}</code>: chuỗi thật', "")]),
        st(code(J_RUN, "ChayThu.java (2/6): hàm ký mã truy cập bằng khoá chung", lines=(11, 18)) + """<p class="note"><code>Base64</code> (base64url): viết byte thành ký tự chữ và số an toàn trong đường dẫn; <code>Mac</code> tính chữ ký băm có khoá.</p>""",
           """Hàm ký dựng mã truy cập từ ba phần: phần đầu ghi thuật toán, phần thân ghi hạn dùng và quyền, rồi chữ ký.""", clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>\"GET\"</code>, <code>\"POST\"</code>", "phương thức của yêu cầu mạng: GET là lệnh đọc dữ liệu, POST là lệnh ghi (tạo hoặc đổi dữ liệu)"],
                  ["<code>Authorization: Bearer …</code>", "tiêu đề (dòng thông tin kèm yêu cầu) mang mã truy cập; Bearer nghĩa là ai cầm mã này thì được nhận quyền ghi trong mã"],
                  ["<code>WWW-Authenticate</code>", "tiêu đề trong trả lời từ chối: máy chủ nói muốn xác thực kiểu nào và vì sao mã bị loại"]]),
           """Trước khi đọc hàm gửi yêu cầu, ta cần ba từ. Lệnh đọc và lệnh ghi là hai phương thức của yêu cầu mạng, tiêu đề cầm mã mang mã truy cập, và tiêu đề trả lời báo kiểu xác thực máy chủ muốn.""", clear=True),
        st(code(J_RUN, "ChayThu.java (3/6): gửi một yêu cầu qua chuỗi và in kết quả", lines=(19, 29)),
           """Hàm chạy thử tạo yêu cầu giả, đẩy qua chuỗi bộ lọc không cần máy chủ thật, rồi in mã trạng thái.""", clear=True),
        jstep([(("<code>var ctx = new AnnotationConfigWebApplicationContext();</code>", "tạo mới một đối tượng Spring giữ mọi bean; <code>var</code>: máy tự suy ra kiểu của biến", "Dòng này tạo mới đối tượng Spring giữ mọi bean."), "", ""),
               (R("foreach", "Dấu hai chấm duyệt từng phần tử của dãy, theo thứ tự."), "<code>for (Filter f : …getFilters(\"/han-muc\"))</code>: f là từng trạm", ""),
               (R("cast", "Ép kiểu bảo máy coi giá trị theo sau là kiểu trong ngoặc."), "<code>(FilterChainProxy) chuoi</code>; <code>++i</code> tăng i thêm 1 rồi mới lấy giá trị", "")]),
        st(code(J_RUN, "ChayThu.java (4/6): hàm chính dựng Spring rồi in chuỗi bộ lọc", lines=(30, 38)),
           """Hàm chính dựng Spring, xin chuỗi bộ lọc rồi in tên từng trạm theo đúng thứ tự.""", clear=True),
        st(code(J_RUN, "ChayThu.java (5/6): bốn mã thử và năm ca đầu", lines=(39, 49))
           + """<p class="note"><code>exp</code> là hạn dùng, tính bằng số giây từ 1/1/1970 (giờ Unix): 4102444800 là năm 2100, 1700000000 là ngày 14/11/2023.</p>""",
           """Ta tự ký bốn mã: của An chỉ có quyền số dư, của Bình có thêm quyền hạn mức, mã giả ký bằng khoá kẻ gian, mã cũ đã hết hạn.""", clear=True),
        st(code(J_RUN, "ChayThu.java (6/6): hai ca ghi cuối và dấu đóng", lines=(50, 53)),
           """Hai ca cuối gửi lệnh ghi, rồi hai dấu ngoặc đóng hàm chính và lớp.""", clear=True),
        st(table(["tệp jar trong thư mục lib", "để làm gì"],
                 [["spring-security-web, -config, -core, -crypto 7.1.2", "chuỗi bộ lọc và cấu hình bảo mật"],
                  ["spring-security-oauth2-resource-server, -jose, -core 7.1.2; nimbus-jose-jwt 10.9.1", "đọc và kiểm mã truy cập có chữ ký"],
                  ["spring-core, -beans, -context, -aop, -expression, -web, -test 7.0.10", "bộ khung Spring và yêu cầu giả để thử"],
                  ["jakarta.servlet-api 6.1.0, micrometer-commons, -observation 1.17.2, commons-logging 1.3.5, jspecify 1.0.1", "thư viện phụ mà các jar trên cần"]])
           + """<p class="note">Tải về từ Maven Central (kho thư viện Java công khai, địa chỉ <code>repo1.maven.org/maven2</code>): 20 tệp jar, đặt hết vào thư mục <code>lib</code>; lệnh biên dịch ở bước sau có <code>-cp "lib/*"</code>: <code>-cp</code> là đường tìm thư viện (classpath), <code>lib/*</code> là mọi tệp jar trong thư mục đó.</p>""",
           """Thư mục thư viện phải có hai mươi tệp đóng gói, tải từ kho thư viện công khai.""", clear=True, introduces=["bnx_classpath"]),
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>javac … -d out</code>", "biên dịch mã Java; <code>-d out</code> ghi các tệp đã biên dịch vào thư mục <code>out</code>"],
                  ["<code>java -Dstdout.encoding=UTF-8</code>", "chạy chương trình; <code>-D</code> đặt một thông số cho Java, ở đây để in chữ có dấu đúng"],
                  ["<code>-cp \"out;lib/*\"</code>", "đường tìm lớp; dấu <code>;</code> ngăn hai đường trên Windows (Linux và macOS dùng <code>:</code>)"]]),
           """Hai lệnh sắp chạy có vài cờ: một cờ ghi ra thư mục kết quả, một cờ đặt thông số cho Java, dấu chấm phẩy ngăn hai đường tìm.""", clear=True),
        st(code(SH_RUN, "Biên dịch và chạy (thư viện Spring nằm trong thư mục lib)", lines=(4, 5)) + out(OUT_CHAIN, "Kết quả chạy thật (lược bớt bằng dấu …)"),
           """Kết quả chạy thật in chuỗi mười bốn trạm: trạm đọc mã ở vị trí tám, trạm quan sát của ta ngay sau, trạm dịch lỗi ở mười ba.""",
           focus=[2, 4, ["4.3", "4.5", "4.6"], ["4.9", "4.10"]], clear=True),
        st(out(OUT_A) + """
$$① \\; \\text{không mã} \\Rightarrow \\text{qua trạm 8; trạm 14 từ chối, trạm 13 thấy vô danh} \\Rightarrow \\hl{401}$$""",
           """Phép tính thứ nhất, không mang mã: bị trạm kiểm quyền từ chối, và vì còn vô danh nên nhận bốn trăm lẻ một.""", clear=True),
        st(out(OUT_B, "Ca mã ký bằng khoá khác") + out(OUT_E, "Ca mã thật nhưng đã hết hạn") + """
$$② \\; \\text{mã hỏng hoặc hết hạn} \\Rightarrow \\text{dừng ở trạm 8} \\Rightarrow \\hl{401}$$""",
           """Phép tính thứ hai: mã ký sai khoá và mã đã hết hạn đều dừng ngay ở trạm đọc mã, không có câu quan sát, và nhận bốn trăm lẻ một.""", clear=True),
        st(out(OUT_C) + out(OUT_D) + """
$$③ \\; \\text{mã tốt, thiếu quyền} \\Rightarrow \\text{trạm 14 từ chối, trạm 13 thấy đã xác thực} \\Rightarrow \\hl{403}$$
$$④ \\; \\text{đủ quyền} \\Rightarrow \\text{qua cả 14 trạm} \\Rightarrow \\hlg{200}$$""",
           """Phép tính thứ ba: mã của An chỉ có quyền số dư nên nhận bốn trăm lẻ ba. Phép tính thứ tư: mã của Bình đủ quyền nên nhận hai trăm.""", clear=True),
        jstep([(("<code>record Ban(String ten, boolean khoe) { }</code>", "lớp dữ liệu gọn: khai các trường, Java tự có hàm tạo và hàm đọc cùng tên (<code>b.ten()</code>, <code>b.khoe()</code>)", "Lớp dữ liệu gọn chỉ khai các trường, còn hàm tạo và hàm đọc tự có."), "một bản có tên và cờ khoẻ", ""),
               (("<code>so.stream().filter(Ban::khoe).toList()</code>", "giữ các bản mà <code>khoe</code> đúng, gom lại thành danh sách; <code>Ban::khoe</code> viết gọn cho <code>b -&gt; b.khoe()</code>", "Dòng này giữ những bản khoẻ rồi gom thành danh sách, hai dấu hai chấm viết gọn tên hàm."), "bản trượt bị loại", "")]),
        jstep([(("<code>Map&lt;String, Integer&gt; dem = new TreeMap&lt;&gt;();</code> <code>dem.merge(b.ten(), 1, Integer::sum)</code>", "bảng tra từ tên bản tới số yêu cầu, xếp theo tên; <code>merge</code>: chưa có khoá thì đặt 1, có rồi thì cộng thêm 1", "Bảng tra đếm yêu cầu từng bản, có rồi thì cộng một."), "{bản 1=34, …}", ""),
               (R("div", "Phần dư cho biết bản kế tiếp, xoay vòng."), "<code>song.get(i % song.size())</code>: i chia số bản khoẻ lấy dư", "")]),
        st(code(J_LB, "ChiaTai.java (1/2) — MÔ PHỎNG bằng Java thuần, không phải Spring Cloud", lines=(1, 12)) + """<p class="note">Bộ chia thật của Spring Cloud bắt đầu từ một vị trí ngẫu nhiên, nên bản nhận dư không cố định là bản 1.</p>""",
           """Phần chia tải là mô phỏng bằng Java thuần, không dựng cổng thật: lọc các bản khoẻ rồi giao yêu cầu xoay vòng.""", clear=True),
        st(code(J_LB, "ChiaTai.java (2/2): ba bản khoẻ, rồi bản 2 trượt", lines=(13, 21)) + out(OUT_LB, "Kết quả chạy thật của mô phỏng") + """
$$⑤ \\; 3 - 1 = 2 \\text{ bản khoẻ}; \\quad 100 : 2 = \\hlg{50} \\text{ mỗi bản}$$""",
           """Đủ ba bản khoẻ thì bản một nhận ba mươi tư, hai bản kia ba mươi ba. Phép tính thứ năm: bản hai trượt, còn hai bản, một trăm chia hai là năm mươi.""", clear=True),
    ], checks=["alg.bnx_l17_chain_len() == 14 and alg.bnx_l17_pos('CsrfFilter') == 5",
               "alg.bnx_l17_pos('BearerTokenAuthenticationFilter') == 8 and alg.bnx_l17_pos('TramQuanSat') == 9",
               "alg.bnx_l17_pos('ExceptionTranslationFilter') == 13 and alg.bnx_l17_pos('AuthorizationFilter') == 14",
               f"alg.bnx_l17_trace('GET', {T_NONE}, 'han_muc') == (401, 'ExceptionTranslationFilter', True, False)",
               f"alg.bnx_l17_trace('GET', {T_GIA}, 'han_muc') == (401, 'BearerTokenAuthenticationFilter', False, False)",
               f"alg.bnx_l17_trace('GET', {T_CU}, 'han_muc') == (401, 'BearerTokenAuthenticationFilter', False, False)",
               f"alg.bnx_l17_trace('GET', {T_AN}, 'han_muc') == (403, 'ExceptionTranslationFilter', True, False)",
               f"alg.bnx_l17_trace('GET', {T_BINH}, 'han_muc') == (200, None, True, True)",
               "alg.bnx_l17_round_robin([True, True, True], 100) == [34, 33, 33]",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: bảng quyết định viết tay", [
        jstep([(R("pdef", "Khai hàm Python gồm tên, tham số, dấu hai chấm, và thân thụt vào."), "<code>def kiem(ma, quyen_can):</code>", ""),
               (R("pnone", "Giá trị rỗng là chưa có gì, và phép không thuộc đúng khi không có trong dãy."), "<code>if ma is None:</code> trả 401 khi không mang mã", ""),
               (("<code>not ma[\"chu_ky_dung\"] or ma[\"het_han\"]</code>", "<code>ma[\"…\"]</code>: giá trị của khoá trong từ điển; <code>not</code> đảo đúng thành sai; <code>or</code> đúng nếu một vế đúng; <code>x not in ma[\"quyen\"]</code>: x không có trong danh sách quyền", "Ngoặc vuông lấy giá trị theo khoá, chữ không đảo đúng sai, chữ hoặc đúng nếu một vế đúng."), "", "")]),
        st(code(PY_CHECK, "Bảng quyết định bằng Python, không dùng Spring", lines=(1, 8)),
           """Ta kiểm bằng đường khác, không dùng Spring: viết bảng quyết định thành một hàm. Không mã hoặc mã hỏng thì bốn trăm lẻ một vì không tin được, thiếu quyền thì bốn trăm lẻ ba, còn lại hai trăm.""", clear=True),
        jstep([(("<code>dict(an, quyen=[…])</code>", "bản sao của từ điển <code>an</code>, thay giá trị của khoá <code>quyen</code>; <code>gia, cu = x, y</code> gán hai biến một lúc", "Bản sao của từ điển với một khoá đổi giá trị, và gán hai biến một lúc."), "", ""),
               (("<code>[len(range(i, 100, 3)) for i in range(3)]</code>", "danh sách sinh sẵn: với i là 0, 1, 2 đếm các số từ i tới trước 100 cách nhau 3, tức số yêu cầu về bản i; <code>100 // 2</code>: chia lấy phần nguyên", "Danh sách sinh sẵn lặp i từ không tới hai, đếm các số cách nhau ba, nên ra số yêu cầu mỗi bản."), "", "")]),
        st(code(PY_CHECK, "(tiếp) năm ca như chương trình Java, và phép chia tải", lines=(9, 13)) + out(OUT_CHECK),
           """Hàm cho năm mã trạng thái và phép chia tải khớp Spring chạy thật, nên ta tin cách hiểu.""", clear=True),
    ], checks=[f"[alg.bnx_l17_status('GET', t, 'han_muc') for t in ({T_NONE}, {T_GIA}, {T_AN}, {T_BINH}, {T_CU})] == [401, 401, 403, 200, 401]",
               "100 // 2 == 50 and [len(range(i, 100, 3)) for i in range(3)] == alg.bnx_l17_round_robin([True] * 3, 100) == [34, 33, 33]",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]",
               "alg.bnx_l17_pos('ExceptionTranslationFilter') == 13 and alg.bnx_l17_pos('BearerTokenAuthenticationFilter') == 8"])

    quymo = sc("quymo", "example", "Khi lưu lượng lớn dần: bản chết còn trong danh sách", [
        jstep([(R("for", "Vòng lặp đếm gồm biến đếm, điều kiện còn lặp, bước sau mỗi vòng."), "<code>for (long i = 0; i &lt; tocDo * giay; i++)</code>", ""),
               (("<code>if (i % soBan == 0) roi++;</code>", "<code>%</code>: phần dư; dư 0 thì <code>roi++</code> tăng đếm thêm 1: cứ soBan yêu cầu có một yêu cầu về bản số 0", "Phần dư bằng không thì tăng đếm một, nên cứ ba yêu cầu có một lỗi."), "soBan = 3: i = 0, 3, 6…", ""),
               (("<code>for (long r : new long[] {100, 10_000, 1_000_000})</code>", "duyệt ba tốc độ; dấu gạch dưới trong số chỉ để dễ đọc", "Vòng này duyệt ba tốc độ, gạch dưới chỉ để dễ đọc."), "", "")]),
        st(P_QUYMO.show(title="CuaSoLoi.java — MÔ PHỎNG: yêu cầu rơi vào bản đã chết nhưng chưa bị loại") + """<p class="note">35 giây (thời gian sống của bộ đệm) và 10 giây (chu kỳ kiểm sức khoẻ) là số minh hoạ, không phải số mặc định đã kiểm.</p>""",
           """Ta đo bằng mô phỏng nhỏ, không phải Spring Cloud. Bản số không đã chết nhưng nằm trong danh sách cũ bốn mươi lăm giây, là mười giây chờ lần kiểm kế cộng ba mươi lăm giây bộ đệm, hai số minh hoạ.""", clear=True),
        st(P_QUYMO.out_html() + table(["yêu cầu mỗi giây", "yêu cầu lỗi, tối đa trong 45 giây (mô phỏng)", "giữ nguyên danh sách cũ", "thử lại sang bản khác (lệnh đọc)"],
                 [[nowrap("100 (×1)"), "1 500", "gãy nhẹ", "ước lượng: gần 0 lỗi thấy ngoài (không mô phỏng việc thử lại)"],
                  [nowrap("10 000 (×100)"), "150 000", "gãy nặng", "ước lượng: gần 0 lỗi, thêm ⅓ tải thử lại"],
                  [nowrap("1 000 000 (×10 000)"), "15 000 000", "không chấp nhận được", "ước lượng: gần 0 lỗi, bản sống chịu thêm tải"]]),
           """Số lỗi tăng thẳng theo tốc độ: một nghìn năm trăm, một trăm năm mươi nghìn, rồi mười lăm triệu. Cho thử lại sang bản khác thì khách gần như không thấy lỗi, ước lượng chứ không đo.""", clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["giữ danh sách cũ, chờ sổ cập nhật", "đơn giản, ít tải phụ", "lỗi tỉ lệ với tốc độ × 45 giây", "lưu lượng thấp, chịu được vài lỗi"],
                  ["rút ngắn chu kỳ kiểm", "phát hiện sớm hơn", "bộ đệm 35 giây vẫn là phần lớn cửa sổ; số lần kiểm tăng", "bộ đệm đã ngắn"],
                  ["thử lại sang bản khác", "khách không thấy lỗi", "chỉ an toàn với lệnh đọc; lệnh ghi cần khoá lũy đẳng", "lưu lượng lớn, có lệnh đọc nhiều"]]),
           """Giải pháp cũ gãy ở chỗ chờ sổ cập nhật, vì lỗi tỉ lệ với tốc độ nhân bốn mươi lăm giây. Thử lại chỉ an toàn với lệnh đọc, còn lệnh ghi cần khoá lũy đẳng, tức mã gửi kèm để gửi lại không bị làm hai lần.""",
           clear=True),
    ], checks=["[alg.bnx_l17_lost(r, 3, 45) for r in (100, 10000, 1000000)] == [1500, 150000, 15000000]",
               "alg.bnx_l17_stale_window(10, 35) == 45", "10000 // 100 == 1000000 // 10000 == 100"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Coi 401 và 403 là một, hoặc trả <b class="red">403 cho mọi lần từ chối</b>.
401 là <b>chưa biết bạn là ai</b>: bên gọi nên lấy mã mới rồi thử lại. 403 là <b>biết rồi nhưng không cho</b>: thử lại với đúng mã ấy vẫn 403.</div>""",
           """Lỗi thứ nhất, của người mới, là coi bốn trăm lẻ một và bốn trăm lẻ ba là một. Một là chưa biết bạn là ai nên lấy mã mới, ba là biết rồi nhưng không cho.""", clear=True),
        st(code(J_RUN, "ChayThu.java (hết): hai ca gửi lệnh ghi POST", lines=(50, 51)) + out(OUT_FG),
           """Lỗi thứ hai lộ ra lúc mới dựng: hai ca cuối gửi lệnh ghi. Kết quả chạy thật: lệnh ghi không mang mã nhận bốn trăm lẻ ba chứ không phải bốn trăm lẻ một.""",
           focus=[0, 2, ["4.1", "4.2"], ["4.3", "4.4", "4.5", "4.6"]], clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Thấy lệnh POST không mang mã nhận <b class="red">403</b> rồi đi tìm lỗi phân quyền.
Thủ phạm là trạm <b>chống giả mạo yêu cầu</b> (CsrfFilter; CSRF là kiểu tấn công nhờ phiên đăng nhập có sẵn của khách để gửi lệnh ghi từ trang lạ) ở vị trí 5, đứng <b>trước</b> trạm đọc mã ở vị trí 8, và mặc định bật cho các lệnh ghi.
<br><span class="note">Hướng dẫn của Spring Security: dịch vụ nền không phục vụ trình duyệt có thể tắt lớp này, và nên cân nhắc trước khi tắt. Bài học chung: cùng một con số 403, phải hỏi <b>trạm nào</b> trả.</span>
<br><span class="note">Quan sát chạy thật ở bộ kiểm, với cấu hình này: lệnh POST mang mã ký sai nhận 401 chứ không phải 403, nên yêu cầu có đầu mục mã không bị trạm chống giả mạo chặn. Hướng dẫn chính thức đã đọc không giải thích cơ chế, nên bài không khẳng định lý do.</span></div>""",
           """Thủ phạm là trạm chống giả mạo yêu cầu ở vị trí năm, đứng trước trạm đọc mã và mặc định bật cho lệnh ghi. Cùng một con số bốn trăm lẻ ba, phải hỏi trạm nào trả.""", clear=True, introduces=["bnx_csrf"]),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc hệ thống lớn dần).</b> <b class="red">Chỉ kiểm quyền ở cổng</b>, các dịch vụ phía sau tin mọi yêu cầu tới mình.
Hệ thống lớn dần, dịch vụ gọi thẳng nhau trong mạng nội bộ, không qua cổng: trên đường ấy không còn lần kiểm quyền nào.
<br><span class="note">Cách chữa: cổng kiểm thô (có mã, mã còn hạn), còn <b>mỗi dịch vụ là một máy chủ tài nguyên</b>, tự kiểm chữ ký và quyền như ví dụ vừa chạy.</span></div>""",
           """Lỗi thứ ba lộ ra khi hệ thống lớn dần: chỉ kiểm quyền ở cổng, trong khi các dịch vụ gọi thẳng nhau không qua cổng. Cách chữa: mỗi dịch vụ tự kiểm chữ ký và quyền.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> Để <b class="red">mật khẩu dạng chữ thường</b> trong kho cấu hình tập trung.
Kho ấy thường là một kho mã nguồn: ai đọc được lịch sử kho là đọc được mật khẩu, kể cả mật khẩu đã đổi từ năm trước.</div>"""
           + code(Y_CIPHER, "Tệp cấu hình trong kho (chép từ hướng dẫn của Spring Cloud Config, không chạy trên máy này)")
           + """<p style='margin-top:18px'><span class='note'>Giá trị bắt đầu bằng <code>{cipher}</code> là bản đã mã hoá; máy chủ cấu hình giải mã rồi mới gửi cho dịch vụ qua HTTP. Việc còn lại: đổi mật khẩu đã lộ trong lịch sử kho; giữ kín khoá giải mã; bảo vệ đường truyền, vì giá trị đã giải mã đi qua mạng.</span></p>""",
           """Lỗi thứ tư: mật khẩu chữ thường trong kho cấu hình, nên ai đọc được lịch sử kho là đọc được mật khẩu. Giá trị bắt đầu bằng nhãn mã hoá thì máy chủ giải mã rồi mới gửi đi.""",
           focus=[1, 1, "3.4", 4], clear=True),
    ], checks=[f"alg.bnx_l17_status('GET', {T_NONE}, 'han_muc') == 401 and alg.bnx_l17_status('GET', {T_AN}, 'han_muc') == 403",
               f"alg.bnx_l17_trace('POST', {T_NONE}, 'han_muc') == (403, 'CsrfFilter', False, False)",
               f"alg.bnx_l17_trace('POST', {T_BINH}, 'han_muc') == (200, None, True, True)",
               "alg.bnx_l17_pos('CsrfFilter') == 5 < alg.bnx_l17_pos('BearerTokenAuthenticationFilter') == 8"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Luật như trong bài: <code>/han-muc</code> đòi quyền <code>SCOPE_han_muc</code>, đường dẫn khác chỉ cần đã xác thực. Mã thật, còn hạn, scope <code>so_du</code>. Lệnh đọc tới <code>/so-du</code> nhận mã nào? Tới <code>/han-muc</code> nhận mã nào, do trạm số mấy trả?"],
                  ["2", "Một dịch vụ đăng ký 4 bản, 1 bản trượt kiểm sức khoẻ. 90 yêu cầu chia xoay vòng thì mỗi bản khoẻ nhận bao nhiêu? Nếu trượt 2 bản thì sao?"],
                  ["3", "Quyết định (số minh hoạ): 3 bản, 100 yêu cầu mỗi giây chia đều. Một bản chết hẳn; sổ kiểm mỗi 10 giây (đã bật lọc bản đạt kiểm), bộ đệm 35 giây. Chọn: giữ nguyên, giảm chu kỳ kiểm xuống 2 giây, hay giữ nguyên và cho thử lại sang bản khác?"]]),
           """Đến lượt bạn. Câu một, mã thật chỉ có quyền số dư gửi lệnh đọc tới hai đường dẫn thì nhận mã nào? Câu hai, bốn bản, một bản trượt, chín mươi yêu cầu thì mỗi bản khoẻ nhận bao nhiêu? Câu ba chọn một trong ba cách. Hãy tạm dừng và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: mã thật nên qua trạm đọc mã (số 8); phần còn lại do luật của từng đường dẫn quyết định.</p>
$$\\text{/so-du: chỉ cần đã xác thực} \\Rightarrow \\hlg{200}; \\qquad \\text{/han-muc: thiếu quyền} \\Rightarrow \\hlg{403} \\text{, do trạm dịch lỗi số 13 trả}$$""",
           """Đáp án câu một. Đường dẫn số dư chỉ cần đã xác thực nên nhận hai trăm, đường dẫn hạn mức đòi quyền mã không có nên nhận bốn trăm lẻ ba từ trạm mười ba."""),
        st("""<p>Câu 2: chỉ các bản khoẻ được chia việc.</p>
$$4 - 1 = 3 \\text{ bản}: \\; 90 : 3 = \\hlg{30} \\text{ mỗi bản}; \\qquad 4 - 2 = 2 \\text{ bản}: \\; 90 : 2 = \\hlg{45} \\text{ mỗi bản}$$""",
           """Đáp án câu hai. Trượt một bản còn ba bản, chín mươi chia ba là ba mươi. Trượt hai bản thì mỗi bản nhận bốn mươi lăm, tức gấp rưỡi."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["giữ nguyên: kiểm 10 giây, đệm 35 giây", "không phải làm gì", "bản chết còn nhận việc tới 10 + 35 = 45 giây: khoảng 100 × 45 : 3 = 1500 yêu cầu lỗi"],
                  ["giảm chu kỳ kiểm xuống 2 giây", "phát hiện sớm hơn 8 giây", "vẫn tới 2 + 35 = 37 giây, khoảng 1234 yêu cầu lỗi (cận trên); số lần kiểm tăng 5 lần"],
                  ["giữ nguyên, lỗi kết nối thì thử lại sang bản khác", "yêu cầu rơi vào bản chết được cứu ngay", "chỉ an toàn với lệnh đọc; lệnh ghi phải có khoá lũy đẳng, kẻo xử lý hai lần"]]),
           """Đáp án câu ba, tính bằng cận trên. Giữ nguyên thì khoảng một nghìn năm trăm yêu cầu lỗi, giảm chu kỳ kiểm xuống hai giây vẫn còn khoảng một nghìn hai trăm ba mươi tư vì bộ đệm là phần lớn. Thử lại cứu yêu cầu ngay nhưng chỉ an toàn với lệnh đọc.""",
           focus=["1.2", "1.3", "1.3", "1.4"]),
    ], checks=[f"alg.bnx_l17_status('GET', {T_AN}, None) == 200",
               f"alg.bnx_l17_trace('GET', {T_AN}, 'han_muc')[:2] == (403, 'ExceptionTranslationFilter') and alg.bnx_l17_pos('ExceptionTranslationFilter') == 13",
               "alg.bnx_l17_round_robin([True, False, True, True], 90) == [30, 0, 30, 30]",
               "alg.bnx_l17_round_robin([True, False, False, True], 90) == [45, 0, 0, 45] and 45 / 30 == 1.5",
               "alg.bnx_l17_stale_window(10, 35) == 45 and alg.bnx_l17_lost(100, 3, 45) == 1500",
               "alg.bnx_l17_stale_window(2, 35) == 37 and alg.bnx_l17_lost(100, 3, 37) == 1233 and -(-100 * 37 // 3) == 1234",
               "alg.bnx_l17_stale_window(10, 35) - alg.bnx_l17_stale_window(2, 35) == 8 and 10 // 2 == 5"])

    lab_pr = practice_scene(sc, "Tự làm: bảng quyết định 401/403 và chia cho các bản khoẻ", practice_steps2(
        st, "BNX", "L17",
        """<p><b>Đề</b>: viết <code>mau.py</code> (Python):</p>
<ol><li>hàm <code>kiem(ma, duong)</code>: không mã → 401; chữ ký sai hoặc hết hạn → 401; đường <code>/chuyen-tien</code> thiếu quyền <code>chuyen_tien</code> → 403; còn lại 200</li>
<li>6 ca: (không mã, <code>/so-du</code>), (giả, <code>/so-du</code>), (cũ, <code>/chuyen-tien</code>), (An, <code>/so-du</code>), (An, <code>/chuyen-tien</code>), (Bình, <code>/chuyen-tien</code>); in <code>ca i: mã</code></li>
<li>4 bản <code>b1…b4</code>, <code>b2</code> trượt; chia <b>250</b> yêu cầu xoay vòng cho các bản khoẻ, in <code>b1=… b3=… b4=…</code></li></ol>
<p class="note">Mã An, Bình, giả, cũ và quy ước chi tiết nằm trong <code>de.md</code>. Số liệu khác ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm. Viết hàm trả mã trạng thái theo luật, chạy sáu ca, rồi chia hai trăm năm mươi yêu cầu xoay vòng cho các bản khoẻ trong bốn bản. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> kiểm theo đúng thứ tự: không mã, rồi chữ ký và hạn, rồi quyền. Với phần chia: lọc danh sách bản khoẻ, rồi <code>khoe[i % len(khoe)]</code> cho yêu cầu thứ i từ 0. 250 : 3 dư 1, nên bản đầu nhận thêm một.
Lời giải đầy đủ ở <code>labs/BNX/L17/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, kiểm theo đúng thứ tự: không mã, rồi chữ ký và hạn, rồi quyền. Phần chia thì lọc các bản khoẻ rồi lấy số thứ tự chia lấy dư.""", pause=180), "BNX", "L17")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("chuỗi trạm có thứ tự", "trạm đọc mã: mã hỏng thì 401", "trạm kiểm quyền + trạm dịch lỗi: 401 hoặc 403",
                 "mỗi dịch vụ tự kiểm mã", "cổng tra sổ, chia cho bản khoẻ"),
           """Tổng kết: yêu cầu đi qua chuỗi trạm có thứ tự, trạm đọc mã trả bốn trăm lẻ một khi mã hỏng, trạm dịch lỗi chọn bốn trăm lẻ một hay ba. Mỗi dịch vụ tự kiểm mã, cổng chia việc cho các bản khoẻ."""),
        st("""<div class='box key'><b>Tư duy:</b> 401 là chưa biết bạn là ai, 403 là biết rồi nhưng không cho. Gặp một lần từ chối, hãy hỏi <b>trạm nào</b> trả nó. Đừng tin một lớp kiểm duy nhất, và khi lưu lượng tăng, hỏi danh sách bản <b>cũ bao lâu</b>.</div>""",
           """Điều cần mang theo: gặp một lần từ chối, hãy hỏi trạm nào trả nó, đừng tin một lớp kiểm duy nhất, và hỏi danh sách bản cũ bao lâu."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Spring Security: một yêu cầu đi qua những gì, 401 khác 403 ở đâu?", "chuỗi bộ lọc có thứ tự; trạm đọc mã trả 401 khi mã hỏng; trạm kiểm quyền từ chối, trạm dịch lỗi trả 401 nếu còn vô danh, 403 nếu đã xác thực"],
                  ["Spring Security OAuth2: dịch vụ kiểm mã truy cập thế nào?", "là máy chủ tài nguyên: kiểm chữ ký bằng khoá của máy chủ cấp mã, kiểm hạn, đổi scope thành quyền <code>SCOPE_…</code>; từng dịch vụ tự kiểm, không chỉ cổng"],
                  ["Spring Cloud và Consul để làm gì?", "sổ đăng ký giữ các bản và kiểm sức khoẻ; cổng ghi tên dịch vụ, tra sổ rồi chia xoay vòng, chỉ gặp bản khoẻ khi đã bật lọc theo kiểm sức khoẻ; mật khẩu trong cấu hình tập trung phải mã hoá"]]),
           """Người phỏng vấn thường hỏi ba câu. Trạm nào trả bốn trăm lẻ một, trạm nào bốn trăm lẻ ba. Dịch vụ kiểm chữ ký và hạn rồi đổi phạm vi thành quyền. Cổng tra sổ rồi chia xoay vòng.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Bài sau: kiểm thử Java, viết <b>ca kiểm</b> cho từng nhánh của một hàm và thay phần phụ thuộc bên ngoài bằng <b>đối tượng giả</b>.</p>""",
           """Bài mười tám viết ca kiểm tự động cho từng nhánh của một hàm, và thay phần phụ thuộc bên ngoài bằng đối tượng giả.""",
           forward_ref=True),
    ], checks=[f"alg.bnx_l17_status('GET', {T_NONE}, 'han_muc') == 401 and alg.bnx_l17_status('GET', {T_AN}, 'han_muc') == 403",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L17", "spring_security_spring_cloud",
                  "Bài 17 — Spring Security và Spring Cloud: chuỗi bộ lọc, cổng và khám phá dịch vụ",
                  "curriculum/bnx.yaml L17; audit/bnx/verify_bnx.py L17; audit/bnx/sources_l17.md: hướng dẫn Spring Security 7.1.2 (Architecture, "
                  "OAuth2 Resource Server, CSRF), Spring Cloud Gateway 5.0.4, Spring Cloud Commons 5.0.4 (LoadBalancer), Spring Cloud Consul 5.0.4, "
                  "Spring Cloud Config 5.0.6 (đọc 2026-11-11); Spring Security 7.1.2 chạy thật trên Temurin JDK 21.0.13; phần chia tải là mô phỏng",
                  ["Lần theo một yêu cầu qua chuỗi bộ lọc bảo mật và nói bộ lọc nào trả 401, bộ lọc nào trả 403",
                   "Đọc cấu hình một dịch vụ kiểm mã truy cập như máy chủ tài nguyên và chỉ ra dòng nào quyết định 401, 403",
                   "Giải thích vai trò của cổng, cấu hình tập trung và sổ đăng ký dịch vụ trong Spring Cloud",
                   "Tính cách cổng chia tải khi một bản dịch vụ trượt kiểm sức khoẻ"],
                  scenes,
                  covers=[(1, "example"), (2, "formula"), (3, "formula"), (4, "practice")])


# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
write_lab("BNX", "L17", LAB_DE, "py", LAB_PY, LAB_OUT)
