from lib import *

# Sổ chuyển khoản nhỏ: ghép lớp (bất biến), bản ghi, bản đồ, danh sách, ngoại lệ. Các biến thể (đúng, lỗi cố ý, sửa sai cách)
# được ghép từ cùng các mảnh dưới đây, nên số dòng trong dấu vết lỗi được TÍNH từ mã (lnc) chứ không gõ tay.
TYPES = """
import java.util.ArrayList;
import java.util.HashMap;

class KhongDuTien extends Exception {
    KhongDuTien(String thongBao) { super(thongBao); }
}

record Lenh(String tu, String den, long tien) {}
"""

SO_CAI = """
class SoCai {
    private HashMap<String, Long> soDu = new HashMap<>();
    private long tongGoc = 0;

    void mo(String stk, long tien) {
        soDu.put(stk, tien);
        tongGoc += tien;                      // tổng tiền phải giữ mãi
    }

    long tong() {
        long t = 0;
        for (long x : soDu.values()) {
            t += x;
        }
        return t;
    }

    long lay(String stk) {
        Long v = soDu.get(stk);
        if (v == null) {
            throw new IllegalArgumentException("Khong co tai khoan " + stk);
        }
        return v;
    }

    void chuyen(Lenh l) throws KhongDuTien {
        long a = lay(l.tu());                 // kiểm tra trước ...
        long b = lay(l.den());
        if (l.tien() <= 0) {
            throw new IllegalArgumentException("So tien phai duong");
        }
        if (l.tien() > a) {
            throw new KhongDuTien(l.tu() + " chi co " + a);
        }
        soDu.put(l.tu(), a - l.tien());       // ... sửa sau: trừ bên gửi
        soDu.put(l.den(), b + l.tien());      // cộng bên nhận
        kiem();                               // kiểm bất biến sau MỖI lần chuyển
    }

    void kiem() {
        if (tong() != tongGoc) {
            throw new IllegalStateException("Lech tong " + tong() + " != " + tongGoc);
        }
    }
}
"""

MO = """
        SoCai so = new SoCai();
        so.mo("A", 1000000);
        so.mo("B", 500000);
        so.mo("C", 1500000);
        ArrayList<Lenh> ds = new ArrayList<>();"""

LENH = """
        ds.add(new Lenh("A", "B", 300000));
        ds.add(new Lenh("B", "C", 1000000));
        ds.add(new Lenh("A", "X", 50000));
        ds.add(new Lenh("C", "A", 200000));"""

VONG = """
        for (Lenh l : ds) {
            try {
                so.chuyen(l);
                System.out.println("OK " + l);
            } catch (KhongDuTien e) {
                System.out.println("TU CHOI " + e.getMessage());
            } catch (IllegalArgumentException e) {
                System.out.println("SAI LENH " + e.getMessage());
            }
        }"""

IN = """
        System.out.println("A=" + so.lay("A") + " B=" + so.lay("B") + " C=" + so.lay("C"));
        System.out.println("Tong " + so.tong());"""

BUG = ("soDu.put(l.den(), b + l.tien());      // cộng bên nhận",
       "soDu.put(l.den(), a + l.tien());      // cộng bên nhận")


def ledger(name, so_cai=SO_CAI, lenh=LENH, vong=VONG, tail=IN):
    main = f"\npublic class {name} {{\n    public static void main(String[] args) {{" + MO + lenh + vong + tail + "\n    }\n}"
    return (TYPES + so_cai + main).strip("\n")


def lnc(code, s, after=None):
    """Số dòng (từ 1) đầu tiên chứa s; after: chỉ tìm sau dòng chứa chuỗi này."""
    lines = code.split("\n")
    start = 0 if after is None else next(i for i, l in enumerate(lines) if after in l) + 1
    return next(i for i, l in enumerate(lines[start:], start + 1) if s in l)


def ln(p, s, after=None):
    return lnc(p["code"], s, after)


