from lib import *
from labkit import write_lab, practice_steps, practice_scene

N_LON = 1000000
LOAI = ["chuyen", "nap", "rut"]
_tong = {"rut": 0, "nap": 0, "chuyen": 0}
for _i in range(1, N_LON + 1):
    _tong[("rut", "nap", "chuyen")[_i % 3]] += (_i % 7 + 1) * 1000
TONG_LON = "{" + ", ".join(f"{k}={_tong[k]}" for k in LOAI) + "}"


def build():
    ham = prog("HamLaGiaTri", r"""
import java.util.function.Function;
import java.util.function.Predicate;

public class HamLaGiaTri {
    public static void main(String[] args) {
        Predicate<Long> lon = so -> so > 1000000;      // nhận một số, trả đúng hoặc sai
        Function<Long, Long> phi = so -> so / 1000;    // nhận số tiền, trả phí
        System.out.println(lon.test(2500000L));
        System.out.println(lon.test(800000L));
        System.out.println(phi.apply(2500000L));
    }
}""", out="true\nfalse\n2500")
    xep = prog("XepNgan", r"""
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class XepNgan {
    record GiaoDich(int ma, String loai, long soTien) {}

    public static void main(String[] args) {
        List<GiaoDich> ds = new ArrayList<>(List.of(
                new GiaoDich(1, "rut", 500000), new GiaoDich(2, "nap", 2000000),
                new GiaoDich(3, "rut", 300000), new GiaoDich(4, "chuyen", 1200000),
                new GiaoDich(5, "nap", 1500000), new GiaoDich(6, "rut", 700000)));
        ds.sort(Comparator.comparing(GiaoDich::loai)
                .thenComparing(Comparator.comparingLong(GiaoDich::soTien).reversed()));
        for (GiaoDich g : ds) {
            System.out.print(g.ma() + " ");
        }
        System.out.println();
    }
}""", out="4 2 5 6 1 3 ")
    thong_ke = prog("ThongKe", r"""
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class ThongKe {
    record GiaoDich(int ma, String loai, long soTien) {}

    public static void main(String[] args) {
        List<GiaoDich> ds = List.of(
                new GiaoDich(1, "rut", 500000), new GiaoDich(2, "nap", 2000000),
                new GiaoDich(3, "rut", 300000), new GiaoDich(4, "chuyen", 1200000),
                new GiaoDich(5, "nap", 1500000), new GiaoDich(6, "rut", 700000),
                new GiaoDich(7, "chuyen", 350000), new GiaoDich(8, "nap", 900000));
        long lon = ds.stream().filter(g -> g.soTien() >= 1000000).mapToLong(GiaoDich::soTien).sum();
        Map<String, Long> tong = ds.stream().collect(
                Collectors.groupingBy(GiaoDich::loai, TreeMap::new, Collectors.summingLong(GiaoDich::soTien)));
        System.out.println(lon);
        System.out.println(tong);
        System.out.println(ds.stream().map(GiaoDich::loai).distinct().sorted().toList());
    }
}""", out="4700000\n{chuyen=1550000, nap=4400000, rut=1500000}\n[chuyen, nap, rut]")
    vong = prog("ThongKeVong", r"""
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class ThongKeVong {
    record GiaoDich(int ma, String loai, long soTien) {}

    public static void main(String[] args) {
        List<GiaoDich> ds = List.of(
                new GiaoDich(1, "rut", 500000), new GiaoDich(2, "nap", 2000000),
                new GiaoDich(3, "rut", 300000), new GiaoDich(4, "chuyen", 1200000),
                new GiaoDich(5, "nap", 1500000), new GiaoDich(6, "rut", 700000),
                new GiaoDich(7, "chuyen", 350000), new GiaoDich(8, "nap", 900000));
        long lon = 0;
        Map<String, Long> tong = new TreeMap<>();
        for (GiaoDich g : ds) {
            if (g.soTien() >= 1000000) {
                lon += g.soTien();
            }
            tong.put(g.loai(), tong.getOrDefault(g.loai(), 0L) + g.soTien());
        }
        System.out.println(lon);
        System.out.println(tong);
    }
}""", out="4700000\n{chuyen=1550000, nap=4400000, rut=1500000}")
    luoi = prog("Luoi", r"""
import java.util.List;
import java.util.stream.Stream;

public class Luoi {
    public static void main(String[] args) {
        Stream<Integer> s = List.of(1, 2, 3, 4).stream()
                .filter(x -> { System.out.println("loc " + x); return x % 2 == 0; })
                .map(x -> { System.out.println("nhan " + x); return x * 10; });
        System.out.println("chua chay gi");
        System.out.println(s.toList());
    }
}""", out="chua chay gi\nloc 1\nloc 2\nnhan 2\nloc 3\nloc 4\nnhan 4\n[20, 40]")
    ngan_mach = prog("NganMach", r"""
import java.util.stream.IntStream;

public class NganMach {
    public static void main(String[] args) {
        long[] dem = {0};                                  // mảng một ô: đếm số phần tử đã duyệt
        IntStream.rangeClosed(1, 1000000)
                .peek(i -> dem[0]++)
                .filter(i -> i % 10 == 0)
                .findFirst();                              // dừng ngay khi thấy phần tử đầu
        System.out.println("da duyet " + dem[0] + " phan tu");
    }
}""", out="da duyet 10 phan tu")
    cap_bien = prog("CapBien", r"""
import java.util.List;

public class CapBien {
    public static void main(String[] args) {
        long tong = 0;
        for (int x : List.of(1, 2, 3)) {
            Runnable r = () -> System.out.println(tong + x);
            tong += x;
        }
    }
}""", expect="compile_error:local variables referenced from a lambda expression must be final or effectively final",
                    err="error: local variables referenced from a lambda expression must be final or effectively final\n            Runnable r = () -> System.out.println(tong + x);…\n                                                  ^")
    dung_hai = prog("DungHai", r"""
import java.util.List;
import java.util.stream.Stream;

public class DungHai {
    public static void main(String[] args) {
        Stream<Integer> s = List.of(1, 2, 3).stream();
        System.out.println(s.count());
        System.out.println(s.count());                     // dùng lại đường ống đã chạy
    }
}""", out="3", expect="runtime_error:IllegalStateException",
                    err='Exception in thread "main" java.lang.IllegalStateException: stream has already been …')
    trung_khoa = prog("TrungKhoa", r"""
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class TrungKhoa {
    record GiaoDich(int ma, String loai, long soTien) {}

    public static void main(String[] args) {
        List<GiaoDich> ds = List.of(new GiaoDich(1, "nap", 2000000),
                new GiaoDich(2, "rut", 500000), new GiaoDich(3, "nap", 1500000));
        Map<String, Long> m = ds.stream().collect(
                Collectors.toMap(GiaoDich::loai, GiaoDich::soTien));       // hai dòng cùng loại nap
        System.out.println(m);
    }
}""", out="", expect="runtime_error:IllegalStateException",
                      err='Exception in thread "main" java.lang.IllegalStateException: Duplicate key nap (…)')
    sua_khoa = prog("SuaKhoa", r"""
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class SuaKhoa {
    record GiaoDich(int ma, String loai, long soTien) {}

    public static void main(String[] args) {
        List<GiaoDich> ds = List.of(new GiaoDich(1, "nap", 2000000),
                new GiaoDich(2, "rut", 500000), new GiaoDich(3, "nap", 1500000));
        Map<String, Long> m = ds.stream().collect(
                Collectors.toMap(GiaoDich::loai, GiaoDich::soTien, Long::sum, TreeMap::new));
        System.out.println(m);
    }
}""", out="{nap=3500000, rut=500000}")

    lon = project("ThongKeLon", {
        "TaoFile.java": r"""
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class TaoFile {
    public static void main(String[] args) throws IOException {
        int n = Integer.parseInt(args[0]);
        String[] loai = {"rut", "nap", "chuyen"};
        try (BufferedWriter w = Files.newBufferedWriter(Path.of("lon.csv"))) {
            w.write("ma,loai,so_tien\n");
            for (int i = 1; i <= n; i++) {
                w.write(i + "," + loai[i % 3] + "," + (i % 7 + 1) * 1000 + "\n");
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
            List<String> dong = Files.readAllLines(Path.of("lon.csv"));
            System.out.println(dong.stream().skip(1).count());
        } catch (OutOfMemoryError e) {
            System.out.println("het bo nho");
        }
    }
}""",
        "ThongKeLon.java": r"""
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class ThongKeLon {
    public static void main(String[] args) throws IOException {
        try (Stream<String> dong = Files.lines(Path.of("lon.csv"))) {     // đọc LƯỜI từng dòng
            Map<String, Long> tong = dong.skip(1).map(d -> d.split(",")).collect(
                    Collectors.groupingBy(f -> f[1], TreeMap::new,
                            Collectors.summingLong(f -> Long.parseLong(f[2]))));
            System.out.println(tong);
        }
    }
}""",
    }, [
        ("javac TaoFile.java DocHet.java ThongKeLon.java", ""),
        (f"java TaoFile {N_LON}", f"da ghi {N_LON} dong"),
        ("java -Xmx32m DocHet", "het bo nho"),
        ("java -Xmx32m ThongKeLon", TONG_LON),
    ])

    lab = prog("ThongKeStream", r"""
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class ThongKeStream {
    record GiaoDich(int ma, String loai, long soTien) {}

    public static void main(String[] args) {
        List<GiaoDich> ds = List.of(
                new GiaoDich(1, "nap", 3000000), new GiaoDich(2, "rut", 450000),
                new GiaoDich(3, "chuyen", 800000), new GiaoDich(4, "rut", 1200000),
                new GiaoDich(5, "nap", 200000), new GiaoDich(6, "chuyen", 1500000),
                new GiaoDich(7, "rut", 500000), new GiaoDich(8, "nap", 650000));
        long rutLon = ds.stream().filter(g -> g.loai().equals("rut") && g.soTien() >= 500000)
                .mapToLong(GiaoDich::soTien).sum();
        Map<String, Long> dem = ds.stream().collect(
                Collectors.groupingBy(GiaoDich::loai, TreeMap::new, Collectors.counting()));
        Map<String, Long> tong = ds.stream().collect(
                Collectors.groupingBy(GiaoDich::loai, TreeMap::new, Collectors.summingLong(GiaoDich::soTien)));
        Map<String, Long> tongVong = new TreeMap<>();
        for (GiaoDich g : ds) {
            tongVong.merge(g.loai(), g.soTien(), Long::sum);
        }
        System.out.println("Rut tu 500000: " + rutLon);
        System.out.println("Dem: " + dem);
        System.out.println("Tong: " + tong);
        System.out.println("Khop vong lap: " + tong.equals(tongVong));
    }
}""", out="Rut tu 500000: 1700000\nDem: {chuyen=2, nap=3, rut=3}\nTong: {chuyen=2300000, nap=3850000, rut=2150000}\nKhop vong lap: true")
    write_lab("JV2", "L03", """# Lab JV2 L03 — Thống kê bằng Stream, đối chiếu với vòng lặp

Viết chương trình `ThongKeStream` (tệp `ThongKeStream.java`) với `record GiaoDich(int ma, String loai, long soTien) {}` và tám giao dịch
(`ma`, `loai`, `soTien`): `(1, nap, 3000000)`, `(2, rut, 450000)`, `(3, chuyen, 800000)`, `(4, rut, 1200000)`, `(5, nap, 200000)`, `(6, chuyen, 1500000)`, `(7, rut, 500000)`, `(8, nap, 650000)`.

1. Bằng **Stream** (`filter`, `mapToLong`, `sum`): tổng tiền các giao dịch loại `rut` có `soTien >= 500000`.
2. Bằng `Collectors.groupingBy(..., TreeMap::new, Collectors.counting())`: số giao dịch theo loại.
3. Bằng `groupingBy` với `Collectors.summingLong`: tổng tiền theo loại.
4. Bằng **vòng lặp** `for` và `TreeMap.merge(khoá, số, Long::sum)`: tổng tiền theo loại; in `true` nếu bản đồ này `equals` bản đồ ở bước 3.

In bốn dòng đúng dạng:
```
Rut tu 500000: <số>
Dem: {…}
Tong: {…}
Khop vong lap: true
```

Chạy: `javac ThongKeStream.java && java ThongKeStream`. Chấm: `bash labs/cham.sh JV2 L03 ThongKeStream.java`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: thống kê tám giao dịch bằng Stream", practice_steps(
        st, "JV2", "L03",
        """<p><b>Đề</b>: tám giao dịch (số liệu trong <code>de.md</code>), làm bốn việc.</p>
<ol><li>Stream: tổng tiền loại <code>rut</code> mà <code>soTien &gt;= 500000</code>.</li>
<li><code>groupingBy</code> + <code>counting()</code>: số giao dịch theo loại (<code>TreeMap</code>).</li>
<li><code>groupingBy</code> + <code>summingLong</code>: tổng tiền theo loại.</li>
<li>Vòng <code>for</code> + <code>merge</code>: cùng tổng đó; in <code>true</code> nếu <code>equals</code>.</li></ol>
<p class="note">Tệp <code>ThongKeStream.java</code>; bốn dòng in theo mẫu ở <code>de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Có tám giao dịch cho trong đề bài. Hãy dùng đường ống để tính tổng tiền các giao dịch rút từ năm trăm nghìn trở lên, rồi đếm số giao dịch theo loại và tính tổng tiền theo loại bằng hàm gom nhóm.
        Sau đó tự viết vòng lặp tính tổng theo loại và kiểm hai bản đồ có bằng nhau không. In bốn dòng theo mẫu. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        lab["out"], "ThongKeStream.java",
        """<div class="box key"><b>Nếu kẹt:</b> <code>ds.stream().filter(g -&gt; … ).mapToLong(GiaoDich::soTien).sum()</code>. Gom nhóm: <code>Collectors.groupingBy(GiaoDich::loai, TreeMap::new, Collectors.counting())</code>.
Vòng lặp: <code>m.merge(g.loai(), g.soTien(), Long::sum)</code>. Lời giải: <code>labs/JV2/L03/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, đường ống đầu tiên là lọc, đổi sang số nguyên dài, rồi cộng. Gom nhóm dùng hàm gom nhóm theo loại, với bản đồ có thứ tự và hàm đếm hoặc hàm cộng. Trong vòng lặp, dùng hàm trộn của bản đồ với phép cộng.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=180), "JV2", "L03")

    sc_hook = sc("hook", "hook", "Mười dòng vòng lặp, hay một dòng nói điều mình muốn?", [
        st(code_block(vong, lines=(14, 21)) + out_block(vong),
           """Ở bài trước, ta thống kê giao dịch bằng vòng lặp. Vòng lặp nói máy phải làm thế nào, mở một biến tổng, duyệt từng phần tử, kiểm điều kiện, cộng dồn. Mười dòng, ba chỗ dễ lỗi, và đọc xong vẫn phải đoán mục đích.
           Kết quả là tổng các giao dịch từ một triệu trở lên, và tổng theo từng loại."""),
        st(code_block(thong_ke, lines=(15, 17)),
           """Cùng việc đó, cách kể mục đích gọn hơn nhiều. Lọc ra giao dịch từ một triệu, đổi sang số tiền, cộng lại. Gom các giao dịch theo loại rồi cộng tiền của từng loại. Dòng nào nói đúng điều mình muốn, và đây là đường ống, kiểu viết thống trị trong mã Java hiện đại.""", clear=True),
        st("""<div class="box key">Hôm nay: <b>hàm là một giá trị</b> có thể truyền đi (hàm ngắn không tên, tham chiếu hàm), và <b>đường ống Stream</b> lọc, biến đổi, gom nhóm.
Kèm câu hỏi của người làm nghề: đường ống chạy <b>khi nào</b>, và với tệp lớn gấp một nghìn lần thì còn chạy nổi không?</div>""",
           """Hôm nay ta học hàm là một giá trị có thể truyền đi, và đường ống để lọc, biến đổi, gom nhóm. Kèm câu hỏi của người làm nghề, đường ống chạy khi nào, và với tệp lớn gấp một nghìn lần thì còn chạy nổi không.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: giao diện, bộ so sánh và bản đồ", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① giao diện", "một giao diện đòi các hàm; lớp cài hết thì dùng được, ví dụ bộ so sánh có <code>compare(a, b)</code>"],
                  ["② bản ghi", "<code>record GiaoDich(int ma, String loai, long soTien)</code> có sẵn <code>loai()</code>, <code>soTien()</code>"],
                  ["③ bản đồ", "<code>TreeMap</code> giữ khoá theo thứ tự; <code>getOrDefault</code> cộng dồn theo khoá"],
                  ["④ đọc từng dòng", "mở tệp trong khối có tài nguyên và chỉ giữ một dòng mỗi lúc"]]),
           """Ta ôn lại bốn điều. Giao diện đòi một số hàm, lớp cài đủ thì dùng được, như bộ so sánh đòi hàm so sánh. Bản ghi tự có các hàm đọc theo tên trường. Bản đồ có thứ tự giữ khoá theo thứ tự chữ cái, và hàm lấy mặc định giúp cộng dồn.
           Cuối cùng, tệp lớn phải đọc từng dòng trong khối có tài nguyên, mỗi lúc chỉ giữ một dòng.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã tám ký hiệu của hàm ngắn và đường ống", [
        st(table(["viết", "nghĩa"],
                 [["<code>so -&gt; so &gt; 1000000</code>", "<b>hàm ngắn không tên</b>: bên trái mũi tên là tham số, bên phải là kết quả trả về"],
                  ["<code>Predicate&lt;Long&gt;</code>", "giao diện của hàm nhận một giá trị, trả <b>đúng/sai</b>; gọi bằng <code>.test(x)</code>"],
                  ["<code>Function&lt;A, B&gt;</code>", "giao diện của hàm nhận <code>A</code>, trả <code>B</code>; gọi bằng <code>.apply(x)</code>"],
                  ["<code>GiaoDich::soTien</code>", "<b>tham chiếu hàm</b>: cách viết tắt của <code>g -&gt; g.soTien()</code>"],
                  ["<code>ds.stream()</code>", "mở một <b>đường ống</b> (Stream) đi qua từng phần tử của danh sách"],
                  ["<code>filter</code> / <code>map</code>", "bước giữa: giữ phần tử thoả điều kiện / đổi mỗi phần tử thành giá trị khác"],
                  ["<code>sum</code> / <code>collect</code> / <code>toList</code>", "bước <b>cuối</b>: lấy kết quả ra; không có bước cuối thì đường ống <b>không chạy</b>"],
                  ["<code>groupingBy(khoá, …)</code>", "gom các phần tử cùng khoá vào một nhóm, rồi tính tiếp trong từng nhóm"]]),
           """Bảng này có tám thứ. Hàm ngắn không tên có tham số bên trái mũi tên và kết quả bên phải. Hai giao diện hay dùng nhất là hàm trả đúng sai, và hàm biến đổi từ kiểu này sang kiểu kia. Tham chiếu hàm là cách viết tắt của hàm ngắn chỉ gọi một hàm có sẵn.
           Mở đường ống từ danh sách. Bước giữa như lọc và biến đổi chỉ khai báo việc cần làm. Bước cuối mới lấy kết quả, và nếu không có bước cuối thì đường ống không chạy. Cuối cùng là gom nhóm theo khoá.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]),
        st(code_block(ham, lines=(6, 10)) + out_block(ham),
           """Ta thử ngay. Hàm thứ nhất nhận một số, trả đúng nếu lớn hơn một triệu. Hàm thứ hai nhận số tiền, chia một nghìn để ra phí. Hai triệu rưỡi thì đúng, tám trăm nghìn thì sai, và phí của hai triệu rưỡi là hai nghìn năm trăm.
           Cả hai hàm đều là giá trị nằm trong một biến, ta có thể truyền chúng cho hàm khác.""", clear=True),
    ], checks=["2500000 > 1000000", "not (800000 > 1000000)", "2500000 // 1000 == 2500"])
    sc_int = sc("intuition", "intuition", "Hình dung: băng chuyền, mỗi phần tử đi hết các trạm", [
        st(svg(1500, 330,
               box(20, 120, 220, 90, ["danh sách", "8 giao dịch"], C_GRAY, 24, bold=True), arrow(245, 165, 330, 165, "#475569"),
               box(335, 120, 240, 90, ["filter", "soTien ≥ 1 triệu"], C_BLUE, 24, bold=True), arrow(580, 165, 665, 165, "#475569"),
               box(670, 120, 240, 90, ["mapToLong", "lấy số tiền"], C_BLUE, 24, bold=True), arrow(915, 165, 1000, 165, "#475569"),
               box(1005, 120, 220, 90, ["sum", "BƯỚC CUỐI"], C_GREEN, 24, bold=True), arrow(1230, 165, 1300, 165, "#16a34a"),
               box(1305, 120, 180, 90, ["4 700 000", "kết quả"], C_AMBER, 24, bold=True),
               txt(750, 60, "mỗi phần tử đi hết các trạm rồi mới tới phần tử sau", 28, "middle", "#1f2937", True),
               txt(750, 290, "không có trạm cuối thì băng chuyền không chạy", 26, "middle", "#dc2626", True)),
           """Hình dung đường ống như một băng chuyền. Phần tử đi qua trạm lọc, rồi trạm biến đổi, rồi tới trạm cuối để lấy kết quả. Điều quan trọng là mỗi phần tử đi hết các trạm rồi mới tới phần tử sau, chứ không phải trạm một xử lý hết rồi mới sang trạm hai.
           Và nếu không có trạm cuối thì băng chuyền không bao giờ chạy."""),
        st(code_block(luoi, lines=(6, 10)),
           """Ta kiểm tra bằng cách cho mỗi trạm in một dòng. Danh sách một, hai, ba, bốn. Trạm lọc giữ số chẵn, trạm biến đổi nhân mười. Ta in ra dòng chưa chạy gì trước khi gọi bước cuối, để xem đường ống thực sự bắt đầu lúc nào.""", clear=True),
        st(out_block(luoi) + "<p class='note'>Dòng \"chua chay gi\" in <b>trước</b> mọi dòng \"loc\"; rồi từng phần tử đi hết các trạm: 1 bị loại ngay, 2 đi tiếp tới \"nhan\".</p>",
           """Kết quả thật. Dòng chưa chạy gì xuất hiện trước tiên, nghĩa là hai trạm đầu chỉ khai báo. Khi gọi bước cuối, phần tử một vào trạm lọc và bị loại, phần tử hai qua lọc rồi qua trạm biến đổi, rồi mới tới phần tử ba.
           Kết quả cuối là hai mươi và bốn mươi.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: từ vòng lặp sang đường ống", [
        st(code_block(vong, lines=(14, 21)) + "<p><b>Bước 1.</b> Tách vòng lặp thành các <b>việc rời nhau</b>: lọc (<code>if</code>), lấy tiền, cộng (<code>lon +=</code>).</p>",
           """Bước một, nhìn vào vòng lặp và tách thành những việc rời nhau. Lệnh rẽ nhánh là việc lọc, lấy số tiền là việc biến đổi, phép cộng dồn là việc gom lại thành một số. Ba việc lẫn trong một khối nên ta khó thấy từng việc.""", clear=True),
        st("""<p><b>Bước 2.</b> Mỗi việc thành một trạm, nối bằng dấu chấm:</p>
<p><code>if (g.soTien() &gt;= 1000000)</code> &rarr; <code>.filter(g -&gt; g.soTien() &gt;= 1000000)</code></p>
<p><code>lon += g.soTien()</code> &rarr; <code>.mapToLong(GiaoDich::soTien).sum()</code></p>""",
           """Bước hai, mỗi việc thành một trạm. Điều kiện của lệnh rẽ nhánh trở thành hàm ngắn đưa cho trạm lọc. Phép cộng dồn trở thành trạm lấy số tiền rồi trạm cộng. Biến tổng và vòng lặp biến mất, vì đường ống tự lo.""", clear=True),
        st("""<p><b>Bước 3.</b> Gom nhóm: <code>groupingBy(khoá, bộ-gom-trong-nhóm)</code>. Với khoá = loại, bộ gom = <code>summingLong(soTien)</code>:</p>
<p><code>tong.put(loai, tong.getOrDefault(loai, 0L) + soTien)</code> &harr; <code>groupingBy(GiaoDich::loai, …, summingLong(GiaoDich::soTien))</code></p>""",
           """Bước ba, gom nhóm. Dòng cộng dồn theo khoá bằng bản đồ chính là việc mà hàm gom nhóm làm thay. Khoá là loại giao dịch, còn cách gom trong nhóm là cộng số tiền. Hai cách viết cho cùng một kết quả.""", clear=True),
        st("""<p><b>Bước 4.</b> Thử bằng số với <b>nap</b>: ba dòng <code>2 000 000</code>, <code>1 500 000</code>, <code>900 000</code>:</p>
$$\\text{nap} = 2\\,000\\,000 + 1\\,500\\,000 + 900\\,000 = \\hl{4\\,400\\,000}$$
<p>Đúng bằng giá trị <code>nap=4400000</code> trong kết quả ✓</p>""",
           """Bước bốn, thử bằng số với loại nạp. Có ba giao dịch nạp, hai triệu, một triệu rưỡi và chín trăm nghìn. Cộng lại được bốn triệu bốn trăm nghìn, nên đúng bằng giá trị mà đường ống sẽ in ra cho loại nạp.""", clear=True),
    ], checks=["2000000 + 1500000 + 900000 == 4400000"])
    sc_ex = sc("example", "example", "Ví dụ: tám giao dịch, ba câu hỏi, hai cách viết", [
        st(code_block(thong_ke, lines=(10, 14)) + "<p class='note'>Tám giao dịch: rút, nạp, rút, chuyển, nạp, rút, chuyển, nạp.</p>",
           """Ta làm trọn vẹn một ví dụ với tám giao dịch gồm ba loại. Ba câu hỏi: tổng các giao dịch từ một triệu trở lên, tổng theo loại, và danh sách các loại. Ta tính tay trước.""", clear=True),
        st("$$① \\; \\text{từ 1 triệu}: 2\\,000\\,000 + 1\\,200\\,000 + 1\\,500\\,000 = \\hl{4\\,700\\,000}$$"
           "<p>(900 000 và các số nhỏ hơn bị loại.)</p>",
           """Phép tính thứ nhất, các giao dịch từ một triệu trở lên là hai triệu, một triệu hai trăm nghìn và một triệu rưỡi. Cộng lại được bốn triệu bảy trăm nghìn. Giao dịch chín trăm nghìn không đủ nên bị loại.""", clear=True),
        st("$$② \\; \\text{rut}: 500\\,000 + 300\\,000 + 700\\,000 = \\hl{1\\,500\\,000}$$"
           "$$③ \\; \\text{nap}: 2\\,000\\,000 + 1\\,500\\,000 + 900\\,000 = \\hl{4\\,400\\,000}$$"
           "$$④ \\; \\text{chuyen}: 1\\,200\\,000 + 350\\,000 = \\hl{1\\,550\\,000}$$",
           """Phép tính thứ hai, loại rút cộng lại được một triệu rưỡi. Phép thứ ba, loại nạp được bốn triệu bốn trăm nghìn. Phép thứ tư, loại chuyển được một triệu năm trăm năm mươi nghìn.""", clear=True),
        st("$$⑤ \\; \\text{tổng theo loại} = 1\\,500\\,000 + 4\\,400\\,000 + 1\\,550\\,000 = \\hl{7\\,450\\,000}$$"
           "<p>= tổng cả tám giao dịch ✓ (không nhóm nào mất hay bị tính hai lần)</p>",
           """Phép thứ năm, cộng ba tổng theo loại được bảy triệu bốn trăm năm mươi nghìn, đúng bằng tổng của cả tám giao dịch. Nghĩa là không nhóm nào bị mất, cũng không giao dịch nào bị tính hai lần.""", clear=True),
        st(code_block(thong_ke, lines=(15, 20)) + out_block(thong_ke),
           """Chạy thật bằng đường ống, ba dòng in ra khớp với ba phép tính tay. Tổng từ một triệu là bốn triệu bảy trăm nghìn, tổng theo loại đúng như đã cộng, và danh sách các loại theo thứ tự chữ cái.
           Bản vòng lặp cho đúng hai dòng đầu y hệt.""", clear=True),
    ], checks=["2000000 + 1200000 + 1500000 == 4700000", "500000 + 300000 + 700000 == 1500000", "1200000 + 350000 == 1550000",
               "1500000 + 4400000 + 1550000 == 7450000",
               "500000 + 2000000 + 300000 + 1200000 + 1500000 + 700000 + 350000 + 900000 == 7450000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: so hai cách viết", [
        st(out_block(vong) + "<p class='note'>Bản vòng lặp <code>ThongKeVong</code> in <b>y hệt</b> hai dòng đầu của bản đường ống. Hai cách viết khác nhau hoàn toàn, nên đây là một phép đối chứng độc lập.</p>",
           """Cách kiểm thứ nhất là viết cùng bài toán theo cách cũ rồi so. Bản vòng lặp in đúng hai dòng giống bản đường ống, bốn triệu bảy trăm nghìn và tổng theo loại. Hai cách viết hoàn toàn khác nhau mà ra cùng kết quả, nên ta có thêm lòng tin."""),
        st("""<p>Kiểm tính chất: tổng theo ba nhóm phải <b>bằng</b> tổng cả danh sách; tổng từ 1 triệu trở lên <b>không vượt</b> tổng cả danh sách:</p>
$$4\\,700\\,000 \\le 7\\,450\\,000 \\quad\\text{và}\\quad 1\\,550\\,000 + 4\\,400\\,000 + 1\\,500\\,000 = 7\\,450\\,000$$""",
           """Cách kiểm thứ hai là kiểm tính chất. Tổng của ba nhóm phải bằng tổng cả danh sách. Và vì tổng các giao dịch lớn là một phần của tất cả, nên nó không thể vượt tổng tất cả. Cả hai đều đúng với số liệu của ta.""", clear=True),
    ], checks=["4700000 <= 7450000", "1550000 + 4400000 + 1500000 == 7450000"])
    sc_scale = sc("scale", "concept", "Khi dữ liệu lớn gấp một nghìn lần: đường ống lười cứu bộ nhớ", [
        st(code_block(ngan_mach, lines=(5, 10)) + out_block(ngan_mach),
           """Điều đầu tiên là đường ống lười. Ta tìm phần tử đầu tiên chia hết cho mười trong một triệu số. Ta đếm số phần tử thực sự được duyệt bằng cách chèn một trạm đếm. Kết quả là chỉ mười phần tử, vì đường ống dừng ngay khi tìm được.
           Vòng lặp viết vụng có thể duyệt cả một triệu.""", clear=True),
        st(term_block(lon, 1, 4, title="Cùng một tệp một triệu dòng, bộ nhớ chỉ 32 megabyte"),
           """Điều thứ hai là kết hợp với đọc từng dòng. Ta tạo tệp một triệu dòng. Cách đọc hết rồi mới tạo đường ống thì hết bộ nhớ, như bài trước. Còn cách tạo đường ống trực tiếp từ tệp, mỗi lúc chỉ giữ một dòng, thì chạy xong, gom được ba nhóm.
           Tổng của ba nhóm vẫn đúng bằng tổng cả tệp, và không tốn thêm bộ nhớ vì số nhóm chỉ là ba.""", clear=True),
        st(table(["số dòng", "1 000", "1 000 000", "1 000 000 000"],
                 [["bộ nhớ khi giữ mọi dòng rồi mới tạo đường ống", "≈ 64 nghìn byte", "≈ 64 triệu byte", "<b>≈ 64 tỉ byte</b>"],
                  ["bộ nhớ khi đường ống đọc lười từ tệp", "≈ một dòng", "≈ một dòng", "≈ một dòng"],
                  ["thời gian đọc (tỉ lệ)", "×1", "×1 000", "<b>×1 000 000</b>"]])
           + "<p class='note'>Đánh đổi: đường ống lười chỉ đi <b>một chiều, một lần</b>; cần duyệt lại thì phải đọc lại tệp. Thời gian vẫn tăng theo số dòng; chỉ bộ nhớ là không đổi.</p>",
           """Tóm lại theo quy mô. Giữ mọi dòng thì bộ nhớ tăng theo số dòng và gãy ở khoảng một triệu với giới hạn nhỏ. Đọc lười thì bộ nhớ gần như không đổi. Nhưng thời gian vẫn tăng đều theo số dòng, một tỉ dòng vẫn tốn gấp một triệu lần một nghìn dòng.
           Đánh đổi là đường ống lười chỉ đi một chiều, một lần.""", clear=True),
    ], checks=["1000 * 64 == 64000", "1000000 * 64 == 64000000", "1000000000 // 1000 == 1000000",
               f"sum((i % 7 + 1) * 1000 for i in range(1, 1000001)) == {sum(_tong.values())}"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Hàm ngắn muốn sửa biến bên ngoài.</div>'
           + code_block(cap_bien, lines=(5, 9)) + out_block(cap_bien),
           """Lỗi thứ nhất là hàm ngắn muốn sửa biến bên ngoài. Hàm ngắn chỉ được đọc biến cục bộ mà không đổi sau khi gán, vì hàm có thể chạy muộn, ở luồng khác, khi biến đã không còn. Biến tổng ở đây bị cộng thêm sau đó, nên trình biên dịch từ chối.
           Muốn gom kết quả thì dùng bước cuối của đường ống, đừng cộng vào biến ngoài."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Dùng lại một đường ống đã chạy.</div>'
           + code_block(dung_hai, lines=(6, 8)) + out_block(dung_hai),
           """Lỗi thứ hai là dùng lại một đường ống đã chạy. Mỗi đường ống chỉ chạy một lần. Lần đếm đầu cho ra ba, lần thứ hai nổ ngoại lệ báo đường ống đã dùng. Cách sửa là mở đường ống mới từ danh sách mỗi lần cần.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Gom thành bản đồ khi khoá có thể trùng.</div>'
           + code_block(trung_khoa, lines=(9, 12)) + out_block(trung_khoa),
           """Lỗi thứ ba hay gặp ở người đã đi làm. Gom danh sách thành bản đồ với khoá là loại giao dịch. Khi dữ liệu thử chỉ có khoá khác nhau thì chạy ngon. Đến ngày dữ liệu thật có hai dòng cùng loại, ngoại lệ khoá trùng làm cả đường ống nổ.""", clear=True),
        st('<div class="box key"><b>Cách sửa:</b> đưa thêm hàm hợp nhất hai giá trị cùng khoá (ở đây <code>Long::sum</code>).</div>'
           + code_block(sua_khoa, lines=(12, 13)) + out_block(sua_khoa),
           """Cách sửa là thêm hàm hợp nhất cho hai giá trị cùng khoá, ở đây là phép cộng. Hai dòng nạp được cộng lại thành ba triệu năm trăm nghìn, và không còn nổ khi dữ liệu có khoá trùng.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Danh sách các số tiền: <code>[400000, 1500000, 250000, 3000000, 900000]</code>.</p>
<ol><li>Giá trị của <code>.stream().filter(x -&gt; x &gt;= 900000).mapToLong(x -&gt; x).sum()</code>?</li>
<li>Đoạn <code>ds.stream().filter(...).map(...);</code> (không có bước cuối) in gì, làm gì?</li></ol>
<p><b>Chọn A hay B?</b> Cần tổng tiền từ một tệp 30 GB. A: <code>Files.readAllLines(p).stream()…</code>. B: <code>Files.lines(p)…</code> trong khối có tài nguyên. Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Có năm số tiền. Hãy tính tổng các số từ chín trăm nghìn trở lên. Rồi nói đoạn đường ống không có bước cuối thì in ra gì và làm gì. Cuối cùng chọn giữa đọc hết tệp ba mươi gigabyte vào bộ nhớ rồi mới tạo đường ống, và tạo đường ống trực tiếp từ tệp, và nói vì sao.
           Hãy dừng video và tự làm.""", pause=25),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "<code>1500000 + 3000000 + 900000 = 5400000</code>", "chỉ giữ các số ≥ 900000; 400000 và 250000 bị loại"],
                  ["2", "không in gì, không làm gì", "thiếu bước cuối nên đường ống <b>không chạy</b>"],
                  ["3", "<b>B</b>", "A giữ mọi dòng (≈ 64 byte × số dòng ≫ bộ nhớ); B đọc lười, mỗi lúc một dòng"]]),
           """Đáp án câu một, giữ các số từ chín trăm nghìn trở lên là một triệu rưỡi, ba triệu và chín trăm nghìn, cộng lại được năm triệu bốn trăm nghìn. Câu hai, không có bước cuối thì đường ống không chạy, nên không in gì và không làm gì.
           Câu ba chọn phương án B, vì phương án A giữ mọi dòng trong bộ nhớ, còn B đọc lười từng dòng.""",
           focus=["1.2", "1.3", "1.4"]),
        st("""<div class="box key"><b>Quy tắc:</b> đường ống tiện và dễ đọc, nhưng chỉ <b>lười</b> khi nguồn lười. Nguồn đã nằm hết trong bộ nhớ thì đường ống không cứu được bộ nhớ.</div>""",
           """Quy tắc rút ra. Đường ống tiện và dễ đọc, nhưng chỉ lười khi nguồn của nó lười. Nếu nguồn đã nằm hết trong bộ nhớ thì đường ống không cứu được bộ nhớ."""),
    ], checks=["1500000 + 3000000 + 900000 == 5400000", "sum(x for x in [400000, 1500000, 250000, 3000000, 900000] if x >= 900000) == 5400000"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("hàm là giá trị: x -> …", "tham chiếu hàm: Lop::ham", "đường ống: nguồn → bước giữa → bước cuối", "bước cuối mới chạy",
                 "mỗi phần tử đi hết các trạm", "nguồn lười thì đường ống lười"),
           """Tổng kết chuỗi logic. Hàm là một giá trị, viết gọn bằng mũi tên. Tham chiếu hàm là cách viết tắt. Đường ống gồm nguồn, các bước giữa và bước cuối. Chỉ bước cuối mới làm đường ống chạy.
           Mỗi phần tử đi hết các trạm rồi mới tới phần tử sau. Và đường ống chỉ lười khi nguồn của nó lười."""),
        st("""<div class='box key'><b>Tư duy:</b> khi viết đường ống, hỏi: <b>nguồn</b> nằm hết trong bộ nhớ không, <b>khoá</b> có thể trùng không, đường ống có <b>bước cuối</b> không,
và hàm ngắn có đang <b>sửa biến bên ngoài</b> không. Vòng lặp vẫn tốt khi cần kiểm soát từng bước.</div>""",
           """Điều cần mang theo. Khi viết đường ống, hãy hỏi bốn câu. Nguồn có nằm hết trong bộ nhớ không. Khoá có thể trùng không. Đường ống có bước cuối không. Và hàm ngắn có đang sửa biến bên ngoài không. Vòng lặp vẫn tốt khi cần kiểm soát từng bước."""),
    ])
    return lesson("L03", "ham_la_gia_tri_stream", "Bài 3 — Hàm là giá trị: hàm ngắn và đường ống Stream",
                  "curriculum/jv2.yaml L03; audit/jv2/verify_jv2.py L03 (javac/java chạy thật, JDK 21; -Xmx32m cho phép đo bộ nhớ); "
                  "The Java Language Specification, Java SE 21: §15.27 (biểu thức lambda), §15.13 (tham chiếu phương thức), §15.27.2 (biến cục bộ phải effectively final: §4.12.4); "
                  "java.util.stream (Java SE 21 API: đường ống lười, bước cuối, một lần dùng), Collectors.toMap (khoá trùng ném IllegalStateException), "
                  "Files.lines (đọc lười); dev.java/learn",
                  ["Đọc hàm ngắn, giao diện hàm và tham chiếu hàm",
                   "Mô tả đường ống chạy theo từng phần tử và chỉ chạy khi có bước cuối",
                   "Viết đường ống lọc, biến đổi và gom nhóm, đối chiếu với vòng lặp",
                   "Nhận ra khi nào đường ống giữ được bộ nhớ nhỏ và khi nào không",
                   "Tính thống kê tám giao dịch bằng đường ống và kiểm lại bằng vòng lặp"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "example"), (2, "intuition"), (3, "example"), (4, "scale"), (5, "practice")])
