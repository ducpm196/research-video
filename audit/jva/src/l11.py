from lib import *


def ln(p, s):
    """Số thứ tự (từ 1) của dòng đầu tiên trong mã của p chứa chuỗi s."""
    return next(i for i, l in enumerate(p["code"].split("\n"), 1) if s in l)


def build():
    phi = prog("Phi", """
import java.util.ArrayList;

interface CachTinhPhi {
    long phi(long tien);                      // lời hứa: có phương thức này
}

class PhiTheoBac implements CachTinhPhi {    // biểu phí ba bậc của bài 3
    @Override
    public long phi(long tien) {
        if (tien < 500000) {
            return 0;
        } else if (tien < 10000000) {
            return 2200;
        }
        return 5500;
    }
}

class PhiPhanTram implements CachTinhPhi {
    @Override
    public long phi(long tien) {
        long p = tien * 5 / 1000;             // 0,5% như bài 2 (số minh hoạ)
        return p < 1000 ? 1000 : p;           // tối thiểu 1000
    }
}

public class Phi {
    public static void main(String[] args) {
        ArrayList<CachTinhPhi> ds = new ArrayList<>();
        ds.add(new PhiTheoBac());
        ds.add(new PhiPhanTram());
        for (CachTinhPhi c : ds) {            // một vòng lặp cho mọi cách tính
            System.out.println(c.phi(100000) + " " + c.phi(2000000));
        }
    }
}""", out="0 2200\n1000 10000")
    ban_ghi = prog("BanGhi", """
record GiaoDich(String stk, long tien) {}

enum TrangThai { CHO, THANH_CONG, THAT_BAI }

public class BanGhi {
    static String moTa(TrangThai t) {
        return switch (t) {
            case CHO -> "dang cho";
            case THANH_CONG -> "xong";
            case THAT_BAI -> "loi";
        };
    }
    public static void main(String[] args) {
        GiaoDich a = new GiaoDich("A01", 500000);
        GiaoDich b = new GiaoDich("A01", 500000);
        System.out.println(a);                       // (1)
        System.out.println(a == b);                  // (2)
        System.out.println(a.equals(b));             // (3)
        System.out.println(a.tien() + 2200);         // (4) cộng phí bậc 2 (minh hoạ)
        System.out.println(moTa(TrangThai.THANH_CONG)); // (5)
    }
}""", out="GiaoDich[stk=A01, tien=500000]\nfalse\ntrue\n502200\nxong")
    kiem = prog("Kiem", """
record GiaoDich(String stk, long tien) {}

class GiaoDichThuong {                    // lớp thường, không phải bản ghi
    String stk;
    long tien;
    GiaoDichThuong(String stk, long tien) { this.stk = stk; this.tien = tien; }
}

public class Kiem {
    public static void main(String[] args) {
        GiaoDich a = new GiaoDich("A01", 500000);
        GiaoDich b = new GiaoDich("A01", 500000);
        System.out.println(a.stk().equals(b.stk()) && a.tien() == b.tien());
        GiaoDichThuong x = new GiaoDichThuong("A01", 500000);
        GiaoDichThuong y = new GiaoDichThuong("A01", 500000);
        System.out.println(x.equals(y));
    }
}""", out="true\nfalse")
    yeu_hon = prog("YeuHon", """
interface CachTinhPhi {
    long phi(long tien);
}

class MienPhi implements CachTinhPhi {
    long phi(long tien) {                 // quên chữ public
        return 0;
    }
}

public class YeuHon {
    public static void main(String[] args) {
        System.out.println(new MienPhi().phi(100000));
    }
}""", expect="compile_error:attempting to assign weaker access privileges; was public",
       err="error: phi(long) in MienPhi cannot implement phi(long) in CachTinhPhi\n"
           "  attempting to assign weaker access privileges; was public")
    quen = prog("QuenGhiDe", """
class TaiKhoan {
    long phiThuongNien() {
        return 50000;                     // số minh hoạ
    }
}

class TaiKhoanVip extends TaiKhoan {
    long phiThuongnien() {                // gõ sai: chữ n viết thường
        return 0;                         // khách VIP được miễn
    }
}

public class QuenGhiDe {
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoanVip();
        System.out.println(tk.phiThuongNien());
    }
}""", out="50000")
    co_ghi_de = prog("CoGhiDe", """
class TaiKhoan {
    long phiThuongNien() {
        return 50000;
    }
}

class TaiKhoanVip extends TaiKhoan {
    @Override
    long phiThuongnien() {                // vẫn gõ sai, nhưng có chú thích
        return 0;
    }
}

public class CoGhiDe {
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoanVip();
        System.out.println(tk.phiThuongNien());
    }
}""", expect="compile_error:method does not override or implement a method from a supertype")
    quiz = prog("DoanKetQua", """
interface Phi {
    long tinh(long tien);
}
class MienPhi implements Phi {
    @Override public long tinh(long tien) { return 0; }
}
class NuaPhanTram implements Phi {
    @Override public long tinh(long tien) { return tien * 5 / 1000; }
}
record GiaoDich(String stk, long tien) {}

public class DoanKetQua {
    public static void main(String[] args) {
        Phi[] ds = { new MienPhi(), new NuaPhanTram() };
        long tong = 0;
        for (Phi p : ds) {
            tong += p.tinh(300000);
        }
        System.out.println(tong);
        System.out.println(new GiaoDich("B02", 7).equals(new GiaoDich("B02", 7)));
        System.out.println(new GiaoDich("B02", 7) == new GiaoDich("B02", 7));
    }
}""", out="1500\ntrue\nfalse")

    p_main = ln(phi, "public class Phi")
    p_bac, p_pt = ln(phi, "class PhiTheoBac"), ln(phi, "class PhiPhanTram")
    q_main = ln(quiz, "Phi[] ds")
    sc_hook = sc("hook", "hook", "Mỗi loại phí một công thức: thêm loại mới có phải sửa khắp nơi?", [
        st("""<p>Ngân hàng có phí theo bậc (biểu phí bài 3), phí theo phần trăm, rồi mai có thêm miễn phí cho khách VIP (đều là số minh hoạ). Viết tất cả vào một hàm với chuỗi
<code>if … else if …</code> thì mỗi lần thêm loại mới lại phải sửa hàm cũ.</p>
<div class="box key">Hôm nay: <b>giao diện</b> và <b>đa hình</b> (cùng một lời gọi, mỗi đối tượng làm theo cách của lớp nó: mỗi cách tính phí là một lớp, chạy qua <b>một</b> vòng lặp),
<b>bản ghi</b> cho dữ liệu giao dịch, <b>kiểu liệt kê</b> cho trạng thái.</div>""",
           """Ngân hàng có phí theo bậc như biểu phí ở bài ba, phí theo phần trăm, rồi mai lại có miễn phí cho khách đặc biệt, tất cả đều là số minh hoạ.
           Viết tất cả vào một hàm với chuỗi lệnh rẽ nhánh thì mỗi lần thêm loại mới lại phải sửa hàm cũ.
           Hôm nay ta học giao diện và đa hình, để mỗi cách tính phí là một lớp riêng, chạy qua cùng một vòng lặp.
           Đa hình nghĩa là nhiều hình dạng: cùng một lời gọi, mỗi đối tượng làm theo cách riêng của lớp nó.
           Ta cũng học bản ghi cho dữ liệu giao dịch, và kiểu liệt kê cho trạng thái giao dịch."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: lớp, danh sách và so bằng nội dung", [
        st(table(["đã học", "điều dùng lại hôm nay"],
                 [["① Lớp và đối tượng", "trường, hàm tạo, phương thức, <code>toString</code>; mỗi <code>new</code> là một đối tượng riêng"],
                  ["② Danh sách", "<code>ArrayList&lt;…&gt;</code>, vòng lặp duyệt từng phần tử"],
                  ["③ So sánh", "<code>==</code> so <b>địa chỉ</b> đối tượng; <code>equals</code> so <b>nội dung</b> (như với chuỗi)"]]),
           """Ta ôn ba điều. Thứ nhất, lớp có trường, hàm tạo và phương thức, và mỗi lần tạo mới là một đối tượng riêng.
           Thứ hai, danh sách và vòng lặp duyệt từng phần tử.
           Thứ ba, với đối tượng, dấu bằng bằng so địa chỉ, còn phương thức so bằng so nội dung, như bạn đã thấy với chuỗi."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ký hiệu: giao diện, cài đặt, kế thừa, bản ghi, liệt kê", [
        st(table(["viết", "nghĩa"],
                 [["<code>interface CachTinhPhi { long phi(long tien); }</code>", "<b>giao diện</b>: lời hứa “có phương thức này”, chưa có thân"],
                  ["<code>class PhiTheoBac implements CachTinhPhi</code>", "<b>cài</b> giao diện: phải viết đủ thân các phương thức đã hứa"],
                  ["<code>@Override</code>", "<b>ghi đè</b> = viết lại phương thức cùng tên, cùng tham số của lớp cha hay giao diện; trình biên dịch kiểm giúp"],
                  ["<code>class TaiKhoanVip extends TaiKhoan</code>", "<b>kế thừa</b>: lớp con nhận phương thức của lớp cha, có thể ghi đè"],
                  ["<code>record GiaoDich(String stk, long tien) {}</code>", "<b>bản ghi</b>: lớp dữ liệu không đổi; tự sinh <code>stk()</code>, <code>tien()</code>, <code>equals</code>, <code>toString</code>"],
                  ["<code>enum TrangThai { CHO, THANH_CONG, THAT_BAI }</code>", "<b>kiểu liệt kê</b>: đúng ba giá trị cố định"]]),
           """Bảng ký hiệu của bài. Giao diện là một lời hứa: có phương thức tính phí, nhận số tiền, trả về phí, nhưng chưa có thân.
           Một lớp cài giao diện thì phải viết đủ thân cho mọi phương thức đã hứa.
           Ghi đè nghĩa là viết lại một phương thức cùng tên, cùng tham số đã có ở lớp cha hoặc giao diện, để thay cách làm.
           Chú thích ghi đè nhờ trình biên dịch kiểm rằng phương thức đó đúng là ghi đè, và hàm đổi ra chuỗi ở bài bảy cũng là một phương thức ghi đè.
           Kế thừa cho lớp con nhận các phương thức của lớp cha, và có thể ghi đè chúng.
           Bản ghi là lớp chỉ chứa dữ liệu không đổi, trình biên dịch tự sinh phần còn lại. Kiểu liệt kê có đúng một số giá trị cố định."""),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: một lời hứa, nhiều cách làm, máy chọn theo đối tượng thật", [
        st(svg(1500, 420,
               box(450, 20, 600, 100, ["giao diện CachTinhPhi", "long phi(long tien)"], C_PURPLE, bold=True),
               box(120, 190, 460, 100, ["PhiTheoBac", "0 / 2 200 / 5 500 theo bậc"], C_BLUE, bold=True),
               box(920, 190, 460, 100, ["PhiPhanTram", "tien × 5 / 1000, tối thiểu 1000"], C_BLUE, bold=True),
               arrow(350, 185, 600, 125, "#9333ea", "cài", dash=True), arrow(1150, 185, 900, 125, "#9333ea", "cài", dash=True),
               box(400, 330, 700, 80, ["vòng lặp: c.phi(2000000) với mỗi c", "ra 2200, rồi ra 10000"], C_AMBER, 22, bold=True),
               arrow(520, 330, 400, 295, "#16a34a"), arrow(980, 330, 1100, 295, "#16a34a")),
           """Hình này là đa hình. Ở trên là giao diện, lời hứa có phương thức tính phí.
           Hai lớp bên dưới cùng cài lời hứa đó, mỗi lớp một công thức.
           Vòng lặp chỉ biết mỗi phần tử là một cách tính phí, và gọi cùng một lệnh.
           Máy ảo nhìn đối tượng thật để chọn đúng bản cài, nên hai triệu ra hai nghìn hai trăm với phí theo bậc, và mười nghìn với phí phần trăm."""),
        st(table(["", "kế thừa <code>extends</code>", "giao diện <code>implements</code>"],
                 [["nhận được", "trường và thân phương thức của lớp cha (phần <code>private</code> vẫn chỉ lớp cha đụng được)", "chủ yếu là lời hứa: tên và kiểu của phương thức"],
                  ["số lượng", "chỉ <b>một</b> lớp cha", "<b>nhiều</b> giao diện"],
                  ["dùng khi", "“là một” thật sự, ít tầng", "nhiều cách làm cùng một việc"]]),
           """Kế thừa và giao diện khác nhau thế nào? Kế thừa nhận cả trường lẫn thân phương thức của lớp cha, còn giao diện chủ yếu chỉ cho lời hứa.
           Một lớp chỉ kế thừa được một lớp cha, nhưng cài được nhiều giao diện.
           Vì vậy, khi có nhiều cách làm cùng một việc, như tính phí, hãy nghĩ tới giao diện trước.""", clear=True),
        st(svg(1500, 330,
               box(60, 40, 420, 110, ["a: GiaoDich", "stk = A01, tien = 500000"], C_BLUE, 22, bold=True),
               box(60, 190, 420, 110, ["b: GiaoDich", "stk = A01, tien = 500000"], C_BLUE, 22, bold=True),
               box(640, 40, 800, 110, ["a == b: cùng MỘT đối tượng?", "hai lần new là hai đối tượng → false"], C_RED, 22, bold=True),
               box(640, 190, 800, 110, ["a.equals(b): cùng NỘI DUNG?", "bản ghi so từng thành phần → true"], C_GREEN, 22, bold=True),
               arrow(485, 95, 630, 95, "#dc2626"), arrow(485, 245, 630, 245, "#16a34a")),
           """Còn bản ghi thì sao? Hai lần tạo mới cho hai đối tượng riêng, nên so địa chỉ ra sai.
           Nhưng bản ghi tự sinh phép so bằng nội dung, so từng thành phần, nên hai giao dịch cùng số tài khoản, cùng số tiền thì bằng nhau.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: hai cách tính phí cài cùng một giao diện", [
        st(code_block(phi, lines=(3, 5), title="Bước 1. Viết lời hứa"),
           """Bước một, viết giao diện. Nó chỉ nói có một phương thức tính phí, nhận số tiền và trả về số phí.
           Không có thân, vì mỗi lớp sẽ tự quyết định công thức."""),
        st(code_block(phi, lines=(p_bac, p_bac + 10), title="Bước 2. Cách thứ nhất: phí theo bậc của bài 3"),
           """Bước hai, lớp phí theo bậc cài giao diện, nên phải viết thân cho phương thức tính phí, và thân đó chính là biểu phí ba bậc của bài ba, số minh hoạ.
           Phương thức phải công khai, vì phương thức đã hứa trong giao diện luôn công khai."""),
        st(code_block(phi, lines=(p_pt, p_pt + 6), title="Bước 3. Cách thứ hai: phí phần trăm, có mức tối thiểu"),
           """Bước ba, lớp phí phần trăm lấy số tiền nhân năm chia một nghìn, tức không phẩy năm phần trăm như bài hai, số minh hoạ.
           Nếu kết quả nhỏ hơn một nghìn thì lấy một nghìn, nhờ toán tử ba ngôi, nên phí không bao giờ dưới mức tối thiểu."""),
        st(code_block(phi, lines=(p_main + 2, p_main + 7), title="Bước 4. Một vòng lặp cho mọi cách tính") + out_block(phi),
           """Bước bốn, danh sách có kiểu là giao diện, nên chứa được cả hai lớp. Vòng lặp gọi cùng một lệnh cho mọi phần tử.
           Dòng đầu là phí theo bậc: một trăm nghìn dưới năm trăm nghìn nên miễn phí, hai triệu ở bậc hai nên hai nghìn hai trăm.
           Dòng hai là phí phần trăm: một trăm nghìn cho năm trăm, dưới mức tối thiểu nên lấy một nghìn, còn hai triệu thì được mười nghìn."""),
    ], checks=["100000 < 500000 and 500000 <= 2000000 < 10000000", "100000 * 5 // 1000 == 500",
               "max(100000 * 5 // 1000, 1000) == 1000", "max(2000000 * 5 // 1000, 1000) == 10000"])
    sc_ex = sc("example", "example", "Ví dụ: bản ghi và kiểu liệt kê, từng phép tính", [
        st(code_block(ban_ghi, lines=(1, 11), title="Tệp BanGhi.java, phần đầu")
           + "<p><code>return switch</code>: lệnh chọn của bài 3 dùng như <b>một giá trị</b>, lấy giá trị sau mũi tên.</p>",
           """Ví dụ này khai bản ghi giao dịch gồm số tài khoản và số tiền, và kiểu liệt kê ba trạng thái: chờ, thành công, thất bại.
           Hàm mô tả dùng lệnh chọn dạng mũi tên của bài ba như một giá trị: nhánh khớp cho ra chữ đứng sau mũi tên, và hàm trả về chữ đó.
           Không cần nhánh mặc định, vì đã đủ ba trạng thái."""),
        st(code_block(ban_ghi, lines=(14, 16)) + "$$① \\; \\text{in a} \\to \\hl{\\text{GiaoDich[stk=A01, tien=500000]}}$$",
           """Phép tính thứ nhất in bản ghi a. Bản ghi tự sinh cách in: tên kiểu, rồi từng thành phần trong ngoặc vuông."""),
        st(code_block(ban_ghi, lines=(17, 18)) + "$$② \\; a == b \\to \\hl{\\text{false}} \\qquad ③ \\; a.\\text{equals}(b) \\to \\hlg{\\text{true}}$$",
           """Phép tính thứ hai so địa chỉ, mà hai lần tạo mới là hai đối tượng, nên ra sai.
           Phép tính thứ ba so nội dung, hai thành phần đều trùng, nên ra đúng."""),
        st(code_block(ban_ghi, lines=(19, 19)) + "$$④ \\; 500\\,000 + 2\\,200 = \\hl{502\\,200}$$",
           """Phép tính thứ tư lấy số tiền bằng phương thức truy cập tự sinh, cộng phí bậc hai là hai nghìn hai trăm, ra năm trăm linh hai nghìn hai trăm."""),
        st(code_block(ban_ghi, lines=(9, 9)) + code_block(ban_ghi, lines=(20, 20)) + "$$⑤ \\; \\text{THANH\\_CONG} \\to \\hl{\\text{xong}}$$",
           """Phép tính thứ năm đưa trạng thái thành công vào hàm mô tả, và nhánh đó trả chữ xong."""),
        st(out_block(ban_ghi),
           """Chạy thật, năm dòng in ra khớp đúng năm phép tính."""),
    ], checks=["500000 + 2200 == 502200"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: so tay từng thành phần, và so với lớp thường", [
        st(code_block(kiem, lines=(ln(kiem, "GiaoDich a"), ln(kiem, "x.equals"))) + out_block(kiem),
           """Kiểm phép tính thứ ba bằng đường khác: so tay từng thành phần. Số tiền so bằng dấu bằng bằng được, vì là số trần.
           Kết quả đúng, khớp với phép so của bản ghi.
           Còn một lớp thường cùng hai trường thì ra sai, vì lớp thường không tự sinh phép so nội dung."""),
        st(table(["số tiền", "phí theo bậc (bài 3)", "phí phần trăm: <code>tien * 5 / 1000</code>, tối thiểu 1000"],
                 [["100 000", "dưới 500 000 → 0", "$500 < 1000 \\Rightarrow 1000$"],
                  ["2 000 000", "bậc 2 → 2 200", "$10000 \\ge 1000 \\Rightarrow 10000$"]]),
           """Kiểm phí bằng tay, theo đúng công thức. Theo biểu phí bậc, một trăm nghìn được miễn phí, còn hai triệu ở bậc hai nên là hai nghìn hai trăm.
           Phí phần trăm của một trăm nghìn là năm trăm, nhỏ hơn mức tối thiểu nên thành một nghìn.
           Của hai triệu là mười nghìn, không dưới mức tối thiểu. Cả bốn số khớp với hai dòng in ở bước bốn.""", clear=True),
    ], checks=["100000 * 5 // 1000 < 1000", "2000000 * 5 // 1000 >= 1000", "(0 if 100000 < 500000 else 2200) == 0"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Cài phương thức của giao diện mà quên <code>public</code>.</div>'
           + code_block(yeu_hon, lines=(5, 9)) + out_block(yeu_hon, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là cài phương thức của giao diện mà quên chữ công khai.
           Phương thức đã hứa trong giao diện luôn công khai, nên bản cài không được hẹp hơn, và trình biên dịch báo đang gán quyền truy cập yếu hơn."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Không ghi <code>@Override</code>, gõ sai tên mà không ai báo.</div>'
           + code_block(quen, lines=(1, 11)) + out_block(quen),
           """Lỗi thứ hai hay gặp ở người đã đi làm. Lớp tài khoản đặc biệt muốn ghi đè phí thường niên về không, nhưng gõ sai một chữ n viết thường.
           Không có lỗi biên dịch, vì đó là một phương thức mới hoàn toàn hợp lệ. Hàm chính tạo một tài khoản đặc biệt rồi gọi phí thường niên, nhưng máy chạy bản của lớp cha, nên khách vẫn bị thu năm mươi nghìn.""", clear=True),
        st(code_block(co_ghi_de, lines=(7, 11), title="Thêm @Override: trình biên dịch bắt ngay") + out_block(co_ghi_de, "Trình biên dịch báo"),
           """Thêm chú thích ghi đè, vẫn tên gõ sai đó, thì trình biên dịch báo ngay: phương thức này không ghi đè gì cả.
           Vì vậy, mọi phương thức ghi đè nên có chú thích này."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Kế thừa nhiều tầng thay vì dùng giao diện.</div>'
           + svg(1500, 300,
                 box(20, 40, 300, 70, "TaiKhoan", C_GRAY, 22, bold=True), arrow(325, 75, 380, 75),
                 box(385, 40, 330, 70, "TaiKhoanCaNhan", C_GRAY, 22), arrow(720, 75, 775, 75),
                 box(780, 40, 330, 70, "TaiKhoanCaNhanVip", C_GRAY, 22), arrow(1115, 75, 1170, 75),
                 box(1175, 40, 305, 70, ["…VipMienPhi", "sửa cha là vỡ con"], C_RED, 20),
                 box(20, 190, 420, 90, ["TaiKhoan", "có trường CachTinhPhi"], C_GREEN, 22, bold=True),
                 arrow(445, 235, 560, 235, "#16a34a", "ghép"),
                 box(570, 190, 300, 90, "PhiTheoBac", C_BLUE, 22), box(890, 190, 300, 90, "PhiPhanTram", C_BLUE, 22),
                 box(1210, 190, 270, 90, "MienPhi", C_BLUE, 22)),
           """Lỗi thứ ba là kế thừa nhiều tầng: tài khoản, tài khoản cá nhân, cá nhân đặc biệt, rồi đặc biệt miễn phí.
           Mỗi tầng phụ thuộc tầng trên, nên sửa lớp cha là vỡ lớp con, và mỗi kiểu phí mới lại thêm một tầng.
           Cách tốt hơn ở hàng dưới: tài khoản giữ một trường kiểu giao diện tính phí, rồi ghép cách tính nào cũng được.""",
           clear=True, focus=[2, 2, 2]),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(1, 10), title="Các kiểu trong bài"),
           """Bây giờ tới phần bạn tự làm. Đây là các kiểu: một giao diện tính phí, lớp miễn phí trả không, lớp nửa phần trăm trả số tiền nhân năm chia một nghìn, và bản ghi giao dịch."""),
        st(code_block(quiz, lines=(q_main, q_main + 7), title="Đoán ba dòng in ra"),
           """Mảng có hai cách tính phí, vòng lặp cộng phí của ba trăm nghìn theo từng cách. Rồi ta so hai bản ghi giao dịch bằng nội dung, và bằng địa chỉ.
           Hãy dừng video và viết ra ba dòng in ra.""", pause=20),
        st(table(["dòng in", "lý do", "in ra"],
                 [["① <code>tong</code>", "$0 + 300\\,000 \\times 5 / 1000 = 0 + 1\\,500$", "<b>1500</b>"],
                  ["② <code>equals</code>", "bản ghi so từng thành phần: B02 = B02, 7 = 7", "<b>true</b>"],
                  ["③ <code>==</code>", "hai lần <code>new</code> là hai đối tượng", "<b>false</b>"]]),
           """Đáp án như sau. Dòng một, miễn phí cho không, nửa phần trăm của ba trăm nghìn là một nghìn năm trăm, tổng là một nghìn năm trăm.
           Dòng hai, bản ghi so từng thành phần, đều trùng nên ra đúng.
           Dòng ba, hai lần tạo mới là hai đối tượng khác địa chỉ, nên ra sai."""),
        st(out_block(quiz),
           """Chạy thật, ba dòng in ra là một nghìn năm trăm, đúng, và sai, khớp đáp án."""),
    ], checks=["0 + 300000 * 5 // 1000 == 1500"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("giao diện: lời hứa", "nhiều lớp cài cùng lời hứa", "một vòng lặp gọi, máy chọn bản cài", "bản ghi: so theo nội dung",
                 "kiểu liệt kê: tập giá trị cố định"),
           """Tổng kết chuỗi logic. Giao diện là lời hứa, nhiều lớp cài cùng lời hứa đó.
           Một vòng lặp gọi chung một lệnh, máy ảo chọn bản cài theo đối tượng thật.
           Bản ghi so bằng nội dung, còn kiểu liệt kê là một tập giá trị cố định."""),
        st("""<div class='box key'><b>Tư duy:</b> nhiều cách làm một việc → <b>giao diện</b>, đừng xây tháp kế thừa. Mọi phương thức ghi đè
đều gắn <code>@Override</code>. Dữ liệu chỉ để chở (giao dịch, lệnh) → <b>bản ghi</b>; trạng thái hữu hạn → <b>kiểu liệt kê</b>, không dùng chuỗi tự gõ.</div>""",
           """Điều cần mang theo. Nhiều cách làm một việc thì dùng giao diện, đừng xây tháp kế thừa. Mọi phương thức ghi đè đều gắn chú thích ghi đè.
           Dữ liệu chỉ để chở như giao dịch thì dùng bản ghi, còn trạng thái hữu hạn thì dùng kiểu liệt kê thay vì chuỗi tự gõ."""),
    ])
    return lesson("L11", "giao_dien_ban_ghi_liet_ke", "Bài 11 — Kế thừa, giao diện, đa hình; bản ghi và kiểu liệt kê",
                  "curriculum/jva.yaml L11; audit/jva/verify_jva.py L11 (javac/java chạy thật); The Java Language Specification, Java SE 21 "
                  "(§8.1.4 một lớp cha trực tiếp, §8.1.5 cài nhiều giao diện, §8.4.8 kế thừa và ghi đè, §9.4 phương thức giao diện ngầm public, "
                  "§9.6.4.4 @Override, §8.9 kiểu liệt kê, §8.10 bản ghi và equals/toString sinh tự động, §15.28.1 switch biểu thức phải đủ trường hợp); "
                  "Java SE 21 API: java.lang.Record (equals so từng thành phần; định dạng toString không đặc tả, kết quả chạy thật trên JDK); dev.java/learn",
                  ["Viết giao diện và hai lớp cài nó, chạy qua một vòng lặp (đa hình)", "Dùng kế thừa và chú thích ghi đè đúng cách",
                   "Khai bản ghi, so bằng nội dung", "Khai kiểu liệt kê và chọn theo trường hợp"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
