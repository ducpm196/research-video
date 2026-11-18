import lib2
from lib2 import *
from libj import jstep, nowrap, JROW

SHORT = {
    "class": "Lớp là khối chứa các hàm và dữ liệu, nằm giữa cặp ngoặc nhọn.",
    "main": "Hàm chính là chỗ máy bắt đầu chạy chương trình.",
    "decl": "Khai biến là viết kiểu rồi tên rồi giá trị: số nguyên, số nguyên lớn, đúng sai, chuỗi chữ.",
    "new": "Chữ tạo mới tạo một đối tượng, hoặc một mảng với các giá trị liệt kê.",
    "for": "Vòng lặp đếm có khai biến đếm, điều kiện còn lặp, bước sau mỗi vòng; hai dấu cộng là tăng một.",
    "foreach": "Dấu hai chấm duyệt từng phần tử của dãy, theo thứ tự.",
    "lambda": "Hàm ngắn không tên: tham số bên trái mũi tên, việc làm bên phải.",
    "print": "Lệnh này in một dòng ra màn hình, và dấu cộng nối chuỗi với số.",
    "div": "Chia hai số nguyên thì bỏ phần lẻ, nên mười ba chia bốn ra ba.",
    "try": "Khối thử chạy trước, có lỗi thì nhảy sang khối bắt lỗi, và khối bắt lỗi trống là bỏ qua lỗi.",
    "sig": "Khai hàm gồm kiểu trả về, tên, rồi các tham số trong ngoặc tròn.",
    "fld": "Chữ cuối cùng là gán một lần rồi không đổi, chữ tĩnh là một bản chung cho cả lớp.",
    "ctor": "Hàm tạo cùng tên lớp, chạy khi tạo mới, và chép tham số vào trường của đối tượng.",
}


