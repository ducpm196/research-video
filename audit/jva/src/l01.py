from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    tran_luong = prog("TranLuong", """
public class TranLuong {
    public static void main(String[] args) {
        int dot = 900000000;            // một đợt lương: 900 triệu đồng (số minh hoạ)
        int tong = dot + dot + dot;     // ba đợt, cất trong kiểu int
        System.out.println("Tong luong: " + tong);
    }
}""", out="Tong luong: -1594967296")
    bien = prog("Bien", """
public class Bien {
    public static void main(String[] args) {
        long soDu = 100000;                 // tạo ngăn tên soDu, đặt vào 100000
        System.out.println("So du: " + soDu);
        soDu = soDu + 50000;                // nạp thêm 50000: tính vế phải, ghi đè
        System.out.println("So du: " + soDu);
    }
}""", out="So du: 100000\nSo du: 150000")
    kieu = prog("Kieu", """
public class Kieu {
    public static void main(String[] args) {
        int soLenh = 3;                     // số nguyên
        long soDu = 5000000000L;            // số nguyên lớn, chữ L ở cuối
        double laiSuat = 0.055;             // số thực (số minh hoạ)
        boolean daKhoa = false;             // chỉ đúng hoặc sai
        char hang = 'A';                    // một ký tự, nháy đơn
        String ten = "Nguyen Van An";       // chuỗi chữ, nháy kép
        System.out.println(ten + ", hang " + hang);
        System.out.println("So du: " + soDu + ", so lenh: " + soLenh);
        System.out.println("Lai: " + laiSuat + ", khoa: " + daKhoa);
    }
}""", out="Nguyen Van An, hang A\nSo du: 5000000000, so lenh: 3\nLai: 0.055, khoa: false")
    tran = prog("Tran", """
public class Tran {
    public static void main(String[] args) {
        int lonNhat = Integer.MAX_VALUE;   // có sẵn: số lớn nhất của int
        int nhoNhat = Integer.MIN_VALUE;   // có sẵn: số nhỏ nhất của int
        System.out.println(lonNhat);
        System.out.println(nhoNhat);
        System.out.println(lonNhat + 1);   // vượt số lớn nhất một đơn vị
    }
}""", out="2147483647\n-2147483648\n-2147483648")
    luong = prog("Luong", """
public class Luong {
    public static void main(String[] args) {
        long dot = 900000000L;          // (1) một đợt lương (số minh hoạ)
        long tong = dot + dot;          // (2) hai đợt
        tong = tong + dot;              // (3) thêm đợt thứ ba
        long phi = 3 * 5500L;           // (4) phí ba lần chuyển (số minh hoạ)
        long tongTru = tong + phi;      // (5) tổng bị trừ khỏi tài khoản
        System.out.println("Tong luong: " + tong);
        System.out.println("Phi: " + phi);
        System.out.println("Tong tru: " + tongTru);
    }
}""", out="Tong luong: 2700000000\nPhi: 16500\nTong tru: 2700016500")
    gan_sai = prog("GanSai", """
public class GanSai {
    public static void main(String[] args) {
        int soDu = "100000";            // chuỗi chữ, không phải số
        System.out.println(soDu);
    }
}""", expect="compile_error:incompatible types: String cannot be converted to int")
    tien_thuc = prog("TienThuc", """
public class TienThuc {
    public static void main(String[] args) {
        double a = 0.1;                 // 0,1 nghìn đồng = 100 đồng
        double b = 0.2;                 // 0,2 nghìn đồng = 200 đồng
        System.out.println(a + b);      // mong 0.3
        long x = 100;                   // cách đúng: tính theo đồng
        long y = 200;
        System.out.println(x + y);
    }
}""", out="0.30000000000000004\n300")
    thap_phan = prog("ThapPhan", """
import java.math.BigDecimal;

public class ThapPhan {
    public static void main(String[] args) {
        BigDecimal a = new BigDecimal("0.1");   // tạo từ chuỗi "0.1"
        BigDecimal b = new BigDecimal("0.2");
        System.out.println(a.add(b));           // cộng chính xác
    }
}""", out="0.3")
    quiz = prog("Doan", """
public class Doan {
    public static void main(String[] args) {
        int x = 5;
        int y = x;
        x = x + 10;
        System.out.println("x = " + x);
        System.out.println("y = " + y);
        System.out.println(x + y + " dong");
    }
}""", out="x = 15\ny = 5\n20 dong")

    quy_mo = prog("QuyMo", """
public class QuyMo {
    public static void main(String[] args) {
        int moiLenh = 1000000;              // một triệu đồng mỗi lệnh (số minh hoạ)
        int lo1 = 100;                      // lô 100 lệnh
        int lo2 = 2147;
        int lo3 = 2148;
        int lo4 = 10000;
        System.out.println(moiLenh * lo1);
        System.out.println(moiLenh * lo2);
        System.out.println(moiLenh * lo3);
        System.out.println(moiLenh * lo4);
    }
}""", out="100000000\n2147000000\n-2146967296\n1410065408")
    so_du = prog("SoDu", """
public class SoDu {
    public static void main(String[] args) {
        long soDu = 1500000;                        // số dư đầu (số minh hoạ)
        long chuyen = 250000;                       // mỗi lệnh chuyển
        long phi = 2200;                            // phí mỗi lệnh (số minh hoạ)
        long tongChuyen = 3 * chuyen;
        long tongPhi = 3 * phi;
        soDu = soDu - tongChuyen - tongPhi;         // tính vế phải rồi ghi đè
        System.out.println("Tong chuyen: " + tongChuyen);
        System.out.println("Tong phi: " + tongPhi);
        System.out.println("So du con lai: " + soDu);
        int dot = 800000000;
        int sai = dot + dot + dot;                  // cất trong int
        long dot2 = 800000000L;
        long dung = dot2 + dot2 + dot2;             // cất trong long
        System.out.println("Int: " + sai);
        System.out.println("Long: " + dung);
    }
}""", out="Tong chuyen: 750000\nTong phi: 6600\nSo du con lai: 743400\nInt: -1894967296\nLong: 2400000000")
    write_lab("JVA", "L01", """# Lab JVA L01 — Số dư sau ba lệnh chuyển

Trong Git Bash, đứng trong thư mục làm việc của bạn. Viết chương trình `SoDu` (tệp `SoDu.java`), số liệu là số minh hoạ:

1. Dùng ba biến `long`: số dư đầu **1 500 000**, mỗi lệnh chuyển **250 000**, phí mỗi lệnh **2 200**. Tính `tongChuyen` và `tongPhi` cho **ba lệnh**, rồi **gán lại** `soDu = soDu - tongChuyen - tongPhi`. In ba dòng: `Tong chuyen: …`, `Tong phi: …`, `So du con lai: …`.
2. Cộng ba lần **800 000 000** hai cách: bằng biến `int` (in `Int: …`) và bằng biến `long` (in `Long: …`). Đoán trước kết quả `int`, rồi kiểm bằng `jshell`: gõ `800000000 + 800000000 + 800000000`.

Chạy: `javac SoDu.java && java SoDu`. Chấm: `bash labs/cham.sh JVA L01 SoDu.java`.
""", "java", so_du["code"], so_du["out"])
    sc_lab = practice_scene(sc, "Tự làm: số dư sau ba lệnh chuyển", practice_steps(
        st, "JVA", "L01",
        """<p><b>Đề</b>: viết <code>SoDu.java</code>, số liệu là số minh hoạ.</p>
<ol><li>Ba biến <code>long</code>: số dư đầu 1 500 000; mỗi lệnh chuyển 250 000; phí mỗi lệnh 2 200. Tính tổng chuyển và tổng phí cho <b>3 lệnh</b>, gán lại <code>soDu</code>, in ba dòng</li>
<li>Cộng ba lần 800 000 000 bằng <code>int</code> (in <code>Int: …</code>) và bằng <code>long</code> (in <code>Long: …</code>)</li></ol>
<p class="note">Đoán kết quả <code>int</code> trước, rồi kiểm bằng <code>jshell</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Viết chương trình với ba biến số nguyên dài: số dư đầu một triệu rưỡi, mỗi lệnh chuyển hai trăm năm mươi nghìn, phí mỗi lệnh hai nghìn hai trăm.
        Tính tổng chuyển và tổng phí cho ba lệnh, gán lại số dư, rồi in ba dòng. Sau đó cộng ba lần tám trăm triệu hai cách, bằng kiểu số nguyên và bằng kiểu số nguyên dài, và in cả hai.
        Hãy đoán trước kết quả kiểu số nguyên, kiểm bằng công cụ gõ từng dòng, rồi dừng video và tự viết, đừng chép lại ví dụ.""",
        so_du["out"], "SoDu.java",
        """<div class="box key"><b>Nếu kẹt:</b> <code>long tongChuyen = 3 * chuyen;</code>, rồi <code>soDu = soDu - tongChuyen - tongPhi;</code>. Với phần hai, nhớ viết chữ <code>L</code> sau số khi cất vào <code>long</code>.
Lời giải nằm ở <code>labs/JVA/L01/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, tính tổng chuyển bằng ba nhân với số tiền một lệnh, rồi gán lại số dư bằng số dư trừ tổng chuyển trừ tổng phí. Với phần hai, nhớ viết chữ L sau số khi cất vào kiểu số nguyên dài.
        Lời giải nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=60), "JVA", "L01")

    sc_hook = sc("hook", "hook", "Ba đợt lương chín trăm triệu, vì sao tổng lại âm?", [
        st(out_block(tran_luong, "Một chương trình cộng ba đợt lương, mỗi đợt 900 triệu đồng, in ra"),
           """Một chương trình cộng ba đợt lương, mỗi đợt chín trăm triệu đồng. Tổng đúng phải là hai tỉ bảy trăm triệu.
           Thế mà máy in ra một số âm, và không hề báo lỗi."""),
        st("""<p>Lỗi không nằm ở phép cộng, mà ở <b>cái ngăn</b> dùng để cất con số.</p>
<div class="box key">Hôm nay: <b>biến</b> là ngăn nhớ có tên, <b>kiểu</b> quyết định ngăn to bao nhiêu và chứa được gì.</div>""",
           """Lỗi không nằm ở phép cộng, mà ở cái ngăn dùng để cất con số. Hôm nay ta học biến, tức là ngăn nhớ có tên,
           và kiểu, thứ quyết định ngăn to bao nhiêu và chứa được gì."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại điều đã biết từ bài trước", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① chương trình", "máy làm từng lệnh trong hàm chính, từ trên xuống"],
                  ["② lệnh in", "<code>System.out.println(…)</code> in giá trị trong ngoặc rồi xuống dòng"],
                  ["③ dấu <code>+</code>", "hai số thì cộng; có một vế là chuỗi thì nối chữ, làm từ trái sang phải"],
                  ["④ bộ nhớ", "chỗ giữ dữ liệu khi chương trình đang chạy, như tờ giấy nháp"]]),
           """Ta ôn lại bốn điều từ bài trước. Máy làm từng lệnh trong hàm chính, từ trên xuống. Lệnh in in giá trị trong ngoặc.
           Dấu cộng có một vế là chuỗi thì thành nối chữ. Còn bộ nhớ giữ dữ liệu khi chương trình chạy, như tờ giấy nháp.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
        st("""<p>Câu hỏi hôm nay: muốn <b>nhớ</b> một con số để dùng lại ở lệnh sau, ta ghi nó vào đâu trên tờ giấy nháp ấy?</p>""",
           """Câu hỏi hôm nay là, muốn nhớ một con số để dùng lại ở lệnh sau, ta ghi nó vào đâu trên tờ giấy nháp ấy."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã một dòng khai báo biến", [
        st(code_block(bien, title="Tệp Bien.java"),
           """Đây là chương trình có một biến tên số dư. Dòng thứ ba tạo biến, dòng thứ năm cộng thêm năm mươi nghìn. Ta đọc kỹ dòng tạo biến trước."""),
        st(table(["viết", "nghĩa"],
                 [["<code>long</code>", "<b>kiểu</b>: ngăn này chứa số nguyên (loại ngăn to)"],
                  ["<code>soDu</code>", "<b>tên</b> biến; theo quy ước (không bắt buộc): chữ đầu viết thường, mỗi từ sau viết hoa chữ đầu"],
                  ["<code>=</code>", "<b>gán</b>: tính vế phải, rồi đặt kết quả vào ngăn bên trái (không phải “bằng” của toán)"],
                  ["<code>100000</code>", "giá trị đặt vào lúc tạo"],
                  ["<code>;</code>", "hết một lệnh, như ở bài trước"]]),
           """Chữ đầu là kiểu, ở đây là kiểu số nguyên dài, nghĩa là ngăn chỉ chứa số nguyên. Tiếp theo là tên biến, theo quy ước thì chữ đầu viết thường.
           Dấu bằng là phép gán, không phải dấu bằng của toán, vì máy tính vế phải trước rồi đặt kết quả vào ngăn bên trái.
           Sau đó là giá trị lúc tạo, và dấu chấm phẩy.""", clear=True, focus=["1.2", "1.3", "1.4", ["1.5", "1.6"]]),
        st(code_block(bien, lines=(5, 6)) + out_block(bien),
           """Vì vậy dòng số dư bằng số dư cộng năm mươi nghìn không phải phương trình vô lý. Máy đọc giá trị cũ, cộng thêm,
           rồi ghi đè vào chính ngăn đó, nên lệnh in thứ hai in ra số mới."""),
        st(table(["kiểu", "chứa gì", "ví dụ giá trị", "cỡ"],
                 [["<code>int</code>", "số nguyên", "<code>3</code>, <code>-15</code>", "4 byte"],
                  ["<code>long</code>", "số nguyên lớn (giá trị lớn viết thêm chữ <code>L</code>)", "<code>5000000000L</code>", "8 byte"],
                  ["<code>double</code>", "số thực, có phần lẻ", "<code>0.055</code>", "8 byte"],
                  ["<code>boolean</code>", "đúng hoặc sai", "<code>true</code>, <code>false</code>", "—"],
                  ["<code>char</code>", "một ký tự, nháy đơn", "<code>'A'</code>", "2 byte"],
                  ["<code>String</code>", "chuỗi chữ, nháy kép", "<code>\"Nguyen Van An\"</code>", "tuỳ độ dài"]])
           + "<span class='note'>1 byte = 8 ô nhớ nhỏ, mỗi ô chỉ là 0 hoặc 1.</span>",
           """Đây là sáu kiểu dùng nhiều nhất. Kiểu số nguyên chiếm bốn bai, kiểu số nguyên dài chiếm tám bai, mà một bai là tám ô nhớ nhỏ, mỗi ô chỉ là không hoặc một.
           Kiểu số thực chứa số có phần lẻ, như lãi suất. Kiểu đúng sai chỉ có hai giá trị, đúng hoặc sai.
           Kiểu ký tự chứa một ký tự trong nháy đơn, còn kiểu chuỗi chứa cả dòng chữ trong nháy kép.""", clear=True,
           focus=[1, ["1.2", "1.3"], "1.4", "1.5", ["1.6", "1.7"]]),
        st(code_block(kieu, lines=(3, 11)) + out_block(kieu),
           """Đây là cả sáu kiểu trong một chương trình, ba lệnh in cuối dùng phép nối chữ để in mọi biến. Để ý số năm tỉ in ra không có chữ L,
           vì chữ L chỉ là ký hiệu trong mã nguồn, báo đây là số nguyên dài."""),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: biến là một ngăn có tên và có cỡ", [
        st(svg(1500, 400,
               box(40, 40, 320, 120, ["soLenh", "int, 4 byte", "3"], C_BLUE, bold=True),
               box(420, 40, 640, 120, ["soDu", "long, 8 byte", "100000"], C_GREEN, bold=True),
               txt(1270, 110, "ngăn to hơn, chứa số lớn hơn", 24, "middle", "#1f2937"),
               box(40, 250, 330, 110, ["① đọc soDu", "được 100000"], C_GRAY),
               arrow(375, 305, 470, 305, "#2a78d6"),
               box(480, 250, 400, 110, ["② tính vế phải", "100000 + 50000 = 150000"], C_AMBER),
               arrow(885, 305, 980, 305, "#2a78d6"),
               box(990, 250, 420, 110, ["③ ghi vào soDu", "giá trị cũ bị thay"], C_GREEN, bold=True),
               txt(750, 225, "soDu = soDu + 50000;", 26, "middle", "#1f2937", True)),
           """Hãy hình dung mỗi biến là một ngăn kéo dán nhãn tên. Ngăn kiểu số nguyên dài to gấp đôi ngăn kiểu số nguyên.
           Hàng dưới là phép gán theo ba nhịp: đọc giá trị đang có, tính vế phải, rồi ghi đè vào ngăn."""),
        st(svg(1500, 330,
               box(40, 60, 300, 100, ["-2 147 483 648", "nhỏ nhất"], C_BLUE, bold=True),
               box(380, 60, 220, 100, ["…", "số âm"], C_GRAY),
               box(640, 60, 220, 100, ["0"], C_GRAY, bold=True),
               box(900, 60, 220, 100, ["…", "số dương"], C_GRAY),
               box(1160, 60, 300, 100, ["2 147 483 647", "lớn nhất"], C_RED, bold=True),
               '<path d="M1310,165 L1310,250 L190,250 L190,175" fill="none" stroke="#dc2626" stroke-width="3.5" '
               'stroke-dasharray="8 6" marker-end="url(#ah)"/>',
               txt(750, 238, "cộng thêm 1 vào số lớn nhất: quay vòng về số nhỏ nhất, KHÔNG báo lỗi", 24, "middle", "#dc2626", True),
               txt(750, 305, "giống đồng hồ ki-lô-mét quay vòng, nhưng int quay về số âm nhỏ nhất", 24, "middle", "#1f2937")),
           """Ngăn kiểu số nguyên chỉ chứa các số từ khoảng âm hai tỉ một tới khoảng dương hai tỉ một.
           Cộng một vào số lớn nhất thì kết quả không vừa ngăn, nên quay vòng về số nhỏ nhất, và máy không báo gì.
           Giống đồng hồ ki-lô-mét của xe máy quay vòng khi tới năm chữ số chín, chỉ khác là ngăn kiểu số nguyên quay về số âm nhỏ nhất chứ không về không."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: vì sao số lớn nhất là 2 147 483 647", [
        st("""<p><b>Bước 1.</b> Mỗi byte có 8 ô, mỗi ô chỉ là 0 hoặc 1. Kiểu <code>int</code> có 4 byte:</p>
$$4 \\times 8 = \\hl{32} \\text{ ô}$$""",
           """Bước một, đếm số ô. Mỗi bai gồm tám ô, mỗi ô chỉ là không hoặc một, vì máy chỉ có hai con số đó.
           Kiểu số nguyên có bốn bai, nên có bốn nhân tám là ba mươi hai ô."""),
        st("""<p><b>Bước 2.</b> Mỗi ô thêm vào làm số cách xếp <b>gấp đôi</b>, nên 32 ô cho:</p>
$$2^{32} = \\hl{4\\,294\\,967\\,296} \\text{ giá trị khác nhau}$$""",
           """Bước hai, đếm số giá trị. Một ô có hai cách, hai ô có bốn cách, vì mỗi ô thêm vào làm số cách gấp đôi.
           Vậy ba mươi hai ô cho hai mũ ba mươi hai, hơn bốn tỉ hai trăm triệu giá trị."""),
        st("""<p><b>Bước 3.</b> Java chia đôi: một nửa cho số âm, nửa kia cho số 0 và số dương:</p>
$$2^{31} = 2\\,147\\,483\\,648 \\text{ số âm} \\qquad 2^{31} - 1 = \\hl{2\\,147\\,483\\,647} \\text{ là số dương lớn nhất}$$""",
           """Bước ba, chia đôi. Một nửa số giá trị dành cho số âm, nửa kia cho số không và các số dương.
           Nửa thứ hai phải nhường một chỗ cho số không, nên số dương lớn nhất là hai mũ ba mươi mốt trừ một."""),
        st("""<p><b>Bước 4.</b> Cộng 1 vào số lớn nhất: kết quả đúng là $2\\,147\\,483\\,648$, nằm ngoài miền của <code>int</code>. Java không báo lỗi mà <b>quay vòng</b>: trừ đi đúng một vòng $2^{32}$ giá trị.</p>
$$2\\,147\\,483\\,648 - 4\\,294\\,967\\,296 = \\hl{-2\\,147\\,483\\,648}$$"""
           + code_block(tran, lines=(3, 7)) + out_block(tran),
           """Bước bốn, vượt giới hạn. Java có sẵn hai giá trị giữ số lớn nhất và số nhỏ nhất của kiểu số nguyên, ta in chúng rồi cộng thêm một. Cộng một vào số lớn nhất thì kết quả đúng là hai tỉ một trăm bốn mươi bảy triệu bốn trăm tám mươi ba nghìn sáu trăm bốn mươi tám, nằm ngoài miền của kiểu số nguyên.
           Theo luật của Java, máy không báo lỗi mà quay vòng, nghĩa là trừ đi đúng hai mũ ba mươi hai, tức một vòng đủ mọi giá trị.
           Kết quả là âm hai tỉ một trăm bốn mươi bảy triệu bốn trăm tám mươi ba nghìn sáu trăm bốn mươi tám, đúng số nhỏ nhất của kiểu số nguyên.
           Chạy thật, dòng cuối đúng là số đó, và không có thông báo lỗi nào."""),
    ], checks=["4 * 8 == 32", "2**32 == 4294967296", "2**31 - 1 == 2147483647",
               "(2**31 - 1) + 1 == 2147483648", "2147483648 - 4294967296 == -2**31",
               "((2**31 - 1) + 1 + 2**31) % 2**32 - 2**31 == -2**31"])
    sc_ex = sc("example", "example", "Ví dụ: cộng ba đợt lương bằng kiểu số nguyên dài", [
        st(code_block(luong, title="Tệp Luong.java"),
           """Ta làm lại bài toán ba đợt lương bằng kiểu số nguyên dài, theo đơn vị đồng. Chương trình có năm phép tính đánh số, ta đi từng phép."""),
        st(code_block(luong, lines=(3, 4))
           + "<p>① một đợt lương; ② cộng hai đợt:</p>$$① \\; 900\\,000\\,000 \\qquad ② \\; 900\\,000\\,000 + 900\\,000\\,000 = \\hl{1\\,800\\,000\\,000}$$",
           """Phép tính thứ nhất đặt chín trăm triệu vào biến đợt, chữ L báo đây là số nguyên dài.
           Phép tính thứ hai cộng hai đợt, ra một tỉ tám trăm triệu, cất vào biến tổng."""),
        st(code_block(luong, lines=(5, 5))
           + "<p>③ vế phải dùng giá trị <b>cũ</b> của <code>tong</code>, rồi ghi đè:</p>$$③ \\; 1\\,800\\,000\\,000 + 900\\,000\\,000 = \\hl{2\\,700\\,000\\,000}$$",
           """Phép tính thứ ba là phép gán ta vừa học. Vế phải dùng giá trị cũ của tổng, cộng thêm một đợt, ra hai tỉ bảy trăm triệu rồi ghi đè.
           Số này vượt giới hạn của kiểu số nguyên, nhưng ngăn tám bai chứa thoải mái."""),
        st(code_block(luong, lines=(6, 7))
           + "<p>④ phí 5 500 đồng mỗi lần (số minh hoạ); ⑤ tổng bị trừ:</p>"
           "$$④ \\; 3 \\times 5\\,500 = \\hl{16\\,500} \\qquad ⑤ \\; 2\\,700\\,000\\,000 + 16\\,500 = \\hl{2\\,700\\,016\\,500}$$",
           """Phép tính thứ tư tính phí ba lần chuyển, mỗi lần năm nghìn năm trăm đồng, là số minh hoạ, ra mười sáu nghìn năm trăm.
           Phép tính thứ năm cộng phí vào tổng lương, ra hai tỉ bảy trăm triệu không trăm mười sáu nghìn năm trăm đồng."""),
        st(out_block(luong),
           """Chạy thật chương trình, ba dòng in ra đúng ba con số ta vừa tính tay."""),
    ], checks=["900000000 + 900000000 == 1800000000", "1800000000 + 900000000 == 2700000000",
               "3 * 5500 == 16500", "2700000000 + 16500 == 2700016500"])
    sc_jsh = sc("jshell", "example", "Ví dụ: thử từng dòng Java, tự đoán rồi kiểm", [
        st("""<p>JDK có sẵn công cụ gõ từng dòng, tên <code>jshell</code>: gõ một dòng Java, bấm xuống dòng, thấy giá trị ngay.</p>
<div class="code"><div>jshell&gt; int soLenh = 100</div><div>soLenh ==&gt; 100</div><div>jshell&gt; soLenh * 3</div><div>&#36;2 ==&gt; 300</div><div>jshell&gt; long lon = 3000000000L</div><div>lon ==&gt; 3000000000</div><div>jshell&gt; 1 + 2 + "A"</div><div>&#36;4 ==&gt; "3A"</div></div>
<span class='note'>Vào: gõ <code>jshell</code> trong Git Bash. Thoát: <code>/exit</code>. Dấu <code>==&gt;</code> đọc là “có giá trị”; <code>&#36;2</code> là tên máy tự đặt cho kết quả chưa có tên.</span>""",
           """Bây giờ ta có thêm một cách thử: công cụ gõ từng dòng, đi kèm bộ công cụ JDK. Bạn gõ một dòng Java rồi bấm phím xuống dòng, máy chạy ngay và in giá trị, không cần tạo tệp hay biên dịch riêng.
           Dấu mũi tên đôi đọc là có giá trị. Khi dòng gõ vào là một biểu thức chưa có tên, máy tự đặt cho kết quả một tên bắt đầu bằng dấu đô la.
           Ở đây, ba nhân với biến cho ba trăm, và một cộng hai rồi nối chữ A cho chuỗi ba A. Gõ lệnh thoát khi xong.""",
           focus=[1, "2.1", "2.2", "2.4", ["2.3", "2.4"], 3]),
        st(table(["gõ vào công cụ", "bạn đoán"],
                 [["<code>int s = 2000000000 + 2000000000</code>", "?"],
                  ["<code>long t = 2000000000L + 2000000000L</code>", "?"],
                  ["<code>0.1 + 0.2</code>", "?"]]),
           """Đây là cách học nhanh nhất: tự đoán rồi mới kiểm. Với mỗi dòng, hãy đoán máy in gì rồi mới gõ thử. Dòng một cộng hai lần hai tỉ trong kiểu số nguyên.
           Dòng hai làm đúng phép đó trong kiểu số nguyên dài. Dòng ba là không phẩy một cộng không phẩy hai. Hãy dừng video, đoán, rồi gõ thử trên máy.""",
           pause=20, clear=True, focus=[1, 1, "1.2", "1.3", "1.4", 1]),
        st(table(["gõ vào công cụ", "máy in", "vì sao"],
                 [["<code>int s = 2000000000 + 2000000000</code>", "<code>s ==&gt; -294967296</code>", "4 000 000 000 vượt <code>int</code>, bị trừ một vòng 4 294 967 296"],
                  ["<code>long t = 2000000000L + 2000000000L</code>", "<code>t ==&gt; 4000000000</code>", "<code>long</code> chứa thoải mái"],
                  ["<code>0.1 + 0.2</code>", "<code>0.30000000000000004</code>", "số thực lưu theo hệ hai, phải cắt bớt"]]),
           """Kết quả thật. Dòng một ra một số âm, vì bốn tỉ vượt giới hạn nên bị trừ đi một vòng hai mũ ba mươi hai. Dòng hai ra đúng bốn tỉ, vì ngăn kiểu số nguyên dài chứa thoải mái.
           Dòng ba ra số có đuôi lệch như ta đã thấy. Từ nay, mỗi khi nghi ngờ một dòng Java, hãy thử nó ở đây trước khi đưa vào chương trình.""",
           clear=True, focus=[1, "1.2", "1.3", "1.4", 1]),
    ], checks=["2000000000 + 2000000000 - 2**32 == -294967296", "2000000000 + 2000000000 == 4000000000",
               "0.1 + 0.2 == 0.30000000000000004", "2**32 == 4294967296", "4000000000 > 2**31 - 1"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: nhân thay cộng, đoán trước số âm", [
        st("""<p>Đường khác 1: ba đợt bằng nhau thì <b>nhân</b> thay vì cộng ba lần:</p>
$$3 \\times 900\\,000\\,000 = 2\\,700\\,000\\,000 \\; ✓$$""",
           """Đường kiểm thứ nhất, vì ba đợt bằng nhau nên ta nhân ba với chín trăm triệu thay vì cộng ba lần. Kết quả hai tỉ bảy trăm triệu, khớp với khi chạy."""),
        st("""<p>Đường khác 2: tổng vượt số lớn nhất của <code>int</code>, nên ở đầu bài máy đã <b>quay vòng</b>, tức là trừ đúng một vòng $2^{32}$:</p>
$$2\\,700\\,000\\,000 > 2\\,147\\,483\\,647 \\qquad 2\\,700\\,000\\,000 - 4\\,294\\,967\\,296 = \\hl{-1\\,594\\,967\\,296}$$"""
           + out_block(tran_luong, "Kết quả chạy ở đầu bài"),
           """Đường kiểm thứ hai giải thích số âm ở đầu bài. Hai tỉ bảy vượt số lớn nhất của kiểu số nguyên, nên bị quay vòng, nghĩa là trừ đi đúng hai mũ ba mươi hai.
           Phép trừ này cho đúng con số âm mà máy đã in, đến từng chữ số."""),
    ], checks=["3 * 900000000 == 2700000000", "2700000000 > 2147483647",
               "2700000000 - 2**32 == -1594967296", "(3 * 900000000 + 2**31) % 2**32 - 2**31 == -1594967296"])
    sc_scale = sc("quymo", "concept", "Khi lô lệnh lớn dần, kiểu int hỏng ở đâu?", [
        st(code_block(quy_mo, lines=(3, 11)),
           """Giả sử mỗi lệnh chuyển một triệu đồng, số minh hoạ, và ta lấy tổng của cả lô bằng phép nhân trong kiểu số nguyên. Ta thử bốn lô cỡ khác nhau.
           Một trăm lệnh, hai nghìn một trăm bốn mươi bảy lệnh, hai nghìn một trăm bốn mươi tám lệnh, và mười nghìn lệnh."""),
        st(table(["lô", "tổng đúng (đồng)", "máy in", "kết luận"],
                 [["100 lệnh", "100 000 000", "100000000", "đúng"],
                  ["2 147 lệnh", "2 147 000 000", "2147000000", "đúng, sát giới hạn 2 147 483 647"],
                  ["2 148 lệnh", "2 148 000 000", "-2146967296", "<b>sai</b>, ra số âm"],
                  ["10 000 lệnh", "10 000 000 000", "1410065408", "<b>sai nhưng dương</b>, trông hợp lý"]])
           + out_block(quy_mo),
           """Lô một trăm lệnh đúng, và lô hai nghìn một trăm bốn mươi bảy lệnh vẫn đúng, sát giới hạn. Thêm đúng một lệnh nữa, lô hai nghìn một trăm bốn mươi tám ra số âm.
           Nguy hiểm hơn, lô mười nghìn lệnh ra khoảng một tỉ bốn trăm triệu, một số dương trông hợp lý nhưng sai, vì mười tỉ bị trừ đi hai vòng.""",
           clear=True, focus=[["1.2", "1.3"], "1.4", "1.5"]),
        st("""<div class="box key"><b>Điều người làm nghề rút ra.</b> Thử bằng lô nhỏ (100 lệnh) <b>không bao giờ bắt được</b> lỗi này: nó chỉ lộ khi hệ thống lớn lên.
Việc cần làm: đoán trước giá trị lớn nhất, thử đúng <b>sát giới hạn</b> và vượt một đơn vị, và chọn <code>long</code> cho tiền: nó chứa tới 9 223 372 036 854 775 807, đủ cho hơn 9 nghìn tỉ lệnh một triệu đồng (số minh hoạ).</div>""",
           """Thử bằng lô nhỏ không bao giờ bắt được lỗi này, vì nó chỉ lộ khi hệ thống lớn lên. Người làm nghề đoán trước giá trị lớn nhất, và thử đúng sát giới hạn rồi vượt thêm một đơn vị.
           Họ chọn kiểu số nguyên dài cho tiền, vì nó chứa được hơn chín tỉ tỉ, đủ cho hơn chín nghìn tỉ lệnh một triệu đồng.""", clear=True),
    ], checks=["1000000 * 100 == 100000000", "1000000 * 2147 == 2147000000", "1000000 * 2147 <= 2**31 - 1",
               "1000000 * 2148 > 2**31 - 1", "((1000000 * 2148 + 2**31) % 2**32) - 2**31 == -2146967296",
               "((10**10 + 2**31) % 2**32) - 2**31 == 1410065408", "2**63 - 1 == 9223372036854775807",
               "(2**63 - 1) // 10**6 == 9223372036854"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Đặt một chuỗi chữ vào ngăn kiểu số.</div>'
           + code_block(gan_sai, lines=(3, 3)) + out_block(gan_sai, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là đặt một chuỗi trong nháy kép vào ngăn kiểu số nguyên. Nhìn giống số, nhưng nháy kép biến nó thành chữ.
           Trình biên dịch từ chối ngay, báo không đổi được chuỗi thành số nguyên."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Dùng <code>int</code> cho tổng tiền: tràn số mà không báo.</div>'
           + code_block(tran_luong, lines=(3, 5)) + out_block(tran_luong),
           """Lỗi thứ hai, gặp cả ở người đã đi làm, là dùng kiểu số nguyên cho tổng tiền. Từng khoản thì vừa, cộng lại thì vượt hai tỉ một.
           Chương trình chạy êm, chỉ có con số sai, nên rất khó phát hiện. Tổng tiền tính bằng đồng nên dùng kiểu số nguyên dài."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Dùng <code>double</code> cho tiền.</div>'
           + code_block(tien_thuc, lines=(3, 8)) + out_block(tien_thuc),
           """Lỗi thứ ba là dùng kiểu số thực cho tiền. Không phẩy một cộng không phẩy hai ra một số lệch ở chữ số thứ mười bảy sau dấu phẩy.
           Lý do là số thực lưu theo hệ hai, tức chỉ dùng hai chữ số không và một.
           Mà không phẩy một viết trong hệ hai là số lẻ vô hạn, như một phần ba trong hệ mười, nên máy phải cắt bớt.
           Cách đúng là đổi ra đồng, một trăm cộng hai trăm ra đúng ba trăm."""),
        st('<p>Khi tiền <b>bắt buộc</b> có phần lẻ (tỉ giá, lãi suất), Java có kiểu số thập phân chính xác <code>BigDecimal</code>:</p>'
           + code_block(thap_phan, lines=(5, 7))
           + "<span class='note'>(cần dòng <code>import java.math.BigDecimal;</code> ở đầu tệp)</span>" + out_block(thap_phan),
           """Khi tiền bắt buộc có phần lẻ, như tỉ giá, Java có sẵn một kiểu số thập phân chính xác.
           Ta tạo số từ chuỗi chữ, không từ số thực, để không mang theo sai lệch của hệ hai, rồi cộng bằng lệnh riêng, ra đúng không phẩy ba. Bài này chỉ cần biết nó tồn tại."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(3, 8), title="Đoán ba dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Biến x nhận năm, biến y nhận giá trị của x, rồi x được cộng thêm mười.
           Ba lệnh in in x, in y, và in x cộng y nối chữ đồng. Hãy dừng video, viết ra giấy ba dòng in ra.""", pause=20),
        st(table(["sau lệnh", "x", "y", "vì sao"],
                 [["<code>int x = 5;</code>", "5", "—", "tạo ngăn x, đặt 5"],
                  ["<code>int y = x;</code>", "5", "5", "y nhận <b>bản sao</b> giá trị của x"],
                  ["<code>x = x + 10;</code>", "15", "5", "chỉ ngăn x bị ghi đè; y không đổi"]]),
           """Đáp án, ta lập bảng giá trị sau từng lệnh. Lệnh một tạo x bằng năm. Lệnh hai chép giá trị năm sang y, chỉ là bản sao.
           Lệnh ba ghi đè mười lăm vào x, còn y vẫn là năm vì không lệnh nào ghi vào y.""", focus=[1, "1.2", "1.3", "1.4"]),
        st("<p>Dòng in thứ ba: hai số đứng trước nên cộng trước, rồi mới nối chữ (quy tắc dấu cộng của bài trước):</p>"
           "$$15 + 5 + \\text{\" dong\"} = 20 + \\text{\" dong\"} = \\hl{\\text{20 dong}}$$",
           """Dòng in thứ ba dùng quy tắc dấu cộng của bài trước. Hai số đứng trước nên cộng thành hai mươi, rồi mới nối chữ đồng."""),
        st(out_block(quiz),
           """Chạy thật, ba dòng in ra là x bằng mười lăm, y bằng năm, và hai mươi đồng."""),
    ], checks=["5 + 10 == 15", "str(15 + 5) + ' dong' == '20 dong'"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("biến = ngăn có tên", "kiểu = cỡ ngăn và thứ được chứa", "gán: tính vế phải rồi ghi đè",
                 "vượt cỡ thì quay vòng, không báo", "tiền: số nguyên dài theo đồng"),
           """Tổng kết chuỗi logic. Biến là ngăn nhớ có tên, kiểu quyết định cỡ ngăn và thứ được chứa.
           Phép gán tính vế phải rồi ghi đè. Vượt cỡ ngăn thì số quay vòng mà không báo, vì vậy tiền dùng số nguyên dài theo đồng."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi khai một biến, hỏi hai câu: <b>giá trị lớn nhất</b> nó có thể đạt là bao nhiêu,
và nó có cần <b>phần lẻ chính xác</b> không. Tổng tiền tính bằng đồng (không có phần lẻ) thì chọn <code>long</code>; cần phần lẻ chính xác thì dùng <code>BigDecimal</code>.</div>""",
           """Điều cần mang theo. Trước khi khai một biến, hãy hỏi giá trị lớn nhất nó có thể đạt là bao nhiêu, và nó có cần phần lẻ chính xác không.
           Với tổng tiền tính bằng đồng, câu trả lời là kiểu số nguyên dài; còn khi cần phần lẻ chính xác thì dùng kiểu số thập phân chính xác."""),
    ])
    return lesson("L01", "bien_va_kieu_du_lieu", "Bài 1 — Biến và kiểu dữ liệu",
                  "curriculum/jva.yaml L01; audit/jva/verify_jva.py L01 (javac/java chạy thật); The Java Language Specification, "
                  "Java SE 21: §4.2.1 (miền giá trị int, long, char), §4.2.2 (phép toán số nguyên không báo tràn), "
                  "§15.18.2 (tràn khi cộng: giữ các bit thấp theo bù hai), §4.2.3 (số thực IEEE 754), §3.10.1 (hậu tố L); "
                  "java.math.BigDecimal (Java SE 21 API); dev.java/learn",
                  ["Khai báo và gán biến, đọc đúng phép gán là tính vế phải rồi ghi đè",
                   "Chọn đúng kiểu trong sáu kiểu số nguyên, số nguyên dài, số thực, đúng sai, ký tự, chuỗi",
                   "Suy ra giới hạn của kiểu số nguyên và giải thích hiện tượng tràn số",
                   "Tính tổng tiền bằng kiểu số nguyên dài theo đồng, biết vì sao không dùng số thực",
                   "Chạy từng dòng Java bằng công cụ gõ từng dòng, tự đoán kết quả rồi kiểm",
                   "Dự đoán lô lệnh cỡ nào làm kiểu số nguyên tràn, và vì sao thử bằng lô nhỏ không bắt được",
                   "Viết chương trình có biến số nguyên dài, phép gán lại và so sánh hai kiểu"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_jsh, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "sym"), (2, "example"), (3, "formula"), (4, "example"), (5, "jshell"), (6, "quymo"), (7, "practice")])
