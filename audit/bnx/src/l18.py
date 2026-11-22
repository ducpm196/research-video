import lib2
from lib2 import *
from libj import jstep, nowrap, JROW


def R(k, say):
    """Hàng của khuôn libj.JROW với lời đọc rút gọn (bài này nhiều bảng, giữ lời đọc ≤ 2300 từ)."""
    return (JROW[k][0], JROW[k][1], say)


# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l18.yaml, audit/bnx/ver/l18.py) ──
# Thư viện: audit/bnx/deps/l18/ (JUnit Platform Console Standalone 1.14.4 = JUnit Jupiter 5.14.4, Mockito 5.24.0), JDK 21.
JAVA_PHI = r'''
class Phi {
    // Phí chuyển tiền (số minh hoạ). Đề bài:
    //   dưới 500 000 đồng: miễn phí
    //   từ 500 000 tới dưới 10 000 000: phí 5 000
    //   từ 10 000 000 trở lên: phí 5 500
    static long tinh(long soTien) {
        if (soTien < 500_000) return 0;
        if (soTien <= 10_000_000) return 5_000;
        return 5_500;
    }
}
'''

JAVA_PHITEST = r'''
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class PhiTest {
    @Test void mienPhi() { assertEquals(0, Phi.tinh(200_000)); }
    @Test void phiVua() { assertEquals(5000, Phi.tinh(2_000_000)); }
    @Test void phiCao() { assertEquals(5500, Phi.tinh(50_000_000)); }
    @Test void bien() { assertEquals(5500, Phi.tinh(10_000_000)); }
}
'''

SH_PHI = r'''
javac -encoding UTF-8 -cp "lib/*" -d out Phi.java PhiTest.java
java -jar lib/junit-platform-console-standalone-1.14.4.jar execute \
  --class-path out --select-class PhiTest \
  --disable-banner --disable-ansi-colors --details-theme ascii
'''

SH_FIX = r'''
sed -i 's/<= 10_000_000/< 10_000_000/' Phi.java
javac -encoding UTF-8 -cp "lib/*" -d out Phi.java PhiTest.java
java -jar lib/junit-platform-console-standalone-1.14.4.jar execute \
  --class-path out --select-class PhiTest \
  --disable-banner --disable-ansi-colors --details summary
'''

JAVA_DV = r'''
interface CongThanhToan { boolean chuyen(String tk, long soTien); }

class ChuyenTien {
    private final CongThanhToan cong;
    ChuyenTien(CongThanhToan cong) { this.cong = cong; }
    long chuyen(String tk, long soTien) {
        long phi = Phi.tinh(soTien);
        if (!cong.chuyen(tk, soTien + phi))
            throw new IllegalStateException("cổng từ chối");
        return phi;
    }
}
'''

JAVA_DVTEST = r'''
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import org.junit.jupiter.api.Test;
class ChuyenTienTest {
    CongThanhToan cong = mock(CongThanhToan.class);
    @Test void goiCongDungMotLan() {
        when(cong.chuyen("TK01", 2_005_000)).thenReturn(true);
        long phi = new ChuyenTien(cong).chuyen("TK01", 2_000_000);
        assertEquals(5000, phi);
        verify(cong, times(1)).chuyen("TK01", 2_005_000);
    }
}
'''

JAVA_TUCHOI = r'''
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import org.junit.jupiter.api.Test;
class TuChoiTest {
    CongThanhToan cong = mock(CongThanhToan.class);
    ChuyenTien dv = new ChuyenTien(cong);
    @Test void congTuChoiThiNemLoi() {   // chưa dặn: giả trả false
        assertThrows(IllegalStateException.class,
            () -> dv.chuyen("TK01", 2_000_000));
        verify(cong, times(1)).chuyen("TK01", 2_005_000);
    }
}
'''

SH_MOCK = r'''
javac -encoding UTF-8 -cp "lib/*" -d out *.java
L=lib; java -jar $L/junit-platform-console-standalone-1.14.4.jar \
  execute -cp out -cp $L/mockito-core-5.24.0.jar \
  -cp $L/byte-buddy-1.17.7.jar -cp $L/byte-buddy-agent-1.17.7.jar \
  -cp $L/objenesis-3.3.jar --select-class ChuyenTienTest \
  --select-class TuChoiTest --disable-banner \
  --disable-ansi-colors --details-theme ascii
'''

JAVA_FAKE = r'''
public class Main {
    public static void main(String[] a) {
        long[] ghi = new long[2];       // [số lần gọi, số tiền]
        CongThanhToan gia = (tk, soTien) -> {    // giả viết tay
            ghi[0]++; ghi[1] = soTien;
            return true;
        };
        long phi = new ChuyenTien(gia).chuyen("TK01", 2_000_000);
        System.out.println(phi + " " + ghi[0] + " " + ghi[1]);
    }
}
'''

JAVA_CLOCK = r'''
import java.time.*;
public class Main {
    static boolean kip(Clock dongHo) {     // kịp trước 22 giờ
        return LocalTime.now(dongHo).isBefore(LocalTime.of(22, 0));
    }
    public static void main(String[] a) {
        ZoneOffset vn = ZoneOffset.ofHours(7);
        Instant t = Instant.parse("2026-11-11T21:59:00+07:00");
        System.out.println(kip(Clock.fixed(t, vn)));
        System.out.println(kip(Clock.fixed(t.plusSeconds(60), vn)));
    }
}
'''

# Đầu ra thật (chạy 2026-11-11, JDK 21.0.13 Temurin, Git Bash); cắt bớt bằng "…", bỏ dòng thời gian chạy vì không ổn định
OUT_PHI = """
+-- JUnit Jupiter [OK]
| '-- PhiTest [OK]
|   +-- phiCao() [OK]
|   +-- phiVua() [OK]
|   +-- bien() [X] expected: <5500> but was: <5000>
|   '-- mienPhi() [OK]
…
       PhiTest.bien(PhiTest.java:8)
…
[         4 tests found           ]
[         3 tests successful      ]
[         1 tests failed          ]
"""
OUT_FIX = """
[         4 tests found           ]
[         4 tests successful      ]
[         0 tests failed          ]
"""
OUT_MOCK = """
+-- JUnit Jupiter [OK]
| +-- ChuyenTienTest [OK]
| | '-- goiCongDungMotLan() [OK]
| '-- TuChoiTest [OK]
|   '-- congTuChoiThiNemLoi() [OK]
…
[         2 tests found           ]
[         2 tests successful      ]
[         0 tests failed          ]
"""
OUT_FAKE = """
5000 1 2005000
"""
OUT_CLOCK = """
true
false
"""

SPOKEN = {}


_KEEP_CASE = {"Java", "API", "HTTP", "SQL", "JSON", "Redis"}


def _lower_first(t):
    w = t.split(" ", 1)[0].strip(",:")
    if w in _KEEP_CASE or (len(w) > 1 and w.isupper()):
        return t
    return t[:1].lower() + t[1:]


def _fmerge(a, b):
    if a in (0, None):
        return b
    if b in (0, None):
        return a
    la, lb = (a if isinstance(a, list) else [a]), (b if isinstance(b, list) else [b])
    return la + [x for x in lb if x not in la]


def _merge_short(st_, minw=8, maxc=170, maxw=38):
    """Câu ≤ 7 từ (TTS/ASR dễ méo) ghép vào câu sau (hoặc câu trước) bằng dấu phẩy; focus ghép theo (như bài L03)."""
    ss = lv.sentences(st_["say"])
    foc = st_.get("focus")
    fl = list(foc) if isinstance(foc, list) and len(foc) == len(ss) else None
    j = 0
    while j < len(ss):
        if len(ss[j].split()) < minw and ss[j].endswith("."):
            nxt = ss[j][:-1] + ", " + _lower_first(ss[j + 1]) if j + 1 < len(ss) else None
            if nxt and len(nxt) <= maxc and len(nxt.split()) <= maxw:
                ss[j:j + 2] = [nxt]
                if fl:
                    fl[j:j + 2] = [_fmerge(fl[j], fl[j + 1])]
                continue
            if j > 0 and ss[j - 1].endswith("."):
                prv = ss[j - 1][:-1] + ", " + _lower_first(ss[j])
                if len(prv) <= maxc and len(prv.split()) <= maxw:
                    ss[j - 1:j + 1] = [prv]
                    if fl:
                        fl[j - 1:j + 1] = [_fmerge(fl[j - 1], fl[j])]
                    j -= 1
                    continue
        j += 1
    st_["say"] = " ".join(ss)
    if fl is not None:
        st_["focus"] = fl


