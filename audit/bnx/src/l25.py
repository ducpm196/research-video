import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from labkit import write_lab, practice_steps, practice_scene
from libj import jstep, nowrap

lib2.begin("L25")

# ── Mã chạy THẬT: Spring Framework 7.0.10 (context, jdbc, tx, aop) + AspectJ weaver 1.9.24 + H2 2.3.232 (audit/bnx/deps/l25, sha256 ở README.md) ──
# Đầu ra tất định (đệm ở audit/bnx/progcache/L25.json). Nguồn Java cần jar là kind "other": ghi vào thư mục của script, không chạy riêng.
J_CFG = prog("Cfg", r'''
import javax.sql.DataSource;
import org.springframework.context.annotation.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.*;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;
@Configuration
@EnableTransactionManagement
@EnableAspectJAutoProxy
public class Cfg {
  @Bean DataSource ds() {
    return new DriverManagerDataSource(
        "jdbc:h2:mem:l25;DB_CLOSE_DELAY=-1", "sa", "");
  }
  @Bean JdbcTemplate jt(DataSource d) { return new JdbcTemplate(d); }
  @Bean PlatformTransactionManager tm(DataSource d) {
    return new DataSourceTransactionManager(d);
  }
  @Bean NhatKy nk(JdbcTemplate j) { return new NhatKy(j); }
  @Bean ChuyenTien ct(JdbcTemplate j, NhatKy n) {
    return new ChuyenTien(j, n);
  }
  @Bean DoGio dg() { return new DoGio(); }
}
''', lang="java", kind="other")

J_NK = prog("NhatKy", r'''
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.*;
public class NhatKy {
  final JdbcTemplate j;
  NhatKy(JdbcTemplate j) { this.j = j; }
  @Transactional
  public void ghi(String m) {
    j.update("insert into nhat_ky values (?)", m);
  }
  @Transactional(propagation = Propagation.REQUIRES_NEW)
  public void ghiRieng(String m) {
    j.update("insert into nhat_ky values (?)", m);
  }
}
''', lang="java", kind="other")

J_CT = prog("ChuyenTien", r'''
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.*;
import org.springframework.transaction.support.*;
public class ChuyenTien {
  final JdbcTemplate j;
  final NhatKy nk;
  ChuyenTien(JdbcTemplate j, NhatKy nk) { this.j = j; this.nk = nk; }
  static final String TRU =
      "update tk set so_du = so_du - 100 where id = 1";
  @Transactional
  public void chuyenLoi(boolean rieng) {
    j.update(TRU);
    if (rieng) nk.ghiRieng("thu chuyen"); else nk.ghi("thu chuyen");
    throw new IllegalStateException("het han muc");
  }
  @Transactional
  public void chuyenKiem() throws Exception {
    j.update(TRU);
    throw new Exception("loi kiem tra");
  }
  @Transactional(rollbackFor = Exception.class)
  public void chuyenKiemHoanTac() throws Exception {
    j.update(TRU);
    throw new Exception("loi kiem tra");
  }
  @Transactional(propagation = Propagation.REQUIRES_NEW)
  public boolean rieng() {
    return TransactionSynchronizationManager
        .isActualTransactionActive();
  }
  public boolean goiNoiBo() { return this.rieng(); }
}
''', lang="java", kind="other")

J_DG = prog("DoGio", r'''
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
@Aspect
public class DoGio {
  int dem = 0;
  boolean khongAm = true;
  @Around("execution(* ChuyenTien.rieng(..))")
  public Object doThoiGian(ProceedingJoinPoint p)
      throws Throwable {
    long t = System.nanoTime();
    try {
      return p.proceed();
    } finally {
      dem++;
      khongAm &= System.nanoTime() - t >= 0;
    }
  }
}
''', lang="java", kind="other")

J_TX = prog("DemTx", r'''
import org.springframework.aop.support.AopUtils;
import org.springframework.context.annotation.*;
import org.springframework.jdbc.core.JdbcTemplate;
public class DemTx {
  static JdbcTemplate j;
  interface Lenh { void chay() throws Exception; }
  static void mo(String ten, Lenh l) {
    j.update("delete from nhat_ky");
    j.update("update tk set so_du = 1000 where id = 1");
    try { l.chay(); } catch (Exception e) { }
    long sd = j.queryForObject(
        "select so_du from tk where id = 1", Long.class);
    long nk = j.queryForObject(
        "select count(*) from nhat_ky", Long.class);
    System.out.println(ten + ": so du " + sd + ", nhat ky " + nk);
  }
  public static void main(String[] a) {
    var c = new AnnotationConfigApplicationContext(Cfg.class);
    j = c.getBean(JdbcTemplate.class);
    j.execute("create table tk (id int, so_du bigint)");
    j.execute("create table nhat_ky (m varchar(40))");
    j.update("insert into tk values (1, 1000)");
    var ct = c.getBean(ChuyenTien.class);
    System.out.println("ct la proxy: " + AopUtils.isAopProxy(ct));
    mo("1 REQUIRED, loi chay", () -> ct.chuyenLoi(false));
    mo("2 REQUIRES_NEW, loi chay", () -> ct.chuyenLoi(true));
    mo("3 loi kiem tra, mac dinh", ct::chuyenKiem);
    mo("4 loi kiem tra, rollbackFor", ct::chuyenKiemHoanTac);
    System.out.println("goi qua proxy: giao dich " + ct.rieng());
    System.out.println("goi noi bo: giao dich " + ct.goiNoiBo());
    var dg = c.getBean(DoGio.class);
    System.out.println("doan cat chay " + dg.dem + " lan, khong am "
        + dg.khongAm);
  }
}
''', lang="java", kind="other")

J_ISO = prog("DemCoLap", r'''
import java.sql.*;
public class DemCoLap {
  static final String U = "jdbc:h2:mem:iso;DB_CLOSE_DELAY=-1";
  static long so(Connection c) throws Exception {
    try (ResultSet r = c.createStatement().executeQuery(
        "select so_du from tk where id = 1")) {
      r.next();
      return r.getLong(1);
    }
  }
  static String thu(int muc) throws Exception {
    try (Connection a = DriverManager.getConnection(U, "sa", "");
         Connection b = DriverManager.getConnection(U, "sa", "")) {
      b.createStatement().execute("update tk set so_du = 1000");
      a.setAutoCommit(false);
      a.setTransactionIsolation(muc);
      long l1 = so(a);
      b.createStatement().execute("update tk set so_du = so_du + 50");
      long l2 = so(a);
      a.commit();
      return l1 + " -> " + l2;
    }
  }
  public static void main(String[] x) throws Exception {
    try (Connection c = DriverManager.getConnection(U, "sa", "")) {
      c.createStatement().execute("create table tk (id int, so_du bigint)");
      c.createStatement().execute("insert into tk values (1, 1000)");
    }
    System.out.println("READ_COMMITTED: "
        + thu(Connection.TRANSACTION_READ_COMMITTED));
    System.out.println("REPEATABLE_READ: "
        + thu(Connection.TRANSACTION_REPEATABLE_READ));
    System.out.println("SERIALIZABLE: "
        + thu(Connection.TRANSACTION_SERIALIZABLE));
  }
}
''', lang="java", kind="other")

