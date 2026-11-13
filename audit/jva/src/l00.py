from lib import *
from labkit import write_lab, practice_steps, practice_scene

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
}""", expect="compile_error:class Chao is public, should be declared in a file named Chao.java")
    thieu_cham_phay = prog("Thieu", """
public class Thieu {
    public static void main(String[] args) {
        System.out.println("Chao ban!")
    }
}""", expect="compile_error:';' expected",
        err="Thieu.java:3: error: ';' expected\n        System.out.println(\"Chao ban!\")\n" + " " * 39 + "^\n1 error")
    chinh_ta = prog("Chinh", """
public class Chinh {
    public static void main(String[] args) {
        System.out.printn("Chao ban!");
    }
}""", expect="compile_error:cannot find symbol",
        err="Chinh.java:3: error: cannot find symbol\n        System.out.printn(\"Chao ban!\");\n" + " " * 18
            + "^\n  symbol:   method printn(String)\n  location: variable out of type PrintStream\n1 error")
    phieu = prog("PhieuSo", """
public class PhieuSo {
    public static void main(String[] args) {
        System.out.println("Xin chao Lan");
        System.out.println("So du: 250000 dong");
        System.out.println("Phi: 1500 + 500");
        System.out.println("Tong phi: " + (1500 + 500));
        System.out.println("Ghep: " + 1500 + 500);
    }
}""", out="Xin chao Lan\nSo du: 250000 dong\nPhi: 1500 + 500\nTong phi: 2000\nGhep: 1500500")
    sai_sytem = prog("SaiTen", """
