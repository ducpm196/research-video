from lib import *

# ── Mã Java hiện trên màn hình (chạy NGUYÊN VĂN bằng javac/java: audit/bnx/screen/l16.yaml, audit/bnx/ver/l16.py) ──
# Mỗi hằng là MỘT tệp Java đầy đủ; màn hình hiện từng đoạn bằng code(…, lines=(a, b)). Tên lớp = JAVA_CLASS[tên hằng].
JAVA_CLASS = {"J_POOL": "BeLuong", "J_QUEUE": "HangDoi", "J_CF": "GhepLoiGoi", "J_FJ": "ChiaDoi", "J_SHARED": "DungChung",
              "J_CHECK": "KiemLai"}

J_POOL = r'''
import java.util.*;
import java.util.concurrent.*;
public class BeLuong {
  public static void main(String[] a) throws Exception {
    ExecutorService be = Executors.newFixedThreadPool(4);
    Set<String> luong = ConcurrentHashMap.newKeySet();
    List<Future<Integer>> hen = new ArrayList<>();
    for (int i = 1; i <= 10; i++) {
      int so = i;
      hen.add(be.submit(() -> {
        Thread.sleep(100);               // mỗi việc chờ 100 ms
        luong.add(Thread.currentThread().getName());
        return so * so;
      }));
    }
    int tong = 0;
    for (Future<Integer> h : hen) tong += h.get();  // chờ kết quả
    be.shutdown();
    System.out.println("số luồng đã dùng: " + luong.size());
    System.out.println("tổng 10 kết quả: " + tong);
    System.out.println("số lượt: " + (10 + 4 - 1) / 4);
  }
}
'''

J_QUEUE = r'''
import java.util.concurrent.*;
public class HangDoi {
  public static void main(String[] a) {
    CountDownLatch cua = new CountDownLatch(1);  // giữ việc lại
    ThreadPoolExecutor be = new ThreadPoolExecutor(4, 4, 0,
        TimeUnit.SECONDS, new ArrayBlockingQueue<>(2));
    int nhan = 0, tuChoi = 0;
    for (int i = 1; i <= 10; i++) {
      try {
        be.execute(() -> {
          try { cua.await(); } catch (InterruptedException e) { }
        });
        nhan++;
      } catch (RejectedExecutionException e) { tuChoi++; }
    }
    System.out.println("số luồng: " + be.getPoolSize());
    System.out.println("trong hàng đợi: " + be.getQueue().size());
    System.out.println("nhận " + nhan + ", từ chối " + tuChoi);
    cua.countDown();
    be.shutdown();
  }
}
'''

J_CF = r'''
import java.util.*;
import java.util.concurrent.*;
import static java.util.concurrent.CompletableFuture.*;
public class GhepLoiGoi {
  static Queue<String> xong = new ConcurrentLinkedQueue<>();
  static int goi(String ten, int ms, int giaTri) {
    try { Thread.sleep(ms); } catch (InterruptedException e) { }
    xong.add(ten);                     // ghi lại thứ tự xong
    return giaTri;
  }
  public static void main(String[] a) {
    ExecutorService be = Executors.newFixedThreadPool(3);
    long t0 = System.nanoTime();
    var diem = supplyAsync(() -> goi("điểm", 400, 700), be);
    var soDu = supplyAsync(() -> goi("số dư", 200, 500), be);
    var hanMuc = supplyAsync(() -> goi("hạn mức", 300, 300), be);
    var khaDung = soDu.thenCombine(hanMuc, (x, y) -> x + y);
    allOf(diem, khaDung).join();       // chờ cả ba lời gọi
    long ms = (System.nanoTime() - t0) / 1_000_000;
    System.out.println("thứ tự xong: " + xong);
    System.out.println("khả dụng: " + khaDung.join());
    System.out.println("điểm: " + diem.join());
    System.out.println("chờ dưới 900 ms: " + (ms < 900));
    be.shutdown();
  }
}
'''

J_FJ = r'''
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
public class ChiaDoi extends RecursiveTask<Long> {
  static final int NGUONG = 10_000;
  static AtomicInteger la = new AtomicInteger();
  final int tu, den;                   // cộng các số từ tu tới den
  ChiaDoi(int tu, int den) { this.tu = tu; this.den = den; }
  protected Long compute() {
    if (den - tu + 1 <= NGUONG) {      // đủ nhỏ: tự cộng, là việc lá
      la.incrementAndGet();
      long s = 0;
      for (int i = tu; i <= den; i++) s += i;
      return s;
    }
    int giua = (tu + den) / 2;
    ChiaDoi trai = new ChiaDoi(tu, giua);
    ChiaDoi phai = new ChiaDoi(giua + 1, den);
    trai.fork();                       // đẩy nửa trái vào hàng việc
    return phai.compute() + trai.join();  // tự làm nửa phải
  }
  public static void main(String[] a) {
    ForkJoinPool be = new ForkJoinPool(4);
    long tong = be.invoke(new ChiaDoi(1, 1_000_000));
    System.out.println("tổng: " + tong);
    System.out.println("số việc lá: " + la.get());
  }
}
'''

J_SHARED = r'''
import java.util.*;
import java.util.concurrent.*;
public class DungChung {
  static void thu(Executor io, Executor cpu) throws Exception {
    List<String> xong = new CopyOnWriteArrayList<>();
    CountDownLatch het = new CountDownLatch(3);
    for (int ms : new int[] {300, 400}) {
      io.execute(() -> {               // việc chờ vào ra
        try { Thread.sleep(ms); } catch (InterruptedException e) { }
        xong.add("chờ " + ms); het.countDown();
      });
    }
    cpu.execute(() -> { xong.add("tính"); het.countDown(); });
    het.await();
    System.out.println(xong);
  }
  public static void main(String[] a) throws Exception {
    ExecutorService chung = Executors.newFixedThreadPool(2);
    ExecutorService rieng = Executors.newFixedThreadPool(2);
    thu(chung, chung);                 // một bể cho cả hai loại việc
    thu(chung, rieng);                 // tách bể cho việc tính
    chung.shutdown(); rieng.shutdown();
  }
}
'''

J_CHECK = r'''
public class KiemLai {
  static int la(int n) {               // đếm việc lá theo số phần tử
    return n <= 10_000 ? 1 : la(n - n / 2) + la(n / 2);
  }
  public static void main(String[] a) {
    long s = 0;
    for (int i = 1; i <= 1_000_000; i++) s += i;   // một luồng
    System.out.println("vòng lặp: " + s);
    System.out.println("số việc lá: " + la(1_000_000));
  }
}
'''

# Đầu ra thật (chạy 2026-11-11, Temurin JDK 21.0.13, Windows 11; mỗi chương trình chạy 3 lần cho cùng kết quả)
OUT_POOL = """
số luồng đã dùng: 4
tổng 10 kết quả: 385
số lượt: 3
"""
OUT_QUEUE = """
số luồng: 4
trong hàng đợi: 2
nhận 6, từ chối 4
"""
OUT_CF = """
thứ tự xong: [số dư, hạn mức, điểm]
khả dụng: 800
điểm: 700
chờ dưới 900 ms: true
"""
OUT_FJ = """
tổng: 500000500000
số việc lá: 128
"""
OUT_SHARED = """
[chờ 300, tính, chờ 400]
[tính, chờ 300, chờ 400]
"""
OUT_CHECK = """
vòng lặp: 500000500000
số việc lá: 128
"""

CALLS = "[('điểm', 400), ('số dư', 200), ('hạn mức', 300)]"

_KEEP_CASE = {"API", "Java", "JVM", "Spring", "A", "B", "C"}


def _lower_first(t):
    w = t.split(" ", 1)[0].strip(",:")
    if w in _KEEP_CASE or (len(w) > 1 and w.isupper()):
        return t
    return t[:1].lower() + t[1:]


def _fmerge(a, b):
    if a in (0, None):
        return b
    if b in (0, None):
        return a
    la, lb = (a if isinstance(a, list) else [a]), (b if isinstance(b, list) else [b])
    return la + [x for x in lb if x not in la]