def S(k):
    """Hàng của khuôn libj.JROW với lời đọc rút gọn (bài này nhiều bảng, giữ lời đọc ≤ 2300 từ)."""
    return (JROW[k][0], JROW[k][1], SHORT[k])

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
  static CountDownLatch xuat = new CountDownLatch(1); // chốt
  static final int K = 4;      // thời gian ×4 cho ổn định
  static int goi(String ten, int ms, int giaTri) {
    try { xuat.await(); Thread.sleep(ms * K); }
    catch (InterruptedException e) { }
    xong.add(ten);                     // ghi lại thứ tự xong
    return giaTri;
  }
  public static void main(String[] a) {
    ExecutorService be = Executors.newFixedThreadPool(3);
    var diem = supplyAsync(() -> goi("điểm", 400, 700), be);
    var soDu = supplyAsync(() -> goi("số dư", 200, 500), be);
    var hanMuc = supplyAsync(() -> goi("hạn mức", 300, 300), be);
    var khaDung = soDu.thenCombine(hanMuc, (x, y) -> x + y);
    long t0 = System.nanoTime();
    xuat.countDown();                  // cả ba cùng xuất phát
    allOf(diem, khaDung).join();       // chờ cả ba lời gọi
    long ms = (System.nanoTime() - t0) / 1_000_000 / K;
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
        try { Thread.sleep(4*ms); } catch (InterruptedException e) { }
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



# ── AF2 (WP4, 2026-11-14): cảnh quy mô + Tự làm ──
lib2.begin("L16")
P_BE_LUONG = prog("be_luong", J_POOL, lang="java", java_class="BeLuong", out=OUT_POOL, claims=["10 việc chỉ dùng đúng 4 luồng", "tổng các bình phương từ 1 tới 10 là 385", "số lượt là 3"])
P_HANG_DOI = prog("hang_doi", J_QUEUE, lang="java", java_class="HangDoi", out=OUT_QUEUE, claims=["bể 4 luồng + hàng 2 chỗ nhận 6 việc, từ chối 4"])
P_GHEP = prog("ghep_loi_goi", J_CF, lang="java", java_class="GhepLoiGoi", out=OUT_CF, claims=["thứ tự xong số dư, hạn mức, điểm; khả dụng 800; chờ dưới 900 ms"])
P_CHIA = prog("chia_doi", J_FJ, lang="java", java_class="ChiaDoi", out=OUT_FJ, claims=["tổng 500000500000 và 128 việc lá"])
P_DUNG = prog("dung_chung", J_SHARED, lang="java", java_class="DungChung", out=OUT_SHARED, claims=["dùng chung một bể: việc tính xong sau việc chờ 300; tách bể: xong trước"])
P_KIEM = prog("kiem_lai", J_CHECK, lang="java", java_class="KiemLai", out=OUT_CHECK, claims=["vòng lặp một luồng ra 500000500000 và 128 lá"])

J_QUYMO = r'''
import java.util.concurrent.*;
public class HangQuyMo {
  static void thu(int n, int cho) {
    CountDownLatch cua = new CountDownLatch(1);   // giữ việc lại
    BlockingQueue<Runnable> q = cho < 0 ? new LinkedBlockingQueue<>()
        : new ArrayBlockingQueue<>(cho);
    ThreadPoolExecutor be = new ThreadPoolExecutor(4, 4, 0,
        TimeUnit.SECONDS, q);
    int tuChoi = 0;
    for (int i = 0; i < n; i++) {
      try {
        be.execute(() -> {
          try { cua.await(); } catch (InterruptedException e) { }
        });
      } catch (RejectedExecutionException e) { tuChoi++; }
    }
    System.out.println(n + " viec, hang " + (cho < 0 ? "vo han"
        : cho + " cho") + ": trong hang " + be.getQueue().size()
        + ", tu choi " + tuChoi);
    cua.countDown();
    be.shutdown();
  }
  public static void main(String[] a) {
    for (int n : new int[] {10, 1000, 100000}) {
      thu(n, -1);
      thu(n, 2);
    }
  }
}
'''
P_QUYMO = prog("HangQuyMo", J_QUYMO, lang="java", timeout=120,
               claims=["bể 4 luồng, hàng không giới hạn: 6, 996, 99 996 việc nằm chờ ở 10, 1 000, 100 000 việc",
                       "bể 4 luồng, hàng 2 chỗ: nhận 6 việc, từ chối 4, 994, 99 994"])

# Lab (số liệu khác ví dụ): lõi 3, hàng 5 chỗ, gửi 14 việc bị giữ → 3 luồng, 5 chờ, nhận 8, từ chối 6; 14 việc → 5 lượt; 100 000 số, ngưỡng 5 000 → 32 lá
LAB_JAVA = r'''
import java.util.concurrent.*;

public class Lab {
    static int la(int n) {
        return n <= 5000 ? 1 : la(n - n / 2) + la(n / 2);
    }

    public static void main(String[] args) {
        CountDownLatch cua = new CountDownLatch(1);
        ThreadPoolExecutor be = new ThreadPoolExecutor(3, 3, 0,
                TimeUnit.SECONDS, new ArrayBlockingQueue<>(5));
        int nhan = 0, tuChoi = 0;
        for (int i = 1; i <= 14; i++) {
            try {
                be.execute(() -> {
                    try { cua.await(); } catch (InterruptedException e) { }
                });
                nhan++;
            } catch (RejectedExecutionException e) {
                tuChoi++;
            }
        }
        System.out.println("so luong: " + be.getPoolSize());
        System.out.println("trong hang doi: " + be.getQueue().size());
        System.out.println("nhan " + nhan + ", tu choi " + tuChoi);
        System.out.println("so luot cho 14 viec: " + (14 + 3 - 1) / 3);
        System.out.println("so viec la: " + la(100000));
        cua.countDown();
        be.shutdown();
    }
}
'''
LAB_OUT = """so luong: 3
trong hang doi: 5
nhan 8, tu choi 6
so luot cho 14 viec: 5
so viec la: 32"""

LAB_DE = """# Lab BNX L16 — Bể luồng có hàng đợi giới hạn và việc lá của cây chia đôi

Viết `Lab.java` (một tệp, một lớp `public class Lab`, chỉ cần `import java.util.concurrent.*;`). Số liệu là số minh hoạ.

**Phần 1 — hàng đợi giới hạn.** Dựng `ThreadPoolExecutor` có **3 luồng cố định** (số lõi = số tối đa = 3, thời gian giữ luồng thừa `0, TimeUnit.SECONDS`)
và `ArrayBlockingQueue` **5 chỗ**. Dùng một `CountDownLatch(1)` làm chốt: mỗi việc chỉ gọi `cua.await()` nên giữ nguyên luồng cho tới khi bạn thả chốt (khối `catch (InterruptedException e)` để trống).
Gửi **liền 14 việc** bằng `be.execute(...)`; việc nào bể từ chối thì `RejectedExecutionException` được ném ra: bắt lại và đếm `nhan`, `tuChoi`.
Rồi in 3 dòng: `so luong:` (số luồng của bể), `trong hang doi:` (số việc đang nằm trong hàng), `nhan <a>, tu choi <b>`.
Cuối cùng thả chốt (`cua.countDown()`) và `be.shutdown()`.

**Phần 2 — số lượt.** In `so luot cho 14 viec:` với số lượt khi 14 việc chia cho 3 luồng (chia làm tròn lên, tính bằng số nguyên).

**Phần 3 — việc lá.** Viết hàm đệ quy `la(int n)` trả về số việc lá khi chia đôi `n` phần tử tới khi mỗi mảnh không quá **5 000**
(`n <= 5000` thì là 1 lá; ngược lại là `la(n - n / 2) + la(n / 2)`). In `so viec la:` cho `n = 100000`.

In đúng 5 dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh BNX L16 Lab.java`.
"""


def build():
    hook = sc("hook", "hook", "Ba lời gọi 200, 300, 400 ms: chờ 900 hay 400?", [
        st("""<p>Khách mở màn hình tổng quan của ứng dụng ngân hàng. Dịch vụ phải hỏi <b>ba nơi</b> (số minh hoạ):
số dư mất <b>200 ms</b>, hạn mức mất <b>300 ms</b>, điểm tín dụng mất <b>400 ms</b> (ms là mili giây, một phần nghìn giây).</p>
<div class="box key">Hỏi lần lượt: $200 + 300 + 400 = 900$ ms. Hỏi cùng lúc rồi chờ cả ba: khoảng <b>400 ms</b>.
Vậy 500 ms kia biến đi đâu, và khi mười nghìn khách cùng mở thì chuyện gì xảy ra?</div>""",
           """Chào bạn, khách mở màn hình tổng quan, và dịch vụ phải hỏi ba nơi, số liệu minh hoạ. Số dư mất hai trăm mili giây, hạn mức ba trăm, điểm tín dụng bốn trăm. Hỏi lần lượt thì khách chờ chín trăm, hỏi cùng lúc thì chỉ khoảng bốn trăm. Năm trăm kia biến đi đâu, và khi mười nghìn khách cùng mở thì chuyện gì xảy ra?""", focus=[1, 1, 2, 2]),
    ], checks=["alg.bnx_work_total([200, 300, 400]) == 900", "alg.bnx_pool_makespan([200, 300, 400], 3) == 400",
               "alg.bnx_pool_makespan([200, 300, 400], 1) - alg.bnx_pool_makespan([200, 300, 400], 3) == 500"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① luồng (thread)", "một dòng chạy lệnh trong chương trình; nhiều luồng chạy được cùng lúc", "2 luồng, mỗi luồng chờ 100 ms: xong sau khoảng 100 ms, không phải 200"],
                  ["② việc chờ vào ra", "phần lớn thời gian là <b>chờ</b> mạng, đĩa, cơ sở dữ liệu; lúc chờ không dùng nhân xử lý", "gọi dịch vụ số dư, chờ 200 ms"],
                  ["③ việc nặng tính toán", "nhân xử lý (một đơn vị của bộ xử lý, mỗi lúc chạy một luồng) phải <b>làm</b> suốt", "cộng các số từ 1 tới 1 000 000"],
                  ["④ hàng đợi", "nơi việc nằm chờ khi chưa có luồng rảnh; vào trước ra trước", "4 luồng đang bận, việc thứ 5 xếp hàng"]]),
           """Trước hết ta cần hiểu bốn điều. Luồng là một dòng chạy lệnh, và nhiều luồng chạy được cùng lúc. Việc chờ vào ra phần lớn chỉ chờ mạng, đĩa hay cơ sở dữ liệu, không dùng nhân xử lý. Việc nặng tính toán bắt nhân xử lý làm suốt. Hàng đợi là nơi việc chờ khi chưa có luồng rảnh, vào trước thì ra trước."""),
        st("""<p>Làm thử: 3 việc, mỗi việc chờ 100 ms.</p>
$$\\text{1 luồng: } 3 \\cdot 100 = 300 \\text{ ms}; \\qquad \\text{3 luồng: } \\hl{100} \\text{ ms}; \\qquad \\text{tổng công việc vẫn là } 300$$""",
           """Làm thử với ba việc, mỗi việc chờ một trăm mili giây. Một luồng mất ba trăm, ba luồng chỉ mất một trăm, nhưng tổng công việc vẫn là ba trăm."""),
    ], checks=["alg.bnx_pool_makespan([100, 100], 2) == 100", "alg.bnx_pool_makespan([100] * 3, 1) == 300",
               "alg.bnx_pool_makespan([100] * 3, 3) == 100", "alg.bnx_work_total([100] * 3) == 300",
               "alg.bnx_pool_schedule([100] * 5, 4)[4][0] == 100"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên trong Java", "nghĩa"],
                 [["ExecutorService", "<b>bể luồng</b>: nhận việc, giao cho các luồng có sẵn; <code>submit</code> gửi một việc"],
                  ["Future", "<b>phiếu hẹn</b>: giữ chỗ cho kết quả chưa có; <code>get</code> chờ tới khi có"],
                  ["CompletableFuture", "<b>lời hứa kết quả</b> ghép được: <code>supplyAsync</code> chạy một việc, <code>thenCombine</code> ghép hai kết quả, <code>allOf</code> chờ mọi lời hứa, <code>join</code> lấy kết quả"],
                  ["ForkJoinPool, RecursiveTask", "<b>bể chia để trị</b>: một việc tự chia mình thành việc con, <code>fork</code> đẩy việc con vào hàng, <code>join</code> chờ kết quả của nó"]]),
           """Bảng này giải mã các tên sẽ hiện trên màn hình. Bể luồng giao việc cho các luồng có sẵn, phiếu hẹn giữ chỗ cho kết quả chưa có, còn lời hứa kết quả ghép được nhiều kết quả. Bể chia để trị có việc tự chia mình thành việc con.""", clear=True, introduces=['bnx_forkjoin']),
        st(table(["tên trong Java", "nghĩa"],
                 [["lấy việc của nhau (work-stealing)", "luồng hết việc lấy việc đang chờ của luồng còn bận"],
                  ["ThreadPoolExecutor", "bể luồng tự dựng, chỉnh được số luồng và hàng đợi; <code>ArrayBlockingQueue</code> là hàng có sức chứa cố định, đầy thì từ chối"],
                  ["CountDownLatch", "chốt đếm ngược: lệnh chờ đứng tới khi bộ đếm về 0; bài dùng để giữ việc lại"],
                  ["<code>() -&gt; { … }</code>", "viết gọn một việc nhỏ không tên; khối bắt lỗi ngắt luồng để trống cho gọn, mã thật không nên nuốt lỗi này"]]),
           """Luồng hết việc thì lấy việc của luồng còn bận. Bể tự dựng chỉnh được số luồng và hàng đợi, hàng đầy thì từ chối. Chốt đếm ngược giữ việc lại, còn mũi tên viết gọn một việc nhỏ.""", clear=True),
        st(table(["tên trong Java", "nghĩa"],
                 [["AtomicInteger, ConcurrentLinkedQueue, CopyOnWriteArrayList, <code>ConcurrentHashMap.newKeySet()</code>", "số đếm, hàng, danh sách và tập hợp mà nhiều luồng cùng đụng vào cũng không hỏng dữ liệu; HashSet hay ArrayList thường thì có thể hỏng"],
                  ["<code>execute</code> / <code>submit</code>", "gửi một việc không cần kết quả / gửi một việc và nhận lại phiếu hẹn"],
                  ["<code>Runnable</code>", "một việc không trả kết quả, viết dưới dạng <code>() -&gt; { … }</code>"]]),
           """Các lớp ở dòng đầu chứa số đếm, hàng, danh sách hay tập hợp mà nhiều luồng cùng đụng vào vẫn an toàn. Lệnh thực thi gửi việc không cần kết quả, còn lệnh gửi trả lại phiếu hẹn.""", clear=True, introduces=["bnx_atomic_coll"]),
        st(table(["tên trong Java", "nghĩa"],
                 [["<code>import static</code>", "nhập sẵn tên hàm để khỏi viết lại tên lớp mỗi lần gọi"],
                  ["<code>List&lt;Integer&gt;</code>, <code>var</code>", "ngoặc nhọn nói kiểu phần tử trong danh sách (số nguyên); <code>var</code> để máy tự suy ra kiểu"],
                  ["<code>throws Exception</code>", "đặt sau tên hàm: hàm này có thể gặp lỗi mà không tự xử lý, để nơi gọi lo; hàm chính cho qua để mã ngắn"],
                  ["<code>extends RecursiveTask&lt;Long&gt;</code>", "<code>extends</code>: lớp mới kế thừa lớp mẫu; <code>&lt;Long&gt;</code> nói kết quả của việc là số nguyên lớn (kiểu Long)"]]),
           """Nhập tĩnh cho gọi hàm mà khỏi viết tên lớp. Ngoặc nhọn nói kiểu phần tử. Khai báo ném lỗi nghĩa là hàm không tự xử lý lỗi, còn lớp con kế thừa lớp mẫu.""", clear=True),
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
           """Hình này là bể bốn luồng nhận mười việc, mỗi việc một trăm mili giây. Bốn việc đầu chạy ngay, sáu việc còn lại chờ trong hàng. Có ba lượt, nên xong sau khoảng ba trăm."""),
        st(svg(1500, 470,
               txt(750, 34, "Ba lời gọi 200, 300, 400 ms", 26, "middle", "#1f2937", True),
               txt(150, 100, "lần lượt", 22, "end"),
               box(170, 65, 240, 60, "số dư 200", C_BLUE, 20), box(410, 65, 360, 60, "hạn mức 300", C_GREEN, 20),
               box(770, 65, 480, 60, "điểm 400", C_AMBER, 20), txt(1270, 103, "= 900 ms", 24, "start", "#dc2626", True),
               txt(150, 215, "cùng lúc", 22, "end"),
               box(170, 180, 240, 60, "số dư 200", C_BLUE, 20), box(170, 250, 360, 60, "hạn mức 300", C_GREEN, 20),
               box(170, 320, 480, 60, "điểm 400", C_AMBER, 20), txt(670, 358, "= 400 ms (lời gọi dài nhất)", 24, "start", "#16a34a", True),
               txt(750, 440, "Chờ ngắn lại còn 400 ms; tổng công việc vẫn là 200 + 300 + 400 = 900 ms", 24, "middle", "#1f2937", True)),
           """Hình thứ hai đặt ba lời gọi lên trục thời gian. Hỏi lần lượt thì ba đoạn nối đuôi nhau, dài chín trăm mili giây, còn hỏi cùng lúc thì chỉ chờ đoạn dài nhất, là bốn trăm."""),
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
           """Hình thứ ba là cộng các số từ một tới một triệu. Việc gốc chia đôi bảy lần, tới khi mỗi mảnh còn khoảng bảy nghìn tám trăm số thì thành việc lá. Phần luồng rảnh lấy việc là minh hoạ, bài không đo được."""),
    ], checks=["alg.bnx_pool_schedule([100] * 10, 4)[4] == (100, 200)", "alg.bnx_pool_schedule([100] * 10, 4)[9] == (200, 300)",
               "alg.bnx_pool_admit(10, 4, 10**9) == (10, 0) and 10 - 4 == 6", "alg.bnx_pool_makespan([100] * 10, 4) == 300",
               "alg.bnx_pool_makespan([200, 300, 400], 1) == 900", "alg.bnx_pool_makespan([200, 300, 400], 3) == 400",
               "alg.bnx_fj_depth(1000000, 10000) == 7", "alg.bnx_fj_leaves(1, 1000000, 10000) == 128",
               "1000000 // 128 == 7812 and -(-1000000 // 128) == 7813", "alg.bnx_fj_leaves(1, 500000, 10000) == 64"])

    form = sc("formula", "formula", "Suy ra từng bước: từ một luồng tới ba công cụ", [
        st("""<p><b>Bước 1.</b> Mỗi việc tạo một luồng mới thì tốn, nghìn việc sinh nghìn luồng. Vì vậy ta giữ sẵn một <b>bể n luồng</b> và dùng lại chúng; việc chưa có luồng thì xếp hàng.</p>
<p>Làm thử: 10 việc, mỗi việc 100 ms, bể 4 luồng.</p>
$$10 : 4 = 2{,}5 \\text{, làm tròn lên: } 3 \\text{ lượt} \\;\\Rightarrow\\; 3 \\cdot 100 = \\hl{300} \\text{ ms}$$""",
           """Bước một, mỗi việc tạo một luồng mới thì tốn, nên ta giữ sẵn một bể luồng và dùng lại. Mười việc chia cho bốn luồng, làm tròn lên, được ba lượt, nên xong sau ba trăm mili giây.""", clear=True),
        st("""<p><b>Bước 2.</b> Hàng đợi <b>không giới hạn</b> thì việc tới nhanh hơn sức xử lý sẽ dồn lại mãi, vì không gì chặn nó.</p>
<p>Làm thử (số minh hoạ): bể 4 luồng, mỗi việc 100 ms, mỗi giây tới 50 việc.</p>
$$4 \\cdot \\frac{1000}{100} = 40 \\text{ việc/giây}; \\qquad (50 - 40) \\cdot 60 = \\hl{600} \\text{ việc nằm chờ sau 1 phút}$$
<span class='note'>Cách chữa: hàng đợi có giới hạn. Đầy thì từ chối sớm, bên gọi biết ngay để thử lại sau.</span>""",
           """Bước hai, hàng đợi không giới hạn thì việc tới nhanh hơn sức xử lý sẽ dồn lại mãi. Bể bốn luồng xử lý bốn mươi việc mỗi giây mà tới năm mươi, nên sau một phút có sáu trăm việc chờ. Cách chữa là hàng giới hạn.""", clear=True),
        st("""<p><b>Bước 3.</b> Việc chờ vào ra không dùng nhân xử lý lúc chờ, nên nhiều việc chờ <b>cùng lúc</b> được. Khi đủ luồng, thời gian chờ cả nhóm là lời gọi <b>dài nhất</b>, không phải tổng. Ký hiệu max nghĩa là lấy số lớn nhất.</p>
$$\\max(200, 300, 400) = \\hl{400} \\text{ ms} \\quad \\text{thay cho} \\quad 200 + 300 + 400 = 900 \\text{ ms}$$
<span class='note'>Làm thử: chỉ có 2 luồng, gửi theo thứ tự 400, 200, 300 thì luồng hai làm 200 rồi 300: chờ 500 ms.</span>""",
           """Bước ba, việc chờ vào ra không dùng nhân xử lý lúc chờ, nên khi đủ luồng, chờ cả nhóm là lời gọi dài nhất, bốn trăm mili giây. Với hai luồng, luồng hai làm hai trăm rồi ba trăm, nên chờ năm trăm.""",
           clear=True, introduces=["max_fn"]),
        st("""<p><b>Bước 4.</b> Phiếu hẹn thường chỉ cho ta ngồi chờ. <b>Lời hứa kết quả</b> thì ghép được: “khi số dư <b>và</b> hạn mức cùng có, hãy cộng lại”.</p>
$$\\text{khả dụng} = \\text{số dư} + \\text{hạn mức} = 500 + 300 = \\hl{800} \\quad \\text{(số minh hoạ)}$$""",
           """Bước bốn, phiếu hẹn chỉ cho ta ngồi chờ, còn lời hứa kết quả ghép được vì ta dặn trước. Khi số dư và hạn mức cùng có thì cộng lại, năm trăm cộng ba trăm là tám trăm.""", clear=True),
        st("""<p><b>Bước 5.</b> Việc nặng tính toán thì thêm luồng quá số nhân không nhanh hơn. Ta <b>chia đôi</b> việc tới khi mỗi mảnh ≤ <b>ngưỡng</b> (cỡ mảnh nhỏ nhất ta còn chịu chia), để mọi nhân đều có việc.</p>
<p>Làm thử: 1 000 000 số, ngưỡng 10 000.</p>
$$\\frac{1\\,000\\,000}{2^6} = 15\\,625 > 10\\,000; \\qquad \\frac{1\\,000\\,000}{2^7} = 7\\,812{,}5 \\le 10\\,000 \\;\\Rightarrow\\; 2^7 = \\hl{128} \\text{ việc lá}$$""",
           """Bước năm, việc nặng tính toán thì thêm luồng quá số nhân không nhanh hơn, nên ta chia đôi tới khi mỗi mảnh không quá ngưỡng. Một triệu số, ngưỡng mười nghìn: chia bảy lần, được một trăm hai mươi tám việc lá.""",
           clear=True),
        st(table(["loại việc", "công cụ", "vì sao"],
                 [["chờ vào ra (gọi dịch vụ, cơ sở dữ liệu)", "bể luồng <b>riêng</b>, hàng đợi có giới hạn, ghép bằng CompletableFuture", "lúc chờ không tốn nhân xử lý, nên số luồng được nhiều hơn số nhân"],
                  ["nặng tính toán, chia nhỏ được", "ForkJoinPool, số luồng khoảng số nhân", "nhiều luồng hơn số nhân chỉ thêm tranh nhau"]]),
           """Bước sáu, chọn công cụ theo loại việc. Việc chờ vào ra dùng bể riêng với hàng đợi giới hạn. Việc nặng tính toán dùng bể chia để trị, số luồng khoảng số nhân.""",
           focus=[0, "1.2", "1.3"], clear=True),
    ], checks=["alg.bnx_pool_rounds(10, 4) == 3 and alg.bnx_pool_makespan([100] * 10, 4) == 300",
               "alg.bnx_pool_throughput(4, 100) == 40", "alg.bnx_queue_backlog(50, 4, 100, 60) == 600",
               "alg.bnx_pool_makespan([200, 300, 400], 3) == max(200, 300, 400) == 400",
               "alg.bnx_pool_makespan([400, 200, 300], 2) == 500", "alg.bnx_work_total([200, 300, 400]) == 900",
               "500 + 300 == 800 and alg.bnx_pool_schedule([400, 200, 300], 3)[2][1] == 300",
               "1000000 / 2 ** 6 == 15625 and 1000000 / 2 ** 7 == 7812.5", "alg.bnx_fj_depth(1000000, 10000) == 7",
               "alg.bnx_fj_leaves(1, 1000000, 10000) == 2 ** 7 == 128"])

    ex = sc("example", "example", "Ví dụ chạy thật bằng Java, từng phép tính", [
        jstep([(S("class"), "<code>public class BeLuong { … }</code>: lớp tên BeLuong chứa hàm chính", ""),
               (S("main"), "<code>public static void main(String[] a) throws Exception {</code>: máy bắt đầu chạy từ đây", "")]),
        jstep([(S("decl"), "<code>int tong = 0;</code>, <code>long t0 = …;</code>", ""),
               (S("new"), "<code>new ArrayList&lt;&gt;()</code>, <code>new CountDownLatch(1)</code>, <code>new int[] {300, 400}</code>", "")]),
        st(code(J_POOL, "BeLuong.java (1/3): nhập thư viện, tạo bể 4 luồng", lines=(1, 8)),
           """Ta chạy thật bằng Java. Hai dòng đầu nhập thư viện, rồi khai lớp và hàm chính. Dòng năm tạo bể bốn luồng, tập hợp ghi tên luồng đã làm, danh sách giữ các phiếu hẹn.""", clear=True),
        jstep([(S("for"), "<code>for (int i = 1; i &lt;= 10; i++)</code>: i chạy 1, 2, … 10", ""),
               (S("foreach"), "<code>for (Future&lt;Integer&gt; h : hen) tong += h.get();</code>: h là từng phiếu hẹn trong <code>hen</code>; <code>tong += x</code> cộng x vào tong", ""),
               (S("lambda"), "<code>be.submit(() -&gt; { … })</code>: gửi một việc nhỏ không tên; trong đó <code>Thread.sleep(100)</code> cho luồng ngủ 100 mili giây", "")]),
        st(code(J_POOL, "BeLuong.java (2/3): gửi 10 việc", lines=(9, 18)),
           """Vòng lặp gửi mười việc, mỗi việc chờ một trăm mili giây, ghi tên luồng rồi trả về bình phương. Sau đó ta chờ từng phiếu hẹn, cộng kết quả và đóng bể.""", clear=True),
        jstep([(S("print"), '<code>System.out.println("số luồng đã dùng: " + luong.size());</code>', ""),
               (S("div"), "<code>(10 + 4 - 1) / 4</code> ra 3: 13 chia 4 được 3 dư 1, bỏ phần lẻ", "")]),
        st(code(J_POOL, "BeLuong.java (3/3): in kết quả", lines=(19, 23)) + out(OUT_POOL, "Kết quả chạy thật (riêng dòng “số lượt” là phép tính từ công thức, không đo)")
           + """$$① \\; 10 : 4 = 2{,}5 \\text{, làm tròn lên: } 3 \\text{ lượt} \\;\\Rightarrow\\; 3 \\cdot 100 = \\hl{300} \\text{ ms}$$""",
           """Kết quả chạy thật: mười việc chỉ dùng bốn luồng, tổng bình phương là ba trăm tám mươi lăm. Phép tính thứ nhất: ba lượt, mỗi lượt một trăm, nên xong sau ba trăm.""", clear=True),
        st(code(J_QUEUE, "HangDoi.java (1/3): bể 4 luồng, hàng đợi chỉ 2 chỗ", lines=(1, 8)),
           """Chương trình thứ hai giới hạn hàng đợi: chốt giữ mọi việc lại, bể có bốn luồng, và hàng chỉ chứa hai việc.""", clear=True),
        st(table(["tham số của ThreadPoolExecutor", "nghĩa"],
                 [["4, 4", "số luồng lõi và số luồng tối đa; bằng nhau thì bể có số luồng cố định"],
                  ["0, TimeUnit.SECONDS", "thời gian giữ luồng thừa; ở đây không có luồng thừa"],
                  ["ArrayBlockingQueue(2)", "hàng đợi chỉ chứa 2 việc"]])
           + "<p style='margin-top:18px'><span class='note'>Quy tắc nhận việc theo hướng dẫn chính thức của Java: dưới số luồng lõi thì thêm luồng; từ số lõi trở lên thì ưu tiên xếp hàng; "
             "hàng đầy thì thêm luồng tới số tối đa; vượt nữa thì từ chối. Hàng không giới hạn không bao giờ đầy, nên số luồng không vượt số lõi.</span></p>",
           """Hai số đầu là số luồng lõi và tối đa, bằng nhau thì bể cố định. Theo hướng dẫn chính thức, chưa đủ luồng lõi thì thêm luồng, rồi xếp hàng, hàng đầy thì thêm luồng tới mức tối đa, vượt nữa thì từ chối.""", clear=True),
        jstep([(S("try"), "<code>try { be.execute(…); nhan++; } catch (RejectedExecutionException e) { tuChoi++; }</code>: gửi bị từ chối thì ném lỗi, nhảy sang khối bắt lỗi để đếm; khối bắt lỗi trống <code>{ }</code> là bỏ qua lỗi", "")]),
        st(code(J_QUEUE, "HangDoi.java (2/3): gửi liền 10 việc", lines=(9, 17)),
           """Vòng lặp gửi mười việc liền nhau, việc bị từ chối thì bể ném lỗi và ta đếm nó.""", clear=True),
        st(code(J_QUEUE, "HangDoi.java (3/3): in rồi thả chốt", lines=(18, 22)) + out(OUT_QUEUE)
           + """$$② \\; 4 \\text{ luồng} + 2 \\text{ chỗ chờ} = \\hl{6} \\text{ việc được nhận}; \\qquad 10 - 6 = \\hl{4} \\text{ việc bị từ chối}$$""",
           """Kết quả chạy thật: bốn luồng, hai việc trong hàng, nhận sáu và từ chối bốn. Phép tính thứ hai: bốn cộng hai chỗ chờ là sáu việc được nhận, nên còn bốn việc bị từ chối.""", clear=True),
        jstep([(S("sig"), "<code>static int goi(String ten, int ms, int giaTri)</code>: trả về số nguyên, nhận ba tham số", ""),
               (S("fld"), "<code>static final int K = 4;</code>: hằng chung của lớp; <code>static Queue&lt;String&gt; xong = new …</code>: một hàng chung cho mọi hàm", "")]),
        st(code(J_CF, "GhepLoiGoi.java (1/4): nhập thư viện, lời gọi giả", lines=(1, 12)),
           """Chương trình thứ ba ghép ba lời gọi. Hàm gọi giả lập chờ chốt xuất phát, chờ đủ số mili giây, ghi tên vào hàng chung rồi trả về giá trị. Mọi thời gian phóng bốn lần cho ổn định, khi đo ta chia lại.""", clear=True),
        st(code(J_CF, "GhepLoiGoi.java (2/4): gửi ba lời gọi, ghép", lines=(13, 21)),
           """Hàm chính gửi ba lời gọi vào bể ba luồng, cố ý gửi lời gọi chậm nhất trước, ghép số dư với hạn mức, rồi thả chốt.""", clear=True),
        jstep([(("<code>long ms = (System.nanoTime() - t0) / 1_000_000 / K;</code>", "<code>System.nanoTime()</code>: đồng hồ đo bằng nano giây; chia <code>1_000_000</code> ra mili giây (gạch dưới chỉ để dễ đọc số), chia K để bù phần phóng", "Đồng hồ nano giây, chia một triệu ra mili giây, rồi chia hệ số phóng."), "t0 là lúc xuất phát", ""),
               (("<code>(ms &lt; 900)</code>", "phép so sánh cho đúng hoặc sai; ghép vào chuỗi thì in <code>true</code> hoặc <code>false</code>", "Phép so sánh cho đúng hoặc sai, ghép vào chuỗi thì in chữ đúng hoặc sai."), "<code>5 &lt; 9</code> là true", "")]),
        st(code(J_CF, "GhepLoiGoi.java (3/4): chờ, đo, in kết quả", lines=(22, 30)),
           """Ta chờ cả ba xong, đo thời gian và in bốn dòng kết quả.""", clear=True),
        st(out(OUT_CF) + """
$$③ \\; 200 + 300 + 400 = 900 \\text{ ms}; \\qquad \\max(200, 300, 400) = \\hl{400} \\text{ ms}; \\qquad 900 - 400 = 500 \\text{ ms}$$""",
           """Kết quả chạy thật: thứ tự xong vẫn là số dư, hạn mức, rồi điểm. Phép tính thứ ba: lần lượt chín trăm, song song bốn trăm, bớt chờ năm trăm mili giây.""", clear=True),
        jstep([(S("ctor"), "<code>ChiaDoi(int tu, int den) { this.tu = tu; this.den = den; }</code>", ""),
               (("<code>protected Long compute()</code>", "hàm bể chia để trị gọi để làm việc, trả về số nguyên lớn; <code>protected</code>: chỉ lớp này và lớp con gọi được", "Hàm tính là chỗ bể chia để trị gọi để làm việc, trả về số nguyên lớn."), "<code>compute()</code> trả tổng các số từ tu tới den", "")]),
        st(code(J_FJ, "ChiaDoi.java (1/3): việc tự chia đôi", lines=(1, 10)),
           """Chương trình thứ tư cộng các số từ một tới một triệu bằng bể chia để trị, ngưỡng mười nghìn, bộ đếm dùng chung đếm việc lá.""", clear=True),
        st(code(J_FJ, "ChiaDoi.java (2/3): chia đôi, đẩy một nửa, tự làm một nửa", lines=(11, 20)),
           """Đoạn không quá ngưỡng là việc lá, tự cộng. Đoạn lớn thì chia đôi, đẩy nửa trái cho luồng rảnh, tự làm nửa phải rồi chờ nửa trái.""", clear=True),
        st(code(J_FJ, "ChiaDoi.java (3/3): giao việc gốc, in kết quả", lines=(21, 27))
           + out(OUT_FJ),
           """Hàm chính giao việc gốc rồi in tổng và số việc lá cho ta xem.""", clear=True),
        st("""<p>Dùng lại hai số vừa in:</p>
<p>$$④ \\; \\frac{1\\,000\\,000}{2^7} = 7\\,812{,}5 \\le 10\\,000 \\;\\Rightarrow\\; 2^7 = \\hl{128} \\text{ việc lá}$$</p>
<p>$$⑤ \\; \\frac{1\\,000\\,000 \\cdot 1\\,000\\,001}{2} = \\hlg{500\\,000\\,500\\,000}$$</p>""",
           """Phép tính thứ tư: đúng một trăm hai mươi tám việc lá. Phép tính thứ năm: tổng bằng một triệu nhân một triệu lẻ một chia hai.""", clear=True),
    ], checks=["alg.bnx_gauss(10) == 55 and sum(i * i for i in range(1, 11)) == 385", "alg.bnx_pool_rounds(10, 4) == (10 + 4 - 1) // 4 == 3",
               "alg.bnx_pool_makespan([100] * 10, 4) == 300 and alg.bnx_work_total([100] * 10) == 1000",
               "alg.bnx_pool_admit(10, 4, 2) == (6, 4)",
               f"alg.bnx_finish_order({CALLS}, 3) == ['số dư', 'hạn mức', 'điểm']",
               "alg.bnx_pool_makespan([400, 200, 300], 3) == 400 and alg.bnx_work_total([400, 200, 300]) == 900",
               "alg.bnx_work_total([400, 200, 300]) - alg.bnx_pool_makespan([400, 200, 300], 3) == 500",
               "alg.bnx_fj_leaves(1, 1000000, 10000) == 128", "alg.bnx_fj_sum(1, 1000000, 10000) == 500000500000",
               "alg.bnx_gauss(1000000) == 500000500000", "1000000 / 2 ** alg.bnx_fj_depth(1000000, 10000) == 7812.5"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: một luồng, không dùng bể", [
        st(code(J_CHECK, "KiemLai.java: vòng lặp một luồng và đếm lá theo số phần tử")
           + "<p class='note'><code>c ? x : y</code> cho x nếu điều kiện c đúng, ngược lại cho y. Hàm <b>đệ quy</b> là hàm tự gọi lại chính nó với phần việc nhỏ hơn: <code>la</code> gọi <code>la</code> trên hai nửa.</p>",
           """Ta kiểm bằng một đường khác hẳn, không dùng bể luồng nào. Hàm đếm việc lá là hàm đệ quy, tức tự gọi lại chính nó trên hai nửa, và dấu hỏi hai chấm chọn giá trị theo điều kiện. Hàm chính cộng một tới một triệu bằng một vòng lặp.""", clear=True),
        st(out(OUT_CHECK) + table(["đại lượng", "bể chia để trị", "một luồng", "công thức"],
                 [["tổng 1 tới 1 000 000", "500 000 500 000", "500 000 500 000", "$1\\,000\\,000 \\cdot 1\\,000\\,001 : 2 = 500\\,000\\,500\\,000$"],
                  ["số việc lá", "128 (bộ đếm)", "128 (đếm theo số phần tử)", "$2^7 = 128$"]]),
           """Kết quả chạy thật: một luồng cũng ra năm trăm tỉ năm trăm nghìn, và cách đếm theo số phần tử cũng ra một trăm hai mươi tám lá. Ba đường khớp nhau, nên chia việc cho nhiều luồng không làm sai đáp số.""",
           focus=[0, "2.1"], clear=True),
    ], checks=["sum(range(1, 1000001)) == alg.bnx_fj_sum(1, 1000000, 10000) == 500000500000",
               "alg.bnx_gauss(1000000) == 1000000 * 1000001 // 2 == 500000500000",
               "alg.bnx_fj_leaves(1, 1000000, 10000) == 2 ** alg.bnx_fj_depth(1000000, 10000) == 128"])

    quymo = sc("quymo", "example", "Khi tải lớn dần: hàng đợi không giới hạn gãy ở đâu", [
        st(P_QUYMO.show(lines=(1, 9), title="HangQuyMo.java (1/3): bể 4 luồng, hàng không giới hạn hoặc hàng 2 chỗ"),
           """Ta đo thật khi số việc tăng dần. Hàm thử dựng bể bốn luồng, hàng không giới hạn nếu tham số âm, còn không thì hàng có sức chứa cố định.""", clear=True),
        st(P_QUYMO.show(lines=(10, 19), title="HangQuyMo.java (2/3): gửi từng việc, đếm việc bị từ chối, in"),
           """Vòng lặp gửi từng việc và đếm việc bị từ chối, rồi in kết quả.""", clear=True),
        st(P_QUYMO.show(lines=(20, 29), title="HangQuyMo.java (3/3): thử ba cỡ"),
           """Hàm chính thử ba cỡ, mười, một nghìn và một trăm nghìn việc, mỗi cỡ hai lần.""", clear=True),
        st(P_QUYMO.out_html(),
           """Hàng không giới hạn nuốt mọi việc dư, còn hàng hai chỗ luôn giữ đúng hai việc và từ chối phần còn lại.""", clear=True),
        st(table(["số việc N", "hàng không giới hạn: việc nằm chờ (đo thật)", "việc cuối mới bắt đầu sau (100 ms mỗi việc, số minh hoạ)", "hàng 2 chỗ: việc bị từ chối (đo thật)"],
                 [[nowrap("10 (×1)"), "6", "2 lượt = 200 ms", "4"],
                  [nowrap("1 000 (×100)"), "996", "249 lượt ≈ 25 giây", "994"],
                  [nowrap("100 000 (×10 000)"), "99 996", "24 999 lượt ≈ 42 phút", "99 994"]])
           + "<p style='margin-top:14px'><span class='note'>Thời gian chờ tính từ số đo thật, không đo đồng hồ (đồng hồ phụ thuộc máy). Ở cỡ 100 000, bể giữ 99 996 phiếu việc trong bộ nhớ.</span></p>",
           """Ở mười việc, hàng không giới hạn chỉ giữ sáu việc, chẳng ai thấy gì. Gấp trăm lần, việc cuối chờ khoảng hai mươi lăm giây. Gấp mười nghìn lần, hàng giữ gần một trăm nghìn việc, chờ khoảng bốn mươi hai phút.""", clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["hàng không giới hạn", "không khách nào bị từ chối ngay", "chờ dài dần, bộ nhớ phình theo số việc dư", "tải thấp và chắc chắn không vượt sức bể"],
                  ["hàng có giới hạn, đầy thì từ chối", "thời gian chờ và bộ nhớ có trần", "bên gọi phải thử lại, nên lệnh ghi cần khoá lũy đẳng", "tải biến động, cần báo sớm cho bên gọi"]]),
           """Hàng có giới hạn đặt trần cho thời gian chờ và bộ nhớ, đổi lại bên gọi phải thử lại. Vì vậy lệnh ghi cần khoá lũy đẳng, tức mã gửi kèm để gửi lại không bị làm hai lần.""",
           clear=True),
    ], checks=["[alg.bnx_l16_backlog(n, 4) for n in (10, 1000, 100000)] == [6, 996, 99996]",
               "[alg.bnx_l16_rejected(n, 4, 2) for n in (10, 1000, 100000)] == [4, 994, 99994]",
               "[alg.bnx_l16_last_start_ms(n, 4, 100) for n in (10, 1000, 100000)] == [200, 24900, 2499900]",
               "round(2499900 / 60000) == 42 and 24900 // 1000 == 24"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới, lúc mới dựng).</b> Nghĩ rằng song song làm <b class="red">tổng công việc ít đi</b>.