def _spoken(scenes):
    for sc_ in scenes:
        for s_ in sc_["steps"]:
            for a_, b_ in SPOKEN.items():
                s_["say"] = s_["say"].replace(a_, b_)
            _merge_short(s_)
    return scenes



# ── AF2 (WP4, 2026-11-14): cảnh quy mô + Tự làm ──
lib2.begin("L18")

J_QUYMO = r'''
import java.util.Arrays;
public class BoCa {
  static int[] moc;
  static int dem(long x) {               // số mốc ≤ x
    int i = Arrays.binarySearch(moc, (int) x);
    return i >= 0 ? i + 1 : -i - 1;
  }
  static int tinh(long x, int loi) {     // loi: chỉ số mốc bị nhầm < thành <=
    return dem(x) - (loi >= 0 && x == moc[loi] ? 1 : 0);
  }
  static int lot(long[] ca, int k) {     // số lỗi mà bộ ca không bắt được
    int song = 0;
    for (int loi = 0; loi < k; loi++) {
      boolean bat = false;
      for (long x : ca) if (tinh(x, loi) != tinh(x, -1)) bat = true;
      if (!bat) song++;
    }
    return song;
  }
  public static void main(String[] a) {
    for (int k : new int[] {2, 200, 2000}) {
      moc = new int[k];
      long[] giua = new long[k + 1], bien = new long[2 * k + 1];
      for (int i = 0; i < k; i++) {
        moc[i] = (i + 1) * 10;
        bien[2 * i] = moc[i];
        bien[2 * i + 1] = moc[i] - 1;
      }
      for (int i = 0; i <= k; i++) giua[i] = i * 10 + 5;
      bien[2 * k] = 5;
      String s = k + " moc: giua khoang " + giua.length + " ca, lot "
          + lot(giua, k);
      System.out.println(s + "; sat moc " + bien.length
          + " ca, lot " + lot(bien, k));
    }
  }
}
'''
P_QUYMO = prog("BoCa", J_QUYMO, lang="java", timeout=180,
               claims=["k mốc, bộ ca giữa khoảng k + 1 ca bỏ lọt k lỗi nhầm dấu; bộ ca sát mốc 2k + 1 ca bỏ lọt 0 (k = 2, 200, 2000), mô phỏng đột biến bằng Java thuần"])

# Lab (số liệu khác ví dụ): phí rút tiền 2 mốc 2 000 000 / 20 000 000; mã nhầm dấu ở mốc 20 000 000; cổng giả đếm lời gọi; đồng hồ đứng yên 17 giờ
LAB_JAVA = r'''
import java.time.*;

public class Lab {
    interface Cong { boolean chuyen(String tk, long soTien); }

    // Đề: dưới 2 000 000: 0; từ 2 000 000 tới dưới 20 000 000: 3 000; từ 20 000 000: 4 000
    static long tinh(long soTien) {
        if (soTien < 2_000_000) return 0;
        if (soTien <= 20_000_000) return 3_000;   // nhầm dấu: phải là <
        return 4_000;
    }

    static long chuyen(Cong cong, String tk, long soTien) {
        long phi = tinh(soTien);
        if (!cong.chuyen(tk, soTien + phi)) throw new IllegalStateException();
        return phi;
    }

    static boolean kip(Clock dongHo) {
        return LocalTime.now(dongHo).isBefore(LocalTime.of(17, 0));
    }

    static int dat = 0, truot = 0;

    static void ca(long vao, long mongDoi) {
        long nhan = tinh(vao);
        boolean ok = nhan == mongDoi;
        if (ok) dat++; else truot++;
        System.out.println("ca " + vao + ": mong doi " + mongDoi + ", nhan " + nhan
                + ", " + (ok ? "DAT" : "TRUOT"));
    }

    public static void main(String[] args) {
        ca(1_999_999, 0);
        ca(2_000_000, 3_000);
        ca(19_999_999, 3_000);
        ca(20_000_000, 4_000);
        ca(30_000_000, 4_000);
        System.out.println("tong: " + dat + " dat, " + truot + " truot");

        long[] ghi = new long[2];
        Cong gia = (tk, soTien) -> { ghi[0]++; ghi[1] = soTien; return true; };
        chuyen(gia, "TK07", 12_000_000);
        System.out.println("cong goi " + ghi[0] + " lan, so tien " + ghi[1]);

        ZoneOffset vn = ZoneOffset.ofHours(7);
        Instant t = Instant.parse("2026-11-11T16:59:00+07:00");
        System.out.println(kip(Clock.fixed(t, vn)));
        System.out.println(kip(Clock.fixed(t.plusSeconds(60), vn)));
    }
}
'''
LAB_OUT = """ca 1999999: mong doi 0, nhan 0, DAT
ca 2000000: mong doi 3000, nhan 3000, DAT
ca 19999999: mong doi 3000, nhan 3000, DAT
ca 20000000: mong doi 4000, nhan 3000, TRUOT
ca 30000000: mong doi 4000, nhan 4000, DAT
tong: 4 dat, 1 truot
cong goi 1 lan, so tien 12003000
true
false"""

LAB_DE = """# Lab BNX L18 — Ca kiểm tự viết, cổng giả đếm lời gọi, đồng hồ đứng yên (không cần tải thư viện)

Lab chạy được chỉ với JDK, không cần JUnit hay Mockito: ta tự viết phần "khẳng định" và "đối tượng giả" bằng Java thuần. Số liệu là số minh hoạ.

Viết `Lab.java` (một tệp, `public class Lab`, `import java.time.*;`) gồm các phần đề cho sẵn dưới đây (chép nguyên) rồi tự viết hàm `ca` và `main`:

```java
interface Cong { boolean chuyen(String tk, long soTien); }

// Đề: dưới 2 000 000: 0; từ 2 000 000 tới dưới 20 000 000: 3 000; từ 20 000 000: 4 000
static long tinh(long soTien) {
    if (soTien < 2_000_000) return 0;
    if (soTien <= 20_000_000) return 3_000;   // nhầm dấu: phải là <
    return 4_000;
}
static long chuyen(Cong cong, String tk, long soTien) {   // phí rồi gọi cổng với soTien + phí
    long phi = tinh(soTien);
    if (!cong.chuyen(tk, soTien + phi)) throw new IllegalStateException();
    return phi;
}
static boolean kip(Clock dongHo) {   // kịp trước 17 giờ
    return LocalTime.now(dongHo).isBefore(LocalTime.of(17, 0));
}
```
(`Cong` đặt trong lớp `Lab` dưới dạng `interface Cong {…}` lồng.)

**Phần 1 — ca kiểm.** Viết hàm `ca(long vao, long mongDoi)`: gọi `tinh(vao)`, so với `mongDoi` (lấy từ ĐỀ, không từ mã), đếm số ca đạt và trượt, in `ca <vao>: mong doi <m>, nhan <n>, DAT` hoặc `TRUOT`.
Gọi cho 5 số tiền theo thứ tự: 1999999, 2000000, 19999999, 20000000, 30000000 (mong đợi lấy từ đề). Rồi in `tong: <đạt> dat, <trượt> truot`.

**Phần 2 — cổng giả.** Viết đối tượng giả `Cong` bằng một biểu thức lambda, ghi lại số lần gọi và số tiền cuối cùng. Gọi `chuyen(gia, "TK07", 12_000_000)` rồi in `cong goi <số lần> lan, so tien <số tiền>`.

**Phần 3 — đồng hồ.** Với `Clock.fixed` ở `2026-11-11T16:59:00+07:00` (múi giờ +7) rồi sau 60 giây, in kết quả `kip(...)` hai dòng.

In đúng 9 dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh BNX L18 Lab.java`.
"""


