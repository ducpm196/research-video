from lib import *
from labkit import write_lab, practice_steps, practice_scene


def part(p, a, b):
    """Bản sao của p chỉ giữ các dòng in ra từ a tới b (để hiện từng phần kết quả)."""
    return dict(p, out="\n".join(p["out"].split("\n")[a:b]))


def build():
    ngay = prog("Ngay", r"""
import java.time.LocalDate;
import java.time.Period;
import java.time.temporal.ChronoUnit;

public class Ngay {
    public static void main(String[] args) {
        LocalDate tu = LocalDate.of(2026, 2, 10);
        LocalDate den = LocalDate.of(2026, 5, 10);
        System.out.println(ChronoUnit.DAYS.between(tu, den));
        System.out.println(Period.between(tu, den));
        System.out.println(LocalDate.of(2026, 1, 31).plusMonths(1));
        System.out.println(LocalDate.of(2028, 1, 31).plusMonths(1));
        System.out.println(LocalDate.of(2026, 1, 31).plusDays(30));
    }
}""", out="89\nP3M\n2026-02-28\n2028-02-29\n2026-03-02")
    gio = prog("GioToanCau", r"""
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;

public class GioToanCau {
    public static void main(String[] args) {
        Instant t = Instant.parse("2026-03-08T07:30:00Z");               // một điểm trên trục thời gian
        System.out.println(t.atZone(ZoneId.of("Asia/Ho_Chi_Minh")));
        System.out.println(t.atZone(ZoneId.of("America/New_York")));
        ZoneId ny = ZoneId.of("America/New_York");
        ZonedDateTime a = ZonedDateTime.of(2026, 3, 8, 0, 0, 0, 0, ny);
        System.out.println(Duration.between(a, a.plusDays(1)));          // ngày chuyển sang giờ mùa hè
        ZonedDateTime b = ZonedDateTime.of(2026, 11, 1, 0, 0, 0, 0, ny);
        System.out.println(Duration.between(b, b.plusDays(1)));          // ngày lùi về giờ chuẩn
    }
}""", out="2026-03-08T14:30+07:00[Asia/Ho_Chi_Minh]\n2026-03-08T03:30-04:00[America/New_York]\nPT23H\nPT25H")
    tien_double = prog("TienDouble", r"""
import java.math.BigDecimal;

public class TienDouble {
    public static void main(String[] args) {
        System.out.println(0.1 * 3);
        System.out.println(new BigDecimal("0.1").multiply(new BigDecimal("3")));
        System.out.println(new BigDecimal(0.1));                         // từ số thực: lấy luôn sai số
        System.out.println(BigDecimal.valueOf(0.1));                     // từ chữ số của số thực: 0.1
    }
}""", out="0.30000000000000004\n0.3\n0.1000000000000000055511151231257827021181583404541015625\n0.1")
    lai_ngay = prog("LaiNgay", r"""
import java.math.BigDecimal;
import java.math.RoundingMode;

public class LaiNgay {
    public static void main(String[] args) {
        BigDecimal goc = new BigDecimal("100000000");
        BigDecimal laiSuat = new BigDecimal("0.072");                    // 7,2% một năm (số minh hoạ)
        BigDecimal tich = goc.multiply(laiSuat).multiply(BigDecimal.valueOf(89));
        BigDecimal lai = tich.divide(BigDecimal.valueOf(365), 0, RoundingMode.HALF_UP);
        System.out.println(tich);
        System.out.println(lai);
        System.out.println(goc.add(lai));
    }
}""", out="640800000.000\n1755616\n101755616")
    lam_tron = prog("LamTron", r"""
import java.math.BigDecimal;
import java.math.RoundingMode;

public class LamTron {
    static String dong(String s) {
        BigDecimal x = new BigDecimal(s);
        return s + ": HALF_UP " + x.setScale(0, RoundingMode.HALF_UP) + ", HALF_EVEN " + x.setScale(0, RoundingMode.HALF_EVEN)
                + ", DOWN " + x.setScale(0, RoundingMode.DOWN);
    }

    static void lech(int n) {
        BigDecimal dung = BigDecimal.ZERO, len = BigDecimal.ZERO, chan = BigDecimal.ZERO;
        for (int i = 0; i < n; i++) {
            BigDecimal v = new BigDecimal(i).add(new BigDecimal("0.5"));   // phần lẻ luôn 0,5
            dung = dung.add(v);
            len = len.add(v.setScale(0, RoundingMode.HALF_UP));
            chan = chan.add(v.setScale(0, RoundingMode.HALF_EVEN));
        }
        System.out.println(n + " giao dich: lech HALF_UP " + len.subtract(dung)
                + ", lech HALF_EVEN " + chan.subtract(dung));
    }

    public static void main(String[] args) {
        System.out.println(dong("2.5"));
        System.out.println(dong("3.5"));
        System.out.println(dong("-2.5"));
        lech(1000);
        lech(1000000);
    }
}""", out="2.5: HALF_UP 3, HALF_EVEN 2, DOWN 2\n3.5: HALF_UP 4, HALF_EVEN 4, DOWN 3\n-2.5: HALF_UP -3, HALF_EVEN -2, DOWN -2\n"
             "1000 giao dich: lech HALF_UP 500.0, lech HALF_EVEN 0.0\n1000000 giao dich: lech HALF_UP 500000.0, lech HALF_EVEN 0.0")
    dinh_dang = prog("DinhDang", r"""
import java.text.NumberFormat;
import java.util.Locale;

public class DinhDang {
    public static void main(String[] args) throws Exception {
        double x = 1234567.891;
        Locale vi = Locale.forLanguageTag("vi-VN");
        System.out.println(String.format(Locale.US, "%,.2f", x));
        System.out.println(String.format(vi, "%,.2f", x));
        try {
            Double.parseDouble("1.234,5");                                  // chỉ hiểu dấu chấm thập phân
        } catch (NumberFormatException e) {
            System.out.println("parseDouble: that bai");
        }
        System.out.println(NumberFormat.getInstance(vi).parse("1.234,5"));
    }
}""", out="1,234,567.89\n1.234.567,89\nparseDouble: that bai\n1234.5")

    lab = prog("LaiTheoNgay", r"""
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class LaiTheoNgay {
    public static void main(String[] args) {
        LocalDate gui = LocalDate.of(2026, 1, 15);
        LocalDate den = LocalDate.of(2026, 4, 20);
        long soNgay = ChronoUnit.DAYS.between(gui, den);
        BigDecimal goc = new BigDecimal("120000000");
        BigDecimal lai = goc.multiply(new BigDecimal("0.06")).multiply(BigDecimal.valueOf(soNgay))
                .divide(BigDecimal.valueOf(365), 0, RoundingMode.HALF_UP);
        System.out.println("So ngay: " + soNgay);
        System.out.println("Lai: " + lai);
        System.out.println("Tong: " + goc.add(lai));
        System.out.println("Dao han la: " + den.getDayOfWeek());
    }
}""", out="So ngay: 95\nLai: 1873973\nTong: 121873973\nDao han la: MONDAY")
    write_lab("JV2", "L08", """# Lab JV2 L08 — Lãi theo ngày, đúng đến từng đồng

Gửi **120 000 000 đồng** ngày **2026-01-15**, đáo hạn ngày **2026-04-20**, lãi **6% một năm** (số minh hoạ). Lãi tính theo công thức
`lãi = gốc × lãi suất × số ngày / 365`, **làm tròn HALF_UP về đồng**.

Viết `LaiTheoNgay` (tệp `LaiTheoNgay.java`):
1. Đếm số ngày bằng `ChronoUnit.DAYS.between` (không tự cộng tay).
2. Tính lãi bằng `BigDecimal` **tạo từ chuỗi** (`new BigDecimal("0.06")`), chia bằng `divide(…, 0, RoundingMode.HALF_UP)`.
3. In bốn dòng đúng dạng:

```
So ngay: 95
Lai: 1873973
Tong: 121873973
Dao han la: MONDAY
```

(`Dao han la` là `getDayOfWeek()` của ngày đáo hạn.) Tự tính tay trước: số ngày từ 15 tháng 1 tới 15 tháng 4 là 31 + 28 + 31 = 90, cộng 5 ngày nữa.

Chạy: `javac LaiTheoNgay.java && java LaiTheoNgay`. Chấm: `bash labs/cham.sh JV2 L08 LaiTheoNgay.java`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: lãi theo ngày cho khoản gửi 120 triệu", pr_steps(
        st, "JV2", "L08",
        """<p><b>Đề</b>: gửi <b>120 000 000</b> đồng ngày <b>2026-01-15</b>, đáo hạn <b>2026-04-20</b>, lãi <b>6%</b> một năm (số minh hoạ).</p>
<ol><li>Số ngày bằng <code>ChronoUnit.DAYS.between</code>.</li><li>Lãi = gốc × 0,06 × số ngày / 365, <code>BigDecimal</code> từ chuỗi, <code>HALF_UP</code> về đồng.</li>
<li>In: <code>So ngay</code>, <code>Lai</code>, <code>Tong</code>, <code>Dao han la</code> (thứ trong tuần).</li></ol>
<p class="note">Tệp <code>LaiTheoNgay.java</code>. Tính tay số ngày trước: 31 + 28 + 31 + 5.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Gửi một trăm hai mươi triệu đồng ngày mười lăm tháng một, đáo hạn ngày hai mươi tháng tư, lãi sáu phần trăm một năm. Hãy đếm số ngày bằng hàm có sẵn, tính lãi bằng số thập phân chính xác tạo từ chuỗi, làm tròn nửa lên về đồng.
        In số ngày, lãi, tổng, và thứ trong tuần của ngày đáo hạn. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        lab["out"], "LaiTheoNgay.java",
        """<div class="box key"><b>Nếu kẹt:</b> <code>goc.multiply(…)</code> với lãi suất, rồi <code>.multiply(…)</code> với số ngày, rồi <code>.divide(365, 0, HALF_UP)</code> (chia cho <code>BigDecimal.valueOf(365)</code>).
Thứ trong tuần: <code>den.getDayOfWeek()</code>. Lời giải: <code>labs/JV2/L08/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, nhân gốc với lãi suất rồi với số ngày, rồi chia cho ba trăm sáu mươi lăm với không chữ số thập phân và kiểu làm tròn nửa lên. Thứ trong tuần lấy từ ngày đáo hạn.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=180), "JV2", "L08")

    sc_hook = sc("hook", "hook", "Ba triệu giao dịch nửa đồng: cuối ngày lệch một triệu rưỡi đồng", [
        st(svg(1500, 300,
               box(20, 90, 340, 110, ["phí 2,5 đồng", "làm tròn → 3 đồng"], C_AMBER, 26, bold=True), arrow(365, 145, 470, 145, "#475569"),
               box(475, 90, 340, 110, ["lặp 1 000 000 lần", "mỗi lần thừa 0,5"], C_BLUE, 26, bold=True), arrow(820, 145, 925, 145, "#475569"),
               box(930, 60, 550, 170, ["cuối ngày lệch 500 000 đồng", "so với tổng đúng", "kiểm toán sẽ hỏi"], C_RED, 26, bold=True),
               txt(750, 275, "tiền và thời gian: hai thứ trông đơn giản nhất, sai nhiều nhất", 26, "middle", "#1f2937", True)),
           """Một khoản phí hai đồng rưỡi, làm tròn thành ba đồng. Nửa đồng thừa, nghe không đáng gì. Nhưng nếu một triệu giao dịch đều có phần lẻ đúng nửa đồng và luôn làm tròn lên, thì cuối ngày tổng lệch năm trăm nghìn đồng so với tổng đúng. Kiểm toán sẽ hỏi.
           Tiền và thời gian là hai thứ trông đơn giản nhất mà lại sai nhiều nhất."""),
        st("""<div class="box key">Hôm nay: <b>ngày giờ</b> (ngày, điểm thời gian, múi giờ, vì sao một ngày có khi chỉ 23 giờ) và <b>tiền</b> (<code>BigDecimal</code>, các kiểu làm tròn, định dạng theo vùng).
Rồi bài toán lãi theo ngày, và câu hỏi quy mô: sai lệch làm tròn lớn thế nào khi số giao dịch tăng một nghìn lần?</div>""",
           """Hôm nay ta học ngày giờ và tiền. Ngày, điểm thời gian, múi giờ, và vì sao một ngày có khi chỉ hai mươi ba giờ. Rồi số thập phân chính xác, các kiểu làm tròn, và định dạng theo vùng. Cuối cùng là bài toán lãi theo ngày, và câu hỏi quy mô, sai lệch làm tròn lớn thế nào khi số giao dịch tăng một nghìn lần.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: số thực lệch, tiền dùng số nguyên, tên đầy đủ", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① số thực lệch", "<code>0.1 + 0.2</code> ra <code>0.30000000000000004</code>: số thực lưu <b>gần đúng</b> nhị phân"],
                  ["② tiền bằng số nguyên", "tiền tính bằng <code>long</code> theo đồng để tránh sai số; chia nguyên <b>bỏ phần lẻ</b>"],
                  ["③ nạp tên", "<code>import java.time.LocalDate;</code> để viết <code>LocalDate</code> thay cho tên đầy đủ"],
                  ["④ ngoại lệ", "chuỗi sai định dạng thì <code>parse…</code> ném <code>NumberFormatException</code>"]]),
           """Ta ôn lại bốn điều. Số thực lưu gần đúng theo nhị phân, nên không phẩy một cộng không phẩy hai lệch một chút. Tiền nên tính bằng số nguyên theo đồng, và chia nguyên bỏ phần lẻ. Muốn viết tên ngắn thì nạp tên từ gói. Và chuỗi sai định dạng thì hàm đổi số ném ngoại lệ.
           Bài này đưa ra lời giải đầy đủ hơn cho hai điều đầu.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã bảy thứ của ngày giờ và tiền", [
        st(table(["viết", "nghĩa"],
                 [["<code>LocalDate</code>", "<b>ngày lịch</b> (năm-tháng-ngày), không có giờ, không có múi giờ"],
                  ["<code>Instant</code>", "<b>một điểm duy nhất</b> trên trục thời gian, tính theo UTC; mọi nơi trên thế giới cùng đồng ý đó là lúc nào"],
                  ["<code>ZonedDateTime</code>", "<b>cách một nơi cụ thể đọc</b> một điểm thời gian: ngày, giờ và độ lệch múi giờ"],
                  ["<code>Duration</code> / <code>Period</code>", "khoảng thời gian <b>theo giờ-giây</b> / <b>theo ngày-tháng-năm lịch</b>"],
                  ["<code>BigDecimal</code>", "số thập phân <b>chính xác</b>, dùng cho tiền; tạo từ <b>chuỗi</b>, không tạo từ số thực"],
                  ["<code>RoundingMode</code>", "quy tắc làm tròn: <code>HALF_UP</code> (5 thì lên), <code>HALF_EVEN</code> (5 thì về số chẵn), <code>DOWN</code> (bỏ phần lẻ)"],
                  ["<code>Locale</code>", "vùng ngôn ngữ: quy định dấu ngăn nghìn, dấu thập phân khi <b>in và đọc số</b>"]]),
           """Bảng này có bảy thứ. Ngày lịch chỉ có năm, tháng, ngày. Điểm thời gian là một điểm duy nhất trên trục thời gian, mọi nơi cùng đồng ý đó là lúc nào. Ngày giờ có múi giờ là cách một nơi cụ thể đọc điểm đó.
           Khoảng thời gian có hai loại, theo giờ và giây, hoặc theo ngày, tháng, năm lịch. Số thập phân chính xác dùng cho tiền, và phải tạo từ chuỗi. Kiểu làm tròn quy định năm thì làm gì. Cuối cùng vùng ngôn ngữ quy định dấu ngăn nghìn và dấu thập phân khi in và đọc số.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: một điểm thời gian, nhiều cách đọc", [
        st(svg(1500, 380,
               '<line x1="40" y1="190" x2="1460" y2="190" stroke="#475569" stroke-width="4"/>',
               '<circle cx="740" cy="190" r="14" fill="#dc2626"/>',
               box(540, 20, 400, 80, ["Instant", "2026-03-08T07:30:00Z"], C_AMBER, 26, bold=True), arrow(740, 105, 740, 170, "#dc2626"),
               box(60, 260, 560, 90, ["TP. Hồ Chí Minh", "14:30 ngày 8 tháng 3 (UTC+7)"], C_BLUE, 26, bold=True),
               box(880, 260, 580, 90, ["New York", "03:30 ngày 8 tháng 3 (giờ mùa hè UTC−4)"], C_GREEN, 26, bold=True),
               arrow(700, 205, 340, 255, "#2a78d6"), arrow(780, 205, 1170, 255, "#16a34a")),
           """Hình dung một điểm thời gian là một khoảnh khắc duy nhất, chấm đỏ trên trục. Thành phố Hồ Chí Minh đọc nó là mười bốn giờ ba mươi. Một thành phố bên Bắc Mỹ đọc cùng khoảnh khắc đó là ba giờ ba mươi sáng, trong múi giờ mùa hè. Khoảnh khắc không đổi, chỉ cách đọc khác nhau.
           Vì thế hệ thống nên lưu điểm thời gian, và chỉ đổi sang giờ địa phương khi hiển thị."""),
        st(code_block(gio, lines=(8, 10)),
           """Đây là đoạn mã thật. Ta tạo một điểm thời gian từ chuỗi, rồi hỏi hai múi giờ đọc nó thế nào.""", clear=True),
        st(code_block(gio, lines=(11, 15)) + out_block(part(gio, 2, 4)),
           """Một chi tiết nữa. Thành phố bên Bắc Mỹ này chuyển sang giờ mùa hè vào đúng ngày tám tháng ba, nên ngày đó chỉ có hai mươi ba giờ. Ngày một tháng mười một lùi giờ nên có hai mươi lăm giờ. Hãy nhớ, một ngày không phải lúc nào cũng dài hai mươi bốn giờ.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: công thức lãi theo ngày và vì sao dùng số thập phân chính xác", [
        st("<p><b>Bước 1.</b> Lãi đơn theo ngày: <b>lãi = gốc × lãi suất năm × số ngày / 365</b>.</p><p>Vì lãi suất là <b>mỗi năm</b>, nên phần của năm là <code>số ngày / 365</code>.</p>",
           """Bước một, công thức lãi đơn theo ngày. Vì lãi suất tính cho cả năm, nên phần của năm mà khoản gửi tồn tại là số ngày chia ba trăm sáu mươi lăm. Nhân phần đó với gốc và lãi suất ta được lãi.""", clear=True),
        st("<p><b>Bước 2.</b> Số ngày <b>do máy đếm</b>: <code>ChronoUnit.DAYS.between(gui, den)</code>.</p>"
           "<p>Vì sao không tự cộng: tháng dài ngắn khác nhau, năm nhuận thêm một ngày; máy biết lịch, ta dễ sai.</p>",
           """Bước hai, số ngày để máy đếm. Vì tháng dài ngắn khác nhau và năm nhuận có thêm một ngày, nên tự cộng tay rất dễ sai, còn máy biết lịch.""", clear=True),
        st("<p><b>Bước 3.</b> Tính bằng <b>số thập phân chính xác</b>, nhân hết rồi <b>chia sau cùng một lần</b>:</p>"
           "<p><code>gốc × lãi suất × ngày</code> (chính xác) rồi <code>÷ 365</code>, làm tròn <b>một lần</b>.</p>"
           "<p>Vì sao chia cuối: mỗi lần làm tròn ở giữa chừng đều thêm sai số.</p>",
           """Bước ba, nhân hết rồi chia ở cuối cùng, làm tròn đúng một lần. Vì mỗi lần làm tròn ở giữa chừng đều thêm một chút sai số, nên làm tròn càng muộn càng tốt.""", clear=True),
        st("<p><b>Bước 4.</b> Thử bằng số nguyên làm đường khác: nhân lãi suất <code>0,072</code> thành <code>72 / 1000</code>:</p>"
           "$$\\frac{100\\,000\\,000 \\times 72 \\times 89}{1\\,000 \\times 365} = \\frac{640\\,800\\,000\\,000}{365\\,000} \\approx 1\\,755\\,616{,}43 \\to \\hl{1\\,755\\,616}$$",
           """Bước bốn, thử bằng số nguyên. Vì lãi suất bảy phẩy hai phần trăm là bảy mươi hai phần nghìn, nên ta nhân tử số với bảy mươi hai và mẫu số với một nghìn. Tử số là sáu trăm bốn mươi tỉ tám trăm triệu, mẫu số là ba trăm sáu mươi lăm nghìn. Kết quả một triệu bảy trăm năm mươi lăm nghìn sáu trăm mười sáu phẩy bốn ba, làm tròn về một triệu bảy trăm năm mươi lăm nghìn sáu trăm mười sáu.""", clear=True),
    ], checks=["100000000 * 72 * 89 == 640800000000", "1000 * 365 == 365000", "round(640800000000 / 365000) == 1755616", "int(640800000000 / 365000 * 100) == 175561643"])
    sc_ex = sc("example", "example", "Ví dụ: lãi 89 ngày, từng bước, chạy thật", [
        st(code_block(ngay, lines=(7, 11)) + out_block(part(ngay, 0, 2)),
           """Phép làm thứ nhất, đếm ngày. Từ mười tháng hai tới mười tháng năm có tám mươi chín ngày. Cùng khoảng đó theo lịch là ba tháng. Hai cách đo khác nhau, và ta cần cách đếm ngày cho lãi.""", clear=True),
        st("$$① \\; 28 + 31 + 30 = \\hl{89} \\text{ ngày}$$"
           "<p>(10/2 → 10/3: 28 ngày; → 10/4: 31 ngày; → 10/5: 30 ngày.)</p>",
           """Phép làm thứ hai, kiểm bằng tay. Từ mười tháng hai tới mười tháng ba là hai mươi tám ngày, tới mười tháng tư là ba mươi mốt, tới mười tháng năm là ba mươi. Cộng lại tám mươi chín, khớp với máy.""", clear=True),
        st(code_block(lai_ngay, lines=(6, 12)) + out_block(lai_ngay),
           """Phép làm thứ ba, tính lãi. Tích gốc, lãi suất và số ngày là sáu trăm bốn mươi triệu tám trăm nghìn, vẫn chính xác, có ba chữ số thập phân vì lãi suất có ba chữ số. Chia ba trăm sáu mươi lăm, làm tròn nửa lên về đồng, được một triệu bảy trăm năm mươi lăm nghìn sáu trăm mười sáu.""", clear=True),
        st("$$② \\; 100\\,000\\,000 \\times 0{,}072 \\times 89 = \\hl{640\\,800\\,000}$$"
           "$$③ \\; 640\\,800\\,000 / 365 \\approx 1\\,755\\,616{,}43 \\to \\hl{1\\,755\\,616}$$"
           "$$④ \\; 100\\,000\\,000 + 1\\,755\\,616 = \\hl{101\\,755\\,616}$$",
           """Phép làm thứ tư, năm và sáu, kiểm bằng tay ba bước. Tích là sáu trăm bốn mươi triệu tám trăm nghìn. Chia ba trăm sáu mươi lăm được một triệu bảy trăm năm mươi lăm nghìn sáu trăm mười sáu phẩy bốn ba. Cộng với gốc được một trăm linh một triệu bảy trăm năm mươi lăm nghìn sáu trăm mười sáu. Khớp với chương trình.""", clear=True),
        st(code_block(lam_tron, lines=(24, 26)) + out_block(part(lam_tron, 0, 3)),
           """Phép làm thứ năm, ba cách làm tròn. Hai rưỡi: nửa lên cho ba, nửa về số chẵn cho hai, bỏ phần lẻ cho hai. Ba rưỡi: nửa lên cho bốn, nửa về số chẵn cũng bốn, bỏ phần lẻ cho ba. Số âm hai rưỡi: nửa lên cho âm ba, bỏ phần lẻ cho âm hai. Cùng một con số, kiểu làm tròn khác nhau cho kết quả khác nhau.""", clear=True),
    ], checks=["28 + 31 + 30 == 89", "100000000 * 72 // 1000 * 89 == 640800000", "round(640800000 / 365) == 1755616", "100000000 + 1755616 == 101755616"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: cùng phép tính bằng số nguyên", [
        st("<p>Đường khác: tính bằng <b>số nguyên</b>, làm tròn nửa lên bằng cách <b>cộng nửa mẫu số</b> rồi chia nguyên:</p>"
           "$$\\frac{640\\,800\\,000 \\times 1\\,000 + 365\\,000 / 2}{365\\,000} \\;\\Rightarrow\\; (640\\,800\\,000\\,000 + 182\\,500) / 365\\,000 = \\hl{1\\,755\\,616}$$"
           "<p>Trùng với kết quả của <code>BigDecimal</code> ✓. Vì phép chia nguyên bỏ phần lẻ, thêm nửa mẫu số trước khi chia chính là &ldquo;5 thì lên&rdquo;.</p>",
           """Đường kiểm khác là tính bằng số nguyên. Muốn làm tròn nửa lên bằng phép chia nguyên, ta cộng thêm nửa mẫu số vào tử số rồi mới chia. Vì phép chia nguyên bỏ phần lẻ, nên thêm nửa mẫu số trước khi chia chính là quy tắc năm thì lên. Kết quả vẫn là một triệu bảy trăm năm mươi lăm nghìn sáu trăm mười sáu.""", clear=True),
        st(code_block(tien_double, lines=(5, 8)) + out_block(tien_double),
           """Kiểm thêm lý do không dùng số thực cho tiền. Số thực cho ra không phẩy ba mươi chữ số lệch. Số thập phân chính xác tạo từ chuỗi cho đúng không phẩy ba. Và nếu tạo từ số thực thì ta nhận luôn sai số, như dòng thứ ba. Chỉ khi tạo từ chuỗi chữ số, hoặc dùng hàm tạo từ biểu diễn chữ của số thực, mới sạch.""", clear=True),
    ], checks=["(640800000 * 1000 + 365000 // 2) // 365000 == 1755616", "365000 // 2 == 182500", "640800000 * 1000 == 640800000000"])
    sc_scale = sc("scale", "concept", "Khi số giao dịch tăng một nghìn lần: sai lệch làm tròn cộng dồn", [
        st(code_block(lam_tron, lines=(11, 21)),
           """Ta đo sai lệch cộng dồn. Mỗi giao dịch có phần lẻ đúng nửa đồng, ta so tổng đúng với tổng sau khi làm tròn bằng hai cách, nửa lên và nửa về số chẵn. Đây là trường hợp xấu nhất, nhưng nó có thật, ví dụ khi chia đôi một số lẻ.""", clear=True),
        st(table(["số giao dịch", "1 000", "1 000 000", "1 000 000 000"],
                 [["lệch khi luôn làm tròn nửa lên (đo thật tới 1 triệu)", "500", "<b>500 000</b>", "<b>500 000 000</b> (tính)"],
                  ["lệch khi làm tròn nửa về số chẵn (đo thật)", "0", "0", "0"]])
           + "<p class='note'>Mỗi giao dịch thừa 0,5 đồng, nên lệch = 0,5 × số giao dịch. Với phần lẻ ngẫu nhiên, nửa lên lệch ít hơn; ngưỡng thật do quy định kế toán của đơn vị, không phải do ngôn ngữ lập trình.</p>",
           """Kết quả thật. Một nghìn giao dịch thì lệch năm trăm đồng. Một triệu giao dịch thì lệch năm trăm nghìn đồng. Một tỉ giao dịch thì lệch năm trăm triệu đồng, đây là con số tính từ quy luật. Làm tròn nửa về số chẵn thì phần thừa và phần thiếu triệt tiêu, nên không lệch.
           Đánh đổi, kiểu nửa về số chẵn cân bằng hơn nhưng khó giải thích với khách hàng. Quy tắc cuối cùng do quy định kế toán quyết định, và phải thống nhất một kiểu cho toàn hệ thống.""", clear=True),
    ], checks=["1000 // 2 == 500", "1000000 // 2 == 500000", "1000000000 // 2 == 500000000"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Cộng 30 ngày thay vì cộng 1 tháng.</div>'
           + code_block(ngay, lines=(11, 13)) + "<p class='note'>Kết quả thật: <code>2026-02-28</code>, <code>2028-02-29</code>, và <code>plusDays(30)</code> từ 31 tháng 1 ra <code>2026-03-02</code>.</p>",
           """Lỗi thứ nhất là cộng ba mươi ngày thay vì cộng một tháng. Cộng một tháng vào ngày ba mươi mốt tháng một cho ngày hai mươi tám tháng hai, vì thư viện lùi về ngày cuối tháng. Năm nhuận cho hai mươi chín. Còn cộng ba mươi ngày thì rơi vào mùng hai tháng ba. Hãy chọn đúng điều đặc tả muốn nói, một tháng hay ba mươi ngày."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Tạo <code>BigDecimal</code> từ số thực.</div>'
           + out_block(tien_double).replace("<div>0.30000000000000004</div>", "").replace("<div>0.3</div><div>0.1000", "<div>0.1000"),
           """Lỗi thứ hai là tạo số thập phân chính xác từ một số thực. Con số không phẩy một khi đã là số thực thì đã lệch, và hàm tạo lấy nguyên sai số đó, ra một dãy dài chữ số. Hãy tạo từ chuỗi, hoặc dùng hàm tạo từ biểu diễn chữ.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Định dạng và đọc số theo vùng mặc định của máy.</div>'
           + code_block(dinh_dang, lines=(7, 9)) + out_block(part(dinh_dang, 0, 2)),
           """Lỗi thứ ba hay gặp ở người đã đi làm. In số theo vùng ngôn ngữ thì dấu ngăn nghìn và dấu thập phân đổi chỗ cho nhau. Mã chạy đúng trên máy của bạn, rồi sai trên máy chủ đặt ở vùng khác, hoặc ngược lại.""", clear=True),
        st(code_block(dinh_dang, lines=(10, 15)) + out_block(part(dinh_dang, 2, 4)),
           """Hàm đọc số thông thường luôn dùng dấu chấm thập phân, nên chuỗi kiểu Việt Nam làm nó thất bại. Bộ đọc theo vùng ngôn ngữ thì hiểu đúng. Hãy chỉ rõ vùng ngôn ngữ ở mọi chỗ in và đọc.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Gửi <b>50 000 000</b> đồng, lãi <b>4,8%</b> một năm, <b>40</b> ngày, chia cho <b>365</b> (số minh hoạ).</p>
<ol><li>Tính lãi chính xác: <code>50 000 000 × 0,048 × 40 / 365</code>; làm tròn <b>HALF_UP</b> về đồng.</li>
<li>Nếu làm tròn <b>sau mỗi bước</b> (<code>50 000 000 × 0,048</code> rồi <code>× 40</code> rồi <code>/ 365</code>) thì có thể khác không? Vì sao tính một lần cuối vẫn tốt hơn?</li></ol>
<p><b>Chọn A hay B?</b> Lưu thời điểm giao dịch cho hệ thống có khách ở nhiều nước. A: <code>LocalDateTime</code> (giờ địa phương không kèm múi giờ). B: <code>Instant</code>. Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Gửi năm mươi triệu đồng, lãi bốn phẩy tám phần trăm một năm, bốn mươi ngày. Hãy tính lãi chính xác rồi làm tròn nửa lên về đồng. Rồi nói nếu làm tròn sau mỗi bước thì có thể khác không, và vì sao làm tròn một lần ở cuối vẫn tốt hơn.
           Cuối cùng chọn giữa ngày giờ địa phương không múi giờ và điểm thời gian để lưu thời điểm giao dịch cho khách ở nhiều nước, và giải thích. Hãy dừng video và tự làm.""", pause=30),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "50 000 000 × 0,048 = 2 400 000; × 40 = 96 000 000; / 365 = 263 013,69… → <b>263 014</b>", "chia ở cuối cùng, làm tròn một lần"],
                  ["2", "<b>có thể khác</b>; một lần cuối vẫn tốt hơn", "mỗi lần làm tròn giữa chừng thêm sai số, và sai số nhân lên ở các bước sau"],
                  ["3", "<b>B</b> (<code>Instant</code>)", "<code>LocalDateTime</code> không nói đó là giờ ở đâu; hai khách ở hai múi giờ cùng ghi 14:30 sẽ lẫn"]]),
           """Đáp án câu một. Năm mươi triệu nhân không phẩy không bốn tám bằng hai triệu bốn trăm nghìn, nhân bốn mươi được chín mươi sáu triệu. Chia ba trăm sáu mươi lăm được hai trăm sáu mươi ba nghìn không trăm mười ba phẩy sáu chín, làm tròn thành hai trăm sáu mươi ba nghìn không trăm mười bốn.
           Câu hai, làm tròn giữa chừng có thể khác, vì mỗi lần làm tròn thêm sai số rồi bị nhân lên. Câu ba chọn phương án B, vì giờ địa phương không kèm múi giờ không nói rõ đó là giờ ở đâu.""",
           focus=[1, "1.2", "1.3", "1.4", "1.4"]),
        st("""<div class="box key"><b>Quy tắc:</b> lưu <b>Instant</b>, hiển thị theo múi giờ; tiền bằng <b>BigDecimal từ chuỗi</b> (hoặc số nguyên đồng); <b>chia và làm tròn một lần ở cuối</b>; luôn chỉ rõ <b>Locale</b>.</div>""",
           """Quy tắc rút ra. Lưu điểm thời gian, hiển thị theo múi giờ. Tiền bằng số thập phân chính xác tạo từ chuỗi, hoặc số nguyên đồng. Chia và làm tròn một lần ở cuối. Và luôn chỉ rõ vùng ngôn ngữ."""),
    ], checks=["50000000 * 48 // 1000 == 2400000", "2400000 * 40 == 96000000", "round(96000000 / 365) == 263014", "int(96000000 / 365 * 100) == 26301369"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("lưu Instant, hiển thị theo múi giờ", "ngày không luôn 24 giờ", "tiền: BigDecimal từ chuỗi", "nhân hết, chia và làm tròn một lần cuối",
                 "chọn một kiểu làm tròn cho cả hệ thống", "chỉ rõ Locale"),
           """Tổng kết chuỗi logic. Lưu điểm thời gian và hiển thị theo múi giờ. Một ngày không luôn dài hai mươi bốn giờ. Tiền dùng số thập phân chính xác tạo từ chuỗi. Nhân hết rồi chia và làm tròn một lần ở cuối.
           Chọn một kiểu làm tròn cho cả hệ thống. Và luôn chỉ rõ vùng ngôn ngữ."""),
        st("""<div class='box key'><b>Tư duy:</b> với mọi con số tiền hay mốc thời gian, hỏi bốn câu: nó <b>thuộc múi giờ nào</b>, <b>ai quyết định</b> kiểu làm tròn, sai lệch nhỏ này <b>nhân với số giao dịch</b> thành bao nhiêu,
và máy khác có <b>vùng ngôn ngữ khác</b> thì còn đúng không.</div>""",
           """Điều cần mang theo. Với mọi con số tiền hay mốc thời gian, hãy hỏi bốn câu. Nó thuộc múi giờ nào. Ai quyết định kiểu làm tròn. Sai lệch nhỏ này nhân với số giao dịch thành bao nhiêu. Và máy khác có vùng ngôn ngữ khác thì còn đúng không."""),
    ])
    return lesson("L08", "thoi_gian_va_tien", "Bài 8 — Thời gian và tiền: java.time, BigDecimal, làm tròn, vùng ngôn ngữ",
                  "curriculum/jv2.yaml L08; audit/jv2/verify_jv2.py L08 (javac/java chạy thật, JDK 21; dữ liệu múi giờ của JDK); "
                  "java.time (Java SE 21 API: Instant, ZonedDateTime, Duration, Period, ChronoUnit.DAYS.between); "
                  "java.math.BigDecimal và RoundingMode (Java SE 21 API: HALF_UP, HALF_EVEN; BigDecimal(double) lấy nguyên giá trị nhị phân); "
                  "java.util.Locale và String.format (dữ liệu vùng CLDR); IEEE 754-2019 mục làm tròn về số chẵn gần nhất; "
                  "IANA Time Zone Database (America/New_York: giờ mùa hè bắt đầu 2026-03-08, kết thúc 2026-11-01); dev.java/learn",
                  ["Phân biệt ngày lịch, điểm thời gian và ngày giờ theo múi giờ, và nhớ rằng một ngày có thể dài 23 hay 25 giờ",
                   "Tính lãi theo ngày bằng số thập phân chính xác và kiểm lại bằng số nguyên",
                   "Nêu sai lệch cộng dồn của các kiểu làm tròn khi số giao dịch tăng một nghìn lần",
                   "Nhận ra bẫy cộng ngày với cộng tháng, tạo số chính xác từ số thực, và vùng ngôn ngữ",
                   "Viết chương trình lãi theo ngày cho khoản gửi 120 triệu và chạy thử"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "intuition"), (2, "example"), (3, "scale"), (4, "pitfalls"), (5, "practice")])
