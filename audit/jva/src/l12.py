from lib import *
from labkit import write_lab, practice_steps, practice_scene

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

    lab_code = (TYPES + SO_CAI + """
public class SoCaiLab {
    public static void main(String[] args) {
        SoCai so = new SoCai();
        so.mo("P", 2000000);
        so.mo("Q", 800000);
        so.mo("R", 1200000);
        System.out.println("Mo xong: tong " + so.tong());
        ArrayList<Lenh> ds = new ArrayList<>();
        ds.add(new Lenh("P", "Q", 500000));
        ds.add(new Lenh("Q", "R", 2000000));
        ds.add(new Lenh("P", "Z", 10000));
        ds.add(new Lenh("R", "P", 700000));
        for (Lenh l : ds) {
            try {
                so.chuyen(l);
                System.out.println("OK " + l);
            } catch (KhongDuTien e) {
                System.out.println("TU CHOI " + e.getMessage());
            } catch (IllegalArgumentException e) {
                System.out.println("SAI LENH " + e.getMessage());
            }
        }
        System.out.println("P=" + so.lay("P") + " Q=" + so.lay("Q") + " R=" + so.lay("R"));
        System.out.println("Cuoi ngay: tong " + so.tong());
    }
}""").strip("\n")
    lab_so = prog("SoCaiLab", lab_code, out="Mo xong: tong 4000000\nOK Lenh[tu=P, den=Q, tien=500000]\nTU CHOI Q chi co 1300000\n"
                  "SAI LENH Khong co tai khoan Z\nOK Lenh[tu=R, den=P, tien=700000]\nP=2200000 Q=1300000 R=500000\nCuoi ngay: tong 4000000")
    quy_mo_so = prog("QuyMoSo", """
import java.util.HashMap;

public class QuyMoSo {
    public static void main(String[] args) {
        int[] n = {3, 1000, 10000};                       // số tài khoản
        int[] m = {4, 1000, 10000};                       // số lệnh chuyển
        for (int k = 0; k < n.length; k++) {
            HashMap<Integer, Long> soDu = new HashMap<>();
            for (int i = 0; i < n[k]; i++) {
                soDu.put(i, 1000000L);
            }
            long buoc = 0;                                // số lần cộng trong các lần kiểm tổng
            for (int j = 0; j < m[k]; j++) {
                long t = 0;
                for (long x : soDu.values()) {            // kiểm bất biến: cộng lại mọi số dư
                    t += x;
                    buoc++;
                }
            }
            System.out.println("N=" + n[k] + " M=" + m[k] + ": " + buoc + " buoc");
        }
    }
}""", out="N=3 M=4: 12 buoc\nN=1000 M=1000: 1000000 buoc\nN=10000 M=10000: 100000000 buoc")
    write_lab("JVA", "L12", """# Lab JVA L12 — Dựng sổ chuyển khoản qua ba mốc

Trong Git Bash, thư mục làm việc của bạn, tệp `SoCaiLab.java`. Số liệu là số minh hoạ: ba tài khoản **P = 2 000 000**, **Q = 800 000**, **R = 1 200 000** (tổng gốc 4 000 000).

**Mốc 1 — sổ và tổng.** Lớp `SoCai` giữ `HashMap<String, Long> soDu` và `tongGoc`; hàm `mo(stk, tien)` đặt số dư và cộng `tongGoc`; hàm `tong()` cộng mọi số dư; hàm `lay(stk)` ném `IllegalArgumentException` nếu không có khoá. Hàm chính mở P, Q, R và in `Mo xong: tong 4000000`.

**Mốc 2 — chuyển có kiểm tra trước.** Bản ghi `record Lenh(String tu, String den, long tien) {}` và `class KhongDuTien extends Exception`. Hàm `chuyen(Lenh l) throws KhongDuTien`: lấy số dư hai bên, ném `IllegalArgumentException("So tien phai duong")` nếu tiền không dương, ném `KhongDuTien(tu + " chi co " + a)` nếu tiền lớn hơn số dư bên gửi; **chỉ sau đó** mới trừ bên gửi và cộng bên nhận.

**Mốc 3 — kiểm bất biến sau mỗi lệnh.** Hàm `kiem()` ném `IllegalStateException("Lech tong …")` khi `tong() != tongGoc`; `chuyen` gọi `kiem()` cuối cùng. Hàm chính duyệt bốn lệnh: P→Q 500000, Q→R 2000000, P→Z 10000, R→P 700000; mỗi lệnh trong `try`, bắt `KhongDuTien` (in `TU CHOI …`) và `IllegalArgumentException` (in `SAI LENH …`), thành công in `OK ` + lệnh. Cuối cùng in ba số dư và `Cuoi ngay: tong …`.

Chạy từng mốc để thấy kết quả tăng dần. Chấm bản hoàn chỉnh: `bash labs/cham.sh JVA L12 SoCaiLab.java`.
""", "java", lab_so["code"], lab_so["out"])
    sc_lab = practice_scene(sc, "Tự làm: dựng sổ chuyển khoản qua ba mốc", practice_steps(
        st, "JVA", "L12",
        """<p><b>Đề</b>: tệp <code>SoCaiLab.java</code>, ba tài khoản P 2 000 000, Q 800 000, R 1 200 000 (số minh hoạ). Dựng <b>dần</b>:</p>
<ol><li><b>Mốc 1</b>: <code>SoCai</code> với bản đồ, <code>mo</code>, <code>tong</code>, <code>lay</code> → in <code>Mo xong: tong 4000000</code></li>
<li><b>Mốc 2</b>: bản ghi <code>Lenh</code>, <code>KhongDuTien</code>, hàm <code>chuyen</code> <b>kiểm tra trước, sửa sau</b></li>
<li><b>Mốc 3</b>: <code>kiem()</code> sau mỗi lệnh; chạy bốn lệnh P→Q 500000, Q→R 2000000, P→Z 10000, R→P 700000</li></ol>""",
        """Bây giờ tới phần bạn tự làm trên máy, và đây là phần lớn nhất của khoá. Bạn dựng dần sổ chuyển khoản qua ba mốc, chạy thử sau từng mốc.
        Mốc một, sổ cái với bản đồ số dư, mở ba tài khoản và in tổng bốn triệu. Mốc hai, bản ghi lệnh, ngoại lệ không đủ tiền, và hàm chuyển kiểm tra trước, sửa sau.
        Mốc ba, kiểm bất biến sau mỗi lệnh, rồi chạy bốn lệnh gồm một lệnh hợp lệ, một lệnh quá số dư, một lệnh sai tài khoản và một lệnh hợp lệ nữa. Hãy dừng video và tự dựng, đừng chép lại ví dụ.""",
        lab_so["out"], "SoCaiLab.java",
        """<div class="box key"><b>Nếu kẹt:</b> làm <b>từng mốc</b>, chạy được mới sang mốc sau. Trong <code>chuyen</code>: lấy <code>a</code>, <code>b</code> bằng <code>lay</code>, ném lỗi nếu có, rồi mới <code>put</code> hai lần và gọi <code>kiem()</code>. Hai nhánh <code>catch</code> theo thứ tự trong đề.
Lời giải nằm ở <code>labs/JVA/L12/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, hãy làm từng mốc, chạy được mới sang mốc sau. Trong hàm chuyển, lấy số dư hai bên, ném lỗi nếu cần, rồi mới đặt hai số dư mới và gọi hàm kiểm. Hai khối bắt theo đúng thứ tự trong đề.
        Lời giải nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=90), "JVA", "L12")

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
    nlines = len(so["code"].split("\n"))
    seg = [(1, l_cls - 1), (l_cls, l_tong - 1), (l_tong, l_lay_end), (l_ch, l_tru - 1), (l_tru, l_kiem_end + 1),
           (l_main - 2, l_for - 1), (l_for, nlines)]
    tep_say = ["""Đây là toàn bộ tệp, chia thành bảy phần để bạn gõ lại. Phần một là hai kiểu dữ liệu và các dòng nhập ở đầu tệp.""",
               """Phần hai mở đầu lớp sổ cái, với bản đồ số dư, tổng gốc và phương thức mở tài khoản.""",
               """Phần ba là phương thức cộng tổng và phương thức lấy số dư an toàn.""",
               """Phần bốn là nửa đầu của phương thức chuyển: kiểm tra trước, chưa sửa gì.""",
               """Phần năm là nửa sau: sửa hai số dư, rồi phương thức kiểm bất biến.""",
               """Phần sáu là hàm chính, mở ba tài khoản và nạp bốn lệnh vào danh sách.""",
               """Phần bảy là vòng lặp chạy từng lệnh trong khối thử, rồi in ba số dư và tổng."""]
    sc_tep = sc("tep", "example", "Toàn bộ tệp So.java, từng phần, để bạn gõ lại", [
        st(code_block(so, lines=a_b, title=f"Tệp So.java, phần {i + 1} trên 7"), tep_say[i])
        for i, a_b in enumerate(seg)])
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
    sc_scale = sc("quymo", "concept", "Khi số tài khoản và số lệnh tăng gấp nghìn lần: kiểm tổng sau mỗi lệnh còn rẻ không?", [
        st(code_block(quy_mo_so, lines=(7, 19)),
           """Kiểm bất biến sau mỗi lệnh có giá của nó: mỗi lần phải cộng lại mọi số dư. Ta đếm số lần cộng với ba quy mô, chương trình thật chạy cả ba.""",
           clear=True),
        st(out_block(quy_mo_so),
           """Ba tài khoản bốn lệnh là mười hai lần cộng. Một nghìn tài khoản một nghìn lệnh là một triệu lần. Mười nghìn tài khoản mười nghìn lệnh là một trăm triệu lần.""",
           clear=True),
        st(table(["tài khoản N", "lệnh M", "số lần cộng = N × M", "thời gian nếu 10 nano giây mỗi lần (số minh hoạ)"],
                 [["3", "4", "12", "gần như không"], ["1 000", "1 000", "1 000 000", "10 mili giây"],
                  ["10 000", "10 000", "100 000 000", "1 giây"],
                  ["1 000 000", "1 000 000", "1 000 000 000 000", "10 000 giây ≈ 2,8 giờ"]]),
           """Từ một nghìn lên một triệu, cả tài khoản lẫn lệnh đều gấp một nghìn lần, nhưng chi phí gấp một triệu lần, vì hai con số nhân với nhau.
           Nếu mỗi lần cộng mất mười phần tỉ giây, số minh hoạ, thì một triệu tài khoản và một triệu lệnh cần gần ba giờ chỉ để kiểm tổng, mỗi ngày.""",
           clear=True),
        st("""<div class="box key"><b>Điều người làm nghề rút ra.</b> Ba điều đổi khi sổ lớn lên.
<b>① Kiểm gia tăng:</b> mỗi lệnh chuyển chỉ cần kiểm <b>tổng thay đổi của chính lệnh đó bằng 0</b> (một phép tính), còn kiểm đầy đủ toàn bộ chạy <b>định kỳ</b>.
<b>② Tra cứu:</b> bản đồ tra một tài khoản trong cỡ một bước, danh sách phải duyệt tới N bước.
<b>③ Bộ nhớ:</b> dữ liệu nằm trong biến thì <b>mất khi tắt chương trình</b>, và nhiều chương trình không dùng chung được. Vì thế hệ thống thật lưu vào <b>cơ sở dữ liệu</b>: lưu bền, có giao dịch (làm trọn hoặc hoàn tác), có chỉ mục để tra nhanh, và cho nhiều người dùng cùng lúc.</div>""",
           """Ba điều đổi khi sổ lớn lên. Một, kiểm gia tăng: mỗi lệnh chuyển chỉ cần kiểm rằng tổng thay đổi của chính lệnh đó bằng không, là một phép tính, còn kiểm đầy đủ toàn bộ thì chạy định kỳ.
           Hai, bản đồ tra một tài khoản trong cỡ một bước, còn danh sách phải duyệt tới N bước.
           Ba, dữ liệu nằm trong biến thì mất khi tắt chương trình, và nhiều chương trình không dùng chung được. Vì thế hệ thống thật lưu vào cơ sở dữ liệu, bền, có giao dịch làm trọn hoặc hoàn tác, có chỉ mục, và cho nhiều người cùng dùng.""",
           clear=True),
    ], checks=["3 * 4 == 12", "1000 * 1000 == 10**6", "10**4 * 10**4 == 10**8", "10**6 * 10**6 == 10**12",
               "10**12 * 10 // 10**9 == 10000", "round(10000 / 3600, 1) == 2.8", "(10**6 * 10**6) // (1000 * 1000) == 10**6"])
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
                   "Phân biệt nơi phát hiện với nơi sai khi đọc dấu vết lỗi, và sửa tận gốc",
                   "Nhận ra hai cách sửa sai: nuốt ngoại lệ và chỉ đối soát cuối ngày",
                   "Theo dõi toàn bộ tệp sổ cái hoàn chỉnh, từng phần, và gõ lại được",
                   "Dự đoán chi phí kiểm toàn bộ sau mỗi lệnh khi số tài khoản và số lệnh tăng gấp nghìn lần, và vì sao cần cơ sở dữ liệu",
                   "Dựng sổ chuyển khoản qua ba mốc: sổ và tổng, chuyển có kiểm tra trước, kiểm bất biến sau mỗi lệnh"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_tep, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "formula"), (2, "example"), (3, "pitfalls"), (4, "pitfalls"), (5, "tep"), (6, "quymo"), (7, "practice")])