def build():
    hook = sc("hook", "hook", "Một dấu bằng thừa, mỗi giao dịch thu thiếu 500 đồng", [
        st("""<p>Ngân hàng tính phí chuyển tiền (số minh hoạ): từ <b>10 000 000</b> đồng trở lên thu <b>5 500</b> đồng.
Lập trình viên viết nhầm <code>&lt;=</code> thay cho <code>&lt;</code>, nên khách chuyển <b>đúng 10 000 000</b> chỉ bị thu <b>5 000</b>.</p>
<div class="box key">Mỗi giao dịch thu thiếu 5 500 − 5 000 = <b>500</b> đồng. Với 20 000 giao dịch đúng mốc mỗi tháng (số minh hoạ): 20 000 × 500 = <b>10 000 000</b> đồng.
Thử tay ba số tiền bất kỳ đều thấy đúng. Làm sao để máy tự bắt lỗi này trước khi lên chạy thật?</div>""",
           """Chào bạn, ngân hàng tính phí chuyển tiền bằng số minh hoạ: từ mười triệu đồng trở lên thu năm nghìn năm trăm đồng. Lập trình viên viết nhầm một dấu so sánh, nên khách chuyển đúng mười triệu chỉ bị thu năm nghìn. Hai mươi nghìn giao dịch đúng mốc mỗi tháng thiếu mười triệu đồng. Thử tay ba số đều đúng, vậy làm sao để máy tự bắt lỗi?""", focus=[1, 1, 2, 2]),
    ], checks=["alg.bnx_jt_fee(10_000_000) == 5500", "alg.bnx_jt_fee(10_000_000, True) == 5000",
               "alg.bnx_jt_fee(10_000_000) - alg.bnx_jt_fee(10_000_000, True) == 500",
               "20_000 * (alg.bnx_jt_fee(10_000_000) - alg.bnx_jt_fee(10_000_000, True)) == 10_000_000"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① nhánh của một hàm", "mỗi câu <code>if</code> rẽ hàm thành các đường đi khác nhau; mỗi đường đi là một nhánh", "2 mốc so sánh cắt trục số tiền thành 3 khoảng, tức 3 nhánh"],
                  ["② giao diện (<code>interface</code>)", "bản kê tên các hàm, chưa có thân hàm; lớp nào viết đủ các hàm đó thì dùng thay cho nhau được", "<code>CongThanhToan</code> có một hàm <code>chuyen</code>"],
                  ["③ phần phụ thuộc bên ngoài", "thứ mã của ta gọi tới nhưng không do ta điều khiển", "cổng thanh toán, cơ sở dữ liệu, đồng hồ, mạng"],
                  ["④ ngoại lệ (<code>exception</code>)", "cách một hàm báo lỗi: dừng ngay và ném lỗi ra cho nơi gọi", "cổng từ chối thì ném <code>IllegalStateException</code>"]]),
           """Trước hết ta cần hiểu bốn điều. Câu điều kiện rẽ hàm thành các nhánh. Giao diện là bản kê tên các hàm chưa có thân hàm, nên lớp nào viết đủ các hàm đó thì dùng thay nhau được. Phần phụ thuộc bên ngoài là thứ mã gọi tới mà không điều khiển được, như cổng thanh toán hay đồng hồ. Ngoại lệ là cách một hàm báo lỗi.""",
           introduces=["bnx_ngoai_le"]),
        st("""<p>Làm thử: theo đề, chuyển 2 000 000 đồng thì phí 5 000 đồng, nên số tiền trừ ở cổng là</p>
$$2\\,000\\,000 + 5\\,000 = \\hl{2\\,005\\,000}\\ \\text{đồng}$$""",
           """Làm thử với đề phí của bài. Chuyển hai triệu đồng thì phí là năm nghìn, vì hai triệu nằm giữa hai mốc, nên cổng thanh toán phải trừ hai triệu không trăm linh năm nghìn đồng."""),
    ], checks=["alg.bnx_jt_fee_branches() == 3", "alg.bnx_jt_fee(2_000_000) == 5000", "2_000_000 + alg.bnx_jt_fee(2_000_000) == 2_005_000"])

    sym = sc("sym", "symbol", "Giải mã các từ của JUnit 5 và Mockito", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["JUnit 5", "bộ khung kiểm thử của Java: tìm các ca kiểm, chạy từng ca, in bản báo"],
                  ["<code>@Test</code>", "nhãn (annotation) gắn trước một hàm để báo: đây là một ca kiểm"],
                  ["<code>assertEquals(mong đợi, thực tế)</code>", "so hai giá trị; khác nhau thì ca <b>trượt</b> và bản báo ghi cả hai"],
                  ["<code>assertThrows(loại lỗi, đoạn mã)</code>", "ca chỉ đạt khi đoạn mã ném đúng loại lỗi đó"]]),
           """Bảng này giải mã các từ của bộ khung kiểm thử. Bộ khung chạy từng ca rồi in bản báo, và nhãn đặt trước một hàm báo đó là một ca kiểm. Lệnh so bằng nhận mong đợi trước, thực tế sau, khác nhau thì ca trượt. Lệnh chờ lỗi chỉ đạt khi đoạn mã ném đúng loại lỗi.""", clear=True, introduces=['bnx_junit']),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["Mockito", "thư viện tạo <b>đối tượng giả</b> (mock) từ một giao diện hay một lớp"],
                  ["<code>mock(X.class)</code>", "tạo đối tượng giả của X: có đủ các hàm của X nhưng không làm gì, chỉ <b>ghi lại</b> mọi lời gọi"],
                  ["<code>when(lời gọi).thenReturn(giá trị)</code>", "dặn trước: gặp đúng lời gọi này thì trả giá trị này; chưa dặn thì trả giá trị mặc định (<code>false</code>, 0, <code>null</code>)"],
                  ["<code>verify(giả, times(1)).hàm(tham số)</code>", "kiểm tương tác: lời gọi này đã xảy ra đúng 1 lần, đúng tham số"]]),
           """Bảng thứ hai là thư viện đối tượng giả, nó chỉ ghi lại mọi lời gọi. Lệnh dặn trước nói gặp lời gọi này thì trả giá trị này, chưa dặn thì trả mặc định là sai. Lệnh kiểm tương tác hỏi lời gọi đã xảy ra đúng một lần chưa.""", clear=True, introduces=['bnx_mockito']),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["<code>static</code>", "hàm hay biến thuộc về cả lớp, gọi không cần tạo đối tượng: <code>Phi.tinh(…)</code>"],
                  ["<code>x -&gt; …</code> (lambda)", "một hàm nhỏ không tên viết tại chỗ, dùng làm cổng giả hay đoạn mã truyền vào"],
                  ["<code>Instant.parse(\"…+07:00\")</code>, <code>Clock.fixed</code>", "một thời điểm (giờ cộng 7 so với giờ gốc) / đồng hồ đứng yên tại thời điểm đó"],
                  ["<code>Arrays.binarySearch</code>, hàm tạo", "tìm một số trong dãy đã sắp xếp (không thấy thì trả số âm); hàm tạo là hàm tên trùng lớp, chạy khi tạo đối tượng"]]),
           """Bảng này giải mã vài chữ Java sẽ gặp: hàm của cả lớp, hàm nhỏ không tên, đồng hồ đứng yên, và tìm trong dãy đã sắp xếp.""", clear=True, introduces=["bnx_binary_search"]),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["<code>javac</code>, biên dịch; <code>java</code>", "<code>javac</code> dịch tệp nguồn <code>.java</code> thành tệp Java chạy được (biên dịch); <code>java</code> chạy tệp đó"],
                  ["Maven Central", "kho thư viện Java công khai trên mạng; ta tải tệp <code>.jar</code> (thư viện đóng gói) từ đó"],
                  ["<code>int</code>, <code>long</code>, <code>long[]</code>", "số nguyên thường, số nguyên dài, mảng số nguyên dài; phần tử thứ i viết <code>a[i]</code>, đếm từ 0"],
                  ["<code>c ? x : y</code>, <code>(int) x</code>", "chọn x nếu điều kiện c đúng, ngược lại y; ép x về số nguyên"]]),
           """Bốn dòng nữa cho cú pháp Java. Lệnh biên dịch dịch tệp nguồn thành tệp chạy được, thư viện tải từ kho công khai. Mảng đánh số từ không, dấu hỏi hai chấm chọn một trong hai giá trị theo điều kiện.""", clear=True),
    ], checks=["alg.bnx_jt_transfer(2_000_000, accept=False)[0] == 'lỗi'", "len(alg.bnx_jt_transfer(2_000_000)[1]) == 1"])

    intu = sc("intuition", "intuition", "Hình dung: ca kiểm là một phép so, đối tượng giả là người đóng thế", [
        st(svg(1500, 470,
               box(40, 60, 300, 100, ["① sắp đặt", "số tiền 10 000 000"], C_BLUE, 24, True),
               box(450, 60, 300, 100, ["② gọi hàm", "Phi.tinh(…)"], C_PURPLE, 24, True),
               box(860, 60, 280, 100, ["thực tế", "5 000"], C_AMBER, 24, True),
               box(860, 250, 280, 100, ["mong đợi (theo đề)", "5 500"], C_GREEN, 24, True),
               box(1240, 150, 230, 110, ["③ so", "khác → trượt"], C_RED, 26, True),
               arrow(345, 110, 445, 110), arrow(755, 110, 855, 110),
               arrow(1145, 120, 1235, 180, "#d97706"), arrow(1145, 290, 1235, 230, "#16a34a"),
               txt(750, 430, "Ca kiểm = sắp đặt đầu vào, gọi hàm, so thực tế với mong đợi lấy từ ĐỀ BÀI", 24, "middle", "#1f2937", True)),
           """Một ca kiểm chỉ gồm ba việc. Sắp đặt đầu vào mười triệu đồng, gọi hàm tính phí để nhận giá trị thực tế năm nghìn, rồi so với mong đợi theo đề là năm nghìn năm trăm, khác nhau nên ca trượt."""),
        st(svg(1500, 470,
               box(40, 170, 260, 110, ["ca kiểm", "ChuyenTienTest"], C_BLUE, 24, True),
               box(420, 170, 320, 110, ["dịch vụ ChuyenTien", "(mã của ta)"], C_PURPLE, 24, True),
               box(900, 40, 540, 110, ["cổng thanh toán thật", "mạng, chậm, trừ tiền thật"], C_GRAY, 24, True, dash=True),
               box(900, 300, 540, 110, ["đối tượng giả (mock)", "trả lời như đã dặn, ghi lại lời gọi"], C_GREEN, 24, True),
               arrow(305, 225, 415, 225), arrow(745, 200, 895, 110, "#6b7280", dash=True), arrow(745, 250, 895, 340, "#16a34a"),
               txt(770, 120, "không dùng", 22, "middle", "#6b7280"), txt(815, 330, "thay vào", 22, "middle", "#16a34a"),
               arrow(895, 385, 310, 270, "#2a78d6"), txt(560, 380, "hỏi lại: gọi mấy lần, tham số gì", 22, "middle", "#2a78d6"),
               txt(750, 455, "Cùng một giao diện CongThanhToan: dịch vụ không biết mình đang gọi đồ thật hay đồ giả", 24, "middle", "#1f2937", True)),
           """Hình thứ hai cho thấy vai của đối tượng giả. Cổng thanh toán thật cần mạng, chạy chậm và trừ tiền thật, nên ca kiểm thay nó bằng đối tượng giả cùng giao diện. Đối tượng giả ghi lại lời gọi, nên cuối ca ta hỏi nó đã được gọi mấy lần."""),
    ], checks=["alg.bnx_jt_fee(10_000_000, True) == 5000 and alg.bnx_jt_fee(10_000_000) == 5500",
               "alg.bnx_jt_fee_run(True)[2] == [('bien', 5500, 5000)]"])

    form = sc("formula", "formula", "Suy ra từng bước: từ thử tay tới kiểm tương tác", [
        st("""<p><b>Bước 1.</b> Thử tay thì mỗi lần sửa mã lại phải thử lại, và sẽ có lần quên. <b>Ca kiểm</b> là một hàm nhỏ: gọi hàm cần kiểm rồi so với giá trị mong đợi, nên máy chạy lại được sau mỗi lần sửa.</p>
<span class='note'>Làm thử: <code>assertEquals(0, Phi.tinh(200_000))</code>, vì 200 000 dưới mốc 500 000 nên đề cho phí 0.</span>""",
           """Bước một, thử tay thì mỗi lần sửa mã lại phải thử lại và sẽ có lần quên, nên ta viết ca kiểm, là hàm nhỏ so kết quả với mong đợi. Làm thử, hai trăm nghìn đồng dưới mốc năm trăm nghìn nên mong đợi là không đồng.""", clear=True),
        st("""<p><b>Bước 2.</b> Nhánh nào không chạy trong ca kiểm thì lỗi trong nhánh đó không lộ ra, nên <b>mỗi nhánh cần ít nhất một ca</b>.</p>
$$\\text{2 mốc} \\;\\Rightarrow\\; 2 + 1 = \\hl{3}\\ \\text{nhánh} \\;\\Rightarrow\\; \\text{ít nhất 3 ca}$$""",
           """Bước hai, nhánh nào không chạy trong ca kiểm thì lỗi trong nhánh đó không lộ ra, nên mỗi nhánh cần ít nhất một ca. Hai mốc cắt trục số tiền thành ba khoảng, nên cần ít nhất ba ca."""),
        st("""<p><b>Bước 3.</b> Ba ca ở <b>giữa</b> ba khoảng vẫn chưa chạm tới dấu so sánh. Lỗi <code>&lt;</code> thành <code>&lt;=</code> chỉ lộ ở <b>đúng mốc</b>, nên thêm ca ở mốc biên.</p>
<span class='note'>Làm thử: tại đúng 10 000 000, đề cho 5 500; mã viết <code>&lt;=</code> trả 5 000. Ba ca kia vẫn đạt.</span>""",
           """Bước ba, ba ca ở giữa ba khoảng chưa chạm tới dấu so sánh, vì lỗi nhầm dấu chỉ lộ ra ở đúng mốc, nên ta thêm một ca ở mốc biên. Tại đúng mười triệu, đề cho năm nghìn năm trăm còn mã nhầm trả năm nghìn.""", clear=True),
        st("""<p><b>Bước 4.</b> Dịch vụ chuyển tiền gọi ra cổng thanh toán. Gọi cổng thật trong ca kiểm thì chậm, cần mạng và trừ tiền thật.
Vì dịch vụ chỉ biết <b>giao diện</b> <code>CongThanhToan</code> và nhận cổng qua hàm tạo, ca kiểm đưa vào một <b>đối tượng giả</b>.</p>
<span class='note'>Làm thử: dặn giả trả <code>true</code> khi được gọi với TK01 và 2 000 000 + 5 000 = 2 005 000.</span>""",
           """Bước bốn, dịch vụ chuyển tiền gọi ra cổng thanh toán, mà gọi cổng thật trong ca kiểm thì chậm và trừ tiền thật. Vì dịch vụ nhận cổng qua hàm tạo, nên ca kiểm đưa vào một đối tượng giả đã dặn trả lời đúng.""", clear=True),
        st("""<p><b>Bước 5.</b> Giá trị trả về đúng vẫn chưa đủ. Gọi cổng <b>0 lần</b> thì tiền không đi; gọi <b>2 lần</b> thì khách bị trừ hai lần.
Nên ca kiểm hỏi lại đối tượng giả: lời gọi đã xảy ra <b>đúng 1 lần</b> với <b>đúng tham số</b> chưa. Đó là <b>kiểm tương tác</b>.</p>
<span class='note'>Làm thử: <code>verify(cong, times(1)).chuyen("TK01", 2_005_000)</code>.</span>""",
           """Bước năm, giá trị trả về đúng vẫn chưa đủ, vì gọi cổng không lần nào thì tiền không đi, gọi hai lần thì khách bị trừ hai lần. Nên ca kiểm hỏi đối tượng giả lời gọi đã xảy ra đúng một lần chưa, đó là kiểm tương tác.""", clear=True),
    ], checks=["alg.bnx_jt_fee(200_000) == 0", "alg.bnx_jt_fee_branches() == 2 + 1 == 3",
               "alg.bnx_jt_fee_run(True)[:2] == (3, 1)", "alg.bnx_jt_transfer(2_000_000)[1] == [('TK01', 2_005_000)]"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        jstep([(R("class", "Lớp là khối chứa các hàm và dữ liệu, nằm giữa cặp ngoặc nhọn."), "<code>class Phi { … }</code>", ""),
               (R("sig", "Khai hàm gồm kiểu trả về, tên, rồi các tham số."), "<code>static long tinh(long soTien)</code>: trả về số nguyên lớn, nhận một số tiền", ""),
               (("<code>if (soTien &lt; 500_000) return 0;</code>", "nếu điều kiện đúng thì trả về giá trị đó và hàm dừng ngay; gạch dưới trong số chỉ để dễ đọc", "Nếu điều kiện đúng thì hàm trả về ngay, gạch dưới chỉ để dễ đọc số."), "200_000 là 200000, nên trả 0", "")]),
        st(code(JAVA_PHI, "Phi.java: hàm tính phí, còn một lỗi ở dấu so sánh"),
           """Hàm tính phí viết bằng Java, kèm đề bài ở phần chú thích. Câu điều kiện thứ hai viết nhỏ hơn hoặc bằng mười triệu, và đó là chỗ sai so với đề.""", clear=True),
        jstep([(R("impstatic", "Câu nhập tĩnh lấy sẵn một hàm để gọi bằng tên ngắn."), "<code>import static org.junit…Assertions.assertEquals;</code>: viết <code>assertEquals(…)</code> thẳng", ""),
               (("<code>@Test void mienPhi() { … }</code>", "<code>@Test</code> báo đây là một ca kiểm; <code>void</code>: hàm không trả gì; thân hàm giữa cặp ngoặc nhọn", "Nhãn báo đây là một ca kiểm, và hàm không trả gì."), "mỗi ca là một hàm", "")]),
        st(code(JAVA_PHITEST, "PhiTest.java: bốn ca kiểm viết bằng JUnit 5")
           + """$$① \\; \\text{2 mốc} \\Rightarrow 2 + 1 = \\hl{3}\\ \\text{nhánh} \\Rightarrow \\text{ít nhất 3 ca kiểm}$$""",
           """Lớp kiểm thử có bốn ca. Phép tính thứ nhất, hai mốc cho ba nhánh nên cần ít nhất ba ca. Ba ca đầu ở giữa các khoảng, ca thứ tư ở đúng mốc mười triệu.""", clear=True),
        st(table(["viết trong mã hoặc lệnh", "nghĩa"],
                 [["<code>javac … -d out</code>", "ghi các tệp đã biên dịch vào thư mục <code>out</code>"],
                  ["<code>execute --class-path out --select-class PhiTest</code>", "chạy bộ kiểm thử: tìm lớp trong <code>out</code>, chọn lớp <code>PhiTest</code>"],
                  ["<code>--disable-banner --disable-ansi-colors --details-theme ascii</code>; <code>--details summary</code>", "chỉ chỉnh cách in: bỏ biểu ngữ, bỏ màu, vẽ cây bằng ký tự thường; <code>summary</code> chỉ in tóm tắt"]]),
           """Trước khi chạy, ta cần vài chỗ. Biên dịch ghi ra thư mục out, còn các cờ dài chỉ chỉnh cách in.""", clear=True),
        st(code(SH_PHI, "Biên dịch rồi chạy bằng JUnit Platform (thư viện nằm trong thư mục lib)")
           + """<p class="note"><code>-cp "lib/*"</code>: đường tìm thư viện (classpath), <code>lib/*</code> là mọi tệp jar trong thư mục <code>lib</code>. Tải <code>junit-platform-console-standalone-1.14.4.jar</code> từ Maven Central, đặt vào <code>lib</code>. <code>sed -i 's/cũ/mới/' tệp</code> thay chữ <code>cũ</code> bằng <code>mới</code> ngay trong tệp.</p>""",
           """Máy chỉ cần bộ Java và một tệp thư viện của bộ khung kiểm thử. Lệnh đầu biên dịch, lệnh sau chạy bộ khung.""", clear=True, introduces=["bnx_sed_i"]),
        st(out(OUT_PHI) + """
$$② \\; 3\\ \\text{đạt} + 1\\ \\text{trượt} = \\hl{4}\\ \\text{ca}; \\qquad ③ \\; 5500 - 5000 = \\hl{500}\\ \\text{đồng thu thiếu}$$""",
           """Bản báo chạy thật: ba ca ở giữa khoảng đạt, ca ở mốc biên trượt, mong đợi năm nghìn năm trăm nhưng nhận năm nghìn. Phép tính thứ hai, ba đạt cộng một trượt là bốn ca. Phép tính thứ ba, thu thiếu năm trăm đồng, đúng số ở đầu bài.""", clear=True),
        st("""<p>Thứ tự chạy là phiCao, phiVua, bien, mienPhi: <b>không</b> theo thứ tự viết trong tệp, nên các ca không được dựa vào nhau.</p>
<p style='margin-top:18px'><b>Bộ bốn ca này còn hở:</b> hàm có hai mốc nhưng chỉ có ca ở đúng mốc 10 000 000. Lỗi tương tự ở mốc 500 000 vẫn lọt, vì cả bốn ca vẫn đạt.</p>
<p style='margin-top:18px'><span class='note'>Quy tắc của bài là mỗi mốc một ca ở đúng mốc, nên cần thêm ca ở 500 000 và 499 999; câu 1 cuối bài tính các giá trị ấy.</span></p>""",
           """Bộ khung chạy các ca không theo thứ tự viết, nên các ca không được dựa vào nhau. Bộ bốn ca này còn hở, vì lỗi tương tự ở năm trăm nghìn vẫn lọt.""", clear=True),
        st(code(SH_FIX, "Sửa dấu so sánh, chạy lại cả bốn ca") + out(OUT_FIX),
           """Ta đổi dấu nhỏ hơn hoặc bằng thành nhỏ hơn rồi chạy lại. Kết quả chạy thật: bốn ca đạt, nên chỗ sửa không làm hỏng nhánh khác.""", clear=True),
        jstep([(("<code>interface CongThanhToan { boolean chuyen(String tk, long soTien); }</code>", "giao diện: chỉ kê tên và tham số của hàm, chưa có thân; <code>boolean</code>: trả về đúng hoặc sai", "Giao diện chỉ kê tên hàm mà chưa có thân hàm, và hàm này trả về đúng hoặc sai."), "", ""),
               (R("fld", "Chữ riêng tư là chỉ lớp này dùng được, chữ cuối cùng là gán một lần."), "<code>private final CongThanhToan cong;</code>", "")]),
        jstep([(R("ctor", "Hàm tạo cùng tên lớp, chạy khi tạo mới, chép tham số vào trường."), "<code>ChuyenTien(CongThanhToan cong) { this.cong = cong; }</code>", ""),
               (R("throw", "Câu này ném một đối tượng lỗi, việc đang làm dừng và nhảy tới nơi bắt lỗi."), "<code>throw new IllegalStateException(\"cổng từ chối\");</code>", "")]),
        st(code(JAVA_DV, "ChuyenTien.java: dịch vụ gọi ra cổng thanh toán qua một giao diện"),
           """Dịch vụ chuyển tiền nhận cổng qua giao diện và hàm tạo. Nó tính phí rồi gọi cổng với số tiền cộng phí, ném lỗi nếu cổng từ chối.""", clear=True),
        jstep([(R("new", "Chữ tạo mới tạo một đối tượng, hoặc một mảng với các giá trị liệt kê."), "<code>new ChuyenTien(cong).chuyen(\"TK01\", 2_000_000)</code>: tạo dịch vụ với cổng giả rồi gọi hàm", "")]),
        st(code(JAVA_DVTEST, "ChuyenTienTest.java: thay cổng bằng đối tượng giả của Mockito")
           + """$$④ \\; \\text{tham số gọi cổng:}\\quad 2\\,000\\,000 + 5\\,000 = \\hl{2\\,005\\,000}$$""",
           """Ca kiểm tạo đối tượng giả, dặn nó trả lời đúng, gọi dịch vụ rồi so phí với năm nghìn. Dòng cuối đòi cổng được gọi đúng một lần. Phép tính thứ tư, hai triệu cộng phí năm nghìn là hai triệu không trăm linh năm nghìn.""", clear=True),
        st(code(JAVA_TUCHOI, "TuChoiTest.java: cổng từ chối thì sao?"),
           """Ca tiếp theo xét cổng từ chối: ta không dặn gì nên đối tượng giả trả sai, và dịch vụ phải ném đúng loại lỗi.""", clear=True),
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>L=lib</code> rồi <code><span>&#36;</span>L/…</code>", "gán cho biến của vỏ lệnh tên <code>L</code> giá trị <code>lib</code>; <code><span>&#36;</span>L</code> dùng lại giá trị đó"],
                  ["<code>-cp A -cp B …</code>", "mỗi <code>-cp</code> thêm một thư viện vào đường tìm lớp"],
                  ["<code>\\</code> ở cuối dòng", "lệnh còn viết tiếp ở dòng sau"],
                  ["<code>javac … *.java</code>", "dấu <code>*</code> thay cho mọi tên: biên dịch mọi tệp có đuôi <code>.java</code> trong thư mục"]]),
           """Lệnh sau dài nên có bốn chỗ mới. Gán một biến bằng tên thư mục, mỗi cờ đường tìm thêm một thư viện, dấu gạch chéo ngược báo lệnh viết tiếp, và dấu sao thay cho mọi tên tệp.""", clear=True),
        st(code(SH_MOCK, "Biên dịch tất cả, chạy hai lớp kiểm thử có Mockito")
           + """<p class="note">Năm tệp jar thêm vào <code>lib</code>, tải từ Maven Central: <code>mockito-core-5.24.0</code>, <code>byte-buddy-1.17.7</code>, <code>byte-buddy-agent-1.17.7</code>, <code>objenesis-3.3</code>, cộng tệp JUnit ở bước trước.</p>""",
           """Lệnh lần này dài hơn vì thư viện đối tượng giả cần thêm ba thư viện đi kèm, rồi chọn hai lớp kiểm thử.""", clear=True),
        st(out(OUT_MOCK) + """
$$⑤ \\; \\text{số lần gọi cổng ghi được} = \\hlg{1} = \\text{số lần mong đợi}$$""",
           """Kết quả chạy thật: cả hai ca đều đạt, cổng được gọi đúng một lần ở cả hai. Phép tính thứ năm, một lời gọi ghi được bằng một lần mong đợi. Java hai mươi mốt còn in một cảnh báo ra luồng lỗi, không phải kết quả.""", clear=True),
    ], checks=["alg.bnx_jt_fee_branches() == 3", "len(alg.bnx_jt_fee_cases()) == 4", "alg.bnx_jt_fee_run(True) == (3, 1, [('bien', 5500, 5000)])",
               "alg.bnx_jt_fee_run(True)[2][0][1] - alg.bnx_jt_fee_run(True)[2][0][2] == 500",
               "alg.bnx_jt_fee_run(False) == (4, 0, [])",
               "alg.bnx_jt_transfer(2_000_000) == (5000, [('TK01', 2_005_000)])",
               "alg.bnx_jt_transfer(2_000_000, accept=False) == ('lỗi', [('TK01', 2_005_000)])",
               "[alg.bnx_jt_fee(a) for a in (200_000, 2_000_000, 50_000_000)] == [0, 5000, 5500]"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: đối tượng giả viết tay, không dùng thư viện", [
        jstep([(("<code>long[] ghi = new long[2];</code>", "<code>long[]</code>: mảng số nguyên lớn; <code>new long[2]</code> tạo mảng 2 ô, ban đầu đều 0; <code>ghi[0]</code> là ô đầu, <code>ghi[1]</code> là ô sau", "Mảng hai ô số nguyên lớn lúc đầu đều bằng không, đánh số từ không."), "ghi[0] đếm lần gọi, ghi[1] giữ số tiền", ""),
               (R("lambda", "Hàm ngắn không tên: tham số bên trái mũi tên, việc làm bên phải."), "<code>(tk, soTien) -&gt; { ghi[0]++; ghi[1] = soTien; return true; }</code>: cổng giả viết tay", ""),
               (R("incr", "Hai dấu cộng sau tên biến tăng biến đó thêm một, nên mỗi lần gọi đếm thêm một."), "<code>ghi[0]++</code>: tăng số lần gọi thêm 1", "")]),
        st(code(JAVA_FAKE, "Đường khác: tự viết đối tượng giả bằng Java thuần") + out(OUT_FAKE),
           """Ta kiểm lại bằng đường khác, không dùng thư viện nào. Kết quả chạy thật in phí năm nghìn, một lần gọi và hai triệu không trăm linh năm nghìn, nên khớp với ca kiểm dùng thư viện.""", clear=True),
    ], checks=["alg.bnx_jt_transfer(2_000_000)[0] == 5000", "len(alg.bnx_jt_transfer(2_000_000)[1]) == 1",
               "alg.bnx_jt_transfer(2_000_000)[1][0][1] == 2_005_000 == 2_000_000 + alg.bnx_jt_fee(2_000_000)"])

    quymo = sc("quymo", "example", "Khi bảng phí lớn dần: số ca cần và số lỗi lọt lưới", [
        jstep([(("<code>import java.util.Arrays;</code>", "lấy lớp <code>Arrays</code> trong gói <code>java.util</code> về dùng", "Câu nhập lấy lớp có sẵn trong thư viện Java về dùng."), "để gọi <code>Arrays.binarySearch</code>", ""),
               (R("sig", "Khai hàm gồm kiểu trả về, tên, rồi các tham số."), "<code>static int tinh(long x, int loi)</code>: trả về số nguyên, nhận hai tham số", "")]),
        st(P_QUYMO.show(lines=(1, 10), title="BoCa.java (1/4): phí là số mốc ≤ số tiền; lỗi là một mốc bị nhầm dấu"),
           """Ta đo thật bằng Java thuần: bảng phí có k mốc, phí bằng số mốc không vượt số tiền, và một lỗi là một mốc bị nhầm dấu so sánh.""", clear=True),
        jstep([(R("for", "Vòng lặp đếm gồm biến đếm, điều kiện còn lặp, bước sau mỗi vòng."), "<code>for (int loi = 0; loi &lt; k; loi++)</code>: loi chạy 0, 1, … k − 1", ""),
               (R("foreach", "Dấu hai chấm duyệt từng phần tử của dãy."), "<code>for (long x : ca)</code>: x là từng số trong bộ ca", ""),
               (R("decl", "Khai biến là viết kiểu rồi tên rồi giá trị, như đúng sai hay số nguyên."), "<code>boolean bat = false;</code>: cờ đúng sai, lúc đầu sai", "")]),
        st(P_QUYMO.show(lines=(11, 19), title="BoCa.java (2/4): đếm lỗi mà bộ ca không bắt được"),
           """Hàm thử từng lỗi một. Lỗi nào mà không ca nào cho kết quả khác bản đúng thì lỗi đó lọt lưới.""", clear=True),
        st(P_QUYMO.show(lines=(20, 30), title="BoCa.java (3/4): hai bộ ca cho mỗi cỡ bảng phí"),
           """Hàm chính thử ba cỡ bảng phí, với hai bộ ca. Bộ thứ nhất lấy một số ở giữa mỗi khoảng, bộ thứ hai lấy đúng mỗi mốc và số sát dưới mốc.""", clear=True),
        st(P_QUYMO.show(lines=(31, 37), title="BoCa.java (4/4): in số ca và số lỗi lọt") + P_QUYMO.out_html(),
           """Kết quả chạy thật cho thấy bộ ca giữa khoảng bỏ lọt mọi lỗi nhầm dấu ở mọi cỡ, còn bộ ca sát mốc không lọt lỗi nào.""", clear=True),
        st(table(["số mốc k", "ca giữa khoảng", "lỗi lọt", "ca sát mốc", "lỗi lọt", "chạy 10 ms mỗi ca (số minh hoạ)"],
                 [[nowrap("2 (×1)"), "3", "2 trên 2", "5", "0", "50 ms"],
                  [nowrap("200 (×100)"), "201", "200 trên 200", "401", "0", "4 giây"],
                  [nowrap("2 000 (×1000)"), "2 001", "2 000 trên 2 000", "4 001", "0", "40 giây; gọi cổng thật 2 giây mỗi ca: hơn 2 giờ"]]),
           """Hai nghìn mốc cần bốn nghìn lẻ một ca sát mốc. Dùng đối tượng giả mười mili giây mỗi ca thì mất bốn mươi giây, còn gọi cổng thật hai giây mỗi ca thì mất hơn hai giờ.""", clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["chỉ ca giữa khoảng", "ít ca nhất, k + 1", "bỏ lọt mọi lỗi nhầm dấu ở mốc", "không bao giờ đủ cho mã có mốc"],
                  ["ca sát mốc + đối tượng giả", "bắt hết lỗi mốc, chạy nhanh", "2k + 1 ca phải viết; sinh từ bảng mốc: mỗi mốc hai ca (đúng mốc, liền dưới) cộng một ca dưới mốc đầu", "phí, hạn mức, thuế: có mốc"],
                  ["ca gọi cổng thật", "kiểm cả bên ngoài", "chậm hàng nghìn lần, mạng rớt thì trượt oan", "ít ca canh cổng, chạy riêng"]]),
           """Ca giữa khoảng không thấy lỗi mốc dù bảng phí lớn bao nhiêu. Ca sát mốc cần hai k cộng một ca, nên sinh chúng từ chính bảng phí. Ca gọi cổng thật chậm hàng nghìn lần nên chạy riêng.""", clear=True),
    ], checks=["[alg.bnx_l18_cases_mid(k) for k in (2, 200, 2000)] == [3, 201, 2001]",
               "[alg.bnx_l18_cases_edge(k) for k in (2, 200, 2000)] == [5, 401, 4001]",
               "[alg.bnx_l18_survivors_mid(k) for k in (2, 200, 2000)] == [2, 200, 2000] and [alg.bnx_l18_survivors_edge(k) for k in (2, 200, 2000)] == [0, 0, 0]",
               "[alg.bnx_l18_suite_ms(alg.bnx_l18_cases_edge(k), 10) for k in (2, 200, 2000)] == [50, 4010, 40010]",
               "alg.bnx_l18_suite_ms(4001, 2000) == 8_002_000 and 8_002_000 // 3_600_000 == 2"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> “Ba ca đều đạt, vậy hàm đúng.” Ở ví dụ, ba ca giữa khoảng đều đạt trong khi hàm vẫn sai ở đúng mốc 10 000 000.
<b class="red">Ca kiểm đạt không chứng minh mã đúng</b>, chỉ chứng minh các trường hợp đã kiểm.
<br><span class="note">Cách chữa: lấy giá trị mong đợi từ đề bài, không từ mã; mỗi nhánh một ca, mỗi mốc thêm ca ở đúng mốc.</span></div>""",
           """Lỗi thứ nhất, của người mới, là thấy ba ca đều đạt thì kết luận hàm đúng. Ca kiểm đạt chỉ chứng minh các trường hợp đã kiểm. Cách chữa là lấy mong đợi từ đề bài chứ không từ mã, và thêm ca ở đúng mỗi mốc.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Tin rằng ca dùng đối tượng giả đã kiểm được bên ngoài.
Đối tượng giả trả <code>true</code> vì <b>ta dặn</b> nó thế. Nếu cổng thật đổi cách trả lời, mọi ca vẫn đạt.
<b class="red">Đối tượng giả kiểm cách mã của ta gọi bên ngoài, không kiểm bên ngoài chạy đúng.</b>
<br><span class="note">Cách chữa: giữ thêm một số ít ca gọi môi trường thử của cổng; không dặn giả nhiều hơn điều ca kiểm cần.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là tin rằng ca dùng đối tượng giả đã kiểm được bên ngoài. Giả trả lời đúng chỉ vì ta dặn, nên cổng thật đổi cách trả lời thì mọi ca vẫn đạt. Cách chữa là giữ thêm ít ca gọi môi trường thử.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Ca kiểm <b class="red">lúc đạt lúc trượt</b> vì phụ thuộc thứ nằm ngoài ca:
<b>đồng hồ thật</b> (lệnh sau 22 giờ tính sang ngày kế, số minh hoạ: ca chạy ban ngày thì đạt, bản dựng ban đêm thì trượt),
<b>mạng</b> (gọi dịch vụ thật), <b>thứ tự chạy</b> (ca sau dùng dữ liệu ca trước để lại).
<br><span class="note">Cách chữa: đưa đồng hồ vào làm tham số (<code>java.time.Clock</code>) rồi cho ca kiểm một đồng hồ đứng yên; thay mạng bằng đối tượng giả; mỗi ca tự sắp đặt dữ liệu của mình.</span>
<br><span class="note">JUnit mặc định tạo một đối tượng mới của lớp kiểm thử cho mỗi ca, nên biến khai trong lớp (như đối tượng giả) không rò sang ca khác; dữ liệu tĩnh hay dữ liệu bên ngoài (tệp, cơ sở dữ liệu) thì có thể rò.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm: ca kiểm lúc đạt lúc trượt vì phụ thuộc thứ nằm ngoài ca, như đồng hồ thật, mạng, hoặc dữ liệu ca trước để lại. Cách chữa là đưa đồng hồ vào làm tham số, thay mạng bằng đối tượng giả, và để mỗi ca tự sắp đặt dữ liệu.""", clear=True),
        st(code(JAVA_CLOCK, "Đồng hồ là tham số: ca kiểm tự chọn thời điểm"),
           """Hàm kiểm giờ chốt nhận đồng hồ làm tham số thay vì hỏi giờ của máy. Ta tạo đồng hồ đứng yên ở hai mươi mốt giờ năm mươi chín, rồi sáu mươi giây sau.""", clear=True),
        st(out(OUT_CLOCK),
           """Kết quả chạy thật: trước giờ chốt một phút thì đúng, tại giờ chốt thì sai, và chạy lúc nào cũng ra hai dòng này.""", clear=True),
    ], checks=["alg.bnx_jt_fee_run(True)[0] == 3 and alg.bnx_jt_fee(10_000_000, True) != alg.bnx_jt_fee(10_000_000)",
               "alg.bnx_jt_before_cutoff(21, 59) and not alg.bnx_jt_before_cutoff(22, 0)",
               "alg.bnx_jt_before_cutoff(15, 0) and not alg.bnx_jt_before_cutoff(22, 30)"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Theo đề, phí của 499 999, của 500 000 và của 9 999 999 đồng là bao nhiêu? Với mã còn lỗi <code>&lt;=</code>, ca nào trong ba ca này trượt?"],
                  ["2", "Mã đã sửa. Chuyển 20 000 000 đồng từ TK01: lệnh kiểm tương tác phải đòi cổng được gọi mấy lần, với số tiền nào?"],
                  ["3", "Quyết định (số minh hoạ): 100 ca kiểm. Ca dùng đối tượng giả chạy 10 mili giây, ca gọi cổng thử thật chạy 2 000 mili giây. Toàn giả, toàn thật, hay 90 giả + 10 thật?"]]),
           """Đến lượt bạn. Câu một, theo đề thì phí của ba số tiền trên màn hình là bao nhiêu, với mã còn lỗi thì ca nào trượt? Câu hai, chuyển hai mươi triệu thì cổng được gọi mấy lần? Câu ba, chọn cách nào cho một trăm ca? Hãy tạm dừng và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: 499 999 dưới mốc 500 000; hai số kia nằm từ 500 000 tới dưới 10 000 000.</p>
$$499\\,999 \\to \\hlg{0}; \\quad 500\\,000 \\to \\hlg{5000}; \\quad 9\\,999\\,999 \\to \\hlg{5000}$$
<p>Mã còn lỗi cũng trả đúng ba giá trị này: <b>không ca nào trượt</b>. Chỉ ca ở đúng 10 000 000 mới bắt được lỗi.</p>""",
           """Đáp án câu một. Số thứ nhất dưới mốc nên phí bằng không, hai số kia nằm giữa hai mốc nên phí năm nghìn. Mã còn lỗi cũng trả đúng ba giá trị này, nên chỉ ca ở đúng mười triệu bắt được lỗi."""),
        st("""<p>Câu 2: 20 000 000 từ mốc 10 000 000 trở lên nên phí 5 500.</p>
$$20\\,000\\,000 + 5\\,500 = \\hlg{20\\,005\\,500}; \\quad \\text{đúng } \\hlg{1} \\text{ lần}$$""",
           """Đáp án câu hai. Hai mươi triệu từ mốc mười triệu trở lên nên phí năm nghìn năm trăm. Lệnh kiểm tương tác đòi cổng gọi đúng một lần, với hai mươi triệu không trăm linh năm nghìn năm trăm."""),
        st(table(["lựa chọn", "thời gian một lượt", "được", "mất"],
                 [["100 ca dùng đối tượng giả", "100 × 10 = 1 000 mili giây", "nhanh, chạy sau mỗi lần sửa", "không biết cổng thật có trả lời như ta dặn"],
                  ["100 ca gọi cổng thử thật", "100 × 2 000 = 200 000 mili giây", "kiểm được cả cổng", "chậm 200 lần; mạng rớt thì ca trượt oan"],
                  ["90 giả + 10 thật", "90 × 10 + 10 × 2 000 = 20 900 mili giây", "phần xử lý kiểm nhanh, vẫn có ca canh cổng", "phải nuôi hai loại ca, ca thật chạy riêng"]]),
           """Đáp án câu ba, không có lựa chọn nào chỉ toàn được. Toàn giả thì một lượt mất một nghìn mili giây nhưng không biết cổng thật. Toàn thật thì chậm gấp hai trăm lần và mạng rớt thì trượt oan. Chín mươi giả cộng mười thật mất hai mươi nghìn chín trăm mili giây.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["[alg.bnx_jt_fee(a) for a in (499_999, 500_000, 9_999_999)] == [0, 5000, 5000]",
               "[alg.bnx_jt_fee(a, True) for a in (499_999, 500_000, 9_999_999)] == [alg.bnx_jt_fee(a) for a in (499_999, 500_000, 9_999_999)]",
               "alg.bnx_jt_transfer(20_000_000) == (5500, [('TK01', 20_005_500)])",
               "alg.bnx_jt_suite_ms(100, 0) == 1000", "alg.bnx_jt_suite_ms(0, 100) == 200_000", "alg.bnx_jt_suite_ms(90, 10) == 20_900",
               "alg.bnx_jt_suite_ms(0, 100) // alg.bnx_jt_suite_ms(100, 0) == 200"])

    lab_pr = practice_scene(sc, "Tự làm: ca kiểm, cổng giả đếm lời gọi, đồng hồ đứng yên", practice_steps2(
        st, "BNX", "L18",
        """<p><b>Đề</b>: viết <code>Lab.java</code> (chỉ JDK, không thư viện). Hàm <code>tinh</code> phí rút tiền cho sẵn trong <code>de.md</code> (mốc 2 000 000 và 20 000 000; mã còn nhầm dấu ở mốc sau):</p>
<ol><li><code>ca(vao, mongDoi)</code>: so, đếm đạt/trượt, in <code>ca … : mong doi …, nhan …, DAT/TRUOT</code> cho 5 số tiền, rồi <code>tong: … dat, … truot</code></li>
<li>cổng giả bằng lambda đếm lời gọi: <code>cong goi … lan, so tien …</code> khi chuyển 12 000 000</li>
<li>hai dòng <code>kip(Clock.fixed(…))</code> ở 16:59 và 17:00 (+07)</li></ol>
<p class="note">Lab là <b>mô hình Java thuần</b>: không dùng JUnit hay Mockito, ta tự viết phần so và cổng giả bằng lambda. Mong đợi lấy từ đề, không từ mã. Số liệu khác ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm. Đề cho sẵn hàm tính phí rút tiền hai mốc, mã nhầm một dấu ở mốc thứ hai. Hãy viết ca kiểm cho năm số tiền, cổng giả đếm lời gọi, và hai ca đồng hồ.""",
        LAB_OUT, "Lab.java",
        """<div class="box key"><b>Nếu kẹt:</b> mong đợi lấy từ đề: 2 000 000 là mốc, nên số tiền đúng mốc thuộc khoảng sau. Cổng giả: <code>long[] ghi = new long[2]; Cong gia = (tk, so) -> { ghi[0]++; ghi[1] = so; return true; };</code>.
Lời giải đầy đủ ở <code>labs/BNX/L18/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, nhớ mong đợi lấy từ đề chứ không từ mã, và số tiền đúng mốc thuộc khoảng sau. Lời giải chỉ mở sau khi đã tự thử.""", pause=240), "BNX", "L18")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mỗi nhánh một ca", "thêm ca ở mốc biên", "đọc bản báo: mong đợi và thực nhận", "thay bên ngoài bằng đối tượng giả", "kiểm lời gọi: 1 lần, đúng tham số"),
           """Tổng kết chuỗi lập luận. Mỗi nhánh một ca, mỗi mốc thêm ca ở đúng mốc. Ca trượt thì bản báo ghi mong đợi và thực nhận. Phần bên ngoài thay bằng đối tượng giả, rồi kiểm lời gọi đúng một lần."""),
        st("""<div class='box key'><b>Tư duy:</b> ca kiểm đạt chỉ nói về những trường hợp đã kiểm; đối tượng giả chỉ nói về cách mã của ta gọi ra ngoài.
Ca nào phụ thuộc đồng hồ thật, mạng hay thứ tự chạy thì sớm muộn cũng lúc đạt lúc trượt.</div>""",
           """Ca kiểm đạt chỉ nói về những trường hợp đã kiểm, còn đối tượng giả chỉ nói về cách mã gọi ra ngoài. Ca phụ thuộc đồng hồ thật, mạng hay thứ tự chạy thì sớm muộn lúc đạt lúc trượt."""),
        st(table(["Nếu bị hỏi về dòng “automated tests (JUnit 5, Mockito)” trên CV", "ý trả lời một dòng"],
                 [["Bạn chọn ca kiểm cho một hàm thế nào?", "mỗi nhánh một ca, thêm ca ở đúng mốc biên; giá trị mong đợi lấy từ đề, không từ mã"],
                  ["Khi nào dùng đối tượng giả, và nó không kiểm được gì?", "khi phần phụ thuộc chậm, cần mạng hay tốn tiền; nó chỉ kiểm cách ta gọi, nên vẫn cần ít ca gọi môi trường thử"],
                  ["Gặp ca lúc đạt lúc trượt thì làm gì?", "tìm phụ thuộc ẩn: đồng hồ, mạng, thứ tự, dữ liệu dùng chung; đưa đồng hồ vào làm tham số"]]),
           """Người phỏng vấn hay hỏi ba câu. Chọn ca kiểm: mỗi nhánh một ca, thêm ca ở mốc biên. Dùng đối tượng giả khi phần phụ thuộc chậm. Ca lúc đạt lúc trượt thì tìm đồng hồ, mạng, thứ tự chạy.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Bài sau: Redis nâng cao, gồm cụm nhiều nút, khoá có hạn và khử trùng yêu cầu gửi lại.</p>""",
           """Bài mười chín sang Redis nâng cao, gồm cụm nhiều nút, khoá có hạn và cách khử trùng yêu cầu gửi lại.""",
           forward_ref=True),
    ], checks=["alg.bnx_jt_fee_branches() == 3", "alg.bnx_jt_transfer(2_000_000)[1] == [('TK01', 2_005_000)]"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L18", "junit5_mockito", "Bài 18 — Kiểm thử Java với JUnit 5 và Mockito: ca kiểm, đối tượng giả và kiểm tương tác",
                  "curriculum/bnx.yaml L18; audit/bnx/verify_bnx.py L18; JUnit 5.14.4 User Guide (docs.junit.org/5.14.4: Annotations, "
                  "Test Instance Lifecycle, Test Execution Order, Console Launcher); Mockito 5.24.0 Javadoc lớp Mockito; "
                  "Java SE 21 API java.time.Clock (đọc 2026-11-11; audit/bnx/sources_l18.md); chạy thật JUnit Platform 1.14.4 + Mockito 5.24.0 trên JDK 21",
                  ["Lập ca kiểm cho từng nhánh của một hàm (đọc ca JUnit 5 trên màn hình, tự lập ca ở lab) và đọc bản báo ca trượt",
                   "Thay phần phụ thuộc bên ngoài bằng đối tượng giả (đọc cách Mockito làm, tự viết cổng giả bằng hàm ở lab)",
                   "Kiểm một lời gọi đã xảy ra đúng số lần với đúng tham số",
                   "Chỉ ra ca kiểm dễ vỡ vì phụ thuộc đồng hồ, mạng hay thứ tự chạy"],
                  scenes,
                  covers=[(1, "practice"), (2, "example"), (3, "example"), (4, "pitfalls")], assumes=["bnx_classpath"])


# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
write_lab("BNX", "L18", LAB_DE, "java", LAB_JAVA, LAB_OUT)