J_POOL = prog("DemBe", r'''
import java.sql.*;
import javax.sql.DataSource;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.jdbc.datasource.AbstractDataSource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.support.TransactionTemplate;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
public class DemBe {
  static class Be extends AbstractDataSource {
    final Semaphore cho;
    Be(int n) { cho = new Semaphore(n); }
    public Connection getConnection() throws SQLException {
      try {
        if (!cho.tryAcquire(400, TimeUnit.MILLISECONDS))
          throw new SQLException("het gio cho ket noi");
      } catch (InterruptedException e) { throw new SQLException(e); }
      Connection c = DriverManager.getConnection(
          "jdbc:h2:mem:be;DB_CLOSE_DELAY=-1", "sa", "");
      return (Connection) java.lang.reflect.Proxy.newProxyInstance(
          getClass().getClassLoader(), new Class<?>[] {Connection.class},
          (p, m, a) -> {
            Object r = m.invoke(c, a);
            if (m.getName().equals("close")) cho.release();
            return r;
          });
    }
    public Connection getConnection(String u, String p)
        throws SQLException { return getConnection(); }
  }
  static void doc(DataSource ds) {
    new JdbcTemplate(ds).queryForObject("select 1", Integer.class);
  }
  static void cho(CyclicBarrier b) {
    try { b.await(); } catch (Exception e) { }
  }
  static int chay(int luong, int be) throws Exception {
    var ds = new Be(be);
    var tm = new DataSourceTransactionManager(ds);
    var ngoai = new TransactionTemplate(tm);
    var trong = new TransactionTemplate(tm);
    trong.setPropagationBehavior(
        TransactionDefinition.PROPAGATION_REQUIRES_NEW);
    var loi = new AtomicInteger();
    var xong = new CountDownLatch(luong);
    var nhom = Executors.newFixedThreadPool(luong);
    var cua = new CyclicBarrier(luong);
    var cua2 = new CyclicBarrier(luong);
    for (int i = 0; i < luong; i++) nhom.submit(() -> {
      try {
        ngoai.executeWithoutResult(s -> {
          doc(ds);
          cho(cua);
          try {
            trong.executeWithoutResult(t -> doc(ds));
          } catch (Exception e) { loi.incrementAndGet(); }
          cho(cua2);
        });
      } catch (Exception e) { }
      xong.countDown();
    });
    xong.await();
    nhom.shutdown();
    return loi.get();
  }
  public static void main(String[] x) throws Exception {
    for (int[] c : new int[][] {{3, 3}, {3, 4}, {6, 6}, {6, 7}})
      System.out.println(c[0] + " luong, be " + c[1] + " ket noi: "
          + chay(c[0], c[1]) + " luong het gio");
  }
}
''', lang="java", kind="other")

SH_RUN = prog("ChaySpring", r'''
D=/d/research-video/audit/bnx/deps/l25
ls $D/spring-tx-7.0.10.jar >/dev/null 2>&1 || { echo "NOT_VERIFIED: thiếu jar" >&2; exit 97; }
mkdir -p lib out && cp $D/*.jar lib/
javac -encoding UTF-8 -cp "lib/*" -d out *.java
for c in DemTx DemCoLap DemBe; do
  java -Dstdout.encoding=UTF-8 -cp "out;lib/*" $c 2>/dev/null
done
''', lang="bash", files={"Cfg.java": "Cfg", "NhatKy.java": "NhatKy", "ChuyenTien.java": "ChuyenTien", "DoGio.java": "DoGio",
                         "DemTx.java": "DemTx", "DemCoLap.java": "DemCoLap", "DemBe.java": "DemBe"}, timeout=400)


LAB_PY = r'''
LOI_KIEM_TRA = {"IOException", "SQLException", "Exception"}   # kiểm tra: phải khai hoặc bắt
LOI_KHONG_KIEM_TRA = {"IllegalArgumentException", "RuntimeException", "NullPointerException"}


def hoan_tac(loi, rollback_for=()):
    if loi is None:
        return False
    if loi == "Error":
        return True
    if loi in LOI_KHONG_KIEM_TRA:
        return True
    return loi in rollback_for or ("Exception" in rollback_for and loi in LOI_KIEM_TRA)


CAC_CA = [
    ("IllegalArgumentException", ()),
    ("IOException", ()),
    ("IOException", ("Exception",)),
    ("Error", ()),
    (None, ()),
]
for loi, khai in CAC_CA:
    print(f"{loi or 'khong loi'} + {','.join(khai) or 'khong khai'}: {'hoan tac' if hoan_tac(loi, khai) else 'chot'}")
'''
LAB_OUT = """IllegalArgumentException + khong khai: hoan tac
IOException + khong khai: chot
IOException + Exception: hoan tac
Error + khong khai: hoan tac
khong loi + khong khai: chot"""
LAB_DE = """# Lab BNX L25 — Bảng quyết định hoàn tác của giao dịch

**MÔ PHỎNG**: bài này chỉ mô phỏng luật hoàn tác bằng Python thuần; không chạy Spring và không có cơ sở dữ liệu thật. Luật chép theo hướng dẫn chính thức của Spring (đã chạy thật ở phần ví dụ của video).

Theo quy tắc mặc định của Spring: ngoại lệ **không kiểm tra** (lớp con của `RuntimeException`) và `Error` làm giao dịch **hoàn tác**; ngoại lệ **kiểm tra** (như `IOException`)
thì **chốt**, trừ khi khai `rollbackFor` chứa kiểu đó (hoặc kiểu cha như `Exception`). Không có lỗi thì chốt.

Viết `mau.py` có hàm `hoan_tac(loi, rollback_for)` trả `True` khi giao dịch bị hoàn tác, rồi in đúng 5 dòng cho 5 ca sau (theo thứ tự), mỗi dòng dạng
`<loi> + <khai>: hoan tac` hoặc `...: chot` (không lỗi thì ghi `khong loi`, không khai thì ghi `khong khai`):

1. `IllegalArgumentException`, không khai   2. `IOException`, không khai   3. `IOException`, khai `Exception`   4. `Error`, không khai   5. không có lỗi

Gợi ý: kiểu kiểm tra: `IOException`, `SQLException`, `Exception`; không kiểm tra: `IllegalArgumentException`, `RuntimeException`, `NullPointerException`.
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L25 mau.py`.
"""


