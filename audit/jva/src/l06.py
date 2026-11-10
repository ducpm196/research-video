from lib import *


def ln(p, s):
    """Số thứ tự (tính từ 1) của dòng đầu tiên trong mã của p có chứa s."""
    for i, l in enumerate(p["code"].split("\n"), 1):
        if s in l:
            return i
    raise ValueError(s)


# Hàm tính phí chuyển khoản dùng chung cho nhiều chương trình (biểu phí là SỐ MINH HOẠ, không phải của ngân hàng nào)
TINH_PHI = """    static long tinhPhi(long soTien) {       // phí minh hoạ, đơn vị đồng
        if (soTien < 500000) {
            return 0;
        } else if (soTien < 10000000) {
            return 2200;
        }
        return 5500;
    }"""


def build():
    phi = prog("Phi", """
public class Phi {
%s

    public static void main(String[] args) {
        System.out.println(tinhPhi(300000));
        System.out.println(tinhPhi(2000000));
        System.out.println(tinhPhi(10000000));
    }
}""" % TINH_PHI, out="0\n2200\n5500")
    nap = prog("NapChong", """
public class NapChong {
%s

    static long tinhPhi(long soTien, int soLan) {   // cùng tên, thêm một tham số
        return tinhPhi(soTien) * soLan;
    }

    public static void main(String[] args) {
        System.out.println(tinhPhi(2000000));
        System.out.println(tinhPhi(2000000, 3));
    }
}""" % TINH_PHI, out="2200\n6600")
    gia_tri = prog("GiaTri", """
public class GiaTri {
    static void tangSo(long x) {
        x = x + 100000;                  // chỉ đổi bản sao x
    }

    static void tangO(long[] m) {
        m[0] = m[0] + 100000;            // đổi ô của mảng dùng chung
    }

    public static void main(String[] args) {
        long soDu = 500000;
        long[] a = {500000};
        tangSo(soDu);
        tangO(a);
        System.out.println(soDu + " " + a[0]);
    }
}""", out="500000 600000")
    goi = prog("Goi", """
public class Goi {
%s

    static long tongTru(long soTien) {       // tổng số tiền bị trừ khỏi tài khoản
        long phi = tinhPhi(soTien);          // gọi lồng: hàm gọi hàm
        return soTien + phi;
    }

    public static void main(String[] args) {
        long soDu = 5000000;
        soDu = soDu - tongTru(2000000);
        System.out.println("Con lai: " + soDu);
    }
}""" % TINH_PHI, out="Con lai: 2997800")
    kiem = prog("KiemPhi", """
public class KiemPhi {
%s

    public static void main(String[] args) {
        long[] thu = {499999, 500000, 9999999, 10000000};   // các số tiền ở biên
        for (int i = 0; i < thu.length; i++) {
            System.out.println(thu[i] + " -> " + tinhPhi(thu[i]));
        }
    }
}""" % TINH_PHI, out="499999 -> 0\n500000 -> 2200\n9999999 -> 2200\n10000000 -> 5500")
    pham_vi = prog("PhamVi", """
public class PhamVi {
    static long tinhPhi(long soTien) {
        long phi = 2200;
        return phi;
    }

    public static void main(String[] args) {
        tinhPhi(2000000);
        System.out.println(phi);         // SAI: phi chỉ sống bên trong tinhPhi
    }
}""", expect="compile_error:cannot find symbol")
    thieu = prog("ThieuTra", """
public class ThieuTra {
    static long tinhPhi(long soTien) {
        if (soTien < 500000) {
            return 0;
        } else if (soTien < 10000000) {
            return 2200;
        }
    }                                    // SAI: nhánh còn lại không trả gì

    public static void main(String[] args) {
        System.out.println(tinhPhi(2000000));
    }
}""", expect="compile_error:missing return statement")
    bo_qua = prog("BoQua", """
public class BoQua {
    static long truPhi(long soDu, long phi) {
        soDu = soDu - phi;               // chỉ đổi bản sao
        return soDu;
    }

    public static void main(String[] args) {
        long soDu = 500000;
        truPhi(soDu, 2200);              // SAI: bỏ đi giá trị trả về
        System.out.println(soDu);
        soDu = truPhi(soDu, 2200);       // ĐÚNG: gán lại giá trị trả về
        System.out.println(soDu);
    }
}""", out="500000\n497800")
    quiz = prog("DoanHam", """
public class DoanHam {
    static int gapDoi(int x) {
        x = x * 2;
        return x;
    }
    static int gapDoi(int x, int lan) {
        for (int i = 0; i < lan; i++) { x = gapDoi(x); }
        return x;
    }
    public static void main(String[] args) {
        int a = 5;
        int b = gapDoi(a);
        System.out.println(a + " " + b);
        System.out.println(gapDoi(a, 3));
    }
}""", out="5 10\n40")

    p_head, p_main = ln(phi, "static long tinhPhi"), ln(phi, "tinhPhi(300000)")
    sc_hook = sc("hook", "hook", "Biểu phí đổi, phải sửa ở bao nhiêu chỗ?", [
        st("""<p>Phép tính phí chuyển khoản xuất hiện ở ứng dụng điện thoại, ở quầy giao dịch, ở báo cáo cuối ngày… Mỗi chỗ chép lại cùng một đoạn rẽ nhánh.</p>
<div class="box warn">Biểu phí đổi: sửa mười chỗ, sót một chỗ, và khách hàng bị tính phí sai.</div>""",
           """Phép tính phí chuyển khoản xuất hiện ở ứng dụng điện thoại, ở quầy giao dịch, ở báo cáo cuối ngày, mỗi chỗ chép lại cùng một đoạn rẽ nhánh.
           Khi biểu phí đổi, chỉ cần sót một chỗ là khách hàng bị tính phí sai."""),
        st("""<p>Hôm nay ta học <b>hàm</b>, còn gọi là <b>phương thức</b>: đặt tên cho một đoạn mã, viết <b>một lần</b>, gọi ở <b>nhiều nơi</b>.</p>
<div class="box key">Sửa biểu phí khi đó chỉ cần sửa đúng một hàm.</div>""",
           """Hôm nay ta học hàm, trong Java còn gọi là phương thức. Ta đặt tên cho một đoạn mã, viết một lần, rồi gọi nó ở nhiều nơi.
           Khi biểu phí đổi, chỉ cần sửa đúng một hàm."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng hôm nay", [
        st(table(["đã học", "viết", "dùng lại hôm nay"],
                 [["① hàm chính: nơi chương trình bắt đầu", "<code>public static void main(String[] args)</code>", "hàm chính sẽ gọi hàm của ta"],
                  ["② rẽ nhánh theo bậc", "<code>if … else if … else</code>", "thân hàm tính phí"],
                  ["③ biến mảng giữ tham chiếu", "<code>long[] b = a;</code> thì <code>b</code>, <code>a</code> chung một mảng", "hàm nhận mảng"]]),
           """Trước hết ta ôn lại ba điều. Thứ nhất, hàm chính là nơi chương trình bắt đầu chạy, và bạn đã viết nó từ chương trình đầu tiên.
           Thứ hai, lệnh rẽ nhánh nếu, nếu không thì nếu, chọn một bậc phí theo số tiền.
           Thứ ba, biến mảng chỉ giữ tham chiếu, tức mũi tên chỉ tới dãy ô trong bộ nhớ, nên hai biến có thể cùng trỏ vào một mảng.""", focus=[1, "1.2", "1.3", "1.4"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ký hiệu của một hàm", [
        st(code_block(phi, lines=(p_head, p_head + 7), title="Tệp Phi.java: hàm tính phí")
           + code_block(phi, lines=(p_main, p_main + 2)),
           """Đây là hàm tính phí chuyển khoản, với biểu phí là số minh hoạ. Bên dưới là ba lời gọi hàm từ hàm chính.""",
           focus=[2, 3]),
        st(table(["viết", "nghĩa"],
                 [["<code>static</code>", "<b>tĩnh</b>: hàm thuộc về lớp (cái hộp chứa mã, ở đây là <code>Phi</code>), không cần tạo gì thêm, nên hàm chính gọi thẳng được"],
                  ["<code>long</code> trước tên", "<b>kiểu trả về</b>: hàm trả ra một số kiểu <code>long</code>"],
                  ["<code>tinhPhi</code>", "tên hàm, thường là động từ: tính, kiểm, đổi…"],
                  ["<code>(long soTien)</code>", "<b>tham số</b>: biến nhận giá trị mỗi lần hàm được gọi"],
                  ["<code>return 2200;</code>", "trả giá trị về chỗ gọi và <b>kết thúc hàm ngay</b>"],
                  ["<code>tinhPhi(2000000)</code>", "<b>lời gọi</b>; 2000000 là đối số, được chép vào <code>soTien</code>"],
                  ["<code>void</code>", "đứng chỗ kiểu trả về: hàm <b>không</b> trả giá trị nào"]]),
           """Từ khoá tĩnh nghĩa là hàm thuộc về lớp, tức cái hộp chứa mã mang tên Phi, không cần tạo thêm gì, nên hàm chính gọi thẳng được.
           Chữ đứng trước tên hàm là kiểu trả về, ở đây là số nguyên dài.
           Tên hàm thường là một động từ, như tính, kiểm, đổi.
           Trong ngoặc tròn là tham số, nhận giá trị mỗi lần hàm được gọi.
           Lệnh trả về đưa giá trị về chỗ gọi, và kết thúc hàm ngay.
           Lời gọi hàm ghi tên hàm và đối số, đối số được chép vào tham số.
           Hàm không trả giá trị nào thì ở chỗ kiểu trả về ghi một từ khoá riêng, nghĩa là không trả gì.""", clear=True,
           focus=["1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: gọi hàm là gửi đi một bản sao, chờ nhận kết quả", [
        st(svg(1500, 360,
               box(40, 110, 400, 150, ["hàm chính", "in tinhPhi(2000000)", "đứng chờ…"], C_BLUE, 26, True),
               arrow(450, 150, 1030, 150, "#2a78d6", "① gọi: chép 2000000 vào soTien"),
               box(1040, 110, 420, 150, ["tinhPhi", "soTien = 2000000", "return 2200"], C_GREEN, 26, True),
               arrow(1030, 230, 450, 230, "#16a34a", "② trả về 2200, hàm chính chạy tiếp"),
               txt(750, 330, "tham số là biến RIÊNG của hàm, sinh ra khi gọi và mất đi khi hàm trả về", 24, "middle", "#1f2937", True)),
           """Hãy hình dung lời gọi hàm như gửi một phiếu yêu cầu. Hàm chính chép hai triệu vào tham số của hàm tính phí, rồi đứng chờ.
           Gặp lệnh trả về, hàm tính phí gửi lại hai nghìn hai trăm, và hàm chính chạy tiếp từ chỗ đã dừng.
           Tham số là biến riêng của hàm, sinh ra khi gọi và mất đi khi hàm trả về."""),
        st(svg(1500, 400,
               panel(20, 20, 700, 360, "số nguyên: chép GIÁ TRỊ", C_BLUE),
               box(60, 120, 260, 90, ["soDu (hàm chính)", "500000"], C_AMBER, 24),
               box(420, 120, 260, 90, ["x (tangSo)", "500000 → 600000"], C_AMBER, 24),
               arrow(325, 165, 410, 165, "#d97706", "chép"),
               txt(370, 300, "đổi x không đụng tới soDu", 24, "middle", "#dc2626", True),
               panel(780, 20, 700, 360, "mảng: chép MŨI TÊN", C_GREEN),
               box(820, 100, 220, 80, ["a (hàm chính)"], C_AMBER, 24),
               box(820, 240, 220, 80, ["m (tangO)"], C_AMBER, 24),
               arrow(1045, 140, 1230, 190, "#d97706"),
               arrow(1045, 280, 1230, 225, "#d97706"),
               box(1240, 160, 200, 90, ["500000", "→ 600000"], C_BLUE, 24, True),
               txt(1130, 360, "hai tên, MỘT mảng", 24, "middle", "#16a34a", True)),
           """Java luôn truyền theo giá trị, nghĩa là tham số nhận một bản sao của đối số.
           Với số nguyên, bản sao là chính con số, nên hàm đổi bản sao không làm đổi biến của người gọi.
           Với mảng, bản sao là mũi tên tham chiếu, nên hai tên cùng trỏ vào một mảng, và hàm đổi được các ô."""),
        st(code_block(gia_tri, lines=(2, 8), title="Tệp GiaTri.java: hai hàm"),
           """Chạy thật để kiểm hình vẽ. Hàm thứ nhất tăng bản sao của số dư, hàm thứ hai tăng ô đầu của mảng."""),
        st(code_block(gia_tri, lines=(ln(gia_tri, "long soDu"), ln(gia_tri, "tangO(a)") + 1), title="Hàm chính gọi cả hai")
           + out_block(gia_tri),
           """Hàm chính gọi cả hai hàm với số dư và mảng cùng bằng năm trăm nghìn.
           Kết quả in ra năm trăm nghìn và sáu trăm nghìn, đúng như hình.""", focus=[2, 4]),
    ])
    n2 = ln(nap, "int soLan")
    sc_form = sc("formula", "formula", "Suy ra từng bước: tách phép tính phí thành một hàm", [
        st("<p><b>Bước 1. Hỏi đầu vào và đầu ra.</b> Cần biết gì? Số tiền chuyển. Trả ra gì? Số tiền phí.</p>"
           + code_block(phi, lines=(p_head, p_head)),
           """Bước một, hỏi hai câu. Hàm cần biết gì để làm việc, đó là số tiền chuyển, nên ta có một tham số số nguyên dài.
           Hàm trả ra gì, đó là số tiền phí, nên kiểu trả về cũng là số nguyên dài."""),
        st("<p><b>Bước 2. Viết thân hàm.</b> Mỗi nhánh kết thúc bằng một lệnh <code>return</code>.</p>"
           + code_block(phi, lines=(p_head + 1, p_head + 6)),
           """Bước hai, viết thân hàm bằng lệnh rẽ nhánh đã học, mỗi nhánh kết thúc bằng một lệnh trả về.
           Dòng trả về cuối cùng phục vụ mọi số tiền từ mười triệu trở lên, vì hai nhánh trên đã trả về trước đó."""),
        st("<p><b>Bước 3. Gọi hàm với ba số tiền.</b></p>" + code_block(phi, lines=(p_main, p_main + 2)) + out_block(phi),
           """Bước ba, gọi hàm từ hàm chính với ba số tiền. Ba trăm nghìn nhỏ hơn năm trăm nghìn nên phí bằng không.
           Hai triệu rơi vào bậc giữa nên phí là hai nghìn hai trăm. Mười triệu không nhỏ hơn mười triệu, nên phí là năm nghìn năm trăm.""",
           focus=[2, "4.1", "4.2", "4.3"]),
        st("<p><b>Bước 4. Nạp chồng:</b> cùng tên, khác danh sách tham số.</p>"
           + code_block(nap, lines=(n2, n2 + 2)) + out_block(nap),
           """Bước bốn, nạp chồng. Hai hàm được trùng tên nếu danh sách tham số khác nhau, và trình biên dịch chọn hàm theo số lượng và kiểu đối số.
           Gọi thêm số lần là ba thì ra sáu nghìn sáu trăm, vì hai nghìn hai trăm nhân ba.""", focus=[1, 2, 4]),
    ], checks=["[(0 if x < 500000 else (2200 if x < 10000000 else 5500)) for x in [300000, 2000000, 10000000]] == [0, 2200, 5500]",
               "2200 * 3 == 6600"])
    g11, g16 = ln(goi, "static long tongTru"), ln(goi, "long soDu = 5000000")
    sc_ex = sc("example", "example", "Ví dụ: lần theo các lời gọi lồng nhau, từng phép tính", [
        st(code_block(goi, lines=(g11, g11 + 3), title="Tệp Goi.java: hàm gọi hàm")
           + code_block(goi, lines=(g16, g16 + 2)),
           """Ví dụ này có thêm hàm tính tổng tiền bị trừ, nó gọi lại hàm tính phí. Hàm chính có số dư năm triệu và chuyển đi hai triệu.
           Ta lần theo từng lời gọi.""", focus=[2, 3, 3]),
        st(code_block(goi, lines=(g16 + 1, g16 + 1))
           + "$$① \\; \\text{tongTru}(2000000) \\to \\text{soTien} = \\hl{2000000}$$"
           + "$$② \\; \\text{tinhPhi}(2000000) \\to \\text{soTien} = \\hl{2000000}$$",
           """Phép tính thứ nhất, hàm chính gọi hàm tổng bị trừ, và hai triệu được chép vào tham số của nó.
           Phép tính thứ hai, hàm này gọi tiếp hàm tính phí, và hai triệu lại được chép vào tham số riêng của hàm tính phí."""),
        st(code_block(goi, lines=(3, 6))
           + "$$③ \\; 2000000 \\ge 500000 \\text{ và } 2000000 \\text{ nhỏ hơn } 10000000 \\to \\text{return } \\hl{2200}$$",
           """Phép tính thứ ba, trong hàm tính phí, hai triệu không nhỏ hơn năm trăm nghìn, nhưng nhỏ hơn mười triệu.
           Vì vậy nhánh thứ hai chạy và trả về hai nghìn hai trăm."""),
        st(code_block(goi, lines=(g11 + 1, g11 + 2))
           + "$$④ \\; \\text{phi} = 2200, \\quad 2000000 + 2200 = \\hl{2002200}$$"
           + "$$⑤ \\; 5000000 - 2002200 = \\hlg{2997800}$$",
           """Phép tính thứ tư, quay về hàm tổng bị trừ, biến phí nhận hai nghìn hai trăm, và hàm trả về hai triệu không trăm linh hai nghìn hai trăm.
           Phép tính thứ năm, quay về hàm chính, số dư thành hai triệu chín trăm chín mươi bảy nghìn tám trăm."""),
        st(out_block(goi),
           """Chạy thật chương trình, dòng in ra đúng là hai triệu chín trăm chín mươi bảy nghìn tám trăm."""),
    ], checks=["(0 if 2000000 < 500000 else (2200 if 2000000 < 10000000 else 5500)) == 2200",
               "2000000 + 2200 == 2002200", "5000000 - 2002200 == 2997800"])
    k5 = ln(kiem, "long[] thu")
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: trừ từng khoản và thử ở biên", [
        st("<p>Đường khác cho ví dụ: trừ <b>từng khoản</b> thay vì trừ tổng.</p>"
           "$$5000000 - 2000000 - 2200 = 2997800 \\; \\checkmark$$",
           """Đường kiểm thứ nhất, trừ từng khoản thay vì trừ một tổng. Năm triệu trừ hai triệu, rồi trừ tiếp phí, vẫn ra đúng số cũ.
           Kết quả khớp, nên phép gọi lồng đã cộng phí đúng."""),
        st(code_block(kiem, lines=(k5, k5 + 3), title="Tệp KiemPhi.java: thử bốn số tiền ở biên"),
           """Đường kiểm thứ hai, thử hàm ở biên, vì lỗi bậc phí thường nằm sát ranh giới.
           Mỗi ranh giới có một số ngay dưới và một số đúng bằng nó, và vòng lặp đếm gọi hàm cho từng số."""),
        st(out_block(kiem) + table(["số tiền", "theo biểu phí (tính tay)", "máy in ra"],
                                   [["499999", "dưới 500000 → 0", "0 ✓"], ["500000", "không dưới 500000 → 2200", "2200 ✓"],
                                    ["9999999", "dưới 10000000 → 2200", "2200 ✓"], ["10000000", "không dưới 10000000 → 5500", "5500 ✓"]]),
           """Ta tính tay theo biểu phí rồi so với máy. Số ngay dưới năm trăm nghìn có phí bằng không.
           Năm trăm nghìn thì không còn dưới mức ấy, nên phí là hai nghìn hai trăm.
           Hai số quanh mười triệu cũng khớp, nên hàm đúng ở cả hai ranh giới.""", focus=[3, "3.2", "3.3", ["3.4", "3.5"]]),
    ], checks=["5000000 - 2000000 - 2200 == 5000000 - 2002200",
               "[(0 if x < 500000 else (2200 if x < 10000000 else 5500)) for x in [499999, 500000, 9999999, 10000000]] == [0, 2200, 2200, 5500]"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Dùng biến của hàm khác.</div>'
           + code_block(pham_vi, lines=(3, 10)) + out_block(pham_vi, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là dùng biến khai bên trong một hàm khác. Biến phí chỉ sống bên trong hàm tính phí.
           Vùng mã mà một tên biến dùng được gọi là phạm vi của biến, ở đây là cặp ngoặc nhọn của hàm tính phí.
           Ra khỏi phạm vi đó, tên này không còn tồn tại, nên trình biên dịch báo không tìm thấy ký hiệu.""",
           focus=[1, 2, 2, 4]),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Có nhánh không trả về giá trị.</div>'
           + code_block(thieu, lines=(3, 9)) + out_block(thieu, "Trình biên dịch báo"),
           """Lỗi thứ hai là quên lệnh trả về ở một nhánh. Hàm hứa trả về số nguyên dài, nhưng khi số tiền từ mười triệu trở lên thì không có lệnh trả về nào chạy.
           Trình biên dịch phát hiện ngay, và báo thiếu lệnh trả về.""", focus=[1, 2, 4]),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tưởng hàm sửa được biến số nguyên của người gọi.</div>'
           + code_block(bo_qua, lines=(2, 4)) + code_block(bo_qua, lines=(8, 12)) + out_block(bo_qua),
           """Lỗi thứ ba gặp cả ở người đã đi làm: gọi hàm trừ phí rồi bỏ đi giá trị trả về, vì tưởng hàm đã sửa số dư.
           Hàm chỉ sửa bản sao, nên số dư vẫn là năm trăm nghìn, mà không có báo lỗi nào.
           Cách đúng là gán lại giá trị trả về, khi đó số dư mới là bốn trăm chín mươi bảy nghìn tám trăm.""",
           focus=[3, [2, 5], [3, 5]]),
    ])
    q_main = ln(quiz, "int a = 5")
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(2, 9), title="Đoán hai dòng in ra") + code_block(quiz, lines=(q_main, q_main + 3)),
           """Bây giờ tới phần bạn tự làm. Có hai hàm gấp đôi trùng tên: một hàm nhận một số, một hàm nhận thêm số lần lặp.
           Hàm chính gọi gấp đôi với biến a bằng năm, in a và b, rồi gọi bản hai tham số với số lần là ba.
           Hãy dừng video, viết ra giấy hai dòng in ra.""", pause=20, focus=[1, 2, 3, 3]),
        st("<p>Dòng thứ nhất: tham số <code>x</code> là bản sao, nên <code>a</code> vẫn là 5.</p>"
           "$$\\text{gapDoi}(5) = 5 \\times 2 = 10 \\quad \\to \\quad \\hl{\\text{5 10}}$$",
           """Đáp án như sau. Hàm gấp đôi chỉ nhân đôi bản sao, nên a vẫn là năm, còn b nhận giá trị trả về là mười.
           Dòng thứ nhất là năm mười."""),
        st("<p>Dòng thứ hai: bản hai tham số gọi bản một tham số ba lần.</p>"
           "$$5 \\to 10 \\to 20 \\to \\hl{40}$$",
           """Dòng thứ hai, trình biên dịch chọn bản hai tham số vì có hai đối số. Vòng lặp chạy ba lần, mỗi lần gọi bản một tham số, nên năm thành mười, rồi hai mươi, rồi bốn mươi."""),
        st(out_block(quiz),
           """Chạy thật chương trình, hai dòng in ra đúng là năm mười, và bốn mươi."""),
    ], checks=["5 * 2 == 10", "5 * 2 ** 3 == 40"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("đặt tên một việc", "tham số nhận bản sao", "return trả kết quả", "người gọi gán lại kết quả"),
           """Tổng kết chuỗi logic. Ta đặt tên cho một việc thành một hàm, tham số nhận bản sao của đối số,
           lệnh trả về đưa kết quả ra, và người gọi phải gán lại kết quả đó."""),
        st("""<div class='box key'><b>Tư duy:</b> mỗi hàm làm <b>một việc</b>, tên là động từ nói đúng việc đó. Hàm dài quá một màn hình
hoặc vừa tính, vừa in, vừa sửa dữ liệu là dấu hiệu nên tách. Muốn đổi số của người gọi thì <b>trả về</b> giá trị mới.</div>""",
           """Điều cần mang theo. Mỗi hàm chỉ làm một việc, với tên là động từ nói đúng việc đó.
           Hàm quá dài, hoặc vừa tính, vừa in, vừa sửa dữ liệu, là dấu hiệu nên tách nhỏ.
           Muốn đổi số của người gọi thì trả về giá trị mới."""),
    ])
    return lesson("L06", "phuong_thuc", "Bài 6 — Phương thức (hàm): viết một lần, gọi nhiều nơi",
                  "curriculum/jva.yaml L06; audit/jva/verify_jva.py L06 (javac/java chạy thật); The Java Language Specification, "
                  "Java SE 21 (JLS §8.4 khai báo phương thức, §8.4.7 thân và missing return, §8.4.9 nạp chồng, "
                  "§15.12.4 gọi phương thức: đối số được chép vào tham số, §6.3 phạm vi biến); dev.java/learn; biểu phí là số minh hoạ",
                  ["Khai báo hàm tĩnh có tham số, kiểu trả về và lệnh trả về; gọi hàm, kể cả gọi lồng",
                   "Giải thích truyền theo giá trị: hàm không đổi được biến số nguyên của người gọi nhưng đổi được ô của mảng",
                   "Viết hai hàm nạp chồng và biết máy chọn hàm nào",
                   "Nhận ra lỗi phạm vi biến, thiếu lệnh trả về, bỏ quên giá trị trả về"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
