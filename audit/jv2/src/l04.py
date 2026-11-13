from lib import *
from labkit import write_lab, practice_steps, practice_scene

MINI_DI = r"""
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

public class MiniDi {
    @Retention(RetentionPolicy.RUNTIME) @interface ThanhPhan {}
    @Retention(RetentionPolicy.RUNTIME) @interface Tiem {}
    @interface KhongGiu {}

    @ThanhPhan static class KhoDuLieu { long soDu(String tk) { return 1000000; } }
    @ThanhPhan static class DichVuPhi { long phi(long t) { return t / 1000; } }
    @ThanhPhan @KhongGiu static class ChuyenTien {
        @Tiem KhoDuLieu kho;
        @Tiem DichVuPhi dvPhi;
        String chuyen(long t) { return "so du " + kho.soDu("A") + ", phi " + dvPhi.phi(t); }
    }

    static Map<Class<?>, Object> hop = new HashMap<>();

    static Object lay(Class<?> loai) throws Exception {
        if (hop.containsKey(loai)) {
            return hop.get(loai);
        }
        if (!loai.isAnnotationPresent(ThanhPhan.class)) {
            throw new IllegalArgumentException("khong phai thanh phan: " + loai.getSimpleName());
        }
        Object o = loai.getDeclaredConstructor().newInstance();
        hop.put(loai, o);
        for (Field f : loai.getDeclaredFields()) {
            if (f.isAnnotationPresent(Tiem.class)) {
                f.setAccessible(true);
                f.set(o, lay(f.getType()));
            }
        }
        return o;
    }

    public static void main(String[] args) throws Exception {
        ChuyenTien c = (ChuyenTien) lay(ChuyenTien.class);
        System.out.println(c.chuyen(5000000));
        System.out.println(c.kho == lay(KhoDuLieu.class));
        System.out.println(hop.size());
        System.out.println(ChuyenTien.class.isAnnotationPresent(KhongGiu.class));
    }
}"""


