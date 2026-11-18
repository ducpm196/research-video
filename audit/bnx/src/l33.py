import lib2
from lib2 import *
from libj import jstep, JROW
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from labkit import write_lab, practice_steps, practice_scene

lib2.begin("L33")

# ── Mã chạy THẬT: JDK 21 + Tomcat nhúng 10.1.61 (tomcat-embed-core, tomcat-embed-jasper; jar ở audit/bnx/deps/l33, sha256 ở README.md, tải bằng Maven từ Maven Central).
#    Tomcat nhúng chạy đúng bộ chứa Servlet và bộ biên dịch JSP của Tomcat; KHÔNG chạy JBoss/WildFly (chỉ giảng khái niệm). Đầu ra tất định
#    (cổng ngẫu nhiên không in, thời gian không in, chỉ in số đếm và đúng/sai) — đệm ở audit/bnx/progcache/L33.json. ──
J_CHAO = prog("Chao", r'''
import jakarta.servlet.http.*;
import java.io.IOException;

public class Chao extends HttpServlet {
  int soYeuCau = 0;
  @Override public void init() {
    System.out.println("init: tao 1 lan");
  }
  @Override protected void doGet(HttpServletRequest q, HttpServletResponse r)
      throws IOException {
    soYeuCau++;
    r.setContentType("text/plain");
    r.getWriter().print("yeu cau so " + soYeuCau);
  }
  @Override public void destroy() {
    System.out.println("destroy: thu hoi 1 lan");
  }
}
''', lang="java", kind="other", reason="Chao.java: Servlet tối thiểu (jakarta.servlet), có init, doGet, destroy và một trường đếm của thể hiện.",
    read_check="Biên dịch cùng jar Tomcat nhúng và chạy trong nguồn L33_ChayWar.")

J_MAY = prog("May", r'''
import org.apache.catalina.startup.Tomcat;
import java.net.URI;
import java.net.http.*;
import java.nio.file.*;
import java.util.stream.*;

public class May {
  static String lay(int cong, String duong) throws Exception {
    URI u = URI.create("http://localhost:" + cong + "/" + duong);
    return HttpClient.newHttpClient()
        .send(HttpRequest.newBuilder(u).build(),
              HttpResponse.BodyHandlers.ofString()).body().trim();
  }
  static long dem(Path thuMuc) throws Exception {
    try (Stream<Path> s = Files.walk(thuMuc)) {
      return s.filter(Files::isRegularFile).count();
    }
  }
  static void chep(Path nguon, Path dich) throws Exception {
    try (Stream<Path> s = Files.walk(nguon)) {
      for (Path p : (Iterable<Path>) s::iterator) {
        Path d = dich.resolve(nguon.relativize(p).toString());
        if (Files.isDirectory(p)) Files.createDirectories(d);
        else Files.copy(p, d, StandardCopyOption.REPLACE_EXISTING);
      }
    }
  }
  public static void main(String[] a) throws Exception {
    Path goc = Files.createTempDirectory("tc");
    Tomcat t = new Tomcat();
    t.setBaseDir(goc.toString());
    t.setPort(0);
    t.getConnector();
    String ngu = a[1].isEmpty() ? "" : "/" + a[1];
    t.addWebapp(ngu, Path.of(a[0]).toAbsolutePath().toString());
    t.start();
    int cong = t.getConnector().getLocalPort();
    long truoc = dem(goc.resolve("work"));
    for (int i = 2; i < a.length; i++)
      System.out.println(a[i] + " -> " + lay(cong, a[i]));
    long sau = dem(goc.resolve("work"));
    if (sau > 0) {
      System.out.println("tep Jasper sinh ra: truoc " + truoc + ", sau " + sau);
      chep(goc.resolve("work"), Path.of("jsp-work"));
    }
    t.stop();
    t.destroy();
  }
}
''', lang="java", kind="other", reason="May.java: dựng Tomcat nhúng, triển khai một thư mục hoặc gói .war, gửi yêu cầu HTTP rồi tắt.",
    read_check="Biên dịch cùng jar Tomcat nhúng và chạy trong nguồn L33_ChayWar, L33_ChayJsp.")

J_TAI = prog("Tai", r'''
import jakarta.servlet.http.*;
import org.apache.catalina.Context;
import org.apache.catalina.startup.Tomcat;
import org.apache.coyote.AbstractProtocol;
import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class Tai {
  static AtomicInteger dang = new AtomicInteger(), toiDa = new AtomicInteger();

  public static void main(String[] a) throws Exception {
    Path goc = Files.createTempDirectory("tc");
    Tomcat t = new Tomcat();
    t.setBaseDir(goc.toString());
    t.setPort(0);
    ((AbstractProtocol<?>) t.getConnector().getProtocolHandler()).setMaxThreads(4);
    Context ctx = t.addContext("", goc.toString());
    Tomcat.addServlet(ctx, "cham", new HttpServlet() {
      @Override protected void doGet(HttpServletRequest q, HttpServletResponse r)
          throws IOException {
        toiDa.accumulateAndGet(dang.incrementAndGet(), Math::max);
        try { Thread.sleep(100); } catch (InterruptedException e) { }
        dang.decrementAndGet();
        r.getWriter().print("ok");
      }
    });
    ctx.addServletMappingDecoded("/cham", "cham");
    t.start();
    URI u = URI.create("http://localhost:" + t.getConnector().getLocalPort() + "/cham");
    HttpClient c = HttpClient.newHttpClient();
    for (int n : new int[] {4, 40, 200}) {
      toiDa.set(0);
      long bd = System.nanoTime();
      List<CompletableFuture<?>> ds = new ArrayList<>();
      for (int i = 0; i < n; i++)
        ds.add(c.sendAsync(HttpRequest.newBuilder(u).build(),
                           HttpResponse.BodyHandlers.ofString()));
      for (var d : ds) d.join();
      long ms = (System.nanoTime() - bd) / 1_000_000, can = (n + 3) / 4 * 100L;
      System.out.println(n + " yeu cau, 4 luong: dong thoi toi da " + toiDa
          + ", thoi gian >= " + can + " ms: " + (ms >= can));
    }
    t.stop();
    t.destroy();
  }
}
''', lang="java", kind="other", reason="Tai.java: Tomcat nhúng với bể luồng 4 và một Servlet chậm 100 ms; đo số cuộc xử lý đồng thời tối đa khi n yêu cầu đến cùng lúc.",
    read_check="Biên dịch cùng jar Tomcat nhúng và chạy trong nguồn L33_ChayTai.")

_JARS = r'''
D=/d/research-video/audit/bnx/deps/l33
ls $D/tomcat-embed-core-10.1.61.jar >/dev/null 2>&1 || { echo "NOT_VERIFIED: thieu jar Tomcat" >&2; exit 97; }
mkdir -p lib out && cp $D/*.jar lib/
'''

SH_WAR = prog("ChayWar", _JARS + r'''
javac -cp "lib/*" -d out May.java && jar cf lib/may.jar -C out .
mkdir -p war/WEB-INF/classes
cat > war/WEB-INF/web.xml <<'EOF'
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee" version="6.0">
  <servlet>
    <servlet-name>chao</servlet-name>
    <servlet-class>Chao</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>chao</servlet-name>
    <url-pattern>/chao</url-pattern>
  </servlet-mapping>
</web-app>
EOF
javac -cp "lib/*" -d war/WEB-INF/classes Chao.java
jar --create --file app.war -C war .
jar tf app.war | sort
java -cp "lib/*" May app.war app app/chao app/chao app/chao 2>/dev/null
''', lang="bash", files={"May.java": "May", "Chao.java": "Chao"}, timeout=300,
    claims=["gói .war là tệp nén gồm WEB-INF/web.xml và WEB-INF/classes/Chao.class; Tomcat nhúng nạp gói: init chạy 1 lần, ba yêu cầu thấy bộ đếm 1, 2, 3 (cùng một thể hiện), destroy chạy 1 lần khi tắt"])

