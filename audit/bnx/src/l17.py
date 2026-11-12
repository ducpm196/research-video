from lib import *

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
  static final String KHOA = "khoa-bi-mat-chi-de-hoc-dai-32-byte!!";
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
        "khoa-cua-ke-gian-cung-dai-32-byte!!!");
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


def build():
    hook = sc("hook", "hook", "Ba yêu cầu tới cùng một địa chỉ: 401, 403 và 200", [
        st("""<p>Dịch vụ hạn mức của một ngân hàng nhận <b>ba yêu cầu</b> tới cùng một địa chỉ <code>/han-muc</code>:</p>
<div class="box key">Yêu cầu không mang mã truy cập: bị chặn, nhận <b>401</b>. Yêu cầu có mã hợp lệ nhưng thiếu quyền: nhận <b>403</b>.
Yêu cầu đủ quyền: nhận <b>200</b>.<br>Ai chặn, chặn ở đâu, và vì sao hai lần từ chối lại mang hai con số khác nhau?</div>""",
           """Chào bạn, dịch vụ hạn mức của một ngân hàng nhận ba yêu cầu tới cùng một địa chỉ.
           Yêu cầu không mang mã truy cập bị chặn và nhận mã bốn trăm lẻ một, còn yêu cầu có mã hợp lệ nhưng thiếu quyền thì nhận bốn trăm lẻ ba.
           Chỉ yêu cầu đủ quyền mới nhận mã hai trăm, vậy ai chặn, chặn ở đâu, và vì sao hai lần từ chối mang hai con số khác nhau?""",
           focus=[1, 2, 2]),
        st("""<p>Dịch vụ ấy chạy <b>ba bản</b> giống nhau. Một bản <b>trượt kiểm sức khoẻ</b>.</p>
$$100 \\text{ yêu cầu chia xoay vòng cho } 3 - 1 = 2 \\text{ bản còn lại}: \\quad 100 : 2 = \\hl{50} \\text{ yêu cầu mỗi bản}$$
<span class='note'>Điều kiện: sổ chỉ trả các bản khoẻ, hoặc bộ chia tải tự lọc. Mặc định không đủ; bước 7 ở phần suy ra nói rõ cách bật.</span>""",
           """Dịch vụ ấy chạy ba bản giống nhau, và một bản vừa trượt kiểm sức khoẻ.
           Một trăm yêu cầu khi đó được chia xoay vòng cho hai bản còn lại, nên mỗi bản nhận năm mươi yêu cầu, vì bản hỏng không được giao việc.
           Điều này chỉ đúng khi sổ chỉ trả các bản khoẻ hoặc bộ chia tải tự lọc, mà mặc định chưa đủ, bước bảy sẽ nói rõ cách bật."""),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["ai chặn yêu cầu", "<b>chuỗi bộ lọc</b> của Spring Security: nhiều trạm nối tiếp đứng trước dịch vụ"],
                  ["dịch vụ kiểm mã truy cập thế nào", "cấu hình nó thành <b>máy chủ tài nguyên</b>: kiểm chữ ký, hạn, rồi quyền"],
                  ["ai biết bản nào còn sống", "<b>Spring Cloud</b>: cổng, sổ đăng ký dịch vụ có kiểm sức khoẻ, cấu hình tập trung"]]),
           """Hôm nay ta trả lời ba câu. Ai chặn yêu cầu, đó là chuỗi bộ lọc bảo mật của Spring, gồm nhiều trạm nối tiếp đứng trước dịch vụ.
           Dịch vụ kiểm mã truy cập thế nào, đó là khi ta cấu hình nó thành một máy chủ tài nguyên.
           Và ai biết bản nào còn sống để chia việc, đó là cổng và sổ đăng ký dịch vụ của Spring Cloud.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=[f"alg.bnx_l17_status('GET', {T_NONE}, 'han_muc') == 401", f"alg.bnx_l17_status('GET', {T_AN}, 'han_muc') == 403",
               f"alg.bnx_l17_status('GET', {T_BINH}, 'han_muc') == 200",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]", "sum([True, False, True]) == 3 - 1 == 2"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① mã truy cập", "chuỗi có <b>chữ ký</b> do máy chủ cấp mã phát; mang hạn dùng và <b>phạm vi quyền</b> (scope)", "scope <code>so_du han_muc</code>: 2 quyền, cách nhau một dấu cách"],
                  ["② mã trạng thái", "con số máy chủ trả về cho mỗi yêu cầu", "200: xong; 401: chưa xác thực; 403: bị cấm"],
                  ["③ bean", "đối tượng do Spring tạo và giữ; ta khai bằng nhãn <code>@Bean</code>", "một bean giữ luật bảo mật, một bean kiểm chữ ký"],
                  ["④ bản dịch vụ", "một tiến trình đang chạy của cùng một dịch vụ; nhiều bản để chịu tải và chịu lỗi", "3 bản, 1 bản hỏng: còn 3 − 1 = 2 bản phục vụ"],
                  ["⑤ xác thực và phân quyền", "xác thực: biết người gọi là ai; phân quyền: xét người đó có được làm việc này không", "mã hỏng là lỗi xác thực; mã tốt mà thiếu quyền là lỗi phân quyền"]]),
           """Trước hết ta cần hiểu năm điều. Thứ nhất, mã truy cập là một chuỗi có chữ ký do máy chủ cấp mã phát ra, mang hạn dùng và phạm vi quyền.
           Thứ hai, mã trạng thái là con số máy chủ trả về cho mỗi yêu cầu: hai trăm là xong, bốn trăm lẻ một là chưa xác thực, bốn trăm lẻ ba là bị cấm.
           Thứ ba, Spring tự tạo và giữ các đối tượng cho ta, và ta khai chúng bằng một nhãn đặt trên hàm.
           Thứ tư, bản dịch vụ là một tiến trình đang chạy của cùng một dịch vụ, người ta chạy nhiều bản để chịu tải và chịu lỗi.
           Thứ năm, xác thực là biết người gọi là ai, còn phân quyền là xét người đó có được làm việc này hay không.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
        st("""<p>Làm thử: 3 bản đăng ký, 1 bản hỏng, 100 yêu cầu chia đều.</p>
$$3 - 1 = 2 \\text{ bản}; \\qquad 100 : 2 = \\hl{50} \\text{ yêu cầu mỗi bản}; \\qquad \\text{còn đủ 3 bản thì } 100 = 34 + 33 + 33$$""",
           """Làm thử ngay với ba bản đăng ký, một bản hỏng. Còn hai bản, nên một trăm yêu cầu chia đều thì mỗi bản nhận năm mươi.
           Nếu còn đủ ba bản thì một trăm không chia hết cho ba, nên bản đầu nhận ba mươi tư, hai bản sau nhận ba mươi ba."""),
    ], checks=["alg.bnx_l17_authorities('so_du han_muc') == ['SCOPE_so_du', 'SCOPE_han_muc']",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]",
               "alg.bnx_l17_round_robin([True, True, True], 100) == [34, 33, 33]", "sum(alg.bnx_l17_round_robin([True] * 3, 100)) == 100"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên trong Spring Security", "nghĩa"],
                 [["Filter", "<b>bộ lọc</b>, một trạm: nhận yêu cầu, làm một việc, rồi chuyển tiếp hoặc trả lời luôn"],
                  ["SecurityFilterChain", "<b>chuỗi bộ lọc bảo mật</b>: danh sách trạm có thứ tự mà yêu cầu phải đi qua"],
                  ["BearerTokenAuthenticationFilter", "<b>trạm đọc mã</b>: lấy mã truy cập trong yêu cầu và kiểm nó"],
                  ["AuthorizationFilter", "<b>trạm kiểm quyền</b>: so quyền của người gọi với luật của đường dẫn"],
                  ["ExceptionTranslationFilter", "<b>trạm dịch lỗi</b>: đổi lỗi của trạm kiểm quyền thành 401 hoặc 403"],
                  ["SCOPE_han_muc", "quyền sinh từ phạm vi <code>han_muc</code> trong mã; tiền tố <code>SCOPE_</code> do Spring thêm"]]),
           """Bảng này giải mã các tên của phần bảo mật. Bộ lọc là một trạm: nó nhận yêu cầu, làm một việc, rồi chuyển tiếp hoặc trả lời luôn.
           Chuỗi bộ lọc bảo mật là danh sách trạm có thứ tự mà mọi yêu cầu phải đi qua.
           Trạm đọc mã có nhiệm vụ lấy mã truy cập trong yêu cầu và kiểm nó.
           Trạm kiểm quyền thì so quyền của người gọi với luật của đường dẫn.
           Trạm dịch lỗi đổi lỗi của trạm kiểm quyền thành mã bốn trăm lẻ một hoặc bốn trăm lẻ ba.
           Dòng cuối là tên một quyền, do Spring ghép một tiền tố cố định với phạm vi quyền ghi trong mã.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
        st(table(["tên trong Spring Cloud", "nghĩa"],
                 [["Spring Cloud Gateway", "<b>cổng</b>: cửa vào chung, nhận yêu cầu rồi chuyển tới đúng dịch vụ"],
                  ["Consul", "<b>sổ đăng ký dịch vụ</b>: mỗi bản tự ghi tên, địa chỉ; sổ kiểm sức khoẻ từng bản"],
                  ["<code>lb://ten-dich-vu</code>", "địa chỉ theo <b>tên</b>: cổng tra sổ lấy các bản rồi chia tải (load balance)"],
                  ["Spring Cloud Config", "<b>cấu hình tập trung</b>: một máy chủ giữ cấu hình cho mọi dịch vụ"]]),
           """Bảng thứ hai là các tên của Spring Cloud. Cổng là cửa vào chung, nhận yêu cầu rồi chuyển tới đúng dịch vụ.
           Sổ đăng ký dịch vụ là nơi mỗi bản tự ghi tên và địa chỉ của mình, và sổ kiểm sức khoẻ từng bản.
           Địa chỉ ở hàng thứ ba không ghi máy nào cả mà ghi tên dịch vụ, nên cổng phải tra sổ lấy các bản rồi chia tải.
           Cuối cùng, cấu hình tập trung là một máy chủ giữ cấu hình cho mọi dịch vụ.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
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
           """Hình này là mười bốn trạm của chuỗi bộ lọc, đứng trước dịch vụ. Yêu cầu đi từ trạm một sang phải, qua hết mới tới dịch vụ.
           Yêu cầu không mang mã vẫn qua được trạm đọc mã số tám, nhưng trạm kiểm quyền số mười bốn ném lỗi, và trạm dịch lỗi số mười ba trả bốn trăm lẻ một.
           Mã hỏng, tức sai chữ ký hoặc hết hạn, thì chính trạm tám trả bốn trăm lẻ một ngay, không đi tiếp.
           Mã tốt nhưng thiếu quyền thì trạm mười bốn ném lỗi, và lần này trạm mười ba trả bốn trăm lẻ ba, vì đã biết người gọi là ai.
           Trạm xác thực đứng trước trạm phân quyền, vì phải biết ai gọi rồi mới xét cho hay không."""),
        st(svg(1500, 520,
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
               txt(900, 500, "Nếu sổ chỉ trả bản khoẻ: bản 2 trượt bị loại, 100 : 2 = 50 mỗi bản", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là phần Spring Cloud. Ứng dụng khách chỉ biết một địa chỉ, là cổng.
           Cổng không nhớ sẵn địa chỉ các bản, mà tra sổ đăng ký dịch vụ, nơi mỗi bản đã tự ghi tên lúc khởi động.
           Sổ định kỳ kiểm sức khoẻ từng bản. Khi sổ được dặn chỉ trả các bản khoẻ, hoặc bộ chia tải tự lọc, bản hai trượt thì bị loại khỏi danh sách.
           Vì chỉ còn hai bản khoẻ, một trăm yêu cầu được chia xoay vòng, mỗi bản năm mươi.
           Ở phía dưới, máy chủ cấu hình giữ cấu hình chung, và mỗi dịch vụ hỏi nó lúc khởi động."""),
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
        st("""<p><b>Bước 1.</b> Bảo mật có nhiều việc khác nhau: đọc mã, kiểm quyền, đổi lỗi thành câu trả lời. Gộp vào một chỗ thì khó thay từng phần,
nên Spring Security chia thành <b>chuỗi trạm có thứ tự</b>. Thứ tự là luật: trạm xác thực phải đứng <b>trước</b> trạm phân quyền.</p>
<p>Làm thử: trạm đọc mã ở vị trí 8, trạm kiểm quyền ở vị trí 14.</p>
$$8 < 14 \\;\\Rightarrow\\; \\text{khi tới trạm kiểm quyền, đã biết người gọi là ai (hoặc biết là vô danh)}$$""",
           """Bước một, bảo mật có nhiều việc khác nhau, nên Spring chia chúng thành một chuỗi trạm có thứ tự, để thay được từng phần.
           Thứ tự là luật, vì trạm xác thực phải đứng trước trạm phân quyền.
           Làm thử, trạm đọc mã ở vị trí tám, trạm kiểm quyền ở vị trí mười bốn, nên khi tới trạm kiểm quyền thì đã biết người gọi là ai.""",
           clear=True),
        st("""<p><b>Bước 2.</b> Trạm đọc mã chỉ lo <b>xác thực</b>. Có mã thì kiểm chữ ký và hạn dùng; hỏng thì trả <b>401</b> ngay, vì không thể tin một chữ nào trong mã.
Không có mã thì trạm cho đi tiếp như một <b>khách vô danh</b>, vì có thể đường dẫn ấy không đòi gì.</p>"""
           + table(["yêu cầu", "trạm đọc mã (số 8)", "đi tiếp?"],
                   [["không mang mã", "không có gì để kiểm", "có, với tư cách vô danh"],
                    ["mã sai chữ ký hoặc hết hạn", "trả <b>401</b>", "không"],
                    ["mã tốt", "ghi nhận người gọi và các quyền", "có"]]),
           """Bước hai, trạm đọc mã chỉ lo xác thực. Có mã thì nó kiểm chữ ký và hạn dùng, hỏng thì trả bốn trăm lẻ một ngay, vì không thể tin một chữ nào trong mã.
           Không có mã thì trạm cho đi tiếp như một khách vô danh, vì có thể đường dẫn ấy không đòi gì.
           Bảng làm thử ba trường hợp: không mang mã thì đi tiếp, mã hỏng thì dừng ở đây, mã tốt thì đi tiếp cùng các quyền của nó.""",
           focus=[1, 1, 1, 2], clear=True),
        st("""<p><b>Bước 3.</b> Trạm kiểm quyền (số 14) chỉ biết <b>ném lỗi từ chối</b>. Trạm dịch lỗi (số 13) bọc ngoài nó, bắt lỗi ấy và hỏi một câu: người gọi đã được xác thực chưa?</p>"""
           + table(["người gọi", "trạm dịch lỗi trả", "nghĩa"],
                   [["vô danh (chưa xác thực)", "<b>401</b>", "chưa biết bạn là ai: hãy mang mã tới"],
                    ["đã xác thực, thiếu quyền", "<b>403</b>", "biết rồi nhưng không cho: mang lại mã ấy cũng vô ích"]]),
           """Bước ba, trạm kiểm quyền chỉ biết ném lỗi từ chối. Trạm dịch lỗi bọc ngoài nó, bắt lỗi ấy, rồi hỏi người gọi đã được xác thực chưa.
           Nếu là khách vô danh thì trả bốn trăm lẻ một, nghĩa là chưa biết bạn là ai, hãy mang mã tới.
           Nếu đã xác thực mà thiếu quyền thì trả bốn trăm lẻ ba, nghĩa là biết rồi nhưng không cho, nên gửi lại đúng mã ấy cũng vô ích.""",
           focus=[1, 1, "2.2", "2.3"], clear=True),
        st("""<p><b>Bước 4.</b> Dịch vụ tự kiểm mã, không hỏi lại máy chủ cấp mã mỗi lần, nên nó cần <b>khoá để kiểm chữ ký</b>. Khai địa chỉ máy chủ cấp mã,
dịch vụ sẽ tự lấy khoá công khai ở đó. Dịch vụ như thế gọi là <b>máy chủ tài nguyên</b>.</p>"""
           + code(Y_RS, "application.yml (chép từ hướng dẫn của Spring Security, không chạy trên máy này)")
           + """<p>Làm thử: mã ghi scope <code>so_du han_muc</code> thì người gọi có 2 quyền: <code>SCOPE_so_du</code> và <code>SCOPE_han_muc</code>.</p>"""
           + """<p style='margin-top:18px'><span class='note'>Mặc định dịch vụ kiểm nơi cấp (iss) và hạn (exp, nbf); đối tượng nhận (aud) phải khai thêm. Theo hướng dẫn chính thức, việc tìm khoá chỉ làm ở yêu cầu đầu tiên có mã, nên khởi động không bị buộc vào máy chủ cấp mã.</span></p>""",
           """Bước bốn, dịch vụ tự kiểm mã chứ không hỏi lại máy chủ cấp mã mỗi lần, nên nó cần khoá để kiểm chữ ký.
           Trong tệp cấu hình này, dòng cuối khai địa chỉ máy chủ cấp mã, và dịch vụ sẽ tự lấy khoá công khai ở đó.
           Một dịch vụ tự kiểm mã như thế được gọi là máy chủ tài nguyên.
           Làm thử, mã ghi hai phạm vi quyền thì người gọi có hai quyền, mỗi quyền là tiền tố cố định ghép với một phạm vi.
           Mặc định dịch vụ chỉ kiểm nơi cấp và hạn dùng của mã, còn đối tượng nhận mã phải khai thêm, và việc tìm khoá chỉ làm ở yêu cầu đầu tiên có mã.""",
           focus=[1, "3.6", 1, 4, 5], clear=True),
        st("""<p><b>Bước 5.</b> Địa chỉ các bản thay đổi liên tục (thêm bản, bản chết), nên không ghi cứng vào cổng. Cổng ghi <b>tên dịch vụ</b>, rồi tra sổ đăng ký lấy các bản đang khoẻ.</p>"""
           + code(Y_GW, "application.yml của cổng (chép từ hướng dẫn của Spring Cloud Gateway, không chạy trên máy này)"),
           """Bước năm, địa chỉ các bản thay đổi liên tục, nên ta không ghi cứng vào cổng. Cổng ghi tên dịch vụ, rồi tra sổ đăng ký lấy các bản đang khoẻ.
           Trong cấu hình của cổng, dòng địa chỉ bắt đầu bằng hai chữ cái viết tắt của chia tải, theo sau là tên dịch vụ, còn dòng cuối là mẫu đường dẫn.""",
           focus=[1, 1, ["3.8", "3.10"]], clear=True),
        st("""<p><b>Chia xoay vòng:</b> yêu cầu thứ $i$ giao cho bản thứ $i$ chia lấy dư cho số bản khoẻ. Làm thử với 2 bản khoẻ: yêu cầu 0, 2, 4 về bản đầu, yêu cầu 1, 3, 5 về bản sau.</p>
$$6 \\text{ yêu cầu}, 2 \\text{ bản khoẻ}: \\quad 6 : 2 = \\hl{3} \\text{ yêu cầu mỗi bản}$$""",
           """Chia xoay vòng nghĩa là yêu cầu thứ i giao cho bản thứ i chia lấy dư cho số bản khoẻ.
           Làm thử với hai bản khoẻ, các yêu cầu số chẵn về bản đầu, các yêu cầu số lẻ về bản sau, nên sáu yêu cầu chia ra mỗi bản ba.""",
           clear=True),
        st(table(["mảnh của Spring Cloud", "giữ gì", "vì sao cần"],
                 [["cổng", "luật định tuyến: đường dẫn nào về dịch vụ nào", "khách chỉ cần biết một địa chỉ"],
                  ["sổ đăng ký dịch vụ", "tên, địa chỉ và sức khoẻ của từng bản", "bản thêm vào hay chết đi, không ai phải sửa cấu hình"],
                  ["cấu hình tập trung", "cấu hình của mọi dịch vụ ở một nơi", "đổi một chỗ, không sửa từng bản"]]),
           """Bước sáu, ghép ba mảnh của Spring Cloud. Cổng giữ luật định tuyến, vì khách chỉ cần biết một địa chỉ.
           Sổ đăng ký giữ tên, địa chỉ và sức khoẻ của từng bản, vì thế bản thêm vào hay chết đi thì không ai phải sửa cấu hình.
           Cấu hình tập trung giữ cấu hình của mọi dịch vụ ở một nơi, để đổi một chỗ thay vì sửa từng bản.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p><b>Bước 7.</b> Bản trượt kiểm sức khoẻ không tự biến mất khỏi danh sách của cổng: tuỳ cấu hình. Số liệu mặc định lấy từ hướng dẫn chính thức:</p>"""
           + table(["cơ chế", "mặc định", "ghi chú"],
                   [["Consul kiểm HTTP tới <code>/actuator/health</code>, hỏng thì đánh dấu critical", "bật, mỗi 10 giây", "Consul làm, trước khi bộ chia tải thấy gì"],
                    ["truy vấn sổ chỉ lấy bản đạt: <code>spring.cloud.consul.discovery.query-passing</code>", "false (tắt)", "tắt thì truy vấn không đòi chỉ trả bản đạt; bài không dựng Consul nên không đo"],
                    ["bộ chia tải tự kiểm thêm: <code>spring.cloud.loadbalancer.configurations=health-check</code>", "tắt; chu kỳ 25 giây khi bật", "hướng dẫn nói với sổ đăng ký thật thường không cần"],
                    ["bộ đệm danh sách bản của bộ chia tải: <code>spring.cloud.loadbalancer.cache.ttl</code>", "35 giây", "danh sách cũ còn dùng tới khi hết hạn đệm"]]),
           """Bước bảy, bản trượt kiểm sức khoẻ không tự biến mất khỏi danh sách của cổng, mà tuỳ cấu hình, với số mặc định lấy từ hướng dẫn chính thức.
           Sổ đăng ký tự kiểm mỗi mười giây và đánh dấu bản hỏng, nhưng việc truy vấn sổ chỉ lấy bản đạt kiểm thì mặc định đang tắt, tên gốc hiện trên màn hình.
           Bộ chia tải cũng có chế độ tự kiểm thêm, mặc định tắt, chu kỳ hai mươi lăm giây khi bật, và hướng dẫn nói với sổ đăng ký thật thì thường không cần.
           Danh sách các bản còn được đệm ba mươi lăm giây. Vì bài không dựng sổ đăng ký thật nên không đo được bản hỏng ở lại bao lâu, chỉ tính cận trên ở câu ba.""", clear=True),
    ], checks=["alg.bnx_l17_pos('BearerTokenAuthenticationFilter') == 8 < alg.bnx_l17_pos('AuthorizationFilter') == 14",
               "alg.bnx_l17_pos('ExceptionTranslationFilter') == 13",
               f"alg.bnx_l17_trace('GET', {T_NONE}, 'han_muc')[2] is True and alg.bnx_l17_trace('GET', {T_GIA}, 'han_muc')[2] is False",
               f"alg.bnx_l17_status('GET', {T_GIA}, 'han_muc') == 401 and alg.bnx_l17_status('GET', {T_CU}, 'han_muc') == 401",
               f"alg.bnx_l17_status('GET', {T_NONE}, 'han_muc') == 401 and alg.bnx_l17_status('GET', {T_AN}, 'han_muc') == 403",
               "len(alg.bnx_l17_authorities('so_du han_muc')) == 2",
               "alg.bnx_l17_round_robin([True, True], 6) == [3, 3]", "[i % 2 for i in range(6)] == [0, 1, 0, 1, 0, 1]"])

    ex = sc("example", "example", "Ví dụ chạy thật Spring Security, từng phép tính", [
        st(code(J_CFG, "CauHinh.java (trích): luật bảo mật của dịch vụ hạn mức", lines=(12, 21)),
           """Ta chạy thật bộ khung bảo mật của Spring, bản bảy chấm một. Hai nhãn đầu báo cho Spring rằng lớp này là cấu hình bảo mật.
           Khoá bí mật ở đây chỉ để học, dùng cho việc ký và kiểm mã.
           Hàm có nhãn khai một đối tượng cho Spring giữ, chính là chuỗi bộ lọc.
           Luật thứ nhất nói đường dẫn hạn mức đòi đúng quyền hạn mức, luật thứ hai nói mọi đường dẫn khác chỉ cần đã xác thực.
           Lệnh cuối biến dịch vụ thành máy chủ tài nguyên, tức là thêm trạm đọc mã truy cập vào chuỗi.""",
           focus=[0, ["2.1", "2.2"], "2.4", ["2.5", "2.6"], ["2.7", "2.8", "2.9"], "2.10"], clear=True),
        st(code(J_CFG, "CauHinh.java (tiếp): trạm quan sát và bộ kiểm chữ ký", lines=(22, 30)),
           """Hai dòng đầu chèn một trạm của riêng ta vào ngay sau trạm đọc mã, để quan sát yêu cầu nào đi qua được trạm ấy.
           Hàm thứ hai khai bộ kiểm chữ ký cho Spring giữ, cũng bằng một nhãn đặt trên hàm.
           Nó dùng chính khoá bí mật ở trên, nên mã ký bằng khoá khác sẽ bị loại.""",
           focus=[["2.1", "2.2"], ["2.5", "2.6"], ["2.7", "2.8"]], clear=True),
        st(code(J_CFG, "CauHinh.java (hết): trạm quan sát chỉ in một câu rồi chuyển tiếp", lines=(31, 37)),
           """Trạm quan sát rất đơn giản: mỗi khi có yêu cầu tới, nó in một câu báo đã qua trạm, rồi chuyển yêu cầu cho trạm kế tiếp.
           Nhờ vậy, yêu cầu nào không in câu này thì đã bị chặn từ trạm đọc mã trở về trước.""",
           focus=[["2.1", "2.4", "2.5"], 0], clear=True),
        st(code(J_RUN, "ChayThu.java (trích): gửi một yêu cầu qua chuỗi và in kết quả", lines=(19, 29)),
           """Chương trình chạy thử có một hàm gửi yêu cầu. Nó in tên ca, rồi tạo một yêu cầu tới đường dẫn hạn mức, không cần máy chủ thật.
           Nếu ca ấy có mã thì mã được gắn vào đầu mục xác thực của yêu cầu.
           Sau đó yêu cầu được đẩy qua chuỗi bộ lọc, và nếu lọt tới cuối chuỗi thì chương trình in rằng đã tới dịch vụ.
           Ba lệnh cuối in mã trạng thái, và đầu mục thách thức xác thực nếu có.""",
           focus=["2.1", ["2.2", "2.3"], "2.4", ["2.5", "2.6", "2.7"], ["2.8", "2.9", "2.10"]], clear=True),
        st(code(J_RUN, "ChayThu.java (tiếp): dựng Spring rồi in chuỗi bộ lọc", lines=(31, 38)),
           """Hàm chính dựng Spring với lớp cấu hình vừa viết, rồi xin Spring đối tượng chuỗi bộ lọc.
           Vòng lặp in ra tên từng trạm mà một yêu cầu tới đường dẫn hạn mức sẽ đi qua, kèm số thứ tự.""",
           focus=[["2.1", "2.2", "2.3", "2.4", "2.5"], ["2.6", "2.7", "2.8"]], clear=True),
        st(code(J_RUN, "ChayThu.java (tiếp): bốn mã thử và năm ca", lines=(39, 49)),
           """Tiếp theo ta tự ký bốn mã bằng hàm băm có khoá. Mã của An chỉ có quyền số dư, mã của Bình có cả quyền số dư và quyền hạn mức.
           Mã giả ghi quyền hạn mức nhưng ký bằng khoá của kẻ gian, còn mã cũ ký đúng khoá nhưng hạn dùng đã qua.
           Năm lệnh cuối gửi năm ca: không mang mã, mã giả, mã thiếu quyền, mã đủ quyền, và mã hết hạn.""",
           focus=["2.1", ["2.2", "2.3"], ["2.4", "2.5", "2.6"], ["2.7", "2.8", "2.9", "2.10", "2.11"]], clear=True),
        st(code(SH_RUN, "Biên dịch và chạy (thư viện Spring nằm trong thư mục lib)", lines=(4, 5)) + out(OUT_CHAIN, "Kết quả chạy thật (lược bớt bằng dấu …)"),
           """Hai lệnh này biên dịch rồi chạy chương trình, với các thư viện của Spring nằm trong một thư mục.
           Kết quả chạy thật trước hết in ra chuỗi bộ lọc, gồm mười bốn trạm.
           Trạm chống giả mạo yêu cầu ở vị trí năm, trạm đọc mã ở vị trí tám, và trạm quan sát của ta nằm ngay sau nó, ở vị trí chín.
           Trạm dịch lỗi ở vị trí mười ba, bọc lấy trạm kiểm quyền ở vị trí cuối cùng.""",
           focus=[2, 4, ["4.3", "4.5", "4.6"], ["4.9", "4.10"]], clear=True),
        st(out(OUT_A) + """
$$① \\; \\text{không mã} \\Rightarrow \\text{qua trạm 8, tới trạm 9}; \\; \\text{trạm 14 từ chối, trạm 13 thấy vô danh} \\Rightarrow \\hl{401}$$""",
           """Phép tính thứ nhất, ca không mang mã. Câu quan sát có in ra, nghĩa là yêu cầu đã qua trạm đọc mã.
           Nó bị trạm kiểm quyền từ chối, và vì người gọi còn vô danh nên trạm dịch lỗi trả bốn trăm lẻ một.
           Hàng cuối là đầu mục thách thức, báo cho bên gọi rằng nơi này đòi mã truy cập.""",
           focus=["2.1", "2.2", [3, "2.3"], "2.4"], clear=True),
        st(out(OUT_B) + out(OUT_E, "Ca mã hết hạn") + """
$$② \\; \\text{mã hỏng} \\Rightarrow \\text{dừng ở trạm 8, không tới trạm 9} \\Rightarrow \\hl{401}$$""",
           """Phép tính thứ hai, ca mã ký bằng khoá khác. Lần này không có câu quan sát, nghĩa là yêu cầu dừng ngay ở trạm đọc mã.
           Mã trạng thái vẫn là bốn trăm lẻ một như phép một, nhưng trạm trả lời thì khác, và đầu mục ghi rõ lý do là chữ ký không hợp lệ.
           Ca mã hết hạn cũng dừng ở trạm đọc mã với bốn trăm lẻ một, kèm đúng thời điểm mã đã hết hạn.""",
           focus=["2.1", 5, ["2.2", "2.3"], 4], clear=True),
        st(out(OUT_C) + """
$$③ \\; \\text{mã tốt, thiếu quyền} \\Rightarrow \\text{tới trạm 9}; \\; \\text{trạm 14 từ chối, trạm 13 thấy đã xác thực} \\Rightarrow \\hl{403}$$""",
           """Phép tính thứ ba, mã của An là mã thật nhưng chỉ có quyền số dư. Câu quan sát có in, vì mã qua được trạm đọc mã.
           Trạm kiểm quyền từ chối giống phép một, nhưng lần này người gọi đã được xác thực, nên trạm dịch lỗi trả bốn trăm lẻ ba.
           Đầu mục thách thức ghi lý do là phạm vi quyền không đủ cho yêu cầu này.""",
           focus=["2.1", "2.2", [3, "2.3"], "2.4"], clear=True),
        st(out(OUT_D) + """
$$④ \\; \\text{mã tốt, đủ quyền} \\Rightarrow \\text{qua cả 14 trạm} \\Rightarrow \\hlg{200}$$""",
           """Phép tính thứ tư, mã của Bình có quyền hạn mức. Yêu cầu qua trạm quan sát, qua trạm kiểm quyền, rồi tới dịch vụ.
           Mã trạng thái là hai trăm, nên không trạm nào chặn yêu cầu này.
           Vậy cùng một địa chỉ cho ba kết quả, bốn trăm lẻ một, bốn trăm lẻ ba và hai trăm, đúng như đề bài.""",
           focus=["2.1", ["2.2", "2.3"], "2.4", 3], clear=True),
        st(code(J_LB, "ChiaTai.java (trích) — MÔ PHỎNG bằng Java thuần, không phải Spring Cloud", lines=(2, 12)),
           """Phần chia tải thì máy này không dựng cổng và sổ đăng ký thật, nên ta dùng một mô phỏng nhỏ bằng Java thuần.
           Mỗi bản có một tên và một cờ sức khoẻ, và hàm chia trước hết lọc ra các bản khoẻ.
           Vòng lặp giao yêu cầu thứ i cho bản thứ i chia lấy dư cho số bản khoẻ, rồi đếm số yêu cầu mỗi bản nhận.""",
           focus=[0, ["2.2", "2.3", "2.4"], ["2.6", "2.7", "2.8", "2.9"]], clear=True),
        st(code(J_LB, "ChiaTai.java (tiếp): ba bản khoẻ, rồi bản 2 trượt", lines=(13, 20)) + out(OUT_LB, "Kết quả chạy thật của mô phỏng") + """
$$⑤ \\; 3 - 1 = 2 \\text{ bản khoẻ}; \\quad 100 : 2 = \\hlg{50} \\text{ mỗi bản}$$""",
           """Hàm chính thử hai lần với một trăm yêu cầu. Khi cả ba bản khoẻ, bản một nhận ba mươi tư, hai bản kia nhận ba mươi ba.
           Khi bản hai trượt kiểm sức khoẻ, nó biến khỏi kết quả, còn bản một và bản ba mỗi bản nhận năm mươi.
           Đó là phép tính thứ năm: ba bản trừ một bản trượt còn hai, và một trăm chia hai là năm mươi yêu cầu mỗi bản.""",
           focus=[2, ["2.2", "2.3", "2.4", "4.1"], ["2.5", "2.6", "2.7", "4.2"], 5], clear=True),
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
        st(code(PY_CHECK, "Bảng quyết định bằng Python, không dùng Spring", lines=(1, 8)),
           """Ta kiểm bằng một đường khác hẳn, không dùng Spring: tự viết bảng quyết định thành một hàm ngắn.
           Không có mã thì trả bốn trăm lẻ một, vì chưa biết bạn là ai.
           Có mã mà chữ ký sai hoặc đã hết hạn thì cũng bốn trăm lẻ một, vì mã không tin được.
           Mã tin được mà thiếu quyền cần có thì bốn trăm lẻ ba, còn lại là hai trăm.""",
           focus=[0, ["2.2", "2.3"], ["2.4", "2.5"], ["2.6", "2.7", "2.8"]], clear=True),
        st(code(PY_CHECK, "(tiếp) năm ca như chương trình Java, và phép chia tải", lines=(9, 13)) + out(OUT_CHECK),
           """Phần tiếp theo mô tả lại bốn mã như trong chương trình Java, rồi hỏi hàm năm ca theo đúng thứ tự cũ.
           Lệnh cuối tính phép chia tải bằng cách đếm: một trăm chia hai, và số yêu cầu mỗi bản nhận khi đủ ba bản.
           Kết quả chạy thật cho năm mã trạng thái, rồi năm mươi và bộ ba ba mươi tư, ba mươi ba, ba mươi ba.""",
           focus=[["2.1", "2.2", "2.3", "2.4"], "2.5", 4], clear=True),
        st(table(["ca", "Spring Security chạy thật", "bảng quyết định", "trạm trả lời"],
                 [["không mang mã", "401", "401", "trạm dịch lỗi (13)"],
                  ["mã ký bằng khoá khác", "401", "401", "trạm đọc mã (8)"],
                  ["mã thật, thiếu quyền", "403", "403", "trạm dịch lỗi (13)"],
                  ["mã thật, đủ quyền", "200", "200", "không trạm nào chặn"],
                  ["mã thật, đã hết hạn", "401", "401", "trạm đọc mã (8)"],
                  ["100 yêu cầu, 2 bản khoẻ", "—", "50 mỗi bản", "mô phỏng Java: 50 và 50"]]),
           """Bảng này đặt hai đường cạnh nhau. Cả năm ca, bộ khung của Spring chạy thật và bảng quyết định viết tay cho cùng một mã trạng thái.
           Cột cuối nhắc trạm nào trả lời, lấy từ câu quan sát của lần chạy thật.
           Phép chia tải cũng khớp giữa phép đếm và mô phỏng.
           Vì hai đường độc lập cho cùng kết quả, ta tin cách hiểu của mình về chuỗi bộ lọc.""",
           focus=[0, 0, 0, "1.7", 0], clear=True),
    ], checks=[f"[alg.bnx_l17_status('GET', t, 'han_muc') for t in ({T_NONE}, {T_GIA}, {T_AN}, {T_BINH}, {T_CU})] == [401, 401, 403, 200, 401]",
               "100 // 2 == 50 and [len(range(i, 100, 3)) for i in range(3)] == alg.bnx_l17_round_robin([True] * 3, 100) == [34, 33, 33]",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]",
               "alg.bnx_l17_pos('ExceptionTranslationFilter') == 13 and alg.bnx_l17_pos('BearerTokenAuthenticationFilter') == 8"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Coi 401 và 403 là một, hoặc trả <b class="red">403 cho mọi lần từ chối</b>.
401 là <b>chưa biết bạn là ai</b>: bên gọi nên lấy mã mới rồi thử lại. 403 là <b>biết rồi nhưng không cho</b>: thử lại với đúng mã ấy vẫn 403.
<br><span class="note">Trả sai mã thì ứng dụng khách hoặc xin mã mới mãi, hoặc không bao giờ xin lại.</span></div>""",
           """Lỗi thứ nhất, của người mới, là coi bốn trăm lẻ một và bốn trăm lẻ ba là một.
           Bốn trăm lẻ một là chưa biết bạn là ai, nên bên gọi cần lấy mã mới rồi thử lại.
           Bốn trăm lẻ ba là biết rồi nhưng không cho, nên thử lại với đúng mã ấy thì vẫn bị cấm.
           Trả sai con số thì ứng dụng khách hoặc xin mã mới mãi, hoặc không bao giờ xin lại.""", clear=True),
        st(code(J_RUN, "ChayThu.java (hết): hai ca gửi lệnh ghi POST", lines=(50, 51)) + out(OUT_FG),
           """Lỗi thứ hai lộ ra ngay lúc mới dựng. Hai ca cuối của chương trình gửi lệnh ghi thay cho lệnh đọc.
           Kết quả chạy thật: lệnh ghi không mang mã nhận bốn trăm lẻ ba chứ không phải bốn trăm lẻ một, và không hề qua trạm quan sát.
           Còn lệnh ghi mang mã đủ quyền thì qua hết chuỗi và nhận hai trăm.""",
           focus=[0, 2, ["4.1", "4.2"], ["4.3", "4.4", "4.5", "4.6"]], clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Thấy lệnh POST không mang mã nhận <b class="red">403</b> rồi đi tìm lỗi phân quyền.
Thủ phạm là trạm <b>chống giả mạo yêu cầu</b> (CsrfFilter) ở vị trí 5, đứng <b>trước</b> trạm đọc mã ở vị trí 8, và mặc định bật cho các lệnh ghi.
<br><span class="note">Hướng dẫn của Spring Security: dịch vụ nền không phục vụ trình duyệt có thể tắt lớp này, và nên cân nhắc trước khi tắt. Bài học chung: cùng một con số 403, phải hỏi <b>trạm nào</b> trả.</span>
<br><span class="note">Quan sát chạy thật ở bộ kiểm, với cấu hình này: lệnh POST mang mã ký sai nhận 401 chứ không phải 403, nên yêu cầu có đầu mục mã không bị trạm chống giả mạo chặn. Hướng dẫn chính thức đã đọc không giải thích cơ chế, nên bài không khẳng định lý do.</span></div>""",
           """Đó là lỗi thứ hai, của người đã đi làm: thấy lệnh ghi không mang mã nhận bốn trăm lẻ ba rồi đi tìm lỗi phân quyền.
           Thủ phạm là trạm chống giả mạo yêu cầu ở vị trí năm, đứng trước trạm đọc mã ở vị trí tám, và mặc định bật cho các lệnh ghi.
           Theo hướng dẫn chính thức của Spring, dịch vụ nền không phục vụ trình duyệt có thể tắt lớp này, và nên cân nhắc trước khi tắt.
           Chạy thật với cấu hình này, lệnh ghi mang mã ký sai nhận bốn trăm lẻ một chứ không phải bốn trăm lẻ ba.
           Vậy yêu cầu có mã không bị trạm này chặn, còn lý do thì hướng dẫn không nêu.
           Bài học chung là cùng một con số bốn trăm lẻ ba, ta phải hỏi trạm nào đã trả nó.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc hệ thống lớn dần).</b> <b class="red">Chỉ kiểm quyền ở cổng</b>, các dịch vụ phía sau tin mọi yêu cầu tới mình.
Lúc đầu chỉ có một đường vào nên ổn. Hệ thống lớn dần, dịch vụ gọi thẳng nhau trong mạng nội bộ, không qua cổng: trên đường ấy không còn lần kiểm quyền nào.
<br><span class="note">Cách chữa: cổng kiểm thô (có mã, mã còn hạn), còn <b>mỗi dịch vụ là một máy chủ tài nguyên</b>, tự kiểm chữ ký và quyền như ví dụ vừa chạy.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm, lộ ra khi hệ thống lớn dần: chỉ kiểm quyền ở cổng, còn các dịch vụ phía sau tin mọi yêu cầu tới mình.
           Lúc đầu chỉ có một đường vào nên mọi thứ ổn.
           Về sau các dịch vụ gọi thẳng nhau trong mạng nội bộ mà không qua cổng, nên trên đường ấy không có lần kiểm quyền nào.
           Cách chữa là cổng chỉ kiểm thô, còn mỗi dịch vụ là một máy chủ tài nguyên, tự kiểm chữ ký và quyền như ví dụ vừa chạy.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> Để <b class="red">mật khẩu dạng chữ thường</b> trong kho cấu hình tập trung.
Kho ấy thường là một kho mã nguồn: ai đọc được kho, đọc được lịch sử, là đọc được mật khẩu, kể cả mật khẩu đã đổi từ năm trước.</div>"""
           + code(Y_CIPHER, "Tệp cấu hình trong kho (chép từ hướng dẫn của Spring Cloud Config, không chạy trên máy này)")
           + """<p style='margin-top:18px'><span class='note'>Giá trị bắt đầu bằng <code>{cipher}</code> là bản đã mã hoá; máy chủ cấu hình giải mã rồi mới gửi cho dịch vụ qua HTTP. Việc còn lại: đổi mật khẩu đã lộ trong lịch sử kho; giữ kín khoá giải mã (máy chủ cần khoá đối xứng hoặc cặp khoá); bảo vệ đường truyền, vì giá trị đã giải mã đi qua mạng.</span></p>""",
           """Lỗi thứ tư, cũng của người đã đi làm, lộ ra khi vận hành lâu dài: để mật khẩu dạng chữ thường trong kho cấu hình tập trung.
           Kho ấy thường là một kho mã nguồn, nên ai đọc được lịch sử của kho là đọc được mật khẩu, kể cả mật khẩu đã đổi từ năm trước.
           Cách chữa có sẵn trong Spring Cloud: giá trị mật khẩu trong tệp này bắt đầu bằng một nhãn báo đây là bản đã mã hoá.
           Máy chủ cấu hình giải mã giá trị ấy rồi mới gửi cho dịch vụ, nên trong kho không còn mật khẩu đọc được.
           Nhưng việc chưa xong, vì mật khẩu đã lộ trong lịch sử kho thì phải đổi ngay.
           Khoá giải mã nằm ở máy chủ cấu hình, nên khoá ấy giờ là bí mật cần giữ kín, và giá trị đã giải mã đi qua mạng tới dịch vụ nên đường truyền phải được bảo vệ.""",
           focus=[1, 1, "3.4", 4, 4, 4], clear=True),
    ], checks=[f"alg.bnx_l17_status('GET', {T_NONE}, 'han_muc') == 401 and alg.bnx_l17_status('GET', {T_AN}, 'han_muc') == 403",
               f"alg.bnx_l17_trace('POST', {T_NONE}, 'han_muc') == (403, 'CsrfFilter', False, False)",
               f"alg.bnx_l17_trace('POST', {T_BINH}, 'han_muc') == (200, None, True, True)",
               "alg.bnx_l17_pos('CsrfFilter') == 5 < alg.bnx_l17_pos('BearerTokenAuthenticationFilter') == 8"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Luật như trong bài: <code>/han-muc</code> đòi quyền <code>SCOPE_han_muc</code>, đường dẫn khác chỉ cần đã xác thực. Mã thật, còn hạn, scope <code>so_du</code>. Lệnh đọc tới <code>/so-du</code> nhận mã nào? Tới <code>/han-muc</code> nhận mã nào, do trạm số mấy trả?"],
                  ["2", "Một dịch vụ đăng ký 4 bản, 1 bản trượt kiểm sức khoẻ. 90 yêu cầu chia xoay vòng thì mỗi bản khoẻ nhận bao nhiêu? Nếu trượt 2 bản thì sao?"],
                  ["3", "Quyết định (số minh hoạ): 3 bản, 100 yêu cầu mỗi giây chia đều. Một bản chết hẳn. Sổ kiểm sức khoẻ mỗi 10 giây, giả định đã bật tuỳ chọn chỉ lấy bản đạt kiểm (query-passing); bên gọi giữ danh sách bản trong bộ đệm 35 giây. Chọn: giữ nguyên, giảm chu kỳ kiểm xuống 2 giây, hay giữ nguyên và cho thử lại sang bản khác?"]]),
           """Đến lượt bạn. Câu một, với luật như trong bài, một mã thật chỉ có quyền số dư gửi lệnh đọc tới hai đường dẫn thì nhận những mã trạng thái nào?
           Câu hai, bốn bản đăng ký, một bản trượt kiểm sức khoẻ, chín mươi yêu cầu chia xoay vòng thì mỗi bản khoẻ nhận bao nhiêu?
           Câu ba, một bản chết hẳn, sổ kiểm mỗi mười giây, đã bật lọc bản đạt kiểm, danh sách cũ giữ ba mươi lăm giây, bạn chọn cách nào trong ba cách trên màn hình?
           Hãy tạm dừng lại và làm từng câu ra giấy trước khi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: mã thật nên qua trạm đọc mã (số 8); phần còn lại do luật của từng đường dẫn quyết định.</p>
$$\\text{/so-du: chỉ cần đã xác thực} \\Rightarrow \\hlg{200}; \\qquad \\text{/han-muc: thiếu quyền} \\Rightarrow \\hlg{403} \\text{, do trạm dịch lỗi số 13 trả}$$""",
           """Đáp án câu một. Mã thật nên qua được trạm đọc mã. Đường dẫn số dư chỉ cần đã xác thực, nên nhận hai trăm.
           Đường dẫn hạn mức đòi quyền mà mã không có, nên trạm kiểm quyền từ chối, và trạm dịch lỗi số mười ba trả bốn trăm lẻ ba."""),
        st("""<p>Câu 2: chỉ các bản khoẻ được chia việc.</p>
$$4 - 1 = 3 \\text{ bản}: \\; 90 : 3 = \\hlg{30} \\text{ mỗi bản}; \\qquad 4 - 2 = 2 \\text{ bản}: \\; 90 : 2 = \\hlg{45} \\text{ mỗi bản}$$""",
           """Đáp án câu hai. Trượt một bản thì còn ba bản khoẻ, chín mươi chia ba là ba mươi yêu cầu mỗi bản.
           Trượt hai bản thì còn hai, mỗi bản nhận bốn mươi lăm, tức là tải trên mỗi bản còn sống tăng lên gấp rưỡi."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["giữ nguyên: kiểm 10 giây, đệm 35 giây", "không phải làm gì", "bản chết còn nhận việc tới 10 + 35 = 45 giây: khoảng 100 × 45 : 3 = 1500 yêu cầu lỗi"],
                  ["giảm chu kỳ kiểm xuống 2 giây", "phát hiện sớm hơn 8 giây", "vẫn tới 2 + 35 = 37 giây, khoảng 1234 yêu cầu lỗi (cận trên); số lần kiểm tăng 5 lần"],
                  ["giữ nguyên, lỗi kết nối thì thử lại sang bản khác", "yêu cầu rơi vào bản chết được cứu ngay", "chỉ an toàn với lệnh đọc; lệnh ghi phải có khoá lũy đẳng, kẻo xử lý hai lần"]]),
           """Đáp án câu ba, tính bằng cận trên và với giả định đã bật tuỳ chọn chỉ lấy bản đạt kiểm. Giữ nguyên thì bản chết còn nhận việc tới bốn mươi lăm giây, vì mười giây chờ lần kiểm kế cộng ba mươi lăm giây bộ đệm.
           Mỗi giây một phần ba trong một trăm yêu cầu rơi vào bản ấy, nên có khoảng một nghìn năm trăm yêu cầu lỗi.
           Giảm chu kỳ kiểm xuống hai giây chỉ bớt được tám giây, vẫn còn khoảng một nghìn hai trăm ba mươi tư yêu cầu lỗi, vì bộ đệm mới là phần lớn.
           Cho thử lại sang bản khác thì cứu được yêu cầu ngay, nhưng chỉ an toàn với lệnh đọc, còn lệnh ghi phải có khoá lũy đẳng kẻo xử lý hai lần.
           Một lập luận hợp lý là chọn cách ba cho lệnh đọc và lệnh có khoá lũy đẳng, rồi mới xét rút ngắn bộ đệm.""",
           focus=[0, "1.2", "1.2", "1.3", "1.4", "1.4"]),
    ], checks=[f"alg.bnx_l17_status('GET', {T_AN}, None) == 200",
               f"alg.bnx_l17_trace('GET', {T_AN}, 'han_muc')[:2] == (403, 'ExceptionTranslationFilter') and alg.bnx_l17_pos('ExceptionTranslationFilter') == 13",
               "alg.bnx_l17_round_robin([True, False, True, True], 90) == [30, 0, 30, 30]",
               "alg.bnx_l17_round_robin([True, False, False, True], 90) == [45, 0, 0, 45] and 45 / 30 == 1.5",
               "alg.bnx_l17_stale_window(10, 35) == 45 and alg.bnx_l17_lost(100, 3, 45) == 1500",
               "alg.bnx_l17_stale_window(2, 35) == 37 and alg.bnx_l17_lost(100, 3, 37) == 1233 and -(-100 * 37 // 3) == 1234",
               "alg.bnx_l17_stale_window(10, 35) - alg.bnx_l17_stale_window(2, 35) == 8 and 10 // 2 == 5"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("chuỗi trạm có thứ tự", "trạm đọc mã: mã hỏng thì 401", "trạm kiểm quyền + trạm dịch lỗi: 401 hoặc 403",
                 "mỗi dịch vụ tự kiểm mã", "cổng tra sổ, chia cho bản khoẻ"),
           """Tổng kết chuỗi lập luận. Yêu cầu đi qua một chuỗi trạm có thứ tự, trong đó trạm đọc mã trả bốn trăm lẻ một khi mã hỏng.
           Trạm kiểm quyền từ chối, còn trạm dịch lỗi chọn bốn trăm lẻ một cho khách vô danh và bốn trăm lẻ ba cho người đã xác thực.
           Mỗi dịch vụ tự kiểm mã như một máy chủ tài nguyên, còn cổng tra sổ đăng ký rồi chia việc cho các bản khoẻ."""),
        st("""<div class='box key'><b>Tư duy:</b> 401 là chưa biết bạn là ai, 403 là biết rồi nhưng không cho. Gặp một lần từ chối, đừng chỉ nhìn con số:
hãy hỏi <b>trạm nào</b> trả nó. Và đừng tin một lớp kiểm duy nhất: cổng kiểm thô, từng dịch vụ kiểm lại.</div>""",
           """Điều cần mang theo. Bốn trăm lẻ một là chưa biết bạn là ai, bốn trăm lẻ ba là biết rồi nhưng không cho.
           Gặp một lần từ chối, đừng chỉ nhìn con số mà hãy hỏi trạm nào đã trả nó.
           Và đừng tin một lớp kiểm duy nhất, vì cổng chỉ kiểm thô, còn từng dịch vụ phải kiểm lại."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Spring Security: một yêu cầu đi qua những gì, 401 khác 403 ở đâu?", "chuỗi bộ lọc có thứ tự; trạm đọc mã trả 401 khi mã hỏng; trạm kiểm quyền từ chối, trạm dịch lỗi trả 401 nếu còn vô danh, 403 nếu đã xác thực"],
                  ["Spring Security OAuth2: dịch vụ kiểm mã truy cập thế nào?", "là máy chủ tài nguyên: kiểm chữ ký bằng khoá của máy chủ cấp mã, kiểm hạn, đổi scope thành quyền <code>SCOPE_…</code>; từng dịch vụ tự kiểm, không chỉ cổng"],
                  ["Spring Cloud và Consul để làm gì?", "sổ đăng ký giữ các bản và kiểm sức khoẻ; cổng ghi tên dịch vụ, tra sổ rồi chia xoay vòng, và chỉ gặp bản khoẻ khi đã bật lọc theo kiểm sức khoẻ; cấu hình tập trung, mật khẩu phải mã hoá"]]),
           """Nếu người phỏng vấn hỏi về các dòng bảo mật và Spring Cloud trên hồ sơ, đây là ba câu hay gặp.
           Một yêu cầu đi qua những gì: qua chuỗi bộ lọc có thứ tự, và ta nói được trạm nào trả bốn trăm lẻ một, trạm nào trả bốn trăm lẻ ba.
           Dịch vụ kiểm mã thế nào: nó là máy chủ tài nguyên, kiểm chữ ký, kiểm hạn, rồi đổi phạm vi quyền thành quyền, và từng dịch vụ tự kiểm.
           Sổ đăng ký và cổng để làm gì: sổ giữ các bản và kiểm sức khoẻ, cổng tra sổ rồi chia xoay vòng, chỉ gặp bản khoẻ khi đã bật lọc, còn mật khẩu phải mã hoá.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st(table(["Câu hỏi tiếp theo hay gặp", "ý trả lời (theo hướng dẫn chính thức)"],
                 [["Cổng có tự loại bản hỏng không?", "Consul kiểm mỗi 10 giây, hỏng thì đánh dấu critical; lọc bản hỏng cần bật <code>query-passing</code> (mặc định false) hoặc bộ kiểm của bộ chia tải (mặc định tắt)"],
                  ["Máy chủ tài nguyên kiểm những gì mặc định?", "nơi cấp (iss), hạn (exp, nbf); đối tượng nhận (aud) phải khai thêm"],
                  ["Khởi động có cần máy chủ cấp mã chạy không?", "không: việc tìm khoá làm ở yêu cầu đầu tiên có mã"],
                  ["Khi nào tắt chống giả mạo yêu cầu?", "dịch vụ nền không phục vụ trình duyệt có thể tắt, sau khi cân nhắc"]]),
           """Còn bốn câu hỏi tiếp theo hay gặp, trả lời theo hướng dẫn chính thức. Sổ đăng ký kiểm sức khoẻ mỗi mười giây và đánh dấu bản hỏng, nhưng lọc bản hỏng khỏi danh sách phải bật tuỳ chọn riêng, mặc định đang tắt.
           Máy chủ tài nguyên mặc định kiểm nơi cấp và hạn dùng của mã, còn đối tượng nhận mã phải khai thêm.
           Việc tìm khoá làm ở yêu cầu đầu tiên có mã, nên khởi động dịch vụ không bị buộc vào máy chủ cấp mã.
           Cuối cùng, dịch vụ nền không phục vụ trình duyệt có thể tắt lớp chống giả mạo yêu cầu, nhưng hãy cân nhắc trước khi tắt.""", clear=True),
        st("""<p>Bài sau: kiểm thử Java, viết <b>ca kiểm</b> cho từng nhánh của một hàm và thay phần phụ thuộc bên ngoài bằng <b>đối tượng giả</b>.</p>""",
           """Ở bài mười tám, ta viết ca kiểm tự động cho từng nhánh của một hàm, và thay phần phụ thuộc bên ngoài bằng đối tượng giả.""",
           forward_ref=True),
    ], checks=[f"alg.bnx_l17_status('GET', {T_NONE}, 'han_muc') == 401 and alg.bnx_l17_status('GET', {T_AN}, 'han_muc') == 403",
               "alg.bnx_l17_round_robin([True, False, True], 100) == [50, 0, 50]"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
    return lesson("L17", "spring_security_spring_cloud",
                  "Bài 17 — Spring Security và Spring Cloud: chuỗi bộ lọc, cổng và khám phá dịch vụ",
                  "curriculum/bnx.yaml L17; audit/bnx/verify_bnx.py L17; audit/bnx/sources_l17.md: hướng dẫn Spring Security 7.1.2 (Architecture, "
                  "OAuth2 Resource Server, CSRF), Spring Cloud Gateway 5.0.4, Spring Cloud Commons 5.0.4 (LoadBalancer), Spring Cloud Consul 5.0.4, "
                  "Spring Cloud Config 5.0.6 (đọc 2026-11-11); Spring Security 7.1.2 chạy thật trên Temurin JDK 21.0.13; phần chia tải là mô phỏng",
                  ["Lần theo một yêu cầu qua chuỗi bộ lọc bảo mật và nói bộ lọc nào trả 401, bộ lọc nào trả 403",
                   "Cấu hình một dịch vụ kiểm mã truy cập như máy chủ tài nguyên",
                   "Giải thích vai trò của cổng, cấu hình tập trung và sổ đăng ký dịch vụ trong Spring Cloud",
                   "Tính cách cổng chia tải khi một bản dịch vụ trượt kiểm sức khoẻ"],
                  scenes)
