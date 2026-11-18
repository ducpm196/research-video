from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    tq = prog("TuongQuan", """
import java.util.*;
public class TuongQuan {
    public static void main(String[] args) {
        Map<String, String> cho = new HashMap<>();             // mã thông điệp -> yêu cầu đang chờ
        for (int i = 0; i < 5; i++) cho.put("M" + i, "chuyen " + (i + 1) * 100);
        String[] ve = { "M2 chuyen 300", "M0 chuyen 100", "M1 chuyen 200",
                        "M4 chuyen 500", "M3 chuyen 400" };    // phản hồi: mã + việc
        int theoThuTu = 0, theoMa = 0;                         // số phản hồi ghép đúng
        for (int k = 0; k < ve.length; k++) {
            String ma = ve[k].substring(0, 2), viec = ve[k].substring(3);
            if (cho.get("M" + k).equals(viec)) theoThuTu++;    // ghép theo thứ tự đến
            if (cho.get(ma).equals(viec)) theoMa++;            // ghép theo mã tương quan
        }
        System.out.println("ghep theo thu tu: " + theoThuTu + "/5 dung");
        System.out.println("ghep theo ma: " + theoMa + "/5 dung");
    }
}""", out="""ghep theo thu tu: 0/5 dung
ghep theo ma: 5/5 dung""")
    het_gio = prog("HetGio", """
public class HetGio {
    static int soLanGhiNo(boolean daHachToan, boolean hoiTruoc) {
        int n = daHachToan ? 1 : 0;           // phản hồi bị mất, nhưng lõi có thể đã ghi nợ rồi
        if (hoiTruoc) {
            if (!daHachToan) n++;             // hỏi trạng thái: chỉ gửi lại khi chưa hạch toán
        } else {
            n++;                              // gửi lại ngay, không hỏi
        }
        return n;
    }
    public static void main(String[] args) {
        System.out.println("da hach toan, gui lai ngay:  " + soLanGhiNo(true, false));
        System.out.println("da hach toan, hoi truoc:     " + soLanGhiNo(true, true));
        System.out.println("chua hach toan, hoi truoc:   " + soLanGhiNo(false, true));
        System.out.println("chua hach toan, gui lai ngay: " + soLanGhiNo(false, false));
    }
}""", out="""da hach toan, gui lai ngay:  2
da hach toan, hoi truoc:     1
chua hach toan, hoi truoc:   1
chua hach toan, gui lai ngay: 1""")
    lab_tq = prog("GhepPhanHoi", """
import java.util.*;
public class GhepPhanHoi {
    public static void main(String[] args) {
        Map<String, String> cho = new HashMap<>();
        for (int i = 0; i < 6; i++) cho.put("M" + i, "chuyen " + (i + 1) * 100);
        String[] ve = { "M3", "M5", "M0", "M1", "M4", "M2" };    // mã tương quan, theo thứ tự phản hồi về
        int dung = 0;
        for (int k = 0; k < ve.length; k++) {
            System.out.println("phan hoi " + k + ": " + ve[k] + " -> " + cho.get(ve[k]));
            if (ve[k].equals("M" + k)) dung++;
        }
        System.out.println("dung neu ghep theo thu tu: " + dung + "/6");
    }
}""", out="""phan hoi 0: M3 -> chuyen 400
phan hoi 1: M5 -> chuyen 600
phan hoi 2: M0 -> chuyen 100
phan hoi 3: M1 -> chuyen 200
phan hoi 4: M4 -> chuyen 500
phan hoi 5: M2 -> chuyen 300
dung neu ghep theo thu tu: 1/6""")
    hook = sc("hook", "hook", "Vì sao phản hồi về không đúng thứ tự, và hết giờ chờ thì làm gì?", [
        st("""<p>Kênh số gửi $5$ lệnh sang lõi ngân hàng (hệ thống trung tâm giữ tài khoản và sổ cái) qua hàng đợi (nơi xếp thông điệp, lấy ra theo thứ tự vào). Phản hồi quay về <b>lộn xộn</b>: lệnh $2$ trả lời trước lệnh $0$.</p>
<div class="box key">Nếu ghép phản hồi theo <b>thứ tự đến</b>, cả $5$ lệnh nhận nhầm kết quả. Phải ghép theo <b>mã tương quan</b>: mã mà mỗi phản hồi mang theo để chỉ ra nó trả lời lệnh nào.</div>""",
           """Kênh số gửi năm lệnh sang lõi ngân hàng, hệ thống trung tâm giữ tài khoản và sổ cái, qua hàng đợi, tức nơi xếp thông điệp và lấy ra theo thứ tự vào. Phản hồi quay về lộn xộn, lệnh hai được trả lời trước lệnh không.
           Nếu ghép phản hồi theo thứ tự đến, cả năm lệnh nhận nhầm kết quả. Phải ghép theo mã tương quan, tức mã mà mỗi phản hồi mang theo để chỉ ra nó trả lời lệnh nào."""),
        st(table(["cách ghép", "số phản hồi đúng (thứ tự về: 2, 0, 1, 4, 3)"],
                 [["theo thứ tự đến", "0 trên 5"], ["theo mã tương quan", "5 trên 5"]]),
           """Ghép theo thứ tự đến thì không phản hồi nào đúng. Ghép theo mã tương quan thì đúng cả năm.
           Hôm nay ta học thêm một việc khó hơn, là khi hết giờ chờ mà không biết lõi ngân hàng đã hạch toán, tức ghi vào sổ, hay chưa."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: những điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Kênh số", "ứng dụng ngân hàng trên điện thoại hay trang web mà khách dùng", "ứng dụng chuyển tiền"],
                  ["② Lõi ngân hàng (core banking)", "hệ thống trung tâm giữ tài khoản và sổ cái (sổ ghi mọi khoản tiền vào ra)", "T24"],
                  ["③ Hạch toán", "ghi khoản tiền vào sổ cái, tức là trừ hay cộng tiền thật sự", "ghi nợ 500 000 vào tài khoản A"]]),
           """Trước hết ta cần hiểu vài điều. Kênh số là ứng dụng ngân hàng trên điện thoại hay trang web mà khách dùng. Lõi ngân hàng là hệ thống trung tâm giữ tài khoản và sổ cái, tức sổ ghi mọi khoản tiền vào ra.
           Hạch toán là ghi khoản tiền vào sổ cái, tức là trừ hay cộng tiền thật sự, ví dụ ghi nợ năm trăm nghìn vào tài khoản A."""),
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["④ Hàng đợi", "nơi xếp thông điệp (gói dữ liệu gửi giữa hai hệ thống), lấy theo thứ tự vào", "lệnh 0, 1, 2 xếp hàng"],
                  ["⑤ Thông điệp có tiêu đề", "ngoài nội dung còn có các nhãn như mã thông điệp", "mã thông điệp M7"],
                  ["⑥ Yêu cầu – phản hồi", "bên gửi hỏi, bên nhận làm rồi trả lời", "hỏi chuyển tiền, trả kết quả"]]),
           """Hàng đợi là nơi xếp thông điệp, tức gói dữ liệu gửi giữa hai hệ thống, và lấy ra theo thứ tự vào. Thông điệp ngoài nội dung còn có các nhãn như mã thông điệp.
           Còn yêu cầu và phản hồi là bên gửi hỏi, bên nhận làm rồi trả lời.""", clear=True),
        st("""$$5! = 5 \\cdot 4 \\cdot 3 \\cdot 2 \\cdot 1 = 120$$""",
           """Năm phản hồi có thể về theo một trăm hai mươi thứ tự khác nhau, vì năm nhân bốn nhân ba nhân hai nhân một bằng một trăm hai mươi."""),
    ], checks=["5 * 4 * 3 * 2 * 1 == 120 == math.factorial(5)"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["Temenos T24 (nay là Temenos Transact)", "phần mềm lõi ngân hàng (nơi giữ tài khoản và sổ cái)"],
                  ["OFS", "Open Financial Service: bản tin dạng chữ để gọi chức năng của lõi từ bên ngoài"],
                  ["IBM MQ", "phần mềm hàng đợi thông điệp, chuyển bản tin giữa hệ thống"],
                  ["MessageID / CorrelationID", "mã của thông điệp / mã của thông điệp mà phản hồi này trả lời"],
                  ["hết giờ chờ (timeout)", "không nhận phản hồi trong thời hạn, chưa biết kết quả"],
                  ["phạm vi bài", "không dạy cú pháp bản tin OFS hay lệnh IBM MQ thật; chỉ dạy cơ chế ghép phản hồi theo mã, dùng chung cho mọi hàng đợi"]]),
           """Temenos T24 là phần mềm lõi ngân hàng, nay hãng đã đổi tên. OFS là bản tin dạng chữ để gọi chức năng của lõi từ bên ngoài. IBM MQ là phần mềm hàng đợi, chuyển bản tin giữa các hệ thống.
           Mã thông điệp là mã của chính thông điệp, còn mã tương quan là mã của thông điệp mà phản hồi này trả lời. Hết giờ chờ là khi không nhận được phản hồi trong thời hạn. Bài này chỉ dạy cơ chế ghép phản hồi, không dạy cú pháp bản tin thật."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: hai hàng đợi và mã tương quan", [
        st(svg(1500, 440,
               box(40, 160, 260, 110, ["Kênh số", "gửi lệnh"], C_BLUE, bold=True),
               box(420, 40, 380, 90, "hàng đợi yêu cầu", C_AMBER), box(420, 300, 380, 90, "hàng đợi phản hồi", C_AMBER),
               box(960, 160, 300, 110, ["Lõi ngân hàng", "xử lý song song"], C_GREEN, bold=True),
               arrow(300, 190, 415, 100, "#2a78d6"), txt(230, 135, "M7", 24, "middle", "#2a78d6", True, halo=True), arrow(800, 95, 955, 190, "#475569"),
               arrow(955, 245, 805, 340, "#16a34a"), txt(1100, 325, "tương quan = M7", 22, "middle", "#16a34a", True, halo=True), arrow(415, 345, 300, 250, "#16a34a"),
               txt(750, 425, "mẫu minh hoạ, không phải cú pháp T24 thật", 22, "middle", "#6b7280")),
           """Hình cho thấy luồng chung. Kênh số đặt lệnh vào hàng đợi yêu cầu, mang mã thông điệp, ví dụ M bảy. Lõi ngân hàng lấy ra xử lý, có thể song song nhiều lệnh.
           Phản hồi được đặt vào hàng đợi phản hồi, mang mã tương quan bằng đúng M bảy. Nhờ đó kênh số biết phản hồi nào trả lời lệnh nào. Hình này chỉ là mẫu minh hoạ."""),
        st(svg(1500, 420,
               txt(60, 50, "Lệnh gửi theo thứ tự:", 26, "start", "#1f2937", True),
               box(60, 80, 160, 60, "0", C_BLUE), box(240, 80, 160, 60, "1", C_BLUE), box(420, 80, 160, 60, "2", C_BLUE), box(600, 80, 160, 60, "3", C_BLUE), box(780, 80, 160, 60, "4", C_BLUE),
               txt(560, 232, "Phản hồi về theo thứ tự:", 26, "start", "#1f2937", True),
               box(60, 250, 160, 60, "2", C_AMBER), box(240, 250, 160, 60, "0", C_AMBER), box(420, 250, 160, 60, "1", C_AMBER), box(600, 250, 160, 60, "4", C_AMBER), box(780, 250, 160, 60, "3", C_AMBER),
               arrow(500, 142, 140, 246, "#dc2626", None, dash=True),
               txt(1200, 150, "Ghép theo thứ tự đến:", 26, "middle", "#dc2626", True), txt(1200, 190, "phản hồi 2 bị gán cho lệnh 0 (sai)", 24, "middle", "#dc2626"),
               txt(1200, 300, "Ghép theo mã tương quan:", 26, "middle", "#16a34a", True), txt(1200, 340, "phản hồi 2 → lệnh 2 (đúng)", 24, "middle", "#16a34a")),
           """ Lệnh gửi theo thứ tự không, một, hai, ba, bốn. Phản hồi về theo thứ tự hai, không, một, bốn, ba.
           Ghép theo thứ tự đến thì phản hồi của lệnh hai bị gán cho lệnh không, sai. Ghép theo mã tương quan thì phản hồi hai về đúng lệnh hai."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: ghép đúng và xử lý khi hết giờ chờ", [
        st("""<p><b>Bước 1.</b> Lõi xử lý song song, nên thứ tự phản hồi <b>có thể không</b> theo thứ tự gửi. $5$ phản hồi có thể về theo $120$ thứ tự.</p>
<span class='note'>Làm thử: chỉ $1$ thứ tự trong $120$ là đúng thứ tự gửi.</span>""",
           """Bước một, vì lõi xử lý song song, nên thứ tự phản hồi có thể không theo thứ tự gửi. Năm phản hồi có thể về theo một trăm hai mươi thứ tự. Làm thử, chỉ một thứ tự trong số đó trùng đúng thứ tự gửi."""),
        st("""<p><b>Bước 2.</b> Mỗi phản hồi mang <b>mã tương quan</b> bằng mã thông điệp của lệnh. Bên gửi giữ bảng “mã → lệnh đang chờ” rồi tra theo mã.</p>
<span class='note'>Làm thử: mọi phản hồi đều tìm ra lệnh của mình → $5$ trên $5$.</span>""",
           """Bước hai, vì mỗi phản hồi mang mã tương quan bằng mã thông điệp của lệnh, nên bên gửi giữ một bảng mã và lệnh đang chờ, rồi tra theo mã. Làm thử, mọi phản hồi đều tìm ra lệnh của mình, năm trên năm."""),
        st("""<p><b>Bước 3.</b> Hết giờ chờ chỉ cho biết chưa có phản hồi, không cho biết lõi đã hạch toán chưa. <b>Truy vấn trạng thái trước</b>, rồi mới quyết định thử lại.</p>
<span class='note'>Làm thử: đã hạch toán mà gửi lại ngay → ghi nợ $2$ lần.</span>
<p>Lưu ý: “chưa thấy” chưa chắc chắn, vì lệnh gốc có thể còn trong hàng đợi. Gửi lại phải dùng <b>cùng mã tham chiếu</b> (mã riêng của lệnh chuyển tiền, giữ nguyên qua mọi lần gửi) để lõi từ chối trùng, hoặc đặt hạn sống (Expiry) cho bản tin.</p>""",
           """Bước ba, vì hết giờ chờ chỉ cho biết chưa có phản hồi, chứ không cho biết lõi đã hạch toán chưa, nên ta truy vấn trạng thái trước, rồi mới quyết định thử lại. Làm thử, nếu đã hạch toán mà gửi lại ngay, khách bị ghi nợ hai lần.
           Lưu ý, kết quả chưa thấy cũng chưa chắc chắn, vì lệnh gốc có thể còn trong hàng đợi. Nên gửi lại phải dùng cùng mã tham chiếu, tức mã riêng của lệnh được giữ nguyên qua mọi lần gửi, để lõi từ chối trùng.""", clear=True),
    ], checks=["math.factorial(5) == 120", "alg.bnk_reply_match([2, 0, 1, 4, 3]) == (0, 5)", "alg.bnk_unknown_outcome(True, False) == 2"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Năm lệnh mã $0..4$. Phản hồi về theo thứ tự $2, 0, 1, 4, 3$.</p>
$$① \\; \\text{ghép theo thứ tự đến: } 0 \\text{ trên } 5\\ \\text{đúng}$$""",
           """Năm lệnh có mã từ không tới bốn. Phản hồi về theo thứ tự hai, không, một, bốn, ba. Phép tính thứ nhất, ghép theo thứ tự đến thì không phản hồi nào đúng."""),
        st("""<p>Vì sao $0$? Vị trí về thứ $k$ chứa mã $2, 0, 1, 4, 3$, và <b>không vị trí nào trùng mã của nó</b> ($2 \\ne 0$, $0 \\ne 1$, $1 \\ne 2$, $4 \\ne 3$, $3 \\ne 4$).</p>
$$② \\; \\text{số vị trí trùng} = \\hl{0}$$""",
           """Phép tính thứ hai. Vị trí thứ nhất chứa hai, khác không. Vị trí thứ hai chứa không, khác một. Số vị trí trùng là không."""),
        st("""$$③ \\; \\text{ghép theo mã tương quan: } \\hlg{5} \\text{ trên } 5\\ \\text{đúng}$$""",
           """Phép tính thứ ba, ghép theo mã tương quan thì cả năm đều đúng, vì mỗi phản hồi tự mang mã của lệnh."""),
        st("""<p>Hết giờ chờ, lõi <b>đã</b> hạch toán, gửi lại không truy vấn.</p>
$$④ \\; 1 + 1 = \\hl{2}\\ \\text{lần ghi nợ}$$""",
           """Phép tính thứ tư, hết giờ chờ, nhưng lõi đã hạch toán, và ta gửi lại mà không truy vấn. Số lần ghi nợ là một cộng một, bằng hai."""),
        st("""<p>Cùng tình huống nhưng <b>truy vấn trạng thái trước</b>: thấy đã hạch toán nên không gửi lại.</p>
$$⑤ \\; \\text{số lần ghi nợ} = \\hlg{1}$$""",
           """Phép tính thứ năm, cùng tình huống nhưng truy vấn trạng thái trước. Thấy đã hạch toán nên không gửi lại, số lần ghi nợ là một."""),
    ], checks=["alg.bnk_reply_match([2, 0, 1, 4, 3])[0] == 0 and all(r != k for k, r in enumerate([2, 0, 1, 4, 3]))",
               "alg.bnk_reply_match([2, 0, 1, 4, 3])[1] == 5", "1 + 1 == alg.bnk_unknown_outcome(True, False)", "alg.bnk_unknown_outcome(True, True) == 1"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm các thứ tự không trùng", [
        st("""<p>Đường khác: vét cạn $120$ thứ tự, đếm những thứ tự mà <b>không</b> phản hồi nào về đúng vị trí. Đáp số là $44$, và thứ tự $2, 0, 1, 4, 3$ nằm trong $44$ đó.</p>
$$\\text{44 trên 120} \\approx \\hl{37\\%}$$
<p class="small">Đây là xác suất nếu mọi thứ tự về đều có khả năng như nhau (mô hình minh hoạ).</p>
""",
           """Kiểm bằng đường khác. Ta vét cạn một trăm hai mươi thứ tự, đếm những thứ tự mà không phản hồi nào về đúng vị trí. Có bốn mươi bốn thứ tự như vậy, và thứ tự của ta nằm trong đó.
           Bốn mươi bốn trên một trăm hai mươi là khoảng ba mươi bảy phần trăm.
           Ta gọi đó là xác suất trong mô hình minh hoạ, vì ta giả sử mọi thứ tự về đều có khả năng như nhau. """),
        st(table(["tình huống", "đã hạch toán?", "truy vấn trước?", "số lần ghi nợ"],
                 [["A", "có", "không", "2 (sai)"], ["B", "có", "có", "1"], ["C", "chưa", "có", "1 (gửi lại cùng mã tham chiếu)"], ["D", "chưa", "không", "1 nếu lệnh gốc đã mất hẳn; 2 nếu lệnh gốc tới muộn mà lần gửi lại khác mã"]]),
           """Bảng này tổng hợp bốn tình huống. Tình huống A chắc chắn ghi nợ hai lần. Vì truy vấn trước cho ta biết đã hạch toán chưa, nên tình huống B và C đều đúng một lần. Ở tình huống C, lần gửi lại mang cùng mã tham chiếu, để lõi từ chối nếu lệnh gốc tới muộn.
           Tình huống D chỉ đúng một lần khi lệnh gốc đã mất hẳn. Nếu lệnh gốc tới muộn mà lần gửi lại mang mã khác, khách vẫn bị ghi nợ hai lần.""", clear=True),
    ], checks=["sum(1 for p in __import__('itertools').permutations(range(5)) if all(p[i] != i for i in range(5))) == 44",
               "round(44 / 120 * 100) == 37", "[alg.bnk_unknown_outcome(a, b) for a, b in ((True, False), (True, True), (False, True), (False, False))] == [2, 1, 1, 1]"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Giả định phản hồi về <b>đúng thứ tự gửi</b>. Khi tải nhẹ có thể đúng, khi tải cao thì sai, nên lỗi chỉ hiện lúc cao điểm.</div>""",
           """Lỗi thứ nhất, của người mới. Giả định phản hồi về đúng thứ tự gửi. Khi tải nhẹ có thể đúng, khi tải cao thì sai, nên lỗi chỉ hiện lúc cao điểm."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Hết giờ chờ rồi gửi lại ngay</b>. Lõi có thể đã hạch toán, nên khách bị ghi nợ hai lần.
<br><span class="note">Cách chữa: truy vấn trạng thái bằng mã tham chiếu của lệnh trước khi gửi lại, và gắn khoá lũy đẳng vào lệnh (mã duy nhất mỗi lệnh, gặp lại thì bỏ qua).</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là hết giờ chờ rồi gửi lại ngay. Lõi có thể đã hạch toán, nên khách bị ghi nợ hai lần.
           Cách chữa là truy vấn trạng thái bằng mã tham chiếu của lệnh trước khi gửi lại, và gắn khoá lũy đẳng vào lệnh, tức mã duy nhất mỗi lệnh, gặp lại thì bỏ qua."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nhiều bản của dịch vụ (cùng một chương trình chạy trên nhiều máy để chịu tải) cùng đọc <b>một hàng đợi phản hồi</b>, nên bản này lấy nhầm phản hồi của bản kia.
Mỗi bản cần hàng đợi phản hồi riêng, hoặc chỉ nhận thông điệp có mã tương quan của mình.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là nhiều bản của dịch vụ cùng đọc một hàng đợi phản hồi. Nhiều bản nghĩa là cùng một chương trình chạy trên nhiều máy để chịu tải, nên bản này lấy nhầm phản hồi của bản kia.
           Mỗi bản cần hàng đợi phản hồi riêng, hoặc chỉ nhận thông điệp có mã tương quan của mình."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Phản hồi về theo thứ tự 0, 2, 1, 3, 4. Ghép theo thứ tự đến đúng mấy lệnh?"],
                  ["2", "Lõi chưa hạch toán, bạn truy vấn rồi gửi lại. Ghi nợ mấy lần?"],
                  ["3", "Quyết định: khi hết giờ chờ với lệnh chuyển tiền, làm gì đầu tiên?"]]),
           """Đến lượt bạn. Câu một, phản hồi về theo thứ tự không, hai, một, ba, bốn, ghép theo thứ tự đến đúng mấy lệnh? Câu hai, lõi chưa hạch toán, bạn truy vấn rồi gửi lại, ghi nợ mấy lần?
           Câu ba, khi hết giờ chờ với lệnh chuyển tiền, việc đầu tiên là gì? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: vị trí $0$ chứa $0$ ✓, vị trí $3$ chứa $3$ ✓, vị trí $4$ chứa $4$ ✓; vị trí $1$ chứa $2$, vị trí $2$ chứa $1$.</p>
$$\\hl{3}\\ \\text{trên } 5$$""",
           """Đáp án câu một. Vị trí không chứa không, đúng. Vị trí ba chứa ba, vị trí bốn chứa bốn, đúng. Vị trí một và hai chứa nhầm. Vậy đúng ba trên năm."""),
        st("""$$\\text{ghi nợ} = \\hlg{1}\\ \\text{lần (chỉ lần gửi lại)}$$""",
           """Đáp án câu hai. Lõi chưa hạch toán nên lần đầu chưa trừ gì, và lần gửi lại trừ đúng một lần."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["truy vấn trạng thái trước, rồi mới thử lại", "không ghi nợ trùng", "chậm hơn một vòng hỏi"],
                  ["gửi lại ngay", "nhanh", "có thể ghi nợ hai lần"]]),
           """Đáp án câu ba. Việc đầu tiên là truy vấn trạng thái bằng mã tham chiếu của lệnh, rồi mới quyết định thử lại. Chậm hơn một vòng hỏi, nhưng không ghi nợ trùng. Gửi lại ngay thì nhanh nhưng có thể ghi nợ hai lần."""),
    ], checks=["alg.bnk_reply_match([0, 2, 1, 3, 4])[0] == 3", "alg.bnk_unknown_outcome(False, True) == 1"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("lõi xử lý song song", "phản hồi lộn xộn", "ghép theo mã tương quan", "hết giờ chờ → truy vấn trước"),
           """Lõi xử lý song song nên phản hồi lộn xộn. Ghép theo mã tương quan. Hết giờ chờ thì truy vấn trạng thái trước khi thử lại."""),
        st("""<div class='box key'><b>Tư duy:</b> “không có phản hồi” là <b>trạng thái chưa biết</b>, không phải “thất bại”. Chưa biết thì đi hỏi, đừng đoán.</div>""",
           """Không có phản hồi là trạng thái chưa biết, không phải thất bại. Chưa biết thì đi hỏi, đừng đoán."""),
    ])
    # ── AF2: mô phỏng ghép phản hồi và hết giờ chờ bằng Java (T24, IBM MQ không chạy trên máy), quy mô, tự làm ──
    run = sc("chay_that", "example", "Chạy thật: ghép phản hồi theo mã tương quan (mô phỏng bằng Java)", [
        *jsteps([("main", "<code>public static void main(String[] args)</code>: chương trình bắt đầu ở đây", None),
               ("idx", "<code>ve[k]</code>: phản hồi thứ k của mảng <code>ve</code>; <code>ve.length</code>: số phản hồi, ở đây là 5",
                "phản hồi thứ k của mảng ve, và độ dài mảng ve là năm phản hồi."),
               ("for", "<code>for (int k = 0; k &lt; ve.length; k++) { … }</code>: k chạy từ 0 tới 4", None),
               ("arrinit", "<code>String[] ve = { \"M2 chuyen 300\", … };</code>", None),
               ("diamond", "<code>Map&lt;String, String&gt; cho = new HashMap&lt;&gt;()</code>", None),
               ("map", "<code>cho.put(\"M\" + i, …)</code>; <code>cho.get(ma)</code>; <code>.equals(viec)</code>", None),
               ("if", "<code>if (cho.get(\"M\" + k).equals(viec)) theoThuTu++;</code>: khớp thì đếm thêm một", None)]),
        st(code_block(tq, lines=(1, 8), title="TuongQuan.java (phần 1): bảng chờ và năm phản hồi lộn xộn"),
           """Lõi ngân hàng T24 và IBM MQ không chạy trên máy này, nên ta mô phỏng cơ chế bằng Java. Một bản đồ nhớ các yêu cầu đang chờ, khoá là mã thông điệp. Năm phản hồi về lộn xộn, mỗi phản hồi mang mã tương quan và việc đã làm. Dấu cộng giữa chữ và số ghép chúng thành một chuỗi, tức một dãy chữ, và vòng lặp thêm năm yêu cầu vào bản đồ."""),
        st(code_block(tq, lines=(9, 13), title="Phần 2: thử hai cách ghép cho từng phản hồi"),
           """Với từng phản hồi ta thử hai cách ghép. Cách một coi phản hồi thứ k là của yêu cầu thứ k. Cách hai tra bản đồ bằng mã tương quan. Hàm cắt chuỗi tách hai ký tự đầu làm mã, phần sau làm việc.""", clear=True),
        st(code_block(tq, lines=(14, 17), title="Phần 3: in kết quả hai cách") + out_block(tq),
           """Khi chạy thật, ghép theo thứ tự đến đúng không phản hồi nào trên năm, vì thứ tự về đã bị xáo hết. Ghép theo mã đúng cả năm. Vì thế ta tra theo mã.""", clear=True),
        *jsteps([("sig", "<code>static int soLanGhiNo(boolean daHachToan, boolean hoiTruoc)</code>: trả về số nguyên, nhận hai giá trị đúng hoặc sai",
                "hàm đếm số lần ghi nợ, trả về một số nguyên, và nhận hai tham số đúng hoặc sai là đã hạch toán chưa và có hỏi trước không."),
               ("inc1", "<code>n++;</code>: tăng số lần ghi nợ thêm một", None)]),
        st(code_block(het_gio, lines=(1, 10), title="HetGio.java (phần 1): phản hồi bị mất, số lần ghi nợ cuối cùng"),
           """Bây giờ là hết giờ chờ. Phản hồi bị mất, nhưng lõi có thể đã ghi nợ rồi hoặc chưa. Nếu gửi lại ngay thì ta cộng thêm một lần ghi nợ. Nếu hỏi trạng thái trước thì chỉ gửi lại khi lõi chưa hạch toán. Dấu hỏi chấm hai chấm chọn một trong hai giá trị, đã hạch toán thì một, chưa thì không, và dấu chấm than đảo đúng thành sai.""", clear=True),
        st(code_block(het_gio, lines=(11, 17), title="Phần 2: bốn tình huống") + out_block(het_gio),
           """Khi chạy thật, đã hạch toán rồi mà gửi lại ngay thì ghi nợ hai lần, khách bị trừ gấp đôi. Hỏi trạng thái trước thì cả hai trường hợp hỏi trước đều đúng một lần.  Vậy khi hết giờ chờ, phải truy vấn trạng thái trước khi thử lại.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: ghép theo thứ tự chỉ đúng nhờ may, hết giờ chờ thành chuyện hằng ngày", [
        st("""<p>Với $n$ phản hồi đang bay và thứ tự về <b>ngẫu nhiên</b>, số phản hồi mà cách ghép theo thứ tự đến ghép đúng có kỳ vọng bằng $1$, bất kể $n$ lớn thế nào; vậy số ghép sai kỳ vọng là $n - 1$. Giả sử $0{,}1\\%$ lệnh hết giờ chờ <i>(số minh hoạ)</i>:</p><p class="note">Kỳ vọng: giá trị trung bình khi lặp lại thật nhiều lần. Mỗi phản hồi trùng đúng vị trí với xác suất $1/n$; $n$ phản hồi nên trung bình $n \\cdot (1/n) = 1$ phản hồi trúng. Phản hồi đang bay: đã gửi đi nhưng chưa nhận về.</p>"""
           + table(["tải", "phản hồi đang bay n", "ghép theo thứ tự: sai kỳ vọng", "lệnh hết giờ chờ mỗi ngày"],
                   [["×1", "5", "4", "100 (trên 100 000 lệnh)"],
                    ["×100", "500", "<b>499</b>", "10 000 (trên 10 triệu lệnh)"],
                    ["×10 000", "50 000", "<b>49 999</b>", "<b>1 000 000</b> (trên 1 tỉ lệnh)"]]),
           """Phản hồi đang bay là phản hồi đã gửi đi nhưng chưa nhận về. Với n phản hồi đang bay và thứ tự về ngẫu nhiên, mỗi phản hồi trùng đúng vị trí của nó với xác suất một chia n. Nên trung bình, tức kỳ vọng, cách ghép theo thứ tự đến chỉ ghép đúng một phản hồi, bất kể n lớn thế nào. Vậy số ghép sai trung bình là n trừ một. Giả sử một phần nghìn số lệnh hết giờ chờ, đây là số minh hoạ.
           Với năm phản hồi đang bay, sai trung bình bốn. Tải tăng một trăm lần thì sai bốn trăm chín mươi chín. Tải tăng mười nghìn lần thì sai gần năm mươi nghìn. Số lệnh hết giờ chờ mỗi ngày đi từ một trăm lên một triệu.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Ghép theo thứ tự đến chỉ “chạy được” khi n nhỏ và thứ tự giữ nguyên; ở tải lớn gần như luôn sai. Gửi lại ngay khi hết giờ chờ, nhân với 1 triệu lệnh mỗi ngày, là trừ trùng hàng loạt.</div>
<div class="box key"><b>Đánh đổi:</b> mã tương quan phải <b>duy nhất</b> và bảng chờ trong bộ nhớ phải dọn khi hết hạn; hỏi trạng thái cho mỗi lệnh hết giờ chờ thêm tải (cỡ 0,1% lượng lệnh).</div>""",
           """Ghép theo thứ tự đến chỉ chạy được khi n nhỏ và thứ tự giữ nguyên, ở tải lớn gần như luôn sai. Gửi lại ngay khi hết giờ chờ, nhân với một triệu lệnh mỗi ngày, là trừ trùng hàng loạt.
           Đánh đổi là mã tương quan phải duy nhất và bảng chờ trong bộ nhớ phải dọn khi hết hạn. """, clear=True),
    ], checks=["5 - 1 == 4", "500 - 1 == 499", "50000 - 1 == 49999", "100000 * 0.001 == 100", "round(10_000_000 * 0.001) == 10000",
               "round(1_000_000_000 * 0.001) == 1_000_000"])
    write_lab("BNK", "L10", """# Lab BNK L10 — Sáu phản hồi lộn xộn

Sáu yêu cầu có mã thông điệp `M0 … M5`, yêu cầu `Mi` có nội dung `chuyen <(i+1)*100>` (`M0` → `chuyen 100`, …, `M5` → `chuyen 600`). Sáu phản hồi về theo thứ tự mã tương quan: `M3, M5, M0, M1, M4, M2`.

Viết chương trình `GhepPhanHoi` (tệp `GhepPhanHoi.java`, khai `public class GhepPhanHoi` và `import java.util.*;` đầu tệp):
1. Một `Map<String, String>` từ mã thông điệp sang nội dung yêu cầu.
2. Với phản hồi thứ `k` (từ 0), in `phan hoi <k>: <mã> -> <yêu cầu tra được theo mã>`.
3. Đếm số phản hồi mà việc **ghép theo thứ tự đến** (coi phản hồi `k` là của `M<k>`) sẽ đúng, rồi in `dung neu ghep theo thu tu: <số>/6`.

Khung tệp:

```java
import java.util.*;
public class GhepPhanHoi {
    public static void main(String[] args) {
        // ... bản đồ, vòng lặp for, in kết quả
    }
}
```

Chạy: `javac GhepPhanHoi.java && java GhepPhanHoi`. Chấm: `bash labs/cham.sh BNK L10 GhepPhanHoi.java`.
""", "java", lab_tq["code"], lab_tq["out"])
    lab = practice_scene(sc, "Tự làm: sáu phản hồi lộn xộn", practice_steps(
        st, "BNK", "L10",
        """<p><b>Đề</b>: yêu cầu <code>Mi</code> là <code>chuyen (i+1)*100</code>; phản hồi về theo mã <code>M3 M5 M0 M1 M4 M2</code>. Viết <code>GhepPhanHoi.java</code>:</p>
<ol><li>bản đồ mã → yêu cầu</li>
<li>mỗi phản hồi in <code>phan hoi 0: M3 -&gt; chuyen 400</code></li>
<li>dòng cuối: số phản hồi đúng nếu ghép theo <b>thứ tự đến</b></li></ol>""",
        """Bây giờ tới phần bạn tự làm. Sáu yêu cầu mang mã từ M không tới M năm, nội dung là chuyển một trăm, hai trăm, cho tới sáu trăm. Sáu phản hồi về theo thứ tự mã M ba, M năm, M không, M một, M bốn, M hai.
        Hãy viết chương trình in cho mỗi phản hồi yêu cầu mà mã của nó chỉ tới, rồi đếm xem nếu ghép theo thứ tự đến thì đúng mấy phản hồi. Hãy dừng video và tự viết.""",
        lab_tq["out"], "GhepPhanHoi.java",
        """<div class="box key"><b>Nếu kẹt:</b> nạp bản đồ bằng vòng <code>for</code>: <code>cho.put("M" + i, "chuyen " + (i + 1) * 100);</code>. Với phản hồi thứ <code>k</code>, tra <code>cho.get(ve[k])</code>; ghép theo thứ tự đúng khi <code>ve[k].equals("M" + k)</code>.
Lời giải ở <code>labs/BNK/L10/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, nạp bản đồ bằng một vòng lặp, rồi với mỗi phản hồi tra bản đồ bằng chính mã của nó. Ghép theo thứ tự đến chỉ đúng khi mã của phản hồi thứ k đúng bằng M cộng k. Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=150), "BNK", "L10")
    return lesson("L10", "t24_ofs_ibm_mq_tuong_quan", "Bài 10 — Lõi ngân hàng T24: OFS, IBM MQ và mã tương quan",
                  "curriculum/bnk.yaml L10; audit/bnk/verify_bnk.py L10; audit/review/screen_code/BNK.yaml (mô phỏng bằng Java 21; T24 và IBM MQ không chạy trên máy: chỉ mô phỏng logic, không kiểm cú pháp sản phẩm); IBM MQ / JMS: MessageID và CorrelationID (khái niệm chung); Temenos: trang temenos.com/t24 ghi \"T24 is now Temenos Transact\" (tra 2026-11-16); OFS: tên gọi theo Temenos, bản tin trong bài là mẫu minh hoạ; kỳ vọng số điểm cố định của một hoán vị ngẫu nhiên bằng 1 (tổ hợp)",
                  ["Ghép phản hồi theo mã tương quan thay vì thứ tự đến", "Tính xác suất phản hồi không trùng thứ tự gửi bằng vét cạn",
                   "Xử lý đúng khi hết giờ chờ: truy vấn trạng thái trước", "Tránh nhiều bản dịch vụ lấy nhầm phản hồi của nhau",
                   "Chạy mô phỏng ghép phản hồi và hết giờ chờ để thấy số đúng và số lần ghi nợ",
                   "Tính số ghép sai kỳ vọng và số lệnh hết giờ chờ khi tải tăng ×100, ×10 000",
                   "Viết chương trình ghép phản hồi lộn xộn theo mã tương quan"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "chay_that"), (2, "check"), (3, "chay_that"), (4, "quy_mo"), (5, "chay_that"), (6, "quy_mo"), (7, "practice")], intro={('hook', 0): ['bnk_loi_ngan_hang', 'bnk_tuong_quan'], ('hook', 1): ['bnk_hach_toan']}, assumes=['bnk_ghi_no_co', 'bnk_luy_dang', 'bnk_ky_vong'])
