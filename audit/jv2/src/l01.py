from lib import *
from labkit import write_lab, practice_steps, practice_scene

N_LON = 1000000
TONG_LON = sum((i % 7 + 1) * 1000 for i in range(1, N_LON + 1))   # 3 999 998 000: vượt phạm vi int
TONG_NHO = sum((i % 7 + 1) * 1000 for i in range(1, 1001))        # 4 003 000

CSV_VD = "ma,loai,so_tien\n1,rut,500000\n2,nap,2000000\n3,rut,300000\n4,chuyen,1200000\n5,nap,1500000\n6,rut,700000\n"


def build():
    tham_so = prog("ThamSo", r"""
public class ThamSo {
    public static void main(String[] args) {
        String loai = args[0];                       // tham số thứ nhất
        long soTien = Long.parseLong(args[1]);       // đổi chữ thành số
        System.out.println("Loai: " + loai + ", so tien: " + soTien);
        System.out.println("Gap doi: " + soTien * 2);
    }
}""", out="Loai: rut, so tien: 250000\nGap doi: 500000", args="rut 250000")
    tham_so_loi = prog("ThamSo", tham_so["code"], out="", expect="runtime_error:NumberFormatException",
                       err='Exception in thread "main" java.lang.NumberFormatException: For input string: "abc"', args="rut abc")
    thieu_so = prog("ThamSo", tham_so["code"], out="", expect="runtime_error:ArrayIndexOutOfBoundsException",
                    err='Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 1 out of bounds for length 1',
                    args="rut")
    ban_phim = prog("BanPhim", r"""
import java.util.Scanner;

public class BanPhim {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();                  // đọc một số nguyên: số giao dịch
        long tong = 0;
        for (int i = 0; i < n; i++) {
            tong += in.nextLong();             // đọc từng số tiền
        }
        System.out.println("Tong " + n + " giao dich: " + tong);
    }
}""", out="Tong 3 giao dich: 60000", stdin="3\n10000 20000 30000\n")
    doc_csv = prog("DocCsv", r"""
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

public class DocCsv {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("gd.csv");
        Files.writeString(p, "ma,loai,so_tien\n1,rut,500000\n2,nap,2000000\n3,rut,300000\n"
                + "4,chuyen,1200000\n5,nap,1500000\n6,rut,700000\n");
        Map<String, Long> tong = new HashMap<>();
        Map<String, Integer> dem = new HashMap<>();
        try (BufferedReader br = Files.newBufferedReader(p)) {
            br.readLine();                               // bỏ dòng tiêu đề
            String dong;
            while ((dong = br.readLine()) != null) {
                String[] f = dong.split(",");            // f[0]=ma, f[1]=loai, f[2]=so_tien
                long tien = Long.parseLong(f[2]);
                tong.put(f[1], tong.getOrDefault(f[1], 0L) + tien);
                dem.put(f[1], dem.getOrDefault(f[1], 0) + 1);
            }
        }
        for (String loai : new String[]{"nap", "rut", "chuyen"}) {
            System.out.println(loai + ": " + dem.get(loai) + " giao dich, tong " + tong.get(loai));
        }
    }
}""", out="nap: 2 giao dich, tong 3500000\nrut: 3 giao dich, tong 1500000\nchuyen: 1 giao dich, tong 1200000")
    dong_cua = prog("DongCua", r"""
public class DongCua {
    static class Cua implements AutoCloseable {
        private final String ten;
        Cua(String ten) { this.ten = ten; System.out.println("mo " + ten); }
        void dung() { System.out.println("dung " + ten); }
        @Override
        public void close() { System.out.println("dong " + ten); }
    }

    public static void main(String[] args) {
        try (Cua a = new Cua("A"); Cua b = new Cua("B")) {
            a.dung();
            b.dung();
            throw new IllegalStateException("loi giua chung");
        } catch (IllegalStateException e) {
            System.out.println("bat: " + e.getMessage());
        }
    }
}""", out="mo A\nmo B\ndung A\ndung B\ndong B\ndong A\nbat: loi giua chung")
    mo_tep = prog("MoTep", r"""
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class MoTep {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("khong_co.csv");        // đường dẫn tương đối: tính từ thư mục đang chạy
        System.out.println(Files.readAllLines(p).size());
    }
}""", out="", expect="runtime_error:NoSuchFileException",
                   err='Exception in thread "main" java.nio.file.NoSuchFileException: khong_co.csv')
    sai_dong = prog("SaiDong", r"""
import java.util.Scanner;

public class SaiDong {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        String ten = in.nextLine();
        System.out.println("n=" + n + " ten=[" + ten + "]");
    }
}""", out="n=5 ten=[]", stdin="5\nan\n")
    dung_dong = prog("DungDong", r"""
import java.util.Scanner;

public class DungDong {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = Integer.parseInt(in.nextLine().trim());     // đọc cả dòng rồi mới đổi
        String ten = in.nextLine();
        System.out.println("n=" + n + " ten=[" + ten + "]");
    }
}""", out="n=5 ten=[an]", stdin="5\nan\n")
    cat_duoi = prog("CatDuoi", r"""
public class CatDuoi {
    public static void main(String[] args) {
        String dong = "7,rut,";                                   // thiếu số tiền ở cuối
        System.out.println(dong.split(",").length);               // mặc định bỏ ô rỗng cuối
        System.out.println(dong.split(",", -1).length);           // -1: giữ mọi ô
        String tieuDe = "﻿ma";                               // dấu BOM của Excel
        System.out.println(tieuDe.equals("ma") + " " + tieuDe.length());
    }
}""", out="2\n3\nfalse 3")

    lon = project("DuLieuLon", {
        "TaoFile.java": r"""
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class TaoFile {
    public static void main(String[] args) throws IOException {
        int n = Integer.parseInt(args[0]);
        try (BufferedWriter w = Files.newBufferedWriter(Path.of("lon.csv"))) {
            w.write("ma,loai,so_tien\n");
            for (int i = 1; i <= n; i++) {
                w.write(i + ",rut," + (i % 7 + 1) * 1000 + "\n");
            }
        }
        System.out.println("da ghi " + n + " dong");
    }
}""",
        "DocHet.java": r"""
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class DocHet {
    public static void main(String[] args) throws IOException {
        try {
            List<String> dong = Files.readAllLines(Path.of("lon.csv"));    // giữ MỌI dòng trong bộ nhớ
            System.out.println("doc xong " + dong.size() + " dong");
        } catch (OutOfMemoryError e) {
            System.out.println("het bo nho");
        }
    }
}""",
        "TongDong.java": r"""
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class TongDong {
    public static void main(String[] args) throws IOException {
        long tong = 0;
        try (BufferedReader br = Files.newBufferedReader(Path.of("lon.csv"))) {
            br.readLine();
            String dong;
            while ((dong = br.readLine()) != null) {          // mỗi lúc chỉ giữ MỘT dòng
                tong += Long.parseLong(dong.split(",")[2]);
            }
        }
        System.out.println("Tong: " + tong);
    }
}""",
    }, [
        ("javac TaoFile.java DocHet.java TongDong.java", ""),
        ("java TaoFile 1000", "da ghi 1000 dong"),
        ("java -Xmx32m DocHet", "doc xong 1001 dong"),
        (f"java TaoFile {N_LON}", f"da ghi {N_LON} dong"),
        ("java -Xmx32m DocHet", "het bo nho"),
        ("java -Xmx32m TongDong", f"Tong: {TONG_LON}"),
    ])
    phan_ung = project("DoiChieu", {"DocCsv.java": doc_csv["code"]}, [
        ("javac DocCsv.java", ""),
        ("java DocCsv", doc_csv["out"]),
        ('grep -c ",rut," gd.csv', "3"),
        ('grep -c ",nap," gd.csv', "2"),
    ])
    pipe = project("Ong", {"BanPhim.java": ban_phim["code"], "ThamSo.java": tham_so["code"]}, [
        ("javac BanPhim.java ThamSo.java", ""),
        ("java ThamSo rut 250000", tham_so["out"]),
        (r"printf '3\n10000 20000 30000\n' | java BanPhim", ban_phim["out"]),
    ])

    # ── lab ──
    lab = prog("TongTheoLoai", r"""
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

public class TongTheoLoai {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("giao_dich.csv");
        Files.writeString(p, "ma,loai,so_tien\n1,chuyen,850000\n2,nap,4000000\n3,chuyen,150000\n"
                + "4,rut,600000\n5,nap,250000\n6,chuyen,400000\n7,rut,900000\n");
        Map<String, Long> tong = new HashMap<>();
        Map<String, Integer> dem = new HashMap<>();
        long tatCa = 0;
        try (BufferedReader br = Files.newBufferedReader(p)) {
            br.readLine();
            String dong;
            while ((dong = br.readLine()) != null) {
                String[] f = dong.split(",");
                long tien = Long.parseLong(f[2]);
                tong.put(f[1], tong.getOrDefault(f[1], 0L) + tien);
                dem.put(f[1], dem.getOrDefault(f[1], 0) + 1);
                tatCa += tien;
            }
        }
        for (String loai : new String[]{"nap", "rut", "chuyen"}) {
            System.out.println(loai + ": " + dem.get(loai) + " giao dich, tong " + tong.get(loai));
        }
        System.out.println("Tong tat ca: " + tatCa);
    }
}""", out="nap: 2 giao dich, tong 4250000\nrut: 2 giao dich, tong 1500000\nchuyen: 3 giao dich, tong 1400000\nTong tat ca: 7150000")
    write_lab("JV2", "L01", """# Lab JV2 L01 — Tổng giao dịch theo loại

Viết chương trình `TongTheoLoai` (tệp `TongTheoLoai.java`), **không cần mạng, không cần tệp có sẵn**:

1. Dùng `Files.writeString(Path.of("giao_dich.csv"), …)` ghi ra tệp đúng nội dung dưới đây (dòng đầu là tiêu đề):

```
ma,loai,so_tien
1,chuyen,850000
2,nap,4000000
3,chuyen,150000
4,rut,600000
5,nap,250000
6,chuyen,400000
7,rut,900000
```

2. Đọc lại tệp đó bằng `try (BufferedReader …)`, bỏ dòng tiêu đề, cộng theo từng loại và đếm số giao dịch (kiểu `long` cho tiền).
3. In ba dòng theo thứ tự `nap`, `rut`, `chuyen` đúng dạng `nap: 2 giao dich, tong 4250000`, rồi một dòng `Tong tat ca: <tổng>`.

Chạy: `javac TongTheoLoai.java && java TongTheoLoai`. Chấm: `bash labs/cham.sh JV2 L01 TongTheoLoai.java`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: tổng giao dịch theo loại", practice_steps(
        st, "JV2", "L01",
        """<p><b>Đề</b>: ghi rồi đọc lại một tệp CSV bảy dòng, cộng theo loại.</p>
<ol><li>Ghi <code>giao_dich.csv</code> bằng <code>Files.writeString</code> (tiêu đề + 7 dòng như trong <code>de.md</code>).</li>
<li>Đọc lại bằng <code>try (BufferedReader …)</code>, bỏ dòng tiêu đề, cộng và đếm theo loại.</li>
<li>In theo thứ tự <code>nap</code>, <code>rut</code>, <code>chuyen</code>, rồi <code>Tong tat ca: …</code></li></ol>
<p class="note">Tiền dùng <code>long</code>. Tệp tên <code>TongTheoLoai.java</code>; dữ liệu 7 dòng ở <code>labs/JV2/L01/de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Chương trình tự ghi ra một tệp bảng bảy dòng, lấy dữ liệu từ đề bài, rồi đọc lại bằng khối thử có tài nguyên. Bỏ dòng tiêu đề, cộng tiền và đếm số giao dịch theo từng loại.
        In ba loại theo đúng thứ tự nạp, rút, chuyển, rồi in tổng tất cả. Tiền dùng kiểu số nguyên dài. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        lab["out"], "TongTheoLoai.java",
        """<div class="box key"><b>Nếu kẹt:</b> sau khi mở tệp, gọi <code>br.readLine()</code> một lần để bỏ tiêu đề; rồi <code>while ((dong = br.readLine()) != null)</code>, tách bằng <code>split(",")</code>.
Cộng bằng <code>getOrDefault</code>. Lời giải: <code>labs/JV2/L01/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, sau khi mở tệp hãy đọc một dòng để bỏ tiêu đề, rồi lặp đọc từng dòng cho tới khi hết. Tách mỗi dòng bằng dấu phẩy, và cộng dồn bằng hàm lấy giá trị mặc định.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=150), "JV2", "L01")

    # ── cảnh ──
    sc_hook = sc("hook", "hook", "Số cứng trong mã không đủ: dữ liệu thật nằm ở ngoài", [
        st(svg(1500, 330,
               panel(20, 10, 450, 300, "Số viết sẵn trong mã", C_RED),
               txt(245, 130, "long soTien = 500000;", 24, "middle", "#1f2937", True),
               txt(245, 180, "đổi số = sửa mã", 24), txt(245, 220, "= biên dịch lại", 24),
               panel(520, 10, 960, 300, "Dữ liệu từ bên ngoài", C_GREEN),
               box(555, 80, 270, 80, ["tham số", "dòng lệnh"], C_BLUE, 24), box(850, 80, 270, 80, ["bàn phím", "hoặc ống"], C_BLUE, 24),
               box(1145, 80, 300, 80, ["tệp trên đĩa", "một triệu dòng"], C_BLUE, 24),
               txt(1000, 230, "ba cửa vào, một chương trình không phải sửa", 26, "middle", "#16a34a", True)),
           """Ở bài trước, số tiền nằm cứng trong mã, muốn đổi phải sửa và biên dịch lại. Chương trình thật nhận dữ liệu từ bên ngoài, qua ba cửa. Tham số khi gõ lệnh, bàn phím hoặc đầu ra của lệnh khác, và tệp trên đĩa.
           Một ngân hàng nhận cả triệu giao dịch mỗi ngày thì chỉ có thể đi qua cửa thứ ba."""),
        st("""<div class="box key">Hôm nay: <b>nhập dữ liệu</b>. Đọc <b>tham số</b> và <b>bàn phím</b>, ghi và đọc <b>tệp văn bản</b> chuẩn mã hoá tiếng Việt,
tự động <b>đóng tài nguyên</b>, và câu hỏi của người làm nghề: đọc một tệp lớn gấp một nghìn lần thì còn chạy được không?</div>""",
           """Hôm nay ta học nhập dữ liệu. Đọc tham số và bàn phím, ghi và đọc tệp văn bản, tự động đóng tài nguyên sau khi dùng.
           Rồi câu hỏi của người làm nghề: đọc một tệp lớn gấp một nghìn lần thì chương trình còn chạy nổi không."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: chuỗi, bản đồ, ngoại lệ và nhiều tệp", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① cắt chuỗi", "<code>\"1,rut,500\".split(\",\")</code> cho mảng ba chuỗi; <code>f[2]</code> là phần tử thứ ba (đếm từ 0)"],
                  ["② bản đồ đếm", "<code>m.put(k, m.getOrDefault(k, 0) + 1)</code> cộng dồn theo khoá"],
                  ["③ ngoại lệ", "lỗi lúc chạy dừng chương trình và in dòng đầu <code>Exception in thread \"main\" …</code>; ngoại lệ có kiểm tra phải khai <code>throws</code>"],
                  ["④ biên dịch, chạy", "<code>javac Tên.java</code> rồi <code>java Tên</code>; tiền tính bằng <code>long</code> theo đồng"]]),
           """Ta ôn lại bốn điều. Cắt chuỗi bằng dấu phẩy cho ra một mảng, đếm vị trí từ không. Bản đồ cộng dồn theo khoá bằng hàm lấy giá trị mặc định.
           Lỗi lúc chạy làm chương trình dừng và in dòng báo lỗi, còn ngoại lệ có kiểm tra phải khai báo ở đầu hàm. Cuối cùng là biên dịch rồi chạy, và tiền tính bằng số nguyên dài theo đồng.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã tám thứ của việc nhập dữ liệu", [
        st(table(["viết", "nghĩa"],
                 [["<code>String[] args</code>", "mảng chứa các <b>tham số gõ sau tên lớp</b> khi chạy: <code>java ThamSo rut 250000</code>"],
                  ["<code>Long.parseLong(s)</code>", "đổi chuỗi chữ số thành <code>long</code>; sai định dạng thì ném <code>NumberFormatException</code>"],
                  ["<code>System.in</code>", "<b>đầu vào chuẩn</b>: bàn phím, hoặc kết quả lệnh đứng trước dấu <code>|</code>"],
                  ["<code>new Scanner(System.in)</code>", "bộ đọc: <code>nextInt()</code>, <code>nextLong()</code> đọc từng số, <code>nextLine()</code> đọc cả dòng"],
                  ["<code>Path.of(\"gd.csv\")</code>", "<b>đường dẫn</b>; tên không có thư mục là đường dẫn tương đối, tính từ nơi chạy lệnh"],
                  ["<code>Files.writeString(p, s)</code>", "ghi cả chuỗi ra tệp; <code>Files.newBufferedReader(p)</code> mở tệp để đọc từng dòng"],
                  ["<code>try (… ) { … }</code>", "<b>khối có tài nguyên</b>: thoát khối, kể cả khi lỗi, máy tự gọi <code>close()</code>"],
                  ["CSV", "tệp văn bản, mỗi dòng một bản ghi, các ô <b>ngăn bằng dấu phẩy</b>"]]),
           """Bảng này có tám thứ. Mảng tham số chứa các chữ gõ sau tên lớp khi chạy. Hàm đổi chuỗi thành số nguyên dài, sai định dạng thì ném ngoại lệ. Đầu vào chuẩn là bàn phím, hoặc kết quả của lệnh đứng trước dấu gạch đứng.
           Bộ đọc lấy từng số hoặc cả dòng. Đường dẫn không có thư mục là đường dẫn tương đối, tính từ nơi chạy lệnh. Có hàm ghi cả chuỗi ra tệp và hàm mở tệp để đọc từng dòng.
           Khối có tài nguyên tự đóng tài nguyên khi thoát. Và tệp bảng ngăn bằng dấu phẩy, mỗi dòng là một bản ghi.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9"]),
        st(code_block(tham_so, lines=(3, 6)) + out_block(tham_so),
           """Đây là cửa thứ nhất. Tham số thứ nhất là loại giao dịch, đếm từ không. Tham số thứ hai là chữ số, đổi sang số nguyên dài rồi nhân đôi.
           Chạy với hai tham số, rút và hai trăm năm mươi nghìn, ta thấy ngay kết quả."""),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: ba cửa vào và khối có tài nguyên", [
        st(svg(1500, 420,
               box(20, 40, 360, 90, ["tham số", "args[0], args[1]"], C_BLUE, 24, bold=True),
               box(20, 165, 360, 90, ["đầu vào chuẩn", "Scanner(System.in)"], C_BLUE, 24, bold=True),
               box(20, 290, 360, 90, ["tệp", "Files, BufferedReader"], C_BLUE, 24, bold=True),
               arrow(385, 85, 560, 190, "#2a78d6"), arrow(385, 210, 560, 210, "#2a78d6"), arrow(385, 335, 560, 230, "#2a78d6"),
               box(565, 120, 340, 180, ["chương trình", "Java"], C_GREEN, 28, bold=True),
               arrow(910, 210, 1090, 210, "#16a34a"),
               box(1095, 150, 360, 120, ["đầu ra chuẩn", "System.out.println"], C_AMBER, 24, bold=True)),
           """Hình dung chương trình như một cái máy có ba cửa vào. Tham số dòng lệnh, đầu vào chuẩn, và tệp trên đĩa. Chương trình xử lý rồi đưa kết quả ra đầu ra chuẩn, là màn hình.
           Cùng một chương trình, chỉ đổi dữ liệu ở cửa vào là cho ra kết quả khác, không phải sửa mã."""),
        st(svg(1500, 300,
               box(20, 100, 280, 90, ["① mở", "tệp, bộ đọc"], C_BLUE, 26, bold=True), arrow(305, 145, 420, 145, "#2a78d6"),
               box(425, 100, 300, 90, ["② dùng", "đọc từng dòng"], C_GREEN, 26, bold=True), arrow(730, 145, 845, 145, "#16a34a"),
               box(850, 100, 300, 90, ["③ đóng", "tự động gọi close"], C_AMBER, 26, bold=True),
               '<path d="M575,102 L575,40 L1000,40 L1000,98" fill="none" stroke="#dc2626" stroke-width="3.5" stroke-dasharray="8 6" marker-end="url(#ah)"/>',
               txt(790, 30, "lỗi xảy ra giữa chừng: vẫn đi qua bước ③", 24, "middle", "#dc2626", True),
               txt(750, 250, "đóng muộn = rò rỉ: tệp bị khoá, bộ nhớ không trả", 26, "middle", "#1f2937", True)),
           """Bước mở, dùng, đóng luôn đi theo bộ ba. Nếu quên đóng, tệp bị giữ khoá và bộ nhớ không được trả, thứ mà máy chủ chạy nhiều tháng sẽ phải trả giá.
           Khối có tài nguyên đảm bảo bước đóng luôn chạy, kể cả khi lỗi xảy ra giữa chừng, vì nó nằm trong cấu trúc của câu lệnh chứ không nhờ trí nhớ của người viết."""),
        st(code_block(dong_cua, lines=(2, 8)),
           """Ta xem thật. Lớp cửa chỉ in ra khi mở, dùng và đóng. Muốn dùng được trong khối có tài nguyên, lớp phải cam kết có hàm đóng, nên nó khai là đóng được tự động."""),
        st(code_block(dong_cua, lines=(10, 18)),
           """Khối có tài nguyên mở hai cửa, a rồi b, dùng cả hai, rồi cố tình ném lỗi giữa chừng. Ta sẽ xem thứ tự đóng.""", clear=True),
        st(out_block(dong_cua) + "<p class='note'>Đóng theo thứ tự <b>ngược lại</b> với lúc mở, và xong hết trước khi khối bắt lỗi chạy.</p>",
           """Kết quả thật. Hai cửa mở theo thứ tự a rồi b. Khi lỗi xảy ra, cả hai đều được đóng, b trước rồi a, giống tháo đồ ngược chiều lúc xếp. Chỉ sau đó khối bắt lỗi mới in ra thông báo.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: đọc một tệp bảng thành tổng theo loại", [
        st(code_block(doc_csv, lines=(15, 18)) + "<p><b>Bước 1.</b> Mở tệp, <b>bỏ dòng tiêu đề</b> bằng một lần đọc, rồi đọc tới hết.</p>",
           """Bước một, mở tệp và bỏ dòng tiêu đề, vì dòng đầu là chữ, không phải số liệu. Ta lặp lại việc đọc, mỗi lần lấy một dòng tiếp theo. Mỗi lần đọc trả về một chuỗi, và khi hết tệp thì trả về giá trị rỗng, nên điều kiện lặp là khác rỗng."""),
        st(code_block(doc_csv, lines=(19, 20)) + "<p><b>Bước 2.</b> Cắt dòng bằng dấu phẩy: <code>\"2,nap,2000000\"</code> thành <code>f[0]=\"2\"</code>, <code>f[1]=\"nap\"</code>, <code>f[2]=\"2000000\"</code>.</p>",
           """Bước hai, cắt dòng. Vì các ô ngăn bằng dấu phẩy, nên cắt tại dấu phẩy cho ra một mảng ba chuỗi. Ô thứ hai là loại, ô thứ ba là số tiền, nhưng vẫn còn là chữ.
           Ta đổi chữ thành số nguyên dài để cộng được."""),
        st(code_block(doc_csv, lines=(21, 22)) + "<p><b>Bước 3.</b> Cộng dồn theo loại: tổng mới = tổng cũ của loại đó (mặc định 0) + số tiền.</p>",
           """Bước ba, cộng dồn theo loại. Tổng mới của một loại bằng tổng cũ của loại đó cộng số tiền, và nếu loại này chưa gặp thì tổng cũ là không.
           Ta làm tương tự với bản đồ đếm, tăng số giao dịch của loại lên một."""),
        st("""<p><b>Bước 4.</b> Thử bằng số với hai dòng đầu: <code>1,rut,500000</code> và <code>2,nap,2000000</code>:</p>
$$\\text{rut} = 0 + 500\\,000 = 500\\,000 ,\\quad \\text{nap} = 0 + 2\\,000\\,000 = 2\\,000\\,000$$""",
           """Bước bốn, thử bằng số. Dòng một là rút năm trăm nghìn, loại rút chưa có nên tổng cũ bằng không, tổng mới là năm trăm nghìn. Dòng hai là nạp hai triệu, loại nạp cũng mới, tổng mới là hai triệu.
           Mỗi loại có một tổng riêng, không lẫn vào nhau.""", clear=True),
    ], checks=["0 + 500000 == 500000", "0 + 2000000 == 2000000"])
    sc_ex = sc("example", "example", "Ví dụ: sáu giao dịch, ba loại, từng phép cộng", [
        st(code_block(doc_csv, lines=(10, 12)) + "<p class='note'>Dữ liệu ghi ra <code>gd.csv</code>: tiêu đề và sáu dòng; chương trình đầy đủ ở các khung sau.</p>",
           """Ta làm trọn vẹn một ví dụ. Chương trình tự ghi ra sáu giao dịch gồm rút, nạp, rút, chuyển, nạp, rút, rồi đọc lại và cộng theo loại. Ta sẽ tự cộng bằng tay rồi so với chương trình."""),
        st("$$① \\; \\text{rut}: 500\\,000 + 300\\,000 + 700\\,000 = \\hl{1\\,500\\,000} \\;(3 \\text{ dòng})$$"
           "$$② \\; \\text{nap}: 2\\,000\\,000 + 1\\,500\\,000 = \\hl{3\\,500\\,000} \\;(2 \\text{ dòng})$$",
           """Phép cộng thứ nhất, loại rút có ba dòng, năm trăm nghìn cộng ba trăm nghìn cộng bảy trăm nghìn, bằng một triệu năm trăm nghìn.
           Phép cộng thứ hai, loại nạp có hai dòng, hai triệu cộng một triệu rưỡi, bằng ba triệu năm trăm nghìn.""", clear=True),
        st("$$③ \\; \\text{chuyen}: \\hl{1\\,200\\,000} \\;(1 \\text{ dòng})$$"
           "$$④ \\; \\text{tổng số dòng} = 3 + 2 + 1 = \\hl{6}$$"
           "$$⑤ \\; \\text{tổng tiền} = 1\\,500\\,000 + 3\\,500\\,000 + 1\\,200\\,000 = \\hl{6\\,200\\,000}$$",
           """Phép thứ ba, loại chuyển chỉ có một dòng, một triệu hai trăm nghìn. Phép thứ tư, tổng số dòng là ba cộng hai cộng một bằng sáu, đúng bằng số giao dịch.
           Phép thứ năm, cộng ba tổng lại được sáu triệu hai trăm nghìn, và cũng bằng cộng cả sáu số tiền gốc."""),
        st(out_block(doc_csv),
           """Chạy thật, ba dòng in ra khớp với các phép cộng tay. Loại nạp hai giao dịch ba triệu năm trăm nghìn, loại rút ba giao dịch một triệu năm trăm nghìn, loại chuyển một giao dịch một triệu hai trăm nghìn.""", clear=True),
        st(code_block(ban_phim, lines=(5, 11)) + term_block(pipe, 2, 3),
           """Cuối cùng là cửa bàn phím. Chương trình đọc số giao dịch, rồi đọc đúng chừng ấy số tiền. Ta không gõ tay mà dùng lệnh in rồi nối bằng dấu gạch đứng, ba số cộng lại được sáu mươi nghìn.""", clear=True),
    ], checks=["500000 + 300000 + 700000 == 1500000", "2000000 + 1500000 == 3500000", "3 + 2 + 1 == 6",
               "1500000 + 3500000 + 1200000 == 6200000", "500000 + 2000000 + 300000 + 1200000 + 1500000 + 700000 == 6200000",
               "10000 + 20000 + 30000 == 60000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm bằng lệnh của hệ điều hành", [
        st(term_block(phan_ung, 2, 4, title="Đếm số dòng mỗi loại bằng công cụ khác") +
           "<p class='note'><code>grep -c</code> đếm số dòng có chứa mẫu; chương trình Java ghi ra tệp, công cụ khác đọc lại.</p>",
           """Cách kiểm khác là dùng một công cụ hoàn toàn khác. Chương trình vừa ghi ra tệp, ta cho lệnh đếm dòng đọc lại tệp đó. Có ba dòng chứa chữ rút và hai dòng chứa chữ nạp.
           Trùng khít với số giao dịch mà chương trình Java đếm, nên đường đọc tệp của ta không bỏ sót dòng nào."""),
        st("""<p>Kiểm tổng bằng cách khác: cộng sáu số tiền gốc, không nhóm theo loại:</p>
$$500\\,000 + 2\\,000\\,000 + 300\\,000 + 1\\,200\\,000 + 1\\,500\\,000 + 700\\,000 = \\hl{6\\,200\\,000}$$""",
           """Kiểm tổng theo cách khác. Cộng thẳng sáu số tiền gốc mà không nhóm theo loại, ta được sáu triệu hai trăm nghìn. Đúng bằng tổng của ba nhóm, vậy việc nhóm theo loại không làm mất hay nhân đôi dòng nào.""", clear=True),
    ], checks=["500000 + 2000000 + 300000 + 1200000 + 1500000 + 700000 == 6200000"])
    sc_scale = sc("scale", "concept", "Khi tệp lớn gấp một nghìn, rồi một nghìn lần nữa", [
        st(table(["số dòng", "1 000", "1 000 000", "1 000 000 000"],
                 [["bộ nhớ nếu giữ mọi dòng (ước lượng ≈ 64 byte một dòng)", "64 nghìn byte", "64 triệu byte", "<b>64 tỉ byte</b>"],
                  ["bộ nhớ nếu chỉ giữ một dòng", "vài trăm byte", "vài trăm byte", "vài trăm byte"]])
           + "<p class='note'>Con số 64 byte là ước lượng cho dòng ~15 ký tự (đối tượng chuỗi, mảng ký tự, ô tham chiếu); đo thật ở khung sau.</p>",
           """Bây giờ là chuyện quy mô. Nếu đọc cả tệp rồi giữ mọi dòng trong bộ nhớ, thì bộ nhớ tăng theo số dòng. Mỗi dòng ngắn chiếm chừng sáu mươi bốn byte, con số này là ước lượng.
           Một nghìn dòng là sáu mươi bốn nghìn byte, chẳng đáng kể. Một triệu dòng là sáu mươi bốn triệu byte. Một tỉ dòng là sáu mươi bốn tỉ byte, không máy nào chứa nổi. Còn nếu chỉ giữ một dòng mỗi lúc thì bộ nhớ gần như không đổi."""),
        st(term_block(lon, 1, 3, title="Một nghìn dòng: đọc hết vẫn ổn, dù chỉ cho 32 megabyte"),
           """Ta đo thật. Tạo tệp một nghìn dòng, rồi chạy chương trình đọc hết với bộ nhớ tối đa ba mươi hai megabyte. Chạy trơn tru, đọc xong một nghìn không trăm linh một dòng, kể cả dòng tiêu đề.""", clear=True),
        st(term_block(lon, 3, 6, title="Một triệu dòng: đọc hết thì hết bộ nhớ, đọc từng dòng thì xong"),
           """Giờ ta tạo một tệp có tới một triệu dòng để thử sức. Đọc hết vào bộ nhớ với cùng giới hạn ba mươi hai megabyte thì chương trình báo hết bộ nhớ. Đọc từng dòng, mỗi lúc chỉ giữ một dòng, thì xong và cho tổng gần bốn tỉ, lớn hơn cả phạm vi của số nguyên thường, nên bắt buộc dùng số nguyên dài.
           Đánh đổi: đọc từng dòng không cho phép nhảy tới dòng bất kỳ hay đọc lại, nhưng trả bằng bộ nhớ không đổi.""", clear=True),
    ], checks=["1000 * 64 == 64000", "1000000 * 64 == 64000000", "1000000000 * 64 == 64000000000", f"sum((i % 7 + 1) * 1000 for i in range(1, 1000001)) == {TONG_LON}",
               f"{TONG_LON} > 2**31 - 1", f"sum((i % 7 + 1) * 1000 for i in range(1, 1001)) == {TONG_NHO}"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Đọc số bằng bộ đọc rồi đọc cả dòng: dòng trống bí ẩn.</div>'
           + code_block(sai_dong, lines=(5, 8)) + out_block(sai_dong) + "<p class='note'>Đầu vào: <code>5</code>, xuống dòng, <code>an</code>.</p>",
           """Lỗi thứ nhất của người mới. Đọc số nguyên rồi ngay sau đó đọc cả dòng. Hàm đọc số chỉ lấy chữ số năm, dấu xuống dòng ngay sau vẫn còn nằm lại. Lệnh đọc dòng tiếp theo nhặt đúng cái đuôi đó và trả về chuỗi rỗng, còn chữ an chưa được đọc.
           Chạy thật cho ra tên rỗng."""),
        st('<div class="box key"><b>Cách sửa:</b> luôn đọc cả dòng rồi mới đổi sang số.</div>' + code_block(dung_dong, lines=(5, 8)) + out_block(dung_dong),
           """Cách sửa là luôn đọc cả dòng rồi mới đổi sang số. Dấu xuống dòng được tiêu thụ cùng với dòng chứa số. Lần đọc sau ra đúng chữ an.""", clear=True),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Đường dẫn tương đối: tệp "không tồn tại" dù nó nằm trên đĩa.</div>'
           + code_block(mo_tep, lines=(6, 9)) + out_block(mo_tep),
           """Lỗi thứ hai là đường dẫn tương đối. Tên tệp không có thư mục được tính từ thư mục đang đứng khi chạy lệnh, chứ không phải từ nơi đặt mã nguồn. Đứng nhầm thư mục thì báo không có tệp, dù tệp nằm đâu đó trên đĩa.
           Trước khi nghi ngờ mã, hãy hỏi mình đang đứng ở thư mục nào.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tệp xuất từ Excel và ô cuối rỗng.</div>'
           + code_block(cat_duoi, lines=(3, 8)) + out_block(cat_duoi),
           """Lỗi thứ ba hay gặp ở người đã đi làm. Cắt chuỗi mặc định bỏ ô rỗng ở cuối, nên dòng thiếu số tiền cho ra hai ô thay vì ba, và truy cập ô thứ ba sẽ nổ vào lúc chạy ở máy chủ. Truyền thêm số âm một để giữ mọi ô.
           Tệp lưu từ bảng tính còn có thể mở đầu bằng một ký tự vô hình gọi là BOM. Nó làm tên cột đầu dài ba thay vì hai ký tự, nên so sánh với chữ ma cho ra sai.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Tệp <code>sao_ke.csv</code> có 2 GB, mỗi dòng <code>ngay,tien</code>. Cần tính <b>tổng</b> cột <code>tien</code>. Máy có 4 GB bộ nhớ cho chương trình.</p>
<ol><li><b>Chọn A hay B?</b> A: <code>Files.readAllLines</code> rồi cộng. B: <code>BufferedReader</code>, đọc từng dòng và cộng dồn. Vì sao?</li>
<li>Biến cộng dồn nên có kiểu gì?</li>
<li>Nếu tên cột đầu là <code>ngay</code> mà <code>equals("ngay")</code> ra <code>false</code>, nghi ngờ điều gì?</li></ol>""",
           """Bây giờ tới phần bạn tự làm. Một tệp sao kê hai gigabyte, mỗi dòng có ngày và tiền, cần tính tổng cột tiền, máy có bốn gigabyte bộ nhớ. Hãy chọn giữa đọc hết vào bộ nhớ và đọc từng dòng, và giải thích vì sao.
           Biến cộng dồn nên có kiểu gì. Và nếu so sánh tên cột đầu ra sai thì nghi ngờ điều gì. Hãy dừng video và tự làm.""", pause=25),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "<b>B</b>: đọc từng dòng", "A giữ ≈ 64 byte × số dòng ≫ 2 GB nên nhiều khả năng hết bộ nhớ; B chỉ giữ một dòng"],
                  ["2", "<code>long</code>", "tổng có thể vượt 2 147 483 647"],
                  ["3", "dấu BOM hoặc khoảng trắng đầu ô", "ký tự vô hình làm chuỗi dài hơn; thử <code>length()</code>"]]),
           """Đáp án, chọn phương án B, đọc từng dòng, vì phương án A giữ nhiều bộ nhớ hơn cả kích thước tệp. Biến cộng dồn dùng kiểu số nguyên dài, vì tổng có thể vượt phạm vi của số nguyên thường.
           Còn so sánh sai tên cột thì nghi ký tự vô hình ở đầu, hãy in độ dài của chuỗi để thấy.""",
           focus=["1.2", "1.3", "1.4"]),
        st("""<p>Tính số: giả sử mỗi bản ghi dài 20 byte, tệp 2 GB có $2\\,000\\,000\\,000 / 20 = 10^8$ dòng. Giữ hết:</p>
$$10^8 \\times 64 = \\hl{6{,}4 \\times 10^9} \\text{ byte} \\approx 6{,}4 \\text{ GB} > 4 \\text{ GB}$$""",
           """Ta tính cho chắc. Giả sử mỗi dòng hai mươi byte, tệp hai gigabyte có một trăm triệu dòng. Giữ hết thì cần một trăm triệu nhân sáu mươi bốn, bằng sáu phẩy bốn gigabyte, lớn hơn bốn gigabyte mà máy có.
           Vậy phương án A chắc chắn hết bộ nhớ, còn phương án B thì không.""", clear=True),
    ], checks=["2 * 10**9 // 20 == 10**8", "10**8 * 64 == 6400000000", "10**8 * 64 > 4 * 10**9"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("ba cửa vào: tham số, đầu vào chuẩn, tệp", "đổi chữ thành số: parseLong", "mở – dùng – đóng", "cắt dòng, cộng dồn theo loại",
                 "bộ nhớ ≈ số dòng × 64 byte", "tệp lớn thì đọc từng dòng"),
           """Tổng kết chuỗi logic. Dữ liệu vào qua ba cửa là tham số, đầu vào chuẩn và tệp. Chữ phải được đổi thành số trước khi tính. Tài nguyên luôn đi theo bộ ba mở, dùng, đóng.
           Cắt dòng rồi cộng dồn theo loại. Giữ mọi dòng thì bộ nhớ tăng theo số dòng. Vì thế tệp lớn thì đọc từng dòng."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi đọc dữ liệu từ bên ngoài, hỏi bốn câu: dữ liệu <b>lớn đến đâu</b> và có cần giữ hết trong bộ nhớ không,
ô nào có thể <b>rỗng hay sai định dạng</b>, ai <b>đóng</b> tài nguyên, và đường dẫn tính từ <b>thư mục nào</b>.</div>""",
           """Điều cần mang theo. Trước khi đọc dữ liệu từ bên ngoài, hãy hỏi bốn câu. Dữ liệu lớn đến đâu, và có cần giữ hết trong bộ nhớ không.
           Ô nào có thể rỗng hay sai định dạng. Ai chịu trách nhiệm đóng tài nguyên. Và đường dẫn được tính từ thư mục nào."""),
    ])
    return lesson("L01", "nhap_du_lieu_tep", "Bài 1 — Nhập dữ liệu: tham số, bàn phím, tệp văn bản",
                  "curriculum/jv2.yaml L01; audit/jv2/verify_jv2.py L01 (javac/java chạy thật, JDK 21; -Xmx32m cho phép đo bộ nhớ); "
                  "java.nio.file.Files và java.util.Scanner (Java SE 21 API); JLS §14.20.3 (try-with-resources: đóng theo thứ tự ngược); "
                  "String.split(regex, limit) (Java SE 21 API: limit âm giữ ô rỗng cuối); RFC 4180 (định dạng CSV); dev.java/learn",
                  ["Đọc tham số dòng lệnh và dữ liệu từ bàn phím, đổi chữ thành số",
                   "Mô tả vì sao tài nguyên phải được đóng và khối có tài nguyên đóng theo thứ tự nào",
                   "Tính tổng theo loại từ tệp bảng ngăn bằng dấu phẩy bằng cắt dòng và bản đồ cộng dồn",
                   "Nhận ra khi nào đọc cả tệp vào bộ nhớ gãy và chuyển sang đọc từng dòng",
                   "Viết chương trình ghi rồi đọc lại tệp bảng và in tổng theo loại"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "example"), (2, "intuition"), (3, "example"), (4, "scale"), (5, "practice")])
