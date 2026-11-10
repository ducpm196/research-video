from lib import *


def build():
    ba_kieu = prog("BaKieu", """
public class BaKieu {
    public static void main(String[] args) {
        int i = 1;
        while (i <= 3) {                    // kiểm trước, đúng thì làm
            System.out.println("while " + i);
            i++;
        }
        for (int k = 1; k <= 3; k++) {      // bắt đầu; điều kiện; bước
            System.out.println("for " + k);
        }
        int n = 10;
        do {                                // làm trước, kiểm sau
            System.out.println("do " + n);
            n++;
        } while (n <= 3);
    }
}""", out="while 1\nwhile 2\nwhile 3\nfor 1\nfor 2\nfor 3\ndo 10")
    vuot = prog("VuotHanMuc", """
public class VuotHanMuc {
    public static void main(String[] args) {
        long hanMuc = 5000000;                      // hạn mức một lệnh (số minh hoạ)
        int dem = 0;
        for (int i = 1; i <= 8; i++) {
            long soTien = (i * 7 % 10) * 1000000L;  // giả lập số tiền lệnh thứ i
            if (soTien <= hanMuc) {
                continue;                           // không vượt: sang lệnh sau
            }
            dem++;
            System.out.println("Lenh " + i + ": " + soTien);
        }
        System.out.println("So lenh vuot: " + dem);
    }
}""", out="Lenh 1: 7000000\nLenh 4: 8000000\nLenh 7: 9000000\nLenh 8: 6000000\nSo lenh vuot: 4")
    lai_tay = prog("LaiTay", """
public class LaiTay {
    public static void main(String[] args) {
        long soDu = 100000000;
        soDu += soDu * 5 / 1000;      // tháng 1
        soDu += soDu * 5 / 1000;      // tháng 2
        soDu += soDu * 5 / 1000;      // tháng 3
        System.out.println(soDu);     // còn 9 dòng y hệt nữa mới đủ 12 tháng
    }
}""", out="101507512")
    lai = prog("LaiThang", """
public class LaiThang {
    public static void main(String[] args) {
        long soDu = 100000000;                      // 100 triệu đồng
        for (int thang = 1; thang <= 12; thang++) {
            long lai = soDu * 5 / 1000;             // 0,5% mỗi tháng (số minh hoạ)
            soDu += lai;                            // cộng dồn: lãi nhập vào gốc
            if (thang <= 3 || thang >= 11) {
                System.out.println("Thang " + thang + ": lai " + lai + ", so du " + soDu);
            }
        }
        System.out.println("Sau 12 thang: " + soDu);
    }
}""", out="Thang 1: lai 500000, so du 100500000\nThang 2: lai 502500, so du 101002500\n"
          "Thang 3: lai 505012, so du 101507512\nThang 11: lai 525570, so du 105639579\n"
          "Thang 12: lai 528197, so du 106167776\nSau 12 thang: 106167776")
    kiem_lai = prog("KiemLai", """
public class KiemLai {
    public static void main(String[] args) {
        double congThuc = 100000000 * Math.pow(1.005, 12);   // gốc nhân 1,005 mũ 12
        System.out.println((long) congThuc);                  // ép kiểu: bỏ phần lẻ
    }
}""", out="106167781")
    dem_thang = prog("DemThang", """
public class DemThang {
    public static void main(String[] args) {
        int lanA = 0;
        for (int thang = 1; thang < 12; thang++) {    // dấu < : dừng trước 12
            lanA++;
        }
        int lanB = 0;
        for (int thang = 1; thang <= 12; thang++) {   // dấu <= : chạy cả tháng 12
            lanB++;
        }
        System.out.println(lanA + " va " + lanB);
    }
}""", out="11 va 12")
    quen_tang = prog("QuenTang", """
public class QuenTang {
    public static void main(String[] args) {
        int thang = 1;
        int soVong = 0;                 // bộ đếm an toàn, chỉ để chương trình mẫu tự dừng
        while (thang <= 12) {
            soVong++;
            if (soVong == 1000) {
                System.out.println("Da 1000 vong, thang van = " + thang);
                break;                  // thoát hẳn vòng lặp
            }
            // quên viết: thang++;
        }
    }
}""", out="Da 1000 vong, thang van = 1")
    cong_thuc = prog("CongThuc", """
public class CongThuc {
    public static void main(String[] args) {
        double tongThuc = 0;
        long tongDong = 0;
        for (int i = 1; i <= 10; i++) {
            tongThuc += 0.1;            // 0,1 nghìn đồng mỗi lần
            tongDong += 100;            // 100 đồng mỗi lần
        }
        System.out.println(tongThuc);
        System.out.println(tongDong);
    }
}""", out="0.9999999999999999\n1000")
    quiz = prog("BoQua", """
public class BoQua {
    public static void main(String[] args) {
        int tong = 0;
        for (int i = 1; i <= 10; i++) {
            if (i % 3 == 0) {
                continue;
            }
            if (i > 7) {
                break;
            }
            tong += i;
        }
        System.out.println("tong = " + tong);
    }
}""", out="tong = 19")

    sc_hook = sc("hook", "hook", "Mười hai tháng lãi, phải viết mười hai lần?", [
        st(code_block(lai_tay, lines=(3, 7), title="Tính lãi ba tháng bằng tay") + out_block(lai_tay),
           """Muốn tính lãi cộng dồn ba tháng, ta viết ba dòng giống hệt nhau. Mười hai tháng thì mười hai dòng.
           Còn đếm một nghìn lệnh chuyển tiền xem bao nhiêu lệnh vượt hạn mức, chẳng lẽ viết một nghìn dòng."""),
        st("""<div class="box key">Hôm nay: <b>vòng lặp</b> bảo máy làm lại một khối lệnh nhiều lần, với hai mẫu dùng hằng ngày:
<b>cộng dồn</b> và <b>đếm</b>. Và ba lỗi kinh điển: lệch một, không dừng, cộng số thực bị lệch.</div>""",
           """Hôm nay ta học vòng lặp, cách bảo máy làm lại một khối lệnh nhiều lần, với hai mẫu dùng hằng ngày là cộng dồn và đếm.
           Ta cũng gặp ba lỗi kinh điển: lệch một lần, vòng lặp không dừng, và cộng số thực bị lệch."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại điều kiện và phép gán từ các bài trước", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① điều kiện", "<code>thang &lt;= 12</code> cho đúng hoặc sai"],
                  ["② rẽ nhánh", "<code>if</code>: điều kiện đúng mới làm khối trong ngoặc nhọn"],
                  ["③ cộng dồn, tăng một", "<code>soDu += lai;</code> và <code>thang++;</code>"],
                  ["④ chia nguyên", "<code>soDu * 5 / 1000</code>: nhân trước, chia sau, bỏ phần lẻ đồng"]]),
           """Ta ôn lại bốn điều. Phép so sánh cho kết quả đúng hoặc sai. Lệnh rẽ nhánh nếu chỉ làm khối khi điều kiện đúng.
           Cộng bằng là cộng dồn, hai dấu cộng là tăng thêm một. Và tính phần trăm bằng số nguyên thì nhân trước, chia sau.
           Vòng lặp chỉ là lệnh rẽ nhánh được hỏi lại nhiều lần.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ba kiểu vòng lặp và hai lệnh điều khiển", [
        st(table(["viết", "nghĩa"],
                 [["<code>while (đk) { … }</code>", "<b>trong khi</b> điều kiện đúng thì làm khối, rồi kiểm lại"],
                  ["<code>for (bắt đầu; đk; bước) { … }</code>", "<b>vòng lặp đếm</b>: gom bắt đầu, điều kiện, bước vào một dòng"],
                  ["<code>do { … } while (đk);</code>", "<b>làm trước, kiểm sau</b>: chạy ít nhất một lần"],
                  ["<code>break;</code>", "<b>thoát</b> hẳn vòng lặp"],
                  ["<code>continue;</code>", "<b>bỏ qua</b> phần còn lại của vòng này, sang vòng sau"]]),
           """Bảng này có ba kiểu vòng lặp và hai lệnh điều khiển. Vòng lặp trong khi kiểm điều kiện, đúng thì làm khối rồi kiểm lại.
           Vòng lặp đếm gom bắt đầu, điều kiện và bước vào một dòng. Vòng lặp làm rồi mới kiểm chạy ít nhất một lần.
           Lệnh thoát ra khỏi vòng lặp ngay. Lệnh bỏ qua nhảy sang vòng sau.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6"]),
        st(code_block(ba_kieu, lines=(3, 10)),
           """Chương trình này in từ một tới ba bằng hai cách. Vòng lặp trong khi cần ba thứ rời nhau: biến bắt đầu bằng một, điều kiện, và lệnh tăng ở cuối khối.
           Vòng lặp đếm gom đủ ba thứ đó vào ngoặc tròn ở một dòng, nên khó quên hơn."""),
        st(code_block(ba_kieu, lines=(11, 15)) + out_block(ba_kieu),
           """Ở vòng lặp làm rồi mới kiểm, n bằng mười nên điều kiện sai ngay từ đầu. Thế mà khối vẫn chạy một lần, vì máy làm trước rồi mới kiểm.
           Kết quả là ba dòng, ba dòng, và đúng một dòng."""),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: đi vòng quanh một sân, mỗi vòng hỏi lại một lần", [
        st(svg(1500, 400,
               box(20, 150, 260, 100, ["① bắt đầu", "thang = 1"], C_GRAY, bold=True),
               arrow(285, 200, 372, 200, "#2a78d6"),
               '<polygon points="375,200 560,115 745,200 560,285" fill="#dbeafe" stroke="#2a78d6" stroke-width="3"/>',
               txt(560, 195, "② thang &lt;= 12 ?", 24, "middle", "#1f2937", True),
               txt(560, 225, "điều kiện", 20, "middle", "#1f2937"),
               arrow(747, 200, 858, 200, "#16a34a", "đúng"),
               box(860, 150, 320, 100, ["③ thân vòng lặp", "tính lãi, cộng dồn"], C_GREEN, bold=True),
               arrow(1185, 200, 1258, 200, "#2a78d6"),
               box(1260, 150, 220, 100, ["④ bước", "thang++"], C_AMBER, bold=True),
               '<path d="M1370,252 L1370,350 L560,350 L560,292" fill="none" stroke="#d97706" stroke-width="3.5" marker-end="url(#ah)"/>',
               txt(965, 340, "quay lại hỏi điều kiện", 22, "middle", "#d97706", True),
               arrow(560, 113, 560, 50, "#dc2626"),
               txt(580, 45, "sai: ra khỏi vòng lặp, chạy lệnh tiếp theo", 22, "start", "#dc2626", True)),
           """Hãy hình dung vòng lặp đếm như đi vòng quanh một sân. Bước một, đặt biến tháng bằng một, chỉ làm một lần.
           Bước hai, hỏi điều kiện. Đúng thì sang bước ba, làm thân vòng lặp, rồi bước bốn tăng tháng thêm một.
           Sau đó quay lại hỏi điều kiện. Khi điều kiện sai, máy ra khỏi vòng lặp và chạy lệnh tiếp theo."""),
        st(code_block(vuot, lines=(3, 13)),
           """Mẫu cộng dồn ta sẽ làm ở ví dụ lãi, còn đây là mẫu đếm. Ta giả lập tám lệnh chuyển tiền, số tiền lệnh thứ i tính bằng phép chia lấy dư, vì chưa học cách lưu nhiều số.
           Hạn mức ở đây là số tiền tối đa cho một lệnh, năm triệu đồng, số minh hoạ. Lệnh nào không vượt hạn mức thì lệnh bỏ qua nhảy sang lệnh sau, còn lệnh vượt thì biến đếm tăng một."""),
        st(table(["lệnh i", "1", "2", "3", "4", "5", "6", "7", "8"],
                 [["i × 7 % 10 (triệu)", "7", "4", "1", "8", "5", "2", "9", "6"],
                  ["vượt 5 triệu?", "<b>có</b>", "không", "không", "<b>có</b>", "không (bằng)", "không", "<b>có</b>", "<b>có</b>"]])
           + out_block(vuot),
           """Bảng này tính tay tám lệnh. Lệnh năm đúng bằng năm triệu, không vượt, nên bị bỏ qua. Có bốn lệnh vượt là lệnh một, bốn, bảy và tám.
           Chạy thật, chương trình in đúng bốn lệnh đó và số lệnh vượt là bốn.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: từ mười hai dòng giống nhau tới một vòng lặp", [
        st(code_block(lai_tay, lines=(4, 6))
           + "<p><b>Bước 1.</b> Ba dòng <b>giống hệt</b>; chỉ chú thích tháng là khác. Phần lặp lại là thân, phần thay đổi là số tháng.</p>",
           """Bước một, tìm phần lặp lại. Ba dòng tính lãi giống hệt nhau, chỉ có số tháng là khác,
           nên dòng tính lãi là thân vòng lặp, còn số tháng là biến đếm."""),
        st(code_block(lai, lines=(4, 4))
           + "<p><b>Bước 2.</b> Biến đếm cần ba thứ: <b>bắt đầu</b> <code>thang = 1</code>, <b>điều kiện</b> <code>thang &lt;= 12</code>, <b>bước</b> <code>thang++</code>.</p>",
           """Bước hai, viết đầu vòng lặp. Vì cần chạy từ tháng một tới tháng mười hai, nên biến tháng bắt đầu bằng một,
           điều kiện là nhỏ hơn hoặc bằng mười hai, và sau mỗi vòng tăng một."""),
        st("""<p><b>Bước 3.</b> Tháng nhận lần lượt 1, 2, …, 12, đếm cả hai đầu nên:</p>
$$\\text{số lần chạy} = \\text{cuối} - \\text{đầu} + 1 = 12 - 1 + 1 = \\hl{12}$$""",
           """Bước ba, đếm số lần thân vòng lặp chạy. Biến tháng nhận một, hai, cho tới mười hai, và vì đếm cả hai đầu nên số lần là cuối trừ đầu cộng một.
           Mười hai trừ một cộng một bằng mười hai lần, đúng mười hai tháng."""),
        st("""<p><b>Bước 4.</b> Nếu viết <code>thang &lt; 12</code> thì số cuối là 11:</p>
$$11 - 1 + 1 = \\hl{11} \\text{ lần, thiếu một tháng}$$""",
           """Bước bốn, thử đổi dấu. Nếu viết nhỏ hơn hẳn mười hai thì tháng cuối cùng được chạy là mười một.
           Theo cùng công thức, số lần là mười một, thiếu đúng một tháng. Chọn dấu sai là lỗi lệch một mà ta sẽ gặp ở phần lỗi."""),
    ], checks=["12 - 1 + 1 == 12", "len(range(1, 13)) == 12", "len(range(1, 12)) == 11", "11 - 1 + 1 == 11"])
    sc_ex = sc("example", "example", "Ví dụ: lãi cộng dồn mười hai tháng bằng số nguyên", [
        st(code_block(lai, lines=(3, 11), title="Tệp LaiThang.java"),
           """Đây là chương trình đầy đủ. Số dư đầu một trăm triệu đồng, lãi minh hoạ không phẩy năm phần trăm mỗi tháng.
           Mỗi vòng tính lãi bằng số nguyên rồi cộng dồn, và in ba tháng đầu cùng hai tháng cuối."""),
        st("$$① \\; 100\\,000\\,000 \\times 5 / 1000 = \\hl{500\\,000} \\;\\to\\; 100\\,500\\,000$$"
           "$$② \\; 100\\,500\\,000 \\times 5 / 1000 = \\hl{502\\,500} \\;\\to\\; 101\\,002\\,500$$",
           """Phép tính thứ nhất, tháng một, lãi là năm trăm nghìn, số dư thành một trăm triệu năm trăm nghìn.
           Phép tính thứ hai, tháng hai tính lãi trên số dư mới, nên lãi lớn hơn một chút, năm trăm linh hai nghìn năm trăm.
           Đó chính là cộng dồn, lãi tháng trước sinh thêm lãi ở tháng sau."""),
        st("$$③ \\; 101\\,002\\,500 \\times 5 / 1000 = 505\\,012.5 \\to \\hl{505\\,012} \\;\\to\\; 101\\,507\\,512$$"
           "<p>Phép chia nguyên bỏ 0.5 đồng. Số dư tháng 3 trùng với bản viết tay ở đầu bài ✓</p>",
           """Phép tính thứ ba, tháng ba, lãi đúng ra là năm trăm linh năm nghìn không trăm mười hai phẩy năm. Vì chia số nguyên nên phần lẻ nửa đồng bị bỏ.
           Số dư tháng ba trùng với bản viết tay ở đầu bài, nghĩa là vòng lặp làm đúng việc ta đã làm bằng tay.""", clear=True),
        st("$$④ \\; \\text{tháng 4 tới 11: thân vòng lặp chạy thêm } 11 - 4 + 1 = 8 \\text{ lần} \\;\\to\\; 105\\,639\\,579$$"
           "$$⑤ \\; 105\\,639\\,579 \\times 5 / 1000 = 528\\,197.895 \\to \\hl{528\\,197} \\;\\to\\; \\hl{106\\,167\\,776}$$",
           """Phép tính thứ tư, từ tháng bốn tới tháng mười một, thân vòng lặp chạy thêm tám lần, ta để máy làm và đọc số dư nó in ra.
           Phép tính thứ năm, tháng mười hai, lãi khoảng năm trăm hai mươi tám nghìn đồng, bỏ phần lẻ. Số dư cuối là khoảng một trăm linh sáu triệu một trăm sáu mươi tám nghìn.""", clear=True),
        st(out_block(lai),
           """Chạy thật, sáu dòng in ra khớp với từng phép tính tay, kể cả tháng ba đã bỏ nửa đồng.""", clear=True),
    ], checks=["100000000 * 5 // 1000 == 500000", "100500000 * 5 // 1000 == 502500", "101002500 * 5 // 1000 == 505012",
               "11 - 4 + 1 == 8", "105639579 * 5 // 1000 == 528197", "105639579 + 528197 == 106167776"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: công thức lãi kép", [
        st("""<p>Không làm tròn thì mỗi tháng số dư nhân với $1.005$, nên 12 tháng là nhân 12 lần:</p>
$$100\\,000\\,000 \\times 1.005^{12} \\approx 106\\,167\\,781.19$$""" + code_block(kiem_lai, lines=(3, 4))
           + "<span class='note'><code>Math.pow(a, n)</code> là lệnh có sẵn của Java, tính a mũ n, ra số thực; "
             "<code>(long)</code> ép về số nguyên dài, bỏ phần lẻ.</span>" + out_block(kiem_lai),
           """Đường kiểm khác là công thức lãi kép, tức lãi được nhập vào gốc để tháng sau sinh lãi tiếp. Nếu không làm tròn, mỗi tháng số dư được nhân với một phẩy không không năm, nên mười hai tháng là nhân mười hai lần.
           Java có sẵn lệnh tính lũy thừa, ép về số nguyên dài để dễ đọc, và chương trình in ra số trên màn hình."""),
        st("""<p>Chênh lệch: $106\\,167\\,781 - 106\\,167\\,776 = \\hl{5}$ đồng. Hợp lý, vì mỗi tháng phép chia nguyên bỏ <b>dưới 1 đồng</b>,
12 tháng bỏ chưa tới 13 đồng (kể cả phần lãi của số tiền bị bỏ).</p>""",
           """Hai cách chênh nhau năm đồng. Con số này hợp lý, vì mỗi tháng phép chia nguyên chỉ bỏ đi chưa tới một đồng.
           Mười hai tháng bỏ chưa tới mười ba đồng, kể cả phần lãi của số tiền bị bỏ, nên năm đồng nằm trong giới hạn đó.""", clear=True),
    ], checks=["abs(100000000 * 1.005**12 - 106167781.19) < 0.01",
               "__import__('functools').reduce(lambda s, _: s + s * 5 // 1000, range(12), 100000000) == 106167776",
               "int(100000000 * 1.005**12) - 106167776 == 5", "(1.005**12 - 1) / 0.005 < 13"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Lệch một: <code>&lt;</code> thay cho <code>&lt;=</code>.</div>'
           + code_block(dem_thang, lines=(3, 11)) + out_block(dem_thang),
           """Lỗi thứ nhất là lệch một lần. Hai vòng lặp chỉ khác nhau một dấu bằng. Dấu nhỏ hơn hẳn dừng trước tháng mười hai, chạy mười một lần.
           Dấu nhỏ hơn hoặc bằng chạy đủ mười hai lần. Cách tránh là dùng công thức cuối trừ đầu cộng một để đếm trước số lần."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Quên tăng biến đếm: vòng lặp không bao giờ dừng.</div>'
           + code_block(quen_tang, lines=(3, 11)) + out_block(quen_tang),
           """Lỗi thứ hai là quên tăng biến đếm trong vòng lặp trong khi. Tháng mãi bằng một, điều kiện mãi đúng, nên vòng lặp không bao giờ dừng.
           Chương trình mẫu có thêm bộ đếm an toàn, tới vòng thứ một nghìn thì dùng lệnh thoát, để ta thấy tháng vẫn bằng một.
           Trước khi chạy, hãy chỉ ra dòng nào làm điều kiện tiến dần tới sai."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Cộng dồn số thực trong vòng lặp.</div>'
           + code_block(cong_thuc, lines=(3, 10)) + out_block(cong_thuc),
           """Lỗi thứ ba hay gặp ở người đã đi làm, là cộng dồn số thực trong vòng lặp. Cộng không phẩy một mười lần không ra một, mà ra một số nhỏ hơn một một chút.
           Sai số nhỏ của từng lần cộng dồn lại sau mỗi vòng. Biến số nguyên dài tính theo đồng thì ra đúng một nghìn."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(3, 13), title="Đoán dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Biến i chạy từ một tới mười. Số chia hết cho ba thì bị bỏ qua. Khi i lớn hơn bảy thì thoát.
           Còn lại thì cộng i vào tổng. Hãy dừng video, lập bảng từng vòng và viết ra dòng in ra.""", pause=20),
        st(table(["i", "1", "2", "3", "4", "5", "6", "7", "8"],
                 [["việc làm", "cộng", "cộng", "bỏ qua", "cộng", "cộng", "bỏ qua", "cộng", "<b>thoát</b>"],
                  ["tong sau vòng", "1", "3", "3", "7", "12", "12", "19", "19"]]),
           """Đáp án, ta lập bảng. Vòng một và hai cộng vào, tổng là ba. Vòng ba, ba chia hết cho ba nên bỏ qua. Vòng bốn và năm cộng, tổng là mười hai.
           Vòng sáu bỏ qua, vòng bảy cộng, tổng là mười chín. Vòng tám, tám lớn hơn bảy nên thoát, các vòng chín, mười không bao giờ chạy.""",
           focus=[1, "1.3", "1.2", ["1.2", "1.3"], "1.2", "1.2"]),
        st("$$1 + 2 + 4 + 5 + 7 = \\hl{19}$$" + out_block(quiz),
           """Kiểm lại, các số được cộng là một, hai, bốn, năm, bảy, tổng là mười chín. Chạy thật, chương trình in tổng bằng mười chín."""),
    ], checks=["1 + 2 + 4 + 5 + 7 == 19", "sum(i for i in range(1, 8) if i % 3 != 0) == 19"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("tìm phần lặp lại", "biến đếm: bắt đầu, điều kiện, bước", "số lần = cuối − đầu + 1",
                 "cộng dồn và đếm", "điều kiện phải tiến tới sai"),
           """Tổng kết chuỗi logic. Tìm phần lặp lại để làm thân vòng lặp. Biến đếm cần bắt đầu, điều kiện và bước.
           Đếm trước số lần bằng cuối trừ đầu cộng một. Hai mẫu hay dùng là cộng dồn và đếm. Và điều kiện phải tiến dần tới sai thì vòng lặp mới dừng."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi chạy một vòng lặp, trả lời ba câu: nó chạy <b>mấy lần</b>, dòng nào làm nó <b>dừng</b>,
và biến cộng dồn có phải số nguyên tính theo đồng không.</div>""",
           """Điều cần mang theo. Trước khi chạy một vòng lặp, hãy trả lời ba câu. Nó chạy mấy lần, dòng nào làm nó dừng,
           và biến cộng dồn có phải số nguyên tính theo đồng không."""),
    ])
    return lesson("L04", "vong_lap", "Bài 4 — Vòng lặp",
                  "curriculum/jva.yaml L04; audit/jva/verify_jva.py L04 (javac/java chạy thật); The Java Language Specification, "
                  "Java SE 21: §14.12 (while), §14.13 (do: thân chạy trước khi kiểm), §14.14.1 (for cơ bản: khởi tạo, điều kiện, cập nhật), "
                  "§14.15 (break), §14.16 (continue), §15.26.2 (+= ép về kiểu biến), §5.1.3 (ép double sang long bỏ phần lẻ); "
                  "java.lang.Math.pow (Java SE 21 API); dev.java/learn",
                  ["Viết vòng lặp trong khi, vòng lặp đếm, vòng lặp làm rồi mới kiểm, và chọn đúng loại",
                   "Đếm trước số lần chạy bằng cuối trừ đầu cộng một, tránh lỗi lệch một",
                   "Dùng hai mẫu cộng dồn và đếm, cùng lệnh thoát và lệnh bỏ qua",
                   "Tính lãi cộng dồn bằng số nguyên theo đồng và kiểm lại bằng công thức lãi kép"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