Ba lời gọi vẫn tốn $200 + 300 + 400 = 900$ ms công; chỉ có thời gian chờ ngắn lại còn 400 ms, và chỉ khi <b>đủ luồng</b>.
<br><span class="note">Bể chỉ 1 luồng: chờ lại đủ 900 ms. Bể 2 luồng, gửi theo thứ tự 400, 200, 300: chờ 500 ms.</span></div>""",
           """Lỗi thứ nhất, của người mới, là nghĩ song song làm tổng công việc ít đi. Ba lời gọi vẫn tốn chín trăm mili giây công, chỉ thời gian chờ ngắn lại.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc tải tăng).</b> Dùng <code>Executors.newFixedThreadPool(4)</code> rồi yên tâm.
Bể này có hàng đợi <b class="red">không giới hạn</b>: bảng quy mô vừa đo cho thấy 100 000 việc dồn thành 99 996 việc nằm chờ.
<br><span class="note">Cách chữa: <code>ThreadPoolExecutor</code> với <code>ArrayBlockingQueue</code> có giới hạn. Hàng đầy thì mặc định ném
<code>RejectedExecutionException</code>; chọn <code>CallerRunsPolicy</code> thì luồng gửi tự chạy việc đó, nên bên gửi chậm lại.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, lộ ra lúc tải tăng. Bể cố định quen thuộc của Java dùng hàng đợi không giới hạn, nên một trăm nghìn việc dồn thành gần một trăm nghìn việc chờ. Cách chữa: hàng giới hạn.""", clear=True),
        st(code(J_SHARED, "DungChung.java (1/3): hai việc chờ vào ra", lines=(1, 12)),
           """Lỗi thứ ba cần một chương trình nhỏ. Hàm thử nhận hai bể, một cho việc chờ, một cho việc tính, và gửi hai việc chờ vào bể thứ nhất.""", clear=True),
        st(code(J_SHARED, "DungChung.java (2/3): một việc tính, in thứ tự xong", lines=(13, 18)),
           """Rồi hàm gửi một việc tính ngắn vào bể thứ hai và in thứ tự xong.""", clear=True),
        st(code(J_SHARED, "DungChung.java (3/3): một bể dùng chung, rồi tách bể", lines=(19, 24)) + out(OUT_SHARED),
           """Lần đầu dùng chung một bể hai luồng, lần sau tách bể cho việc tính. Kết quả chạy thật: dùng chung thì việc tính xong sau việc chờ ba trăm vì cả hai luồng ngồi chờ, tách bể thì xong trước.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Cho việc <b class="red">chờ vào ra</b> chạy trong bể dùng chung với việc tính.
