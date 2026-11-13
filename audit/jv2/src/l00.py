from lib import *
from labkit import write_lab, practice_steps, practice_scene

TAI_KHOAN = """
package bank.model;

public class TaiKhoan {
    private long soDu;                        // riêng tư: chỉ lớp này chạm vào được

    public TaiKhoan(long soDuDau) {
        this.soDu = soDuDau;
    }

    public void rut(long soTien) {
        if (soTien <= soDu) {
            soDu -= soTien;
        }
    }

    public long soDu() {
        return soDu;
    }

    String moTa() {                           // mặc định: chỉ gói bank.model thấy
        return "TK con " + soDu;
    }
}"""

PHI_CHUYEN = """
package bank.service;

public class PhiChuyen {
    // đến 2 triệu: 3000 đồng; phần vượt 2 triệu tính thêm 1 phần nghìn (số minh hoạ)
    public static long tinh(long soTien) {
        if (soTien <= 2000000) {
            return 3000;
        }
        return 3000 + (soTien - 2000000) / 1000;
    }
}"""

APP = """
package bank;

import bank.model.TaiKhoan;
import bank.service.PhiChuyen;

public class App {
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoan(10000000);
        long soTien = 5000000;
        long phi = PhiChuyen.tinh(soTien);
        tk.rut(soTien + phi);
        System.out.println("Phi: " + phi);
        System.out.println("So du con: " + tk.soDu());
    }
}"""

SAI_TRUY_CAP = """
package bank;

import bank.model.TaiKhoan;

public class Sai {
    public static void main(String[] args) {
        TaiKhoan tk = new TaiKhoan(100);
        tk.soDu = 5000;
        System.out.println(tk.moTa());
    }
}"""

HAI_GOI_A = """
package nganhang;

public class TaiKhoan {
    public String loai() {
        return "thanh toan";
    }
}"""

HAI_GOI_B = """
package thetindung;

public class TaiKhoan {
    public String loai() {
        return "tin dung";
    }
}"""

TRUNG_TEN = """
public class TrungTen {
    public static void main(String[] args) {
        nganhang.TaiKhoan a = new nganhang.TaiKhoan();
        thetindung.TaiKhoan b = new thetindung.TaiKhoan();
        System.out.println("Loai A: " + a.loai());
        System.out.println("Loai B: " + b.loai());
    }
}"""

NHAP_SAO = """
import nganhang.*;
import thetindung.*;

public class NhapSao {
    public static void main(String[] args) {
        TaiKhoan a = null;
        System.out.println("xong");
    }
}"""

LAB_HANG = """
package shop.kho;

public class Hang {
    private int soLuong;

    public Hang(int soLuong) {
        this.soLuong = soLuong;
    }

    public boolean ban(int n) {
        if (n > soLuong) {
            return false;
        }
        soLuong -= n;
        return true;
    }

    public int con() {
        return soLuong;
    }
}"""

LAB_MAIN = """
package shop;

import shop.kho.Hang;

public class Main {
    public static void main(String[] args) {
        Hang h = new Hang(12);
        h.ban(5);
        System.out.println("ban 5 cai, con " + h.con());
        if (!h.ban(9)) {
            System.out.println("ban 9 cai: tu choi, con " + h.con());
        }
    }
}"""

LAB_OUT = "ban 5 cai, con 7\nban 9 cai: tu choi, con 7\nban 5 cai, con 7\nban 9 cai: tu choi, con 7"


