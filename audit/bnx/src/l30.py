import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from labkit import write_lab, practice_steps, practice_scene
from libj import jstep, nowrap

lib2.begin("L30")

# ── Mã chạy THẬT: JDK 21 thuần; Resilience4j 2.3.0 (audit/bnx/deps/l30, sha256 ở README.md) chỉ để SO với bản tự cài ──
# Đồng hồ trong bản tự cài là đồng hồ GIẢ (số mili giây truyền vào), nên đầu ra tất định; riêng R4j chờ thật 1,1 giây.
def codo(pts, color, label, lx, ly):
    """Mũi tên gấp khúc (đường gãy) có đầu nhọn ở điểm cuối, để mũi tên chạm đúng hộp đích."""
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3.5" marker-end="url(#ah)"/>'
            + txt(lx, ly, label, 22, "middle", color))


J_THULAI = prog("ThuLai", r'''
public class ThuLai {
  static String chay(int hong, int toiDa, int goc) {
    int cho = 0;
    for (int lan = 1; lan <= toiDa; lan++) {
      if (lan > hong)
        return "thanh cong o lan " + lan + ", cho tong " + cho + " ms";
      if (lan == toiDa)
        return "that bai sau " + toiDa + " lan, cho tong " + cho + " ms";
      cho += goc << (lan - 1);          // 100, 200, 400, ...
    }
    return "";
  }
  public static void main(String[] a) {
    System.out.println("hong 2 lan, toi da 4: " + chay(2, 4, 100));
    System.out.println("hong 5 lan, toi da 4: " + chay(5, 4, 100));
    System.out.println("hong 0 lan, toi da 4: " + chay(0, 4, 100));
  }
}
''', lang="java", kind="other", reason="ThuLai.java: thử lại có lùi theo luỹ thừa 2, cộng thời gian chờ (đồng hồ giả, không ngủ thật).", read_check="Biên dịch và chạy trong nguồn L30_ChayTuCai.")

J_CAUDAO = prog("CauDao", r'''
public class CauDao {
  enum T { DONG, MO, NUA_MO }
  T t = T.DONG;
  int hong = 0;
  long moLuc;
  static final int NGUONG = 3;
  static final long CHO = 1000;
  boolean choPhep(long ms) {
    if (t == T.MO) {
      if (ms - moLuc < CHO) return false;
      t = T.NUA_MO;                      // hết thời gian chờ: cho thử một cuộc
    }
    return true;
  }
  void ghi(boolean tot, long ms) {
    if (t == T.NUA_MO) {
      if (tot) { t = T.DONG; hong = 0; } else { t = T.MO; moLuc = ms; }
    } else if (tot) {
      hong = 0;
    } else if (++hong >= NGUONG) {
      t = T.MO;
      moLuc = ms;
    }
  }
  public static void main(String[] a) {
    CauDao c = new CauDao();
    int that = 0, tuChoi = 0;
    for (long ms = 0; ms <= 4000; ms += 500) {
      boolean tot = ms > 2500;           // dịch vụ hỏng tới 2500 ms rồi hồi phục
      if (!c.choPhep(ms)) {
        tuChoi++;
        System.out.println("t=" + ms + " tu choi (cau dao MO)");
        continue;
      }
      c.ghi(tot, ms);
      System.out.println("t=" + ms + (tot ? " thanh cong" : " that bai") + " -> " + c.t);
    }
    System.out.println("tong: " + (9 - tuChoi) + " cuoc goi that, " + tuChoi + " cuoc bi chan");
  }
}
''', lang="java", kind="other", reason="CauDao.java: cầu dao ba trạng thái với đồng hồ giả (mili giây truyền vào).", read_check="Biên dịch và chạy trong nguồn L30_ChayTuCai.")

J_VACH = prog("VachNgan", r'''
import java.util.concurrent.*;
public class VachNgan {
  public static void main(String[] a) throws Exception {
    Semaphore ngan = new Semaphore(2);
    CountDownLatch dangGiu = new CountDownLatch(2), nha = new CountDownLatch(1);
    for (int i = 0; i < 2; i++)
      new Thread(() -> {
        ngan.tryAcquire();
        dangGiu.countDown();
        try { nha.await(); } catch (InterruptedException e) { }
        ngan.release();
      }).start();
    dangGiu.await();
    int nhan = 0, tuChoi = 0;
    for (int i = 0; i < 3; i++)
      if (ngan.tryAcquire()) nhan++; else tuChoi++;
    System.out.println("2 cuoc dang cham: them 3 cuoc -> nhan " + nhan + ", tu choi " + tuChoi);
    nha.countDown();
    Thread.sleep(200);
    System.out.println("sau khi 2 cuoc cham xong: con " + ngan.availablePermits() + " cho trong");
  }
}
''', lang="java", kind="other", reason="VachNgan.java: vách ngăn bằng Semaphore: hạn chế số cuộc gọi đồng thời tới một dịch vụ phụ thuộc.", read_check="Biên dịch và chạy trong nguồn L30_ChayTuCai.")

J_GIOIHAN = prog("GioiHan", r'''
public class GioiHan {
  double thung = 5;                       // xô token, dung tích 5
  long truoc = 0;
  boolean cho(long ms) {
    thung = Math.min(5, thung + (ms - truoc) / 1000.0 * 2);   // nạp 2 token mỗi giây
    truoc = ms;
    if (thung >= 1) { thung -= 1; return true; }
    return false;
  }
  public static void main(String[] a) {
    GioiHan g = new GioiHan();
    int ok = 0;
    for (int i = 0; i < 12; i++) if (g.cho(0)) ok++;
    System.out.println("12 yeu cau cung luc luc 0 ms: nhan " + ok + ", tu choi " + (12 - ok));
    ok = 0;
    for (int i = 0; i < 12; i++) if (g.cho(1000)) ok++;
    System.out.println("12 yeu cau cung luc sau 1 giay: nhan " + ok);
  }
}
''', lang="java", kind="other", reason="GioiHan.java: giới hạn tốc độ kiểu xô token với đồng hồ giả.", read_check="Biên dịch và chạy trong nguồn L30_ChayTuCai.")

J_CANBANG = prog("CanBang", r'''
public class CanBang {
  static int[] chay(boolean it) {
    int[] dur = {100, 10, 10, 10, 10, 10, 10, 10};   // mili giây mỗi yêu cầu
    int[] max = {0, 0};
    long[][] ketThuc = new long[2][8];
    int[] soCuoc = {0, 0};
    for (int i = 0; i < dur.length; i++) {
      long ms = i * 10L;                 // yêu cầu i đến lúc i × 10 ms
      int[] dang = new int[2];
      for (int s = 0; s < 2; s++)
        for (int k = 0; k < soCuoc[s]; k++) if (ketThuc[s][k] > ms) dang[s]++;
      int s = it ? (dang[1] < dang[0] ? 1 : 0) : i % 2;
      ketThuc[s][soCuoc[s]++] = ms + dur[i];
      dang[s]++;
      max[s] = Math.max(max[s], dang[s]);
    }
    return max;
  }
  public static void main(String[] a) {
    int[] v = chay(false), l = chay(true);
    System.out.println("xoay vong: toi da dong thoi may 1 = " + v[0] + ", may 2 = " + v[1]);
    System.out.println("it ket noi nhat: toi da dong thoi may 1 = " + l[0] + ", may 2 = " + l[1]);
  }
}
''', lang="java", kind="other", reason="CanBang.java: so sánh chia xoay vòng với chia cho máy ít kết nối nhất (mô phỏng, đồng hồ giả).", read_check="Biên dịch và chạy trong nguồn L30_ChayTuCai.")

J_QUYMO = prog("QuyMo", r'''
public class QuyMo {
  public static void main(String[] a) {
    for (int n : new int[] {100, 10000}) {
      CauDao c = new CauDao();
      int that = 0;
      for (int i = 0; i < n; i++) {
        long ms = i * 10000L / n;          // n yêu cầu rải đều trong 10 giây sự cố
        if (!c.choPhep(ms)) continue;
        c.ghi(false, ms);
        that++;
      }
      System.out.println(n + " yeu cau, 10 giay su co: thu lai 3 lan khong cau dao "
          + 4 * n + " cuoc goi, co cau dao " + that);
    }
  }
}
''', lang="java", kind="other", reason="QuyMo.java: số cuộc gọi tới dịch vụ đang hỏng, có và không có cầu dao (dùng lớp CauDao).", read_check="Biên dịch cùng CauDao.java và chạy trong nguồn L30_ChayTuCai.")

