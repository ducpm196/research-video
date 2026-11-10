from lib import *


def ln(p, s):
    """Số thứ tự (tính từ 1) của dòng đầu tiên trong mã của p có chứa s."""
    for i, l in enumerate(p["code"].split("\n"), 1):
        if s in l:
            return i
    raise ValueError(s)


# Lớp tài khoản dùng chung cho các chương trình của bài (đặt cùng tệp với lớp công khai có hàm chính)
TK = """class TaiKhoan {
    private String chu;                  // tên chủ tài khoản
    private long soDu;                   // bất biến: soDu luôn >= 0

    TaiKhoan(String chu) {               // hàm tạo: mở tài khoản, số dư 0
        this.chu = chu;
        this.soDu = 0;
    }

    void nap(long soTien) {
        if (soTien > 0) {
            soDu += soTien;
        } else {
            System.out.println("Tu choi nap " + soTien);
        }
    }

    boolean rut(long soTien) {
        if (soTien <= 0 || soTien > soDu) {
            System.out.println("Tu choi rut " + soTien + ", so du " + soDu);
            return false;
        }
        soDu -= soTien;
        return true;
    }

    long laySoDu() {
        return soDu;
    }

    public String toString() {
        return chu + ": " + soDu + " dong";
    }
}
"""


def build():
    ngan = prog("Ngan", TK + """
public class Ngan {
    public static void main(String[] args) {
        TaiKhoan an = new TaiKhoan("An");
        TaiKhoan binh = new TaiKhoan("Binh");
        an.nap(1000000);                     // (1)
        binh.nap(300000);                    // (2)
        an.rut(400000);                      // (3)
        boolean ok = binh.rut(500000);       // (4) quá số dư
        System.out.println(an);              // (5)
        System.out.println(binh + ", rut duoc: " + ok);
    }
}""", out="Tu choi rut 500000, so du 300000\nAn: 600000 dong\nBinh: 300000 dong, rut duoc: false")
    kiem = prog("KiemTk", TK + """
public class KiemTk {
    public static void main(String[] args) {
        TaiKhoan an = new TaiKhoan("An");
        TaiKhoan binh = new TaiKhoan("Binh");
        long vao = 0;                        // tổng tiền nạp thành công
        long ra = 0;                         // tổng tiền rút thành công
        an.nap(1000000);    vao += 1000000;
        binh.nap(300000);   vao += 300000;
        if (an.rut(400000)) { ra += 400000; }
        if (binh.rut(500000)) { ra += 500000; }
        long tong = an.laySoDu() + binh.laySoDu();
        System.out.println(tong + " = " + (vao - ra) + "? " + (tong == vao - ra));
        System.out.println("Khong am: " + (an.laySoDu() >= 0 && binh.laySoDu() >= 0));
    }
}""", out="Tu choi rut 500000, so du 300000\n900000 = 900000? true\nKhong am: true")
    quen_this = prog("QuenThis", """
class TaiKhoan {
    private String chu;

    TaiKhoan(String chu) {
        chu = chu;                       // SAI: gán tham số cho chính nó
    }

    public String toString() {
        return "Chu: " + chu;
    }
}

public class QuenThis {
    public static void main(String[] args) {
        System.out.println(new TaiKhoan("An"));
    }
}""", out="Chu: null")
    chung = prog("Chung", """
class TaiKhoan {
    private String chu;
    private static long soDu;            // SAI: một biến chung cho cả lớp
    TaiKhoan(String chu) { this.chu = chu; }
    void nap(long soTien) { soDu += soTien; }
    public String toString() { return chu + ": " + soDu + " dong"; }
}

public class Chung {
    public static void main(String[] args) {
        TaiKhoan an = new TaiKhoan("An");
        TaiKhoan binh = new TaiKhoan("Binh");
        an.nap(1000000);                 // chỉ nạp vào tài khoản của An
        System.out.println(binh);
    }
}""", out="Binh: 1000000 dong")
    cong_khai = prog("CongKhai", """
class TaiKhoan {
    public long soDu;                    // SAI: ai cũng sửa được
}

public class CongKhai {
    public static void main(String[] args) {
        TaiKhoan an = new TaiKhoan();
        an.soDu = -500000;               // không qua rut, không bị kiểm
        System.out.println(an.soDu);
    }
}""", out="-500000")
    rieng = prog("RiengTu", """
class TaiKhoan {
    private long soDu;                   // ĐÚNG: chỉ mã trong lớp được sửa
}

public class RiengTu {
    public static void main(String[] args) {
        TaiKhoan an = new TaiKhoan();
        an.soDu = -500000;
    }
}""", expect="compile_error:soDu has private access in TaiKhoan")
    quiz = prog("DoanTk", TK + """
public class DoanTk {
    public static void main(String[] args) {
        TaiKhoan c = new TaiKhoan("Cuc");
        c.nap(500000);
        c.rut(200000);
        c.rut(400000);
        c.nap(-100);
        TaiKhoan d = c;
        d.rut(100000);
        System.out.println(c);
    }
}""", out="Tu choi rut 400000, so du 300000\nTu choi nap -100\nCuc: 200000 dong")

    f2, f5 = ln(ngan, "private String chu"), ln(ngan, "TaiKhoan(String chu)")
    f10, f18 = ln(ngan, "void nap"), ln(ngan, "boolean rut")
    f31 = ln(ngan, "public String toString")
    m3 = ln(ngan, 'new TaiKhoan("An")')
    sc_hook = sc("hook", "hook", "Ai giữ cho số dư không bao giờ âm?", [
        st("""<p>Với mảng, số dư nằm trong một mảng, tên chủ tài khoản nằm trong mảng khác, và <b>dòng mã nào cũng gán được</b> <code>soDu[2] = -500000</code>.</p>
<div class="box warn">Một lệnh gán sai ở đâu đó trong một triệu dòng mã là đủ tạo ra số dư âm.</div>""",
           """Với mảng, số dư và tên chủ tài khoản nằm ở hai mảng khác nhau, và dòng mã nào cũng gán được một số âm vào ô số dư.
           Chỉ cần một lệnh gán sai trong một triệu dòng mã là có số dư âm."""),
        st("""<p>Hôm nay ta học <b>lớp</b> và <b>đối tượng</b>: gói dữ liệu cùng <b>luật</b> của nó vào một chỗ, và khoá dữ liệu lại.</p>
<div class="box key">Luật “số dư không bao giờ âm” được viết đúng một lần, bên trong lớp tài khoản.</div>
<span class='note'>Một điều phải luôn đúng với dữ liệu, như “số dư ≥ 0”, người lập trình gọi là <b>bất biến</b>.</span>""",
           """Hôm nay ta học lớp và đối tượng. Ta gói dữ liệu cùng luật của nó vào một chỗ, rồi khoá dữ liệu lại.
           Luật số dư không bao giờ âm khi đó được viết đúng một lần, bên trong lớp tài khoản.
           Một điều phải luôn đúng với dữ liệu như vậy, người lập trình gọi là bất biến."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng hôm nay", [
        st(table(["đã học", "viết", "dùng lại hôm nay"],
                 [["① hàm có tham số và giá trị trả về", "<code>static long tinhPhi(long soTien)</code>", "hàm nạp, hàm rút"],
                  ["② từ khoá tạo mới, biến giữ tham chiếu", "<code>long[] a = new long[5];</code>", "tạo đối tượng tài khoản"],
                  ["③ chuỗi chữ và phép nối", "<code>\"So du: \" + soDu</code>", "mô tả tài khoản thành một dòng chữ"]]),
           """Trước hết ta ôn lại ba điều. Thứ nhất, hàm có tham số, kiểu trả về và lệnh trả về.
           Thứ hai, từ khoá tạo mới xin bộ nhớ cho một mảng, và biến chỉ giữ tham chiếu tới nó.
           Thứ ba, chuỗi chữ đặt trong nháy kép, và dấu cộng nối chuỗi với số.""", focus=[1, "1.2", "1.3", "1.4"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ký hiệu của lớp và đối tượng", [
        st(code_block(ngan, lines=(1, f5 + 3), title="Lớp tài khoản: trường và hàm tạo")
           + code_block(ngan, lines=(m3, m3 + 2))
           + "<span class='note'>Một tệp chứa được nhiều lớp, nhưng chỉ <b>một</b> lớp <code>public</code>, trùng tên tệp: "
             "ở đây là lớp <code>Ngan</code> có hàm chính, tệp <code>Ngan.java</code>.</span>",
           """Đây là phần đầu của lớp tài khoản, gồm hai trường dữ liệu và một hàm tạo.
           Bên dưới, hàm chính tạo hai đối tượng tài khoản và nạp tiền vào một tài khoản.
           Hai lớp nằm chung một tệp được, miễn là chỉ một lớp công khai, và tên tệp trùng tên lớp công khai đó.""", focus=[2, 3, 4]),
        st(table(["viết", "nghĩa"],
                 [["<code>class TaiKhoan { … }</code>", "<b>lớp</b>: bản thiết kế gồm dữ liệu và hành vi"],
                  ["<code>private long soDu;</code>", "<b>trường</b>: mỗi đối tượng có một bản riêng; <code>private</code> = chỉ mã trong lớp được đụng vào"],
                  ["<code>TaiKhoan(String chu)</code>", "<b>hàm tạo</b>: trùng tên lớp, không có kiểu trả về, chạy khi <code>new</code>"],
                  ["<code>this.chu = chu;</code>", "<code>this</code> là chính đối tượng này: trường <code>this.chu</code> nhận tham số <code>chu</code>"],
                  ["<code>new TaiKhoan(\"An\")</code>", "tạo một <b>đối tượng</b> mới, trả về tham chiếu tới nó"],
                  ["<code>an.nap(1000000)</code>", "gọi hàm của <b>đúng</b> đối tượng <code>an</code>; không có <code>static</code>"],
                  ["<code>public String toString()</code>", "trả về dòng chữ mô tả; lệnh in tự gọi khi in một đối tượng"]]),
           """Lớp là bản thiết kế, gồm dữ liệu và hành vi đi kèm.
           Trường là dữ liệu mỗi đối tượng có một bản riêng, còn từ khoá riêng tư nghĩa là chỉ mã trong lớp được đụng vào.
           Hàm tạo trùng tên lớp, không có kiểu trả về, và chạy mỗi khi tạo đối tượng.
           Từ khoá chỉ chính đối tượng này phân biệt trường với tham số trùng tên.
           Từ khoá tạo mới dựng một đối tượng, rồi trả về tham chiếu tới nó.
           Gọi hàm qua tên đối tượng và dấu chấm thì hàm làm việc trên đúng đối tượng đó, nên không có từ khoá tĩnh.
           Hàm đổi ra chuỗi trả về dòng mô tả, và lệnh in tự gọi nó.""", clear=True,
           focus=["1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: một bản thiết kế, nhiều đối tượng, dữ liệu sau cửa khoá", [
        st(svg(1500, 400,
               box(20, 110, 360, 190, ["lớp TaiKhoan", "trường: chu, soDu", "hàm: nap, rut, toString"], C_PURPLE, 24, True),
               arrow(385, 160, 690, 100, "#9333ea", "new"),
               arrow(385, 250, 690, 300, "#9333ea", "new"),
               box(700, 40, 380, 120, ["đối tượng 1", "chu = An", "soDu = 600000"], C_BLUE, 24, True),
               box(700, 240, 380, 120, ["đối tượng 2", "chu = Binh", "soDu = 300000"], C_BLUE, 24, True),
               box(1260, 55, 200, 90, ["biến an"], C_AMBER, 24),
               box(1260, 255, 200, 90, ["biến binh"], C_AMBER, 24),
               arrow(1255, 100, 1090, 100, "#d97706"),
               arrow(1255, 300, 1090, 300, "#d97706")),
           """Hãy hình dung lớp như bản thiết kế một cuốn sổ tài khoản. Mỗi lần dùng từ khoá tạo mới, máy làm ra một cuốn sổ thật, gọi là một đối tượng.
           Hai đối tượng có trường riêng, nên số dư của An và của Bình nằm ở hai chỗ khác nhau.
           Biến an và biến bình chỉ giữ tham chiếu tới từng cuốn sổ, giống biến mảng."""),
        st(svg(1500, 400,
               panel(560, 30, 420, 340, "đối tượng tài khoản", C_BLUE),
               box(640, 120, 260, 170, ["soDu (riêng tư)", "luôn ≥ 0"], C_GREEN, 24, True),
               arrow(245, 160, 630, 160, "#16a34a", "nap(x): x > 0 ?"),
               arrow(245, 260, 630, 260, "#16a34a", "rut(x): x ≤ soDu ?"),
               box(20, 120, 220, 80, ["nạp tiền"], C_GRAY, 24),
               box(20, 220, 220, 80, ["rút tiền"], C_GRAY, 24),
               box(1080, 160, 400, 90, ["an.soDu = -500000", "lỗi biên dịch"], C_RED, 24, True, dash=True),
               txt(1280, 300, "không có đường vào thứ ba", 24, "middle", "#dc2626", True)),
           """Hình thứ hai cho thấy vì sao luật được giữ. Trường số dư là riêng tư, nên từ bên ngoài chỉ có hai cánh cửa là hàm nạp và hàm rút.
           Mỗi cửa kiểm tra trước khi đổi số dư: nạp phải là số dương, rút không được quá số dư.
           Lệnh gán thẳng từ bên ngoài bị trình biên dịch chặn, nên không có đường vào thứ ba."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: dựng lớp tài khoản giữ luật số dư không âm", [
        st("<p><b>Bước 1. Trường riêng tư.</b> Chỉ mã trong lớp được đổi <code>soDu</code>.</p>" + code_block(ngan, lines=(f2, f2 + 1)),
           """Bước một, khai hai trường riêng tư. Vì chỉ mã bên trong lớp đổi được số dư, nên muốn giữ luật, ta chỉ cần kiểm tra mã trong lớp này."""),
        st("<p><b>Bước 2. Hàm tạo đặt trạng thái ban đầu hợp lệ.</b></p>" + code_block(ngan, lines=(f5, f5 + 3))
           + "<span class='note'>Mới mở: soDu = 0, nên luật “không âm” đúng ngay từ đầu.</span>",
           """Bước hai, viết hàm tạo. Tài khoản mới mở có số dư bằng không, nên luật không âm đúng ngay từ lúc tạo.
           Từ khoá chỉ chính đối tượng này cho biết vế trái là trường, còn vế phải là tham số."""),
        st("<p><b>Bước 3. Hàm nạp chỉ nhận số dương.</b></p>" + code_block(ngan, lines=(f10, f10 + 6)),
           """Bước ba, hàm nạp chỉ cộng khi số tiền lớn hơn không. Cộng một số dương vào số không âm thì vẫn không âm, nên luật vẫn đúng.
           Số không dương thì bị từ chối kèm thông báo."""),
        st("<p><b>Bước 4. Hàm rút từ chối khi rút quá số dư.</b></p>" + code_block(ngan, lines=(f18, f18 + 7)),
           """Bước bốn, hàm rút từ chối khi số tiền không dương hoặc lớn hơn số dư, và trả về sai.
           Nếu qua được phép kiểm, số tiền rút không lớn hơn số dư, nên số dư sau khi trừ vẫn lớn hơn hoặc bằng không."""),
        st("<p><b>Bước 5. Hàm đọc số dư và hàm mô tả.</b></p>" + code_block(ngan, lines=(f31 - 4, f31 + 2)),
           """Bước năm, thêm hàm đọc số dư để bên ngoài xem được mà không sửa được, và hàm đổi ra chuỗi để in tài khoản.
           Hàm đổi ra chuỗi phải có từ khoá công khai, vì mọi đối tượng Java đã có sẵn một hàm cùng tên ở dạng công khai, và bản ta viết lại không được hẹp quyền hơn."""),
    ], checks=["all(s + x >= 0 for s in [0, 300000] for x in [1, 500000])",
               "all(s - x >= 0 for s in [0, 300000, 600000] for x in range(1, s + 1, 100000))"])
    m5 = ln(ngan, "an.nap(1000000)")
    sc_ex = sc("example", "example", "Ví dụ: hai tài khoản độc lập, từng phép tính", [
        st(code_block(ngan, lines=(m3, m3 + 7), title="Tệp Ngan.java: hàm chính"),
           """Hàm chính tạo hai tài khoản cho An và Bình, rồi làm bốn thao tác và in kết quả. Ta lần từng thao tác, với số dư ban đầu đều bằng không."""),
        st(code_block(ngan, lines=(m5, m5 + 1))
           + "$$① \\; \\text{an: } 0 + 1000000 = \\hl{1000000} \\qquad ② \\; \\text{binh: } 0 + 300000 = \\hl{300000}$$",
           """Phép tính thứ nhất, nạp một triệu, số dư của An thành một triệu.
           Phép tính thứ hai, nạp ba trăm nghìn cho Bình. Vì hai đối tượng có trường riêng, nên số dư của An không bị ảnh hưởng."""),
        st(code_block(ngan, lines=(m5 + 2, m5 + 2))
           + "$$③ \\; 400000 \\le 1000000 \\to \\text{an: } 1000000 - 400000 = \\hl{600000}$$",
           """Phép tính thứ ba, An rút bốn trăm nghìn. Vì bốn trăm nghìn không lớn hơn một triệu, nên lệnh rút được chấp nhận, số dư của An còn sáu trăm nghìn."""),
        st(code_block(ngan, lines=(m5 + 3, m5 + 3))
           + "$$④ \\; 500000 > 300000 \\to \\text{từ chối, binh giữ } \\hl{300000}, \\; \\text{ok} = \\text{false}$$",
           """Phép tính thứ tư, Bình rút năm trăm nghìn, nhiều hơn số dư ba trăm nghìn.
           Hàm rút in thông báo từ chối, không trừ đồng nào, và trả về sai."""),
        st(code_block(ngan, lines=(m5 + 4, m5 + 5)) + out_block(ngan),
           """Phép tính thứ năm, in hai tài khoản, lệnh in tự gọi hàm đổi ra chuỗi.
           Chạy thật, dòng đầu là thông báo từ chối, rồi An sáu trăm nghìn, Bình ba trăm nghìn kèm chữ sai.""",
           focus=[1, ["3.1", "3.2", "3.3"]]),
    ], checks=["0 + 1000000 == 1000000", "0 + 300000 == 300000", "400000 <= 1000000 and 1000000 - 400000 == 600000",
               "500000 > 300000"])
    k5 = ln(kiem, "long vao = 0")
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: tiền vào trừ tiền ra bằng tổng số dư", [
        st("<p>Đường khác: không nhìn từng tài khoản, chỉ ghi sổ <b>tiền vào</b> và <b>tiền ra</b> thành công.</p>"
           "$$(1000000 + 300000) - 400000 = 900000 = 600000 + 300000$$",
           """Ta kiểm bằng đường khác: không nhìn từng tài khoản, chỉ ghi sổ tiền vào và tiền ra thành công.
           Tiền vào là một triệu ba trăm nghìn, tiền ra chỉ có bốn trăm nghìn vì lệnh rút của Bình bị từ chối, nên tổng phải là chín trăm nghìn."""),
        st(code_block(kiem, lines=(k5, k5 + 8), title="Tệp KiemTk.java: ghi sổ ngay cạnh mỗi thao tác"),
           """Chương trình kiểm ghi sổ ngay cạnh mỗi thao tác, và chỉ cộng tiền ra khi hàm rút trả về đúng, vì lệnh rút bị từ chối không lấy đi đồng nào.
           Cuối cùng nó so tổng số dư với tiền vào trừ tiền ra, và kiểm cả hai số dư không âm."""),
        st(out_block(kiem),
           """Chạy thật, hai vế cùng là chín trăm nghìn và phép so ra đúng, nên không đồng nào bị tạo ra hay mất đi.
           Dòng cuối xác nhận luật không âm vẫn giữ sau mọi thao tác.""", focus=["2.2", "2.3"]),
    ], checks=["(1000000 + 300000) - 400000 == 600000 + 300000 == 900000"])
    c3 = ln(chung, "private static")
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Quên <code>this.</code> khi tham số trùng tên trường.</div>'
           + code_block(quen_this, lines=(4, 10)) + out_block(quen_this)
           + "<span class='note'><code>null</code> là <b>giá trị rỗng</b>: biến chưa trỏ tới đối tượng nào. "
             "Trường kiểu chuỗi chưa được gán thì mặc định là <code>null</code>.</span>",
           """Lỗi thứ nhất, của người mới, là quên từ khoá chỉ đối tượng này khi tham số trùng tên trường.
           Dòng gán chỉ gán tham số cho chính nó, nên trường tên chủ giữ giá trị rỗng mặc định.
           Giá trị rỗng nghĩa là biến chưa trỏ tới đối tượng nào, và trường kiểu chuỗi chưa gán thì mặc định như vậy.""",
           focus=[1, [2, 4], 5]),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Nhầm <code>static</code> với trường riêng của mỗi đối tượng.</div>'
           + code_block(chung, lines=(c3, c3 + 2)) + code_block(chung, lines=(ln(chung, "an.nap"), ln(chung, "an.nap") + 1))
           + out_block(chung),
           """Lỗi thứ hai gặp cả ở người đã đi làm: thêm từ khoá tĩnh vào trường số dư.
           Trường tĩnh thuộc về lớp, chỉ có một bản dùng chung cho mọi đối tượng.
           Vì vậy nạp một triệu cho An, mà in tài khoản Bình cũng thấy một triệu.""", focus=[2, 2, [3, 5]]),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Để trường <code>public</code> cho tiện.</div>'
           + code_block(cong_khai, lines=(1, 3)) + code_block(cong_khai, lines=(8, 9)) + out_block(cong_khai)
           + "<span class='note'>Lớp không viết hàm tạo nào thì Java tự thêm một hàm tạo không tham số, nên "
             "<code>new TaiKhoan()</code> vẫn chạy.</span>",
           """Lỗi thứ ba cũng của người đã đi làm: để trường số dư công khai cho tiện.
           Khi đó một dòng mã bất kỳ gán thẳng âm năm trăm nghìn, không đi qua hàm rút, nên không có phép kiểm nào chạy.
           Để ý lớp này không viết hàm tạo nào, nên Java tự thêm một hàm tạo không tham số.""",
           focus=[1, [3, 5], 6]),
        st('<div class="box key"><b>Sửa:</b> trường <code>private</code>, trình biên dịch chặn ngay.</div>'
           + code_block(rieng, lines=(2, 2)) + code_block(rieng, lines=(8, 8)) + out_block(rieng, "Trình biên dịch báo"),
           """Cách sửa là để trường riêng tư. Lúc đó cùng dòng gán ấy bị trình biên dịch chặn, vì số dư là trường riêng tư của lớp tài khoản.
           Lỗi bị bắt trước khi chương trình kịp chạy.""", focus=[[1, 2], [3, 5], 5]),
    ])
    q3 = ln(quiz, 'new TaiKhoan("Cuc")')
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(q3, q3 + 7), title="Lớp TaiKhoan như trên. Đoán các dòng in ra"),
           """Bây giờ tới phần bạn tự làm, với lớp tài khoản như trên. Tài khoản của Cúc nạp năm trăm nghìn, rút hai trăm nghìn, rút bốn trăm nghìn, rồi nạp âm một trăm.
           Sau đó biến d được gán bằng biến c, rồi rút một trăm nghìn qua d. Hãy dừng video, viết ra giấy mọi dòng in ra.""", pause=20),
        st(table(["thao tác", "kiểm", "số dư", "in ra"],
                 [["nap(500000)", "500000 &gt; 0", "500000", ""],
                  ["rut(200000)", "200000 ≤ 500000", "300000", ""],
                  ["rut(400000)", "400000 &gt; 300000: từ chối", "300000", "Tu choi rut 400000, so du 300000"],
                  ["nap(-100)", "-100 không dương: từ chối", "300000", "Tu choi nap -100"],
                  ["d = c; d.rut(100000)", "cùng một đối tượng", "200000", ""]]),
           """Đáp án như sau. Sau khi nạp và rút lần đầu, số dư là ba trăm nghìn.
           Rút bốn trăm nghìn bị từ chối vì quá số dư, nên in dòng từ chối thứ nhất.
           Nạp âm một trăm bị từ chối vì không dương, nên in dòng thứ hai.
           Biến d trỏ vào cùng đối tượng với c, nên số dư của Cúc còn hai trăm nghìn.""",
           focus=[1, ["1.2", "1.3"], "1.4", "1.5", "1.6"]),
        st(out_block(quiz),
           """Chạy thật chương trình, ta được hai dòng từ chối, rồi dòng cuối là Cúc hai trăm nghìn đồng."""),
    ], checks=["500000 - 200000 == 300000", "400000 > 300000", "300000 - 100000 == 200000"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("lớp = bản thiết kế", "new tạo đối tượng có trường riêng", "trường private", "hàm kiểm luật trước khi đổi"),
           """Tổng kết chuỗi logic. Lớp là bản thiết kế, từ khoá tạo mới dựng đối tượng có trường riêng,
           trường được khoá riêng tư, và chỉ các hàm của lớp, sau khi kiểm luật, mới được đổi dữ liệu."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi viết lớp, hãy viết ra <b>luật</b> của nó, ví dụ “số dư không bao giờ âm”.
Rồi kiểm: mọi đường đổi dữ liệu có đi qua phép kiểm luật không? Trường <code>public</code> hay <code>static</code> nhầm chỗ là đường vào thứ ba.</div>""",
           """Điều cần mang theo. Trước khi viết một lớp, hãy viết ra luật của nó, ví dụ số dư không bao giờ âm.
           Rồi kiểm xem mọi đường đổi dữ liệu có đi qua phép kiểm luật không. Trường công khai, hay trường tĩnh nhầm chỗ, là đường vào thứ ba."""),
    ])
    return lesson("L07", "lop_doi_tuong", "Bài 7 — Lớp và đối tượng: tài khoản tự giữ luật của mình",
                  "curriculum/jva.yaml L07; audit/jva/verify_jva.py L07 (javac/java chạy thật); The Java Language Specification, "
                  "Java SE 21 (JLS §8.1 khai báo lớp, §8.3 trường và §8.3.1.1 trường static, §8.8 hàm tạo, §15.8.3 this, "
                  "§6.6 kiểm soát truy cập private, §6.4.1 che khuất tên, §4.12.5 giá trị mặc định null, §15.9 new; "
                  "Object.toString, Java SE 21 API); dev.java/learn",
                  ["Khai báo lớp có trường riêng tư, hàm tạo, các hàm của đối tượng (nạp, rút) và hàm đổi ra chuỗi",
                   "Tạo nhiều đối tượng độc lập bằng từ khoá tạo mới và gọi hàm trên từng đối tượng",
                   "Giữ bất biến số dư không âm bằng cách kiểm trong hàm nạp, hàm rút",
                   "Nhận ra lỗi quên this, trường static dùng chung, trường public phá bất biến"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
