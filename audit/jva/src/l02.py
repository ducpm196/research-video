from lib import *


def build():
    bay = prog("Bay", """
public class Bay {
    public static void main(String[] args) {
        System.out.println(7 / 2);      // hai số nguyên
        System.out.println(7.0 / 2);    // có một số thực
    }
}""", out="3\n3.5")
    phep_gan = prog("PhepGan", """
public class PhepGan {
    public static void main(String[] args) {
        long soDu = 100000;
        soDu += 50000;                  // như soDu = soDu + 50000
        soDu -= 20000;                  // như soDu = soDu - 20000
        int soLenh = 0;
        soLenh++;                       // tăng thêm 1
        soLenh++;
        System.out.println(soDu + " dong, " + soLenh + " lenh");
        System.out.println(soDu >= 100000);   // so sánh: ra đúng hoặc sai
    }
}""", out="130000 dong, 2 lenh\ntrue")
    uu_tien = prog("UuTien", """
public class UuTien {
    public static void main(String[] args) {
        System.out.println(2 + 3 * 4);      // nhân trước, cộng sau
        System.out.println((2 + 3) * 4);    // ngoặc trước
        System.out.println(20 - 5 - 3);     // cùng mức: từ trái sang phải
    }
}""", out="14\n20\n12")
    ngan_mach = prog("NganMach", """
public class NganMach {
    public static void main(String[] args) {
        long tong = 300000;
        int soNguoi = 0;
        // vế trái sai thì && dừng luôn, không tính vế phải, nên không chia cho 0
        boolean moiNguoiTren = soNguoi != 0 && tong / soNguoi > 50000;
        System.out.println(moiNguoiTren);
    }
}""", out="false")
    chia_deu = prog("ChiaDeu", """
public class ChiaDeu {
    public static void main(String[] args) {
        System.out.println(100000 / 3);     // mỗi người được bao nhiêu
        System.out.println(100000 % 3);     // còn dư bao nhiêu đồng
        System.out.println(-100000 / 3);
        System.out.println(-100000 % 3);
    }
}""", out="33333\n1\n-33333\n-1")
    chia_nam = prog("ChiaNam", """
public class ChiaNam {
    public static void main(String[] args) {
        System.out.println(7 / 2);            // (1)
        System.out.println(7 % 2);            // (2)
        System.out.println((double) 7 / 2);   // (3)
        System.out.println(-7 / 2);           // (4)
        System.out.println(-7 % 2);           // (5)
    }
}""", out="3\n1\n3.5\n-3\n-1")
    kiem_chia = prog("KiemChia", """
public class KiemChia {
    public static void main(String[] args) {
        int a = 7;
        int b = -7;
        System.out.println((a / 2) * 2 + a % 2);   // phải ra lại 7
        System.out.println((b / 2) * 2 + b % 2);   // phải ra lại -7
    }
}""", out="7\n-7")
    nguoc = prog("Nguoc", """
public class Nguoc {
    public static void main(String[] args) {
        long tong = 300000;
        int soNguoi = 0;
        boolean moiNguoiTren = tong / soNguoi > 50000 && soNguoi != 0;
        System.out.println(moiNguoiTren);
    }
}""", expect="runtime_error:ArithmeticException",
        err='Exception in thread "main" java.lang.ArithmeticException: / by zero')
    ep_muon = prog("EpMuon", """
public class EpMuon {
    public static void main(String[] args) {
        System.out.println((double) (7 / 2));   // chia nguyên xong mới ép
        System.out.println((double) 7 / 2);     // ép trước rồi mới chia
    }
}""", out="3.0\n3.5")
    phi_pt = prog("PhiPhanTram", """
public class PhiPhanTram {
    public static void main(String[] args) {
        long soTien = 1234567;                     // số tiền chuyển (đồng)
        // phí 0,5% (số minh hoạ) = soTien * 5 / 1000
        System.out.println(soTien * (5 / 1000));   // 5 / 1000 ra 0
        System.out.println(soTien / 1000 * 5);     // chia trước, mất phần lẻ
        System.out.println(soTien * 5 / 1000);     // nhân trước rồi mới chia
    }
}""", out="0\n6170\n6172")
    quiz = prog("DoanToan", """
public class DoanToan {
    public static void main(String[] args) {
        int a = 17;
        int b = 5;
        System.out.println(a / b + " " + a % b);
        System.out.println((double) a / b);
        System.out.println(a > 10 && a % 2 == 0);
    }
}""", out="3 2\n3.4\nfalse")

    sc_hook = sc("hook", "hook", "Bảy chia hai, vì sao Java trả lời là ba?", [
        st(code_block(bay, lines=(3, 4)) + out_block(bay),
           """Trên máy tính bỏ túi, bảy chia hai ra ba phẩy năm. Trong Java, dòng đầu in ra ba, còn dòng thứ hai lại in ra ba phẩy năm.
           Hai dòng chỉ khác nhau ở phần chấm không viết sau số bảy."""),
        st("""<p>Với tiền, phần lẻ bị bỏ đi là <b>tiền thật</b> bị mất hoặc bị thừa.</p>
<div class="box key">Hôm nay: các phép toán <code>+ - * / %</code>, ép kiểu, thứ tự tính, phép so sánh và phép logic, kể cả mẹo <b>ngắn mạch</b> để tránh chia cho 0.</div>""",
           """Với tiền, phần lẻ bị bỏ đi là tiền thật bị mất hoặc bị thừa. Hôm nay ta học các phép toán, cách ép kiểu, thứ tự tính,
           phép so sánh và phép logic, kể cả mẹo ngắn mạch để tránh chia cho không."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại biến và kiểu từ bài trước", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① biến", "ngăn nhớ có tên, khai bằng kiểu + tên + giá trị"],
                  ["② kiểu", "<code>int</code>, <code>long</code>: số nguyên; <code>double</code>: số thực; <code>boolean</code>: đúng hoặc sai"],
                  ["③ gán <code>=</code>", "tính vế phải trước, rồi ghi đè vào ngăn bên trái"],
                  ["④ chia cho 0", "số nguyên chia cho 0 là lỗi khi chạy, chương trình dừng"]]),
           """Ta ôn lại từ hai bài trước. Biến là ngăn nhớ có tên, khai bằng kiểu, tên và giá trị.
           Kiểu số nguyên chứa số nguyên, kiểu số thực chứa số có phần lẻ, kiểu đúng sai chỉ có đúng hoặc sai.
           Phép gán tính vế phải rồi ghi đè. Còn chia số nguyên cho không là lỗi khi chạy.""", focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã các phép toán", [
        st(table(["viết", "đọc là", "ghi chú"],
                 [["<code>+ - *</code>", "cộng, trừ, nhân", "như toán"],
                  ["<code>/</code>", "chia", "hai số nguyên thì <b>bỏ phần lẻ</b>"],
                  ["<code>%</code>", "chia lấy dư", "phần còn lại sau phép chia nguyên"],
                  ["<code>(double) x</code>", "ép kiểu", "đổi x thành số thực trước khi tính tiếp"],
                  ["<code>x += 5</code>", "cộng dồn", "viết gọn của <code>x = x + 5</code>; có cả <code>-=</code>, <code>*=</code>"],
                  ["<code>x++</code>, <code>x--</code>", "tăng một, giảm một", "viết gọn của <code>x = x + 1</code> và <code>x = x - 1</code>"]]),
           """Bảng thứ nhất là các phép tính. Cộng, trừ, nhân giống toán, còn chia hai số nguyên thì bỏ phần lẻ.
           Dấu phần trăm là phép chia lấy dư. Tên kiểu trong ngoặc đặt trước một số là ép kiểu, đổi số đó thành số thực.
           Cộng bằng là viết gọn của cộng dồn, hai dấu cộng liền nhau là tăng thêm một, hai dấu trừ liền nhau là giảm đi một.""",
           focus=[1, ["1.2", "1.3"], "1.4", "1.5", ["1.6", "1.7"]]),
        st(table(["viết", "đọc là", "kết quả"],
                 [["<code>==</code>  <code>!=</code>", "bằng, khác", "đúng hoặc sai"],
                  ["<code>&lt;</code>  <code>&lt;=</code>  <code>&gt;</code>  <code>&gt;=</code>", "nhỏ hơn, nhỏ hơn hoặc bằng, lớn hơn, lớn hơn hoặc bằng", "đúng hoặc sai"],
                  ["<code>a &amp;&amp; b</code>", "a <b>và</b> b", "đúng khi cả hai đúng"],
                  ["<code>a || b</code>", "a <b>hoặc</b> b", "đúng khi ít nhất một vế đúng"],
                  ["<code>!a</code>", "<b>không phải</b> a", "đảo đúng thành sai và ngược lại"]]),
           """Bảng thứ hai là phép so sánh và phép logic, kết quả luôn là đúng hoặc sai. Hai dấu bằng liền nhau là so sánh bằng, còn một dấu bằng là phép gán.
           Hai dấu và là phép và, đúng khi cả hai vế đúng. Hai vạch đứng là phép hoặc, đúng khi ít nhất một vế đúng.
           Dấu chấm than đảo đúng thành sai.""", clear=True, focus=[["1.2", "1.3"], "1.2", "1.4", "1.5", "1.6"]),
        st(code_block(phep_gan, lines=(3, 10)) + out_block(phep_gan),
           """Chương trình này dùng thử. Số dư một trăm nghìn, cộng dồn năm mươi nghìn, trừ bớt hai mươi nghìn, còn một trăm ba mươi nghìn.
           Số lệnh tăng một hai lần thành hai. Dòng cuối so sánh số dư với một trăm nghìn, kết quả là giá trị đúng."""),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: chia kẹo, thứ tự tính và cửa ngắn mạch", [
        st(svg(1500, 360,
               txt(750, 40, "7 viên kẹo chia đều cho 2 người", 26, "middle", "#1f2937", True),
               box(80, 80, 420, 140, ["người 1", "● ● ●"], C_BLUE, size=28, bold=True),
               box(560, 80, 420, 140, ["người 2", "● ● ●"], C_BLUE, size=28, bold=True),
               box(1040, 80, 380, 140, ["còn lại", "●"], C_AMBER, size=28, bold=True),
               txt(540, 280, "7 / 2 = 3  (mỗi người được 3: thương)", 26, "middle", "#2a78d6", True),
               txt(1230, 280, "7 % 2 = 1  (số dư)", 26, "middle", "#d97706", True),
               txt(750, 335, "kiểm lại: 3 × 2 + 1 = 7", 24, "middle", "#1f2937")),
           """Hãy hình dung bảy viên kẹo chia đều cho hai người. Mỗi người được ba viên, đó là phép chia nguyên.
           Còn thừa một viên không chia được, đó là phép chia lấy dư. Ba nhân hai cộng một lại ra đúng bảy."""),
        st(code_block(uu_tien, lines=(3, 5)) + out_block(uu_tien),
           """Thứ tự tính giống toán. Nhân, chia và chia lấy dư làm trước cộng trừ, nên hai cộng ba nhân bốn là mười bốn.
           Phần trong ngoặc luôn được làm trước, nên dòng hai cho kết quả là hai mươi. Các phép cùng mức thì làm từ trái sang phải, nên hai mươi trừ năm trừ ba là mười hai."""),
        st(svg(1500, 300,
               box(40, 90, 360, 120, ["vế trái", "soNguoi != 0"], C_BLUE, bold=True),
               arrow(405, 150, 560, 150, "#dc2626", "sai"),
               box(570, 90, 380, 120, ["dừng: cả biểu thức", "là SAI"], C_RED, bold=True),
               arrow(220, 215, 220, 270, "#16a34a"),
               txt(240, 262, "đúng → mới tính vế phải", 22, "start", "#16a34a", True),
               box(1010, 90, 450, 120, ["vế phải", "tong / soNguoi > 50000"], C_GRAY, dash=True),
               txt(1235, 60, "không bao giờ được tính khi vế trái sai", 22, "middle", "#6b7280")),
           """Phép và có một tính chất quan trọng tên là ngắn mạch. Máy luôn tính giá trị của vế trái trước tiên. Nếu vế trái sai thì cả biểu thức chắc chắn sai,
           nên máy dừng luôn, không tính vế phải. Phép hoặc cũng vậy, vế trái đúng thì dừng."""),
        st(code_block(ngan_mach, lines=(3, 7)) + out_block(ngan_mach),
           """Nhờ vậy ta đặt phép kiểm số người khác không ở vế trái. Số người bằng không nên vế trái sai, máy không chạy tới phép chia,
           và chương trình in giá trị sai một cách bình thường, không lỗi."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: chia đều một trăm nghìn cho ba người", [
        st("""<p><b>Bước 1. Thương.</b> Hai vế đều là số nguyên nên kết quả là số nguyên: phần lẻ bị <b>bỏ đi</b>.</p>
$$100\\,000 / 3 = 33\\,333.333... \\to \\hl{33\\,333}$$""",
           """Bước một, tính thương. Một trăm nghìn chia ba bằng ba mươi ba nghìn ba trăm ba mươi ba phẩy ba ba mãi.
           Vì hai vế đều là số nguyên nên Java bỏ phần lẻ, mỗi người được ba mươi ba nghìn ba trăm ba mươi ba đồng."""),
        st("""<p><b>Bước 2. Số dư</b> là phần chưa chia được: lấy số ban đầu trừ phần đã chia.</p>
$$100\\,000 \\,\\%\\, 3 = 100\\,000 - 33\\,333 \\times 3 = 100\\,000 - 99\\,999 = \\hl{1}$$""",
           """Bước hai, tính số dư. Ba người nhận tổng cộng chín mươi chín nghìn chín trăm chín mươi chín đồng,
           nên còn dư đúng một đồng. Nghĩa là số dư bằng số ban đầu trừ đi thương nhân số chia."""),
        st("""<p><b>Bước 3. Số âm.</b> Java bỏ phần lẻ bằng cách làm tròn <b>về phía 0</b>, nên thương không thành −33 334. Số dư mang dấu của số bị chia:</p>
$$-100\\,000 / 3 \\to \\hl{-33\\,333} \\qquad -100\\,000 - (-33\\,333) \\times 3 = \\hl{-1}$$""",
           """Bước ba, với số âm. Java bỏ phần lẻ bằng cách làm tròn về phía số không, nên thương là âm ba mươi ba nghìn ba trăm ba mươi ba.
           Theo cùng công thức ở bước hai, số dư là âm một, tức là số dư mang dấu của số bị chia."""),
        st(code_block(chia_deu, lines=(3, 6)) + out_block(chia_deu),
           """Bước bốn, chạy thật để đối chiếu. Bốn dòng in ra đúng bốn con số ta vừa suy ra, cả hai số âm."""),
    ], checks=["100000 // 3 == 33333", "100000 - 33333 * 3 == 1", "100000 % 3 == 1",
               "int(-100000 / 3) == -33333", "math.fmod(-100000, 3) == -1", "-100000 - (-33333) * 3 == -1"])
    sc_ex = sc("example", "example", "Ví dụ: năm phép chia với bảy và hai", [
        st(code_block(chia_nam, title="Tệp ChiaNam.java"),
           """Bây giờ ta áp dụng cho năm phép tính với bảy và hai. Hãy đoán từng dòng trước khi xem kết quả."""),
        st(code_block(chia_nam, lines=(3, 4)) + "$$① \\; 7 / 2 = 3.5 \\to \\hl{3} \\qquad ② \\; 7 \\,\\%\\, 2 = 7 - 3 \\times 2 = \\hl{1}$$",
           """Phép tính thứ nhất, bảy chia hai là ba phẩy năm, bỏ phần lẻ còn ba, vì cả hai là số nguyên.
           Phép tính thứ hai, số dư là bảy trừ ba nhân hai, bằng một."""),
        st(code_block(chia_nam, lines=(5, 5)) + "$$③ \\; (\\text{double})\\, 7 / 2 = 7.0 / 2 = \\hl{3.5}$$",
           """Phép tính thứ ba, phép ép kiểu làm trước phép chia, nên số bảy thành bảy phẩy không trước.
           Có một vế là số thực nên phép chia giữ phần lẻ, ra ba phẩy năm."""),
        st(code_block(chia_nam, lines=(6, 7))
           + "$$④ \\; -7 / 2 = -3.5 \\to \\hl{-3} \\qquad ⑤ \\; -7 \\,\\%\\, 2 = -7 - (-3) \\times 2 = \\hl{-1}$$",
           """Phép tính thứ tư, âm bảy chia hai là âm ba phẩy năm, làm tròn về phía không thành âm ba, không phải âm bốn.
           Phép tính thứ năm, số dư là âm bảy trừ âm ba nhân hai, bằng âm một."""),
        st(out_block(chia_nam),
           """Chạy thật, năm dòng in ra là ba, một, ba phẩy năm, âm ba và âm một, đúng như ta đã tính."""),
    ], checks=["7 // 2 == 3", "7 % 2 == 1", "7 / 2 == 3.5", "int(-7 / 2) == -3", "math.fmod(-7, 2) == -1"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: ghép thương và dư phải ra lại số ban đầu", [
        st("""<p>Luật luôn đúng với số nguyên (b khác 0): <b>thương × số chia + dư = số ban đầu</b>.</p>"""
           + table(["số ban đầu", "thương", "dư", "ghép lại"],
                   [["7", "3", "1", "3 × 2 + 1 = 7 ✓"], ["−7", "−3", "−1", "(−3) × 2 + (−1) = −7 ✓"]]),
           """Đường kiểm khác là một luật luôn đúng với số nguyên. Thương nhân số chia, cộng số dư, phải ra lại số ban đầu.
           Với bảy, ba nhân hai cộng một là bảy. Với âm bảy, âm ba nhân hai cộng âm một là âm bảy, nên cả hai cặp thương và dư đều khớp."""),
        st(code_block(kiem_chia, lines=(3, 6)) + out_block(kiem_chia),
           """Ta cũng nhờ Java tự ghép lại, và nó in ra đúng bảy và âm bảy.
           Nếu ai đó nghĩ âm bảy chia hai ra âm bốn thì ghép lại sẽ không khớp, nghĩa là luật này bắt được hiểu sai."""),
    ], checks=["(7 // 2) * 2 + 7 % 2 == 7", "int(-7 / 2) * 2 + math.fmod(-7, 2) == -7", "(-4) * 2 + math.fmod(-7, 2) != -7"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Đặt phép chia ở vế trái, phép kiểm ở vế phải.</div>'
           + code_block(nguoc, lines=(5, 5)) + out_block(nguoc),
           """Lỗi thứ nhất, của người mới, là đảo thứ tự hai vế. Máy tính vế trái trước, mà vế trái là phép chia cho số người bằng không.
           Chương trình dừng với lỗi chia cho không, phép kiểm ở vế phải không kịp chạy. Phép kiểm phải đứng trước phép chia."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới và cả người đã đi làm).</b> Ép kiểu sau khi đã chia nguyên.</div>'
           + code_block(ep_muon, lines=(3, 4)) + out_block(ep_muon),
           """Lỗi thứ hai là ép kiểu quá muộn. Ở dòng đầu, phần trong ngoặc là bảy chia hai được tính trước, ra ba, phần lẻ đã mất.
           Ép ba thành số thực chỉ được ba phẩy không. Muốn giữ phần lẻ thì phải ép trước khi chia, như dòng thứ hai."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tính phí phần trăm bằng số nguyên theo sai thứ tự.</div>'
           + code_block(phi_pt, lines=(3, 7)) + out_block(phi_pt),
           """Lỗi thứ ba là tính phí phần trăm bằng số nguyên, với mức phí minh hoạ không phẩy năm phần trăm.
           Dòng đầu tính năm chia một nghìn trước, ra không, nên phí bằng không. Dòng hai chia trước nên mất phần lẻ, thiếu hai đồng.
           Nhân trước rồi mới chia thì chỉ bỏ phần lẻ dưới một đồng."""),
        st("""<p>Phí đúng là $1\\,234\\,567 \\times 5 / 1000 = 6\\,172.835$. Phần lẻ $0.835$ đồng làm tròn thế nào là <b>quy định nghiệp vụ</b>,
không phải thói quen của phép chia: khi cần, dùng kiểu số thập phân chính xác <code>BigDecimal</code> với cách làm tròn ghi rõ.</p>""",
           """Phí chính xác có phần lẻ tám trăm ba mươi lăm phần nghìn đồng. Làm tròn phần lẻ thế nào là quy định nghiệp vụ, không nên để phép chia tự quyết.
           Khi cần, ta dùng kiểu số thập phân chính xác của bài trước, kèm cách làm tròn ghi rõ.""", clear=True),
    ], checks=["1234567 * (5 // 1000) == 0", "1234567 // 1000 * 5 == 6170", "1234567 * 5 // 1000 == 6172",
               "Fraction(1234567 * 5, 1000) == Fraction(6172835, 1000)"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(3, 7), title="Đoán ba dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Biến a là mười bảy, biến b là năm. Dòng đầu in thương và số dư, cách nhau một dấu cách.
           Dòng hai ép a thành số thực rồi chia. Dòng ba hỏi a lớn hơn mười và a chẵn. Hãy dừng video, viết ra ba dòng in ra.""", pause=20),
        st("""<p>Dòng ①: <code>/</code> và <code>%</code> làm trước <code>+</code>, rồi nối chữ từ trái sang phải:</p>
$$17 / 5 = \\hl{3} \\qquad 17 \\,\\%\\, 5 = 17 - 3 \\times 5 = \\hl{2} \\qquad 3 + \\text{\" \"} + 2 \\to \\text{3 2}$$""",
           """Đáp án dòng một. Phép chia và chia lấy dư làm trước phép cộng, nên ta có thương ba và số dư hai.
           Sau đó nối chữ từ trái sang phải, ra ba, dấu cách, hai."""),
        st("""<p>Dòng ②: ép trước rồi chia: $17.0 / 5 = \\hl{3.4}$. Dòng ③: $17 > 10$ đúng, nhưng $17 \\,\\%\\, 2 = 1$ nên “a chẵn” sai, cả biểu thức <b>sai</b>.</p>""",
           """Dòng hai, ép kiểu làm trước nên là mười bảy phẩy không chia năm, ra ba phẩy bốn.
           Dòng ba, mười bảy lớn hơn mười là đúng, nhưng mười bảy chia hai dư một nên vế chẵn là sai, và phép và cho kết quả sai."""),
        st(out_block(quiz),
           """Chạy thật, ba dòng in ra là ba dấu cách hai, ba phẩy bốn, và giá trị sai."""),
    ], checks=["17 // 5 == 3", "17 % 5 == 2", "17 / 5 == 3.4", "(17 > 10 and 17 % 2 == 0) == False"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("số nguyên / số nguyên: bỏ phần lẻ, về phía 0", "% là phần dư, dấu theo số bị chia",
                 "muốn phần lẻ: ép trước khi chia", "&& và || dừng sớm: kiểm trước, chia sau"),
           """Tổng kết chuỗi logic. Số nguyên chia số nguyên thì bỏ phần lẻ, làm tròn về phía không. Phép chia lấy dư cho phần còn lại, mang dấu của số bị chia.
           Muốn giữ phần lẻ thì ép kiểu trước khi chia. Phép và, phép hoặc dừng sớm, nên đặt phép kiểm trước phép chia."""),
        st("""<div class='box key'><b>Tư duy:</b> với mỗi phép chia, hỏi ba câu: hai vế là kiểu gì, số chia có thể bằng 0 không,
và phần lẻ bị bỏ đi thì <b>ai chịu</b>. Với tiền: nhân trước, chia sau, làm tròn theo quy định ghi rõ.</div>""",
           """Điều cần mang theo. Với mỗi phép chia, hãy hỏi ba câu. Hai vế là kiểu gì, số chia có thể bằng không không, và phần lẻ bị bỏ đi thì ai chịu.
           Với tiền, nhân trước, chia sau, và làm tròn theo quy định ghi rõ."""),
    ])
    return lesson("L02", "toan_tu_va_bieu_thuc", "Bài 2 — Toán tử và biểu thức",
                  "curriculum/jva.yaml L02; audit/jva/verify_jva.py L02 (javac/java chạy thật); The Java Language Specification, "
                  "Java SE 21: §15.17.2 (chia số nguyên làm tròn về phía 0), §15.17.3 (phần dư: (a/b)*b+(a%b)==a, dấu theo số bị chia), "
                  "§15.16 (ép kiểu), §15.7 (tính từ trái sang phải), §15.23–15.24 (&& và || chỉ tính vế phải khi cần), "
                  "§15.26.2 (gán ghép +=), §15.14.2 (++); dev.java/learn",
                  ["Tính đúng phép chia nguyên và chia lấy dư, kể cả với số âm",
                   "Ép kiểu đúng chỗ để giữ phần lẻ, và biết thứ tự tính của biểu thức",
                   "Dùng phép so sánh và phép logic, đặt phép kiểm trước nhờ ngắn mạch",
                   "Tính phí phần trăm bằng số nguyên theo thứ tự nhân trước, chia sau"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
