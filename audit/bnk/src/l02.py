from lib import *
from labkit import write_lab, practice_steps, practice_scene


PROXY_SRC = """
import java.lang.reflect.*;
public class ProxyGiaoDich {
    interface Dich { void chuyenTien(); void ghiVet(); }
    static int moGiaoDich = 0;
    static class DichThat implements Dich {
        public void chuyenTien() { ghiVet(); }      // gọi thẳng: this.ghiVet(), không qua proxy
        public void ghiVet() { System.out.println("  ghiVet chay"); }
    }
    public static void main(String[] args) {
        Dich that = new DichThat();
        Dich proxy = (Dich) Proxy.newProxyInstance(Dich.class.getClassLoader(), new Class<?>[] { Dich.class },
            (p, m, a) -> {
                moGiaoDich++;                       // proxy mở giao dịch trước khi vào hàm thật
                System.out.println("proxy mo giao dich cho " + m.getName());
                return m.invoke(that, a);
            });
        proxy.chuyenTien();
        System.out.println("so giao dich: " + moGiaoDich);
        proxy.ghiVet();
        System.out.println("so giao dich: " + moGiaoDich);
    }
}"""

LAB_SRC = """
import java.lang.reflect.*;
public class ChuyenKhoanProxy {
    interface Dich { void chuyenKhoan(); void tinhPhi(); void thongBao(); }
    static int moGiaoDich = 0;
    static class DichThat implements Dich {
        public void chuyenKhoan() { tinhPhi(); thongBao(); }   // hai lời gọi thẳng bằng this
        public void tinhPhi() { }
        public void thongBao() { }
    }
    public static void main(String[] args) {
        Dich that = new DichThat();
        Dich proxy = (Dich) Proxy.newProxyInstance(Dich.class.getClassLoader(), new Class<?>[] { Dich.class },
            (p, m, a) -> {
                moGiaoDich++;
                return m.invoke(that, a);
            });
        proxy.chuyenKhoan();
        System.out.println("sau chuyenKhoan: " + moGiaoDich);
        proxy.tinhPhi();
        System.out.println("sau tinhPhi: " + moGiaoDich);
        proxy.thongBao();
        System.out.println("sau thongBao: " + moGiaoDich);
    }
}"""


