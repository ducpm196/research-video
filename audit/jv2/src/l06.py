from lib import *
from labkit import write_lab, practice_steps, practice_scene

PHI_DUNG = r"""
    static long phi(long soTien) {
        if (soTien <= 0) {
            throw new IllegalArgumentException("so tien phai duong");
        }
        if (soTien <= 1000000) {
            return 1000;
        }
        if (soTien <= 10000000) {
            return 5000;
        }
        return 10000;
    }
"""

TU_KIEM = r"""
public class TuKiem {
    static int dat = 0, hong = 0;
""" + PHI_DUNG + r"""
    static void kiem(String ten, long mong, long thuc) {
        if (mong == thuc) {
            dat++;
            System.out.println("DAT  " + ten);
        } else {
            hong++;
            System.out.println("HONG " + ten + ": mong " + mong + ", thuc " + thuc);
        }
    }

    static void kiemNgoaiLe(String ten, long soTien) {
        try {
            phi(soTien);
            hong++;
            System.out.println("HONG " + ten + ": khong nem ngoai le");
        } catch (IllegalArgumentException e) {
            dat++;
            System.out.println("DAT  " + ten);
        }
    }

    public static void main(String[] args) {
        kiem("bac dau", 1000, phi(1));
        kiem("bien 1 trieu", 1000, phi(1000000));
        kiem("sau bien 1 trieu", 5000, phi(1000001));
        kiem("bien 10 trieu", 5000, phi(10000000));
        kiem("sau bien 10 trieu", 10000, phi(10000001));
        kiemNgoaiLe("so khong", 0);
        kiemNgoaiLe("so am", -5);
        System.out.println("dat " + dat + ", hong " + hong);
    }
}"""

LAB_LOI = r"""
import java.util.function.LongSupplier;

public class KiemPhiChuyenKhoan {
    static int dat = 0, hong = 0;

    static long phiChuyenKhoan(long soTien, boolean cungNganHang) {
        if (soTien <= 0) {
            throw new IllegalArgumentException("so tien phai duong");
        }
        if (cungNganHang) {
            return 0;
        }
        if (soTien < 500000) {
            return 2000;
        }
        if (soTien <= 5000000) {
            return 7000;
        }
        return 11000;
    }

    static void kiem(String ten, long mong, LongSupplier thuc) {
        long v = thuc.getAsLong();
        if (mong == v) {
            dat++;
            System.out.println("DAT  " + ten);
        } else {
            hong++;
            System.out.println("HONG " + ten + ": mong " + mong + ", thuc " + v);
        }
    }

    static void kiemNgoaiLe(String ten, long soTien) {
        try {
            phiChuyenKhoan(soTien, false);
            hong++;
            System.out.println("HONG " + ten + ": khong nem ngoai le");
        } catch (IllegalArgumentException e) {
            dat++;
            System.out.println("DAT  " + ten);
        }
    }

    public static void main(String[] args) {
        kiem("cung ngan hang", 0, () -> phiChuyenKhoan(2000000, true));
        kiem("bien 500000", 2000, () -> phiChuyenKhoan(500000, false));
        kiem("sau bien 500001", 7000, () -> phiChuyenKhoan(500001, false));
        kiem("bien 5000000", 7000, () -> phiChuyenKhoan(5000000, false));
        kiemNgoaiLe("so khong", 0);
        System.out.println("dat " + dat + ", hong " + hong);
    }
}"""