def _merge_short(st_, minw=8, maxc=170, maxw=38):
    """Câu ≤ 7 từ (TTS/ASR dễ méo) ghép vào câu sau (hoặc câu trước) bằng dấu phẩy; focus ghép theo (như bài L03)."""
    ss = lv.sentences(st_["say"])
    foc = st_.get("focus")
    fl = list(foc) if isinstance(foc, list) and len(foc) == len(ss) else None
    j = 0
    while j < len(ss):
        if len(ss[j].split()) < minw and ss[j].endswith("."):
            nxt = ss[j][:-1] + ", " + _lower_first(ss[j + 1]) if j + 1 < len(ss) else None
            if nxt and len(nxt) <= maxc and len(nxt.split()) <= maxw:
                ss[j:j + 2] = [nxt]
                if fl:
                    fl[j:j + 2] = [_fmerge(fl[j], fl[j + 1])]
                continue
            if j > 0 and ss[j - 1].endswith("."):
                prv = ss[j - 1][:-1] + ", " + _lower_first(ss[j])
                if len(prv) <= maxc and len(prv.split()) <= maxw:
                    ss[j - 1:j + 1] = [prv]
                    if fl:
                        fl[j - 1:j + 1] = [_fmerge(fl[j - 1], fl[j])]
                    j -= 1
                    continue
        j += 1
    st_["say"] = " ".join(ss)
    if fl is not None:
        st_["focus"] = fl


def _spoken(scenes):
    for sc_ in scenes:
        for s_ in sc_["steps"]:
            _merge_short(s_)
    return scenes


def L(a, b):
    """Các dòng a..b của khối mã (phần thứ hai của khung, sau dòng tiêu đề)."""
    return [f"2.{i}" for i in range(a, b + 1)]


def build():
    hook = sc("hook", "hook", "Ba lời gọi 200, 300, 400 ms: chờ 900 hay 400?", [
        st("""<p>Khách mở màn hình tổng quan của ứng dụng ngân hàng. Dịch vụ phải hỏi <b>ba nơi</b> (số minh hoạ):
số dư mất <b>200 ms</b>, hạn mức mất <b>300 ms</b>, điểm tín dụng mất <b>400 ms</b>.</p>
<div class="box key">Hỏi lần lượt: $200 + 300 + 400 = 900$ ms. Hỏi cùng lúc rồi chờ cả ba: khoảng <b>400 ms</b>.
Vậy 500 ms kia biến đi đâu, và khi nghìn khách cùng mở thì chuyện gì xảy ra?</div>""",
           """Chào bạn, khách mở màn hình tổng quan của ứng dụng ngân hàng, và dịch vụ phải hỏi ba nơi, với số minh hoạ như sau.
           Số dư mất hai trăm mili giây, hạn mức mất ba trăm, điểm tín dụng mất bốn trăm mili giây.
           Hỏi lần lượt thì khách chờ chín trăm mili giây, còn hỏi cùng lúc rồi chờ cả ba thì chỉ khoảng bốn trăm.
           Vậy năm trăm mili giây kia biến đi đâu, và khi nghìn khách cùng mở thì chuyện gì xảy ra?""", focus=[1, 1, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["ai làm các việc chạy cùng lúc", "một <b>bể luồng</b> có số luồng cố định; việc dư xếp vào hàng đợi"],
                  ["ghép kết quả của nhiều lời gọi thế nào", "<b>CompletableFuture</b>: lời hứa kết quả, ghép được với nhau; thời gian chờ là lời gọi dài nhất"],
                  ["việc nặng tính toán thì sao", "<b>ForkJoinPool</b>: chia đôi tới khi đủ nhỏ, luồng rảnh lấy việc của luồng bận"]]),
           """Hôm nay ta trả lời ba câu. Ai làm các việc chạy cùng lúc, và vì sao hàng đợi của bể luồng phải có giới hạn.
           Ghép kết quả của nhiều lời gọi song song thế nào, và thời gian chờ tính ra sao.
           Cuối cùng, việc nặng tính toán thì chia nhỏ thế nào để mọi nhân xử lý cùng làm."""),
    ], checks=["alg.bnx_work_total([200, 300, 400]) == 900", "alg.bnx_pool_makespan([200, 300, 400], 3) == 400",
               "alg.bnx_pool_makespan([200, 300, 400], 1) - alg.bnx_pool_makespan([200, 300, 400], 3) == 500"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① luồng (thread)", "một dòng chạy lệnh trong chương trình; nhiều luồng chạy được cùng lúc", "2 luồng, mỗi luồng chờ 100 ms: xong sau khoảng 100 ms, không phải 200"],
                  ["② việc chờ vào ra", "phần lớn thời gian là <b>chờ</b> mạng, đĩa, cơ sở dữ liệu; lúc chờ không dùng nhân xử lý", "gọi dịch vụ số dư, chờ 200 ms"],
                  ["③ việc nặng tính toán", "nhân xử lý phải <b>làm</b> suốt; một nhân chỉ làm một việc tại một lúc", "cộng các số từ 1 tới 1 000 000"],
                  ["④ hàng đợi", "nơi việc nằm chờ khi chưa có luồng nào rảnh; vào trước ra trước", "4 luồng đang bận, việc thứ 5 xếp hàng"]]),
           """Trước hết ta cần hiểu bốn điều. Thứ nhất, luồng là một dòng chạy lệnh trong chương trình, và nhiều luồng chạy được cùng lúc.
           Thứ hai, việc chờ vào ra là việc mà phần lớn thời gian chỉ chờ mạng, đĩa hay cơ sở dữ liệu, lúc chờ không dùng nhân xử lý.
           Thứ ba, việc nặng tính toán bắt nhân xử lý làm suốt, mà một nhân chỉ làm một việc tại một lúc.
           Thứ tư, hàng đợi là nơi việc nằm chờ khi chưa có luồng nào rảnh, vào trước thì ra trước.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st("""<p>Làm thử: 3 việc, mỗi việc chờ 100 ms.</p>