def build():
    pgd = prog("ProxyGiaoDich", PROXY_SRC, out="""proxy mo giao dich cho chuyenTien
  ghiVet chay
so giao dich: 1
proxy mo giao dich cho ghiVet
  ghiVet chay
so giao dich: 2""")
    lab_proxy = prog("ChuyenKhoanProxy", LAB_SRC, out="""sau chuyenKhoan: 1
sau tinhPhi: 2
sau thongBao: 3""")
    hook = sc("hook", "hook", "Vì sao dòng ghi vết vẫn mất dù đã gắn nhãn giao dịch?", [
        st("""<p>Một lệnh chuyển tiền thất bại giữa chừng. Lập trình viên gắn <code>@Transactional</code> lên hàm chuyển tiền, và nhãn giao dịch <b>luôn mở giao dịch mới</b> lên hàm ghi vết, vậy mà dòng ghi vết <b>không còn</b> trong bảng.</p>
<div class="box key">Hôm nay ta trả lời: Spring <b>tạo và nối</b> các đối tượng thế nào, <b>proxy</b> là gì, và vì sao nhãn giao dịch đôi khi <b>không có tác dụng</b>.</div>""",
           """Chào bạn, một lệnh chuyển tiền thất bại giữa chừng. Lập trình viên đã gắn nhãn giao dịch lên hàm chuyển tiền, và nhãn luôn mở giao dịch mới lên hàm ghi vết,
           vậy mà dòng ghi vết không còn trong bảng.
           Hôm nay ta trả lời ba câu. Spring tạo và nối các đối tượng thế nào, proxy là gì, và vì sao nhãn giao dịch đôi khi không có tác dụng."""),
        st(table(["cách gọi hàm ghi vết (nhãn luôn mở giao dịch mới)", "giao dịch đã mở", "dòng ghi vết sau khi chuyển tiền hỏng"],
                 [["gọi thẳng trong cùng lớp", "1", "mất"],
                  ["gọi qua một bean khác (qua proxy)", "2", "còn"]]),
           """Bảng này là kết quả mô phỏng ở cuối bài, khi hàm ghi vết mang nhãn luôn mở giao dịch mới. Nếu hàm ghi vết được gọi thẳng trong cùng lớp, chỉ có một giao dịch được mở và dòng ghi vết mất theo.
           Nếu gọi qua một bean khác, tức là qua proxy, có hai giao dịch và dòng ghi vết còn lại."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Lớp và đối tượng", "lớp là khuôn, đối tượng là bản làm ra từ khuôn; hàm viết trong lớp gọi là phương thức", "lớp TaiKhoan, đối tượng tài khoản số 1"],
                  ["② Một hàm gọi hàm khác", "phương thức A có thể gọi phương thức B của chính đối tượng đó hoặc của đối tượng khác", "chuyenTien gọi ghiVet"],
                  ["③ Giao dịch", "một nhóm thao tác ghi vào cơ sở dữ liệu (phần mềm lưu dữ liệu lâu dài thành các bảng, mỗi bảng nhiều dòng): hoặc cùng thành công, hoặc cùng huỷ", "trừ tiền và cộng tiền cùng lúc"]]),
           """Trước hết ta cần hiểu bốn điều. Lớp là cái khuôn, đối tượng là bản làm ra từ khuôn, và một hàm viết trong lớp gọi là phương thức.
           Một phương thức có thể gọi phương thức khác của chính đối tượng đó, hoặc của đối tượng khác, ví dụ chuyển tiền gọi ghi vết.
           Cơ sở dữ liệu là phần mềm lưu dữ liệu lâu dài thành các bảng, mỗi bảng gồm nhiều dòng.
           Giao dịch là nhóm thao tác ghi vào cơ sở dữ liệu mà hoặc cùng thành công, hoặc cùng bị huỷ, ví dụ trừ tiền và cộng tiền."""),
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["④ Ngoại lệ (exception)", "đối tượng báo lỗi được “ném” ra; phương thức dừng ngay, lỗi bay ngược lên người gọi tới khi có chỗ bắt (<code>try … catch</code>)", "<code>throw new RuntimeException(\"hết tiền\")</code>"],
                  ["loại không bắt buộc xử lý", "<code>RuntimeException</code> và các lớp con: Java không bắt phải khai báo hay bắt", "chia cho 0, số dư âm"],
                  ["loại bắt buộc xử lý (checked)", "Java buộc người viết phải bắt hoặc khai báo <code>throws</code>", "<code>IOException</code> khi đọc tệp"]]),
           """Điều thứ tư là ngoại lệ. Ngoại lệ là một đối tượng báo lỗi được ném ra. Phương thức đang chạy dừng ngay, và lỗi bay ngược lên người gọi, cho tới khi có chỗ bắt nó.
           Java chia ngoại lệ làm hai loại. Loại thời gian chạy thì Java không bắt buộc phải khai báo hay bắt, ví dụ lỗi số dư âm do ta tự ném.
           Loại bắt buộc xử lý thì người viết phải bắt hoặc khai báo, ví dụ lỗi khi đọc tệp.""", clear=True),
        st("""$$-500\\,000 + 500\\,000 = 0$$""",
           """Một ví dụ số cho giao dịch. Trừ năm trăm nghìn ở một tài khoản và cộng năm trăm nghìn ở tài khoản kia, tổng bằng không. Nếu chỉ làm một nửa, sổ sách lệch."""),
    ], checks=["-500000 + 500000 == 0"])
    sym = sc("sym", "symbol", "Giải mã vài từ trong Spring", [
        st(table(["từ", "nghĩa"],
                 [["Spring / Spring Boot", "bộ khung viết dịch vụ Java: lo tạo đối tượng, nối chúng, mở giao dịch; Spring Boot là cách đóng gói và chạy nhanh bộ khung đó"],
                  ["nhãn (annotation)", "dòng bắt đầu bằng <code>@</code> đặt trên phương thức hay lớp, mang lời dặn cho công cụ khác đọc, ví dụ <code>@Transactional</code>"],
                  ["từ khoá <code>this</code>", "tham chiếu tới chính đối tượng đang chạy phương thức; <code>this.ghiVet()</code> là tự gọi mình"],
                  ["commit / rollback", "chốt lưu vĩnh viễn mọi thay đổi của giao dịch / huỷ mọi thay đổi đó"]]),
           """Bảng này giải mã bốn từ đầu. Spring là bộ khung viết dịch vụ Java, lo tạo đối tượng, nối chúng với nhau và mở giao dịch. Spring Boot là cách đóng gói và chạy nhanh bộ khung đó.
           Nhãn là dòng bắt đầu bằng ký hiệu a còng đặt trên phương thức hay lớp, mang lời dặn cho công cụ khác đọc, ví dụ nhãn giao dịch.
           Từ khoá tự chỉ là tham chiếu tới chính đối tượng đang chạy, nên gọi qua từ khoá này là đối tượng tự gọi mình. Chốt là lưu vĩnh viễn mọi thay đổi của giao dịch, còn hoàn tác là huỷ mọi thay đổi đó."""),
        st(table(["từ", "nghĩa"],
                 [["bean", "đối tượng do Spring tạo và quản lý"],
                  ["IoC (đảo điều khiển)", "bạn không tự tạo đối tượng bằng new, Spring tạo rồi trao cho bạn"],
                  ["tiêm phụ thuộc", "Spring nối các bean với nhau, thường qua hàm tạo (phương thức chạy lúc tạo đối tượng)"],
                  ["proxy", "một đối tượng vỏ bọc bean, chạy thêm việc trước và sau khi gọi phương thức"],
                  ["REQUIRED / REQUIRES_NEW", "tham gia giao dịch đang có / luôn mở giao dịch mới"]]),
           """Bảng thứ hai giải thích nghĩa của năm thuật ngữ tiếp theo. Bean là đối tượng do Spring tạo và quản lý. Đảo điều khiển nghĩa là bạn không tự tạo đối tượng, Spring tạo rồi trao cho bạn.
           Tiêm phụ thuộc là Spring nối các bean với nhau, thường qua hàm tạo, tức phương thức chạy lúc tạo đối tượng. Proxy là đối tượng vỏ bọc bean, chạy thêm việc trước và sau lời gọi.
           Cuối cùng, chế độ tham gia nghĩa là dùng giao dịch đang có, còn chế độ mới nghĩa là luôn mở giao dịch mới.""", clear=True),
    ])
    intu = sc("intuition", "intuition", "Hình dung: vỏ bọc proxy đứng giữa", [
        st(svg(1500, 380,
               panel(40, 30, 1420, 320, "Spring container (hộp chứa các bean)", C_AMBER),
               box(100, 130, 300, 100, ["Controller", "bean"], C_BLUE),
               box(560, 130, 300, 100, ["Proxy", "vỏ bọc"], C_PURPLE),
               box(1020, 130, 360, 100, ["TransferService", "bean thật"], C_GREEN),
               arrow(400, 180, 555, 180, "#2a78d6", "gọi"), arrow(860, 180, 1015, 180, "#9333ea", "chuyển tiếp"),
               txt(700, 300, "Controller không giữ bean thật mà giữ proxy", 26, "middle", "#1f2937", True)),
           """Hình cho thấy cách Spring nối các bean. Controller, tức lớp nhận yêu cầu từ bên ngoài, muốn gọi dịch vụ chuyển tiền. Nhưng thứ nó nhận được không phải bean thật, mà là một proxy vỏ bọc.
           Proxy đứng giữa, rồi mới chuyển lời gọi tới bean thật."""),
        st(svg(1500, 400,
               box(60, 150, 240, 90, "Proxy", C_PURPLE, bold=True),
               box(380, 40, 300, 70, "1. mở giao dịch", C_GREEN), box(380, 150, 300, 90, ["2. chạy hàm", "chuyenTien()"], C_BLUE),
               box(380, 280, 300, 70, "3. commit / rollback", C_GREEN),
               arrow(300, 170, 375, 90, "#16a34a"), arrow(530, 115, 530, 145, "#475569"), arrow(530, 245, 530, 275, "#475569"),
               txt(1080, 160, "Nhãn @Transactional thật ra", 26, "middle", "#1f2937", True),
               txt(1080, 200, "chỉ là lời dặn cho proxy:", 26, "middle", "#1f2937", True),
               txt(1080, 240, "mở trước, đóng sau", 26, "middle", "#1f2937", True)),
           """Proxy làm ba việc. Trước tiên mở một giao dịch. Rồi chạy hàm chuyển tiền thật. Cuối cùng, commit nếu thành công, hoặc rollback nếu có lỗi.
           Nhãn giao dịch thật ra chỉ là lời dặn cho proxy, rằng hãy mở trước và đóng sau."""),
        st(svg(1500, 420,
               box(60, 40, 280, 90, "Proxy", C_PURPLE, bold=True),
               box(480, 40, 460, 90, ["chuyenTien() (bean thật)", "đã trong giao dịch 1"], C_GREEN),
               box(480, 230, 460, 90, ["this.ghiVet()", "gọi thẳng, không qua proxy"], C_RED),
               arrow(340, 85, 475, 85, "#9333ea"), arrow(710, 135, 710, 225, "#dc2626"),
               txt(1230, 150, "Không qua proxy", 26, "middle", "#dc2626", True),
               txt(1230, 190, "nên không có", 26, "middle", "#dc2626", True),
               txt(1230, 230, "giao dịch mới", 26, "middle", "#dc2626", True)),
           """Nhưng khi hàm chuyển tiền bên trong tự gọi ghi vết bằng từ khoá this, lời gọi đó đi thẳng, không qua proxy. Không có proxy thì không ai đọc nhãn, nên không có giao dịch mới.
           Đây chính là lỗi mở đầu bài."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: khi nào có giao dịch mới?", [
        st("""<p><b>Bước 1.</b> Vì lớp này có phương thức mang nhãn giao dịch, người gọi từ bên ngoài nhận <b>proxy</b>, nên lời gọi đầu tiên vào <code>chuyenTien()</code> đi qua proxy và mở giao dịch 1.</p>
<span class='note'>Làm thử: số giao dịch đã mở = $1$.</span>""",
           """Bước một, vì lớp dịch vụ có phương thức mang nhãn giao dịch, nên người gọi từ bên ngoài nhận proxy.
           Lời gọi đầu tiên vào hàm chuyển tiền vì vậy đi qua proxy và mở giao dịch thứ nhất.
           Làm thử, số giao dịch đã mở bằng một."""),
        st("""<p><b>Bước 2.</b> Hàm ghi vết với chế độ <code>REQUIRES_NEW</code> chỉ mở giao dịch mới khi lời gọi <b>đi qua proxy</b>.</p>
<span class='note'>Qua proxy: $1 + 1 = 2$ giao dịch. Gọi thẳng: vẫn $1$ giao dịch.</span>""",
           """Bước hai, vì proxy mới là nơi đọc nhãn, nên hàm ghi vết chỉ mở giao dịch mới khi lời gọi đi qua proxy.
           Làm thử, qua proxy thì một cộng một bằng hai giao dịch, còn gọi thẳng vẫn chỉ một giao dịch."""),
        st("""<p><b>Bước 3.</b> Giao dịch mới commit riêng, nên khi giao dịch ngoài hỏng, dòng ghi vết vẫn còn. Giao dịch dùng chung thì mất theo.</p>
<p class="small">Mặc định Spring chỉ rollback khi <code>RuntimeException</code> hoặc <code>Error</code> (lỗi nghiêm trọng của máy ảo, như hết bộ nhớ) bay ra khỏi phương thức; ngoại lệ bắt buộc xử lý thì vẫn commit, trừ khi khai báo <code>rollbackFor</code>.</p>""",
           """Bước ba, vì giao dịch mới commit riêng, nên khi giao dịch ngoài hỏng, dòng ghi vết vẫn còn. Còn giao dịch dùng chung thì mất theo.
           Mặc định Spring chỉ rollback khi một ngoại lệ thời gian chạy, hoặc một lỗi nghiêm trọng của máy ảo như hết bộ nhớ, bay ra khỏi phương thức.
           Ngoại lệ loại bắt buộc xử lý thì mặc định vẫn commit, trừ khi ta khai báo thêm trong nhãn."""),
    ], checks=["alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[0] == 1 + 1", "alg.bnk_spring_sim(False, 'REQUIRES_NEW', True)[0] == 1",
               "alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[1] == ['audit']"])
    ex = sc("example", "example", "Ví dụ bằng số, từng trường hợp", [
        st("""<p>Chuyển $500\\,000$ đồng, giao dịch ngoài hỏng. <b>Trường hợp A:</b> ghi vết gọi thẳng bằng <code>this</code>.</p>
$$① \\; \\text{giao dịch đã mở} = \\hl{1}$$""",
           """Ta chạy ba trường hợp. Trường hợp A, chuyển năm trăm nghìn đồng, giao dịch ngoài hỏng, ghi vết gọi thẳng bằng this. Phép tính thứ nhất, số giao dịch đã mở là một."""),
        st("""<p>Giao dịch ngoài hỏng nên rollback cả hai dòng.</p>
$$② \\; \\text{dòng còn lại} = \\hl{0}$$""",
           """Phép tính thứ hai, giao dịch ngoài hỏng nên rollback cả dòng chuyển tiền lẫn dòng ghi vết. Số dòng còn lại là không."""),
        st("""<p><b>Trường hợp B:</b> ghi vết gọi qua bean khác, chế độ mới.</p>
$$③ \\; \\text{giao dịch đã mở} = 1 + 1 = \\hlg{2}$$""",
           """Trường hợp B, ghi vết gọi qua một bean khác với chế độ mới. Phép tính thứ ba, số giao dịch đã mở là một cộng một bằng hai."""),
        st("""<p>Dòng ghi vết commit riêng, dòng chuyển tiền bị huỷ.</p>
$$④ \\; \\text{dòng còn lại} = \\hlg{1}\\ \\text{(dòng ghi vết)}$$""",
           """Phép tính thứ tư, dòng ghi vết đã commit riêng, còn dòng chuyển tiền bị huỷ, nên còn lại đúng một dòng, là dòng ghi vết."""),
        st("""<p><b>Trường hợp C:</b> mọi thứ thành công, lời gọi qua proxy.</p>
$$⑤ \\; \\text{dòng còn lại} = \\hlg{2}$$""",
           """Trường hợp C, mọi việc thành công. Phép tính thứ năm, cả hai dòng đều commit, nên còn hai dòng."""),
    ], checks=["alg.bnk_spring_sim(False, 'REQUIRES_NEW', True)[0] == 1", "len(alg.bnk_spring_sim(False, 'REQUIRES_NEW', True)[1]) == 0",
               "alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[0] == 1 + 1", "len(alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[1]) == 1",
               "len(alg.bnk_spring_sim(True, 'REQUIRES_NEW', False)[1]) == 2"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm lần đi qua proxy", [
        st("""<p>Đường khác: vì chỉ proxy mới mở giao dịch, nên số giao dịch bằng giao dịch đầu cộng <b>số lần lời gọi đi qua proxy có chế độ mở mới</b>.</p>
$$\\text{giao dịch} = 1 + \\text{số lần qua proxy với chế độ mới}$$""",
           """Kiểm bằng đường khác. Vì chỉ proxy mới mở giao dịch, nên số giao dịch bằng một, là giao dịch đầu, cộng số lần lời gọi đi qua proxy với chế độ mở mới."""),
        st(table(["trường hợp", "lần qua proxy với chế độ mới", "giao dịch = 1 + lần", "khớp mô phỏng"],
                 [["A: gọi thẳng", "0", "1", "có"], ["B: qua bean khác", "1", "2", "có"], ["REQUIRED qua proxy", "0", "1", "có"]]),
           """Bảng này so sánh. Gọi thẳng thì không có lần nào qua proxy, nên một giao dịch. Qua bean khác với chế độ mới là một lần, nên hai giao dịch.
           Chế độ dùng chung qua proxy cũng không mở thêm, nên một giao dịch. Cả ba khớp mô phỏng."""),
    ], checks=["alg.bnk_spring_sim(True, 'REQUIRED', True)[0] == 1 + 0",
               "all(alg.bnk_spring_sim(v, m, False)[0] == 1 + (1 if (v and m == 'REQUIRES_NEW') else 0) for v in (True, False) for m in ('REQUIRED', 'REQUIRES_NEW'))"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tự viết <code>new TransferService()</code>. Đối tượng đó không do Spring tạo, nên không được nối phụ thuộc và không có proxy.</div>""",
           """Lỗi thứ nhất, của người mới. Tự tạo đối tượng dịch vụ bằng từ khoá tạo mới. Đối tượng đó không do Spring tạo, nên không được nối phụ thuộc và không có proxy."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Gọi hàm có nhãn giao dịch từ trong cùng lớp</b> bằng <code>this</code>. Ở chế độ proxy (mặc định), nhãn bị bỏ qua.
<br><span class="note">Cách chữa: tách hàm sang bean khác, rồi gọi qua bean đó.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là gọi hàm có nhãn giao dịch từ trong cùng lớp bằng this. Ở chế độ proxy mặc định, nhãn bị bỏ qua vì lời gọi không đi qua proxy.
           Cách chữa là tách hàm sang bean khác rồi gọi qua bean đó."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Bắt ngoại lệ bằng <code>try … catch</code> ngay trong hàm có nhãn rồi chỉ ghi log. Ngoại lệ không bay ra tới proxy, nên proxy <b class="red">commit nửa chừng</b>.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là bắt ngoại lệ ngay trong hàm có nhãn rồi chỉ ghi nhật ký. Ngoại lệ không bay ra tới proxy, nên proxy không thấy lỗi nào và cứ commit, làm dữ liệu bị lưu nửa chừng."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Gọi ghi vết qua proxy, chế độ mới, giao dịch ngoài hỏng. Còn dòng nào?"],
                  ["2", "Như câu 1 nhưng chế độ dùng chung (REQUIRED). Còn dòng nào?"],
                  ["3", "Quyết định: đặt hàm ghi vết ở đâu để luôn lưu được vết?"]]),
           """Đến lượt bạn. Câu một, gọi ghi vết qua proxy, chế độ mới, giao dịch ngoài hỏng, còn dòng nào? Câu hai, như câu một nhưng chế độ dùng chung, còn dòng nào?
           Câu ba, đặt hàm ghi vết ở đâu để luôn lưu được vết? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: giao dịch mới commit riêng, nên còn dòng ghi vết.</p>
$$\\text{số dòng} = \\hl{1}$$""",
           """Đáp án câu một. Giao dịch mới commit riêng, nên còn đúng dòng ghi vết, một dòng."""),
        st("""<p>Câu 2: dùng chung thì ghi vết nằm trong giao dịch ngoài, nên bị rollback cùng.</p>
$$\\text{số dòng} = \\hl{0}$$""",
           """Đáp án câu hai. Chế độ dùng chung đưa ghi vết vào giao dịch ngoài, nên bị rollback cùng, số dòng là không."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["hàm ghi vết ở bean riêng, chế độ mới", "vết lưu kể cả khi giao dịch chính hỏng", "tốn thêm một giao dịch"],
                  ["cùng lớp, gọi bằng this", "ít mã", "nhãn bị bỏ qua, vết mất"]]),
           """Đáp án câu ba. Đặt hàm ghi vết ở một bean riêng với chế độ mới, thì vết luôn được lưu dù giao dịch chính hỏng, đổi lại tốn thêm một giao dịch.
           Để cùng lớp thì ít mã nhưng nhãn bị bỏ qua."""),
    ], checks=["len(alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[1]) == 1", "len(alg.bnk_spring_sim(True, 'REQUIRED', True)[1]) == 0"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("Spring tạo bean", "trao proxy cho người gọi", "proxy đọc nhãn", "mở / đóng giao dịch"),
           """Tổng kết chuỗi logic. Spring tạo bean, trao proxy cho người gọi. Proxy đọc nhãn rồi mở và đóng giao dịch."""),
        st("""<div class='box key'><b>Tư duy:</b> nhãn chỉ có tác dụng khi lời gọi <b>đi qua proxy</b>.
Khi giao dịch “không chạy”, hãy hỏi trước tiên: lời gọi này có đi qua proxy không?</div>""",
           """Điều cần mang theo. Nhãn chỉ có tác dụng khi lời gọi đi qua proxy. Khi giao dịch không chạy, hãy hỏi trước tiên, lời gọi này có đi qua proxy không."""),
    ])
    # ── AF2: mã chạy thật (mô phỏng proxy bằng java.lang.reflect.Proxy), quy mô, tự làm ──
    run = sc("chay_that", "example", "Chạy thật: tự dựng một proxy đếm giao dịch", [
        st(code_block(pgd, lines=(3, 8), title="Tệp ProxyGiaoDich.java (phần 1): giao diện và lớp thật"),
           """Ta mô phỏng cơ chế proxy bằng thư viện chuẩn của Java, vì Spring thật dùng đúng cơ chế này. Giao diện là danh sách tên hàm mà lớp hứa có, ở đây là hai hàm chuyển tiền và ghi vết.
           Lớp thật cài đặt hai hàm đó. Hàm chuyển tiền gọi hàm ghi vết bằng cách gọi thẳng chính nó."""),
        st(code_block(pgd, lines=(10, 17), title="Phần 2: proxy đứng giữa, tạo ngay lúc chạy"),
           """Proxy được tạo ngay lúc chạy, và nó đứng giữa người gọi với đối tượng thật. Đoạn có mũi tên là việc proxy làm mỗi khi có ai gọi một hàm của nó.
           Việc đó tăng biến đếm, tức là mở một giao dịch, in tên hàm được gọi, rồi mới gọi hàm thật.""", clear=True),
        st(code_block(pgd, lines=(18, 21), title="Phần 3: gọi qua proxy, đếm giao dịch"),
           """Ta gọi hàm chuyển tiền qua proxy và in số giao dịch. Rồi ta gọi hàm ghi vết cũng qua proxy, và in lại số giao dịch.""", clear=True),
        st(out_block(pgd),
           """Khi chạy thật, gọi chuyển tiền qua proxy thì proxy mở một giao dịch, rồi hàm thật chạy và tự gọi ghi vết. Lời gọi bên trong đi thẳng, không qua proxy, nên không mở thêm, số giao dịch vẫn là một.
           Khi ta gọi ghi vết qua proxy, giao dịch thứ hai mới được mở. Đây chính là lỗi gọi trong cùng lớp làm mất nhãn giao dịch.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: giao dịch lồng nhau làm cạn kết nối khi tải tăng", [
        st("""<p>Mỗi giao dịch giữ một <b>kết nối</b> (đường nối từ dịch vụ tới cơ sở dữ liệu) trong lúc chạy. Giao dịch ngoài giữ một, hàm ghi vết chế độ mới giữ thêm một: tối đa $C = 2$ kết nối cho mỗi yêu cầu.
Gọi $T$ là số yêu cầu chạy cùng lúc. Để không bị kẹt, hộp kết nối cần ít nhất $T \\cdot (C - 1) + 1$ kết nối.</p>"""
           + table(["tải", "yêu cầu cùng lúc T", "kết nối tối thiểu", "hộp mặc định 10 kết nối"],
                   [["×1", "5", "5 × 1 + 1 = 6", "đủ"],
                    ["×100", "500", "500 × 1 + 1 = 501", "<b>thiếu</b>: kẹt"],
                    ["×10 000", "50 000", "50 000 × 1 + 1 = 50 001", "<b>thiếu</b>, và vượt giới hạn của cơ sở dữ liệu"]]),
           """Mỗi giao dịch giữ một kết nối tới cơ sở dữ liệu trong lúc chạy. Giao dịch ngoài giữ một, hàm ghi vết với chế độ mới giữ thêm một, nên mỗi yêu cầu tối đa hai kết nối.
           Để không bị kẹt, hộp kết nối cần ít nhất số yêu cầu cùng lúc nhân với một, cộng một. Với năm yêu cầu cùng lúc thì cần sáu, hộp mười kết nối là đủ.
           Tải tăng một trăm lần, năm trăm yêu cầu cùng lúc cần năm trăm linh một kết nối, hộp mười kết nối bị kẹt. Tải tăng mười nghìn lần cần hơn năm mươi nghìn, vượt cả giới hạn của cơ sở dữ liệu.""", clear=True),
        st("""<div class="box warn"><b>Vì sao kẹt.</b> Mười yêu cầu cùng giữ kết nối thứ nhất, rồi cả mười cùng xin kết nối thứ hai: hộp hết, không yêu cầu nào tiến được, tới khi quá thời gian chờ (mặc định HikariCP là 30 giây).
<b>Giải pháp cũ gãy:</b> tăng hộp kết nối lên 501 hay 50 001 tốn bộ nhớ và làm cơ sở dữ liệu quá tải.</div>
<div class="box key"><b>Đánh đổi:</b> không lồng chế độ mới ở đường nóng; ghi vết bằng cách khác (ghi sau, hàng đợi); hoặc giới hạn số yêu cầu cùng lúc nhỏ hơn hộp. Mỗi cách đổi lấy một chút chậm trễ hay phức tạp.</div>""",
           """Hãy xem vì sao các yêu cầu bị kẹt chờ nhau. Mười yêu cầu cùng giữ kết nối thứ nhất, rồi cả mười cùng xin kết nối thứ hai, nhưng hộp đã hết, nên không yêu cầu nào tiến được, tới khi quá thời gian chờ. Mặc định của thư viện kết nối phổ biến này là ba mươi giây.
           Giải pháp cũ gãy, vì tăng hộp lên năm trăm hay năm mươi nghìn kết nối tốn bộ nhớ và làm cơ sở dữ liệu quá tải.
           Đánh đổi là không lồng chế độ mới ở đường chạy nóng, ghi vết bằng cách khác, hoặc giới hạn số yêu cầu cùng lúc nhỏ hơn hộp. Mỗi cách đổi lấy một chút chậm trễ hay phức tạp.""", clear=True),
    ], checks=["5 * (2 - 1) + 1 == 6", "500 * (2 - 1) + 1 == 501", "50000 * (2 - 1) + 1 == 50001", "6 <= 10 < 501"])
    write_lab("BNK", "L02", """# Lab BNK L02 — Đếm giao dịch của ba lời gọi

`ChuyenKhoanProxy.java`: một dịch vụ có ba hàm `chuyenKhoan`, `tinhPhi`, `thongBao`; **`chuyenKhoan` tự gọi `tinhPhi` và `thongBao` bằng cách gọi thẳng chính nó**. Proxy mở một giao dịch mỗi khi một hàm được gọi **qua proxy**.

Chép khung sau, rồi điền hai chỗ `// TODO`:

```java
import java.lang.reflect.*;
public class ChuyenKhoanProxy {
    interface Dich { void chuyenKhoan(); void tinhPhi(); void thongBao(); }
    static int moGiaoDich = 0;
    static class DichThat implements Dich {
        public void chuyenKhoan() { tinhPhi(); thongBao(); }
        public void tinhPhi() { }
        public void thongBao() { }
    }
    public static void main(String[] args) {
        Dich that = new DichThat();
        Dich proxy = (Dich) Proxy.newProxyInstance(Dich.class.getClassLoader(), new Class<?>[] { Dich.class },
            (p, m, a) -> {
                // TODO 1: đếm một giao dịch (moGiaoDich++)
                return m.invoke(that, a);
            });
        // TODO 2: gọi qua proxy lần lượt chuyenKhoan(), tinhPhi(), thongBao();
        //         sau mỗi lời gọi in "sau <tên hàm>: <số giao dịch>" (tên hàm viết như trong khung)
    }
}
```

Trước khi chạy, **dự đoán** ba con số rồi mới chấm. Chạy: `javac ChuyenKhoanProxy.java && java ChuyenKhoanProxy`. Chấm: `bash labs/cham.sh BNK L02 ChuyenKhoanProxy.java`.
""", "java", lab_proxy["code"], lab_proxy["out"])
    lab = practice_scene(sc, "Tự làm: đếm giao dịch của ba lời gọi", practice_steps(
        st, "BNK", "L02",
        """<p><b>Đề</b>: dịch vụ có <code>chuyenKhoan</code>, <code>tinhPhi</code>, <code>thongBao</code>; <code>chuyenKhoan</code> tự gọi hai hàm kia bằng <code>this</code>.</p>
<ol><li>Chép khung trong <code>de.md</code>, điền <code>moGiaoDich++</code> vào proxy</li>
<li>Gọi qua proxy cả ba hàm, mỗi lần in <code>sau &lt;tên hàm&gt;: &lt;số&gt;</code></li>
<li><b>Dự đoán</b> ba số trước khi chạy</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Dịch vụ có ba hàm, và hàm chuyển khoản tự gọi hai hàm còn lại bằng cách gọi thẳng chính nó. Hãy chép khung trong thư mục thực hành, điền câu lệnh tăng biến đếm vào proxy,
        rồi gọi qua proxy cả ba hàm và in số giao dịch sau mỗi lần. Trước khi chạy, hãy dự đoán ba con số. Hãy dừng video, tự làm, đừng chép lại ví dụ.""",
        lab_proxy["out"], "ChuyenKhoanProxy.java",
        """<div class="box key"><b>Nếu kẹt:</b> chỉ lời gọi <b>qua proxy</b> mới tăng biến đếm. Lời <code>tinhPhi(); thongBao();</code> bên trong <code>chuyenKhoan</code> đi thẳng nên không tăng.
Khung đầy đủ ở <code>labs/BNK/L02/de.md</code>, lời giải ở <code>labs/BNK/L02/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, nhớ rằng chỉ lời gọi qua proxy mới tăng biến đếm. Hai lời gọi bên trong hàm chuyển khoản đi thẳng nên không tăng. Khung đầy đủ nằm trong tệp đề, lời giải nằm trong thư mục thực hành, chỉ mở sau khi bạn đã tự thử.""", pause=120), "BNK", "L02")
    return lesson("L02", "spring_boot_proxy_giao_dich", "Bài 2 — Spring Boot: bean, proxy và giao dịch",
                  "curriculum/bnk.yaml L02; audit/bnk/verify_bnk.py L02; audit/review/screen_code/BNK.yaml (mã chạy thật bằng JDK 21: java.lang.reflect.Proxy mô phỏng cơ chế proxy, Spring thật dùng JDK dynamic proxy hoặc CGLIB); Spring Framework Reference (Transaction Management: “In proxy mode (which is the default), only external method calls coming in through the proxy are intercepted”; rollback mặc định cho RuntimeException và Error; AOP proxies; Proxying Mechanisms); Java Language Specification §11 (checked / unchecked exceptions); HikariCP README (maximumPoolSize mặc định 10, connectionTimeout mặc định 30 000 ms) và wiki About Pool Sizing (pool size = Tn × (Cm − 1) + 1); Spring Boot dùng HikariCP làm hộp kết nối mặc định",
                  ["Nêu cách Spring tạo bean và trao proxy cho người gọi", "Dự đoán số giao dịch được mở khi gọi qua proxy hoặc gọi thẳng",
                   "Nhận ra lỗi gọi hàm cùng lớp làm mất nhãn giao dịch", "Chọn nơi đặt hàm ghi vết để luôn lưu được",
                   "Tính số kết nối cơ sở dữ liệu tối thiểu khi giao dịch lồng nhau và tải tăng ×100, ×10 000",
                   "Viết phần đếm giao dịch của một proxy và dự đoán số đếm qua ba lời gọi"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "intuition"), (2, "chay_that"), (3, "pitfalls"), (4, "example"), (5, "quy_mo"), (6, "practice")])