Việc tính cần gần 0 ms mà phải đợi <b>300 ms</b> mới có luồng. Các phương thức <code>…Async</code> của CompletableFuture
<b>không truyền bể</b> thì chạy trên <code>ForkJoinPool.commonPool()</code>, bể chung của cả chương trình: hôm nay ổn, vài tháng sau một dịch vụ ngoài chậm đi là mọi việc tính đói theo.
Điều kiện: nếu bể chung không cho nổi hai luồng song song (ví dụ máy chỉ có một nhân) thì mỗi việc chạy trên một luồng mới.
<br><span class="note">Cách chữa: việc chờ vào ra luôn có bể riêng, có giới hạn. <code>orTimeout</code> chỉ báo lỗi quá hạn cho bên gọi; việc đang chạy không bị huỷ và luồng của bể vẫn bận (theo mô tả trong Javadoc của Java SE 21; bài không chạy thử).</span></div>""",
           """Lỗi thứ ba, của người đã đi làm: việc chờ vào ra chạy chung bể với việc tính. Lời hứa kết quả không truyền bể thì chạy trên bể chung, nên dịch vụ ngoài chậm là việc tính đói theo. Cách chữa là một bể riêng.""", clear=True),
    ], checks=["alg.bnx_work_total([200, 300, 400]) == 900 and alg.bnx_pool_makespan([200, 300, 400], 3) == 400",
               "alg.bnx_pool_makespan([200, 300, 400], 1) == 900 and alg.bnx_pool_makespan([400, 200, 300], 2) == 500",
               "alg.bnx_l16_backlog(100000, 4) == 99996",
               "alg.bnx_shared_order([300, 400], 2, True) == (['chờ 300', 'tính', 'chờ 400'], 300)",
               "alg.bnx_shared_order([300, 400], 2, False) == (['tính', 'chờ 300', 'chờ 400'], 0)"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Bể 3 luồng nhận 8 việc, mỗi việc 200 ms. Cần mấy lượt, và xong sau khoảng bao lâu?"],
                  ["2", "Bốn lời gọi mất 150, 250, 100 và 500 ms. Gọi lần lượt mất bao lâu? Gọi song song trên 4 luồng rồi chờ cả bốn mất bao lâu?"],
                  ["3", "Quyết định (số minh hoạ): bể 4 luồng, mỗi việc 100 ms, giờ cao điểm tới 50 việc/giây. Chọn hàng đợi không giới hạn, hàng đợi 20 chỗ và từ chối, hay hàng đợi 20 chỗ và luồng gửi tự chạy?"]]),
           """Đến lượt bạn. Câu một, bể ba luồng nhận tám việc, mỗi việc hai trăm mili giây, cần mấy lượt và xong sau bao lâu? Câu hai, bốn lời gọi mất một trăm năm mươi, hai trăm năm mươi, một trăm và năm trăm, gọi lần lượt và song song thì chờ bao lâu? Câu ba chọn loại hàng đợi. Hãy tạm dừng và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: 8 việc chia cho 3 luồng, làm tròn lên.</p>