SH_JSP = prog("ChayJsp", _JARS + r'''
javac -cp "lib/*" -d out May.java && jar cf lib/may.jar -C out .
mkdir -p site
cat > site/chao.jsp <<'EOF'
<%@ page contentType="text/plain" %>
Xin chao <%= request.getParameter("ten") %>, 2 + 3 = <%= 2 + 3 %>
EOF
java -cp "lib/*" May site "" "chao.jsp?ten=An" "chao.jsp?ten=Binh" 2>/dev/null
find jsp-work -type f | sed 's#.*/##' | sort
J=jsp-work/Tomcat/localhost/ROOT/org/apache/jsp
grep -n "out.write\|out.print" $J/chao_jsp.java
javap -cp jsp-work/Tomcat/localhost/ROOT org.apache.jsp.chao_jsp |
  sed -n 2p | cut -d' ' -f1-6 | sed 's/org.apache.jasper.runtime.//'
''', lang="bash", files={"May.java": "May"}, timeout=300,
    claims=["trang JSP được dịch thành một lớp Java (Servlet) ở yêu cầu đầu: trước 0 tệp, sau 2 tệp (chao_jsp.java, chao_jsp.class); lớp sinh ra kế thừa HttpJspBase; văn bản cố định thành out.write, biểu thức thành out.print; yêu cầu thứ hai không sinh thêm tệp"])

SH_CU = prog("ChayCu", _JARS + r'''
cat > Cu.java <<'EOF'
import javax.servlet.http.HttpServlet;
public class Cu extends HttpServlet { }
EOF
javac -cp "lib/*" Cu.java 2>&1 | head -1
sed -i 's/javax\.servlet/jakarta.servlet/' Cu.java
javac -cp "lib/*" -d out Cu.java && echo "bien dich duoc"
''', lang="bash", timeout=200,
    claims=["Servlet viết theo javax.servlet không biên dịch với Tomcat 10.1 (package javax.servlet.http does not exist); đổi sang jakarta.servlet thì biên dịch được"])

SH_TAI = prog("ChayTai", _JARS + r'''
javac -cp "lib/*" -d out Tai.java && jar cf lib/tai.jar -C out .
java -cp "lib/*" Tai 2>/dev/null
''', lang="bash", files={"Tai.java": "Tai"}, timeout=300,
    claims=["bể 4 luồng: 4, 40 và 200 yêu cầu cùng lúc đều chỉ có tối đa 4 cuộc xử lý đồng thời; thời gian không thể nhỏ hơn số lượt × 100 ms"])

# ── Lab (cham.sh, Java thuần): bộ chứa tí hon có vòng đời init một lần, service nhiều lần, destroy một lần ──
LAB_JAVA = r'''
import java.util.*;
import java.util.function.Supplier;

interface MiniServlet {
    void init();
    String service(String ten);
    void destroy();
}

class ChaoVi implements MiniServlet {
    int dem = 0;
    public void init() { System.out.println("init ChaoVi"); }
    public String service(String ten) { dem++; return "Xin chao " + ten + " (so " + dem + ")"; }
    public void destroy() { System.out.println("destroy ChaoVi"); }
}

class ChaoAnh implements MiniServlet {
    int dem = 0;
    public void init() { System.out.println("init ChaoAnh"); }
    public String service(String ten) { dem++; return "Hello " + ten + " (so " + dem + ")"; }
    public void destroy() { System.out.println("destroy ChaoAnh"); }
}

public class MauBoChua {
    Map<String, Supplier<MiniServlet>> khaiBao = new LinkedHashMap<>();
    Map<String, MiniServlet> dangChay = new LinkedHashMap<>();

    String xuLy(String duong, String ten) {
        MiniServlet s = dangChay.get(duong);
        if (s == null) {
            s = khaiBao.get(duong).get();
            s.init();
            dangChay.put(duong, s);
        }
        return duong + "?ten=" + ten + " -> " + s.service(ten);
    }

    void dung() {
        for (MiniServlet s : dangChay.values()) s.destroy();
    }

    public static void main(String[] a) {
        MauBoChua c = new MauBoChua();
        c.khaiBao.put("/vi", ChaoVi::new);
        c.khaiBao.put("/en", ChaoAnh::new);
        System.out.println(c.xuLy("/vi", "Lan"));
        System.out.println(c.xuLy("/vi", "Minh"));
        System.out.println(c.xuLy("/en", "Ann"));
        System.out.println(c.xuLy("/vi", "Hoa"));
        c.dung();
    }
}
'''
LAB_OUT = """init ChaoVi
/vi?ten=Lan -> Xin chao Lan (so 1)
/vi?ten=Minh -> Xin chao Minh (so 2)
init ChaoAnh
/en?ten=Ann -> Hello Ann (so 1)
/vi?ten=Hoa -> Xin chao Hoa (so 3)
destroy ChaoVi
destroy ChaoAnh"""
LAB_DE = """# Lab BNX L33 — Bộ chứa tí hon: vòng đời Servlet bằng tay (Java thuần, không cần Tomcat)

Dán đoạn sau vào đầu tệp `MauBoChua.java` (ba kiểu này **cho sẵn**, đừng sửa):

```java
import java.util.*;
import java.util.function.Supplier;

interface MiniServlet {
    void init();
    String service(String ten);
    void destroy();
}

class ChaoVi implements MiniServlet {
    int dem = 0;
    public void init() { System.out.println("init ChaoVi"); }
    public String service(String ten) { dem++; return "Xin chao " + ten + " (so " + dem + ")"; }
    public void destroy() { System.out.println("destroy ChaoVi"); }
}

class ChaoAnh implements MiniServlet {
    int dem = 0;
    public void init() { System.out.println("init ChaoAnh"); }
    public String service(String ten) { dem++; return "Hello " + ten + " (so " + dem + ")"; }
    public void destroy() { System.out.println("destroy ChaoAnh"); }
}
```

Viết lớp `public class MauBoChua` (một **bộ chứa** tí hon):
1. Hai bảng: `khaiBao` (đường dẫn → hàm tạo, ví dụ `"/vi"` → `ChaoVi::new`) và `dangChay` (đường dẫn → thể hiện đã tạo). Dùng `LinkedHashMap` cho cả hai, vì `dung()` phải duyệt theo thứ tự thêm vào (`HashMap` không bảo đảm thứ tự).
2. `String xuLy(String duong, String ten)`: nếu đường dẫn **chưa có** thể hiện thì tạo bằng `khaiBao`, gọi `init()` **đúng một lần**, cất vào `dangChay`. Rồi trả `duong + "?ten=" + ten + " -> " + s.service(ten)`.
3. `void dung()`: gọi `destroy()` của từng thể hiện **đã tạo**, theo thứ tự tạo (duyệt `dangChay.values()` của `LinkedHashMap`).
4. `main`: khai báo `"/vi"` → `ChaoVi::new` và `"/en"` → `ChaoAnh::new`; in `xuLy("/vi","Lan")`, `xuLy("/vi","Minh")`, `xuLy("/en","Ann")`, `xuLy("/vi","Hoa")`; rồi gọi `dung()`.

Chạy: `javac MauBoChua.java && java MauBoChua`. Chấm: `bash labs/cham.sh BNX L33 MauBoChua.java`.
"""


