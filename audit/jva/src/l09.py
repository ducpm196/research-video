from lib import *
from labkit import write_lab, practice_steps, practice_scene


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

    tra_cuu = prog("TraCuuTk", """
import java.util.HashMap;

public class TraCuuTk {
    public static void main(String[] args) {
        HashMap<String, Long> soDu = new HashMap<>();
        soDu.put("A01", 2000000L);
        soDu.put("B02", 500000L);
        String[] hoi = {"B02", "Z99", "A01"};           // ba lượt khách hỏi số dư
        for (String k : hoi) {
            if (soDu.containsKey(k)) {                  // có khoá này không?
                System.out.println(k + ": " + soDu.get(k));
            } else {
                System.out.println(k + ": khong co");
            }
        }
    }
}""", out="B02: 500000\nZ99: khong co\nA01: 2000000")
    lam_da = prog("MuiTen", """
import java.util.ArrayList;

public class MuiTen {
    public static void main(String[] args) {
        ArrayList<Long> gd = new ArrayList<>();
        gd.add(300000L);
        gd.add(-50000L);
        gd.add(1200000L);
        gd.add(450000L);
        gd.forEach(x -> System.out.println("GD " + x));    // với mỗi x: in ra
        gd.sort((a, b) -> Long.compare(b, a));             // số lớn đứng trước
        System.out.println(gd);
    }
}""", out="GD 300000\nGD -50000\nGD 1200000\nGD 450000\n[1200000, 450000, 300000, -50000]")
    quet_ds = prog("QuetDanhSach", """
import java.util.ArrayList;

public class QuetDanhSach {
    public static void main(String[] args) {
        int[] co = {1000, 1000000};                      // số tài khoản: x1, x1000
        for (int k = 0; k < co.length; k++) {
            ArrayList<Long> ds = new ArrayList<>();
            for (int i = 0; i < co[k]; i++) {
                ds.add(1000000L + i);
            }
            long can = ds.get(ds.size() - 1);            // tài khoản nằm ở cuối
            int buoc = 0;
            for (int i = 0; i < ds.size(); i++) {
                buoc++;
                if (ds.get(i) == can) {
                    break;
                }
            }
            System.out.println(co[k] + " tai khoan: " + buoc + " buoc");
        }
    }
}""", out="1000 tai khoan: 1000 buoc\n1000000 tai khoan: 1000000 buoc")
    thong_ke = prog("ThongKe", """
import java.util.ArrayList;
import java.util.HashMap;

public class ThongKe {
    public static void main(String[] args) {
        String[] loai = {"CK", "NAP", "CK", "RUT", "CK", "NAP", "CK"};
        HashMap<String, Integer> dem = new HashMap<>();
        for (String t : loai) {
            dem.put(t, dem.getOrDefault(t, 0) + 1);       // lấy số cũ, cộng một, đặt lại
        }
        ArrayList<Long> tien = new ArrayList<>();
        tien.add(300000L);
        tien.add(900000L);
        tien.add(120000L);
        tien.add(450000L);
        tien.sort((a, b) -> Long.compare(b, a));          // lớn trước
        System.out.println("So giao dich: " + loai.length);
        System.out.println("CK: " + dem.get("CK"));
        System.out.println("NAP: " + dem.get("NAP"));
        System.out.println("RUT: " + dem.get("RUT"));
        System.out.println("Lon truoc: " + tien);
    }
}""", out="So giao dich: 7\nCK: 4\nNAP: 2\nRUT: 1\nLon truoc: [900000, 450000, 300000, 120000]")
    write_lab("JVA", "L09", """# Lab JVA L09 — Thống kê giao dịch

Trong Git Bash, viết `ThongKe` (tệp `ThongKe.java`, số liệu là số minh hoạ). Nhớ `import java.util.ArrayList;` và `import java.util.HashMap;`.

1. Mảng loại giao dịch `{"CK", "NAP", "CK", "RUT", "CK", "NAP", "CK"}`. Đếm số lần mỗi loại bằng `HashMap<String, Integer>` và `getOrDefault`.
2. Danh sách `ArrayList<Long>` gồm `300000, 900000, 120000, 450000`. Sắp **giảm dần** bằng `tien.sort((a, b) -> Long.compare(b, a));`.
3. In đúng năm dòng: `So giao dich: …` (độ dài mảng), `CK: …`, `NAP: …`, `RUT: …`, `Lon truoc: [...]` (in thẳng danh sách).

Chạy: `javac ThongKe.java && java ThongKe`. Chấm: `bash labs/cham.sh JVA L09 ThongKe.java`.
""", "java", thong_ke["code"], thong_ke["out"])
    sc_lab = practice_scene(sc, "Tự làm: thống kê giao dịch", practice_steps(
        st, "JVA", "L09",
        """<p><b>Đề</b>: viết <code>ThongKe.java</code> (số minh hoạ).</p>
<ol><li>Mảng loại <code>{"CK","NAP","CK","RUT","CK","NAP","CK"}</code>; đếm mỗi loại bằng <code>HashMap&lt;String, Integer&gt;</code> và <code>getOrDefault</code></li>
<li>Danh sách <code>ArrayList&lt;Long&gt;</code>: 300000, 900000, 120000, 450000; sắp <b>giảm dần</b> bằng <code>sort((a, b) -&gt; Long.compare(b, a))</code></li>
<li>In năm dòng: <code>So giao dich</code>, <code>CK</code>, <code>NAP</code>, <code>RUT</code>, <code>Lon truoc</code></li></ol>""",
        """Bây giờ tới phần bạn tự làm trên máy. Cho một mảng bảy loại giao dịch. Dùng bản đồ và phương thức lấy hoặc mặc định để đếm số lần của từng loại.
        Rồi cho một danh sách bốn số tiền, sắp giảm dần bằng hàm nhỏ viết bằng mũi tên. In năm dòng gồm số giao dịch, ba số đếm, và danh sách đã sắp. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        thong_ke["out"], "ThongKe.java",
        """<div class="box key"><b>Nếu kẹt:</b> trong vòng lặp duyệt: <code>dem.put(t, dem.getOrDefault(t, 0) + 1);</code>. Sắp giảm dần: <code>tien.sort((a, b) -&gt; Long.compare(b, a));</code> — đảo <code>a</code> và <code>b</code> so với sắp tăng.
Lời giải nằm ở <code>labs/JVA/L09/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, trong vòng lặp duyệt, đặt lại khoá bằng số cũ lấy hoặc mặc định cộng một. Sắp giảm dần bằng cách viết hàm so sánh với hai tham số đảo chỗ cho nhau so với sắp tăng.
        Lời giải nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=60), "JVA", "L09")

    sc_hook = sc("hook", "hook", "Số giao dịch trong ngày không biết trước, mảng cố định có đủ không?", [
        st("""<p>Mảng số dư ở bài 5 có đúng $5$ ô, tạo xong là <b>không đổi độ dài</b>. Nhưng hôm nay có bao nhiêu giao dịch? Không ai biết trước.</p>
<p>Khách đưa số tài khoản <code>"A01"</code>, ta muốn tra ra số dư ngay, không dò từng ô.</p>""",
           """Mảng số dư bạn đã học có năm ô, độ dài cố định. Nhưng số giao dịch trong ngày thì không ai biết trước.
           Còn khi khách đưa số tài khoản, ta muốn tra ra số dư ngay."""),
        st("""<div class="box key">Hôm nay: <b>danh sách</b> lớn dần theo dữ liệu, và <b>bản đồ khoá–giá trị</b> tra số dư theo số tài khoản.
Cuối bài bạn đếm được số giao dịch theo từng loại.</div>
<span class='note'><b>Khoá</b>: thứ dùng để tra (số tài khoản). <b>Giá trị</b>: thứ tra ra được (số dư).</span>""",
           """Hôm nay ta học hai công cụ cho hai việc đó: danh sách lớn dần, và bản đồ khoá–giá trị.
           Trong bản đồ, khoá là thứ ta dùng để tra, như số tài khoản, còn giá trị là thứ tra ra được, như số dư.
           Cuối bài, bạn đếm được giao dịch theo từng loại."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: mảng, đối tượng và vòng lặp cộng dồn", [
        st(table(["đã học", "điều cần nhớ hôm nay"],
                 [["① Mảng", "chỉ số chạy từ <code>0</code> tới <code>n − 1</code>; độ dài cố định; vượt chỉ số là lỗi khi chạy"],
                  ["② Lớp và đối tượng", "lớp là bản thiết kế; <code>new</code> tạo một đối tượng theo lớp; gọi phương thức (hàm gắn với đối tượng) bằng dấu chấm, như <code>tk.nap(500000)</code>"],
                  ["③ Vòng lặp cộng dồn", "biến tổng bắt đầu từ <code>0</code>, mỗi vòng cộng thêm một phần tử"]]),
           """Ta ôn ba điều. Thứ nhất, mảng có chỉ số từ không tới n trừ một, độ dài cố định.
           Thứ hai, lớp là bản thiết kế, từ khoá tạo mới sinh ra một đối tượng theo bản thiết kế đó, và ta gọi phương thức, tức hàm gắn với đối tượng, bằng dấu chấm.
           Thứ ba, vòng lặp cộng dồn bắt đầu tổng bằng không, mỗi vòng cộng thêm một phần tử."""),
        st("""<p>Danh sách và bản đồ <b>cũng là lớp</b>, có sẵn trong thư viện của Java (gói <code>java.util</code>). Ta chỉ cần tạo đối tượng rồi gọi phương thức.</p>""",
           """Tin vui là danh sách và bản đồ cũng chỉ là lớp có sẵn trong thư viện, nên bạn đã biết cách dùng: tạo đối tượng, rồi gọi phương thức."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ký hiệu: danh sách, bản đồ và kiểu trong ngoặc nhọn", [
        st(code_block(tong, lines=(5, 15), title="Phần thân hàm chính của Tong.java"),
           """Chương trình đầu tiên tạo một danh sách giao dịch, thêm ba số tiền, rồi cộng tổng. Ta đọc từng ký hiệu ở bảng sau."""),
        st(table(["viết", "nghĩa"],
                 [["<code>import java.util.ArrayList;</code>", "dòng đầu tệp: mượn lớp danh sách từ thư viện"],
                  ["<code>ArrayList&lt;Long&gt;</code>", "danh sách mà mỗi phần tử là một số <code>Long</code>; cặp ngoặc nhọn <code>&lt;…&gt;</code> gọi là <b>kiểu tổng quát</b>: một khuôn dùng chung, kiểu phần tử điền vào trong"],
                  ["<code>new ArrayList&lt;&gt;()</code>", "tạo danh sách rỗng; ngoặc nhọn trống: trình biên dịch tự suy ra kiểu"],
                  ["<code>gd.add(500000L)</code>", "thêm vào <b>cuối</b>; chữ <code>L</code> nói đây là số kiểu <code>long</code>"],
                  ["<code>gd.get(0)</code>, <code>gd.size()</code>", "lấy phần tử ở chỉ số 0; số phần tử hiện có"],
                  ["<code>for (long x : gd)</code>", "vòng lặp duyệt: lần lượt gán từng phần tử cho <code>x</code>; dùng được cả với mảng"]]),
           """Dòng nhập mượn lớp danh sách từ thư viện. Cặp ngoặc nhọn quanh kiểu gọi là kiểu tổng quát, một khuôn dùng chung cho nhiều kiểu phần tử, và kiểu ở trong nói mỗi phần tử là số nguyên dài.
           Ngoặc nhọn trống khi tạo mới nghĩa là trình biên dịch tự suy ra kiểu.
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
           Vì thế khi chứa số, kiểu trong ngoặc nhọn là lớp bọc, viết hoa chữ đầu."""),
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
    sc_tra = sc("tracuu", "example", "Ví dụ: khách hỏi số dư, có khoá thì trả, không có thì báo", [
        st(code_block(tra_cuu, lines=(5, 15)) + out_block(tra_cuu),
           """Ví dụ tra cứu: bản đồ có hai tài khoản, và ba khách lần lượt hỏi. Với mỗi số tài khoản, phương thức hỏi có khoá không cho đúng hoặc sai.
           Đúng thì in số dư lấy theo khoá, sai thì báo không có, thay vì để nhận giá trị rỗng. Chạy thật, khoá B không hai ra năm trăm nghìn, khoá Z chín chín báo không có, khoá A không một ra hai triệu.""",
           focus=[["1.2", "1.3"], "1.6", ["1.7", "1.9"], 3]),
    ], checks=["{'A01': 2000000, 'B02': 500000}.get('B02') == 500000", "'Z99' not in {'A01': 2000000, 'B02': 500000}"])
    sc_lam = sc("muiten", "example", "Ví dụ: hàm nhỏ viết bằng mũi tên và sắp xếp bằng bộ so sánh", [
        st(code_block(lam_da, lines=(5, 12)) + out_block(lam_da)
           + "<span class='note'>Hàm nhỏ viết bằng mũi tên gọi là <b>lambda</b>; bộ so sánh gọi là <b>Comparator</b>.</span>",
           """Đây là hai chỗ bạn sẽ gặp rất nhiều trong mã thật, chỉ cần đọc hiểu. Thứ nhất, hàm nhỏ không tên viết bằng mũi tên: nhận x, rồi làm biểu thức sau mũi tên.
           Phương thức duyệt gọi nó cho từng phần tử, nên in bốn dòng theo thứ tự đã thêm. Thứ hai, phương thức sắp xếp nhận một bộ so sánh, ta viết nó cũng bằng mũi tên với hai tham số a và b.
           Hàm so sánh hai số dài trả về âm nếu a đứng trước, bằng không nếu bằng nhau, dương nếu a đứng sau. Ta đảo a và b nên số lớn đứng trước, và danh sách in ra giảm dần.""",
           focus=[1, "1.6", "1.6", "1.7", "1.7", 3]),
    ], checks=["sorted([300000, -50000, 1200000, 450000], reverse=True) == [1200000, 450000, 300000, -50000]",
               "(450000 > 300000) - (450000 < 300000) == 1"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đi theo chỉ số, và cộng các số đếm", [
        st(code_block(kiem, lines=(5, 13), title="Cùng danh sách, cộng theo chỉ số") + out_block(kiem),
           """Kiểm tổng bằng đường khác: thay vòng lặp duyệt bằng vòng lặp đếm theo chỉ số, từ không tới kích thước trừ một.
           Kết quả vẫn là một triệu tám trăm nghìn, vì hai vòng lặp đi qua cùng ba phần tử."""),
        st("<p>Kiểm phép đếm: mỗi giao dịch được đếm <b>đúng một lần</b>, nên tổng các số đếm phải bằng số phần tử của mảng.</p>"
           "$$3 + 2 + 1 = 6 = \\text{số phần tử của mảng} \\; \\checkmark$$",
           """Kiểm phép đếm: mỗi giao dịch được đếm đúng một lần, nên tổng các số đếm phải bằng số phần tử.
           Ba cộng hai cộng một bằng sáu, và mảng có đúng sáu phần tử, khớp.""", clear=True),
    ], checks=["500000 - 200000 + 1500000 == 1800000", "3 + 2 + 1 == len(['NAP', 'RUT', 'NAP', 'CK', 'NAP', 'RUT'])"])
    sc_scale = sc("quymo", "concept", "Khi số tài khoản tăng gấp nghìn lần: tra bằng danh sách hay bằng bản đồ?", [
        st(code_block(quet_ds, lines=(5, 19)),
           """Ta tìm tài khoản nằm ở cuối danh sách, bằng cách duyệt từng phần tử, với hai cỡ. Chương trình đếm số bước chứ không đo giờ."""),
        st(out_block(quet_ds),
           """Một nghìn tài khoản mất một nghìn bước, một triệu tài khoản mất một triệu bước: tăng đúng theo số tài khoản.""", clear=True),
        st(table(["số tài khoản", "danh sách: số so sánh mỗi lượt tra (tối đa)", "bản đồ: mỗi lượt tra (trung bình)"],
                 [["1 000", "1 000", "khoảng 1"], ["1 000 000", "1 000 000", "khoảng 1"]])
           + "<span class='note'>Phần mô tả lớp <code>HashMap</code> trong Java SE 21 nói phép lấy và đặt có thời gian gần như không đổi khi hàm băm phân tán tốt.</span>",
           """Tra bằng bản đồ khác hẳn. Theo phần mô tả lớp này trong Java, phép lấy và đặt có thời gian gần như không đổi khi các khoá phân tán đều. Nên mỗi lượt tra tốn cỡ một bước, dù có một nghìn hay một triệu tài khoản.
           Nếu mỗi giây có một nghìn lượt tra trên một triệu tài khoản, danh sách phải làm đến một nghìn triệu phép so sánh mỗi giây, số minh hoạ, còn bản đồ làm cỡ một nghìn bước.""",
           clear=True),
        st("""<div class="box key"><b>Điều người làm nghề rút ra.</b> Chọn cấu trúc dữ liệu theo <b>thao tác chính</b> và <b>quy mô dự kiến</b>: tra theo khoá thì bản đồ, giữ thứ tự thêm vào thì danh sách.
Với năm tài khoản chọn nào cũng được; với một triệu tài khoản, chọn sai là hệ thống chậm đi hàng triệu lần ở mỗi lượt tra. Cơ sở dữ liệu lưu thêm <b>chỉ mục</b> cũng vì lý do này.</div>""",
           """Người làm nghề chọn cấu trúc dữ liệu theo thao tác chính và quy mô dự kiến: tra theo khoá thì dùng bản đồ, cần giữ thứ tự thêm vào thì dùng danh sách.
           Với năm tài khoản chọn nào cũng được, nhưng với một triệu tài khoản, chọn sai làm mỗi lượt tra chậm đi hàng triệu lần. Cơ sở dữ liệu lưu thêm chỉ mục cũng vì lý do này.""", clear=True),
    ], checks=["1000 * 1000000 == 1000000000", "1000000 // 1000 == 1000"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Viết kiểu số trần trong ngoặc nhọn.</div>'
           + code_block(kieu_tran, lines=(5, 5)) + out_block(kieu_tran, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là viết kiểu số trần trong ngoặc nhọn.
           Trình biên dịch báo kiểu không mong đợi, vì danh sách chỉ chứa đối tượng. Sửa bằng lớp bọc, chữ đầu viết hoa."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Xoá phần tử ngay trong vòng lặp duyệt.</div>'
           + code_block(xoa, lines=(5, 14)) + out_block(xoa),
           """Lỗi thứ hai là xoá phần tử ngay trong vòng lặp duyệt, ở đây là bỏ tài khoản B không hai.
           Danh sách bị đổi giữa chừng, nên ở đây bộ duyệt, tức phần máy dùng ngầm để đi qua từng phần tử trong vòng lặp duyệt, ném ngoại lệ sửa đổi đồng thời.
           Java chỉ cố gắng phát hiện chứ không hứa lần nào cũng ném: có khi vòng lặp dừng sớm và bỏ sót phần tử, nên đừng dựa vào ngoại lệ này."""),
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
           Bản đồ tra giá trị theo khoá, và lấy hoặc mặc định giúp đếm tần suất, tức mỗi loại xuất hiện bao nhiêu lần, một cách gọn gàng."""),
        st("""<div class='box key'><b>Tư duy:</b> kiểu trong ngoặc nhọn luôn là kiểu đối tượng; với số là <b>lớp bọc</b> (<code>Long</code>, <code>Integer</code>), nên so bằng
<code>equals</code>, không bằng <code>==</code>. Khoá không có thì <code>get</code> ra <code>null</code>. Không xoá phần tử trong vòng lặp duyệt.</div>""",
           """Điều cần mang theo. Kiểu trong ngoặc nhọn luôn là đối tượng, với số là lớp bọc, nên so bằng nội dung, không so địa chỉ.
           Thiếu khoá thì phương thức lấy trả giá trị rỗng. Và đừng xoá phần tử trong vòng lặp duyệt."""),
    ])
    return lesson("L09", "danh_sach_va_ban_do", "Bài 9 — Danh sách và bản đồ",
                  "curriculum/jva.yaml L09; audit/jva/verify_jva.py L09 (javac/java chạy thật); The Java Language Specification, Java SE 21 "
                  "(§5.1.7 đóng hộp, §5.1.8 mở hộp, §14.14.2 vòng lặp duyệt); Java SE 21 API: java.util.ArrayList (bộ duyệt fail-fast, "
                  "ConcurrentModificationException), java.util.HashMap, java.util.Map.getOrDefault, java.lang.Integer.valueOf (luôn đệm −128..127); dev.java/learn",
                  ["Tạo danh sách, thêm, lấy theo chỉ số, duyệt và cộng tổng", "Dùng bản đồ khoá–giá trị để tra số dư theo số tài khoản",
                   "Đếm tần suất bằng lấy hoặc mặc định", "Nêu hộp hoá và vì sao lớp bọc phải so bằng equals",
                   "Tra cứu theo khoá bằng bản đồ, có khoá thì trả số dư, không có thì báo",
                   "Đọc hiểu hàm nhỏ viết bằng mũi tên và sắp xếp danh sách bằng bộ so sánh",
                   "Dự đoán số bước mỗi lượt tra khi số tài khoản tăng gấp nghìn lần, với danh sách và với bản đồ",
                   "Viết chương trình thống kê giao dịch: đếm theo loại bằng bản đồ và sắp danh sách số tiền giảm dần"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_tra, sc_lam, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "example"), (2, "example"), (3, "formula"), (4, "pitfalls"), (5, "tracuu"), (6, "muiten"), (7, "quymo"), (8, "practice")])
