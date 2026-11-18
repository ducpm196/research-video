from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    giu_ref = prog("GiuThamChieu", """
import java.lang.ref.WeakReference;
public class GiuThamChieu {
    public static void main(String[] args) {
        Object tk = new byte[1_000_000];   // gần 1 MB trên heap
        WeakReference<Object> yeu = new WeakReference<>(tk);   // tham chiếu yếu: chỉ để hỏi
        System.out.println("con tham chieu: " + (yeu.get() != null));
        tk = null;   // bỏ tham chiếu mạnh cuối cùng
        System.gc();   // xin máy dọn rác
        System.out.println("sau khi bo: " + (yeu.get() != null));
    }
}""", out="""con tham chieu: true
sau khi bo: false""")
    ro_ri = prog("RoRi", """
import java.util.*;
public class RoRi {
    static final Map<Integer, byte[]> BO_DEM = new HashMap<>();   // biến static: một gốc
    static long dungMB() {
        System.gc();
        Runtime rt = Runtime.getRuntime();
        return (rt.totalMemory() - rt.freeMemory()) / 1_048_576;   // số MB đang dùng
    }
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) BO_DEM.put(i, new byte[1_048_576]);
        System.out.println("giu 5 doi tuong, heap >= 5 MB? " + (dungMB() >= 5));
        BO_DEM.clear();
        System.out.println("sau khi xoa, heap >= 5 MB? " + (dungMB() >= 5));
    }
}""", out="""giu 5 doi tuong, heap >= 5 MB? true
sau khi xoa, heap >= 5 MB? false""")
    cong_tien = prog("CongTien", """
import java.math.BigDecimal;
public class CongTien {
    public static void main(String[] args) {
        double a = 0;
        BigDecimal b = BigDecimal.ZERO;
        long c = 0;
        for (int i = 0; i < 10; i++) {
            a += 0.1;                           // số thực nhị phân
            b = b.add(new BigDecimal("0.1"));   // số thập phân, tạo từ chuỗi
            c += 1;                             // số nguyên: đơn vị một phần mười
        }
        System.out.println(a + " | " + b + " | " + c + " phan muoi");
    }
}""", out="0.9999999999999999 | 1.0 | 10 phan muoi")
    so_sanh = prog("SoSanh", """
public class SoSanh {
    public static void main(String[] args) {
        String s = new String("abc");
        String t = new String("abc");
        System.out.println(s == t);        // cùng một đối tượng?
        System.out.println(s.equals(t));   // cùng nội dung?
    }
}""", out="""false
true""")
    phi_lech = prog("PhiLech", """
public class PhiLech {
    public static void main(String[] args) {
        double tong = 0;
        long phanMuoi = 0;
        for (int i = 0; i < 20; i++) {
            tong += 0.3;
            phanMuoi += 3;
        }
        System.out.println("double: " + tong);
        System.out.println("so nguyen: " + phanMuoi + " phan muoi");
        System.out.println("bang 6? " + (tong == 6.0));
    }
}""", out="""double: 5.999999999999998
so nguyen: 60 phan muoi
bang 6? false""")
    sc_hook = sc("hook", "hook", "Vì sao một con số tiền lại lệch, và vì sao dịch vụ sập sau vài ngày?", [
        st("""<p>Cộng mười lần số $0{,}1$ bằng kiểu số thực của Java, máy in ra <b>0.9999999999999999</b>, không phải $1$.</p>
<div class="box key">Hôm nay ta trả lời ba câu: <b>đối tượng nằm ở đâu</b> trong bộ nhớ, <b>ai dọn rác</b>, và <b>tiền nên lưu bằng kiểu gì</b>.</div>""",
           """Chào bạn, cộng mười lần số không phẩy một bằng kiểu số thực của Java, máy không cho ra đúng một.
           """),
        st("""<p>Một chương trình khác, chạy liên tục để phục vụ khách, chạy tốt vài ngày rồi báo hết bộ nhớ và sập. Mã không viết sai chữ nào.</p>
<div class="box key">Cả hai lỗi đều có gốc ở một chỗ: <b>hiểu sai cách Java giữ dữ liệu</b>.</div>""",
           """Một chương trình khác, chạy liên tục phục vụ khách, chạy tốt vài ngày rồi báo hết bộ nhớ và sập, dù mã không viết sai chữ nào.
           """),
    ])
    sc_pre = sc("prereq", "prereq", "Trước hết: sáu khái niệm cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Biến", "cái tên gắn với một giá trị", "<code>int a = 5</code>: tên a giữ số năm"],
                  ["② Lớp", "bản thiết kế: nói một loại đồ vật có những dữ liệu gì, làm được việc gì", "lớp <code>TaiKhoan</code>"],
                  ["③ Đối tượng", "một đồ vật cụ thể làm theo bản thiết kế lớp", "tài khoản có số dư 100"]]),
           """Trước hết ta cần hiểu ba điều. Điều thứ nhất, biến là một cái tên gắn với một giá trị, ví dụ tên a giữ số năm.
           Điều thứ hai, lớp là một bản thiết kế, nói một loại đồ vật có những dữ liệu gì và làm được việc gì, ví dụ lớp tài khoản.
           Điều thứ ba, đối tượng là một đồ vật cụ thể làm theo bản thiết kế đó."""),
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["④ Trường", "một ô dữ liệu bên trong đối tượng", "trường <code>soDu</code> giữ 100"],
                  ["⑤ Phương thức", "một việc đối tượng làm được, gọi bằng dấu chấm", "<code>s.equals(t)</code>: hỏi dãy chữ s có cùng nội dung với dãy chữ t không"],
                  ["⑥ Tham chiếu", "giá trị chỉ đường tới một đối tượng; biến giữ tham chiếu chứ không giữ cả đối tượng", "tờ giấy ghi địa chỉ nhà, không phải ngôi nhà"]]),
           """Thêm ba điều nữa. Trường là một ô dữ liệu bên trong đối tượng, ví dụ trường số dư giữ một trăm.
           Phương thức là một việc đối tượng làm được, gọi bằng dấu chấm.
           Còn tham chiếu là giá trị chỉ đường tới một đối tượng, giống tờ giấy ghi địa chỉ nhà, chứ không phải chính ngôi nhà.""", clear=True),
        st("""<p>Một đơn vị đo bộ nhớ (cách tính quen dùng cho bộ nhớ): $1\\,\\text{KB} = 1024$ byte, và $1\\,\\text{MB} = 1024 \\cdot 1024 = 1\\,048\\,576$ byte. Một gi ga byte (GB) bằng 1024 MB.</p>""",
           """Thêm một đơn vị đo, theo cách tính quen dùng cho bộ nhớ: một ki lô byte bằng một nghìn không trăm hai mươi bốn byte, và một mê ga byte là số đó nhân với chính nó. """,
           introduces=["cdot"]),
    ], checks=["1024 * 1024 == 1048576"])
    sc_sym = sc("sym", "symbol", "Giải mã vài chữ trong mã Java", [
        st("""<table class='t'><tr><th>viết</th><th>nghĩa</th></tr>
<tr><td><code>new TaiKhoan()</code></td><td>tạo một đối tượng mới của lớp <code>TaiKhoan</code> trên heap (vùng nhớ dùng chung cho mọi đối tượng)</td></tr>
<tr><td><code>tk</code></td><td>tên biến giữ tham chiếu tới đối tượng</td></tr>
<tr><td><code>tk.soDu</code></td><td>dấu chấm: đi theo tham chiếu tới trường <code>soDu</code> của đối tượng</td></tr>
<tr><td><code>a == b</code></td><td>với hai biến đối tượng: so hai tham chiếu có trỏ cùng một đối tượng không (với số như <code>int</code> thì so giá trị)</td></tr></table>""",
           """Bảng này giải mã bốn mẫu chữ hay gặp. Từ khoá tạo đối tượng sinh một đối tượng mới của lớp tài khoản trên heap, vùng nhớ dùng chung cho mọi đối tượng.
           Biến tài khoản giữ tham chiếu tới đối tượng đó. Dấu chấm đi theo tham chiếu để tới một trường bên trong.
           Với hai biến đối tượng, hai dấu bằng so hai tham chiếu có trỏ cùng một đối tượng không, còn với số thì so giá trị."""),
        st(table(["viết", "nghĩa"],
                 [["<code>int</code>, <code>long</code>, <code>double</code>", "ba kiểu số: số nguyên vừa, số nguyên dài, số thực nhị phân (máy ghi số bằng hệ hai: chỉ hai chữ số 0 và 1, nên 0,1 chỉ ghi gần đúng)"],
                  ["<code>final</code>", "gán giá trị một lần rồi không đổi nữa"],
                  ["<code>Map&lt;Integer, byte[]&gt;</code>", "bản đồ có khoá là số nguyên, giá trị là mảng byte"],
                  ["máy ảo Java", "chương trình đọc và chạy mã Java đã dịch, lo luôn bộ nhớ và dọn rác"],
                  ["<code>javac</code>, <code>java</code>", "lệnh dịch tệp mã ra dạng máy ảo hiểu, rồi lệnh chạy nó"]]),
           """Thêm vài chữ nữa, ba kiểu số là số nguyên vừa, số nguyên dài, và số thực nhị phân. Số thực nhị phân là số máy ghi bằng hệ hai, chỉ hai chữ số không và một, nên không phẩy một chỉ ghi gần đúng.
           Từ khoá cuối nghĩa là gán một lần rồi không đổi. Cặp ngoặc nhọn ghi kiểu của bản đồ, khoá là số nguyên, giá trị là mảng byte. Máy ảo Java là chương trình chạy mã đã dịch: một lệnh để dịch, một lệnh để chạy.""", clear=True),
        st(table(["viết", "nghĩa"],
                 [["<code>public class PhiLech { … }</code>", "khung tệp: mọi mã nằm trong một lớp, tên lớp trùng tên tệp <code>PhiLech.java</code>"],
                  ["<code>import java.util.*;</code>", "nhập các lớp có sẵn trong thư viện của Java để dùng"],
                  ["<code>public static void main(String[] args) { … }</code>", "hàm chính: chương trình bắt đầu chạy từ đây; hàm là một nhóm lệnh có tên; <code>args</code> là mảng chuỗi gõ thêm sau lệnh chạy, bài này không dùng"],
                  ["<code>for (int i = 0; i &lt; 5; i++) { … }</code>", "vòng lặp: làm phần trong ngoặc nhọn với i = 0, 1, 2, 3, 4, tức năm lần"],
                  ["<code>System.out.println(x)</code>", "in giá trị x ra màn hình rồi xuống dòng"],
                  ["<code>\"abc\"</code>", "chuỗi: một dãy chữ nằm trong ngoặc kép"]]),
           """Bây giờ là khung của một tệp Java. Mã nằm trong một lớp, tên lớp trùng tên tệp, và dòng nhập cho dùng các lớp có sẵn.
           Chương trình chạy từ hàm chính; hàm là nhóm lệnh có tên, và tham số mảng chuỗi chứa các chữ gõ thêm sau lệnh chạy, bài này không dùng. Vòng lặp làm phần trong ngoặc nhọn nhiều lần.
           Lệnh in đưa một giá trị ra màn hình, và chuỗi là dãy chữ nằm giữa hai dấu ngoặc kép.""", clear=True),
        st(table(["từ", "nghĩa"],
                 [["dịch vụ", "chương trình chạy liên tục, chờ người khác gọi tới"],
                  ["yêu cầu", "một lần được gọi tới, ví dụ một lần chuyển tiền"],
                  ["bộ xử lý", "con chip chạy lệnh; có nhiều bộ thì làm được nhiều việc cùng lúc"],
                  ["JDK 21", "bộ công cụ của Java: mở cửa sổ gõ lệnh (như Git Bash), gõ <code>java -version</code> phải thấy số 21"]]),
           """Vài từ đời thường nữa. Dịch vụ là chương trình chạy liên tục chờ người khác gọi tới, mỗi lần gọi là một yêu cầu. 
           Để chạy mã trong bài, cài bộ công cụ Java bản hai mươi mốt, rồi gõ lệnh hỏi phiên bản, phải thấy số hai mươi mốt.""", clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: ngăn xếp, heap và các mũi tên", [
        st(svg(1500, 400,
               panel(40, 40, 380, 320, "Stack (ngăn xếp)", C_BLUE),
               box(70, 120, 320, 70, "a = 5", C_GRAY), box(70, 220, 320, 70, "tk = ●", C_GRAY),
               panel(620, 40, 840, 320, "Heap (vùng nhớ chung)", C_AMBER),
               box(840, 170, 340, 120, ["TaiKhoan", "soDu = 100"], C_GREEN, bold=True),
               arrow(390, 255, 835, 235, "#2a78d6", "tham chiếu")),
           """Hình bên trái là ngăn xếp, mỗi lần gọi hàm có một khung riêng giữ biến cục bộ. Đối tượng tài khoản nằm bên phải, trong heap. Biến tài khoản chỉ giữ một mũi tên trỏ sang đó."""),
        st(svg(1500, 400,
               panel(40, 40, 380, 320, "Stack", C_BLUE),
               box(70, 120, 320, 70, "tk = ●", C_GRAY), box(70, 220, 320, 70, "tk2 = ●", C_GRAY),
               panel(620, 40, 840, 320, "Heap", C_AMBER),
               box(840, 170, 340, 120, ["TaiKhoan", "soDu = 100"], C_GREEN, bold=True),
               arrow(390, 155, 835, 215, "#2a78d6"), arrow(390, 255, 835, 250, "#2a78d6")),
           """Hai biến tài khoản có thể cùng trỏ tới một đối tượng. Khi đó sửa số dư qua tên này, tên kia cũng thấy ngay,
           vì chỉ có một tài khoản duy nhất trên heap."""),
        st(svg(1500, 420,
               box(40, 150, 200, 90, "gốc", C_BLUE, bold=True),
               box(340, 150, 180, 90, "A", C_GREEN, bold=True), box(620, 150, 180, 90, "B", C_GREEN, bold=True),
               box(900, 150, 180, 90, "C", C_GREEN, bold=True),
               box(340, 300, 180, 90, "D", C_GRAY, dash=True), box(620, 300, 180, 90, "E", C_GRAY, dash=True),
               box(1180, 150, 180, 90, "F", C_GRAY, dash=True),
               arrow(240, 195, 335, 195), arrow(520, 195, 615, 195), arrow(800, 195, 895, 195), arrow(520, 345, 615, 345),
               txt(1100, 60, "xanh: còn tới được từ gốc, xám: không có đường từ gốc → rác", 26, "middle", "#1f2937", True)),
           """Nó xuất phát từ các gốc, đi theo mọi mũi tên, và đánh dấu mọi đối tượng chạm tới.
           A, B và C tới được từ gốc nên được giữ. D, E và F không có đường tới, nên là rác."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: đánh dấu rồi quét", [
        st("""<p><b>Bước 1. Chọn các gốc.</b> Gốc là những chỗ chắc chắn còn dùng: biến cục bộ của các hàm đang chạy, biến <code>static</code> (biến gắn với cả lớp, sống suốt chương trình), và các luồng đang chạy (luồng: một dòng việc chạy riêng).</p>
<span class='note'>Làm thử: ở hình trước, gốc chỉ trỏ tới A, nên tập đánh dấu ban đầu là {A}.</span>""",
           """Bước một, chọn các gốc. Gốc là những chỗ chắc chắn còn được dùng, như biến cục bộ của các hàm đang chạy, biến tĩnh, và các luồng đang chạy.
           Biến tĩnh là biến gắn với cả lớp, sống suốt chương trình. Làm thử với hình trước, gốc chỉ trỏ tới A, nên tập đánh dấu chỉ có A."""),
        st("""<p><b>Bước 2. Đi theo mũi tên.</b> Mỗi đối tượng được đánh dấu thì đánh dấu luôn mọi đối tượng nó trỏ tới, lặp đến khi hết.</p>
<span class='note'>Làm thử: A trỏ B, B trỏ C, C không trỏ gì, nên tập là {A, B, C}.</span>""",
           """Bước hai, đi theo mũi tên. Đối tượng nào được đánh dấu thì mọi đối tượng nó trỏ tới cũng được đánh dấu, lặp cho tới khi hết.
           Làm thử, A trỏ tới B, B trỏ tới C, C không trỏ đi đâu, nên tập đánh dấu là A, B, C."""),
        st("""<p><b>Bước 3. Quét.</b> Mọi đối tượng chưa được đánh dấu là rác, bộ nhớ của chúng được giải phóng.</p>
<span class='note'>Làm thử: sáu đối tượng trừ ba đã đánh dấu còn ba đối tượng rác: D, E, F.</span>""",
           """Bước ba, quét. Mọi đối tượng chưa được đánh dấu là rác, và bộ nhớ của chúng được giải phóng.
           Làm thử, nên sáu trừ ba còn ba đối tượng rác, là D, E và F.
           
          """),
    ], checks=["alg.bnk_reachable({'A': ['B'], 'B': ['C'], 'C': [], 'D': ['E'], 'E': [], 'F': []}, ['A']) == ['A', 'B', 'C']",
               "6 - 3 == 3"])
    sc_ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Giả sử mỗi đối tượng chiếm $100$ byte <i>(số minh hoạ)</i>, và heap đang có sáu đối tượng A đến F.</p>
$$① \\; 6 \\cdot 100 = \\hl{600}\\ \\text{byte}$$""",
           """Giả sử mỗi đối tượng chiếm một trăm byte, đây là số minh hoạ, và heap đang có sáu đối tượng từ A đến F.
           Phép tính thứ nhất, tổng bộ nhớ là sáu nhân một trăm, bằng sáu trăm byte."""),
        st("""<p>Đối tượng còn sống: A, B, C.</p>
$$② \\; \\text{sống} = 3$$""",
           """Phép tính thứ hai, đối tượng còn sống là A, B và C, tức ba đối tượng."""),
        st("""<p>Dùng lại $3$ đối tượng sống ở phép ②.</p>
$$③ \\; 3 \\cdot 100 = \\hlg{300}\\ \\text{byte}$$""",
           """Phép tính thứ ba, bộ nhớ đang sống là ba nhân một trăm, bằng ba trăm byte."""),
        st("""<p>Dùng lại $600$ ở ① và $300$ ở ③.</p>
$$④ \\; 600 - 300 = \\hl{300}\\ \\text{byte} = 3 \\cdot 100$$""",
           """Phép tính thứ tư, bộ nhớ dọn được là sáu trăm trừ ba trăm, bằng ba trăm byte."""),
        st("""<p>Bây giờ xoá mũi tên A→B. Gốc chỉ còn tới A, nên tập sống là {A}: sống $1$, rác $5$.</p>
$$⑤ \\; 5 \\cdot 100 = \\hl{500}\\ \\text{byte}$$""",
           """Bây giờ xoá mũi tên từ A sang B. Gốc chỉ còn tới được A, nên tập sống chỉ còn một đối tượng, và rác là năm đối tượng.
           Phép tính thứ năm, dọn được năm nhân một trăm, bằng năm trăm byte."""),
    ], checks=["6 * 100 == 600", "len(alg.bnk_reachable({'A': ['B'], 'B': ['C'], 'C': [], 'D': ['E'], 'E': [], 'F': []}, ['A'])) * 100 == 300",
               "600 - 300 == 300 == 3 * 100",
               "len(alg.bnk_reachable({'A': [], 'B': ['C'], 'C': [], 'D': ['E'], 'E': [], 'F': []}, ['A'])) == 1 and (6 - 1) * 100 == 500"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: tiền không được lưu bằng số thực", [
        st("""<p>Đường khác cho phần dọn rác: đếm thẳng từng đối tượng. A, B, C có đường từ gốc. D trỏ tới E nhưng không có đường từ gốc.
F không ai trỏ. Rác: $3$ ✓ — <b>bị trỏ tới chưa chắc còn sống</b>.</p>""",
           """Kiểm bằng đường khác, đếm thẳng từng đối tượng. A, B và C đều có đường từ gốc. D trỏ tới E, nhưng cả hai không có đường từ gốc, còn F không ai trỏ tới.
           Bị trỏ tới chưa chắc còn sống, phải tới được từ gốc."""),
        st(table(["cách lưu tiền", "cộng 10 lần 0,1", "đúng 1?"],
                 [["kiểu double (số thực nhị phân)", "0.9999999999999999", "không"],
                  ["BigDecimal tạo từ chuỗi <code>\"0.1\"</code> (số thập phân)", "1.0", "có"],
                  ["số nguyên theo đơn vị nhỏ nhất: lưu 0,1 thành 1 phần mười", "1 + 1 + … = 10 phần mười = 1", "có"]]),
           """Bảng này so ba cách lưu tiền. Số không phẩy một viết ở hệ hai là dãy lặp vô hạn, như một phần ba ở hệ mười, nên máy phải cắt bớt và cộng mười lần bị lệch.
           BigDecimal giữ số thập phân nên đúng, với điều kiện tạo từ chuỗi. Số nguyên theo đơn vị nhỏ nhất thì mười phần mười đúng bằng một."""),
    ], checks=["alg.bnk_float_vs_decimal()[0] != 1.0", "str(alg.bnk_float_vs_decimal()[1]) == '1.0'", "alg.bnk_float_vs_decimal()[2] == 10",
               "__import__('decimal').Decimal(0.1) != __import__('decimal').Decimal('0.1')", "sum([1] * 10) == 10",
               "len([o for o in 'ABCDEF' if o not in alg.bnk_reachable({'A': ['B'], 'B': ['C'], 'D': ['E']}, ['A'])]) == 3"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Dùng <code>==</code> để so hai chuỗi hay hai đối tượng. <code>==</code> chỉ hỏi
“cùng một đối tượng không”, nên hai chuỗi giống chữ nhưng tạo riêng vẫn cho <code>false</code>. Muốn so nội dung dùng <code>equals</code>.</div>""",
           """Lỗi thứ nhất, của người mới. Dùng hai dấu bằng để so hai chuỗi, vì nó chỉ hỏi hai tham chiếu có cùng một đối tượng không.
           Hai chuỗi giống chữ nhưng tạo riêng vẫn không bằng nhau. Muốn so nội dung thì gọi phương thức so nội dung."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Rò rỉ bộ nhớ</b>: bỏ dữ liệu vào một <code>static Map</code> làm bộ đệm (nơi giữ sẵn dữ liệu hay dùng để lấy lại cho nhanh)
mà không bao giờ xoá. Gốc <code>static</code> vẫn trỏ tới chúng, nên chúng vẫn “tới được” và bộ thu gom rác không dọn.
<br><span class="note">Phép thử: theo dõi kích thước heap sau mỗi lần dọn; nếu cứ tăng thì có thứ đang bị giữ.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là rò rỉ bộ nhớ. Họ bỏ dữ liệu vào một bản đồ tĩnh làm bộ đệm, tức nơi giữ sẵn dữ liệu hay dùng, mà không bao giờ xoá.
           Gốc tĩnh vẫn trỏ tới chúng nên chúng không bị dọn. """, clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Dùng <code>double</code> cho số tiền rồi so sánh <code>==</code>. Kết quả
lệch ở chữ số thập phân thứ mười sáu, đủ làm đối soát cuối ngày không khớp.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm. Dùng kiểu số thực nhị phân cho số tiền, rồi so sánh bằng nhau.
           Sai lệch nhỏ ở chữ số thập phân thứ mười sáu cũng đủ làm bước đối soát cuối ngày, tức so sổ của hai bên, không khớp."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Heap có 4 đối tượng, gốc chỉ trỏ tới X, X trỏ tới Y, Z trỏ tới W. Mấy đối tượng là rác?"],
                  ["2", "Cùng heap ở câu 1, mỗi đối tượng 50 byte. Dọn được bao nhiêu byte?"],
                  ["3", "Quyết định: lưu số dư bằng double hay số nguyên?"]]),
           """Bây giờ đến lượt bạn. Câu một, heap có bốn đối tượng, gốc chỉ trỏ tới X, X trỏ tới Y, còn Z trỏ tới W. Có mấy đối tượng là rác?
           Câu hai, cùng heap đó, mỗi đối tượng năm mươi byte, dọn được bao nhiêu byte? Câu ba, lưu số dư bằng số thực nhị phân hay số nguyên? Hãy dừng video và làm ra giấy.""",
           pause=20),
        st("""<p>Câu 1. Gốc → X → Y nên sống là X và Y. Z và W không có đường từ gốc.</p>
$$4 - 2 = \\hl{2}$$""",
           """Đáp án câu một. Từ gốc đi tới X rồi Y, nên sống là hai đối tượng X và Y. Z và W không có đường từ gốc, nên rác là bốn trừ hai bằng hai.""",
           introduces=None),
        st("""$$2 \\cdot 50 = \\hlg{100}\\ \\text{byte}$$""",
           """Đáp án câu hai. Hai đối tượng rác nhân năm mươi byte, bằng một trăm byte."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["double", "tính nhanh, dễ viết", "lệch ở chữ số cuối, không an toàn cho tiền"],
                  ["số nguyên đơn vị nhỏ nhất", "chính xác, nhanh", "phải nhớ đơn vị khi hiển thị"]]),
           """Đáp án câu ba. Số thực nhị phân dễ viết nhưng lệch. Số nguyên đơn vị nhỏ nhất, hoặc BigDecimal, chính xác."""),
    ], checks=["4 - len(alg.bnk_reachable({'X': ['Y'], 'Z': ['W']}, ['X'])) == 2", "2 * 50 == 100"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("tên biến", "tham chiếu", "đối tượng trên heap", "còn tới được từ gốc?", "sống / rác"),
           """Tên biến giữ tham chiếu, tham chiếu trỏ tới đối tượng trên heap. Đối tượng còn tới được từ gốc thì sống, không thì là rác."""),
        st("""<div class='box key'><b>Tư duy:</b> rò rỉ bộ nhớ không phải “quên dọn” mà là “vẫn còn người trỏ tới”.
Với tiền: <b>không dùng double</b>; dùng số nguyên đơn vị nhỏ nhất hoặc BigDecimal.</div>""",
           """Rò rỉ bộ nhớ là vẫn còn người trỏ tới, không phải quên dọn. Với tiền, hãy dùng số nguyên đơn vị nhỏ nhất, hoặc BigDecimal."""),
    ])
    # ── AF2: mã chạy thật, quy mô, tự làm ──
    add_steps([sc_pre], "prereq", [
        st(table(["thêm ba thứ dùng trong mã", "nghĩa", "ví dụ"],
                 [["⑦ Mảng byte", "dãy ô nhớ liền nhau, mỗi ô một byte", "<code>new byte[1_000_000]</code>: một triệu ô, gần 1 MB"],
                  ["⑧ Bản đồ (Map)", "bảng tra: đưa khoá vào thì lấy ra giá trị", "<code>map.put(1, x)</code>: cất x dưới khoá 1"],
                  ["⑨ Tham chiếu yếu", "dây buộc lỏng: trỏ tới đối tượng nhưng <b>không giữ nó sống</b>", "<code>WeakReference</code>: hỏi <code>get()</code> còn đối tượng hay đã bị dọn"]]),
           """Thêm ba thứ sẽ xuất hiện trong mã. Mảng byte là dãy ô nhớ liền nhau, mỗi ô một byte.
           Bản đồ là bảng tra, đưa khoá vào thì lấy ra giá trị. Tham chiếu yếu là dây buộc lỏng, nó trỏ tới đối tượng nhưng không giữ nó sống, chỉ để hỏi xem nó còn không.""",
           clear=True),
    ], at=2)
    sc_pre["title"] = "Trước hết: chín khái niệm cần hiểu"
    sc_run = sc("chay_that", "example", "Chạy thật: tham chiếu mạnh, tham chiếu yếu và gốc static", [
        *jsteps([("cmt", "<code>// gần 1 MB trên heap</code>", None),
               ("concat", "<code>\"con tham chieu: \" + (yeu.get() != null)</code>", None),
               ("cmp", "<code>i &lt;= 5</code>; <code>dungMB() &gt;= 5</code>; <code>yeu.get() != null</code>", None),
               ("null", "<code>tk = null;</code>; <code>new WeakReference&lt;&gt;(tk)</code>; <code>yeu.get() != null</code>: <code>!=</code> là “khác”", None),
               ("incr", "<code>a += 0.1</code>; <code>c += 1</code>; <code>i++</code>", None)]),
        st(code_block(giu_ref, title="Tệp GiuThamChieu.java"),
           """Dòng đầu tạo một mảng gần một mê ga byte, và biến thứ nhất giữ tham chiếu tới nó.
           Dòng thứ hai buộc thêm một tham chiếu yếu, chỉ để hỏi mảng còn hay không. Rồi ta gán rỗng cho biến thứ nhất và xin dọn rác."""),
        st(out_block(giu_ref),
           """Kết quả in thật có hai dòng. Dòng đầu là còn, vì biến vẫn trỏ tới đối tượng. Dòng sau là không còn, vì hết tham chiếu mạnh thì đối tượng thành rác và máy đã dọn nó.
           Lệnh xin dọn chỉ là gợi ý, nhưng ở cách chạy mặc định trên máy này nó được thực hiện.""", clear=True),
        *jsteps([("sig", "<code>static long dungMB()</code>: hàm <code>dungMB</code>, trả về số nguyên dài, không có tham số",
                "hàm đo bộ nhớ, trả về một số nguyên dài, và trong ngoặc tròn không có tham số nào."),
               ("runtime", "<code>rt.totalMemory() - rt.freeMemory()</code>", None),
               ("ret", "<code>return … / 1_048_576;</code>", None)]),
        st(code_block(ro_ri, lines=(1, 8), title="Tệp RoRi.java (phần đầu)"),
           """Bây giờ tới gốc tĩnh. Biến tĩnh bản đồ là một gốc, nên mọi mảng nó giữ đều còn tới được.
           Hàm đo gọi dọn rác, rồi lấy tổng bộ nhớ đã xin trừ phần còn trống, chia cho một mê ga byte, ra số mê ga byte heap đang dùng.""", clear=True),
        st(code_block(ro_ri, lines=(9, 15), title="Tệp RoRi.java (phần hàm chính)"),
           """Trong hàm chính, vòng lặp bỏ năm mảng, mỗi mảng đúng một mê ga byte, vào bản đồ rồi đo. """, clear=True),
        st(out_block(ro_ri) + '<p class="note">Đúng với bộ dọn mặc định (G1), chọn khi máy có từ 2 bộ xử lý và từ 2 GB bộ nhớ; máy yếu hơn có thể ra khác.</p>',
           """Khi bản đồ còn giữ năm mảng, heap đang dùng từ năm mê ga byte trở lên. Xoá bản đồ, năm mảng thành rác bị dọn, nên heap không còn tới năm mê ga byte.
           Kết quả này đúng với bộ dọn mặc định; máy yếu hơn có thể ra khác. Rác còn nằm trong bản đồ tĩnh thì không bị dọn: đó là rò rỉ bộ nhớ.""", clear=True),
    ])
    add_steps([sc_chk], "check", [
        st(code_block(cong_tien, title="Tệp CongTien.java"),
           """Đây là chương trình cộng bằng ba cách. Biến thứ nhất là số thực nhị phân, biến thứ hai là số thập phân tạo từ chuỗi, biến thứ ba là số nguyên đếm theo phần mười.
           """, clear=True),
        st(out_block(cong_tien),
           """Chạy thật, số thực nhị phân cho không phẩy chín chín chín vì không lưu đúng không phẩy một, còn hai cách kia cho đúng một.""", clear=True),
    ])
    add_steps([sc_pit], "pitfalls", [
        st(code_block(so_sanh, title="Chạy thật: hai chuỗi cùng chữ") + out_block(so_sanh),
           """Chạy thật hai chuỗi cùng chữ a b c, nhưng được tạo riêng bằng từ khoá tạo mới. Phép so hai dấu bằng cho kết quả sai, vì đó là hai đối tượng khác nhau.
           """, clear=True),
    ], at=1)
    sc_scale = sc("quy_mo", "example", "Quy mô: rò rỉ nhỏ, tải lớn", [
        st("""<p>Giả sử mỗi yêu cầu bỏ lại $1$ KB (1024 byte) trong bản đồ tĩnh, và heap của dịch vụ là $4$ GB $= 4 \\cdot 1024^3$ byte <i>(số minh hoạ)</i>.</p>
$$\\text{thời gian đầy} = \\frac{4 \\cdot 1024^3}{\\text{yêu cầu mỗi giây} \\cdot 1024}\\ \\text{giây}$$
""" + table(["tải", "yêu cầu mỗi giây", "rò rỉ mỗi giây", "đầy heap sau"],
            [["×1", "10", "10 240 byte", "≈ 419 430 giây ≈ <b>4,9 ngày</b>"],
             ["×100", "1 000", "1 024 000 byte", "≈ 4 194 giây ≈ <b>70 phút</b>"],
             ["×10 000", "100 000", "102 400 000 byte", "≈ <b>42 giây</b>"]]),
           """Giả sử mỗi yêu cầu bỏ lại một ki lô byte trong bản đồ tĩnh, và heap của dịch vụ là bốn gi ga byte. Đây là số minh hoạ.
            Với mười yêu cầu mỗi giây, heap đầy sau khoảng bốn phẩy chín ngày.
           Tải tăng một trăm lần, còn khoảng bảy mươi phút. Tải tăng mười nghìn lần, chỉ còn khoảng bốn mươi hai giây.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Khởi động lại dịch vụ mỗi đêm đủ ở tải ×1 vì 4,9 ngày dài hơn một ngày. Ở ×100 phải khởi động lại mỗi giờ, ở ×10 000 thì sập
trước khi kịp khởi động lại. <b>Tăng heap gấp đôi</b> chỉ kéo dài gấp đôi thời gian, không đổi bản chất.</div>
<div class="box key"><b>Sửa gốc:</b> giới hạn bộ đệm, ví dụ tối đa $10\\,000$ mục, tức tối đa $10\\,240\\,000$ byte (khoảng 10 MB) dù tải bao nhiêu.
<b>Đánh đổi:</b> mục bị đuổi đi thì lần sau phải tra lại từ nguồn gốc, chậm hơn.</div>""",
           """Giải pháp cũ là khởi động lại dịch vụ mỗi đêm. Ở tải gốc nó đủ vì bốn phẩy chín ngày dài hơn một ngày. Gấp trăm lần thì phải khởi động lại mỗi giờ, gấp mười nghìn lần thì sập trước khi kịp khởi động.
           Tăng heap gấp đôi chỉ kéo dài gấp đôi thời gian. Cách sửa gốc là giới hạn bộ đệm, ví dụ tối đa mười nghìn mục, khoảng mười mê ga byte dù tải bao nhiêu.
           Đánh đổi là mục bị đuổi thì lần sau phải tra lại từ nguồn, chậm hơn.""", clear=True),
    ], checks=["round(4 * 1024**3 / 10240) == 419430", "round(419430 / 86400, 1) == 4.9", "10 * 1024 == 10240",
               "1000 * 1024 == 1024000", "round(4 * 1024**3 / 1024000) == 4194", "round(4194 / 60) == 70",
               "100000 * 1024 == 102400000", "round(4 * 1024**3 / 102400000) == 42", "10000 * 1024 == 10240000"])
    write_lab("BNK", "L00", """# Lab BNK L00 — Phí 0,3 bị cộng hai mươi lần

Một khoản phí **0,3** (đơn vị bất kỳ, số minh hoạ) bị cộng **20 lần** vào một tổng.

Viết chương trình `PhiLech` (tệp `PhiLech.java`):
1. Một biến `double` cộng `0.3` hai mươi lần; một biến `long` cộng `3` (đơn vị: một phần mười) hai mươi lần.
2. In đúng ba dòng:
   - `double: <tổng double>`
   - `so nguyen: <tổng long> phan muoi`
   - `bang 6? <kết quả so sánh tổng double == 6.0>`

Cần JDK 21: mở cửa sổ gõ lệnh (Git Bash), gõ `java -version` phải thấy số 21. Khung tệp `PhiLech.java` (viết bài vào chỗ `...`):

```java
public class PhiLech {
    public static void main(String[] args) {
        // ... khai hai biến, vòng lặp for (int i = 0; i < 20; i++), in ba dòng bằng System.out.println
    }
}
```

Chạy: `javac PhiLech.java && java PhiLech`. Chấm: `bash labs/cham.sh BNK L00 PhiLech.java`.
""", "java", phi_lech["code"], phi_lech["out"])
    sc_lab = practice_scene(sc, "Tự làm: phí 0,3 cộng hai mươi lần", practice_steps(
        st, "BNK", "L00",
        """<p><b>Đề</b>: một khoản phí 0,3 bị cộng 20 lần. Viết <code>PhiLech.java</code>:</p>
<ol><li>biến <code>double</code> cộng <code>0.3</code> hai mươi lần; biến <code>long</code> cộng <code>3</code> (một phần mười) hai mươi lần</li>
<li>in ba dòng: <code>double: …</code>, <code>so nguyen: … phan muoi</code>, <code>bang 6? …</code> (so <code>tong == 6.0</code>)</li></ol>
<p class="note">Chạy: <code>javac PhiLech.java &amp;&amp; java PhiLech</code>. Hai dấu <code>&amp;&amp;</code> nối hai lệnh: lệnh sau chỉ chạy nếu lệnh trước thành công.</p>""",
        """Bây giờ tới phần bạn tự làm. Một khoản phí không phẩy ba bị cộng hai mươi lần. Hãy cộng nó hai mươi lần bằng số thực nhị phân, và cộng số ba, tức ba phần mười, hai mươi lần bằng số nguyên.
        Để chạy, gõ lệnh dịch rồi hai dấu và nối lệnh chạy, nghĩa là lệnh sau chỉ chạy nếu lệnh dịch thành công. Hãy dừng video, tự viết và chạy.""",
        phi_lech["out"], "PhiLech.java",
        """<div class="box key"><b>Nếu kẹt:</b> khai <code>double tong = 0;</code> và <code>long phanMuoi = 0;</code>, rồi vòng lặp 20 lần: <code>tong += 0.3;</code> và <code>phanMuoi += 3;</code>.
Lời giải ở <code>labs/BNK/L00/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, khai một biến số thực và một biến số nguyên dài, bắt đầu bằng không, rồi cộng không phẩy ba và ba trong vòng lặp hai mươi lần.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi tự thử.""", pause=90), "BNK", "L00")
    scenes = [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_run, sc_chk, sc_pit, sc_quiz, sc_scale, sc_lab, sc_rec]
    return lesson("L00", "java_bo_nho_gc", "Bài 0 — Java hiện đại: bộ nhớ, đối tượng và bộ thu gom rác",
                  "curriculum/bnk.yaml L00; audit/bnk/verify_bnk.py L00; audit/review/screen_code/BNK.yaml (mã chạy thật bằng JDK 21); The Java Virtual Machine Specification (Java SE 21); IEEE 754; JEP 248 (G1 mặc định từ JDK 9 trên máy server-class) và HotSpot GC Tuning Guide Java SE 21; Java SE 21 API: BigDecimal(String) và BigDecimal(double), java.lang.ref.WeakReference, Runtime.totalMemory/freeMemory, System.gc (chỉ là gợi ý); IEC 80000-13 (KiB = 1024 byte)",
                  ["Phân biệt dữ liệu nằm trên stack và trên heap", "Xác định đối tượng nào bị thu gom từ đồ thị tham chiếu",
                   "Nhận ra rò rỉ bộ nhớ do tham chiếu static và chạy thật để thấy nó", "Tính sau bao lâu rò rỉ làm đầy heap khi tải tăng ×100 và ×10 000",
                   "Chọn kiểu dữ liệu đúng cho số tiền"],
                  scenes, covers=[(1, "intuition"), (2, "example"), (3, "chay_that"), (4, "quy_mo"), (5, "practice")], intro={('sym', 0): ['bnk_heap'], ('sym', 1): ['bnk_may_ao'], ('pitfalls', 3): ['bnk_doi_soat']})