def build():
    tu_kiem = prog("TuKiem", TU_KIEM, out="DAT  bac dau\nDAT  bien 1 trieu\nDAT  sau bien 1 trieu\nDAT  bien 10 trieu\nDAT  sau bien 10 trieu\n"
                                          "DAT  so khong\nDAT  so am\ndat 7, hong 0")
    loi_code = TU_KIEM.replace("public class TuKiem ", "public class TuKiemLoi ").replace("soTien <= 1000000", "soTien < 1000000").replace("soTien <= 10000000", "soTien < 10000000")
    tu_kiem_loi = prog("TuKiemLoi", loi_code, out="DAT  bac dau\nHONG bien 1 trieu: mong 1000, thuc 5000\nDAT  sau bien 1 trieu\n"
                                                  "HONG bien 10 trieu: mong 5000, thuc 10000\nDAT  sau bien 10 trieu\nDAT  so khong\nDAT  so am\ndat 5, hong 2")
    xanh_gia = prog("XanhGia", r"""
public class XanhGia {
    static long phiLoi(long soTien) {
        return 1000;                                  // quên kiểm số không hợp lệ: không ném ngoại lệ
    }

    public static void main(String[] args) {
        try {                                         // ca kiểm viết sai: nuốt mọi ngoại lệ
            phiLoi(0);
            System.out.println("ca kiem A: DAT");
        } catch (Exception e) {
            System.out.println("ca kiem A: DAT");
        }
        try {                                         // ca kiểm đúng: phải ném thì mới đạt
            phiLoi(0);
            System.out.println("ca kiem B: HONG, khong nem ngoai le");
        } catch (IllegalArgumentException e) {
            System.out.println("ca kiem B: DAT");
        }
    }
}""", out="ca kiem A: DAT\nca kiem B: HONG, khong nem ngoai le")
    so_thuc = prog("SoThuc", r"""
public class SoThuc {
    public static void main(String[] args) {
        double tong = 0.1 + 0.2;
        System.out.println(tong == 0.3);                      // so sánh bằng nhau tuyệt đối
        System.out.println(Math.abs(tong - 0.3) < 1e-9);      // so sánh với sai số cho phép
    }
}""", out="false\ntrue")
    thu_tu = prog("ThuTu", r"""
public class ThuTu {
    static long soDu = 0;                                     // trạng thái DÙNG CHUNG giữa các ca kiểm

    static void caA() {
        soDu += 100;
        System.out.println("A " + (soDu == 100 ? "DAT" : "HONG"));
    }

    static void caB() {
        if (soDu >= 50) {
            soDu -= 50;
        }
        System.out.println("B " + (soDu == 50 ? "DAT" : "HONG"));
    }

    public static void main(String[] args) {
        System.out.println("thu tu A, B:");
        caA();
        caB();
        soDu = 0;
        System.out.println("thu tu B, A:");
        caB();
        caA();
    }
}""", out="thu tu A, B:\nA DAT\nB DAT\nthu tu B, A:\nB HONG\nA DAT")

    ju_files = {
        "PhiChuyen.java": "public class PhiChuyen {\n" + PHI_DUNG.replace("    static long phi", "    public static long phi").replace("\n    ", "\n    ").strip("\n") + "\n}",
        "PhiChuyenTest.java": r"""
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class PhiChuyenTest {
    @Test
    void bacDau() {
        assertEquals(1000, PhiChuyen.phi(1));
    }

    @Test
    void bienMotTrieu() {
        assertEquals(1000, PhiChuyen.phi(1000000));
    }

    @Test
    void sauBienMotTrieu() {
        assertEquals(5000, PhiChuyen.phi(1000001));
    }

    @Test
    void soKhong() {
        assertThrows(IllegalArgumentException.class, () -> PhiChuyen.phi(0));
    }
}""",
    }
    ju = project("JUnit", ju_files, [
        ("J=lib/junit-platform-console-standalone-1.10.2.jar", ""),
        ("javac -cp $J -d out PhiChuyen.java PhiChuyenTest.java", ""),
        ("kiem() { java -jar $J execute -cp out -c PhiChuyenTest --details=summary 2>/dev/null; }", ""),
        ("kiem | grep -E 'tests (successful|failed)'", "[         4 tests successful      ]\n[         0 tests failed          ]"),
        ("sed -i 's/soTien <= 1000000/soTien < 1000000/' PhiChuyen.java", ""),
        ("javac -cp $J -d out PhiChuyen.java PhiChuyenTest.java", ""),
        ("kiem | grep -E '=> |tests (successful|failed)'",
         "    => org.opentest4j.AssertionFailedError: expected: <1000> but was: <5000>\n[         3 tests successful      ]\n[         1 tests failed          ]"),
    ], deps=True)
    tai = project("TaiJar", {"x.txt": "x"}, [("sha256sum lib/junit-platform-console-standalone-1.10.2.jar | cut -c1-16", "a1de557821293ce9")], deps=True)

    lab = prog("KiemPhiChuyenKhoan", LAB_LOI, out="DAT  cung ngan hang\nHONG bien 500000: mong 2000, thuc 7000\nDAT  sau bien 500001\n"
                                                  "DAT  bien 5000000\nDAT  so khong\ndat 4, hong 1")
    write_lab("JV2", "L06", """# Lab JV2 L06 — Viết năm ca kiểm và bắt một lỗi biên

Hàm cần kiểm (số minh hoạ), **đã có lỗi** — bạn chưa biết ở đâu:

```java
static long phiChuyenKhoan(long soTien, boolean cungNganHang) {
    if (soTien <= 0) {
        throw new IllegalArgumentException("so tien phai duong");
    }
    if (cungNganHang) {
        return 0;
    }
    if (soTien < 500000) {
        return 2000;
    }
    if (soTien <= 5000000) {
        return 7000;
    }
    return 11000;
}
```

**Đặc tả đúng:** số tiền không dương → ném `IllegalArgumentException`; cùng ngân hàng → phí 0; khác ngân hàng: đến **500 000** là 2 000; đến **5 000 000** là 7 000; trên đó là 11 000.

Viết tệp `KiemPhiChuyenKhoan.java` gồm hàm trên, hai hàm trợ giúp tự viết và `main` với **năm ca kiểm** theo bảng:

| tên ca | gọi | mong đợi |
|---|---|---|
| `cung ngan hang` | `phiChuyenKhoan(2000000, true)` | 0 |
| `bien 500000` | `phiChuyenKhoan(500000, false)` | 2000 |
| `sau bien 500001` | `phiChuyenKhoan(500001, false)` | 7000 |
| `bien 5000000` | `phiChuyenKhoan(5000000, false)` | 7000 |
| `so khong` | `phiChuyenKhoan(0, false)` | ném `IllegalArgumentException` |

Hàm trợ giúp `kiem(String ten, long mong, LongSupplier thuc)` in `DAT  <ten>` (hai dấu cách sau chữ DAT) hoặc `HONG <ten>: mong <mong>, thuc <thuc>`; `kiemNgoaiLe(ten, soTien)` in `DAT  <ten>` nếu có ném đúng ngoại lệ, ngược lại `HONG <ten>: khong nem ngoai le`. Cuối cùng in `dat <số>, hong <số>`.

Mong đợi: đúng **một** ca `HONG` — đó là lỗi trong hàm. Chấm bản **chưa sửa**: `bash labs/cham.sh JV2 L06 KiemPhiChuyenKhoan.java`. Sau đó tự sửa hàm và chạy lại để thấy năm dòng `DAT`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: năm ca kiểm và một lỗi biên", practice_steps(
        st, "JV2", "L06",
        """<p><b>Đề</b>: hàm <code>phiChuyenKhoan</code> (trong <code>de.md</code>) có một lỗi biên.</p>
<ol><li>Tự viết <code>kiem(ten, mong, thuc)</code> và <code>kiemNgoaiLe(ten, soTien)</code> in <code>DAT  …</code> hoặc <code>HONG …</code>.</li>
<li>Viết <b>5 ca kiểm</b> theo bảng đặc tả: cùng ngân hàng, biên 500 000, sau biên, biên 5 000 000, số không.</li>
<li>In <code>dat …, hong …</code>. Chấm bản <b>chưa sửa</b> (ra đúng 1 ca HONG); rồi sửa hàm.</li></ol>
<p class="note">Tệp <code>KiemPhiChuyenKhoan.java</code>; bảng ca kiểm và định dạng dòng in ở <code>labs/JV2/L06/de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Đề bài cho một hàm tính phí chuyển khoản có một lỗi biên, kèm bảng đặc tả. Hãy tự viết hai hàm trợ giúp để khẳng định, rồi viết năm ca kiểm theo bảng, gồm cùng ngân hàng, hai biên, một ca sau biên và số không.
        Chạy trên bản chưa sửa, bạn phải thấy đúng một ca báo hỏng. Rồi tự sửa lỗi và chạy lại. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        lab["out"], "KiemPhiChuyenKhoan.java",
        """<div class="box key"><b>Nếu kẹt:</b> <code>kiem</code> nhận <code>LongSupplier</code> để gọi hàm bên trong nó: <code>kiem("bien 500000", 2000, () -&gt; phiChuyenKhoan(500000, false));</code>.
Lỗi nằm ở dấu so sánh quanh 500 000. Lời giải: <code>labs/JV2/L06/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, hàm trợ giúp nhận một hàm ngắn để gọi hàm cần kiểm bên trong nó, nhờ đó bắt được cả lúc ném ngoại lệ. Lỗi nằm ở dấu so sánh quanh năm trăm nghìn.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=240), "JV2", "L06")

    sc_hook = sc("hook", "hook", "Một dấu nhỏ hơn thay cho nhỏ hơn hoặc bằng, và đúng một đồng tiền bị tính sai", [
        st(svg(1500, 300,
               box(20, 90, 340, 100, ["đặc tả", "đến 1 triệu: phí 1 000"], C_BLUE, 26, bold=True), arrow(365, 140, 470, 140, "#475569"),
               box(475, 90, 340, 100, ["mã viết", "if (t < 1000000)"], C_AMBER, 26, bold=True), arrow(820, 140, 925, 140, "#475569"),
               box(930, 60, 550, 160, ["giao dịch ĐÚNG 1 000 000", "bị tính 5 000 thay vì 1 000", "mọi bài kiểm bằng mắt đều bỏ sót"], C_RED, 26, bold=True),
               txt(750, 270, "một ca kiểm đặt đúng ở biên bắt được lỗi này trong một giây", 26, "middle", "#16a34a", True)),
           """Đặc tả nói giao dịch đến một triệu đồng thì phí một nghìn. Người viết gõ dấu nhỏ hơn thay vì nhỏ hơn hoặc bằng. Với mọi giao dịch khác thì chương trình chạy đúng, nên không ai nhận ra. Chỉ giao dịch đúng một triệu bị tính năm nghìn.
           Một ca kiểm đặt đúng ở biên bắt được lỗi này trong một giây, còn mắt người thì rất dễ bỏ qua."""),
        st("""<div class="box key">Hôm nay: <b>kiểm thử đơn vị</b>. Biến một câu của đặc tả thành một ca kiểm chạy được, chọn đúng <b>giá trị ở biên</b>, tự viết khẳng định,
rồi dùng <b>JUnit 5</b> đúng như dự án thật. Kèm câu hỏi của người làm nghề: kiểm hết mọi đầu vào được không?</div>""",
           """Hôm nay ta học kiểm thử đơn vị. Biến một câu của đặc tả thành một ca kiểm chạy được, chọn đúng giá trị ở biên, tự viết khẳng định, rồi dùng bộ kiểm thử chuẩn như trong dự án thật. Kèm câu hỏi của người làm nghề, kiểm hết mọi đầu vào được không.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: hàm tĩnh, rẽ nhánh, ngoại lệ, hàm ngắn", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① hàm tĩnh", "<code>static long phi(long soTien)</code> nhận số, trả số; gọi bằng <code>phi(5)</code>"],
                  ["② rẽ nhánh theo bậc", "<code>if (t &lt;= 1000000) …</code>: dấu <code>&lt;=</code> hay <code>&lt;</code> quyết định giá trị đúng biên rơi vào bậc nào"],
                  ["③ ngoại lệ", "<code>throw new IllegalArgumentException(\"…\")</code> báo đầu vào sai; <code>catch</code> bắt đúng loại ngoại lệ đó"],
                  ["④ hàm ngắn", "<code>() -&gt; phi(5)</code> là một việc chưa chạy, đưa cho nơi khác gọi sau"]]),
           """Ta ôn lại bốn điều. Hàm tĩnh nhận số và trả số. Rẽ nhánh theo bậc, trong đó dấu so sánh quyết định giá trị đúng ở biên rơi vào bậc nào. Ngoại lệ báo đầu vào sai, và có thể bắt đúng loại. Hàm ngắn là một việc chưa chạy, đưa cho nơi khác gọi sau.
           Tất cả đều dùng trong bài này.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã tám từ của kiểm thử", [
        st(table(["từ", "nghĩa"],
                 [["ca kiểm (test case)", "một đầu vào cụ thể và <b>đầu ra mong đợi</b> lấy từ đặc tả, không lấy từ mã"],
                  ["khẳng định (assertion)", "câu lệnh so <b>mong đợi</b> với <b>thực tế</b>; khác thì ca kiểm hỏng"],
                  ["giá trị biên", "giá trị đúng ở chỗ hành vi đổi: <code>1 000 000</code> và hai bên của nó, <code>1 000 001</code>"],
                  ["lớp tương đương", "nhóm đầu vào được hàm xử lý như nhau (mọi số từ 1 tới 1 000 000): kiểm <b>một đại diện</b> là đủ"],
                  ["<code>@Test</code>", "nhãn của JUnit 5 báo hàm này là một ca kiểm; JUnit tự tìm và chạy"],
                  ["<code>assertEquals(mong, thuc)</code>", "khẳng định hai giá trị bằng nhau; <b>mong đợi viết trước</b>"],
                  ["<code>assertThrows(X.class, việc)</code>", "khẳng định <b>việc</b> phải ném ngoại lệ loại <code>X</code>; không ném thì hỏng"],
                  ["<code>import static</code>", "nạp tên một hàm tĩnh để viết gọn <code>assertEquals</code> thay cho tên dài đủ"]]),
           """Bảng này có tám từ. Ca kiểm là một đầu vào cụ thể cùng đầu ra mong đợi lấy từ đặc tả, không lấy từ mã. Khẳng định là lệnh so mong đợi với thực tế. Giá trị biên là giá trị đúng ở chỗ hành vi đổi, cùng hai bên của nó.
           Lớp tương đương là nhóm đầu vào được xử lý như nhau, nên kiểm một đại diện là đủ. Nhãn kiểm thử báo cho bộ kiểm thử biết hàm nào là ca kiểm. Có khẳng định bằng nhau và khẳng định phải ném ngoại lệ. Và nạp tên tĩnh giúp viết gọn.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: trục số, ba bậc, và chỗ lỗi ẩn nấp", [
        st(svg(1500, 380,
               '<line x1="40" y1="190" x2="1460" y2="190" stroke="#475569" stroke-width="4"/>',
               box(40, 60, 330, 70, ["không hợp lệ", "số ≤ 0 → ngoại lệ"], C_RED, 24, bold=True),
               box(430, 60, 330, 70, ["bậc 1: phí 1 000", "1 … 1 000 000"], C_BLUE, 24, bold=True),
               box(800, 60, 330, 70, ["bậc 2: phí 5 000", "… 10 000 000"], C_GREEN, 24, bold=True),
               box(1150, 60, 310, 70, ["bậc 3: phí 10 000", "trên 10 000 000"], C_AMBER, 24, bold=True),
               *[f'<circle cx="{x}" cy="190" r="11" fill="#dc2626"/>' for x in (400, 780, 1140)],
               txt(560, 245, "biên 1: 1 000 000 / 1 000 001", 22, "middle", "#dc2626", True),
               txt(780, 285, "biên 2: 10 000 000 / 10 000 001", 22, "middle", "#dc2626", True),
               txt(240, 245, "0 và −5", 22, "middle", "#dc2626", True),
               txt(750, 345, "lỗi hay ẩn ở điểm đỏ: nơi dấu < hay <= quyết định", 26, "middle", "#1f2937", True)),
           """Hình dung hàm phí như một trục số chia thành các bậc. Bên trái là vùng không hợp lệ, rồi ba bậc phí. Giữa các bậc là những điểm đỏ, các giá trị biên. Lỗi lệch dấu so sánh luôn ẩn ở điểm đỏ, vì nó chỉ làm sai đúng một giá trị ở đó.
           Vì vậy ca kiểm tốt nhất đặt đúng ở các điểm đỏ và hai bên của nó."""),
        st(code_block(tu_kiem, lines=(4, 15)),
           """Ta xem hàm cần kiểm. Số không hoặc số âm thì ném ngoại lệ. Đến một triệu thì phí một nghìn. Đến mười triệu thì phí năm nghìn. Trên đó là mười nghìn. Các số này là số minh hoạ.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: từ đặc tả tới bảy ca kiểm", [
        st("<p><b>Bước 1.</b> Đếm các <b>vùng</b> của đặc tả: không hợp lệ, bậc 1, bậc 2, bậc 3 &rarr; <b>4 vùng</b>, có <b>3 biên</b> giữa chúng (0/1, 1 000 000, 10 000 000).</p>",
           """Bước một, đếm các vùng của đặc tả. Có bốn vùng, gồm không hợp lệ và ba bậc phí. Giữa bốn vùng có ba biên, là không, một triệu và mười triệu.""", clear=True),
        st("<p><b>Bước 2.</b> Mỗi biên giữa hai bậc cần <b>hai ca</b>: giá trị <b>đúng biên</b> và giá trị <b>ngay sau biên</b>.</p>"
           "<p>Vì sao: lỗi dấu <code>&lt;</code> / <code>&lt;=</code> chỉ làm sai <b>đúng giá trị biên</b>; ca ngay sau biên chứng tỏ bậc mới bắt đầu đúng chỗ.</p>",
           """Bước hai, mỗi biên giữa hai bậc cần hai ca. Một ca đúng giá trị biên và một ca ngay sau biên. Vì lỗi lệch dấu chỉ làm sai đúng giá trị biên, còn ca ngay sau biên chứng tỏ bậc mới bắt đầu đúng chỗ.""", clear=True),
        st("<p><b>Bước 3.</b> Vùng không hợp lệ cần <b>mỗi dạng một ca</b>: số không và một số âm. Thêm một ca ở bậc thấp nhất (giá trị 1).</p>"
           "<p>Tổng: hai biên giữa bậc × 2 ca + ca bậc đầu + hai ca không hợp lệ = 2 × 2 + 1 + 2 = <b>7</b>.</p>",
           """Bước ba, vùng không hợp lệ cần mỗi dạng một ca, số không và một số âm. Thêm một ca ở bậc thấp nhất. Vì mỗi dạng hỏng có thể bị xử lý khác nhau nên mỗi dạng cần một ca riêng. Cộng lại là hai biên nhân hai ca, cộng một, cộng hai, bằng bảy ca.""", clear=True),
        st("<p><b>Bước 4.</b> Viết <b>mong đợi trước</b>, từ đặc tả chứ không từ mã:</p>"
           + table(["ca", "đầu vào", "mong đợi"],
                   [["bậc đầu", "1", "1 000"], ["biên 1", "1 000 000", "1 000"], ["sau biên 1", "1 000 001", "5 000"], ["biên 2", "10 000 000", "5 000"],
                    ["sau biên 2", "10 000 001", "10 000"], ["số không / số âm", "0, −5", "ngoại lệ"]]),
           """Bước bốn, viết giá trị mong đợi trước, và lấy từ đặc tả chứ không lấy từ mã. Nếu lấy từ mã thì ca kiểm chỉ lặp lại lỗi của mã. Bảng này có đủ bảy ca, hai ca cuối cùng chung một dòng vì cùng mong đợi ngoại lệ.""", clear=True),
    ], checks=["2 * 2 + 1 + 2 == 7", "4 - 1 == 3"])
    sc_ex = sc("example", "example", "Ví dụ: bảy ca kiểm tự viết, chạy thật", [
        st(code_block(tu_kiem, lines=(17, 25)),
           """Phép làm thứ nhất, hàm khẳng định đầu tiên. Nó nhận tên ca, giá trị mong đợi và giá trị thực, so hai số, rồi in đạt hay hỏng, kèm hai giá trị nếu hỏng. Nó cũng đếm số ca đạt và hỏng.""", clear=True),
        st(code_block(tu_kiem, lines=(27, 36)),
           """Phép làm thứ hai, hàm khẳng định ném ngoại lệ. Nó gọi hàm phí bên trong khối bắt lỗi. Nếu hàm phí chạy bình thường thì ca hỏng, vì lẽ ra phải ném. Chỉ khi bắt được đúng loại ngoại lệ thì ca mới đạt.""", clear=True),
        st(code_block(tu_kiem, lines=(38, 47)),
           """Phép làm thứ ba, bảy ca kiểm lấy thẳng từ bảng đã suy ra. Mỗi ca ghi giá trị mong đợi trước, rồi mới gọi hàm.""", clear=True),
        st("$$④ \\; \\text{dự đoán}: 7 \\text{ ca đạt}, \\; 0 \\text{ hỏng} \\quad (7 + 0 = 7)$$" + out_block(tu_kiem),
           """Phép làm thứ tư, ta dự đoán trước là bảy ca đạt, không ca hỏng. Chạy thật, bảy dòng đạt và dòng tổng kết khớp với dự đoán. Hàm này đúng với đặc tả ở mọi biên.""", clear=True),
    ], checks=["7 + 0 == 7"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: cố tình gây lỗi, ca kiểm phải đỏ", [
        st("<p><b>Đối chứng âm.</b> Ca kiểm xanh chưa chứng minh gì nếu nó <b>không thể đỏ</b>. Ta đổi hai dấu <code>&lt;=</code> thành <code>&lt;</code> trong hàm phí rồi chạy lại đúng bảy ca:</p>"
           + out_block(tu_kiem_loi),
           """Cách kiểm khác là cố tình gây lỗi. Ca kiểm xanh chưa chứng minh gì nếu nó không thể đỏ. Ta đổi hai dấu nhỏ hơn hoặc bằng thành nhỏ hơn rồi chạy lại đúng bảy ca. Hai ca ở đúng biên báo hỏng, và nói rõ mong đợi bao nhiêu, thực tế bao nhiêu.
           Năm ca còn lại vẫn đạt, nên ta biết lỗi nằm ở biên chứ không ở chỗ khác.""", clear=True),
        st("<p>Đếm: 7 ca = <b>5</b> đạt + <b>2</b> hỏng; hai ca hỏng là <b>đúng hai ca ở biên</b>, khớp với phép suy luận ở bước hai.</p>"
           "<p>Bỏ hai ca biên khỏi bảng thì chỉ còn <b>5</b> ca, <b>tất cả đều xanh</b>, và lỗi lọt qua mà không ai biết.</p>",
           """Ta đếm lại, bảy ca gồm năm đạt và hai hỏng. Vì hai ca hỏng chính là hai ca biên, nên phép suy luận ở bước hai là đúng. Nếu bỏ hai ca biên khỏi bảng thì chỉ còn năm ca, tất cả đều xanh, và lỗi lọt qua mà không ai biết.""", clear=True),
    ], checks=["5 + 2 == 7"])
    sc_ju = sc("junit", "concept", "Cùng ca kiểm, viết bằng JUnit 5 như dự án thật", [
        st(pcode(ju, "PhiChuyenTest.java", lines=(4, 10), title="Tệp PhiChuyenTest.java (đầu tệp)"),
           """Trong dự án thật, người ta không tự viết hàm khẳng định mà dùng một bộ kiểm thử chuẩn có sẵn. Mỗi ca kiểm là một hàm có nhãn kiểm thử. Khẳng định bằng nhau nhận giá trị mong đợi trước, giá trị thực sau. Ta chỉ cần bốn ca để giữ ngắn.""", clear=True),
        st("<p>Công cụ tải về một tệp, đặt vào thư mục <code>lib</code>; kiểm băm để chắc không bị thay (băm đầy đủ ở <code>labs/ENV.md</code>):</p>"
           + term_block(tai, 0, 1)
           + "<p class='note'>Lệnh tải bằng <code>curl -L -o</code> và địa chỉ chính thức nằm ở <code>labs/ENV.md</code>, mục tệp tải thêm.</p>",
           """Công cụ chỉ là một tệp đóng gói, tải về bỏ vào thư mục thư viện. Ta kiểm băm của nó để chắc tệp không bị thay đổi. Địa chỉ tải và băm đầy đủ nằm trong tệp môi trường của khoá học.""", clear=True),
        st(term_block(ju, 0, 4, title="Biên dịch kèm tệp đóng gói; chạy; chỉ xem hai dòng tổng kết"),
           """Ta đặt tên tệp đóng gói vào một biến cho ngắn, biên dịch với đường dẫn tìm lớp có thêm tệp đó, rồi định nghĩa một hàm chạy bộ kiểm thử trên thư mục đích. Ta lọc lấy hai dòng tổng kết. Bốn ca thành công, không ca hỏng.""", clear=True),
        st(term_block(ju, 4, 7, title="Gây lỗi biên rồi chạy lại: bộ kiểm thử nói rõ mong đợi và thực tế"),
           """Ta cố tình gây lỗi, đổi dấu ở biên, biên dịch lại và chạy. Bộ kiểm thử báo ba ca thành công, một ca hỏng, và nói rõ mong đợi một nghìn nhưng thực tế là năm nghìn. Đúng như bộ khẳng định tự viết, chỉ khác là có sẵn, chạy được cả trăm ca cùng lúc.""", clear=True),
    ])
    sc_scale = sc("scale", "concept", "Khi đầu vào nhiều lên: không kiểm hết được, phải chọn", [
        st(table(["số đầu vào của hàm", "1 (kiểu long)", "2 đầu vào", "3 đầu vào"],
                 [["tổng số giá trị có thể", "2<sup>64</sup> ≈ 1,8 × 10<sup>19</sup>", "2<sup>128</sup>", "2<sup>192</sup>"],
                  ["thời gian kiểm hết, mỗi ca 1 nano giây", "<b>≈ 584 năm</b>", "vô hạn trong thực tế", "vô hạn trong thực tế"]]),
           """Bây giờ là chuyện quy mô. Một số nguyên dài có hai mũ sáu mươi bốn giá trị, cỡ mười tám tỉ tỉ. Nếu mỗi ca kiểm tốn một nano giây, kiểm hết một đầu vào cần khoảng năm trăm tám mươi bốn năm. Hai đầu vào thì bình phương con số đó. Kiểm hết là không thể, nên ta buộc phải chọn.""", clear=True),
        st(table(["số đầu vào độc lập, mỗi đầu vào 5 lớp", "3", "6", "10"],
                 [["mọi tổ hợp", "125", "15 625", "<b>9 765 625</b>"],
                  ["chỉ kiểm biên từng đầu vào (≈ 2 × 5 mỗi đầu vào)", "30", "60", "<b>100</b>"]])
           + "<p class='note'>Đánh đổi: kiểm từng đầu vào cho ta lòng tin về <b>từng biên</b>, không bắt được lỗi chỉ xuất hiện ở một <b>tổ hợp</b> riêng. Người làm nghề thêm vài tổ hợp rủi ro cao (tiền lớn × khác ngân hàng) thay vì mọi tổ hợp.</p>",
           """Với nhiều đầu vào độc lập, mỗi đầu vào năm lớp, số tổ hợp tăng theo lũy thừa. Ba đầu vào là một trăm hai mươi lăm tổ hợp, mười đầu vào là gần mười triệu tổ hợp. Còn kiểm biên từng đầu vào chỉ tăng đều, mười đầu vào là một trăm ca.
           Đánh đổi là cách này không bắt được lỗi chỉ xuất hiện ở một tổ hợp riêng, nên người làm nghề thêm vài tổ hợp rủi ro cao thay vì mọi tổ hợp.""", clear=True),
    ], checks=["2**64 == 18446744073709551616", "round(2**64 / 1e9 / 3600 / 24 / 365.25) == 585 or round(2**64 / 1e9 / 3600 / 24 / 365.25) == 584",
               "5**3 == 125", "5**6 == 15625", "5**10 == 9765625", "2 * 5 * 3 == 30", "2 * 5 * 6 == 60", "2 * 5 * 10 == 100"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> So sánh số thực bằng <code>==</code> trong khẳng định.</div>'
           + code_block(so_thuc, lines=(3, 5)) + out_block(so_thuc),
           """Lỗi thứ nhất là so sánh số thực bằng dấu bằng. Không phẩy một cộng không phẩy hai không đúng bằng không phẩy ba, vì số thực lưu gần đúng. Ca kiểm như vậy hỏng dù hàm đúng. Cách làm đúng là so với một sai số cho phép. Với tiền, hãy dùng số nguyên theo đồng để tránh hẳn chuyện này."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Ca kiểm xanh giả: nuốt ngoại lệ nên không bao giờ hỏng.</div>'
           + code_block(xanh_gia, lines=(7, 12)) + out_block(xanh_gia),
           """Lỗi thứ hai là ca kiểm xanh giả. Ca A bắt mọi ngoại lệ và coi cả hai nhánh là đạt, nên dù hàm quên kiểm số không, ca vẫn đạt. Ca B đúng, chỉ đạt khi có ném đúng loại ngoại lệ, và nó báo hỏng. Một ca kiểm không thể hỏng thì không có giá trị gì.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Các ca kiểm dùng chung trạng thái, nên kết quả phụ thuộc thứ tự chạy.</div>'
           + code_block(thu_tu, lines=(2, 14)),
           """Lỗi thứ ba hay gặp ở người đã đi làm. Hai ca kiểm cùng dùng một biến số dư dùng chung. Ca A nạp một trăm, ca B rút năm mươi và tin rằng số dư đang là một trăm. Ca B chỉ đạt nếu ca A đã chạy trước.""", clear=True),
        st(code_block(thu_tu, lines=(16, 23)) + out_block(thu_tu),
           """Chạy theo thứ tự A rồi B thì cả hai đạt. Đổi thành B rồi A thì ca B hỏng, dù mã không đổi một chữ. Bộ kiểm thử thật có thể chạy theo thứ tự bất kỳ, nên mỗi ca kiểm phải tự dựng dữ liệu của chính nó và không dựa vào ca khác.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Đặc tả: phí rút tiền ATM là <b>0</b> nếu số tiền <b>dưới 3 000 000</b>, <b>0,1%</b> nếu từ 3 000 000 trở lên (số minh hoạ).</p>
<ol><li>Chọn các ca ở <b>biên</b> (đúng biên và ngay sau biên); ghi giá trị đầu vào và <b>mong đợi</b>.</li>
<li>Hàm viết <code>if (t &lt;= 3000000)</code> (sai dấu): ca nào trong bảng của bạn <b>hỏng</b>?</li></ol>
<p><b>Chọn A hay B?</b> Cần kiểm hàm có 4 đầu vào, mỗi đầu vào 6 lớp. A: mọi tổ hợp. B: biên từng đầu vào cộng vài tổ hợp rủi ro. Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Đặc tả nói phí rút tiền là không đồng nếu số tiền dưới ba triệu, và không phẩy một phần trăm nếu từ ba triệu trở lên. Hãy chọn các ca ở biên, ghi đầu vào và mong đợi. Rồi nếu hàm viết sai dấu thì ca nào hỏng.
           Cuối cùng chọn giữa mọi tổ hợp và biên từng đầu vào cho hàm bốn đầu vào, mỗi đầu vào sáu lớp, và giải thích vì sao. Hãy dừng video và tự làm.""", pause=30),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "2 999 999 → 0; <b>3 000 000 → 3 000</b>; 3 000 001 → 3 000", "đúng biên là 3 000 000 (từ đó trở lên), 0,1% × 3 000 000 = 3 000; số ngay trước biên cũng cần"],
                  ["2", "ca <b>3 000 000</b> hỏng (hàm cho 0, mong 3 000)", "dấu <code>&lt;=</code> đẩy đúng biên sang bậc miễn phí"],
                  ["3", "<b>B</b>", "6<sup>4</sup> = 1 296 tổ hợp so với 4 × 12 = 48 ca biên; chọn thêm vài tổ hợp rủi ro"]]),
           """Đáp án câu một, ca ngay trước biên cho phí không, ca đúng ba triệu và ca ngay sau biên đều cho phí ba nghìn. Biên đúng là ba triệu, vì từ ba triệu trở lên mới tính phí, và không phẩy một phần trăm của ba triệu là ba nghìn.
           Câu hai, ca đúng ba triệu hỏng, vì dấu nhỏ hơn hoặc bằng đẩy đúng biên sang bậc miễn phí. Câu ba chọn phương án B, vì sáu mũ bốn là một nghìn hai trăm chín mươi sáu tổ hợp, so với bốn mươi tám ca biên.""",
           focus=[1, "1.2", "1.3", "1.4"]),
        st("""<div class="box key"><b>Quy tắc:</b> mong đợi lấy từ <b>đặc tả</b>; đặt ca ở <b>biên</b> và ngay sau biên; mỗi ca <b>tự dựng dữ liệu</b>; và luôn thử <b>gây lỗi cố ý</b> để chắc ca kiểm có thể đỏ.</div>""",
           """Quy tắc rút ra. Giá trị mong đợi lấy từ đặc tả. Đặt ca ở biên và ngay sau biên. Mỗi ca tự dựng dữ liệu của nó. Và luôn thử gây lỗi cố ý để chắc ca kiểm có thể đỏ."""),
    ], checks=["3000000 * 1 // 1000 == 3000", "6**4 == 1296", "4 * 12 == 48", "2 * 6 == 12"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("đặc tả → vùng và biên", "mỗi biên hai ca", "mong đợi lấy từ đặc tả", "khẳng định: mong đợi vs thực tế",
                 "gây lỗi cố ý: ca phải đỏ", "không kiểm hết: chọn theo rủi ro"),
           """Tổng kết chuỗi logic. Từ đặc tả, tìm các vùng và các biên. Mỗi biên hai ca, đúng biên và ngay sau biên. Mong đợi lấy từ đặc tả. Khẳng định so mong đợi với thực tế. Gây lỗi cố ý để chắc ca kiểm có thể đỏ.
           Và vì không thể kiểm hết, ta chọn ca theo rủi ro."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi tin một ca kiểm xanh, hỏi ba câu: nếu mã sai thì <b>nó có đỏ không</b>, mong đợi của nó lấy từ <b>đặc tả hay từ mã</b>,
và nó có <b>chạy độc lập</b> khi đổi thứ tự không.</div>""",
           """Điều cần mang theo. Trước khi tin một ca kiểm xanh, hãy hỏi ba câu. Nếu mã sai thì nó có đỏ không. Mong đợi của nó lấy từ đặc tả hay từ mã. Và nó có chạy độc lập khi đổi thứ tự không."""),
    ])
    return lesson("L06", "kiem_thu_don_vi", "Bài 6 — Kiểm thử đơn vị: ca ở biên, khẳng định, JUnit 5",
                  "curriculum/jv2.yaml L06; audit/jv2/verify_jv2.py L06 (javac/java chạy thật, JDK 21; JUnit Platform Console Standalone 1.10.2, sha256 ở labs/ENV.md); "
                  "JUnit 5 User Guide (junit.org/junit5/docs/current/user-guide: @Test, assertEquals, assertThrows); "
                  "Myers, G. J. (1979), The Art of Software Testing, chương 4 (phân hoạch lớp tương đương, phân tích giá trị biên); "
                  "IEEE 754 (số thực nhị phân) cho ca 0,1 + 0,2; The Java Language Specification, Java SE 21: §15.20.1; dev.java/learn",
                  ["Chọn các ca kiểm ở biên và ngay sau biên từ đặc tả",
                   "Viết khẳng định tự viết và chạy bảy ca kiểm thật",
                   "Dùng JUnit 5 để chạy cùng các ca kiểm và đọc kết quả đạt hay hỏng",
                   "Nêu vì sao phải gây lỗi cố ý để chắc ca kiểm có thể đỏ",
                   "Nhận ra vì sao không kiểm hết được và số tổ hợp bùng nổ ra sao",
                   "Viết năm ca kiểm cho hàm phí chuyển khoản và tìm lỗi biên"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_ju, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "formula"), (2, "example"), (3, "junit"), (4, "check"), (5, "scale"), (6, "practice")])