$$\\text{1 luồng: } 3 \\cdot 100 = 300 \\text{ ms}; \\qquad \\text{3 luồng: } \\hl{100} \\text{ ms}; \\qquad \\text{tổng công việc vẫn là } 300$$""",
           """Làm thử ngay với ba việc, mỗi việc chờ một trăm mili giây. Một luồng làm lần lượt nên mất ba trăm mili giây.
           Ba luồng làm cùng lúc nên chỉ mất một trăm, nhưng tổng công việc vẫn là ba trăm, vì không việc nào ngắn đi."""),
    ], checks=["alg.bnx_pool_makespan([100, 100], 2) == 100", "alg.bnx_pool_makespan([100] * 3, 1) == 300",
               "alg.bnx_pool_makespan([100] * 3, 3) == 100", "alg.bnx_work_total([100] * 3) == 300",
               "alg.bnx_pool_schedule([100] * 5, 4)[4][0] == 100"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên trong Java", "nghĩa"],
                 [["ExecutorService", "<b>bể luồng</b>: nhận việc, giao cho các luồng có sẵn; <code>submit</code> gửi một việc"],
                  ["Future", "<b>phiếu hẹn</b>: giữ chỗ cho kết quả chưa có; <code>get</code> chờ tới khi có"],
                  ["CompletableFuture", "<b>lời hứa kết quả</b> ghép được: <code>supplyAsync</code> chạy một việc, <code>thenCombine</code> ghép hai kết quả, <code>allOf</code> chờ mọi lời hứa, <code>join</code> lấy kết quả"],
                  ["ForkJoinPool", "<b>bể chia để trị</b>: <code>fork</code> đẩy việc con vào hàng việc, <code>join</code> chờ kết quả của nó"],
                  ["RecursiveTask", "một việc tự chia mình thành việc con và trả về kết quả"],
                  ["work-stealing", "<b>lấy việc của nhau</b>: luồng hết việc lấy việc đang chờ của luồng còn bận"]]),
           """Bảng này giải mã các tên sẽ hiện trên màn hình. Tên thứ nhất là bể luồng, nó nhận việc rồi giao cho các luồng có sẵn.
           Tên thứ hai là phiếu hẹn, giữ chỗ cho một kết quả chưa có, và ta chờ phiếu để lấy kết quả.
           Tên thứ ba là lời hứa kết quả, khác phiếu hẹn ở chỗ ghép được với nhau: ghép hai kết quả, hoặc chờ mọi lời hứa cùng xong.
           Tên thứ tư là bể chia để trị, có lệnh đẩy việc con vào hàng việc và lệnh chờ kết quả của việc con.
           Tên thứ năm là một việc tự chia mình thành việc con rồi trả về kết quả.
           Cuối cùng, lấy việc của nhau nghĩa là luồng hết việc thì lấy việc đang chờ của luồng còn bận.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
        st(table(["tên dùng thêm trong mã", "nghĩa"],
                 [["ThreadPoolExecutor", "bể luồng tự dựng, chỉnh được số luồng và hàng đợi (đối số giải ở ví dụ thứ hai)"],
                  ["ArrayBlockingQueue", "hàng đợi có sức chứa cố định: đầy thì không nhận thêm"],
                  ["RejectedExecutionException", "lỗi bể ném ra khi từ chối một việc"],
                  ["CountDownLatch", "chốt đếm ngược: luồng gọi lệnh chờ sẽ đứng tới khi bộ đếm về 0; bài dùng để giữ việc lại"],
                  ["nhân xử lý", "một đơn vị của bộ xử lý, mỗi lúc chạy một luồng"]]),
           """Bảng này giải thêm vài tên sẽ gặp trong mã. Bể luồng tự dựng cho chỉnh được số luồng và hàng đợi, đối số sẽ giải ở ví dụ thứ hai.
           Hàng đợi có sức chứa cố định thì đầy là không nhận thêm, và lúc ấy bể ném lỗi từ chối.
           Chốt đếm ngược làm các luồng đứng chờ tới khi bộ đếm về không, bài dùng nó để giữ việc lại.
           Nhân xử lý là một đơn vị của bộ xử lý, mỗi lúc chạy một luồng.
           Trong các chương trình sau, khối bắt lỗi ngắt luồng được để trống cho gọn, còn mã thật không nên nuốt lỗi này.""", clear=True),
    ], checks=["alg.bnx_pool_rounds(10, 4) == 3"])

    def lane(y, name, cells):
        s = txt(150, y + 38, name, 22, "end")
        for x, w, lab, col in cells:
            s += box(x, y, w, 60, lab, col, 20)
        return s

    intu = sc("intuition", "intuition", "Hình dung: bể luồng, lời gọi song song và cây chia đôi", [
        st(svg(1500, 480,
               txt(750, 34, "Bể 4 luồng nhận 10 việc, mỗi việc 100 ms", 26, "middle", "#1f2937", True),
               lane(60, "luồng 1", [(170, 300, "việc 1", C_BLUE), (480, 300, "việc 5", C_GREEN), (790, 300, "việc 9", C_AMBER)]),
               lane(135, "luồng 2", [(170, 300, "việc 2", C_BLUE), (480, 300, "việc 6", C_GREEN), (790, 300, "việc 10", C_AMBER)]),
               lane(210, "luồng 3", [(170, 300, "việc 3", C_BLUE), (480, 300, "việc 7", C_GREEN)]),
               lane(285, "luồng 4", [(170, 300, "việc 4", C_BLUE), (480, 300, "việc 8", C_GREEN)]),
               txt(170, 385, "0", 22), txt(475, 385, "100 ms", 22), txt(785, 385, "200 ms", 22), txt(1095, 385, "300 ms", 22),
               box(1160, 110, 300, 180, ["hàng đợi", "lúc đầu: việc 5 tới 10", "(6 việc nằm chờ)"], C_GRAY, 22, True),
               txt(750, 445, "Lượt 1: việc 1–4. Lượt 2: việc 5–8. Lượt 3: việc 9–10. Xong sau 3 lượt, khoảng 300 ms", 24, "middle", "#1f2937", True)),
           """Hình này là một bể bốn luồng nhận mười việc, mỗi việc một trăm mili giây. Bốn việc đầu được bốn luồng nhận ngay, sáu việc còn lại nằm trong hàng đợi.
           Sau một trăm mili giây, bốn luồng rảnh và lấy tiếp việc năm tới việc tám. Lượt thứ ba chỉ còn việc chín và việc mười.
           Vì có ba lượt, mỗi lượt một trăm mili giây, nên cả mười việc xong sau khoảng ba trăm mili giây."""),
        st(svg(1500, 470,
               txt(750, 34, "Ba lời gọi 200, 300, 400 ms", 26, "middle", "#1f2937", True),
               txt(150, 100, "lần lượt", 22, "end"),
               box(170, 65, 240, 60, "số dư 200", C_BLUE, 20), box(410, 65, 360, 60, "hạn mức 300", C_GREEN, 20),
               box(770, 65, 480, 60, "điểm 400", C_AMBER, 20), txt(1270, 103, "= 900 ms", 24, "start", "#dc2626", True),
               txt(150, 215, "cùng lúc", 22, "end"),
               box(170, 180, 240, 60, "số dư 200", C_BLUE, 20), box(170, 250, 360, 60, "hạn mức 300", C_GREEN, 20),
               box(170, 320, 480, 60, "điểm 400", C_AMBER, 20), txt(670, 358, "= 400 ms (lời gọi dài nhất)", 24, "start", "#16a34a", True),
               txt(750, 440, "Chờ ngắn lại còn 400 ms; tổng công việc vẫn là 200 + 300 + 400 = 900 ms", 24, "middle", "#1f2937", True)),
           """Hình thứ hai đặt ba lời gọi lên trục thời gian. Hỏi lần lượt thì ba đoạn nối đuôi nhau, dài chín trăm mili giây.
           Hỏi cùng lúc thì ba đoạn xếp chồng, nên ta chỉ chờ đoạn dài nhất, là bốn trăm mili giây.
           Chú ý là tổng công việc vẫn bằng chín trăm, vì ba luồng cùng bận, chỉ có thời gian chờ là ngắn lại."""),
        st(svg(1500, 520,
               txt(750, 34, "Chia đôi tới khi đủ nhỏ, luồng rảnh lấy việc của luồng bận", 26, "middle", "#1f2937", True),
               box(550, 55, 400, 60, "1 … 1 000 000", C_BLUE, 22, True),
               box(250, 160, 380, 60, "1 … 500 000", C_BLUE, 22), box(870, 160, 380, 60, "500 001 … 1 000 000", C_BLUE, 22),
               arrow(700, 118, 450, 156), arrow(800, 118, 1050, 156),
               txt(750, 260, "… chia đôi 7 lần …", 24, "middle", "#6b7280"),
               box(60, 290, 300, 60, "lá: 7 812 số", C_GREEN, 22), box(400, 290, 300, 60, "lá: 7 813 số", C_GREEN, 22),
               txt(750, 328, "…", 30), box(800, 290, 300, 60, "lá: 7 812 số", C_GREEN, 22), box(1140, 290, 300, 60, "lá: 7 813 số", C_GREEN, 22),
               box(120, 390, 420, 60, "luồng A: còn việc trong hàng", C_AMBER, 22), box(960, 390, 420, 60, "luồng B: hết việc", C_GRAY, 22),
               arrow(955, 420, 545, 420, "#dc2626", "lấy việc", 22),
               txt(750, 500, "128 việc lá, mỗi lá tự cộng; kết quả cộng dồn ngược lên gốc", 24, "middle", "#1f2937", True)),
           """Hình thứ ba là việc nặng tính toán, cộng các số từ một tới một triệu. Việc gốc chia đôi, mỗi nửa lại chia đôi, bảy lần như thế.
           Tới khi mỗi mảnh còn khoảng bảy nghìn tám trăm số thì nó đủ nhỏ, gọi là việc lá, và tự cộng lấy.
           Mỗi luồng giữ hàng việc của mình. Luồng nào hết việc thì lấy việc đang chờ của luồng còn bận, nên không nhân xử lý nào ngồi không.
           Phần lấy việc này là minh hoạ theo hướng dẫn chính thức của Java, bài không đo được luồng nào thật sự lấy việc của luồng nào."""),
    ], checks=["alg.bnx_pool_schedule([100] * 10, 4)[4] == (100, 200)", "alg.bnx_pool_schedule([100] * 10, 4)[9] == (200, 300)",
               "alg.bnx_pool_admit(10, 4, 10**9) == (10, 0) and 10 - 4 == 6", "alg.bnx_pool_makespan([100] * 10, 4) == 300",
               "alg.bnx_pool_makespan([200, 300, 400], 1) == 900", "alg.bnx_pool_makespan([200, 300, 400], 3) == 400",
               "alg.bnx_fj_depth(1000000, 10000) == 7", "alg.bnx_fj_leaves(1, 1000000, 10000) == 128",
               "1000000 // 128 == 7812 and -(-1000000 // 128) == 7813", "alg.bnx_fj_leaves(1, 500000, 10000) == 64"])

    form = sc("formula", "formula", "Suy ra từng bước: từ một luồng tới ba công cụ", [
        st("""<p><b>Bước 1.</b> Mỗi việc tạo một luồng mới thì tốn, và nghìn việc sẽ sinh nghìn luồng. Vì vậy ta giữ sẵn một <b>bể n luồng</b>
và dùng lại chúng; việc chưa có luồng thì xếp hàng.</p>
<p>Làm thử: 10 việc, mỗi việc 100 ms, bể 4 luồng.</p>
$$10 : 4 = 2{,}5 \\text{, làm tròn lên: } 3 \\text{ lượt} \\;\\Rightarrow\\; 3 \\cdot 100 = \\hl{300} \\text{ ms}$$""",
           """Bước một, mỗi việc tạo một luồng mới thì tốn, và nghìn việc sẽ sinh nghìn luồng. Vì vậy ta giữ sẵn một bể có số luồng cố định và dùng lại chúng.
           Làm thử, mười việc chia cho bốn luồng, làm tròn lên, được ba lượt, nên xong sau ba trăm mili giây.""", clear=True),
        st("""<p><b>Bước 2.</b> Hàng đợi <b>không giới hạn</b> thì việc tới nhanh hơn sức xử lý sẽ dồn lại mãi, vì không gì chặn nó.</p>
<p>Làm thử (số minh hoạ): bể 4 luồng, mỗi việc 100 ms, mỗi giây tới 50 việc.</p>
$$4 \\cdot \\frac{1000}{100} = 40 \\text{ việc/giây}; \\qquad (50 - 40) \\cdot 60 = \\hl{600} \\text{ việc nằm chờ sau 1 phút}$$
<span class='note'>Cách chữa: hàng đợi có giới hạn. Đầy thì từ chối sớm, bên gọi biết ngay để thử lại sau.</span>""",
           """Bước hai, nếu hàng đợi không giới hạn thì khi việc tới nhanh hơn sức xử lý, hàng sẽ dài mãi, vì không gì chặn nó lại.
           Làm thử bằng số minh hoạ, bể bốn luồng xử lý được bốn mươi việc mỗi giây, mà mỗi giây tới năm mươi việc.
           Mỗi giây dư mười việc, nên sau một phút có sáu trăm việc nằm chờ, và mỗi việc chờ đều giữ bộ nhớ.
           Cách chữa là hàng đợi có giới hạn, đầy thì từ chối sớm để bên gọi biết ngay."""),
        st("""<p><b>Bước 3.</b> Việc chờ vào ra không dùng nhân xử lý lúc chờ, nên nhiều việc chờ <b>cùng lúc</b> được. Khi đủ luồng,
thời gian chờ cả nhóm là lời gọi <b>dài nhất</b>, không phải tổng. Ký hiệu max nghĩa là lấy số lớn nhất.</p>
$$\\max(200, 300, 400) = \\hl{400} \\text{ ms} \\quad \\text{thay cho} \\quad 200 + 300 + 400 = 900 \\text{ ms}$$
<span class='note'>Làm thử: chỉ có 2 luồng, gửi theo thứ tự 400, 200, 300 thì luồng hai làm 200 rồi 300: chờ 500 ms.</span>""",
           """Bước ba, việc chờ vào ra không dùng nhân xử lý lúc chờ, nên nhiều việc chờ cùng lúc được. Vì vậy khi đủ luồng, thời gian chờ cả nhóm là lời gọi dài nhất, là bốn trăm mili giây.
           Làm thử với chỉ hai luồng, luồng thứ hai phải làm lời gọi hai trăm rồi tới lời gọi ba trăm, nên ta chờ năm trăm mili giây.""",
           clear=True, introduces=["max_fn"]),
        st("""<p><b>Bước 4.</b> Phiếu hẹn thường chỉ cho ta ngồi chờ. <b>Lời hứa kết quả</b> thì ghép được: “khi số dư <b>và</b> hạn mức cùng có,
hãy cộng lại”, không luồng nào phải đứng chờ để cộng.</p>
$$\\text{khả dụng} = \\text{số dư} + \\text{hạn mức} = 500 + 300 = \\hl{800} \\quad \\text{(số minh hoạ)}$$""",
           """Bước bốn, phiếu hẹn thường chỉ cho ta ngồi chờ. Lời hứa kết quả thì ghép được, vì ta dặn trước: khi số dư và hạn mức cùng có thì hãy cộng lại.
           Làm thử bằng số minh hoạ, số dư năm trăm cộng hạn mức ba trăm, được số tiền khả dụng là tám trăm."""),
        st("""<p><b>Bước 5.</b> Việc nặng tính toán thì thêm luồng quá số nhân không nhanh hơn. Ta <b>chia đôi</b> việc tới khi mỗi mảnh ≤ ngưỡng,
để mọi nhân đều có việc; luồng hết việc lấy việc của luồng bận.</p>
<p>Làm thử: 1 000 000 số, ngưỡng 10 000.</p>
$$\\frac{1\\,000\\,000}{2^6} = 15\\,625 > 10\\,000; \\qquad \\frac{1\\,000\\,000}{2^7} = 7\\,812{,}5 \\le 10\\,000 \\;\\Rightarrow\\; 2^7 = \\hl{128} \\text{ việc lá}$$""",
           """Bước năm, với việc nặng tính toán, thêm luồng quá số nhân xử lý thì không nhanh hơn. Vì vậy ta chia đôi việc tới khi mỗi mảnh không quá ngưỡng, để mọi nhân đều có việc.
           Làm thử, một triệu số với ngưỡng mười nghìn. Chia đôi sáu lần còn mười lăm nghìn sáu trăm hai mươi lăm số, vẫn lớn hơn ngưỡng.
           Chia đôi bảy lần thì còn khoảng bảy nghìn tám trăm số, đủ nhỏ, nên có hai mũ bảy, tức một trăm hai mươi tám việc lá.""",
           clear=True),
        st(table(["loại việc", "công cụ", "vì sao"],
                 [["chờ vào ra (gọi dịch vụ, cơ sở dữ liệu)", "bể luồng <b>riêng</b>, hàng đợi có giới hạn, ghép bằng CompletableFuture", "lúc chờ không tốn nhân xử lý, nên số luồng được nhiều hơn số nhân"],
                  ["nặng tính toán, chia nhỏ được", "ForkJoinPool, số luồng khoảng số nhân", "nhiều luồng hơn số nhân chỉ thêm tranh nhau"]]),
           """Bước sáu, chọn công cụ theo loại việc. Việc chờ vào ra dùng bể luồng riêng có hàng đợi giới hạn, vì lúc chờ không tốn nhân xử lý nên số luồng được nhiều hơn số nhân.
           Việc nặng tính toán dùng bể chia để trị với số luồng khoảng số nhân, vì nhiều luồng hơn chỉ thêm tranh nhau.""",
           focus=[0, "1.2", "1.3"], clear=True),
    ], checks=["alg.bnx_pool_rounds(10, 4) == 3 and alg.bnx_pool_makespan([100] * 10, 4) == 300",
               "alg.bnx_pool_throughput(4, 100) == 40", "alg.bnx_queue_backlog(50, 4, 100, 60) == 600",
               "alg.bnx_pool_makespan([200, 300, 400], 3) == max(200, 300, 400) == 400",
               "alg.bnx_pool_makespan([400, 200, 300], 2) == 500", "alg.bnx_work_total([200, 300, 400]) == 900",
               "500 + 300 == 800 and alg.bnx_pool_schedule([400, 200, 300], 3)[2][1] == 300",
               "1000000 / 2 ** 6 == 15625 and 1000000 / 2 ** 7 == 7812.5", "alg.bnx_fj_depth(1000000, 10000) == 7",
               "alg.bnx_fj_leaves(1, 1000000, 10000) == 2 ** 7 == 128"])

    ex = sc("example", "example", "Ví dụ chạy thật bằng Java, từng phép tính", [
        st(code(J_POOL, "BeLuong.java (trích): gửi 10 việc vào bể 4 luồng", lines=(5, 15)),
           """Ta chạy thật bằng Java. Dòng đầu tạo một bể cố định bốn luồng. Tập hợp ở dòng hai ghi tên các luồng đã làm việc, còn danh sách ở dòng ba giữ mười phiếu hẹn.
           Vòng lặp gửi mười việc vào bể. Mỗi việc chờ một trăm mili giây, ghi tên luồng đang chạy mình, rồi trả về bình phương của số thứ tự.""",
           focus=[0, "2.1", ["2.2", "2.3"], ["2.4", "2.6"], ["2.7", "2.8", "2.9"]], clear=True),
        st(code(J_POOL, "BeLuong.java (tiếp): chờ kết quả rồi in", lines=(16, 21)),
           """Phần tiếp theo chờ từng phiếu hẹn và cộng mười kết quả lại. Sau đó ta đóng bể, vì bể không tự tắt.
           Ba dòng cuối in số luồng đã dùng, tổng mười kết quả, và số lượt tính bằng phép chia làm tròn lên.""",
           focus=[["2.1", "2.2"], "2.3", ["2.4", "2.5", "2.6"]], clear=True),
        st(out(OUT_POOL),
           """Kết quả chạy thật. Mười việc chỉ dùng đúng bốn luồng. Tổng các bình phương từ một tới mười là ba trăm tám mươi lăm, nên không việc nào bị mất. Số lượt là ba.""",
           focus=[0, "2.1", "2.2", "2.3"]),
        st("""$$① \\; 10 : 4 = 2{,}5 \\text{, làm tròn lên: } 3 \\text{ lượt} \\;\\Rightarrow\\; 3 \\cdot 100 = \\hl{300} \\text{ ms}; \\qquad \\text{tổng công việc } 10 \\cdot 100 = 1000 \\text{ ms}$$""",
           """Phép tính thứ nhất. Ba lượt, mỗi lượt một trăm mili giây, nên mười việc xong sau khoảng ba trăm mili giây. Tổng công việc vẫn là một nghìn mili giây, chia cho bốn luồng cùng làm."""),
        st(code(J_QUEUE, "HangDoi.java (trích): bể 4 luồng, hàng đợi chỉ 2 chỗ", lines=(4, 15)),
           """Chương trình thứ hai cho hàng đợi một giới hạn. Chốt ở dòng đầu giữ mọi việc lại, để không việc nào xong trong lúc ta gửi.
           Hai dòng kế tạo bể bốn luồng, với hàng đợi chỉ có hai chỗ. Vòng lặp gửi mười việc liền nhau.
           Việc nào được nhận thì tăng biến đếm nhận. Việc nào bể không còn chỗ thì bể ném lỗi từ chối, và ta tăng biến đếm từ chối.""",
           focus=[0, "2.1", ["2.2", "2.3"], ["2.5", "2.7"], "2.10", "2.11"], clear=True),
        st(table(["đối số của ThreadPoolExecutor", "nghĩa"],
                 [["4 (số luồng lõi)", "bể giữ tới 4 luồng làm việc; chưa đủ 4 thì mỗi việc mới được một luồng mới, dù luồng cũ đang rảnh"],
                  ["4 (số luồng tối đa)", "trần số luồng của bể; bằng số luồng lõi thì bể có số luồng cố định"],
                  ["0, TimeUnit.SECONDS", "thời gian một luồng thừa (vượt số lõi) được rảnh trước khi bị bỏ; ở đây không có luồng thừa"],
                  ["ArrayBlockingQueue(2)", "hàng đợi chỉ chứa 2 việc; hàng đầy thì xét tiếp bước sau"]])
           + "<p style='margin-top:18px'><span class='note'>Quy tắc nhận việc theo hướng dẫn chính thức của Java: dưới số luồng lõi thì thêm luồng; từ số lõi trở lên thì ưu tiên xếp hàng; "
             "hàng đầy thì thêm luồng tới số tối đa; vượt nữa thì từ chối. Hàng đợi không giới hạn không bao giờ đầy, nên số luồng không vượt "
             "số lõi và số tối đa vô nghĩa. Số minh hoạ: lõi 2, tối đa 4, hàng 2 chỗ nhận 6 việc rồi từ chối việc thứ 7 (chạy thật ở bộ kiểm).</span></p>",
           """Trước khi chạy, ta đọc kỹ các đối số của hàm tạo bể, tên gốc hiện trên màn hình. Đối số đầu là số luồng lõi, đối số thứ hai là số luồng tối đa, và đặt bằng nhau thì bể có số luồng cố định.
           Hai đối số kế là thời gian giữ luồng thừa, ở đây không dùng tới. Đối số cuối là hàng đợi, chỉ chứa hai việc.
           Quy tắc nhận việc theo hướng dẫn chính thức: chưa đủ luồng lõi thì thêm luồng, đủ rồi thì ưu tiên xếp hàng, hàng đầy thì thêm luồng tới số tối đa, vượt nữa thì từ chối.
           Vì vậy hàng đợi không giới hạn không bao giờ đầy, số luồng không vượt số lõi, và số luồng tối đa không có tác dụng.""", clear=True),
        st(code(J_QUEUE, "HangDoi.java (tiếp): in rồi thả chốt", lines=(16, 20)),
           """Phần cuối in số luồng của bể, số việc đang nằm trong hàng đợi, và hai biến đếm. Sau đó ta thả chốt cho các việc chạy xong, rồi đóng bể.""",
           focus=[["2.1", "2.2", "2.3"], ["2.4", "2.5"]], clear=True),
        st(out(OUT_QUEUE) + """
$$② \\; 4 \\text{ luồng} + 2 \\text{ chỗ chờ} = \\hl{6} \\text{ việc được nhận}; \\qquad 10 - 6 = \\hl{4} \\text{ việc bị từ chối}$$""",
           """Kết quả chạy thật, bốn luồng, hai việc trong hàng đợi, nhận sáu và từ chối bốn.
           Đó là phép tính thứ hai: bốn luồng của phép một cộng hai chỗ chờ là sáu việc được nhận, nên mười trừ sáu còn bốn việc bị từ chối ngay.""",
           focus=[2, 3]),
        st(code(J_CF, "GhepLoiGoi.java (trích): một lời gọi giả mất ms mili giây", lines=(3, 10)),
           """Chương trình thứ ba ghép ba lời gọi, và dòng đầu nhập sẵn các lệnh của lời hứa kết quả để dòng sau gọi cho ngắn.
           Hàm gọi giả lập một lời gọi ra ngoài: nó chờ đủ số mili giây được giao.
           Xong thì nó ghi tên mình vào một hàng chung để ta biết thứ tự xong, rồi trả về giá trị.""",
           focus=["2.1", ["2.4", "2.5"], ["2.3", "2.6", "2.7"]], clear=True),
        st(code(J_CF, "GhepLoiGoi.java (tiếp): gửi ba lời gọi, ghép, chờ cả ba", lines=(12, 23))
           + "<span class='note'>Dòng cuối của tệp, <code>be.shutdown();</code>, không hiện ở đây cho vừa màn hình; thiếu nó chương trình không tự thoát.</span>",
           """Hàm chính tạo một bể ba luồng riêng cho việc chờ vào ra. Ba dòng tiếp gửi ba lời gọi, cố ý gửi lời gọi chậm nhất trước.
           Dòng kế ghép số dư với hạn mức thành số tiền khả dụng, bằng phép cộng chạy khi cả hai cùng có.
           Sau đó ta chờ mọi lời hứa cùng xong, rồi đo thời gian đã trôi qua.
           Bốn dòng in cho biết thứ tự xong, số khả dụng, điểm, và thời gian chờ có dưới chín trăm mili giây hay không.
           Dòng đóng bể ở cuối tệp không hiện ra đây cho vừa màn hình, nhưng thiếu nó thì chương trình không tự thoát.""",
           focus=["2.1", ["2.3", "2.4", "2.5"], "2.6", ["2.7", "2.8"], ["2.9", "2.10", "2.11", "2.12"], 0], clear=True),
        st(out(OUT_CF) + """
$$③ \\; 200 + 300 + 400 = 900 \\text{ ms}; \\qquad \\max(200, 300, 400) = \\hl{400} \\text{ ms}; \\qquad 900 - 400 = 500 \\text{ ms}$$""",
           """Kết quả chạy thật. Dù gửi lời gọi chậm nhất trước, thứ tự xong vẫn là số dư, hạn mức, rồi điểm, vì cả ba chạy cùng lúc trên ba luồng.
           Khả dụng là tám trăm, điểm là bảy trăm, và thời gian chờ đúng là dưới chín trăm mili giây.
           Phép tính thứ ba: lần lượt mất chín trăm, song song chờ lời gọi dài nhất là bốn trăm, nên khách bớt chờ năm trăm mili giây.""",
           focus=["2.1", ["2.2", "2.3", "2.4"], 3], clear=True),
        st(code(J_FJ, "ChiaDoi.java (trích): việc tự chia đôi", lines=(3, 14)),
           """Chương trình thứ tư cộng các số từ một tới một triệu bằng bể chia để trị. Lớp này là một việc trả về số nguyên dài.
           Ngưỡng là mười nghìn, và một bộ đếm dùng chung đếm số việc lá. Mỗi việc nhớ đoạn số của mình, từ đâu tới đâu.
           Trong hàm tính, nếu đoạn không quá ngưỡng thì đó là việc lá: tăng bộ đếm, rồi tự cộng bằng một vòng lặp.""",
           focus=[0, "2.1", ["2.2", "2.3"], ["2.4", "2.5"], ["2.6", "2.7", "2.8", "2.9", "2.10", "2.11"]], clear=True),
        st(code(J_FJ, "ChiaDoi.java (tiếp): chia đôi, đẩy một nửa, tự làm một nửa", lines=(15, 26)),
           """Nếu đoạn còn lớn thì ta tìm điểm giữa và tạo hai việc con, nửa trái và nửa phải.
           Lệnh đẩy đưa nửa trái vào hàng việc, để luồng nào rảnh thì lấy. Luồng hiện tại tự làm nửa phải, rồi mới chờ nửa trái và cộng hai kết quả.
           Hàm chính tạo bể bốn luồng, giao việc gốc từ một tới một triệu, rồi in tổng và số việc lá.""",
           focus=[["2.1", "2.2", "2.3"], "2.4", "2.5", ["2.7", "2.8", "2.9", "2.10", "2.11"]], clear=True),
        st(out(OUT_FJ) + """
$$④ \\; \\frac{1\\,000\\,000}{2^7} = 7\\,812{,}5 \\le 10\\,000 \\;\\Rightarrow\\; 2^7 = \\hl{128} \\text{ việc lá}$$
$$⑤ \\; 128 \\text{ lá cộng dồn lại}: \\; \\frac{1\\,000\\,000 \\cdot 1\\,000\\,001}{2} = \\hlg{500\\,000\\,500\\,000}$$""",
           """Kết quả chạy thật in tổng là năm trăm tỉ năm trăm nghìn, và đúng một trăm hai mươi tám việc lá.
           Phép tính thứ tư: chia đôi bảy lần thì mỗi mảnh còn khoảng bảy nghìn tám trăm số, không quá ngưỡng, nên có một trăm hai mươi tám việc lá.
           Phép tính thứ năm: một trăm hai mươi tám lá ấy cộng dồn lại phải bằng công thức tổng từ một tới một triệu, và hai con số khớp nhau.""",
           focus=[2, 3, 4], clear=True),
    ], checks=["alg.bnx_gauss(10) == 55 and sum(i * i for i in range(1, 11)) == 385", "alg.bnx_pool_rounds(10, 4) == (10 + 4 - 1) // 4 == 3",
               "alg.bnx_pool_makespan([100] * 10, 4) == 300 and alg.bnx_work_total([100] * 10) == 1000",
               "alg.bnx_pool_admit(10, 4, 2) == (6, 4)",
               f"alg.bnx_finish_order({CALLS}, 3) == ['số dư', 'hạn mức', 'điểm']",
               "alg.bnx_pool_makespan([400, 200, 300], 3) == 400 and alg.bnx_work_total([400, 200, 300]) == 900",
               "alg.bnx_work_total([400, 200, 300]) - alg.bnx_pool_makespan([400, 200, 300], 3) == 500",
               "alg.bnx_fj_leaves(1, 1000000, 10000) == 128", "alg.bnx_fj_sum(1, 1000000, 10000) == 500000500000",
               "alg.bnx_gauss(1000000) == 500000500000", "1000000 / 2 ** alg.bnx_fj_depth(1000000, 10000) == 7812.5"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: một luồng, không dùng bể", [
        st(code(J_CHECK, "KiemLai.java: vòng lặp một luồng và đếm lá theo số phần tử"),
           """Ta kiểm bằng một đường khác hẳn, không dùng bể luồng nào. Hàm đầu đếm việc lá chỉ theo số phần tử: không quá mười nghìn thì là một lá, lớn hơn thì chia hai nửa rồi cộng số lá.
           Hàm chính cộng các số từ một tới một triệu bằng một vòng lặp trên một luồng duy nhất, rồi in tổng và số lá.""",
           focus=[0, ["2.2", "2.3", "2.4"], ["2.6", "2.7", "2.8", "2.9"]], clear=True),
        st(out(OUT_CHECK),
           """Kết quả chạy thật: vòng lặp một luồng cũng ra năm trăm tỉ năm trăm nghìn, và cách đếm theo số phần tử cũng ra một trăm hai mươi tám lá.""", clear=True),
        st(table(["đại lượng", "bể chia để trị", "một luồng", "công thức"],
                 [["tổng 1 tới 1 000 000", "500 000 500 000", "500 000 500 000", "$1\\,000\\,000 \\cdot 1\\,000\\,001 : 2 = 500\\,000\\,500\\,000$"],
                  ["số việc lá", "128 (bộ đếm)", "128 (đếm theo số phần tử)", "$2^7 = 128$"],
                  ["10 việc, 4 luồng", "3 lượt (chương trình in)", "—", "10 : 4 làm tròn lên là 3, tức 300 ms"]]),
           """Bảng này đặt ba đường cạnh nhau. Tổng tính bằng bể chia để trị, bằng một luồng, và bằng công thức đều là một con số.
           Số việc lá cũng khớp ở cả ba đường. Số lượt của bể bốn luồng khớp giữa chương trình và phép chia làm tròn lên.
           Vì các đường độc lập cho cùng kết quả, ta tin rằng chia việc cho nhiều luồng không làm sai đáp số.""",
           focus=["1.2", "1.3", "1.4", 0], clear=True),
        st("""<div class="box warn"><b>Đừng hiểu nhầm.</b> Ví dụ cộng một triệu số chỉ để thấy cơ chế chia đôi, không để đo tốc độ.
Thời gian đo được phụ thuộc máy và độ khởi động của chương trình: trên máy thử, lần chạy đầu bể chia để trị chậm hơn vòng lặp, các lần sau lại nhanh hơn.
<br><span class="note">Hướng dẫn chính thức của lớp ForkJoinTask nêu quy tắc kinh nghiệm: mỗi việc nên làm hơn 100 và dưới 10 000 bước tính cơ bản. Việc lá quá nhẹ thì công chia việc lấn át lợi ích.</span></div>""",
           """Đừng hiểu nhầm ví dụ này: cộng một triệu số chỉ để ta thấy cơ chế chia đôi, không để đo tốc độ.
           Thời gian đo được phụ thuộc máy và độ khởi động của chương trình, trên máy thử, lần chạy đầu bể chia để trị chậm hơn vòng lặp, các lần sau lại nhanh hơn.
           Hướng dẫn chính thức nêu một quy tắc kinh nghiệm, mỗi việc nên làm hơn một trăm và dưới mười nghìn bước tính cơ bản, vì việc lá quá nhẹ thì công chia việc lấn át lợi ích.""", clear=True),
    ], checks=["sum(range(1, 1000001)) == alg.bnx_fj_sum(1, 1000000, 10000) == 500000500000",
               "alg.bnx_gauss(1000000) == 1000000 * 1000001 // 2 == 500000500000",
               "alg.bnx_fj_leaves(1, 1000000, 10000) == 2 ** alg.bnx_fj_depth(1000000, 10000) == 128",
               "alg.bnx_pool_rounds(10, 4) == 3 and alg.bnx_pool_makespan([100] * 10, 4) == 300"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới, lúc mới dựng).</b> Nghĩ rằng song song làm <b class="red">tổng công việc ít đi</b>.
Ba lời gọi vẫn tốn $200 + 300 + 400 = 900$ ms công; chỉ có thời gian chờ ngắn lại còn 400 ms, và chỉ khi <b>đủ luồng</b>.
<br><span class="note">Bể chỉ 1 luồng: chờ lại đủ 900 ms. Bể 2 luồng, gửi theo thứ tự 400, 200, 300: chờ 500 ms.</span></div>""",
           """Lỗi thứ nhất, của người mới lúc mới dựng hệ thống, là nghĩ rằng song song làm tổng công việc ít đi.
           Ba lời gọi vẫn tốn chín trăm mili giây công, chỉ có thời gian chờ ngắn lại còn bốn trăm, và chỉ khi đủ luồng.
           Nếu bể chỉ có một luồng thì ta chờ lại đủ chín trăm, còn bể hai luồng thì chờ năm trăm mili giây.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc tải tăng).</b> Dùng <code>Executors.newFixedThreadPool(4)</code> rồi yên tâm.
