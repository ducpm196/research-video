from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    bo_dem = prog("BoDem", """
import java.util.*;
public class BoDem {
    static Map<Integer, Long> boDem = new HashMap<>();   // giả lập Redis: khoá tra cứu -> số dư
    static long tong = 0;
    static int trung = 0;
    static long soDu(int tk) {
        if (boDem.containsKey(tk)) { trung++; tong += 1; return boDem.get(tk); }   // trúng: 1 ms
        tong += 1 + 20;   // trượt: 1 ms bộ đệm + 20 ms cơ sở dữ liệu
        long v = tk * 1000L;   // giả lập đọc từ cơ sở dữ liệu
        boDem.put(tk, v);   // nạp vào bộ đệm
        return v;
    }
    public static void main(String[] args) {
        for (int i = 0; i < 100; i++) soDu(i % 10);   // 100 lần hỏi, 10 tài khoản
        System.out.println("trung " + trung + "/100, trung binh " + tong / 100.0 + " ms");
    }
}""", out="trung 90/100, trung binh 3.0 ms")
    ma_chan = prog("MaChan", """
public class MaChan {
    static long maCuoi = 0;
    static String giaTri = "";
    static boolean ghi(long ma, String v) {
        if (ma < maCuoi) return false;                   // từ chối mã chặn cũ
        maCuoi = ma;
        giaTri = v;
        return true;
    }
    public static void main(String[] args) {
        System.out.println("B ghi (ma 34): " + ghi(34, "B"));              // B lấy khoá sau, mã 34
        System.out.println("A tinh day ghi (ma 33): " + ghi(33, "A"));     // A tạm dừng rồi ghi muộn
        System.out.println("gia tri cuoi: " + giaTri);
    }
}""", out="""B ghi (ma 34): true
A tinh day ghi (ma 33): false
gia tri cuoi: B""")
    lab_dem = prog("BoDemNho", """
import java.util.*;
public class BoDemNho {
    static Map<Integer, Long> boDem = new HashMap<>();
    static long tong = 0;
    static int trung = 0;
    static long soDu(int tk) {
        if (boDem.containsKey(tk)) { trung++; tong += 2; return boDem.get(tk); }
        tong += 2 + 30;
        long v = tk * 1000L;
        boDem.put(tk, v);
        return v;
    }
    public static void main(String[] args) {
        for (int i = 0; i < 40; i++) soDu(i % 4);
        System.out.println("trung " + trung + "/40, trung binh " + tong / 40.0 + " ms");
    }
}""", out="trung 36/40, trung binh 5.0 ms")
    hook = sc("hook", "hook", "Vì sao bộ đệm làm nhanh gấp nhiều lần, và vì sao khoá phân tán vẫn có thể sai?", [
        st("""<p>Mỗi lần tra số dư mất $20$ ms ở cơ sở dữ liệu <i>(số minh hoạ)</i>. Có bộ đệm mất $1$ ms mỗi lần hỏi, với tỉ lệ trúng $90\\%$, trung bình chỉ còn khoảng <b>3 ms</b>.</p>
<div class="box key">Nhưng một khoá phân tán có hạn <b>10 giây</b> vẫn có thể bị <b>hai người cùng giữ</b> nếu một người bị tạm dừng.</div>""",
           """Giả sử mỗi lần tra số dư mất hai mươi mili giây ở cơ sở dữ liệu, đây là số minh hoạ. Có bộ đệm mất một mili giây mỗi lần hỏi, với tỉ lệ trúng chín mươi phần trăm, trung bình chỉ còn khoảng ba mili giây.
           Nhưng một khoá phân tán có hạn mười giây vẫn có thể bị hai người cùng giữ, nếu một người bị tạm dừng."""),
        st(table(["ý hỏi", "bài này trả lời"],
                 [["bộ đệm nhanh hơn bao nhiêu", "độ trễ trung bình = tđệm + (1 − tỉ lệ trúng) × tcsdl"],
                  ["khoá có hạn sai ở đâu", "người giữ khoá bị tạm dừng quá hạn rồi vẫn ghi"],
                  ["chữa thế nào", "mã chặn tăng dần, kho dữ liệu được ghi từ chối mã cũ"]]),
           """Hôm nay ta trả lời ba câu: bộ đệm nhanh hơn bao nhiêu, khoá có hạn sai ở đâu, và cách chữa bằng mã chặn tăng dần để kho dữ liệu từ chối mã cũ."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: những điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Bộ đệm (cache)", "nơi giữ tạm một bản sao dữ liệu ở chỗ đọc nhanh, để khỏi hỏi nơi gốc chậm hơn", "bản sao số dư trong bộ nhớ"],
                  ["② Redis", "một kho “tên tra cứu → giá trị” chạy trong bộ nhớ, hay dùng làm bộ đệm", "tên <code>so_du:42</code> → giá trị 1500000"],
                  ["③ Hai nghĩa của “khoá”", "khoá tra cứu (key): cái tên để tìm giá trị; khoá giữ quyền (lock): ai giữ thì được làm, người khác phải chờ", "key <code>so_du:42</code>; lock trên tài khoản 42"]]),
           """Trước hết ta cần hiểu vài điều. Bộ đệm là nơi giữ tạm một bản sao dữ liệu ở chỗ đọc nhanh, để khỏi phải hỏi nơi gốc chậm hơn.
           Redis là một kho tên tra cứu và giá trị chạy trong bộ nhớ, hay được dùng làm bộ đệm. 
           Chú ý chữ khoá có hai nghĩa. Khoá tra cứu là cái tên để tìm giá trị. Còn khoá giữ quyền thì ai giữ được làm việc, người khác phải chờ."""),
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["⑥ Khoá phân tán", "khoá giữ quyền dùng chung giữa nhiều máy chủ, đặt ở một nơi lưu chung như Redis", "hai máy chủ cùng muốn sửa tài khoản 42"],
                  ["⑦ Hết hạn (TTL)", "mỗi mục tự biến mất sau một thời gian", "hạn 60 giây"],
                  ["⑧ Độ trễ", "thời gian từ lúc hỏi tới lúc có đáp; đo bằng mili giây (ms), mỗi ms là một phần nghìn giây", "bộ đệm 1 ms, cơ sở dữ liệu 20 ms (số minh hoạ)"]]),
           """Khoá phân tán là khoá giữ quyền dùng chung giữa nhiều máy chủ, đặt ở một nơi lưu chung như Redis. Mỗi mục trong kho có thể tự hết hạn sau một thời gian.
           Độ trễ là thời gian từ lúc hỏi tới lúc có đáp, đo bằng mili giây, mỗi mili giây là một phần nghìn giây. Ví dụ minh hoạ là bộ đệm một mili giây, cơ sở dữ liệu hai mươi mili giây.""", clear=True),
        st("""$$0{,}9 + 0{,}1 = 1$$""",
           """Một phép kiểm nhỏ. Tỉ lệ trúng cộng tỉ lệ trượt luôn bằng một. Không phẩy chín cộng không phẩy một bằng một."""),
    ], checks=["abs(0.9 + 0.1 - 1) < 1e-12"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["cache-aside", "hỏi bộ đệm trước; trượt thì hỏi cơ sở dữ liệu rồi nạp vào bộ đệm"],
                  ["hit / miss", "trúng bộ đệm / trượt bộ đệm"],
                  ["TTL", "thời gian sống của một mục trước khi tự xoá"],
                  ["SET key value NX PX 10000", "lệnh Redis đặt khoá chỉ khi chưa có (NX), hết hạn sau 10 000 mili giây (PX)"],
                  ["fencing token (mã chặn)", "số tăng dần cấp kèm mỗi lần giữ khoá, kho dữ liệu được ghi dùng để từ chối người cũ; lệnh SET NX PX (và cả thuật toán Redlock dùng nhiều máy Redis) không tự cấp, phải lấy từ một bộ đếm tăng dần"],
                  ["nhả khoá", "so giá trị mình đã đặt rồi mới xoá, gộp thành một bước không chen được (Redis chạy một đoạn lệnh nhỏ); không xoá thẳng"]]),
           """Kiểu hỏi bộ đệm trước, trượt thì hỏi cơ sở dữ liệu rồi nạp vào bộ đệm. Trúng là có trong bộ đệm, trượt là không có.
           Thời gian sống là hạn tự xoá của mỗi mục. Lệnh đặt khoá có hai tuỳ chọn, chỉ đặt khi chưa có, và tự hết hạn. Mã chặn là số tăng dần để kho dữ liệu được ghi từ chối người giữ khoá cũ.
           Lệnh đặt khoá không tự cấp mã chặn, nên phải lấy từ một bộ đếm tăng dần. Cuối cùng, khi nhả khoá, phải so giá trị mình đã đặt rồi mới xoá, gộp thành một bước không ai chen vào được, để không xoá nhầm khoá của người khác."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: bộ đệm và khoá hết hạn", [
        st(svg(1500, 400,
               box(40, 150, 220, 100, ["Dịch vụ", "tra số dư"], C_BLUE, bold=True),
               box(560, 40, 380, 100, ["Redis (bộ đệm)", "1 ms"], C_AMBER, bold=True),
               box(560, 260, 380, 100, ["Cơ sở dữ liệu", "20 ms"], C_GREEN, bold=True),
               arrow(260, 180, 555, 100, "#2a78d6", "1. hỏi"),
               arrow(1000, 90, 1100, 90, "#16a34a", "trúng → trả"),
               arrow(260, 220, 555, 300, "#2a78d6"), txt(40, 320, "2. trượt → hỏi tiếp", 22, "start", "#2a78d6", halo=True),
               arrow(945, 330, 1100, 330, "#475569", None), txt(1250, 100, "90 trong 100 lần", 26, "middle", "#16a34a", True),
               txt(1250, 340, "10 trong 100 lần", 26, "middle", "#d97706", True)),
           """Hình cho thấy kiểu hỏi bộ đệm trước. Dịch vụ hỏi Redis trước. Nếu trúng thì trả luôn, chỉ mất một mili giây, và đó là chín mươi trong một trăm lần.
           Nếu trượt thì hỏi tiếp cơ sở dữ liệu, mất thêm hai mươi mili giây, và đó là mười trong một trăm lần."""),
        st(svg(1500, 460,
               txt(60, 50, "Giây", 24, "start", "#475569"),
               box(120, 80, 520, 70, "A giữ khoá (mã chặn 1), hạn 10 giây", C_BLUE),
               box(640, 80, 280, 70, ["A tạm dừng…", "(ví dụ máy ngừng để dọn rác)"], C_GRAY, dash=True, size=20),
               box(740, 190, 420, 70, "giây 11: B giữ khoá (mã chặn 2)", C_AMBER),
               box(740, 290, 360, 70, "giây 11,5: B ghi", C_AMBER),
               box(1000, 80, 440, 70, "giây 12: A tỉnh dậy, vẫn ghi!", C_RED),
               txt(750, 420, "Khoá của A đã hết hạn từ giây 10, nhưng A không biết", 26, "middle", "#dc2626", True)),
           """Hình thứ hai cho thấy lỗi của khoá có hạn. A giữ khoá với hạn mười giây, rồi bị tạm dừng. Khoá hết hạn, B lấy khoá ở giây mười một và ghi lúc mười một phẩy năm.
           Đến giây mười hai A tỉnh dậy, không biết khoá đã hết, và vẫn ghi đè lên B."""),
        st(svg(1500, 400,
               box(60, 150, 260, 100, ["B ghi", "mã chặn 2"], C_AMBER, bold=True),
               box(60, 280, 260, 80, ["A ghi muộn", "mã chặn 1"], C_RED),
               box(620, 130, 420, 140, ["Kho dữ liệu được ghi", "nhớ mã chặn lớn nhất = 2"], C_GREEN, bold=True),
               arrow(320, 190, 615, 190, "#16a34a", "nhận"), arrow(320, 320, 615, 240, "#dc2626"), txt(335, 352, "1 < 2 → từ chối", 22, "start", "#dc2626", halo=True),
               txt(1260, 180, "Kho dữ liệu chặn người cũ", 26, "middle", "#1f2937", True),
               txt(1260, 220, "dù khoá đã hết hạn", 26, "middle", "#1f2937", True)),
           """Mã chặn chữa lỗi này. Một bộ đếm tăng dần cấp mã chặn mỗi khi có người giữ khoá. Kho dữ liệu được ghi, ví dụ cơ sở dữ liệu, mới là nơi kiểm, chứ không phải Redis. Nó nhớ mã chặn lớn nhất đã thấy, ở đây là hai.
           Khi A ghi muộn với mã chặn một, kho thấy một nhỏ hơn hai và từ chối. """),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: độ trễ trung bình và an toàn của khoá", [
        st("""<p><b>Bước 1.</b> Luôn hỏi bộ đệm: mọi lần tốn $c$ (thời gian bộ đệm, ở bảng đầu bài ghi là tđệm). Trượt (xác suất $1 - h$, với $h$ là tỉ lệ trúng) thì tốn thêm $d$ (thời gian cơ sở dữ liệu, ghi là tcsdl).</p>
<span class='note'>Làm thử: $h = 0{,}9$, $c = 1$, $d = 20$: trượt $0{,}1$ lần, mỗi lần thêm $20$ ms.</span>""",
           """Bước một, vì ta luôn hỏi bộ đệm trước, nên mọi lần đều tốn thời gian của bộ đệm, gọi là c, tức t đệm ở bảng đầu bài. Lần nào trượt, với xác suất một trừ h, trong đó h là tỉ lệ trúng, thì tốn thêm thời gian của cơ sở dữ liệu, gọi là d.
           Làm thử với h bằng không phẩy chín, mỗi lần trượt thêm hai mươi mili giây."""),
        st("""<p><b>Bước 2.</b> Vì mọi lần tốn $c$ và chỉ phần trượt tốn thêm $d$, nên gộp lại: $T = c + (1 - h) \\cdot d$.</p>
<span class='note'>Làm thử: $T = 1 + 0{,}1 \\cdot 20 = 3$ ms.</span>""",
           """Bước hai, vì mọi lần tốn thời gian bộ đệm và chỉ phần trượt tốn thêm, nên gộp lại, trung bình T bằng thời gian bộ đệm cộng, một trừ h, nhân thời gian cơ sở dữ liệu. Làm thử, một cộng không phẩy một nhân hai mươi bằng ba mili giây."""),
        st("""<p><b>Bước 3.</b> Khoá có hạn không bảo đảm “một người giữ”, vì người giữ có thể bị tạm dừng lâu hơn hạn. Kho dữ liệu được ghi phải kiểm <b>mã chặn</b> mới an toàn.</p>
<span class='note'>Làm thử: ghi mã 2 rồi mã 1 → kho dữ liệu nhận mã 2, từ chối mã 1.</span>""",
           """Bước ba, vì người giữ khoá có thể bị tạm dừng lâu hơn hạn, nên khoá có hạn không bảo đảm chỉ một người giữ. Kho dữ liệu được ghi phải kiểm mã chặn mới an toàn.
           Làm thử, ghi mã hai rồi mã một, kho dữ liệu nhận mã hai và từ chối mã một."""),
    ], checks=["abs(1 + (1 - 0.9) * 20 - 3) < 1e-9", "abs(alg.bnk_cache_avg(0.9, 1, 20) - 3) < 1e-9", "alg.bnk_fencing_sim(True) == ['B']"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Dùng $c = 1$ ms, $d = 20$ ms <i>(số minh hoạ)</i>.</p>
$$① \\; h = 0{,}9:\\quad T = 1 + 0{,}1 \\cdot 20 = \\hlg{3}\\ \\text{ms}$$""",
           """Dùng thời gian bộ đệm một mili giây và cơ sở dữ liệu hai mươi mili giây, đây là số minh hoạ. Phép tính thứ nhất, với h bằng không phẩy chín, T bằng một cộng không phẩy một nhân hai mươi, là ba mili giây."""),
        st("""$$② \\; h = 0{,}5:\\quad T = 1 + 0{,}5 \\cdot 20 = \\hl{11}\\ \\text{ms}$$""",
           """Phép tính thứ hai, với h bằng không phẩy năm, T bằng một cộng không phẩy năm nhân hai mươi, là mười một mili giây."""),
        st("""$$③ \\; \\text{không có bộ đệm: } T = \\hl{20}\\ \\text{ms}$$""",
           """Phép tính thứ ba, không có bộ đệm, mọi lần đều hỏi cơ sở dữ liệu, nên T bằng hai mươi mili giây."""),
        st("""<p>Dùng lại $T = 3$ ở ① và $20$ ở ③.</p>
$$④ \\; \\text{nhanh gấp} \\; \\frac{20}{3} \\approx \\hlg{6{,}7}\\ \\text{lần}$$""",
           """Phép tính thứ tư, nhanh gấp hai mươi chia ba, xấp xỉ sáu phẩy bảy lần."""),
        st("""<p>Khoá hạn $10$ giây, A tạm dừng tới giây $12$: quá hạn $12 - 10 = \\hl{2}$ giây.</p>
$$⑤ \\; \\text{không mã chặn: ghi cuối là A (đè B)};\\quad \\text{có mã chặn: ghi cuối là B}$$""",
           """Phép tính thứ năm, khoá hạn mười giây mà A tạm dừng tới giây mười hai, nên quá hạn hai giây. Không có mã chặn thì người ghi cuối là A, đè lên B. Có mã chặn thì người ghi cuối là B."""),
    ], checks=["abs(alg.bnk_cache_avg(0.9, 1, 20) - 3) < 1e-9", "abs(alg.bnk_cache_avg(0.5, 1, 20) - 11) < 1e-9", "abs(20 / 3 - 6.7) < 0.05",
               "12 - 10 == 2 and alg.bnk_fencing_sim(False)[-1] == 'A' and alg.bnk_fencing_sim(True)[-1] == 'B'"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: tính theo từng trường hợp", [
        st("""<p>Đường khác: vì mỗi trường hợp có độ trễ riêng, ta tính theo từng trường hợp thay vì công thức. Trong $100$ lần, $90$ lần trúng tốn $1$ ms, $10$ lần trượt tốn $1 + 20$ ms.</p>
$$\\frac{90 \\cdot 1 + 10 \\cdot 21}{100} = \\frac{300}{100} = \\hl{3}\\ \\text{ms}$$""",
           """Kiểm bằng đường khác. Thay vì dùng công thức, ta tính theo từng trường hợp. Trong một trăm lần, chín mươi lần trúng tốn một mili giây, mười lần trượt tốn hai mươi mốt mili giây.
           Cộng lại được ba trăm, nên chia một trăm bằng ba mili giây, khớp công thức."""),
        st(table(["tỉ lệ trúng", "độ trễ trung bình", "so với 20 ms"],
                 [["0,5", "11 ms", "nhanh 1,8 lần"], ["0,9", "3 ms", "nhanh 6,7 lần"], ["0,99", "1,2 ms", "nhanh 16,7 lần"]]),
           """ Vì phần trượt tốn nhiều nhất, nên từ không phẩy năm lên không phẩy chín chín, độ trễ giảm từ mười một xuống một phẩy hai mili giây."""),
    ], checks=["(90 * 1 + 10 * 21) / 100 == 3.0", "abs(alg.bnk_cache_avg(0.99, 1, 20) - 1.2) < 1e-9", "abs(20 / 1.2 - 16.7) < 0.05", "abs(20 / 11 - 1.8) < 0.05"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Lưu <b>số dư</b> trong bộ đệm rồi dùng nó để quyết định trừ tiền. Bộ đệm có thể cũ. Số dư thật để quyết định luôn đọc từ cơ sở dữ liệu nguồn.</div>""",
           """Lỗi thứ nhất, của người mới. Lưu số dư trong bộ đệm rồi dùng nó để quyết định trừ tiền. Bộ đệm có thể cũ. Số dư dùng để quyết định phải luôn đọc từ cơ sở dữ liệu nguồn."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Bộ đệm hết hạn cùng lúc</b>: nghìn khoá cùng hạn $60$ giây, đến giờ tất cả trượt, nghìn truy vấn đổ về cơ sở dữ liệu cùng lúc.
<br><span class="note">Cách chữa: cộng thêm một số ngẫu nhiên nhỏ vào hạn, và chỉ cho một yêu cầu nạp lại mỗi khoá.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là bộ đệm hết hạn cùng lúc. Hàng nghìn khoá cùng hạn sáu mươi giây, đến giờ tất cả trượt, nghìn truy vấn đổ về cơ sở dữ liệu cùng lúc.
           Cách chữa là cộng thêm một số ngẫu nhiên nhỏ vào hạn, và chỉ cho một yêu cầu nạp lại mỗi khoá."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tin khoá phân tán là đủ để bảo vệ việc ghi tiền. Khoá có hạn có thể bị hai người cùng giữ. Hãy để <b>cơ sở dữ liệu</b> chặn: ràng buộc duy nhất (cấm hai dòng trùng giá trị), hoặc cột phiên bản (mỗi lần sửa tăng 1; câu sửa chỉ thành công nếu phiên bản còn như lúc đọc).</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là tin khoá phân tán là đủ để bảo vệ việc ghi tiền. Khoá có hạn có thể bị hai người cùng giữ. Hãy để cơ sở dữ liệu chặn, bằng ràng buộc duy nhất, tức cấm hai dòng trùng giá trị.
           Hoặc dùng cột phiên bản. Mỗi lần sửa thì phiên bản tăng một, và câu sửa chỉ thành công nếu phiên bản vẫn còn như lúc đọc."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "tđệm = 2 ms, tcsdl = 30 ms, tỉ lệ trúng 0,8. Độ trễ trung bình?"],
                  ["2", "Nhanh hơn không có bộ đệm bao nhiêu lần?"],
                  ["3", "Quyết định: dùng khoá Redis để bảo vệ việc trừ tiền?"]]),
           """Đến lượt bạn. Câu một, thời gian bộ đệm hai mili giây, cơ sở dữ liệu ba mươi mili giây, tỉ lệ trúng không phẩy tám, độ trễ trung bình là bao nhiêu?
           Câu hai, nhanh hơn không có bộ đệm bao nhiêu lần? Câu ba, có nên dùng khoá Redis để bảo vệ việc trừ tiền không? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""$$T = 2 + 0{,}2 \\cdot 30 = 2 + 6 = \\hl{8}\\ \\text{ms}$$""",
           """Đáp án câu một. T bằng hai cộng không phẩy hai nhân ba mươi, bằng hai cộng sáu, là tám mili giây."""),
        st("""$$\\frac{30}{8} = \\hlg{3{,}75}\\ \\text{lần}$$""",
           """Đáp án câu hai. Ba mươi chia tám bằng ba phẩy bảy mươi lăm lần."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["chỉ khoá Redis", "nhanh, dễ viết", "khoá hết hạn có thể bị hai người cùng giữ, có thể trừ trùng"],
                  ["khoá Redis + ràng buộc / cột phiên bản ở cơ sở dữ liệu", "khoá giảm tranh chấp, cơ sở dữ liệu bảo đảm đúng", "thêm mã"]]),
           """Đáp án câu ba. Chỉ dùng khoá Redis thì nhanh nhưng có thể trừ trùng. Nên dùng khoá để giảm tranh chấp, và để cơ sở dữ liệu bảo đảm tính đúng bằng ràng buộc hoặc cột phiên bản."""),
    ], checks=["abs(alg.bnk_cache_avg(0.8, 2, 30) - 8) < 1e-9", "abs(30 / 8 - 3.75) < 1e-9"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("hỏi bộ đệm trước", "T = tđệm + (1 − h) × tcsdl", "khoá có hạn có thể quá hạn", "mã chặn + ràng buộc cơ sở dữ liệu"),
           """Tổng kết, hỏi bộ đệm trước, độ trễ trung bình là thời gian bộ đệm cộng tỉ lệ trượt nhân thời gian cơ sở dữ liệu. Khoá có hạn có thể quá hạn, nên cần mã chặn và ràng buộc ở cơ sở dữ liệu."""),
        st("""<div class='box key'><b>Tư duy:</b> bộ đệm là để <b>đọc nhanh</b>, không phải nguồn sự thật cho tiền.
Khoá phân tán là <b>tối ưu</b>; tính đúng đắn phải do cơ sở dữ liệu bảo đảm.</div>""",
           """Bộ đệm là để đọc nhanh, không phải nguồn sự thật cho tiền. Khoá phân tán là một tối ưu, còn tính đúng đắn phải do cơ sở dữ liệu bảo đảm."""),
    ])
    # ── AF2: P1 Map/mô phỏng, mô phỏng bộ đệm và mã chặn bằng Java, quy mô, tự làm ──
    add_steps([pre], "prereq", [
        st(table(["thêm hai điều", "nghĩa", "ví dụ"],
                 [["④ Bản đồ (Map) trong Java", "bảng tra trong bộ nhớ: <code>put(khoá, giá trị)</code> cất, <code>get(khoá)</code> lấy, <code>containsKey(khoá)</code> hỏi có chưa; dòng <code>import java.util.*;</code> đầu tệp để dùng được; <code>Map&lt;Integer, Long&gt;</code>: khoá là số nguyên, giá trị là số nguyên dài; chữ <code>L</code> sau số (<code>1000L</code>) báo số nguyên dài; <code>i % 4</code>: phần dư của i chia 4", "<code>boDem.put(7, 7000L)</code>"],
                  ["⑤ Mô phỏng", "chương trình nhỏ làm giả hành vi của một hệ thống thật để hiểu cơ chế; <b>không phải</b> hệ thống thật", "bản đồ Java đóng vai Redis"]]),
           """Thêm hai điều nữa. Bản đồ trong Java là bảng tra nằm trong bộ nhớ: lệnh cất đặt một giá trị dưới một khoá, lệnh lấy trả giá trị, và lệnh hỏi cho biết khoá đã có chưa. Cặp ngoặc nhọn sau chữ bản đồ ghi kiểu: khoá là số nguyên, giá trị là số nguyên dài, và chữ L sau một số báo đó là số nguyên dài. Dấu phần trăm giữa hai số cho phần dư của phép chia.
           Mô phỏng là chương trình nhỏ làm giả một hệ thống thật để hiểu cơ chế; ở bài này, một bản đồ Java đóng vai Redis.""", clear=True),
    ], at=1)
    pre["title"] = "Trước hết: tám điều cần hiểu"
    run = sc("chay_that", "example", "Chạy thật: mô phỏng bộ đệm và mã chặn bằng Java", [
        *jsteps([("sig", "<code>static long soDu(int tk)</code>: trả về số nguyên dài, nhận một số nguyên là mã tài khoản<br><code>static boolean ghi(long ma, String v)</code>: trả về đúng hoặc sai, nhận mã chặn và giá trị",
                "hàm số dư nhận mã tài khoản, trả về số nguyên dài; hàm ghi nhận mã chặn và giá trị, trả về đúng hoặc sai."),
               ("for", "<code>for (int i = 0; i &lt; 100; i++) soDu(i % 10);</code>: gọi 100 lần, i chạy từ 0 tới 99", None),
               ("if", "<code>if (boDem.containsKey(tk)) { … }</code>: có trong bộ đệm thì trúng", None),
               ("incr", "<code>trung++;</code>, <code>tong += 1;</code>", None),
               ("concat", "<code>\"trung \" + trung + \"/100, trung binh \" + …</code>", None)]),
        st(code_block(bo_dem, lines=(1, 12), title="BoDem.java (phần 1): hỏi bộ đệm trước, trượt thì hỏi cơ sở dữ liệu rồi nạp"),
           """Ta mô phỏng bộ đệm bằng Java, vì Redis thật cần cài riêng, còn cơ chế thì giống nhau. Một bản đồ đóng vai Redis. Khi hỏi số dư, nếu khoá đã có thì trúng, tốn một mili giây.
           Nếu chưa có thì trượt, tốn một mili giây hỏi bộ đệm cộng hai mươi mili giây hỏi cơ sở dữ liệu, rồi nạp kết quả vào bộ đệm."""),
        st(code_block(bo_dem, lines=(13, 17), title="Phần 2: một trăm lần hỏi, mười tài khoản") + out_block(bo_dem)
           + '<p class="note"><code>tong / 100.0</code>: có <code>.0</code> để phép chia cho ra số thập phân; chia cho <code>100</code> sẽ cắt phần lẻ.</p>',
           """Ta hỏi một trăm lần, quay vòng mười tài khoản. Mười lần đầu trượt, chín mươi lần sau trúng. Chương trình in chín mươi trúng trên một trăm, và trung bình ba mili giây.
           Chữ chấm không sau một trăm để phép chia ra số thập phân, chia cho một trăm thì cắt mất phần lẻ.""", clear=True),
        st(code_block(ma_chan, lines=(1, 9), title="MaChan.java (phần 1): kho dữ liệu từ chối mã chặn cũ"),
           """Bây giờ là mã chặn. Kho dữ liệu được ghi nhớ mã chặn lớn nhất đã thấy, và từ chối mọi lần ghi mang mã nhỏ hơn.""", clear=True),
        st(code_block(ma_chan, lines=(10, 15), title="Phần 2: B ghi trước, A ghi muộn"),
           """Người B lấy khoá sau nên mang mã ba mươi bốn và ghi trước. Người A mang mã ba mươi ba, bị tạm dừng quá hạn rồi mới tỉnh dậy và ghi.""", clear=True),
        st(out_block(ma_chan),
           """Khi chạy thật, lần ghi của B được nhận. Lần ghi muộn của A bị từ chối vì mã cũ hơn, nên giá trị cuối cùng là của B. """, clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: bộ đệm giữ cơ sở dữ liệu khỏi quá tải được tới đâu?", [
        st("""<p>Mỗi lần hỏi cơ sở dữ liệu giữ một kết nối $20$ ms (số minh hoạ). Số kết nối bận trung bình bằng số lần hỏi mỗi giây nhân thời gian giữ (định luật Little):</p>
$$\\text{kết nối bận} = \\text{lần hỏi mỗi giây} \\cdot 0{,}02$$"""
           + table(["tải", "yêu cầu mỗi giây", "không bộ đệm", "trúng 90%", "trúng 99%"],
                   [["×1", "100", "2", "0,2", "0,02"],
                    ["×100", "10 000", "200", "20", "2"],
                    ["×10 000", "1 000 000", "<b>20 000</b>", "<b>2 000</b>", "<b>200</b>"]]),
           """Mỗi lần hỏi cơ sở dữ liệu giữ một kết nối hai mươi mili giây. Số kết nối bận trung bình bằng số lần hỏi mỗi giây nhân thời gian giữ, tức nhân không phẩy không hai.
           Ở một trăm yêu cầu mỗi giây, không có bộ đệm thì cần hai kết nối. Tải tăng một trăm lần cần hai trăm. Tải tăng mười nghìn lần cần hai mươi nghìn.
           Bộ đệm trúng chín mươi phần trăm cắt con số này còn một phần mười, trúng chín mươi chín phần trăm còn một phần trăm.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Bộ đệm trúng 90% cứu được ×100 (cần 20 kết nối, một nhóm kết nối vài chục là đủ) nhưng ở ×10 000 vẫn cần 2 000: gãy. Tăng tỉ lệ trúng lên 99% còn 200; muốn xuống mười thì phải trúng <b>99,95%</b> (20 000 × 0,0005 = 10), mà tỉ lệ trúng càng cao càng khó.
Thêm một cạm bẫy: khi nhiều mục cùng hết hạn một lúc, mọi yêu cầu cùng trượt và dồn xuống cơ sở dữ liệu.</div>
<div class="box key"><b>Đánh đổi:</b> sống lâu hơn thì trúng nhiều hơn nhưng số dư hiển thị có thể <b>cũ</b>; số dư tiền thật phải ghi và đọc có kiểm soát. Ở quy mô lớn còn phải chia cơ sở dữ liệu và đặt hạn hết hạn ngẫu nhiên để tránh dồn cục.</div>""",
           """Bộ đệm trúng chín mươi phần trăm cứu được tải gấp trăm lần, cần hai mươi kết nối, một nhóm kết nối, tức số kết nối mở sẵn để dùng chung, vài chục là đủ. Nhưng ở tải gấp mười nghìn lần vẫn cần hai nghìn, nên gãy.
           Tăng tỉ lệ trúng lên chín mươi chín phần trăm còn hai trăm, còn muốn xuống mười thì phải trúng chín mươi chín phẩy chín mươi lăm phần trăm. Một cạm bẫy khác là nhiều mục cùng hết hạn một lúc, mọi yêu cầu cùng trượt và dồn xuống cơ sở dữ liệu.
           Đánh đổi là sống lâu hơn thì trúng nhiều hơn, nhưng số dư hiển thị có thể cũ. Ở quy mô lớn phải chia cơ sở dữ liệu và đặt hạn hết hạn ngẫu nhiên.""", clear=True),
    ], checks=["100 * 0.02 == 2.0", "round(10000 * 0.02) == 200", "round(1000000 * 0.02) == 20000", "round(2 * 0.1, 2) == 0.2",
               "round(200 * 0.1) == 20", "round(20000 * 0.1) == 2000", "round(2 * 0.01, 2) == 0.02", "round(200 * 0.01) == 2", "round(20000 * 0.01) == 200"])
    d_lab = write_lab("BNK", "L06", """# Lab BNK L06 — Bộ đệm nhỏ, bốn tài khoản

Bộ đệm kiểu **hỏi bộ đệm trước, trượt thì hỏi cơ sở dữ liệu rồi nạp vào bộ đệm**. Trúng bộ đệm tốn **2 ms**; trượt tốn **2 ms** (hỏi bộ đệm) **cộng 30 ms** (hỏi cơ sở dữ liệu). Số liệu là số minh hoạ.

Viết chương trình `BoDemNho` (tệp `BoDemNho.java`, đầu tệp có `import java.util.*;`), dùng một `Map<Integer, Long>` làm bộ đệm:
1. Hàm `soDu(int tk)`: nếu bộ đệm có `tk` thì tính trúng; nếu không thì tính trượt, đọc `tk * 1000L` làm số dư giả lập và nạp vào bộ đệm.
2. Gọi `soDu(i % 4)` cho `i` từ 0 tới 39 (40 lần hỏi, bốn tài khoản).
3. In một dòng: `trung 36/40, trung binh 5.0 ms` (số trúng, và tổng độ trễ chia 40).

Chạy: `javac BoDemNho.java && java BoDemNho`. Chấm: `bash labs/cham.sh BNK L06 BoDemNho.java`.

## Phần thêm (không chấm): mã chặn
Thư mục `ma_chan/` có `MaChan.java` đầy đủ (đúng như trong video) và `ket_qua.txt`. Cần JDK 21.
1. `cd ma_chan`, rồi `javac MaChan.java && java MaChan`: B ghi được, A ghi muộn bị từ chối, giá trị cuối là B.
2. **Đoán trước**: đổi mã của B thành 32 (nhỏ hơn mã 33 của A) thì ai ghi được, giá trị cuối là gì? Sửa `main`, chạy lại và so với đoán.
3. Thêm lần ghi thứ ba, người C mang mã 35 ghi "C" sau cùng, và đoán giá trị cuối rồi chạy.
""", "java", lab_dem["code"], lab_dem["out"])
    (d_lab / "ma_chan").mkdir(exist_ok=True)
    (d_lab / "ma_chan" / "MaChan.java").write_text(ma_chan["code"] + chr(10), encoding="utf-8", newline=chr(10))
    (d_lab / "ma_chan" / "ket_qua.txt").write_text(ma_chan["out"] + chr(10), encoding="utf-8", newline=chr(10))
    lab = practice_scene(sc, "Tự làm: bộ đệm nhỏ, bốn tài khoản", practice_steps(
        st, "BNK", "L06",
        """<p><b>Đề</b>: trúng bộ đệm 2 ms; trượt 2 + 30 ms. Viết <code>BoDemNho.java</code>:</p>
<ol><li>bộ đệm <code>Map&lt;Integer, Long&gt;</code>; hàm <code>soDu(tk)</code>: có thì trúng, không thì trượt rồi nạp <code>tk * 1000L</code></li>
<li>gọi <code>soDu(i % 4)</code> cho <code>i</code> từ 0 tới 39</li>
<li>in <code>trung …/40, trung binh … ms</code></li></ol>
<p class="note">Phần thêm (không chấm): thư mục <code>ma_chan/</code> của lab có <code>MaChan.java</code> để thử đổi mã chặn.</p>""",
        """Bây giờ tới phần bạn tự làm. Trúng bộ đệm tốn hai mili giây, trượt tốn hai cộng ba mươi mili giây. Hãy viết chương trình với một bản đồ làm bộ đệm, và một hàm hỏi số dư: có trong bộ đệm thì tính trúng, chưa có thì tính trượt rồi nạp vào.
        Gọi hàm bốn mươi lần, quay vòng bốn tài khoản, rồi in số lần trúng và độ trễ trung bình. Hãy dừng video, tự viết và chạy. Nếu còn sức, làm phần thêm trong thư mục thực hành.""",
        lab_dem["out"], "BoDemNho.java",
        """<div class="box key"><b>Nếu kẹt:</b> mô theo <code>BoDem</code>: <code>if (boDem.containsKey(tk)) { trung++; tong += 2; return boDem.get(tk); }</code>, còn lại <code>tong += 2 + 30;</code>, nạp bằng <code>boDem.put(tk, v)</code>.
Độ trễ trung bình là <code>tong / 40.0</code>. Lời giải ở <code>labs/BNK/L06/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, làm theo mẫu ví dụ: nếu bản đồ đã có khoá thì cộng độ trễ trúng, nếu chưa thì cộng độ trễ trượt rồi nạp. Độ trễ trung bình là tổng chia bốn mươi, viết dưới dạng số thực. Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=150), "BNK", "L06")
    return lesson("L06", "redis_cache_khoa_phan_tan", "Bài 6 — Redis, bộ đệm và khoá phân tán",
                  "curriculum/bnk.yaml L06; audit/bnk/verify_bnk.py L06; audit/review/screen_code/BNK.yaml (mô phỏng bằng Java 21, Redis thật không chạy trong bài: chỉ mô phỏng logic, không kiểm cú pháp Redis); Redis documentation (SET NX PX); Kleppmann, How to do distributed locking (fencing token); định luật Little L = λ·W (Little, 1961)",
                  ["Tính độ trễ trung bình của bộ đệm theo tỉ lệ trúng", "Nêu vì sao khoá có hạn có thể bị hai người giữ",
                   "Áp mã chặn để nơi lưu từ chối người giữ khoá cũ", "Quyết định đúng khi dùng khoá phân tán cho tiền",
                   "Chạy mô phỏng bộ đệm và mã chặn bằng Java để thấy kết quả",
                   "Tính số kết nối cơ sở dữ liệu bận khi tải tăng ×100, ×10 000 ở các tỉ lệ trúng khác nhau",
                   "Viết hàm đọc bộ đệm kiểu hỏi trước, trượt thì nạp, và tính độ trễ trung bình"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "formula"), (2, "intuition"), (3, "chay_that"), (4, "quiz"), (5, "chay_that"), (6, "quy_mo"), (7, "practice")])
