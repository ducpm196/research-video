from lib import *

HELLO = None


def build():
    hello = prog("Chao", """
public class Chao {
    public static void main(String[] args) {
        System.out.println("Chao ban!");
        System.out.println("So du: 100000 dong");
    }
}""", out="Chao ban!\nSo du: 100000 dong")
    tong = prog("Tong", """
public class Tong {
    public static void main(String[] args) {
        System.out.println(2 + 3);             // (1) phép cộng hai số
        System.out.println("2 + 3");           // (2) một chuỗi chữ
        System.out.println("Tong: " + 2 + 3);  // (3) chuỗi đứng trước
        System.out.println("Tong: " + (2 + 3));// (4) ngoặc tính trước
        System.out.println(2 + 3 + " dong");   // (5) số đứng trước
    }
}""", out="5\n2 + 3\nTong: 23\nTong: 5\n5 dong")
    sai_ten = prog("Loi", """
public class Chao {
    public static void main(String[] args) {
        System.out.println("Chao ban!");
    }
}""", expect="compile_error:should be declared in a file named Chao.java")
    thieu_cham_phay = prog("Thieu", """
public class Thieu {
    public static void main(String[] args) {
        System.out.println("Chao ban!")
    }
}""", expect="compile_error:';' expected")
    chia_khong = prog("ChiaKhong", """
public class ChiaKhong {
    public static void main(String[] args) {
        System.out.println("Bat dau");
        int soNguoi = 0;
        System.out.println(100000 / soNguoi);
        System.out.println("Ket thuc");
    }
}""", out="Bat dau", expect="runtime_error:ArithmeticException",
        err='Exception in thread "main" java.lang.ArithmeticException: / by zero')
    quiz = prog("DoanKetQua", """
public class DoanKetQua {
    public static void main(String[] args) {
        System.out.println("A" + 1 + 2);
        System.out.println(1 + 2 + "A");
        System.out.println("A" + (1 + 2));
    }
}""", out="A12\n3A\nA3")

    sc_hook = sc("hook", "hook", "Máy chỉ hiểu số, vậy dòng chữ bạn gõ chạy thành lệnh bằng cách nào?", [
        st("""<p>Bên trong máy tính chỉ có các số $0$ và $1$. Thế mà bạn gõ một dòng chữ, bấm chạy, và màn hình in ra số dư tài khoản.</p>
<div class="box key">Hôm nay ta đi hết con đường đó: <b>gõ mã nguồn → biên dịch → chạy</b>, và viết chương trình Java đầu tiên.</div>""",
           """Chào bạn, bên trong máy tính chỉ có các số không và một. Thế mà bạn gõ một dòng chữ, bấm chạy, và màn hình in ra số dư tài khoản.
           Hôm nay ta đi hết con đường đó, từ lúc gõ mã nguồn, qua bước biên dịch, tới lúc chạy, và viết chương trình Java đầu tiên của bạn."""),
        st("""<p>Mọi dịch vụ ngân hàng bạn sẽ học sau này, từ chuyển khoản tới đối soát, đều bắt đầu từ đúng ba bước ấy.</p>
<div class="box key">Hiểu ba bước này giúp bạn đọc được thông báo lỗi, thay vì sợ nó.</div>""",
           """Mọi dịch vụ ngân hàng bạn sẽ học sau này, từ chuyển khoản tới đối soát, đều bắt đầu từ đúng ba bước ấy.
           Hiểu chúng giúp bạn đọc được thông báo lỗi, thay vì sợ nó."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại ba điều về máy tính", [
        st(table(["khái niệm", "nghĩa", "ví dụ đời thường"],
                 [["① Bộ xử lý", "làm từng lệnh rất đơn giản, rất nhanh", "người thu ngân bấm máy tính"],
                  ["② Bộ nhớ", "chỗ để giữ dữ liệu khi đang chạy", "tờ giấy nháp"],
                  ["③ Tệp", "dữ liệu được lưu trên ổ đĩa, có tên", "cuốn sổ có tên trên gáy"]]),
           """Trước hết ta ôn lại ba điều. Điều thứ nhất, bộ xử lý làm từng lệnh rất đơn giản nhưng rất nhanh, giống người thu ngân bấm máy tính.
           Điều thứ hai, bộ nhớ là chỗ giữ dữ liệu khi chương trình đang chạy, giống tờ giấy nháp.
           Điều thứ ba, tệp là dữ liệu được lưu trên ổ đĩa và có tên, giống cuốn sổ có tên ghi trên gáy."""),
        st("""<p>Một <b>chương trình</b> là danh sách lệnh viết sẵn, máy làm lần lượt <b>từ trên xuống</b>.</p>""",
           """Ghép ba điều lại, một chương trình là danh sách lệnh viết sẵn, và máy làm lần lượt từ trên xuống dưới."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã các ký hiệu trong chương trình đầu tiên", [
        st(code_block(hello, title="Tệp Chao.java"),
           """Đây là chương trình đầu tiên, nằm trong tệp tên là Chao chấm Java. Nó có sáu dòng, ta đọc từng ký hiệu một ở bảng sau.
           Đừng lo nếu chưa hiểu hết, mỗi chữ đều sẽ được giải thích."""),
        st(table(["viết", "nghĩa"],
                 [["<code>public class Chao</code>", "khai một lớp tên Chao; tên tệp phải là <code>Chao.java</code>"],
                  ["<code>{ … }</code>", "cặp ngoặc nhọn gom các lệnh thành một khối"],
                  ["<code>public static void main(String[] args)</code>", "hàm chính: chỗ máy bắt đầu chạy"],
                  ["<code>System.out.println(…)</code>", "in giá trị trong ngoặc ra màn hình rồi xuống dòng"],
                  ["<code>\"Chao ban!\"</code>", "một chuỗi chữ, nằm giữa hai dấu nháy kép"],
                  ["<code>;</code>", "dấu chấm phẩy kết thúc một lệnh"]]),
           """Dòng đầu khai một lớp tên Chao, và tên tệp bắt buộc trùng với tên lớp. Cặp ngoặc nhọn gom các lệnh thành một khối.
           Dòng thứ hai là hàm chính, chỗ máy bắt đầu chạy. Lệnh in sẽ in giá trị trong ngoặc ra màn hình rồi xuống dòng.
           Chữ nằm giữa hai dấu nháy kép là một chuỗi. Còn dấu chấm phẩy đánh dấu hết một lệnh.""", clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: từ chữ bạn gõ tới kết quả trên màn hình", [
        st(svg(1500, 380,
               box(30, 130, 260, 120, ["Chao.java", "mã nguồn"], C_BLUE, bold=True),
               arrow(295, 190, 420, 190, "#2a78d6", "javac"),
               box(430, 130, 280, 120, ["Chao.class", "mã byte"], C_AMBER, bold=True),
               arrow(715, 190, 840, 190, "#2a78d6", "java"),
               box(850, 110, 300, 160, ["JVM", "máy ảo Java", "chạy từng lệnh"], C_GREEN, bold=True),
               arrow(1155, 190, 1270, 190, "#16a34a"),
               box(1280, 130, 200, 120, ["màn hình", "Chao ban!"], C_GRAY),
               txt(750, 330, "biên dịch MỘT lần, máy ảo trên mỗi hệ điều hành chạy cùng tệp .class", 24, "middle", "#1f2937", True)),
           """Hình này là cả con đường. Bên trái là tệp mã nguồn bạn gõ. Trình biên dịch đọc nó và tạo ra tệp mã bai, dạng lệnh mà người khó đọc nhưng máy ảo hiểu.
           Sau đó máy ảo Java, viết tắt JVM, nạp tệp mã bai và chạy từng lệnh, rồi kết quả hiện ra màn hình.
           Nhờ có máy ảo, cùng một tệp mã bai chạy được trên nhiều hệ điều hành."""),
        st(table(["bước", "ai làm", "bắt được lỗi gì"],
                 [["biên dịch", "trình biên dịch <code>javac</code>", "lỗi cú pháp, sai kiểu, sai tên: <b>lỗi biên dịch</b>"],
                  ["chạy", "máy ảo <code>java</code>", "chia cho 0, vượt chỉ số…: <b>lỗi khi chạy</b> (ngoại lệ)"]]),
           """Hai bước này bắt hai loại lỗi khác nhau. Trình biên dịch bắt lỗi viết sai luật của ngôn ngữ, gọi là lỗi biên dịch, và khi đó không có tệp mã bai nào được tạo.
           Còn máy ảo chỉ phát hiện một số lỗi khi đang chạy, như chia cho không. Loại này gọi là lỗi khi chạy, hay ngoại lệ."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: tạo, biên dịch, chạy", [
        st("""<p><b>Bước 1. Tạo tệp.</b> Gõ mã vào tệp <code>Chao.java</code>. Tên tệp trùng tên lớp <code>public</code>, kể cả chữ hoa.</p>
<span class='note'>Làm thử: lớp tên Chao thì tệp phải là Chao.java, không phải chao.java.</span>""",
           """Bước một là tạo tệp: gõ toàn bộ đoạn mã bên trái vào một tệp tên là Chao chấm Java. Tên tệp phải trùng tên lớp, kể cả chữ hoa và chữ thường, vì luật của Java bắt lớp công khai nằm trong tệp cùng tên.
           Làm thử, lớp tên Chao viết hoa chữ đầu, thì tệp cũng phải viết hoa chữ đầu."""),
        st('<p><b>Bước 2. Biên dịch.</b></p><div class="code"><div>javac Chao.java</div></div>'
           "<span class='note'>Làm thử: không có lỗi thì không in gì, và trong thư mục xuất hiện thêm tệp Chao.class.</span>",
           """Bước hai, biên dịch. Gõ lệnh gọi trình biên dịch, kèm tên tệp. Nếu không có lỗi thì lệnh này không in gì cả, nghĩa là mã đã đúng luật,
           và trong thư mục xuất hiện thêm một tệp mã bai cùng tên Chao."""),
        st('<p><b>Bước 3. Chạy.</b></p><div class="code"><div>java Chao</div></div>' + out_block(hello),
           """Bước ba, chạy. Gõ lệnh gọi máy ảo kèm tên lớp, không cần đuôi tệp. Máy ảo tìm hàm chính và làm từng lệnh từ trên xuống.
           Lệnh in thứ nhất in dòng chào bạn, lệnh in thứ hai in dòng số dư. Có hai lệnh in nên có đúng hai dòng."""),
    ], checks=["len(['Chao ban!', 'So du: 100000 dong']) == 2"])
    sc_ex = sc("example", "example", "Ví dụ: máy tính toán và nối chữ theo thứ tự nào?", [
        st(code_block(tong, title="Tệp Tong.java"),
           """Chương trình này có năm lệnh in, mỗi lệnh thử một cách viết khác nhau với hai số hai và ba. Ta đoán từng dòng trước khi chạy."""),
        st(code_block(tong, lines=(3, 4)) + "<p>Dòng ① in một phép cộng hai số, dòng ② in một chuỗi chữ:</p>$$① \\; 2 + 3 = \\hl{5} \\qquad ② \\; \\text{\"2 + 3\"} \\to \\text{2 + 3}$$",
           """Phép tính thứ nhất, hai cộng ba là năm, vì cả hai đều là số. Dòng thứ hai nằm trong dấu nháy kép nên là chữ, máy in nguyên văn hai cộng ba."""),
        st(code_block(tong, lines=(5, 5)) + "<p>Dòng ③: máy làm <b>từ trái sang phải</b>. Chuỗi cộng số thì <b>nối chữ</b>:</p>"
           "$$③ \\; (\\text{\"Tong: \"} + 2) + 3 = \\text{\"Tong: 2\"} + 3 = \\hl{\\text{Tong: 23}}$$",
           """Phép tính thứ ba, máy làm từ trái sang phải. Chuỗi tổng cộng với số hai thì không cộng số mà nối chữ, ra tổng hai.
           Rồi nối tiếp số ba, ra tổng hai ba, không phải tổng năm."""),
        st(code_block(tong, lines=(6, 7)) + "<p>Dòng ④: ngoặc được tính trước. Dòng ⑤: hai số đứng trước nên cộng số trước rồi mới nối chữ.</p>"
           "$$④ \\; \\text{\"Tong: \"} + (2 + 3) = \\hlg{\\text{Tong: 5}} \\qquad ⑤ \\; (2 + 3) + \\text{\" dong\"} = \\hlg{\\text{5 dong}}$$",
           """Phép tính thứ tư, phần trong ngoặc được tính trước, ra năm, rồi mới nối vào chữ, nên in tổng năm.
           Phép tính thứ năm, hai số đứng trước nên được cộng thành năm trước, rồi mới nối chữ đồng."""),
        st(out_block(tong),
           """Chạy thật chương trình, năm dòng in ra đúng như ta đoán: năm, hai cộng ba, tổng hai ba, tổng năm, và năm đồng."""),
    ], checks=["2 + 3 == 5", "'Tong: ' + str(2) + str(3) == 'Tong: 23'", "'Tong: ' + str(2 + 3) == 'Tong: 5'", "str(2 + 3) + ' dong' == '5 dong'"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm số dòng và kiểu của từng vế", [
        st(table(["dòng", "vế trái lúc gặp dấu +", "loại phép +", "kết quả"],
                 [["①", "số 2", "cộng số", "5"], ["③", "chuỗi \"Tong: \"", "nối chữ (cả hai lần)", "Tong: 23"],
                  ["④", "chuỗi \"Tong: \"", "ngoặc là số 5, rồi nối", "Tong: 5"], ["⑤", "số 2", "cộng số, rồi nối", "5 dong"]]),
           """Kiểm bằng đường khác, chỉ cần nhìn vế bên trái mỗi lần gặp dấu cộng. Nếu vế trái là số và vế phải là số thì cộng số.
           Nếu một trong hai vế là chuỗi thì nối chữ. Áp quy tắc này cho từng dòng, ta ra đúng bốn kết quả như khi chạy."""),
        st("""<p>Đếm: chương trình có $5$ lệnh in nên phải có đúng $5$ dòng kết quả. Kết quả chạy có $5$ dòng ✓</p>""",
           """Thêm một phép kiểm nữa, chương trình có năm lệnh in thì phải có đúng năm dòng kết quả. Kết quả chạy có năm dòng, khớp."""),
    ], checks=["len('5|2 + 3|Tong: 23|Tong: 5|5 dong'.split('|')) == 5"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Lưu lớp <code>Chao</code> vào tệp <code>Loi.java</code>.</div>'
           + code_block(sai_ten, lines=(1, 1)) + out_block(sai_ten, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là đặt tên tệp khác tên lớp. Lớp tên Chao nhưng lưu trong một tệp tên khác.
           Trình biên dịch từ chối ngay, và báo rằng lớp Chao phải nằm trong tệp tên Chao chấm Java."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Quên dấu <code>;</code> cuối lệnh in.</div>'
           + code_block(thieu_cham_phay, lines=(3, 3)) + out_block(thieu_cham_phay, "Trình biên dịch báo"),
           """Lỗi thứ hai, cũng của người mới, là quên dấu chấm phẩy cuối lệnh. Trình biên dịch báo rằng nó đang chờ một dấu chấm phẩy,
           kèm số dòng. Hãy đọc số dòng trong thông báo, đó là chỗ cần sửa."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tin rằng “biên dịch được là chạy đúng”.</div>'
           + code_block(chia_khong, lines=(3, 6)) + out_block(chia_khong),
           """Lỗi thứ ba, của cả người đã đi làm, là tin rằng biên dịch được thì chạy đúng. Chương trình này biên dịch không lỗi.
           Nhưng khi chạy, nó in bắt đầu, rồi chia một trăm nghìn cho số người bằng không, và máy ảo ném ra ngoại lệ phép tính.
           Dòng kết thúc không bao giờ được in. Trình biên dịch không biết lúc chạy số người bằng bao nhiêu."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(3, 5), title="Đoán ba dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Chương trình có ba lệnh in. Lệnh một nối chữ A với một rồi với hai. Lệnh hai lấy một cộng hai rồi nối chữ A.
           Lệnh ba nối chữ A với một cộng hai đặt trong ngoặc. Hãy dừng video, viết ra giấy ba dòng in ra.""", pause=20),
        st("<p>Áp quy tắc vế trái:</p>$$\\text{\"A\"} + 1 + 2 = \\hl{\\text{A12}} \\qquad 1 + 2 + \\text{\"A\"} = \\hl{\\text{3A}} \\qquad \\text{\"A\"} + (1 + 2) = \\hl{\\text{A3}}$$",
           """Đáp án như sau. Dòng một, vế trái là chuỗi nên nối cả hai lần, ra A một hai. Dòng hai, hai số đứng trước nên cộng thành ba rồi nối, ra ba A.
           Dòng ba, ngoặc tính trước ra ba, rồi nối, ra A ba."""),
        st(out_block(quiz),
           """Chạy thật chương trình, ba dòng in ra đúng là A một hai, ba A, và A ba."""),
    ], checks=["'A' + str(1) + str(2) == 'A12'", "str(1 + 2) + 'A' == '3A'", "'A' + str(1 + 2) == 'A3'"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("gõ mã nguồn .java", "biên dịch → .class", "máy ảo chạy hàm chính", "từng lệnh từ trên xuống"),
           """Tổng kết chuỗi logic. Bạn gõ mã nguồn vào tệp Java, trình biên dịch tạo tệp mã bai, và máy ảo chạy hàm chính, từng lệnh từ trên xuống."""),
        st("""<div class='box key'><b>Tư duy:</b> lỗi biên dịch thì đọc số dòng mà trình biên dịch chỉ ra; lỗi khi chạy thì chương trình
đã chạy tới một lệnh nào đó rồi mới dừng. Dấu <code>+</code> với chuỗi là <b>nối chữ</b>, làm từ trái sang phải.</div>""",
           """Điều cần mang theo. Gặp lỗi biên dịch thì đọc số dòng mà trình biên dịch chỉ ra. Gặp lỗi khi chạy thì chương trình đã chạy tới một lệnh nào đó rồi mới dừng.
           Và dấu cộng với chuỗi là nối chữ, máy làm từ trái sang phải."""),
    ])
    return lesson("L00", "chuong_trinh_dau_tien", "Bài 0 — Chương trình đầu tiên: mã nguồn, biên dịch và máy ảo Java",
                  "curriculum/jva.yaml L00; audit/jva/verify_jva.py L00 (javac/java chạy thật); The Java Language Specification, Java SE 21; dev.java/learn",
                  ["Kể đúng ba bước gõ, biên dịch, chạy và vai trò của máy ảo Java", "Đọc được chương trình có hàm chính và lệnh in",
                   "Phân biệt lỗi biên dịch với lỗi khi chạy", "Dự đoán dấu cộng là cộng số hay nối chữ"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