def build():
    write_lab("BNX", "L33", LAB_DE, "java", LAB_JAVA, LAB_OUT)
    hook = sc("hook", "hook", "Dự án cũ vẫn đang chạy: đọc và sửa nó thế nào?", [
        st("""<p>Ngân hàng còn nhiều ứng dụng web viết bằng <b>Servlet</b> (chương trình phục vụ trên máy chủ web) và <b>JSP</b> (trang động), đóng gói <code>.war</code>, chạy trên <b>Tomcat</b> hoặc <b>JBoss</b>.</p>
<div class="box key">Đo thật: 3 yêu cầu chỉ khởi tạo chương trình <b>1 lần</b>; một trang JSP được <b>dịch thành chương trình Java</b> ở yêu cầu đầu (0 → 2 tệp); bể 4 luồng, 200 yêu cầu cùng lúc: tối đa <b>4</b> chạy đồng thời. Làm sao đọc và sửa được loại dự án này?</div>""",
           """Chào bạn, ngân hàng còn nhiều ứng dụng web viết bằng chương trình phục vụ trên máy chủ web và trang động, chạy trên Tomcat. Đo thật: ba yêu cầu chỉ khởi tạo một lần, một trang động được dịch thành mã Java, và bể bốn luồng chỉ chạy tối đa bốn cái cùng lúc. Làm sao đọc và sửa loại dự án này?"""),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["chương trình web chạy thế nào", "<b>vòng đời</b>: <code>init</code> một lần, <code>service</code> nhiều lần, <code>destroy</code> một lần"],
                  ["trang động .jsp là gì", "<b>dịch thành Servlet</b> ở yêu cầu đầu rồi biên dịch"],
                  ["Tomcat và JBoss/WildFly khác gì", "<b>bộ chứa Servlet</b> với <b>máy chủ ứng dụng đầy đủ</b>"],
                  ["đọc và bảo trì dự án cũ", "<code>web.xml</code>, gói <code>.war</code>, <code>javax</code> → <code>jakarta</code>, bể luồng"]]),
           """Hôm nay ta trả lời bốn câu: chương trình web chạy thế nào, trang động là gì, bộ chứa nhẹ khác máy chủ đầy đủ ở đâu, và cách đọc dự án cũ.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ], checks=["alg.bnx_l33_waves(200, 4) == 50"])

    pre = sc("prereq", "prereq", "Trước hết: sáu điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① yêu cầu và phản hồi HTTP", "trình duyệt gửi một yêu cầu, máy chủ trả một phản hồi", "<code>GET /chao</code>"],
                  ["② máy chủ web", "chương trình lắng nghe cổng mạng, gọi mã của ta khi có yêu cầu; <b>Tomcat nhúng</b> là Tomcat dùng như thư viện, do chính chương trình Java của ta khởi động", "Tomcat"],
                  ["③ luồng", "một dây việc chạy song song; nhiều yêu cầu cùng lúc cần nhiều luồng", "4 luồng = tối đa 4 việc cùng lúc"],
                  ["④ lớp và giao diện", "lớp con thừa hưởng việc của lớp cha; giao diện là hợp đồng các hàm phải có", "<code>extends HttpServlet</code>"],
                  ["⑤ tệp nén zip", "một tệp chứa nhiều tệp; <code>.war</code> thực chất là zip", "<code>jar tf app.war</code>"],
                  ["⑥ biên dịch", "đổi mã nguồn Java thành lớp chạy được", "<code>javac</code>"]]),
           """Trước hết ta cần hiểu sáu điều. Trình duyệt gửi yêu cầu thì máy chủ trả phản hồi. Máy chủ web gọi mã của ta khi có yêu cầu, còn bản nhúng do chính chương trình Java khởi động. Luồng là dây việc chạy song song. Lớp con thừa hưởng việc của lớp cha. Gói triển khai là tệp nén, và biên dịch là đổi mã nguồn thành lớp chạy được.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["alg.bnx_l33_waves(8, 4) == 2"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>Servlet</code>, <code>HttpServlet</code>", "chương trình Java nhận yêu cầu HTTP và trả phản hồi; chạy trong bộ chứa"],
                  ["<code>init</code>, <code>doGet</code>, <code>destroy</code>", "hàm khởi động (một lần), hàm xử lý yêu cầu GET, hàm thu hồi (một lần)"],
                  ["<code>web.xml</code>", "tệp khai báo: Servlet nào, ứng với đường dẫn nào"],
                  ["<code>&lt;%= … %&gt;</code>", "trong trang JSP: tính biểu thức rồi chèn kết quả vào trang"],
                  ["<code>.war</code>, <code>WEB-INF</code>", "gói triển khai (zip); thư mục WEB-INF là phần không trả cho trình duyệt"],
                  ["<code>javax.servlet</code> / <code>jakarta.servlet</code>", "tên gói thư viện Servlet: cũ / mới (Tomcat 10 trở lên dùng jakarta)"]]),
           """Bảng này giải mã các tên của bài. Đó là chương trình phục vụ web với ba hàm khởi động, xử lý yêu cầu và thu hồi, tệp khai báo, và dấu biểu thức trong trang động. Gói triển khai là tệp nén, và Tomcat bản mười trở lên dùng kiểu tên gói thư viện mới.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ], checks=["alg.bnx_l33_waves(4, 4) == 1"])

    intu = sc("intuition", "intuition", "Hình dung: vòng đời chương trình web và trang động", [
        st(svg(1500, 500,
               txt(750, 40, "Bộ chứa tạo Servlet MỘT lần, phục vụ nhiều yêu cầu bằng các luồng của bể, thu hồi MỘT lần", 26, "middle", "#1f2937", True),
               box(40, 130, 260, 100, ["nạp lớp", "tạo một thể hiện"], C_BLUE, 22, True),
               box(360, 130, 260, 100, ["init()", "đúng 1 lần"], C_GREEN, 24, True),
               box(680, 130, 380, 100, ["service() → doGet()", "mỗi yêu cầu một luồng của bể"], C_AMBER, 22, True),
               box(1120, 130, 340, 100, ["destroy()", "đúng 1 lần khi tắt"], C_RED, 24, True),
               arrow(305, 180, 355, 180), arrow(625, 180, 675, 180), arrow(1065, 180, 1115, 180),
               box(40, 290, 1420, 80, ["MỘT thể hiện dùng chung cho mọi yêu cầu: trường của lớp (như soYeuCau) là dữ liệu CHUNG của mọi khách"], C_PURPLE, 22),
               box(40, 400, 1420, 70, "Chạy thật trong bài: Tomcat nhúng 10.1.61 (đo: init 1 lần, ba yêu cầu thấy bộ đếm 1, 2, 3)", C_GRAY, 22)),
           """Đây là vòng đời của chương trình web. Bộ chứa tạo đúng một thể hiện và gọi khởi tạo một lần, rồi mỗi yêu cầu được một luồng của bể gọi vào hàm phục vụ. Vì chỉ có một thể hiện, trường của lớp là dữ liệu chung của mọi khách."""),
        st(svg(1500, 520,
               txt(750, 40, "Trang động .jsp: ở yêu cầu đầu được dịch thành mã Java, biên dịch, rồi chạy như Servlet", 26, "middle", "#1f2937", True),
               box(40, 110, 260, 90, ["chao.jsp", "chữ cố định + <%= %>"], C_BLUE, 22, True),
               box(370, 110, 260, 90, ["dịch", "(Jasper)"], C_AMBER, 24, True),
               box(700, 110, 300, 90, ["chao_jsp.java", "lớp kế thừa HttpJspBase"], C_GREEN, 22, True),
               box(1070, 110, 260, 90, ["biên dịch", "→ chao_jsp.class"], C_GREEN, 22, True),
               arrow(305, 155, 365, 155), arrow(635, 155, 695, 155), arrow(1005, 155, 1065, 155),
               box(40, 250, 680, 150, ["Tomcat = bộ chứa Servlet và JSP", "chỉ lo phần web; chạy thật trong bài"], C_BLUE, 22),
               box(780, 250, 680, 150, ["JBoss / WildFly = máy chủ ứng dụng đầy đủ", "thêm EJB (thành phần doanh nghiệp), JTA (giao dịch phân tán)"], C_PURPLE, 22),
               txt(750, 450, "Bài này chạy thật Tomcat; JBoss/WildFly chỉ giảng khái niệm, không chạy trên máy", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là trang động. Ở yêu cầu đầu, bộ biên dịch trang dịch tệp trang thành mã Java rồi biên dịch thành lớp chạy như một chương trình phục vụ. Tomcat là bộ chứa nhẹ chỉ lo phần web. Máy chủ ứng dụng đầy đủ có thêm thành phần doanh nghiệp, tức các lớp Java do máy chủ quản lý sẵn. Bài này chỉ chạy thật Tomcat.""", introduces=["bnx_ejb"]),
    ], checks=["alg.bnx_l33_waves(200, 4) == 50"])

    form = sc("formula", "formula", "Suy ra từng bước: từ một lớp Java tới một gói triển khai", [
        jstep([(("<code>int soYeuCau = 0;</code>", "<b>trường</b>: biến khai trong lớp, ngoài mọi hàm; mọi lần gọi hàm của thể hiện đó dùng chung một bản", "Trường là biến khai trong lớp, mọi lần gọi hàm dùng chung một bản."), "", ""),
               (("<code>@Override protected void doGet(HttpServletRequest q, HttpServletResponse r)</code>", "<code>@Override</code>: hàm này thay hàm cùng tên của lớp cha; <code>protected</code>: lớp con và cùng gói gọi được; <code>q</code> là yêu cầu đến, <code>r</code> là phản hồi sẽ trả", "Chú thích báo hàm thay hàm của lớp cha; tham số là yêu cầu và phản hồi."), "", ""),
               (("<code>… throws IOException {</code>", "lời báo: hàm có thể ném lỗi loại đó; ai gọi phải bắt lỗi hoặc khai báo tiếp", "Lời báo hàm có thể ném lỗi, và ai gọi phải bắt lỗi."), "", ""),
               (("<code>r.setContentType(\"text/plain\");</code>, <code>r.getWriter().print(…)</code>", "dòng đầu báo kiểu nội dung trả về là chữ thuần; <code>getWriter()</code> lấy đầu ghi vào phản hồi, <code>print</code> ghi một chuỗi", "Báo kiểu nội dung là chữ thuần, rồi ghi một chuỗi vào phản hồi."), "", "")],
              intro="Chương trình phục vụ này có bốn chỗ cần đọc."),
        st("""<p><b>Bước 1. Servlet là một lớp Java.</b> Kế thừa <code>HttpServlet</code> và viết <code>doGet</code> cho yêu cầu GET. Nên đọc dự án cũ là đọc các lớp như thế này.</p>"""
           + J_CHAO.show(lines=(4, 14), title="Chao.java: Servlet tối thiểu (jakarta.servlet)"),
           """Bước một là chương trình phục vụ web chỉ là một lớp Java kế thừa lớp cha có sẵn, nên đọc dự án cũ là đọc các lớp như thế này.""", clear=True),
        st("""<p><b>Bước 2. Vòng đời do bộ chứa điều khiển.</b> Hướng dẫn của Tomcat/Jakarta: bộ chứa gọi <code>init</code> <b>đúng một lần</b> sau khi tạo thể hiện; mỗi yêu cầu vào <code>service</code>; <code>destroy</code> khi gỡ khỏi dịch vụ. Nên <b>một thể hiện</b> phục vụ mọi yêu cầu.</p>"""
           + """$$3 \\text{ yêu cầu} \\Rightarrow init \\times 1, \\; service \\times 3, \\; destroy \\times 1$$""",
           """Bước hai là vòng đời. Theo hướng dẫn chính thức, bộ chứa gọi khởi tạo đúng một lần, mỗi yêu cầu vào hàm phục vụ, và thu hồi khi gỡ chương trình. Vì vậy ba yêu cầu thì khởi tạo một lần, phục vụ ba lần, thu hồi một lần.""", clear=True),
        jstep([(("<code>cat &gt; war/WEB-INF/web.xml &lt;&lt;'EOF' … EOF</code>", "<code>cat &gt; tệp</code> ghi vào tệp; <code>&lt;&lt;'EOF'</code> mở khối chữ nhiều dòng: mọi dòng tới dòng chỉ có chữ <code>EOF</code> được ghi nguyên văn", "Lệnh ghi nhiều dòng vào tệp, nguyên văn tới dòng kết khối."), "", ""),
               (("<code>&lt;servlet&gt;</code>, <code>&lt;servlet-name&gt;</code>, <code>&lt;servlet-class&gt;</code>", "khai một Servlet: tên tự đặt, và tên lớp Java thật của nó", "Thẻ khai một chương trình phục vụ có tên tự đặt và tên lớp thật."), "", ""),
               (("<code>&lt;servlet-mapping&gt;</code>, <code>&lt;url-pattern&gt;</code>", "nối tên với đường dẫn: yêu cầu tới <code>/chao</code> thì giao cho Servlet tên <code>chao</code>; thẻ ngoài cùng <code>&lt;web-app&gt;</code> bọc tất cả", "Thẻ nối tên với đường dẫn, nên yêu cầu tới đường dẫn đó được giao đúng chỗ."), "", "")],
              intro="Tệp khai báo viết bằng thẻ, ghi bằng khối chữ nhiều dòng."),
        st("""<p><b>Bước 3. Khai báo và đóng gói.</b> <code>web.xml</code> nói Servlet nào ứng với đường dẫn nào; thư mục <code>WEB-INF</code> chứa khai báo và lớp; cả thư mục nén thành <code>.war</code>.</p>"""
           + SH_WAR.show_from("cat > war/WEB-INF/web.xml", 12, title="web.xml trong WEB-INF"),
           """Bước ba là khai báo và đóng gói. Tệp khai báo nói chương trình nào ứng với đường dẫn nào, và cả thư mục nén lại thành một gói, nên ứng dụng chỉ là một tệp để chép lên máy chủ.""", clear=True),
        st(table(["viết trong trang", "nghĩa", "ví dụ nhỏ"],
                 [["<code>&lt;%@ page contentType=\"text/plain\" %&gt;</code>", "chỉ thị đầu trang: trả về văn bản thuần, không phải trang HTML", "trình duyệt hiện chữ nguyên văn"],
                  ["<code>request.getParameter(\"ten\")</code>", "lấy giá trị của tham số <code>ten</code> trong địa chỉ sau dấu <code>?</code>", "<code>chao.jsp?ten=An</code> cho <code>An</code>"],
                  ["<code>&lt;%= 2 + 3 %&gt;</code>", "tính biểu thức rồi chèn kết quả vào trang", "chèn <code>5</code>"],
                  ["<code>cat &gt; site/chao.jsp &lt;&lt;'EOF' … EOF</code>", "như với <code>web.xml</code>: ghi mọi dòng tới dòng <code>EOF</code> vào tệp <code>chao.jsp</code>", "tệp có 2 dòng"]]),
           """Dòng chỉ thị đầu trang cho trả về văn bản thuần. Hàm lấy tham số đọc giá trị sau dấu hỏi trong địa chỉ, nên dấu biểu thức mới chèn được tên vào trang. Khối chữ nhiều dòng ghi trang vào tệp.""", clear=True),
        st("""<p><b>Bước 4. Trang động.</b> Trang JSP là chữ cố định trộn với <code>&lt;%= … %&gt;</code>. Ở yêu cầu đầu, Tomcat <b>dịch</b> nó thành lớp Java, biên dịch rồi chạy như Servlet; các yêu cầu sau dùng lại lớp đã biên dịch (mặc định; trang bị sửa thì dịch lại).</p>"""
           + SH_JSP.show_from("cat > site/chao.jsp", 4, title="site/chao.jsp"),
           """Bước bốn là trang động. Trang chỉ là chữ cố định trộn với biểu thức. Ở yêu cầu đầu, Tomcat dịch trang thành lớp Java rồi biên dịch, nên các yêu cầu sau dùng lại lớp đã biên dịch.""", clear=True),
        st("""<p><b>Bước 5. Bể luồng quyết định sức chứa.</b> Tomcat cho mỗi yêu cầu một luồng của bể; hướng dẫn của Tomcat: <code>maxThreads</code> mặc định <b>200</b>. Mỗi yêu cầu mất <i>t</i> giây thì bể <i>L</i> luồng xử lý tối đa <i>L / t</i> yêu cầu mỗi giây.</p>"""
           + """$$\\frac{200}{0{,}5 \\text{ giây}} = \\hl{400} \\text{ yêu cầu mỗi giây}$$""",
           """Bước năm là bể luồng quyết định sức chứa. Tomcat cho mỗi yêu cầu một luồng của bể, và theo hướng dẫn chính thức mặc định là hai trăm luồng. Mỗi yêu cầu mất nửa giây thì hai trăm luồng xử lý tối đa bốn trăm yêu cầu mỗi giây.""", clear=True),
        jstep([(("<code>sed -i 's/javax\\.servlet/jakarta.servlet/' Cu.java</code>", "thay chữ <code>javax.servlet</code> bằng <code>jakarta.servlet</code> ngay trong tệp; dòng <code>import</code> thành <code>import jakarta.servlet.http.HttpServlet;</code>", "Lệnh thay chữ sửa ngay trong tệp."), "", ""),
               (("<code>javac -cp \"lib/*\" Cu.java 2&gt;&amp;1 | head -1</code>", "biên dịch với mọi jar trong <code>lib</code>; <code>2&gt;&amp;1</code> gộp chữ lỗi vào đầu ra; <code>head -1</code> chỉ giữ dòng đầu", "Biên dịch với mọi thư viện, gộp chữ lỗi vào đầu ra và giữ dòng đầu."), "", "")],
              intro="Hai lệnh sửa và biên dịch cần đọc trước."),
        st("""<p><b>Bước 6. Hai tên gói thư viện.</b> Tomcat 9 dùng <code>javax.servlet</code>; từ Tomcat 10 là <code>jakarta.servlet</code>. Hướng dẫn nâng cấp của Tomcat: phải <b>biên dịch lại</b> ứng dụng với API mới. Nên dự án cũ thường kẹt ở tên gói cũ.</p>"""
           + SH_CU.show_from("cat > Cu.java", 7, title="Cu.java: Servlet theo tên gói cũ, biên dịch lỗi, sửa tên gói rồi biên dịch lại"),
           """Bước sáu là hai tên gói thư viện. Tomcat chín dùng tên cũ, từ bản mười là tên mới, nên phải biên dịch lại ứng dụng. Biên dịch đầu báo lỗi, đổi tên gói thì được.""", clear=True),
    ], checks=["alg.bnx_l33_throughput(200, 0.5) == 400", "alg.bnx_l33_waves(200, 4) == 50"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        jstep([(("<code>public static void main(String[] a) throws Exception</code>", "hàm máy chạy đầu tiên; <code>String[] a</code>: mảng các chuỗi gõ kèm lúc chạy (<code>a[0]</code> là chuỗi đầu); <code>throws Exception</code>: hàm có thể ném lỗi mà không bắt", "Hàm chính chạy đầu tiên, nhận mảng chuỗi gõ kèm."), "", ""),
               (("<code>Path goc = Files.createTempDirectory(\"tc\");</code>", "tạo một thư mục tạm mới tên bắt đầu bằng <code>tc</code>, trả về đường dẫn của nó; Tomcat dùng làm chỗ làm việc", "Tạo một thư mục tạm mới để Tomcat làm việc."), "", ""),
               (("<code>Path.of(a[0]).toAbsolutePath().toString()</code>", "<code>a[0]</code>: đối số đầu gõ kèm lúc chạy; đổi thành đường dẫn tuyệt đối (đầy đủ từ gốc ổ đĩa) rồi thành chuỗi", "Đối số đầu đổi thành đường dẫn tuyệt đối rồi thành chuỗi."), "", ""),
               (("<code>a[1].isEmpty() ? \"\" : \"/\" + a[1]</code>", "<code>điều_kiện ? x : y</code>: bằng <code>x</code> nếu đúng, bằng <code>y</code> nếu sai; ở đây đối số thứ hai rỗng thì địa chỉ gốc, không thì thêm <code>/</code> trước tên", "Dấu hỏi chấm chọn giá trị đầu nếu đúng, ngược lại giá trị sau."), "", "")],
              intro="Chương trình khởi động có bốn chỗ cần đọc."),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>Tomcat t = new Tomcat();</code>", "tạo một máy chủ Tomcat ngay trong chương trình Java (đó là Tomcat nhúng)"],
                  ["<code>t.setPort(0);</code>", "cổng 0 nghĩa là để hệ điều hành tự chọn một cổng đang trống"],
                  ["<code>t.addWebapp(\"/app\", thư_mục)</code>", "nạp ứng dụng ở thư mục (hoặc gói <code>.war</code>) vào địa chỉ bắt đầu bằng <code>/app</code>"],
                  ["<code>t.start();</code> rồi <code>getLocalPort()</code>", "bật máy chủ, rồi hỏi cổng thật nó đang nghe"]]),
           """Tạo Tomcat nhúng là tạo một máy chủ ngay trong chương trình Java. Cổng không để hệ điều hành tự chọn cổng trống. Rồi ta nạp ứng dụng, bật máy chủ và hỏi cổng thật.""", clear=True),
        st("""<p><code>May.java</code> khởi động Tomcat nhúng trên cổng ngẫu nhiên và nạp ứng dụng (thư mục hoặc gói <code>.war</code>). Phần <code>import</code> và các hàm phụ <code>lay</code>, <code>dem</code>, <code>chep</code> nằm ở nguồn bài.</p>"""
           + J_MAY.show(lines=(28, 37), title="May.java (1/2): khởi động Tomcat nhúng rồi nạp ứng dụng"),
           """Ta chạy thật bằng JDK hai mươi mốt và Tomcat nhúng: khởi động trên cổng ngẫu nhiên, nạp ứng dụng, rồi lấy số cổng.""", clear=True),
        jstep([(("<code>for (int i = 2; i &lt; a.length; i++)</code>", "vòng đếm bắt đầu từ <code>i = 2</code> vì hai đối số đầu đã dùng; <code>a.length</code>: số chuỗi gõ kèm; mỗi vòng gọi địa chỉ <code>a[i]</code>", "Vòng đếm bắt đầu từ hai vì hai đối số đầu đã dùng."), "", "")],
              intro="Vòng gọi địa chỉ có một chỗ mới."),
        st(J_MAY.show(lines=(38, 47), title="May.java (2/2): gửi yêu cầu, đếm tệp Jasper sinh ra, rồi tắt"),
           """Sau đó nó gửi từng yêu cầu và in kết quả, đếm tệp mà bộ biên dịch trang sinh ra, rồi tắt Tomcat.""", clear=True),
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>javac -cp \"lib/*\" -d war/WEB-INF/classes Chao.java</code>", "biên dịch <code>Chao.java</code> với mọi jar trong <code>lib</code>; <code>-d</code>: đặt tệp lớp đã biên dịch vào thư mục sau nó"],
                  ["<code>jar --create --file app.war -C war .</code>, <code>jar tf app.war | sort</code>", "nén thư mục <code>war</code> thành <code>app.war</code> (<code>-C war .</code>: vào thư mục <code>war</code> rồi lấy mọi thứ); <code>tf</code> liệt kê tên tệp trong gói; <code>sort</code> xếp theo chữ cái"],
                  ["<code>java -cp \"lib/*\" May app.war app app/chao … 2&gt;/dev/null</code>", "chạy lớp <code>May</code>; đối số theo thứ tự: gói, tên ứng dụng <code>app</code>, rồi từng địa chỉ cần gọi; <code>2&gt;/dev/null</code> vứt chữ báo lỗi và nhật ký"]]),
           """Ba lệnh mới cần đọc. Lệnh biên dịch đặt lớp vào thư mục khai báo. Lệnh nén tạo và liệt kê gói. Lệnh chạy nhận gói, tên ứng dụng, rồi các địa chỉ cần gọi, và vứt chữ nhật ký.""", clear=True),
        st(SH_WAR.show_from('javac -cp "lib/*" -d war', 4, title="Chạy thật: biên dịch, nén .war, nạp vào Tomcat nhúng (JDK 21, Tomcat 10.1.61)"),
           """Ta biên dịch chương trình phục vụ vào thư mục khai báo, nén thành gói, liệt kê nội dung gói, rồi cho Tomcat nạp gói và gửi ba yêu cầu.""", clear=True),
        st(SH_WAR.out_html("""META-INF/
META-INF/MANIFEST.MF
WEB-INF/
WEB-INF/classes/
WEB-INF/classes/Chao.class
WEB-INF/web.xml""", "Kết quả chạy thật: nội dung gói app.war")
           + """$$① \\; \\text{.war là zip: } \\text{WEB-INF/web.xml} + \\text{WEB-INF/classes/Chao.class}$$""",
           """Phép tính thứ nhất là nội dung gói. Đúng là tệp nén, trong đó có tệp khai báo và lớp đã biên dịch của chương trình.""", clear=True),
        st(SH_WAR.out_html("""init: tao 1 lan
app/chao -> yeu cau so 1
app/chao -> yeu cau so 2
app/chao -> yeu cau so 3
destroy: thu hoi 1 lan""", "Kết quả chạy thật: ba yêu cầu, một thể hiện")
           + """$$② \\; init \\times 1, \\; \\text{bộ đếm } 1, 2, 3, \\; destroy \\times 1$$""",
           """Phép tính thứ hai là vòng đời. Khởi tạo chỉ chạy một lần, và bộ đếm trong trường tăng một, hai, ba, nghĩa là cả ba yêu cầu dùng chung một thể hiện. Thu hồi chạy một lần khi tắt.""", clear=True),
        st(SH_JSP.out_html("""chao.jsp?ten=An -> Xin chao An, 2 + 3 = 5
chao.jsp?ten=Binh -> Xin chao Binh, 2 + 3 = 5
tep Jasper sinh ra: truoc 0, sau 2
chao_jsp.class
chao_jsp.java""", "Kết quả chạy thật: một trang JSP, hai yêu cầu")
           + """$$③ \\; 0 \\to 2 \\text{ tệp ở yêu cầu đầu; yêu cầu thứ hai không thêm tệp}$$""",
           """Phép tính thứ ba là trang động. Trước yêu cầu đầu chưa có tệp nào, sau hai yêu cầu có hai tệp, mã Java và lớp đã biên dịch, nên yêu cầu thứ hai không biên dịch lại.""", clear=True),
        st(SH_JSP.out_html("""122:      out.write("Xin chao ");
123:      out.print( request.getParameter("ten") );
124:      out.write(", 2 + 3 = ");
125:      out.print( 2 + 3 );""", "Trích mã Java do Tomcat sinh ra từ trang (lọc dòng out.write, out.print)")
           + """$$④ \\; \\text{chữ cố định} \\to out.write; \\quad \\text{biểu thức} \\to out.print$$""",
           """Phép tính thứ tư là mã sinh ra. Chữ cố định của trang thành lệnh ghi chữ, và mỗi biểu thức thành một lệnh in kết quả. Trang động chỉ là một chương trình Java được viết hộ.""", clear=True),
        st(SH_CU.out_html("""Cu.java:1: error: package javax.servlet.http does not exist
bien dich duoc""", "Kết quả chạy thật: tên gói cũ và sau khi đổi")
           + """$$⑤ \\; javax.servlet \\to jakarta.servlet \\Rightarrow \\text{biên dịch được với Tomcat 10.1}$$""",
           """Phép tính thứ năm là tên gói. Với Tomcat mười, chương trình viết theo tên gói cũ không biên dịch được vì gói không tồn tại. Đổi sang tên gói mới thì biên dịch được.""", clear=True),
    ], checks=["alg.bnx_l33_throughput(200, 0.5) == 400", "alg.bnx_l33_waves(200, 4) == 50"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: đọc mã đã biên dịch", [
        st(SH_JSP.out_html("public final class org.apache.jsp.chao_jsp extends HttpJspBase", "Chạy thật: công cụ javap đọc lớp đã biên dịch (không đọc mã nguồn sinh ra)")
           + table(["con số", "đường thứ nhất", "đường khác"],
                   [["trang JSP là một Servlet", "mã Java sinh ra: chao_jsp extends HttpJspBase", "javap đọc lớp đã biên dịch: cùng lớp cha"],
                    ["init chỉ chạy một lần", "đầu ra thật: 1 dòng init, 3 yêu cầu", "hướng dẫn chính thức: gọi init đúng một lần"]]),
           """Ta kiểm bằng đường khác. Công cụ đọc lớp đã biên dịch cho thấy lớp sinh ra từ trang kế thừa lớp cha của bộ biên dịch trang, nên trang động thật sự là một chương trình phục vụ. Hướng dẫn chính thức cũng nói khởi tạo chạy đúng một lần.""", clear=True),
    ], checks=["alg.bnx_l33_waves(4, 4) == 1"])

    quymo = sc("quymo", "example", "Khi tải tăng: bể 4 luồng và 4, 40, 200 yêu cầu", [
        jstep([(("<code>static AtomicInteger dang = new AtomicInteger(), toiDa = new AtomicInteger();</code>", "hai biến số nguyên mà nhiều luồng cùng cập nhật không bị lẫn; <code>static</code>: một bản chung của lớp; khai hai biến một dòng, cách nhau dấu phẩy", "Hai biến số nguyên mà nhiều luồng cùng cập nhật không bị lẫn."), "<code>dang</code>: số cuộc đang chạy; <code>toiDa</code>: mức cao nhất đã thấy", ""),
               (("<code>((AbstractProtocol&lt;?&gt;) t.getConnector().getProtocolHandler()).setMaxThreads(4)</code>", "lấy bộ xử lý giao thức của Tomcat; <code>(AbstractProtocol&lt;?&gt;)</code> là <b>ép kiểu</b> sang kiểu có hàm <code>setMaxThreads</code>; hàm đặt bể còn 4 luồng", "Ép sang kiểu có hàm đặt cỡ bể, rồi đặt bốn luồng."), "", "")],
              intro="Phần đầu chương trình đo tải có hai chỗ mới.", introduces=["bnx_atomic_coll"]),
        st("""<p><code>Tai.java</code>: Tomcat nhúng có bể chỉ <b>4</b> luồng (<code>setMaxThreads(4)</code>) và một Servlet chậm cố ý (ngủ 100 ms). Phần <code>import</code> nằm ở nguồn bài.</p>"""
           + J_TAI.show(lines=(13, 21), title="Tai.java (1/4): hai bộ đếm và bể 4 luồng"),
           """Ta đo thật bằng một Tomcat nhúng mà bể chỉ có bốn luồng. Chương trình có hai bộ đếm, số cuộc đang chạy và mức cao nhất.""", clear=True),
        jstep([(("<code>new HttpServlet() { … }</code>", "<b>lớp ẩn danh</b>: viết luôn thân một lớp con của <code>HttpServlet</code> ngay tại chỗ tạo đối tượng, khỏi đặt tên", "Lớp ẩn danh viết luôn thân lớp con ngay tại chỗ tạo."), "", ""),
               (("<code>toiDa.accumulateAndGet(dang.incrementAndGet(), Math::max)</code>", "<code>dang.incrementAndGet()</code>: tăng <code>dang</code> thêm 1 và trả giá trị mới; <code>accumulateAndGet(x, Math::max)</code>: đặt <code>toiDa</code> bằng số lớn hơn giữa nó và <code>x</code>", "Tăng số cuộc đang chạy, rồi cập nhật mức cao nhất."), "", ""),
               (("<code>try { Thread.sleep(100); } catch (InterruptedException e) { }</code>", "ngủ 100 mili giây để giả việc chậm; <code>catch</code> bắt lỗi bị đánh thức giữa chừng và bỏ qua vì khối trống", "Ngủ một trăm mili giây để giả việc chậm; khối bắt lỗi trống bỏ qua lỗi."), "", ""),
               (("<code>Tomcat.addServlet(ctx, \"cham\", …)</code>, <code>ctx.addServletMappingDecoded(\"/cham\", \"cham\")</code>", "đăng ký Servlet với tên <code>cham</code> vào ngữ cảnh <code>ctx</code>, rồi nối đường dẫn <code>/cham</code> với tên đó", "Đăng ký theo tên rồi nối đường dẫn."), "", "")],
              intro="Phần phục vụ chậm có bốn chỗ cần đọc."),
        st(J_TAI.show(lines=(22, 32), title="Tai.java (2/4): Servlet chậm 100 ms, đếm số cuộc chạy đồng thời"),
           """Chương trình phục vụ chậm cố ý ngủ một trăm mili giây, và ghi lại số cuộc chạy đồng thời cùng mức cao nhất.""", clear=True),
        jstep([(("<code>for (int n : new int[] {4, 40, 200}) { … }</code>", "duyệt từng cỡ tải trong mảng vừa tạo: <code>n</code> lần lượt là 4, 40, 200", "Duyệt từng cỡ tải trong mảng vừa tạo."), "", ""),
               (("<code>List&lt;CompletableFuture&lt;?&gt;&gt; ds = new ArrayList&lt;&gt;();</code>", "danh sách các <b>hẹn kết quả</b> (việc đang chạy nền, kết quả có sau); <code>&lt;?&gt;</code>: kiểu kết quả nào cũng được", "Danh sách các hẹn kết quả."), "", ""),
               (("<code>c.sendAsync(…)</code>, <code>for (var d : ds) d.join();</code>", "<code>sendAsync</code>: gửi yêu cầu mà không chờ, trả hẹn kết quả; <code>join()</code>: chờ hẹn đó xong; <code>var</code>: để máy tự suy kiểu của <code>d</code>", "Gửi không chờ trả về một hẹn, rồi chờ từng hẹn xong."), "", ""),
               (("<code>long bd = System.nanoTime();</code>", "mốc giờ của đồng hồ máy theo nano giây, để trừ ra thời gian đã trôi", "Mốc giờ của đồng hồ máy để tính thời gian đã trôi."), "", "")],
              intro="Phần gửi yêu cầu có bốn chỗ mới."),
        st(J_TAI.show(lines=(33, 43), title="Tai.java (3/4): khởi động Tomcat, gửi n yêu cầu cùng lúc, chờ xong"),
           """Rồi ta khởi động Tomcat, và với mỗi cỡ tải n thì gửi n yêu cầu cùng lúc mà không chờ nhau, rồi chờ mọi hẹn xong.""", clear=True),
        jstep([(("<code>long ms = (System.nanoTime() - bd) / 1_000_000, can = (n + 3) / 4 * 100L;</code>", "khai hai biến <code>long</code> một dòng; <code>1_000_000</code>: gạch dưới chỉ để dễ đọc số; <code>(n + 3) / 4</code>: chia 4 <b>làm tròn lên</b> (số lượt); <code>100L</code>: số 100 kiểu <code>long</code>", "Chia bốn làm tròn lên cho số lượt, nhân một trăm mili giây."), "ví dụ <code>n = 40</code>: tổng <code>43</code> chia 4 bỏ phần lẻ ra <code>10</code> lượt, <code>10 × 100 = 1000</code> ms", "")],
              intro="Dòng so sánh có một biểu thức cần đọc."),
        st(J_TAI.show(lines=(44, 51), title="Tai.java (4/4): so với mức tối thiểu rồi tắt"),
           """Cuối cùng ta so thời gian thật với mức tối thiểu. Màn hình chỉ in đúng hay sai, vì số mili giây thật đổi theo từng máy.""", clear=True),
        st(SH_TAI.out_html("""4 yeu cau, 4 luong: dong thoi toi da 4, thoi gian >= 100 ms: true
40 yeu cau, 4 luong: dong thoi toi da 4, thoi gian >= 1000 ms: true
200 yeu cau, 4 luong: dong thoi toi da 4, thoi gian >= 5000 ms: true""", "Chạy thật: Servlet chậm 100 ms, bể 4 luồng")
           + """$$4 \\to 40 \\to 200 \\;(\\times 50): \\; \\text{đồng thời tối đa } 4; \\quad \\text{thời gian} \\ge \\frac{n}{4} \\times 100 \\text{ ms (làm tròn lên)}$$""",
           """Đây là số đo thật khi tải tăng năm mươi lần. Bể bốn luồng thì dù bốn, bốn mươi hay hai trăm yêu cầu đến cùng lúc, số cuộc chạy đồng thời vẫn tối đa bốn. Vì vậy hai trăm chia bốn lượt, mỗi lượt một trăm mili giây, là ít nhất năm nghìn.""", clear=True),
        st(table(["cách", "được", "mất", "chọn khi"],
                 [["giữ bể mặc định (200), xử lý nhanh", "đơn giản; đủ cho phần lớn dịch vụ nhẹ", "một việc chậm (gọi dịch vụ ngoài không hết giờ) chiếm dần cả 200 luồng", "việc ngắn, có hạn chót cho mọi cuộc gọi ngoài"],
                  ["tăng bể (ví dụ 1 000)", "chịu được nhiều yêu cầu chậm hơn", "mỗi luồng tốn bộ nhớ; chuyển ngữ cảnh nhiều; dồn tải sang cơ sở dữ liệu", "đã đo: luồng rảnh nhưng yêu cầu vẫn chờ"],
                  ["thu nhỏ việc chậm (hết giờ, bất đồng bộ)", "bể không cạn", "phải sửa mã, kiểm thử lại", "dịch vụ lõi, tải tăng đều"]]),
           """Bảng này là các lựa chọn của người làm nghề. Giữ bể mặc định thì đơn giản, nhưng một việc chậm sẽ chiếm dần cả hai trăm luồng. Tăng bể chịu được nhiều việc chậm hơn, đổi lại tốn bộ nhớ. Thu nhỏ việc chậm thì bể không cạn, đổi lại phải sửa mã.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l33_waves(4, 4) == 1 and alg.bnx_l33_waves(40, 4) == 10 and alg.bnx_l33_waves(200, 4) == 50",
               "alg.bnx_l33_waves(4, 4) * 100 == 100 and alg.bnx_l33_waves(40, 4) * 100 == 1000 and alg.bnx_l33_waves(200, 4) * 100 == 5000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Chép mẫu cũ trên mạng viết theo <code>javax.servlet</code> vào Tomcat 10 trở lên: <b class="red">package javax.servlet.http does not exist</b> (đã đo). Xem Tomcat bản nào và dùng đúng tên gói.</div>
$$\\text{Tomcat } 9 \\to javax; \\quad \\text{Tomcat } 10{+} \\to jakarta$$""",
           """Lỗi thứ nhất là chép mẫu cũ viết theo tên gói cũ vào Tomcat mười trở lên, và bị báo gói không tồn tại như đã đo. Hãy xem Tomcat bản nào và dùng đúng tên gói.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Lưu <b class="red">dữ liệu của từng khách vào trường của Servlet</b>. Chỉ có <b>một</b> thể hiện cho mọi yêu cầu (đã đo: bộ đếm 1, 2, 3): khách này thấy dữ liệu khách kia, và nhiều luồng ghi đồng thời gây lỗi khó tìm. Dữ liệu từng khách để trong biến cục bộ hoặc <b>phiên</b> (bộ nhớ riêng của từng khách trên máy chủ, nhận ra qua một mã gửi kèm mỗi yêu cầu).</div>
$$\\text{1 thể hiện} \\times n \\text{ khách} \\Rightarrow \\text{trường là dữ liệu chung}$$""",
           """Lỗi thứ hai, lộ ra lúc mới dựng: lưu dữ liệu từng khách vào trường của chương trình phục vụ. Chỉ có một thể hiện cho mọi yêu cầu, nên khách này thấy dữ liệu khách kia. Hãy để dữ liệu từng khách trong biến cục bộ hoặc phiên.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Việc chậm không có hạn chót chiếm dần bể luồng. Đo thật: bể 4 luồng, 200 yêu cầu cùng lúc: tối đa 4 chạy, tổng thời gian ≥ 5 000 ms. Bể mặc định 200 cũng cạn y vậy, chỉ muộn hơn.</div>
$$\\frac{200}{4} \\times 100 = \\hl{5\\,000} \\text{ ms}$$""",
           """Lỗi thứ ba, lộ ra khi tải tăng: việc chậm không có hạn chót chiếm dần bể luồng. Đo thật, bể bốn luồng với hai trăm yêu cầu chỉ chạy bốn cái, tổng thời gian ít nhất năm nghìn mili giây.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> <b class="red">Không ai dám nâng cấp máy chủ</b> vì đổi javax → jakarta phải biên dịch lại mọi thứ; càng để lâu càng khó nâng cấp, nên hãy kiểm trang phiên bản được hỗ trợ của Tomcat xem bản mình dùng còn được vá lỗi không. Hướng dẫn của Tomcat có công cụ chuyển đổi ứng dụng khi triển khai; cần kế hoạch, kiểm thử, và đo trước-sau.</div>
<table class='t'><tr><th>trì hoãn mãi</th><th>chuyển có kế hoạch</th></tr><tr><td>nợ nâng cấp tích tụ</td><td>công cụ chuyển đổi hoặc sửa import + kiểm thử</td></tr></table>""",
           """Lỗi thứ tư, lộ ra khi vận hành lâu dài: không ai dám nâng cấp máy chủ vì đổi tên gói phải biên dịch lại, nên nợ nâng cấp tích tụ. Hãy có kế hoạch và kiểm thử.""", clear=True),
    ], checks=["alg.bnx_l33_waves(200, 4) * 100 == 5000"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Bể 8 luồng, mỗi yêu cầu mất 0,25 giây. Thông lượng tối đa mỗi giây là bao nhiêu? 40 yêu cầu đến cùng lúc thì xử lý xong sau ít nhất bao lâu?"],
                  ["2", "Một ứng dụng có 120 trang JSP, mỗi trang được gọi lần đầu lúc nào? Có bao nhiêu lần dịch và biên dịch ở lần chạy đầu của cả hệ thống nếu mỗi trang được gọi một lần?"],
                  ["3", "Quyết định (số minh hoạ): ứng dụng cũ dùng Tomcat 9 (<code>javax</code>), còn 30 Servlet, đội 3 người. Nâng lên Tomcat 10 bằng sửa import, hay dùng công cụ chuyển đổi khi triển khai, hay viết lại bằng Spring Boot? Vì sao?"]]),
           """Đến lượt bạn. Câu một: bể tám luồng, mỗi yêu cầu mất một phần tư giây, thông lượng tối đa mỗi giây là bao nhiêu, và bốn mươi yêu cầu cùng lúc xong sau ít nhất bao lâu? Câu hai: một trăm hai mươi trang động, mỗi trang gọi một lần, có bao nhiêu lần dịch ở lần chạy đầu? Câu ba: Tomcat chín, ba mươi chương trình phục vụ, đội ba người, nên sửa tên gói, dùng công cụ chuyển đổi, hay viết lại bằng Spring, bộ khung dựng dịch vụ mới? Hãy dừng lại làm ra giấy.""",
           pause=30),
        st("""<p>Câu 1: thông lượng = 8 : 0,25; số lượt = 40 : 8.</p>
$$\\frac{8}{0{,}25} = \\hlg{32} \\text{ yêu cầu/giây}; \\quad \\frac{40}{8} \\times 0{,}25 = 5 \\times 0{,}25 = \\hl{1{,}25} \\text{ giây}$$""",
           """Đáp án câu một. Tám luồng chia một phần tư giây là ba mươi hai yêu cầu mỗi giây. Bốn mươi yêu cầu chia tám luồng là năm lượt, mỗi lượt một phần tư giây, nên ít nhất một phẩy hai mươi lăm giây."""),
        st("""<p>Câu 2: theo mặc định mỗi trang dịch và biên dịch <b>một lần</b>, ở yêu cầu đầu của <b>chính trang đó</b> (trang bị sửa thì dịch lại; biên dịch trước khi triển khai thì 0 lần lúc chạy).</p>
$$120 \\text{ trang} \\Rightarrow \\hlg{120} \\text{ lần dịch và biên dịch}$$""",
           """Đáp án câu hai. Theo mặc định, mỗi trang dịch một lần ở yêu cầu đầu của chính nó, nên một trăm hai mươi trang là một trăm hai mươi lần. Trang bị sửa thì dịch lại, trang biên dịch trước thì không."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["sửa import (30 Servlet)", "mã sạch, nhanh nếu ít dùng thư viện cũ", "mọi thư viện kèm theo cũng phải có bản jakarta; phải kiểm thử toàn bộ"],
                  ["công cụ chuyển đổi khi triển khai", "ít sửa mã, thử nhanh", "thêm một bước triển khai; vẫn nợ kỹ thuật"],
                  ["viết lại bằng Spring Boot", "bỏ nợ cũ", "tốn nhiều tháng; đội 3 người; rủi ro hành vi khác"]]),
           """Đáp án câu ba. Sửa tên gói cho mã sạch, nhưng mọi thư viện kèm theo cũng phải đổi và phải kiểm thử toàn bộ. Công cụ chuyển đổi ít sửa mã, đổi lại vẫn nợ kỹ thuật. Viết lại tốn nhiều tháng. Hợp lý là dùng công cụ chuyển đổi trước, rồi sửa dần.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_l33_throughput(8, 0.25) == 32 and alg.bnx_l33_waves(40, 8) * 0.25 == 1.25", "120 * 1 == 120"])

    lab_pr = practice_scene(sc, "Tự làm: bộ chứa tí hon với vòng đời Servlet", practice_steps2(
        st, "BNX", "L33",
        """<p><b>Đề</b>: viết bộ chứa tí hon <code>MauBoChua</code> (Java thuần): tạo thể hiện ở yêu cầu đầu của mỗi đường dẫn, gọi <code>init</code> đúng một lần, <code>service</code> mỗi yêu cầu, <code>destroy</code> một lần khi dừng.</p>
<p>Ba kiểu cho sẵn và định dạng đầu ra chính xác nằm trong <code>de.md</code>; số liệu <b>khác</b> ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm. Viết một bộ chứa tí hon bằng Java thuần. Ở yêu cầu đầu của mỗi đường dẫn thì tạo và khởi tạo một lần, mỗi yêu cầu gọi hàm phục vụ, khi dừng thì thu hồi. Hãy dừng video và tự viết.""",
        LAB_OUT, "MauBoChua.java",
        """<div class="box key"><b>Nếu kẹt:</b> dùng hai bảng <code>LinkedHashMap</code> (giữ thứ tự thêm vào): <code>khaiBao</code> (cách tạo) và <code>dangChay</code> (thể hiện đã tạo). <code>dangChay.get(duong) == null</code> nghĩa là lần đầu: tạo, <code>init()</code>, cất vào bảng.
Lời giải đầy đủ ở <code>labs/BNX/L33/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, dùng hai bảng giữ thứ tự thêm vào, một cho cách tạo và một cho thể hiện đã tạo. Chưa có thể hiện nghĩa là lần đầu, thì tạo, khởi tạo, rồi cất vào bảng.""", pause=240), "BNX", "L33")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("Servlet = lớp Java, bộ chứa gọi", "vòng đời: init 1, service n, destroy 1", "JSP = Servlet được viết hộ", "bể luồng = sức chứa", "javax → jakarta: biên dịch lại"),
           """Chương trình web là một lớp Java do bộ chứa gọi, với khởi tạo một lần, phục vụ nhiều lần, thu hồi một lần. Bể luồng quyết định sức chứa."""),
        st("""<div class='box key'><b>Tư duy:</b> dự án cũ không bí ẩn: mọi thứ là lớp Java, tệp khai báo và một gói zip. Đọc theo thứ tự <b>khai báo → lớp → vòng đời → bể luồng</b>; thấy gì lạ thì <b>đo</b> (đếm khởi tạo, đếm luồng) thay vì đoán.
Và Tomcat, JBoss chỉ là tên bộ chứa: vòng đời và bể luồng mới là thứ mang theo.</div>""",
           """Dự án cũ không bí ẩn: mọi thứ là lớp Java, tệp khai báo và một gói nén. Thấy gì lạ thì đo thay vì đoán."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Servlet, JSP: vòng đời ra sao?", "một thể hiện, <code>init</code> một lần, <code>service</code> mỗi yêu cầu bằng luồng của bể, <code>destroy</code> một lần (đo: 3 yêu cầu, init 1); trường của lớp là dữ liệu chung"],
                  ["JSP khác Servlet thế nào?", "JSP được dịch thành Servlet ở yêu cầu đầu (đo: 0 → 2 tệp); logic nặng nên đặt ở lớp Java, không ở trang"],
                  ["Tomcat khác JBoss/WildFly?", "Tomcat là bộ chứa Servlet/JSP; JBoss/WildFly là máy chủ ứng dụng đầy đủ (bài chỉ chạy thật Tomcat); nâng cấp: javax → jakarta phải biên dịch lại"]]),
           """Nếu người phỏng vấn hỏi về dòng này, có ba câu hay gặp. Vòng đời: một thể hiện, khởi tạo một lần, phục vụ mỗi yêu cầu bằng luồng của bể. Trang động dịch thành chương trình phục vụ ở yêu cầu đầu. Bộ chứa nhẹ chỉ lo phần web.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Bài sau: <b>hệ thống phê duyệt tín dụng</b>: luồng, máy trạng thái, phân quyền duyệt theo hạn mức, truy vấn lịch sử có đồng ý của khách.</p>""",
           """Ở bài ba mươi tư, ta tìm hiểu hệ thống phê duyệt tín dụng: luồng xử lý, máy trạng thái, phân quyền theo hạn mức, và truy vấn lịch sử có đồng ý của khách.""",
           forward_ref=True),
    ], checks=["alg.bnx_l33_waves(200, 4) == 50"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L33", "he_cu_servlet_jsp_tomcat",
                  "Bài 33 — Hệ cũ: Servlet, JSP, Tomcat, JBoss",
                  "curriculum/bnx.yaml L33; audit/bnx/verify_bnx.py L33; audit/bnx/sources_l33.md: trang chủ và hướng dẫn Tomcat 10.1 (Jasper, cấu hình bộ kết nối, nâng cấp 9 → 10), "
                  "Servlet API của Tomcat, WildFly (về WildFly), đọc 2026-11-14; Tomcat nhúng 10.1.61 chạy thật trên Temurin JDK 21.0.13 (jar ở audit/bnx/deps/l33); JBoss/WildFly không chạy",
                  OBJ33,
                  scenes, assumes=["bnx_sed_i"],
                  covers=COV33)


OBJ33 = ["Đọc một Servlet tối thiểu và vòng đời init một lần, service nhiều lần, destroy một lần trên Tomcat nhúng",
         "Đọc nội dung một gói war và tệp web.xml khai báo Servlet",
         "Mô tả cách trang JSP được dịch thành Servlet ở yêu cầu đầu và đếm tệp sinh ra",
         "Xác định lỗi biên dịch của tên gói javax.servlet với Tomcat 10 và sửa sang jakarta.servlet",
         "Tính thông lượng và số lượt chờ của bể luồng",
         "Đo số cuộc xử lý đồng thời tối đa của bể 4 luồng khi có 4, 40 và 200 yêu cầu cùng lúc",
         "Phân biệt bộ chứa Servlet như Tomcat với máy chủ ứng dụng đầy đủ như JBoss hoặc WildFly",
         "Viết bộ chứa tí hon có vòng đời init, service, destroy bằng Java thuần"]
COV33 = [(1, "example"), (2, "example"), (3, "example"), (4, "example"), (5, "formula"), (6, "quymo"), (7, "intuition"), (8, "practice")]
