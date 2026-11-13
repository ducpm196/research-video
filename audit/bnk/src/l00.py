from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    giu_ref = prog("GiuThamChieu", """
import java.lang.ref.WeakReference;
public class GiuThamChieu {
    public static void main(String[] args) {
        Object tk = new byte[1_000_000];                       // một đối tượng gần 1 MB trên heap
        WeakReference<Object> yeu = new WeakReference<>(tk);   // tham chiếu yếu: chỉ để hỏi, không giữ sống
        System.out.println("con tham chieu: " + (yeu.get() != null));
        tk = null;                                             // bỏ tham chiếu mạnh cuối cùng
        System.gc();                                           // xin máy dọn rác
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
        return (rt.totalMemory() - rt.freeMemory()) / 1_000_000;   // heap đang dùng, đơn vị MB
    }
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) BO_DEM.put(i, new byte[1_000_000]);
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
           Nó cho ra không phẩy chín chín chín, chín chín chín, và còn nhiều chữ chín nữa. Một ngân hàng không thể chấp nhận sai lệch như vậy."""),
        st("""<p>Một dịch vụ khác chạy tốt vài ngày rồi báo hết bộ nhớ và sập. Mã không có lỗi cú pháp nào.</p>
<div class="box key">Cả hai lỗi đều có gốc ở một chỗ: <b>hiểu sai cách Java giữ dữ liệu</b>.</div>""",
           """Một dịch vụ khác chạy tốt vài ngày, rồi báo hết bộ nhớ và sập, dù mã không có lỗi cú pháp nào.
           Cả hai lỗi đều có gốc ở một chỗ, là hiểu sai cách Java giữ dữ liệu."""),
    ])
    sc_pre = sc("prereq", "prereq", "Trước hết: sáu khái niệm cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Biến", "cái tên gắn với một giá trị", "<code>int a = 5</code>: tên a giữ số năm"],
                  ["② Lớp", "bản thiết kế: nói một loại đồ vật có những dữ liệu gì, làm được việc gì", "lớp <code>TaiKhoan</code>"],
                  ["③ Đối tượng", "một đồ vật cụ thể làm theo bản thiết kế lớp", "tài khoản có số dư 100"]]),
           """Trước hết ta cần hiểu ba điều. Điều thứ nhất, biến là một cái tên gắn với một giá trị, ví dụ tên a giữ số năm.
           Điều thứ hai, lớp là một bản thiết kế, nói một loại đồ vật có những dữ liệu gì và làm được việc gì, ví dụ lớp tài khoản.
           Điều thứ ba, đối tượng là một đồ vật cụ thể làm theo bản thiết kế đó, ví dụ một tài khoản có số dư một trăm."""),
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["④ Trường", "một ô dữ liệu bên trong đối tượng", "trường <code>soDu</code> giữ 100"],
                  ["⑤ Phương thức", "một việc đối tượng làm được, gọi bằng dấu chấm", "<code>s.equals(t)</code>: hỏi s có cùng nội dung với t không"],
                  ["⑥ Tham chiếu", "giá trị chỉ đường tới một đối tượng; biến giữ tham chiếu chứ không giữ cả đối tượng", "tờ giấy ghi địa chỉ nhà, không phải ngôi nhà"]]),
           """Thêm ba điều nữa. Trường là một ô dữ liệu bên trong đối tượng, ví dụ trường số dư giữ một trăm.
           Phương thức là một việc đối tượng làm được, và ta gọi nó bằng dấu chấm, ví dụ hỏi chuỗi s có cùng nội dung với chuỗi t không.
           Còn tham chiếu là giá trị chỉ đường tới một đối tượng, giống tờ giấy ghi địa chỉ nhà, chứ không phải chính ngôi nhà.""", clear=True),
        st("""<p>Một đơn vị đo bộ nhớ (cách tính quen dùng cho bộ nhớ): $1\\,\\text{KB} = 1024$ byte, và $1\\,\\text{MB} = 1024 \\cdot 1024 = 1\\,048\\,576$ byte.</p>""",
           """Thêm một đơn vị đo, theo cách tính quen dùng cho bộ nhớ: một ki lô byte bằng một nghìn không trăm hai mươi bốn byte, và một mê ga byte là số đó nhân với chính nó.""",
           introduces=["cdot"]),
    ], checks=["1024 * 1024 == 1048576"])
    sc_sym = sc("sym", "symbol", "Giải mã vài chữ trong mã Java", [
        st("""<table class='t'><tr><th>viết</th><th>nghĩa</th></tr>
<tr><td><code>new TaiKhoan()</code></td><td>tạo một đối tượng mới của lớp <code>TaiKhoan</code> trên heap</td></tr>
<tr><td><code>tk</code></td><td>tên biến giữ tham chiếu tới đối tượng</td></tr>
<tr><td><code>tk.soDu</code></td><td>dấu chấm: đi theo tham chiếu tới trường <code>soDu</code> của đối tượng</td></tr>
<tr><td><code>a == b</code></td><td>với hai biến đối tượng: so hai tham chiếu có trỏ cùng một đối tượng không (với số như <code>int</code> thì so giá trị)</td></tr></table>""",
           """Bảng này giải mã bốn mẫu chữ hay gặp. Từ khoá tạo đối tượng sinh ra một đối tượng mới của lớp tài khoản trên vùng nhớ heap.
           Biến tài khoản giữ tham chiếu tới đối tượng đó. Dấu chấm nghĩa là đi theo tham chiếu để tới một trường bên trong.
           Còn với hai biến đối tượng, hai dấu bằng so xem hai tham chiếu có trỏ cùng một đối tượng hay không, còn với số nguyên thì so giá trị."""),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: ngăn xếp, heap và các mũi tên", [
        st(svg(1500, 400,
               panel(40, 40, 380, 320, "Stack (ngăn xếp)", C_BLUE),
               box(70, 120, 320, 70, "a = 5", C_GRAY), box(70, 220, 320, 70, "tk = ●", C_GRAY),
               panel(620, 40, 840, 320, "Heap (vùng nhớ chung)", C_AMBER),
               box(840, 170, 340, 120, ["TaiKhoan", "soDu = 100"], C_GREEN, bold=True),
               arrow(390, 255, 835, 235, "#2a78d6", "tham chiếu")),
           """Hình bên trái là ngăn xếp, mỗi lần gọi hàm có một khung riêng giữ biến cục bộ. Số năm nằm ngay trong khung.
           Còn đối tượng tài khoản nằm bên phải, trong heap, vùng nhớ dùng chung. Biến tài khoản chỉ giữ một mũi tên trỏ sang đó."""),
        st(svg(1500, 400,
               panel(40, 40, 380, 320, "Stack", C_BLUE),
               box(70, 120, 320, 70, "tk = ●", C_GRAY), box(70, 220, 320, 70, "tk2 = ●", C_GRAY),
               panel(620, 40, 840, 320, "Heap", C_AMBER),
               box(840, 170, 340, 120, ["TaiKhoan", "soDu = 100"], C_GREEN, bold=True),
               arrow(390, 155, 835, 215, "#2a78d6"), arrow(390, 255, 835, 250, "#2a78d6")),
           """Hai biến tài khoản có thể cùng trỏ tới một đối tượng. Khi đó sửa số dư qua tên này, tên kia cũng thấy ngay,
           vì chỉ có một tài khoản duy nhất trên heap. Đây là điểm người mới hay nhầm với việc sao chép giá trị."""),
        st(svg(1500, 420,
               box(40, 150, 200, 90, "gốc", C_BLUE, bold=True),
               box(340, 150, 180, 90, "A", C_GREEN, bold=True), box(620, 150, 180, 90, "B", C_GREEN, bold=True),
               box(900, 150, 180, 90, "C", C_GREEN, bold=True),
               box(340, 300, 180, 90, "D", C_GRAY, dash=True), box(620, 300, 180, 90, "E", C_GRAY, dash=True),
               box(1180, 150, 180, 90, "F", C_GRAY, dash=True),
               arrow(240, 195, 335, 195), arrow(520, 195, 615, 195), arrow(800, 195, 895, 195), arrow(520, 345, 615, 345),
               txt(1100, 60, "xanh: còn tới được từ gốc, xám: không có đường từ gốc → rác", 26, "middle", "#1f2937", True)),
           """Bộ thu gom rác nhìn heap như một đồ thị. Nó xuất phát từ các gốc, đi theo mọi mũi tên, và đánh dấu mọi đối tượng chạm tới.
           A, B và C tới được từ gốc nên được giữ. D, E và F không còn đường nào tới, nên là rác và sẽ bị dọn."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: đánh dấu rồi quét", [
        st("""<p><b>Bước 1. Chọn các gốc.</b> Gốc là những chỗ chắc chắn còn dùng: biến cục bộ của các hàm đang chạy, biến <code>static</code> (biến gắn với cả lớp, sống suốt chương trình), và các luồng đang chạy (luồng: một dòng việc chạy riêng).</p>
<span class='note'>Làm thử: ở hình trước, gốc chỉ trỏ tới A, nên tập đánh dấu ban đầu là {A}.</span>""",
           """Bước một, chọn các gốc. Gốc là những chỗ chắc chắn còn được dùng, như biến cục bộ của các hàm đang chạy, biến tĩnh, và các luồng đang chạy.
           Biến tĩnh là biến gắn với cả lớp, sống suốt chương trình. Luồng là một dòng việc chạy riêng trong chương trình.
           Làm thử với hình trước, gốc chỉ trỏ tới A, nên tập đánh dấu lúc đầu chỉ có A."""),
        st("""<p><b>Bước 2. Đi theo mũi tên.</b> Mỗi đối tượng được đánh dấu thì đánh dấu luôn mọi đối tượng nó trỏ tới, lặp đến khi hết.</p>
<span class='note'>Làm thử: A trỏ B, B trỏ C, C không trỏ gì, nên tập là {A, B, C}.</span>""",
           """Bước hai, đi theo mũi tên. Hễ một đối tượng được đánh dấu thì mọi đối tượng nó trỏ tới cũng được đánh dấu, lặp cho tới khi hết.
           Làm thử, A trỏ tới B, B trỏ tới C, C không trỏ đi đâu, nên tập đánh dấu là A, B, C."""),
        st("""<p><b>Bước 3. Quét.</b> Mọi đối tượng chưa được đánh dấu là rác, bộ nhớ của chúng được giải phóng.</p>
<span class='note'>Làm thử: sáu đối tượng trừ ba đã đánh dấu còn ba đối tượng rác: D, E, F.</span>
<p>Thực tế: bộ thu gom G1 (mặc định trên máy chủ thông thường từ Java 9) thường không quét từng ô, mà chép đối tượng sống sang vùng mới rồi giải phóng cả vùng cũ.</p>""",
           """Bước ba, quét. Mọi đối tượng chưa được đánh dấu là rác, và bộ nhớ của chúng được giải phóng.
           Làm thử, vì có sáu đối tượng và đã đánh dấu ba, nên còn lại ba đối tượng rác, là D, E và F.
           Trong thực tế, bộ thu gom mặc định của Java trên máy chủ thông thường không quét từng ô, mà chép đối tượng sống sang vùng mới rồi giải phóng cả vùng cũ.
           Ý tưởng tới được từ gốc thì vẫn như vậy."""),
    ], checks=["alg.bnk_reachable({'A': ['B'], 'B': ['C'], 'C': [], 'D': ['E'], 'E': [], 'F': []}, ['A']) == ['A', 'B', 'C']",
               "6 - 3 == 3"])
    sc_ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Giả sử mỗi đối tượng chiếm $100$ byte <i>(số minh hoạ)</i>, và heap đang có sáu đối tượng A đến F.</p>
$$① \\; 6 \\cdot 100 = \\hl{600}\\ \\text{byte}$$""",
           """Giả sử mỗi đối tượng chiếm một trăm byte, đây là số minh hoạ, và heap đang có sáu đối tượng từ A đến F.
           Phép tính thứ nhất, tổng bộ nhớ là sáu nhân một trăm, bằng sáu trăm byte."""),
        st("""<p>Đối tượng còn sống: A, B, C.</p>
$$② \\; \\text{sống} = 3$$""",
           """Phép tính thứ hai, theo bước đánh dấu, đối tượng còn sống là A, B và C, tức là ba đối tượng."""),
        st("""<p>Dùng lại $3$ đối tượng sống ở phép ②.</p>
$$③ \\; 3 \\cdot 100 = \\hlg{300}\\ \\text{byte}$$""",
           """Phép tính thứ ba, bộ nhớ đang sống là ba nhân một trăm, bằng ba trăm byte."""),
        st("""<p>Dùng lại $600$ ở ① và $300$ ở ③.</p>
$$④ \\; 600 - 300 = \\hl{300}\\ \\text{byte} = 3 \\cdot 100$$""",
           """Phép tính thứ tư, bộ nhớ dọn được là sáu trăm trừ ba trăm, bằng ba trăm byte. Số này đúng bằng ba đối tượng D, E, F nhân một trăm."""),
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
           """Kiểm bằng đường khác, đếm thẳng từng đối tượng. A, B và C đều có đường từ gốc. D trỏ tới E, nhưng cả hai không có đường từ gốc.
           F không ai trỏ tới. Vậy rác là ba đối tượng, khớp với kết quả ở trên. Lưu ý, bị trỏ tới chưa chắc còn sống, phải tới được từ gốc."""),
        st(table(["cách lưu tiền", "cộng 10 lần 0,1", "đúng 1?"],
                 [["kiểu double (số thực nhị phân)", "0.9999999999999999", "không"],
                  ["BigDecimal tạo từ chuỗi <code>\"0.1\"</code> (số thập phân)", "1.0", "có"],
                  ["số nguyên theo đơn vị nhỏ nhất: lưu 0,1 thành 1 phần mười", "1 + 1 + … = 10 phần mười = 1", "có"]]),
           """Bảng này so ba cách lưu tiền. Kiểu số thực nhị phân không biểu diễn đúng số không phẩy một, nên cộng mười lần bị lệch.
           BigDecimal giữ số thập phân nên đúng, với điều kiện tạo nó từ chuỗi chữ không phẩy một. Nếu tạo từ một số thực nhị phân, nó mang theo luôn sai lệch.
           Cách thứ ba là lưu số nguyên theo đơn vị nhỏ nhất. Ở đây đơn vị là một phần mười, nên cộng mười lần số một được mười phần mười, đúng bằng một."""),
    ], checks=["alg.bnk_float_vs_decimal()[0] != 1.0", "str(alg.bnk_float_vs_decimal()[1]) == '1.0'", "alg.bnk_float_vs_decimal()[2] == 10",
               "__import__('decimal').Decimal(0.1) != __import__('decimal').Decimal('0.1')", "sum([1] * 10) == 10",
               "len([o for o in 'ABCDEF' if o not in alg.bnk_reachable({'A': ['B'], 'B': ['C'], 'D': ['E']}, ['A'])]) == 3"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Dùng <code>==</code> để so hai chuỗi hay hai đối tượng. <code>==</code> chỉ hỏi
“cùng một đối tượng không”, nên hai chuỗi giống chữ nhưng tạo riêng vẫn cho <code>false</code>. Muốn so nội dung dùng <code>equals</code>.</div>""",
           """Lỗi thứ nhất, của người mới. Dùng hai dấu bằng để so hai chuỗi. Nó chỉ hỏi hai tham chiếu có cùng một đối tượng không.
           Hai chuỗi giống chữ nhưng tạo riêng vẫn cho kết quả là không bằng nhau. Muốn so nội dung thì gọi phương thức so sánh nội dung bằng dấu chấm."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Rò rỉ bộ nhớ</b>: bỏ dữ liệu vào một <code>static Map</code> làm bộ đệm (nơi giữ sẵn dữ liệu hay dùng để lấy lại cho nhanh)
mà không bao giờ xoá. Gốc <code>static</code> vẫn trỏ tới chúng, nên chúng vẫn “tới được” và bộ thu gom rác không dọn.
<br><span class="note">Phép thử: theo dõi kích thước heap sau mỗi lần dọn; nếu cứ tăng thì có thứ đang bị giữ.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là rò rỉ bộ nhớ. Họ bỏ dữ liệu vào một bản đồ tĩnh làm bộ đệm, tức nơi giữ sẵn dữ liệu hay dùng để lấy lại cho nhanh, mà không bao giờ xoá.
           Gốc tĩnh vẫn trỏ tới chúng, nên chúng vẫn tới được, và bộ thu gom rác không dọn. Hãy theo dõi kích thước heap sau mỗi lần dọn.
           Nếu nó cứ tăng, có thứ đang bị giữ.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Dùng <code>double</code> cho số tiền rồi so sánh <code>==</code>. Kết quả
lệch ở chữ số thập phân thứ mười sáu, đủ làm đối soát cuối ngày không khớp.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm. Dùng kiểu số thực nhị phân cho số tiền, rồi so sánh bằng nhau.
           Sai lệch nhỏ ở chữ số thập phân thứ mười sáu cũng đủ làm đối soát cuối ngày không khớp."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Heap có 4 đối tượng, gốc chỉ trỏ tới X, X trỏ tới Y, Z trỏ tới W. Mấy đối tượng là rác?"],
                  ["2", "Mỗi đối tượng 50 byte. Dọn được bao nhiêu byte?"],
                  ["3", "Quyết định: lưu số dư bằng double hay số nguyên?"]]),
           """Bây giờ đến lượt bạn. Câu một, heap có bốn đối tượng, gốc chỉ trỏ tới X, X trỏ tới Y, còn Z trỏ tới W. Có mấy đối tượng là rác?
           Câu hai, mỗi đối tượng năm mươi byte, dọn được bao nhiêu byte? Câu ba, lưu số dư bằng số thực nhị phân hay số nguyên? Hãy dừng video và làm ra giấy.""",
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
           """Đáp án câu ba là một đánh đổi. Số thực nhị phân dễ viết nhưng lệch. Số nguyên đơn vị nhỏ nhất, hoặc BigDecimal, chính xác. Với tiền hãy chọn cách chính xác."""),
    ], checks=["4 - len(alg.bnk_reachable({'X': ['Y'], 'Z': ['W']}, ['X'])) == 2", "2 * 50 == 100"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("tên biến", "tham chiếu", "đối tượng trên heap", "còn tới được từ gốc?", "sống / rác"),
           """Tổng kết chuỗi logic. Tên biến giữ tham chiếu, tham chiếu trỏ tới đối tượng trên heap. Đối tượng còn tới được từ gốc thì sống, không thì là rác."""),
        st("""<div class='box key'><b>Tư duy:</b> rò rỉ bộ nhớ không phải “quên dọn” mà là “vẫn còn người trỏ tới”.
Với tiền: <b>không dùng double</b>; dùng số nguyên đơn vị nhỏ nhất hoặc BigDecimal.</div>""",
           """Điều cần mang theo. Rò rỉ bộ nhớ không phải là quên dọn, mà là vẫn còn người trỏ tới. Còn với tiền, không dùng số thực nhị phân.
           Hãy dùng số nguyên đơn vị nhỏ nhất, hoặc BigDecimal."""),
    ])
    # ── AF2: mã chạy thật, quy mô, tự làm ──
    add_steps([sc_pre], "prereq", [
        st(table(["thêm ba thứ dùng trong mã", "nghĩa", "ví dụ"],
                 [["⑦ Mảng byte", "dãy ô nhớ liền nhau, mỗi ô một byte", "<code>new byte[1_000_000]</code>: một triệu ô, gần 1 MB"],
                  ["⑧ Bản đồ (Map)", "bảng tra: đưa khoá vào thì lấy ra giá trị", "<code>map.put(1, x)</code>: cất x dưới khoá 1"],
                  ["⑨ Tham chiếu yếu", "dây buộc lỏng: trỏ tới đối tượng nhưng <b>không giữ nó sống</b>", "<code>WeakReference</code>: hỏi <code>get()</code> còn đối tượng hay đã bị dọn"]]),
           """Thêm ba thứ sẽ xuất hiện trong mã. Mảng byte là dãy ô nhớ liền nhau, mỗi ô một byte, ví dụ một triệu ô là gần một mê ga byte.
           Bản đồ là bảng tra, đưa khoá vào thì lấy ra giá trị. Tham chiếu yếu là dây buộc lỏng, nó trỏ tới đối tượng nhưng không giữ đối tượng sống, chỉ dùng để hỏi xem đối tượng còn hay đã bị dọn.""",
           clear=True),
    ], at=2)
    sc_pre["title"] = "Trước hết: chín khái niệm cần hiểu"
    sc_run = sc("chay_that", "example", "Chạy thật: tham chiếu mạnh, tham chiếu yếu và gốc static", [
        st(code_block(giu_ref, lines=(4, 9), title="Tệp GiuThamChieu.java (phần chính)"),
           """Ta chạy thật một chương trình ngắn. Dòng đầu tạo một đối tượng gần một mê ga byte, và biến thứ nhất giữ tham chiếu tới nó.
           Dòng thứ hai buộc thêm một tham chiếu yếu, chỉ để hỏi đối tượng còn hay không. Rồi ta gán tham chiếu mạnh bằng rỗng và xin máy dọn rác."""),
        st(out_block(giu_ref),
           """Kết quả in thật có hai dòng. Dòng đầu là còn, vì biến vẫn trỏ tới đối tượng. Dòng sau là không còn, vì hết tham chiếu mạnh thì đối tượng thành rác và máy đã dọn nó.
           Theo đặc tả, lệnh xin dọn chỉ là gợi ý, nhưng ở cách chạy mặc định của máy ảo Java trên máy này, nó được thực hiện.""", clear=True),
        st(code_block(ro_ri, lines=(3, 13), title="Tệp RoRi.java (phần chính)"),
           """Bây giờ tới gốc tĩnh. Biến tĩnh bản đồ là một gốc, nên mọi mảng nó giữ đều còn tới được. Đối tượng Runtime cho biết bộ nhớ của chương trình, gồm tổng bộ nhớ đã xin và phần còn trống.
           Hàm đo gọi dọn rác rồi lấy hiệu hai số đó, ra số mê ga byte heap đang dùng. Ta bỏ năm mảng, mỗi mảng một mê ga byte, vào bản đồ và đo. Sau đó xoá bản đồ và đo lại.""", clear=True),
        st(out_block(ro_ri),
           """Khi bản đồ còn giữ năm mảng, heap đang dùng từ năm mê ga byte trở lên, kết quả là đúng. Xoá bản đồ rồi, năm mảng thành rác và bị dọn, nên heap không còn tới năm mê ga byte.
           Vậy rác còn nằm trong bản đồ tĩnh thì không bị dọn. Đó chính là rò rỉ bộ nhớ.""", clear=True),
    ])
    add_steps([sc_chk], "check", [
        st(code_block(cong_tien, lines=(4, 12), title="Tệp CongTien.java (phần chính)"),
           """Đây là chương trình cộng bằng ba cách. Biến thứ nhất là số thực nhị phân, biến thứ hai là số thập phân tạo từ chuỗi, biến thứ ba là số nguyên đếm theo phần mười.
           Mỗi vòng cộng một phần mười vào cả ba, tổng cộng mười vòng.""", clear=True),
        st(out_block(cong_tien),
           """Chạy thật, ba kết quả khác nhau đúng như bảng vừa nói. Số thực nhị phân cho không phẩy chín chín chín và nhiều chữ chín, vì nó không biểu diễn đúng không phẩy một, nên hai cách còn lại cho đúng một.""", clear=True),
    ])
    add_steps([sc_pit], "pitfalls", [
        st(code_block(so_sanh, lines=(3, 6), title="Chạy thật: hai chuỗi cùng chữ") + out_block(so_sanh),
           """Chạy thật hai chuỗi cùng chữ a b c, nhưng được tạo riêng bằng từ khoá tạo mới. Phép so hai dấu bằng cho kết quả sai, vì đó là hai đối tượng khác nhau.
           Phương thức so nội dung cho kết quả đúng.""", clear=True),
    ], at=1)
    sc_scale = sc("quy_mo", "example", "Quy mô: rò rỉ nhỏ, tải lớn", [
        st("""<p>Giả sử mỗi yêu cầu bỏ lại $1$ KB (1024 byte) trong bản đồ tĩnh, và heap của dịch vụ là $4$ GB $= 4 \\cdot 1024^3$ byte <i>(số minh hoạ)</i>.</p>
$$\\text{thời gian đầy} = \\frac{4 \\cdot 1024^3}{\\text{yêu cầu mỗi giây} \\cdot 1024}\\ \\text{giây}$$
""" + table(["tải", "yêu cầu mỗi giây", "rò rỉ mỗi giây", "đầy heap sau"],
            [["×1", "10", "10 240 byte", "≈ 419 430 giây ≈ <b>4,9 ngày</b>"],
             ["×100", "1 000", "1 024 000 byte", "≈ 4 194 giây ≈ <b>70 phút</b>"],
             ["×10 000", "100 000", "102 400 000 byte", "≈ <b>42 giây</b>"]]),
           """Giả sử mỗi yêu cầu bỏ lại một ki lô byte trong bản đồ tĩnh, và heap của dịch vụ là bốn nghìn không trăm chín mươi sáu mê ga byte. Đây là số minh hoạ.
           Thời gian đầy bằng tổng heap chia cho tốc độ rò rỉ mỗi giây. Với mười yêu cầu mỗi giây, heap đầy sau khoảng bốn phẩy chín ngày.
           Tải tăng một trăm lần, còn khoảng bảy mươi phút. Tải tăng mười nghìn lần, chỉ còn khoảng bốn mươi hai giây.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Khởi động lại dịch vụ mỗi đêm đủ ở tải ×1 vì 4,9 ngày dài hơn một ngày. Ở ×100 phải khởi động lại mỗi giờ, ở ×10 000 thì sập
trước khi kịp khởi động lại. <b>Tăng heap gấp đôi</b> chỉ kéo dài gấp đôi thời gian, không đổi bản chất.</div>
<div class="box key"><b>Sửa gốc:</b> giới hạn bộ đệm, ví dụ tối đa $10\\,000$ mục, tức tối đa $10\\,240\\,000$ byte (khoảng 10 MB) dù tải bao nhiêu.
<b>Đánh đổi:</b> mục bị đuổi đi thì lần sau phải tra lại từ nguồn gốc, chậm hơn.</div>""",
           """Giải pháp cũ là khởi động lại dịch vụ mỗi đêm. Nó đủ ở tải gốc vì bốn phẩy chín ngày dài hơn một ngày. Ở tải gấp trăm lần phải khởi động lại mỗi giờ, và ở tải gấp mười nghìn lần dịch vụ sập trước khi kịp khởi động lại.
           Tăng heap gấp đôi chỉ kéo dài gấp đôi thời gian, không đổi bản chất. Cách sửa gốc là giới hạn bộ đệm, ví dụ tối đa mười nghìn mục, tức khoảng mười mê ga byte dù tải bao nhiêu.
           Đánh đổi là mục bị đuổi đi thì lần sau phải tra lại từ nguồn gốc, chậm hơn.""", clear=True),
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

Chạy: `javac PhiLech.java && java PhiLech`. Chấm: `bash labs/cham.sh BNK L00 PhiLech.java`.
""", "java", phi_lech["code"], phi_lech["out"])
    sc_lab = practice_scene(sc, "Tự làm: phí 0,3 cộng hai mươi lần", practice_steps(
        st, "BNK", "L00",
        """<p><b>Đề</b>: một khoản phí 0,3 bị cộng 20 lần. Viết <code>PhiLech.java</code>:</p>
<ol><li>biến <code>double</code> cộng <code>0.3</code> hai mươi lần; biến <code>long</code> cộng <code>3</code> (một phần mười) hai mươi lần</li>
<li>in ba dòng: <code>double: …</code>, <code>so nguyen: … phan muoi</code>, <code>bang 6? …</code> (so <code>tong == 6.0</code>)</li></ol>
<p class="note">Chạy: <code>javac PhiLech.java &amp;&amp; java PhiLech</code>.</p>""",
        """Bây giờ tới phần bạn tự làm. Một khoản phí không phẩy ba bị cộng hai mươi lần. Hãy viết chương trình cộng nó hai mươi lần bằng số thực nhị phân, và cộng số ba, tức ba phần mười, hai mươi lần bằng số nguyên.
        In ba dòng như trên màn hình: tổng số thực, tổng số nguyên, và kết quả so sánh tổng số thực với sáu. Hãy dừng video, tự viết và chạy, đừng chép lại ví dụ.""",
        phi_lech["out"], "PhiLech.java",
        """<div class="box key"><b>Nếu kẹt:</b> khai <code>double tong = 0;</code> và <code>long phanMuoi = 0;</code>, rồi vòng lặp 20 lần: <code>tong += 0.3;</code> và <code>phanMuoi += 3;</code>.
Lời giải ở <code>labs/BNK/L00/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, khai một biến số thực và một biến số nguyên dài, bắt đầu bằng không. Trong vòng lặp hai mươi lần, cộng không phẩy ba vào biến thứ nhất và cộng ba vào biến thứ hai.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=90), "BNK", "L00")
    scenes = [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_run, sc_chk, sc_pit, sc_quiz, sc_scale, sc_lab, sc_rec]
    return lesson("L00", "java_bo_nho_gc", "Bài 0 — Java hiện đại: bộ nhớ, đối tượng và bộ thu gom rác",
                  "curriculum/bnk.yaml L00; audit/bnk/verify_bnk.py L00; audit/review/screen_code/BNK.yaml (mã chạy thật bằng JDK 21); The Java Virtual Machine Specification (Java SE 21); IEEE 754; JEP 248 (G1 mặc định từ JDK 9 trên máy server-class) và HotSpot GC Tuning Guide Java SE 21; Java SE 21 API: BigDecimal(String) và BigDecimal(double), java.lang.ref.WeakReference, Runtime.totalMemory/freeMemory, System.gc (chỉ là gợi ý); IEC 80000-13 (KiB = 1024 byte)",
                  ["Phân biệt dữ liệu nằm trên stack và trên heap", "Xác định đối tượng nào bị thu gom từ đồ thị tham chiếu",
                   "Nhận ra rò rỉ bộ nhớ do tham chiếu static và chạy thật để thấy nó", "Tính sau bao lâu rò rỉ làm đầy heap khi tải tăng ×100 và ×10 000",
                   "Chọn kiểu dữ liệu đúng cho số tiền"],
                  scenes, covers=[(1, "intuition"), (2, "example"), (3, "chay_that"), (4, "quy_mo"), (5, "practice")])