Bể này có hàng đợi <b class="red">không giới hạn</b>: tải tăng tới 50 việc/giây trong khi bể làm được 40 thì mỗi phút dồn thêm 600 việc, tới khi hết bộ nhớ.
<br><span class="note">Cách chữa: <code>ThreadPoolExecutor</code> với <code>ArrayBlockingQueue</code> có giới hạn. Hàng đầy thì mặc định ném
<code>RejectedExecutionException</code>; chọn <code>CallerRunsPolicy</code> thì luồng gửi tự chạy việc đó, nên bên gửi chậm lại.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, lộ ra lúc tải tăng. Cách tạo bể cố định quen thuộc nhất của Java dùng một hàng đợi không giới hạn.
           Khi tải tăng tới năm mươi việc mỗi giây mà bể chỉ làm được bốn mươi, mỗi phút dồn thêm sáu trăm việc, cho tới khi hết bộ nhớ.
           Cách chữa là tự tạo bể với hàng đợi có giới hạn. Hàng đầy thì mặc định bể ném lỗi từ chối, như chương trình thứ hai đã cho thấy.
           Ta cũng có thể chọn chính sách để luồng gửi tự chạy việc đó, nhờ vậy bên gửi tự chậm lại.""", clear=True),
        st(code(J_SHARED, "DungChung.java (trích): hai việc chờ vào ra và một việc tính", lines=(4, 15)),
           """Lỗi thứ ba cần một chương trình nhỏ. Hàm thử nhận hai bể, một cho việc chờ vào ra, một cho việc tính.
           Nó gửi hai việc chờ, ba trăm và bốn trăm mili giây, vào bể thứ nhất. Rồi nó gửi một việc tính rất ngắn vào bể thứ hai.
           Mỗi việc xong thì ghi tên vào danh sách, và cuối cùng hàm in danh sách theo thứ tự xong.""",
           focus=[0, "2.1", ["2.4", "2.5", "2.6", "2.7"], "2.10", ["2.2", "2.11", "2.12"]], clear=True),
        st(code(J_SHARED, "DungChung.java (tiếp): một bể dùng chung, rồi tách bể", lines=(17, 22)) + out(OUT_SHARED),
           """Hàm chính tạo hai bể, mỗi bể hai luồng. Lần thử đầu dùng chung một bể cho cả hai loại việc, lần thử sau cho việc tính một bể riêng.
           Kết quả chạy thật: khi dùng chung, việc tính chỉ xong sau việc chờ ba trăm, vì cả hai luồng đều đang ngồi chờ. Khi tách bể, việc tính xong trước tiên.""",
           focus=[["2.2", "2.3"], ["2.4", "2.5"], "4.1", "4.2"], clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Cho việc <b class="red">chờ vào ra</b> chạy trong bể dùng chung với việc tính.
Việc tính cần gần 0 ms mà phải đợi <b>300 ms</b> mới có luồng. Trong Java, các phương thức <code>…Async</code> của CompletableFuture
<b>không truyền bể</b> thì chạy trên <code>ForkJoinPool.commonPool()</code>, bể chung của cả tiến trình: hôm nay ổn, vài tháng sau một dịch vụ ngoài chậm đi là mọi việc tính đói theo.
Điều kiện: nếu bể chung không cho nổi hai luồng song song (ví dụ máy chỉ có một nhân, kể cả khi bị giới hạn còn một nhân) thì mỗi việc chạy trên một luồng mới.
<br><span class="note">Cách chữa: việc chờ vào ra luôn có bể riêng, có giới hạn. <code>orTimeout</code> chỉ báo lỗi quá hạn cho bên gọi; việc đang chạy không bị huỷ và luồng của bể vẫn bận (chạy thật ở bộ kiểm). Muốn nhả luồng, đặt hạn ngay ở nơi gọi ra ngoài.</span></div>""",
           """Đó là lỗi thứ ba, của người đã đi làm, lộ ra khi vận hành lâu dài: cho việc chờ vào ra chạy chung bể với việc tính.
           Việc tính gần như không tốn thời gian mà phải đợi ba trăm mili giây mới có luồng.
           Trong Java, lời hứa kết quả chạy không đồng bộ mà không được truyền bể riêng thì chạy trên một bể chung của cả tiến trình.
           Nếu bể chung không cho nổi hai luồng song song, ví dụ máy chỉ có một nhân, thì mỗi việc chạy trên một luồng mới.
           Hôm nay mọi thứ ổn, nhưng vài tháng sau một dịch vụ ngoài chậm đi là mọi việc tính đói theo.
           Cách chữa là việc chờ vào ra luôn có bể riêng, có giới hạn.
           Lệnh đặt hạn chờ của lời hứa kết quả chỉ báo lỗi quá hạn cho bên gọi, còn việc đang chạy không bị huỷ.
           Luồng của bể vẫn bận, nên muốn nhả luồng phải đặt hạn ngay ở nơi gọi ra ngoài.""", clear=True),
    ], checks=["alg.bnx_work_total([200, 300, 400]) == 900 and alg.bnx_pool_makespan([200, 300, 400], 3) == 400",
               "alg.bnx_pool_makespan([200, 300, 400], 1) == 900 and alg.bnx_pool_makespan([400, 200, 300], 2) == 500",
               "alg.bnx_pool_throughput(4, 100) == 40 and alg.bnx_queue_backlog(50, 4, 100, 60) == 600",
               "alg.bnx_shared_order([300, 400], 2, True) == (['chờ 300', 'tính', 'chờ 400'], 300)",
               "alg.bnx_shared_order([300, 400], 2, False) == (['tính', 'chờ 300', 'chờ 400'], 0)"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Bể 3 luồng nhận 8 việc, mỗi việc 200 ms. Cần mấy lượt, và xong sau khoảng bao lâu?"],
                  ["2", "Bốn lời gọi mất 150, 250, 100 và 500 ms. Gọi lần lượt mất bao lâu? Gọi song song trên 4 luồng rồi chờ cả bốn mất bao lâu?"],
                  ["3", "Quyết định (số minh hoạ): bể 4 luồng, mỗi việc 100 ms, giờ cao điểm tới 50 việc/giây. Chọn hàng đợi không giới hạn, hàng đợi 20 chỗ và từ chối, hay hàng đợi 20 chỗ và luồng gửi tự chạy?"]]),
           """Đến lượt bạn. Câu một, bể ba luồng nhận tám việc, mỗi việc hai trăm mili giây, thì cần mấy lượt và xong sau bao lâu?
           Câu hai, bốn lời gọi mất một trăm năm mươi, hai trăm năm mươi, một trăm và năm trăm mili giây, gọi lần lượt và gọi song song thì chờ bao lâu?
           Câu ba, giờ cao điểm việc tới nhanh hơn sức xử lý của bể, bạn chọn loại hàng đợi nào trong ba loại trên màn hình?
           Hãy tạm dừng lại và làm từng câu ra giấy trước khi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: 8 việc chia cho 3 luồng, làm tròn lên.</p>
$$8 : 3 \\approx 2{,}67 \\text{, làm tròn lên: } 3 \\text{ lượt} \\;\\Rightarrow\\; 3 \\cdot 200 = \\hlg{600} \\text{ ms}$$""",
           """Đáp án câu một. Tám việc chia cho ba luồng, làm tròn lên, được ba lượt. Mỗi lượt hai trăm mili giây, nên xong sau khoảng sáu trăm mili giây."""),
        st("""<p>Câu 2: lần lượt thì cộng, song song đủ luồng thì lấy lời gọi dài nhất.</p>
$$150 + 250 + 100 + 500 = \\hlg{1000} \\text{ ms}; \\qquad \\max(150, 250, 100, 500) = \\hlg{500} \\text{ ms}$$""",
           """Đáp án câu hai. Gọi lần lượt thì cộng cả bốn, được một nghìn mili giây. Gọi song song trên bốn luồng thì chỉ chờ lời gọi dài nhất, là năm trăm mili giây."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["hàng đợi không giới hạn", "không khách nào bị từ chối ngay", "dư 50 − 40 = 10 việc/giây: sau 60 giây 600 việc chờ, việc cuối chờ 600 : 40 = 15 giây, bộ nhớ đầy dần"],
                  ["20 chỗ, đầy thì từ chối", "việc được nhận chờ nhiều nhất 20 : 40 = 0,5 giây; bộ nhớ có trần", "khoảng 10 việc/giây bị từ chối, bên gọi phải thử lại"],
                  ["20 chỗ, luồng gửi tự chạy", "không mất việc, bên gửi tự chậm lại", "luồng nhận yêu cầu bị giữ 100 ms mỗi lần, độ trễ lan ngược ra phía trước"]]),
           """Đáp án câu ba. Hàng đợi không giới hạn không từ chối ai, nhưng mỗi giây dư mười việc, sau một phút có sáu trăm việc chờ và việc cuối phải chờ mười lăm giây.
           Hàng đợi hai mươi chỗ và từ chối thì việc được nhận chờ nhiều nhất nửa giây, đổi lại khoảng mười việc mỗi giây bị từ chối và phải thử lại.
           Để luồng gửi tự chạy thì không mất việc, nhưng luồng nhận yêu cầu bị giữ lại, nên độ trễ lan ngược ra phía trước.
           Nếu khách không chờ nổi mười lăm giây thì giới hạn và từ chối sớm tốt hơn, miễn là bên gọi thử lại được an toàn, tức lệnh ghi có khoá lũy đẳng.""",
           focus=["1.2", "1.3", "1.4", "1.3"]),
    ], checks=["alg.bnx_pool_rounds(8, 3) == 3 and alg.bnx_pool_makespan([200] * 8, 3) == 600",
               "alg.bnx_work_total([150, 250, 100, 500]) == 1000 and alg.bnx_pool_makespan([150, 250, 100, 500], 4) == 500",
               "alg.bnx_pool_makespan([150, 250, 100, 500], 1) == 1000",
               "50 - alg.bnx_pool_throughput(4, 100) == 10 and alg.bnx_queue_backlog(50, 4, 100, 60) == 600",
               "alg.bnx_queue_backlog(50, 4, 100, 60) / alg.bnx_pool_throughput(4, 100) == 15",
               "20 / alg.bnx_pool_throughput(4, 100) == 0.5"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("bể n luồng, dùng lại", "hàng đợi có giới hạn", "chờ vào ra: chờ = lời gọi dài nhất", "nặng tính: chia đôi tới ngưỡng", "tách bể theo loại việc"),
           """Tổng kết chuỗi lập luận. Bể luồng giữ sẵn một số luồng và dùng lại chúng, còn hàng đợi phải có giới hạn để tải tăng không nuốt hết bộ nhớ.
           Việc chờ vào ra chạy song song thì thời gian chờ là lời gọi dài nhất. Việc nặng tính toán thì chia đôi tới ngưỡng, rồi tách bể theo loại việc."""),
        st("""<div class='box key'><b>Tư duy:</b> song song không làm tổng công việc ít đi, chỉ làm thời gian chờ ngắn lại.
Trước khi thêm luồng, hãy hỏi: việc này đang <b>chờ</b> hay đang <b>tính</b>, và khi tải gấp đôi thì việc dư nằm ở đâu.</div>""",
           """Điều cần mang theo. Song song không làm tổng công việc ít đi, chỉ làm thời gian chờ ngắn lại.
           Trước khi thêm luồng, hãy hỏi việc này đang chờ hay đang tính, và khi tải gấp đôi thì việc dư sẽ nằm ở đâu."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Vì sao không dùng thẳng <code>Executors.newFixedThreadPool</code>?", "hàng đợi của nó không giới hạn; cách đúng là tự tạo bể với hàng đợi có giới hạn và chọn rõ chính sách khi đầy"],
                  ["CompletableFuture khác Future ở đâu, chạy trên bể nào?", "ghép được (thenCombine, allOf) mà không giữ luồng chờ; không truyền bể thì chạy trên bể chung (hoặc luồng mới nếu bể chung dưới hai luồng), nên việc chờ vào ra nên truyền bể riêng"],
                  ["Khi nào dùng ForkJoinPool, lấy việc của nhau là gì?", "việc nặng tính toán chia nhỏ được; luồng hết việc lấy việc đang chờ của luồng bận; không để việc chờ vào ra trong đó"]]),
           """Nếu người phỏng vấn hỏi về dòng đa luồng trên hồ sơ, đây là ba câu hay gặp. Vì sao không dùng thẳng cách tạo bể cố định có sẵn: vì hàng đợi của nó không giới hạn.
           Lời hứa kết quả khác phiếu hẹn ở đâu: nó ghép được mà không giữ luồng chờ, và việc chờ vào ra nên được truyền một bể riêng, vì bể chung dùng chung cho cả tiến trình.
           Khi nào dùng bể chia để trị: khi việc nặng tính toán chia nhỏ được, và luồng hết việc sẽ lấy việc của luồng bận.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st(table(["Câu hỏi tiếp theo hay gặp", "ý trả lời (theo hướng dẫn chính thức của Java SE 21)"],
                 [["Bể tự dựng: số luồng tối đa có tác dụng khi nào?", "chỉ khi hàng đợi đầy mới thêm luồng tới số tối đa; hàng đợi không giới hạn thì số luồng không vượt số lõi"],
                  ["Lời hứa kết quả gặp lỗi thì sao?", "<code>join</code> ném <code>CompletionException</code> bọc lỗi gốc; <code>exceptionally</code> và <code>handle</code> nhận lỗi để xử lý"],
                  ["<code>thenCompose</code> khác <code>thenCombine</code> ở đâu?", "<code>thenCombine</code> ghép kết quả của hai lời hứa; <code>thenCompose</code> nối tiếp một lời hứa khác sinh ra từ kết quả bước trước"],
                  ["<code>orTimeout</code> có huỷ việc không?", "không: chỉ hoàn tất lời hứa bằng lỗi quá hạn; việc đang chạy vẫn giữ luồng (chạy thật ở bộ kiểm)"]]),
           """Còn bốn câu hỏi tiếp theo hay gặp, trả lời theo hướng dẫn chính thức. Số luồng tối đa chỉ có tác dụng khi hàng đợi đầy, còn hàng đợi không giới hạn thì số luồng không vượt số lõi.
           Khi lời hứa kết quả gặp lỗi, lệnh lấy kết quả ném lỗi bọc lỗi gốc, còn lệnh bắt lỗi và lệnh xử lý cả hai trường hợp nhận lỗi để xử lý.
           Lệnh ghép hai kết quả khác lệnh nối tiếp ở chỗ lệnh nối tiếp dựng lời hứa mới từ kết quả bước trước.
           Cuối cùng, hạn chờ không huỷ việc đang chạy, nó chỉ báo lỗi quá hạn cho bên gọi.""", clear=True),
        st("""<p>Bài sau: Spring Security và Spring Cloud, một yêu cầu đi qua <b>chuỗi bộ lọc</b> bảo mật thế nào, và <b>cổng</b> chia tải ra sao.</p>""",
           """Ở bài mười bảy, ta lần theo một yêu cầu đi qua chuỗi bộ lọc bảo mật của Spring, rồi xem cổng chia tải thế nào.""",
           forward_ref=True),
    ], checks=["alg.bnx_pool_makespan([200, 300, 400], 3) == 400", "alg.bnx_fj_leaves(1, 1000000, 10000) == 128"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
    return lesson("L16", "be_luong_completablefuture_forkjoin",
                  "Bài 16 — Đa luồng Java nâng cao: bể luồng, CompletableFuture và ForkJoinPool",
                  "curriculum/bnx.yaml L16; audit/bnx/verify_bnx.py L16; audit/bnx/sources_l16.md: Javadoc Java SE 21 (Executors, "
                  "ThreadPoolExecutor, CompletableFuture, ForkJoinPool, ForkJoinTask) và The Java Tutorials, Fork/Join (đọc 2026-11-11); "
                  "mã chạy thật Temurin JDK 21.0.13",
                  ["Gửi việc vào bể luồng cố định và giải thích vì sao phải giới hạn hàng đợi",
                   "Ghép nhiều lời gọi chạy song song bằng CompletableFuture và tính thời gian chờ",
                   "Chia một bài toán lớn thành việc nhỏ bằng ForkJoinPool và giải thích cơ chế lấy việc của nhau",
                   "Chọn đúng công cụ cho việc nặng tính toán và việc chờ vào ra"],
                  scenes)
