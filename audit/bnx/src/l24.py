import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from libj import jstep, nowrap

lib2.begin("L24")

# ── Mã chạy THẬT (audit/bnx/deps/l24: Hibernate ORM 7.1.0.Final + H2 2.3.232 do Maven tải; sha256 ở README.md) ──
# Đầu ra là đầu ra thật (đệm ở audit/bnx/progcache/L24.json), tất định: đếm câu SQL, không in thời gian.
J_KHACH = prog("Khach", r'''
import jakarta.persistence.*;
import java.util.*;
@Entity
public class Khach {
  @Id Long id;
  String ten;
  @OneToMany(mappedBy = "khach")
  List<TaiKhoan> tk = new ArrayList<>();
}
''', lang="java", kind="other")

J_TK = prog("TaiKhoan", r'''
import jakarta.persistence.*;
@Entity
public class TaiKhoan {
  @Id Long id;
  @ManyToOne(fetch = FetchType.LAZY)
  Khach khach;
  long soDu;
}
''', lang="java", kind="other")

J_KHO = prog("Kho", r'''
import org.hibernate.*;
import org.hibernate.cfg.Configuration;
public class Kho {
  static SessionFactory mo(int n) {
    SessionFactory sf = new Configuration()
        .addAnnotatedClass(Khach.class)
        .addAnnotatedClass(TaiKhoan.class)
        .setProperty("hibernate.connection.url", "jdbc:h2:mem:bnx")
        .setProperty("hibernate.hbm2ddl.auto", "create-drop")
        .setProperty("hibernate.generate_statistics", "true")
        .buildSessionFactory();
    try (Session s = sf.openSession()) {
      Transaction t = s.beginTransaction();
      for (long i = 1; i <= n; i++) {
        Khach k = new Khach();
        k.id = i;
        k.ten = "K" + i;
        s.persist(k);
        for (long j = 1; j <= 2; j++) {
          TaiKhoan a = new TaiKhoan();
          a.id = i * 10 + j;
          a.khach = k;
          a.soDu = 1000 * j;
          s.persist(a);
        }
      }
      t.commit();
    }
    return sf;
  }
  static SessionFactory xem() {      // cùng CSDL trong bộ nhớ, bật in câu SQL
    return new Configuration()
        .addAnnotatedClass(Khach.class)
        .addAnnotatedClass(TaiKhoan.class)
        .setProperty("hibernate.connection.url", "jdbc:h2:mem:bnx")
        .setProperty("hibernate.show_sql", "true")
        .buildSessionFactory();
  }
}
''', lang="java", kind="other")

J_SQL = prog("DemSql", r'''
import org.hibernate.*;
public class DemSql {
  public static void main(String[] x) {
    SessionFactory goc = Kho.mo(2);
    SessionFactory sf = Kho.xem();
    try (Session s = sf.openSession()) {
      for (Khach k : s.createQuery("select k from Khach k",
          Khach.class).getResultList())
        System.out.println(k.ten + ": " + k.tk.size() + " tai khoan");
    }
  }
}
''', lang="java", kind="other")

J_N1 = prog("DemN1", r'''
import org.hibernate.*;
import org.hibernate.stat.Statistics;
public class DemN1 {
  static final String LUOI = "select k from Khach k where k.id <= :n";
  static final String NHANH =
      "select k from Khach k join fetch k.tk where k.id <= :n";
  static long dem(SessionFactory sf, String q, long n) {
    Statistics st = sf.getStatistics();
    st.clear();
    try (Session s = sf.openSession()) {
      for (Khach k : s.createQuery(q, Khach.class)
          .setParameter("n", n).getResultList())
        k.tk.size();           // đụng vào danh sách tài khoản
    }
    return st.getPrepareStatementCount();
  }
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(500);
    for (long n : new long[] {5, 50, 500})
      System.out.println(n + " khach: tai luoi " + dem(sf, LUOI, n)
          + " cau, JOIN FETCH " + dem(sf, NHANH, n) + " cau");
  }
}
''', lang="java", kind="other")

J_BAN = prog("DemBan", r'''
import org.hibernate.*;
import org.hibernate.stat.Statistics;
public class DemBan {
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(3);
    Statistics st = sf.getStatistics();
    try (Session s = sf.openSession()) {
      st.clear();
      TaiKhoan a = s.find(TaiKhoan.class, 11L);
      TaiKhoan b = s.find(TaiKhoan.class, 11L);
      System.out.println("doc hai lan: cung doi tuong " + (a == b)
          + ", " + st.getPrepareStatementCount() + " cau SQL");
      Transaction t = s.beginTransaction();
      a.soDu = a.soDu + 500;          // không gọi hàm lưu nào
      s.createQuery("select count(t) from TaiKhoan t", Long.class)
          .getSingleResult();
      System.out.println("sau truy van, truoc chot: "
          + st.getEntityUpdateCount() + " UPDATE");
      t.commit();
    }
    try (Session s = sf.openSession()) {
      st.clear();
      TaiKhoan c = s.find(TaiKhoan.class, 12L);
      s.detach(c);                    // rời ngữ cảnh bền vững
      Transaction t = s.beginTransaction();
      c.soDu = c.soDu + 500;
      t.commit();
      System.out.println("sua doi tuong da roi: "
          + st.getEntityUpdateCount() + " UPDATE");
    }
    try (Session s = sf.openSession()) {
      System.out.println("so du 11: " + s.find(TaiKhoan.class, 11L).soDu
          + ", so du 12: " + s.find(TaiKhoan.class, 12L).soDu);
    }
  }
}
''', lang="java", kind="other")

J_LOI = prog("DemLoi", r'''
import org.hibernate.*;
public class DemLoi {
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(3);
    Khach k;
    try (Session s = sf.openSession()) {
      k = s.find(Khach.class, 1L);
    }                                 // phiên đã đóng
    try {
      System.out.println(k.tk.size());
    } catch (LazyInitializationException e) {
      System.out.println("loi: " + e.getClass().getSimpleName());
    }
  }
}
''', lang="java", kind="other")

J_NHO = prog("DemNho", r'''
import org.hibernate.*;
public class DemNho {
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(500);
    try (Session s = sf.openSession()) {
      for (Khach k : s.createQuery("select k from Khach k join fetch "
          + "k.tk", Khach.class).getResultList())
        k.ten.length();
      System.out.println("ngu canh giu: "
          + s.getStatistics().getEntityCount() + " doi tuong");
      s.clear();
      System.out.println("sau clear: "
          + s.getStatistics().getEntityCount() + " doi tuong");
    }
  }
}
''', lang="java", kind="other")

J_TRANG = prog("DemTrang", r'''
import org.hibernate.*;
import java.util.*;
public class DemTrang {
  static void in(String ten, Session s, List<Khach> ds, long cau) {
    System.out.println(ten + ": " + ds.size() + " khach, " + cau
        + " cau, ngu canh giu " + s.getStatistics().getEntityCount() + " doi tuong");
  }
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(500);
    try (Session s = sf.openSession()) {
      sf.getStatistics().clear();
      List<Khach> ds = s.createQuery("select k from Khach k join fetch k.tk",
          Khach.class).setMaxResults(20).getResultList();
      in("cat tai cho (join fetch + trang)", s, ds, sf.getStatistics().getPrepareStatementCount());
    }
    try (Session s = sf.openSession()) {
      sf.getStatistics().clear();
      List<Long> ma = s.createQuery("select k.id from Khach k order by k.id",
          Long.class).setMaxResults(20).getResultList();
      List<Khach> ds = s.createQuery("select k from Khach k join fetch k.tk "
          + "where k.id in :ma", Khach.class).setParameter("ma", ma).getResultList();
      in("hai buoc (lay ma roi join fetch)", s, ds, sf.getStatistics().getPrepareStatementCount());
    }
  }
}
''', lang="java", kind="other", files={"Khach.java": "Khach", "TaiKhoan.java": "TaiKhoan", "Kho.java": "Kho"})

