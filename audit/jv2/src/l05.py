from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    mat = prog("MatCapNhat", r"""
import java.util.concurrent.CyclicBarrier;

public class MatCapNhat {
    static int soDu = 100;
    static CyclicBarrier hang = new CyclicBarrier(2);         // chờ đủ 2 luồng mới đi tiếp

    static Thread nap(int tien) {
        return new Thread(() -> {
            try {
                int doc = soDu;                               // 1. đọc số dư
                hang.await();                                 // đợi luồng kia cũng đã đọc
                soDu = doc + tien;                            // 2. ghi số dư mới
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        });
    }

    public static void main(String[] args) throws Exception {
        Thread a = nap(50), b = nap(30);
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("130 hoac 150: " + (soDu == 130 || soDu == 150));
        System.out.println("180 (dung): " + (soDu == 180));
    }
}""", out="130 hoac 150: true\n180 (dung): false")
    dua = prog("DuaTranh", r"""
public class DuaTranh {
    static int dem = 0;

    public static void main(String[] args) throws Exception {
        Runnable viec = () -> {
            for (int i = 0; i < 1000000; i++) {
                dem++;                                        // đọc, cộng, ghi: ba bước
            }
        };
        Thread a = new Thread(viec), b = new Thread(viec);
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("mong doi 2000000; thuc te nho hon: " + (dem < 2000000));
    }
}""", out="mong doi 2000000; thuc te nho hon: true")
    dong_bo = prog("DongBo", r"""
import java.util.concurrent.atomic.AtomicInteger;

public class DongBo {
    static int dem = 0;
    static final Object khoa = new Object();
    static AtomicInteger nguyenTu = new AtomicInteger();

    public static void main(String[] args) throws Exception {
        Runnable viec = () -> {
            for (int i = 0; i < 1000000; i++) {
                synchronized (khoa) {                         // chỉ một luồng vào khối này
                    dem++;
                }
                nguyenTu.incrementAndGet();                   // phép cộng nguyên tử
            }
        };
        Thread a = new Thread(viec), b = new Thread(viec);
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("synchronized: " + dem);
        System.out.println("nguyen tu: " + nguyenTu.get());
    }
}""", out="synchronized: 2000000\nnguyen tu: 2000000")
    nhom = prog("NhomLuong", r"""
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class NhomLuong {
    static long phi(long soTien) {
        return soTien <= 2000000 ? 3000 : 3000 + (soTien - 2000000) / 1000;
    }

    public static void main(String[] args) throws Exception {
        ExecutorService nhom = Executors.newFixedThreadPool(4);       // 4 luồng làm việc
        Map<String, Integer> dem = new ConcurrentHashMap<>();
        List<Future<Long>> hen = new ArrayList<>();
        for (int i = 1; i <= 5; i++) {
            long tien = i * 1000000L;
            String loai = (i % 2 == 0) ? "chan" : "le";
            hen.add(nhom.submit(() -> {
                dem.merge(loai, 1, Integer::sum);                     // cộng an toàn cho nhiều luồng
                return phi(tien);
            }));
        }
        long tong = 0;
        for (Future<Long> f : hen) {
            tong += f.get();                                          // đợi kết quả từng việc
        }
        nhom.shutdown();
        System.out.println("tong phi: " + tong);
        System.out.println(new TreeMap<>(dem));
    }
}""", out="tong phi: 21000\n{chan=2, le=3}")
    chay_run = prog("ChayHayBat", r"""
public class ChayHayBat {
    public static void main(String[] args) throws Exception {
        Runnable viec = () -> System.out.println("chay trong: " + Thread.currentThread().getName());
        Thread a = new Thread(viec, "nhan-vien");
        a.run();                                                  // gọi như hàm thường
        Thread b = new Thread(viec, "nhan-vien");
        b.start();                                                // mở luồng mới thật sự
        b.join();
    }
}""", out="chay trong: main\nchay trong: nhan-vien")
    loi_nhom = prog("LoiTrongNhom", r"""
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class LoiTrongNhom {
    public static void main(String[] args) throws Exception {
        ExecutorService nhom = Executors.newFixedThreadPool(2);
        Future<Long> hen = nhom.submit(() -> {
            if (true) {
                throw new IllegalArgumentException("so tien am");
            }
            return 1L;
        });
        System.out.println("da giao viec, chua thay loi gi");
        try {
            System.out.println(hen.get());                        // lỗi chỉ lộ ra ở đây
        } finally {
            nhom.shutdown();
        }
    }
}""", out="da giao viec, chua thay loi gi", expect="runtime_error:ExecutionException",
                    err='…ExecutionException: java.lang.IllegalArgumentException: so tien am')
    ket_cho = prog("KetCho", r"""
import java.lang.management.ManagementFactory;
import java.util.concurrent.CyclicBarrier;

public class KetCho {
    static class TaiKhoan {
        final int ma;
        long soDu;
        TaiKhoan(int ma, long soDu) { this.ma = ma; this.soDu = soDu; }
    }

    static CyclicBarrier hang = new CyclicBarrier(2);

    static void chuyen(TaiKhoan tu, TaiKhoan den, long tien) throws Exception {
        synchronized (tu) {                                       // khoá tài khoản nguồn trước
            hang.await();                                         // (ép hai luồng cùng ở đây)
            synchronized (den) {                                  // rồi mới khoá tài khoản đích
                tu.soDu -= tien;
                den.soDu += tien;
            }
        }
    }

    public static void main(String[] args) throws Exception {
        TaiKhoan a = new TaiKhoan(1, 100), b = new TaiKhoan(2, 100);
        Thread t1 = new Thread(() -> { try { chuyen(a, b, 10); } catch (Exception e) { } });
        Thread t2 = new Thread(() -> { try { chuyen(b, a, 20); } catch (Exception e) { } });
        t1.setDaemon(true);
        t2.setDaemon(true);
        t1.start();
        t2.start();
        Thread.sleep(500);
        long[] ket = ManagementFactory.getThreadMXBean().findDeadlockedThreads();
        System.out.println("so luong bi ket: " + (ket == null ? 0 : ket.length));
    }
}""", out="so luong bi ket: 2")
    sua_ket = prog("SuaKetCho", r"""
public class SuaKetCho {
    static class TaiKhoan {
        final int ma;
        long soDu;
        TaiKhoan(int ma, long soDu) { this.ma = ma; this.soDu = soDu; }
    }

    static void chuyen(TaiKhoan tu, TaiKhoan den, long tien) throws Exception {
        TaiKhoan truoc = tu.ma < den.ma ? tu : den;               // luôn khoá mã NHỎ trước
        TaiKhoan sau = tu.ma < den.ma ? den : tu;
        synchronized (truoc) {
            synchronized (sau) {
                tu.soDu -= tien;
                den.soDu += tien;
            }
        }
    }

    public static void main(String[] args) throws Exception {
        TaiKhoan a = new TaiKhoan(1, 100), b = new TaiKhoan(2, 100);
        Thread t1 = new Thread(() -> { try { chuyen(a, b, 10); } catch (Exception e) { } });
        Thread t2 = new Thread(() -> { try { chuyen(b, a, 20); } catch (Exception e) { } });
        t1.start();
        t2.start();
        t1.join(2000);
        t2.join(2000);
        System.out.println("xong; tong tien = " + (a.soDu + b.soDu) + ", A = " + a.soDu + ", B = " + b.soDu);
    }
}""", out="xong; tong tien = 200, A = 110, B = 90")
    gian = prog("ThoiGian", r"""
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class ThoiGian {
    static long chay(int soLuong, int soViec) throws Exception {
        ExecutorService nhom = Executors.newFixedThreadPool(soLuong);
        long bd = System.nanoTime();
        List<Future<Integer>> ds = new ArrayList<>();
        for (int i = 0; i < soViec; i++) {
            ds.add(nhom.submit(() -> {
                Thread.sleep(50);                                 // mỗi việc chờ 50 mili giây
                return 1;
            }));
        }
        for (Future<Integer> f : ds) {
            f.get();
        }
        nhom.shutdown();
        return (System.nanoTime() - bd) / 1000000;
    }

    public static void main(String[] args) throws Exception {
        for (int n : new int[]{10, 100}) {
            long lyThuyet = 400L / n * 50;                        // 400 việc / n luồng, mỗi lượt 50 ms
            long ms = chay(n, 400);
            boolean gan = ms >= lyThuyet && ms < lyThuyet * 3 / 2 + 100;
            System.out.println(n + " luong: ly thuyet " + lyThuyet + " ms, do gan dung: " + gan);
        }
    }
}""", out="10 luong: ly thuyet 2000 ms, do gan dung: true\n100 luong: ly thuyet 200 ms, do gan dung: true")

    lab = prog("DemSaiDung", r"""
import java.util.concurrent.atomic.AtomicInteger;

public class DemSaiDung {
    static int thuong = 0;
    static int dongBo = 0;
    static final Object khoa = new Object();
    static AtomicInteger nguyenTu = new AtomicInteger();

    public static void main(String[] args) throws Exception {
        Runnable viec = () -> {
            for (int i = 0; i < 250000; i++) {
                thuong++;
                synchronized (khoa) {
                    dongBo++;
                }
                nguyenTu.incrementAndGet();
            }
        };
        Thread[] ds = new Thread[4];
        for (int i = 0; i < ds.length; i++) {
            ds[i] = new Thread(viec);
            ds[i].start();
        }
        for (Thread t : ds) {
            t.join();
        }
        System.out.println("Khong dong bo: dem < 1000000 -> " + (thuong < 1000000));
        System.out.println("Dong bo: " + dongBo);
        System.out.println("Nguyen tu: " + nguyenTu.get());
    }
}""", out="Khong dong bo: dem < 1000000 -> true\nDong bo: 1000000\nNguyen tu: 1000000")
    write_lab("JV2", "L05", """# Lab JV2 L05 — Đo tranh chấp dữ liệu và sửa cho đúng

Viết `DemSaiDung` (tệp `DemSaiDung.java`). **Bốn luồng**, mỗi luồng lặp **250 000** lần; mỗi vòng làm ba việc:

1. tăng biến `static int thuong` bằng `thuong++` (không bảo vệ);
2. tăng biến `static int dongBo` **bên trong** `synchronized (khoa) { … }`;
3. tăng `AtomicInteger nguyenTu` bằng `incrementAndGet()`.

Tạo bốn `Thread` từ cùng một `Runnable`, `start()` cả bốn rồi `join()` cả bốn. In ba dòng:

```
Khong dong bo: dem < 1000000 -> true
Dong bo: 1000000
Nguyen tu: 1000000
```

(Dòng đầu in `thuong < 1000000` — giá trị thật của `thuong` thay đổi mỗi lần chạy, nên bài chỉ in kết quả so sánh.)

Chạy: `javac DemSaiDung.java && java DemSaiDung`. Chấm: `bash labs/cham.sh JV2 L05 DemSaiDung.java`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: bốn luồng cùng cộng, đo và sửa", practice_steps(
        st, "JV2", "L05",
        """<p><b>Đề</b>: <b>4 luồng</b>, mỗi luồng <b>250 000</b> vòng, ba biến đếm.</p>
<ol><li><code>thuong++</code> không bảo vệ; <code>dongBo++</code> trong <code>synchronized</code>; <code>nguyenTu.incrementAndGet()</code>.</li>
<li><code>start()</code> cả bốn luồng, rồi <code>join()</code> cả bốn.</li>
<li>In ba dòng: <code>thuong &lt; 1000000</code>, <code>dongBo</code>, <code>nguyenTu</code>.</li></ol>
<p class="note">Giá trị thật của <code>thuong</code> đổi mỗi lần chạy; chỉ in kết quả so sánh. Tệp <code>DemSaiDung.java</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Bốn luồng, mỗi luồng lặp hai trăm năm mươi nghìn vòng, và mỗi vòng tăng ba biến. Một biến thường không bảo vệ, một biến tăng trong khối đồng bộ, và một biến nguyên tử.
        Mở cả bốn luồng rồi đợi cả bốn xong. In ba dòng, dòng đầu chỉ in kết quả so sánh vì giá trị thật đổi mỗi lần chạy. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        lab["out"], "DemSaiDung.java",
        """<div class="box key"><b>Nếu kẹt:</b> <code>Thread[] ds = new Thread[4];</code> rồi vòng <code>for</code> tạo và <code>start()</code>; vòng <code>for</code> thứ hai <code>join()</code>.
Khối đồng bộ: <code>synchronized (khoa) { dongBo++; }</code>. Lời giải: <code>labs/JV2/L05/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, tạo mảng bốn luồng, một vòng để mở và một vòng để đợi. Biến đồng bộ tăng bên trong khối đồng bộ với một đối tượng khoá dùng chung. Biến nguyên tử dùng hàm tăng và lấy.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=240), "JV2", "L05")

    sc_hook = sc("hook", "hook", "Hai khách cùng nạp tiền một giây: số dư mất một khoản", [
        st(svg(1500, 330,
               box(20, 40, 330, 90, ["luồng A: nạp 50", "đọc: 100"], C_BLUE, 26, bold=True),
               box(20, 200, 330, 90, ["luồng B: nạp 30", "đọc: 100"], C_AMBER, 26, bold=True),
               arrow(355, 85, 560, 160, "#2a78d6"), arrow(355, 245, 560, 190, "#d97706"),
               box(565, 110, 330, 100, ["số dư = 100", "(cả hai đều thấy)"], C_GRAY, 26),
               arrow(900, 160, 1000, 85, "#2a78d6", "A ghi 150"), arrow(900, 160, 1000, 245, "#d97706", "B ghi 130"),
               box(1005, 40, 470, 90, ["kết quả 130 hoặc 150"], C_RED, 26, bold=True),
               txt(1240, 270, "đáng ra phải là 180: mất 30 hoặc 50", 26, "middle", "#dc2626", True)),
           """Số dư một trăm. Khách A nạp năm mươi, khách B nạp ba mươi, cùng một giây. Mỗi luồng đọc số dư, cộng, rồi ghi lại. Nếu cả hai cùng đọc một trăm trước khi ai kịp ghi, thì người ghi sau đè lên người ghi trước.
           Kết quả là một trăm ba mươi hoặc một trăm năm mươi, trong khi đúng ra là một trăm tám mươi. Một khoản tiền biến mất và không có lỗi nào được báo."""),
        st("""<div class="box key">Hôm nay: <b>luồng</b>. Cách chạy nhiều việc cùng lúc, <b>vì sao</b> nó làm hỏng dữ liệu, ba cách sửa (<b>khoá</b>, phép <b>nguyên tử</b>, <b>nhóm luồng</b>),
và một bẫy chỉ xảy ra khi tải tăng: <b>bế tắc</b>. Kèm câu hỏi quy mô: cần bao nhiêu luồng để phục vụ gấp một trăm lần số yêu cầu?</div>""",
           """Hôm nay ta học luồng, cách chạy nhiều việc cùng lúc, vì sao nó làm hỏng dữ liệu, và ba cách sửa là khoá, phép nguyên tử và nhóm luồng. Cuối cùng là một bẫy chỉ xảy ra khi tải tăng, gọi là bế tắc.
           Kèm câu hỏi quy mô, cần bao nhiêu luồng để phục vụ gấp một trăm lần số yêu cầu.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: biến, vòng lặp, hàm ngắn, ngoại lệ", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① cộng vào biến", "<code>dem++</code> trông là một bước, nhưng máy làm ba: <b>đọc</b> giá trị, <b>cộng</b> một, <b>ghi</b> lại"],
                  ["② hàm ngắn", "<code>() -&gt; { … }</code> là một việc viết gọn; có thể đưa cho hàm khác chạy"],
                  ["③ ngoại lệ", "lỗi dừng luồng đang chạy; <code>try … catch</code> bắt lại ở nơi gọi"],
                  ["④ trạng thái chung", "một biến <code>static</code> chỉ có <b>một bản</b>, mọi nơi trong chương trình cùng thấy và cùng sửa"]]),
           """Ta ôn lại bốn điều. Lệnh tăng một trông là một bước, nhưng máy làm ba bước, đọc, cộng và ghi. Hàm ngắn là một việc viết gọn và có thể đưa cho nơi khác chạy. Ngoại lệ làm dừng việc đang chạy và có thể bắt lại.
           Biến dùng chung chỉ có một bản, mọi nơi cùng thấy và cùng sửa. Ba bước của lệnh tăng và biến dùng chung chính là gốc của lỗi hôm nay.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã tám thứ của luồng", [
        st(table(["viết", "nghĩa"],
                 [["luồng (<code>Thread</code>)", "một <b>đường chạy</b> riêng trong cùng chương trình; nhiều luồng chạy xen kẽ hoặc song song, <b>dùng chung bộ nhớ</b>"],
                  ["<code>t.start()</code> / <code>t.join()</code>", "mở luồng chạy / <b>đợi</b> luồng đó kết thúc; gọi <code>t.run()</code> thì <b>không</b> mở luồng mới"],
                  ["tranh chấp dữ liệu (race)", "kết quả <b>phụ thuộc thứ tự xen kẽ</b> của các luồng, nên khác nhau giữa các lần chạy"],
                  ["<code>synchronized (khoa) { … }</code>", "<b>khoá</b>: tại một thời điểm chỉ <b>một</b> luồng được vào khối; luồng khác chờ ngoài cửa"],
                  ["<code>AtomicInteger</code>", "số nguyên có phép tăng <b>nguyên tử</b>: đọc–cộng–ghi xảy ra trọn vẹn như một bước"],
                  ["<code>ExecutorService</code>", "<b>nhóm luồng</b> có sẵn; <code>submit(việc)</code> giao việc, trả về <code>Future</code>"],
                  ["<code>Future&lt;T&gt;</code>", "<b>phiếu hẹn</b>: <code>get()</code> đợi và lấy kết quả (hoặc ném lại lỗi của việc)"],
                  ["<code>ConcurrentHashMap</code>", "bản đồ an toàn cho nhiều luồng; <code>merge(khoá, 1, Integer::sum)</code> cộng nguyên tử"]]),
           """Bảng này có tám thứ. Luồng là một đường chạy riêng trong cùng chương trình, các luồng dùng chung bộ nhớ. Hàm mở luồng khác với hàm đợi luồng, và gọi hàm chạy trực tiếp thì không mở luồng nào.
           Tranh chấp dữ liệu là khi kết quả phụ thuộc thứ tự xen kẽ. Khoá chỉ cho một luồng vào khối tại một thời điểm. Số nguyên nguyên tử làm trọn vẹn cả ba bước đọc, cộng, ghi như một bước. Nhóm luồng có sẵn, giao việc thì nhận về một phiếu hẹn.
           Lấy phiếu hẹn thì đợi và nhận kết quả. Và bản đồ an toàn cho nhiều luồng có hàm cộng nguyên tử.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: sáu cách xen kẽ, và khoá biến chúng thành hai", [
        st(svg(1500, 330,
               txt(140, 70, "luồng A", 28, "middle", "#2a78d6", True), txt(140, 200, "luồng B", 28, "middle", "#d97706", True),
               box(260, 40, 280, 60, "đọc: 100", C_BLUE, 24), box(560, 40, 280, 60, "ghi: 100+50", C_BLUE, 24),
               box(260, 170, 280, 60, "đọc: 100", C_AMBER, 24), box(860, 170, 280, 60, "ghi: 100+30", C_AMBER, 24),
               arrow(200, 290, 1300, 290, "#475569"), txt(1380, 296, "thời gian", 24, "middle", "#475569"),
               txt(560, 140, "cả hai đọc 100 trước khi ai ghi", 24, "middle", "#dc2626", True),
               txt(1200, 70, "ghi 150, rồi bị B ghi đè 130", 24, "middle", "#dc2626", True)),
           """Trước hết là hình. Hai đường thời gian của hai luồng. Cả hai cùng đọc một trăm trước khi ai kịp ghi. Luồng A ghi một trăm năm mươi, rồi luồng B ghi một trăm ba mươi, đè lên kết quả của A. Khoản năm mươi biến mất."""),
        st(code_block(mat, lines=(7, 17)),
           """Ta tái hiện lỗi mà không phụ thuộc may rủi. Mỗi luồng đọc số dư, rồi chờ ở một hàng rào cho tới khi luồng kia cũng đã đọc, rồi mới ghi số dư mới. Hàng rào ép cả hai cùng thấy một trăm trước khi ai kịp ghi.""", clear=True),
        st(out_block(mat) + "<p class='note'>Không có lần chạy nào cho 180. Kết quả 130 hay 150 tuỳ luồng nào ghi sau; <b>tiền của luồng ghi trước bị mất</b>.</p>",
           """Kết quả thật. Số dư luôn là một trăm ba mươi hoặc một trăm năm mươi, không bao giờ một trăm tám mươi. Luồng ghi sau đè lên luồng ghi trước, nên khoản của luồng ghi trước biến mất.""", clear=True),
        st(table(["thứ tự xen kẽ", "A đọc", "B đọc", "A ghi", "B ghi", "kết quả"],
                 [["A trọn, rồi B trọn", "100", "150", "150", "180", "<b>180</b> đúng"],
                  ["B trọn, rồi A trọn", "130", "100", "180", "130", "<b>180</b> đúng"],
                  ["cả hai đọc trước, A ghi sau", "100", "100", "150", "130", "<b>150</b> mất 30"],
                  ["cả hai đọc trước, B ghi sau", "100", "100", "150", "130", "<b>130</b> mất 50"]])
           + "<p class='note'>Hai hàng đầu: hai luồng nối đuôi nhau (có khoá). Hai hàng sau: xen kẽ làm mất tiền.</p>",
           """Ta liệt kê các cách xen kẽ. Nếu hai luồng nối đuôi nhau, luồng này xong rồi luồng kia mới bắt đầu, thì kết quả luôn là một trăm tám mươi, đúng. Nếu cả hai cùng đọc trước khi ai ghi, thì kết quả là một trăm năm mươi hoặc một trăm ba mươi tuỳ ai ghi sau, và sai.
           Khoá làm cho chỉ còn hai cách nối đuôi, loại bỏ mọi cách xen kẽ.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: vì sao khoá và phép nguyên tử sửa được", [
        st("<p><b>Bước 1.</b> <code>dem++</code> là ba bước máy: <code>t = dem</code>; <code>t = t + 1</code>; <code>dem = t</code>.</p>"
           "<p>Hai luồng có thể cùng làm bước 1 trước khi ai làm bước 3 &rarr; <b>một lần cộng bị mất</b>.</p>",
           """Bước một, tách lệnh tăng ra. Máy đọc giá trị vào ô tạm, cộng một vào ô tạm, rồi ghi ô tạm trở lại. Nếu hai luồng cùng đọc trước khi ai ghi, thì cả hai cùng ghi lại cùng một giá trị, nên một lần cộng bị mất.""", clear=True),
        st("<p><b>Bước 2.</b> Khối <code>synchronized (khoa)</code> bắt ba bước phải <b>chạy trọn</b> trước khi luồng khác vào:</p>"
           "<p>luồng A: [đọc, cộng, ghi] &rarr; luồng B: [đọc, cộng, ghi]</p>",
           """Bước hai, đặt ba bước vào một khối có khoá. Vì chỉ một luồng được vào khối tại một thời điểm, nên ba bước của luồng này phải chạy trọn trước khi luồng kia bắt đầu. Ta chỉ còn các cách nối đuôi, không còn xen kẽ.""", clear=True),
        st("<p><b>Bước 3.</b> Phép nguyên tử làm cùng việc <b>không cần khoá</b>: phần cứng có lệnh <b>so sánh rồi đổi</b> trong một bước.</p>"
           "<p><code>nguyenTu.incrementAndGet()</code> &rarr; luôn đúng; thường nhanh hơn khoá khi chỉ có <b>một ô</b> cần bảo vệ.</p>",
           """Bước ba, phép nguyên tử. Phần cứng có sẵn lệnh so sánh rồi đổi trong một bước, nên số nguyên nguyên tử làm cả ba việc đọc, cộng, ghi mà không cần khoá. Khi chỉ có một ô cần bảo vệ, cách này thường nhanh hơn khoá.""", clear=True),
        st("<p><b>Bước 4.</b> Thử bằng số: 2 luồng, mỗi luồng cộng 1 000 000 lần:</p>"
           "$$\\text{đúng} = 2 \\times 1\\,000\\,000 = \\hl{2\\,000\\,000}$$"
           "<p>Không khoá: mỗi lần xen kẽ làm mất ít nhất 1, nên thực tế <b>nhỏ hơn</b> (thường chỉ còn một phần nhỏ).</p>",
           """Bước bốn, thử bằng số. Hai luồng, mỗi luồng cộng một triệu lần, thì kết quả đúng là hai triệu. Khi không khoá, mỗi lần xen kẽ làm mất ít nhất một lần cộng, nên kết quả thực tế nhỏ hơn hai triệu, và thường nhỏ hơn rất nhiều.""", clear=True),
    ], checks=["2 * 1000000 == 2000000"])
    sc_ex = sc("example", "example", "Ví dụ: đo tranh chấp, sửa bằng khoá, rồi giao việc cho nhóm luồng", [
        st(code_block(dua, lines=(5, 14)),
           """Ta đo thật. Hai luồng, mỗi luồng cộng một triệu lần vào cùng một biến. Đúng ra phải ra hai triệu."""),
        st("<p><b>① Đúng là</b> $2 \\times 1\\,000\\,000 = 2\\,000\\,000$.</p><p><b>② Thực tế (không khoá)</b> luôn nhỏ hơn, giá trị đổi mỗi lần chạy.</p>"
           + out_block(dua),
           """Phép làm thứ nhất, đúng ra phải là hai triệu. Phép thứ hai, chạy thật thì kết quả nhỏ hơn hai triệu và đổi mỗi lần chạy, nên chương trình chỉ in ra việc nó nhỏ hơn. Một kết quả đổi theo từng lần chạy là dấu hiệu rõ ràng của tranh chấp dữ liệu.""", clear=True),
        st(code_block(dong_bo, lines=(9, 16)) + out_block(dong_bo),
           """Phép làm thứ ba, sửa bằng hai cách. Đặt phép tăng trong khối có khoá, hoặc dùng số nguyên nguyên tử. Cả hai đều cho đúng hai triệu, mọi lần chạy.""", clear=True),
        st(code_block(nhom, lines=(16, 26)),
           """Phép làm thứ tư, giao việc cho nhóm luồng. Nhóm có bốn luồng, ta giao năm việc, mỗi việc tính phí của một số tiền và ghi lại việc loại chẵn hay lẻ vào bản đồ an toàn. Mỗi lần giao việc ta nhận về một phiếu hẹn.""", clear=True),
        st("$$③ \\; \\text{phí} (1, 2, 3, 4, 5 \\text{ triệu}) = 3\\,000 + 3\\,000 + 4\\,000 + 5\\,000 + 6\\,000 = \\hl{21\\,000}$$"
           "$$④ \\; \\text{lẻ} = 3 \\; (1, 3, 5), \\quad \\text{chẵn} = 2 \\; (2, 4)$$" + code_block(nhom, lines=(28, 33)) + out_block(nhom),
           """Phép thứ ba, tính tay các phí. Một triệu và hai triệu đều là ba nghìn, ba triệu là bốn nghìn, bốn triệu là năm nghìn, năm triệu là sáu nghìn, cộng lại hai mươi mốt nghìn. Phép thứ tư, ba việc lẻ và hai việc chẵn.
           Chạy thật, in ra đúng hai mươi mốt nghìn và bản đồ hai chẵn ba lẻ, dù các việc chạy xen kẽ trên bốn luồng.""", clear=True),
    ], checks=["3000 + 3000 + 4000 + 5000 + 6000 == 21000", "3000 + (3000000 - 2000000) // 1000 == 4000", "3000 + (5000000 - 2000000) // 1000 == 6000",
               "len([1, 3, 5]) == 3", "len([2, 4]) == 2"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: tính tuần tự một luồng", [
        st("<p>Tính lại bằng <b>một luồng</b>, không có gì xen kẽ: tổng phí = <code>3000 + 3000 + 4000 + 5000 + 6000</code> = <b>21 000</b> ✓ khớp với nhóm luồng.</p>"
           "<p>Và bộ đếm: một luồng cộng 2 000 000 lần cho đúng <b>2 000 000</b>, bằng kết quả của khoá và của phép nguyên tử.</p>",
           """Cách kiểm khác là tính lại bằng một luồng, nơi không có gì xen kẽ, nên kết quả tuần tự là chuẩn so sánh. Tổng phí tính tuần tự là hai mươi mốt nghìn, khớp với nhóm luồng. Một luồng cộng hai triệu lần cho đúng hai triệu, bằng kết quả của khoá và phép nguyên tử.
           Vậy hai cách sửa không làm mất hay thừa lần cộng nào."""),
        st("<p>Kiểm tính chất bất biến: sau mọi chuyển tiền, <b>tổng tiền không đổi</b>. A + B = 100 + 100 = <b>200</b> trước và sau khi chuyển 10 từ A sang B (A = 90, B = 110): 90 + 110 = 200 ✓</p>",
           """Cách kiểm thứ hai là tính chất bất biến của ngân hàng. Sau mọi lần chuyển tiền, tổng tiền không đổi. Hai tài khoản mỗi bên một trăm, chuyển mười từ A sang B, còn chín mươi và một trăm mười, tổng vẫn hai trăm. Ta sẽ dùng chính tính chất này để bắt lỗi tiếp theo.""", clear=True),
    ], checks=["3000 + 3000 + 4000 + 5000 + 6000 == 21000", "100 + 100 == 200", "90 + 110 == 200"])
    sc_scale = sc("scale", "concept", "Khi số yêu cầu tăng một trăm lần, mười nghìn lần: bao nhiêu luồng?", [
        st(code_block(gian, lines=(27, 32)) + out_block(gian),
           """Ta đo thật. Bốn trăm việc, mỗi việc chờ năm mươi mili giây, như chờ cơ sở dữ liệu. Nhóm mười luồng làm bốn mươi lượt, mỗi lượt năm mươi mili giây, cần hai nghìn mili giây. Nhóm một trăm luồng chỉ cần bốn lượt, hai trăm mili giây.
           Đo thật khớp lý thuyết, nên ta dùng được công thức để dự đoán.""", clear=True),
        st(table(["yêu cầu mỗi giây", "100", "10 000", "1 000 000"],
                 [["số luồng cần = tốc độ × thời gian một việc (0,05 giây)", "5", "<b>500</b>", "<b>50 000</b>"],
                  ["bộ nhớ riêng cho ngăn xếp (≈ 1 megabyte một luồng, mặc định thường gặp)", "≈ 5 MB", "≈ 500 MB", "<b>≈ 50 GB</b>"]])
           + "<p class='note'>Công thức: số việc đang chạy = tốc độ đến × thời gian xử lý (định luật Little). 1 MB mỗi luồng là mặc định thường gặp trên máy 64 bit, tuỳ hệ điều hành.</p>",
           """Giờ nhân quy mô. Số luồng cần bằng tốc độ yêu cầu nhân thời gian xử lý một việc, đây là một định luật của lý thuyết xếp hàng. Một trăm yêu cầu mỗi giây cần năm luồng. Mười nghìn yêu cầu mỗi giây cần năm trăm luồng. Một triệu yêu cầu mỗi giây cần năm mươi nghìn luồng.
           Mỗi luồng giữ riêng chừng một megabyte ngăn xếp, nên năm mươi nghìn luồng cần cỡ năm mươi gigabyte, vượt quá bộ nhớ của hầu hết máy.""", clear=True),
        st("""<div class="box warn"><b>Đánh đổi của người làm nghề:</b> thêm luồng chỉ giúp khi việc <b>chờ</b> (mạng, cơ sở dữ liệu). Việc <b>tính toán</b> thuần thì quá số lõi CPU không nhanh hơn.
Khoá thì ngược lại: <b>nhiều luồng tranh một khoá thì xếp hàng</b>, quá nhiều luồng làm chậm đi. Giải pháp khi tải quá lớn là luồng nhẹ, hàng đợi và chia nhỏ khoá; mỗi cách có giá riêng.</div>""",
           """Đánh đổi của người làm nghề. Thêm luồng chỉ giúp khi việc phải chờ, như mạng hay cơ sở dữ liệu. Việc tính toán thuần thì quá số lõi của bộ xử lý không nhanh hơn. Khoá thì ngược lại, nhiều luồng tranh một khoá thì phải xếp hàng, quá nhiều luồng làm chương trình chậm đi.
           Khi tải quá lớn, người ta dùng luồng nhẹ, hàng đợi và chia nhỏ khoá, mỗi cách có giá riêng.""", clear=True),
    ], checks=["400 // 10 * 50 == 2000", "400 // 100 * 50 == 200", "100 * 0.05 == 5", "10000 * 0.05 == 500", "1000000 * 0.05 == 50000", "50000 * 1 // 1000 == 50"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Gọi <code>run()</code> thay cho <code>start()</code>: không có luồng mới.</div>'
           + code_block(chay_run, lines=(3, 8)) + out_block(chay_run),
           """Lỗi thứ nhất là gọi hàm chạy thay vì hàm mở luồng. Hàm chạy chỉ là một hàm thường, nên việc được làm ngay trong luồng chính, không ai chạy song song. Hàm mở luồng mới tạo ra luồng thật, in tên luồng nhân viên."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Lỗi trong nhóm luồng bị giấu cho tới khi lấy kết quả.</div>'
           + code_block(loi_nhom, lines=(8, 13)) + code_block(loi_nhom, lines=(16, 16)) + out_block(loi_nhom),
           """Lỗi thứ hai là lỗi bị giấu. Việc giao cho nhóm luồng nổ ngoại lệ, nhưng không ai thấy, chương trình in rằng đã giao việc. Lỗi chỉ lộ ra khi lấy kết quả từ phiếu hẹn, được bọc trong một ngoại lệ khác. Nếu không bao giờ lấy kết quả thì lỗi mất tăm.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Bế tắc: chuyển A&rarr;B và B&rarr;A cùng lúc, mỗi luồng giữ một khoá và chờ khoá kia.</div>'
           + code_block(ket_cho, lines=(14, 19)),
           """Lỗi thứ ba hay gặp ở người đã đi làm. Chuyển tiền cần khoá cả hai tài khoản. Luồng một khoá A rồi chờ B, luồng hai khoá B rồi chờ A. Mỗi bên giữ thứ bên kia cần và chờ thứ bên kia đang giữ, nên không ai đi tiếp được. Đó là bế tắc.""", clear=True),
        st(out_block(ket_cho) + '<div class="box key"><b>Cách sửa:</b> luôn khoá theo <b>một thứ tự chung</b>, ví dụ mã nhỏ trước.</div>',
           """Bộ công cụ đếm được hai luồng bị kẹt. Cách sửa là luôn khoá theo một thứ tự chung, ví dụ mã tài khoản nhỏ trước.""", clear=True),
        st(code_block(sua_ket, lines=(10, 19)) + out_block(sua_ket),
           """Khi mọi luồng cùng đi theo một chiều thì không tạo được vòng chờ. Chạy lại, cả hai chuyển tiền đều xong, và tổng tiền vẫn là hai trăm, đúng tính chất bất biến.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Ba luồng, mỗi luồng chạy <code>for (int i = 0; i &lt; 500; i++) dem++;</code> trên biến <code>static int dem = 0</code> (không khoá).</p>
<ol><li>Giá trị <b>đúng</b> của <code>dem</code> nếu không có tranh chấp?</li>
<li>Khi có tranh chấp, <code>dem</code> có thể ra <b>1 501</b> không? Có thể ra <b>1 200</b> không?</li></ol>
<p><b>Chọn A hay B?</b> Cần cộng dồn <b>một</b> bộ đếm từ 8 luồng. A: <code>synchronized</code>. B: <code>AtomicLong</code>. Và nếu phải cập nhật <b>hai biến liên quan nhau</b> (số dư A và số dư B) thì sao? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Ba luồng, mỗi luồng cộng năm trăm lần vào một biến không khoá. Hãy nói giá trị đúng nếu không có tranh chấp. Và khi có tranh chấp thì giá trị có thể ra một nghìn năm trăm lẻ một không, có thể ra một nghìn hai trăm không.
           Rồi chọn giữa khoá và số nguyên nguyên tử để cộng dồn một bộ đếm từ tám luồng, và nếu phải cập nhật hai biến liên quan nhau thì sao. Hãy dừng video và tự làm.""", pause=30),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "<b>1 500</b>", "3 × 500"],
                  ["2", "1 501: <b>không</b>; 1 200: <b>có thể</b>", "mỗi lần ghi chỉ cộng đúng 1 vào giá trị đã đọc nên tối đa 1 500; xen kẽ chỉ làm <b>mất</b> lần cộng"],
                  ["3", "một bộ đếm: <b>B</b>; hai biến liên quan: <b>A (khoá)</b>", "phép nguyên tử chỉ bảo vệ <b>từng ô</b>; hai biến cần cùng thay đổi phải nằm trong <b>một khối có khoá</b>"]]),
           """Đáp án câu một, giá trị đúng là ba nhân năm trăm, bằng một nghìn năm trăm. Câu hai, một nghìn năm trăm lẻ một thì không bao giờ có, vì mỗi lần ghi chỉ cộng đúng một, còn một nghìn hai trăm thì có thể, vì xen kẽ chỉ làm mất các lần cộng.
           Câu ba, một bộ đếm thì chọn số nguyên tử. Hai biến liên quan nhau thì chọn khoá, vì phép nguyên tử chỉ bảo vệ từng ô, còn hai biến cùng đổi phải nằm trong một khối có khoá.""",
           focus=[1, "1.2", "1.3", "1.4"]),
        st("""<div class="box key"><b>Quy tắc:</b> bảo vệ <b>một ô</b> &rarr; phép nguyên tử; bảo vệ <b>một nhóm giá trị phải đổi cùng lúc</b> &rarr; khoá. Và luôn khoá theo <b>cùng một thứ tự</b>.</div>""",
           """Quy tắc rút ra. Bảo vệ một ô thì dùng phép nguyên tử. Bảo vệ một nhóm giá trị phải đổi cùng lúc thì dùng khoá. Và luôn khoá theo cùng một thứ tự."""),
    ], checks=["3 * 500 == 1500"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("dem++ = đọc, cộng, ghi", "xen kẽ ⇒ mất cập nhật".replace("⇒", "thì"), "khoá: chạy trọn rồi nhường", "nguyên tử: một ô", "nhóm luồng + phiếu hẹn",
                 "khoá theo thứ tự chung", "luồng cần = tốc độ × thời gian"),
           """Tổng kết chuỗi logic. Lệnh tăng gồm ba bước đọc, cộng, ghi. Các luồng xen kẽ thì mất cập nhật. Khoá bắt một khối chạy trọn rồi mới nhường. Phép nguyên tử bảo vệ một ô. Nhóm luồng giao việc và trả phiếu hẹn.
           Luôn khoá theo thứ tự chung để tránh bế tắc. Và số luồng cần bằng tốc độ nhân thời gian xử lý."""),
        st("""<div class='box key'><b>Tư duy:</b> với mọi dữ liệu dùng chung, hỏi bốn câu: <b>ai</b> cùng sửa nó, có <b>bất biến</b> nào cần giữ sau mỗi thao tác (tổng tiền),
cần khoá <b>mấy thứ</b> và theo thứ tự nào, và khi tải tăng <b>một trăm lần</b> thì nó xếp hàng ở đâu.</div>""",
           """Điều cần mang theo. Với mọi dữ liệu dùng chung, hãy hỏi bốn câu. Ai cùng sửa nó. Có bất biến nào cần giữ sau mỗi thao tác, ví dụ tổng tiền. Cần khoá mấy thứ và theo thứ tự nào. Và khi tải tăng gấp một trăm lần thì nó xếp hàng ở đâu."""),
    ])
    return lesson("L05", "luong_race_khoa_nhom_luong", "Bài 5 — Luồng: tranh chấp dữ liệu, khoá và nhóm luồng",
                  "curriculum/jv2.yaml L05; audit/jv2/verify_jv2.py L05 (javac/java chạy thật, JDK 21; hàng rào CyclicBarrier ép xen kẽ; ThreadMXBean.findDeadlockedThreads); "
                  "The Java Language Specification, Java SE 21: §17.4 (mô hình bộ nhớ), §14.19 (synchronized), §17.1; "
                  "java.util.concurrent (Java SE 21 API: ExecutorService, Future.get ném ExecutionException, ConcurrentHashMap.merge, atomic); "
                  "Little, J. D. C. (1961), A Proof for the Queuing Formula L = λW, Operations Research 9(3); "
                  "java launcher -Xss (JDK 21 tools: ngăn xếp luồng mặc định 1 MB trên Linux x64); dev.java/learn",
                  ["Mô tả vì sao hai luồng cùng cộng vào một biến thì mất cập nhật",
                   "Đo tranh chấp dữ liệu và sửa bằng khoá hoặc phép nguyên tử",
                   "Dùng nhóm luồng và phiếu hẹn để chạy nhiều việc và gom kết quả",
                   "Nhận ra bế tắc khi khoá hai thứ và sửa bằng thứ tự khoá chung",
                   "Nhận ra số luồng cần tăng theo tốc độ nhân thời gian xử lý, và khi nào thêm luồng không còn giúp ích",
                   "Viết chương trình bốn luồng đo tranh chấp và sửa đúng"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "intuition"), (2, "example"), (3, "example"), (4, "pitfalls"), (5, "scale"), (6, "practice")])
