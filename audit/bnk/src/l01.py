from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    mat = prog("MatCapNhat", """
public class MatCapNhat {
    static int dem = 0;
    public static void main(String[] args) throws Exception {
        Runnable viec = () -> { for (int i = 0; i < 1_000_000; i++) dem++; };
        Thread a = new Thread(viec);
        Thread b = new Thread(viec);
        a.start(); b.start();      // hai luồng cùng chạy
        a.join(); b.join();        // chờ cả hai xong
        System.out.println("dung 2000000? " + (dem == 2_000_000));
    }
}""", out="dung 2000000? false")
    co_khoa = prog("CoKhoa", """
public class CoKhoa {
    static int dem = 0;
    static final Object KHOA = new Object();
    public static void main(String[] args) throws Exception {
        Runnable viec = () -> {
            for (int i = 0; i < 1_000_000; i++) {
                synchronized (KHOA) { dem++; }   // mỗi lúc chỉ một luồng vào khối này
            }
        };
        Thread a = new Thread(viec);
        Thread b = new Thread(viec);
        a.start(); b.start();
        a.join(); b.join();
        System.out.println("dung 2000000? " + (dem == 2_000_000));
    }
}""", out="dung 2000000? true")
    luong_ao = prog("LuongAo", """
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
public class LuongAo {
    public static void main(String[] args) throws Exception {
        AtomicInteger xong = new AtomicInteger();
        long t0 = System.nanoTime();
        try (ExecutorService ex = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 10_000; i++) {
                ex.submit(() -> { Thread.sleep(100); return xong.incrementAndGet(); });
            }
        }                                  // đóng: chờ mọi việc xong
        long ms = (System.nanoTime() - t0) / 1_000_000;
        System.out.println("xong " + xong + " yeu cau, duoi 2 giay? " + (ms < 2000));
    }
}""", out="xong 10000 yeu cau, duoi 2 giay? true")
    lab_khoa = prog("TongBaLuong", """
public class TongBaLuong {
    static long tong = 0;
    static final Object KHOA = new Object();
    public static void main(String[] args) throws Exception {
        Runnable viec = () -> {
            for (int i = 0; i < 200_000; i++) {
                synchronized (KHOA) { tong++; }
            }
        };
        Thread[] ds = { new Thread(viec), new Thread(viec), new Thread(viec) };
        for (Thread t : ds) t.start();
        for (Thread t : ds) t.join();
        System.out.println("tong = " + tong);
    }
}""", out="tong = 600000")
    hook = sc("hook", "hook", "Vì sao hai người cùng nạp tiền lại làm mất một khoản?", [
        st("""<p>Số dư là $100$. Người A nạp $50$, người B nạp $30$ cùng lúc. Đúng ra phải ra $180$.</p>
<div class="box key">Nhưng máy có thể in ra <b>180</b>, <b>150</b> hoặc <b>130</b>, tuỳ luồng nào chen vào trước.</div>""",
           """Chào bạn, số dư là một trăm. Người A nạp năm mươi, người B nạp ba mươi, cùng một lúc, nên kết quả đúng phải là một trăm tám mươi.
           Nhưng máy có thể in ra một trăm tám mươi, một trăm năm mươi, hoặc một trăm ba mươi, tuỳ luồng nào chen vào trước."""),
        st(table(["tình huống", "hậu quả"],
                 [["hai luồng sửa cùng một số dư", "mất một khoản nạp, ngân hàng lệch sổ"],
                  ["10 000 yêu cầu cùng chờ đối tác trả lời", "hết luồng, yêu cầu mới xếp hàng dài"]]),
           """Hôm nay ta học hai chuyện. Một là hai luồng sửa cùng một số dư thì mất khoản nạp. Hai là mười nghìn yêu cầu cùng chờ đối tác thì dịch vụ hết luồng.
           Luồng ảo của Java hai mươi mốt giải quyết chuyện thứ hai."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: ba điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Luồng", "một dòng việc chạy riêng trong chương trình; nhiều luồng chạy cùng lúc và dùng chung dữ liệu", "mỗi yêu cầu chuyển tiền một luồng"],
                  ["② Đọc rồi ghi", "muốn tăng số dư phải đọc số cũ, cộng, rồi ghi lại", "đọc 100, ghi 150"],
                  ["③ Chạy xen kẽ", "CPU (bộ xử lý chạy lệnh) đổi qua lại giữa các luồng ngay giữa chừng", "A đọc, B đọc, rồi mới ghi"]]),
           """Ôn ba điều. Luồng là một dòng việc chạy riêng trong chương trình. Nhiều luồng chạy cùng lúc và dùng chung dữ liệu, ví dụ mỗi yêu cầu chuyển tiền có một luồng.
           Muốn tăng số dư phải đọc số cũ, cộng thêm, rồi ghi lại.
           Còn bộ xử lý chạy lệnh có thể đổi qua lại giữa các luồng ngay giữa chừng, nên A đọc, B đọc rồi mới ghi là chuyện bình thường."""),
        st("""$$100 + 50 + 30 = 180$$""",
           """Nếu hai việc chạy lần lượt, hết việc này rồi mới tới việc kia, thì một trăm cộng năm mươi cộng ba mươi bằng một trăm tám mươi, đúng như mong đợi.""",
           introduces=["plus"] if False else None),
    ], checks=["100 + 50 + 30 == 180"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["race condition", "kết quả phụ thuộc thứ tự chạy may rủi của các luồng"],
                  ["lost update", "một lần ghi đè mất lần ghi trước"],
                  ["vùng găng", "đoạn mã đọc rồi ghi dữ liệu dùng chung, chỉ an toàn khi mỗi lúc một luồng chạy"],
                  ["lock (khoá)", "chỉ một luồng được vào vùng găng tại một thời điểm"],
                  ["blocking I/O", "luồng đứng chờ mạng hoặc đĩa, không làm gì"],
                  ["virtual thread", "luồng ảo, rất nhẹ, do Java quản lý chứ không do hệ điều hành"],
                  ["luồng nền (platform thread)", "luồng thật do hệ điều hành quản lý, tạo bằng <code>new Thread</code>"],
                  ["luồng chạy (carrier thread)", "<b>một</b> luồng nền mà luồng ảo đang mượn để chạy; luồng ảo chờ thì trả lại"]]),
           """Bảng dưới đây giải nghĩa tám thuật ngữ mà bài sẽ dùng. Điều kiện tranh chấp là khi kết quả phụ thuộc thứ tự chạy may rủi. Mất cập nhật là khi một lần ghi đè mất lần ghi trước.
           Vùng găng là đoạn mã đọc rồi ghi dữ liệu dùng chung, chỉ an toàn khi mỗi lúc một luồng chạy. Khoá cho phép chỉ một luồng vào vùng găng. Chờ vào ra là khi luồng đứng đợi mạng hoặc đĩa. Luồng ảo là luồng rất nhẹ do Java quản lý.
           Luồng nền là luồng thật do hệ điều hành quản lý. Còn luồng chạy là một luồng nền mà luồng ảo đang mượn để chạy, và khi luồng ảo chờ thì trả nó lại."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: xen kẽ, khoá, và luồng ảo", [
        st(svg(1500, 420,
               txt(60, 60, "Luồng A", 26, "start", "#1f2937", True), txt(60, 200, "Luồng B", 26, "start", "#1f2937", True),
               box(200, 30, 230, 60, "A đọc: 100", C_BLUE), box(700, 30, 230, 60, "A ghi: 150", C_BLUE),
               box(330, 170, 230, 60, "B đọc: 100", C_AMBER), box(960, 170, 230, 60, "B ghi: 130", C_AMBER),
               arrow(315, 95, 700, 60, "#2a78d6"),
               txt(750, 330, "B ghi sau cùng: số dư = 130, khoản nạp 50 của A biến mất", 28, "middle", "#dc2626", True),
               txt(750, 380, "A và B cùng đọc 100 trước khi ai kịp ghi", 24, "middle", "#475569")),
           """Hình cho thấy một cách xen kẽ xấu. A đọc số dư một trăm. Trước khi A kịp ghi, B cũng đọc một trăm. A ghi một trăm năm mươi.
           Rồi B ghi một trăm ba mươi, đè lên kết quả của A. Khoản nạp năm mươi của A biến mất."""),
        st(svg(1500, 420,
               box(60, 130, 260, 120, ["Luồng A", "giữ khoá"], C_GREEN, bold=True),
               box(560, 130, 380, 120, ["vùng găng", "đọc rồi ghi số dư"], C_AMBER, bold=True),
               box(1180, 130, 260, 120, ["Luồng B", "đang chờ"], C_GRAY),
               arrow(320, 190, 555, 190, "#16a34a"), arrow(1180, 190, 945, 190, "#6b7280", None, dash=True),
               txt(750, 330, "Chỉ một luồng vào vùng găng. Luồng kia chờ, rồi mới vào.", 28, "middle", "#1f2937", True)),
           """Khoá giải quyết chuyện đó. Luồng A giữ khoá và vào vùng găng, nơi đọc rồi ghi số dư. Luồng B tới sau, thấy khoá đang bị giữ, nên đứng chờ.
           Khi A xong, B mới vào. Hai việc chạy lần lượt, nên kết quả luôn đúng."""),
        st(svg(1500, 440,
               panel(40, 30, 700, 380, "Luồng nền: 200 luồng", C_AMBER),
               box(80, 110, 160, 60, "chờ", C_GRAY), box(260, 110, 160, 60, "chờ", C_GRAY), box(440, 110, 160, 60, "chờ", C_GRAY),
               box(80, 200, 160, 60, "chờ", C_GRAY), box(260, 200, 160, 60, "chờ", C_GRAY), box(440, 200, 160, 60, "chờ", C_GRAY),
               txt(390, 330, "200 luồng đều đứng chờ → yêu cầu thứ 201 xếp hàng", 24, "middle", "#dc2626", True),
               panel(780, 30, 680, 380, "Luồng ảo: 10 000 luồng", C_GREEN),
               box(820, 110, 600, 70, "luồng ảo chờ → nhả luồng nền", C_BLUE),
               box(820, 210, 600, 70, "luồng nền đi chạy việc khác", C_GREEN),
               arrow(1120, 180, 1120, 205, "#475569"),
               txt(1120, 340, "chờ không giữ chân luồng nền", 24, "middle", "#16a34a", True)),
           """Hình thứ ba so sánh hai cách xử lý việc chờ. Bên trái, mỗi yêu cầu giữ một luồng nền trong lúc chờ. Hai trăm luồng đều đứng chờ, nên yêu cầu thứ hai trăm lẻ một phải xếp hàng.
           Bên phải, luồng ảo khi chờ sẽ nhả luồng nền ra, để luồng nền đi chạy việc khác. Nhờ vậy mười nghìn luồng ảo cùng chờ cũng không cạn."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: bao nhiêu kết quả có thể xảy ra?", [
        st("""<p><b>Bước 1.</b> Mỗi luồng gồm hai việc nhỏ, <b>đọc</b> rồi <b>ghi</b>, và việc ghi luôn sau việc đọc của cùng luồng.</p>
<span class='note'>Làm thử: hai luồng thì có $2 \\cdot 2 = 4$ việc nhỏ.</span>""",
           """Bước một, vì mỗi luồng gồm hai việc nhỏ là đọc rồi ghi, và việc ghi luôn sau việc đọc của cùng luồng, nên hai luồng có bốn việc nhỏ.
           Làm thử, hai nhân hai bằng bốn.""",
           introduces=["cdot"]),
        st("""<p><b>Bước 2.</b> Cách xếp bốn việc vào bốn ô, giữ thứ tự trong từng luồng, bằng số cách chọn hai ô cho luồng A.</p>
<span class='note'>Làm thử: ô đầu của A có $4$ chỗ, ô sau còn $3$, được $4 \\cdot 3$; đổi chỗ hai ô vẫn là một cách chọn nên chia $2 \\cdot 1$: $\\frac{4 \\cdot 3}{2 \\cdot 1} = 6$ cách.</span>""",
           """Bước hai, vì thứ tự trong từng luồng được giữ, nên số cách xếp bằng số cách chọn hai ô trong bốn ô cho luồng A.
           Làm thử, ô thứ nhất của A có bốn chỗ, ô thứ hai còn ba chỗ, nhưng đổi chỗ hai ô vẫn là cùng một cách chọn, nên bốn nhân ba chia hai nhân một bằng sáu cách."""),
        st("""<p><b>Bước 3.</b> Chạy thử cả sáu cách: hai cách cho $180$, hai cách cho $130$, hai cách cho $150$.</p>
<span class='note'>Chỉ đúng khi một luồng xong cả đọc lẫn ghi rồi luồng kia mới đọc.</span>""",
           """Bước ba, ta chạy thử cả sáu cách. Hai cách cho kết quả một trăm tám mươi, hai cách cho một trăm ba mươi, hai cách cho một trăm năm mươi.
           Kết quả chỉ đúng khi một luồng xong cả đọc lẫn ghi rồi luồng kia mới đọc.
           Vì vậy mới có lúc đúng lúc sai, và rất khó thấy khi kiểm thử."""),
    ], checks=["2 * 2 == 4", "math.comb(4, 2) == 6 == len(set(__import__('itertools').permutations([0, 0, 1, 1])))",
               "alg.bnk_lost_update(100, [50, 30]) == [130, 150, 180]"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Chạy A đọc, B đọc, A ghi, B ghi, với số dư đầu $100$.</p>
$$① \\; \\text{A đọc } 100,\\ \\text{B đọc } 100$$""",
           """Ta theo dõi cách xen kẽ xấu. Phép tính thứ nhất, A đọc được một trăm, và B cũng đọc được một trăm, vì chưa ai ghi."""),
        st("""$$② \\; \\text{A ghi } 100 + 50 = \\hl{150}$$""",
           """Phép tính thứ hai, A ghi giá trị đã đọc cộng năm mươi, là một trăm năm mươi."""),
        st("""$$③ \\; \\text{B ghi } 100 + 30 = \\hl{130}$$""",
           """Phép tính thứ ba, B ghi giá trị mà B đã đọc, một trăm, cộng ba mươi, là một trăm ba mươi, và nó đè lên kết quả của A."""),
        st("""$$④ \\; 180 - 130 = \\hl{50}\\ \\text{đã mất}$$""",
           """Phép tính thứ tư, kết quả đúng là một trăm tám mươi, thực tế còn một trăm ba mươi, nên mất đúng năm mươi, chính là khoản nạp của A."""),
        st("""$$⑤ \\; \\text{có khoá: } 100 + 50 + 30 = \\hlg{180}$$""",
           """Phép tính thứ năm, khi có khoá, hai việc chạy lần lượt, nên luôn ra một trăm tám mươi."""),
    ], checks=["100 + 50 == 150", "100 + 30 == 130", "180 - 130 == 50", "alg.bnk_lost_update(100, [50, 30])[-1] == 100 + 50 + 30"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: luồng ảo nhanh hơn bao nhiêu?", [
        st("""<p>Mười nghìn yêu cầu, mỗi yêu cầu chờ $0{,}1$ giây. Với $200$ luồng nền:</p>
<p>Vì mỗi lượt xử lý được $200$ yêu cầu, nên cần $\\frac{10\\,000}{200} = 50$ lượt:</p>
$$50 \\cdot 0{,}1 = \\hl{5}\\ \\text{giây}$$""",
           """Giờ so thời gian xử lý. Mười nghìn yêu cầu, mỗi yêu cầu chờ không phẩy một giây. Vì mỗi lượt xử lý được hai trăm yêu cầu, nên cần năm mươi lượt.
           Năm mươi nhân không phẩy một bằng năm giây."""),
        st(table(["cách tính", "kết quả"],
                 [["theo lô: 50 lô × 0,1 giây", "5 giây"],
                  ["theo thông lượng: 200 ÷ 0,1 = 2000 yêu cầu mỗi giây, 10 000 ÷ 2000", "5 giây"],
                  ["luồng ảo (mô hình lý tưởng): tất cả chờ cùng lúc", "0,1 giây"]]),
           """Kiểm bằng đường khác. Thông lượng là hai trăm chia không phẩy một, bằng hai nghìn yêu cầu mỗi giây, nên mười nghìn yêu cầu mất năm giây, khớp với cách tính theo lô.
           Luồng ảo, trong mô hình lý tưởng bỏ qua chi phí CPU, chờ tất cả cùng lúc nên chỉ mất không phẩy một giây."""),
    ], checks=["alg.bnk_batch_time(10000, 200, 0.1) == 5.0", "abs(10000 / (200 / 0.1) - 5.0) < 1e-9", "alg.bnk_batch_time(10000, 10000, 0.1) == 0.1"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ rằng <code>soDu += 50</code> là một việc không thể chia nhỏ. Thực ra nó là <b>đọc, cộng, ghi</b>: ba việc,
nên luồng khác chen vào được.</div>""",
           """Lỗi thứ nhất, của người mới. Nghĩ rằng một câu lệnh cộng thêm năm mươi là một việc không chia nhỏ được.
           Thực ra nó gồm đọc, cộng và ghi, nên luồng khác chen vào được."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Giữ khoá khi gọi mạng.</b> Khoá bao cả lời gọi sang đối tác mất $300$ ms
thì mọi luồng khác chờ $300$ ms theo. Khoá chỉ nên bao đoạn đọc rồi ghi ngắn.<br><span class="note">Phép thử: đo thời gian giữ khoá.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là giữ khoá khi gọi mạng. Nếu khoá bao cả lời gọi sang đối tác mất ba trăm mili giây,
           mọi luồng khác phải chờ ba trăm mili giây theo. Khoá chỉ nên bao đoạn đọc rồi ghi ngắn, và hãy đo thời gian giữ khoá."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nghĩ luồng ảo làm CPU chạy nhanh hơn. Nó chỉ giúp việc <b>chờ</b>.
<code>synchronized</code> là từ khoá Java bọc một khối mã bằng khoá, mỗi lúc chỉ một luồng vào.
Ở Java 21, chờ bên trong khối <code>synchronized</code> có thể <b>ghim</b> luồng ảo vào luồng nền (luồng nền bị giữ chân), mất lợi ích.
Từ Java 24 (JEP 491, một bản đề xuất tính năng chính thức của Java), <code>synchronized</code> không còn ghim; gọi mã native (mã máy viết ngoài Java) vẫn ghim.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là nghĩ luồng ảo làm CPU chạy nhanh hơn. Nó chỉ giúp những việc phải chờ.
           Khối đồng bộ là một từ khoá của Java, bọc một đoạn mã bằng khoá để mỗi lúc chỉ một luồng vào.
           Ở Java hai mươi mốt, chờ bên trong khối đồng bộ có thể ghim luồng ảo vào luồng nền, tức là giữ chân luồng nền, nên mất lợi ích.
           Từ Java hai mươi tư, khối đồng bộ không còn ghim, nhưng gọi mã máy gốc viết ngoài Java vẫn ghim."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Ba luồng, mỗi luồng đọc rồi ghi. Có bao nhiêu cách xen kẽ?"],
                  ["2", "2000 yêu cầu, mỗi yêu cầu chờ 0,2 giây, 50 luồng nền. Mất bao lâu?"],
                  ["3", "Quyết định: dịch vụ gọi đối tác chậm 300 ms, hàng nghìn yêu cầu cùng lúc. Chọn gì?"]]),
           """Đến lượt bạn. Câu một, ba luồng, mỗi luồng đọc rồi ghi, có bao nhiêu cách xen kẽ? Câu hai, hai nghìn yêu cầu, mỗi yêu cầu chờ không phẩy hai giây, năm mươi luồng nền, mất bao lâu?
           Câu ba, dịch vụ gọi đối tác chậm ba trăm mili giây, hàng nghìn yêu cầu cùng lúc, bạn chọn gì? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Xếp $6$ việc vào $6$ ô: ô đầu có $6$ cách chọn việc, ô hai $5$ cách, …: $6 \\cdot 5 \\cdot 4 \\cdot 3 \\cdot 2 \\cdot 1 = 720$ thứ tự. Hai việc của mỗi luồng có $2$ cách đứng trước sau mà chỉ $1$ cách hợp lệ (đọc trước ghi sau), nên chia cho $2 \\cdot 2 \\cdot 2 = 8$.</p>
$$\\frac{720}{8} = \\hl{90}$$""",
           """Đáp án câu một. Xếp sáu việc vào sáu ô, ô đầu có sáu cách chọn, ô hai có năm cách, cứ thế được bảy trăm hai mươi thứ tự. Vì hai việc của mỗi luồng có hai cách đứng trước sau mà chỉ một cách hợp lệ, là đọc trước ghi sau, nên ta chia cho hai nhân hai nhân hai, là tám.
           Kết quả là chín mươi cách."""),
        st("""$$\\frac{2000}{50} \\cdot 0{,}2 = 40 \\cdot 0{,}2 = \\hlg{8}\\ \\text{giây}$$""",
           """Đáp án câu hai. Hai nghìn chia năm mươi bằng bốn mươi lượt, nhân không phẩy hai, được tám giây."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["tăng số luồng nền lên rất lớn", "không phải sửa mã", "tốn bộ nhớ, hệ điều hành chuyển luồng nặng"],
                  ["luồng ảo (Java 21)", "chờ gần như miễn phí, mã vẫn viết tuần tự", "tránh chỗ gây ghim (Java 21: chờ trong synchronized; mã native); đo trước khi tin"]]),
           """Đáp án câu ba là một đánh đổi. Tăng số luồng nền thì không sửa mã nhưng tốn bộ nhớ. Luồng ảo cho phép chờ gần như miễn phí mà mã vẫn viết tuần tự, nhưng phải tránh ghim và phải đo."""),
    ], checks=["len(set(__import__('itertools').permutations([0, 0, 1, 1, 2, 2]))) == 90 == 720 // 8",
               "6 * 5 * 4 * 3 * 2 * 1 == 720 == math.factorial(6) and 2 * 2 * 2 == 8",
               "alg.bnk_batch_time(2000, 50, 0.2) == 8.0"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("đọc – ghi chen nhau", "mất cập nhật", "khoá vùng găng ngắn", "luồng ảo cho việc chờ"),
           """Tổng kết chuỗi logic. Đọc và ghi chen nhau gây mất cập nhật. Khoá một vùng găng ngắn sửa chuyện đó. Còn luồng ảo giải quyết việc chờ mạng quá nhiều."""),
        st("""<div class='box key'><b>Tư duy:</b> lỗi tranh chấp không hiện mỗi lần chạy, nên phải <b>suy luận</b> mọi cách xen kẽ chứ đừng chỉ chạy thử.
Khoá bao ít nhất có thể; luồng ảo là cho chờ, không phải cho tính toán.</div>""",
           """Điều cần mang theo. Lỗi tranh chấp không hiện mỗi lần chạy, nên phải suy luận mọi cách xen kẽ chứ đừng chỉ chạy thử.
           Khoá bao ít nhất có thể, và luồng ảo là để chờ, không phải để tính toán."""),
    ])
    # ── AF2: P1 tại chỗ, mã chạy thật, quy mô, tự làm ──
    add_steps([pre], "prereq", [
        st(table(["thêm ba điều", "nghĩa", "ví dụ"],
                 [["④ Máy chủ và yêu cầu", "máy chủ là chương trình chạy liên tục, chờ máy khách (ứng dụng điện thoại, chương trình khác) gửi <b>yêu cầu</b>; mỗi yêu cầu được xử lý rồi trả lời", "yêu cầu “chuyển 500 000 đồng”"],
                  ["⑤ Đối tác", "hệ thống bên ngoài mà dịch vụ phải gọi qua mạng; trả lời chậm, cỡ hàng trăm mili giây", "cổng thanh toán của đối tác"],
                  ["⑥ Cú pháp luồng trong Java", "<code>new Thread(việc)</code> tạo luồng; <code>start()</code> cho chạy; <code>join()</code> chờ luồng xong; <code>() -> { … }</code> viết gọn một việc", "<code>Runnable viec = () -> { … };</code>"]]),
           """Thêm ba điều nữa. Máy chủ là chương trình chạy liên tục, chờ máy khách gửi yêu cầu, mỗi yêu cầu được xử lý rồi trả lời. Đối tác là hệ thống bên ngoài mà dịch vụ phải gọi qua mạng, và nó trả lời khá chậm, cỡ hàng trăm mili giây.
           Cuối cùng là cú pháp luồng trong Java. Tạo luồng thì đưa cho nó một việc, lệnh bắt đầu cho luồng chạy, lệnh chờ cho luồng xong, và mũi tên với cặp ngoặc nhọn là cách viết gọn một việc.""", clear=True),
    ], at=1)
    pre["title"] = "Trước hết: sáu điều cần hiểu"
    run = sc("chay_that", "example", "Chạy thật: mất cập nhật, khoá, luồng ảo", [
        st(code_block(mat, lines=(2, 9), title="Tệp MatCapNhat.java (phần chính)"),
           """Ta chạy thật hai luồng cùng cộng vào một biến dùng chung. Mỗi luồng làm cùng một việc là cộng thêm một, một triệu lần.
           Lệnh bắt đầu cho cả hai luồng chạy, rồi lệnh chờ đợi cả hai xong, và ta kiểm xem tổng có đúng hai triệu không."""),
        st(out_block(mat),
           """Chạy thật in ra không đúng. Vì cộng thêm một thực ra là đọc, cộng, rồi ghi, nên hai luồng hay đọc cùng một số rồi ghi đè nhau, mất những lần cộng.
           Con số mất cụ thể thay đổi từng lần chạy, nên ta chỉ in đúng hay sai.""", clear=True),
        st(code_block(co_khoa, lines=(2, 9), title="Tệp CoKhoa.java (phần chính): bọc phép cộng trong khối đồng bộ"),
           """Bây giờ ta bọc phép cộng vào một khối đồng bộ, dùng một đối tượng làm khoá. Mỗi lúc chỉ một luồng được vào khối đó, luồng kia chờ ở cửa.""",
           clear=True),
        st(out_block(co_khoa),
           """Chạy thật in đúng. Vì hai luồng vào khối lần lượt, nên không còn chuyện đọc chen vào giữa, và tổng đúng hai triệu.""", clear=True),
        st(code_block(luong_ao, lines=(5, 12), title="Tệp LuongAo.java (phần chính): mười nghìn việc, mỗi việc chờ một phần mười giây"),
           """Còn đây là cách chạy bằng luồng ảo của Java hai mươi mốt. Bộ phân việc này tạo mỗi việc một luồng ảo. Mỗi việc chỉ ngủ một phần mười giây, giả làm đang chờ đối tác, rồi tăng một biến đếm an toàn khi nhiều luồng cùng tăng.
           Ta đo tổng thời gian, và hỏi có dưới hai giây không.""", clear=True),
        st(out_block(luong_ao),
           """Chạy thật cho thấy mười nghìn việc xong, trong dưới hai giây. Nếu chỉ có hai trăm luồng nền, ta đã tính được là mất năm giây, vì mỗi luồng ảo khi chờ nhả luồng chạy cho việc khác.
           Kết quả này đúng khi máy không quá tải.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: tải tăng ×100 và ×10 000, giải pháp nào gãy?", [
        st("""<p>Mỗi yêu cầu chờ đối tác $0{,}1$ giây; có $200$ luồng nền; ngăn xếp mỗi luồng nền thường cỡ $1$ MB (tuỳ hệ điều hành); luồng ảo cỡ $1$ KB <i>(số minh hoạ)</i>.</p>"""
           + table(["tải", "yêu cầu chờ cùng lúc", "200 luồng nền: thời gian", "một luồng nền mỗi yêu cầu: bộ nhớ", "luồng ảo: bộ nhớ"],
                   [["×1", "10 000", "5 giây", "10 000 MB ≈ 10 GB", "10 000 KB ≈ 10 MB"],
                    ["×100", "1 000 000", "500 giây ≈ <b>8,3 phút</b>", "1 000 000 MB ≈ <b>1 TB</b>", "≈ 1 GB"],
                    ["×10 000", "100 000 000", "50 000 giây ≈ <b>13,9 giờ</b>", "≈ <b>100 TB</b>", "≈ <b>100 GB</b>"]]),
           """Giả sử mỗi yêu cầu chờ đối tác không phẩy một giây, có hai trăm luồng nền, ngăn xếp mỗi luồng nền cỡ một mê ga byte, luồng ảo cỡ một ki lô byte. Đây là số minh hoạ.
           Với mười nghìn yêu cầu chờ cùng lúc, hai trăm luồng nền mất năm giây. Tải tăng một trăm lần thì mất tám phẩy ba phút, và tăng mười nghìn lần thì mất mười ba phẩy chín giờ.
           Nếu cho mỗi yêu cầu một luồng nền, bộ nhớ ngăn xếp lên tới một nghìn tỉ byte ở tải gấp trăm lần. Luồng ảo kéo con số đó xuống khoảng một nghìn mê ga byte.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Tăng số luồng nền: ở ×1 còn chạy được, ở ×100 một luồng mỗi yêu cầu cần cỡ 1 TB bộ nhớ, không máy nào có. Giữ 200 luồng thì mất 8,3 phút, người dùng bỏ đi.
<b>Luồng ảo</b> kéo bộ nhớ xuống cỡ 1 GB, nhưng ở ×10 000 vẫn cần cỡ 100 GB: cũng gãy.</div>
<div class="box key"><b>Đánh đổi người làm nghề chọn:</b> luồng ảo cho việc <b>chờ</b>; nếu việc là tính toán thì số lõi CPU mới là giới hạn. Ở quy mô cực lớn, phải <b>giới hạn số yêu cầu đồng thời</b> và <b>chia ra nhiều máy</b>.</div>""",
           """Giải pháp cũ là tăng số luồng nền. Ở tải gốc còn chạy được, nhưng ở tải gấp trăm lần, mỗi yêu cầu một luồng cần cỡ một nghìn tỉ byte bộ nhớ, không máy nào có. Còn giữ hai trăm luồng thì mất tám phút, người dùng đã bỏ đi.
           Luồng ảo kéo bộ nhớ xuống cỡ một nghìn mê ga byte, nhưng ở tải gấp mười nghìn lần vẫn cần cỡ một trăm nghìn mê ga byte, nên cũng gãy.
           Đánh đổi là luồng ảo chỉ giúp việc chờ. Nếu việc là tính toán thì số lõi bộ xử lý mới là giới hạn, và ở quy mô cực lớn phải giới hạn số yêu cầu đồng thời rồi chia ra nhiều máy.""", clear=True),
    ], checks=["10000 / 200 * 0.1 == 5.0", "1000000 / 200 * 0.1 == 500.0", "round(500 / 60, 1) == 8.3", "100000000 / 200 * 0.1 == 50000.0",
               "round(50000 / 3600, 1) == 13.9", "10000 * 1 == 10000", "1000000 * 1 == 10**6 and 100000000 * 1 == 10**8"])
    write_lab("BNK", "L01", """# Lab BNK L01 — Ba luồng cộng chung một tổng

Ba luồng, **mỗi luồng cộng 1 vào biến chung `tong` đúng 200 000 lần**. Tổng đúng phải là 600 000.

Viết chương trình `TongBaLuong` (tệp `TongBaLuong.java`):
1. Biến chung `static long tong = 0;` và một đối tượng khoá `static final Object KHOA = new Object();`.
2. Một việc `Runnable` cộng 200 000 lần, **mỗi lần cộng bọc trong** `synchronized (KHOA) { … }`.
3. Tạo ba luồng cho cùng việc đó, `start()` cả ba rồi `join()` cả ba.
4. In đúng một dòng: `tong = 600000`.

Chạy: `javac TongBaLuong.java && java TongBaLuong`. Chấm: `bash labs/cham.sh BNK L01 TongBaLuong.java`.
""", "java", lab_khoa["code"], lab_khoa["out"])
    lab = practice_scene(sc, "Tự làm: ba luồng cộng chung một tổng", practice_steps(
        st, "BNK", "L01",
        """<p><b>Đề</b>: ba luồng, mỗi luồng cộng 1 vào biến chung <code>tong</code> đúng 200 000 lần. Viết <code>TongBaLuong.java</code>:</p>
<ol><li>biến chung <code>static long tong</code> và đối tượng khoá <code>KHOA</code></li>
<li>mỗi lần cộng bọc trong <code>synchronized (KHOA) { … }</code></li>
<li>tạo ba luồng, <code>start()</code> cả ba, <code>join()</code> cả ba</li>
<li>in một dòng <code>tong = …</code></li></ol>""",
        """Bây giờ tới phần bạn tự làm. Ba luồng, mỗi luồng cộng một vào một biến chung đúng hai trăm nghìn lần. Hãy bọc mỗi lần cộng trong khối đồng bộ với một đối tượng khoá.
        Tạo ba luồng, cho cả ba chạy, rồi chờ cả ba xong, và in tổng. Hãy dừng video, tự viết và chạy, đừng chép lại ví dụ.""",
        lab_khoa["out"], "TongBaLuong.java",
        """<div class="box key"><b>Nếu kẹt:</b> làm theo mẫu <code>CoKhoa</code>: <code>Runnable viec = () -&gt; { for (…) { synchronized (KHOA) { tong++; } } };</code>, rồi
<code>Thread[] ds = { new Thread(viec), new Thread(viec), new Thread(viec) };</code> và hai vòng <code>for</code> gọi <code>start()</code>, <code>join()</code>.
Lời giải ở <code>labs/BNK/L01/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, làm theo mẫu khoá vừa xem. Viết một việc có vòng lặp, mỗi lần cộng bọc trong khối đồng bộ. Rồi tạo mảng ba luồng cùng việc, và hai vòng lặp, một vòng cho chạy và một vòng chờ xong.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=120), "BNK", "L01")
    return lesson("L01", "da_luong_khoa_luong_ao", "Bài 1 — Đa luồng, khoá và luồng ảo Java 21",
                  "curriculum/bnk.yaml L01; audit/bnk/verify_bnk.py L01; audit/review/screen_code/BNK.yaml (mã chạy thật bằng JDK 21); JEP 444 Virtual Threads (JDK 21: ghim khi chờ trong synchronized hoặc native); JEP 491 Synchronize Virtual Threads without Pinning (JDK 24); Goetz et al., Java Concurrency in Practice; Java SE 21 API: Executors.newVirtualThreadPerTaskExecutor, AtomicInteger; The java Command (-Xss: ngăn xếp luồng mặc định phụ thuộc nền tảng, thường 1 MB)",
                  ["Liệt kê mọi cách xen kẽ của hai luồng và nhận ra mất cập nhật", "Giải thích khoá làm các luồng chạy lần lượt",
                   "Tính thời gian xử lý theo lô và so với luồng ảo", "Chọn giữa tăng luồng nền và luồng ảo khi tải tăng ×100 và ×10 000",
                   "Viết mã dùng khoá để nhiều luồng cộng chung một tổng mà không mất cập nhật"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "formula"), (2, "chay_that"), (3, "check"), (4, "quy_mo"), (5, "practice")])