SH_RUN = prog("ChayHib", r'''
D=/d/research-video/audit/bnx/deps/l24
ls $D/hibernate-core-7.1.0.Final.jar >/dev/null 2>&1 || { echo "NOT_VERIFIED: thiếu jar" >&2; exit 97; }
mkdir -p lib out && cp $D/*.jar lib/
javac -encoding UTF-8 -cp "lib/*" -d out *.java
for c in DemSql DemN1 DemBan DemLoi DemNho DemTrang; do
  java -Dstdout.encoding=UTF-8 -cp "out;lib/*" $c 2>/dev/null
done
''', lang="bash", files={"Khach.java": "Khach", "TaiKhoan.java": "TaiKhoan", "Kho.java": "Kho", "DemSql.java": "DemSql",
                         "DemN1.java": "DemN1", "DemBan.java": "DemBan", "DemLoi.java": "DemLoi", "DemNho.java": "DemNho", "DemTrang.java": "DemTrang"},
              timeout=400,
              claims=["tải lười 6, 51, 501 câu SQL cho 5, 50, 500 khách; nối kèm tải luôn 1 câu",
                      "sửa đối tượng đang quản lý sinh một lệnh UPDATE ngay khi truy vấn kế tiếp, trước cả khi chốt",
                      "sửa đối tượng đã rời ngữ cảnh: 0 UPDATE", "đọc danh sách lười sau khi đóng phiên báo LazyInitializationException",
                      "ngữ cảnh giữ 1500 đối tượng, sau clear còn 0",
                      "phân trang cùng nối kèm tải danh sách: Hibernate cắt trong bộ nhớ (ngữ cảnh giữ cả 1500 đối tượng); hai bước (lấy mã rồi nối kèm) chỉ giữ 60"])

PY_CHECK = prog("DemPy", r'''
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE k (id INTEGER)")
db.execute("CREATE TABLE t (id INTEGER, kid INTEGER)")
for i in range(1, 51):
    db.execute("INSERT INTO k VALUES (?)", (i,))
    db.execute("INSERT INTO t VALUES (?, ?)", (i * 10 + 1, i))
    db.execute("INSERT INTO t VALUES (?, ?)", (i * 10 + 2, i))
n = []
db.set_trace_callback(lambda c: n.append(c))
for (i,) in db.execute("SELECT id FROM k").fetchall():
    db.execute("SELECT * FROM t WHERE kid = ?", (i,)).fetchall()
print(len(n), "cau")
''', lang="python", claims=["50 khách đọc kiểu tải lười: 51 câu SQL"])

JAVA_REPO = r'''
interface KhachRepo extends CrudRepository<Khach, Long> {
  List<Khach> findByTen(String ten);
  long countByTen(String ten);
}
'''
lib2.other("interface KhachRepo", kind="other", lang="java",
           reason="Giao diện kho truy cập dữ liệu theo mẫu của hướng dẫn Spring Data (UserRepository, countByLastname).",
           read_check="Ghép từ hai ví dụ trong hướng dẫn Spring Data JPA/Commons (audit/bnx/sources_l24.md, mã [SDREPO]); KHÔNG chạy trên máy này: cần Spring Data và cấu hình Spring. "
                      "Quy tắc đặt tên findBy/countBy theo hướng dẫn; Khach/Long là thực thể của bài.")

JQL_FETCH = '''select k from Khach k
 join fetch k.tk
 where k.id <= :n'''
lib2.other("select k from Khach k", kind="other", lang="sql",
           reason="Câu truy vấn theo đối tượng (JPQL/HQL) đã chạy thật trong DemN1.java (hằng NHANH); ở đây xuống dòng để dễ đọc.",
           read_check="Câu này là hằng NHANH của DemN1.java (chạy thật, đếm 1 câu SQL ở 5, 50, 500 khách); chỉ khác chỗ xuống dòng.")

# Số liệu lab (khác số ví dụ): 12 khách, mỗi khách 3 thẻ → cách 1: 1 + 12 = 13 câu, cách 2: 1 câu
LAB_PY = r'''
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE khach (id INTEGER PRIMARY KEY, ten TEXT);
CREATE TABLE the (id INTEGER PRIMARY KEY, khach_id INTEGER, han_muc INTEGER);
""")
for i in range(1, 13):
    db.execute("INSERT INTO khach VALUES (?, ?)", (i, f"K{i}"))
    for j in range(1, 4):
        db.execute("INSERT INTO the VALUES (?, ?, ?)", (i * 10 + j, i, 2000000 * j))
db.commit()

dem = 0
def dem_sql(cau):
    global dem
    dem += 1

db.set_trace_callback(dem_sql)

# Cach 1: 1 cau lay khach, roi moi khach 1 cau lay the
tong = 0
for (kid,) in db.execute("SELECT id FROM khach").fetchall():
    tong += len(db.execute("SELECT id FROM the WHERE khach_id = ?", (kid,)).fetchall())
print(f"Cach 1: {dem} cau, tong so the {tong}")

# Cach 2: mot cau noi hai bang
dem = 0
dong = db.execute("SELECT k.id, t.id FROM khach k JOIN the t ON t.khach_id = k.id").fetchall()
print(f"Cach 2: {dem} cau, tong so the {len(dong)}")
'''
LAB_OUT = "Cach 1: 13 cau, tong so the 36\nCach 2: 1 cau, tong so the 36"

LAB_DE = """# Lab BNX L24 — Đếm câu SQL: một cộng N so với nối bảng

Cơ sở dữ liệu nhỏ (sqlite, không cần cài thêm gì) có bảng `khach(id, ten)` (12 khách) và bảng `the(id, khach_id, han_muc)` (mỗi khách 3 thẻ, `khach_id` là khoá ngoại). Dựng dữ liệu bằng đoạn sau (cho sẵn, không cần viết lại):

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE khach (id INTEGER PRIMARY KEY, ten TEXT)")
db.execute("CREATE TABLE the (id INTEGER PRIMARY KEY, khach_id INTEGER, han_muc INTEGER)")
for i in range(1, 13):
    db.execute("INSERT INTO khach VALUES (?, ?)", (i, f"K{i}"))
    for j in range(1, 4):
        db.execute("INSERT INTO the VALUES (?, ?, ?)", (i * 10 + j, i, 2000000 * j))
db.commit()
```
Số liệu là số minh hoạ. Viết chương trình Python (`mau.py`) làm hai cách và **đếm số câu SQL thật** bằng `db.set_trace_callback(hàm)`
(thư viện sqlite3 gọi hàm đó mỗi lần chạy một câu). Đăng ký hàm này SAU khi đã nạp dữ liệu, để các câu tạo bảng và nạp dữ liệu không bị đếm:

1. Cách 1: một câu lấy danh sách khách, rồi với MỖI khách một câu lấy thẻ của khách đó. Cộng tổng số thẻ.
2. Cách 2: một câu `JOIN` hai bảng lấy mọi cặp (khách, thẻ).

In đúng hai dòng: `Cach 1: <số câu> cau, tong so the <n>` và `Cach 2: <số câu> cau, tong so the <n>`.
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L24 mau.py`.
"""

