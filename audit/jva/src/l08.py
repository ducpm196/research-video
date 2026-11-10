from lib import *


def ln(p, s):
    """Số thứ tự (tính từ 1) của dòng đầu tiên trong mã của p có chứa s."""
    for i, l in enumerate(p["code"].split("\n"), 1):
        if s in l:
            return i
    raise ValueError(s)


DONG = "0123456789;1234567"


def build():
    chuoi = prog("Chuoi", """
public class Chuoi {
    public static void main(String[] args) {
        String ten = "Nguyen Van An";
        System.out.println(ten.length());          // số ký tự
        System.out.println(ten.charAt(0));         // ký tự ở chỉ số 0
        System.out.println(ten.indexOf(" "));      // vị trí dấu cách đầu tiên
        System.out.println(ten.substring(0, 6));   // từ chỉ số 0 tới TRƯỚC 6
        System.out.println(ten.substring(7));      // từ chỉ số 7 tới hết
        System.out.println("[" + "  0123  ".trim() + "]");   // bỏ khoảng trắng hai đầu
    }
}""", out="13\nN\n6\nNguyen\nVan An\n[0123]")
    so_sanh = prog("SoSanh", """
public class SoSanh {
    public static void main(String[] args) {
        String a = "1234";
        String b = new String("1234");     // tạo riêng một đối tượng mới
        String c = "1234";                 // viết y hệt a ngay trong mã
        System.out.println(a == b);        // so mũi tên
        System.out.println(a.equals(b));   // so nội dung
        System.out.println(a == c);        // đúng: hai chuỗi hằng y hệt dùng chung
    }
}""", out="false\ntrue\ntrue")
    bat_bien = prog("BatBien", """
public class BatBien {
    public static void main(String[] args) {
        String s = "vnd";
        String t = s.toUpperCase();        // trả về chuỗi MỚI, s giữ nguyên
        System.out.println(s + " " + t);
        s = s + " 2026";                   // tạo chuỗi mới, rồi s trỏ sang nó
        System.out.println(s);
    }
}""", out="vnd VND\nvnd 2026")
    tach = prog("TachDong", """
import java.util.Locale;

public class TachDong {
    public static void main(String[] args) {
        String dong = "%s";             // số tài khoản;số tiền
        int p = dong.indexOf(";");                     // (1)
        String stk = dong.substring(0, p);             // (2)
        String phan2 = dong.substring(p + 1);          // (3)
        long soTien = Long.parseLong(phan2);           // (4) chuỗi thành số
        String dep = String.format(Locale.US, "%%,d", soTien);   // (5)
        System.out.println(p);
        System.out.println(stk + " | " + phan2);
        System.out.println(phan2 + 1);
        System.out.println(soTien + 1);
        System.out.println(dep + " dong");
    }
}""" % DONG, out="10\n0123456789 | 1234567\n12345671\n1234568\n1,234,567 dong")
    kiem = prog("KiemTach", """
public class KiemTach {
    public static void main(String[] args) {
        String dong = "%s";
        String[] phan = dong.split(";");               // tách tại mỗi dấu ;
        System.out.println(phan.length);
        System.out.println(phan[0].equals("0123456789"));
        System.out.println(Long.parseLong(phan[1]) == 1234567);
        System.out.println(phan[0].length() + 1 + phan[1].length() == dong.length());
    }
}""" % DONG, out="2\ntrue\ntrue\ntrue")
    quen_gan = prog("QuenGan", """
public class QuenGan {
    public static void main(String[] args) {
        String stk = "  0123456789  ";
        stk.trim();                          // SAI: chuỗi mới bị bỏ đi
        System.out.println("[" + stk + "]");
        stk = stk.trim();                    // ĐÚNG: gán lại
        System.out.println("[" + stk + "]");
    }
}""", out="[  0123456789  ]\n[0123456789]")
    rong = prog("Rong", """
public class Rong {
    static String timTen(String stk) {
        if (stk.equals("0123456789")) {
            return "An";
        }
        return null;                         // không tìm thấy
    }

    public static void main(String[] args) {
        System.out.println("An".equals(timTen("999")));   // an toàn
        System.out.println(timTen("999").equals("An"));   // ném ngoại lệ
    }
}""", out="false", expect="runtime_error:NullPointerException",
        # dòng lỗi đầy đủ dài 141 ký tự, tràn khung: hiện phần đầu nguyên văn rồi " …" để người học biết dòng còn tiếp
        # (verify_jva và screen_code coi "…" là đoạn lược); phần sau là: because the return value of "Rong.timTen(String)" is null
        err='Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.equals(Object)" …')
    noi = prog("NoiChuoi", """
public class NoiChuoi {
    public static void main(String[] args) {
        int n = 10000;
        String s = "";
        long daChep = 0;
        for (int i = 0; i < n; i++) {
            s = s + "x";                     // tạo chuỗi mới, chép lại cả chuỗi cũ
            daChep += s.length();
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) { sb.append("x"); }   // thêm vào cuối
        System.out.println(s.equals(sb.toString()) + ", da chep " + daChep);
    }
}""", out="true, da chep 50005000")
    quiz = prog("DoanChuoi", """
public class DoanChuoi {
    public static void main(String[] args) {
        String s = "  STK;12345  ";
        String t = s.trim();
        System.out.println(s.length() + " " + t.length());
        String[] p = t.split(";");
        System.out.println(p[0].charAt(1) + p[1].substring(3));
        System.out.println(t.indexOf("4"));
    }
}""", out="13 9\nT45\n7")

    sc_hook = sc("hook", "hook", "Hai số tài khoản giống hệt nhau, máy vẫn bảo khác?", [
        st("""<p>Khách gõ số tài khoản <code>0123456789</code>, hệ thống tra đúng số đó trong danh sách… và báo <b>không tìm thấy</b>.</p>
<div class="box warn">Lỗi thật hay gặp: so hai chuỗi bằng <code>==</code>, hoặc quên bỏ khoảng trắng thừa ở hai đầu.</div>""",
           """Khách gõ đúng số tài khoản, hệ thống tra đúng số đó trong danh sách, vậy mà báo không tìm thấy.
           Thủ phạm thường là so hai chuỗi bằng dấu bằng bằng, hoặc quên bỏ khoảng trắng thừa ở hai đầu."""),
        st("""<p>Dữ liệu ngân hàng phần lớn là <b>chữ</b>: số tài khoản, tên khách, từng dòng tệp đối soát <code>0123456789;1234567</code>.</p>
<div class="box key">Hôm nay ta học <b>chuỗi</b>: đọc, cắt, so sánh, đổi thành số và định dạng tiền cho đúng.</div>""",
           """Dữ liệu ngân hàng phần lớn là chữ, như số tài khoản, tên khách, hay từng dòng của tệp đối soát, tức tệp hai bên gửi nhau để so khớp giao dịch.
           Hôm nay ta học chuỗi: đọc, cắt, so sánh, đổi thành số, và định dạng tiền cho đúng."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng hôm nay", [
        st(table(["đã học", "viết", "dùng lại hôm nay"],
                 [["① mảng: chỉ số từ 0 tới length − 1", "<code>a[0]</code>, <code>a.length</code>", "ký tự trong chuỗi cũng đánh chỉ số từ 0"],
                  ["② đối tượng và tham chiếu, gọi hàm qua dấu chấm", "<code>an.nap(1000000)</code>", "chuỗi là đối tượng: <code>ten.length()</code>"],
                  ["③ dấu <code>+</code> với chuỗi là nối chữ", "<code>\"A\" + 1 + 2</code> ra <code>A12</code>", "phân biệt chuỗi số với số"]]),
           """Trước hết ta ôn lại ba điều. Thứ nhất, phần tử của mảng đánh chỉ số từ không tới độ dài trừ một.
           Thứ hai, đối tượng được giữ qua tham chiếu, và ta gọi hàm của nó qua dấu chấm.
           Thứ ba, dấu cộng có một vế là chuỗi thì nối chữ, làm từ trái sang phải.""", focus=[1, "1.2", "1.3", "1.4"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã các hàm hay dùng của chuỗi", [
        st(code_block(chuoi, lines=(3, 9), title="Tệp Chuoi.java"),
           """Chuỗi trong Java là một đối tượng, nên ta gọi hàm của nó qua dấu chấm. Chương trình này thử sáu hàm trên tên Nguyễn Văn An."""),
        st(table(["viết", "nghĩa", "kết quả"],
                 [["<code>ten.length()</code>", "số ký tự; chuỗi <b>có</b> ngoặc tròn, mảng thì không", "13"],
                  ["<code>ten.charAt(0)</code>", "ký tự ở chỉ số 0, đếm từ 0 như mảng", "N"],
                  ["<code>ten.indexOf(\" \")</code>", "chỉ số lần xuất hiện đầu tiên; không có thì ra −1", "6"],
                  ["<code>ten.substring(0, 6)</code>", "chuỗi con từ chỉ số 0 tới <b>trước</b> 6", "Nguyen"],
                  ["<code>ten.substring(7)</code>", "chuỗi con từ chỉ số 7 tới hết", "Van An"],
                  ["<code>\"  0123  \".trim()</code>", "bỏ khoảng trắng ở hai đầu", "[0123]"]]),
           """Hàm độ dài cho số ký tự, và với chuỗi thì có ngoặc tròn, khác mảng.
           Hàm lấy ký tự đếm chỉ số từ không, giống mảng.
           Hàm tìm vị trí trả về chỉ số lần xuất hiện đầu tiên, không thấy thì ra âm một.
           Hàm cắt với hai số lấy từ chỉ số đầu tới trước chỉ số sau.
           Với một số, nó lấy từ đó tới hết chuỗi.
           Hàm cắt khoảng trắng bỏ dấu cách thừa ở hai đầu.""", clear=True,
           focus=["1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ])
    cells = [box(60 + k * 76, 150, 70, 80, ch, C_RED if ch == ";" else C_BLUE, 26, True) for k, ch in enumerate(DONG)]
    idx = [txt(95 + k * 76, 135, str(k), 20, "middle", "#2a78d6") for k in range(len(DONG))]
    sc_int = sc("intuition", "intuition", "Hình dung: dãy ký tự đánh số, và hai kiểu so sánh", [
        st(svg(1500, 360, *cells, *idx,
               txt(475, 290, "substring(0, 10): chỉ số 0 … 9", 24, "middle", "#2a78d6", True),
               txt(1180, 290, "substring(11): chỉ số 11 … 17", 24, "middle", "#2a78d6", True),
               txt(855, 330, "indexOf(\";\") = 10, length() = 18", 24, "middle", "#dc2626", True)),
           """Hãy hình dung chuỗi như một dãy ô ký tự, đánh chỉ số từ không, giống mảng.
           Dòng đối soát này có mười tám ký tự, dấu chấm phẩy nằm ở chỉ số mười.
           Phần trước là chỉ số không tới chín, phần sau là mười một tới mười bảy."""),
        st(svg(1500, 400,
               box(20, 40, 160, 80, ["a"], C_AMBER, 26, True),
               box(20, 160, 160, 80, ["c"], C_AMBER, 26, True),
               box(20, 280, 160, 80, ["b"], C_AMBER, 26, True),
               arrow(185, 80, 480, 120, "#d97706"),
               arrow(185, 200, 480, 145, "#d97706"),
               arrow(185, 320, 480, 320, "#d97706"),
               box(490, 80, 300, 90, ["\"1234\"", "đối tượng thứ nhất"], C_BLUE, 24, True),
               box(490, 275, 300, 90, ["\"1234\"", "đối tượng thứ hai (new)"], C_BLUE, 24, True),
               txt(1140, 130, "a == b: so MŨI TÊN → false", 26, "middle", "#dc2626", True),
               txt(1140, 200, "a.equals(b): so TỪNG KÝ TỰ → true", 26, "middle", "#16a34a", True),
               txt(1140, 270, "a == c: cùng một đối tượng → true", 24, "middle", "#6b7280"),
               txt(1140, 310, "(chỉ chuỗi hằng viết y hệt trong mã mới dùng chung)", 22, "middle", "#6b7280")),
           """Chuỗi là đối tượng, nên biến chuỗi chỉ giữ mũi tên tham chiếu, giống biến mảng.
           Dấu bằng bằng so hai mũi tên, nên hai đối tượng riêng có cùng nội dung vẫn cho kết quả sai.
           Hàm so nội dung thì so từng ký tự, nên cho kết quả đúng.
           Biến c trỏ cùng đối tượng với a vì Java dùng chung một đối tượng cho các chuỗi hằng viết y hệt ngay trong mã.
           Chuỗi khách gõ vào, đọc từ tệp hay ghép lúc chạy thì không được dùng chung như thế, nên đừng dựa vào điều này."""),
        st(code_block(so_sanh, lines=(3, 8), title="Tệp SoSanh.java") + out_block(so_sanh),
           """Chạy thật để kiểm. Dấu bằng bằng giữa a và b in sai, hàm so nội dung in đúng, còn a với c in đúng chỉ vì hai chuỗi hằng dùng chung.
           Quy tắc rút ra là muốn so nội dung hai chuỗi thì luôn dùng hàm so nội dung.""", focus=[4, [2, 4], 2]),
    ])
    b4 = ln(bat_bien, "toUpperCase")
    t5 = ln(tach, 'String dong')
    sc_form = sc("formula", "formula", "Suy ra từng bước: cắt một dòng đối soát thành hai phần", [
        st("<p><b>Bước 1. Độ dài chuỗi con.</b> <code>substring(a, b)</code> lấy chỉ số $a$ tới $b - 1$, nên có</p>"
           "$$(b - 1) - a + 1 = b - a \\text{ ký tự}$$",
           """Bước một, đếm độ dài chuỗi con. Hàm cắt lấy từ chỉ số a tới chỉ số b trừ một, nên số ký tự là b trừ một, trừ a, cộng một, tức là b trừ a.
           Ví dụ cắt từ không tới sáu được sáu ký tự."""),
        st("<p><b>Bước 2. Tìm chỗ cắt.</b> Gọi $p$ là chỉ số dấu <code>;</code>.</p>"
           "$$\\text{phần trước} = \\text{substring}(0, p) \\qquad \\text{phần sau} = \\text{substring}(p + 1)$$",
           """Bước hai, tìm chỗ cắt. Gọi p là chỉ số của dấu chấm phẩy, tìm bằng hàm tìm vị trí.
           Phần trước lấy từ không tới trước p, nên không dính dấu chấm phẩy.
           Phần sau bắt đầu từ p cộng một, vì phải bỏ qua chính dấu chấm phẩy."""),
        st("<p><b>Bước 3. Kiểm độ dài:</b> hai phần cộng dấu <code>;</code> phải bằng cả dòng.</p>"
           "$$p + 1 + (n - p - 1) = n$$",
           """Bước ba, kiểm bằng độ dài. Phần trước có p ký tự, dấu chấm phẩy một ký tự, phần sau có n trừ p trừ một ký tự.
           Cộng lại bằng n, nghĩa là không mất và không thừa ký tự nào."""),
        st("<p><b>Bước 4. Chuỗi bất biến:</b> không hàm nào sửa được chuỗi cũ; kết quả nằm ở chuỗi được <b>trả về</b>.</p>"
           + code_block(bat_bien, lines=(b4 - 1, b4 + 3)) + out_block(bat_bien),
           """Bước bốn, một tính chất quan trọng là chuỗi bất biến, nghĩa là không hàm nào sửa được nội dung của chuỗi đã tạo.
           Hàm đổi chữ hoa trả về chuỗi mới, nên biến s vẫn là chữ thường. Phép nối cũng tạo chuỗi mới, rồi biến s trỏ sang nó.""",
           focus=[1, [2, 4], [2, 4]]),
    ], checks=["len('Nguyen Van An'[0:6]) == 6 - 0", "all(len('0123456789;1234567'[a:b]) == b - a for a in range(0, 5) for b in range(5, 18))",
               "len('0123456789') + 1 + len('1234567') == len('0123456789;1234567')"])
    sc_ex = sc("example", "example", "Ví dụ: tách dòng “số tài khoản;số tiền”, từng phép tính", [
        st(code_block(tach, lines=(t5, t5 + 5), title="Tệp TachDong.java"),
           """Bây giờ ta tách một dòng đối soát, gồm số tài khoản, dấu chấm phẩy, và số tiền một triệu hai trăm ba mươi tư nghìn năm trăm sáu mươi bảy đồng.
           Ta tính từng lệnh trong năm lệnh đánh số."""),
        st(code_block(tach, lines=(t5 + 1, t5 + 3))
           + "$$① \\; p = \\hl{10} \\qquad ② \\; \\text{substring}(0, 10) = \\hl{\\text{0123456789}} \\qquad ③ \\; \\text{substring}(11) = \\hl{\\text{1234567}}$$",
           """Phép tính thứ nhất, dấu chấm phẩy nằm ở chỉ số mười, vì trước nó có đúng mười chữ số.
           Phép tính thứ hai, cắt từ không tới trước mười được số tài khoản mười chữ số.
           Phép tính thứ ba, cắt từ mười một tới hết được bảy chữ số của số tiền, nhưng vẫn đang là chuỗi."""),
        st(code_block(tach, lines=(t5 + 4, t5 + 4)) + code_block(tach, lines=(t5 + 8, t5 + 9))
           + "$$④ \\; \\text{\"1234567\"} + 1 = \\text{12345671} \\qquad 1234567 + 1 = \\hl{1234568}$$",
           """Phép tính thứ tư, hàm đổi chuỗi thành số nguyên dài biến bảy chữ số thành một con số thật.
           Để thấy khác biệt, chuỗi cộng một là nối chữ, ra tám chữ số. Còn số cộng một là cộng số, ra số lớn hơn đúng một đơn vị.""",
           focus=[1, 3, 3]),
        st(code_block(tach, lines=(t5 + 5, t5 + 5))
           + "$$⑤ \\; 1234567 \\to \\hlg{\\text{1,234,567}}$$"
           + "<span class='note'>Ghi rõ <code>Locale.US</code> (cần <code>import java.util.Locale;</code> ở đầu tệp): máy đặt vùng Việt Nam sẽ in dấu chấm, 1.234.567.</span>",
           """Phép tính thứ năm, hàm định dạng với mẫu phần trăm, dấu phẩy, chữ d chèn dấu phân cách hàng nghìn.
           Ta ghi rõ tham số vùng nước Mỹ, vì máy đặt vùng Việt Nam sẽ dùng dấu chấm thay cho dấu phẩy."""),
        st(out_block(tach),
           """Chạy thật chương trình, năm dòng in ra khớp đúng với năm phép tính ta vừa làm tay.""",
           focus=[[2]]),
    ], checks=["'0123456789;1234567'.index(';') == 10", "'0123456789;1234567'[0:10] == '0123456789'",
               "'0123456789;1234567'[11:] == '1234567'", "'1234567' + str(1) == '12345671' and int('1234567') + 1 == 1234568",
               "format(1234567, ',d') == '1,234,567'"])
    k4 = ln(kiem, "split")
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: tách bằng hàm tách và đếm độ dài", [
        st(code_block(kiem, lines=(k4, k4 + 4), title="Tệp KiemTach.java")
           + "<span class='note'>Chữ trong ngoặc của <code>split</code> là một mẫu đặc biệt: <code>\";\"</code> dùng thẳng được, "
             "nhưng dấu <code>.</code> hay <code>|</code> thì không.</span>",
           """Ta kiểm bằng một đường khác hẳn: không dùng hàm tìm vị trí mà dùng hàm tách, vì hàm này tự cắt chuỗi tại mỗi dấu chấm phẩy và trả về một mảng chuỗi. Lưu ý chữ trong ngoặc là một mẫu đặc biệt, nên dấu chấm hay dấu vạch đứng không dùng thẳng được như dấu chấm phẩy.
           Ta kiểm số phần, so nội dung bằng hàm so nội dung, và kiểm độ dài như bước ba.""", focus=[2, 3, 2]),
        st(out_block(kiem) + "$$10 + 1 + 7 = 18 \\; \\checkmark$$",
           """Chạy thật, mảng có hai phần, phần đầu đúng số tài khoản, phần sau đổi ra đúng số tiền.
           Dòng cuối đúng, vì mười cộng một cộng bảy bằng mười tám, đúng độ dài cả dòng, nên hai cách tách cho cùng kết quả.""",
           focus=[["2.1", "2.2", "2.3"], ["2.4", 3]]),
    ], checks=["'0123456789;1234567'.split(';') == ['0123456789', '1234567']", "10 + 1 + 7 == len('0123456789;1234567')"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Gọi hàm của chuỗi mà không gán lại kết quả.</div>'
           + code_block(quen_gan, lines=(3, 7)) + out_block(quen_gan),
           """Lỗi thứ nhất, của người mới, là gọi hàm cắt khoảng trắng mà không gán lại.
           Vì chuỗi bất biến, hàm trả về chuỗi mới rồi chuỗi ấy bị bỏ đi, nên dòng in đầu vẫn còn khoảng trắng.
           Phải gán lại kết quả thì mới được chuỗi sạch.""", focus=[1, [2, "4.1"], "4.2"]),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Gọi hàm trên giá trị rỗng <code>null</code>, tức biến không trỏ tới chuỗi nào (khác chuỗi không có ký tự <code>""</code>).</div>'
           + code_block(rong, lines=(ln(rong, '"An".equals'), ln(rong, '"An".equals') + 1)) + out_block(rong),
           """Lỗi thứ hai gặp cả ở người đã đi làm: hàm tra tên trả về giá trị rỗng khi không tìm thấy, nghĩa là không trỏ tới chuỗi nào.
           Gọi hàm so nội dung trên giá trị rỗng thì máy ảo ném ngoại lệ con trỏ rỗng, báo rằng không gọi được hàm so nội dung.
           Cách an toàn là đặt chuỗi hằng đứng trước, vì nó không bao giờ rỗng, nên dòng đầu in sai chứ không ném lỗi.""",
           focus=[1, [2, "4.2"], [2, "4.1"]]),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nối chuỗi bằng <code>+</code> trong vòng lặp lớn.</div>'
           + code_block(noi, lines=(ln(noi, "for"), ln(noi, "sb.append") + 1)) + out_block(noi),
           """Lỗi thứ ba là nối chuỗi bằng dấu cộng trong vòng lặp lớn, vì mỗi lần nối, máy tạo chuỗi mới và chép lại cả chuỗi cũ.
           Với mười nghìn lần, số ký tự phải chép là năm mươi triệu không trăm linh năm nghìn, bằng n nhân n cộng một chia hai.
           Bộ dựng chuỗi, tức một đối tượng giữ dãy ký tự sửa được, chỉ thêm vào cuối, nên công việc tăng theo n chứ không theo n bình phương, mà kết quả y hệt.""",
           focus=[[1, 2], "4.1", [2, "4.1"]]),
    ], checks=["sum(range(1, 10000 + 1)) == 10000 * (10000 + 1) // 2 == 50005000"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(3, 8), title="Đoán ba dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Chuỗi s có hai dấu cách ở mỗi đầu, ở giữa là ba chữ cái, dấu chấm phẩy, rồi năm chữ số từ một tới năm.
           Chương trình in độ dài trước và sau khi cắt khoảng trắng, rồi tách, cắt, và tìm vị trí chữ số bốn.
           Hãy dừng video, viết ra giấy ba dòng in ra.""", pause=20),
        st(table(["biểu thức", "lý do", "giá trị"],
                 [["<code>s.length()</code>", "2 + 3 + 1 + 5 + 2", "13"],
                  ["<code>t.length()</code>", "bỏ 4 dấu cách: 13 − 4", "9"],
                  ["<code>p[0].charAt(1)</code>", "\"STK\", chỉ số 1", "T"],
                  ["<code>p[1].substring(3)</code>", "\"12345\" từ chỉ số 3", "45"],
                  ["<code>t.indexOf(\"4\")</code>", "S T K ; 1 2 3 4 → chỉ số 7", "7"]]),
           """Đáp án như sau. Chuỗi s dài mười ba ký tự, vì hai cộng ba cộng một cộng năm cộng hai.
           Bỏ bốn dấu cách thì còn chín.
           Phần đầu sau khi tách có chữ T ở chỉ số một.
           Phần sau cắt từ chỉ số ba còn bốn năm, nối với chữ T thành T bốn năm.
           Trong chuỗi đã cắt, chữ số bốn đứng ở chỉ số bảy.""", focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6"]),
        st(out_block(quiz),
           """Chạy thật chương trình, ba dòng in ra là mười ba chín, T bốn năm, và bảy."""),
    ], checks=["len('  STK;12345  ') == 13 and len('  STK;12345  '.strip()) == 9",
               "'STK;12345'.split(';')[0][1] + 'STK;12345'.split(';')[1][3:] == 'T45'",
               "'STK;12345'.index('4') == 7"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("chuỗi = dãy ký tự, chỉ số từ 0", "kết quả ở chuỗi trả về, phải gán lại", "so nội dung bằng equals", "chuỗi số → số bằng Long.parseLong"),
           """Tổng kết chuỗi logic. Chuỗi là dãy ký tự đánh chỉ số từ không. Không hàm nào sửa chuỗi cũ, kết quả nằm ở chuỗi trả về, nên phải gán lại.
           So nội dung thì dùng hàm so nội dung, và muốn tính toán thì đổi chuỗi số thành số trước."""),
        st("""<div class='box key'><b>Tư duy:</b> dữ liệu chữ đi vào hệ thống luôn qua ba bước: <b>làm sạch</b> (<code>trim</code>),
<b>tách</b> (<code>indexOf/substring</code> hoặc <code>split</code>), <b>kiểm</b> (độ dài, <code>equals</code>). Viết <code>"hằng".equals(x)</code> để không vấp giá trị rỗng.</div>""",
           """Điều cần mang theo. Dữ liệu chữ đi vào hệ thống luôn qua ba bước: làm sạch, tách, rồi kiểm độ dài và nội dung.
           Và hãy đặt chuỗi hằng đứng trước khi so, để không vấp giá trị rỗng."""),
    ])
    return lesson("L08", "chuoi", "Bài 8 — Chuỗi: cắt, so sánh và định dạng dữ liệu chữ",
                  "curriculum/jva.yaml L08; audit/jva/verify_jva.py L08 (javac/java chạy thật); The Java Language Specification, "
                  "Java SE 21 (JLS §4.3.3 lớp String, §3.10.5 chuỗi hằng dùng chung một đối tượng, §15.21.3 so sánh tham chiếu ==, "
                  "§15.18.1 nối chuỗi); java.lang.String (length, charAt, indexOf, substring, trim, split, equals, format), "
                  "java.lang.StringBuilder, java.lang.Long.parseLong, java.util.Formatter (cờ ',' theo Locale), Java SE 21 API; "
                  "JEP 358 thông báo NullPointerException chi tiết; dev.java/learn",
                  ["Dùng length, charAt, indexOf, substring, trim, split trên chuỗi, với chỉ số từ 0",
                   "Giải thích vì sao == so tham chiếu còn equals so nội dung",
                   "Tách dòng “số tài khoản;số tiền”, đổi phần số bằng Long.parseLong và định dạng 1,234,567",
                   "Tránh lỗi quên gán lại chuỗi, gọi hàm trên giá trị rỗng, nối chuỗi trong vòng lặp lớn"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