public class SaiTen {
    public static void main(String[] args) {
        Sytem.out.println("Chao");
    }
}""", expect="compile_error:package Sytem does not exist")
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
<div class="box key">Hôm nay ta đi hết con đường đó: <b>gõ mã nguồn → biên dịch → chạy</b>, và viết chương trình Java đầu tiên.</div>
<span class='note'><b>Mã nguồn</b>: các dòng lệnh bạn gõ bằng chữ. <b>Biên dịch</b>: dịch cả tệp mã nguồn sang dạng máy đọc được, trước khi chạy.</span>""",
           """Chào bạn, bên trong máy tính chỉ có các số không và một. Thế mà bạn gõ một dòng chữ, bấm chạy, và màn hình in ra số dư tài khoản.
           Hôm nay ta đi hết con đường đó, từ lúc gõ mã nguồn, qua bước biên dịch, tới lúc chạy, và viết chương trình Java đầu tiên của bạn.
           Mã nguồn là các dòng lệnh bạn gõ bằng chữ, còn biên dịch là dịch cả tệp mã nguồn sang dạng máy đọc được, trước khi chạy.
           Mọi dịch vụ ngân hàng sau này, từ chuyển khoản tới đối soát, đều bắt đầu từ ba bước ấy, và hiểu chúng giúp bạn đọc được thông báo lỗi thay vì sợ nó."""),
    ])
    sc_pre = sc("prereq", "prereq", "Trước hết: ba điều về máy tính", [
        st(table(["khái niệm", "nghĩa", "ví dụ đời thường"],
                 [["① Bộ xử lý", "làm từng lệnh rất đơn giản, rất nhanh", "người thu ngân bấm máy tính"],
                  ["② Bộ nhớ", "chỗ để giữ dữ liệu khi đang chạy", "tờ giấy nháp"],
                  ["③ Tệp", "dữ liệu được lưu trên ổ đĩa, có tên", "cuốn sổ có tên trên gáy"],
                  ["④ Thư mục", "ngăn chứa tệp; cửa sổ lệnh luôn <b>đứng</b> ở một thư mục", "ngăn tủ đựng các cuốn sổ"]]),
           """Trước hết, ta cần hiểu bốn điều về máy tính. Điều thứ nhất, bộ xử lý làm từng lệnh rất đơn giản nhưng rất nhanh, giống người thu ngân bấm máy tính.
           Điều thứ hai, bộ nhớ là chỗ giữ dữ liệu khi chương trình đang chạy, giống tờ giấy nháp.
           Điều thứ ba, tệp là dữ liệu được lưu trên ổ đĩa và có tên, giống cuốn sổ có tên ghi trên gáy.
           Điều thứ tư, thư mục là ngăn chứa tệp, giống ngăn tủ đựng sổ. Khi ta gõ lệnh cho máy, ta luôn đứng ở một thư mục nào đó, và lệnh chỉ thấy các tệp nằm ngay trong thư mục ấy."""),
        st("""<p>Một <b>chương trình</b> là danh sách lệnh viết sẵn, máy làm lần lượt <b>từ trên xuống</b>.</p>""",
           """Ghép ba điều lại, một chương trình là danh sách lệnh viết sẵn, và máy làm lần lượt từ trên xuống dưới."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã các ký hiệu trong chương trình đầu tiên", [
        st(code_block(hello, title="Tệp Chao.java"),
           """Đây là chương trình đầu tiên, nằm trong tệp tên là Chao chấm Java. Nó có sáu dòng, ta đọc từng ký hiệu một ở bảng sau.
           Đừng lo nếu chưa hiểu hết, mỗi chữ đều sẽ được giải thích."""),
        st(table(["viết", "nghĩa"],
                 [["<code>public class Chao</code>", "khai một <b>lớp</b> tên Chao: cái hộp có tên chứa mã (mọi lệnh Java nằm trong một lớp); tên tệp phải là <code>Chao.java</code>"],
                  ["<code>{ … }</code>", "cặp ngoặc nhọn gom các lệnh thành một khối"],
                  ["<code>public static void main(String[] args)</code>", "<b>hàm</b> là một nhóm lệnh có tên; hàm tên <code>main</code> là <b>hàm chính</b>, chỗ máy bắt đầu chạy (từng chữ ở bảng sau)"],
                  ["<code>System.out.println(…)</code>", "in giá trị trong ngoặc ra màn hình rồi xuống dòng"],
                  ["<code>\"Chao ban!\"</code>", "một <b>chuỗi</b> (dãy ký tự), nằm giữa hai dấu nháy kép"],
                  ["<code>;</code>", "dấu chấm phẩy kết thúc một lệnh"],
                  ["<code>// …</code>", "<b>chú thích</b>: từ hai gạch chéo tới hết dòng, máy bỏ qua, viết cho người đọc"]]),
           """Dòng đầu khai một lớp tên Chao. Lớp, nói gọn, là một cái hộp có tên để chứa mã, và mọi lệnh Java phải nằm trong một lớp; tên tệp bắt buộc trùng với tên lớp.
           Cặp ngoặc nhọn gom các lệnh thành một khối.
           Dòng thứ hai khai một hàm, tức một nhóm lệnh có tên. Hàm này là hàm chính, chỗ máy bắt đầu chạy, và từng chữ của dòng đó ta giải mã ngay ở bảng sau.
           Lệnh in sẽ in giá trị trong ngoặc ra màn hình rồi xuống dòng.
           Chữ nằm giữa hai dấu nháy kép là một chuỗi, tức một dãy ký tự. Dấu chấm phẩy đánh dấu hết một lệnh.
           Còn hai gạch chéo mở đầu một chú thích, phần máy bỏ qua, viết cho người đọc.""", clear=True,
           focus=["1.2", "1.2", "1.3", "1.4", "1.4", "1.5", "1.6", "1.7", "1.8"]),
        st(table(["viết", "nghĩa"],
                 [["<code>public</code>", "<b>công khai</b>: nơi khác đều gọi được hàm này"],
                  ["<code>static</code>", "hàm <b>gắn với cả lớp</b>: máy gọi được ngay, chưa cần tạo vật nào từ lớp"],
                  ["<code>void</code>", "<b>rỗng</b>: hàm làm xong không trả giá trị nào về"],
                  ["<code>main</code>", "<b>tên hàm</b>: máy tìm đúng tên này để bắt đầu chạy"],
                  ["<code>String[] args</code>", "trong ngoặc tròn là <b>tham số</b>: danh sách chữ người chạy gõ thêm sau tên lớp (chương trình này chưa dùng)"],
                  ["<code>System.out</code>", "<code>System</code>: kho lệnh có sẵn của hệ thống; <code>out</code>: <b>đầu ra chuẩn</b>, tức màn hình"],
                  ["<code>println</code>", "lệnh in một dòng rồi xuống dòng"]]),
           """Bảng này giải mã từng chữ ở dòng hàm chính và dòng lệnh in. Chữ công khai nghĩa là nơi khác đều gọi được hàm này.
           Chữ gắn với lớp nghĩa là máy gọi được hàm ngay, chưa cần tạo vật nào từ lớp. Chữ rỗng nghĩa là hàm làm xong không trả giá trị nào về.
           Tiếp theo là tên hàm, máy tìm đúng tên này để bắt đầu chạy. Trong ngoặc tròn là tham số, một danh sách chữ mà người chạy chương trình có thể gõ thêm sau tên lớp; chương trình này chưa dùng nó.
           Ở lệnh in, chữ đầu là kho lệnh có sẵn của hệ thống, chữ thứ hai là đầu ra chuẩn, tức màn hình. Chữ cuối là lệnh in một dòng rồi xuống dòng.
           Bạn cứ gõ đúng như mẫu. Về sau, bài vòng lặp sẽ dùng danh sách chữ gõ thêm, và bài về hàm sẽ giảng kỹ chữ gắn với lớp.""", clear=True,
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", 1, 1], forward_ref=True),
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
           Máy ảo là một chương trình đóng vai một chiếc máy tính tưởng tượng: nó đọc mã bai rồi ra lệnh lại cho máy thật.
           Nhờ có máy ảo, cùng một tệp mã bai chạy được trên nhiều hệ điều hành, tức phần mềm nền điều khiển cả chiếc máy tính."""),
        st(table(["bước", "ai làm", "bắt được lỗi gì"],
                 [["biên dịch", "trình biên dịch <code>javac</code>", "viết sai luật của ngôn ngữ (thiếu dấu <code>;</code>, sai tên, đặt chữ vào chỗ cần số): <b>lỗi biên dịch</b>"],
                  ["chạy", "máy ảo <code>java</code>", "chia cho 0, đọc ô không tồn tại…: <b>lỗi khi chạy</b> (máy ảo <b>ném ra ngoại lệ</b>: báo lỗi rồi dừng)"]]),
           """Hai bước này bắt hai loại lỗi khác nhau. Trình biên dịch bắt lỗi viết sai luật của ngôn ngữ, như thiếu dấu chấm phẩy hay sai tên, gọi là lỗi biên dịch, và khi đó không có tệp mã bai nào được tạo.
           Còn máy ảo chỉ phát hiện một số lỗi khi đang chạy, như chia cho không. Loại lỗi này gọi là lỗi khi chạy, vì chỉ lúc chương trình đang chạy mới lộ ra.
           Khi gặp nó, máy ảo ném ra một ngoại lệ, nghĩa là dừng việc đang làm và in thông báo lỗi."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: tạo, biên dịch, chạy", [
        st("""<p><b>Chuẩn bị.</b> Cài bộ công cụ <b>JDK</b> bản 21 trở lên (có bản miễn phí, ví dụ ở jdk.java.net hoặc adoptium.net); trong đó có trình biên dịch <code>javac</code> và máy ảo <code>java</code>.
Mở <b>Git Bash</b>: cửa sổ lệnh đi kèm Git for Windows (macOS, Linux: Terminal). Cả khoá chỉ dùng cửa sổ này.</p>
<div class="code"><div>javac -version</div></div>
<span class='note'>Làm thử: lệnh in ra số phiên bản, ví dụ javac 21.0.2, là máy đã sẵn sàng.</span>""",
           """Trước khi bắt đầu, máy cần có bộ công cụ JDK, bản hai mươi mốt trở lên, có bản tải miễn phí, vì trong đó có sẵn trình biên dịch và máy ảo.
           Ta gõ lệnh trong cửa sổ lệnh, tức một khung chữ nơi ta gõ lệnh cho máy rồi bấm phím xuống dòng. Cả khoá chỉ dùng loại cửa sổ này, tên trên màn hình, để lệnh chạy giống nhau trên mọi máy.
           Làm thử, gõ lệnh hỏi phiên bản của trình biên dịch; nó in ra số phiên bản là máy đã sẵn sàng."""),
        st("""<p><b>Bước 0. Đứng vào một thư mục làm việc.</b></p>
<div class="code"><div>mkdir -p ~/hoc/jva</div><div>cd ~/hoc/jva</div><div>pwd</div><div>ls</div></div>
<span class='note'>Làm thử: <code>pwd</code> in đường dẫn bạn đang đứng, ví dụ /c/Users/ban/hoc/jva; <code>ls</code> chưa in gì vì thư mục còn trống.</span>""",
           """Bước không, tạo một thư mục làm việc rồi đứng vào đó. Lệnh tạo thư mục có cờ p, nghĩa là không báo lỗi nếu thư mục đã có, và dấu ngã là thư mục nhà của bạn.
           Lệnh đổi thư mục đi vào thư mục vừa tạo. Lệnh in vị trí cho biết bạn đang đứng ở đâu, và lệnh liệt kê cho thấy trong đó chưa có tệp nào.
           Nhớ điều này, vì lệnh biên dịch ở bước hai chỉ nhìn thấy các tệp nằm ngay trong thư mục bạn đang đứng.""",
           focus=[1, "2.1", "2.2", ["2.3", "2.4"], 3]),
        st("""<p><b>Bước 1. Tạo tệp.</b> Mở trình soạn mã (ví dụ Visual Studio Code), gõ mã, lưu vào đúng thư mục trên với tên <code>Chao.java</code>. Tên tệp trùng tên lớp <code>public</code> (công khai: mọi nơi khác đều được dùng), kể cả chữ hoa.</p>
<span class='note'>Làm thử: lớp tên Chao thì tệp phải là Chao.java, không phải chao.java.</span>""",
           """Bước một là tạo tệp: mở một trình soạn mã, gõ đoạn mã vào đó, rồi lưu vào đúng thư mục vừa đứng, với tên Chao chấm Java. Tên tệp phải trùng tên lớp, kể cả chữ hoa chữ thường, vì luật của Java bắt lớp công khai nằm trong tệp cùng tên.
           Làm thử, lớp tên Chao viết hoa chữ đầu, thì tệp cũng viết hoa chữ đầu."""),
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
           """Chương trình này có năm lệnh in, mỗi lệnh thử một cách viết khác nhau với hai số hai và ba. Phần sau hai gạch chéo ở cuối mỗi dòng là chú thích, máy bỏ qua, nó chỉ đánh số cho ta dễ theo dõi.
           Ta đoán từng dòng trước khi chạy."""),
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
    sc_err = sc("doc_loi", "example", "Ví dụ: đọc một thông báo lỗi biên dịch thật", [
        st('<p>Tệp <code>Thieu.java</code> quên dấu <code>;</code> ở dòng thứ ba:</p>' + out_block(thieu_cham_phay, "Trình biên dịch báo"),
           """Ta đọc thông báo lỗi từ trên xuống. Dòng đầu cho biết tên tệp, số dòng là ba, và lỗi là máy đang chờ một dấu chấm phẩy.
           Dòng thứ hai là chính dòng mã đó, in lại. Dòng thứ ba có dấu mũ, chỉ đúng cột nơi máy nhận ra thiếu, ngay sau ngoặc đóng. Dòng cuối đếm số lỗi.""",
           focus=[0, "3.1", "3.2", "3.3", "3.4"]),
        st('<p>Lần này gõ sai chính tả tên lệnh in, thiếu chữ <code>l</code>:</p>' + out_block(chinh_ta, "Trình biên dịch báo"),
           """Lần này ta gõ sai chính tả tên lệnh in, thiếu một chữ cái. Máy báo không tìm thấy ký hiệu, nghĩa là nó không biết tên lệnh này.
           Dấu mũ chỉ đúng chỗ tên sai. Hai dòng dưới nói rõ: máy tìm một lệnh tên như thế trong đầu ra của hệ thống mà không thấy.""",
           focus=["3.2", "3.1", "3.3", ["3.4", "3.5"]], clear=True),
        st("""<div class="box key"><b>Cách đọc lỗi biên dịch.</b>
<ol><li>Đọc <b>dòng đầu</b>: tên tệp, số dòng, lời báo.</li><li>Nhìn <b>dấu mũ</b>: máy nhận ra lỗi ở đó.</li>
<li>Sửa <b>lỗi đầu tiên</b> rồi biên dịch lại: các lỗi sau thường là hệ quả của nó.</li></ol>
<span class="note">Máy báo chỗ nó <b>nhận ra</b>; chỗ sai thật có thể nằm ngay trước đó.</span></div>""",
           """Rút ra cách đọc lỗi biên dịch. Một, đọc dòng đầu để biết tệp, dòng và lời báo. Hai, nhìn dấu mũ để biết máy nhận ra lỗi ở đâu.
           Ba, chỉ sửa lỗi đầu tiên rồi biên dịch lại, vì các lỗi sau thường là hệ quả của nó.
           Và nhớ rằng máy báo chỗ nó nhận ra lỗi, còn chỗ sai thật có thể nằm ngay trước đó.""", clear=True,
           focus=[0, "1.2", "1.2", "1.2", "1.3"]),
    ])
    sc_scale = sc("quymo", "concept", "Khi lô giao dịch lớn dần, lỗi nằm ở đâu thì rẻ nhất?", [
        st("""<p>Một lô $n$ lệnh, mỗi lệnh mất $1$ mili giây (số minh hoạ). Lệnh <b>ở giữa lô</b> chia cho $0$ nên chương trình dừng.</p>"""
           + table(["lô n", "cả lô", "lệnh lỗi", "đã xong", "chưa làm", "làm dở phải bỏ"],
                   [["10", "0,01 giây", "5", "4", "6", "4 mili giây"],
                    ["1 000", "1 giây", "500", "499", "501", "0,499 giây"],
                    ["1 000 000", "1 000 giây ≈ 16,7 phút", "500 000", "499 999", "500 001", "499,999 giây ≈ 8,3 phút"]]),
           """Giả sử một lô có n lệnh, mỗi lệnh mất một phần nghìn giây, số minh hoạ. Lệnh ở giữa lô chia cho không, nên chương trình dừng giữa chừng.
           Lô mười lệnh đã xong bốn lệnh, còn sáu chưa làm. Lô một nghìn lệnh đã xong bốn trăm chín mươi chín, chưa làm năm trăm linh một.
           Lô một triệu lệnh mất gần mười bảy phút, chết ở giữa thì gần tám phút công việc đã làm dở và nửa triệu lệnh nằm chờ.""",
           focus=[1, 1, "2.2", "2.3", "2.4"]),
        st("""<div class="box key"><b>Điều người làm nghề rút ra.</b> Càng lớn, lỗi chỉ lộ lúc chạy càng đắt: phải biết <b>đã xong tới đâu</b> và chạy tiếp thế nào.
Lỗi biên dịch thì rẻ nhất: <b>0</b> lệnh bị chạy, sửa ngay tại bàn. Vì thế người ta dồn nhiều lỗi nhất có thể về phía biên dịch.</div>""",
           """Lô càng lớn thì lỗi chỉ lộ lúc chạy càng đắt, vì ta phải biết đã xong tới đâu và chạy tiếp thế nào.
           Lỗi biên dịch rẻ nhất, vì không lệnh nào bị chạy. Nên người làm nghề cố đẩy càng nhiều lỗi càng tốt về phía biên dịch.""",
           clear=True),
    ], checks=["10 // 2 - 1 == 4", "10 - (10 // 2 - 1) == 6", "1000 // 2 - 1 == 499", "1000 - 499 == 501",
               "1000000 // 2 - 1 == 499999", "1000000 - 499999 == 500001", "1000000 * 1 / 1000 == 1000",
               "round(1000 / 60, 1) == 16.7", "round(499.999 / 60, 1) == 8.3", "10 * 1 / 1000 == 0.01"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: nhìn kiểu của từng vế", [
        st(table(["dòng", "vế trái của dấu + đầu tiên", "loại phép +", "kết quả"],
                 [["①", "số 2", "cộng số", "5"], ["③", "chuỗi \"Tong: \"", "nối chữ (cả hai lần)", "Tong: 23"],
                  ["④", "chuỗi \"Tong: \"", "ngoặc là số 5, rồi nối", "Tong: 5"], ["⑤", "số 2", "cộng số, rồi nối", "5 dong"]]),
           """Kiểm bằng đường khác, chỉ cần nhìn kiểu của hai vế mỗi lần gặp dấu cộng, làm từ trái sang phải. Nếu cả hai vế đều là số thì cộng số.
           Nếu một trong hai vế là chuỗi thì nối chữ. Áp quy tắc này cho từng dòng, ta ra đúng bốn kết quả như khi chạy."""),
    ], checks=["len('5|2 + 3|Tong: 23|Tong: 5|5 dong'.split('|')) == 5"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Lưu lớp <code>Chao</code> vào tệp <code>Loi.java</code>.</div>'
           + code_block(sai_ten, lines=(1, 1)) + out_block(sai_ten, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là đặt tên tệp khác tên lớp. Lớp tên Chao nhưng lưu trong một tệp tên khác.
           Trình biên dịch từ chối ngay, và báo rằng lớp Chao phải nằm trong tệp tên Chao chấm Java."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Biên dịch khi đang đứng sai thư mục.</div>'
           '<div class="code"><div>cd ~</div><div>javac Chao.java</div></div>'
           '<p><b>Trình biên dịch báo</b> (thư mục nhà chưa có tệp Chao.java)</p>'
           '<div class="code"><div>error: file not found: Chao.java</div><div>Usage: javac &lt;options&gt; &lt;source files&gt;</div>'
           '<div>use --help for a list of possible options</div></div>',
           """Lỗi thứ hai, cũng của người mới, là biên dịch khi đang đứng sai thư mục. Lệnh đổi thư mục kèm dấu ngã đưa ta về thư mục nhà, nơi chưa có tệp Chao.
           Khi đó trình biên dịch báo không tìm thấy tệp, vì nó chỉ nhìn thư mục đang đứng. Cách sửa là hỏi lại vị trí bằng lệnh in vị trí, rồi đi vào đúng thư mục chứa tệp."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tin rằng “biên dịch được là chạy đúng”.</div>'
           + code_block(chia_khong, lines=(3, 6)) + out_block(chia_khong),
           """Lỗi thứ ba, của cả người đã đi làm, là tin rằng biên dịch được thì chạy đúng. Chương trình này biên dịch không lỗi.
           Nó tạo một ô nhớ có tên là số người, đặt vào số không; loại ô nhớ có tên này gọi là biến.
           Khi chạy, nó in bắt đầu, rồi chia một trăm nghìn cho số không, và máy ảo ném ra ngoại lệ phép tính. Dòng kết thúc không được in vì chương trình đã dừng."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(3, 5), title="Đoán ba dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Chương trình có ba lệnh in. Lệnh một nối chữ A với một rồi với hai. Lệnh hai lấy một cộng hai rồi nối chữ A.
           Lệnh ba nối chữ A với một cộng hai đặt trong ngoặc. Hãy dừng video, viết ra giấy ba dòng in ra.""", pause=20),
        st("<p>Áp quy tắc dấu cộng, từ trái sang phải:</p>$$\\text{\"A\"} + 1 + 2 = \\hl{\\text{A12}} \\qquad 1 + 2 + \\text{\"A\"} = \\hl{\\text{3A}} \\qquad \\text{\"A\"} + (1 + 2) = \\hl{\\text{A3}}$$",
           """Đáp án như sau. Dòng một, vế trái là chuỗi nên nối cả hai lần, ra A một hai. Dòng hai, hai số đứng trước nên cộng thành ba rồi nối, ra ba A.
           Dòng ba, ngoặc tính trước ra ba, rồi nối, ra A ba."""),
        st(out_block(quiz),
           """Chạy thật chương trình, ba dòng in ra đúng là A một hai, ba A, và A ba."""),
        st(table(["tình huống", "lỗi lúc biên dịch hay lúc chạy? vì sao?"],
                 [["a. gõ <code>Sytem.out.println(\"Chao\");</code> (thiếu chữ <code>s</code>)", "?"],
                  ["b. chia tổng tiền cho số người, nhưng danh sách rỗng nên số người bằng 0", "?"],
                  ["c. quên dấu <code>;</code> cuối một lệnh", "?"]]),
           """Câu hai là một quyết định. Với mỗi tình huống, hãy nói máy báo lỗi lúc biên dịch hay lúc chạy, và vì sao. Tình huống a gõ thiếu một chữ trong tên kho lệnh hệ thống.
           Tình huống b chia cho số người bằng không vì danh sách rỗng. Tình huống c quên dấu chấm phẩy. Hãy dừng video và trả lời.""", pause=15,
           focus=[1, 1, "1.2", "1.3", "1.4", 1]),
        st(table(["tình huống", "lúc nào", "vì sao"],
                 [["a", "<b>biên dịch</b>", "tên <code>Sytem</code> không tồn tại, máy tra tên là biết ngay"],
                  ["b", "<b>chạy</b>", "số người chỉ biết bằng 0 khi chạy, máy không đoán trước được"],
                  ["c", "<b>biên dịch</b>", "thiếu dấu là sai luật viết, thấy ngay khi đọc mã"]]),
           """Đáp án, tình huống a là lỗi biên dịch, vì máy tra tên và biết ngay không có tên đó. Tình huống b là lỗi lúc chạy, vì số người bằng không hay không chỉ biết khi chạy.
           Tình huống c là lỗi biên dịch, vì thiếu dấu là sai luật viết. Quy tắc: cái gì máy nhìn mã là biết thì bị bắt lúc biên dịch, cái gì phụ thuộc dữ liệu lúc chạy thì chưa.""",
           focus=["1.2", "1.3", "1.4", 1]),
    ], checks=["'A' + str(1) + str(2) == 'A12'", "str(1 + 2) + 'A' == '3A'", "'A' + str(1 + 2) == 'A3'"])
    write_lab("JVA", "L00", """# Lab JVA L00 — Phiếu số dư đầu tiên

Làm trong **Git Bash**, đứng đúng thư mục (xem bước 1).

1. `mkdir -p ~/hoc/jva`, rồi `cd ~/hoc/jva`; kiểm bằng `pwd`.
2. Dùng trình soạn mã tạo tệp `PhieuSo.java` (chữ hoa chữ đầu) trong thư mục đó, lớp `PhieuSo`. Hàm chính in **đúng năm dòng**:
   - `Xin chao Lan`
   - `So du: 250000 dong`
   - `Phi: 1500 + 500` (chuỗi, in nguyên chữ)
   - `Tong phi: 2000` (chuỗi nối với **phép cộng hai số đặt trong ngoặc**)
   - `Ghep: 1500500` (cùng hai số nhưng **không ngoặc**, để thấy dấu + nối chữ)
3. `javac PhieuSo.java && java PhieuSo`
4. Xoá thử dấu `;` ở dòng cuối, biên dịch lại, đọc dòng đầu thông báo (tệp, số dòng) rồi sửa lại.

Chấm: `bash labs/cham.sh JVA L00 PhieuSo.java`.
""", "java", phieu["code"], phieu["out"])
    sc_lab = practice_scene(sc, "Tự làm: phiếu số dư năm dòng", practice_steps(
        st, "JVA", "L00",
        """<p><b>Đề</b> (trong Git Bash):</p>
<ol><li><code>mkdir -p ~/hoc/jva</code>, <code>cd ~/hoc/jva</code>, <code>pwd</code></li>
<li>Tạo <code>PhieuSo.java</code>, in năm dòng: <code>Xin chao Lan</code>; <code>So du: 250000 dong</code>; <code>Phi: 1500 + 500</code>; <code>Tong phi: …</code> (cộng hai số trong ngoặc); <code>Ghep: …</code> (không ngoặc)</li>
<li>Biên dịch, chạy; xoá thử một dấu <code>;</code>, đọc dòng đầu thông báo, rồi sửa lại</li></ol>""",
        """Bây giờ tới phần bạn tự làm trên máy, trong cửa sổ lệnh. Tạo thư mục làm việc, đứng vào đó, rồi viết chương trình in phiếu năm dòng.
        Dòng một là lời chào. Dòng hai là số dư hai trăm năm mươi nghìn đồng. Dòng ba in nguyên chữ một nghìn năm trăm cộng năm trăm.
        Dòng bốn nối chữ với phép cộng hai số trong ngoặc. Dòng năm nối chữ với hai số không ngoặc. Chạy xong, xoá thử một dấu chấm phẩy, đọc dòng đầu thông báo rồi sửa lại.
        Hãy dừng video và tự làm, đừng chép lại ví dụ.""",
        phieu["out"], "PhieuSo.java",
        """<div class="box key"><b>Nếu kẹt:</b> lệnh in thứ tư viết <code>"Tong phi: " + (1500 + 500)</code>, lệnh in thứ năm viết <code>"Ghep: " + 1500 + 500</code> — máy làm từ trái sang phải nên lệnh thứ năm nối chữ hai lần.
Lời giải nằm ở <code>labs/JVA/L00/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, nhớ rằng máy làm từ trái sang phải. Dòng bốn đặt phép cộng trong ngoặc để cộng số trước. Dòng năm không ngoặc nên nối chữ hai lần.
        Lời giải nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=60), "JVA", "L00")
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
                  ["Kể đúng ba bước gõ, biên dịch, chạy và vai trò của máy ảo Java",
                   "Nêu ý nghĩa từng chữ của chương trình đầu tiên: lớp, hàm chính, lệnh in, chuỗi, chú thích",
                   "Phân biệt lỗi biên dịch với lỗi khi chạy, và biết lỗi nào rẻ nhất khi lô giao dịch lớn dần",
                   "Dự đoán dấu cộng là cộng số hay nối chữ",
                   "Đọc thông báo lỗi biên dịch: tên tệp, số dòng, dấu mũ và lời gợi ý",
                   "Viết, biên dịch và chạy một chương trình trong cửa sổ lệnh, đứng đúng thư mục"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_err, sc_scale, sc_chk, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "intuition"), (2, "sym"), (3, "quymo"), (4, "example"), (5, "doc_loi"), (6, "practice")])
