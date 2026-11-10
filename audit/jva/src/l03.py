from lib import *

PHI = """
public class Phi {
    public static void main(String[] args) {
        long soTien = @;                 // số tiền chuyển (đồng)
        long phi;
        if (soTien < 500000) {           // bậc 1: dưới 500 nghìn
            phi = 0;
        } else if (soTien < 10000000) {  // bậc 2: từ 500 nghìn tới dưới 10 triệu
            phi = 2200;
        } else {                         // bậc 3: từ 10 triệu trở lên
            phi = 5500;
        }
        System.out.println(soTien + " -> phi " + phi);
    }
}"""


def phi_prog(so_tien, phi):
    return prog("Phi", PHI.replace("@", str(so_tien)), out=f"{so_tien} -> phi {phi}")


def build():
    phi_sai = prog("PhiSai", """
public class PhiSai {
    public static void main(String[] args) {
        long soTien = 10000000;
        long phi;
        if (soTien > 10000000) {         // quy định ghi "từ 10 triệu": phải là >=
            phi = 5500;
        } else if (soTien > 500000) {
            phi = 2200;
        } else {
            phi = 0;
        }
        System.out.println(soTien + " -> phi " + phi);
    }
}""", out="10000000 -> phi 2200")
    rut = prog("RutTien", """
public class RutTien {
    public static void main(String[] args) {
        long soDu = 300000;
        long soTien = 500000;
        if (soTien <= soDu) {            // điều kiện: đúng hoặc sai
            soDu -= soTien;
            System.out.println("Da rut, con " + soDu);
        } else {                         // điều kiện sai thì làm khối này
            System.out.println("Khong du tien");
        }
    }
}""", out="Khong du tien")
    kenh = prog("Kenh", """
public class Kenh {
    public static void main(String[] args) {
        String kenh = "APP";
        switch (kenh) {
            case "ATM" -> System.out.println("Rut tien mat");
            case "APP", "WEB" -> System.out.println("Chuyen khoan online");
            default -> System.out.println("Kenh khac");
        }
    }
}""", out="Chuyen khoan online")
    vip = prog("Vip", """
public class Vip {
    public static void main(String[] args) {
        boolean laVip = true;
        long phi = laVip ? 0 : 2200;     // khách VIP được miễn phí (số minh hoạ)
        System.out.println("Phi: " + phi);
    }
}""", out="Phi: 0")
    p1 = phi_prog(499999, 0)
    p2 = phi_prog(500000, 2200)
    p3 = phi_prog(10000000, 5500)
    kiem = prog("KiemBien", """
public class KiemBien {
    public static void main(String[] args) {
        long soTien = 500000;
        System.out.println(soTien < 500000);                         // bậc 1?
        System.out.println(soTien >= 500000 && soTien < 10000000);   // bậc 2?
        System.out.println(soTien >= 10000000);                      // bậc 3?
    }
}""", out="false\ntrue\nfalse")
    gan_nham = prog("GanNham", """
public class GanNham {
    public static void main(String[] args) {
        int soLan = 3;
        if (soLan = 5) {                 // định so sánh, lại viết phép gán
            System.out.println("Khoa the");
        }
    }
}""", expect="compile_error:incompatible types: int cannot be converted to boolean")
    thieu_ngoac = prog("ThieuNgoac", """
public class ThieuNgoac {
    public static void main(String[] args) {
        long soDu = 100000;
        long soTien = 500000;
        if (soTien <= soDu)
            System.out.println("Dong y rut");
            soDu = soDu - soTien;        // thụt lề nhưng KHÔNG thuộc nhánh nếu
        System.out.println("So du: " + soDu);
    }
}""", out="So du: -400000")
    quiz = prog("Hang", """
public class Hang {
    public static void main(String[] args) {
        int diem = 85;                   // điểm tín dụng (số minh hoạ)
        String hang;
        if (diem >= 50) {
            hang = "Bac";
        } else if (diem >= 80) {
            hang = "Vang";
        } else {
            hang = "Thuong";
        }
        System.out.println(hang);
        System.out.println(diem >= 80 ? "Uu tien" : "Binh thuong");
    }
}""", out="Bac\nUu tien")

    bieu_phi = table(["số tiền chuyển", "phí (số minh hoạ)"],
                     [["dưới 500 000 đồng", "0 đồng"], ["từ 500 000 đến dưới 10 000 000 đồng", "2 200 đồng"],
                      ["từ 10 000 000 đồng trở lên", "5 500 đồng"]])
    sc_hook = sc("hook", "hook", "Chuyển đúng mười triệu, phí tính sai bậc", [
        st("<p><b>Biểu phí chuyển khoản</b> (số minh hoạ, không phải biểu phí của ngân hàng nào):</p>" + bieu_phi,
           """Đây là một biểu phí chuyển khoản ba bậc, số liệu chỉ để minh hoạ. Dưới năm trăm nghìn thì miễn phí.
           Từ năm trăm nghìn đến dưới mười triệu thì phí hai nghìn hai trăm đồng. Từ mười triệu trở lên thì phí năm nghìn năm trăm đồng.""",
           focus=[2, "2.2", "2.3", "2.4"]),
        st(out_block(phi_sai, "Một chương trình tính phí cho đúng 10 000 000 đồng in ra")
           + '<div class="box key">Hôm nay: dạy máy <b>chọn</b> việc để làm theo điều kiện, và kiểm thử ở đúng <b>biên</b> của mỗi bậc.</div>',
           """Một chương trình tính phí cho đúng mười triệu đồng lại ra hai nghìn hai trăm, tức là bậc giữa. Sai ở một ký tự duy nhất.
           Hôm nay ta học cách dạy máy chọn việc để làm theo điều kiện, và cách kiểm thử ở đúng biên của mỗi bậc.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại phép so sánh và phép logic từ bài trước", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① so sánh", "<code>&lt;</code> <code>&lt;=</code> <code>&gt;</code> <code>&gt;=</code> <code>==</code> <code>!=</code> cho kết quả đúng hoặc sai"],
                  ["② <code>&amp;&amp;</code>, <code>||</code>", "và, hoặc; dừng sớm khi đã biết kết quả"],
                  ["③ kiểu đúng sai", "<code>boolean</code>: biến chỉ giữ đúng hoặc sai"],
                  ["④ chương trình", "đến giờ mọi lệnh đều chạy, lần lượt từ trên xuống"]]),
           """Ta ôn lại từ bài trước. Phép so sánh như nhỏ hơn, lớn hơn hoặc bằng, cho kết quả đúng hoặc sai.
           Phép và, phép hoặc ghép các điều kiện, và dừng sớm khi đã biết kết quả. Kiểu đúng sai giữ đúng một trong hai giá trị đó.
           Và đến giờ, mọi lệnh đều chạy lần lượt từ trên xuống. Hôm nay ta cho máy bỏ qua một số lệnh.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã lệnh rẽ nhánh", [
        st(table(["viết", "nghĩa"],
                 [["<code>if (đk) { … }</code>", "<b>nếu</b> điều kiện đúng thì làm khối trong ngoặc nhọn"],
                  ["<code>else if (đk2) { … }</code>", "<b>nếu không, mà</b> điều kiện hai đúng thì làm khối này"],
                  ["<code>else { … }</code>", "<b>nếu không</b> (mọi điều kiện trên đều sai) thì làm khối này"],
                  ["<code>switch (x) { case A -&gt; …; default -&gt; …; }</code>", "<b>chọn theo trường hợp</b>: x bằng A thì làm việc sau mũi tên; <code>default</code>: không trường hợp nào khớp thì làm việc này"],
                  ["<code>đk ? a : b</code>", "<b>ba ngôi</b> (ba phần: điều kiện, a, b): điều kiện đúng thì lấy a, sai thì lấy b"]])
           + "<span class='note'>đk = điều kiện: một biểu thức cho kết quả đúng hoặc sai.</span>",
           """Bảng này là năm cách viết của hôm nay. Lệnh rẽ nhánh nếu: điều kiện trong ngoặc tròn đúng thì làm khối trong ngoặc nhọn.
           Nhánh nếu không, mà, thêm một điều kiện nữa. Nhánh nếu không cuối cùng nhận mọi trường hợp còn lại.
           Lệnh chọn theo trường hợp so một giá trị với từng trường hợp, và nhánh mặc định nhận mọi giá trị không khớp trường hợp nào.
           Toán tử ba ngôi, gọi vậy vì có ba phần là điều kiện và hai giá trị, chọn một trong hai giá trị đó.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6"]),
        st(code_block(rut, lines=(3, 10)) + out_block(rut),
           """Ví dụ rút tiền. Số dư ba trăm nghìn, muốn rút năm trăm nghìn. Điều kiện số tiền nhỏ hơn hoặc bằng số dư là sai,
           nên máy bỏ qua khối đầu và làm khối nếu không, in ra không đủ tiền. Chỉ một trong hai khối được chạy."""),
        st(code_block(kenh, lines=(3, 8)) + out_block(kenh),
           """Lệnh chọn theo trường hợp, dạng mũi tên, có từ Java mười bốn. Kênh là ứng dụng, trùng trường hợp thứ hai, nên in chuyển khoản trực tuyến.
           Một trường hợp có thể gom nhiều giá trị, cách nhau dấu phẩy. Dạng mũi tên chỉ chạy đúng một trường hợp rồi thoát."""),
        st(code_block(vip, lines=(3, 5)) + out_block(vip),
           """Toán tử ba ngôi gọn hơn khi chỉ cần chọn một giá trị. Khách là khách ưu tiên, điều kiện đúng, nên phí lấy giá trị đứng trước dấu hai chấm, là không."""),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: ngã ba trên đường, mỗi lần chỉ đi một ngả", [
        st(svg(1500, 470,
               '<polygon points="40,170 260,80 480,170 260,260" fill="#dbeafe" stroke="#2a78d6" stroke-width="3"/>',
               txt(260, 165, "soTien &lt; 500 000 ?", 22, "middle", "#1f2937", True),
               txt(260, 195, "điều kiện 1", 20, "middle", "#1f2937"),
               arrow(482, 170, 588, 170, "#dc2626", "sai"),
               '<polygon points="590,170 820,80 1050,170 820,260" fill="#dbeafe" stroke="#2a78d6" stroke-width="3"/>',
               txt(820, 165, "soTien &lt; 10 000 000 ?", 22, "middle", "#1f2937", True),
               txt(820, 195, "điều kiện 2", 20, "middle", "#1f2937"),
               arrow(1052, 170, 1158, 170, "#dc2626", "sai"),
               box(1160, 120, 300, 100, ["phí 5 500", "bậc 3"], C_RED, bold=True),
               arrow(260, 262, 260, 335, "#16a34a"), txt(275, 305, "đúng", 22, "start", "#16a34a", True),
               box(110, 340, 300, 90, ["phí 0", "bậc 1"], C_GREEN, bold=True),
               arrow(820, 262, 820, 335, "#16a34a"), txt(835, 305, "đúng", 22, "start", "#16a34a", True),
               box(670, 340, 300, 90, ["phí 2 200", "bậc 2"], C_AMBER, bold=True),
               txt(1310, 300, "xét từ trái sang phải;", 22, "middle", "#1f2937"),
               txt(1310, 330, "gặp điều kiện đúng đầu tiên", 22, "middle", "#1f2937"),
               txt(1310, 360, "thì đi ngả đó và DỪNG", 22, "middle", "#1f2937", True)),
           """Hãy hình dung chuỗi nếu, nếu không như những ngã ba nối tiếp nhau. Ở mỗi ngã ba, máy hỏi một điều kiện.
           Đúng thì rẽ xuống làm việc của bậc đó, rồi ra khỏi cả chuỗi. Sai thì đi tiếp tới ngã ba sau.
           Nếu mọi điều kiện đều sai, máy đi tới cuối đường, là nhánh nếu không cuối cùng. Mỗi số tiền chỉ đi đúng một ngả."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: từ câu chữ của biểu phí tới điều kiện", [
        st("""<p><b>Bước 1.</b> Đổi từng chữ của quy định thành một dấu so sánh:</p>"""
           + table(["câu chữ", "dấu", "biên có thuộc bậc không"],
                   [["“dưới 500 000”", "<code>soTien &lt; 500000</code>", "không: 500 000 thuộc bậc sau"],
                    ["“từ 10 000 000 trở lên”", "<code>soTien &gt;= 10000000</code>", "có: 10 000 000 thuộc bậc này"]]),
           """Bước một, đổi chữ thành dấu. Chữ dưới năm trăm nghìn nghĩa là nhỏ hơn hẳn, nên đúng năm trăm nghìn không thuộc bậc một.
           Chữ từ mười triệu trở lên nghĩa là lớn hơn hoặc bằng, nên đúng mười triệu thuộc bậc ba.""",
           focus=[1, "2.2", "2.3"]),
        st("""<p><b>Bước 2.</b> Bậc giữa có hai đầu, nên là <b>điều kiện ghép</b> bằng phép và:</p>
$$500\\,000 \\le \\text{soTien} \\;\\text{ và }\\; \\text{soTien} < 10\\,000\\,000$$""",
           """Bước hai, bậc giữa có hai đầu. Số tiền phải lớn hơn hoặc bằng năm trăm nghìn, và đồng thời nhỏ hơn mười triệu.
           Vì cần cả hai cùng đúng nên ta ghép bằng phép và của bài trước."""),
        st("""<p><b>Bước 3.</b> Trong chuỗi <code>if … else if</code>, tới được nhánh hai nghĩa là điều kiện một đã <b>sai</b>, tức là đã biết soTien ≥ 500 000. Nên chỉ cần viết nửa còn lại:</p>"""
           + code_block(p2, lines=(5, 8)),
           """Bước ba, rút gọn nhờ thứ tự. Máy chỉ tới nhánh hai khi điều kiện một đã sai, nghĩa là số tiền đã lớn hơn hoặc bằng năm trăm nghìn.
           Vì vậy nhánh hai chỉ cần viết nửa còn lại, nhỏ hơn mười triệu."""),
        st("""<p><b>Bước 4.</b> Nhánh <code>else</code> nhận mọi số còn lại, tức là soTien ≥ 10 000 000, đúng bậc ba. Ba nhánh phủ <b>mọi</b> số tiền, không chồng lên nhau.</p>"""
           + code_block(p2, lines=(9, 11)),
           """Bước bốn, nhánh nếu không cuối cùng nhận mọi số còn lại. Hai điều kiện trên đều sai nghĩa là số tiền từ mười triệu trở lên, đúng bậc ba.
           Như vậy ba nhánh phủ mọi số tiền, và không có số nào rơi vào hai bậc."""),
    ], checks=["(500000 < 500000) == False", "(10000000 > 10000000) == False and 10000000 >= 10**7", "499999 < 500000",
               "all((x < 500000) + (500000 <= x < 10000000) + (x >= 10000000) == 1 for x in [0, 499999, 500000, 9999999, 10000000, 10**12])"])
    sc_ex = sc("example", "example", "Ví dụ: thử ba số tiền nằm đúng ở biên", [
        st(code_block(p2, lines=(3, 12), title="Tệp Phi.java (dòng đầu đổi số tiền để thử)"),
           """Đây là chương trình tính phí đầy đủ. Ta thử ba số tiền nằm đúng ở biên, bằng cách đổi số ở dòng đầu rồi chạy lại. Có năm phép so sánh, ta đi từng phép."""),
        st("<p><b>Thử 499 999 đồng.</b></p>$$① \\; 499\\,999 < 500\\,000 \\;\\to\\; \\text{đúng} \\;\\to\\; \\hl{\\text{phí } 0}$$" + out_block(p1),
           """Thử bốn trăm chín mươi chín nghìn chín trăm chín mươi chín đồng. Phép so sánh thứ nhất, số này nhỏ hơn năm trăm nghìn, đúng.
           Máy làm khối bậc một, phí bằng không, và bỏ qua mọi nhánh sau."""),
        st("<p><b>Thử 500 000 đồng.</b></p>$$② \\; 500\\,000 < 500\\,000 \\;\\to\\; \\text{sai} \\qquad ③ \\; 500\\,000 < 10\\,000\\,000 \\;\\to\\; \\text{đúng} \\;\\to\\; \\hl{\\text{phí } 2\\,200}$$"
           + out_block(p2),
           """Thử đúng năm trăm nghìn. Phép so sánh thứ hai, năm trăm nghìn nhỏ hơn năm trăm nghìn là sai, vì hai số bằng nhau.
           Vì vậy máy chưa dừng mà đi tiếp xuống dưới. Phép so sánh thứ ba, năm trăm nghìn nhỏ hơn mười triệu là đúng, nên phí là hai nghìn hai trăm.""", clear=True),
        st("<p><b>Thử 10 000 000 đồng.</b></p>$$④ \\; 10^{7} < 500\\,000 \\;\\to\\; \\text{sai} \\qquad ⑤ \\; 10^{7} < 10^{7} \\;\\to\\; \\text{sai} \\;\\to\\; \\texttt{else} \\;\\to\\; \\hl{\\text{phí } 5\\,500}$$"
           + out_block(p3),
           """Thử đúng mười triệu. Phép so sánh thứ tư, mười triệu nhỏ hơn năm trăm nghìn là sai. Phép so sánh thứ năm, mười triệu nhỏ hơn mười triệu cũng sai.
           Hai điều kiện đều sai nên máy làm nhánh nếu không cuối cùng, phí năm nghìn năm trăm.""", clear=True),
        st(table(["số tiền", "bậc theo biểu phí", "chương trình in"],
                 [["499 999", "dưới 500 000 → 0", "0 ✓"], ["500 000", "từ 500 000 → 2 200", "2 200 ✓"],
                  ["10 000 000", "từ 10 000 000 → 5 500", "5 500 ✓"]]),
           """Đặt cạnh biểu phí, cả ba số ở biên đều ra đúng bậc. Đây là lý do ta thử ở biên, vì lỗi dấu hay nằm đúng ở đó.""", clear=True),
    ], checks=["499999 < 500000", "(500000 < 500000) == False", "500000 < 10000000",
               "(10**7 < 500000) == False", "(10**7 < 10**7) == False"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: ba điều kiện độc lập, đúng một cái đúng", [
        st(code_block(kiem, lines=(3, 6)) + out_block(kiem),
           """Đường kiểm khác không dựa vào thứ tự nhánh. Ta viết đủ điều kiện của từng bậc, mỗi bậc một phép so sánh riêng, theo đúng câu chữ của biểu phí.
           Với năm trăm nghìn, chỉ điều kiện bậc hai đúng, nên kết quả khớp với chương trình chính."""),
        st(table(["số tiền", "bậc 1: &lt; 500 000", "bậc 2: ≥ 500 000 và &lt; 10 000 000", "bậc 3: ≥ 10 000 000"],
                 [["499 999", "<b>đúng</b>", "sai", "sai"], ["500 000", "sai", "<b>đúng</b>", "sai"],
                  ["10 000 000", "sai", "sai", "<b>đúng</b>"]]),
           """Làm tương tự cho cả ba số, mỗi hàng có đúng một ô đúng, và ô đó trùng với bậc chương trình đã chọn.
           Nếu một hàng có hai ô đúng hoặc không ô nào đúng, nghĩa là quy định hoặc mã có lỗ hổng ở biên.""", clear=True),
    ], checks=["[x < 500000 for x in (499999, 500000, 10**7)] == [True, False, False]",
               "[500000 <= x < 10**7 for x in (499999, 500000, 10**7)] == [False, True, False]",
               "[x >= 10**7 for x in (499999, 500000, 10**7)] == [False, False, True]"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Viết một dấu bằng trong điều kiện.</div>'
           + code_block(gan_nham, lines=(4, 4)) + out_block(gan_nham, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là viết một dấu bằng trong điều kiện. Một dấu bằng là phép gán, kết quả là một số nguyên, không phải đúng sai.
           Trình biên dịch báo không đổi được số nguyên thành kiểu đúng sai. Muốn so sánh phải viết hai dấu bằng."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Bỏ ngoặc nhọn rồi thêm lệnh thứ hai.</div>'
           + code_block(thieu_ngoac, lines=(3, 8)) + out_block(thieu_ngoac),
           """Lỗi thứ hai là bỏ ngoặc nhọn. Không có ngoặc nhọn thì nhánh nếu chỉ gồm đúng một lệnh ngay sau nó.
           Lệnh trừ tiền thụt lề trông như nằm trong nhánh, nhưng thật ra luôn chạy. Kết quả là không có dòng đồng ý rút, mà số dư vẫn bị trừ thành âm bốn trăm nghìn.
           Thói quen tốt là luôn viết ngoặc nhọn, kể cả khi chỉ có một lệnh."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Dùng <code>&gt;</code> khi quy định ghi “từ … trở lên”.</div>'
           + code_block(phi_sai, lines=(3, 11)) + out_block(phi_sai),
           """Lỗi thứ ba hay gặp ở người đã đi làm, là chọn sai dấu ở biên. Biểu phí ghi từ mười triệu trở lên, nhưng mã viết lớn hơn hẳn.
           Đúng mười triệu bị tính phí bậc hai. Nhánh thứ hai cũng sai biên, đúng năm trăm nghìn ra miễn phí.
           Thử với số ở giữa khoảng thì không thấy lỗi, nên luôn thử đúng các số ở biên."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(3, 13), title="Đoán hai dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Điểm tín dụng là tám mươi lăm, đây là số minh hoạ. Chuỗi rẽ nhánh xếp hạng bạc, vàng hoặc thường.
           Dòng in cuối dùng toán tử ba ngôi. Hãy dừng video, viết ra hai dòng in ra, và tìm chỗ sai của chuỗi rẽ nhánh.""", pause=20),
        st("""<p>Xét từ trên xuống: $85 \\ge 50$ <b>đúng</b> ngay ở nhánh đầu, nên <code>hang</code> là Bac và máy <b>không xét tiếp</b> nhánh $85 \\ge 80$.</p>
<p>Dòng cuối: $85 \\ge 80$ đúng nên lấy giá trị trước dấu hai chấm.</p>""",
           """Đáp án như sau. Máy xét từ trên xuống, tám mươi lăm lớn hơn hoặc bằng năm mươi là đúng ngay ở nhánh đầu, nên hạng là bạc.
           Nhánh hạng vàng không bao giờ được xét, dù điều kiện của nó cũng đúng. Dòng cuối, tám mươi lăm lớn hơn hoặc bằng tám mươi là đúng, nên in ưu tiên."""),
        st(out_block(quiz) + '<div class="box key">Sửa: xếp điều kiện <b>chặt nhất lên trước</b>: <code>diem &gt;= 80</code> rồi mới tới <code>diem &gt;= 50</code>.</div>',
           """Chạy thật, hai dòng in ra là bạc và ưu tiên. Cách sửa là đặt điều kiện chặt nhất lên trước, xét lớn hơn hoặc bằng tám mươi rồi mới tới năm mươi.""",
           focus=[2, 3]),
    ], checks=["85 >= 50", "85 >= 80", "('Bac' if 85 >= 50 else 'Vang' if 85 >= 80 else 'Thuong') == 'Bac'"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("điều kiện cho đúng hoặc sai", "xét từ trên xuống", "nhánh đúng đầu tiên chạy, rồi thoát",
                 "nếu không cuối cùng nhận phần còn lại", "thử đúng ở biên"),
           """Tổng kết chuỗi logic. Mỗi điều kiện cho đúng hoặc sai. Máy xét từ trên xuống, nhánh đúng đầu tiên được chạy rồi thoát cả chuỗi.
           Nhánh nếu không cuối cùng nhận mọi trường hợp còn lại. Và luôn thử với các số nằm đúng ở biên."""),
        st("""<div class='box key'><b>Tư duy:</b> mỗi chữ “dưới”, “từ”, “trên”, “không quá” trong quy định là một dấu so sánh;
viết ra từng biên và thử đúng số ở biên. Luôn viết ngoặc nhọn.</div>""",
           """Điều cần mang theo. Mỗi chữ dưới, từ, trên, không quá trong quy định là một dấu so sánh. Hãy viết ra từng biên, thử đúng số ở biên,
           và luôn viết ngoặc nhọn."""),
    ])
    return lesson("L03", "re_nhanh", "Bài 3 — Rẽ nhánh: nếu, nếu không, và chọn theo trường hợp",
                  "curriculum/jva.yaml L03; audit/jva/verify_jva.py L03 (javac/java chạy thật); The Java Language Specification, "
                  "Java SE 21: §14.9 (lệnh if, if-else), §14.11 (switch, nhãn mũi tên không rơi xuống nhánh sau), §15.25 (toán tử ?:), "
                  "§15.26 (phép gán cho giá trị cùng kiểu với biến, nên if (x = 5) với int không biên dịch), §16 (gán chắc chắn trước khi dùng); "
                  "JEP 361 (switch dạng mũi tên chuẩn từ Java 14); dev.java/learn",
                  ["Viết chuỗi nếu, nếu không, mà, nếu không và đoán đúng nhánh nào chạy",
                   "Đổi câu chữ của quy định thành dấu so sánh đúng ở biên, kể cả điều kiện ghép",
                   "Dùng lệnh chọn theo trường hợp dạng mũi tên và toán tử ba ngôi",
                   "Kiểm thử ở biên và nhận ra ba lỗi: một dấu bằng, thiếu ngoặc nhọn, sai dấu biên"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