J_R4J = prog("R4j", r'''
import io.github.resilience4j.circuitbreaker.*;
import java.time.Duration;
public class R4j {
  public static void main(String[] a) throws Exception {
    var cfg = CircuitBreakerConfig.custom()
        .slidingWindowType(CircuitBreakerConfig.SlidingWindowType.COUNT_BASED)
        .slidingWindowSize(4).minimumNumberOfCalls(4)
        .failureRateThreshold(50)
        .waitDurationInOpenState(Duration.ofMillis(1000))
        .permittedNumberOfCallsInHalfOpenState(1).build();
    CircuitBreaker cb = CircuitBreaker.of("dich-vu", cfg);
    cb.getEventPublisher().onStateTransition(e ->
        System.out.println("chuyen: " + e.getStateTransition()));
    int tuChoi = 0;
    for (int i = 1; i <= 6; i++) {
      try {
        cb.executeRunnable(() -> { throw new IllegalStateException("hong"); });
      } catch (CallNotPermittedException e) {
        tuChoi++;
      } catch (IllegalStateException e) { }
    }
    System.out.println("sau 6 cuoc hong: trang thai " + cb.getState() + ", bi chan " + tuChoi);
    Thread.sleep(1100);
    cb.executeRunnable(() -> { });
    System.out.println("sau khi cho 1,1 giay va 1 cuoc tot: " + cb.getState());
  }
}
''', lang="java", kind="other", reason="R4j.java: cùng mô hình cầu dao bằng Resilience4j 2.3.0 thật (cửa sổ đếm 4, ngưỡng 50%, chờ 1 giây).", read_check="Biên dịch cùng jar Resilience4j và chạy trong nguồn L30_ChayR4j.")

SH_TUCAI = prog("ChayTuCai", r'''
javac -encoding UTF-8 ThuLai.java CauDao.java VachNgan.java GioiHan.java CanBang.java QuyMo.java
for c in ThuLai CauDao VachNgan GioiHan CanBang QuyMo; do
  java -Dstdout.encoding=UTF-8 $c
done
''', lang="bash", files={"ThuLai.java": "ThuLai", "CauDao.java": "CauDao", "VachNgan.java": "VachNgan", "GioiHan.java": "GioiHan", "CanBang.java": "CanBang", "QuyMo.java": "QuyMo"}, timeout=200,
    claims=["thử lại: hỏng 2 lần thì thành công ở lần 3 chờ 300 ms; hỏng 5 lần thì thất bại sau 4 lần chờ 700 ms",
            "cầu dao ba trạng thái: 7 cuộc gọi thật, 2 cuộc bị chặn", "vách ngăn: 2 chỗ, thêm 3 cuộc thì nhận 0 từ chối 3", "xô token: 5 nhận 7 từ chối, sau 1 giây nhận 2",
            "chia xoay vòng: máy 1 chồng tới 4 cuộc đồng thời; ít kết nối nhất: 2"])

SH_R4J = prog("ChayR4j", r'''
D=/d/research-video/audit/bnx/deps/l30
ls $D/resilience4j-circuitbreaker-2.3.0.jar >/dev/null 2>&1 || { echo "NOT_VERIFIED: thiếu jar" >&2; exit 97; }
mkdir -p lib out && cp $D/*.jar lib/
javac -encoding UTF-8 -cp "lib/*" -d out R4j.java
java -Dstdout.encoding=UTF-8 -cp "out;lib/*" R4j 2>/dev/null
''', lang="bash", files={"R4j.java": "R4j"}, timeout=200, claims=["Resilience4j thật: CLOSED → OPEN sau 4 cuộc hỏng, các cuộc sau bị chặn, sau 1 giây OPEN → HALF_OPEN → CLOSED"])

# ── Lab (cham.sh, Python): cầu dao nhỏ ──
LAB_PY = r'''
class CauDao:
    def __init__(self, nguong, cho):
        self.nguong, self.cho = nguong, cho
        self.t, self.hong, self.mo_luc = "DONG", 0, 0

    def cho_phep(self, ms):
        if self.t == "MO":
            if ms - self.mo_luc < self.cho:
                return False
            self.t = "NUA_MO"
        return True

    def ghi(self, tot, ms):
        if self.t == "NUA_MO":
            if tot:
                self.t, self.hong = "DONG", 0
            else:
                self.t, self.mo_luc = "MO", ms
        elif tot:
            self.hong = 0
        else:
            self.hong += 1
            if self.hong >= self.nguong:
                self.t, self.mo_luc = "MO", ms


c = CauDao(2, 600)
that = chan = 0
for ms in range(0, 3001, 300):
    tot = ms >= 1500
    if not c.cho_phep(ms):
        chan += 1
        print(f"t={ms} chan")
        continue
    c.ghi(tot, ms)
    that += 1
    print(f"t={ms} {'tot' if tot else 'hong'} -> {c.t}")
print(f"goi that {that}, bi chan {chan}")
'''
LAB_OUT = """t=0 hong -> DONG
t=300 hong -> MO
t=600 chan
t=900 hong -> MO
t=1200 chan
t=1500 tot -> DONG
t=1800 tot -> DONG
t=2100 tot -> DONG
t=2400 tot -> DONG
t=2700 tot -> DONG
t=3000 tot -> DONG
goi that 9, bi chan 2"""
LAB_DE = """# Lab BNX L30 — Cầu dao nhỏ với đồng hồ giả

Viết `mau.py` cài **cầu dao ba trạng thái** `DONG` (đóng, cho gọi) → `MO` (mở, chặn) → `NUA_MO` (thử một cuộc) với **đồng hồ giả** (thời điểm `ms` truyền vào, không ngủ thật):

- ngưỡng: **2** cuộc hỏng liên tiếp thì mở; thời gian chờ ở trạng thái mở: **600 ms** (từ lúc mở tới lúc được thử lại);
- khi `MO` mà chưa đủ 600 ms: chặn (không gọi dịch vụ). Đủ 600 ms thì chuyển `NUA_MO` và cho gọi một cuộc: tốt → `DONG`, hỏng → `MO` (tính lại từ lúc đó);
- gọi mỗi 300 ms từ `ms = 0` tới `3000` (11 lần); dịch vụ hỏng khi `ms < 1500`, tốt từ `1500` trở đi.

In mỗi lần gọi `t=<ms> hong -> <trạng thái>` hoặc `t=<ms> tot -> <trạng thái>`, hoặc `t=<ms> chan` khi bị chặn; dòng cuối `goi that <a>, bi chan <b>`.
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L30 mau.py`.
"""


