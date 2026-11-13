from lib import *
from labkit import write_lab, practice_steps, practice_scene

TONG_PHI_LOI = r"""
public class TongPhi {
    static long phi(long soTien) {
        if (soTien <= 1000000) {
            return 1000;
        }
        if (soTien <= 10000000) {
            return 5000;
        }
        return 10000;
    }

    static long tongPhi(long[] ds) {
        long tong = 0;
        for (int i = 0; i <= ds.length; i++) {
            tong += phi(ds[i]);
        }
        return tong;
    }

    static void baoCao(long[] ds) {
        System.out.println("So giao dich: " + ds.length);
        System.out.println("Tong phi: " + tongPhi(ds));
    }

    public static void main(String[] args) {
        baoCao(new long[]{800000, 2500000, 1000000, 12000000, 9000000});
    }
}"""


def build():
    dau_vet = prog("DauVet", r"""
public class DauVet {
    static long chia(long tong, long soLuong) {
        return tong / soLuong;                                // nổ ở đây khi soLuong = 0
    }

    static long trungBinh(long[] ds) {
        long tong = 0;
        for (long x : ds) {
            tong += x;
        }
        return chia(tong, ds.length);
    }

    static void baoCao(long[] ds) {
        System.out.println("Trung binh: " + trungBinh(ds));
    }

    public static void main(String[] args) {
        baoCao(new long[]{500000, 700000});
        baoCao(new long[]{});                                 // danh sách rỗng
    }
}""", out="Trung binh: 600000", expect="runtime_error:ArithmeticException",
                   err='Exception in thread "main" java.lang.ArithmeticException: / by zero\n\tat DauVet.chia(DauVet.java:3)\n\tat DauVet.trungBinh(DauVet.java:11)\n\tat DauVet.baoCao(DauVet.java:15)\n\tat DauVet.main(DauVet.java:20)')
    boc_loi = prog("BocLoi", r"""
public class BocLoi {
    static void rut(long soDu, long tien) {
        if (tien > soDu) {
            throw new IllegalStateException("so du am: " + (soDu - tien));
        }
    }

    static void chuyen(long soDu, long tien) {
        try {
            rut(soDu, tien);
        } catch (IllegalStateException e) {
            throw new RuntimeException("chuyen tien that bai", e);     // bọc lỗi gốc làm nguyên nhân
        }
    }

    public static void main(String[] args) {
        chuyen(100, 150);
    }
}""", out="", expect="runtime_error:RuntimeException",
                    err='Exception in thread "main" java.lang.RuntimeException: chuyen tien that bai\n\tat BocLoi.chuyen(BocLoi.java:12)\n\tat BocLoi.main(BocLoi.java:17)\nCaused by: java.lang.IllegalStateException: so du am: -50\n\tat BocLoi.rut(BocLoi.java:4)\n\tat BocLoi.chuyen(BocLoi.java:10)\n\t... 1 more')
    nhat_ky = prog("NhatKy", r"""
import java.util.logging.Formatter;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.LogRecord;
import java.util.logging.Logger;
import java.util.logging.StreamHandler;

public class NhatKy {
    static class DinhDang extends Formatter {
        public String format(LogRecord r) {
            return "[" + r.getLevel() + "] " + r.getMessage() + "\n";
        }
    }

    public static void main(String[] args) {
        Logger log = Logger.getLogger("ngan-hang");
        log.setUseParentHandlers(false);
        Handler h = new StreamHandler(System.out, new DinhDang());
        h.setLevel(Level.ALL);
        log.addHandler(h);
        log.setLevel(Level.INFO);                             // chỉ INFO trở lên
        log.fine("chi tiet: so du truoc = 100");
        log.info("bat dau chuyen 50");
        log.warning("so du thap: 50");
        log.severe("chuyen that bai");
        log.setLevel(Level.ALL);                              // bật mọi mức
        log.fine("chi tiet: so du sau = 50");
        h.flush();
    }
}""", out="[INFO] bat dau chuyen 50\n[WARNING] so du thap: 50\n[SEVERE] chuyen that bai\n[FINE] chi tiet: so du sau = 50")
    log_dat = prog("LogDat", r"""
import java.util.logging.Level;
import java.util.logging.Logger;

public class LogDat {
    static long dem = 0;

    static String tinhDat() {
        dem++;                                                // giả lập một phép tính tốn kém
        return "x";
    }

    public static void main(String[] args) {
        Logger log = Logger.getLogger("ngan-hang");
        log.setLevel(Level.INFO);                             // mức FINE đang TẮT
        for (int i = 0; i < 1000000; i++) {
            log.fine("gia tri " + tinhDat());                 // nối chuỗi chạy trước khi biết có ghi hay không
        }
        System.out.println("noi chuoi: " + dem + " lan tinh");
        dem = 0;
        for (int i = 0; i < 1000000; i++) {
            log.fine(() -> "gia tri " + tinhDat());           // hàm ngắn: chỉ chạy khi mức FINE bật
        }
        System.out.println("ham ngan: " + dem + " lan tinh");
    }
}""", out="noi chuoi: 1000000 lan tinh\nham ngan: 0 lan tinh")
    chia_doi = prog("ChiaDoi", r"""
public class ChiaDoi {
    static int soLanKiem;

    static boolean ok(int k, int buocLoi) {
        soLanKiem++;
        long acc = 0;
        for (int i = 1; i <= k; i++) {
            acc += (i == buocLoi) ? 7 : 1;                    // bước lỗi cộng 7 thay vì 1
        }
        return acc == k;                                      // bất biến: sau k bước acc = k
    }

    static int timBuocLoi(int n, int buocLoi) {
        int thap = 0, cao = n;                                // ok(thap) đúng, ok(cao) sai
        soLanKiem = 0;
        while (cao - thap > 1) {
            int giua = (thap + cao) / 2;
            if (ok(giua, buocLoi)) {
                thap = giua;
            } else {
                cao = giua;
            }
        }
        return cao;
    }

    public static void main(String[] args) {
        int b1 = timBuocLoi(16, 11);
        System.out.println("n=16: buoc loi " + b1 + ", kiem " + soLanKiem + " lan");
        int b2 = timBuocLoi(1000000, 711111);
        System.out.println("n=1000000: buoc loi " + b2 + ", kiem " + soLanKiem + " lan");
    }
}""", out="n=16: buoc loi 11, kiem 4 lan\nn=1000000: buoc loi 711111, kiem 20 lan")
    nuot = prog("NuotLoi", r"""
public class NuotLoi {
    static long doc(String s) {
        try {
            return Long.parseLong(s);
        } catch (Exception e) {
            return 0;                                         // nuốt lỗi: trả 0 như không có gì
        }
    }

    public static void main(String[] args) {
        long tong = doc("500000") + doc("2tr") + doc("300000");
        System.out.println("Tong: " + tong);
    }
}""", out="Tong: 800000")
    che = prog("CheThe", r"""
public class CheThe {
    static String che(String pan) {
        return pan.substring(0, 6) + "******" + pan.substring(pan.length() - 4);
    }

    public static void main(String[] args) {
        String pan = "4111111111111111";                      // số thẻ thử nghiệm công khai
        System.out.println("SAI : thanh toan the " + pan);
        System.out.println("DUNG: thanh toan the " + che(pan));
    }
}""", out="SAI : thanh toan the 4111111111111111\nDUNG: thanh toan the 411111******1111")
    loi = prog("TongPhi", TONG_PHI_LOI, out="So giao dich: 5", expect="runtime_error:ArrayIndexOutOfBoundsException",
               err='Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5\n\tat TongPhi.tongPhi(TongPhi.java:15)\n\tat TongPhi.baoCao(TongPhi.java:22)\n\tat TongPhi.main(TongPhi.java:26)')
    lab_dung = TONG_PHI_LOI.replace("i <= ds.length", "i < ds.length")
    lab = prog("TongPhi", lab_dung, out="So giao dich: 5\nTong phi: 22000")

    jdb = project("Jdb", {
        "Loi.java": r"""
public class Loi {
    // phí bằng một phần nghìn số tiền (số minh hoạ)
    static long phi(long soTien) {
        return soTien / 1000;
    }

    public static void main(String[] args) {
        long soDu = 100000;
        long phiThu = phi(soDu);
        soDu = soDu - phiThu;
        System.out.println("con " + soDu);
    }
}""",
        "phien.sh": "( echo 'stop at Loi:10'; echo run; sleep 3; echo 'print phiThu'; sleep 1; echo 'print soDu'; sleep 1; echo next; sleep 1; "
                    "echo 'print soDu'; sleep 1; echo cont; sleep 1; echo quit ) | jdb -classpath . Loi 2>&1",
    }, [
        ("javac -g Loi.java", ""),
        ("bash phien.sh | tr -d '\\r' | grep -E 'Breakpoint hit|\\] +[a-zA-Z]+ = '",
         "Breakpoint hit: \"thread=main\", Loi.main(), line=10 bci=9\nmain[1]  phiThu = 100\nmain[1]  soDu = 100000\nmain[1]  soDu = 99900"),
    ])

    write_lab("JV2", "L07", """# Lab JV2 L07 — Đọc dấu vết ngăn xếp và sửa lỗi

Chương trình `TongPhi` (số minh hoạ) tính tổng phí của năm giao dịch. Nó **đang lỗi**:

```java
public class TongPhi {
    static long phi(long soTien) {
        if (soTien <= 1000000) {
            return 1000;
        }
        if (soTien <= 10000000) {
            return 5000;
        }
        return 10000;
    }

    static long tongPhi(long[] ds) {
        long tong = 0;
        for (int i = 0; i <= ds.length; i++) {
            tong += phi(ds[i]);
        }
        return tong;
    }

    static void baoCao(long[] ds) {
        System.out.println("So giao dich: " + ds.length);
        System.out.println("Tong phi: " + tongPhi(ds));
    }

    public static void main(String[] args) {
        baoCao(new long[]{800000, 2500000, 1000000, 12000000, 9000000});
    }
}
```

Chạy bản này sẽ in `So giao dich: 5` rồi dừng với:

```
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5
	at TongPhi.tongPhi(TongPhi.java:15)
	at TongPhi.baoCao(TongPhi.java:22)
	at TongPhi.main(TongPhi.java:26)
```

Việc của bạn:
1. Đọc dấu vết **từ trên xuống**: dòng `at` đầu tiên là nơi nổ. Chỉ ra **số dòng** và **vì sao** chỉ số 5 không hợp lệ với mảng dài 5.
2. Chép chương trình vào `TongPhi.java`, sửa **một chỗ**, chạy lại.
3. Kết quả phải là hai dòng (so với tay: 1 000 + 5 000 + 1 000 + 10 000 + 5 000 = 22 000):

```
So giao dich: 5
Tong phi: 22000
```

Chạy: `javac TongPhi.java && java TongPhi`. Chấm: `bash labs/cham.sh JV2 L07 TongPhi.java`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: đọc dấu vết và sửa lỗi biên chỉ số", practice_steps(
        st, "JV2", "L07",
        """<p><b>Đề</b>: chương trình <code>TongPhi</code> (mã đầy đủ trong <code>de.md</code>) dừng với dấu vết:</p>
<div class="code"><div>Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 …</div><div>	at TongPhi.tongPhi(TongPhi.java:15)</div><div>	at TongPhi.baoCao(TongPhi.java:22)</div></div>
<ol><li>Đọc từ trên xuống: nổ ở dòng nào, vì sao?</li><li>Sửa <b>một chỗ</b>, chạy lại.</li><li>Kết quả phải ra hai dòng như bên dưới.</li></ol>""",
        """Bây giờ tới phần bạn tự làm trên máy. Chương trình trong đề bài dừng với dấu vết ngăn xếp. Hãy đọc từ trên xuống, chỉ ra dòng nổ và vì sao chỉ số năm không hợp lệ với mảng dài năm. Rồi sửa một chỗ và chạy lại.
        Kết quả phải ra hai dòng, và bạn có thể kiểm bằng tay, một nghìn cộng năm nghìn cộng một nghìn cộng mười nghìn cộng năm nghìn. Hãy dừng video và tự làm.""",
        lab["out"], "TongPhi.java",
        """<div class="box key"><b>Nếu kẹt:</b> mảng dài 5 có chỉ số hợp lệ từ 0 tới 4. Dòng số 15 có vòng <code>for</code> với điều kiện <code>i &lt;= ds.length</code>: đổi dấu.
Lời giải: <code>labs/JV2/L07/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, mảng dài năm có chỉ số hợp lệ từ không tới bốn. Ở dòng mười lăm, điều kiện vòng lặp cho phép đi tới năm. Hãy đổi dấu so sánh.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=180), "JV2", "L07")

    sc_hook = sc("hook", "hook", "Hai giờ sáng: chương trình dừng, màn hình chỉ có một đống dòng chữ", [
        st(code_block(dau_vet, lines=(20, 20)) + out_block(dau_vet),
           """Hai giờ sáng, chương trình báo cáo dừng giữa chừng và màn hình đầy những dòng chữ lạ. Người mới thường nhìn lướt rồi hoảng, hoặc đoán mò và sửa bừa. Nhưng đống chữ đó là lời khai của chương trình, chỉ ra đúng dòng nào nổ và ai đã gọi tới đó.
           Học cách đọc nó, kèm vài dụng cụ, thì phần lớn lỗi tìm ra trong vài phút."""),
        st("""<div class="box key">Hôm nay: <b>gỡ lỗi</b>. Đọc <b>dấu vết ngăn xếp</b> nhiều tầng, kể cả phần <b>nguyên nhân gốc</b>; ghi <b>nhật ký</b> có mức độ; <b>khoanh vùng bằng chia đôi</b>;
và dừng chương trình giữa chừng bằng <b>trình gỡ lỗi</b>. Kèm hai câu hỏi quy mô: nhật ký phình bao nhiêu mỗi ngày, và tìm lỗi trong một triệu bước mất mấy lần kiểm?</div>""",
           """Hôm nay ta học gỡ lỗi. Đọc dấu vết ngăn xếp nhiều tầng, kể cả phần nguyên nhân gốc. Ghi nhật ký có mức độ. Khoanh vùng bằng chia đôi. Và dừng chương trình giữa chừng bằng trình gỡ lỗi. Kèm hai câu hỏi quy mô, nhật ký phình bao nhiêu mỗi ngày, và tìm lỗi trong một triệu bước mất mấy lần kiểm.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: hàm gọi hàm, ngoại lệ và dòng lệnh", [
        st(table(["điều đã biết", "nhắc lại"],
                 [["① hàm gọi hàm", "<code>main</code> gọi <code>baoCao</code>, nó gọi <code>trungBinh</code>, nó gọi <code>chia</code>: mỗi lần gọi là một <b>tầng</b> mới chồng lên"],
                  ["② ngoại lệ", "<code>throw</code> làm chương trình thoát ra khỏi từng tầng cho tới khi có <code>catch</code> bắt; không ai bắt thì chương trình dừng"],
                  ["③ chia nguyên", "<code>tong / 0</code> với số nguyên ném <code>ArithmeticException</code>"],
                  ["④ dòng lệnh", "<code>javac</code> biên dịch, <code>java</code> chạy, <code>|</code> nối đầu ra, <code>grep</code> lọc dòng có mẫu"]]),
           """Ta ôn lại bốn điều. Hàm gọi hàm thì mỗi lần gọi là một tầng mới chồng lên tầng trước. Ngoại lệ làm chương trình thoát khỏi từng tầng cho tới khi có nơi bắt, và nếu không ai bắt thì chương trình dừng. Chia số nguyên cho không ném ngoại lệ số học.
           Và trên dòng lệnh, ta biên dịch, chạy, nối đầu ra và lọc dòng bằng mẫu.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã sáu thứ của gỡ lỗi", [
        st(table(["thấy", "nghĩa"],
                 [["<code>at DauVet.chia(DauVet.java:3)</code>", "<b>một tầng</b> của ngăn xếp: hàm <code>chia</code> trong tệp <code>DauVet.java</code>, <b>dòng số 3</b>"],
                  ["dòng <code>at</code> đầu tiên", "nơi lỗi <b>xảy ra</b>; các dòng dưới là <b>ai đã gọi</b> tới đó, từ gần tới xa"],
                  ["<code>Caused by: …</code>", "<b>nguyên nhân gốc</b>: lỗi ban đầu bị một lỗi khác bọc lại; gốc thường nằm ở <b>cuối</b> dấu vết"],
                  ["mức nhật ký", "<code>FINE</code> &lt; <code>INFO</code> &lt; <code>WARNING</code> &lt; <code>SEVERE</code>: đặt ngưỡng thì mức thấp hơn ngưỡng bị bỏ"],
                  ["điểm dừng (breakpoint)", "dòng mã mà trình gỡ lỗi <b>dừng chương trình</b> để bạn xem biến; <code>jdb</code> là trình gỡ lỗi có sẵn trong JDK"],
                  ["chia đôi (bisect)", "khoanh vùng lỗi bằng cách <b>kiểm điểm giữa</b>, loại một nửa vùng nghi ngờ mỗi lần"]]),
           """Bảng này có sáu thứ. Mỗi dòng chữ có từ at là một tầng của ngăn xếp, cho biết hàm, tệp và số dòng. Dòng đầu tiên là nơi lỗi xảy ra, các dòng dưới là những ai đã gọi tới đó. Dòng nguyên nhân gốc cho biết lỗi ban đầu bị lỗi khác bọc lại.
           Mức nhật ký có thứ tự, đặt ngưỡng thì mức thấp hơn bị bỏ. Điểm dừng là dòng mã nơi trình gỡ lỗi dừng chương trình để xem biến. Và chia đôi là khoanh vùng lỗi bằng cách kiểm điểm giữa, loại một nửa mỗi lần.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: tháp các lần gọi, và lỗi leo từ đáy lên", [
        st(svg(1500, 400,
               box(40, 20, 520, 62, "main  (dòng số 20)", C_GRAY, 26), box(40, 98, 520, 62, "baoCao  (dòng số 15)", C_BLUE, 26),
               box(40, 176, 520, 62, "trungBinh  (dòng số 11)", C_BLUE, 26), box(40, 254, 520, 62, "chia  (dòng số 3)  NỔ Ở ĐÂY", C_RED, 26, bold=True),
               arrow(600, 285, 600, 60, "#dc2626"), txt(780, 175, "lỗi leo ngược lên qua", 26, "start", "#dc2626", True),
               txt(780, 215, "từng tầng, tới khi có catch", 26, "start", "#dc2626", True),
               txt(780, 255, "(không có → chương trình dừng)", 26, "start", "#dc2626", True),
               txt(300, 370, "dấu vết in từ tầng NỔ xuống tầng main", 26, "middle", "#1f2937", True)),
           """Hình dung các lần gọi hàm như một chồng khay. Hàm chính gọi báo cáo, báo cáo gọi trung bình, trung bình gọi chia. Khay trên cùng, tức hàm chia, là nơi lỗi xảy ra. Lỗi leo ngược lên qua từng khay, và nếu không có chỗ bắt thì chương trình dừng.
           Dấu vết được in từ khay nổ xuống tới khay đáy, nên dòng đầu là hiện trường, các dòng sau là đường đi tới hiện trường."""),
        st(code_block(boc_loi, lines=(3, 5)) + code_block(boc_loi, lines=(9, 13)),
           """Phức tạp hơn là lỗi bị bọc. Hàm rút ném ngoại lệ trạng thái sai khi số dư không đủ. Hàm chuyển tiền bắt nó, rồi ném một lỗi khác, có thông báo thân thiện, và truyền lỗi gốc làm tham số thứ hai. Cách này giữ lại nguyên nhân gốc.""", clear=True),
        st(out_block(boc_loi) + "<p class='note'>Dòng trên cùng nói <b>cái gì</b> hỏng (chuyển tiền); phần <code>Caused by</code> nói <b>vì sao</b> (số dư âm 50). Số dòng <code>10</code> và <code>4</code> là nơi lỗi gốc thực sự bắt đầu.</p>",
           """Kết quả thật. Dòng trên cùng nói cái gì hỏng, là việc chuyển tiền. Phần nguyên nhân gốc nói vì sao, là số dư sẽ âm năm mươi. Số dòng của lỗi gốc nằm trong phần đó, nên phải kéo xuống đọc tới hết, đừng dừng ở dòng đầu.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: đọc một dấu vết để tìm thủ phạm", [
        st("<p><b>Bước 1.</b> Đọc <b>dòng đầu</b>: loại lỗi và thông báo. <code>ArithmeticException: / by zero</code> &rarr; có <b>phép chia cho 0</b>.</p>",
           """Bước một, đọc dòng đầu. Loại lỗi là ngoại lệ số học, thông báo nói chia cho không. Vậy ta biết có một phép chia mà mẫu số bằng không, chưa biết ở đâu.""", clear=True),
        st("<p><b>Bước 2.</b> Dòng <code>at</code> <b>đầu tiên</b> chỉ <b>hàm và dòng</b> nổ: <code>DauVet.chia(DauVet.java:3)</code> &rarr; mở tệp, dòng số 3: <code>return tong / soLuong;</code>.</p>"
           "<p>Vì sao đủ để biết <i>nơi nổ</i> nhưng chưa đủ để biết <i>nơi sai</i>: <code>chia</code> chỉ làm đúng việc của nó.</p>",
           """Bước hai, dòng đầu tiên chỉ ra hàm và số dòng nổ. Mở tệp tại dòng đó, ta thấy phép chia. Vì hàm chia chỉ làm đúng việc của nó, nên đây mới là nơi nổ, chưa chắc là nơi sai.""", clear=True),
        st("<p><b>Bước 3.</b> Đi <b>xuống các dòng dưới</b> tới hàm do <b>mình viết và quyết định giá trị truyền vào</b>: <code>trungBinh</code> (dòng số 11) truyền <code>ds.length</code> làm mẫu số.</p>"
           "<p>Câu hỏi: khi nào <code>ds.length = 0</code>? &rarr; <code>baoCao</code> (dòng số 15) được gọi với <b>danh sách rỗng</b> từ <code>main</code> (dòng số 20).</p>"
           + table(["tầng", "quyết định gì"], [["<code>chia</code>", "chỉ làm phép chia"], ["<code>trungBinh</code>", "<b>chọn mẫu số</b> = số phần tử"], ["<code>baoCao</code>, <code>main</code>", "<b>chọn danh sách</b> đưa vào"]]),
           """Bước ba, đi xuống các dòng dưới, tới hàm quyết định giá trị truyền vào. Hàm trung bình truyền độ dài danh sách làm mẫu số. Vì phép chia cho không chỉ xảy ra khi độ dài bằng không, nên ta hỏi khi nào điều đó xảy ra, và thấy hàm chính gọi báo cáo với danh sách rỗng.""", clear=True),
        st("<p><b>Bước 4.</b> Sửa đúng chỗ: <b>quyết định</b> trung bình của danh sách rỗng là gì (ví dụ 0, hoặc báo không có dữ liệu), rồi kiểm <code>if (ds.length == 0)</code> ở <code>trungBinh</code>, không sửa trong <code>chia</code>.</p>"
           "<p>Thử: danh sách rỗng &rarr; không còn chia cho 0.</p>",
           """Bước bốn, sửa đúng chỗ. Quyết định trung bình của danh sách rỗng là gì, rồi kiểm điều kiện đó ở hàm trung bình, không sửa trong hàm chia. Vì sao, vì quy tắc nghiệp vụ thuộc về hàm biết ý nghĩa của danh sách, chứ không thuộc về phép chia thuần.""", clear=True),
    ])
    sc_ex = sc("example", "example", "Ví dụ: bốn tầng, hai lần gọi, một lỗi", [
        st(code_block(dau_vet, lines=(2, 12)),
           """Đây là chương trình có bốn tầng. Hàm chia thực hiện phép chia. Hàm trung bình cộng các số rồi gọi hàm chia với độ dài danh sách. Ta sẽ chạy hai lần, một lần với hai số, một lần với danh sách rỗng.""", clear=True),
        st("$$① \\; (500\\,000 + 700\\,000) / 2 = \\hl{600\\,000}$$"
           "<p>Lần đầu: tổng 1 200 000, hai phần tử, trung bình 600 000.</p>"
           "$$② \\; \\text{danh sách rỗng}: 0 / 0 \\;\\Rightarrow\\; \\text{không xác định}$$",
           """Phép làm thứ nhất, lần gọi đầu tiên có hai số, tổng một triệu hai trăm nghìn, trung bình sáu trăm nghìn. Phép thứ hai, danh sách rỗng thì tổng bằng không và độ dài bằng không, phép chia không xác định.""", clear=True),
        st(code_block(dau_vet, lines=(14, 21)),
           """Phép thứ ba, chạy thật hai lần gọi trong hàm chính, một lần với hai số và một lần với danh sách rỗng.""", clear=True),
        st(out_block(dau_vet),
           """Dòng đầu in sáu trăm nghìn như tính tay. Lần gọi thứ hai nổ với dấu vết bốn tầng. Tầng đầu là hàm chia ở dòng ba. Rồi hàm trung bình ở dòng mười một, hàm báo cáo ở dòng mười lăm, và hàm chính ở dòng hai mươi.""", clear=True),
        st("<p><b>④ Đọc ngược:</b> dòng số 20 cho thấy <b>lần gọi thứ hai</b> là lần nổ; <code>new long[]{}</code> là đầu vào <b>rỗng</b>.</p>"
           "<p><b>⑤ Kết luận:</b> lỗi không nằm ở phép chia mà ở chỗ <b>chưa quyết định</b> điều gì xảy ra với danh sách rỗng. Dấu vết đã chỉ đường trong <b>bốn dòng</b>.</p>",
           """Phép thứ tư, đọc ngược. Dòng hai mươi cho thấy lần gọi thứ hai là lần nổ, với đầu vào rỗng. Phép thứ năm, kết luận là lỗi không nằm ở phép chia mà ở chỗ chưa quyết định điều gì xảy ra với danh sách rỗng. Dấu vết đã chỉ đường trong bốn dòng.""", clear=True),
    ], checks=["(500000 + 700000) // 2 == 600000", "500000 + 700000 == 1200000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: dừng chương trình giữa chừng bằng trình gỡ lỗi", [
        st("<p>Cách khác: không đoán, mà <b>dừng chương trình ở dòng số 10</b> và hỏi giá trị biến. Các lệnh gõ ở dấu nhắc của <code>jdb</code>:</p>"
           + table(["lệnh", "việc làm"], [["<code>stop at Loi:10</code>", "đặt điểm dừng ở dòng số 10"], ["<code>run</code>", "chạy tới điểm dừng"],
                                           ["<code>print soDu</code>", "in giá trị biến <code>soDu</code>"], ["<code>next</code>", "chạy <b>đúng một dòng</b> rồi dừng lại"]])
           + "<p class='note'>Biên dịch bằng <code>javac -g</code> để jdb thấy tên biến.</p>",
           """Cách kiểm khác là không đoán mà dừng chương trình giữa chừng. Trình gỡ lỗi có sẵn trong bộ công cụ cho phép đặt điểm dừng ở một dòng, chạy tới đó, rồi in giá trị biến. Lệnh tiếp theo chạy đúng một dòng rồi dừng lại. Ta biên dịch với cờ g để nó thấy tên biến.""", clear=True),
        st(term_block(jdb, 0, 2, title="Một phiên jdb (các lệnh gõ sẵn trong phien.sh; chỉ lọc ra các dòng chính)")
           + "<p>Kiểm tay: phí = 100 000 / 1 000 = <b>100</b>; số dư sau trừ phí = 100 000 − 100 = <b>99 900</b> ✓ khớp phiên jdb.</p>",
           """Phiên chạy thật cho thấy chương trình dừng ở dòng mười. Phí là một trăm, số dư trước dòng đó là một trăm nghìn. Sau lệnh chạy một dòng, số dư thành chín mươi chín nghìn chín trăm. Tính tay một trăm nghìn trừ một trăm cũng ra đúng chín mươi chín nghìn chín trăm.
           Hai cách độc lập cho cùng kết quả, nên ta tin vào con số.""", clear=True),
    ], checks=["100000 // 1000 == 100", "100000 - 100 == 99900"])
    sc_nk = sc("nhatky", "concept", "Nhật ký: người quan sát khi bạn không có mặt", [
        st(code_block(nhat_ky, lines=(9, 13)),
           """Trên máy chủ không ai đứng gỡ lỗi, nên ta ghi nhật ký. Khác với lệnh in thường, nhật ký có mức độ. Ta tự định dạng mỗi dòng gồm mức và thông điệp để kết quả luôn giống nhau, thay vì in kèm giờ như mặc định.""", clear=True),
        st(code_block(nhat_ky, lines=(21, 27)) + out_block(nhat_ky),
           """Ta đặt ngưỡng ở mức thông tin. Dòng chi tiết bị bỏ, vì mức chi tiết thấp hơn ngưỡng. Ba dòng còn lại được in. Rồi ta hạ ngưỡng xuống, bật mọi mức, và dòng chi tiết thứ hai xuất hiện. Ở môi trường thật, ta bật mức thấp khi cần điều tra mà không phải sửa mã.""", clear=True),
    ])
    sc_scale = sc("scale", "concept", "Khi hệ thống lớn dần: nhật ký phình, và lỗi nằm trong cả triệu bước", [
        st(table(["giao dịch mỗi giây", "100", "10 000", "1 000 000"],
                 [["nhật ký mỗi ngày (3 dòng × 200 byte mỗi giao dịch, số minh hoạ)", "≈ 5,2 GB", "<b>≈ 518 GB</b>", "<b>≈ 51,8 TB</b>"],
                  ["số dòng mỗi ngày", "≈ 26 triệu", "≈ 2,6 tỉ", "≈ 259 tỉ"]])
           + "<p class='note'>Vì thế ngưỡng mặc định là <code>INFO</code>, mức chi tiết bật khi cần, và không bao giờ ghi dữ liệu nhạy cảm.</p>",
           """Về quy mô. Giả sử mỗi giao dịch ghi ba dòng, mỗi dòng hai trăm byte, số minh hoạ. Một trăm giao dịch mỗi giây là hơn năm gigabyte mỗi ngày. Mười nghìn giao dịch mỗi giây là hơn năm trăm gigabyte. Một triệu giao dịch mỗi giây là hơn năm mươi nghìn gigabyte mỗi ngày.
           Vì thế ngưỡng mặc định là mức thông tin, mức chi tiết chỉ bật khi cần.""", clear=True),
        st(code_block(log_dat, lines=(15, 22)) + out_block(log_dat),
           """Còn chi phí ẩn. Dòng ghi mức chi tiết bị tắt, nhưng nếu ta nối chuỗi ngay trong lời gọi thì phép tính tốn kém vẫn chạy một triệu lần, vì nối chuỗi chạy trước khi biết có ghi hay không. Dùng hàm ngắn thì phép tính chỉ chạy khi mức đó bật, nên là không lần nào.""", clear=True),
        st(code_block(chia_doi, lines=(4, 10)),
           """Câu hỏi quy mô thứ hai, lỗi nằm trong một triệu bước thì tìm thế nào. Ta giả lập một chuỗi bước, mỗi bước lẽ ra cộng một, nhưng có một bước lỗi cộng bảy. Bất biến là sau k bước thì tổng đúng bằng k.""", clear=True),
        st(code_block(chia_doi, lines=(16, 23)),
           """Ta kiểm bất biến ở điểm giữa. Đúng thì lỗi nằm sau điểm giữa, sai thì lỗi nằm trước hoặc ngay tại đó. Mỗi lần kiểm điểm giữa, vùng nghi ngờ giảm một nửa.""", clear=True),
        st(out_block(chia_doi) + table(["số bước n", "16", "1 000 000", "1 000 000 000"], [["số lần kiểm khi chia đôi ≈ log₂ n", "4", "20", "<b>30</b>"], ["số lần kiểm khi duyệt từ đầu", "tới 16", "tới 1 000 000", "tới 1 000 000 000"]]),
           """Kết quả thật. Mười sáu bước cần bốn lần kiểm. Một triệu bước chỉ cần hai mươi lần. Một tỉ bước chỉ cần ba mươi lần, trong khi duyệt từ đầu có thể phải tới một tỉ lần. Lệnh chia đôi của hệ quản lý phiên bản dùng đúng ý này để tìm lần chốt gây lỗi, với điều kiện bất biến phải kiểm được và đơn điệu.""", clear=True),
    ], checks=["3 * 200 * 100 * 86400 == 5184000000", "3 * 200 * 10000 * 86400 == 518400000000", "3 * 200 * 1000000 * 86400 == 51840000000000",
               "100 * 3 * 86400 == 25920000", "10000 * 3 * 86400 == 2592000000", "1000000 * 3 * 86400 == 259200000000",
               "__import__('math').ceil(__import__('math').log2(16)) == 4", "__import__('math').ceil(__import__('math').log2(1000000)) == 20",
               "__import__('math').ceil(__import__('math').log2(1000000000)) == 30"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Nuốt lỗi: <code>catch</code> rồi trả giá trị mặc định.</div>'
           + code_block(nuot, lines=(2, 8)) + code_block(nuot, lines=(11, 12)) + out_block(nuot),
           """Lỗi thứ nhất là nuốt lỗi. Hàm đọc số bắt mọi ngoại lệ và trả không như chưa có gì xảy ra. Chuỗi hai chữ t r lẫn vào số không phải số, nhưng chương trình vẫn in tổng tám trăm nghìn, thiếu hai triệu mà không ai biết. Tệ hơn cả lỗi nổ, vì không có dấu vết nào để đọc."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Ghi dữ liệu nhạy cảm vào nhật ký.</div>'
           + code_block(che, lines=(2, 9)) + out_block(che),
           """Lỗi thứ hai hay gặp ở người đã đi làm. Nhật ký thường được nhiều người đọc và lưu rất lâu, nên ghi nguyên số thẻ là rò rỉ dữ liệu. Chuẩn bảo mật thẻ thanh toán chỉ cho hiển thị tối đa sáu số đầu và bốn số cuối. Hãy che phần giữa trước khi ghi.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nối chuỗi trong lời gọi nhật ký dù mức đã tắt: phép tính vẫn chạy.</div>'
           + out_block(log_dat) + "<p class='note'>Quy tắc: thông điệp tốn kém phải nằm trong <b>hàm ngắn</b> để chỉ tính khi mức bật.</p>",
           """Lỗi thứ ba cũng của người đã đi làm, đã thấy ở trên. Nối chuỗi ngay trong lời gọi nhật ký, thì dù mức đã tắt phép tính vẫn chạy. Một triệu lần phép tính tốn kém cho một dòng không bao giờ được ghi. Quy tắc là đặt thông điệp tốn kém trong hàm ngắn.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<div class="code"><div>Exception in thread "main" java.lang.IllegalStateException: khong the huy lenh</div><div>	at Lenh.huy(Lenh.java:30)</div><div>	at Dich.xuLy(Dich.java:12)</div><div>	at App.main(App.java:5)</div><div>Caused by: java.lang.NullPointerException: lenh la null</div><div>	at Kho.tim(Kho.java:8)</div><div>	at Lenh.huy(Lenh.java:28)</div><div>	... 2 more</div></div>
<ol><li>Lỗi <b>gốc</b> là gì, ở tệp nào, dòng nào?</li><li>Chọn <b>A hay B</b> để sửa: A thêm <code>catch</code> bắt <code>NullPointerException</code> trong <code>main</code>; B kiểm <code>null</code> ở <code>Kho.tim</code> hoặc nơi gọi nó. Vì sao?</li></ol>""",
           """Bây giờ tới phần bạn tự làm. Đây là một dấu vết có nguyên nhân gốc. Hãy chỉ ra lỗi gốc là gì, ở tệp nào, dòng nào. Rồi chọn giữa thêm một chỗ bắt lỗi ở hàm chính, và kiểm giá trị rỗng ở nơi tìm lệnh, và giải thích vì sao. Hãy dừng video và tự làm.""", pause=25),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "<b>NullPointerException</b> ở <b>Kho.java dòng số 8</b>", "phần <code>Caused by</code> là gốc; dòng trên cùng chỉ là lỗi bọc bên ngoài"],
                  ["2", "<b>B</b>", "bắt ở <code>main</code> chỉ che lỗi, không sửa nguyên nhân (không tìm thấy lệnh); sửa tại nơi dữ liệu sai sinh ra"]]),
           """Đáp án, lỗi gốc là ngoại lệ giá trị rỗng, ở tệp kho, dòng tám. Phần nguyên nhân gốc mới là nguồn, còn dòng trên cùng chỉ là lỗi bọc bên ngoài. Câu hai chọn phương án B, vì bắt lỗi ở hàm chính chỉ che lỗi, còn nguyên nhân là không tìm thấy lệnh vẫn còn nguyên.""",
           focus=[1, "1.2", "1.3"]),
        st("""<div class="box key"><b>Quy tắc:</b> đọc dấu vết <b>từ trên xuống</b> để biết hiện trường, rồi <b>xuống tới Caused by</b> để biết nguyên nhân; sửa ở <b>nơi dữ liệu sai sinh ra</b>, không sửa nơi nó nổ.</div>""",
           """Quy tắc rút ra. Đọc từ trên xuống để biết hiện trường, rồi xuống tới nguyên nhân gốc. Và sửa ở nơi dữ liệu sai sinh ra, không sửa ở nơi nó nổ."""),
    ])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("dòng đầu: loại lỗi", "dòng at đầu: nơi nổ", "xuống: ai gọi", "Caused by: nguyên nhân gốc", "nhật ký có mức, không ghi dữ liệu nhạy cảm",
                 "chia đôi: log₂ n lần kiểm"),
           """Tổng kết chuỗi logic. Dòng đầu cho biết loại lỗi. Dòng đầu tiên có chữ at là nơi nổ. Các dòng dưới cho biết ai đã gọi. Phần nguyên nhân gốc mới là gốc của lỗi. Nhật ký có mức độ và không ghi dữ liệu nhạy cảm.
           Và khoanh vùng bằng chia đôi chỉ cần chừng lôgarit cơ số hai của n lần kiểm."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng đoán; <b>đọc bằng chứng</b> theo thứ tự (dòng đầu, nơi nổ, đường đi, nguyên nhân gốc), <b>chia đôi</b> khi không còn bằng chứng,
và để lại <b>nhật ký</b> đủ dùng mà không phình, không lộ.</div>""",
           """Điều cần mang theo. Đừng đoán, hãy đọc bằng chứng theo thứ tự. Khi không còn bằng chứng thì chia đôi. Và để lại nhật ký đủ dùng, mà không phình và không để lộ."""),
    ])
    return lesson("L07", "go_loi_dau_vet_nhat_ky", "Bài 7 — Gỡ lỗi: dấu vết ngăn xếp, nhật ký, chia đôi, trình gỡ lỗi",
                  "curriculum/jv2.yaml L07; audit/jv2/verify_jv2.py L07 (javac/java/jdb chạy thật, JDK 21; phiên jdb dùng javac -g); "
                  "Throwable.printStackTrace và getCause (Java SE 21 API: định dạng 'Caused by', '... n more'); java.util.logging (Java SE 21 API: mức, Logger.fine(Supplier)); "
                  "jdb (JDK 21 tools: stop at, run, print, next); PCI DSS (PCI Security Standards Council): hiển thị tối đa sáu số đầu và bốn số cuối của PAN; "
                  "Git: git bisect (git-scm.com/docs/git-bisect); dev.java/learn",
                  ["Đọc dấu vết ngăn xếp nhiều tầng, kể cả phần nguyên nhân gốc, để tìm hiện trường và thủ phạm",
                   "Dùng điểm dừng của jdb để dừng chương trình và kiểm giá trị biến",
                   "Nêu cách ghi nhật ký có mức độ và vì sao không ghi dữ liệu nhạy cảm",
                   "Nhận ra nhật ký phình theo tải và chia đôi chỉ cần log₂ n lần kiểm",
                   "Sửa chương trình lỗi biên chỉ số dựa trên dấu vết và chạy lại cho ra kết quả đúng"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_nk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "example"), (2, "check"), (3, "nhatky"), (4, "scale"), (5, "practice")])