def build():
    doc_nhan = prog("DocNhan", r"""
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.Comparator;

public class DocNhan {
    @Retention(RetentionPolicy.RUNTIME)
    @interface NghiepVu {
        String ten();
        int uuTien() default 5;
    }

    static class DichVu {
        @NghiepVu(ten = "chuyen tien", uuTien = 1)
        public void chuyen() {}

        @NghiepVu(ten = "tra cuu")
        public void tra() {}

        public void khac() {}
    }

    public static void main(String[] args) {
        Method[] ds = DichVu.class.getDeclaredMethods();
        Arrays.sort(ds, Comparator.comparing(Method::getName));       // thứ tự gốc không xác định
        for (Method m : ds) {
            NghiepVu nv = m.getAnnotation(NghiepVu.class);
            String t = (nv == null) ? "khong co nhan"
                    : nv.ten() + " (uu tien " + nv.uuTien() + ")";
            System.out.println(m.getName() + ": " + t);
        }
    }
}""", out="chuyen: chuyen tien (uu tien 1)\nkhac: khong co nhan\ntra: tra cuu (uu tien 5)")
    quen_giu = prog("QuenGiu", r"""
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

public class QuenGiu {
    @Retention(RetentionPolicy.RUNTIME)
    @interface Giu {}

    @interface KhongGiu {}                                    // quên thời hạn giữ

    @Giu @KhongGiu
    static class A {}

    public static void main(String[] args) {
        System.out.println("giu: " + A.class.isAnnotationPresent(Giu.class));
        System.out.println("khong giu: " + A.class.isAnnotationPresent(KhongGiu.class));
    }
}""", out="giu: true\nkhong giu: false")
    sai_ten = prog("SaiTen", r"""
public class SaiTen {
    interface Phi {
        long tinh(long soTien);
    }

    static class PhiThuong implements Phi {
        @Override
        public long tinhh(long soTien) {                      // gõ thừa chữ h
            return soTien / 1000;
        }
    }

    public static void main(String[] args) {
        System.out.println(new PhiThuong().tinhh(5000000));
    }
}""", expect="compile_error:method does not override or implement a method from a supertype",
                   err="error: PhiThuong is not abstract and does not override abstract method tinh(long) in Phi\n    static class PhiThuong implements Phi {\n           ^\nerror: method does not override or implement a method from a supertype\n        @Override\n        ^")
    mini = prog("MiniDi", MINI_DI, out="so du 1000000, phi 5000\ntrue\n3\nfalse")
    vong_tron = prog("VongTron", r"""
import java.lang.reflect.Constructor;
import java.util.HashSet;
import java.util.Set;

public class VongTron {
    static Set<Class<?>> dangTao = new HashSet<>();

    static class A { A(B b) {} }
    static class B { B(A a) {} }                              // A cần B, B cần A

    static Object tao(Class<?> loai) throws Exception {
        if (!dangTao.add(loai)) {
            throw new IllegalStateException("vong phu thuoc tai " + loai.getSimpleName());
        }
        Constructor<?> ham = loai.getDeclaredConstructors()[0];
        Object[] doiSo = new Object[ham.getParameterCount()];
        for (int i = 0; i < doiSo.length; i++) {
            doiSo[i] = tao(ham.getParameterTypes()[i]);
        }
        dangTao.remove(loai);
        return ham.newInstance(doiSo);
    }

    public static void main(String[] args) throws Exception {
        try {
            tao(A.class);
        } catch (IllegalStateException e) {
            System.out.println(e.getMessage());
        }
    }
}""", out="vong phu thuoc tai A")
    quy_mo = prog("QuyMo", r"""
import java.lang.reflect.Field;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.util.HashMap;
import java.util.Map;

public class QuyMo {
    @Retention(RetentionPolicy.RUNTIME) @interface Tiem {}
    static int soDoiTuong = 0;                                // đếm số lần gọi hàm tạo

    static class Kho { Kho() { soDoiTuong++; } }
    static class Phi { Phi() { soDoiTuong++; } }
    static class Chuyen {
        @Tiem Kho kho;
        @Tiem Phi phi;
        Chuyen() { soDoiTuong++; }
    }

    static Map<Class<?>, Object> hop = new HashMap<>();

    static Object lay(Class<?> loai, boolean chung) throws Exception {
        if (chung && hop.containsKey(loai)) {
            return hop.get(loai);                             // dùng lại: một bản cho mọi yêu cầu
        }
        Object o = loai.getDeclaredConstructor().newInstance();
        hop.put(loai, o);
        for (Field f : loai.getDeclaredFields()) {
            if (f.isAnnotationPresent(Tiem.class)) {
                f.setAccessible(true);
                f.set(o, lay(f.getType(), chung));
            }
        }
        return o;
    }

    public static void main(String[] args) throws Exception {
        int[] soYeuCau = {1000, 1000000};
        for (int n : soYeuCau) {
            for (boolean chung : new boolean[]{true, false}) {
                soDoiTuong = 0;
                hop.clear();
                for (int i = 0; i < n; i++) {
                    lay(Chuyen.class, chung);
                }
                String cach = chung ? " dung chung: " : " moi lan: ";
                System.out.println("yeu cau " + n + cach + soDoiTuong + " doi tuong");
            }
        }
    }
}""", out="yeu cau 1000 dung chung: 3 doi tuong\nyeu cau 1000 moi lan: 3000 doi tuong\n"
             "yeu cau 1000000 dung chung: 3 doi tuong\nyeu cau 1000000 moi lan: 3000000 doi tuong")

    di = project("KiemNhan", {"MiniDi.java": MINI_DI}, [
        ("javac MiniDi.java", ""),
        ("java MiniDi", mini["out"]),
        ("javap -v -p 'MiniDi$ChuyenTien' | grep -E '^Runtime|^    MiniDi'",
         "RuntimeVisibleAnnotations:\n    MiniDi$ThanhPhan\nRuntimeInvisibleAnnotations:\n    MiniDi$KhongGiu"),
    ])

    # ── lab ──
    lab = prog("MiniDiKho", r"""
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

public class MiniDiKho {
    @Retention(RetentionPolicy.RUNTIME) @interface ThanhPhan {}
    @Retention(RetentionPolicy.RUNTIME) @interface Tiem {}

    @ThanhPhan static class KhoHang { int soLuong() { return 12; } }
    @ThanhPhan static class BangGia { long gia() { return 45000; } }
    @ThanhPhan static class DonHang {
        @Tiem KhoHang kho;
        @Tiem BangGia bang;
        long tong() { return kho.soLuong() * bang.gia(); }
    }

    static Map<Class<?>, Object> hop = new HashMap<>();

    static Object lay(Class<?> loai) throws Exception {
        if (hop.containsKey(loai)) {
            return hop.get(loai);
        }
        Object o = loai.getDeclaredConstructor().newInstance();
        hop.put(loai, o);
        for (Field f : loai.getDeclaredFields()) {
            if (f.isAnnotationPresent(Tiem.class)) {
                f.setAccessible(true);
                f.set(o, lay(f.getType()));
            }
        }
        return o;
    }

    public static void main(String[] args) throws Exception {
        DonHang d = (DonHang) lay(DonHang.class);
        System.out.println("Tong gia tri kho: " + d.tong());
        System.out.println("Cung mot BangGia: " + (d.bang == lay(BangGia.class)));
        System.out.println("So thanh phan: " + hop.size());
    }
}""", out="Tong gia tri kho: 540000\nCung mot BangGia: true\nSo thanh phan: 3")
    write_lab("JV2", "L04", """# Lab JV2 L04 — Bộ chứa tiêm phụ thuộc cỡ nhỏ

Viết `MiniDiKho` (tệp `MiniDiKho.java`) gồm **ba phần do bạn tự viết**:

1. Hai nhãn `@ThanhPhan` và `@Tiem` (`@interface`, giữ đến lúc chạy: `@Retention(RetentionPolicy.RUNTIME)`).
2. Bộ chứa: `static Map<Class<?>, Object> hop` và hàm `static Object lay(Class<?> loai) throws Exception`: nếu `hop` đã có thì trả lại; nếu chưa thì
   tạo bằng `loai.getDeclaredConstructor().newInstance()`, **bỏ vào `hop` trước**, rồi với mỗi trường có nhãn `@Tiem` thì `setAccessible(true)` và gán `lay(kiểu của trường)`.
3. `main`: lấy `DonHang` từ bộ chứa rồi in ba dòng (bên dưới).

Ba lớp có sẵn (chép nguyên vào tệp, ngay trong `MiniDiKho`):

```java
@ThanhPhan static class KhoHang { int soLuong() { return 12; } }
@ThanhPhan static class BangGia { long gia() { return 45000; } }
@ThanhPhan static class DonHang {
    @Tiem KhoHang kho;
    @Tiem BangGia bang;
    long tong() { return kho.soLuong() * bang.gia(); }
}
```

In đúng ba dòng:
```
Tong gia tri kho: 540000
Cung mot BangGia: true
So thanh phan: 3
```
(`Cung mot BangGia` là `d.bang == lay(BangGia.class)`; `So thanh phan` là `hop.size()`.)

Chạy: `javac MiniDiKho.java && java MiniDiKho`. Chấm: `bash labs/cham.sh JV2 L04 MiniDiKho.java`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: bộ chứa tiêm phụ thuộc cho kho hàng", practice_steps(
        st, "JV2", "L04",
        """<p><b>Đề</b>: tự viết <b>bộ chứa</b> cỡ nhỏ, ba lớp có sẵn trong <code>de.md</code>.</p>
<ol><li>Hai nhãn <code>@ThanhPhan</code>, <code>@Tiem</code> với <code>@Retention(RUNTIME)</code>.</li>
<li><code>lay(Class)</code>: có trong <code>hop</code> thì trả; chưa thì tạo, <b>bỏ vào hop trước</b>, rồi tiêm các trường <code>@Tiem</code>.</li>
<li><code>main</code>: lấy <code>DonHang</code>, in ba dòng.</li></ol>
<p class="note">Tệp <code>MiniDiKho.java</code>; mã ba lớp có sẵn ở <code>labs/JV2/L04/de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Hãy tự viết một bộ chứa tiêm phụ thuộc nhỏ cho ba lớp có sẵn trong đề bài. Viết hai nhãn giữ đến lúc chạy. Viết hàm lấy đối tượng, nếu đã có thì trả lại, nếu chưa thì tạo, bỏ vào hộp trước, rồi tiêm các trường có nhãn.
        Cuối cùng lấy đơn hàng và in ba dòng. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        lab["out"], "MiniDiKho.java",
        """<div class="box key"><b>Nếu kẹt:</b> <code>for (Field f : loai.getDeclaredFields()) if (f.isAnnotationPresent(Tiem.class)) { f.setAccessible(true); f.set(o, lay(f.getType())); }</code>.
Nhớ <code>hop.put(loai, o)</code> <b>trước</b> vòng lặp trường. Lời giải: <code>labs/JV2/L04/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, duyệt các trường khai báo của lớp. Trường nào có nhãn tiêm thì mở quyền truy cập rồi gán bằng cách lấy đối tượng của kiểu trường. Nhớ bỏ đối tượng vào hộp trước khi duyệt trường.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=240), "JV2", "L04")

    sc_hook = sc("hook", "hook", "Chỉ một dòng nhãn, vì sao chương trình tự đổi hành vi?", [
        st("""<div class="box key"><p>Bạn sẽ gặp mã như thế này trong mọi dự án Java ở ngân hàng:</p>
<div class="code"><div><span class="kw">@Service</span></div><div><span class="kw">public</span> <span class="kw">class</span> ChuyenTien {</div>
<div>    <span class="kw">@Autowired</span> KhoDuLieu kho;</div><div>    <span class="kw">@Transactional</span></div><div>    <span class="kw">public</span> <span class="kw">void</span> chuyen(...) { ... }</div><div>}</div></div>
<p>Không có dòng nào tạo <code>KhoDuLieu</code>, không có dòng nào mở giao dịch. Ai làm?</p></div>""",
           """Trong mọi dự án Java ở ngân hàng, bạn sẽ gặp mã như thế này. Một lớp dịch vụ, một trường kho dữ liệu, một hàm chuyển tiền, và vài dòng nhãn có dấu a còng. Không dòng nào tạo ra kho dữ liệu, không dòng nào mở giao dịch. Vậy ai làm những việc đó.
           Câu trả lời là một chương trình khác đọc các nhãn đó lúc chạy."""),
        st("""<div class="box key">Hôm nay: <b>nhãn (annotation)</b> là dữ liệu gắn vào mã; <b>phản chiếu</b> là cách chương trình đọc chính mã của nó lúc chạy.
Ta tự viết một <b>bộ chứa tiêm phụ thuộc</b> cỡ nhỏ: cùng cơ chế với Spring, chưa tới năm mươi dòng. Rồi hỏi quy mô: một triệu yêu cầu thì tạo bao nhiêu đối tượng?</div>""",
           """Hôm nay ta học nhãn, là dữ liệu gắn vào mã, và phản chiếu, là cách chương trình đọc chính mã của nó lúc chạy. Ta tự viết một bộ chứa tiêm phụ thuộc cỡ nhỏ, cùng cơ chế với Spring, chưa tới năm mươi dòng.
           Rồi hỏi quy mô, một triệu yêu cầu thì tạo ra bao nhiêu đối tượng.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: lớp lồng nhau, giao diện, bản đồ, ngoại lệ", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① lớp lồng", "<code>static class A {}</code> viết ngay trong lớp khác; <code>A.class</code> là đối tượng mô tả lớp <code>A</code>"],
                  ["② <code>@Override</code>", "nhãn đã gặp: báo rằng hàm này ghi đè hàm của giao diện hay lớp cha"],
                  ["③ bản đồ", "<code>Map&lt;K, V&gt;</code> với <code>containsKey</code>, <code>get</code>, <code>put</code>"],
                  ["④ ngoại lệ", "ném bằng <code>throw new …</code>; hàm có thể khai <code>throws Exception</code>"]]),
           """Ta ôn lại bốn điều. Lớp có thể viết lồng trong lớp khác, và mỗi lớp có một đối tượng mô tả riêng, viết bằng tên lớp rồi chấm thêm một chữ. Nhãn ghi đè mà ta đã gặp báo rằng hàm này ghi đè hàm của giao diện. Bản đồ có hàm kiểm khoá, lấy và bỏ vào. Và ngoại lệ ném bằng một lệnh, hàm có thể khai báo ném ngoại lệ.
           Bài này dùng cả bốn.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã tám từ của nhãn và phản chiếu", [
        st(table(["viết", "nghĩa"],
                 [["<code>@Tên</code>", "<b>nhãn</b> (annotation): ghi chú có cấu trúc gắn lên lớp, hàm, trường; <b>tự nó không làm gì</b>"],
                  ["<code>@interface NghiepVu { … }</code>", "cách <b>tự định nghĩa</b> một nhãn; <code>String ten();</code> là một tham số của nhãn"],
                  ["<code>@Retention(RetentionPolicy.RUNTIME)</code>", "nhãn của nhãn: <b>giữ đến lúc chạy</b>; không ghi thì nhãn bị bỏ khi nạp lớp"],
                  ["<code>X.class</code>", "đối tượng <b>mô tả</b> lớp <code>X</code>: tên, trường, hàm, nhãn"],
                  ["<code>getDeclaredFields()</code>", "phản chiếu: lấy mảng các <b>trường</b> khai báo trong lớp"],
                  ["<code>f.isAnnotationPresent(X.class)</code>", "trường (hay lớp, hàm) <code>f</code> có gắn nhãn <code>X</code> không?"],
                  ["<code>newInstance()</code>, <code>f.set(o, v)</code>", "tạo đối tượng và gán giá trị cho trường <b>bằng tên lúc chạy</b>, không viết <code>new</code> hay dấu chấm"],
                  ["tiêm phụ thuộc", "đối tượng <b>không tự tạo</b> thứ nó cần; thứ khác tạo và <b>trao</b> cho nó"]]),
           """Bảng này có tám thứ. Nhãn là ghi chú có cấu trúc gắn lên lớp, hàm hay trường, và tự nó không làm gì cả. Ta có thể tự định nghĩa nhãn, với các tham số. Nhãn của nhãn quy định thời hạn giữ, nếu không ghi thì nhãn bị bỏ khi nạp lớp.
           Đối tượng mô tả lớp cho ta tên, trường, hàm và nhãn. Phản chiếu cho phép lấy danh sách trường, hỏi một trường có nhãn nào không, tạo đối tượng và gán giá trị cho trường bằng tên lúc chạy. Cuối cùng, tiêm phụ thuộc nghĩa là đối tượng không tự tạo thứ nó cần, mà được trao cho.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
        st(code_block(doc_nhan, lines=(8, 12)) + code_block(doc_nhan, lines=(14, 22)),
           """Ta thử nhãn tự định nghĩa. Nhãn nghiệp vụ có tên và độ ưu tiên, độ ưu tiên mặc định là năm. Hai hàm được gắn nhãn, một hàm không gắn. Nhãn chỉ là dữ liệu nằm cạnh mã, hàm vẫn chạy như bình thường.""", clear=True),
        st(code_block(doc_nhan, lines=(25, 33)) + out_block(doc_nhan),
           """Phản chiếu cho ta danh sách các hàm của lớp dịch vụ. Với mỗi hàm, ta hỏi có nhãn nghiệp vụ không. Có thì in tên và độ ưu tiên, không thì in là không có nhãn. Độ ưu tiên của hàm tra cứu là năm, lấy từ giá trị mặc định.""", clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: thợ đọc nhãn và hai thời điểm", [
        st(svg(1500, 330,
               box(20, 80, 330, 170, ["mã nguồn", "@ThanhPhan", "class KhoDuLieu"], C_BLUE, 26, bold=True),
               arrow(355, 165, 450, 165, "#2a78d6", "biên dịch"),
               box(455, 80, 330, 170, [".class (còn nhãn", "nếu RUNTIME)", ""], C_GRAY, 26),
               arrow(790, 165, 885, 165, "#16a34a", "nạp lúc chạy"),
               box(890, 50, 590, 230, ["bộ chứa (chương trình khác)", "đọc nhãn bằng phản chiếu:", "thấy @ThanhPhan → tạo đối tượng", "thấy @Tiem → trao đối tượng vào trường"], C_GREEN, 25, bold=True)),
           """Hình dung nhãn như tờ giấy dán trên hộp hàng, còn bộ chứa là người thợ đọc giấy rồi mới xử lý. Mã nguồn có nhãn được biên dịch ra tệp lớp. Nếu nhãn được giữ đến lúc chạy, thì khi nạp lớp, một chương trình khác, chính là bộ chứa, đọc nhãn bằng phản chiếu.
           Thấy nhãn thành phần thì tạo đối tượng, thấy nhãn tiêm thì trao đối tượng vào trường. Cả Spring cũng làm đúng như vậy."""),
        st(code_block(mini, lines=(8, 18)),
           """Đây là bộ chứa của ta, phần đầu. Hai nhãn giữ đến lúc chạy. Ba lớp, ghi nhãn thành phần. Lớp chuyển tiền cần hai thứ, kho dữ liệu và dịch vụ phí, mỗi thứ có nhãn tiêm. Lớp chuyển tiền không tự tạo hai thứ này, và cũng không có dòng tạo mới nào cho chúng.""", clear=True),
        st(code_block(mini, lines=(22, 28)),
           """Đây là phần chính, hàm lấy đối tượng. Nếu trong hộp đã có thì trả lại ngay. Nếu lớp không có nhãn thành phần thì từ chối.""", clear=True),
        st(code_block(mini, lines=(29, 38)),
           """Còn lại thì tạo đối tượng bằng phản chiếu, bỏ vào hộp, rồi duyệt các trường. Trường nào có nhãn tiêm thì lấy đối tượng của kiểu trường đó, lại bằng chính hàm này, mở quyền truy cập rồi gán vào.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: bộ chứa lấy một đối tượng thế nào", [
        st("<p><b>Bước 1.</b> <b>Hỏi hộp trước.</b> <code>hop.containsKey(loai)</code> đúng &rarr; trả đối tượng cũ.</p>"
           "<p>Vì sao: để <b>mỗi lớp chỉ có một bản</b> (singleton); lần sau lấy lại đúng đối tượng đó.</p>",
           """Bước một, hỏi hộp trước. Nếu lớp đã có đối tượng trong hộp thì trả lại luôn. Vì làm vậy mỗi lớp chỉ có một bản, và những lần sau ai xin cũng nhận đúng đối tượng ấy.""", clear=True),
        st("<p><b>Bước 2.</b> <b>Kiểm nhãn.</b> Không có <code>@ThanhPhan</code> &rarr; từ chối.</p>"
           "<p>Vì sao: bộ chứa chỉ quản lý thứ được <b>đánh dấu</b>; lấy nhầm lớp lạ phải báo lỗi to rõ.</p>",
           """Bước hai, kiểm nhãn. Lớp không có nhãn thành phần thì bị từ chối. Vì bộ chứa chỉ quản lý những gì được đánh dấu, và lấy nhầm một lớp lạ thì phải báo lỗi rõ ràng.""", clear=True),
        st("<p><b>Bước 3.</b> <b>Tạo rồi bỏ vào hộp TRƯỚC khi tiêm.</b></p><p><code>Object o = …newInstance();</code> <code>hop.put(loai, o);</code></p>"
           "<p>Vì sao thứ tự này: nếu hai lớp cần nhau, lúc tiêm lần ngược lại sẽ <b>thấy đối tượng đang dở</b> trong hộp thay vì tạo mãi.</p>",
           """Bước ba, tạo rồi bỏ vào hộp trước khi tiêm. Thứ tự này quan trọng. Nếu hai lớp cần nhau, lúc tiêm lần ngược lại sẽ thấy đối tượng đang dựng dở trong hộp, thay vì tạo mãi không dừng.""", clear=True),
        st("<p><b>Bước 4.</b> <b>Tiêm.</b> Mỗi trường có <code>@Tiem</code>: lấy đối tượng của kiểu trường bằng <b>chính hàm này</b>, rồi <code>f.set(o, …)</code>.</p>"
           "<p>Thử với <code>ChuyenTien</code>: 2 trường &rarr; 2 lần gọi lại &rarr; hộp có 1 + 2 = <b>3</b> đối tượng ✓</p>"
           + table(["lần gọi", "thêm vào hộp", "hộp có"], [["lay(ChuyenTien)", "ChuyenTien", "1"], ["  lay(KhoDuLieu)", "KhoDuLieu", "2"], ["  lay(DichVuPhi)", "DichVuPhi", "<b>3</b>"]]),
           """Bước bốn là bước tiêm đối tượng vào các trường. Với mỗi trường có nhãn tiêm, ta lấy đối tượng của kiểu trường bằng chính hàm này, rồi gán vào. Thử với lớp chuyển tiền, có hai trường, nên hai lần gọi lại, và hộp có một cộng hai bằng ba đối tượng.""", clear=True),
    ], checks=["1 + 2 == 3"])
    sc_ex = sc("example", "example", "Ví dụ: lấy ChuyenTien, từng bước một", [
        st("<p><b>① Hộp rỗng.</b> <code>lay(ChuyenTien)</code>: chưa có trong hộp; có <code>@ThanhPhan</code> ✓ &rarr; tạo, bỏ vào hộp.</p>"
           + table(["hộp sau bước này", "kích thước"], [["ChuyenTien", "<b>1</b>"]]),
           """Phép làm thứ nhất. Lúc đầu hộp đang trống, chưa có đối tượng nào. Ta xin lớp chuyển tiền, chưa có trong hộp, có nhãn thành phần, nên tạo ra và bỏ vào hộp. Hộp có một đối tượng.""", clear=True),
        st("<p><b>② Trường thứ nhất</b> <code>kho</code> có <code>@Tiem</code> &rarr; <code>lay(KhoDuLieu)</code> &rarr; tạo, bỏ vào hộp, gán.</p>"
           "<p><b>③ Trường thứ hai</b> <code>dvPhi</code> có <code>@Tiem</code> &rarr; <code>lay(DichVuPhi)</code> &rarr; tạo, bỏ vào hộp, gán.</p>"
           + table(["hộp sau bước này", "kích thước"], [["ChuyenTien, KhoDuLieu, DichVuPhi", "<b>3</b>"]]),
           """Phép làm thứ hai và ba. Trường đầu tiên có nhãn tiêm, nên bộ chứa lấy kho dữ liệu, tạo, bỏ vào hộp rồi gán vào trường. Trường thứ hai cũng vậy với dịch vụ phí. Hộp giờ có ba đối tượng.""", clear=True),
        st("$$④ \\; \\text{phí} = 5\\,000\\,000 / 1\\,000 = \\hl{5\\,000}$$"
           "<p>Hàm <code>chuyen(5 000 000)</code> in: <code>so du 1000000, phi 5000</code> ✓ (số dư 1 000 000 là số minh hoạ của kho).</p>",
           """Phép làm thứ tư, gọi hàm chuyển với năm triệu. Phí là năm triệu chia một nghìn, bằng năm nghìn. Số dư một triệu là số minh hoạ mà kho trả về. Kết quả ta kỳ vọng in ra là số dư một triệu và phí năm nghìn.""", clear=True),
        st("$$⑤ \\; \\text{xin } \\texttt{KhoDuLieu} \\text{ lần nữa} \\Rightarrow \\text{trả đúng đối tượng cũ, hộp vẫn } \\hl{3}$$"
           + code_block(mini, lines=(41, 45)) + out_block(mini),
           """Phép làm thứ năm, xin kho dữ liệu lần nữa thì nhận lại đúng đối tượng cũ, hộp vẫn là ba. Chạy thật, bốn dòng in ra khớp. Số dư và phí như tính tay, hai tham chiếu là một đối tượng, hộp có ba, và lớp chuyển tiền không có nhãn không giữ, nên nhãn đó không đọc được lúc chạy.""", clear=True),
    ], checks=["5000000 // 1000 == 5000", "1 + 2 == 3"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: nhìn vào tệp lớp bằng công cụ javap", [
        st(term_block(di, 2, 3, title="Lệnh javap in nội dung tệp lớp; lọc các dòng nhãn mức lớp") +
           "<p class='note'>Nhãn có <code>RUNTIME</code> nằm ở mục <b>Visible</b> (đọc được lúc chạy); nhãn không khai thời hạn nằm ở mục <b>Invisible</b> (có trong tệp, nhưng phản chiếu không thấy).</p>",
           """Cách kiểm khác là không tin chương trình, mà nhìn thẳng vào tệp lớp bằng lệnh của bộ công cụ. Lọc các dòng nhãn mức lớp, ta thấy nhãn thành phần nằm ở mục nhìn thấy được lúc chạy, còn nhãn không giữ nằm ở mục không nhìn thấy.
           Điều đó khớp với dòng cuối cùng của chương trình, vì dòng ấy in ra sai cho nhãn không giữ."""),
        st("<p>Kiểm đếm: hộp có <b>3</b> đối tượng = số lớp có <code>@ThanhPhan</code> ta đã xin (<code>ChuyenTien</code>) + số trường <code>@Tiem</code> của nó (2) = 1 + 2.</p>",
           """Ta kiểm thêm bằng cách đếm. Ba đối tượng trong hộp bằng số lớp ta xin trực tiếp là một, cộng số trường có nhãn tiêm của nó là hai, nên con số này khớp.""", clear=True),
    ], checks=["1 + 2 == 3"])
    sc_scale = sc("scale", "concept", "Khi một triệu yêu cầu đi qua: dùng chung hay tạo mới mỗi lần?", [
        st(code_block(quy_mo, lines=(21, 26)) + code_block(quy_mo, lines=(38, 47)),
           """Bây giờ là chuyện quy mô. Ta thêm một công tắc vào bộ chứa, dùng chung thì lần sau lấy lại đối tượng cũ, còn không thì tạo mới cho mỗi yêu cầu. Mỗi yêu cầu cần ba đối tượng. Ta đếm số lần hàm tạo được gọi khi có một nghìn yêu cầu, rồi một triệu yêu cầu.""", clear=True),
        st(out_block(quy_mo) + table(["số yêu cầu", "dùng chung", "tạo mới mỗi lần"], [["1 000", "3", "3 000"], ["1 000 000", "3", "<b>3 000 000</b>"]]),
           """Kết quả thật. Dùng chung thì lúc nào cũng chỉ có ba đối tượng, dù một nghìn hay một triệu yêu cầu. Tạo mới mỗi lần thì ba nghìn, rồi ba triệu đối tượng, tăng đúng theo số yêu cầu, mỗi đối tượng lại cần bộ thu gom rác dọn.
           Đây là lý do Spring mặc định dùng chung một bản cho mỗi thành phần.""", clear=True),
        st("""<div class="box warn"><b>Đánh đổi:</b> một bản dùng chung cho mọi yêu cầu nghĩa là mọi yêu cầu cùng <b>sửa chung</b> các trường của nó.
Ở máy chủ, các yêu cầu chạy <b>đồng thời</b>, nên thành phần dùng chung phải <b>không có trạng thái thay đổi</b>, hoặc phải khoá. Ta sẽ thấy lỗi này ở bài về luồng.</div>""",
           """Nhưng có đánh đổi. Một bản dùng chung cho mọi yêu cầu nghĩa là mọi yêu cầu cùng sửa chung các trường của nó. Ở máy chủ, các yêu cầu chạy đồng thời, nên thành phần dùng chung phải không có trạng thái thay đổi, hoặc phải có khoá. Ta sẽ thấy lỗi này ở bài về luồng.""",
           forward_ref=True),
    ], checks=["3 * 1000 == 3000", "3 * 1000000 == 3000000"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Gõ sai tên hàm mà không có <code>@Override</code> thì im lặng; có thì được báo ngay.</div>'
           + code_block(sai_ten, lines=(6, 11)) + out_block(sai_ten),
           """Lỗi thứ nhất là gõ thừa một chữ trong tên hàm. Nhãn ghi đè là một nhãn mà trình biên dịch đọc ngay lúc biên dịch. Nó nói tôi chắc chắn hàm này ghi đè một hàm cha, và trình biên dịch kiểm lời hứa đó. Hứa sai thì báo lỗi.
           Không có nhãn này, ta sẽ có một hàm mới tinh, hàm cũ vẫn trống, và chương trình chạy sai mà không báo gì."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Quên khai thời hạn giữ nhãn.</div>'
           + code_block(quen_giu, lines=(8, 15)) + out_block(quen_giu),
           """Lỗi thứ hai là quên khai thời hạn giữ nhãn. Nhãn không khai thì có trong tệp lớp nhưng bị bỏ khi nạp, nên phản chiếu hỏi thì nhận câu trả lời là không có. Bộ chứa của ta sẽ lặng lẽ bỏ qua mọi thành phần, nên không có lỗi nào, chỉ là không có gì xảy ra.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Hai lớp cần nhau khi tạo qua hàm tạo: vòng phụ thuộc.</div>'
           + code_block(vong_tron, lines=(8, 9)),
           """Lỗi thứ ba hay gặp ở người đã đi làm là vòng phụ thuộc. Lớp A cần B ngay trong hàm tạo, lớp B cần A. Muốn tạo A thì phải có B, muốn tạo B thì phải có A, và không có đối tượng nào để dở dang cất vào hộp, vì hàm tạo chưa chạy xong."""),
        st(code_block(vong_tron, lines=(11, 19)),
           """Bộ chứa cần một tập ghi những lớp đang tạo. Vào hàm tạo lớp nào thì thêm lớp đó vào tập, nếu đã có sẵn nghĩa là ta đang đi vòng, thì ném lỗi. Tạo xong các tham số thì mới bỏ lớp ra khỏi tập.""", clear=True),
        st(out_block(vong_tron) + "<p class='note'>Cách giải: đổi một phía sang tiêm vào trường (như bộ chứa của ta, đối tượng dở dang đã nằm trong hộp), hoặc tốt hơn <b>tách một lớp thứ ba</b> để xoá vòng. Spring cũng báo lỗi tương tự khi tạo qua hàm tạo.</p>",
           """Kết quả thật, bộ chứa phát hiện vòng và dừng, thay vì chạy mãi. Cách giải là đổi một phía sang tiêm vào trường, hoặc tốt hơn là tách ra một lớp thứ ba để xoá vòng. Vòng phụ thuộc thường là dấu hiệu thiết kế lẫn lộn trách nhiệm.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Bộ chứa trong bài với ba lớp <code>A</code>, <code>B</code>, <code>C</code> đều có <code>@ThanhPhan</code>. <code>A</code> có hai trường <code>@Tiem B b</code>, <code>@Tiem C c</code>; <code>B</code> có một trường <code>@Tiem C c</code>; <code>C</code> không có trường nào.</p>
<ol><li>Sau <code>lay(A.class)</code>, <code>hop</code> có mấy đối tượng? Thứ tự các lớp được <b>tạo</b>?</li>
<li>Nếu <code>@Tiem</code> bị quên <code>@Retention(RUNTIME)</code> thì <code>hop.size()</code> bằng mấy?</li></ol>
<p><b>Chọn A hay B?</b> Thành phần giữ <b>số dư tạm</b> của từng khách. A: một bản dùng chung. B: một bản cho mỗi yêu cầu. Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Ba lớp A, B, C đều có nhãn thành phần. A cần B và C, B cần C, C không cần gì. Hãy tính sau khi lấy A thì hộp có mấy đối tượng, và thứ tự tạo. Rồi nếu nhãn tiêm bị quên khai thời hạn giữ thì hộp có mấy đối tượng.
           Cuối cùng chọn giữa một bản dùng chung và một bản cho mỗi yêu cầu cho thành phần giữ số dư tạm của từng khách, và giải thích. Hãy dừng video và tự làm.""", pause=30),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "<b>3</b>; thứ tự tạo: A, rồi B, rồi C", "A vào hộp trước; tiêm <code>b</code> &rarr; tạo B; B tiêm <code>c</code> &rarr; tạo C; sau đó tiêm <code>c</code> của A: C đã có, dùng lại"],
                  ["2", "<b>1</b>", "nhãn tiêm không được giữ nên không trường nào được tiêm; chỉ có A"],
                  ["3", "<b>B</b>: mỗi yêu cầu một bản", "bản dùng chung bị mọi yêu cầu đồng thời ghi đè số dư tạm lẫn nhau"]]),
           """Đáp án câu một, hộp có ba đối tượng, và thứ tự tạo là A, rồi B, rồi C. A vào hộp trước, tiêm trường b thì tạo B, B tiêm trường c thì tạo C. Khi tiêm trường c của A thì C đã có sẵn nên dùng lại.
           Câu hai, nhãn tiêm không được giữ thì không trường nào được tiêm, hộp chỉ có A, tức là một. Câu ba chọn phương án B, vì bản dùng chung bị mọi yêu cầu đồng thời ghi đè số dư tạm lên nhau.""",
           focus=[1, "1.2", "1.3", "1.4", "1.4"]),
        st("""<div class="box key"><b>Quy tắc:</b> thành phần dùng chung phải <b>không giữ trạng thái riêng của từng yêu cầu</b>. Cần trạng thái riêng thì truyền qua tham số, hoặc tạo bản riêng cho mỗi yêu cầu.</div>""",
           """Quy tắc rút ra. Thành phần dùng chung không được giữ trạng thái riêng của từng yêu cầu. Cần trạng thái riêng thì truyền qua tham số, hoặc tạo bản riêng cho mỗi yêu cầu."""),
    ], checks=["1 + 2 == 3", "len({'A', 'B', 'C'}) == 3"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("nhãn = dữ liệu gắn vào mã", "RUNTIME: giữ đến lúc chạy", "phản chiếu đọc nhãn, tạo, gán", "hộp: một bản mỗi lớp",
                 "bỏ vào hộp trước khi tiêm", "dùng chung thì không giữ trạng thái riêng"),
           """Tổng kết chuỗi logic. Nhãn là dữ liệu gắn vào mã, tự nó không làm gì. Muốn đọc được lúc chạy phải khai thời hạn giữ. Phản chiếu đọc nhãn, tạo đối tượng và gán trường. Hộp giữ một bản cho mỗi lớp.
           Bỏ vào hộp trước khi tiêm để tránh tạo mãi. Và thành phần dùng chung thì không được giữ trạng thái riêng của từng yêu cầu."""),
        st("""<div class='box key'><b>Tư duy:</b> khi thấy một nhãn như <code>@Service</code> hay <code>@Transactional</code>, hỏi ba câu: <b>ai đọc</b> nhãn này (lúc biên dịch hay lúc chạy),
nó <b>quản lý bao nhiêu bản</b> của đối tượng, và có <b>vòng phụ thuộc</b> hay trạng thái chung nào bị giấu sau nhãn không.</div>""",
           """Điều cần mang theo. Khi thấy một nhãn như nhãn dịch vụ hay nhãn giao dịch, hãy hỏi ba câu. Ai đọc nhãn này, lúc biên dịch hay lúc chạy. Nó quản lý bao nhiêu bản của đối tượng. Và có vòng phụ thuộc hay trạng thái chung nào bị giấu sau nhãn không."""),
    ])
    return lesson("L04", "nhan_phan_chieu_mini_di", "Bài 4 — Nhãn và phản chiếu: bộ chứa tiêm phụ thuộc cỡ nhỏ",
                  "curriculum/jv2.yaml L04; audit/jv2/verify_jv2.py L04 (javac/java/javap chạy thật, JDK 21); "
                  "The Java Language Specification, Java SE 21: §9.6 (kiểu chú thích), §9.6.4.2 (@Retention), §9.6.4.4 (@Override); "
                  "java.lang.reflect và java.lang.Class (Java SE 21 API: getDeclaredFields, isAnnotationPresent); "
                  "javap (JDK 21 tools: RuntimeVisibleAnnotations / RuntimeInvisibleAnnotations); "
                  "Spring Framework Reference, mục IoC container, circular dependencies (docs.spring.io); dev.java/learn",
                  ["Mô tả nhãn là dữ liệu gắn vào mã mà chương trình khác đọc, và vì sao phải khai thời hạn giữ",
                   "Đọc nhãn tự định nghĩa bằng phản chiếu và dựng bộ chứa tiêm phụ thuộc cỡ nhỏ",
                   "Nêu cách Spring tự thấy và nối các thành phần: cùng cơ chế với bộ chứa cỡ nhỏ",
                   "Nhận ra vòng phụ thuộc và cái giá khi một thành phần được dùng chung cho mọi yêu cầu",
                   "Viết bộ chứa tiêm phụ thuộc cho ba lớp của kho hàng và chạy thử"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "pitfalls"), (2, "example"), (3, "intuition"), (4, "scale"), (5, "practice")])