def build():
    _lab = write_lab("BNX", "L25", LAB_DE, "py", LAB_PY, LAB_OUT)
    # Mã ĐỦ của mọi tệp hiện trên màn hình dạng trích: một nguồn (prog), ghi ra thư mục kèm của lab để người học tự dựng lại
    _md = _lab / "ma_day_du"
    _md.mkdir(exist_ok=True)
    for _n, _p in (("Cfg", J_CFG), ("NhatKy", J_NK), ("ChuyenTien", J_CT), ("DoGio", J_DG), ("DemTx", J_TX), ("DemCoLap", J_ISO), ("DemBe", J_POOL)):
        (_md / f"{_n}.java").write_text(_p.code + "\n", encoding="utf-8", newline="\n")
    (_md / "README.txt").write_text(
        "Mã đủ của các ví dụ trong video BNX L25 (trên màn hình chỉ hiện đoạn trích).\n"
        "Cần các tệp jar: spring-context, spring-jdbc, spring-tx, spring-aop, spring-beans, spring-core, aspectjweaver 1.9.24, h2 2.3.232 (Spring 7.0.10, JDK 21).\n"
        "Dựng và chạy (Git Bash, jar đặt trong thư mục lib):\n"
        "  javac -encoding UTF-8 -cp \"lib/*\" -d out *.java\n"
        "  java -cp \"out;lib/*\" DemTx        # rồi DemCoLap, DemBe\n"
        "Đầu ra khớp phần Kết quả chạy thật trong video.\n", encoding="utf-8", newline="\n")
    hook = sc("hook", "hook", "Chuyển tiền lỗi giữa chừng: số dư về 1000, nhật ký còn hay mất?", [
        st("""<p>Dịch vụ chuyển tiền trừ 100 ở tài khoản rồi ghi một dòng nhật ký, sau đó gặp lỗi và ném ngoại lệ (báo lỗi). Chạy thật hai cách ghi nhật ký (số dư ban đầu 1000):</p>
<div class="box key">Cách 1, nhật ký ghi <b>cùng giao dịch</b>: số dư 1000, nhật ký <b>0</b> dòng. Cách 2, nhật ký ghi <b>giao dịch riêng</b>: số dư 1000, nhật ký <b>1</b> dòng.
Và một lỗi <b>kiểm tra</b> thì số dư lại thành <b>900</b>. Vì sao ba kết quả khác nhau?</div>""",
           """Chào bạn, dịch vụ chuyển tiền trừ một trăm ở tài khoản rồi ghi một dòng nhật ký, sau đó gặp lỗi và ném ngoại lệ, tức là báo lỗi. Số dư ban đầu là một nghìn: ghi nhật ký cùng giao dịch thì số dư về một nghìn và nhật ký trống. Ghi trong giao dịch riêng thì số dư vẫn về một nghìn nhưng nhật ký còn một dòng, và với một loại lỗi khác, số dư lại thành chín trăm. Vì sao ba ca cho ba kết quả khác nhau?""", focus=[1, 2, 2, 2]),
    ], checks=["alg.bnx_l25_balance(1000, 100, True) == 1000", "alg.bnx_l25_balance(1000, 100, False) == 900", "alg.bnx_l25_log_rows('REQUIRED') == 0 and alg.bnx_l25_log_rows('REQUIRES_NEW') == 1"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① giao dịch", "nhóm thao tác ghi: <b>chốt</b> thì cùng có hiệu lực, <b>hoàn tác</b> thì không cái nào; tính cùng thành hoặc cùng bỏ ấy gọi là <b>nguyên tử</b>", "trừ tiền và ghi nhật ký cùng thành hoặc cùng bỏ"],
                  ["② kết nối, bể và luồng", "<b>kết nối</b>: đường nối tới cơ sở dữ liệu, một giao dịch gắn với một kết nối; <b>bể kết nối</b>: nhóm kết nối dùng chung; <b>luồng</b> (thread): một dây việc chạy song song, như một nhân viên làm riêng", "bể 3 kết nối, 3 luồng cùng xin kết nối"],
                  ["③ ngoại lệ", "lỗi ném từ hàm; <b>kiểm tra</b>: phải khai hoặc bắt; <b>không kiểm tra</b>: lớp con của <code>RuntimeException</code>", "<code>IOException</code> là kiểm tra; <code>IllegalStateException</code> không"],
                  ["④ proxy", "đối tượng đứng trước đối tượng thật, nhận lời gọi, làm việc thêm rồi chuyển tiếp", "như lễ tân: ghi sổ rồi mới cho gặp"],
                  ["⑤ nhãn (annotation)", "dấu <code>@…</code> đặt trên lớp hoặc hàm để dặn thư viện", "<code>@Transactional</code>: hàm này chạy trong giao dịch"]]),
           """Trước hết ta cần hiểu năm điều. Giao dịch là nhóm thao tác ghi, chốt thì cùng có hiệu lực, hoàn tác thì không cái nào, tính ấy gọi là nguyên tử. Một giao dịch gắn với một kết nối, các kết nối nằm trong bể dùng chung, và luồng là một dây việc chạy song song. Ngoại lệ kiểm tra buộc phải khai hoặc bắt, ngoại lệ không kiểm tra thì không. Proxy là đối tượng đứng trước đối tượng thật, nhận lời gọi, làm thêm việc rồi chuyển tiếp.""",
           focus=[0, "1.2", "1.3", "1.4", ["1.5", "1.6"]], introduces=["bnx_nguyen_tu"]),
    ], checks=["alg.bnx_l25_rolls_back('IllegalStateException', ()) is True and alg.bnx_l25_rolls_back('IOException', ()) is False"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>@Transactional</code>", "dặn proxy: mở giao dịch trước hàm, <b>chốt</b> khi xong, <b>hoàn tác</b> khi gặp lỗi theo luật"],
                  ["<code>REQUIRED</code>", "<b>dùng chung</b>: có giao dịch rồi thì tham gia, chưa có thì mở mới (mặc định)"],
                  ["<code>REQUIRES_NEW</code>", "<b>luôn mở giao dịch riêng</b> trên kết nối khác; chốt hay hoàn tác độc lập"],
                  ["<code>rollbackFor</code>", "khai thêm kiểu lỗi làm hoàn tác, ví dụ <code>Exception.class</code> gồm cả lỗi kiểm tra"],
                  ["mức cô lập (isolation)", "mức một giao dịch được thấy thay đổi của giao dịch khác đang chạy"],
                  ["<code>@Aspect</code>, <code>@Around</code>", "<b>đoạn cắt</b>: mã chen quanh lời gọi hàm; <code>@Around</code> bọc cả trước và sau"]]),
           """Nhãn giao dịch dặn proxy mở giao dịch trước hàm, chốt khi hàm xong, và hoàn tác khi gặp lỗi theo luật. Kiểu dùng chung là có giao dịch thì tham gia, chưa có thì mở mới, còn kiểu riêng luôn mở giao dịch mới trên kết nối khác. Thuộc tính khai thêm kiểu lỗi làm hoàn tác. Mức cô lập quyết định giao dịch thấy thay đổi nào của giao dịch khác.""",
           focus=["1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
        st(table(["viết trong mã", "đọc là", "ví dụ nhỏ"],
                 [["<code>j.update(TRU)</code>", "<code>j</code> là <code>JdbcTemplate</code>, công cụ của Spring gửi câu SQL; <code>update</code> gửi câu ghi; <code>TRU</code> là chuỗi câu SQL trừ 100", "<code>j.update(\"insert … values (?)\", m)</code>: dấu <code>?</code> giữ chỗ cho giá trị <code>m</code>"],
                  ["<code>@Configuration</code>, <code>@Bean</code>", "lớp khai cách dựng đối tượng; <code>@Bean</code> đánh dấu hàm tạo ra một đối tượng để Spring giữ và đưa cho nơi cần", "<code>@Bean DataSource ds()</code> tạo nguồn kết nối"],
                  ["<code>@Around(\"execution(* ChuyenTien.rieng(..))\")</code>", "chuỗi trong ngoặc chọn hàm bị bọc: hàm <code>rieng</code> của <code>ChuyenTien</code>; <code>*</code> là mọi kiểu trả về, <code>(..)</code> là mọi đối số", "đổi <code>rieng</code> thành <code>*</code> thì bọc mọi hàm"]]),
           """Mã Spring sắp tới có vài chỗ cần đọc trước. Đối tượng gửi câu SQL có hàm cập nhật, và dấu hỏi trong câu giữ chỗ cho giá trị. Nhãn cấu hình khai cách dựng đối tượng, nhãn tạo đối tượng đánh dấu hàm cho Spring giữ. Chuỗi trong nhãn bọc chọn hàm bị bọc.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st(table(["viết trong mã", "đọc là", "ví dụ nhỏ"],
                 [["<code>() -&gt; ct.chuyenLoi(false)</code>, <code>s -&gt; { … }</code>, <code>ct::chuyenKiem</code>", "hàm nhỏ không tên: trái mũi tên là đối số, phải là việc làm; <code>::</code> là cách viết gọn cho lời gọi hàm", "<code>ngoai.executeWithoutResult(s -&gt; { … })</code> chạy khối trong một giao dịch"],
                  ["<code>a.setAutoCommit(false)</code>, <code>a.setTransactionIsolation(muc)</code>", "kết nối <code>a</code> thôi tự chốt từng câu (khi nào chốt do mã quyết định); rồi đặt mức cô lập", "<code>a.commit()</code> chốt cả nhóm"]]),
           """Mũi tên là hàm nhỏ không tên, trái là đối số, phải là việc làm. Hai dòng cuối tắt tự chốt từng câu và đặt mức cô lập.""",
           focus=["1.2", "1.3"], clear=True),
    ], checks=["alg.bnx_l25_rolls_back('IOException', ('Exception',)) is True"])

    intu = sc("intuition", "intuition", "Hình dung: proxy, hai kiểu lan truyền và đường tự gọi", [
        st(svg(1500, 560,
               txt(750, 40, "Lời gọi từ ngoài đi qua proxy; proxy mở giao dịch rồi mới tới hàm thật", 26, "middle", "#1f2937", True),
               box(40, 200, 200, 80, ["bên gọi", "(lớp khác)"], C_GRAY, 22),
               box(330, 150, 320, 180, ["proxy", "1 mở giao dịch", "2 gọi hàm thật", "3 chốt / hoàn tác"], C_AMBER, 22, True),
               box(780, 150, 300, 180, ["đối tượng thật", "chuyenLoi()", "nk.ghi(...)"], C_BLUE, 22, True),
               box(1180, 150, 260, 180, ["cơ sở dữ liệu", "một giao dịch", "một kết nối"], C_PURPLE, 22, True),
               arrow(245, 240, 325, 240), arrow(655, 240, 775, 240), arrow(1085, 240, 1175, 240),
               txt(750, 390, "REQUIRED: hàm trong dùng chung kết nối với hàm ngoài → lỗi ngoài thì cả hai cùng hoàn tác", 24, "middle", "#d97706", True),
               txt(750, 440, "REQUIRES_NEW: hàm trong lấy kết nối KHÁC, chốt ngay → lỗi ngoài sau đó không kéo nó theo", 24, "middle", "#16a34a", True),
               txt(750, 500, "tự gọi this.rieng(): từ đối tượng thật gọi thẳng đối tượng thật, KHÔNG qua proxy", 24, "middle", "#dc2626", True)),
           """Hình này cho thấy proxy: bên gọi gặp proxy trước đối tượng thật, và proxy mở giao dịch, gọi hàm thật, rồi chốt hoặc hoàn tác. Kiểu dùng chung thì hàm trong và hàm ngoài chung kết nối, nên lỗi ở ngoài làm cả hai hoàn tác. Kiểu riêng thì hàm trong chốt ngay trên kết nối khác. Còn khi đối tượng tự gọi hàm của chính nó, lời gọi không qua proxy.""",
           ),
        st(svg(1500, 560,
               txt(750, 40, "Một bể kết nối, nhiều luồng: giao dịch riêng cần THÊM một kết nối mỗi luồng", 26, "middle", "#1f2937", True),
               panel(40, 90, 1420, 130, "bể 3 kết nối, 3 luồng — mỗi luồng đang giữ 1 giao dịch ngoài", C_RED, 24),
               box(80, 150, 400, 55, "luồng 1: giữ kết nối A, xin kết nối trong", C_GRAY, 20),
               box(550, 150, 400, 55, "luồng 2: giữ kết nối B, xin kết nối trong", C_GRAY, 20),
               box(1020, 150, 400, 55, "luồng 3: giữ kết nối C, xin kết nối trong", C_GRAY, 20),
               txt(750, 260, "bể hết kết nối trống: cả 3 luồng chờ nhau tới hết giờ (quá hạn chờ thì bỏ cuộc, báo lỗi)", 24, "middle", "#dc2626", True),
               panel(40, 300, 1420, 130, "bể 4 kết nối, 3 luồng — còn 1 kết nối trống", C_GREEN, 24),
               box(80, 360, 400, 55, "luồng 1 xin kết nối D, xong, trả D", C_GREEN, 20),
               box(550, 360, 400, 55, "luồng 2 xin D, xong, trả D", C_GREEN, 20),
               box(1020, 360, 400, 55, "luồng 3 xin D, xong, trả D", C_GREEN, 20),
               txt(750, 470, "cần: số luồng + 1 kết nối (theo hướng dẫn: vượt số luồng đồng thời ít nhất 1)", 24, "middle", "#1f2937", True),
               txt(750, 520, "số liệu này được đo thật ở phần ví dụ", 22, "middle", "#475569")),
           """Hình thứ hai là điều người đi làm hay quên: mỗi lần tách giao dịch cần thêm một kết nối. Ba luồng, mỗi luồng giữ một giao dịch ngoài rồi xin thêm một kết nối cho giao dịch trong. Bể ba kết nối cạn nên cả ba chờ nhau tới hết giờ. Bể bốn kết nối còn một chỗ trống để các luồng lần lượt mượn rồi trả.""",
           ),
    ], checks=["alg.bnx_l25_pool_min(3) == 4", "alg.bnx_l25_timeouts(3, 3) == 3 and alg.bnx_l25_timeouts(3, 4) == 0"])

    form = sc("formula", "formula", "Suy ra từng bước: từ nhãn tới hành vi của giao dịch", [
        jstep([(("<code>static final String TRU = \"update …\";</code>", "<code>final</code>: gán một lần rồi không đổi; <code>static</code>: một bản chung cho cả lớp; <code>TRU</code> là chuỗi câu SQL trừ tiền", "Chữ cuối cùng nghĩa là gán một lần rồi không đổi, còn chữ tĩnh nghĩa là một bản chung cho cả lớp."), "", ""),
               (("<code>public void chuyenLoi(boolean rieng)</code>", "hàm không trả gì (<code>void</code>), nhận một tham số kiểu đúng hoặc sai tên <code>rieng</code>", "Hàm này không trả gì và nhận một tham số kiểu đúng hoặc sai."), "", ""),
               (("<code>if (rieng) nk.ghiRieng(…); else nk.ghi(…);</code>", "nếu <code>rieng</code> đúng thì làm câu sau <code>if</code>, ngược lại làm câu sau <code>else</code>", "Nếu biến đúng thì làm câu đứng ngay sau, ngược lại làm câu sau từ khoá còn lại."), "", ""),
               (("<code>throw new IllegalStateException(\"…\");</code>", "tạo một đối tượng lỗi rồi ném đi; hàm dừng ngay, lỗi bay ra cho nơi gọi", "Câu này tạo một đối tượng lỗi rồi ném đi, hàm dừng ngay và lỗi bay ra cho nơi gọi."), "", "")]),
        st("""<p><b>Bước 1.</b> Muốn mỗi hàm của dịch vụ tự mở và chốt giao dịch mà không viết lệnh mở/chốt ở từng hàm, Spring bọc đối tượng bằng một <b>proxy</b>. Nhãn <code>@Transactional</code> chỉ là lời dặn cho proxy.</p>"""
           + J_CT.show(lines=(10, 15), title="ChuyenTien.java (trích; mã đủ ở thư mục kèm của lab): hàm trừ tiền, ghi nhật ký, rồi lỗi")
           + """<p>Làm thử: kết quả chạy thật cho thấy <code>ct</code> là proxy (<code>AopUtils.isAopProxy</code> trả <b>true</b>).</p>""",
           """Bước một, vì muốn mỗi hàm tự mở và chốt giao dịch mà không viết lệnh ở từng hàm, Spring bọc đối tượng bằng một proxy. Nhãn giao dịch chỉ là lời dặn cho proxy, và chạy thật cho thấy đối tượng lấy từ Spring đúng là proxy.""", focus=[1, 2],
           clear=True),
        st("""<p><b>Bước 2. Lan truyền.</b> Hàm <code>ghi</code> của nhật ký cũng có <code>@Transactional</code>. Khi nó được gọi từ trong <code>chuyenLoi</code> (đã có giao dịch), kiểu mặc định <code>REQUIRED</code> cho nó <b>tham gia</b> giao dịch ngoài, nên hai việc cùng chung số phận.
Nếu muốn nhật ký sống sót dù chuyển tiền hỏng, dùng <code>REQUIRES_NEW</code>: giao dịch riêng, kết nối khác, chốt ngay.</p>"""
           + J_NK.show(lines=(6, 13), title="NhatKy.java: hai cách ghi nhật ký"),
           """Bước hai là lan truyền: hàm ghi nhật ký có nhãn giao dịch, và khi được gọi từ hàm chuyển tiền, kiểu mặc định cho nó tham gia giao dịch sẵn có, nên hai việc chung số phận. Muốn nhật ký sống sót, ta dùng giao dịch riêng.""", focus=[1, 3],
           clear=True),
        st("""<p><b>Bước 3. Hoàn tác.</b> Proxy bắt ngoại lệ bay ra từ hàm và quyết định. Mặc định hoàn tác khi là <b>lỗi không kiểm tra</b> (lớp con <code>RuntimeException</code>) hoặc <code>Error</code>; lỗi <b>kiểm tra</b> thì vẫn <b>chốt</b>, trừ khi khai <code>rollbackFor</code>.</p>"""
           + table(["lỗi ném ra", "khai gì thêm", "kết quả"],
                   [["IllegalStateException (không kiểm tra)", "không", "<b>hoàn tác</b>"],
                    ["Exception (kiểm tra)", "không", "<b>chốt</b>, số dư vẫn bị trừ"],
                    ["Exception (kiểm tra)", "<code>rollbackFor = Exception.class</code>", "<b>hoàn tác</b>"]]),
           """Bước ba là hoàn tác: proxy bắt ngoại lệ bay ra từ hàm, mặc định hoàn tác với lỗi không kiểm tra hoặc lỗi hệ thống nặng. Lỗi kiểm tra thì vẫn chốt, nên số dư vẫn bị trừ. Chỉ khi ta khai thêm kiểu lỗi đó thì nó mới hoàn tác.""",
           focus=["2.2", "2.3", "2.4"], clear=True),
        st("""<p><b>Bước 4. Tự gọi.</b> Proxy chỉ chặn được lời gọi đi <b>qua nó</b>. Khi hàm <code>goiNoiBo</code> gọi <code>this.rieng()</code>, lời gọi đi thẳng từ đối tượng thật tới đối tượng thật, nên proxy không có cơ hội mở giao dịch: nhãn trên <code>rieng()</code> bị bỏ qua.</p>"""
           + J_CT.show(lines=(26, 31), title="ChuyenTien.java (trích; mã đủ ở thư mục kèm của lab): hàm có nhãn và hàm tự gọi nó"),
           """Bước bốn là tự gọi: proxy chỉ chặn được những lời gọi đi qua nó. Khi hàm tự gọi hàm khác của chính đối tượng, lời gọi đi thẳng từ đối tượng thật tới đối tượng thật, nên proxy không mở giao dịch và nhãn trên hàm kia bị bỏ qua.""", focus=[1, 2, 3],
           clear=True),
        jstep([(("<code>public Object doThoiGian(ProceedingJoinPoint p) throws Throwable</code>", "hàm trả về <code>Object</code> (kiểu chung nhất), nhận <code>p</code> là lời gọi đang bị bọc; <code>throws Throwable</code>: có thể ném mọi loại lỗi", "Hàm trả về kiểu chung nhất, nhận lời gọi đang bị bọc, và lời báo ném lỗi cho phép ném mọi loại lỗi."), "", ""),
               (("<code>long t = System.nanoTime();</code>", "khai biến số nguyên lớn <code>t</code>, lưu giờ hiện tại tính bằng phần tỉ giây", "Khai một biến số nguyên lớn để lưu giờ hiện tại tính bằng phần tỉ giây."), "", ""),
               (("<code>try { return p.proceed(); } finally { dem++; … }</code>", "chạy hàm thật rồi trả kết quả; khối <code>finally</code> luôn chạy sau cùng dù có lỗi hay không; <code>dem++</code>: tăng đếm thêm 1; <code>x &amp;= c</code>: giữ đúng chỉ khi cả hai vế đúng", "Khối thử chạy hàm thật, còn khối cuối cùng luôn chạy sau cùng dù có lỗi hay không, ở đó biến đếm tăng thêm một."), "", "")], intro="Trước khi đọc đoạn cắt, ta đọc ba dòng của nó, vì chúng dùng cú pháp Java chưa gặp."),
        st("""<p><b>Bước 5. Đoạn cắt.</b> Cùng cơ chế proxy: Spring AOP chen đoạn cắt quanh lời gọi. <code>@Around</code> nhận quyền điều khiển, gọi <code>proceed()</code> để chạy hàm thật, và làm việc trước và sau.</p>"""
           + J_DG.show(lines=(7, 17), title="DoGio.java: đoạn cắt đo thời gian quanh hàm rieng()"),
           """Bước năm là đoạn cắt, dùng cùng cơ chế proxy nên kiểu bọc quanh nhận quyền điều khiển, gọi hàm tiến hành để chạy hàm thật, và làm việc trước lẫn sau. Ở đây nó đếm số lần gọi.""", focus=[1, 2],
           clear=True),
        st("""<p><b>Bước 6. Mức cô lập.</b> Hai giao dịch chạy cùng lúc: A đọc số dư, B sửa và chốt, A đọc lại. Mức <b>READ_COMMITTED</b>: A thấy giá trị mới (đọc lại ra khác). Mức <b>REPEATABLE_READ</b>: trên <b>H2</b>, A vẫn thấy giá trị cũ. Mức cô lập là tính năng của <b>cơ sở dữ liệu</b>, nên mỗi hệ có thể một khác (bài chỉ chạy thật trên H2). Spring chỉ đặt mức lên kết nối.</p>"""
           + """$$1000 \\to 1000 + 50 = 1050 \\text{ (đọc lại thấy B)} \\qquad 1000 \\to 1000 \\text{ (không thấy B)}$$""",
           """Bước sáu là mức cô lập: giao dịch A đọc số dư, giao dịch B sửa và chốt, rồi A đọc lại. Ở mức đọc dữ liệu đã chốt, A thấy giá trị mới vì mỗi lần đọc chỉ cần dữ liệu đã chốt. Ở mức đọc lặp lại được, trên H2, A vẫn thấy giá trị cũ, còn các hệ khác có thể cư xử khác.""", focus=[[1], 2],
           clear=True),
    ], checks=["alg.bnx_l25_rolls_back('IllegalStateException', ()) and not alg.bnx_l25_rolls_back('Exception', ())", "alg.bnx_l25_rolls_back('Exception', ('Exception',))",
               "alg.bnx_l25_isolation_reread('READ_COMMITTED', 1000, 50) == 1050 and alg.bnx_l25_isolation_reread('REPEATABLE_READ', 1000, 50) == 1000"])

    ex = sc("example", "example", "Ví dụ chạy thật Spring, từng phép tính", [
        jstep([(("<code>new DriverManagerDataSource(\"jdbc:h2:mem:l25;…\", \"sa\", \"\")</code>", "<code>new</code>: tạo đối tượng nguồn kết nối; ba đối số: địa chỉ (<code>h2:mem:l25</code> là H2 trong bộ nhớ, tên l25), tên đăng nhập <code>sa</code>, mật khẩu rỗng", "Chữ tạo mới tạo đối tượng nguồn kết nối với ba đối số: địa chỉ cơ sở dữ liệu trong bộ nhớ, tên đăng nhập và mật khẩu rỗng."), "", "")]),
        st(J_CFG.show(lines=(7, 14), title="Cfg.java (trích; mã đủ ở thư mục kèm của lab): bật giao dịch và đoạn cắt, khai nguồn dữ liệu"),
           """Ta chạy thật Spring bản bảy chấm không chấm mười với H2, cơ sở dữ liệu nhỏ trong bộ nhớ. Hai nhãn đầu bật proxy cho giao dịch và đoạn cắt, các hàm sau khai nguồn dữ liệu. Đây là đoạn trích, mã đủ của mọi tệp nằm trong thư mục thực hành.""",
           clear=True),
        st(J_TX.show(lines=(23, 28), title="DemTx.java (trích; mã đủ ở thư mục kèm của lab): bốn ca, mỗi ca đặt lại số dư 1000"),
           """Phép tính một tới bốn là bốn ca: mỗi ca đặt lại số dư về một nghìn, xoá nhật ký, gọi một hàm, rồi đọc số dư và đếm dòng nhật ký.""",
           clear=True),
        st(J_CT.show(lines=(16, 25), title="ChuyenTien.java (trích; mã đủ ở thư mục kèm của lab): hai hàm cho ca 3 và ca 4, chỉ khác phần khai rollbackFor"),
           """Ca ba và ca bốn gọi hai hàm này: cùng trừ tiền rồi ném lỗi kiểm tra, chỉ hàm sau khai thêm kiểu lỗi làm hoàn tác.""",
           clear=True),
        st(J_TX.out_html("""ct la proxy: true
1 REQUIRED, loi chay: so du 1000, nhat ky 0
2 REQUIRES_NEW, loi chay: so du 1000, nhat ky 1
3 loi kiem tra, mac dinh: so du 900, nhat ky 0
4 loi kiem tra, rollbackFor: so du 1000, nhat ky 0""")
           + """$$① \\; 1000 \\to \\hl{1000}, \\text{ nhật ký } 0; \\quad ② \\; 1000, \\text{ nhật ký } \\hlg{1}; \\quad ③ \\; 1000 - 100 = \\hl{900}; \\quad ④ \\; 1000$$""",
           """Ca một, hai việc dùng chung giao dịch và gặp lỗi không kiểm tra, nên số dư về một nghìn, nhật ký trống. Ca hai, nhật ký chạy giao dịch riêng nên còn một dòng. Ca ba ném lỗi kiểm tra không khai nên vẫn chốt, số dư còn chín trăm. Ca bốn khai thêm kiểu lỗi, số dư về một nghìn.""",
           focus=[[1], 2, 2, 3], clear=True),
        st(J_TX.show(lines=(29, 33), title="DemTx.java (trích; mã đủ ở thư mục kèm của lab): gọi qua proxy và gọi nội bộ"),
           """Phép tính năm là tự gọi: mã gọi hàm có nhãn giao dịch riêng hai lần, một lần qua proxy, một lần từ hàm bên trong cùng đối tượng, rồi in số lần đoạn cắt đã chạy.""", clear=True),
        st(J_TX.out_html("""goi qua proxy: giao dich true
goi noi bo: giao dich false
doan cat chay 1 lan, khong am true""")
           + """$$⑤ \\; \\text{qua proxy: giao dịch } \\hlg{true}; \\quad \\text{tự gọi: } \\hl{false}; \\quad \\text{đoạn cắt chạy } 1 \\text{ lần}$$""",
           """Hàm có nhãn giao dịch riêng, gọi qua proxy thì có giao dịch đang chạy, còn gọi nội bộ thì không có giao dịch nào. Đoạn cắt cũng chỉ chạy một lần, cho lần gọi qua proxy.""", focus=[1, 2],
           clear=True),
        jstep([(("<code>for (int i = 0; i &lt; luong; i++) nhom.submit(() -&gt; { … });</code>", "lặp <code>luong</code> lần, mỗi lần nộp một việc vào nhóm luồng; <code>() -&gt; { … }</code>: hàm nhỏ không tên, thân là việc của một luồng", "Vòng lặp chạy một lần cho mỗi luồng, mỗi lần nộp một hàm nhỏ không tên làm việc của luồng đó."), "", ""),
               (("<code>try { … } catch (Exception e) { loi.incrementAndGet(); }</code>", "thử chạy khối; có lỗi thì nhảy sang <code>catch</code> và tăng bộ đếm <code>loi</code> thêm 1", "Có lỗi thì nhảy sang khối bắt lỗi và tăng bộ đếm thêm một."), "", "")]),
        st(J_POOL.show(lines=(51, 63), title="DemBe.java (trích; mã đủ ở thư mục kèm của lab): mỗi luồng giữ giao dịch ngoài rồi xin giao dịch riêng"),
           """Phép tính sáu đo thật điều ở hình hai: bể kết nối tự viết có số kết nối cố định. Mỗi luồng giữ giao dịch ngoài, rồi xin giao dịch riêng, và ta đếm số luồng hết giờ.""", focus=[1, 2],
           clear=True),
        st(J_POOL.out_html("""3 luong, be 3 ket noi: 3 luong het gio
3 luong, be 4 ket noi: 0 luong het gio
6 luong, be 6 ket noi: 6 luong het gio
6 luong, be 7 ket noi: 0 luong het gio""")
           + """$$⑥ \\; \\text{bể} = \\text{luồng} \\Rightarrow \\hl{\\text{tất cả}} \\text{ hết giờ}; \\qquad \\text{bể} = \\text{luồng} + 1 \\Rightarrow \\hlg{0}$$""",
           """Kết quả thật: bể bằng số luồng thì mọi luồng đều hết giờ, thêm đúng một kết nối thì không luồng nào hết giờ, đúng như hướng dẫn.""",
           focus=[1, 2], clear=True),
    ], checks=["alg.bnx_l25_balance(1000, 100, True) == 1000 and alg.bnx_l25_balance(1000, 100, False) == 900",
               "alg.bnx_l25_log_rows('REQUIRED') == 0 and alg.bnx_l25_log_rows('REQUIRES_NEW') == 1",
               "alg.bnx_l25_timeouts(6, 6) == 6 and alg.bnx_l25_timeouts(6, 7) == 0"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: JDBC thuần, không Spring", [
        jstep([(("<code>try (Connection a = …; Connection b = …) { … }</code>", "<code>try</code> có ngoặc tròn: mở hai kết nối rồi tự đóng khi khối kết thúc, kể cả khi có lỗi", "Khối thử có ngoặc tròn mở hai kết nối và tự đóng chúng khi khối kết thúc, kể cả khi có lỗi."), "", ""),
               (("<code>long l1 = so(a);</code>", "gọi hàm <code>so</code> với kết nối <code>a</code>, lưu số dư (số nguyên lớn) vào <code>l1</code>", "Gọi hàm đọc số dư với kết nối a và lưu kết quả vào một biến số nguyên lớn."), "", ""),
               (("<code>return l1 + \" -&gt; \" + l2;</code>", "dấu <code>+</code> nối số với chuỗi thành một chuỗi, ví dụ <code>1000 -&gt; 1050</code>", "Dấu cộng giữa số và chuỗi nối chúng thành một chuỗi, như một nghìn mũi tên một nghìn không trăm năm mươi."), "", "")], intro="Trước khi đọc mã, ta đọc ba dòng của nó, vì chúng dùng cú pháp Java chưa gặp."),
        st(J_ISO.show(lines=(11, 23), title="DemCoLap.java (trích; mã đủ ở thư mục kèm của lab): hai kết nối JDBC (bộ lời gọi chuẩn của Java tới cơ sở dữ liệu), không dùng Spring"),
           """Ta kiểm mức cô lập bằng đường khác, vì muốn chắc kết quả không phụ thuộc Spring: chỉ dùng bộ lời gọi chuẩn của Java tới cơ sở dữ liệu. Kết nối A đặt mức cô lập và đọc số dư, kết nối B cộng thêm năm mươi và chốt, rồi A đọc lại.""",
           clear=True, introduces=["bnx_jdbc"]),
        st(J_ISO.out_html("""READ_COMMITTED: 1000 -> 1050
REPEATABLE_READ: 1000 -> 1000
SERIALIZABLE: 1000 -> 1000""") + table(["mức (kết quả đo trên H2)", "lần đọc thứ hai của A", "vì sao"],
                                      [["READ_COMMITTED", "1050", "chỉ cần dữ liệu đã chốt: thấy thay đổi của B"],
                                       ["REPEATABLE_READ", "1000", "đọc lặp lại cho cùng kết quả trong giao dịch"],
                                       ["SERIALIZABLE", "1000", "cô lập chặt nhất"]]),
           """Kết quả thật, ở mức chỉ cần dữ liệu đã chốt, lần đọc thứ hai thấy một nghìn không trăm năm mươi, vì thay đổi của B đã chốt. Ở hai mức chặt hơn, lần đọc thứ hai vẫn là một nghìn. Đây là số đo trên H2, hệ khác có thể cho kết quả khác.""",
           focus=[0, 2, 2], clear=True),
    ], checks=["alg.bnx_l25_isolation_reread('READ_COMMITTED', 1000, 50) == 1050", "alg.bnx_l25_isolation_reread('SERIALIZABLE', 1000, 50) == 1000"])

    quymo = sc("quymo", "example", "Khi tải lớn dần: bể kết nối cần bao nhiêu?", [
        st(table(["số luồng đồng thời", "bể cần tối thiểu nếu có giao dịch riêng (luồng + 1)", "bể bằng số luồng thì", "nguồn số"],
                 [[nowrap("3 (×1)"), "4", "3 luồng hết giờ (đo thật)", "chạy thật DemBe"],
                  ["6", "7", "6 luồng hết giờ (đo thật)", "chạy thật DemBe"],
                  [nowrap("300 (×100)"), "301", "300 luồng chờ nhau tới hết giờ, nếu cả 300 cùng giữ giao dịch ngoài lúc đó (suy từ quy tắc)", "công thức của hướng dẫn"],
                  [nowrap("30 000 (×10 000)"), "30 001", "bể không thể lớn như thế: cơ sở dữ liệu giới hạn kết nối", "suy ra: phải bỏ giao dịch riêng hoặc hạ số luồng"]]),
           """Ba luồng cần bể bốn kết nối, hai dòng đầu đã đo thật. Ba trăm luồng, gấp một trăm lần, cần ba trăm lẻ một kết nối, nếu bể chỉ bằng số luồng thì chờ nhau tới hết giờ. Ba mươi nghìn luồng cần ba mươi nghìn lẻ một kết nối, cơ sở dữ liệu thường không cho nhiều thế, nên cách làm cũ gãy.""",
           focus=[0, "1.2", "1.4", "1.5"]),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["giao dịch riêng cho nhật ký", "nhật ký sống sót khi nghiệp vụ hỏng", "mỗi luồng cần 1 kết nối thêm; nhật ký và nghiệp vụ không còn nguyên tử", "nhật ký kiểm toán phải còn dù lỗi, và bể được tính đủ"],
                  ["dùng chung giao dịch", "một kết nối, nhất quán cả hai", "nghiệp vụ hỏng thì nhật ký mất", "dữ liệu phải cùng thành hoặc cùng bỏ"],
                  ["ghi nhật ký ra ngoài giao dịch (<b>hàng đợi</b>: nơi thông điệp xếp hàng chờ chương trình khác xử lý; hoặc tệp)", "không giữ thêm kết nối", "thêm một thành phần phải vận hành", "tải rất lớn, nhật ký ghi dồn"]]),
           """Người làm nghề phải chọn. Giao dịch riêng giúp nhật ký sống sót khi nghiệp vụ hỏng, đổi lại mỗi luồng cần thêm một kết nối. Dùng chung thì một kết nối và nhất quán, nhưng nghiệp vụ hỏng thì nhật ký mất. Khi tải rất lớn, người ta ghi nhật ký ra ngoài giao dịch, qua hàng đợi hoặc tệp, đổi lại thêm một thành phần.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["[alg.bnx_l25_pool_min(n) for n in (3, 6, 300, 30000)] == [4, 7, 301, 30001]", "alg.bnx_l25_pool_min(3 * 100) == 301 and 30000 // 3 == 10000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Ném <b class="red">lỗi kiểm tra</b> từ hàm có <code>@Transactional</code> và tin rằng giao dịch sẽ hoàn tác. Chạy thật ca 3: số dư vẫn <b>900</b>.
Quy tắc mặc định của Spring: chỉ lỗi không kiểm tra và <code>Error</code> làm hoàn tác. Muốn khác thì khai <code>rollbackFor</code>.</div>""",
           """Lỗi thứ nhất, của người mới, là ném lỗi kiểm tra từ hàm có nhãn giao dịch và tin rằng giao dịch sẽ hoàn tác. Chạy thật ở ca ba, số dư vẫn là chín trăm, vì mặc định chỉ lỗi không kiểm tra làm hoàn tác.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Đặt <code>@Transactional</code> lên hàm rồi <b class="red">gọi nó bằng <code>this.</code></b> từ hàm khác cùng lớp: chạy thật, giao dịch <b>false</b>.
Chương trình vẫn "chạy được" cho tới khi gặp ca hoàn tác. Cách chữa: tách sang một đối tượng khác, hoặc để lời gọi đi qua proxy. Cùng lỗi áp cho đoạn cắt: bị bỏ qua.</div>"""
           + J_CT.show(lines=(26, 31)),
           """Lỗi thứ hai: đặt nhãn giao dịch lên một hàm rồi gọi nó bằng từ khoá chỉ chính nó từ hàm khác cùng lớp. Hàm kia không có giao dịch, nên chương trình chạy êm cho tới ca cần hoàn tác. Cách chữa là tách hàm sang đối tượng khác.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Dùng <code>REQUIRES_NEW</code> khắp nơi cho tiện. Đo thật: khi mọi luồng cùng giữ giao dịch ngoài, bể bằng số luồng thì <b class="red">mọi luồng hết giờ</b> chờ nhau; cần bể ≥ luồng + 1.
Mỗi lần tách là thêm một kết nối bị giữ, nên khi tải tăng, bể kết nối cạn trước cả cơ sở dữ liệu.</div>""",
           """Lỗi thứ ba, khi tải tăng: dùng giao dịch riêng khắp nơi cho tiện. Đo thật: bể bằng số luồng thì tất cả hết giờ, vì mỗi lần tách là giữ thêm một kết nối.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> Hàm <b>ngoài</b> <b class="red">bắt lỗi</b> do hàm <b>trong</b> ném ra (<code>catch</code> rỗng) rồi vẫn chạy tiếp và chốt. Hàm trong đã đánh dấu giao dịch chung là &laquo;chỉ được hoàn tác&raquo;,
nên lúc chốt bên gọi nhận <code>UnexpectedRollbackException</code> (theo hướng dẫn của Spring). Nhật ký ghi "đã chuyển" mà tiền không đi: lỗi chỉ lộ sau nhiều tháng, khi đối soát lệch.
<br><span class="note">Nếu chính hàm trong tự nuốt lỗi thì proxy không thấy lỗi nào, giao dịch cứ chốt: lỗi khác, hậu quả cũng tệ.</span></div>""",
           """Lỗi thứ tư, khi vận hành lâu: hàm ngoài bắt lỗi do hàm trong ném ra rồi vẫn chạy tiếp và chốt. Hàm trong đã đánh dấu giao dịch chung là chỉ được hoàn tác, nên lúc chốt bên gọi nhận một ngoại lệ bất ngờ, và nhật ký ghi đã chuyển mà tiền không đi.""", clear=True),
    ], checks=["not alg.bnx_l25_rolls_back('Exception', ()) and alg.bnx_l25_balance(1000, 100, False) == 900", "alg.bnx_l25_timeouts(3, 3) == 3"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Hàm <code>A</code> (<code>@Transactional</code>) gọi hàm <code>B</code> của <b>đối tượng khác</b> (<code>REQUIRED</code>) rồi A ném <code>IOException</code> (lỗi kiểm tra, không khai gì). Dữ liệu của B còn không?"],
                  ["2", "Dịch vụ có 40 luồng, mỗi luồng có thể giữ giao dịch ngoài rồi gọi <code>REQUIRES_NEW</code>. Bể kết nối tối thiểu bao nhiêu? Bể 40 thì sao?"],
                  ["3", "Quyết định (số minh hoạ): nhật ký kiểm toán phải còn dù chuyển tiền hỏng; tải 2 000 yêu cầu mỗi giây, bể 50 kết nối. Chọn: <code>REQUIRES_NEW</code>, dùng chung giao dịch, hay đẩy ra hàng đợi? Vì sao?"]]),
           """Đến lượt bạn, ba câu. Câu một: hàm A có nhãn giao dịch gọi hàm B của đối tượng khác rồi ném lỗi kiểm tra không khai gì, dữ liệu của B còn không? Câu hai: bốn mươi luồng giữ giao dịch ngoài rồi gọi giao dịch riêng, bể tối thiểu bao nhiêu? Câu ba: nhật ký kiểm toán phải còn dù chuyển tiền hỏng, chọn cách nào? Hãy dừng video và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=30),
        st("""<p>Câu 1: lỗi kiểm tra không khai gì thì <b>chốt</b>, và B tham gia chung giao dịch nên dữ liệu của B cũng được chốt.</p>
$$\\text{IOException, không khai} \\Rightarrow \\hlg{\\text{chốt}} \\Rightarrow \\text{dữ liệu của B còn}$$""",
           """Đáp án câu một. Lỗi kiểm tra mà không khai gì thì giao dịch vẫn chốt, và B tham gia chung giao dịch nên dữ liệu của B cũng được chốt."""),
        st("""<p>Câu 2: theo hướng dẫn, bể phải vượt số luồng đồng thời ít nhất 1.</p>
$$40 + 1 = \\hlg{41} \\text{ kết nối}; \\qquad \\text{bể } 40 = \\text{số luồng} \\Rightarrow \\text{có thể mọi luồng chờ nhau tới hết giờ}$$""",
           """Đáp án câu hai. Bể cần tối thiểu bốn mươi mốt kết nối, vì bể bốn mươi bằng số luồng thì khi mọi luồng cùng giữ giao dịch ngoài, tất cả chờ nhau tới hết giờ."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["giao dịch riêng", "nhật ký chắc chắn còn", "2 000 yêu cầu mỗi giây có thể giữ thêm nhiều kết nối; bể 50 dễ cạn"],
                  ["dùng chung giao dịch", "nhất quán, không thêm kết nối", "chuyển tiền hỏng thì nhật ký mất, trái yêu cầu kiểm toán"],
                  ["đẩy ra hàng đợi (hoặc tệp) có ghi bền", "không giữ thêm kết nối; nhật ký còn", "thêm thành phần; ghi trễ"]]),
           """Đáp án câu ba: giao dịch riêng giữ được nhật ký, nhưng ở hai nghìn yêu cầu mỗi giây bể năm mươi dễ cạn. Dùng chung thì nhật ký mất khi chuyển tiền hỏng, trái yêu cầu kiểm toán. Hàng đợi hoặc tệp không giữ thêm kết nối, đổi lại thêm một thành phần."""),
    ], checks=["not alg.bnx_l25_rolls_back('IOException', ())", "alg.bnx_l25_pool_min(40) == 41 and alg.bnx_l25_timeouts(40, 40) == 40"])

    lab_pr = practice_scene(sc, "Tự làm: bảng quyết định hoàn tác", practice_steps(
        st, "BNX", "L25",
        """<p><b>Đề (MÔ PHỎNG, không chạy Spring)</b>: viết <code>mau.py</code> có hàm <code>hoan_tac(loi, rollback_for)</code> theo quy tắc mặc định của Spring, rồi in 5 dòng cho 5 ca:</p>
<ol><li><code>IllegalArgumentException</code>, không khai</li><li><code>IOException</code>, không khai</li><li><code>IOException</code>, khai <code>Exception</code></li><li><code>Error</code>, không khai</li><li>không có lỗi</li></ol>
<p class="note">Mỗi dòng dạng <code>&lt;lỗi&gt; + &lt;khai&gt;: hoan tac</code> hoặc <code>chot</code>. Kiểu kiểm tra: IOException, SQLException, Exception. Chi tiết trong <code>de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm, một mô phỏng không chạy Spring: viết một hàm Python quyết định giao dịch hoàn tác hay chốt theo quy tắc mặc định của Spring. Chạy hàm cho năm ca có trong đề. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> kiểm theo thứ tự: không lỗi → chốt; <code>Error</code> → hoàn tác; lỗi không kiểm tra → hoàn tác; lỗi kiểm tra → hoàn tác chỉ khi nó (hoặc <code>Exception</code>) nằm trong danh sách khai.
Lời giải đầy đủ ở <code>labs/BNX/L25/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, kiểm theo thứ tự: không lỗi thì chốt, lỗi hệ thống nặng hoặc không kiểm tra thì hoàn tác. Còn lỗi kiểm tra thì chỉ hoàn tác khi nó, hoặc kiểu cha, nằm trong danh sách khai. Lời giải chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L25")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("nhãn dặn proxy", "REQUIRED dùng chung / REQUIRES_NEW tách riêng", "lỗi không kiểm tra → hoàn tác", "tự gọi đi vòng proxy", "bể ≥ luồng + 1"),
           """Nhãn giao dịch là lời dặn cho proxy, kiểu dùng chung cho hai hàm chung số phận còn giao dịch riêng tách chúng. Mặc định chỉ lỗi không kiểm tra làm hoàn tác, và tự gọi trong cùng đối tượng đi vòng qua proxy."""),
        st("""<div class='box key'><b>Tư duy:</b> nhãn không phải phép thuật, nó chỉ chạy khi lời gọi <b>đi qua proxy</b>. Mỗi lần chọn kiểu lan truyền là chọn <b>số phận chung hay riêng</b> và <b>giá bằng kết nối</b>;
đừng tin: hãy chạy ca hoàn tác, ca tự gọi và ca tải để thấy.</div>""",
           """Nhãn chỉ chạy khi lời gọi đi qua proxy. Giao dịch riêng trả bằng kết nối, nên hãy chạy ca hoàn tác, ca tự gọi và ca tải để thấy."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Spring Transaction: REQUIRED và REQUIRES_NEW khác gì?", "dùng chung hay tách giao dịch/kết nối; chạy thật: nghiệp vụ hỏng thì dùng chung mất cả nhật ký, giao dịch riêng giữ nhật ký; đổi lại cần bể ≥ luồng + 1"],
                  ["Lỗi nào làm hoàn tác, tại sao có khi không hoàn tác?", "mặc định chỉ lỗi không kiểm tra và Error; lỗi kiểm tra chốt trừ khi rollbackFor; nuốt lỗi hoặc tự gọi cũng làm không hoàn tác như tưởng"],
                  ["AOP/đoạn cắt dùng thế nào?", "@Around trên proxy, gọi proceed, đo hoặc ghi nhật ký quanh lời gọi; cùng hạn chế tự gọi như giao dịch"]]),
           """Người phỏng vấn thường hỏi ba câu: hai kiểu lan truyền khác gì, lỗi nào làm hoàn tác, và đoạn cắt dùng thế nào. Câu trả lời ngắn nằm sẵn trên bảng.""", clear=True),
        st("""<p>Bài sau: <b>Maven, Gradle và Jenkins</b>: dựng dự án tái lập được, phụ thuộc bắc cầu và xung đột phiên bản.</p>""",
           """Ở bài hai mươi sáu, ta dựng dự án tái lập được bằng công cụ dựng, cùng phụ thuộc bắc cầu và xung đột phiên bản.""",
           forward_ref=True),
    ], checks=["alg.bnx_l25_pool_min(3) == 4"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L25", "giao_dich_spring_aop",
                  "Bài 25 — Giao dịch Spring và AOP chuyên sâu: lan truyền, hoàn tác, tự gọi và đoạn cắt",
                  "curriculum/bnx.yaml L25; audit/bnx/verify_bnx.py L25; audit/bnx/sources_l25.md: hướng dẫn Spring Framework (Transaction Propagation, "
                  "Rolling Back a Declarative Transaction, Using @Transactional, AOP Proxies; đọc 2026-11-13); Spring 7.0.10 + AspectJ weaver 1.9.24 + H2 2.3.232 chạy thật trên Temurin JDK 21.0.13",
                  ["Đọc một hàm có nhãn giao dịch và nói proxy mở, chốt hoặc hoàn tác ở đâu",
                   "So sánh REQUIRED với REQUIRES_NEW qua số dư và số dòng nhật ký sau một lỗi",
                   "Xác định lỗi nào làm giao dịch hoàn tác và khai rollbackFor khi cần",
                   "Chỉ ra vì sao lời gọi tự gọi bỏ qua nhãn giao dịch và đoạn cắt",
                   "So sánh mức cô lập READ_COMMITTED với REPEATABLE_READ trên hai kết nối",
                   "Tính số kết nối tối thiểu của bể khi dùng giao dịch riêng",
                   "Viết bảng quyết định hoàn tác theo quy tắc mặc định của Spring"],
                  scenes, assumes=["bnx_ngoai_le", "bnx_be_ket_noi", "bnx_h2"],
                  covers=[(1, "formula"), (2, "example"), (3, "formula"), (4, "example"), (5, "check"), (6, "quymo"), (7, "practice")])