def build():
    so = prog("So", ledger("So"), out="OK Lenh[tu=A, den=B, tien=300000]\nTU CHOI B chi co 800000\nSAI LENH Khong co tai khoan X\n"
                                       "OK Lenh[tu=C, den=A, tien=200000]\nA=900000 B=800000 C=1300000\nTong 3000000")
    c_loi = ledger("SoLoi", so_cai=SO_CAI.replace(*BUG))
    so_loi = prog("SoLoi", c_loi, out="", expect="runtime_error:IllegalStateException",
                  err='Exception in thread "main" java.lang.IllegalStateException: Lech tong 3500000 != 3000000\n'
                      f'\tat SoCai.kiem(SoLoi.java:{lnc(c_loi, "throw new IllegalStateException")})\n'
                      f'\tat SoCai.chuyen(SoLoi.java:{lnc(c_loi, "kiem();")})\n'
                      f'\tat SoLoi.main(SoLoi.java:{lnc(c_loi, "so.chuyen(l);")})')
    nuot = prog("Nuot", ledger("Nuot", so_cai=SO_CAI.replace(*BUG), vong=VONG.replace(
        """                System.out.println("SAI LENH " + e.getMessage());
            }""",
        """                System.out.println("SAI LENH " + e.getMessage());
            } catch (Exception e) {
                // tạm bỏ qua cho chương trình khỏi dừng
            }""")), out="SAI LENH Khong co tai khoan X\nA=2500000 B=300000 C=2100000\nTong 4900000")
    c_cuoi = ledger("CuoiNgay", so_cai=SO_CAI.replace(*BUG).replace(
        "        kiem();                               // kiểm bất biến sau MỖI lần chuyển\n", ""),
        tail=IN + "\n        so.kiem();                            // chỉ đối soát cuối ngày")
    cuoi = prog("CuoiNgay", c_cuoi, out="OK Lenh[tu=A, den=B, tien=300000]\nOK Lenh[tu=B, den=C, tien=1000000]\n"
                                        "SAI LENH Khong co tai khoan X\nOK Lenh[tu=C, den=A, tien=200000]\n"
                                        "A=2500000 B=300000 C=2100000\nTong 4900000",
                expect="runtime_error:IllegalStateException",
                err='Exception in thread "main" java.lang.IllegalStateException: Lech tong 4900000 != 3000000\n'
                    f'\tat SoCai.kiem(CuoiNgay.java:{lnc(c_cuoi, "throw new IllegalStateException")})\n'
                    f'\tat CuoiNgay.main(CuoiNgay.java:{lnc(c_cuoi, "so.kiem();")})')
    quiz = prog("DoanKetQua", ledger("DoanKetQua", lenh="""
        ds.add(new Lenh("B", "A", 600000));
        ds.add(new Lenh("C", "B", 0));
        ds.add(new Lenh("A", "C", 1000000));"""),
                out="TU CHOI B chi co 500000\nSAI LENH So tien phai duong\nOK Lenh[tu=A, den=C, tien=1000000]\n"
                    "A=0 B=500000 C=2500000\nTong 3000000")

    l_cls = ln(so, "class SoCai")
    l_tong = ln(so, "long tong()")
    l_lay_end = ln(so, "return v;") + 1
    l_ch = ln(so, "void chuyen")
    l_tru = ln(so, "trừ bên gửi")
    l_kiem_end = ln(so, "void kiem()") + 4
    l_main = ln(so, "SoCai so = new SoCai()")
    l_for = ln(so, "for (Lenh l : ds)")
    l_bug = ln(so_loi, "a + l.tien()")
    sc_hook = sc("hook", "hook", "Tình huống: viết sổ chuyển khoản mà tiền không tự sinh, không tự mất", [
        st("""<p>Bạn được giao viết một <b>sổ chuyển khoản</b> nhỏ cho ba tài khoản A, B, C. Yêu cầu quan trọng nhất của mọi sổ ngân hàng:</p>
<div class="box key">Chuyển tiền chỉ <b>dời</b> tiền từ chỗ này sang chỗ khác: <b>tổng tiền trước = tổng tiền sau</b>, sau MỌI lệnh.</div>""",
           """Hôm nay là tình huống chuyên gia. Bạn được giao viết một sổ chuyển khoản nhỏ cho ba tài khoản A, B, C.
           Yêu cầu quan trọng nhất của mọi sổ ngân hàng là chuyển tiền chỉ dời tiền từ chỗ này sang chỗ khác.
           Nghĩa là tổng tiền trước và sau mọi lệnh phải bằng nhau."""),
        st(chain("viết sổ", "chạy bốn lệnh", "kiểm bất biến tổng tiền", "gài một lỗi", "đọc dấu vết, sửa tận gốc"),
           """Ta đi trọn một vòng như người làm thật: viết sổ, chạy bốn lệnh, kiểm bất biến tổng tiền.
           Rồi ta gài một lỗi đời thường, đọc dấu vết để tìm ra nó, và sửa tận gốc."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: ba công cụ sẽ ghép với nhau", [
        st(table(["đã học", "dùng vào sổ thế nào"],
                 [["① Lớp giữ bất biến; bản ghi", "lớp <code>SoCai</code> giấu số dư, chỉ cho sửa qua <code>chuyen</code>; lệnh chuyển là một bản ghi"],
                  ["② Bản đồ khoá → giá trị", "số tài khoản → số dư; <code>get</code> ra <code>null</code> khi không có khoá"],
                  ["③ Ngoại lệ và dấu vết", "không đủ tiền thì ném <code>KhongDuTien</code>; dấu vết đọc từ trên xuống"]]),
           """Ta ghép ba công cụ đã học. Thứ nhất, lớp giấu dữ liệu để giữ bất biến, và bản ghi để chở một lệnh chuyển.
           Thứ hai, bản đồ từ số tài khoản tới số dư, với phương thức lấy trả giá trị rỗng khi không có khoá.
           Thứ ba, ngoại lệ tự định nghĩa cho trường hợp không đủ tiền, và cách đọc dấu vết từ trên xuống."""),
        st(table(["khái niệm", "nghĩa bằng lời thường"],
                 [["bản ghi <code>record</code>", "kiểu chỉ để chở dữ liệu: khai báo các thành phần một lần, máy tự sinh phương thức lấy "
                   "từng thành phần (như <code>l.tu()</code>) và cách in <code>Lenh[tu=A, den=B, tien=300000]</code>"],
                  ["lớp bọc <code>Long</code>", "<code>long</code> là số nguyên thường, luôn có một giá trị; <code>Long</code> là một đối tượng "
                   "bọc một số <code>long</code>, nên có thể là <code>null</code>. Bản đồ chỉ chứa đối tượng nên dùng <code>Long</code>; "
                   "gán sang <code>long</code> thì máy tự lấy số ra, gặp <code>null</code> thì ném lỗi, nên phải kiểm <code>null</code> trước"],
                  ["<code>throws KhongDuTien</code>", "<code>KhongDuTien</code> kế thừa <code>Exception</code> nên là ngoại lệ <b>phải khai báo</b>: "
                   "phương thức có thể ném nó ghi <code>throws</code>, nơi gọi buộc phải bắt bằng <code>catch</code> hoặc khai <code>throws</code> để ném tiếp. "
                   "<code>IllegalArgumentException</code>, <code>IllegalStateException</code> là lỗi lúc chạy, không phải khai báo"]]),
           """Nhắc lại ba khái niệm sẽ gặp trong mã.
           Bản ghi là kiểu chỉ để chở dữ liệu, ta khai báo các thành phần một lần, và máy tự sinh phương thức lấy từng thành phần cùng cách in ra.
           Kiểu số nguyên thường luôn có một giá trị, còn lớp bọc của nó là một đối tượng chứa một số, nên có thể là giá trị rỗng.
           Bản đồ chỉ chứa đối tượng nên dùng lớp bọc, và phải kiểm giá trị rỗng trước khi lấy số ra, nếu không chương trình sẽ ném lỗi.
           Ngoại lệ không đủ tiền thuộc loại phải khai báo, nên phương thức chuyển ghi rõ là có thể ném nó, và nơi gọi buộc phải bắt, hoặc khai báo ném tiếp.
           Hai ngoại lệ đối số sai và trạng thái sai thuộc loại lỗi lúc chạy, nên không phải khai báo.""", clear=True),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã thiết kế: các phần của sổ", [
        st(code_block(so, lines=(ln(so, "class KhongDuTien"), ln(so, "record Lenh")), title="Hai kiểu dữ liệu đầu tệp") + table(["phần", "việc"],
                 [["<code>mo(stk, tien)</code>", "mở tài khoản, cộng vào <code>tongGoc</code>"],
                  ["<code>tong()</code>, <code>lay(stk)</code>", "cộng mọi số dư; lấy một số dư (không có thì ném)"],
                  ["<code>chuyen(l)</code>", "kiểm tra, trừ bên gửi, cộng bên nhận, rồi <code>kiem()</code>"],
                  ["<code>kiem()</code>", "tổng khác <code>tongGoc</code> thì ném <code>IllegalStateException</code>"]]),
           """Đầu tệp có loại ngoại lệ không đủ tiền và bản ghi lệnh gồm tài khoản gửi, tài khoản nhận, số tiền.
           Lớp sổ cái có bốn việc. Mở tài khoản thì cộng vào tổng gốc.
           Phương thức tổng cộng mọi số dư, còn phương thức lấy trả một số dư, và ném ngoại lệ nếu không có tài khoản.
           Phương thức chuyển kiểm tra, trừ, cộng, rồi gọi phương thức kiểm.
           Phương thức kiểm ném ngoại lệ trạng thái sai nếu tổng lệch tổng gốc, vì đó là lỗi lập trình."""),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: một lần chuyển là hai bút toán, tổng không đổi", [
        st(svg(1500, 400,
               panel(20, 20, 640, 360, "trước lệnh A → B 300000", C_GRAY),
               box(50, 90, 180, 90, ["A", "1000000"], C_BLUE, 22, bold=True), box(250, 90, 180, 90, ["B", "500000"], C_BLUE, 22, bold=True),
               box(450, 90, 180, 90, ["C", "1500000"], C_BLUE, 22, bold=True),
               box(140, 250, 400, 90, ["tổng", "3000000"], C_GREEN, 24, bold=True),
               arrow(670, 200, 820, 200, "#d97706", "chuyển"),
               panel(840, 20, 640, 360, "sau lệnh", C_GRAY),
               box(870, 90, 180, 90, ["A", "700000"], C_RED, 22, bold=True), box(1070, 90, 180, 90, ["B", "800000"], C_GREEN, 22, bold=True),
               box(1270, 90, 180, 90, ["C", "1500000"], C_BLUE, 22, bold=True),
               box(960, 250, 400, 90, ["tổng", "3000000"], C_GREEN, 24, bold=True)),
           """Hình này là một lệnh chuyển ba trăm nghìn từ A sang B. Trước lệnh, tổng ba tài khoản là ba triệu.
           Sau lệnh, A giảm ba trăm nghìn, B tăng ba trăm nghìn, C giữ nguyên, nên tổng vẫn là ba triệu."""),
        st(table(["bút toán", "thay đổi"], [["trừ bên gửi A", "$-300\\,000$"], ["cộng bên nhận B", "$+300\\,000$"],
                                            ["tổng thay đổi", "$-300\\,000 + 300\\,000 = \\hlg{0}$"]])
           + "<p>Hai quy tắc: <b>kiểm tra trước, sửa sau</b> (bị từ chối thì chưa chạm vào số dư nào), và <b>kiểm bất biến sau mỗi lệnh</b>.</p>",
           """Một lần chuyển gồm hai bút toán, tức hai dòng ghi tăng hoặc giảm số dư: trừ bên gửi và cộng bên nhận cùng một số tiền, nên tổng thay đổi bằng không.
           Từ đó có hai quy tắc. Kiểm tra trước, sửa sau, để lệnh bị từ chối không chạm vào số dư nào.
           Và kiểm bất biến sau mỗi lệnh, để lỗi lộ ra ngay tại lệnh gây ra nó.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: viết lớp sổ cái", [
        st(code_block(so, lines=(l_cls, l_cls + 8), title="Bước 1. Bản đồ số dư và tổng gốc"),
           """Bước một, sổ cái giữ một bản đồ riêng từ số tài khoản tới số dư, và một tổng gốc.
           Mỗi lần mở tài khoản, ta đặt số dư vào bản đồ và cộng vào tổng gốc, vì đó là tổng tiền phải giữ mãi."""),
        st(code_block(so, lines=(l_tong, l_tong + 6), title="Bước 2. Cộng tổng, và lấy số dư an toàn")
           + code_block(so, lines=(l_lay_end - 6, l_lay_end)),
           """Bước hai, phương thức tổng duyệt mọi giá trị của bản đồ và cộng dồn.
           Phương thức lấy dùng lớp bọc, vì bản đồ trả giá trị rỗng khi không có khoá, và khi đó ta ném ngoại lệ đối số."""),
        st(code_block(so, lines=(l_ch, l_tru - 1), title="Bước 3. Chuyển: kiểm tra trước"),
           """Bước ba, phương thức chuyển kiểm tra trước. Lấy số dư hai bên, nên tài khoản không có sẽ bị ném ngay.
           Số tiền phải dương, và không được vượt số dư bên gửi, nếu không thì ném ngoại lệ không đủ tiền.
           Đến đây chưa có số dư nào bị sửa."""),
        st(code_block(so, lines=(l_tru, l_kiem_end), title="Bước 4. Sửa sau, rồi kiểm bất biến"),
           """Bước bốn, qua hết kiểm tra mới sửa: trừ bên gửi, cộng bên nhận.
           Ngay sau đó gọi phương thức kiểm. Nếu tổng khác tổng gốc thì ném ngoại lệ trạng thái sai, vì bất biến đã vỡ."""),
        st(code_block(so, lines=(l_for, l_for + 9), title="Bước 5. Chạy danh sách lệnh"),
           """Bước năm, hàm chính duyệt danh sách lệnh. Mỗi lệnh đặt trong khối thử.
           Không đủ tiền thì in từ chối, lệnh sai thì in sai lệnh. Lỗi trạng thái thì không bắt, vì đó là lỗi lập trình phải lộ ra."""),
    ], checks=["1000000 + 500000 + 1500000 == 3000000"])
    sc_ex = sc("example", "example", "Ví dụ: chạy bốn lệnh, từng phép tính", [
        st(code_block(so, lines=(l_main, l_main + 8), title="Ba tài khoản và bốn lệnh"),
           """Ba tài khoản được mở với một triệu, năm trăm nghìn và một triệu rưỡi. Rồi có bốn lệnh chuyển. Ta tính từng bước."""),
        st("$$① \\; 1\\,000\\,000 + 500\\,000 + 1\\,500\\,000 = \\hl{3\\,000\\,000} \\text{ (tổng gốc)}$$"
           "$$② \\; \\text{A→B}: \\; A = 1\\,000\\,000 - 300\\,000 = 700\\,000, \\; B = 500\\,000 + 300\\,000 = \\hl{800\\,000}$$",
           """Phép tính thứ nhất, tổng gốc là ba triệu. Phép tính thứ hai, lệnh A sang B ba trăm nghìn hợp lệ, nên A còn bảy trăm nghìn, B thành tám trăm nghìn.""",
           clear=True),
        st("$$③ \\; \\text{B→C}: \\; 1\\,000\\,000 > 800\\,000 \\to \\text{từ chối, không số dư nào đổi}$$"
           "$$④ \\; \\text{A→X}: \\; \\text{không có tài khoản X} \\to \\text{sai lệnh, không số dư nào đổi}$$",
           """Phép tính thứ ba, B cần chuyển một triệu nhưng chỉ có tám trăm nghìn, nên bị từ chối.
           Phép tính thứ tư, tài khoản X không tồn tại, nên là sai lệnh. Cả hai đều bị chặn ở phần kiểm tra, nên không số dư nào đổi."""),
        st("$$⑤ \\; \\text{C→A}: \\; C = 1\\,500\\,000 - 200\\,000 = 1\\,300\\,000, \\; A = 700\\,000 + 200\\,000 = \\hl{900\\,000}$$"
           "$$900\\,000 + 800\\,000 + 1\\,300\\,000 = \\hlg{3\\,000\\,000}$$",
           """Phép tính thứ năm, C chuyển hai trăm nghìn cho A, nên C còn một triệu ba trăm nghìn, A thành chín trăm nghìn.
           Cộng lại, tổng vẫn là ba triệu.""", clear=True),
        st(out_block(so),
           """Chạy thật, sáu dòng khớp từng phép tính: hai lệnh thành công, một từ chối, một sai lệnh, ba số dư cuối và tổng ba triệu.
           Bản ghi lệnh tự in đủ thành phần, nên nhật ký đọc được ngay."""),
    ], checks=["1000000 - 300000 == 700000", "500000 + 300000 == 800000", "1000000 > 800000",
               "1500000 - 200000 == 1300000", "700000 + 200000 == 900000", "900000 + 800000 + 1300000 == 3000000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: dòng tiền ròng của từng tài khoản", [
        st(table(["tài khoản", "đầu ngày", "tiền vào − tiền ra", "cuối ngày"],
                 [["A", "1 000 000", "$-300\\,000 + 200\\,000 = -100\\,000$", "900 000"],
                  ["B", "500 000", "$+300\\,000$", "800 000"],
                  ["C", "1 500 000", "$-200\\,000$", "1 300 000"]])
           + "$$-100\\,000 + 300\\,000 - 200\\,000 = \\hlg{0} \\; \\checkmark$$",
           """Kiểm bằng đường khác: không theo từng lệnh, mà cộng dòng tiền ròng của từng tài khoản trong cả ngày.
           A ra ba trăm nghìn, vào hai trăm nghìn, nên ròng âm một trăm nghìn, còn chín trăm nghìn.
           B ròng cộng ba trăm nghìn, C ròng âm hai trăm nghìn. Cả ba khớp số dư cuối mà chương trình in ra.
           Tổng các dòng ròng bằng không, nghĩa là tổng tiền không đổi, đúng bất biến."""),
    ], checks=["-300000 + 200000 == -100000", "1000000 - 100000 == 900000", "500000 + 300000 == 800000",
               "1500000 - 200000 == 1300000", "-100000 + 300000 - 200000 == 0"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi cố ý, đọc dấu vết, và hai cách sửa sai của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (gài cố ý).</b> Chép dòng trừ sang dòng cộng, quên đổi <code>a</code> thành <code>b</code>.</div>'
           + code_block(so_loi, lines=(l_bug - 1, l_bug)) + out_block(so_loi, "Chạy thì máy ảo in"),
           """Lỗi thứ nhất do ta gài cố ý, và rất đời thường: chép dòng trừ sang dòng cộng, quên đổi chữ a thành chữ b.
           Chương trình dừng ngay ở lệnh đầu tiên, với ngoại lệ trạng thái sai: tổng ba triệu rưỡi khác ba triệu."""),
        st(table(["đọc", "dấu vết nói gì", "suy ra"],
                 [["dòng đầu", "lệch tổng: 3 500 000 thay vì 3 000 000", "thừa $500\\,000 = 1\\,000\\,000 - 500\\,000$: số dư cũ của A trừ của B"],
                  ["<code>at SoCai.kiem</code>", "phương thức kiểm phát hiện", "đây chỉ là nơi <b>phát hiện</b>"],
                  ["<code>at SoCai.chuyen</code>", "kiểm được gọi ngay sau hai bút toán", "lỗi ở hai dòng trừ và cộng ngay trên"],
                  ["<code>at SoLoi.main</code>", "đang chạy lệnh <b>đầu tiên</b> (chưa in OK nào)", "lệnh A → B 300000"]]),
           """Đọc dấu vết từ trên xuống. Dòng đầu nói tổng thừa năm trăm nghìn, đúng bằng số dư cũ của A trừ của B, nên nghi B được cộng nhầm vào số dư của A.
           Dòng kế là phương thức kiểm, nhưng đó chỉ là nơi phát hiện, không phải nơi sai.
           Dòng thứ ba cho biết kiểm được gọi ngay sau hai bút toán, nên lỗi nằm ở hai dòng đó.
           Dòng cuối là hàm chính, và chưa in dòng thành công nào, nên đó là lệnh đầu tiên.""", clear=True),
        st(code_block(so, lines=(l_tru, l_tru + 1), title="Sửa tận gốc: bên nhận cộng vào số dư của chính nó") + out_block(so, "Chạy lại"),
           """Nhìn hai dòng đó: bên nhận đang cộng vào số dư của bên gửi. Sửa a thành b, chạy lại, và tổng trở về ba triệu.""", clear=True),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> “Sửa” bằng cách nuốt ngoại lệ cho chương trình khỏi dừng.</div>'
           + code_block(nuot, lines=(ln(nuot, "catch (Exception e)"), ln(nuot, "catch (Exception e)") + 2)) + out_block(nuot),
           """Lỗi thứ hai, của người đã đi làm, là sửa bằng cách thêm khối bắt mọi ngoại lệ rồi bỏ qua, cho chương trình khỏi dừng.
           Chương trình chạy hết, nhưng tổng thành bốn triệu chín trăm nghìn: gần hai triệu tự sinh ra, không ai được báo.""", clear=True),
        st(table(["lệnh (lỗi gài vẫn còn)", "số dư sau lệnh", "in ra"],
                 [["A → B 300 000", "A = 700 000; B = <b>số dư cũ của A</b> + 300 000 = 1 300 000", "phương thức kiểm ném, bị nuốt: không in OK"],
                  ["B → C 1 000 000", "B có 1 300 000 nên qua kiểm tra: B = 300 000; C = 1 300 000 + 1 000 000 = 2 300 000", "bị nuốt: không in"],
                  ["A → X 50 000", "không đổi", "SAI LENH Khong co tai khoan X"],
                  ["C → A 200 000", "C = 2 100 000; A = 2 300 000 + 200 000 = 2 500 000", "bị nuốt: không in"]])
           + "$$2\\,500\\,000 + 300\\,000 + 2\\,100\\,000 = \\hl{4\\,900\\,000}$$",
           """Lần theo từng lệnh để thấy gần hai triệu từ đâu ra.
           Lệnh một trừ A còn bảy trăm nghìn, nhưng B nhận số dư cũ của A cộng ba trăm nghìn, thành một triệu ba trăm nghìn.
           Phương thức kiểm ném ngoại lệ, khối bắt nuốt mất, nên dòng thành công không được in.
           Lệnh hai, B lúc này có một triệu ba trăm nghìn nên qua kiểm tra, và B còn ba trăm nghìn.
           C nhận một triệu ba trăm nghìn cộng một triệu, thành hai triệu ba trăm nghìn, và lại bị nuốt.
           Lệnh ba sai tài khoản nên in sai lệnh.
           Lệnh bốn, C còn hai triệu một trăm nghìn, còn A nhận hai triệu ba trăm nghìn cộng hai trăm nghìn, thành hai triệu rưỡi.
           Cộng ba số dư được bốn triệu chín trăm nghìn, đúng dòng chương trình in ra.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Chỉ đối soát cuối ngày, không kiểm sau mỗi lệnh.</div>'
           + out_block(cuoi, "Chạy thì máy ảo in"),
           """Lỗi thứ ba là chỉ đối soát, tức so lại tổng tiền, vào cuối ngày. Lệnh B sang C lẽ ra bị từ chối, vẫn chạy được vì số dư đã sai từ lệnh trước.
           Cuối ngày mới biết lệch, và dấu vết chỉ trỏ về hàm chính, không biết lệnh nào gây ra.
           Kiểm sau mỗi lệnh thì dấu vết trỏ đúng lệnh đầu tiên, như ta vừa thấy.""", clear=True),
    ], checks=["700000 + (1000000 + 300000) + 1500000 == 3500000", "3500000 - 3000000 == 1000000 - 500000",
               "4900000 - 3000000 == 1900000",
               "1000000 - 300000 == 700000 and 1000000 + 300000 == 1300000",
               "1000000 <= 1300000 and 1300000 - 1000000 == 300000 and 1300000 + 1000000 == 2300000",
               "2300000 - 200000 == 2100000 and 2300000 + 200000 == 2500000",
               "2500000 + 300000 + 2100000 == 4900000"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(ln(quiz, "SoCai so = new SoCai()"), ln(quiz, "\"A\", \"C\", 1000000")), title="Sổ đã sửa, ba lệnh mới: đoán năm dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Sổ đã sửa đúng, số dư đầu vẫn là một triệu, năm trăm nghìn và một triệu rưỡi.
           Ba lệnh mới: B chuyển cho A sáu trăm nghìn, C chuyển cho B không đồng, và A chuyển cho C một triệu.
           Hãy dừng video và viết ra năm dòng in ra.""", pause=20),
        st(table(["lệnh", "kiểm tra", "kết quả"],
                 [["B → A 600 000", "$600\\,000 > 500\\,000$", "TU CHOI B chi co 500000"],
                  ["C → B 0", "$0 \\le 0$: số tiền phải dương", "SAI LENH So tien phai duong"],
                  ["A → C 1 000 000", "$1\\,000\\,000 > 1\\,000\\,000$ là sai: được chuyển", "A = 0, C = 2 500 000"]]),
           """Đáp án từng lệnh. Lệnh một, B chỉ có năm trăm nghìn mà cần sáu trăm nghìn, nên bị từ chối.
           Lệnh hai, số tiền bằng không, không dương, nên là sai lệnh.
           Lệnh ba nằm đúng biên: một triệu không lớn hơn một triệu, nên được chuyển, A về không, C thành hai triệu rưỡi.
           Tổng vẫn ba triệu."""),
        st(out_block(quiz),
           """Chạy thật, năm dòng khớp đáp án. Ai đoán lệnh ba bị từ chối thì xem lại phép so ở biên."""),
    ], checks=["600000 > 500000", "not (1000000 > 1000000)", "0 + 500000 + 2500000 == 3000000"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("kiểm tra trước", "sửa sau: trừ rồi cộng", "kiểm bất biến sau mỗi lệnh", "lỗi: đọc dấu vết từ trên xuống",
                 "sửa tận gốc, không nuốt"),
           """Tổng kết chuỗi logic. Kiểm tra trước, sửa sau, và kiểm bất biến sau mỗi lệnh.
           Gặp lỗi thì đọc dấu vết, phân biệt nơi phát hiện với nơi sai, rồi sửa tận gốc."""),
        st("""<div class='box key'><b>Tư duy:</b> mỗi hệ thống tiền có một <b>bất biến</b> (ở đây: tổng không đổi). Viết nó thành mã, kiểm sau
mỗi thao tác, và để vi phạm <b>lộ ra ngay</b> kèm dấu vết.</div>""",
           """Điều cần mang theo. Mỗi hệ thống tiền có một bất biến, ở đây là tổng không đổi.
           Hãy viết nó thành mã, kiểm sau mỗi thao tác, và để vi phạm lộ ra ngay kèm dấu vết."""),
        st("""<p>Bạn đã đi hết mười ba bài của khoá học này: từ dòng in đầu tiên tới một sổ chuyển khoản có kiểm bất biến.</p>
<div class='box key'>Chủ đề nên tìm hiểu tiếp: máy ảo Java cấp và thu hồi bộ nhớ cho các đối tượng thế nào (bộ thu gom rác, tức phần tự dọn đối tượng không còn ai dùng).</div>""",
           """Bạn đã đi hết mười ba bài của khoá học này, từ dòng in đầu tiên tới một sổ chuyển khoản có kiểm bất biến.
           Chủ đề nên tìm hiểu tiếp là máy ảo Java cấp và thu hồi bộ nhớ cho các đối tượng thế nào.
           Trong đó có bộ thu gom rác, tức phần tự dọn những đối tượng không còn ai dùng."""),
    ])
    return lesson("L12", "so_chuyen_khoan", "Bài 12 — Tình huống chuyên gia: sổ chuyển khoản nhỏ",
                  "curriculum/jva.yaml L12; audit/jva/verify_jva.py L12 (javac/java chạy thật, kể cả dấu vết lỗi với số dòng tính từ mã); "
                  "The Java Language Specification, Java SE 21 (§8.10 bản ghi, §11.1.1 ngoại lệ có kiểm tra, §14.20 lệnh try nhiều khối catch, "
                  "§5.1.8 mở hộp); Java SE 21 API: java.util.HashMap (get trả null khi không có khoá, values), java.lang.IllegalStateException, "
                  "java.lang.IllegalArgumentException, java.lang.Throwable (dấu vết ngăn xếp); dev.java/learn. Mọi số tiền là số minh hoạ.",
                  ["Ghép lớp, bản ghi, bản đồ, danh sách và ngoại lệ thành một sổ chuyển khoản",
                   "Áp dụng kiểm tra trước, sửa sau và kiểm bất biến tổng tiền sau mỗi lệnh",
                   "Đọc dấu vết lỗi, phân biệt nơi phát hiện với nơi sai, sửa tận gốc",
                   "Nhận ra hai cách sửa sai: nuốt ngoại lệ và chỉ đối soát cuối ngày"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
