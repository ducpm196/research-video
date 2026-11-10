from lib import *

# Hai lớp dùng chung: loại ngoại lệ tự định nghĩa và lớp tài khoản (bài lớp và đối tượng), nay rút quá số dư thì NÉM ngoại lệ.
HEAD = """
class KhongDuTien extends Exception {
    KhongDuTien(String thongBao) {
        super(thongBao);                  // giữ lời nhắn lỗi
    }
}

class TaiKhoan {
    private long soDu;
    TaiKhoan(long soDu) { this.soDu = soDu; }
    long laySoDu() { return soDu; }
    void rut(long tien) throws KhongDuTien {
        if (tien > soDu) {
            throw new KhongDuTien("Can " + tien + ", chi co " + soDu);
        }
        soDu -= tien;
    }
}
"""


def ln(p, s):
    """Số thứ tự (từ 1) của dòng đầu tiên trong mã của p chứa chuỗi s."""
    return next(i for i, l in enumerate(p["code"].split("\n"), 1) if s in l)


def build():
    cu = prog("Cu", """
class TaiKhoan {
    private long soDu;
    TaiKhoan(long soDu) { this.soDu = soDu; }
    void rut(long tien) {
        if (tien > soDu) {
            System.out.println("Khong du tien");   // chỉ in, rồi quay về
            return;
        }
        soDu -= tien;
    }
}

public class Cu {
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoan(100000);
        tk.rut(500000);
        System.out.println("In bien lai: da rut 500000");
    }
}""", out="Khong du tien\nIn bien lai: da rut 500000")
    rut = prog("Rut", HEAD + """
public class Rut {
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoan(100000);
        try {
            tk.rut(30000);
            System.out.println("Rut 30000 xong");
            tk.rut(500000);
            System.out.println("Dong nay khong chay");
        } catch (KhongDuTien e) {
            System.out.println("Tu choi: " + e.getMessage());
        } finally {
            System.out.println("So du: " + tk.laySoDu());
        }
    }
}""", out="Rut 30000 xong\nTu choi: Can 500000, chi co 70000\nSo du: 70000")
    chua_bat = prog("ChuaBat", HEAD + """
public class ChuaBat {
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoan(100000);
        tk.rut(500000);                   // không bắt, không khai báo
    }
}""", expect="compile_error:unreported exception KhongDuTien; must be caught or declared to be thrown")
    tai_nguyen = prog("TaiNguyen", r"""
import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;

public class TaiNguyen {
    public static void main(String[] args) {
        String duLieu = "A01;500000\nB02;300000";
        try (BufferedReader r = new BufferedReader(new StringReader(duLieu))) {
            System.out.println(r.readLine());
            System.out.println(r.readLine());
        } catch (IOException e) {                 // có kiểm tra: bắt buộc bắt
            System.out.println("Loi doc: " + e.getMessage());
        }
    }
}""", out="A01;500000\nB02;300000")
    thu_tu = prog("ThuTu", """
public class ThuTu {
    static int chia(int a, int b) {
        return a / b;
    }
    public static void main(String[] args) {
        System.out.println("1");
        try {
            System.out.println("2: " + chia(10, 2));
            System.out.println("3: " + chia(10, 0));
            System.out.println("4");
        } catch (ArithmeticException e) {
            System.out.println("5: " + e.getMessage());
        } finally {
            System.out.println("6");
        }
        System.out.println("7");
    }
}""", out="1\n2: 5\n5: / by zero\n6\n7")
    vet = prog("Vet", """
public class Vet {
    static int chia(int a, int b) {
        return a / b;
    }
    static int chiaPhi(int phi) {
        return chia(phi, 0);              // lỗi cố ý: 0 người
    }
    public static void main(String[] args) {
        System.out.println("1");
        System.out.println(chiaPhi(10));
    }
}""", out="1", expect="runtime_error:ArithmeticException",
        err='Exception in thread "main" java.lang.ArithmeticException: / by zero\n'
            '\tat Vet.chia(Vet.java:3)\n\tat Vet.chiaPhi(Vet.java:6)\n\tat Vet.main(Vet.java:10)')
    thu_tu_bat = prog("ThuTuBat", """
public class ThuTuBat {
    public static void main(String[] args) {
        int soNguoi = 0;
        try {
            System.out.println(90000 / soNguoi);
        } catch (Exception e) {
            System.out.println("Loi chung");
        } catch (ArithmeticException e) {
            System.out.println("Chia cho 0");
        }
    }
}""", expect="compile_error:exception ArithmeticException has already been caught")
    nuot = prog("Nuot", HEAD + """
public class Nuot {
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoan(100000);
        try {
            tk.rut(500000);
        } catch (KhongDuTien e) {
            // để sau tính
        }
        System.out.println("In bien lai: da rut 500000");
        System.out.println("So du: " + tk.laySoDu());
    }
}""", out="In bien lai: da rut 500000\nSo du: 100000")
    rong = prog("Rong", HEAD + """
public class Rong {
    static long phiMoiLan(long phi, int soLan) {
        return phi / soLan;
    }
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoan(100000);
        try {
            long phi = phiMoiLan(3000, 0);    // lỗi lập trình
            tk.rut(30000 + phi);
        } catch (Exception e) {
            System.out.println("Khong du tien, vui long nap them");
        }
    }
}""", out="Khong du tien, vui long nap them")
    quiz = prog("DoanKetQua", """
public class DoanKetQua {
    static long rut(long soDu, long tien) {
        if (tien > soDu) { throw new IllegalArgumentException("Thieu " + (tien - soDu)); }
        return soDu - tien;
    }
    public static void main(String[] args) {
        long soDu = 100;
        try {
            soDu = rut(soDu, 40);
            soDu = rut(soDu, 90);
            System.out.println("A");
        } catch (IllegalArgumentException e) {
            System.out.println("B " + e.getMessage());
        } finally {
            System.out.println("C " + soDu);
        }
    }
}""", out="B Thieu 30\nC 60")

    r_main = ln(rut, "public class Rut")
    sc_hook = sc("hook", "hook", "Rút quá số dư mà biên lai vẫn in “đã rút”?", [
        st(code_block(cu, lines=(4, 10), title="Lớp tài khoản kiểu cũ, rút gọn: rút quá số dư thì chỉ in thông báo")
           + "<span class='note'>Ở bài 7, hàm rút còn trả về đúng hoặc sai, nhưng không gì <b>buộc</b> người gọi phải xem giá trị đó.</span>",
           """Nhớ lại lớp tài khoản ở bài bảy. Bản rút gọn này, khi rút quá số dư, chỉ in một dòng thông báo rồi quay về.
           Ở bài bảy hàm rút còn trả về đúng hoặc sai, nhưng không gì buộc người gọi phải xem giá trị đó."""),
        st(code_block(cu, lines=(14, 18)) + out_block(cu),
           """Người gọi không hề biết lệnh rút đã thất bại, nên vẫn in biên lai đã rút năm trăm nghìn.
           Với ngân hàng, đó là một lỗi nghiêm trọng."""),
        st("""<div class="box key">Hôm nay: <b>ngoại lệ</b> — cách để phương thức <b>báo lỗi cho người gọi</b>, và buộc người gọi phải xử lý.
Bạn cũng học đọc <b>dấu vết ngăn xếp</b> để tìm đúng lệnh gây lỗi.</div>
<p><b>Ngăn xếp</b> (lời gọi): danh sách các hàm đang chạy dở, hàm được gọi sau cùng nằm trên cùng. <b>Dấu vết ngăn xếp</b>: bản in danh sách đó lúc lỗi xảy ra.</p>""",
           """Hôm nay ta học ngoại lệ, cách để một phương thức báo lỗi cho người gọi và buộc người gọi phải xử lý.
           Bạn cũng sẽ đọc dấu vết ngăn xếp để tìm đúng lệnh gây lỗi.
           Ngăn xếp ở đây là danh sách các hàm đang chạy dở, hàm được gọi sau cùng nằm trên cùng, còn dấu vết ngăn xếp là bản in danh sách đó lúc lỗi xảy ra."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: lớp tài khoản và lỗi khi chạy", [
        st(table(["đã học", "điều dùng lại hôm nay"],
                 [["① Lớp tài khoản", "trường <code>private</code> số dư, hàm tạo, phương thức rút giữ bất biến “số dư không âm”"],
                  ["② Lỗi khi chạy", "chia cho 0 hay vượt chỉ số mảng: máy ảo ném <b>ngoại lệ</b>, chương trình dừng"],
                  ["③ Gọi lồng hàm", "hàm chính gọi hàm A, hàm A gọi hàm B; xong B mới quay về A"]]),
           """Ta ôn ba điều. Thứ nhất, lớp tài khoản có trường số dư riêng, và phương thức rút giữ bất biến số dư không âm.
           Thứ hai, khi chia cho không hay vượt chỉ số mảng, máy ảo ném ra ngoại lệ và chương trình dừng.
           Thứ ba, hàm có thể gọi lồng nhau: hàm chính gọi hàm A, hàm A gọi hàm B, xong B mới quay về A."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ký hiệu: thử, bắt, cuối cùng, ném", [
        st(table(["viết", "nghĩa"],
                 [["<code>try { … }</code>", "<b>khối thử</b>: các lệnh có thể gặp lỗi"],
                  ["<code>catch (KhongDuTien e) { … }</code>", "<b>khối bắt</b>: chạy khi có ngoại lệ đúng loại; <code>e</code> là ngoại lệ đó"],
                  ["<code>finally { … }</code>", "<b>khối cuối cùng</b>: chạy mỗi khi rời khối thử, có lỗi hay không (chỉ bỏ lỡ khi cả chương trình bị tắt ngang, như gọi <code>System.exit</code>)"],
                  ["<code>throw new KhongDuTien(\"…\")</code>", "<b>ném</b>: tạo ngoại lệ và dừng phương thức ngay"],
                  ["<code>throws KhongDuTien</code>", "ghi trên phương thức: “có thể ném loại này”"],
                  ["<code>class KhongDuTien extends Exception</code>", "<b>kế thừa</b>: lớp mới là <b>một loại</b> <code>Exception</code> (lớp cha), nhận sẵn mọi thứ lớp cha có"],
                  ["<code>super(thongBao);</code>", "trong hàm tạo: gọi hàm tạo của lớp cha, đưa lời nhắn cho lớp cha giữ"],
                  ["<code>e.getMessage()</code>", "lấy lời nhắn lỗi đã gửi kèm"]]),
           """Bảng ký hiệu của bài. Khối thử chứa các lệnh có thể gặp lỗi. Khối bắt chạy khi có ngoại lệ đúng loại ghi trong ngoặc, và e chính là ngoại lệ đó.
           Khối cuối cùng chạy mỗi khi rời khối thử, có lỗi hay không, chỉ trừ khi cả chương trình bị tắt ngang.
           Lệnh ném tạo một ngoại lệ và dừng phương thức ngay lập tức.
           Còn khai báo có thể ném thì ghi trên đầu phương thức, báo trước rằng nó có thể ném loại này.
           Dòng kế dùng từ khoá kế thừa: lớp mới là một loại của lớp ngoại lệ gốc, gọi là lớp cha, và nhận sẵn mọi thứ lớp cha có.
           Trong hàm tạo, từ khoá gọi lớp cha chuyển lời nhắn lên cho lớp cha giữ.
           Cuối cùng, ta lấy lời nhắn lỗi bằng phương thức lấy lời nhắn.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: ngoại lệ đi ngược đường gọi tới khối bắt gần nhất", [
        st(svg(1500, 400,
               box(20, 60, 300, 120, ["hàm chính", "khối thử", "gọi tk.rut(500000)"], C_BLUE, 22, bold=True),
               arrow(325, 120, 470, 120, "#2a78d6", "gọi"),
               box(480, 60, 330, 120, ["rut", "500000 > 70000", "ném KhongDuTien"], C_RED, 22, bold=True),
               arrow(645, 185, 645, 260, "#dc2626"),
               txt(660, 230, "ngoại lệ quay ngược về người gọi", 22, "start", "#dc2626"),
               box(480, 270, 330, 100, ["khối bắt", "in Tu choi: …"], C_AMBER, 22, bold=True),
               arrow(815, 320, 960, 320, "#16a34a"),
               box(970, 270, 300, 100, ["khối cuối cùng", "in So du: 70000"], C_GREEN, 22, bold=True),
               box(970, 60, 300, 120, ["lệnh in kế tiếp", "bị bỏ qua"], C_GRAY, 22, dash=True),
               txt(1120, 215, "không chạy", 22, "middle", "#6b7280")),
           """Hình này là đường đi của một ngoại lệ. Trong khối thử, hàm chính gọi rút năm trăm nghìn.
           Số dư chỉ có bảy mươi nghìn, nên phương thức rút ném ngoại lệ không đủ tiền và dừng ngay.
           Ngoại lệ quay ngược về người gọi, và lệnh in kế tiếp bị bỏ qua.
           Máy ảo tìm khối bắt gần nhất đúng loại, chạy nó, rồi chạy khối cuối cùng."""),
        st(table(["", "có kiểm tra", "không kiểm tra"],
                 [["lớp cha", "<code>Exception</code> (trừ nhánh <code>RuntimeException</code>)", "<code>RuntimeException</code>"],
                  ["ví dụ", "<code>KhongDuTien</code> (tự viết), <code>IOException</code>", "<code>ArithmeticException</code>, <code>IllegalArgumentException</code>"],
                  ["trình biên dịch", "<b>bắt buộc</b> bắt, hoặc khai <code>throws</code>", "không bắt buộc"],
                  ["dùng cho", "tình huống nghiệp vụ người gọi phải xử lý", "lỗi lập trình, đối số sai"]]),
           """Ngoại lệ chia làm hai nhóm. Nhóm có kiểm tra gồm con cháu của lớp ngoại lệ gốc, trừ nhánh ngoại lệ khi chạy.
           Với nhóm này, trình biên dịch bắt buộc người gọi phải bắt, hoặc khai báo có thể ném tiếp.
           Nhóm không kiểm tra, như ngoại lệ phép tính, thì không bắt buộc, và thường báo lỗi lập trình.
           Không đủ tiền là tình huống người gọi phải xử lý, nên ta xếp nó vào nhóm có kiểm tra.""", clear=True),
        st(code_block(tai_nguyen, lines=(7, 13), title="Khối thử có tài nguyên: mở ở ngoặc tròn, tự đóng khi rời khối")
           + "<span class='note'><code>\\n</code> trong chuỗi là ký tự xuống dòng, nên <code>duLieu</code> có hai dòng; "
             "<code>r.readLine()</code> đọc từng dòng một.</span>" + out_block(tai_nguyen),
           """Một dạng nữa là khối thử có tài nguyên. Bộ đọc được mở trong ngoặc tròn sau từ khoá thử, và máy tự đóng nó khi rời khối, dù có lỗi hay không.
           Dấu gạch chéo ngược kèm chữ n trong chuỗi là ký tự xuống dòng, nên dữ liệu có hai dòng, và mỗi lần đọc lấy ra một dòng.
           Đọc dữ liệu có thể gặp ngoại lệ vào ra, thuộc nhóm có kiểm tra, nên phải bắt nó hoặc khai báo ném tiếp, và ở đây ta bắt."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: rút quá số dư thì ném ngoại lệ tự định nghĩa", [
        st(code_block(rut, lines=(1, 5), title="Bước 1. Định nghĩa loại ngoại lệ “không đủ tiền”"),
           """Bước một, định nghĩa loại ngoại lệ không đủ tiền. Từ khoá kế thừa nói lớp này là một loại ngoại lệ có kiểm tra, vì lớp cha là ngoại lệ gốc.
           Hàm tạo nhận lời nhắn, rồi chuyển lên cho lớp cha giữ."""),
        st(code_block(rut, lines=(11, 16), title="Bước 2. Phương thức rút: kiểm tra, ném, rồi mới trừ"),
           """Bước hai, phương thức rút khai báo có thể ném không đủ tiền. Số tiền lớn hơn số dư thì ném, kèm lời nhắn cần bao nhiêu, có bao nhiêu.
           Lệnh ném dừng phương thức ngay, nên dòng trừ tiền không chạy, và số dư không bao giờ âm."""),
        st(code_block(chua_bat, lines=(ln(chua_bat, "TaiKhoan tk"), ln(chua_bat, "tk.rut"))) + out_block(chua_bat, "Trình biên dịch báo"),
           """Bước ba, thử gọi rút mà không bắt. Trình biên dịch từ chối, vì đây là ngoại lệ có kiểm tra.
           Nghĩa là không ai quên được trường hợp không đủ tiền."""),
        st(code_block(rut, lines=(r_main + 2, r_main + 13), title="Bước 4. Người gọi bắt và xử lý"),
           """Bước bốn, người gọi đặt hai lệnh rút trong khối thử. Lệnh thứ nhất rút ba mươi nghìn, thành công.
           Lệnh thứ hai bị ném ngoại lệ, nên nhảy thẳng tới khối bắt, in lời từ chối.
           Khối cuối cùng in số dư, vì nó luôn chạy."""),
        st(out_block(rut),
           """Chạy thật, đúng ba dòng: rút ba mươi nghìn xong, từ chối vì chỉ có bảy mươi nghìn, và số dư còn bảy mươi nghìn.
           Dòng không chạy đúng là không xuất hiện."""),
    ], checks=["100000 - 30000 == 70000", "500000 > 70000"])
    sc_ex = sc("example", "example", "Ví dụ: thứ tự in của thử, bắt, cuối cùng — từng bước", [
        st(code_block(thu_tu, lines=(6, 16), title="Tệp ThuTu.java, phần thân hàm chính"),
           """Ví dụ này có bảy lệnh in, đánh số từ một tới bảy. Ta theo máy ảo qua năm bước, rồi đoán những số nào được in."""),
        st(code_block(thu_tu, lines=(6, 8)) + "$$① \\; \\text{in } 1 \\qquad ② \\; 10 / 2 = \\hl{5} \\to \\text{in “2: 5”}$$",
           """Bước một, in số một, vì lệnh nằm trước khối thử. Bước hai, mười chia hai bằng năm, nên in hai, năm."""),
        st(code_block(thu_tu, lines=(9, 10)) + "$$③ \\; 10 / 0 \\to \\text{ném ngoại lệ, bỏ qua “3” và “4”}$$",
           """Bước ba, mười chia không. Phép chia ném ngoại lệ phép tính ngay trong hàm chia,
           nên lệnh in số ba chưa kịp in, và lệnh in số bốn bị bỏ qua."""),
        st(code_block(thu_tu, lines=(11, 12)) + "$$④ \\; \\text{khối bắt in “5: / by zero”}$$",
           """Bước bốn, máy ảo tìm thấy khối bắt đúng loại, in số năm kèm lời nhắn chia cho không."""),
        st(code_block(thu_tu, lines=(13, 16)) + "$$⑤ \\; \\text{khối cuối cùng in } 6, \\text{ rồi chạy tiếp, in } 7$$",
           """Bước năm, khối cuối cùng in số sáu. Lỗi đã được xử lý, nên chương trình chạy tiếp và in số bảy."""),
        st(out_block(thu_tu),
           """Chạy thật, năm dòng in ra đúng như ta theo: một, hai năm, năm kèm lời nhắn, sáu, bảy. Số ba và số bốn không xuất hiện."""),
    ], checks=["10 // 2 == 5", "len(['1', '2: 5', '5: / by zero', '6', '7']) == 5"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: bỏ khối bắt, đọc dấu vết ngăn xếp", [
        st(code_block(vet, lines=(2, 10)) + out_block(vet, "Không có khối bắt: máy ảo tự in dấu vết"),
           """Kiểm phép tính thứ ba bằng đường khác: bỏ khối bắt, để máy ảo tự in dấu vết ngăn xếp.
           Dòng đầu cho cùng loại ngoại lệ và cùng lời nhắn chia cho không, nên khớp với khối bắt ở ví dụ."""),
        st(table(["dấu vết", "đọc là", "lệnh ở đó"],
                 [["<code>at Vet.chia(Vet.java:3)</code>", "lỗi xảy ra ở dòng thứ 3, trong <code>chia</code>", "<code>return a / b;</code> với <code>b = 0</code>"],
                  ["<code>at Vet.chiaPhi(Vet.java:6)</code>", "<code>chia</code> được gọi từ dòng thứ 6", "<code>return chia(phi, 0);</code>"],
                  ["<code>at Vet.main(Vet.java:10)</code>", "<code>chiaPhi</code> được gọi từ hàm chính", "<code>chiaPhi(10)</code>"]]),
           """Đọc từ trên xuống. Dòng đầu là nơi lỗi xảy ra: dòng số ba, phép chia a cho b, với b bằng không.
           Dòng kế cho biết ai gọi nó: dòng số sáu, chính là chỗ truyền số không, tức gốc của lỗi.
           Dòng cuối là hàm chính, nơi mọi thứ bắt đầu. Ba dòng ứng với ba lần gọi lồng, nên khớp với mã.""", clear=True),
    ], checks=["len(['main', 'chiaPhi', 'chia']) == 3"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Bắt loại rộng trước, loại hẹp sau.</div>'
           + code_block(thu_tu_bat, lines=(4, 10)) + out_block(thu_tu_bat, "Trình biên dịch báo"),
           """Lỗi thứ nhất, của người mới, là đặt khối bắt loại rộng trước loại hẹp.
           Khối bắt ngoại lệ gốc đã bắt mọi thứ, nên khối bắt phép tính phía sau không bao giờ tới được, và trình biên dịch báo lỗi. Hãy xếp loại hẹp lên trước."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Khối bắt rỗng nuốt mất lỗi.</div>'
           + code_block(nuot, lines=(ln(nuot, "TaiKhoan tk"), ln(nuot, "So du:"))) + out_block(nuot),
           """Lỗi thứ hai, của người đã đi làm, là khối bắt rỗng, định để sau tính.
           Lỗi bị nuốt mất: biên lai ghi đã rút năm trăm nghìn, nhưng số dư vẫn là một trăm nghìn. Khách được báo thành công dù tiền không hề rút.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Bắt <code>Exception</code> quá rộng.</div>'
           + code_block(rong, lines=(ln(rong, "TaiKhoan tk"), ln(rong, "vui long"))) + out_block(rong),
           """Lỗi thứ ba là bắt loại ngoại lệ gốc, quá rộng. Ở đây lỗi thật là chia cho không, một lỗi lập trình.
           Nhưng khối bắt rộng nuốt luôn nó và báo khách không đủ tiền, dù tài khoản còn một trăm nghìn.""", clear=True),
        st("""<div class="box key">Cách sửa lỗi 2 và 3: chỉ bắt <b>đúng loại</b> mình xử lý được (<code>KhongDuTien</code>), và trong khối bắt
<b>làm việc thật</b>: báo người dùng, ghi nhật ký, không in biên lai. Lỗi lập trình cứ để lộ ra, kèm dấu vết, để sửa tận gốc.</div>""",
           """Cách sửa lỗi hai và ba: chỉ bắt đúng loại mình xử lý được, và trong khối bắt phải làm việc thật, như báo người dùng hay ghi nhật ký.
           Còn lỗi lập trình thì cứ để lộ ra kèm dấu vết, để sửa tận gốc.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(2, 5), title="Đoán các dòng in ra") + code_block(quiz, lines=(7, 16)),
           """Bây giờ tới phần bạn tự làm. Hàm rút ném ngoại lệ đối số không hợp lệ nếu số tiền lớn hơn số dư, kèm số tiền còn thiếu.
           Số dư ban đầu là một trăm, ta rút bốn mươi rồi rút chín mươi. Hãy dừng video và viết ra các dòng in ra.""", pause=20),
        st(table(["lệnh", "điều xảy ra", "số dư"],
                 [["<code>rut(100, 40)</code>", "$40 \\le 100$, trả $100 - 40 = 60$", "60"],
                  ["<code>rut(60, 90)</code>", "$90 > 60$: ném, lời nhắn “Thieu” $90 - 60 = 30$; phép gán không xảy ra", "vẫn 60"],
                  ["khối bắt", "in <b>B Thieu 30</b>; chữ A bị bỏ qua", "60"],
                  ["khối cuối cùng", "in <b>C 60</b>", "60"]]),
           """Đáp án từng bước. Lần rút thứ nhất, bốn mươi không vượt một trăm, nên số dư thành sáu mươi.
           Lần rút thứ hai, chín mươi lớn hơn sáu mươi nên hàm ném, lời nhắn thiếu ba mươi, và phép gán không xảy ra.
           Chữ A bị bỏ qua, khối bắt in B thiếu ba mươi. Khối cuối cùng in C sáu mươi."""),
        st(out_block(quiz),
           """Chạy thật, đúng hai dòng. Nếu bạn đoán C mười, hãy nhớ phép gán chỉ xảy ra khi hàm trả về bình thường."""),
    ], checks=["100 - 40 == 60", "90 - 60 == 30", "90 > 100 - 40"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("phát hiện sai → ném ngoại lệ", "đi ngược đường gọi", "khối bắt gần nhất đúng loại", "khối cuối cùng chạy khi rời khối thử"),
           """Tổng kết chuỗi logic. Phương thức phát hiện điều sai thì ném ngoại lệ. Ngoại lệ đi ngược đường gọi,
           tới khối bắt gần nhất đúng loại. Và khối cuối cùng chạy mỗi khi rời khối thử, có lỗi hay không."""),
        st("""<div class='box key'><b>Tư duy:</b> lỗi nghiệp vụ người gọi phải xử lý (không đủ tiền) dùng ngoại lệ <b>có kiểm tra</b> tự định nghĩa.
Chỉ bắt loại mình xử lý được; không để khối bắt rỗng. Gặp dấu vết thì đọc <b>từ trên xuống</b>: dòng đầu là nơi lỗi xảy ra.</div>""",
           """Điều cần mang theo. Lỗi nghiệp vụ mà người gọi phải xử lý, như không đủ tiền, nên là ngoại lệ có kiểm tra tự định nghĩa.
           Chỉ bắt loại mình xử lý được, và đừng để khối bắt rỗng. Gặp dấu vết thì đọc từ trên xuống, dòng đầu là nơi lỗi xảy ra."""),
    ])
    return lesson("L10", "ngoai_le", "Bài 10 — Ngoại lệ: ném, bắt và đọc dấu vết lỗi",
                  "curriculum/jva.yaml L10; audit/jva/verify_jva.py L10 (javac/java chạy thật); The Java Language Specification, Java SE 21 "
                  "(§11.1.1 ngoại lệ có kiểm tra và không kiểm tra, §11.2 kiểm tra lúc biên dịch, §14.18 lệnh throw, §14.20 lệnh try, "
                  "§14.20.2 try–finally, §14.20.3 try-với-tài-nguyên, §15.17.2 chia số nguyên cho 0); Java SE 21 API: java.lang.Throwable "
                  "(getMessage, printStackTrace), java.lang.AutoCloseable; dev.java/learn",
                  ["Viết và đọc khối thử, bắt, cuối cùng; dự đoán thứ tự in", "Ném ngoại lệ tự định nghĩa khi rút quá số dư",
                   "Phân biệt ngoại lệ có kiểm tra và không kiểm tra", "Đọc dấu vết ngăn xếp để tìm đúng lệnh gây lỗi"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