def build():
    chinh = project("NganHang", {
        "src/bank/App.java": APP, "src/bank/model/TaiKhoan.java": TAI_KHOAN, "src/bank/service/PhiChuyen.java": PHI_CHUYEN,
    }, [
        ('find src -name "*.java" | sort', "src/bank/App.java\nsrc/bank/model/TaiKhoan.java\nsrc/bank/service/PhiChuyen.java"),
        ("javac -d out src/bank/model/TaiKhoan.java src/bank/service/PhiChuyen.java src/bank/App.java", ""),
        ('find out -name "*.class" | sort', "out/bank/App.class\nout/bank/model/TaiKhoan.class\nout/bank/service/PhiChuyen.class"),
        ("java -cp out bank.App", "Phi: 6000\nSo du con: 4994000"),
        ("jar --create --file bank.jar --main-class bank.App -C out .", ""),
        ("jar tf bank.jar | sort", "META-INF/\nMETA-INF/MANIFEST.MF\nbank/\nbank/App.class\nbank/model/\nbank/model/TaiKhoan.class\n"
                                   "bank/service/\nbank/service/PhiChuyen.class"),
        ("java -jar bank.jar", "Phi: 6000\nSo du con: 4994000"),
    ])
    loi_chay = project("LoiChay", {
        "src/bank/App.java": APP, "src/bank/model/TaiKhoan.java": TAI_KHOAN, "src/bank/service/PhiChuyen.java": PHI_CHUYEN,
    }, [
        ("javac -d out src/bank/model/TaiKhoan.java src/bank/service/PhiChuyen.java src/bank/App.java", ""),
        ("java bank.App", "Error: Could not find or load main class bank.App\nCaused by: java.lang.ClassNotFoundException: bank.App"),
        ("java -cp out App", "Error: Could not find or load main class App\nCaused by: java.lang.ClassNotFoundException: App"),
        ("mkdir lib", ""),
        ("jar --create --file lib/bank.jar -C out .", ""),
        ('java -cp "lib/*" bank.App', "Phi: 6000\nSo du con: 4994000"),
    ])
    sai_tc = project("SaiTruyCap", {
        "src/bank/model/TaiKhoan.java": TAI_KHOAN, "src/bank/Sai.java": SAI_TRUY_CAP,
    }, [
        ("javac -d out src/bank/model/TaiKhoan.java src/bank/Sai.java",
         "src/bank/Sai.java:8: error: soDu has private access in TaiKhoan\n        tk.soDu = 5000;\n          ^\n"
         "src/bank/Sai.java:9: error: moTa() is not public in TaiKhoan; cannot be accessed from outside package\n"
         "        System.out.println(tk.moTa());\n                             ^\n2 errors"),
    ])
    trung = project("TrungTen", {
        "src/nganhang/TaiKhoan.java": HAI_GOI_A, "src/thetindung/TaiKhoan.java": HAI_GOI_B, "src/TrungTen.java": TRUNG_TEN,
    }, [
        ("javac -d out src/nganhang/TaiKhoan.java src/thetindung/TaiKhoan.java src/TrungTen.java", ""),
        ("java -cp out TrungTen", "Loai A: thanh toan\nLoai B: tin dung"),
    ])
    nhap_sao = project("NhapSao", {
        "src/nganhang/TaiKhoan.java": HAI_GOI_A, "src/thetindung/TaiKhoan.java": HAI_GOI_B, "src/NhapSao.java": NHAP_SAO,
    }, [
        ("javac -d out src/nganhang/TaiKhoan.java src/thetindung/TaiKhoan.java src/NhapSao.java",
         "src/NhapSao.java:6: error: reference to TaiKhoan is ambiguous\n        TaiKhoan a = null;\n        ^\n"
         "  both class thetindung.TaiKhoan in thetindung and class nganhang.TaiKhoan in nganhang match\n1 error"),
    ])

    lab_sh = """# Lab JV2 L00: dựng dự án hai tệp trong gói shop, biên dịch ra out, chạy bằng -cp rồi bằng tệp đóng gói
mkdir -p src/shop/kho
cat > src/shop/kho/Hang.java <<'EOF'
""" + LAB_HANG.strip("\n") + """
EOF
cat > src/shop/Main.java <<'EOF'
""" + LAB_MAIN.strip("\n") + """
EOF
javac -d out src/shop/kho/Hang.java src/shop/Main.java
java -cp out shop.Main
jar --create --file cuahang.jar --main-class shop.Main -C out .
java -jar cuahang.jar
"""
    write_lab("JV2", "L00", """# Lab JV2 L00 — Cửa hàng hai tệp, hai gói

Dựng dự án nhỏ trong một thư mục tạm, **tự gõ** hai tệp (không chép từ ví dụ):

1. `src/shop/kho/Hang.java`, gói `shop.kho`: lớp `Hang` có trường `private int soLuong`, hàm tạo nhận số lượng đầu, `public boolean ban(int n)`
   (trả `false` và không đổi gì nếu `n` lớn hơn số còn; ngược lại trừ đi và trả `true`), `public int con()`.
2. `src/shop/Main.java`, gói `shop`, có `import shop.kho.Hang;`. Tạo `Hang` 12 cái, bán 5, in `ban 5 cai, con 7`; rồi bán 9, nếu bị từ chối in `ban 9 cai: tu choi, con 7`.

Biên dịch ra thư mục `out` bằng `javac -d out …`, chạy `java -cp out shop.Main`. Đóng gói `cuahang.jar` với `--main-class shop.Main`, chạy `java -jar cuahang.jar`.

Đầu ra của **cả hai lần chạy** gộp lại thành bốn dòng. Lab này chấm bằng một tệp `.sh` gom mọi lệnh của bạn:
`bash labs/cham.sh JV2 L00 lenh.sh` (tệp `lenh.sh` tạo hai tệp Java bằng `cat > … <<'EOF'`, rồi `javac`, `java`, `jar`).
""", "sh", lab_sh, LAB_OUT)

    # ───────────────────────────── cảnh ─────────────────────────────
    sc_hook = sc("hook", "hook", "Ba trăm tệp trong một thư mục: tìm gì, trùng tên thì sao?", [
        st(svg(1500, 330,
               panel(20, 10, 700, 300, "Một thư mục phẳng, ba trăm tệp", C_RED),
               txt(370, 100, "TaiKhoan.java", 26), txt(370, 140, "TaiKhoan.java ???", 26, "middle", "#dc2626", True),
               txt(370, 180, "PhiChuyen.java", 26), txt(370, 220, "BaoCao.java ... (còn 296 tệp)", 26),
               panel(780, 10, 700, 300, "Tên đầy đủ gồm gói + lớp", C_GREEN),
               txt(1130, 100, "nganhang.TaiKhoan", 28, "middle", "#1f2937", True),
               txt(1130, 150, "thetindung.TaiKhoan", 28, "middle", "#1f2937", True),
               txt(1130, 210, "Hai lớp cùng tên, không đụng nhau", 24, "middle", "#16a34a", True)),
           """Một chương trình thật không nằm trong một tệp. Ngân hàng nhỏ cũng có hàng trăm tệp, và hai nhóm khác nhau rất có thể cùng đặt một lớp tên là tài khoản.
           Nhét hết vào một thư mục thì tên trùng nhau và không ai tìm ra gì. Lời giải là gói, nghĩa là cho mỗi lớp một địa chỉ đầy đủ gồm tên gói và tên lớp."""),
        st("""<div class="box key">Hôm nay: <b>dự án nhiều tệp</b>. Ba việc: đặt lớp vào <b>gói</b>, biên dịch ra một thư mục riêng và chạy bằng
<b>đường dẫn tìm lớp</b>, rồi đóng gói thành <b>một tệp</b> chạy được. Thêm ba mức truy cập quyết định lớp nào được nhìn thấy lớp nào.</div>""",
           """Hôm nay ta học dự án nhiều tệp. Ta đặt lớp vào gói, biên dịch ra một thư mục riêng, chạy bằng đường dẫn tìm lớp, rồi đóng gói thành một tệp duy nhất.
           Ta cũng học ba mức truy cập, quyết định lớp nào được nhìn thấy lớp nào."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: lớp, hàm chính và dòng lệnh", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① tệp và lớp", "một lớp công khai nằm trong tệp có <b>cùng tên</b>: lớp <code>Chao</code> ở tệp <code>Chao.java</code>"],
                  ["② biên dịch và chạy", "<code>javac Chao.java</code> tạo <code>Chao.class</code>; <code>java Chao</code> chạy nó"],
                  ["③ dòng lệnh", "<code>cd</code> đổi thư mục, <code>find</code> liệt kê tệp, <code>|</code> nối đầu ra sang lệnh sau"],
                  ["④ trường riêng tư", "<code>private</code> trên trường: chỉ mã trong cùng lớp được chạm vào"]]),
           """Ta ôn lại bốn điều. Lớp công khai nằm trong tệp cùng tên. Lệnh biên dịch biến tệp mã nguồn thành tệp lớp, lệnh chạy khởi động nó.
           Trong cửa sổ lệnh, lệnh liệt kê tìm tệp và dấu gạch đứng nối kết quả sang lệnh sau. Và trường riêng tư thì chỉ mã trong cùng lớp được chạm vào.
           Bài này dùng đúng bốn điều đó, nhưng với nhiều tệp.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã sáu từ của dự án nhiều tệp", [
        st(table(["viết", "nghĩa"],
                 [["<code>package bank.model;</code>", "dòng <b>đầu tiên</b> của tệp: lớp này thuộc <b>gói</b> tên <code>bank.model</code>"],
                  ["<code>import bank.model.TaiKhoan;</code>", "<b>nạp tên</b>: từ nay viết <code>TaiKhoan</code> thay cho tên đầy đủ"],
                  ["<code>javac -d out …</code>", "cờ <code>-d</code>: đặt các tệp <code>.class</code> vào thư mục đích <code>out</code>"],
                  ["<code>java -cp out bank.App</code>", "cờ <code>-cp</code>: <b>đường dẫn tìm lớp</b> là thư mục <code>out</code>; rồi tên đầy đủ của lớp"],
                  ["<code>jar</code>", "lệnh gom nhiều tệp <code>.class</code> thành <b>một tệp</b> đuôi <code>.jar</code>"],
                  ["<code>public</code> / không ghi / <code>private</code>", "ba mức truy cập: ai cũng thấy / chỉ cùng gói / chỉ cùng lớp"]]),
           """Bảng này có sáu thứ. Dòng khai báo gói luôn đứng đầu tệp và nói lớp thuộc gói nào. Lệnh nạp tên cho phép viết tên ngắn thay cho tên đầy đủ.
           Cờ d của lệnh biên dịch đặt các tệp lớp vào thư mục đích. Cờ cờ-pê của lệnh chạy cho biết thư mục để tìm lớp, kèm tên đầy đủ của lớp cần chạy.
           Lệnh đóng gói gom nhiều tệp lớp thành một tệp. Cuối cùng là ba mức truy cập, ai cũng thấy, chỉ cùng gói thấy, hoặc chỉ cùng lớp thấy.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
        st(pcode(chinh, "src/bank/App.java", lines=(1, 8), title="Tệp src/bank/App.java (đoạn đầu)"),
           """Đây là đầu tệp thật của ví dụ hôm nay. Dòng một khai báo gói ngân hàng. Hai dòng nạp tên lấy lớp tài khoản từ gói con mô hình, và lớp tính phí từ gói con dịch vụ.
           Dấu chấm trong tên gói tách các tầng, giống dấu gạch chéo tách thư mục."""),
    ])
    nodes = [(0, "src", "d"), (1, "bank", "d"), (2, "App.java", "f"), (2, "model", "d"), (3, "TaiKhoan.java", "f"),
             (2, "service", "d"), (3, "PhiChuyen.java", "f")]
    rows = {2: "bank.App", 4: "bank.model.TaiKhoan", 6: "bank.service.PhiChuyen"}
    ann = []
    for i, nm in rows.items():
        y = 10 + i * 54
        ann.append(arrow(710 if nodes[i][0] == 3 else 470, y + 21, 880, y + 21, "#16a34a"))
        ann.append(box(890, y, 440, 42, nm, C_GREEN, 26, bold=True))
    out_nodes = [(0, "out", "d"), (1, "bank", "d"), (2, "App.class", "f"), (2, "model", "d"), (3, "TaiKhoan.class", "f"),
                 (2, "service", "d"), (3, "PhiChuyen.class", "f")]
    sc_int = sc("intuition", "intuition", "Hình dung: tên gói là địa chỉ, thư mục là con đường", [
        st(svg(1500, 400, *tree_parts(nodes, 10, 10, 150, 54, 24, hi={2, 4, 6}), *ann),
           """Hãy hình dung tên gói là địa chỉ nhà. Cây thư mục nguồn bên trái có thư mục ngân hàng, trong đó có thư mục mô hình và thư mục dịch vụ.
           Tên đầy đủ của một lớp là địa chỉ của nó, bằng tên các thư mục từ ngân hàng xuống tới tệp, nối bằng dấu chấm. Vì thế tên gói phải khớp đúng đường đi của thư mục."""),
        st(svg(1500, 400, *tree_parts(nodes, 10, 10, 150, 54, 22, col_hi=C_GRAY),
               arrow(700, 200, 790, 200, "#d97706"), txt(745, 170, "javac -d out", 22, "middle", "#d97706", True),
               *tree_parts(out_nodes, 800, 10, 150, 54, 22, hi={2, 4, 6}, col_hi=C_GREEN)),
           """Khi biên dịch với cờ d, cây thư mục đích sao đúng cấu trúc của cây nguồn, chỉ khác tệp mã nguồn đổi thành tệp lớp.
           Khi chạy, máy đọc tên đầy đủ của lớp ứng dụng, đổi mỗi dấu chấm thành dấu gạch chéo, rồi tìm theo con đường đó bên trong thư mục đích."""),
        st(pcode(chinh, "src/bank/model/TaiKhoan.java", lines=(1, 6), title="Tệp src/bank/model/TaiKhoan.java (đầu tệp)")
           + pcode(chinh, "src/bank/service/PhiChuyen.java", lines=(1, 4), title="Tệp src/bank/service/PhiChuyen.java (đầu tệp)"),
           """Hai tệp còn lại cũng bắt đầu bằng dòng khai báo gói khớp với thư mục của chúng. Lớp tài khoản giữ số dư ở trường riêng tư.
           Lớp tính phí chỉ có một hàm tĩnh, nên không cần tạo đối tượng mà gọi thẳng bằng tên lớp."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: từ tên gói tới đường dẫn tệp", [
        st("<p><b>Bước 1.</b> Tên đầy đủ nối gói và lớp bằng dấu chấm:</p>"
           "<p><code>bank.model</code> + <code>.</code> + <code>TaiKhoan</code> = <code>bank.model.TaiKhoan</code></p>",
           """Bước một, ghép tên đầy đủ. Gói là ngân hàng chấm mô hình, lớp là tài khoản, nối bằng một dấu chấm ta được tên đầy đủ.
           Máy ảo luôn dùng tên đầy đủ này, nên hai lớp trùng tên ngắn vẫn là hai lớp khác nhau."""),
        st("<p><b>Bước 2.</b> Đổi mỗi dấu chấm của gói thành dấu gạch chéo, thêm thư mục gốc và đuôi tệp:</p>"
           "<p><code>src/</code> + <code>bank/model</code> + <code>/TaiKhoan</code> + <code>.java</code> = <code>src/bank/model/TaiKhoan.java</code></p>",
           """Bước hai, tìm đường dẫn tệp nguồn. Vì dấu chấm của gói tương ứng với dấu gạch chéo của thư mục, nên ta đổi chúng rồi đặt thư mục gốc phía trước và đuôi tệp phía sau.
           Kết quả là đường dẫn của tệp nguồn mà ta đã viết."""),
        st("<p><b>Bước 3.</b> Cờ <code>-d out</code> chỉ đổi thư mục gốc và đuôi tệp; phần giữa giữ nguyên:</p>"
           + table(["thành phần", "tệp nguồn", "tệp lớp"],
                   [["thư mục gốc", "<code>src/</code>", "<code>out/</code>"], ["gói đổi chấm thành gạch chéo", "<code>bank/model</code>", "<code>bank/model</code>"],
                    ["tên lớp", "<code>/TaiKhoan</code>", "<code>/TaiKhoan</code>"], ["đuôi tệp", "<code>.java</code>", "<code>.class</code>"]]),
           """Bước ba, tệp lớp sau khi biên dịch. Cờ d đổi thư mục gốc thành out, còn đuôi tệp thành lớp, phần giữa giữ nguyên.
           Nên chỉ cần biết tên đầy đủ là suy ra được cả hai đường dẫn."""),
        st("<p><b>Bước 4.</b> <code>-cp out</code> nghĩa là: <b>bắt đầu tìm từ thư mục <code>out</code></b>. Máy ghép <code>out/</code> + tên đầy đủ đã đổi chấm thành gạch chéo + <code>.class</code>:</p>"
           "<p><code>java -cp out bank.App</code> &rarr; mở <code>out/bank/App.class</code> <b class='green'>(đúng)</b></p>"
           "<p><code>java -cp out App</code> &rarr; mở <code>out/App.class</code> <b class='red'>(sai)</b> không có</p>",
           """Bước bốn, vì sao chạy phải kèm tên đầy đủ. Đường dẫn tìm lớp là điểm xuất phát, và máy ghép điểm đó với tên đầy đủ để ra tệp cần mở.
           Gõ đúng tên đầy đủ thì mở được tệp lớp của ứng dụng. Chỉ gõ tên ngắn thì máy tìm một tệp không tồn tại.""", clear=True),
    ])
    sc_ex = sc("example", "example", "Ví dụ: dựng, biên dịch, chạy và đóng gói dự án ba tệp", [
        st(term_block(chinh, 0, 1, title="① Ba tệp nguồn đã viết xong") + "<p class='note'>Ba tệp ở ba thư mục: <code>bank</code>, <code>bank/model</code>, <code>bank/service</code>.</p>",
           """Phép làm thứ nhất, liệt kê ba tệp nguồn. Ta dùng lệnh liệt kê kèm sắp xếp để thứ tự luôn giống nhau trên mọi máy.
           Thấy đúng ba tệp, mỗi tệp nằm ở thư mục khớp với dòng khai báo gói của nó."""),
        st(term_block(chinh, 1, 3, title="② Biên dịch ra out, rồi xem thư mục out"),
           """Phép làm thứ hai, biên dịch. Ta đưa cho trình biên dịch cả ba tệp và cờ d. Lệnh không in gì, nghĩa là không có lỗi.
           Nhìn vào thư mục đích thấy ba tệp lớp nằm đúng cấu trúc thư mục như cây nguồn.""", clear=True),
        st("$$③ \\; 3\\,000 + (5\\,000\\,000 - 2\\,000\\,000) / 1\\,000 = \\hl{6\\,000}$$"
           "$$④ \\; 10\\,000\\,000 - (5\\,000\\,000 + 6\\,000) = \\hl{4\\,994\\,000}$$",
           """Phép làm thứ ba, tính tay phí chuyển năm triệu đồng. Phần vượt hai triệu là ba triệu, chia một nghìn được ba nghìn, cộng ba nghìn cố định thành sáu nghìn đồng.
           Phép làm thứ tư, tài khoản có mười triệu bị rút năm triệu cộng sáu nghìn phí, còn bốn triệu chín trăm chín mươi tư nghìn đồng.""", clear=True),
        st(term_block(chinh, 3, 4, title="⑤ Chạy bằng đường dẫn tìm lớp") ,
           """Phép làm thứ năm, chạy chương trình với cờ cờ-pê trỏ vào thư mục đích. Hai dòng in ra khớp đúng với hai phép tính tay: phí là sáu nghìn, số dư còn bốn triệu chín trăm chín mươi tư nghìn.""", clear=True),
        st(term_block(chinh, 4, 7, title="⑥ Đóng gói và chạy từ một tệp"),
           """Cuối cùng là đóng gói. Lệnh đóng gói gom thư mục đích thành một tệp, và ghi sẵn tên lớp chạy đầu tiên.
           Danh sách bên trong có thêm thư mục mô tả, còn lại giống hệt thư mục đích. Khi chạy chỉ cần một lệnh, đưa tên tệp đóng gói, và ra cùng hai dòng kết quả.""", clear=True),
    ], checks=["3000 + (5000000 - 2000000) // 1000 == 6000", "10000000 - (5000000 + 6000) == 4994000", "5000000 - 2000000 == 3000000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm lớp và so hai cách chạy", [
        st("""<p>Đếm: ba tệp <code>.java</code> &rarr; ba tệp <code>.class</code> &rarr; ba lớp trong tệp đóng gói (ngoài thư mục và tệp mô tả).</p>
<p>Hai cách chạy, <code>java -cp out bank.App</code> và <code>java -jar bank.jar</code>, in <b>cùng</b> hai dòng: <code>Phi: 6000</code> và <code>So du con: 4994000</code>.</p>""",
           """Cách kiểm thứ nhất là đếm. Ba tệp nguồn cho ra ba tệp lớp, và ba tệp lớp đó đều có mặt trong tệp đóng gói. Cách kiểm thứ hai là so hai cách chạy khác nhau.
           Chạy từ thư mục đích và chạy từ tệp đóng gói cho đúng hai dòng giống nhau, nên việc đóng gói không làm đổi hành vi."""),
        st("""<p>Kiểm phí bằng đường khác: phần vượt hai triệu tính 1 phần nghìn nghĩa là $0{,}1\\%$:</p>
$$3\\,000 + 3\\,000\\,000 \\times 0{,}001 = \\hl{6\\,000}$$""",
           """Kiểm phí theo cách khác. Phần vượt hai triệu là ba triệu, tính một phần nghìn tức không phẩy một phần trăm. Ba triệu nhân không phẩy không không một bằng ba nghìn, cộng ba nghìn cố định là sáu nghìn.
           Trùng với kết quả của chương trình, vậy cả công thức và mã đều đúng.""", clear=True),
    ], checks=["3000 + 3000000 * 0.001 == 6000", "len(['App', 'TaiKhoan', 'PhiChuyen']) == 3"])
    sc_scale = sc("scale", "concept", "Khi dự án lớn gấp một trăm lần: tên trùng và đường dẫn dài", [
        st(pcode(trung, "src/nganhang/TaiKhoan.java", lines=(1, 6), title="nganhang/TaiKhoan.java") + term_block(trung, 0, 2, title="Hai lớp cùng tên, hai gói"),
           """Khi dự án to ra, trước hết là chuyện tên trùng. Đây là hai lớp cùng tên tài khoản, nhưng ở hai gói khác nhau. Dùng tên đầy đủ thì chúng sống chung được, chạy ra hai dòng khác nhau.
           Với ba trăm lớp, số cặp có thể trùng tên ngắn là ba trăm nhân hai trăm chín mươi chín chia hai, gần bốn mươi lăm nghìn cặp, mà gói chia nhỏ chuyện đó."""),
        st(table(["số thư viện ngoài", "3", "30", "300"],
                 [["độ dài đường dẫn tìm lớp (số minh hoạ: mỗi tệp 40 ký tự)", "120", "1 200", "<b>12 000</b>"],
                  ["so với giới hạn 8 191 ký tự của dòng lệnh <code>cmd.exe</code>", "vừa", "vừa", "<b>vượt</b>"]])
           + "<p class='note'>Cách rút gọn: <code>java -cp \"lib/*\" bank.App</code> — dấu <code>*</code> lấy mọi tệp <code>.jar</code> trong <code>lib</code>.</p>",
           """Thứ hai là đường dẫn tìm lớp dài ra. Mỗi thư viện ngoài là một tệp đóng gói phải liệt kê trong đường dẫn. Giả sử mỗi tệp chiếm bốn mươi ký tự, ba thư viện cần một trăm hai mươi ký tự, nhưng ba trăm thư viện cần mười hai nghìn.
           Quá giới hạn tám nghìn một trăm chín mươi mốt ký tự của dòng lệnh. Giải pháp là dùng dấu sao, và về lâu dài là công cụ xây dựng tự quản lý danh sách, điều bạn sẽ gặp ở dự án thật.""", clear=True),
        st(term_block(loi_chay, 3, 6, title="Dấu sao lấy mọi tệp đóng gói trong thư mục lib"),
           """Ta thử dấu sao thật. Bỏ tệp đóng gói vào thư mục thư viện rồi chạy chỉ với đường dẫn thư viện gạch chéo sao, chương trình vẫn chạy đúng.
           Đánh đổi của người làm nghề: gói và thư mục giúp quy mô lớn, nhưng đòi kỷ luật đặt tên và công cụ quản lý thư viện.""", clear=True),
    ], checks=["300 * 299 // 2 == 44850", "3 * 40 == 120", "30 * 40 == 1200", "300 * 40 == 12000", "12000 > 8191", "1200 < 8191"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Chạy sai: thiếu <code>-cp</code>, hoặc gõ tên ngắn.</div>'
           + term_block(loi_chay, 1, 3),
           """Lỗi thứ nhất là chạy sai chỗ. Quên cờ cờ-pê thì máy tìm lớp trong thư mục hiện tại và không thấy gì. Có cờ nhưng gõ tên ngắn thì cũng không thấy, như ta vừa suy ra.
           Hai thông báo đều nói không tìm thấy lớp chính. Cách xử lý là kiểm ba thứ: đứng đúng thư mục, có cờ, và tên đầy đủ."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Chạm vào trường riêng tư hay hàm mặc định từ gói khác.</div>'
           + term_block(sai_tc, 0, 1),
           """Lỗi thứ hai là xâm phạm truy cập. Lớp ở gói khác sửa thẳng trường riêng tư thì bị từ chối. Gọi hàm mặc định từ gói khác cũng bị từ chối, vì hàm không công khai.
           Trình biên dịch báo ngay hai lỗi, nên đây là lỗi lúc biên dịch chứ không phải lúc chạy. Muốn cho phép thì phải chủ động mở bằng từ công khai."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nạp tên bằng dấu sao từ hai gói có lớp cùng tên.</div>'
           + pcode(nhap_sao, "src/NhapSao.java", lines=(1, 3), title="Đầu tệp NhapSao.java") + term_block(nhap_sao, 0, 1),
           """Lỗi thứ ba hay gặp ở người đã đi làm. Nạp tên bằng dấu sao từ hai gói, và cả hai gói có lớp cùng tên. Đến chỗ dùng tên ngắn, trình biên dịch không biết chọn lớp nào và báo mơ hồ.
           Cách tránh là nạp tên từng lớp cụ thể, hoặc viết tên đầy đủ ở đúng chỗ cần."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Tệp <code>src/shop/ban/DonHang.java</code> có lớp công khai <code>DonHang</code> với hàm công khai <code>tong()</code>. Lớp <code>Main</code> nằm ở <code>src/shop/Main.java</code>.</p>
<ol><li>Viết dòng đầu của <code>DonHang.java</code> và dòng nạp tên trong <code>Main.java</code>.</li>
<li>Lệnh biên dịch ra <code>out</code> và lệnh chạy <code>Main</code>?</li>
<li>Tệp lớp của <code>DonHang</code> nằm ở đâu?</li></ol>
<p><b>Chọn A hay B?</b> Hàm <code>kiemTra()</code> chỉ cần cho các lớp cùng gói. A: <code>public</code>. B: không ghi mức truy cập. Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Tệp đơn hàng nằm trong thư mục cửa hàng chấm bán, còn lớp chính nằm ở thư mục cửa hàng. Hãy viết dòng khai báo gói, dòng nạp tên, lệnh biên dịch, lệnh chạy, và nói tệp lớp nằm ở đâu.
           Rồi chọn giữa công khai và mặc định cho hàm chỉ cần trong gói, và giải thích vì sao. Hãy dừng video và tự làm.""", pause=25),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "<code>package shop.ban;</code> và <code>import shop.ban.DonHang;</code>", "gói khớp thư mục <code>shop/ban</code>"],
                  ["2", "<code>javac -d out src/shop/ban/DonHang.java src/shop/Main.java</code>; <code>java -cp out shop.Main</code>", "tên đầy đủ <code>shop.Main</code>"],
                  ["3", "<code>out/shop/ban/DonHang.class</code>", "thư mục đích + gói đổi chấm thành gạch chéo"]]),
           """Đáp án, gói của đơn hàng là cửa hàng chấm bán, vì thư mục là cửa hàng gạch chéo bán, và lớp chính nạp tên đúng như vậy. Biên dịch đưa cả hai tệp và cờ d, chạy dùng tên đầy đủ của lớp chính.
           Tệp lớp của đơn hàng nằm trong thư mục đích, rồi cửa hàng, rồi bán, đúng bằng thư mục đích cộng với gói đổi dấu chấm thành gạch chéo.""",
           focus=["1.2", "1.3", "1.4"]),
        st("""<div class="box key"><b>Chọn B</b> (không ghi). Vì hàm chỉ để các lớp trong gói dùng, nên giấu khỏi mọi nơi khác: <b>mở càng ít càng tốt</b>.
Sau này đổi cách làm bên trong, chỉ cần sửa trong gói; còn <code>public</code> là lời hứa với cả thế giới.</div>""",
           """Chọn phương án B, không ghi mức truy cập. Hàm chỉ cần trong gói thì nên giấu khỏi nơi khác, vì mở càng ít càng dễ thay đổi về sau.
           Từ công khai là lời hứa với mọi người dùng bên ngoài, một khi đã hứa thì khó rút lại."""),
    ])
    sc_lab = practice_scene(sc, "Tự làm: cửa hàng hai tệp, hai gói", practice_steps(
        st, "JV2", "L00",
        """<p><b>Đề</b>: dựng dự án <b>hai gói</b>, chạy bằng hai cách.</p>
<ol><li><code>src/shop/kho/Hang.java</code>: <code>private int soLuong</code>, hàm tạo, <code>boolean ban(int n)</code>, <code>int con()</code>.</li>
<li><code>src/shop/Main.java</code>: tạo <code>Hang</code> 12 cái, bán 5 rồi bán 9, in kết quả.</li>
<li><code>javac -d out …</code>, <code>java -cp out shop.Main</code>, rồi <code>jar</code> và <code>java -jar cuahang.jar</code>.</li></ol>
<p class="note">Gom mọi lệnh vào tệp <code>lenh.sh</code> (hai tệp Java tạo bằng <code>cat &gt; … &lt;&lt;'EOF'</code>). Thư mục lab: <code>labs/JV2/L00</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Dựng dự án hai gói. Lớp hàng nằm trong gói cửa hàng chấm kho, giữ số lượng ở trường riêng tư, có hàm bán và hàm đọc số còn.
        Lớp chính ở gói cửa hàng tạo mười hai cái, bán năm, rồi thử bán chín. Biên dịch ra thư mục đích, chạy bằng đường dẫn tìm lớp, rồi đóng gói và chạy từ tệp đóng gói.
        Hãy dừng video, mở trình soạn mã và tự viết, đừng chép lại ví dụ.""",
        LAB_OUT, "lenh.sh",
        """<div class="box key"><b>Nếu kẹt:</b> hàm bán trả <code>false</code> khi <code>n &gt; soLuong</code>, ngược lại trừ rồi trả <code>true</code>. Lớp <code>Main</code> cần <code>import shop.kho.Hang;</code>.
Chạy từ thư mục chứa <code>src</code>. Lời giải: <code>labs/JV2/L00/loi_giai.sh</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, hàm bán trả sai khi số cần bán lớn hơn số còn, ngược lại trừ đi rồi trả đúng. Lớp chính phải nạp tên lớp hàng. Hãy chạy các lệnh từ thư mục chứa thư mục nguồn.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=120), "JV2", "L00")
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("lớp có tên đầy đủ = gói + lớp", "thư mục nguồn khớp tên gói", "javac -d out", "java -cp out tên-đầy-đủ", "jar gom thành một tệp",
                 "mở càng ít càng tốt"),
           """Tổng kết chuỗi logic. Lớp có tên đầy đủ gồm gói và tên lớp. Thư mục nguồn phải khớp tên gói. Biên dịch với cờ d để ra thư mục đích có cùng cấu trúc.
           Chạy với cờ cờ-pê và tên đầy đủ. Đóng gói để gom thành một tệp. Và mức truy cập nên mở càng ít càng tốt."""),
        st("""<div class='box key'><b>Tư duy:</b> khi một chương trình không chạy, hỏi ba câu: tên đầy đủ của lớp là gì, tệp lớp có nằm đúng thư mục
trong đường dẫn tìm lớp không, và lớp đứng đó có được phép nhìn thấy thứ nó đang gọi không.</div>""",
           """Điều cần mang theo. Khi chương trình không chạy, hãy hỏi ba câu. Tên đầy đủ của lớp là gì. Tệp lớp có nằm đúng thư mục trong đường dẫn tìm lớp không.
           Và lớp đứng đó có được phép nhìn thấy thứ nó đang gọi hay không."""),
    ])
    return lesson("L00", "du_an_nhieu_tep", "Bài 0 — Dự án nhiều tệp: gói, biên dịch ra thư mục, tệp đóng gói",
                  "curriculum/jv2.yaml L00; audit/jv2/verify_jv2.py L00 (javac/java/jar chạy thật, JDK 21); The Java Language Specification, "
                  "Java SE 21: §7.4 (khai báo gói), §7.5 (nhập khẩu tên: single-type và on-demand, §6.4.1), §6.6 (kiểm soát truy cập); "
                  "JDK 21 tools: javac -d, java -cp, jar (docs.oracle.com/en/java/javase/21/docs/specs/man); "
                  "Windows: cmd.exe giới hạn dòng lệnh 8191 ký tự (support.microsoft.com KB830473); dev.java/learn",
                  ["Mô tả vì sao tên đầy đủ của lớp gồm gói và tên lớp, và cây thư mục nguồn khớp tên gói",
                   "Dựng dự án ba tệp, biên dịch ra thư mục đích, chạy bằng đường dẫn tìm lớp và đóng gói thành một tệp",
                   "Phân biệt ba mức truy cập và nhận ra lỗi biên dịch khi vượt quyền",
                   "Nhận ra tên trùng và đường dẫn tìm lớp dài ra khi dự án lớn dần, và cách rút gọn",
                   "Viết, biên dịch và chạy dự án hai gói bằng lệnh của chính mình"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "intuition"), (2, "example"), (3, "pitfalls"), (4, "scale"), (5, "practice")])
