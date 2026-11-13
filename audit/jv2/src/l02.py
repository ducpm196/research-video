from lib import *
from labkit import write_lab, practice_steps, practice_scene

GD_VD = "record GiaoDich(int ma, String loai, long soTien) {}"


def build():
    hop_cu = prog("HopCu", r"""
public class HopCu {
    static class Hop {
        private final Object giaTri;                 // Object: nhận mọi thứ
        Hop(Object giaTri) { this.giaTri = giaTri; }
        Object lay() { return giaTri; }
    }

    public static void main(String[] args) {
        Hop h = new Hop("500000");                   // lỡ bỏ vào một CHUỖI
        long tien = (Long) h.lay();                  // cố ép thành số nguyên dài
        System.out.println(tien);
    }
}""", out="", expect="runtime_error:ClassCastException",
                  err='Exception in thread "main" java.lang.ClassCastException: class java.lang.String cannot be cast to class …')
    hop_sai = prog("HopSai", r"""
public class HopSai {
    static class Hop<T> {
        private final T giaTri;                      // T: kiểu do người dùng chọn
        Hop(T giaTri) { this.giaTri = giaTri; }
        T lay() { return giaTri; }
    }

    public static void main(String[] args) {
        Hop<Long> tien = new Hop<Long>("500000");    // hộp của Long mà bỏ chuỗi vào
        System.out.println(tien.lay());
    }
}""", expect="compile_error:incompatible types: String cannot be converted to Long",
                   err="error: incompatible types: String cannot be converted to Long\n        Hop<Long> tien = new Hop<Long>(\"500000\");…\n                                       ^")
    hop_chung = prog("HopChung", r"""
public class HopChung {
    static class Hop<T> {
        private final T giaTri;
        Hop(T giaTri) { this.giaTri = giaTri; }
        T lay() { return giaTri; }
    }

    public static void main(String[] args) {
        Hop<Long> tien = new Hop<>(500000L);
        Hop<String> ten = new Hop<>("An");
        long gapDoi = tien.lay() * 2;                // không cần ép kiểu
        System.out.println(ten.lay() + " " + gapDoi);
    }
}""", out="An 1000000")
    lon_nhat = prog("LonNhat", r"""
public class LonNhat {
    static <T extends Comparable<T>> T lon(T a, T b) {
        return a.compareTo(b) >= 0 ? a : b;          // compareTo: âm, không, hay dương
    }

    public static void main(String[] args) {
        System.out.println(lon(3, 7));
        System.out.println(lon("abc", "abd"));
        System.out.println("chuyen".compareTo("nap") + " " + "nap".compareTo("nap") + " " + "rut".compareTo("nap"));
    }
}""", out="7\nabd\n-11 0 4")
    sap_xep = prog("SapXep", r"""
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class SapXep {
    record GiaoDich(int ma, String loai, long soTien) {}

    static class TheoLoaiRoiTien implements Comparator<GiaoDich> {
        public int compare(GiaoDich a, GiaoDich b) {
            int c = a.loai().compareTo(b.loai());        // khoá 1: loại, tăng dần
            if (c != 0) {
                return c;
            }
            return Long.compare(b.soTien(), a.soTien()); // khoá 2: tiền, GIẢM dần
        }
    }

    public static void main(String[] args) {
        List<GiaoDich> ds = new ArrayList<>(List.of(
                new GiaoDich(1, "rut", 500000), new GiaoDich(2, "nap", 2000000),
                new GiaoDich(3, "rut", 300000), new GiaoDich(4, "chuyen", 1200000),
                new GiaoDich(5, "nap", 1500000), new GiaoDich(6, "rut", 700000)));
        ds.sort(new TheoLoaiRoiTien());
        for (GiaoDich g : ds) {
            System.out.println(g.ma() + " " + g.loai() + " " + g.soTien());
        }
    }
}""", out="4 chuyen 1200000\n2 nap 2000000\n5 nap 1500000\n6 rut 700000\n1 rut 500000\n3 rut 300000")
    bat_bien = prog("BatBien", r"""
import java.util.ArrayList;
import java.util.List;

public class BatBien {
    public static void main(String[] args) {
        List<Long> tien = new ArrayList<>();
        List<Object> chung = tien;                   // có vẻ hợp lý?
        chung.add("abc");                            // nếu được phép, danh sách tiền chứa chuỗi
    }
}""", expect="compile_error:incompatible types: List<Long> cannot be converted to List<Object>",
                    err="error: incompatible types: List<Long> cannot be converted to List<Object>\n        List<Object> chung = tien;…\n                             ^")
    tru_sai = prog("TruSai", r"""
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class TruSai {
    static class Sai implements Comparator<Long> {
        public int compare(Long a, Long b) {
            return (int) (a - b);                    // "a - b" tưởng gọn mà SAI
        }
    }

    public static void main(String[] args) {
        System.out.println((int) (3000000000L - 1L));
        List<Long> ds = new ArrayList<>(List.of(3000000000L, 1L, 2L));
        ds.sort(new Sai());
        System.out.println(ds);
    }
}""", out="-1294967297\n[3000000000, 1, 2]")
    dem_ss = prog("DemSoSanh", r"""
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public class DemSoSanh {
    static class Dem implements Comparator<Integer> {
        long dem = 0;                                // đếm số lần so sánh
        public int compare(Integer a, Integer b) {
            dem++;
            return Integer.compare(a, b);
        }
    }

    public static void main(String[] args) {
        int[] cac = {1000, 100000, 1000000};
        for (int n : cac) {
            Random r = new Random(42);
            List<Integer> ds = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                ds.add(r.nextInt(1000000));
            }
            Dem a = new Dem();
            ds.sort(a);
            Dem b = new Dem();
            ds.sort(b);                              // lần hai: danh sách đã xếp sẵn
            long nlogn = Math.round(n * (Math.log(n) / Math.log(2)));
            System.out.println("n=" + n + ": ngau nhien " + a.dem + ", da xep san " + b.dem + ", n*log2(n)=" + nlogn);
        }
    }
}""", out="n=1000: ngau nhien 8683, da xep san 999, n*log2(n)=9966\nn=100000: ngau nhien 1534624, da xep san 99999, n*log2(n)=1660964\n"
             "n=1000000: ngau nhien 18640873, da xep san 999999, n*log2(n)=19931569")

    lab = prog("SapXepGiaoDich", r"""
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class SapXepGiaoDich {
    record GiaoDich(int ma, String loai, long soTien) {}

    static class TheoLoaiRoiTien implements Comparator<GiaoDich> {
        public int compare(GiaoDich a, GiaoDich b) {
            int c = a.loai().compareTo(b.loai());
            if (c != 0) {
                return c;
            }
            return Long.compare(b.soTien(), a.soTien());
        }
    }

    public static void main(String[] args) {
        List<GiaoDich> ds = new ArrayList<>(List.of(
                new GiaoDich(1, "chuyen", 900000), new GiaoDich(2, "nap", 250000), new GiaoDich(3, "chuyen", 150000),
                new GiaoDich(4, "rut", 600000), new GiaoDich(5, "nap", 4000000), new GiaoDich(6, "rut", 900000),
                new GiaoDich(7, "chuyen", 900000)));
        ds.sort(new TheoLoaiRoiTien());
        for (GiaoDich g : ds) {
            System.out.println(g.ma() + " " + g.loai() + " " + g.soTien());
        }
    }
}""", out="1 chuyen 900000\n7 chuyen 900000\n3 chuyen 150000\n5 nap 4000000\n2 nap 250000\n6 rut 900000\n4 rut 600000")
    write_lab("JV2", "L02", """# Lab JV2 L02 — Sắp xếp giao dịch theo hai khoá

Tự viết chương trình `SapXepGiaoDich` (tệp `SapXepGiaoDich.java`):

1. Khai báo `record GiaoDich(int ma, String loai, long soTien) {}` bên trong lớp.
2. Tạo danh sách bảy giao dịch theo thứ tự này (`ma`, `loai`, `soTien`):
   `(1, chuyen, 900000)`, `(2, nap, 250000)`, `(3, chuyen, 150000)`, `(4, rut, 600000)`, `(5, nap, 4000000)`, `(6, rut, 900000)`, `(7, chuyen, 900000)`.
3. Viết một lớp `TheoLoaiRoiTien implements Comparator<GiaoDich>`: **khoá 1** là `loai` tăng dần; **khoá 2** là `soTien` **giảm dần**
   (dùng `Long.compare`, **không** dùng phép trừ). Sắp xếp bằng `ds.sort(new TheoLoaiRoiTien())`.
4. In mỗi giao dịch một dòng dạng `1 chuyen 900000` (`ma loai soTien`).

Chú ý hai giao dịch `1` và `7` có cùng loại và cùng số tiền: `List.sort` là sắp xếp **ổn định**, nên chúng giữ nguyên thứ tự ban đầu.

Chạy: `javac SapXepGiaoDich.java && java SapXepGiaoDich`. Chấm: `bash labs/cham.sh JV2 L02 SapXepGiaoDich.java`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: sắp xếp giao dịch theo hai khoá", practice_steps(
        st, "JV2", "L02",
        """<p><b>Đề</b>: sắp xếp bảy giao dịch theo <b>loại tăng dần</b>, rồi <b>tiền giảm dần</b>.</p>
<ol><li><code>record GiaoDich(int ma, String loai, long soTien)</code>; bảy giao dịch theo đề trong <code>de.md</code>.</li>
<li>Lớp <code>TheoLoaiRoiTien implements Comparator&lt;GiaoDich&gt;</code>; so tiền bằng <code>Long.compare</code>.</li>
<li><code>ds.sort(…)</code> rồi in <code>ma loai soTien</code> mỗi dòng.</li></ol>
<p class="note">Hai giao dịch 1 và 7 trùng cả loại lẫn tiền: sắp xếp <b>ổn định</b> giữ nguyên thứ tự cũ. Tệp <code>SapXepGiaoDich.java</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Có bảy giao dịch cho trong đề bài. Hãy viết một bộ so sánh với hai khoá, khoá một là loại tăng dần, khoá hai là số tiền giảm dần, và dùng hàm so sánh số nguyên dài chứ không dùng phép trừ.
        Sắp xếp danh sách rồi in từng giao dịch. Chú ý hai giao dịch trùng cả loại lẫn tiền sẽ giữ nguyên thứ tự ban đầu, vì sắp xếp này ổn định. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        lab["out"], "SapXepGiaoDich.java",
        """<div class="box key"><b>Nếu kẹt:</b> trong <code>compare(a, b)</code>: so <code>a.loai().compareTo(b.loai())</code>; nếu khác 0 thì trả luôn; nếu bằng thì trả <code>Long.compare(b.soTien(), a.soTien())</code> (đảo a và b để giảm dần).
Lời giải: <code>labs/JV2/L02/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, trong hàm so sánh, trước hết so hai loại với nhau. Nếu khác nhau thì trả kết quả ngay. Nếu bằng nhau thì so số tiền, nhưng đảo thứ tự hai số để được giảm dần.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=150), "JV2", "L02")

    sc_hook = sc("hook", "hook", "Hộp nhận mọi thứ, và lỗi chỉ lộ ra lúc đã chạy", [
        st(code_block(hop_cu, lines=(9, 12)) + out_block(hop_cu),
           """Hãy tưởng tượng một chiếc hộp cho phép bỏ vào bất cứ thứ gì. Ta lỡ bỏ chuỗi chữ năm trăm nghìn vào, rồi lấy ra và ép thành số nguyên dài. Trình biên dịch im lặng, chương trình chạy, và nó nổ ở đúng dòng đó, có thể là ở máy chủ đang phục vụ khách.
           Lỗi sai kiểu mà chỉ lộ ra khi chạy là loại lỗi đắt nhất."""),
        st("""<div class="box key">Hôm nay: <b>kiểu tổng quát</b>, cho phép một hộp ghi rõ <b>nó chứa kiểu gì</b> để trình biên dịch bắt lỗi sớm.
Rồi hai cách <b>sắp xếp</b> một danh sách: thứ tự tự nhiên của lớp, và bộ so sánh do người gọi chọn; kèm câu hỏi quy mô: sắp xếp một triệu phần tử tốn bao nhiêu lần so sánh.</div>""",
           """Hôm nay ta học kiểu tổng quát, cách để một chiếc hộp ghi rõ nó chứa kiểu gì, nhờ đó trình biên dịch bắt lỗi sớm.
           Rồi hai cách sắp xếp một danh sách, và câu hỏi quy mô là sắp xếp một triệu phần tử tốn bao nhiêu lần so sánh.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: danh sách, bản ghi, hàm tĩnh", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① danh sách có kiểu", "<code>List&lt;Long&gt;</code>: trong ngoặc nhọn là kiểu phần tử; <code>add</code> thêm, <code>get</code> lấy"],
                  ["② bản ghi", "<code>record GiaoDich(int ma, String loai, long soTien) {}</code> tự có <code>ma()</code>, <code>loai()</code>, <code>soTien()</code>"],
                  ["③ giao diện", "lớp <code>implements</code> một giao diện thì phải viết đủ các hàm giao diện đòi"],
                  ["④ so sánh số", "<code>3000000000L</code> là <code>long</code>; <code>(int)</code> ép kiểu có thể cắt mất phần lớn"]]),
           """Ta ôn lại bốn điều. Danh sách có kiểu, trong ngoặc nhọn là kiểu của phần tử. Bản ghi tự có các hàm đọc theo tên trường. Lớp cài một giao diện thì phải viết đủ các hàm mà giao diện đòi.
           Và ép kiểu từ số nguyên dài sang số nguyên thường có thể cắt mất phần lớn giá trị. Bài này dùng cả bốn.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã sáu ký hiệu của kiểu tổng quát và so sánh", [
        st(table(["viết", "nghĩa"],
                 [["<code>Hop&lt;T&gt;</code>", "lớp <b>có tham số kiểu</b> <code>T</code>: một chỗ trống cho kiểu, điền khi dùng"],
                  ["<code>Hop&lt;Long&gt;</code>", "điền <code>T = Long</code>: hộp chỉ nhận và trả <code>Long</code>"],
                  ["<code>new Hop&lt;&gt;(x)</code>", "dấu <code>&lt;&gt;</code> trống: để trình biên dịch tự suy ra kiểu từ <code>x</code>"],
                  ["<code>&lt;T extends Comparable&lt;T&gt;&gt;</code>", "<code>T</code> phải <b>so sánh được</b> với chính nó"],
                  ["<code>a.compareTo(b)</code>", "trả số <b>âm</b> nếu a đứng trước, <b>0</b> nếu bằng, <b>dương</b> nếu a đứng sau"],
                  ["<code>Comparator&lt;X&gt;</code>", "<b>bộ so sánh</b>: một đối tượng có hàm <code>compare(a, b)</code> với cùng quy ước âm, 0, dương"]]),
           """Bảng này có sáu ký hiệu. Chữ T trong ngoặc nhọn là chỗ trống cho một kiểu, điền khi dùng. Điền kiểu số nguyên dài thì hộp chỉ nhận và trả số nguyên dài. Cặp ngoặc nhọn trống để trình biên dịch tự suy ra kiểu.
           Ràng buộc nói rằng kiểu phải so sánh được với chính nó. Hàm so sánh trả số âm khi a đứng trước, không khi bằng nhau, dương khi a đứng sau. Còn bộ so sánh là một đối tượng có hàm so sánh hai phần tử theo cùng quy ước đó.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: hộp dán nhãn kiểu và hai cách xếp hàng", [
        st(svg(1500, 330,
               panel(20, 10, 700, 310, "Hộp không nhãn: Object", C_RED),
               box(60, 90, 260, 70, "\"500000\"", C_AMBER, 26), arrow(325, 125, 400, 125, "#dc2626", "bỏ vào"),
               box(405, 70, 220, 110, ["hộp", "(Object)"], C_GRAY, 26), arrow(405, 240, 330, 240, "#dc2626", "ép thành Long"),
               txt(240, 275, "NỔ lúc chạy", 30, "middle", "#dc2626", True),
               panel(780, 10, 700, 310, "Hộp có nhãn: Hop&lt;Long&gt;", C_GREEN),
               box(820, 90, 260, 70, "\"500000\"", C_AMBER, 26), arrow(1085, 125, 1160, 125, "#16a34a", "bỏ vào"),
               box(1165, 70, 270, 110, ["hộp", "Hop&lt;Long&gt;"], C_BLUE, 26, bold=True),
               txt(1130, 250, "TỪ CHỐI lúc biên dịch", 30, "middle", "#16a34a", True),
               txt(1130, 290, "lỗi tới sớm, trước khi phát hành", 24)),
           """Hình dung hộp không nhãn như một cái thùng nhận mọi thứ. Bỏ gì vào cũng được, nhưng lúc lấy ra phải đoán kiểu, và đoán sai thì nổ ở lúc chạy.
           Hộp có nhãn kiểu thì khác. Trình biên dịch nhìn nhãn và từ chối món sai ngay lúc ta bấm biên dịch, tức là trước khi chương trình tới tay người dùng."""),
        st(code_block(hop_sai, lines=(2, 6)) + code_block(hop_sai, lines=(9, 9)) + out_block(hop_sai),
           """Đây là chiếc hộp có tham số kiểu. Chữ T là chỗ trống, hộp cất giá trị kiểu T và trả giá trị kiểu T. Khi ta khai hộp của số nguyên dài mà bỏ chuỗi vào, trình biên dịch từ chối ngay, kèm dòng chỉ đúng chỗ sai.""", clear=True),
        st(code_block(hop_chung, lines=(9, 13)) + out_block(hop_chung),
           """Dùng đúng thì gọn hơn nữa. Hai hộp, một hộp số nguyên dài, một hộp chuỗi, dùng chung một lớp. Lấy số ra nhân đôi không cần ép kiểu, vì trình biên dịch đã biết đó là số nguyên dài.""", clear=True),
        st(svg(1500, 300,
               box(20, 70, 330, 90, ["① Comparable", "thứ tự TỰ NHIÊN", "một cách, nằm trong lớp"], C_BLUE, 24, bold=True),
               box(20, 180, 330, 90, ["a.compareTo(b)", "chuỗi, số: có sẵn"], C_GRAY, 24),
               box(560, 70, 330, 90, ["② Comparator", "thứ tự DO NGƯỜI GỌI chọn", "nhiều cách, đặt ngoài lớp"], C_GREEN, 24, bold=True),
               box(560, 180, 330, 90, ["compare(a, b)", "loại rồi tiền…"], C_GRAY, 24),
               txt(1180, 120, "dùng cái nào?", 30, "middle", "#1f2937", True),
               txt(1180, 170, "một thứ tự mặc định hiển nhiên", 24), txt(1180, 205, "→ ①", 28, "middle", "#2a78d6", True),
               txt(1180, 245, "nhiều cách xếp tuỳ ngữ cảnh → ②", 24, "middle", "#16a34a", True)),
           """Còn hai cách sắp xếp. Thứ tự tự nhiên nằm ngay trong lớp, mỗi lớp chỉ có một. Chuỗi và số đã có sẵn. Bộ so sánh thì nằm ngoài lớp và do người gọi chọn, nên cùng một danh sách có thể xếp theo nhiều cách.
           Giao dịch có thể xếp theo loại, theo tiền, theo ngày, nên ta dùng bộ so sánh.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: bộ so sánh hai khoá", [
        st(code_block(lon_nhat, lines=(2, 4)) + out_block(lon_nhat),
           """Bước một, hiểu hàm so sánh. Hai số cho ra bảy là lớn hơn. Hai chuỗi so theo thứ tự từ điển, nên chuỗi a b c đứng trước a b d. Với chuyển và nạp, chữ c đứng trước chữ n, nên kết quả là số âm, và chính xác là âm mười một.
           Chỉ dấu của kết quả mới quan trọng, không phải độ lớn."""),
        st("""<p><b>Bước 2.</b> Muốn xếp theo <b>hai khoá</b>: so khoá 1; nếu <b>khác 0</b> thì có đáp án ngay; nếu <b>bằng 0</b> mới so khoá 2.</p>
<p><code>c = a.loai().compareTo(b.loai());</code></p><p><code>if (c != 0) return c;</code></p><p><code>return …khoá 2…;</code></p>""",
           """Bước hai, ghép hai khoá. Vì khoá thứ hai chỉ có ý nghĩa khi hai phần tử ngang nhau ở khoá thứ nhất, nên ta so khoá một trước. Nếu khác không thì có đáp án ngay. Chỉ khi bằng không mới sang khoá hai.""", clear=True),
        st("""<p><b>Bước 3.</b> Muốn <b>giảm dần</b>, đảo hai đối số:</p>
<p><code>Long.compare(a.soTien(), b.soTien())</code> &rarr; tăng dần</p><p><code>Long.compare(b.soTien(), a.soTien())</code> &rarr; <b>giảm dần</b></p>
<p>Thử: a = 2 000 000, b = 1 500 000. <code>Long.compare(b, a)</code> = <code>compare(1 500 000, 2 000 000)</code> = <b>−1</b> &rarr; a đứng <b>trước</b> b ✓</p>""",
           """Bước ba, đảo chiều. Muốn giảm dần thì đảo hai đối số, và ta thử bằng số. Giao dịch a hai triệu, giao dịch b một triệu rưỡi. So b với a, một triệu rưỡi nhỏ hơn hai triệu, nên kết quả là âm một, nghĩa là a đứng trước b. Đúng ý, số lớn đứng trước.""", clear=True),
        st("""<p><b>Bước 4.</b> Vì sao dùng <code>Long.compare</code> chứ không viết <code>a - b</code>? Phép trừ có thể <b>tràn</b>:</p>
<p><code>(int) (3 000 000 000 − 1)</code> = <code>−1 294 967 297</code>: dấu <b>sai</b> &rarr; máy tưởng 3 tỉ đứng <b>trước</b> 1.</p>""",
           """Bước bốn, vì sao không dùng phép trừ. Ba tỉ trừ một là gần ba tỉ, nhưng khi ép về số nguyên thường thì bị tràn và thành âm một tỉ hai trăm chín mươi bốn triệu. Dấu sai, nên máy tin ba tỉ đứng trước một. Ta sẽ thấy nó làm hỏng cả bản sắp xếp ở phần lỗi hay gặp.""", clear=True),
    ], checks=["(1500000 > 2000000) - (1500000 < 2000000) == -1", "ord('c') - ord('n') == -11", "ord('r') - ord('n') == 4",
               "((3000000000 - 1 + 2**31) % 2**32) - 2**31 == -1294967297"])
    sc_ex = sc("example", "example", "Ví dụ: sáu giao dịch xếp theo loại rồi tiền giảm dần", [
        st(code_block(sap_xep, lines=(8, 16)),
           """Đây là bộ so sánh hai khoá của ta, nằm trong một lớp cài giao diện bộ so sánh cho kiểu giao dịch. Khoá một là loại, tăng dần theo từ điển. Nếu hai loại giống nhau thì khoá hai là số tiền, đảo hai đối số để giảm dần."""),
        st(code_block(sap_xep, lines=(18, 26)),
           """Chương trình tạo sáu giao dịch, gọi hàm sắp xếp của danh sách với bộ so sánh của ta, rồi in từng dòng. Ta sẽ tự xếp bằng tay trước, rồi so với kết quả.""", clear=True),
        st("$$① \\; \\text{chuyen} \\;<\\; \\text{nap} \\;<\\; \\text{rut} \\quad (\\text{c} < \\text{n} < \\text{r}) \\Rightarrow \\text{ba nhóm}$$"
           "$$② \\; \\text{chuyen}: 1\\,200\\,000 \\quad (\\text{chỉ có 1 dòng, mã 4})$$",
           """Phép làm thứ nhất, xếp theo loại. Chữ c đứng trước n, n đứng trước r, nên có ba nhóm theo thứ tự chuyển, nạp, rút. Phép thứ hai, nhóm chuyển chỉ có một dòng, là giao dịch bốn, một triệu hai trăm nghìn.""", clear=True),
        st("$$③ \\; \\text{nap}: 2\\,000\\,000 > 1\\,500\\,000 \\Rightarrow \\text{mã 2 rồi mã 5}$$"
           "$$④ \\; \\text{rut}: 700\\,000 > 500\\,000 > 300\\,000 \\Rightarrow \\text{mã 6, mã 1, mã 3}$$",
           """Phép thứ ba, nhóm nạp có hai dòng, hai triệu lớn hơn một triệu rưỡi, nên mã hai đứng trước mã năm. Phép thứ tư, nhóm rút có ba dòng, bảy trăm nghìn lớn hơn năm trăm nghìn lớn hơn ba trăm nghìn, nên thứ tự là mã sáu, mã một, mã ba."""),
        st("$$⑤ \\; \\text{thứ tự mã} = \\hl{4,\\; 2,\\; 5,\\; 6,\\; 1,\\; 3}$$" + out_block(sap_xep),
           """Phép thứ năm, nối các nhóm lại, thứ tự mã là bốn, hai, năm, sáu, một, ba. Chạy thật, sáu dòng in ra đúng thứ tự đó.""", clear=True),
    ], checks=["ord('c') < ord('n') < ord('r')", "2000000 > 1500000", "700000 > 500000 > 300000",
               "[g[0] for g in sorted([(1,'rut',500000),(2,'nap',2000000),(3,'rut',300000),(4,'chuyen',1200000),(5,'nap',1500000),(6,'rut',700000)], key=lambda g: (g[1], -g[2]))] == [4, 2, 5, 6, 1, 3]"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: sắp xếp bằng công cụ dòng lệnh", [
        st("""<p>Cùng dữ liệu, xếp bằng lệnh <code>sort</code> của hệ điều hành: khoá 1 là cột 2 (chữ), khoá 2 là cột 3 (số, giảm dần):</p>
<p><code>sort -t, -k2,2 -k3,3nr</code> cho thứ tự mã: <b>4, 2, 5, 6, 1, 3</b> ✓ trùng với chương trình Java.</p>
<p>Kiểm thêm tính chất: sau khi xếp, mỗi cặp liền nhau <code>(x, y)</code> thoả <code>compare(x, y) ≤ 0</code>; có 6 phần tử nên có <b>5</b> cặp liền nhau.</p>""",
           """Cách kiểm khác là dùng lệnh sắp xếp của hệ điều hành trên cùng dữ liệu, khoá một là cột chữ, khoá hai là cột số giảm dần. Nó cho thứ tự mã bốn, hai, năm, sáu, một, ba, trùng với chương trình Java.
           Ta cũng kiểm tính chất, sau khi xếp thì mỗi cặp liền nhau phải thoả so sánh nhỏ hơn hoặc bằng không. Sáu phần tử có đúng năm cặp liền nhau."""),
    ], checks=["6 - 1 == 5"])
    sc_scale = sc("scale", "concept", "Khi danh sách lớn gấp một nghìn: số lần so sánh tăng thế nào?", [
        st(table(["số phần tử n", "1 000", "100 000", "1 000 000"],
                 [["so sánh khi dữ liệu xáo trộn (đo thật)", "8 683", "1 534 624", "<b>18 640 873</b>"],
                  ["xấp xỉ n × log₂ n", "9 966", "1 660 964", "19 931 569"],
                  ["xếp lại danh sách đã xếp sẵn (đo thật)", "999", "99 999", "<b>999 999</b>"]]),
           """Bây giờ là chuyện quy mô. Ta đếm số lần gọi hàm so sánh khi xếp danh sách số ngẫu nhiên. Với một nghìn phần tử là gần chín nghìn lần. Với một triệu phần tử, lớn gấp một nghìn lần, là mười tám triệu sáu trăm nghìn lần.
           Tăng một nghìn lần số phần tử mà số lần so sánh tăng hơn hai nghìn lần, vì nó theo n nhân lôgarit của n. Con số đo được sát với công thức."""),
        st(code_block(dem_ss, lines=(17, 27)),
           """Mã đo là chương trình này, ta đếm bằng cách cho bộ so sánh tăng một biến mỗi lần được gọi. Hạt giống số ngẫu nhiên cố định, nên ai chạy cũng ra đúng những con số trên bảng.""", clear=True),
        st(out_block(dem_ss) + "<p class='note'>Đánh đổi: bộ so sánh càng đắt (so nhiều khoá, so chuỗi dài) thì nhân với 18 triệu lần càng đau; danh sách đã gần xếp sẵn thì rẻ hơn rất nhiều.</p>",
           """Điều thú vị là hàng cuối. Xếp lại một danh sách đã xếp sẵn chỉ tốn gần đúng n lần so sánh, vì thuật toán nhận ra các đoạn đã đúng thứ tự. Người làm nghề dùng điều này, ví dụ giữ dữ liệu luôn đã xếp để lần sau gần như miễn phí.
           Còn bộ so sánh nhân với hàng chục triệu lần gọi, nên nó phải rẻ và phải nhất quán.""", clear=True),
    ], checks=["round(1000 * __import__('math').log2(1000)) == 9966", "round(100000 * __import__('math').log2(100000)) == 1660964",
               "round(1000000 * __import__('math').log2(1000000)) == 19931569", "18640873 / 8683 > 2000", "1000 - 1 == 999"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Tin rằng danh sách các Long cũng là danh sách các Object.</div>'
           + code_block(bat_bien, lines=(6, 8)) + out_block(bat_bien),
           """Lỗi thứ nhất là nghĩ rằng danh sách số nguyên dài cũng là danh sách mọi thứ. Nghe hợp lý, vì số nguyên dài là một thứ. Nhưng nếu được phép, ta bỏ chuỗi vào qua tên mới và danh sách tiền chứa chuỗi.
           Trình biên dịch chặn ngay, vì hộp chứa kiểu A và hộp chứa kiểu B là hai kiểu khác nhau dù A và B có quan hệ."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Quên rằng hộp tổng quát chỉ ép kiểu đúng khi biên dịch, không thay được việc kiểm dữ liệu.</div>'
           + "<p>Hộp <code>Hop&lt;Long&gt;</code> đảm bảo <b>kiểu</b>, không đảm bảo <b>giá trị hợp lệ</b>: số tiền âm, mã rỗng vẫn lọt qua.</p>"
           + "<p>Kiểu tổng quát bắt lỗi <b>loại</b> dữ liệu; kiểm <b>giá trị</b> vẫn là việc của bạn.</p>",
           """Lỗi thứ hai là tưởng kiểu tổng quát kiểm hết mọi thứ. Hộp số nguyên dài đảm bảo kiểu, nhưng số tiền âm hay giá trị vô lý vẫn lọt qua. Kiểu tổng quát chỉ bắt lỗi về loại dữ liệu, còn kiểm giá trị là việc của người viết.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Viết bộ so sánh bằng phép trừ.</div>'
           + code_block(tru_sai, lines=(6, 10)),
           """Lỗi thứ ba hay gặp ở người đã đi làm. Viết bộ so sánh bằng phép trừ rồi ép kiểu, nhìn rất gọn. Với số nhỏ thì chạy đúng nên qua được kiểm thử."""),
        st(code_block(tru_sai, lines=(13, 16)) + out_block(tru_sai),
           """Nhưng khi gặp số lớn, phép trừ tràn và dấu sai, danh sách ba tỉ, một, hai không được xếp đúng. Hãy luôn dùng hàm so sánh có sẵn của kiểu số.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Danh sách ba giao dịch (<code>loai</code>, <code>soTien</code>): <code>(rut, 400000)</code>, <code>(nap, 900000)</code>, <code>(rut, 900000)</code>.
Bộ so sánh: khoá 1 <code>soTien</code> <b>giảm dần</b>; khoá 2 <code>loai</code> <b>tăng dần</b>.</p>
<ol><li>Viết thứ tự sau khi xếp.</li><li>Nếu đổi <code>Long.compare(b, a)</code> thành <code>Long.compare(a, b)</code> ở khoá 1 thì thứ tự là gì?</li></ol>
<p><b>Chọn A hay B?</b> Cần xếp giao dịch theo ngày ở một chỗ và theo tiền ở chỗ khác. A: lớp <code>GiaoDich implements Comparable</code>. B: hai bộ so sánh riêng. Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Có ba giao dịch, rút bốn trăm nghìn, nạp chín trăm nghìn, rút chín trăm nghìn. Khoá một là tiền giảm dần, khoá hai là loại tăng dần. Hãy viết thứ tự sau khi xếp, rồi thứ tự nếu đảo chiều khoá một.
           Rồi chọn giữa một thứ tự tự nhiên và hai bộ so sánh riêng, và giải thích vì sao. Hãy dừng video và tự làm.""", pause=25),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "(nap, 900000), (rut, 900000), (rut, 400000)", "tiền giảm: 900000, 900000, 400000; hai dòng cùng 900000 thì loại: <code>nap</code> &lt; <code>rut</code>"],
                  ["2", "(rut, 400000), (nap, 900000), (rut, 900000)", "tiền tăng dần; 900000 vẫn xếp <code>nap</code> trước <code>rut</code>"],
                  ["3", "<b>B</b>", "<code>Comparable</code> chỉ cho một thứ tự; hai ngữ cảnh cần hai thứ tự"]]),
           """Đáp án câu một, tiền giảm dần nên hai dòng chín trăm nghìn lên trước. Hai dòng ấy bằng nhau về tiền, nên xét khoá hai, nạp đứng trước rút theo thứ tự từ điển. Dòng bốn trăm nghìn xuống cuối.
           Câu hai, đảo chiều thì tiền tăng dần, bốn trăm nghìn lên đầu, hai dòng chín trăm nghìn vẫn xếp nạp trước rút. Câu ba chọn phương án B, vì thứ tự tự nhiên chỉ có một cách, mà ta cần hai cách.""",
           focus=[1, "1.2", "1.3", "1.4", "1.4"]),
        st("""<div class="box key"><b>Quy tắc chọn:</b> một thứ tự <b>hiển nhiên, duy nhất</b> (số, chuỗi, mã) &rarr; <code>Comparable</code>.
Nhiều thứ tự tuỳ ngữ cảnh, hay lớp không thuộc quyền bạn sửa &rarr; <code>Comparator</code>.</div>""",
           """Quy tắc chọn. Khi có một thứ tự hiển nhiên và duy nhất, như số hay mã, thì dùng thứ tự tự nhiên. Khi có nhiều thứ tự tuỳ ngữ cảnh, hoặc lớp không thuộc quyền bạn sửa, thì dùng bộ so sánh."""),
    ], checks=["sorted([('rut',400000),('nap',900000),('rut',900000)], key=lambda g: (-g[1], g[0])) == [('nap',900000),('rut',900000),('rut',400000)]",
               "sorted([('rut',400000),('nap',900000),('rut',900000)], key=lambda g: (g[1], g[0])) == [('rut',400000),('nap',900000),('rut',900000)]"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("hộp Object nổ lúc chạy", "Hop<T> bắt lỗi lúc biên dịch", "compareTo: âm, 0, dương", "bộ so sánh: khoá 1 rồi khoá 2",
                 "không dùng phép trừ", "n × log n so sánh"),
           """Tổng kết chuỗi logic. Hộp nhận mọi thứ thì lỗi nổ lúc chạy. Hộp có tham số kiểu bắt lỗi lúc biên dịch. So sánh trả âm, không hoặc dương. Bộ so sánh xét khoá một rồi mới tới khoá hai.
           Không dùng phép trừ để so sánh, vì có thể tràn. Và sắp xếp tốn cỡ n nhân lôgarit của n lần so sánh."""),
        st("""<div class='box key'><b>Tư duy:</b> chuyển lỗi về <b>sớm nhất có thể</b>: lúc gõ hơn lúc biên dịch, lúc biên dịch hơn lúc kiểm thử, lúc kiểm thử hơn lúc chạy thật.
Với mọi bộ so sánh, hỏi: <b>có nhất quán</b> không (a trước b thì b không trước a), <b>có tràn</b> không, và nó sẽ bị gọi <b>bao nhiêu triệu lần</b>.</div>""",
           """Điều cần mang theo. Hãy đưa lỗi về càng sớm càng tốt, lúc biên dịch hơn lúc chạy thật. Với mọi bộ so sánh, hỏi ba câu. Nó có nhất quán không, có bị tràn không, và sẽ bị gọi bao nhiêu triệu lần."""),
    ])
    return lesson("L02", "kieu_tong_quat_so_sanh", "Bài 2 — Kiểu tổng quát và sắp xếp: hộp, thứ tự tự nhiên, bộ so sánh",
                  "curriculum/jv2.yaml L02; audit/jv2/verify_jv2.py L02 (javac/java chạy thật, JDK 21; số lần so sánh đo bằng Random(42)); "
                  "The Java Language Specification, Java SE 21: §4.5 (kiểu có tham số), §8.1.2 (lớp tổng quát), §4.10.2 (List<Long> không phải List<Object>), "
                  "§5.1.3 (thu hẹp long sang int); java.lang.Comparable và java.util.Comparator (Java SE 21 API: hợp đồng dấu của kết quả); "
                  "java.util.List.sort (ổn định, TimSort); dev.java/learn",
                  ["Mô tả vì sao kiểu tổng quát đưa lỗi sai kiểu từ lúc chạy về lúc biên dịch",
                   "Nêu cách khai báo hộp tổng quát dùng cho nhiều kiểu và hàm có ràng buộc so sánh được",
                   "Sắp xếp danh sách giao dịch theo hai khoá bằng bộ so sánh",
                   "Phân biệt thứ tự tự nhiên và bộ so sánh để chọn đúng",
                   "Nhận ra số lần so sánh tăng theo n nhân logarit n và bẫy phép trừ làm tràn",
                   "Viết bộ so sánh hai khoá cho bảy giao dịch và chạy thử"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "intuition"), (2, "intuition"), (3, "example"), (4, "quiz"), (5, "scale"), (6, "practice")])