def build():
    write_lab("BNX", "L30", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Dịch vụ phụ thuộc chết: bốn trăm cuộc gọi hay mười hai?", [
        st("""<p>Dịch vụ tra cứu hạn mức của ngân hàng gọi một dịch vụ chấm điểm. Dịch vụ chấm điểm gặp sự cố 10 giây. Mỗi yêu cầu của khách <b>thử lại 3 lần</b> khi lỗi.</p>
<div class="box key">100 yêu cầu thành <b>400</b> cuộc gọi tới dịch vụ đang hỏng; 10 000 yêu cầu thành <b>40 000</b>. Có <b>cầu dao</b>: cả hai trường hợp chỉ còn <b>12</b> cuộc gọi thật.
Vì sao thử lại lại làm sự cố nặng thêm, và cầu dao khác gì?</div>""",
           """Chào bạn, dịch vụ tra cứu hạn mức gọi dịch vụ chấm điểm đang gặp sự cố mười giây. Mỗi yêu cầu thử lại ba lần khi lỗi. Một trăm yêu cầu thành bốn trăm cuộc gọi tới dịch vụ đang hỏng, mười nghìn thành bốn mươi nghìn. Có cầu dao thì cả hai chỉ còn mười hai cuộc gọi thật. Vì sao thử lại làm sự cố nặng thêm, và cầu dao khác gì?""", focus=[1, 2, 2, 2, 2]),
    ], checks=["alg.bnx_l30_retry_load(100, 3) == 400 and alg.bnx_l30_retry_load(10000, 3) == 40000", "alg.bnx_l30_breaker([i * 100 for i in range(100)], 10**9)[0] == 12"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① hết giờ (timeout)", "chờ tối đa một khoảng thời gian rồi bỏ cuộc gọi", "gọi dịch vụ chấm điểm tối đa 2 giây"],
                  ["② thử lại", "gọi lại khi lỗi; lỗi tạm thời thì lần sau có thể thành công. <b>r lần thử lại = 1 + r lần gọi</b> (lần đầu không tính)", "tối đa 4 lần gọi = lần đầu + 3 thử lại"],
                  ["③ lỗi tạm thời và lỗi lâu", "tạm thời: mạng chập chờn; lâu: dịch vụ chết cả phút", "thử lại hợp với loại đầu, có hại với loại sau"],
                  ["④ đồng thời và luồng", "đồng thời: nhiều cuộc gọi chạy cùng lúc. <b>Luồng</b> (thread): một dây việc chạy riêng; mỗi cuộc gọi đang chờ giữ một luồng", "500 cuộc chờ cùng lúc = 500 luồng bị giữ"],
                  ["⑤ đồng hồ giả", "thay giờ thật bằng số mili giây ta truyền vào, để chạy lại ra đúng kết quả cũ", "t = 500 ms, 1 000 ms…"]]),
           """Trước hết ta cần hiểu năm điều. Hết giờ là chờ tối đa một khoảng rồi bỏ cuộc gọi. Thử lại là gọi lại khi lỗi: r lần thử lại là một cộng r lần gọi. Lỗi tạm thời khác lỗi lâu, và thử lại có hại với loại sau. Đồng thời là nhiều cuộc chạy cùng lúc, mỗi cuộc giữ một luồng. Đồng hồ giả thay giờ thật bằng số mili giây truyền vào.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["alg.bnx_l30_retry(2, 4, 100) == ('ok', 3, 300)"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>DONG</code>, <code>MO</code>, <code>NUA_MO</code>", "ba trạng thái cầu dao: đóng (cho gọi), mở (chặn), nửa mở (thử một cuộc)"],
                  ["<code>goc &lt;&lt; (lan - 1)</code>", "dịch sang trái các chữ số 0 và 1 (bit) của số trong máy: mỗi vị trí dịch là nhân đôi. Lần 1 dịch 0 vị trí → 100; lần 2 dịch 1 → 200; lần 3 dịch 2 → 400"],
                  ["<code>Semaphore</code>", "bộ đếm chỗ: có bao nhiêu chỗ thì bấy nhiêu cuộc gọi cùng lúc, hết chỗ thì từ chối"],
                  ["xô token", "xô chứa token, nạp đều mỗi giây; mỗi yêu cầu lấy một token, hết token thì từ chối"],
                  ["ít kết nối nhất", "gửi việc mới cho máy đang xử lý ít việc nhất"],
                  ["<code>CallNotPermittedException</code>", "ngoại lệ (thông báo lỗi chương trình ném ra) của thư viện chịu lỗi khi cầu dao đang mở và chặn cuộc gọi"]]),
           """Ba trạng thái cầu dao: đóng cho gọi, mở thì chặn, nửa mở thử một cuộc. Phép dịch sang trái nhân đôi mỗi vị trí: một trăm, hai trăm, bốn trăm. Bộ đếm chỗ hết chỗ thì từ chối. Xô token nạp đều, mỗi yêu cầu lấy một token. Ít kết nối nhất gửi việc cho máy ít việc nhất. Ngoại lệ chặn là lỗi báo khi cầu dao mở.""",
           focus=["1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ], checks=["alg.bnx_l30_retry(5, 4, 100) == ('that bai', 4, 700)"])

    intu = sc("intuition", "intuition", "Hình dung: ba trạng thái cầu dao và vách ngăn", [
        st(svg(1500, 520,
               txt(750, 40, "Cầu dao: đóng → mở khi hỏng liên tiếp → nửa mở thử một cuộc → đóng lại nếu tốt", 26, "middle", "#1f2937", True),
               box(60, 140, 360, 120, ["DONG", "cho mọi cuộc gọi đi qua", "đếm hỏng liên tiếp"], C_GREEN, 24, True),
               box(560, 140, 360, 120, ["MO", "chặn ngay, không gọi", "chờ đủ 1 000 ms"], C_RED, 24, True),
               box(1060, 140, 360, 120, ["NUA_MO", "cho thử đúng một cuộc", "tốt → DONG, hỏng → MO"], C_AMBER, 24, True),
               arrow(425, 190, 555, 190, "#dc2626", "3 cuộc hỏng", 22), arrow(925, 190, 1055, 190, "#d97706", "hết 1 000 ms", 22),
               codo([(1200, 262), (1200, 318), (740, 318), (740, 266)], "#dc2626", "thử hỏng → MO", 970, 306),
               codo([(1300, 262), (1300, 352), (240, 352), (240, 266)], "#16a34a", "thử tốt → DONG", 480, 340),
               box(60, 400, 640, 80, ["mục đích: dịch vụ đang hỏng được nghỉ,", "bên gọi không chờ vô ích"], C_PURPLE, 22),
               box(780, 400, 640, 80, ["số liệu đo ở phần ví dụ: 9 lần gọi,", "7 gọi thật, 2 bị chặn"], C_GRAY, 22)),
           """Đang đóng thì cuộc nào cũng đi qua, và cầu dao đếm hỏng liên tiếp. Đủ ba cuộc hỏng thì mở và chặn cho tới khi đủ một nghìn mili giây. Hết chờ thì nửa mở thử một cuộc: tốt thì đóng, hỏng thì mở lại. Dịch vụ hỏng nhờ vậy được nghỉ."""),
        st(svg(1500, 460,
               txt(750, 40, "Vách ngăn: dịch vụ chậm không được chiếm hết luồng của cả hệ thống", 26, "middle", "#1f2937", True),
               box(60, 110, 420, 80, "dịch vụ A: 2 chỗ", C_BLUE, 24, True),
               box(60, 230, 420, 80, "dịch vụ B: 2 chỗ", C_BLUE, 24, True),
               box(600, 110, 380, 80, ["A chậm: giữ 2 chỗ", "cuộc thứ 3 bị từ chối ngay"], C_RED, 22),
               box(600, 230, 380, 80, ["B vẫn còn đủ 2 chỗ", "không bị A kéo theo"], C_GREEN, 22),
               box(1080, 110, 380, 200, ["không vách ngăn:", "A chậm chiếm hết luồng chung", "B cũng đứng chờ"], C_AMBER, 22),
               txt(750, 380, "Đánh đổi: từ chối sớm một số yêu cầu để cả hệ thống còn chạy", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là vách ngăn: mỗi dịch vụ có hai chỗ riêng. A chậm giữ cả hai chỗ thì cuộc thứ ba tới A bị từ chối ngay, còn B vẫn đủ chỗ."""),
    ], checks=["alg.bnx_l30_breaker([i * 500 for i in range(9)], 2500) == (7, 2, 'DONG')"])

    form = sc("formula", "formula", "Suy ra từng bước: từ hết giờ tới cầu dao", [
        st("""<p><b>Bước 1. Hết giờ.</b> Cuộc gọi không có hạn chót sẽ giữ luồng vô thời hạn khi dịch vụ kia treo. Nên mọi cuộc gọi ra ngoài phải có hạn chót, ngắn hơn hạn chót của chính yêu cầu đang xử lý.</p>
$$\\text{hạn chót cuộc gọi trong} < \\text{hạn chót yêu cầu ngoài}$$""",
           """Bước một, hết giờ: cuộc gọi không hạn chót giữ luồng mãi khi dịch vụ kia treo, nên hạn chót cuộc gọi ngoài phải ngắn hơn hạn chót yêu cầu đang xử lý.""",
           clear=True),
        jstep([(("<code>static String chay(int hong, int toiDa, int goc) { … return \"…\"; }</code>", "khai hàm: <b>kiểu trả về</b> <code>String</code> (chuỗi chữ), tên <code>chay</code>, ba tham số số nguyên, mỗi tham số là kiểu rồi tên; <code>return</code> trả giá trị về chỗ gọi", "Khai hàm có kiểu trả về, tên và tham số; lệnh trả về đưa giá trị ra chỗ gọi."), "<code>chay(2, 4, 100)</code>", ""),
               (("<code>for (int lan = 1; lan &lt;= toiDa; lan++) { … }</code>", "vòng lặp đếm: khai biến đếm; điều kiện còn lặp; bước sau mỗi vòng (<code>lan++</code> tăng 1)", "Vòng lặp đếm có biến đếm, điều kiện còn lặp, và bước tăng theo từng vòng."), "<code>lan</code> chạy 1, 2, 3, 4", ""),
               (("<code>int cho = 0;</code>, <code>cho += …</code>, <code>if (lan &gt; hong) return …;</code>", "khai biến số nguyên; <code>+=</code> cộng thêm vào biến; <code>if (đk) lệnh;</code> làm lệnh nếu điều kiện đúng", "Dấu cộng bằng cộng thêm vào biến, và lệnh nếu làm câu sau khi điều kiện đúng."), "hỏng 2 lần: lần 3 có <code>3 &gt; 2</code> nên thành công", ""),
               (("<code>\"thanh cong o lan \" + lan + \", cho tong \" + cho + \" ms\"</code>", "dấu <code>+</code> giữa chuỗi và số nối chúng thành một chuỗi", "Dấu cộng giữa chuỗi và số nối thành một chuỗi."), "ra <code>thanh cong o lan 3, cho tong 300 ms</code>", "")]),
        st("""<p><b>Bước 2. Thử lại có lùi.</b> Thử lại ngay thì dồn thêm tải đúng lúc dịch vụ yếu. Nên chờ lâu dần: gốc 100 ms, nhân đôi mỗi lần.</p>"""
           + J_THULAI.show_from("static String chay", 11, title="ThuLai.java (đủ hàm chay)"),
           """Bước hai, thử lại có lùi: thử lại ngay thì dồn tải đúng lúc dịch vụ yếu, nên ta chờ lâu dần, gốc một trăm mili giây, nhân đôi mỗi lần.""",
           clear=True),
        st("""$$100 + 200 =\\hl{300}\\text{ ms (hỏng 2 lần, thành công ở lần 3)}; \\qquad 100 + 200 + 400 = \\hl{700}\\text{ ms (4 lần đều hỏng)}$$""",
           """Hỏng hai lần rồi thành công ở lần ba thì chờ một trăm cộng hai trăm, bằng ba trăm. Bốn lần đều hỏng thì chờ ba lần nên tổng bảy trăm.""",
           clear=True),
        st("""<p><b>Bước 3. Thử lại khuếch đại tải.</b> Nếu dịch vụ hỏng hẳn, mỗi yêu cầu thành 1 + r cuộc gọi (r là số lần thử lại): tải lên dịch vụ đang chết tăng đúng lúc nó cần nghỉ.</p>"""
           + """$$100 \\times (1 + 3) = \\hl{400}; \\qquad 10\\,000 \\times (1 + 3) = \\hl{40\\,000} \\text{ cuộc gọi}$$""",
           """Bước ba, thử lại khuếch đại tải: dịch vụ hỏng hẳn thì mỗi yêu cầu thành một cộng r cuộc gọi, r là số lần thử lại. Nên tải lên dịch vụ đang chết tăng đúng lúc nó cần nghỉ: một trăm yêu cầu thành bốn trăm cuộc, mười nghìn thành bốn mươi nghìn.""", focus=[1, 2],
           clear=True),
        jstep([(("<code>enum T { DONG, MO, NUA_MO }</code>, <code>T t = T.DONG;</code>, <code>t == T.MO</code>", "<code>enum</code>: kiểu chỉ có đúng các giá trị liệt kê; <code>T t = T.DONG</code> khai biến <code>t</code> đang ở DONG; <code>==</code> hỏi hai giá trị có bằng nhau", "Kiểu liệt kê chỉ có các giá trị nêu ra, và hai dấu bằng hỏi hai giá trị có bằng nhau."), "", ""),
               (("<code>boolean choPhep(long ms)</code>, <code>void ghi(boolean tot, long ms)</code>", "<code>boolean</code>: đúng hoặc sai; <code>void</code>: không trả gì; <code>long</code>: số nguyên lớn; <code>return false;</code> trả sai", "Hàm trả đúng sai, hoặc rỗng là không trả gì."), "", ""),
               (("<code>static final int NGUONG = 3;</code>, <code>int hong = 0;</code>", "<code>final</code>: gán một lần rồi không đổi; <code>static</code>: một bản chung cho cả lớp; <code>hong</code>: trường, nhớ giá trị giữa các lần gọi hàm", "Hằng gán một lần nên không đổi; trường nhớ giá trị giữa các lần gọi."), "", ""),
               (("<code>if (…) { … } else if (tot) { … } else if (++hong &gt;= NGUONG) { … }</code>", "chuỗi điều kiện: nhánh nào đúng trước thì làm, bỏ các nhánh sau; <code>++hong</code> tăng <code>hong</code> 1 rồi lấy giá trị mới; <code>&gt;=</code>: lớn hơn hoặc bằng", "Làm nhánh đúng đầu tiên; hai dấu cộng đặt trước tăng biến rồi lấy giá trị mới."), "", "")]),
        st("""<p><b>Bước 4. Cầu dao.</b> Để dịch vụ hỏng được nghỉ, ta đếm hỏng liên tiếp. Đủ ngưỡng thì <b>mở</b>: chặn ngay. Sau thời gian chờ thì <b>nửa mở</b>: thử một cuộc. Cầu dao nhớ trạng thái, nên không cần thử lại mù quáng.</p>"""
           + J_CAUDAO.show_from("boolean choPhep", 7, title="CauDao.java (trích): cho phép hay chặn"),
           """Bước bốn là cầu dao: dịch vụ hỏng cần nghỉ nên ta đếm số lần hỏng liên tiếp, đủ ngưỡng thì mở và chặn ngay. Hàm này nhìn thời điểm hiện tại: chưa đủ thời gian chờ thì chặn, đủ rồi thì nửa mở và cho thử một cuộc.""",
           clear=True),
        st(J_CAUDAO.show_from("void ghi", 10, title="CauDao.java (trích): ghi nhận kết quả mỗi cuộc gọi"),
           """Hàm ghi nhận kết quả rồi chuyển trạng thái theo kết quả đó. Đang nửa mở thì cuộc tốt đóng lại, cuộc hỏng mở lại. Ở trạng thái khác, cuộc tốt xoá bộ đếm hỏng, cuộc hỏng tăng bộ đếm, đủ ngưỡng ba thì mở.""",
           clear=True),
        st("""<p><b>Bước 5. Vách ngăn và giới hạn tốc độ.</b> Vách ngăn: mỗi dịch vụ phụ thuộc có số chỗ riêng (bộ đếm chỗ). Giới hạn tốc độ ở <b>cổng API</b> (cửa chung mọi yêu cầu từ ngoài đi qua trước khi vào các dịch vụ): <b>xô token</b>, dung tích 5, nạp 2 token mỗi giây. Một <b>đợt dồn</b> (burst) 12 yêu cầu cùng lúc thì nhận 5, từ chối 7.</p>"""
           + """$$0 + 1 \\times 2 = 2 \\text{ token sau 1 giây (tối đa 5)} \\Rightarrow \\text{nhận } \\hlg{2}$$""",
           """Bước năm: vách ngăn cho mỗi dịch vụ số chỗ riêng nên dịch vụ chậm không chiếm hết luồng. Giới hạn tốc độ đặt ở cổng API, cửa chung của yêu cầu từ ngoài, dùng xô token dung tích năm, nạp hai token mỗi giây. Đợt dồn mười hai yêu cầu nhận năm, từ chối bảy.""", focus=[1, 2, 2],
           clear=True, introduces=["bnx_burst"]),
        st("""<p><b>Bước 6. Cân bằng tải</b> là chia yêu cầu đến cho nhiều máy cùng làm một việc. <b>Xoay vòng</b>: lần lượt từng máy, không biết máy nào đang bận. <b>Ít kết nối nhất</b>: gửi cho máy đang xử lý ít việc nhất, tốt khi thời gian mỗi việc chênh nhiều.</p>""",
           """Bước sáu là cân bằng tải, chia yêu cầu cho nhiều máy cùng làm một việc. Xoay vòng gửi lần lượt từng máy, không biết máy nào bận. Cách ít kết nối nhất gửi cho máy ít việc nhất.""",
           clear=True),
        jstep([(("<code>int[] dur = {100, 10, …};</code>, <code>dur[i]</code>", "mảng số nguyên: <code>{…}</code> liệt kê các ô; <code>dur[i]</code> là ô thứ i, ô đầu là <code>dur[0]</code>", "Mảng là dãy ô, và chỉ số chọn ô, nghĩa là ô đầu có chỉ số không."), "việc đầu nặng 100 ms", ""),
               (("<code>long[][] ketThuc = new long[2][8];</code>", "mảng hai chiều, 2 hàng 8 cột: <code>ketThuc[s][k]</code> là giờ kết thúc của cuộc thứ k ở máy s; ô mới bằng 0", "Mảng hai chiều như bảng: hàng là máy, cột là cuộc."), "", ""),
               (("<code>long ms = i * 10L;</code>", "<code>10L</code>: số nguyên lớn; yêu cầu thứ i đến lúc i × 10 mili giây", "Chữ L sau số là số nguyên lớn."), "yêu cầu 3 đến lúc 30 ms", "")]),
        st(J_CANBANG.show_from("static int[] chay", 8, title="CanBang.java hàm chay (phần 1): 8 yêu cầu, việc đầu nặng 100 ms, việc sau 10 ms"),
           """Mô phỏng có tám yêu cầu cách nhau mười mili giây, nên việc đầu nặng một trăm chồng lên các việc sau mười.""",
           clear=True),
        jstep([(("<code>for (int s…) for (int k…) if (ketThuc[s][k] &gt; ms) dang[s]++;</code>", "hai vòng lồng nhau: đếm các cuộc của máy s chưa kết thúc lúc ms, tức cuộc đang chạy", "Hai vòng lồng nhau đếm cuộc còn chạy của mỗi máy."), "", ""),
               (("<code>int s = it ? (dang[1] &lt; dang[0] ? 1 : 0) : i % 2;</code>", "<code>đk ? a : b</code> cho a nếu đúng, ngược lại b; ít kết nối nhất: máy 1 nếu <code>dang[1] &lt; dang[0]</code>, không thì máy 0; xoay vòng: <code>i % 2</code> (phần dư)", "Phép chọn ba ngôi cho giá trị đầu nếu đúng, ngược lại giá trị sau, theo điều kiện đứng trước dấu hỏi."), "i = 3 xoay vòng: 3 % 2 = 1", ""),
               (("<code>ketThuc[s][soCuoc[s]++] = ms + dur[i];</code>", "ghi giờ kết thúc vào ô kế tiếp của máy s; <code>soCuoc[s]++</code> dùng giá trị rồi tăng 1", "Ghi giờ kết thúc vào ô kế tiếp; hai dấu cộng đặt sau tăng sau khi dùng."), "", ""),
               (("<code>max[s] = Math.max(max[s], dang[s]);</code>", "giữ số lớn hơn trong hai số: <code>max[s]</code> là số cuộc đồng thời lớn nhất đã gặp ở máy s", "Hàm lấy số lớn giữ mức đồng thời cao nhất."), "", "")]),
        st(J_CANBANG.show_from("for (int s = 0", 9, title="CanBang.java hàm chay (phần 2): chọn máy, ghi giờ kết thúc, giữ số đồng thời lớn nhất"),
           """Mỗi yêu cầu đếm cuộc đang chạy ở từng máy, chọn máy theo cách chia, ghi giờ kết thúc, rồi giữ số đồng thời lớn nhất.""",
           clear=True),
    ], checks=["alg.bnx_l30_retry(2, 4, 100)[2] == 100 + 200 and alg.bnx_l30_retry(5, 4, 100)[2] == 100 + 200 + 400", "alg.bnx_l30_retry_load(100, 3) == 400",
               "alg.bnx_l30_bucket(5, 2, [(0, 12), (1000, 12)]) == [5, 2]"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st(SH_TUCAI.show(lines=(1, 4), title="Chạy thật: biên dịch rồi chạy từng chương trình (JDK 21 thuần)")
           + """<div class="box warn" style="font-size:1.25em"><b>MÔ PHỎNG</b> (đồng hồ giả, không ngủ thật): thử lại, cầu dao, xô token, cân bằng tải. <b>THẬT</b>: vách ngăn (luồng và <code>Semaphore</code> của JDK) và Resilience4j ở phần tự kiểm.</div>""",
           """Ta chạy bằng JDK hai mươi mốt thuần, phần lớn là mô phỏng với đồng hồ giả nên chạy lại ra đúng kết quả cũ. Riêng vách ngăn dùng nhiều luồng thật.""",
           clear=True),
        st(SH_TUCAI.out_html("""hong 2 lan, toi da 4: thanh cong o lan 3, cho tong 300 ms
hong 5 lan, toi da 4: that bai sau 4 lan, cho tong 700 ms
hong 0 lan, toi da 4: thanh cong o lan 1, cho tong 0 ms""")
           + """$$① \\; 100 + 200 = \\hlg{300}; \\quad 100 + 200 + 400 = \\hl{700}; \\quad \\text{không hỏng: } 0$$""",
           """Phép tính thứ nhất là thử lại có lùi: hỏng hai lần thì thành công ở lần ba, chờ tổng ba trăm mili giây. Hỏng năm lần mà tối đa bốn thì thất bại sau bảy trăm, còn không hỏng thì không chờ.""", focus=[1, 3],
           clear=True),
        st(SH_TUCAI.out_html("""t=0 that bai -> DONG
t=500 that bai -> DONG
t=1000 that bai -> MO
t=1500 tu choi (cau dao MO)
t=2000 that bai -> MO
t=2500 tu choi (cau dao MO)
t=3000 thanh cong -> DONG
tong: 7 cuoc goi that, 2 cuoc bi chan""", "Cầu dao: gọi mỗi 500 ms, dịch vụ hỏng tới 2 500 ms (lược các dòng t = 3 500, 4 000 bằng cách chỉ hiện dòng quan trọng)")
           + """$$② \\; 3 \\text{ hỏng} \\Rightarrow \\text{MO}; \\;\\; \\text{sau } 1000 \\text{ ms thử (hỏng) → MO}; \\;\\; 7 \\text{ gọi thật} + 2 \\text{ bị chặn} = 9$$""",
           """Phép tính thứ hai là cầu dao: ba cuộc đầu hỏng nên mở ở một nghìn mili giây, cuộc ở một nghìn năm trăm bị chặn. Ở hai nghìn cho thử một cuộc, vẫn hỏng nên mở lại, cuộc ở hai nghìn năm trăm bị chặn. Ở ba nghìn thử tốt nên đóng. Tổng cộng bảy cuộc gọi thật, hai cuộc bị chặn.""", focus=[[1], 2, 3, 3],
           clear=True),
        st(SH_TUCAI.out_html("""2 cuoc dang cham: them 3 cuoc -> nhan 0, tu choi 3
sau khi 2 cuoc cham xong: con 2 cho trong
12 yeu cau cung luc luc 0 ms: nhan 5, tu choi 7
12 yeu cau cung luc sau 1 giay: nhan 2""")
           + """$$③ \\; 2 \\text{ chỗ đã chiếm} \\Rightarrow \\text{từ chối } 3; \\qquad ④ \\; \\text{xô } 5: \\text{nhận } 5, \\text{từ chối } 7; \\; \\text{sau 1 giây nhận } 2$$""",
           """Phép tính thứ ba là vách ngăn: hai cuộc chậm chiếm hết hai chỗ nên ba cuộc thêm bị từ chối, xong thì chỗ trống trở lại.
           Phép tính thứ tư là xô token: mười hai yêu cầu cùng lúc nhận năm, từ chối bảy; sau một giây nạp hai token nên nhận hai.""",
           clear=True),
        jstep([(("<code>int[] v = chay(false), l = chay(true);</code>, <code>v[0]</code>", "khai hai mảng một dòng: kết quả chia xoay vòng và chia ít kết nối nhất; <code>v[0]</code> là ô đầu, số cuộc đồng thời lớn nhất của máy 1", "Hai mảng kết quả khai một dòng, ô đầu là của máy một."), "", "")]),
        st(J_CANBANG.show_from("public static void main", 5, title="CanBang.java main: in số cuộc đồng thời lớn nhất của hai máy") + SH_TUCAI.out_html("""xoay vong: toi da dong thoi may 1 = 2, may 2 = 1
it ket noi nhat: toi da dong thoi may 1 = 1, may 2 = 1""")
           + """$$⑤ \\; \\text{xoay vòng: máy 1 chồng } \\hl{2} \\text{ việc}; \\quad \\text{ít kết nối nhất: } \\hlg{1} \\text{ mỗi máy}$$""",
           """Phép tính thứ năm là cân bằng tải: chia xoay vòng đẩy việc vào máy đang bận việc nặng, nên máy một chồng hai việc; chia cho máy ít kết nối nhất thì mỗi máy chỉ một việc.""",
           clear=True),
    ], checks=["alg.bnx_l30_retry(2, 4, 100) == ('ok', 3, 300)", "alg.bnx_l30_breaker([i * 500 for i in range(9)], 2500)[:2] == (7, 2)", "alg.bnx_l30_bucket(5, 2, [(0, 12), (1000, 12)]) == [5, 2]"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: Resilience4j thật", [
        jstep([(("<code>import io.github.resilience4j.circuitbreaker.*;</code>, <code>import java.time.Duration;</code>", "<code>import</code>: nạp lớp của thư viện để dùng tên ngắn; dấu <code>*</code> là nạp mọi lớp trong gói; <code>Duration</code>: độ dài thời gian", "Câu nạp thư viện; dấu sao nạp mọi lớp trong gói."), "", ""),
               (("<code>var cfg = CircuitBreakerConfig.custom() … .build();</code>", "<code>var</code>: máy tự suy kiểu; mỗi dòng bắt đầu bằng dấu chấm đặt một thông số; <code>.build()</code> tạo cấu hình", "Một từ khoá để máy tự suy kiểu; mỗi dòng dấu chấm đặt một thông số; dòng cuối tạo cấu hình."), "", ""),
               (("<code>CircuitBreaker.of(\"dich-vu\", cfg)</code>, <code>Duration.ofMillis(1000)</code>, <code>… main(String[] a) throws Exception</code>", "tạo cầu dao tên <code>dich-vu</code> theo cấu hình; 1000 mili giây; hàm chính, <code>throws Exception</code> báo có thể ném lỗi mà không cần bắt", "Tạo cầu dao theo cấu hình; hàm chính khai có thể ném lỗi."), "", "")]),
        jstep([(("<code>.slidingWindowType(COUNT_BASED)</code>", "cửa sổ trượt đếm theo số cuộc, chỉ nhìn các cuộc gần nhất", "Cửa sổ trượt chỉ nhìn các cuộc gần nhất."), "", ""),
               (("<code>.minimumNumberOfCalls(4)</code>", "chưa đủ 4 cuộc thì chưa tính tỉ lệ hỏng, nên chưa mở sớm", "Chưa đủ bốn cuộc nên chưa tính tỉ lệ hỏng, chưa mở sớm."), "", ""),
               (("<code>.failureRateThreshold(50)</code>", "hỏng từ 50% số cuộc trong cửa sổ thì mở", "Hỏng từ một nửa số cuộc trong cửa sổ thì mở."), "", "")]),
        st(J_R4J.show(lines=(1, 10), title="R4j.java (trích): cầu dao của thư viện Resilience4j 2.3.0, cửa sổ 4 cuộc, ngưỡng 50%, chờ 1 giây, nửa mở thử đúng 1 cuộc"),
           """Ta kiểm bằng đường khác hẳn là thư viện chịu lỗi của Java, đặt theo cửa sổ bốn cuộc, ngưỡng năm mươi phần trăm, chờ một giây.""",
           clear=True),
        jstep([(("<code>cb.getEventPublisher().onStateTransition(e -&gt; …)</code>", "đăng ký một hàm ngắn <code>e -&gt; …</code> để thư viện gọi mỗi khi cầu dao đổi trạng thái; <code>e</code> là sự kiện", "Đăng ký hàm ngắn để thư viện gọi khi đổi trạng thái."), "", ""),
               (("<code>for (int i = 1; i &lt;= 6; i++)</code>, <code>tuChoi++;</code>", "vòng lặp đếm 6 lần; <code>tuChoi++</code> tăng biến đếm thêm 1", "Vòng lặp sáu lần; hai dấu cộng tăng biến đếm."), "", ""),
               (("<code>cb.executeRunnable(() -&gt; { throw new IllegalStateException(\"hong\"); });</code>", "chạy đoạn việc qua cầu dao; <code>() -&gt;</code> hàm ngắn không tham số; <code>throw new …</code> ném lỗi, nên cuộc này luôn hỏng", "Chạy đoạn việc luôn ném lỗi qua cầu dao."), "", ""),
               (("<code>catch (CallNotPermittedException e) { tuChoi++; } catch (IllegalStateException e) { }</code>", "bắt lỗi theo loại: loại do cầu dao chặn thì đếm; lỗi cố ý thì bỏ qua (ngoặc nhọn rỗng)", "Bắt lỗi theo loại: chặn thì đếm, lỗi cố ý bỏ qua."), "", "")]),
        st(J_R4J.show(lines=(11, 22), title="R4j.java (tiếp): gọi 6 cuộc hỏng liên tiếp, đếm cuộc bị chặn"),
           """Mã gọi sáu cuộc hỏng liên tiếp nên cầu dao mở và chặn các cuộc cuối, rồi đếm cuộc bị chặn.""",
           clear=True),
        jstep([(("<code>Thread.sleep(1100);</code>", "ngủ 1100 mili giây, lâu hơn thời gian chờ 1000, nên cầu dao sang nửa mở", "Ngủ một nghìn một trăm mili giây nên cầu dao nửa mở."), "", ""),
               (("<code>cb.executeRunnable(() -&gt; { });</code>, <code>cb.getState()</code>", "đoạn việc rỗng không ném lỗi, tức một cuộc tốt; <code>getState()</code> cho trạng thái hiện tại", "Đoạn rỗng không ném lỗi là cuộc tốt; lệnh lấy trạng thái cho biết trạng thái hiện tại."), "", "")]),
        st(J_R4J.show(lines=(23, 25), title="R4j.java (hết): ngủ 1 100 ms, lâu hơn thời gian chờ, rồi gọi một cuộc tốt")
           + SH_R4J.out_html(),
           """Rồi mã ngủ lâu hơn thời gian chờ nên nửa mở, và gọi một cuộc tốt. Thư viện đi đúng ba trạng thái ta cài, chỉ ở kịch bản này.""",
           clear=True),
        st(table(["ca", "cầu dao tự cài", "thư viện thật"],
                                    [["hỏng liên tiếp → mở", "mở sau 3 cuộc hỏng", "mở sau 4 cuộc hỏng (cửa sổ 4, ngưỡng 50%)"],
                                     ["cuộc gọi khi mở", "chặn", "bị chặn (CallNotPermittedException): 2 cuộc"],
                                     ["nửa mở thử mấy cuộc", "đúng 1 cuộc", "phải đặt <code>permittedNumberOfCallsInHalfOpenState(1)</code>; mặc định cho thử nhiều cuộc hơn, nên sau 1 cuộc tốt vẫn nửa mở"],
                                     ["sau thời gian chờ", "nửa mở, thử một cuộc", "mở (OPEN) → nửa mở (HALF_OPEN) → đóng (CLOSED)"]]),
           """Khác nhau là cách đếm: bản tự cài mở sau ba cuộc hỏng, thư viện dùng cửa sổ bốn cuộc nên mở sau bốn. Nửa mở phải đặt thử một cuộc. Ba trạng thái giống nhau ở cấu hình này, chưa chứng minh với mọi cấu hình.""",
           clear=True),
    ], checks=["alg.bnx_l30_breaker([0, 100, 200, 300, 400, 500], 10**9)[:2] == (3, 3)"])

    quymo = sc("quymo", "example", "Khi tải lớn dần: bao nhiêu cuộc gọi tới dịch vụ đang hỏng?", [
        jstep([(("<code>for (int n : new int[] {100, 10000}) { … }</code>", "duyệt từng phần tử của mảng vừa tạo bằng <code>new int[] {…}</code>: mỗi vòng <code>n</code> nhận 100, rồi 10000", "Vòng lặp duyệt từng phần tử, mỗi vòng một cỡ."), "", ""),
               (("<code>CauDao c = new CauDao();</code>", "tạo một cầu dao mới từ lớp <code>CauDao</code> ở bước bốn: đóng, chưa hỏng cuộc nào", "Tạo cầu dao mới."), "", ""),
               (("<code>long ms = i * 10000L / n;</code>, <code>if (!c.choPhep(ms)) continue;</code>", "<code>i * 10000L / n</code>: rải n yêu cầu đều trong 10000 ms; <code>!</code> đảo đúng thành sai; <code>continue</code> bỏ phần còn lại của vòng, sang vòng sau", "Rải đều n yêu cầu trong mười nghìn mili giây; chấm than đảo đúng sai; lệnh tiếp tục sang vòng sau."), "n = 100: yêu cầu i đến lúc i × 100 ms", ""),
               (("<code>c.ghi(false, ms); that++;</code>, <code>4 * n</code>", "ghi một cuộc hỏng; <code>that++</code> đếm cuộc gọi thật; <code>4 * n</code>: thử lại 3 lần là 4 cuộc mỗi yêu cầu", "Ghi cuộc hỏng, đếm cuộc gọi thật; bốn nhân n là số cuộc khi không có cầu dao."), "", "")]),
        st(J_QUYMO.show(lines=(1, 10), title="QuyMo.java (phần 1): n yêu cầu rải đều trong 10 giây sự cố, dịch vụ hỏng suốt"),
           """Mỗi yêu cầu tới dịch vụ đang hỏng: cầu dao chặn thì bỏ qua, cho qua thì ghi cuộc hỏng và đếm.""",
           clear=True),
        st(J_QUYMO.show(lines=(11, 16), title="QuyMo.java (phần 2): in số cuộc gọi không cầu dao (4n) và có cầu dao")
           + """<p><b>Tính tay trước khi chạy</b> (n = 100: yêu cầu i đến lúc i × 100 ms): ba cuộc hỏng đầu ở 0, 100, 200 ms mở cầu dao lúc 200 ms. Chờ 1 000 ms rồi cứ mỗi 1 000 ms thử một cuộc, và cuộc nào cũng hỏng: thử ở 1 200, 2 200, …, 9 200 ms, tức <b>9</b> cuộc (cuộc kế ở 10 200 ms ngoài 10 giây).</p>
$$3 + 9 = \\hl{12}\\text{ cuộc gọi thật; } n = 10\\,000 \\text{ cũng vậy (mở lúc 2 ms, thử ở 1 002, …, 9 002 ms)}$$""",
           """Tính tay trước khi chạy: ba cuộc hỏng đầu mở cầu dao ngay. Rồi mỗi một nghìn mili giây cầu dao cho thử một cuộc, cuộc nào cũng hỏng, nên mười giây có chín cuộc thử. Ba cộng chín bằng mười hai cuộc gọi thật, với cả hai cỡ.""",
           clear=True),
        st(SH_TUCAI.out_html("""100 yeu cau, 10 giay su co: thu lai 3 lan khong cau dao 400 cuoc goi, co cau dao 12
10000 yeu cau, 10 giay su co: thu lai 3 lan khong cau dao 40000 cuoc goi, co cau dao 12""", "Chạy thật: n yêu cầu rải đều trong 10 giây sự cố")
           + """$$100 \\to 10\\,000 \\;(\\times 100): \\; 400 \\to 40\\,000 \\text{ cuộc gọi; có cầu dao: } 12 \\to \\hlg{12}$$""",
           """Đây là số đo thật. Một trăm yêu cầu trong mười giây sự cố, thử lại ba lần, thành bốn trăm cuộc; mười nghìn yêu cầu, gấp một trăm lần, là bốn mươi nghìn. Có cầu dao thì cả hai chỉ mười hai cuộc.""", focus=[1, 2, 3],
           clear=True),
        st(table(["cách", "được", "mất", "chọn khi"],
                 [["không thử lại", "không khuếch đại tải", "lỗi tạm thời nào cũng lộ ra cho khách", "việc không quan trọng"],
                  ["thử lại có lùi", "che được lỗi tạm thời", "dịch vụ hỏng lâu thì tải gấp (1 + r) lần", "lỗi ngắn, dịch vụ có dư công suất"],
                  ["thử lại có lùi + cầu dao + vách ngăn", "tải lên dịch vụ hỏng gần như không đổi; hệ thống còn chạy phần khác", "phải chọn ngưỡng, thời gian chờ; có thể chặn nhầm khi dịch vụ vừa hồi phục", "mọi cuộc gọi ra dịch vụ ngoài quan trọng"]]),
           """Bảng này là các lựa chọn. Không thử lại thì không khuếch đại tải, nhưng lỗi tạm thời nào cũng lộ ra. Thử lại có lùi che lỗi tạm thời, nhưng hỏng lâu thì tải gấp một cộng r. Kết hợp cả ba giữ tải gần như không đổi.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l30_breaker([i * 10000 // 100 for i in range(100)], 10**9)[0] == 12", "alg.bnx_l30_breaker([i * 10000 // 10000 for i in range(10000)], 10**9)[0] == 12", "400 * 100 == 40000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Thử lại <b class="red">ngay lập tức</b> và <b class="red">mãi mãi</b> cho mọi lỗi. Chạy thật: dịch vụ hỏng 10 giây, 10 000 yêu cầu thành 40 000 cuộc gọi. Thử lại phải có số lần tối đa, có lùi, và chỉ cho lỗi tạm thời.</div>"""
           + table(["số yêu cầu trong 10 giây sự cố", "thử lại 3 lần, không cầu dao", "có cầu dao"],
                   [[nowrap("100"), nowrap("400 cuộc gọi"), "12"], [nowrap("10 000"), nowrap("40 000 cuộc gọi"), "12"]]),
           """Lỗi thứ nhất là thử lại ngay lập tức và mãi mãi. Chạy thật, hỏng mười giây thì mười nghìn yêu cầu thành bốn mươi nghìn cuộc. Thử lại phải có số lần tối đa, có lùi, chỉ cho lỗi tạm thời.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Thử lại cho <b class="red">lệnh ghi không có khoá lũy đẳng</b> (mã gắn vào lệnh: gửi lại nhiều lần vẫn chỉ xử lý một lần): lệnh chuyển tiền hết giờ nhưng thật ra đã chạy, thử lại thì chuyển hai lần. Chỉ thử lại lệnh đọc hoặc lệnh có khoá lũy đẳng.</div>""",
           """Lỗi thứ hai: thử lại lệnh ghi không có khoá lũy đẳng, tức mã để gửi lại nhiều lần vẫn chỉ xử lý một lần. Chuyển tiền hết giờ nhưng đã chạy, thử lại thì chuyển hai lần.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Dùng <b class="red">một cầu dao, một bộ đếm chỗ chung</b> cho mọi dịch vụ phụ thuộc: một dịch vụ chậm làm mở cầu dao chung, chặn luôn các dịch vụ khoẻ. Mỗi dịch vụ phụ thuộc một cầu dao và một vách ngăn riêng, như hình đã vẽ.</div>""",
           """Lỗi thứ ba: dùng một cầu dao chung cho mọi dịch vụ phụ thuộc. Một dịch vụ chậm mở cầu dao chung và chặn luôn dịch vụ khoẻ. Mỗi dịch vụ cần cầu dao và vách ngăn riêng.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> Đặt ngưỡng và thời gian chờ <b class="red">một lần rồi quên</b>. Dịch vụ thay đổi cỡ tải: cửa sổ 4 cuộc mở cầu dao oan khi chỉ 4 cuộc đầu hỏng ngẫu nhiên; thời gian chờ quá dài giữ cầu dao mở sau khi dịch vụ đã hồi phục.
Cách chữa: theo dõi số lần cầu dao mở, số cuộc bị chặn, số cuộc thử; chỉnh theo số đo thật.</div>""",
           """Lỗi thứ tư: đặt ngưỡng và thời gian chờ một lần rồi quên. Cỡ tải đổi thì cửa sổ bốn cuộc có thể mở cầu dao oan, còn chờ quá dài giữ cầu dao mở dù dịch vụ đã hồi phục.""", clear=True),
    ], checks=["alg.bnx_l30_retry_load(10000, 3) == 40000", "alg.bnx_l30_breaker([i * 500 for i in range(9)], 2500)[1] == 2"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Gọi tối đa 5 lần (lần đầu + 4 thử lại), gốc 50 ms, nhân đôi mỗi lần. Hỏng cả 5 lần: tổng chờ bao nhiêu (có chờ sau lần cuối không)? Nếu đề nói &laquo;thử lại 5 lần&raquo; thì sao?"],
                  ["2", "Xô token dung tích 4, nạp 1 token mỗi giây. 9 yêu cầu cùng lúc ở ms = 0, rồi 9 yêu cầu cùng lúc ở ms = 2 000. Mỗi đợt nhận mấy?"],
                  ["3", "Quyết định (số minh hoạ): dịch vụ chấm điểm hay chậm 3–4 giây, mỗi giây 500 yêu cầu qua nó. Chọn: tăng hạn chót lên 10 giây, thử lại 3 lần, hay cầu dao + vách ngăn 50 chỗ + hạn chót 2 giây? Vì sao?"]]),
           """Đến lượt bạn, ba câu làm ra giấy. Câu một tính tổng chờ của thử lại có lùi khi hỏng cả năm lần, và khi đề nói thử lại năm lần. Câu hai tính mỗi đợt xô token nhận mấy yêu cầu. Câu ba chọn giữa tăng hạn chót, thử lại, hay cầu dao cùng vách ngăn. Hãy dừng lại làm rồi xem đáp án.""",
           focus=[0, "1.2", "1.2", "1.3", "1.4", "1.4", 0], pause=30),
        st("""<p>Câu 1: chờ sau mỗi lần hỏng, trừ lần cuối: 5 lần gọi chờ 4 lần: 50, 100, 200, 400. &laquo;Thử lại 5 lần&raquo; là 6 lần gọi, chờ thêm 800: tổng 1550 ms.</p>
$$50 + 100 + 200 + 400 = \\hlg{750} \\text{ ms}; \\quad \\text{không chờ sau lần thứ 5}$$""",
           """Đáp án câu một: ta chờ sau mỗi lần hỏng trừ lần cuối, nên năm lần gọi có bốn lần chờ: năm mươi, một trăm, hai trăm, bốn trăm, tổng bảy trăm năm mươi. Thử lại năm lần là sáu lần gọi, tổng một nghìn năm trăm năm mươi."""),
        st("""<p>Câu 2: mỗi đợt 9 yêu cầu; xô đầy 4 token; nạp 1 token mỗi giây nên đến 2 000 ms thêm 2 token (tối đa 4).</p>
$$\\text{đợt 1: xô đầy 4 token} \\Rightarrow \\hlg{4}; \\quad \\text{sau } 2\\,000 \\text{ ms: } 0 + 2 = 2 \\Rightarrow \\text{đợt 2: } \\hlg{2}$$""",
           """Đáp án câu hai. Mỗi đợt có chín yêu cầu. Đợt một xô đầy bốn token nên nhận bốn. Nạp một token mỗi giây, sau hai giây xô có hai token, nên đợt hai nhận hai."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["tăng hạn chót lên 10 giây", "ít lỗi hết giờ", "500 yêu cầu/giây × 10 giây = 5 000 luồng chờ, nếu cuộc gọi treo tới hết hạn chót (chỉ chậm 3,5 giây thì ≈ 1 750): cạn luồng"],
                  ["thử lại 3 lần", "che lỗi tạm thời", "dịch vụ vốn chậm thì tải gấp 4; nghẽn thêm"],
                  ["cầu dao + vách ngăn 50 chỗ + hạn chót 2 giây", "tối đa 50 cuộc đồng thời; chậm thì bị từ chối sớm; hệ còn chạy", "50 chỗ, mỗi cuộc giữ tối đa 2 giây nên chỉ ≤ 25 yêu cầu/giây qua được: ≈ 95% (475/500) bị từ chối; cuộc 3–4 giây vẫn quá hạn"]]),
           """Đáp án câu ba: hạn chót mười giây khiến năm trăm yêu cầu mỗi giây thành năm nghìn luồng chờ, nên cạn luồng. Thử lại ba lần thì tải gấp bốn. Cách thứ ba hợp lý nhất, nhưng khoảng chín mươi lăm phần trăm yêu cầu bị từ chối sớm."""),
    ], checks=["alg.bnx_l30_retry(6, 6, 50)[2] == 1550 and alg.bnx_l30_vach_qua(50, 2) == 25 and round(100 * (1 - alg.bnx_l30_vach_qua(50, 2) / 500)) == 95 and alg.bnx_l30_luong_cho(500, 3.5) == 1750", "alg.bnx_l30_retry(5, 5, 50)[2] == 50 + 100 + 200 + 400 == 750", "alg.bnx_l30_bucket(4, 1, [(0, 9), (2000, 9)]) == [4, 2]", "500 * 10 == 5000"])

    lab_pr = practice_scene(sc, "Tự làm: cầu dao nhỏ với đồng hồ giả", practice_steps2(
        st, "BNX", "L30",
        """<div class="box warn" style="font-size:1.25em"><b>MÔ PHỎNG</b>: đồng hồ giả, giờ là số mili giây truyền vào, chương trình không ngủ thật.</div>
<p><b>Đề</b>: cầu dao <code>DONG</code> → <code>MO</code> → <code>NUA_MO</code> với đồng hồ giả, ngưỡng <b>2</b> cuộc hỏng liên tiếp, chờ <b>600 ms</b>. Gọi mỗi 300 ms từ 0 tới 3000; hỏng khi ms &lt; 1500.</p>
<p>In <code>t=… hong -&gt; …</code>, <code>t=… tot -&gt; …</code>, <code>t=… chan</code>, rồi <code>goi that …, bi chan …</code>.</p>""",
        """Tới phần bạn tự làm, một mô phỏng: viết cầu dao ba trạng thái bằng Python với đồng hồ giả, ngưỡng hai cuộc hỏng, chờ sáu trăm mili giây. Gọi mỗi ba trăm mili giây từ không tới ba nghìn, dịch vụ hỏng trước một nghìn năm trăm. In từng lần gọi, rồi dòng tổng kết. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> lưu trạng thái, số hỏng liên tiếp và <code>mo_luc</code>. Đang <code>MO</code> mà chưa đủ 600 ms thì chặn; đủ rồi thì <code>NUA_MO</code>: tốt → <code>DONG</code>, hỏng → <code>MO</code> (đặt lại <code>mo_luc</code>).
Lời giải đầy đủ ở <code>labs/BNX/L30/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, lưu trạng thái, số hỏng liên tiếp và thời điểm mở. Đang mở mà chưa đủ thời gian chờ thì chặn, đủ rồi thì nửa mở: tốt thì đóng, hỏng thì mở lại. Lời giải chỉ mở sau khi đã tự thử.""", pause=180), "BNX", "L30")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("hết giờ cho mọi cuộc gọi ngoài", "thử lại có lùi, chỉ lỗi tạm thời", "cầu dao ngăn khuếch đại tải", "vách ngăn + giới hạn tốc độ", "cân bằng tải theo mức bận"),
           """Mọi cuộc gọi ngoài có hạn chót, thử lại có lùi chỉ cho lỗi tạm thời. Cầu dao ngăn thử lại khuếch đại tải. Vách ngăn và giới hạn tốc độ giữ một chỗ chậm không kéo sập hệ thống."""),
        st("""<div class='box key'><b>Tư duy:</b> chịu lỗi không phải là &laquo;thử lại cho tới khi được&raquo;, mà là <b>biết lúc nào thôi gọi</b>. Mỗi cơ chế (hết giờ, thử lại, cầu dao, vách ngăn) trả lời một câu hỏi khác; thiếu một cái, sự cố nhỏ thành sự cố lớn.
Và mọi ngưỡng phải <b>đo và chỉnh</b>, không đặt một lần rồi quên.</div>""",
           """Chịu lỗi không phải thử lại cho tới khi được, mà là biết lúc nào thôi gọi. Mỗi cơ chế trả lời một câu hỏi khác, thiếu một cái thì sự cố nhỏ thành lớn, ngưỡng phải đo rồi chỉnh."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Circuit breaker, retry, timeout: bạn dùng thế nào?", "mọi cuộc gọi ngoài có hạn chót ngắn hơn hạn chót yêu cầu; thử lại có lùi, tối đa, chỉ lệnh đọc hoặc lệnh có khoá lũy đẳng; cầu dao DONG/MO/NUA_MO chặn thử lại khuếch đại tải (đo: 40 000 cuộc gọi → 12)"],
                  ["Bulkhead và rate limit khác nhau thế nào?", "vách ngăn giới hạn số cuộc gọi đồng thời tới một dịch vụ phụ thuộc; giới hạn tốc độ (xô token) giới hạn số yêu cầu mỗi giây vào cổng API"],
                  ["Load balancing chọn thuật toán nào?", "xoay vòng khi việc đồng đều; ít kết nối nhất khi thời gian mỗi việc chênh nhiều (đo: xoay vòng chồng 2 việc lên máy bận)"]]),
           """Người phỏng vấn thường hỏi ba câu: dùng hết giờ, thử lại, cầu dao ra sao; vách ngăn khác giới hạn tốc độ thế nào; cân bằng tải chọn kiểu nào. Trả lời nằm sẵn trên bảng.""", clear=True),
        st("""<p>Bài sau: <b>quan sát hệ thống</b>: nhật ký có cấu trúc, mã tương quan, chỉ số và cảnh báo.</p>""",
           """Ở bài ba mươi mốt, ta tìm hiểu quan sát hệ thống: nhật ký có cấu trúc, mã tương quan, chỉ số và cảnh báo.""",
           forward_ref=True),
    ], checks=["alg.bnx_l30_retry_load(10000, 3) == 40000"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L30", "chiu_loi_cau_dao_can_bang_tai",
                  "Bài 30 — Chịu lỗi bằng mã: thử lại, cầu dao, vách ngăn, giới hạn tốc độ và cân bằng tải",
                  "curriculum/bnx.yaml L30; audit/bnx/verify_bnx.py L30; audit/bnx/sources_l30.md: tài liệu Resilience4j (CircuitBreaker, đọc 2026-11-14); "
                  "bản tự cài Java thuần với đồng hồ giả và Resilience4j 2.3.0 thật chạy trên Temurin JDK 21.0.13",
                  ["Tính tổng thời gian chờ của thử lại có lùi theo luỹ thừa 2 và nói khi nào thử lại có hại",
                   "Đọc chuỗi trạng thái của cầu dao ba trạng thái theo đồng hồ giả và đếm cuộc gọi bị chặn",
                   "So sánh cầu dao tự cài với Resilience4j thật: cùng ba trạng thái, khác cách đếm hỏng",
                   "Giải thích vách ngăn bằng bộ đếm chỗ giới hạn số cuộc gọi đồng thời",
                   "Tính số yêu cầu nhận và từ chối của giới hạn tốc độ kiểu xô token",
                   "So sánh chia xoay vòng với chia cho máy ít kết nối nhất",
                   "Viết cầu dao nhỏ với đồng hồ giả"],
                  scenes, assumes=["bnx_ngoai_le"],
                  covers=[(1, "example"), (2, "example"), (3, "check"), (4, "example"), (5, "example"), (6, "example"), (7, "practice")])