$$8 : 3 \\approx 2{,}67 \\text{, làm tròn lên: } 3 \\text{ lượt} \\;\\Rightarrow\\; 3 \\cdot 200 = \\hlg{600} \\text{ ms}$$""",
           """Đáp án câu một. Tám việc chia ba luồng, làm tròn lên, được ba lượt, tức ba lần hai trăm, sáu trăm mili giây."""),
        st("""<p>Câu 2: lần lượt thì cộng, song song đủ luồng thì lấy lời gọi dài nhất.</p>
$$150 + 250 + 100 + 500 = \\hlg{1000} \\text{ ms}; \\qquad \\max(150, 250, 100, 500) = \\hlg{500} \\text{ ms}$$""",
           """Đáp án câu hai. Lần lượt thì cộng cả bốn, được một nghìn mili giây, song song thì chờ lời gọi dài nhất, là năm trăm."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["hàng đợi không giới hạn", "không khách nào bị từ chối ngay", "dư 50 − 40 = 10 việc/giây: sau 60 giây 600 việc chờ, việc cuối chờ 600 : 40 = 15 giây, bộ nhớ đầy dần"],
                  ["20 chỗ, đầy thì từ chối", "việc được nhận chờ nhiều nhất 20 : 40 = 0,5 giây; bộ nhớ có trần", "khoảng 10 việc/giây bị từ chối, bên gọi phải thử lại"],
                  ["20 chỗ, luồng gửi tự chạy", "không mất việc, bên gửi tự chậm lại", "luồng nhận yêu cầu bị giữ 100 ms mỗi lần, độ trễ lan ngược ra phía trước"]]),
           """Đáp án câu ba. Hàng không giới hạn không từ chối ai, nhưng sau một phút việc cuối chờ mười lăm giây. Hàng hai mươi chỗ và từ chối thì chờ nhiều nhất nửa giây, đổi lại khoảng mười việc mỗi giây phải thử lại, miễn là bên gọi thử lại an toàn.""",
           focus=["1.2", "1.3", "1.4", "1.3"]),
    ], checks=["alg.bnx_pool_rounds(8, 3) == 3 and alg.bnx_pool_makespan([200] * 8, 3) == 600",
               "alg.bnx_work_total([150, 250, 100, 500]) == 1000 and alg.bnx_pool_makespan([150, 250, 100, 500], 4) == 500",
               "alg.bnx_pool_makespan([150, 250, 100, 500], 1) == 1000",
               "50 - alg.bnx_pool_throughput(4, 100) == 10 and alg.bnx_queue_backlog(50, 4, 100, 60) == 600",
               "alg.bnx_queue_backlog(50, 4, 100, 60) / alg.bnx_pool_throughput(4, 100) == 15",
               "20 / alg.bnx_pool_throughput(4, 100) == 0.5"])

    lab_pr = practice_scene(sc, "Tự làm: bể luồng giới hạn hàng đợi và việc lá", practice_steps2(
        st, "BNX", "L16",
        """<p><b>Đề</b>: viết <code>Lab.java</code> (<code>import java.util.concurrent.*;</code>):</p>
<ol><li>bể <b>3 luồng cố định</b> + <code>ArrayBlockingQueue</code> <b>5 chỗ</b>, một chốt <code>CountDownLatch(1)</code> giữ việc; gửi liền <b>14 việc</b>, bắt <code>RejectedExecutionException</code>; in số luồng, số việc trong hàng, <code>nhan … tu choi …</code></li>
<li>in số lượt của 14 việc trên 3 luồng</li><li>hàm đệ quy <code>la(n)</code> (hàm tự gọi lại chính nó): số việc lá của <b>100000</b> phần tử, ngưỡng <b>5000</b></li></ol>
<p class="note">Chi tiết từng dòng in nằm trong <code>de.md</code>. Số liệu khác ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm. Viết chương trình Java dựng bể ba luồng với hàng đợi năm chỗ, gửi liền mười bốn việc và đếm việc bị từ chối. Rồi viết hàm đệ quy, tức hàm tự gọi lại chính nó, đếm việc lá. Hãy dừng video và tự viết.""",
        LAB_OUT, "Lab.java",
        """<div class="box key"><b>Nếu kẹt:</b> bể = số luồng lõi 3, tối đa 3, hàng 5 chỗ: nhận được 3 + 5 việc. Số lượt = (14 + 3 − 1) / 3 theo phép chia số nguyên. Hàm lá: <code>n &lt;= 5000 ? 1 : la(n - n / 2) + la(n / 2)</code>.
Lời giải đầy đủ ở <code>labs/BNX/L16/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, nhớ bể nhận được số việc bằng số luồng cộng số chỗ trong hàng, và số lượt là phép chia làm tròn lên. Lời giải chỉ mở sau khi đã tự thử.""", pause=180), "BNX", "L16")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("bể n luồng, dùng lại", "hàng đợi có giới hạn", "chờ vào ra: chờ = lời gọi dài nhất", "nặng tính: chia đôi tới ngưỡng", "tách bể theo loại việc"),
           """Bể luồng dùng lại luồng, hàng đợi phải có giới hạn. Việc chờ chạy song song thì chờ bằng lời gọi dài nhất, việc nặng chia đôi tới ngưỡng, mỗi loại việc có bể riêng."""),
        st("""<div class='box key'><b>Tư duy:</b> song song không làm tổng công việc ít đi, chỉ làm thời gian chờ ngắn lại.
Trước khi thêm luồng, hãy hỏi: việc này đang <b>chờ</b> hay đang <b>tính</b>, và khi tải gấp mười nghìn lần thì việc dư nằm ở đâu.</div>""",
           """Song song không làm tổng công việc ít đi, chỉ làm thời gian chờ ngắn lại. Hãy hỏi việc đang chờ hay đang tính, và khi tải tăng mười nghìn lần thì việc dư nằm ở đâu."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Vì sao không dùng thẳng <code>Executors.newFixedThreadPool</code>?", "hàng đợi của nó không giới hạn; cách đúng là tự tạo bể với hàng đợi có giới hạn và chọn rõ chính sách khi đầy"],
                  ["CompletableFuture khác Future ở đâu, chạy trên bể nào?", "ghép được (thenCombine, allOf) mà không giữ luồng chờ; không truyền bể thì chạy trên bể chung (hoặc luồng mới nếu bể chung dưới hai luồng), nên việc chờ vào ra nên truyền bể riêng"],
                  ["Khi nào dùng ForkJoinPool, lấy việc của nhau là gì?", "việc nặng tính toán chia nhỏ được; luồng hết việc lấy việc đang chờ của luồng bận; không để việc chờ vào ra trong đó"]]),
           """Người phỏng vấn hay hỏi ba câu. Bể cố định có hàng đợi không giới hạn. Lời hứa kết quả ghép được mà không giữ luồng chờ. Bể chia để trị dành cho việc tính.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Bài sau: Spring Security và Spring Cloud, một yêu cầu đi qua <b>chuỗi bộ lọc</b> bảo mật thế nào, và <b>cổng</b> chia tải ra sao.</p>""",
           """Bài mười bảy lần theo một yêu cầu đi qua chuỗi bộ lọc bảo mật của Spring, rồi xem cổng chia tải.""",
           forward_ref=True),
    ], checks=["alg.bnx_pool_makespan([200, 300, 400], 3) == 400", "alg.bnx_fj_leaves(1, 1000000, 10000) == 128"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L16", "be_luong_completablefuture_forkjoin",
                  "Bài 16 — Đa luồng Java nâng cao: bể luồng, CompletableFuture và ForkJoinPool",
                  "curriculum/bnx.yaml L16; audit/bnx/verify_bnx.py L16; audit/bnx/sources_l16.md: Javadoc Java SE 21 (Executors, "
                  "ThreadPoolExecutor, CompletableFuture, ForkJoinPool, ForkJoinTask) và The Java Tutorials, Fork/Join (đọc 2026-11-11); "
                  "mã chạy thật Temurin JDK 21.0.13",
                  ["Gửi việc vào bể luồng cố định và giải thích vì sao phải giới hạn hàng đợi",
                   "Ghép nhiều lời gọi chạy song song bằng CompletableFuture và tính thời gian chờ",
                   "Chia một bài toán lớn thành việc nhỏ bằng ForkJoinPool và nêu cơ chế lấy việc của nhau",
                   "Chọn đúng công cụ cho việc nặng tính toán và việc chờ vào ra"],
                  scenes,
                  covers=[(1, "practice"), (2, "example"), (3, "example"), (4, "formula")])


# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
write_lab("BNX", "L16", LAB_DE, "java", LAB_JAVA, LAB_OUT)