# ── dữ kiện dùng để kiểm (bộ kiểm ver/l24.py tính lại bằng đường khác) ──
def build():
    write_lab("BNX", "L24", LAB_DE, "py", LAB_PY, LAB_OUT)
    _ghi_java()
    hook = sc("hook", "hook", "Năm mươi khách, năm mươi mốt câu SQL", [
        st("""<p>Màn hình quản lý hiện <b>50 khách</b>, mỗi khách kèm danh sách tài khoản. Người viết mã chỉ viết một vòng lặp đọc danh sách tài khoản của từng khách.</p>
<div class="box key">Máy chạy thật cho ra <b>51 câu SQL</b> chứ không phải một. Với 500 khách là <b>501</b> câu; với 10 000 khách là <b>10 001</b> câu.
Câu SQL nào sinh ra từ dòng nào của mã, và sửa bằng cách nào?</div>""",
           """Chào bạn, màn hình quản lý hiện năm mươi khách, mỗi khách kèm danh sách tài khoản, và mã chỉ viết một vòng lặp đọc danh sách ấy. Máy chạy thật cho ra năm mươi mốt câu SQL chứ không phải một câu. Với năm trăm khách là năm trăm lẻ một câu. Sửa bằng cách nào?""", focus=[1, 2, 2, 2]),
    ], checks=["alg.bnx_l24_lazy_sql(50) == 51", "alg.bnx_l24_lazy_sql(500) == 501", "alg.bnx_l24_lazy_sql(10000) == 10001"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① bảng, dòng, khoá ngoại", "<b>khoá ngoại</b>: cột ghi mã dòng của bảng khác", "cột <code>khach_id</code> ghi mã khách sở hữu tài khoản"],
                  ["② câu SQL và một lần gọi cơ sở dữ liệu", "mỗi câu gửi qua mạng tới máy chủ, có độ trễ riêng", "1 ms mỗi câu (số minh hoạ): 51 câu tốn 51 ms"],
                  ["③ giao dịch", "nhóm thao tác ghi: <b>chốt</b> thì cùng có hiệu lực, <b>hoàn tác</b> thì không cái nào", "chuyển tiền: trừ, rồi cộng"],
                  ["④ nhãn (annotation)", "dấu <code>@…</code> đặt trên lớp hoặc trường để dặn thư viện", "<code>@Entity</code>: lớp này ứng với một bảng"],
                  ["⑤ ánh xạ đối tượng và bảng", "thư viện đổi qua lại giữa đối tượng Java và dòng của bảng", "Hibernate là một thư viện như thế; JPA là bộ quy ước chung"]]),
           """Trước hết ta cần hiểu năm điều. Khoá ngoại là cột ghi mã của dòng ở bảng khác. Mỗi câu SQL đi qua mạng và có độ trễ riêng. Giao dịch là nhóm thao tác ghi, chốt thì cùng có hiệu lực, hoàn tác thì không cái nào có. Nhãn dặn thư viện ánh xạ đối tượng Java với dòng của bảng.""",
           focus=[0, "1.2", "1.3", "1.4", ["1.5", "1.6"]]),
    ], checks=["alg.bnx_l24_latency_ms(51, 1) == 51", "alg.bnx_l24_latency_ms(1, 1) == 1"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>@Entity</code>", "<b>thực thể</b>: lớp Java tương ứng một bảng; mỗi đối tượng là một dòng"],
                  ["<code>@Id</code>", "trường là <b>khoá chính</b> của dòng"],
                  ["<code>@OneToMany</code> / <code>@ManyToOne</code>", "một khách có nhiều tài khoản / nhiều tài khoản thuộc một khách; <code>mappedBy</code> chỉ phía giữ khoá ngoại"],
                  ["<code>Session</code>", "<b>phiên</b>: một lần làm việc với cơ sở dữ liệu; bên trong có <b>ngữ cảnh bền vững</b> giữ các đối tượng đã tải"],
                  ["<code>LAZY</code> / <code>EAGER</code>", "<b>tải lười</b>: chờ tới khi đụng mới lấy / <b>tải ngay</b> cùng lúc với đối tượng chủ"],
                  ["JPQL", "ngôn ngữ truy vấn <b>theo đối tượng</b>: <code>select k from Khach k</code> hỏi về lớp và trường, không hỏi về bảng và cột"],
                  ["<code>join fetch</code>", "dặn: nối bảng và <b>tải kèm</b> danh sách trong cùng một câu SQL"]]),
           """Bảng này giải mã các tên trên màn hình. Nhãn thực thể báo lớp Java ứng với một bảng, nhãn mã định danh đánh dấu khoá chính, hai nhãn quan hệ nói một khách có nhiều tài khoản. Phiên chứa ngữ cảnh bền vững giữ các đối tượng đã tải. Tải lười là chờ tới khi đụng mới lấy, tải ngay là lấy cùng lúc.""",
           focus=[["1.2", "1.3"], ["1.3", "1.4"], "1.5", "1.6", ["1.7", "1.8"]]),
        st(table(["viết trong mã", "đọc là", "ví dụ nhỏ"],
                 [["<code>List&lt;TaiKhoan&gt; tk</code>", "danh sách mà mỗi phần tử là một <code>TaiKhoan</code>", "<code>tk.size()</code> cho số tài khoản"],
                  ["<code>try (Session s = sf.openSession()) { … }</code>", "mở một phiên tên <code>s</code>, và <b>tự đóng</b> khi chạy ra khỏi khối ngoặc nhọn", "như phòng có cửa tự đóng khi bạn bước ra"],
                  ["<code>for (Khach k : ds)</code>", "với mỗi khách <code>k</code> trong danh sách <code>ds</code>, chạy khối bên dưới một lần", "3 khách thì chạy 3 lần"],
                  ["<code>:n</code> và <code>.setParameter(\"n\", n)</code>", "<code>:n</code> là chỗ trống có tên trong câu truy vấn; <code>setParameter</code> điền giá trị vào chỗ trống", "<code>where k.id &lt;= :n</code> với n = 5 là &laquo;mã từ 1 tới 5&raquo;"],
                  ["<code>interface KhachRepo extends CrudRepository&lt;Khach, Long&gt;</code>", "<b>giao diện</b> chỉ liệt kê tên hàm; <code>extends</code> là thừa hưởng hàm có sẵn; hai kiểu trong <code>&lt; &gt;</code> là thực thể và kiểu khoá chính", "<code>Long</code>: kiểu của <code>@Id</code> trong <code>Khach</code>"]]),
           """Mã Java sắp tới có vài cách viết cần đọc trước. Khối mở phiên tự đóng phiên khi chạy ra khỏi ngoặc, vòng lặp chạy một lần cho mỗi khách, và dấu hai chấm cùng tên là chỗ trống trong câu truy vấn. Giao diện chỉ liệt kê tên hàm.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"], clear=True),
    ], checks=["alg.bnx_l24_lazy_sql(1) == 2"])

    def box_(x, y, w, h, t, col, size=22, bold=False):
        return box(x, y, w, h, t, col, size, bold)

    intu = sc("intuition", "intuition", "Hình dung: ngữ cảnh bền vững và bốn trạng thái", [
        st(svg(1500, 520,
               txt(750, 40, "Một phiên giữ các đối tượng đã tải; sửa đối tượng trong phiên thì khi chốt tự có UPDATE", 26, "middle", "#1f2937", True),
               panel(480, 70, 540, 300, "ngữ cảnh bền vững (trong một phiên)", C_BLUE, 24),
               box_(520, 140, 220, 70, ["đối tượng TaiKhoan 11", "soDu 1000 → 1500"], C_AMBER, 20),
               box_(760, 140, 220, 70, ["đối tượng TaiKhoan 12", "soDu 2000"], C_GREEN, 20),
               box_(520, 250, 460, 60, "bản chụp lúc tải: 11 → 1000, 12 → 2000", C_GRAY, 20),
               box_(60, 140, 260, 90, ["đối tượng mới", "(tạm thời)"], C_GRAY, 22),
               box_(1180, 140, 260, 90, ["bảng trong cơ sở", "dữ liệu"], C_PURPLE, 22, True),
               arrow(325, 185, 475, 185, "#475569", "persist", 20),
               arrow(1020, 160, 1175, 160, "#d97706", "UPDATE", 20),
               arrow(1175, 215, 1020, 215, "#475569", "find: SELECT", 20),
               box_(60, 400, 330, 70, ["rời ngữ cảnh (detach)", "sửa không còn được theo dõi"], C_RED, 20),
               box_(440, 400, 330, 70, ["so bản chụp với đối tượng", "khác → kiểm bẩn → UPDATE"], C_AMBER, 20),
               box_(820, 400, 330, 70, ["xoá (remove)", "DELETE khi chốt"], C_GRAY, 20),
               txt(750, 505, "bốn trạng thái: tạm thời, được quản lý, đã rời, đã xoá", 24, "middle", "#1f2937", True)),
           """Hình này cho thấy ngữ cảnh bền vững và bốn trạng thái của một đối tượng. Đối tượng mới còn tạm thời, khi lưu thì thành đối tượng được quản lý. Ngữ cảnh giữ bản chụp lúc tải, khi chốt đối tượng nào khác bản chụp thì sinh lệnh cập nhật."""),
        st(svg(1500, 560,
               txt(750, 40, "Cùng một việc, hai cách lấy: 1 + N câu SQL hay 1 câu nối bảng", 26, "middle", "#1f2937", True),
               txt(380, 90, "tải lười", 26, "middle", "#dc2626", True),
               box_(40, 110, 680, 60, "① select khach  → 3 khách: K1, K2, K3", C_AMBER, 22),
               box_(40, 190, 680, 60, "② select tk where khach_id = 1  (đụng vào K1)", C_RED, 22),
               box_(40, 270, 680, 60, "③ select tk where khach_id = 2  (đụng vào K2)", C_RED, 22),
               box_(40, 350, 680, 60, "④ select tk where khach_id = 3  (đụng vào K3)", C_RED, 22),
               txt(380, 460, "1 + N = 1 + 3 = 4 câu; với N = 500 là 501 câu", 24, "middle", "#dc2626", True),
               txt(1120, 90, "nối kèm tải (join fetch)", 26, "middle", "#16a34a", True),
               box_(780, 110, 680, 120, ["① select khach join tk", "trả cả 6 dòng: mỗi khách kèm tài khoản"], C_GREEN, 22),
               box_(780, 270, 680, 140, ["bộ ánh xạ ghép 6 dòng thành 3 khách,", "mỗi khách có danh sách tài khoản đầy đủ", "đụng vào danh sách: không thêm câu nào"], C_GREEN, 22),
               txt(1120, 460, "luôn 1 câu, nhưng mỗi câu trả về nhiều dòng hơn", 24, "middle", "#16a34a", True),
               txt(750, 530, "Đánh đổi: bớt số lần đi tới cơ sở dữ liệu, đổi lại mỗi lần trả nhiều dữ liệu hơn", 24, "middle", "#1f2937", True)),
           """Hình thứ hai đặt hai cách lấy dữ liệu cạnh nhau, với ba khách để dễ đếm. Bên trái là tải lười: một câu lấy ba khách, rồi mỗi lần đụng vào danh sách lại thêm một câu, tổng một cộng N là bốn câu. Bên phải là nối kèm tải: một câu nối hai bảng trả sáu dòng, nên đụng vào danh sách không thêm câu nào."""),
    ], checks=["alg.bnx_l24_lazy_sql(3) == 4", "alg.bnx_l24_rows_join(3, 2) == 6", "alg.bnx_l24_lazy_sql(500) == 501"])

    form = sc("formula", "formula", "Suy ra từng bước: từ một thực thể tới số câu SQL", [
        jstep([(("<code>public class Khach { … }</code>", "khai một lớp tên Khach; phần thân nằm giữa cặp ngoặc nhọn", "Khai một lớp có tên, phần thân nằm giữa cặp ngoặc nhọn."), "", ""),
               (("<code>@Id Long id;</code>, <code>String ten;</code>", "khai trường: kiểu rồi tên; <code>Long</code>: số nguyên lớn; <code>String</code>: chuỗi chữ; nhãn <code>@Id</code> đứng trước: khoá chính", "Khai trường là viết kiểu rồi tên, và nhãn đứng trước cho biết trường là khoá chính."), "", ""),
               (("<code>List&lt;TaiKhoan&gt; tk = new ArrayList&lt;&gt;();</code>", "khai danh sách <code>tk</code> các <code>TaiKhoan</code> và gán ngay một danh sách rỗng mới tạo (<code>new</code>); <code>&lt;&gt;</code> để trống thì lấy kiểu ở vế trái", "Câu này khai một danh sách tài khoản và gán ngay một danh sách rỗng mới tạo."), "", "")],
              intro="Trước khi đọc mã Java, ta cần ba ký hiệu, vì mã dùng chúng ngay."),
        st("""<p><b>Bước 1.</b> Ta muốn mỗi đối tượng Java ứng với một dòng, nên khai <b>thực thể</b>: lớp có nhãn <code>@Entity</code>, một trường khoá chính <code>@Id</code>.
Quan hệ một–nhiều khai ở cả hai phía, và phía có khoá ngoại là phía &laquo;nhiều&raquo;.</p>"""
           + J_KHACH.show(lines=(3, 9), title="Khach.java: khách có danh sách tài khoản"),
           """Bước một, vì muốn mỗi đối tượng ứng với một dòng, ta khai thực thể bằng nhãn trên lớp và một trường khoá chính. Khách có danh sách tài khoản, còn tài khoản giữ khoá ngoại.""",
           focus=[1, 2], clear=True),
        st(J_TK.show(lines=(2, 8), title="TaiKhoan.java: tài khoản thuộc về một khách, tải lười")
           + """<p>Làm thử: 1 khách, 2 tài khoản thì bảng tài khoản có 2 dòng, cùng ghi <code>khach_id = 1</code>.</p>""",
           """Tài khoản khai thuộc về một khách và dặn tải lười, nghĩa là chưa lấy khách vội. Làm thử: một khách, hai tài khoản thì hai dòng cùng ghi mã khách là một.""",
           clear=True),
        st("""<p><b>Bước 2.</b> Muốn thao tác với dòng, ta cần một nơi giữ các đối tượng đang dùng, để không tải trùng và để biết cái nào đã bị sửa. Nơi đó là <b>ngữ cảnh bền vững</b> trong một <b>phiên</b>.
Hai lần tìm cùng một mã trong một phiên cho <b>cùng một đối tượng</b>, và chỉ chạy <b>1</b> câu SQL.</p>"""
           + J_BAN.show(lines=(9, 10), title="DemBan.java (trích)")
           + """<p>Làm thử: hai lệnh tìm, chỉ một SELECT, vì lệnh thứ hai thấy đối tượng đã có trong ngữ cảnh.</p>""",
           """Bước hai, vì cần không tải trùng và biết cái nào đã bị sửa, ta giữ các đối tượng đang dùng trong ngữ cảnh bền vững của một phiên. Hai lần tìm cùng một mã cho cùng một đối tượng và chỉ một câu SQL.""",
           clear=True),
        st("""<p><b>Bước 3.</b> Một khách có thể có hàng trăm tài khoản, và phần lớn màn hình không cần chúng. Nên danh sách quan hệ <b>mặc định tải lười</b>: chỉ lấy khi mã <b>đụng tới</b> (<code>k.tk.size()</code>).
Hậu quả: vòng lặp qua <b>N</b> khách, mỗi khách đụng một lần, sinh <b>N</b> câu phụ cộng <b>1</b> câu lấy danh sách khách.</p>
$$\\text{số câu SQL} = 1 + N \\qquad (N = 3 \\Rightarrow 4;\\; N = 50 \\Rightarrow \\hl{51})$$""",
           """Bước ba, danh sách quan hệ mặc định tải lười, chỉ lấy khi mã đụng tới, vì một khách có thể có hàng trăm tài khoản. Vòng lặp qua N khách sinh N câu phụ cộng một câu lấy danh sách khách, nên số câu SQL bằng một cộng N.""",
           clear=True),
        st("""<p><b>Bước 4.</b> Muốn bỏ N câu phụ, ta dặn lấy danh sách <b>cùng lúc</b> trong câu truy vấn theo đối tượng, bằng <code>join fetch</code>. Câu SQL sinh ra là một phép nối, trả về <b>số dòng = số khách × số tài khoản mỗi khách</b> (khi khách nào cũng có tài khoản).</p>"""
           + code(JQL_FETCH, "câu truy vấn theo đối tượng")
           + """$$\\text{số câu SQL} = \\hl{1}; \\qquad \\text{số dòng trả về} = N \\times 2 \\;\\; (N = 3 \\Rightarrow 6)$$
<p class="note"><b>Điều kiện:</b> <code>join fetch</code> là nối trong, nên khách chưa có tài khoản nào biến mất khỏi kết quả. Muốn giữ họ, viết <code>left join fetch</code> (nối trái).</p>""",
           """Bước bốn, dặn lấy danh sách cùng lúc bằng phép nối kèm tải, nên chỉ còn một câu SQL. Đổi lại số dòng bằng số khách nhân số tài khoản mỗi khách, ba khách hai tài khoản là sáu dòng.""",
           clear=True),
        st("""<p><b>Bước 5.</b> Khi ta sửa đối tượng đang được quản lý, ta <b>không gọi hàm lưu nào</b>. Lúc cần, bộ ánh xạ <b>kiểm bẩn</b>: so đối tượng với bản chụp lúc tải; khác thì sinh <code>UPDATE</code>.
Việc ghi các thay đổi xuống cơ sở dữ liệu gọi là <b>đẩy xuống</b> (flush). Mặc định đẩy khi chốt giao dịch, và cả <b>ngay trước một truy vấn có thể bị ảnh hưởng</b>, để truy vấn thấy dữ liệu mới.</p>"""
           + J_BAN.show(lines=(14, 16), title="DemBan.java (trích): sửa, rồi truy vấn cùng bảng"),
           """Bước năm, sửa đối tượng đang được quản lý thì không gọi hàm lưu nào, vì bộ ánh xạ tự kiểm bẩn: so đối tượng với bản chụp lúc tải, khác thì sinh lệnh cập nhật. Việc ghi xuống gọi là đẩy xuống, xảy ra khi chốt hoặc trước truy vấn kế tiếp.""",
           clear=True),
        st("""<p><b>Bước 6.</b> Kho truy cập dữ liệu của Spring (Spring Data) viết gọn các việc trên: ta khai một <b>giao diện</b>, Spring tạo phần cài đặt.
Theo hướng dẫn chính thức, giao diện cơ sở <code>CrudRepository</code> có sẵn lưu, tìm theo mã, đếm, xoá; và <b>tên hàm</b> như <code>findByTen</code>, <code>countByTen</code> được đọc để <b>sinh truy vấn</b>.</p>"""
           + code(JAVA_REPO, "KhachRepo: giao diện, không có thân hàm (ghép từ ví dụ của hướng dẫn, không chạy trên máy này)")
           + """<p>Làm thử: <code>countByTen("K7")</code> hỏi &laquo;có bao nhiêu khách tên K7&raquo;, không cần viết câu truy vấn nào.</p>""",
           """Bước sáu, kho truy cập dữ liệu của Spring viết gọn các việc trên: ta khai một giao diện, Spring tạo phần cài đặt. Theo hướng dẫn chính thức, tên hàm được đọc để sinh truy vấn, như hàm đếm theo tên.""",
           clear=True),
    ], checks=["alg.bnx_l24_lazy_sql(3) == 4 and alg.bnx_l24_lazy_sql(50) == 51", "alg.bnx_l24_rows_join(3, 2) == 6",
               "alg.bnx_l24_find_sql(2) == 1", "alg.bnx_l24_khach_thay(501, 1, 'trong') == 500 and alg.bnx_l24_khach_thay(501, 1, 'trai') == 501"])

    ex = sc("example", "example", "Ví dụ chạy thật Hibernate, từng phép tính", [
        jstep([(("<code>static SessionFactory mo(int n)</code>", "khai hàm: kiểu trả về <code>SessionFactory</code>, tên <code>mo</code>, tham số n kiểu số nguyên; <code>static</code>: thuộc cả lớp", "Khai hàm gồm kiểu trả về, tên hàm, rồi tham số trong ngoặc tròn."), "", ""),
               (("<code>new Configuration().addAnnotatedClass(Khach.class)</code>", "tạo mới một đối tượng cấu hình; mỗi <code>.hàm(…)</code> chỉnh nó rồi trả lại chính nó nên viết nối nhau; <code>Khach.class</code>: chính lớp Khach; <code>.setProperty(\"khoá\", \"giá trị\")</code>: đặt một thiết lập", "Tạo mới một đối tượng cấu hình, rồi gọi nối tiếp các hàm, mỗi hàm chỉnh nó và trả lại chính nó."), "", "")],
              intro="Ta cần hai ký hiệu này trước khi đọc mã dựng."),
        st(J_KHO.show(lines=(4, 11), title="Kho.java (đoạn đầu; mã đủ ở tệp kèm labs/BNX/L24/java/Kho.java): dựng bộ ánh xạ nối với H2, cơ sở dữ liệu nhỏ trong bộ nhớ"),
           """Ta chạy thật bộ ánh xạ bản bảy chấm một, nối với H2, một cơ sở dữ liệu nhỏ chạy ngay trong bộ nhớ. Đoạn này khai hai thực thể, địa chỉ cơ sở dữ liệu, và dặn tự tạo bảng. Dòng thống kê bật bộ đếm số câu SQL thật.""",
           focus=[0, ["2.2", "2.3", "2.4", "2.5"], "2.7"], clear=True, introduces=["bnx_h2"]),
        jstep([(("<code>public static void main(String[] x)</code>", "nơi chương trình bắt đầu chạy; <code>String[] x</code>: mảng chuỗi gõ kèm, bài không dùng", "Hàm chính là nơi chương trình bắt đầu chạy."), "", ""),
               (("<code>for (Khach k : …getResultList())</code>", "duyệt từng phần tử: mỗi vòng <code>k</code> là một khách trong kết quả", "Vòng lặp duyệt từng khách trong kết quả truy vấn."), "", "")],
              intro="Ta cần hai ký hiệu Java này trước khi đọc tệp chạy."),
        st(J_SQL.show(title="DemSql.java (đủ tệp): in từng câu SQL thật"),
           """Phép tính thứ nhất, in từng câu SQL thật với hai khách: mỗi lần đụng vào danh sách là một lần đi tới cơ sở dữ liệu.""",
           clear=True),
        st(J_SQL.out_html("""Hibernate: select k1_0.id,k1_0.ten from Khach k1_0
Hibernate: select t1_0.khach_id,t1_0.id,t1_0.soDu from TaiKhoan t1_0 …
K1: 2 tai khoan
Hibernate: select t1_0.khach_id,t1_0.id,t1_0.soDu from TaiKhoan t1_0 …
K2: 2 tai khoan""", "Kết quả chạy thật (lược bằng dấu …)")
           + """$$① \\; 2 \\text{ khách} \\Rightarrow 1 + 2 = \\hl{3} \\text{ câu SQL}$$""",
           """Câu đầu lấy hai khách, rồi mỗi lần đụng vào danh sách lại chạy thêm một câu, nên hai khách tốn ba câu SQL.""", clear=True),
        st(J_N1.show(lines=(1, 6), title="DemN1.java (1/3): hai câu truy vấn viết thành hằng")
           + "<p class='note'><code>static final String LUOI = \"…\";</code>: hằng chuỗi dùng chung cho cả lớp, gán một lần rồi không đổi.</p>",
           """Tệp thứ hai chạy cả hai cách. Phần đầu khai hai câu truy vấn thành hằng, một cho tải lười và một cho nối kèm tải.""",
           clear=True),
        st(J_N1.show(lines=(7, 16), title="DemN1.java (2/3): chạy truy vấn, đụng vào danh sách, đọc bộ đếm"),
           """Phép tính thứ hai đếm bằng bộ đếm thật: hàm chạy truy vấn, đụng vào danh sách từng khách, rồi trả số câu SQL ghi nhận.""",
           clear=True),
        jstep([(("<code>for (long n : new long[] {5, 50, 500})</code>", "duyệt từng phần tử: n lần lượt là 5, 50, 500; <code>new long[] {…}</code> tạo mảng số nguyên lớn với các giá trị liệt kê", "Vòng lặp duyệt từng phần tử của một mảng mới tạo, nên n lần lượt là năm, năm mươi, năm trăm."), "", "")]),
        st(J_N1.show(lines=(17, 23), title="DemN1.java (3/3): nạp 500 khách rồi đo ở 5, 50 và 500 khách")
           + J_N1.out_html("""5 khach: tai luoi 6 cau, JOIN FETCH 1 cau
50 khach: tai luoi 51 cau, JOIN FETCH 1 cau
500 khach: tai luoi 501 cau, JOIN FETCH 1 cau""")
           + """$$② \\; N = 5, 50, 500 \\Rightarrow 1 + N = 6,\\; 51,\\; 501; \\qquad \\text{nối kèm tải: } \\hlg{1}$$""",
           """Ta gọi hàm hai lần, một lần tải lười, một lần nối kèm tải. Với năm, năm mươi, năm trăm khách, tải lười cần sáu, năm mươi mốt, năm trăm lẻ một câu, còn nối kèm tải luôn một câu.""",
           clear=True),
        jstep([(("<code>s.find(TaiKhoan.class, 11L)</code>", "tìm trong phiên theo khoá chính: lớp rồi mã; <code>11L</code>: số 11 kiểu long", "Hàm tìm nhận lớp rồi mã khoá chính, và chữ cái đứng sau số cho biết số kiểu nguyên lớn."), "", ""),
               (("<code>a == b</code>", "<code>true</code> khi a và b cùng trỏ một đối tượng trong bộ nhớ", "Hai dấu bằng giữa hai đối tượng hỏi chúng có phải cùng một đối tượng không."), "", ""),
               (("<code>Transaction t = s.beginTransaction(); … t.commit();</code>", "mở giao dịch, làm việc, rồi chốt: thay đổi chỉ có hiệu lực khi chốt", "Mở giao dịch, làm việc, rồi chốt; thay đổi chỉ có hiệu lực khi chốt."), "", "")]),
        st(J_BAN.show(lines=(7, 18), title="DemBan.java (đoạn): đọc hai lần, sửa, rồi truy vấn trước khi chốt; mã đủ ở tệp kèm"),
           """Phép tính thứ ba: tìm tài khoản mười một hai lần, sửa số dư mà không gọi hàm lưu, rồi chạy truy vấn đếm trước khi chốt.""",
           clear=True),
        st(J_BAN.out_html("""doc hai lan: cung doi tuong true, 1 cau SQL
sau truy van, truoc chot: 1 UPDATE""")
           + """$$③ \\; \\text{hai lần tìm} \\Rightarrow \\hl{1} \\text{ câu SELECT}; \\qquad \\text{sửa rồi truy vấn} \\Rightarrow \\hl{1} \\text{ UPDATE trước khi chốt}$$""",
           """Hai biến trỏ cùng một đối tượng và chỉ một câu SQL chạy, còn lệnh cập nhật đã chạy trước khi chốt vì bộ ánh xạ đẩy thay đổi xuống trước truy vấn.""",
           clear=True),
        st(J_BAN.show(lines=(21, 30), title="DemBan.java (tiếp): tải, rời ngữ cảnh, rồi sửa"),
           """Phép tính thứ tư: tải tài khoản mười hai, gỡ khỏi ngữ cảnh, rồi sửa số dư và chốt.""",
           clear=True),
        st(J_BAN.out_html("""sua doi tuong da roi: 0 UPDATE
so du 11: 1500, so du 12: 2000""")
           + """$$④ \\; \\text{đối tượng đã rời ngữ cảnh: sửa } \\Rightarrow \\hl{0} \\text{ UPDATE}; \\quad 1000 + 500 = 1500,\\; 2000 \\text{ nguyên}$$""",
           """Không có lệnh cập nhật nào vì không còn ai theo dõi đối tượng, nên số dư vẫn hai nghìn.""",
           clear=True),
        st(J_NHO.show(lines=(4, 14), title="DemNho.java: ngữ cảnh giữ bao nhiêu đối tượng?"),
           """Phép tính thứ năm: tải năm trăm khách kèm mọi tài khoản trong một phiên rồi hỏi bộ đếm ngữ cảnh giữ bao nhiêu đối tượng.""",
           clear=True),
        st(J_NHO.out_html("""ngu canh giu: 1500 doi tuong
sau clear: 0 doi tuong""")
           + """$$⑤ \\; 500 \\text{ khách} + 500 \\times 2 \\text{ tài khoản} = \\hl{1500} \\text{ đối tượng}$$""",
           """Ngữ cảnh giữ một nghìn năm trăm đối tượng, gồm năm trăm khách và một nghìn tài khoản, và sau khi xoá thì còn không.""",
           clear=True),
    ], checks=["alg.bnx_l24_lazy_sql(2) == 3", "[alg.bnx_l24_lazy_sql(n) for n in (5, 50, 500)] == [6, 51, 501]",
               "alg.bnx_l24_join_sql(500) == 1", "alg.bnx_l24_find_sql(2) == 1",
               "alg.bnx_l24_entities_held(500, 2) == 1500"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm bằng sqlite và Python", [
        jstep([(("<code>for (i,) in db.execute(\"SELECT id FROM k\").fetchall():</code>", "mỗi dòng kết quả là một bộ một phần tử; <code>(i,)</code> tách phần tử đó ra thành i", "Mỗi dòng kết quả là một bộ một phần tử, dấu phẩy tách nó ra thành một tên."), "", ""),
               (("<code>db.execute(\"INSERT INTO k VALUES (?)\", (i,))</code>", "<code>?</code> là chỗ trống trong câu SQL; bộ <code>(i,)</code> điền giá trị vào đó", "Dấu hỏi là chỗ trống trong câu SQL, bộ giá trị phía sau điền vào."), "", ""),
               (("<code>db.set_trace_callback(lambda c: n.append(c))</code>", "<code>lambda c: …</code>: hàm ngắn không tên nhận câu SQL c và thêm vào danh sách n; sqlite3 gọi nó mỗi lần chạy một câu", "Hàm ngắn không tên nhận câu SQL và thêm vào danh sách, và thư viện gọi nó mỗi lần chạy một câu."), "", "")],
              intro="Trước khi đọc mã, ta cần ba ký hiệu Python, vì mã dùng chúng ngay."),
        st(PY_CHECK.show(lines=(2, 13), title="Đếm câu SQL bằng một thư viện khác hẳn: sqlite3 của Python, không dùng Hibernate"),
           """Ta kiểm bằng đường khác hẳn, vì muốn con số không phụ thuộc bộ ánh xạ: mã Python tạo hai bảng nhỏ, năm mươi khách, mỗi khách hai tài khoản. Hàm đếm ghi nhận mỗi câu SQL chạy, còn mã lặp từng khách và hỏi tài khoản của họ.""", clear=True),
        st(PY_CHECK.out_html() + """
$$1 + 50 = \\hlg{51}$$""" + table(["cách đếm", "kết quả cho 50 khách"],
                              [["Hibernate chạy thật, bộ đếm thống kê", "51 câu"],
                               ["sqlite3 của Python, bộ đếm câu SQL", "51 câu"],
                               ["công thức 1 + N", "1 + 50 = 51"]]),
           """Kết quả chạy thật là năm mươi mốt câu, và ba đường độc lập đều cho cùng con số, nên vấn đề một cộng N đến từ cách tải lười, không phải từ một thư viện.""",
           focus=[0, 0], clear=True),
    ], checks=["alg.bnx_l24_lazy_sql(50) == 51", "1 + 50 == alg.bnx_l24_lazy_sql(50)"])

    quymo = sc("quymo", "example", "Khi dữ liệu lớn dần: số câu SQL và thời gian chờ", [
        st(table(["số khách N", "tải lười: 1 + N câu", "chờ nếu 1 ms mỗi câu (số minh hoạ)", "nối kèm tải: 1 câu", "số dòng một câu trả về (2 tài khoản mỗi khách)"],
                 [[nowrap("5 (×1)"), "6", "6 ms", "1", "10"],
                  [nowrap("500 (×100)"), "501", "501 ms", "1", "1 000"],
                  [nowrap("50 000 (×10 000)"), "50 001", "50 001 ms ≈ 50 giây", "1", "100 000"]]),
           """Bảng này cho thấy vấn đề đổi khi dữ liệu lớn dần, với số minh hoạ một mili giây mỗi câu. Năm trăm khách là năm trăm lẻ một câu. Năm mươi nghìn khách thì chờ khoảng năm mươi giây, còn nối kèm tải vẫn một câu nhưng trả một trăm nghìn dòng.""",
           focus=[0, "1.2", "1.3", "1.4"]),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["tải lười, đụng từng khách", "mỗi câu nhẹ; không tải thứ không cần", "số câu tăng thẳng theo N, độ trễ mạng nhân lên", "chỉ cần danh sách của một hai khách"],
                  ["nối kèm tải", "một lần đi tới cơ sở dữ liệu", "trả nhiều dòng, tốn bộ nhớ; nối nhiều danh sách cùng lúc làm số dòng nhân lên", "màn hình cần danh sách của mọi khách trong trang"],
                  ["<b>phân trang</b> (mỗi lần chỉ lấy một trang, ví dụ 20 khách) + nối kèm tải", "giới hạn số khách mỗi lần", "có bẫy: nối kèm một <b>danh sách</b> mà cắt trang ngay trong câu thì Hibernate đọc hết mọi dòng rồi mới cắt trong bộ nhớ; cách đúng là hai bước (lấy mã của 20 khách, rồi nối kèm tải theo các mã đó)", "danh sách dài, hiển thị theo trang"]]),
           """Bảng thứ hai cho thấy người làm nghề phải chọn gì. Tải lười mỗi câu nhẹ nhưng số câu tăng thẳng theo N. Nối kèm tải chỉ một lần đi tới cơ sở dữ liệu, đổi lại trả nhiều dòng và tốn bộ nhớ. Với danh sách dài, người ta phân trang, nhưng cắt trang cùng lúc với nối kèm một danh sách là một cái bẫy.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True, introduces=["bnx_phan_trang"]),
        st(J_TRANG.out_html("""cat tai cho (join fetch + trang): 20 khach, 1 cau, ngu canh giu 1500 doi tuong
hai buoc (lay ma roi join fetch): 20 khach, 2 cau, ngu canh giu 60 doi tuong""", "Chạy thật: 500 khách, một trang 20 khách")
           + """$$\\text{cắt trong câu}: \\hl{1500} \\text{ đối tượng; hai bước: } 20 + 20 \\times 2 = \\hlg{60}$$""",
           """Đo thật với năm trăm khách, một trang hai mươi khách: cắt trang ngay trong câu nối kèm vẫn kéo cả một nghìn năm trăm đối tượng vào bộ nhớ. Hai bước chỉ giữ sáu mươi.""",
           clear=True),
    ], checks=["[alg.bnx_l24_lazy_sql(n) for n in (5, 500, 50000)] == [6, 501, 50001]",
               "[alg.bnx_l24_latency_ms(alg.bnx_l24_lazy_sql(n), 1) for n in (5, 500, 50000)] == [6, 501, 50001]",
               "[alg.bnx_l24_rows_join(n, 2) for n in (5, 500, 50000)] == [10, 1000, 100000]",
               "500 // 5 == 50000 // 500 == 100 and 50000 // 5 == 10000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        jstep([(("<code>try { … } catch (LazyInitializationException e) { … }</code>", "thử chạy khối <code>try</code>; gặp lỗi loại ghi trong ngoặc tròn thì nhảy sang khối <code>catch</code>, lỗi gán vào tên <code>e</code>", "Khối thử chạy trước, gặp lỗi loại đã nêu thì nhảy sang khối bắt lỗi."), "", ""),
               (("<code>e.getClass().getSimpleName()</code>", "tên ngắn của loại lỗi, bỏ phần tên gói đứng trước", "Chuỗi này cho tên ngắn của loại lỗi, bỏ phần tên gói đứng trước."), "", "")]),
        st(J_LOI.show(lines=(3, 13), title="DemLoi.java: đọc danh sách lười sau khi phiên đã đóng") + J_LOI.out_html("loi: LazyInitializationException", "Kết quả chạy thật: một ngoại lệ, tức thông báo lỗi chương trình ném ra khi không làm tiếp được"),
           """Lỗi thứ nhất lộ ra lúc mới dựng: mã tải một khách trong một phiên, phiên đóng, rồi mới đụng vào danh sách tài khoản. Kết quả chạy thật là một ngoại lệ, tức thông báo lỗi mà chương trình ném ra khi không làm tiếp được, vì không còn phiên để chạy câu SQL phụ.""", clear=True, introduces=["bnx_ngoai_le"]),
        st("""<div class="box warn"><b>Lỗi 1 (người đã đi làm, lúc mới dựng).</b> Gặp ngoại lệ trên rồi <b class="red">giữ phiên mở suốt yêu cầu, hoặc đẩy mọi thứ thành tải ngay</b>.
Cách sửa đúng: <b>quyết định ở nơi viết truy vấn</b> xem màn hình cần gì, và nối kèm tải đúng phần ấy, để dữ liệu đủ trước khi phiên đóng.</div>""",
           """Người đã đi làm gặp ngoại lệ này thường giữ phiên mở suốt yêu cầu, hoặc chuyển mọi quan hệ sang tải ngay, đều là chữa triệu chứng. Cách đúng là nối kèm tải đúng phần màn hình cần, ngay ở chỗ viết truy vấn.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc tải tăng).</b> Cho là <b class="red">một cộng N chỉ là chuyện chậm vài mili giây</b>. Ở 500 khách là 501 câu, ở 50 000 khách là 50 001 câu:
một yêu cầu <b>giữ một kết nối</b> từ <b>bể kết nối</b> (nhóm kết nối mở sẵn tới cơ sở dữ liệu, dùng chung, số lượng có hạn) suốt thời gian chạy hết 501 câu nối tiếp (trong một giao dịch vẫn chỉ một kết nối, nhưng giữ lâu), nên nhiều người dùng cùng lúc <b>làm cạn bể</b> trước cả khi cơ sở dữ liệu quá tải.
<br><span class="note">Cách phòng: đếm số câu SQL trong ca kiểm thử của màn hình quan trọng và đặt trần.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là cho rằng một cộng N chỉ là chuyện chậm vài mili giây. Một yêu cầu giữ một kết nối của bể kết nối, tức nhóm kết nối mở sẵn dùng chung, suốt thời gian chạy hết các câu, nên nhiều người cùng lúc làm cạn bể.""", clear=True, introduces=["bnx_be_ket_noi"]),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Một phiên chạy lâu, ví dụ xử lý một tệp lô lớn, <b class="red">tải hàng trăm nghìn đối tượng vào cùng một ngữ cảnh</b>.
Ngữ cảnh giữ MỌI đối tượng đã tải (bài vừa đo: 1500 đối tượng cho 500 khách), nên bộ nhớ phình dần và mỗi lần kiểm bẩn phải so ngày càng nhiều.
<br><span class="note">Cách chữa: xử lý theo lô nhỏ, sau mỗi lô đẩy xuống rồi <code>clear()</code> ngữ cảnh.</span></div>""",
           """Lỗi thứ ba, lộ ra khi vận hành lâu: một phiên xử lý tệp lô lớn tải hàng trăm nghìn đối tượng vào cùng một ngữ cảnh, nên bộ nhớ phình dần. Cách chữa là xử lý theo lô nhỏ, sau mỗi lô đẩy xuống rồi xoá ngữ cảnh.""", clear=True),
    ], checks=["alg.bnx_l24_lazy_sql(500) == 501 and alg.bnx_l24_lazy_sql(50000) == 50001", "alg.bnx_l24_entities_held(500, 2) == 1500"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Trang quản lý hiện 200 khách, mỗi khách đụng vào danh sách tài khoản. Tải lười cần bao nhiêu câu SQL? Nối kèm tải cần bao nhiêu câu? Nếu mỗi khách có 3 tài khoản thì câu nối trả về bao nhiêu dòng?"],
                  ["2", "Mã tải một tài khoản trong phiên, đổi số dư, rồi gọi <code>detach</code> trước khi chốt. Số dư trong bảng có đổi không? Nếu đổi số dư rồi <b>mới</b> detach, kết quả khác không?"],
                  ["3", "Quyết định (số minh hoạ): màn hình quản trị phân trang 20 khách mỗi trang, nhưng một báo cáo đêm đọc 200 000 khách kèm tài khoản. Chọn cho từng việc: tải lười, nối kèm tải, hay nối kèm tải theo lô rồi xoá ngữ cảnh? Giải thích."]]),
           """Đến lượt bạn, ba câu để làm ra giấy. Câu một, hai trăm khách đụng vào danh sách tài khoản, tải lười và nối kèm tải cần bao nhiêu câu SQL? Câu hai, đổi số dư rồi gỡ đối tượng khỏi ngữ cảnh trước khi chốt, số dư trong bảng có đổi không? Câu ba, trang quản trị hai mươi khách còn báo cáo đêm hai trăm nghìn khách, chọn cách nào cho từng việc? Hãy tạm dừng và làm ra giấy.""",
           focus=[0, "1.2", "1.2", "1.3", "1.4", 0], pause=30),
        st("""<p>Câu 1: tải lười một cộng N, nối kèm tải luôn một câu; số dòng = số khách × số tài khoản mỗi khách.</p>
