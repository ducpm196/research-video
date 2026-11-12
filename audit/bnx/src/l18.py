from lib import *

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


def build():
    hook = sc("hook", "hook", "Một dấu bằng thừa, mỗi giao dịch thu thiếu 500 đồng", [
        st("""<p>Ngân hàng tính phí chuyển tiền (số minh hoạ): từ <b>10 000 000</b> đồng trở lên thu <b>5 500</b> đồng.
Lập trình viên viết nhầm <code>&lt;=</code> thay cho <code>&lt;</code>, nên khách chuyển <b>đúng 10 000 000</b> chỉ bị thu <b>5 000</b>.</p>
<div class="box key">Mỗi giao dịch thu thiếu 5 500 − 5 000 = <b>500</b> đồng. Với 20 000 giao dịch đúng mốc mỗi tháng (số minh hoạ): 20 000 × 500 = <b>10 000 000</b> đồng.
Thử tay ba số tiền bất kỳ đều thấy đúng. Làm sao để máy tự bắt lỗi này trước khi lên chạy thật?</div>""",
           """Chào bạn, ngân hàng tính phí chuyển tiền bằng số minh hoạ: từ mười triệu đồng trở lên thì thu năm nghìn năm trăm đồng.
           Lập trình viên viết nhầm một dấu so sánh, nên khách chuyển đúng mười triệu chỉ bị thu năm nghìn đồng.
           Mỗi giao dịch thu thiếu năm trăm đồng, nên hai mươi nghìn giao dịch đúng mốc mỗi tháng làm thu thiếu mười triệu đồng.
           Thử tay ba số tiền bất kỳ đều thấy đúng, vậy làm sao để máy tự bắt lỗi này trước khi lên chạy thật?""", focus=[1, 1, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["viết ca kiểm tự động thế nào, đọc bản báo ra sao", "JUnit 5: mỗi nhánh một ca, thêm ca ở mốc biên; bản báo ghi mong đợi và thực nhận"],
                  ["hàm gọi ra cổng thanh toán thì kiểm sao", "Mockito: thay cổng bằng đối tượng giả, rồi kiểm lời gọi đúng số lần, đúng tham số"],
                  ["vì sao có ca lúc đạt lúc trượt", "ca phụ thuộc đồng hồ thật, mạng hay thứ tự chạy"]]),
           """Hôm nay ta trả lời ba câu hỏi về kiểm thử tự động trong Java, nơi ca kiểm là một đoạn mã nhỏ chạy hàm cần kiểm rồi so kết quả với giá trị mong đợi. Thứ nhất, viết ca kiểm tự động thế nào và đọc bản báo ca trượt ra sao.
           Thứ hai, khi hàm gọi ra cổng thanh toán bên ngoài thì kiểm bằng cách nào. Thứ ba, vì sao có những ca kiểm lúc đạt lúc trượt.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_jt_fee(10_000_000) == 5500", "alg.bnx_jt_fee(10_000_000, True) == 5000",
               "alg.bnx_jt_fee(10_000_000) - alg.bnx_jt_fee(10_000_000, True) == 500",
               "20_000 * (alg.bnx_jt_fee(10_000_000) - alg.bnx_jt_fee(10_000_000, True)) == 10_000_000"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① nhánh của một hàm", "mỗi câu <code>if</code> rẽ hàm thành các đường đi khác nhau; mỗi đường đi là một nhánh", "2 mốc so sánh cắt trục số tiền thành 3 khoảng, tức 3 nhánh"],
                  ["② giao diện (<code>interface</code>)", "bản kê tên các hàm, chưa có thân hàm; lớp nào viết đủ các hàm đó thì dùng thay cho nhau được", "<code>CongThanhToan</code> có một hàm <code>chuyen</code>"],
                  ["③ phần phụ thuộc bên ngoài", "thứ mã của ta gọi tới nhưng không do ta điều khiển", "cổng thanh toán, cơ sở dữ liệu, đồng hồ, mạng"],
                  ["④ ngoại lệ (<code>exception</code>)", "cách một hàm báo lỗi: dừng ngay và ném lỗi ra cho nơi gọi", "cổng từ chối thì ném <code>IllegalStateException</code>"]]),
           """Trước hết ta cần hiểu bốn điều sẽ dùng trong cả bài. Thứ nhất, mỗi câu điều kiện rẽ hàm thành các đường đi khác nhau, mỗi đường đi gọi là một nhánh.
           Thứ hai, giao diện là bản kê tên các hàm mà chưa có thân hàm, nên lớp nào viết đủ các hàm đó thì dùng thay cho nhau được.
           Thứ ba, phần phụ thuộc bên ngoài là thứ mã của ta gọi tới nhưng không điều khiển được, như cổng thanh toán hay đồng hồ.
           Thứ tư, ngoại lệ là cách một hàm báo lỗi, vì nó dừng ngay và ném lỗi ra cho nơi gọi.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st("""<p>Làm thử: theo đề, chuyển 2 000 000 đồng thì phí 5 000 đồng, nên số tiền trừ ở cổng là</p>
$$2\\,000\\,000 + 5\\,000 = \\hl{2\\,005\\,000}\\ \\text{đồng}$$""",
           """Làm thử ngay với đề phí của bài. Chuyển hai triệu đồng thì phí là năm nghìn đồng, vì hai triệu nằm giữa hai mốc.
           Vậy số tiền mà cổng thanh toán phải trừ là hai triệu không trăm linh năm nghìn đồng."""),
    ], checks=["alg.bnx_jt_fee_branches() == 3", "alg.bnx_jt_fee(2_000_000) == 5000", "2_000_000 + alg.bnx_jt_fee(2_000_000) == 2_005_000"])

    sym = sc("sym", "symbol", "Giải mã các từ của JUnit 5 và Mockito", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["JUnit 5", "bộ khung kiểm thử của Java: tìm các ca kiểm, chạy từng ca, in bản báo"],
                  ["<code>@Test</code>", "nhãn gắn trước một hàm để báo: đây là một ca kiểm"],
                  ["<code>assertEquals(mong đợi, thực tế)</code>", "so hai giá trị; khác nhau thì ca <b>trượt</b> và bản báo ghi cả hai"],
                  ["<code>assertThrows(loại lỗi, đoạn mã)</code>", "ca chỉ đạt khi đoạn mã ném đúng loại lỗi đó"]]),
           """Bảng này giải mã các từ của bộ khung kiểm thử, tên gốc hiện trên màn hình. Bộ khung tìm các ca kiểm, chạy từng ca, rồi in bản báo.
           Nhãn a còng đặt trước một hàm để báo với bộ khung rằng hàm đó là một ca kiểm.
           Lệnh so bằng nhận giá trị mong đợi trước, giá trị thực tế sau, và nếu hai giá trị khác nhau thì ca trượt.
           Lệnh chờ lỗi thì ngược lại, vì ca chỉ đạt khi đoạn mã bên trong ném đúng loại lỗi đã nêu.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["Mockito", "thư viện tạo <b>đối tượng giả</b> (mock) từ một giao diện hay một lớp"],
                  ["<code>mock(X.class)</code>", "tạo đối tượng giả của X: có đủ các hàm của X nhưng không làm gì, chỉ <b>ghi lại</b> mọi lời gọi"],
                  ["<code>when(lời gọi).thenReturn(giá trị)</code>", "dặn trước: gặp đúng lời gọi này thì trả giá trị này; chưa dặn thì trả giá trị mặc định (<code>false</code>, 0, <code>null</code>)"],
                  ["<code>verify(giả, times(1)).hàm(tham số)</code>", "kiểm tương tác: lời gọi này đã xảy ra đúng 1 lần, đúng tham số; <code>times(1)</code> là mặc định"]]),
           """Bảng thứ hai là các từ của thư viện tạo đối tượng giả. Đối tượng giả có đủ các hàm của giao diện, nhưng không làm gì cả, chỉ ghi lại mọi lời gọi.
           Lệnh tạo nhận tên giao diện và trả về một đối tượng giả của giao diện đó.
           Lệnh dặn trước nói rằng gặp đúng lời gọi này thì trả giá trị này, còn chưa dặn thì đối tượng giả trả giá trị mặc định, ví dụ sai.
           Lệnh kiểm tương tác hỏi lại đối tượng giả, vì ta cần biết lời gọi đã xảy ra đúng một lần với đúng tham số hay chưa.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
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
           """Hình này cho thấy một ca kiểm chỉ gồm ba việc. Việc một là sắp đặt đầu vào, ở đây là số tiền mười triệu đồng.
           Việc hai là gọi hàm tính phí và nhận về giá trị thực tế là năm nghìn.
           Việc ba là so với giá trị mong đợi lấy từ đề bài là năm nghìn năm trăm, và vì hai số khác nhau nên ca trượt."""),
        st(svg(1500, 470,
               box(40, 170, 260, 110, ["ca kiểm", "ChuyenTienTest"], C_BLUE, 24, True),
               box(420, 170, 320, 110, ["dịch vụ ChuyenTien", "(mã của ta)"], C_PURPLE, 24, True),
               box(900, 40, 540, 110, ["cổng thanh toán thật", "mạng, chậm, trừ tiền thật"], C_GRAY, 24, True, dash=True),
               box(900, 300, 540, 110, ["đối tượng giả (mock)", "trả lời như đã dặn, ghi lại lời gọi"], C_GREEN, 24, True),
               arrow(305, 225, 415, 225), arrow(745, 200, 895, 110, "#6b7280", dash=True), arrow(745, 250, 895, 340, "#16a34a"),
               txt(770, 120, "không dùng", 22, "middle", "#6b7280"), txt(815, 330, "thay vào", 22, "middle", "#16a34a"),
               arrow(895, 385, 310, 270, "#2a78d6"), txt(560, 380, "hỏi lại: gọi mấy lần, tham số gì", 22, "middle", "#2a78d6"),
               txt(750, 455, "Cùng một giao diện CongThanhToan: dịch vụ không biết mình đang gọi đồ thật hay đồ giả", 24, "middle", "#1f2937", True)),
           """Hình thứ hai cho thấy vai của đối tượng giả. Dịch vụ chuyển tiền là mã của ta, và nó gọi ra cổng thanh toán qua một giao diện.
           Cổng thật thì cần mạng, chạy chậm và trừ tiền thật, nên trong ca kiểm ta thay nó bằng đối tượng giả có cùng giao diện.
           Đối tượng giả trả lời như đã dặn và ghi lại lời gọi, nên cuối ca kiểm ta hỏi lại nó đã được gọi mấy lần, với tham số gì."""),
    ], checks=["alg.bnx_jt_fee(10_000_000, True) == 5000 and alg.bnx_jt_fee(10_000_000) == 5500",
               "alg.bnx_jt_fee_run(True)[2] == [('bien', 5500, 5000)]"])

    form = sc("formula", "formula", "Suy ra từng bước: từ thử tay tới kiểm tương tác", [
        st("""<p><b>Bước 1.</b> Thử tay thì mỗi lần sửa mã lại phải thử lại, và sẽ có lần quên. <b>Ca kiểm</b> là một hàm nhỏ: gọi hàm cần kiểm rồi so với giá trị mong đợi, nên máy chạy lại được sau mỗi lần sửa.</p>
<span class='note'>Làm thử: <code>assertEquals(0, Phi.tinh(200_000))</code>, vì 200 000 dưới mốc 500 000 nên đề cho phí 0.</span>""",
           """Bước một, thử tay thì mỗi lần sửa mã lại phải thử lại, và sẽ có lần quên. Vì vậy ta viết ca kiểm, là một hàm nhỏ gọi hàm cần kiểm rồi so với giá trị mong đợi.
           Làm thử, hai trăm nghìn đồng nằm dưới mốc năm trăm nghìn, nên giá trị mong đợi là không đồng.""", clear=True),
        st("""<p><b>Bước 2.</b> Nhánh nào không chạy trong ca kiểm thì lỗi trong nhánh đó không lộ ra, nên <b>mỗi nhánh cần ít nhất một ca</b>.</p>
$$\\text{2 mốc} \\;\\Rightarrow\\; 2 + 1 = \\hl{3}\\ \\text{nhánh} \\;\\Rightarrow\\; \\text{ít nhất 3 ca}$$""",
           """Bước hai, nhánh nào không chạy trong ca kiểm thì lỗi trong nhánh đó không lộ ra, nên mỗi nhánh cần ít nhất một ca.
           Làm thử, hàm phí có hai mốc so sánh, cắt trục số tiền thành ba khoảng, nên có ba nhánh và cần ít nhất ba ca."""),
        st("""<p><b>Bước 3.</b> Ba ca ở <b>giữa</b> ba khoảng vẫn chưa chạm tới dấu so sánh. Lỗi <code>&lt;</code> thành <code>&lt;=</code> chỉ lộ ở <b>đúng mốc</b>, nên thêm ca ở mốc biên.</p>
<span class='note'>Làm thử: tại đúng 10 000 000, đề cho 5 500; mã viết <code>&lt;=</code> trả 5 000. Ba ca kia vẫn đạt.</span>""",
           """Bước ba, ba ca ở giữa ba khoảng vẫn chưa chạm tới dấu so sánh. Lỗi nhầm dấu chỉ lộ ra ở đúng mốc, nên ta thêm một ca ở mốc biên.
           Làm thử, tại đúng mười triệu đồng thì đề cho năm nghìn năm trăm, còn mã viết nhầm trả năm nghìn.""", clear=True),
        st("""<p><b>Bước 4.</b> Dịch vụ chuyển tiền gọi ra cổng thanh toán. Gọi cổng thật trong ca kiểm thì chậm, cần mạng và trừ tiền thật.
Vì dịch vụ chỉ biết <b>giao diện</b> <code>CongThanhToan</code> và nhận cổng qua hàm khởi tạo, ca kiểm đưa vào một <b>đối tượng giả</b>.</p>
<span class='note'>Làm thử: dặn giả trả <code>true</code> khi được gọi với TK01 và 2 000 000 + 5 000 = 2 005 000.</span>""",
           """Bước bốn, dịch vụ chuyển tiền gọi ra cổng thanh toán, mà gọi cổng thật trong ca kiểm thì chậm, cần mạng và trừ tiền thật.
           Vì dịch vụ chỉ biết giao diện của cổng và nhận cổng qua hàm khởi tạo, nên ca kiểm đưa vào một đối tượng giả.
           Làm thử, ta dặn đối tượng giả trả lời đúng, khi được gọi với số tiền hai triệu không trăm linh năm nghìn.""", clear=True),
        st("""<p><b>Bước 5.</b> Giá trị trả về đúng vẫn chưa đủ. Gọi cổng <b>0 lần</b> thì tiền không đi; gọi <b>2 lần</b> thì khách bị trừ hai lần.
Nên ca kiểm hỏi lại đối tượng giả: lời gọi đã xảy ra <b>đúng 1 lần</b> với <b>đúng tham số</b> chưa. Đó là <b>kiểm tương tác</b>.</p>
<span class='note'>Làm thử: <code>verify(cong, times(1)).chuyen("TK01", 2_005_000)</code>.</span>""",
           """Bước năm, giá trị trả về đúng vẫn chưa đủ, vì gọi cổng không lần nào thì tiền không đi, còn gọi hai lần thì khách bị trừ hai lần.
           Nên ca kiểm hỏi lại đối tượng giả, rằng lời gọi đã xảy ra đúng một lần với đúng tham số hay chưa, và đó là kiểm tương tác.
           Làm thử, ta đòi đúng một lời gọi với tài khoản không một và số tiền hai triệu không trăm linh năm nghìn.""", clear=True),
    ], checks=["alg.bnx_jt_fee(200_000) == 0", "alg.bnx_jt_fee_branches() == 2 + 1 == 3",
               "alg.bnx_jt_fee_run(True)[:2] == (3, 1)", "alg.bnx_jt_transfer(2_000_000)[1] == [('TK01', 2_005_000)]"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st(code(JAVA_PHI, "Phi.java: hàm tính phí, còn một lỗi ở dấu so sánh"),
           """Đây là hàm tính phí viết bằng Java, kèm đề bài ghi ở phần chú thích phía trên. Đề có ba mức: dưới năm trăm nghìn thì miễn phí, tới dưới mười triệu thì năm nghìn, còn lại là năm nghìn năm trăm.
           Thân hàm có hai câu điều kiện ứng với hai mốc. Câu thứ hai viết nhỏ hơn hoặc bằng mười triệu, và đó chính là chỗ sai so với đề.""",
           focus=[1, ["2.2", "2.3", "2.4", "2.5"], ["2.7", "2.8", "2.9"], "2.8"], clear=True),
        st("""$$① \\; \\text{2 mốc} \\Rightarrow 2 + 1 = \\hl{3}\\ \\text{nhánh} \\Rightarrow \\text{ít nhất 3 ca kiểm}$$""",
           """Phép tính thứ nhất. Hàm có hai mốc so sánh nên có ba nhánh, vì vậy ta cần ít nhất ba ca kiểm, mỗi nhánh một ca."""),
        st(code(JAVA_PHITEST, "PhiTest.java: bốn ca kiểm viết bằng JUnit 5"),
           """Đây là lớp kiểm thử với bốn ca, mỗi ca là một hàm có gắn nhãn ca kiểm. Ba ca đầu lấy số tiền ở giữa ba khoảng: hai trăm nghìn, hai triệu và năm mươi triệu.
           Mỗi ca so giá trị mong đợi theo đề với giá trị hàm trả về. Ca thứ tư đặt ở đúng mốc mười triệu, nơi đề cho năm nghìn năm trăm.""",
           focus=[1, ["2.5", "2.6", "2.7"], ["2.5", "2.6", "2.7"], "2.8"], clear=True),
        st(code(SH_PHI, "Biên dịch rồi chạy bằng JUnit Platform (thư viện nằm trong thư mục lib)"),
           """Máy không cần công cụ dựng nào, chỉ cần bộ Java và một tệp thư viện của bộ khung kiểm thử.
           Lệnh thứ nhất biên dịch hai tệp nguồn, với thư viện nằm trong đường dẫn lớp. Lệnh thứ hai chạy bộ khung, chỉ cho nó thư mục chứa lớp đã dịch và tên lớp kiểm thử.""",
           focus=[1, "2.1", ["2.2", "2.3", "2.4"]], clear=True),
        st(out(OUT_PHI),
           """Đây là bản báo chạy thật, mỗi ca một dòng, có đánh dấu đạt hoặc trượt. Ba ca ở giữa khoảng đều đạt, còn ca ở mốc biên thì trượt.
           Dòng trượt ghi rõ giá trị mong đợi là năm nghìn năm trăm nhưng nhận về năm nghìn. Bên dưới, bản báo chỉ tới đúng tệp và hàm kiểm bị trượt.
           Ba dòng cuối là tổng kết: tìm thấy bốn ca, ba ca đạt, một ca trượt.""",
           focus=[1, ["2.3", "2.4", "2.5", "2.6"], "2.5", "2.8", ["2.10", "2.11", "2.12"]], clear=True),
        st("""$$② \\; 3\\ \\text{đạt} + 1\\ \\text{trượt} = \\hl{4}\\ \\text{ca}$$
$$③ \\; \\text{mong đợi } 5500,\\ \\text{nhận } 5000:\\quad 5500 - 5000 = \\hl{500}\\ \\text{đồng thu thiếu}$$
<p>Thứ tự chạy là phiCao, phiVua, bien, mienPhi: <b>không</b> theo thứ tự viết trong tệp.</p>
<p style='margin-top:18px'><b>Bộ bốn ca này còn hở:</b> hàm có hai mốc nhưng chỉ có ca ở đúng mốc 10 000 000. Lỗi tương tự ở mốc 500 000 vẫn lọt, vì cả bốn ca vẫn đạt.</p>
<p style='margin-top:18px'><span class='note'>Quy tắc của bài là mỗi mốc một ca ở đúng mốc, nên cần thêm ca ở 500 000 và 499 999; câu 1 cuối bài tính các giá trị ấy. Nhiều ca cùng khuôn chỉ khác số thì dùng ca kiểm có tham số cho gọn.</span></p>""",
           """Phép tính thứ hai. Ba ca đạt cộng một ca trượt là đủ bốn ca đã viết, nên không ca nào bị bỏ sót.
           Phép tính thứ ba. Mong đợi năm nghìn năm trăm mà nhận năm nghìn, tức thu thiếu năm trăm đồng, đúng bằng con số ở đầu bài.
           Để ý thêm, bộ khung chạy các ca không theo thứ tự viết trong tệp, nên các ca không được dựa vào nhau.
           Cũng để ý, bộ bốn ca này còn hở, vì hàm có hai mốc mà chỉ có ca ở đúng mười triệu, nên lỗi tương tự ở năm trăm nghìn vẫn lọt.
           Theo quy tắc của bài, cần thêm ca ở đúng năm trăm nghìn và sát dưới nó, và câu một cuối bài tính các giá trị ấy.""", clear=True),
        st(code(SH_FIX, "Sửa dấu so sánh, chạy lại cả bốn ca"),
           """Bây giờ ta sửa lỗi. Lệnh thứ nhất đổi dấu nhỏ hơn hoặc bằng thành dấu nhỏ hơn ngay trong tệp nguồn của hàm phí.
           Hai lệnh sau biên dịch lại và chạy lại cả bốn ca, lần này chỉ xin in phần tổng kết.""",
           focus=["2.1", "2.1", ["2.2", "2.3", "2.4", "2.5"]], clear=True),
        st(out(OUT_FIX),
           """Kết quả chạy thật sau khi sửa: tìm thấy bốn ca, cả bốn ca đạt, không ca nào trượt. Ba ca cũ vẫn đạt, nên chỗ sửa không làm hỏng nhánh nào khác."""),
        st(code(JAVA_DV, "ChuyenTien.java: dịch vụ gọi ra cổng thanh toán qua một giao diện"),
           """Sang phần thứ hai, đây là dịch vụ chuyển tiền. Trên cùng là giao diện của cổng thanh toán, chỉ có một hàm nhận tài khoản và số tiền, trả về đúng hoặc sai.
           Dịch vụ nhận cổng qua hàm khởi tạo, nên bên ngoài đưa cổng nào vào thì nó dùng cổng đó.
           Hàm chuyển tính phí, rồi gọi cổng với số tiền cộng phí. Nếu cổng trả lời sai thì hàm ném lỗi, còn không thì trả về phí.""",
           focus=[1, "2.1", ["2.4", "2.5"], ["2.7", "2.8"], ["2.9", "2.10"]], clear=True),
        st(code(JAVA_DVTEST, "ChuyenTienTest.java: thay cổng bằng đối tượng giả của Mockito"),
           """Đây là ca kiểm cho dịch vụ, có dùng thư viện tạo đối tượng giả. Trước hết ta tạo một đối tượng giả từ giao diện của cổng thanh toán.
           Trong ca kiểm, ta dặn đối tượng giả trả lời đúng khi được gọi với tài khoản không một và hai triệu không trăm linh năm nghìn.
           Tiếp theo ta gọi dịch vụ chuyển hai triệu đồng và so phí trả về với năm nghìn.
           Dòng cuối là kiểm tương tác, đòi cổng đã được gọi đúng một lần với đúng hai tham số đó.""",
           focus=[1, "2.5", "2.7", ["2.8", "2.9"], "2.10"], clear=True),
        st("""$$④ \\; \\text{tham số gọi cổng:}\\quad 2\\,000\\,000 + 5\\,000 = \\hl{2\\,005\\,000}$$""",
           """Phép tính thứ tư. Số tiền dịch vụ đưa cho cổng là hai triệu cộng phí năm nghìn ở phép trước, tức hai triệu không trăm linh năm nghìn, đúng bằng tham số ta đòi."""),
        st(code(JAVA_TUCHOI, "TuChoiTest.java: cổng từ chối thì sao?"),
           """Ca kiểm tiếp theo xét trường hợp cổng từ chối. Lần này ta không dặn gì, nên đối tượng giả trả giá trị mặc định là sai.
           Lệnh chờ lỗi đòi dịch vụ phải ném đúng loại lỗi khi chuyển hai triệu đồng.
           Dòng cuối vẫn đòi đúng một lời gọi, vì dịch vụ không được tự ý gọi lại cổng lần thứ hai.""",
           focus=[1, ["2.5", "2.7"], ["2.8", "2.9"], "2.10"], clear=True),
        st(code(SH_MOCK, "Biên dịch tất cả, chạy hai lớp kiểm thử có Mockito"),
           """Lệnh chạy lần này dài hơn, vì thư viện tạo đối tượng giả cần thêm ba thư viện đi kèm. Lệnh thứ nhất biên dịch mọi tệp nguồn.
           Lệnh thứ hai thêm từng thư viện vào đường dẫn lớp, rồi chọn hai lớp kiểm thử vừa viết.""",
           focus=[1, "2.1", ["2.2", "2.3", "2.4", "2.5", "2.6", "2.7"]], clear=True),
        st(out(OUT_MOCK),
           """Kết quả chạy thật cho thấy cả hai ca đều đạt. Ca thứ nhất xác nhận cổng được gọi đúng một lần với đúng số tiền.
           Ca thứ hai xác nhận khi cổng từ chối thì dịch vụ ném lỗi và cũng chỉ gọi một lần. Tổng kết ghi hai ca, hai ca đạt, không ca nào trượt.""",
           focus=[1, "2.3", "2.5", ["2.7", "2.8", "2.9"]], clear=True),
        st("""<div class="box warn"><b>Một dòng cảnh báo lạ.</b> Ngoài bản báo trên, Java 21 còn in cảnh báo ra luồng lỗi:
Mockito tự gắn một tác tử vào chính nó để tạo đối tượng giả, mà từ Java 21 JDK hạn chế việc đó (hướng dẫn Mockito).
<br><span class="note">Cảnh báo không làm ca nào trượt; đó là kết quả quan sát khi chạy thật.</span></div>""",
           """Java hai mươi mốt còn in thêm một cảnh báo ra luồng lỗi, vì thư viện giả tự gắn một tác tử vào chính nó, việc mà Java này hạn chế.
           Cảnh báo không làm ca nào trượt, và đó là điều quan sát được khi chạy thật.""", clear=True),
        st("""$$⑤ \\; \\text{số lần gọi cổng ghi được} = \\hlg{1} = \\text{số lần mong đợi}$$
<p>Tham số ghi được: TK01 và 2 005 000, bằng kết quả phép ④.</p>""",
           """Phép tính thứ năm. Đối tượng giả ghi được đúng một lời gọi, bằng số lần mong đợi, nên phép kiểm tương tác đạt.
           Tham số ghi được cũng là hai triệu không trăm linh năm nghìn, bằng kết quả của phép tính thứ tư."""),
    ], checks=["alg.bnx_jt_fee_branches() == 3", "len(alg.bnx_jt_fee_cases()) == 4", "alg.bnx_jt_fee_run(True) == (3, 1, [('bien', 5500, 5000)])",
               "alg.bnx_jt_fee_run(True)[2][0][1] - alg.bnx_jt_fee_run(True)[2][0][2] == 500",
               "alg.bnx_jt_fee_run(False) == (4, 0, [])",
               "alg.bnx_jt_transfer(2_000_000) == (5000, [('TK01', 2_005_000)])",
               "alg.bnx_jt_transfer(2_000_000, accept=False) == ('lỗi', [('TK01', 2_005_000)])",
               "[alg.bnx_jt_fee(a) for a in (200_000, 2_000_000, 50_000_000)] == [0, 5000, 5500]"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: đối tượng giả viết tay, không dùng thư viện", [
        st(code(JAVA_FAKE, "Đường khác: tự viết đối tượng giả bằng Java thuần"),
           """Ta kiểm lại bằng một đường khác, không dùng thư viện nào, vì hai đường độc lập cho cùng kết quả thì ta mới tin. Một mảng hai ô ghi lại số lần gọi và số tiền nhận được.
           Đối tượng giả viết tay là một hàm viết tại chỗ, mỗi lần được gọi thì tăng số đếm, ghi số tiền và trả lời đúng.
           Sau đó ta gọi dịch vụ chuyển hai triệu đồng, rồi in ra phí, số lần gọi và số tiền cổng nhận được.""",
           focus=[1, "2.3", ["2.4", "2.5", "2.6", "2.7"], ["2.8", "2.9"]], clear=True),
        st(out(OUT_FAKE),
           """Kết quả chạy thật in ba số: phí năm nghìn, số lần gọi là một, và số tiền hai triệu không trăm linh năm nghìn, nên khớp với ca kiểm dùng thư viện."""),
        st(table(["đại lượng", "Mockito (verify)", "giả viết tay", "tính tay theo đề"],
                 [["phí của 2 000 000", "5 000", "5 000", "5 000"],
                  ["số lần gọi cổng", "1", "1", "1"],
                  ["số tiền cổng nhận", "2 005 000", "2 005 000", "2 000 000 + 5 000"]]),
           """Bảng này đặt ba đường cạnh nhau. Thư viện tạo đối tượng giả, đối tượng giả viết tay và phép tính tay theo đề đều cho cùng ba con số.
           Vậy thư viện không làm phép màu gì, vì nó chỉ ghi lại lời gọi thay ta và so giúp ta.""", clear=True),
    ], checks=["alg.bnx_jt_transfer(2_000_000)[0] == 5000", "len(alg.bnx_jt_transfer(2_000_000)[1]) == 1",
               "alg.bnx_jt_transfer(2_000_000)[1][0][1] == 2_005_000 == 2_000_000 + alg.bnx_jt_fee(2_000_000)"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> “Ba ca đều đạt, vậy hàm đúng.” Ở ví dụ, ba ca giữa khoảng đều đạt trong khi hàm vẫn sai ở đúng mốc 10 000 000.
<b class="red">Ca kiểm đạt không chứng minh mã đúng</b>, chỉ chứng minh các trường hợp đã kiểm.
<br><span class="note">Cách chữa: lấy giá trị mong đợi từ đề bài, không từ mã; mỗi nhánh một ca, mỗi mốc thêm ca ở đúng mốc.</span></div>""",
           """Lỗi thứ nhất, của người mới, là thấy ba ca đều đạt thì kết luận hàm đúng. Ở ví dụ, ba ca giữa khoảng đều đạt trong khi hàm vẫn sai ở đúng mốc mười triệu.
           Ca kiểm đạt không chứng minh mã đúng, mà chỉ chứng minh các trường hợp đã kiểm.
           Cách chữa là lấy giá trị mong đợi từ đề bài chứ không từ mã, và thêm ca ở đúng mỗi mốc.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Tin rằng ca dùng đối tượng giả đã kiểm được bên ngoài.
Đối tượng giả trả <code>true</code> vì <b>ta dặn</b> nó thế. Nếu cổng thật đổi cách trả lời, mọi ca vẫn đạt.
<b class="red">Đối tượng giả kiểm cách mã của ta gọi bên ngoài, không kiểm bên ngoài chạy đúng.</b>
<br><span class="note">Cách chữa: giữ thêm một số ít ca gọi môi trường thử của cổng; không dặn giả nhiều hơn điều ca kiểm cần.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, hay gặp lúc mới dựng hệ thống, là tin rằng ca dùng đối tượng giả đã kiểm được bên ngoài.
           Đối tượng giả trả lời đúng chỉ vì ta dặn nó thế, nên nếu cổng thật đổi cách trả lời thì mọi ca vẫn đạt.
           Đối tượng giả kiểm cách mã của ta gọi bên ngoài, chứ không kiểm bên ngoài chạy đúng.
           Cách chữa là giữ thêm một số ít ca gọi tới môi trường thử của cổng thanh toán.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Ca kiểm <b class="red">lúc đạt lúc trượt</b> vì phụ thuộc thứ nằm ngoài ca:
<b>đồng hồ thật</b> (lệnh sau 22 giờ tính sang ngày kế, số minh hoạ: ca chạy ban ngày thì đạt, bản dựng ban đêm thì trượt),
<b>mạng</b> (gọi dịch vụ thật), <b>thứ tự chạy</b> (ca sau dùng dữ liệu ca trước để lại).
<br><span class="note">Cách chữa: đưa đồng hồ vào làm tham số (<code>java.time.Clock</code>) rồi cho ca kiểm một đồng hồ đứng yên; thay mạng bằng đối tượng giả; mỗi ca tự sắp đặt dữ liệu của mình.</span>
<br><span class="note">JUnit mặc định tạo một bản thể mới của lớp kiểm thử cho mỗi ca, nên trường của lớp (như đối tượng giả) không rò sang ca khác; dữ liệu tĩnh hay dữ liệu bên ngoài (tệp, cơ sở dữ liệu) thì có thể rò.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm, lộ ra khi vận hành lâu dài, là ca kiểm lúc đạt lúc trượt vì phụ thuộc thứ nằm ngoài ca.
           Thứ nhất là đồng hồ thật, ví dụ lệnh sau hai mươi hai giờ tính sang ngày kế, thì ca chạy ban ngày đạt mà bản dựng ban đêm lại trượt.
           Thứ hai là mạng, và thứ ba là thứ tự chạy, khi ca sau dùng dữ liệu ca trước để lại.
           Cách chữa là đưa đồng hồ vào làm tham số, thay mạng bằng đối tượng giả, và để mỗi ca tự sắp đặt dữ liệu của mình.
           Bộ khung mặc định tạo một bản thể mới của lớp kiểm thử cho mỗi ca, nên trường của lớp không rò sang ca khác, còn dữ liệu tĩnh hay dữ liệu bên ngoài thì có thể rò.""", clear=True),
        st(code(JAVA_CLOCK, "Đồng hồ là tham số: ca kiểm tự chọn thời điểm"),
           """Đoạn mã này cho thấy cách chữa với đồng hồ. Hàm kiểm giờ chốt không tự hỏi giờ của máy, mà nhận một đồng hồ làm tham số.
           Trong phần chạy thử, ta tạo một đồng hồ đứng yên ở hai mươi mốt giờ năm mươi chín phút theo giờ Việt Nam.
           Lần in đầu dùng đúng thời điểm đó, còn lần in sau dùng đồng hồ đứng yên ở sáu mươi giây sau, tức đúng hai mươi hai giờ.""",
           focus=[1, ["2.3", "2.4"], ["2.7", "2.8"], ["2.9", "2.10"]], clear=True),
        st(out(OUT_CLOCK),
           """Kết quả chạy thật: trước giờ chốt một phút thì đúng, tại đúng giờ chốt thì sai. Chạy vào lúc nào trong ngày cũng ra hai dòng này, nên ca kiểm không còn lúc đạt lúc trượt.""", clear=True),
    ], checks=["alg.bnx_jt_fee_run(True)[0] == 3 and alg.bnx_jt_fee(10_000_000, True) != alg.bnx_jt_fee(10_000_000)",
               "alg.bnx_jt_before_cutoff(21, 59) and not alg.bnx_jt_before_cutoff(22, 0)",
               "alg.bnx_jt_before_cutoff(15, 0) and not alg.bnx_jt_before_cutoff(22, 30)"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Theo đề, phí của 499 999, của 500 000 và của 9 999 999 đồng là bao nhiêu? Với mã còn lỗi <code>&lt;=</code>, ca nào trong ba ca này trượt?"],
                  ["2", "Mã đã sửa. Chuyển 20 000 000 đồng từ TK01: lệnh kiểm tương tác phải đòi cổng được gọi mấy lần, với số tiền nào?"],
                  ["3", "Quyết định (số minh hoạ): 100 ca kiểm. Ca dùng đối tượng giả chạy 10 mili giây, ca gọi cổng thử thật chạy 2 000 mili giây. Toàn giả, toàn thật, hay 90 giả + 10 thật?"]]),
           """Đến lượt bạn. Câu một, theo đề thì phí của ba số tiền trên màn hình là bao nhiêu, và với mã còn lỗi thì ca nào trong ba ca đó trượt?
           Câu hai, với mã đã sửa, chuyển hai mươi triệu đồng thì lệnh kiểm tương tác phải đòi cổng được gọi mấy lần, với số tiền nào?
           Câu ba, có một trăm ca kiểm, ca dùng đối tượng giả chạy mười mili giây, ca gọi cổng thử thật chạy hai nghìn mili giây, bạn chọn cách nào?
           Hãy tạm dừng lại và làm từng câu ra giấy trước khi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: 499 999 dưới mốc 500 000; hai số kia nằm từ 500 000 tới dưới 10 000 000.</p>
$$499\\,999 \\to \\hlg{0}; \\quad 500\\,000 \\to \\hlg{5000}; \\quad 9\\,999\\,999 \\to \\hlg{5000}$$
<p>Mã còn lỗi cũng trả đúng ba giá trị này: <b>không ca nào trượt</b>. Chỉ ca ở đúng 10 000 000 mới bắt được lỗi.</p>""",
           """Đáp án câu một. Số thứ nhất nằm dưới mốc năm trăm nghìn nên phí bằng không, còn hai số kia nằm giữa hai mốc nên phí là năm nghìn.
           Mã còn lỗi cũng trả đúng ba giá trị này, nên không ca nào trượt, và chỉ ca ở đúng mười triệu mới bắt được lỗi."""),
        st("""<p>Câu 2: 20 000 000 từ mốc 10 000 000 trở lên nên phí 5 500.</p>
$$20\\,000\\,000 + 5\\,500 = \\hlg{20\\,005\\,500}; \\quad \\text{đúng } \\hlg{1} \\text{ lần}$$""",
           """Đáp án câu hai. Hai mươi triệu nằm từ mốc mười triệu trở lên, nên phí là năm nghìn năm trăm.
           Vậy lệnh kiểm tương tác đòi cổng được gọi đúng một lần, với số tiền hai mươi triệu không trăm linh năm nghìn năm trăm."""),
        st(table(["lựa chọn", "thời gian một lượt", "được", "mất"],
                 [["100 ca dùng đối tượng giả", "100 × 10 = 1 000 mili giây", "nhanh, chạy sau mỗi lần sửa", "không biết cổng thật có trả lời như ta dặn"],
                  ["100 ca gọi cổng thử thật", "100 × 2 000 = 200 000 mili giây", "kiểm được cả cổng", "chậm 200 lần; mạng rớt thì ca trượt oan"],
                  ["90 giả + 10 thật", "90 × 10 + 10 × 2 000 = 20 900 mili giây", "phần xử lý kiểm nhanh, vẫn có ca canh cổng", "phải nuôi hai loại ca, ca thật chạy riêng"]]),
           """Đáp án câu ba, không có lựa chọn nào chỉ toàn được. Toàn đối tượng giả thì một lượt chỉ mất một nghìn mili giây, nhưng không biết cổng thật có trả lời như ta dặn.
           Toàn cổng thật thì mất hai trăm nghìn mili giây, chậm gấp hai trăm lần, và mạng rớt thì ca trượt oan.
           Chín mươi ca giả cộng mười ca thật mất hai mươi nghìn chín trăm mili giây, phần xử lý vẫn kiểm nhanh mà vẫn có ca canh cổng, đổi lại phải nuôi hai loại ca.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["[alg.bnx_jt_fee(a) for a in (499_999, 500_000, 9_999_999)] == [0, 5000, 5000]",
               "[alg.bnx_jt_fee(a, True) for a in (499_999, 500_000, 9_999_999)] == [alg.bnx_jt_fee(a) for a in (499_999, 500_000, 9_999_999)]",
               "alg.bnx_jt_transfer(20_000_000) == (5500, [('TK01', 20_005_500)])",
               "alg.bnx_jt_suite_ms(100, 0) == 1000", "alg.bnx_jt_suite_ms(0, 100) == 200_000", "alg.bnx_jt_suite_ms(90, 10) == 20_900",
               "alg.bnx_jt_suite_ms(0, 100) // alg.bnx_jt_suite_ms(100, 0) == 200"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mỗi nhánh một ca", "thêm ca ở mốc biên", "đọc bản báo: mong đợi và thực nhận", "thay bên ngoài bằng đối tượng giả", "kiểm lời gọi: 1 lần, đúng tham số"),
           """Tổng kết chuỗi lập luận của bài. Mỗi nhánh cần một ca kiểm, và mỗi mốc cần thêm một ca ở đúng mốc.
           Khi ca trượt, bản báo ghi giá trị mong đợi và giá trị thực nhận. Phần phụ thuộc bên ngoài được thay bằng đối tượng giả, rồi ta kiểm lời gọi đúng một lần, đúng tham số."""),
        st("""<div class='box key'><b>Tư duy:</b> ca kiểm đạt chỉ nói về những trường hợp đã kiểm; đối tượng giả chỉ nói về cách mã của ta gọi ra ngoài.
Ca nào phụ thuộc đồng hồ thật, mạng hay thứ tự chạy thì sớm muộn cũng lúc đạt lúc trượt.</div>""",
           """Điều cần mang theo. Ca kiểm đạt chỉ nói về những trường hợp đã kiểm, còn đối tượng giả chỉ nói về cách mã của ta gọi ra ngoài.
           Ca nào phụ thuộc đồng hồ thật, mạng hay thứ tự chạy thì sớm muộn cũng lúc đạt lúc trượt."""),
        st(table(["Nếu bị hỏi về dòng “automated tests (JUnit 5, Mockito)” trên CV", "ý trả lời một dòng"],
                 [["Bạn chọn ca kiểm cho một hàm thế nào?", "mỗi nhánh một ca, thêm ca ở đúng mốc biên; giá trị mong đợi lấy từ đề, không từ mã"],
                  ["Khi nào dùng đối tượng giả, và nó không kiểm được gì?", "khi phần phụ thuộc chậm, cần mạng hay tốn tiền; nó chỉ kiểm cách ta gọi, nên vẫn cần ít ca gọi môi trường thử"],
                  ["Gặp ca lúc đạt lúc trượt thì làm gì?", "tìm phụ thuộc ẩn: đồng hồ, mạng, thứ tự, dữ liệu dùng chung; đưa đồng hồ vào làm tham số"]]),
           """Nếu bị hỏi về dòng kiểm thử tự động trên hồ sơ xin việc, đây là ba câu hay gặp. Chọn ca kiểm thế nào: mỗi nhánh một ca, thêm ca ở mốc biên, mong đợi lấy từ đề.
           Khi nào dùng đối tượng giả: khi phần phụ thuộc chậm hay tốn tiền, và nhớ rằng nó chỉ kiểm cách ta gọi.
           Gặp ca lúc đạt lúc trượt thì tìm phụ thuộc ẩn như đồng hồ, mạng, thứ tự chạy và dữ liệu dùng chung.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st(table(["Câu hỏi tiếp theo hay gặp", "ý trả lời (theo hướng dẫn chính thức)"],
                 [["Nhiều ca cùng khuôn, chỉ khác số, viết sao cho gọn?", "<code>@ParameterizedTest</code> chạy một hàm nhiều lần với đối số khác nhau; phải khai ít nhất một nguồn đối số, ví dụ <code>@ValueSource</code>"],
                  ["Đối tượng gián điệp (spy) khác đối tượng giả ở đâu?", "spy bọc đối tượng thật: hàm thật được gọi, trừ hàm đã dặn trước"],
                  ["Muốn so tham số đã truyền sau khi kiểm tương tác?", "<code>ArgumentCaptor</code>: bắt tham số để khẳng định trên nó sau lệnh kiểm"],
                  ["Gắn đối tượng giả bằng nhãn <code>@Mock</code> thì sao?", "nhãn giảm mã tạo giả lặp lại; với JUnit 5, hướng dẫn Mockito chỉ tới tiện ích <code>MockitoExtension</code>"]]),
           """Còn bốn câu hỏi tiếp theo hay gặp, trả lời theo hướng dẫn chính thức. Ca kiểm có tham số chạy một hàm nhiều lần với đối số khác nhau, và phải khai ít nhất một nguồn đối số.
           Đối tượng gián điệp bọc một đối tượng thật, nên hàm thật được gọi trừ hàm đã dặn trước.
           Muốn so tham số đã truyền thì dùng bộ bắt tham số, rồi khẳng định trên nó sau lệnh kiểm.
           Nhãn tạo đối tượng giả giảm mã lặp lại, và với bộ khung kiểm thử này, hướng dẫn chỉ tới một tiện ích mở rộng riêng.""", clear=True),
        st("""<p>Bài sau: Redis nâng cao, gồm cụm nhiều nút, khoá có hạn và khử trùng yêu cầu gửi lại.</p>""",
           """Ở bài mười chín, ta sang Redis nâng cao, gồm cụm nhiều nút, khoá có hạn và cách khử trùng yêu cầu gửi lại.""",
           forward_ref=True),
    ], checks=["alg.bnx_jt_fee_branches() == 3", "alg.bnx_jt_transfer(2_000_000)[1] == [('TK01', 2_005_000)]"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
    return lesson("L18", "junit5_mockito", "Bài 18 — Kiểm thử Java với JUnit 5 và Mockito: ca kiểm, đối tượng giả và kiểm tương tác",
                  "curriculum/bnx.yaml L18; audit/bnx/verify_bnx.py L18; JUnit 5.14.4 User Guide (docs.junit.org/5.14.4: Annotations, "
                  "Test Instance Lifecycle, Test Execution Order, Console Launcher); Mockito 5.24.0 Javadoc lớp Mockito; "
                  "Java SE 21 API java.time.Clock (đọc 2026-11-11; audit/bnx/sources_l18.md); chạy thật JUnit Platform 1.14.4 + Mockito 5.24.0 trên JDK 21",
                  ["Viết ca kiểm JUnit 5 cho từng nhánh của một hàm và đọc bản báo ca trượt",
                   "Thay phần phụ thuộc bên ngoài bằng đối tượng giả của Mockito",
                   "Kiểm một lời gọi đã xảy ra đúng số lần với đúng tham số",
                   "Chỉ ra ca kiểm dễ vỡ vì phụ thuộc đồng hồ, mạng hay thứ tự chạy"],
                  scenes)
