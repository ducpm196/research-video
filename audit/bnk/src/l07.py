from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    chia = prog("ChiaPhanVung", """
public class ChiaPhanVung {
    public static void main(String[] args) {
        int phanVung = 10, bo = 4, p = 0;
        for (int b = 0; b < bo; b++) {
            int so = phanVung / bo + (b < phanVung % bo ? 1 : 0);   // chia đều, phần dư chia cho các bộ đầu
            StringBuilder sb = new StringBuilder("bo doc " + b + ":");
            for (int k = 0; k < so; k++) sb.append(" P").append(p++);
            System.out.println(sb);
        }
    }
}""", out="""bo doc 0: P0 P1 P2
bo doc 1: P3 P4 P5
bo doc 2: P6 P7
bo doc 3: P8 P9""")
    ghi_nho = prog("GhiNho", """
import java.util.Arrays;
public class GhiNho {
    static int[] chay(boolean ghiNhoTruoc) {
        int[] dem = new int[5];                 // số lần xử lý mỗi thông điệp 0..4
        int viTri = 0;                          // vị trí đã ghi nhớ
        boolean daSap = false;
        while (viTri < 5) {
            int m = viTri;
            if (ghiNhoTruoc) {
                viTri = m + 1;                  // ghi nhớ trước
                if (m == 2 && !daSap) { daSap = true; continue; }   // sập: chưa kịp xử lý
                dem[m]++;
            } else {
                dem[m]++;                       // xử lý trước
                if (m == 2 && !daSap) { daSap = true; continue; }   // sập: chưa kịp ghi nhớ
                viTri = m + 1;
            }
        }
        return dem;
    }
    public static void main(String[] args) {
        System.out.println("ghi nho truoc: " + Arrays.toString(chay(true)));
        System.out.println("xu ly truoc:   " + Arrays.toString(chay(false)));
    }
}""", out="""ghi nho truoc: [1, 1, 0, 1, 1]
xu ly truoc:   [1, 1, 2, 1, 1]""")
    lab_nk = prog("NguoiNgoiKhong", """
public class NguoiNgoiKhong {
    public static void main(String[] args) {
        int phanVung = 7, bo = 9, p = 0, khong = 0;
        for (int b = 0; b < bo; b++) {
            int so = phanVung / bo + (b < phanVung % bo ? 1 : 0);
            StringBuilder sb = new StringBuilder("bo doc " + b + ":");
            if (so == 0) { sb.append(" ngoi khong"); khong++; }
            for (int k = 0; k < so; k++) sb.append(" P").append(p++);
            System.out.println(sb);
        }
        System.out.println("so nguoi ngoi khong: " + khong);
    }
}""", out="""bo doc 0: P0
bo doc 1: P1
bo doc 2: P2
bo doc 3: P3
bo doc 4: P4
bo doc 5: P5
bo doc 6: P6
bo doc 7: ngoi khong
bo doc 8: ngoi khong
so nguoi ngoi khong: 2""")
    hook = sc("hook", "hook", "Vì sao một thông điệp khi thì bị xử lý hai lần, khi thì mất hẳn?", [
        st("""<p>Một bộ đọc Kafka xử lý thông điệp số $2$ rồi <b>sập trước khi ghi nhớ</b> rằng đã đọc. Khi chạy lại, nó đọc thông điệp số $2$ <b>lần nữa</b>.</p>
<div class="box key">Đổi thứ tự “ghi nhớ trước, xử lý sau” thì thông điệp số $2$ lại <b>mất hẳn</b>.</div>""",
           """Chào bạn, một bộ đọc Kafka xử lý thông điệp số hai rồi sập, trước khi kịp ghi nhớ rằng đã đọc. Khi chạy lại, nó đọc thông điệp số hai lần nữa.
           Nếu đổi thứ tự, ghi nhớ trước rồi xử lý sau, thì thông điệp số hai lại mất hẳn."""),
        st(table(["thứ tự", "thông điệp số 2 được xử lý", "tên gọi"],
                 [["xử lý rồi ghi nhớ", "2 lần", "ít nhất một lần"],
                  ["ghi nhớ rồi xử lý", "0 lần", "nhiều nhất một lần"]]),
           """Bảng này là kết quả mô phỏng ở cuối bài. Xử lý rồi mới ghi nhớ thì thông điệp số hai được xử lý hai lần, gọi là ít nhất một lần.
           Ghi nhớ rồi mới xử lý thì có thể mất, gọi là nhiều nhất một lần. Hôm nay ta học cách sống chung với chuyện này."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Kafka và thông điệp", "Kafka là hệ thống chuyển thông điệp: bên gửi ghi thông điệp (một gói dữ liệu báo việc gì đó) vào nhật ký, bên đọc lấy ra xử lý", "“TK-1001 vừa nạp 50 000”"],
                  ["② Nhật ký chỉ thêm", "chỉ ghi nối vào cuối, không sửa dòng cũ", "thông điệp 0, 1, 2, 3, …"],
                  ["③ Số thứ tự (offset)", "vị trí của mỗi thông điệp trong nhật ký", "thông điệp thứ 2 có offset 2"],
                  ["④ Khoá thông điệp và băm chia dư", "khoá (key) là nhãn đi kèm thông điệp, ví dụ số tài khoản; hàm băm biến khoá thành một số (cùng khoá luôn ra cùng số), rồi chia dư để chọn ngăn (sau gọi là phân vùng)", "mã băm 13 chia 6 dư 1 → ngăn 1"]]),
           """Trước hết ta cần hiểu bốn điều. Kafka là hệ thống chuyển thông điệp. Bên gửi ghi thông điệp, tức một gói dữ liệu báo việc gì đó, vào nhật ký, còn bên đọc lấy ra xử lý.
           Nhật ký chỉ thêm là chỉ ghi nối vào cuối, không sửa dòng cũ. Số thứ tự cho biết vị trí của mỗi thông điệp trong nhật ký.
           Khoá thông điệp là nhãn đi kèm, ví dụ số tài khoản. Hàm băm biến khoá thành một số, và cùng khoá luôn ra cùng số. Rồi ta chia dư để chọn một ngăn, ví dụ mười ba chia sáu dư một thì vào ngăn một, mỗi ngăn sau này gọi là một phân vùng."""),
        st("""$$13 = 2 \\cdot 6 + 1$$""",
           """Kiểm phép chia dư. Mười ba bằng hai nhân sáu cộng một, nên mười ba chia sáu dư một."""),
    ], checks=["13 == 2 * 6 + 1 and 13 % 6 == 1"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["topic", "một luồng thông điệp có tên, ví dụ giao dịch chuyển tiền"],
                  ["partition (phân vùng)", "một nhật ký thật của topic; topic gồm nhiều phân vùng chạy song song"],
                  ["consumer group", "nhóm bộ đọc cùng chia nhau các phân vùng của topic"],
                  ["rebalance", "chia lại phân vùng khi có bộ đọc vào hoặc ra khỏi nhóm"],
                  ["commit offset", "ghi nhớ đã đọc tới đâu để lần sau đọc tiếp"]]),
           """Bảng này giải mã năm từ. Topic là một luồng thông điệp có tên. Phân vùng là một nhật ký thật của topic, và topic gồm nhiều phân vùng chạy song song.
           Nhóm bộ đọc là các bộ đọc cùng chia nhau phân vùng. Chia lại là khi có bộ đọc vào hay ra khỏi nhóm. Còn ghi nhớ vị trí là lưu lại đã đọc tới đâu."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: phân vùng, nhóm bộ đọc và chia lại", [
        st(svg(1500, 420,
               panel(40, 30, 760, 360, "Topic có 6 phân vùng", C_AMBER),
               box(70, 100, 320, 50, "P0: 0 1 2 3 …", C_GRAY, size=22), box(410, 100, 360, 50, "P1: 0 1 2 …", C_GRAY, size=22),
               box(70, 170, 320, 50, "P2: 0 1 2 3 …", C_GRAY, size=22), box(410, 170, 360, 50, "P3: 0 1 …", C_GRAY, size=22),
               box(70, 240, 320, 50, "P4: 0 1 2 …", C_GRAY, size=22), box(410, 240, 360, 50, "P5: 0 1 2 3 …", C_GRAY, size=22),
               panel(900, 30, 560, 360, "Nhóm bộ đọc: 3 người", C_GREEN),
               box(940, 100, 480, 70, "Đọc 1: P0, P1", C_BLUE), box(940, 190, 480, 70, "Đọc 2: P2, P3", C_BLUE), box(940, 280, 480, 70, "Đọc 3: P4, P5", C_BLUE)),
           """Hình cho thấy topic có sáu phân vùng, mỗi phân vùng là một nhật ký riêng. Nhóm có ba bộ đọc, mỗi bộ đọc nhận hai phân vùng.
           Quy tắc quan trọng là mỗi phân vùng chỉ có một bộ đọc trong nhóm, nên thứ tự trong phân vùng được giữ."""),
        st(svg(1500, 420,
               panel(40, 30, 700, 360, "Trước: 3 người", C_GREEN),
               box(70, 100, 640, 60, "Đọc 1: P0, P1", C_BLUE), box(70, 180, 640, 60, "Đọc 2: P2, P3", C_BLUE, dash=True), box(70, 260, 640, 60, "Đọc 3: P4, P5", C_BLUE),
               arrow(750, 210, 810, 210, "#dc2626"),
               panel(820, 30, 640, 360, "Sau khi Đọc 2 rời nhóm", C_AMBER),
               box(850, 100, 580, 60, "Đọc 1: P0, P1, P2", C_BLUE), box(850, 200, 580, 60, "Đọc 3: P3, P4, P5", C_BLUE),
               txt(1140, 320, "chia lại (rebalance): mỗi người 3 phân vùng", 24, "middle", "#1f2937", True)),
           """Khi một bộ đọc rời nhóm, hệ thống chia lại. Còn hai bộ đọc, nên sáu phân vùng chia thành ba cho mỗi người.
           Trong lúc chia lại, việc đọc có thể tạm dừng, và các thông điệp chưa ghi nhớ vị trí có thể bị đọc lại."""),
        st(svg(1500, 400,
               box(60, 70, 320, 80, "đọc thông điệp", C_BLUE), box(480, 70, 320, 80, "xử lý", C_GREEN), box(900, 70, 320, 80, "ghi nhớ vị trí", C_AMBER),
               arrow(380, 110, 475, 110), arrow(800, 110, 895, 110),
               txt(750, 210, "Sập giữa “xử lý” và “ghi nhớ” → khởi động lại đọc lại → xử lý hai lần", 26, "middle", "#dc2626", True),
               box(60, 260, 320, 80, "đọc thông điệp", C_BLUE), box(480, 260, 320, 80, "ghi nhớ vị trí", C_AMBER), box(900, 260, 320, 80, "xử lý", C_GREEN),
               arrow(380, 300, 475, 300), arrow(800, 300, 895, 300),
               txt(750, 385, "Sập giữa “ghi nhớ” và “xử lý” → khởi động lại bỏ qua → mất thông điệp", 26, "middle", "#dc2626", True)),
           """Hình thứ ba cho thấy hai thứ tự. Hàng trên, xử lý rồi mới ghi nhớ. Sập ở giữa thì khi chạy lại sẽ đọc lại, nên xử lý hai lần.
           Hàng dưới, ghi nhớ rồi mới xử lý. Sập ở giữa thì khi chạy lại sẽ bỏ qua, nên mất thông điệp."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: chia việc và số lần xử lý", [
        st("""<p><b>Bước 1.</b> Cùng khoá băm ra cùng phân vùng, <b>miễn là số phân vùng không đổi</b>, nên thông điệp cùng một tài khoản nằm cùng một phân vùng và <b>giữ đúng thứ tự</b>.</p>
<span class='note'>Làm thử: khoá TK-1001 hai lần đều vào phân vùng 1. Thêm phân vùng thì khoá có thể chuyển sang phân vùng khác.</span>""",
           """Bước một, vì cùng khoá băm ra cùng phân vùng, miễn là số phân vùng không đổi, nên thông điệp của cùng một tài khoản nằm cùng một phân vùng và giữ đúng thứ tự. Làm thử, khoá T K một không không một hai lần đều vào phân vùng một.
           Nếu thêm phân vùng, phép chia dư đổi, và khoá có thể chuyển sang phân vùng khác."""),
        st("""<p><b>Bước 2.</b> Mỗi phân vùng chỉ một bộ đọc trong nhóm, nên số bộ đọc làm việc thật sự tối đa bằng <b>số phân vùng</b>.</p>
<span class='note'>Làm thử: $6$ phân vùng, $8$ bộ đọc → $6$ làm việc, $2$ ngồi không.</span>""",
           """Bước hai, vì mỗi phân vùng chỉ có một bộ đọc trong nhóm, nên số bộ đọc làm việc tối đa bằng số phân vùng. Làm thử, sáu phân vùng mà tám bộ đọc thì sáu người làm việc, hai người ngồi không."""),
        st("""<p><b>Bước 3.</b> Số lần xử lý một thông điệp phụ thuộc <b>thứ tự</b> giữa xử lý và ghi nhớ khi sập: xử lý trước thì $\\ge 1$ lần, ghi nhớ trước thì $\\le 1$ lần.</p>
<span class='note'>Muốn đúng một lần về hiệu quả: xử lý trước, ghi nhớ sau, và để việc xử lý lũy đẳng.</span>""",
           """Bước ba, vì khi sập, thứ tự giữa xử lý và ghi nhớ quyết định kết quả, nên xử lý trước thì ít nhất một lần, ghi nhớ trước thì nhiều nhất một lần. Muốn hiệu quả đúng một lần, ta xử lý trước, ghi nhớ sau, và làm việc xử lý lũy đẳng."""),
    ], checks=["[alg.bnk_key_partition(k, 6) for k in ('TK-1001', 'TK-1001')] == [1, 1]", "len(alg.bnk_assign(6, 8)[6]) + len(alg.bnk_assign(6, 8)[7]) == 0 and sum(1 for g in alg.bnk_assign(6, 8) if g) == 6",
               "alg.bnk_commit_sim(5, 2, False)[2] >= 1 and alg.bnk_commit_sim(5, 2, True)[2] <= 1"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Topic $6$ phân vùng, nhóm $3$ bộ đọc: chia đều.</p>
$$① \\; \\frac{6}{3} = \\hl{2}\\ \\text{phân vùng mỗi người}$$""",
           """Ta tính bốn tình huống. Tình huống một, topic sáu phân vùng, nhóm ba bộ đọc, chia đều thì mỗi người nhận sáu chia ba, là hai phân vùng."""),
        st("""<p>Một người rời nhóm, còn $2$ người.</p>
$$② \\; \\frac{6}{2} = \\hl{3}\\ \\text{phân vùng mỗi người}$$""",
           """Tình huống hai, một người rời nhóm, còn hai người. Mỗi người nhận sáu chia hai, là ba phân vùng."""),
        st("""<p>Thêm người cho đủ $8$ bộ đọc.</p>
$$③ \\; 8 - 6 = \\hl{2}\\ \\text{người ngồi không}$$""",
           """Tình huống ba, thêm người cho đủ tám bộ đọc. Chỉ có sáu phân vùng nên hai người ngồi không, tám trừ sáu bằng hai."""),
        st("""<p>Năm thông điệp $0..4$, ghi nhớ vị trí sau từng thông điệp. Sập ở thông điệp $2$, thứ tự <b>xử lý rồi ghi nhớ</b>.</p>
$$④ \\; \\text{số lần xử lý} = [1, 1, \\hl{2}, 1, 1]\\quad \\text{tổng } 6$$
<p class="small">Ghi nhớ theo lô nhiều thông điệp một lần thì còn nhiều thông điệp bị xử lý lại hơn.</p>""",
           """Tình huống bốn, năm thông điệp từ không tới bốn, và bộ đọc ghi nhớ vị trí sau từng thông điệp. Sập ở thông điệp hai, thứ tự xử lý rồi ghi nhớ. Số lần xử lý là một, một, hai, một, một, tổng cộng sáu lần cho năm thông điệp.
           Nếu ghi nhớ theo lô nhiều thông điệp một lần, số thông điệp bị xử lý lại còn nhiều hơn.""", clear=True),
        st("""<p>Cùng tình huống nhưng <b>ghi nhớ rồi xử lý</b>.</p>
$$⑤ \\; \\text{số lần xử lý} = [1, 1, \\hl{0}, 1, 1]\\quad \\text{tổng } 4$$""",
           """Tình huống năm, cùng tình huống nhưng ghi nhớ rồi mới xử lý. Số lần xử lý là một, một, không, một, một, tổng bốn lần, tức là mất thông điệp số hai."""),
    ], checks=["6 // 3 == 2 and alg.bnk_assign(6, 3) == [[0, 1], [2, 3], [4, 5]]", "6 // 2 == 3 and alg.bnk_assign(6, 2) == [[0, 1, 2], [3, 4, 5]]",
               "8 - 6 == 2", "alg.bnk_commit_sim(5, 2, False) == [1, 1, 2, 1, 1] and sum(alg.bnk_commit_sim(5, 2, False)) == 6",
               "alg.bnk_commit_sim(5, 2, True) == [1, 1, 0, 1, 1] and sum(alg.bnk_commit_sim(5, 2, True)) == 4"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: khử trùng ở phía xử lý", [
        st("""<p>Đường khác: giữ <b>tập các mã đã xử lý</b>. Thông điệp số $2$ đến hai lần, nhưng lần hai gặp mã đã có nên bỏ qua.</p>
$$\\text{số thông điệp xử lý thật} = \\hlg{5}$$""",
           """Kiểm bằng đường khác. Vì thông điệp đến ít nhất một lần, nên ta giữ tập các mã đã xử lý. Thông điệp số hai đến hai lần, nhưng lần hai gặp mã đã có nên bị bỏ qua. Kết quả là năm thông điệp được xử lý thật, đúng mỗi thông điệp một lần."""),
        st(table(["cách", "xử lý thật mỗi thông điệp", "điều kiện"],
                 [["ít nhất một lần + khử trùng", "đúng 1 lần (về hiệu quả)", "mã thông điệp duy nhất, kho mã bền; ghi mã đã xử lý và tác dụng nghiệp vụ trong cùng một giao dịch cơ sở dữ liệu"],
                  ["nhiều nhất một lần", "0 hoặc 1 lần", "chấp nhận mất"]]),
           """Bảng này so hai cách. Vì thông điệp đã đến ít nhất một lần, nên khử trùng cho hiệu quả đúng một lần, với điều kiện mã thông điệp duy nhất và kho mã bền.
           Mã đã xử lý và tác dụng nghiệp vụ phải được ghi trong cùng một giao dịch cơ sở dữ liệu, nếu không thì sập ở giữa vẫn trùng hoặc mất.
           Nhiều nhất một lần thì có thể mất, chỉ dùng khi chấp nhận mất."""),
    ], checks=["len(set(i for i, c in enumerate(alg.bnk_commit_sim(5, 2, False)) for _ in range(c))) == 5"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ thêm bộ đọc là nhanh hơn mãi. Quá số phân vùng, các bộ đọc thừa <b class="red">ngồi không</b>.</div>""",
           """Lỗi thứ nhất, của người mới. Nghĩ thêm bộ đọc là nhanh hơn mãi. Quá số phân vùng thì các bộ đọc thừa ngồi không."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Xử lý quá lâu</b> trong một lần đọc. Bộ đọc bị coi là chết, nhóm chia lại, thông điệp đang xử lý bị giao cho người khác và <b>xử lý hai lần</b>.
<br><span class="note">Cách chữa: gọi <code>poll()</code> (lệnh lấy thông điệp) lại trong hạn <code>max.poll.interval.ms</code> (hạn tối đa giữa hai lần lấy; giảm <code>max.poll.records</code>, số thông điệp mỗi lần lấy, hoặc tăng hạn), và làm việc xử lý lũy đẳng.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là xử lý quá lâu trong một lần đọc. Bộ đọc bị coi là chết, nhóm chia lại, thông điệp đang xử lý bị giao cho người khác và xử lý hai lần.
           Nhịp báo còn sống chạy ở một luồng riêng, nên lỗi này là do quá hạn giữa hai lần đọc. Cách chữa là đọc lại trong hạn cho phép, bằng cách lấy ít thông điệp hơn mỗi lần hoặc tăng hạn, và làm việc xử lý lũy đẳng."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nghe “đúng một lần” của Kafka rồi tin mọi tác dụng phụ chỉ xảy ra một lần. Giao dịch của Kafka chỉ bao trùm đọc, xử lý, ghi <b>trong Kafka</b>.
Ghi vào cơ sở dữ liệu hay gọi hệ ngoài vẫn cần khoá lũy đẳng.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là nghe đúng một lần của Kafka rồi tin mọi tác dụng phụ chỉ xảy ra một lần. Giao dịch của Kafka chỉ bao trùm việc đọc, xử lý và ghi bên trong Kafka.
           Ghi vào cơ sở dữ liệu hay gọi hệ ngoài vẫn cần khoá lũy đẳng."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "10 phân vùng, 4 bộ đọc, chia khoảng liền nhau; phần dư chia cho những người đầu, mỗi người thêm một. Mỗi người nhận mấy phân vùng?"],
                  ["2", "10 phân vùng, 12 bộ đọc. Mấy người ngồi không?"],
                  ["3", "Quyết định: lệnh trừ tiền nên ghi nhớ vị trí trước hay sau khi xử lý?"]]),
           """Đến lượt bạn. Câu một, mười phân vùng, bốn bộ đọc, chia liền nhau và phần dư chia cho những người đầu, mỗi người thêm một, vậy mỗi người nhận mấy phân vùng? Câu hai, mười phân vùng, mười hai bộ đọc, mấy người ngồi không?
           Câu ba, lệnh trừ tiền nên ghi nhớ vị trí trước hay sau khi xử lý? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: $10 = 4 \\cdot 2 + 2$, nên hai người đầu nhận $3$, hai người sau nhận $2$.</p>
$$[3, 3, 2, 2]\\quad 3 + 3 + 2 + 2 = \\hl{10}$$""",
           """Đáp án câu một. Mười bằng bốn nhân hai cộng hai, nên hai người đầu nhận ba phân vùng, hai người sau nhận hai. Ba cộng ba cộng hai cộng hai bằng mười."""),
        st("""$$12 - 10 = \\hlg{2}\\ \\text{người ngồi không}$$""",
           """Đáp án câu hai. Mười hai bộ đọc trừ mười phân vùng, nên hai người ngồi không."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["xử lý rồi ghi nhớ + khoá lũy đẳng", "không mất lệnh, trùng thì bị chặn", "phải làm khoá lũy đẳng"],
                  ["ghi nhớ rồi xử lý", "không bao giờ xử lý hai lần", "có thể mất lệnh trừ tiền"]]),
           """Đáp án câu ba. Với lệnh trừ tiền, mất lệnh nguy hiểm hơn trùng lệnh, vì trùng ta chặn được bằng khoá lũy đẳng. Nên chọn xử lý rồi mới ghi nhớ, kèm khoá lũy đẳng."""),
    ], checks=["[len(g) for g in alg.bnk_assign(10, 4)] == [3, 3, 2, 2]", "12 - 10 == 2 and sum(1 for g in alg.bnk_assign(10, 12) if not g) == 2"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("khoá → phân vùng", "mỗi phân vùng một bộ đọc", "sập → đọc lại", "xử lý lũy đẳng"),
           """Tổng kết chuỗi logic. Khoá quyết định phân vùng. Mỗi phân vùng chỉ một bộ đọc. Sập thì đọc lại, nên việc xử lý phải lũy đẳng."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng hỏi “Kafka có đúng một lần không”. Hãy hỏi <b>“khi sập giữa chừng, việc của tôi chạy mấy lần, và có hại không?”</b></div>""",
           """Điều cần mang theo. Đừng hỏi Kafka có đúng một lần không. Hãy hỏi, khi sập giữa chừng, việc của tôi chạy mấy lần, và có hại không."""),
    ])
    # ── AF2: P1 nhịp báo còn sống và tác dụng phụ, mô phỏng Kafka bằng Java (chia phân vùng, thứ tự ghi nhớ), quy mô, tự làm ──
    add_steps([pre], "prereq", [
        st(table(["thêm hai điều", "nghĩa", "ví dụ"],
                 [["⑤ Nhịp báo còn sống (heartbeat)", "tín hiệu gửi đều đặn để nhóm biết một bộ đọc chưa chết; ngừng gửi quá hạn thì bị coi là chết và nhóm chia lại việc", "mỗi 3 giây một nhịp"],
                  ["⑥ Tác dụng phụ", "việc làm thay đổi thứ ở bên ngoài chương trình, như ghi cơ sở dữ liệu, gửi thư, gọi hệ khác; khác với việc chỉ tính toán rồi bỏ", "trừ tiền trong cơ sở dữ liệu"]]),
           """Thêm hai điều nữa. Nhịp báo còn sống là tín hiệu gửi đều đặn để nhóm biết một bộ đọc chưa chết. Nếu ngừng gửi quá hạn, bộ đọc bị coi là chết và nhóm chia lại việc.
           Tác dụng phụ là việc làm thay đổi thứ ở bên ngoài chương trình, như ghi cơ sở dữ liệu, gửi thư hay gọi hệ khác, khác với việc chỉ tính toán rồi bỏ kết quả.""", clear=True),
    ], at=1)
    pre["title"] = "Trước hết: sáu điều cần hiểu"
    run = sc("chay_that", "example", "Chạy thật: chia phân vùng và thứ tự ghi nhớ (mô phỏng bằng Java)", [
        st(code_block(chia, lines=(3, 9), title="ChiaPhanVung.java (phần chính): 10 phân vùng cho 4 bộ đọc"),
           """Kafka thật cần cài riêng, nên ta mô phỏng cơ chế bằng Java. Đoạn này chia mười phân vùng cho bốn bộ đọc. Mỗi bộ được số phân vùng bằng mười chia nguyên cho bốn, tức hai, và các bộ đầu nhận thêm một nếu còn dư.
           Mười chia bốn dư hai, nên hai bộ đầu nhận ba phân vùng, hai bộ sau nhận hai."""),
        st(out_block(chia),
           """Khi chạy thật, bộ đọc không và một nhận ba phân vùng, bộ hai và ba nhận hai. Đúng với phép tính tay: ba cộng ba cộng hai cộng hai bằng mười, không phân vùng nào bị thiếu hay trùng.""", clear=True),
        st(code_block(ghi_nho, lines=(3, 12), title="GhiNho.java (phần 1): thông điệp 2 làm bộ đọc sập đúng một lần"),
           """Bây giờ là thứ tự ghi nhớ và xử lý. Hàm này xử lý năm thông điệp và đếm số lần mỗi thông điệp được xử lý. Nếu ghi nhớ trước, thì sập ở thông điệp hai khi vị trí đã lưu nhưng chưa xử lý.
           Lần khởi động lại sau đó bắt đầu sau thông điệp hai, nên thông điệp hai bị mất.""", clear=True),
        st(code_block(ghi_nho, lines=(13, 23), title="Phần 2: xử lý trước, ghi nhớ sau, rồi so hai cách"),
           """Nếu xử lý trước rồi ghi nhớ sau, thì sập ở thông điệp hai khi đã xử lý nhưng chưa lưu vị trí. Lần khởi động lại đọc lại từ thông điệp hai, nên nó bị xử lý hai lần.
           Hàm chính in số lần xử lý của năm thông điệp cho cả hai cách.""", clear=True),
        st(out_block(ghi_nho),
           """Khi chạy thật, ghi nhớ trước cho số lần là một, một, không, một, một: thông điệp hai bị mất. Xử lý trước cho một, một, hai, một, một: thông điệp hai bị xử lý hai lần.
           Vì thế người làm nghề chọn xử lý trước, ghi nhớ sau, rồi khử trùng ở phía xử lý, thay vì chấp nhận mất tiền.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: một phân vùng, một bộ đọc, và khối việc tồn đọng", [
        st("""<p>Mỗi phân vùng được <b>một</b> bộ đọc trong nhóm xử lý, với tốc độ $1\\,000$ thông điệp mỗi giây <i>(số minh hoạ)</i>. Số phân vùng tối thiểu bằng tải chia tốc độ một bộ đọc. Nếu chỉ có $4$ phân vùng, thông điệp xử lý được $4\\,000$ mỗi giây, phần còn lại đọng lại sau một giờ ($3\\,600$ giây):</p>"""
           + table(["tải", "thông điệp mỗi giây", "phân vùng tối thiểu", "chỉ 4 phân vùng: tồn đọng sau 1 giờ"],
                   [["×1", "5 000", "5", "3 600 000"],
                    ["×100", "500 000", "500", "<b>≈ 1,79 tỉ</b>"],
                    ["×10 000", "50 000 000", "50 000", "<b>≈ 180 tỉ</b>"]]),
           """Mỗi phân vùng được một bộ đọc trong nhóm xử lý, với tốc độ một nghìn thông điệp mỗi giây, đây là số minh hoạ. Số phân vùng tối thiểu bằng tải chia tốc độ của một bộ đọc.
           Với năm nghìn thông điệp mỗi giây, cần năm phân vùng. Nếu chỉ có bốn, mỗi giờ đọng lại ba triệu sáu trăm nghìn thông điệp. Tải tăng một trăm lần cần năm trăm phân vùng, và bốn phân vùng đọng hơn một phẩy bảy chín tỉ thông điệp.
           Tải tăng mười nghìn lần cần năm mươi nghìn phân vùng.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Thêm bộ đọc mà không thêm phân vùng không giúp gì: bộ đọc thừa ngồi không. Thêm phân vùng thì <b>cùng khoá có thể sang phân vùng khác</b> (băm chia dư cho số mới), nên thứ tự theo khoá bị phá lúc chuyển.
Số phân vùng lại <b>không giảm được</b> về sau.</div>
<div class="box key"><b>Đánh đổi:</b> chọn số phân vùng dư vừa phải ngay từ đầu, theo tải dự kiến vài năm. Nhiều phân vùng quá thì mỗi lần chia lại lâu hơn và tốn thêm tệp mở; ít quá thì nghẽn như bảng trên.</div>""",
           """Câu hỏi là giải pháp cũ sẽ gãy ở chỗ nào khi tải tăng lên. Thêm bộ đọc mà không thêm phân vùng không giúp gì, vì bộ đọc thừa ngồi không. Thêm phân vùng thì cùng một khoá có thể sang phân vùng khác, vì băm chia dư theo số phân vùng mới, nên thứ tự theo khoá bị phá lúc chuyển.
           Số phân vùng cũng không giảm được về sau. Đánh đổi là chọn số phân vùng dư vừa phải ngay từ đầu, theo tải dự kiến vài năm. Nhiều quá thì mỗi lần chia lại lâu hơn và tốn thêm tệp mở, còn ít quá thì nghẽn như bảng trên.""", clear=True),
    ], checks=["5000 / 1000 == 5", "500000 / 1000 == 500", "50000000 / 1000 == 50000", "(5000 - 4000) * 3600 == 3_600_000",
               "(500_000 - 4000) * 3600 == 1_785_600_000", "(50_000_000 - 4000) * 3600 == 179_985_600_000"])
    write_lab("BNK", "L07", """# Lab BNK L07 — Bảy phân vùng, chín bộ đọc

Một chủ đề có **7 phân vùng** `P0 … P6`, một nhóm có **9 bộ đọc** `0 … 8`. Chia đều: mỗi bộ nhận `phanVung / bo` phân vùng, và **bộ có số thứ tự nhỏ hơn `phanVung % bo`** nhận thêm một; phân vùng phát liên tiếp từ `P0`.

Viết chương trình `NguoiNgoiKhong` (tệp `NguoiNgoiKhong.java`):
1. Với mỗi bộ đọc in một dòng `bo doc <số>:` rồi danh sách phân vùng (mỗi cái ` P<số>`), hoặc ` ngoi khong` nếu bộ không nhận phân vùng nào.
2. Dòng cuối: `so nguoi ngoi khong: <số>`.

Chạy: `javac NguoiNgoiKhong.java && java NguoiNgoiKhong`. Chấm: `bash labs/cham.sh BNK L07 NguoiNgoiKhong.java`.
""", "java", lab_nk["code"], lab_nk["out"])
    lab = practice_scene(sc, "Tự làm: bảy phân vùng, chín bộ đọc", practice_steps(
        st, "BNK", "L07",
        """<p><b>Đề</b>: 7 phân vùng, 9 bộ đọc; mỗi bộ nhận <code>7 / 9</code> phân vùng, bộ có số nhỏ hơn <code>7 % 9</code> nhận thêm một. Viết <code>NguoiNgoiKhong.java</code>:</p>
<ol><li>mỗi bộ đọc in <code>bo doc 0: P0</code> …; bộ không nhận gì in <code>ngoi khong</code></li>
<li>dòng cuối <code>so nguoi ngoi khong: …</code></li></ol>""",
        """Bây giờ tới phần bạn tự làm. Một chủ đề có bảy phân vùng, một nhóm có chín bộ đọc. Mỗi bộ nhận bảy chia nguyên cho chín phân vùng, và bộ có số thứ tự nhỏ hơn phần dư nhận thêm một. Phân vùng được phát liên tiếp từ không.
        Hãy in cho mỗi bộ đọc một dòng, bộ không nhận gì thì ghi ngồi không, và dòng cuối là số người ngồi không. Hãy dừng video, tự viết và chạy, đừng chép lại ví dụ.""",
        lab_nk["out"], "NguoiNgoiKhong.java",
        """<div class="box key"><b>Nếu kẹt:</b> mô theo <code>ChiaPhanVung</code>: <code>int so = phanVung / bo + (b &lt; phanVung % bo ? 1 : 0);</code>. Nếu <code>so == 0</code> thì thêm chữ <code>ngoi khong</code> và tăng biến đếm.
Lời giải ở <code>labs/BNK/L07/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, làm theo mẫu chia phân vùng vừa xem. Nếu số phân vùng của một bộ bằng không thì ghi ngồi không và tăng biến đếm. Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=150), "BNK", "L07")
    return lesson("L07", "kafka_partition_offset", "Bài 7 — Kafka: phân vùng, offset, chia lại và số lần xử lý",
                  "curriculum/bnk.yaml L07; audit/bnk/verify_bnk.py L07; audit/review/screen_code/BNK.yaml (mô phỏng bằng Java 21, Kafka thật không chạy trong bài: chỉ mô phỏng logic); Apache Kafka documentation (consumer groups, delivery semantics, số phân vùng chỉ tăng, không giảm; đổi số phân vùng đổi ánh xạ khoá → phân vùng); băm crc32 chỉ để tất định, Kafka dùng murmur2",
                  ["Chia phân vùng cho nhóm bộ đọc và tính số người ngồi không", "Nêu vì sao cùng khoá giữ đúng thứ tự",
                   "Dự đoán số lần xử lý theo thứ tự ghi nhớ và xử lý khi sập", "Khử trùng ở phía xử lý để được hiệu quả đúng một lần",
                   "Chạy mô phỏng chia phân vùng và thứ tự ghi nhớ để thấy số lần xử lý",
                   "Tính số phân vùng tối thiểu và khối thông điệp tồn đọng khi tải tăng ×100, ×10 000",
                   "Viết chương trình chia phân vùng cho nhóm bộ đọc và đếm người ngồi không"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "chay_that"), (2, "intuition"), (3, "example"), (4, "check"), (5, "chay_that"), (6, "quy_mo"), (7, "practice")])