$$1 + 200 = \\hlg{201}; \\qquad 1; \\qquad 200 \\times 3 = \\hlg{600} \\text{ dòng}$$""",
           """Đáp án câu một: tải lười cần một cộng hai trăm, tức hai trăm lẻ một câu, nối kèm tải luôn một câu, và số dòng bằng hai trăm nhân ba, tức sáu trăm dòng."""),
        st("""<p>Câu 2: theo kết quả chạy thật, đối tượng đã rời ngữ cảnh thì sửa không sinh UPDATE. Phải xét <b>thứ tự</b>.</p>
$$\\text{detach rồi mới sửa} \\Rightarrow \\hlg{0} \\text{ UPDATE (số dư giữ nguyên)}$$
<p>Còn sửa trong ngữ cảnh rồi detach <b>trước</b> khi bộ ánh xạ kịp đẩy xuống: thay đổi cũng không được ghi, vì lúc chốt đối tượng không còn được theo dõi. Chỉ khi đã đẩy xuống (flush) trước lúc detach thì lệnh UPDATE mới đã chạy.</p>""",
           """Đáp án câu hai: gỡ đối tượng rồi mới sửa thì không sinh lệnh cập nhật, số dư giữ nguyên. Sửa trước rồi gỡ mà chưa đẩy xuống thì cũng không được ghi, vì lúc chốt đối tượng không còn được theo dõi."""),
        st(table(["việc", "chọn", "vì sao"],
                 [["trang quản trị, 20 khách mỗi trang", "hai bước: lấy mã của 20 khách, rồi nối kèm tải theo các mã đó", "cắt trang ngay trong câu nối kèm thì đọc hết rồi cắt trong bộ nhớ (đã đo: 1500 đối tượng, so với 60)"],
                  ["báo cáo đêm, 200 000 khách", "nối kèm tải theo lô, mỗi lô xong thì xoá ngữ cảnh", "tải lười thành 200 001 câu; nối một lần giữ cả 600 000 đối tượng nếu 2 tài khoản mỗi khách trong bộ nhớ"],
                  ["lệnh kiểm tra một khách", "tải lười", "chỉ cần một khách; không tải thứ không dùng"]]),
           """Đáp án câu ba: trang quản trị lấy mã của hai mươi khách rồi nối kèm tải theo mã, vì cắt trang ngay trong câu nối kèm là đọc hết rồi cắt trong bộ nhớ. Báo cáo đêm thì tải lười thành hơn hai trăm nghìn câu, nên chọn nối kèm tải theo lô và xoá ngữ cảnh sau mỗi lô. Xem một khách thì tải lười là hợp lý.""",
           focus=["1.2", "1.3", "1.3", "1.4"]),
    ], checks=["alg.bnx_l24_lazy_sql(200) == 201", "alg.bnx_l24_rows_join(200, 3) == 600", "alg.bnx_l24_entities_held(200000, 2) == 600000"])

    lab_pr = practice_scene(sc, "Tự làm: đếm câu SQL của hai cách đọc", practice_steps(
        st, "BNX", "L24",
        """<p><b>Đề</b>: sqlite có bảng <code>khach</code> (12 khách) và <code>the</code> (mỗi khách 3 thẻ, khoá ngoại <code>khach_id</code>). Viết <code>mau.py</code>:</p>
