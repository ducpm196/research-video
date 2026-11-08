from lib import *


def build():
    tong = prog("Tong", """
import java.util.ArrayList;

public class Tong {
    public static void main(String[] args) {
        ArrayList<Long> gd = new ArrayList<>();   // danh sách rỗng
        gd.add(500000L);
        gd.add(-200000L);
        gd.add(1500000L);
        long tong = 0;
        for (long x : gd) {                       // lấy lần lượt từng phần tử
            tong += x;
        }
        System.out.println("So giao dich: " + gd.size());
        System.out.println("Phan tu dau: " + gd.get(0));
        System.out.println("Tong: " + tong);
    }
}""", out="So giao dich: 3\nPhan tu dau: 500000\nTong: 1800000")
    dem = prog("Dem", """
import java.util.HashMap;

public class Dem {
    public static void main(String[] args) {
        String[] loai = {"NAP", "RUT", "NAP", "CK", "NAP", "RUT"};
        HashMap<String, Integer> dem = new HashMap<>();
        for (String t : loai) {
            int cu = dem.getOrDefault(t, 0);   // chưa gặp thì coi là 0
            dem.put(t, cu + 1);                // ghi đè số đếm mới
        }
        System.out.println("NAP: " + dem.get("NAP"));
        System.out.println("RUT: " + dem.get("RUT"));
        System.out.println("CK: " + dem.get("CK"));
        System.out.println("XYZ: " + dem.get("XYZ"));
        System.out.println("So loai: " + dem.size());
    }
}""", out="NAP: 3\nRUT: 2\nCK: 1\nXYZ: null\nSo loai: 3")
    so_du = prog("SoDu", """
import java.util.HashMap;

public class SoDu {
    public static void main(String[] args) {
        HashMap<String, Long> soDu = new HashMap<>();
        soDu.put("A01", 2000000L);                    // (1)
        soDu.put("B02", 500000L);                     // (2)
        soDu.put("A01", soDu.get("A01") - 300000L);   // (3) rút 300 nghìn
        long c = soDu.getOrDefault("C03", 0L);        // (4) chưa mở tài khoản
        System.out.println("A01: " + soDu.get("A01"));
        System.out.println("B02: " + soDu.get("B02"));
        System.out.println("C03: " + c);
        System.out.println("So tai khoan: " + soDu.size()); // (5)
    }
}""", out="A01: 1700000\nB02: 500000\nC03: 0\nSo tai khoan: 2")
    kiem = prog("Kiem", """
import java.util.ArrayList;

public class Kiem {
    public static void main(String[] args) {
        ArrayList<Long> gd = new ArrayList<>();
        gd.add(500000L);
        gd.add(-200000L);
        gd.add(1500000L);
        long tong = 0;
        for (int i = 0; i < gd.size(); i++) {   // đường khác: đi theo chỉ số
            tong += gd.get(i);
        }
        System.out.println("Tong theo chi so: " + tong);
    }
}""", out="Tong theo chi so: 1800000")
    kieu_tran = prog("KieuTran", """
import java.util.ArrayList;

public class KieuTran {
    public static void main(String[] args) {
        ArrayList<long> gd = new ArrayList<>();
        gd.add(500000L);
    }
}""", expect="compile_error:unexpected type")
    xoa = prog("Xoa", """
import java.util.ArrayList;

public class Xoa {
    public static void main(String[] args) {
        ArrayList<String> ds = new ArrayList<>();
        ds.add("A01");
        ds.add("B02");
        ds.add("C03");
        ds.add("D04");
        for (String s : ds) {
            if ("B02".equals(s)) {
                ds.remove(s);            // xoá ngay trong vòng duyệt
            }
        }
        System.out.println(ds);
    }
}""", out="", expect="runtime_error:ConcurrentModificationException",
        err='Exception in thread "main" java.util.ConcurrentModificationException')
    xoa_dung = prog("XoaDung", """
import java.util.ArrayList;

public class XoaDung {
    public static void main(String[] args) {
        ArrayList<String> ds = new ArrayList<>();
        ds.add("A01");
        ds.add("B02");
        ds.add("C03");
        ds.add("D04");
        for (int i = ds.size() - 1; i >= 0; i--) {   // đi từ cuối về đầu
            if ("B02".equals(ds.get(i))) {
                ds.remove(i);                         // xoá theo chỉ số
            }
        }
        System.out.println(ds);
    }
}""", out="[A01, C03, D04]")
    so_sanh = prog("SoSanh", """
import java.util.HashMap;

public class SoSanh {
    public static void main(String[] args) {
        HashMap<String, Integer> dem = new HashMap<>();
        dem.put("NAP", 127);
        dem.put("RUT", 127);
        dem.put("CK", 128);
        dem.put("THE", 128);
        System.out.println(dem.get("NAP") == dem.get("RUT"));
        System.out.println(dem.get("CK") == dem.get("THE"));
        System.out.println(dem.get("CK").equals(dem.get("THE")));
    }
}""", out="true\nfalse\ntrue")
    quiz = prog("DoanKetQua", """
import java.util.ArrayList;
import java.util.HashMap;

public class DoanKetQua {
    public static void main(String[] args) {
        ArrayList<Long> ds = new ArrayList<>();
        ds.add(100L);
        ds.add(200L);
        ds.add(300L);
        HashMap<String, Integer> m = new HashMap<>();
        m.put("CK", 1);
        m.put("CK", m.get("CK") + 1);
        System.out.println(ds.size() + " " + ds.get(2));
        System.out.println(m.get("CK") + " " + m.getOrDefault("RUT", 0));
        System.out.println(m.size());
    }
}""", out="3 300\n2 0\n1")

    sc_hook = sc("hook", "hook", "Số giao dịch trong ngày không biết trước, mảng cố định có đủ không?", [
        st("""<p>Mảng số dư ở bài 5 có đúng $5$ ô, tạo xong là <b>không đổi độ dài</b>. Nhưng hôm nay có bao nhiêu giao dịch? Không ai biết trước.</p>
<p>Khách đưa số tài khoản <code>"A01"</code>, ta muốn tra ra số dư ngay, không dò từng ô.</p>""",
           """Mảng số dư bạn đã học có năm ô, độ dài cố định. Nhưng số giao dịch trong ngày thì không ai biết trước.
           Còn khi khách đưa số tài khoản, ta muốn tra ra số dư ngay."""),
        st("""<div class="box key">Hôm nay: <b>danh sách</b> lớn dần theo dữ liệu, và <b>bản đồ khoá–giá trị</b> tra số dư theo số tài khoản.
Cuối bài bạn đếm được số giao dịch theo từng loại.</div>""",
           """Hôm nay ta học hai công cụ cho hai việc đó: danh sách lớn dần, và bản đồ khoá–giá trị.
           Cuối bài, bạn đếm được giao dịch theo từng loại."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: mảng, đối tượng và vòng lặp cộng dồn", [
        st(table(["đã học", "điều cần nhớ hôm nay"],
                 [["① Mảng", "chỉ số chạy từ <code>0</code> tới <code>n − 1</code>; độ dài cố định; vượt chỉ số là lỗi khi chạy"],
                  ["② Lớp và đối tượng", "<code>new</code> tạo đối tượng; gọi phương thức bằng dấu chấm, như <code>tk.nap(500000)</code>"],
                  ["③ Vòng lặp cộng dồn", "biến tổng bắt đầu từ <code>0</code>, mỗi vòng cộng thêm một phần tử"]]),
           """Ta ôn ba điều. Thứ nhất, mảng có chỉ số từ không tới n trừ một, độ dài cố định.
           Thứ hai, từ khoá tạo mới sinh ra đối tượng, và ta gọi phương thức bằng dấu chấm.
           Thứ ba, vòng lặp cộng dồn bắt đầu tổng bằng không, mỗi vòng cộng thêm một phần tử."""),
        st("""<p>Danh sách và bản đồ <b>cũng là lớp</b>, có sẵn trong thư viện của Java (gói <code>java.util</code>). Ta chỉ cần tạo đối tượng rồi gọi phương thức.</p>""",
           """Tin vui là danh sách và bản đồ cũng chỉ là lớp có sẵn trong thư viện, nên bạn đã biết cách dùng: tạo đối tượng, rồi gọi phương thức."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ký hiệu: danh sách, bản đồ và kiểu trong ngoặc nhọn", [
        st(code_block(tong, lines=(5, 15), title="Phần thân hàm chính của Tong.java"),
           """Chương trình đầu tiên tạo một danh sách giao dịch, thêm ba số tiền, rồi cộng tổng. Ta đọc từng ký hiệu ở bảng sau."""),
        st(table(["viết", "nghĩa"],
                 [["<code>import java.util.ArrayList;</code>", "dòng đầu tệp: mượn lớp danh sách từ thư viện"],
                  ["<code>ArrayList&lt;Long&gt;</code>", "danh sách mà mỗi phần tử là một số <code>Long</code>; kiểu nằm trong ngoặc nhọn"],
                  ["<code>new ArrayList&lt;&gt;()</code>", "tạo danh sách rỗng; ngoặc nhọn trống: máy tự suy ra kiểu"],
                  ["<code>gd.add(500000L)</code>", "thêm vào <b>cuối</b>; chữ <code>L</code> nói đây là số kiểu <code>long</code>"],
                  ["<code>gd.get(0)</code>, <code>gd.size()</code>", "lấy phần tử ở chỉ số 0; số phần tử hiện có"],
                  ["<code>for (long x : gd)</code>", "vòng lặp duyệt: lần lượt gán từng phần tử cho <code>x</code>; dùng được cả với mảng"]]),
           """Dòng nhập mượn lớp danh sách từ thư viện. Kiểu trong ngoặc nhọn nói mỗi phần tử là số nguyên dài.
           Ngoặc nhọn trống khi tạo mới nghĩa là máy tự suy ra kiểu.
           Phương thức thêm đặt phần tử vào cuối, chữ L nói con số thuộc kiểu dài.
           Phương thức lấy nhận chỉ số, phương thức kích thước đếm phần tử.
           Vòng lặp duyệt gán lần lượt từng phần tử cho biến x, và dùng được cả với mảng.""", clear=True),
        st(table(["viết", "nghĩa"],
                 [["<code>HashMap&lt;String, Long&gt;</code>", "bản đồ: khoá là chuỗi (số tài khoản), giá trị là số dư"],
                  ["<code>m.put(k, v)</code>", "đặt giá trị <code>v</code> cho khoá <code>k</code>; khoá đã có thì <b>ghi đè</b>"],
                  ["<code>m.get(k)</code>", "lấy giá trị của khoá <code>k</code>; không có khoá thì ra <code>null</code>"],
                  ["<code>m.getOrDefault(k, 0L)</code>", "như <code>get</code>, nhưng không có khoá thì ra giá trị mặc định"],
                  ["<code>m.size()</code>, <code>m.values()</code>", "số khoá; tất cả giá trị, để duyệt"]]),
           """Bảng thứ hai là bản đồ, với hai kiểu trong ngoặc nhọn: khoá là chuỗi, giá trị là số dư.
           Phương thức đặt gắn giá trị cho khoá, khoá đã có thì ghi đè.
           Phương thức lấy trả giá trị của khoá, không có khoá thì trả giá trị rỗng.
           Lấy hoặc mặc định thì trả con số mặc định khi không có khoá.
           Còn lại là đếm số khoá, và lấy mọi giá trị để duyệt.""", clear=True),
        st(out_block(tong),
           """Chạy thật chương trình đầu tiên: ba giao dịch, phần tử đầu là năm trăm nghìn.
           Tổng là năm trăm nghìn, trừ hai trăm nghìn, cộng một triệu rưỡi, ra một triệu tám trăm nghìn.""", clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: hàng ô đánh số và bảng tra theo khoá", [
        st(svg(1500, 380,
               panel(20, 20, 700, 340, "Danh sách: ô đánh số 0, 1, 2…", C_BLUE),
               txt(125, 125, "0", 24, "middle", "#2a78d6", True), txt(285, 125, "1", 24, "middle", "#2a78d6", True),
               txt(445, 125, "2", 24, "middle", "#2a78d6", True), txt(605, 125, "3", 24, "middle", "#9ca3af", True),
               box(50, 140, 150, 80, "500000", C_GRAY), box(210, 140, 150, 80, "-200000", C_GRAY),
               box(370, 140, 150, 80, "1500000", C_GRAY), box(530, 140, 150, 80, ["thêm", "vào cuối"], C_AMBER, 22, dash=True),
               txt(370, 290, "add: thêm vào cuối, get(i): lấy ô i", 24, "middle", "#1f2937"),
               txt(370, 330, "size() tăng dần, không cố định", 24, "middle", "#1f2937"),
               panel(780, 20, 700, 340, "Bản đồ: khoá → giá trị", C_GREEN),
               box(820, 90, 200, 64, '"A01"', C_BLUE, bold=True), arrow(1025, 122, 1110, 122, "#16a34a"),
               box(1120, 90, 320, 64, "1700000", C_GRAY),
               box(820, 175, 200, 64, '"B02"', C_BLUE, bold=True), arrow(1025, 207, 1110, 207, "#16a34a"),
               box(1120, 175, 320, 64, "500000", C_GRAY),
               box(820, 260, 200, 64, '"C03"', C_RED, dash=True), arrow(1025, 292, 1110, 292, "#dc2626", dash=True),
               box(1120, 260, 320, 64, ["không có khoá", "get ra null"], C_RED, 22)),
           """Bên trái là danh sách, một hàng ô đánh số từ không. Thêm phần tử là đặt thêm một ô vào cuối, nên kích thước tăng dần.
           Bên phải là bản đồ: mỗi số tài khoản trỏ tới đúng một số dư, tra là ra ngay.
           Khoá C không ba chưa có, nên phương thức lấy trả giá trị rỗng."""),
        st(svg(1500, 300,
               box(40, 90, 280, 110, ["long 500000", "số trần"], C_GRAY, bold=True),
               arrow(325, 145, 520, 145, "#d97706", "đóng hộp"),
               box(530, 70, 420, 150, ["đối tượng Long", "bên trong: 500000"], C_AMBER, bold=True),
               arrow(955, 145, 1150, 145, "#16a34a", "mở hộp"),
               box(1160, 90, 300, 110, ["long 500000", "dùng để tính"], C_GRAY, bold=True),
               txt(750, 270, "danh sách và bản đồ chỉ chứa đối tượng, nên kiểu trong ngoặc nhọn viết hoa: Long, Integer", 24, "middle", "#1f2937", True)),
           """Một chi tiết quan trọng: danh sách và bản đồ chỉ chứa đối tượng, không chứa số trần.
           Thêm một số kiểu dài thì máy tự bọc nó vào đối tượng, gọi là đóng hộp, hay hộp hoá. Lấy ra để tính thì máy tự mở hộp.
           Vì thế kiểu trong ngoặc nhọn là lớp bọc, viết hoa chữ đầu."""),
        st(table(["", "mảng", "danh sách", "bản đồ"],
                 [["độ dài", "cố định khi tạo", "lớn dần khi thêm", "lớn dần khi đặt khoá mới"],
                  ["tìm phần tử theo", "chỉ số <code>a[i]</code>", "chỉ số <code>get(i)</code>", "khoá <code>get(k)</code>"],
                  ["không có thì", "lỗi khi chạy", "lỗi khi chạy", "ra <code>null</code> (hoặc mặc định)"],
                  ["chứa số trần <code>long</code>?", "được", "không, dùng <code>Long</code>", "không, dùng <code>Long</code>"]]),
           """Bảng này so ba cách giữ nhiều giá trị. Mảng cố định độ dài, danh sách và bản đồ lớn dần.
           Sai chỉ số thì báo lỗi khi chạy, còn thiếu khoá thì bản đồ trả giá trị rỗng hoặc mặc định."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: đếm số giao dịch theo loại", [
        st(code_block(dem, lines=(5, 6), title="Bước 1. Có dữ liệu và một bản đồ rỗng"),
           """Bước một, ta có một mảng sáu giao dịch, mỗi giao dịch ghi loại: nạp, rút, hoặc chuyển khoản.
           Ta tạo bản đồ rỗng, khoá là tên loại, giá trị là số lần gặp, vì cần tra số đếm theo tên loại."""),
        st(code_block(dem, lines=(7, 8), title="Bước 2. Lấy số đếm cũ, chưa gặp thì là 0"),
           """Bước hai, lấy số đếm cũ. Lần đầu gặp thì chưa có khoá, nên ta dùng lấy hoặc mặc định với số không.
           Lấy thường sẽ trả giá trị rỗng, mà giá trị rỗng không mở hộp thành số được, nên sẽ báo lỗi."""),
        st(code_block(dem, lines=(9, 9), title="Bước 3. Cộng một rồi đặt lại")
           + table(["vòng", "loại", "số cũ", "đặt lại"],
                   [["1", "NAP", "0 (chưa có)", "NAP = 1"], ["2", "RUT", "0 (chưa có)", "RUT = 1"],
                    ["3", "NAP", "1", "NAP = 2"], ["4", "CK", "0 (chưa có)", "CK = 1"]]),
           """Bước ba, cộng một vào số cũ rồi đặt lại, và vì khoá đã có nên giá trị cũ bị ghi đè.
           Theo bảng, vòng một gặp nạp lần đầu nên nạp bằng một, vòng hai rút bằng một.
           Vòng ba gặp nạp lần nữa, số cũ là một nên đặt lại thành hai.""", focus=[2, 3, 3]),
        st(code_block(dem, lines=(11, 15), title="Bước 4. In kết quả") + out_block(dem),
           """Bước bốn, in kết quả: nạp ba, rút hai, chuyển khoản một, đúng như đếm tay.
           Khoá không có thì in giá trị rỗng, và bản đồ có ba khoá, nghĩa là ba loại."""),
    ], checks=["['NAP', 'RUT', 'NAP', 'CK', 'NAP', 'RUT'].count('NAP') == 3",
               "['NAP', 'RUT', 'NAP', 'CK', 'NAP', 'RUT'].count('RUT') == 2",
               "len(set(['NAP', 'RUT', 'NAP', 'CK', 'NAP', 'RUT'])) == 3"])
    sc_ex = sc("example", "example", "Ví dụ: bản đồ tài khoản → số dư, từng phép tính", [
        st(code_block(so_du, lines=(5, 13), title="Tệp SoDu.java, phần thân hàm chính"),
           """Ví dụ này dùng bản đồ từ số tài khoản tới số dư, đúng việc một sổ ngân hàng làm. Có năm phép tính được đánh số."""),
        st(code_block(so_du, lines=(6, 7)) + "<p>Phép ① và ② đặt hai khoá mới:</p>"
           "$$① \\; \\text{A01} \\to 2\\,000\\,000 \\qquad ② \\; \\text{B02} \\to 500\\,000$$",
           """Phép tính thứ nhất đặt khoá A không một với hai triệu đồng. Phép tính thứ hai đặt khoá B không hai với năm trăm nghìn."""),
        st(code_block(so_du, lines=(8, 8)) + "<p>Phép ③: lấy giá trị cũ, trừ, rồi đặt lại vào <b>cùng khoá</b>:</p>"
           "$$③ \\; 2\\,000\\,000 - 300\\,000 = \\hl{1\\,700\\,000}$$",
           """Phép tính thứ ba rút ba trăm nghìn. Máy lấy giá trị cũ hai triệu, trừ đi, ra một triệu bảy trăm nghìn, rồi ghi đè vào cùng khoá."""),
        st(code_block(so_du, lines=(9, 9)) + "<p>Phép ④: khoá <code>\"C03\"</code> chưa có, nên ra giá trị mặc định:</p>"
           "$$④ \\; \\text{C03} \\to \\hlg{0}$$",
           """Phép tính thứ tư tra khoá C không ba, chưa từng được đặt, nên lấy hoặc mặc định trả số không."""),
        st(code_block(so_du, lines=(13, 13)) + "<p>Phép ⑤: đặt <code>\"A01\"</code> hai lần vẫn chỉ là <b>một khoá</b>:</p>"
           "$$⑤ \\; \\text{A01}, \\text{B02} \\to \\hl{2} \\text{ khoá}$$",
           """Phép tính thứ năm đếm số khoá. Khoá A không một đặt hai lần vẫn là một khoá, và tra khoá C không ba không thêm khoá nào, nên có hai khoá."""),
        st(out_block(so_du),
           """Chạy thật chương trình, bốn dòng in ra khớp năm phép tính: một triệu bảy trăm nghìn, năm trăm nghìn, không, và hai tài khoản."""),
    ], checks=["2000000 - 300000 == 1700000", "len({'A01': 1, 'B02': 2}) == 2",
               "{'A01': 1700000, 'B02': 500000}.get('C03', 0) == 0"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đi theo chỉ số, và cộng các số đếm", [
        st(code_block(kiem, lines=(5, 13), title="Cùng danh sách, cộng theo chỉ số") + out_block(kiem),
           """Kiểm tổng bằng đường khác: thay vòng lặp duyệt bằng vòng lặp đếm theo chỉ số, từ không tới kích thước trừ một.
           Kết quả vẫn là một triệu tám trăm nghìn, vì hai vòng lặp đi qua cùng ba phần tử."""),
        st("<p>Kiểm phép đếm: mỗi giao dịch được đếm <b>đúng một lần</b>, nên tổng các số đếm phải bằng số phần tử của mảng.</p>"
           "$$3 + 2 + 1 = 6 = \\text{số phần tử của mảng} \\; \\checkmark$$",
           """Kiểm phép đếm: mỗi giao dịch được đếm đúng một lần, nên tổng các số đếm phải bằng số phần tử.
           Ba cộng hai cộng một bằng sáu, và mảng có đúng sáu phần tử, khớp.""", clear=True),
    ], checks=["500000 - 200000 + 1500000 == 1800000", "3 + 2 + 1 == len(['NAP', 'RUT', 'NAP', 'CK', 'NAP', 'RUT'])"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Viết kiểu số trần trong ngoặc nhọn.</div>'
           + code_block(kieu_tran, lines=(5, 5)) + out_block(kieu_tran, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là viết kiểu số trần trong ngoặc nhọn.
           Trình biên dịch báo kiểu không mong đợi, vì danh sách chỉ chứa đối tượng. Sửa bằng lớp bọc, chữ đầu viết hoa."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Xoá phần tử ngay trong vòng lặp duyệt.</div>'
           + code_block(xoa, lines=(10, 14)) + out_block(xoa),
           """Lỗi thứ hai là xoá phần tử ngay trong vòng lặp duyệt, ở đây là bỏ tài khoản B không hai.
           Danh sách bị đổi giữa chừng, nên bộ duyệt ném ngoại lệ sửa đổi đồng thời."""),
        st(code_block(xoa_dung, lines=(10, 15), title="Cách sửa: duyệt theo chỉ số, từ cuối về đầu") + out_block(xoa_dung),
           """Cách sửa là duyệt theo chỉ số từ cuối về đầu, và xoá theo chỉ số.
           Xoá một ô chỉ làm dịch các ô phía sau, mà các ô đó đã đi qua rồi, nên không bỏ sót ai."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> So hai số lấy từ bản đồ bằng <code>==</code>.</div>'
           + code_block(so_sanh, lines=(6, 12)) + out_block(so_sanh),
           """Lỗi thứ ba hay gặp ở người đã đi làm: so hai lớp bọc bằng dấu bằng bằng, tức so địa chỉ đối tượng chứ không so con số.
           Một trăm hai mươi bảy thì ra đúng, một trăm hai mươi tám lại ra sai."""),
        st("""<div class="box key">Lý do: quy định của Java bảo đảm số trong khoảng $-128$ tới $127$ được đóng hộp vào <b>cùng một</b> đối tượng có sẵn.
Ngoài khoảng đó, máy ảo mặc định tạo đối tượng mới, nên <code>==</code> ra <code>false</code>. So lớp bọc luôn dùng <code>equals</code>.</div>
<span class='note'>Kiểm thử với số đếm nhỏ thì qua, lên hệ thống thật với số lớn thì sai: lỗi rất khó tìm.</span>""",
           """Lý do là Java bảo đảm số từ âm một trăm hai mươi tám tới một trăm hai mươi bảy được đóng hộp vào cùng một đối tượng có sẵn.
           Ngoài khoảng đó, máy ảo mặc định tạo đối tượng mới, nên phải so bằng nội dung.
           Lỗi này khó tìm, vì kiểm thử với số nhỏ thì qua.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(6, 15), title="Đoán ba dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Danh sách có ba số một trăm, hai trăm, ba trăm. Khoá chuyển khoản được đặt bằng một, rồi đặt lại bằng giá trị cũ cộng một.
           Hãy dừng video và viết ra ba dòng in ra.""", pause=20),
        st(table(["dòng in", "lý do", "in ra"],
                 [["① <code>ds.size()</code>, <code>ds.get(2)</code>", "3 phần tử; chỉ số 2 là phần tử <b>thứ ba</b>", "<b>3 300</b>"],
                  ["② <code>m.get(\"CK\")</code>, <code>getOrDefault(\"RUT\", 0)</code>", "$1 + 1 = 2$; khoá RUT chưa có nên ra 0", "<b>2 0</b>"],
                  ["③ <code>m.size()</code>", "khoá CK đặt hai lần vẫn là một khoá", "<b>1</b>"]]),
           """Đáp án như sau. Dòng một, danh sách có ba phần tử, và chỉ số hai là phần tử thứ ba, tức ba trăm.
           Dòng hai, khoá chuyển khoản thành một cộng một bằng hai, còn khoá rút chưa có nên ra không.
           Dòng ba, khoá đặt hai lần vẫn là một khoá."""),
        st(out_block(quiz),
           """Chạy thật, ba dòng khớp đáp án. Ai đoán hai trăm thì nhớ rằng chỉ số bắt đầu từ không."""),
    ], checks=["[100, 200, 300][2] == 300", "1 + 1 == 2", "{'CK': 2}.get('RUT', 0) == 0", "len({'CK': 2}) == 1"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mảng: độ dài cố định", "danh sách: thêm dần, chỉ số 0…size − 1", "bản đồ: khoá → giá trị",
                 "lấy hoặc mặc định để đếm"),
           """Tổng kết chuỗi logic. Mảng có độ dài cố định, còn danh sách thêm dần, chỉ số từ không tới kích thước trừ một.
           Bản đồ tra giá trị theo khoá, và lấy hoặc mặc định giúp đếm tần suất gọn gàng."""),
        st("""<div class='box key'><b>Tư duy:</b> kiểu trong ngoặc nhọn là <b>lớp bọc</b> (<code>Long</code>, <code>Integer</code>), nên so bằng
<code>equals</code>, không bằng <code>==</code>. Khoá không có thì <code>get</code> ra <code>null</code>. Không xoá phần tử trong vòng lặp duyệt.</div>""",
           """Điều cần mang theo. Kiểu trong ngoặc nhọn là lớp bọc, nên so bằng nội dung, không so địa chỉ.
           Thiếu khoá thì phương thức lấy trả giá trị rỗng. Và đừng xoá phần tử trong vòng lặp duyệt."""),
    ])
    return lesson("L09", "danh_sach_va_ban_do", "Bài 9 — Danh sách và bản đồ",
                  "curriculum/jva.yaml L09; audit/jva/verify_jva.py L09 (javac/java chạy thật); The Java Language Specification, Java SE 21 "
                  "(§5.1.7 đóng hộp, §5.1.8 mở hộp, §14.14.2 vòng lặp duyệt); Java SE 21 API: java.util.ArrayList (bộ duyệt fail-fast, "
                  "ConcurrentModificationException), java.util.HashMap, java.util.Map.getOrDefault, java.lang.Integer.valueOf (luôn đệm −128..127); dev.java/learn",
                  ["Tạo danh sách, thêm, lấy theo chỉ số, duyệt và cộng tổng", "Dùng bản đồ khoá–giá trị để tra số dư theo số tài khoản",
                   "Đếm tần suất bằng lấy hoặc mặc định", "Giải thích hộp hoá và vì sao lớp bọc phải so bằng equals"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