<ol><li><b>Cách 1</b>: một câu lấy khách, rồi mỗi khách một câu lấy thẻ</li><li><b>Cách 2</b>: một câu <code>JOIN</code> hai bảng</li></ol>
<p>Đếm câu SQL thật bằng <code>db.set_trace_callback(hàm)</code>. In hai dòng <code>Cach 1: … cau, tong so the …</code> và <code>Cach 2: …</code>.</p>
<p class="note">Dữ liệu và khung tạo bảng nằm trong <code>de.md</code> và lời giải; tự viết phần đếm, đừng chép lại ví dụ DemN1.</p>""",
        """Bây giờ tới phần bạn tự làm: cơ sở dữ liệu nhỏ có mười hai khách, mỗi khách ba thẻ. Viết chương trình Python làm hai cách đọc, một là lấy khách rồi hỏi thẻ từng khách, hai là nối hai bảng trong một câu. Đếm câu SQL thật bằng hàm theo dõi, rồi hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> đặt biến đếm bằng 0, hàm theo dõi tăng nó một đơn vị mỗi lần gọi. Trước cách 2 nhớ đặt biến đếm về 0.
Lời giải đầy đủ ở <code>labs/BNX/L24/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, đặt biến đếm bằng không và cho hàm theo dõi tăng nó một mỗi lần gọi, nhớ đặt lại về không trước cách hai. Lời giải chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L24")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("thực thể = dòng", "ngữ cảnh bền vững giữ đối tượng", "tải lười → một cộng N", "nối kèm tải → một câu", "kiểm bẩn → UPDATE khi chốt"),
           """Tổng kết: thực thể là một dòng của bảng, ngữ cảnh bền vững giữ các đối tượng đang dùng. Tải lười sinh một cộng N câu, nối kèm tải chỉ một câu nhưng trả nhiều dòng hơn. Đối tượng được quản lý bị sửa thì được kiểm bẩn và ghi khi chốt."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng đoán số câu SQL, hãy <b>đếm</b>. Mỗi vòng lặp chạm vào quan hệ lười là một ứng viên cho một cộng N.
Chọn tải lười hay nối kèm tải ở <b>nơi viết truy vấn</b>, theo điều màn hình thật sự cần, và đo lại ở dữ liệu lớn.</div>""",
           """Đừng đoán số câu SQL, hãy đếm nó. Chọn cách tải ở chỗ viết truy vấn theo điều màn hình cần, rồi đo lại ở dữ liệu lớn."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["JPA/Hibernate: vấn đề N+1 là gì, sửa thế nào?", "vòng lặp đụng quan hệ tải lười sinh 1 + N câu; đo bằng bộ đếm; sửa bằng <code>join fetch</code>, và nêu đánh đổi số dòng trả về"],
                  ["Hibernate có kiểm bẩn không, khi nào ghi xuống?", "so đối tượng được quản lý với bản chụp lúc tải; sinh UPDATE khi chốt hoặc ngay trước truy vấn bị ảnh hưởng; đối tượng đã rời ngữ cảnh thì không"],
                  ["Spring Data dùng để làm gì?", "khai giao diện kho truy cập dữ liệu, Spring tạo cài đặt; truy vấn sinh từ tên hàm như <code>findByTen</code> hoặc viết tay bằng <code>@Query</code>"]]),
           """Người phỏng vấn thường hỏi: vấn đề một cộng N, kiểm bẩn, và kho truy cập của Spring. Câu trả lời ngắn nằm sẵn trên bảng.""", clear=True),
        st("""<p>Bài sau: <b>giao dịch trong Spring</b> và <b>đoạn cắt</b> (AOP): lan truyền giao dịch, mức cô lập, quy tắc hoàn tác, và lỗi tự gọi làm giao dịch không chạy.</p>""",
           """Ở bài hai mươi lăm, ta đi sâu vào giao dịch trong Spring và đoạn cắt: lan truyền giao dịch, mức cô lập, quy tắc hoàn tác, và lỗi tự gọi làm giao dịch không chạy.""",
           forward_ref=True),
    ], checks=["alg.bnx_l24_lazy_sql(50) == 51"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L24", "jpa_hibernate_spring_data",
                  "Bài 24 — JPA/Hibernate và Spring Data: thực thể, ngữ cảnh bền vững và vấn đề N+1",
                  "curriculum/bnx.yaml L24; audit/bnx/verify_bnx.py L24; audit/bnx/sources_l24.md: hướng dẫn Hibernate ORM 7.1 (User Guide), "
                  "hướng dẫn Spring Data Commons/JPA (đọc 2026-11-13); Hibernate 7.1.0.Final + H2 2.3.232 chạy thật trên Temurin JDK 21.0.13",
                  ["Khai báo một thực thể và kể bốn trạng thái của đối tượng quanh ngữ cảnh bền vững",
                   "Đếm số câu SQL của một truy vấn tải lười và nhận ra vấn đề một cộng N",
                   "Sửa vấn đề một cộng N bằng phép nối kèm tải và so số câu SQL ở 5, 500 và 50 000 khách",
                   "Giải thích vì sao sửa một đối tượng đang được quản lý thì tự sinh lệnh UPDATE mà không gọi hàm lưu",
                   "Phân biệt đối tượng đang được quản lý với đối tượng đã rời ngữ cảnh khi sửa dữ liệu",
                   "Mô tả cách khai một kho truy cập dữ liệu của Spring Data và cách truy vấn sinh ra từ tên hàm",
                   "Đếm câu SQL của hai cách đọc dữ liệu bằng mã Python và sqlite"],
                  scenes,
                  covers=[(1, "intuition"), (2, "example"), (3, "quymo"), (4, "example"), (5, "example"), (6, "formula"), (7, "practice")])


def _ghi_java():
    """Mã Java ĐỦ của bài (mọi chương trình prog java) ghi vào labs/BNX/L24/java để người học biên dịch lại; tất định."""
    d = ROOT / "labs" / "BNX" / "L24" / "java"
    d.mkdir(parents=True, exist_ok=True)
    for p in lib2.PROGRAMS:
        if p.lesson == "L24" and p.lang == "java":
            (d / f"{p.name}.java").write_text(p.code + "\n", encoding="utf-8", newline="\n")
    (d / "README.txt").write_text(
        "Mã Java đủ của bài 24 (các tệp trên màn hình chỉ hiện từng đoạn).\n"
        "Cần JDK 21, Hibernate ORM 7.1.0.Final, H2 2.3.232 và các thư viện phụ thuộc (do Maven tải) trong thư mục lib.\n"
        "Biên dịch: javac -encoding UTF-8 -cp \"lib/*\" -d out *.java\n"
        "Chạy (Windows dùng dấu chấm phẩy, Linux dùng dấu hai chấm): java -cp \"out;lib/*\" DemSql\n"
        "Các lớp chạy được: DemSql, DemN1, DemBan, DemLoi, DemNho, DemTrang. Đầu ra không in thời gian nên chạy lại ra y hệt.\n",
        encoding="utf-8", newline="\n")


# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
