from lib import *
from labkit import write_lab, practice_steps, practice_scene

N_LON = 1000000
_dau = lambda i: (-1 if i % 3 == 0 else 1) * (i % 7 + 1) * 1000
TONG_LON = sum(_dau(i) for i in range(1, N_LON + 1))

CSV_OK = """ma,ngay,tai_khoan,loai,so_tien
1,2026-01-05,A01,nap,5000000
2,2026-01-07,A02,nap,3000000
3,2026-01-10,A01,rut,1200000
4,2026-01-15,A03,nap,800000
5,2026-02-02,A02,rut,500000
6,2026-02-09,A01,nap,2500000
7,2026-02-20,A03,rut,300000
8,2026-03-01,A02,nap,1000000"""
CSV_LOI = """ma,ngay,tai_khoan,loai,so_tien
1,2026-01-05,A01,nap,5000000
2,2026-01-07,A02,nap,3000000
3,2026-01-10,A01,rut,abc
4,2026-01-15,A03,nap,800000
5,2026-02-02,A02,doi,500000
6,2026-02-09,A01,nap,2500000
7,2026-02-20,A03,rut,300000
8,2026-03-01,A02,nap,1000000"""

F_GD = r"""
package soc;

import java.time.LocalDate;
import java.time.format.DateTimeParseException;

public record GiaoDich(String ma, LocalDate ngay, String taiKhoan, String loai, long soTien) {
    public static GiaoDich phanTich(String dong) {
        String[] f = dong.split(",", -1);
        if (f.length != 5) {
            throw new IllegalArgumentException("so cot khong dung");
        }
        long tien;
        try {
            tien = Long.parseLong(f[4].trim());
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("so tien khong hop le: " + f[4]);
        }
        if (tien <= 0) {
            throw new IllegalArgumentException("so tien phai duong: " + tien);
        }
        if (!f[3].equals("nap") && !f[3].equals("rut")) {
            throw new IllegalArgumentException("loai khong hop le: " + f[3]);
        }
        try {
            return new GiaoDich(f[0], LocalDate.parse(f[1]), f[2], f[3], tien);
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("ngay khong hop le: " + f[1]);
        }
    }

    public long dau() {
        return loai.equals("nap") ? soTien : -soTien;
    }
}"""
F_NK = r"""
package soc;

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

    static final Logger LOG = Logger.getLogger("soc");
    static final Handler H = new StreamHandler(System.out, new DinhDang());

    static {
        LOG.setUseParentHandlers(false);
        H.setLevel(Level.ALL);
        LOG.addHandler(H);
    }

    public static void canhBao(String thongDiep) {
        LOG.warning(thongDiep);
        H.flush();
    }
}"""
F_DOC = r"""
package soc;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.function.Consumer;

public class DocSoCai {
    public static int duyet(Path p, Consumer<GiaoDich> khiDoc) throws IOException {
        int loi = 0;
        try (BufferedReader br = Files.newBufferedReader(p)) {
            br.readLine();                                        // bỏ dòng tiêu đề
            String dong;
            int so = 1;
            while ((dong = br.readLine()) != null) {
                so++;
                try {
                    khiDoc.accept(GiaoDich.phanTich(dong));
                } catch (IllegalArgumentException e) {
                    loi++;
                    NhatKy.canhBao("dong " + so + ": " + e.getMessage());
                }
            }
        }
        return loi;
    }
}"""
F_BC = r"""
package soc;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class BaoCao {
    public static Map<String, Long> soDu(List<GiaoDich> ds) {
        return ds.stream().collect(Collectors.groupingBy(
                GiaoDich::taiKhoan, TreeMap::new, Collectors.summingLong(GiaoDich::dau)));
    }

    public static Map<String, Long> theoThang(List<GiaoDich> ds) {
        return ds.stream().collect(Collectors.groupingBy(
                g -> g.ngay().toString().substring(0, 7), TreeMap::new, Collectors.summingLong(GiaoDich::dau)));
    }

    public static long tong(List<GiaoDich> ds, String loai) {
        return ds.stream().filter(g -> g.loai().equals(loai)).mapToLong(GiaoDich::soTien).sum();
    }
}"""
F_TH = r"""
package soc;

import java.util.Map;
import java.util.TreeMap;

public class TongHop {
    public final Map<String, Long> soDu = new TreeMap<>();
    public long nap, rut;

    public void them(GiaoDich g) {
        soDu.merge(g.taiKhoan(), g.dau(), Long::sum);
        if (g.loai().equals("nap")) {
            nap += g.soTien();
        } else {
            rut += g.soTien();
        }
    }
}"""
F_APP = r"""
package soc;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class App {
    public static void main(String[] args) throws Exception {
        List<GiaoDich> ds = new ArrayList<>();
        int loi = DocSoCai.duyet(Path.of(args[0]), ds::add);
        System.out.println("Doc " + (ds.size() + loi) + " dong: " + ds.size() + " hop le, " + loi + " loi");
        Map<String, Long> soDu = BaoCao.soDu(ds);
        soDu.forEach((tk, tien) -> System.out.println("Tai khoan " + tk + ": " + tien));
        long tong = soDu.values().stream().mapToLong(Long::longValue).sum();
        long nap = BaoCao.tong(ds, "nap"), rut = BaoCao.tong(ds, "rut");
        System.out.println("Tong so du: " + tong);
        System.out.println("Kiem tra: nap " + nap + " - rut " + rut + " = " + (nap - rut)
                + (tong == nap - rut ? " (khop)" : " (LECH)"));
        System.out.println("Theo thang: " + BaoCao.theoThang(ds));
    }
}"""
F_DONG = r"""
package soc;

import java.nio.file.Path;

public class AppDong {
    public static void main(String[] args) throws Exception {
        TongHop t = new TongHop();
        int loi = DocSoCai.duyet(Path.of(args[0]), t::them);      // gom ngay khi đọc, không giữ danh sách
        long tong = t.soDu.values().stream().mapToLong(Long::longValue).sum();
        System.out.println("So tai khoan: " + t.soDu.size() + ", dong loi: " + loi);
        System.out.println("Tong so du: " + tong + (tong == t.nap - t.rut ? " (khop)" : " (LECH)"));
    }
}"""
F_SONG = r"""
package soc;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class AppSong {
    public static void main(String[] args) throws Exception {
        Path p = Path.of(args[0]);
        Map<String, Long> song;
        try (Stream<String> dong = Files.lines(p)) {
            song = dong.skip(1).parallel().map(d -> d.split(",")).collect(Collectors.groupingByConcurrent(
                    f -> f[2], Collectors.summingLong(f -> f[3].equals("nap") ? Long.parseLong(f[4]) : -Long.parseLong(f[4]))));
        }
        TongHop t = new TongHop();
        DocSoCai.duyet(p, t::them);
        System.out.println("song song khop tuan tu: " + song.equals(t.soDu));
    }
}"""
F_KT = r"""
package soc;

import java.util.List;

public class KiemTra {
    static int dat, hong;

    static void kiem(String ten, boolean ok) {
        if (ok) {
            dat++;
            System.out.println("DAT  " + ten);
        } else {
            hong++;
            System.out.println("HONG " + ten);
        }
    }

    static boolean nemLoi(String dong) {
        try {
            GiaoDich.phanTich(dong);
            return false;
        } catch (IllegalArgumentException e) {
            return true;
        }
    }

    public static void main(String[] args) {
        GiaoDich g = GiaoDich.phanTich("1,2026-01-05,A01,nap,5000000");
        GiaoDich r = GiaoDich.phanTich("2,2026-01-06,A01,rut,300");
        kiem("doc dong hop le", g.soTien() == 5000000 && g.taiKhoan().equals("A01"));
        kiem("rut co dau am", r.dau() == -300);
        kiem("so tien khong phai so", nemLoi("3,2026-01-07,A01,nap,abc"));
        kiem("loai la", nemLoi("4,2026-01-08,A01,gui,100"));
        kiem("thieu cot", nemLoi("5,2026-01-09,A01,nap"));
        kiem("so tien am", nemLoi("6,2026-01-10,A01,nap,-500"));
        kiem("so du A01", BaoCao.soDu(List.of(g, r)).get("A01") == 4999700L);
        System.out.println("dat " + dat + ", hong " + hong);
    }
}"""
F_TIEUDE = r"""
package soc;

public class ThuTieuDe {
    public static void main(String[] args) {
        try {
            GiaoDich.phanTich("ma,ngay,tai_khoan,loai,so_tien");   // quên bỏ dòng tiêu đề
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }
    }
}"""
F_TAO = r"""
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class TaoSoCai {
    public static void main(String[] args) throws IOException {
        int n = Integer.parseInt(args[0]);
        try (BufferedWriter w = Files.newBufferedWriter(Path.of("lon.csv"))) {
            w.write("ma,ngay,tai_khoan,loai,so_tien\n");
            for (int i = 1; i <= n; i++) {
                w.write(i + ",2026-01-05,A" + String.format("%02d", i % 100) + "," + (i % 3 == 0 ? "rut" : "nap")
                        + "," + (i % 7 + 1) * 1000 + "\n");
            }
        }
        System.out.println("da ghi " + n + " dong");
    }
}"""

LAB_CSV = ("ma,ngay,tai_khoan,loai,so_tien\n1,2026-03-02,B01,nap,4000000\n2,2026-03-04,B02,nap,2500000\n3,2026-03-09,B01,rut,900000\n"
           "4,2026-03-11,B02,rut,abc\n5,2026-04-01,B03,nap,1500000\n6,2026-04-05,B01,gui,100000\n7,2026-04-12,B02,rut,700000")


def build():
    files = {"src/soc/GiaoDich.java": F_GD, "src/soc/NhatKy.java": F_NK, "src/soc/DocSoCai.java": F_DOC, "src/soc/BaoCao.java": F_BC,
             "src/soc/TongHop.java": F_TH, "src/soc/App.java": F_APP, "src/soc/AppDong.java": F_DONG, "src/soc/AppSong.java": F_SONG,
             "src/soc/KiemTra.java": F_KT, "src/soc/ThuTieuDe.java": F_TIEUDE, "TaoSoCai.java": F_TAO,
             "so_cai.csv": CSV_OK, "so_cai_loi.csv": CSV_LOI}
    OUT_OK = ("Doc 8 dong: 8 hop le, 0 loi\nTai khoan A01: 6300000\nTai khoan A02: 3500000\nTai khoan A03: 500000\nTong so du: 10300000\n"
              "Kiem tra: nap 12300000 - rut 2000000 = 10300000 (khop)\nTheo thang: {2026-01=7600000, 2026-02=1700000, 2026-03=1000000}")
    OUT_LOI = ("[WARNING] dong 4: so tien khong hop le: abc\n[WARNING] dong 6: loai khong hop le: doi\nDoc 8 dong: 6 hop le, 2 loi\n"
               "Tai khoan A01: 7500000\nTai khoan A02: 4000000\nTai khoan A03: 500000\nTong so du: 12000000\n"
               "Kiem tra: nap 12300000 - rut 300000 = 12000000 (khop)\nTheo thang: {2026-01=8800000, 2026-02=2200000, 2026-03=1000000}")
    KT_OUT = ("DAT  doc dong hop le\nDAT  rut co dau am\nDAT  so tien khong phai so\nDAT  loai la\nDAT  thieu cot\nDAT  so tien am\nDAT  so du A01\n"
              "dat 7, hong 0")
    du_an = project("SoCai", files, [
        ("javac -d out src/soc/*.java TaoSoCai.java", ""),
        ("java -cp out soc.KiemTra", KT_OUT),
        ("java -cp out soc.App so_cai.csv", OUT_OK),
        ("java -cp out soc.App so_cai_loi.csv", OUT_LOI),
        ("tail -n +2 so_cai_loi.csv | wc -l", "8"),
        ("java -cp out soc.ThuTieuDe", "so tien khong hop le: so_tien"),
        (f"java -cp out TaoSoCai {N_LON}", f"da ghi {N_LON} dong"),
        ("java -Xmx32m -cp out soc.App lon.csv 2>&1 | grep -m1 -o OutOfMemoryError", "OutOfMemoryError"),
        ("java -Xmx32m -cp out soc.AppDong lon.csv", f"So tai khoan: 100, dong loi: 0\nTong so du: {TONG_LON} (khop)"),
        ("java -Xmx64m -cp out soc.AppSong lon.csv 2>&1 | grep -m1 -o OutOfMemoryError", "OutOfMemoryError"),
        ("java -Xmx128m -cp out soc.AppSong lon.csv", "song song khop tuan tu: true"),
        ("sed -i 's/tien <= 0/false/' src/soc/GiaoDich.java", ""),
        ("javac -d out src/soc/*.java && java -cp out soc.KiemTra | grep -v DAT",
         "HONG so tien am\ndat 6, hong 1"),
    ])

    lab = prog("SoCaiNho", r"""
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.TreeMap;

public class SoCaiNho {
    record GiaoDich(String taiKhoan, String loai, long soTien) {
        static GiaoDich phanTich(String dong) {
            String[] f = dong.split(",", -1);
            long tien;
            try {
                tien = Long.parseLong(f[4].trim());
            } catch (NumberFormatException e) {
                throw new IllegalArgumentException("so tien khong hop le");
            }
            if (!f[3].equals("nap") && !f[3].equals("rut")) {
                throw new IllegalArgumentException("loai khong hop le");
            }
            return new GiaoDich(f[2], f[3], tien);
        }
    }

    public static void main(String[] args) throws IOException {
        Path p = Path.of("so_cai.csv");
        Files.writeString(p, "ma,ngay,tai_khoan,loai,so_tien\n1,2026-03-02,B01,nap,4000000\n2,2026-03-04,B02,nap,2500000\n"
                + "3,2026-03-09,B01,rut,900000\n4,2026-03-11,B02,rut,abc\n5,2026-04-01,B03,nap,1500000\n"
                + "6,2026-04-05,B01,gui,100000\n7,2026-04-12,B02,rut,700000\n");
        Map<String, Long> soDu = new TreeMap<>();
        long nap = 0, rut = 0;
        try (BufferedReader br = Files.newBufferedReader(p)) {
            br.readLine();
            String dong;
            int so = 1;
            while ((dong = br.readLine()) != null) {
                so++;
                try {
                    GiaoDich g = GiaoDich.phanTich(dong);
                    soDu.merge(g.taiKhoan(), g.loai().equals("nap") ? g.soTien() : -g.soTien(), Long::sum);
                    if (g.loai().equals("nap")) {
                        nap += g.soTien();
                    } else {
                        rut += g.soTien();
                    }
                } catch (IllegalArgumentException e) {
                    System.out.println("Bo qua dong " + so + ": " + e.getMessage());
                }
            }
        }
        long tong = 0;
        for (Map.Entry<String, Long> e : soDu.entrySet()) {
            System.out.println(e.getKey() + " " + e.getValue());
            tong += e.getValue();
        }
        System.out.println("Tong " + tong + " khop " + (tong == nap - rut));
    }
}""", out="Bo qua dong 5: so tien khong hop le\nBo qua dong 7: loai khong hop le\nB01 3100000\nB02 1800000\nB03 1500000\nTong 6400000 khop true")
    write_lab("JV2", "L09", """# Lab JV2 L09 — Sổ cái nhỏ: bỏ qua dòng lỗi, in số dư, kiểm bất biến

Viết một tệp `SoCaiNho.java` (một lớp, có thể lồng một `record`). Chương trình tự ghi ra `so_cai.csv` đúng nội dung sau rồi đọc lại:

```
ma,ngay,tai_khoan,loai,so_tien
1,2026-03-02,B01,nap,4000000
2,2026-03-04,B02,nap,2500000
3,2026-03-09,B01,rut,900000
4,2026-03-11,B02,rut,abc
5,2026-04-01,B03,nap,1500000
6,2026-04-05,B01,gui,100000
7,2026-04-12,B02,rut,700000
```

Yêu cầu:
1. Đọc bằng `try (BufferedReader …)`, bỏ dòng tiêu đề, đếm **số dòng của tệp** (tiêu đề là dòng 1).
2. Một hàm `phanTich(dong)` ném `IllegalArgumentException("so tien khong hop le")` khi số tiền không phải số, và `IllegalArgumentException("loai khong hop le")` khi loại không phải `nap` hay `rut`.
3. Dòng lỗi **không làm dừng chương trình**: in `Bo qua dong <số dòng>: <thông điệp>` rồi đọc tiếp.
4. Dòng hợp lệ: số dư theo tài khoản bằng `TreeMap` (`nap` cộng, `rut` trừ); đồng thời cộng riêng tổng nạp và tổng rút.
5. In số dư mỗi tài khoản dạng `B01 3100000`, rồi `Tong <tổng số dư> khop <true/false>` với `khop` là `tổng số dư == tổng nạp − tổng rút`.

Kết quả mong đợi (sáu dòng): hai dòng `Bo qua`, ba dòng số dư, một dòng `Tong`. Tự tính tay trước: B01 = 4 000 000 − 900 000.

Chạy: `javac SoCaiNho.java && java SoCaiNho`. Chấm: `bash labs/cham.sh JV2 L09 SoCaiNho.java`.
""", "java", lab["code"], lab["out"])
    sc_lab = practice_scene(sc, "Tự làm: sổ cái nhỏ có dòng lỗi", pr_steps(
        st, "JV2", "L09",
        """<p><b>Đề</b>: tệp sổ cái 7 dòng (trong <code>de.md</code>), hai dòng lỗi (số tiền <code>abc</code>, loại <code>gui</code>).</p>
<ol><li>Đọc từng dòng, bỏ tiêu đề, đếm số dòng của tệp; <code>phanTich</code> ném <code>IllegalArgumentException</code> khi sai.</li>
<li>Dòng lỗi: in <code>Bo qua dong …: …</code> rồi đọc tiếp; dòng đúng: cộng vào <code>TreeMap</code>.</li>
<li>In số dư từng tài khoản và <code>Tong … khop true</code> (bất biến: tổng số dư = nạp − rút).</li></ol>
<p class="note">Tệp <code>SoCaiNho.java</code>; mọi dữ liệu đã ghi trong <code>labs/JV2/L09/de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Đề bài cho một sổ cái bảy dòng, hai dòng bị lỗi. Hãy đọc từng dòng, bỏ tiêu đề, đếm số dòng của tệp, và viết hàm phân tích dòng, ném ngoại lệ khi số tiền không phải số hoặc loại sai. Dòng lỗi thì in ra và đọc tiếp, không dừng.
        Dòng đúng thì cộng vào bản đồ có thứ tự. Cuối cùng in số dư từng tài khoản, và dòng tổng kèm kết quả kiểm bất biến. Hãy dừng video và tự viết, đừng chép lại ví dụ.""",
        lab["out"], "SoCaiNho.java",
        """<div class="box key"><b>Nếu kẹt:</b> bắt <code>IllegalArgumentException</code> <b>quanh</b> lời gọi <code>phanTich</code> trong vòng <code>while</code>, không bao cả vòng. Số dòng bắt đầu từ 1 ở tiêu đề: tăng <code>so</code> ở đầu mỗi vòng.
Lời giải: <code>labs/JV2/L09/loi_giai.java</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, đặt khối bắt lỗi ngay quanh lời gọi phân tích một dòng, bên trong vòng lặp, chứ không bao cả vòng lặp. Số dòng bắt đầu từ một ở dòng tiêu đề, nên tăng biến đếm ở đầu mỗi vòng.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=300), "JV2", "L09")

    sc_hook = sc("hook", "hook", "Cuối ngày, sổ cái một triệu dòng: báo cáo phải đúng và phải chạy được", [
        st(svg(1500, 300,
               box(20, 90, 300, 110, ["tệp sổ cái", "một triệu dòng"], C_GRAY, 26, bold=True), arrow(325, 145, 410, 145, "#475569"),
               box(415, 90, 300, 110, ["đọc + kiểm", "dòng lỗi → nhật ký"], C_BLUE, 26, bold=True), arrow(720, 145, 805, 145, "#475569"),
               box(810, 90, 300, 110, ["gom theo", "tài khoản, tháng"], C_GREEN, 26, bold=True), arrow(1115, 145, 1200, 145, "#475569"),
               box(1205, 90, 275, 110, ["báo cáo", "+ kiểm bất biến"], C_AMBER, 26, bold=True),
               txt(750, 260, "chín bài đã học ghép lại thành một chương trình có thật", 28, "middle", "#1f2937", True)),
           """Cuối ngày, ngân hàng có một tệp sổ cái cả triệu dòng. Cần một báo cáo số dư theo tài khoản và theo tháng. Báo cáo phải đúng, dòng lỗi phải được ghi lại chứ không làm hỏng cả báo cáo, và chương trình phải chạy được dù tệp lớn.
           Đây là lúc ghép mọi thứ đã học thành một dự án nhiều tệp có thật."""),
        st("""<div class="box key">Hôm nay: <b>dự án tình huống</b>. Dự án nhiều gói; đọc tệp từng dòng; bản ghi và đường ống; kiểm thử; nhật ký cảnh báo; <b>bất biến tổng số dư = tổng nạp − tổng rút</b>;
và câu hỏi cuối: <b>khi tệp lớn gấp một nghìn lần</b>, thiết kế nào còn sống?</div>""",
           """Hôm nay ta làm một dự án tình huống. Dự án nhiều gói, đọc tệp từng dòng, bản ghi và đường ống, kiểm thử, nhật ký cảnh báo, và một bất biến, tổng số dư bằng tổng nạp trừ tổng rút. Câu hỏi cuối cùng là khi tệp lớn gấp một nghìn lần thì thiết kế nào còn sống.""", clear=True),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: chín bài trước, mỗi bài một mảnh", [
        st(table(["mảnh", "bài", "dùng ở đâu trong dự án"],
                 [["gói, <code>javac -d</code>, <code>-cp</code>", "bài 0", "ba thư mục, một lệnh biên dịch"],
                  ["đọc từng dòng, <code>try (…)</code>", "bài 1", "<code>DocSoCai</code>"],
                  ["bộ so sánh, bản đồ có thứ tự", "bài 2", "<code>TreeMap</code> cho báo cáo xếp theo tài khoản"],
                  ["đường ống, <code>groupingBy</code>", "bài 3", "<code>BaoCao</code>"],
                  ["nhãn và phản chiếu", "bài 4", "<code>@Override</code>, nhãn tự định nghĩa"],
                  ["khoá, nhóm luồng, bản đồ an toàn", "bài 5", "gom song song"],
                  ["ca kiểm ở biên", "bài 6", "<code>KiemTra</code>"],
                  ["nhật ký có mức, dấu vết", "bài 7", "<code>NhatKy</code>, cảnh báo dòng lỗi"],
                  ["tiền là số nguyên đồng", "bài 8", "<code>long</code> cho mọi số tiền"]]),
           """Ta ôn lại các mảnh sẽ ghép. Gói và lệnh biên dịch từ bài không. Đọc từng dòng trong khối có tài nguyên từ bài một. Bản đồ có thứ tự từ bài hai. Đường ống và gom nhóm từ bài ba. Nhãn và phản chiếu từ bài bốn. Bản đồ an toàn cho nhiều luồng từ bài năm. Ca kiểm ở biên từ bài sáu.
           Nhật ký có mức độ từ bài bảy. Và tiền là số nguyên theo đồng từ các bài trước.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "1.10"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã sáu thuật ngữ của bài toán sổ cái", [
        st(table(["thuật ngữ", "nghĩa"],
                 [["sổ cái (ledger)", "danh sách <b>mọi giao dịch</b> theo thứ tự; số dư là kết quả <b>cộng dồn</b> từ sổ cái"],
                  ["bất biến (invariant)", "điều <b>luôn đúng</b> sau mỗi thao tác; ở đây: <b>tổng số dư = tổng nạp − tổng rút</b>"],
                  ["đối chiếu (reconcile)", "so <b>hai cách đếm độc lập</b> cùng một thứ: số dòng đọc = hợp lệ + lỗi = số dòng của tệp"],
                  ["dòng lỗi", "dòng không qua kiểm tra; <b>ghi lại và đếm</b>, không bỏ lặng lẽ, không làm dừng cả chương trình"],
                  ["đọc theo dòng (streaming)", "xử lý từng dòng rồi quên nó: bộ nhớ <b>không đổi</b> theo kích thước tệp"],
                  ["bộ gom (accumulator)", "đối tượng cộng dồn kết quả khi từng dòng đi qua (<code>TongHop</code>)"]]),
           """Bảng này giải mã sáu thuật ngữ của bài toán sổ cái. Sổ cái là danh sách mọi giao dịch theo thứ tự, số dư chỉ là kết quả cộng dồn. Bất biến là điều luôn đúng sau mỗi thao tác, ở đây là tổng số dư bằng tổng nạp trừ tổng rút. Đối chiếu là so hai cách đếm độc lập cùng một thứ.
           Dòng lỗi phải được ghi lại và đếm, không bỏ lặng lẽ. Đọc theo dòng là xử lý từng dòng rồi quên, nên bộ nhớ không đổi. Và bộ gom là đối tượng cộng dồn kết quả khi từng dòng đi qua.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: cây dự án và dòng chảy dữ liệu", [
        st(svg(1500, 420,
               *tree_parts([(0, "src/soc", "d"), (1, "GiaoDich.java", "f"), (1, "DocSoCai.java", "f"), (1, "NhatKy.java", "f"), (1, "BaoCao.java", "f"),
                            (1, "TongHop.java", "f"), (1, "App.java", "f"), (1, "KiemTra.java", "f")], 10, 10, 60, 48, 22, hi={1}),
               arrow(430, 90, 700, 90, "#2a78d6"), txt(820, 85, "bản ghi bất biến + phanTich", 24, "start"),
               arrow(430, 140, 700, 140, "#2a78d6"), txt(820, 135, "đọc từng dòng, gọi phanTich, báo lỗi", 24, "start"),
               arrow(430, 190, 700, 190, "#2a78d6"), txt(820, 185, "cảnh báo có mức, in ngay", 24, "start"),
               arrow(430, 240, 700, 240, "#2a78d6"), txt(820, 235, "đường ống gom nhóm", 24, "start"),
               arrow(430, 290, 700, 290, "#2a78d6"), txt(820, 285, "bộ gom cho đọc theo dòng", 24, "start"),
               arrow(430, 340, 700, 340, "#2a78d6"), txt(820, 335, "ghép lại và in báo cáo", 24, "start"),
               arrow(430, 390, 700, 390, "#16a34a"), txt(820, 385, "kiểm thử các ca biên", 24, "start", "#16a34a", True)),
           """Hình dung dự án như một cây thư mục và một dòng chảy. Một gói, bảy tệp, mỗi tệp một việc. Bản ghi bất biến biết cách phân tích một dòng. Bộ đọc đọc từng dòng và gọi bản ghi. Nhật ký in cảnh báo có mức. Lớp báo cáo dùng đường ống để gom nhóm.
           Bộ gom dành cho đọc theo dòng. Lớp chính ghép các phần lại. Và lớp kiểm thử canh các ca biên. Mỗi mảnh nhỏ nên dễ kiểm và dễ thay."""),
        st(pcode(du_an, "src/soc/GiaoDich.java", lines=(7, 16), title="GiaoDich.java: phanTich (đoạn đầu)"),
           """Đây là trái tim của bộ đọc, hàm phân tích một dòng. Cắt dòng, giữ cả ô rỗng ở cuối. Nếu số cột không đủ thì ném lỗi rõ ràng. Số tiền đổi sang số nguyên dài, hỏng thì bọc lại thành một thông báo dễ hiểu.""", clear=True),
        st(pcode(du_an, "src/soc/GiaoDich.java", lines=(18, 23), title="GiaoDich.java: phanTich (đoạn sau)"),
           """Rồi hai kiểm tra nghiệp vụ. Số tiền phải dương, và loại chỉ là nạp hoặc rút. Mỗi kiểm tra ném một thông báo riêng, nói rõ giá trị sai. Nhờ vậy nhật ký sau này chỉ ra được đúng dòng nào sai vì lý do gì.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: vì sao thiết kế như vậy", [
        st("<p><b>Bước 1.</b> Tiền là <b>số nguyên đồng</b> (<code>long</code>), <code>nap</code> mang dấu <b>+</b>, <code>rut</code> mang dấu <b>−</b>:</p>"
           "<p><code>số dư = tổng của (dấu × số tiền)</code></p><p>Vì sao: cộng số nguyên <b>giao hoán và kết hợp</b>, nên thứ tự dòng hay cách gom nhóm không đổi kết quả.</p>",
           """Bước một, tiền là số nguyên đồng, nạp mang dấu cộng, rút mang dấu trừ. Số dư là tổng các số có dấu. Vì phép cộng số nguyên giao hoán và kết hợp, nên thứ tự các dòng hay cách gom nhóm không làm đổi kết quả.""", clear=True),
        st("<p><b>Bước 2.</b> Bất biến: <b>tổng các số dư = tổng nạp − tổng rút</b>.</p>"
           "<p>Vì sao: mỗi dòng hợp lệ đóng góp <b>đúng một lần</b> vào một số dư và vào một trong hai tổng; nếu một dòng bị tính hai lần hay bị rơi, hai vế <b>lệch nhau</b>.</p>",
           """Bước hai, bất biến. Tổng các số dư phải bằng tổng nạp trừ tổng rút. Vì mỗi dòng hợp lệ đóng góp đúng một lần vào một số dư và vào một trong hai tổng, nên nếu có dòng bị tính hai lần hoặc bị rơi thì hai vế lệch nhau.""", clear=True),
        st("<p><b>Bước 3.</b> Bất biến <b>không bắt được</b> dòng bị bỏ đi (bỏ dòng nào cũng khớp). Cần <b>đối chiếu số dòng</b>:</p>"
           "<p><code>đọc = hợp lệ + lỗi</code> và <code>đọc = số dòng của tệp − 1</code> (trừ tiêu đề).</p>",
           """Bước ba, bất biến không bắt được dòng bị bỏ đi, vì bỏ dòng nào hai vế cũng vẫn khớp. Vì vậy cần đối chiếu số dòng, đọc bằng hợp lệ cộng lỗi, và bằng số dòng của tệp trừ tiêu đề.""", clear=True),
        st("<p><b>Bước 4.</b> Thử bằng số với 3 dòng: nạp A 100; rút A 30; nạp B 50:</p>"
           + table(["tính", "giá trị"], [["số dư A", "100 − 30 = <b>70</b>"], ["số dư B", "<b>50</b>"], ["tổng số dư", "70 + 50 = <b>120</b>"],
                                         ["nạp − rút", "(100 + 50) − 30 = <b>120</b> ✓"], ["đọc = hợp lệ + lỗi", "3 = 3 + 0 ✓"]]),
           """Bước bốn, thử bằng số với ba dòng, vì ví dụ nhỏ cho phép kiểm bằng mắt. Số dư của A là một trăm trừ ba mươi bằng bảy mươi. Số dư của B là năm mươi. Tổng số dư một trăm hai mươi. Nạp trừ rút là một trăm năm mươi trừ ba mươi, cũng một trăm hai mươi. Và số dòng đọc là ba, bằng ba hợp lệ cộng không lỗi.""", clear=True),
    ], checks=["100 - 30 == 70", "70 + 50 == 120", "(100 + 50) - 30 == 120", "3 == 3 + 0"])
    sc_ex = sc("example", "example", "Ví dụ: biên dịch, kiểm thử, chạy trên tệp sạch rồi tệp có hai dòng lỗi", [
        st(term_block(du_an, 0, 2, title="Biên dịch cả dự án; chạy kiểm thử"),
           """Phép làm thứ nhất, biên dịch cả gói bằng một lệnh, rồi chạy bộ kiểm thử trước khi tin bất kỳ con số nào. Bảy ca đều đạt, gồm ca số tiền âm và ca thiếu cột.""", clear=True),
        st("$$① \\; \\text{A01}: 5\\,000\\,000 - 1\\,200\\,000 + 2\\,500\\,000 = \\hl{6\\,300\\,000}$$"
           "$$② \\; \\text{A02}: 3\\,000\\,000 - 500\\,000 + 1\\,000\\,000 = \\hl{3\\,500\\,000}$$"
           "$$③ \\; \\text{A03}: 800\\,000 - 300\\,000 = \\hl{500\\,000}$$",
           """Phép làm thứ nhất tới thứ ba, ta tự cộng số dư từng tài khoản trước. Tài khoản A không một là năm triệu trừ một triệu hai cộng hai triệu rưỡi, bằng sáu triệu ba trăm nghìn. A không hai là ba triệu, trừ năm trăm nghìn, cộng một triệu, bằng ba triệu rưỡi. A không ba là tám trăm nghìn trừ ba trăm nghìn, bằng năm trăm nghìn.""", clear=True),
        st("$$④ \\; 6\\,300\\,000 + 3\\,500\\,000 + 500\\,000 = \\hl{10\\,300\\,000}$$"
           "$$⑤ \\; \\text{nạp} = 12\\,300\\,000, \\; \\text{rút} = 2\\,000\\,000 \\Rightarrow 12\\,300\\,000 - 2\\,000\\,000 = \\hl{10\\,300\\,000}$$",
           """Phép thứ tư, tổng số dư là mười triệu ba trăm nghìn. Phép thứ năm, tổng nạp là mười hai triệu ba trăm nghìn, tổng rút là hai triệu, hiệu cũng là mười triệu ba trăm nghìn. Bất biến thoả, ta kỳ vọng chương trình in đúng như vậy.""", clear=True),
        st(term_block(du_an, 2, 3, title="Chạy trên tệp sạch"),
           """Chạy thật, tám dòng đều hợp lệ, số dư từng tài khoản khớp với phép tính tay, và dòng kiểm tra báo khớp. Dòng cuối là số ròng theo tháng, tổng ba tháng cũng là mười triệu ba trăm nghìn.""", clear=True),
        st(term_block(du_an, 3, 4, title="Tệp có hai dòng lỗi (số tiền abc, loại doi)"),
           """Giờ chạy trên tệp có hai dòng lỗi. Nhật ký cảnh báo nói rõ dòng nào, vì lý do gì. Báo cáo vẫn chạy trên sáu dòng còn lại, và dòng đầu của báo cáo nói đã đọc tám dòng, sáu hợp lệ, hai lỗi. Báo cáo không bị hỏng chỉ vì vài dòng xấu, nhưng cũng không giấu chuyện đó.""", clear=True),
    ], checks=["5000000 - 1200000 + 2500000 == 6300000", "3000000 - 500000 + 1000000 == 3500000", "800000 - 300000 == 500000",
               "6300000 + 3500000 + 500000 == 10300000", "5000000 + 3000000 + 800000 + 2500000 + 1000000 == 12300000",
               "1200000 + 500000 + 300000 == 2000000", "12300000 - 2000000 == 10300000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm dòng bằng lệnh của hệ điều hành", [
        st(term_block(du_an, 4, 5, title="Đếm số dòng dữ liệu của tệp có lỗi, không tính tiêu đề")
           + "<p>Đối chiếu: <b>8</b> dòng dữ liệu = <b>6</b> hợp lệ + <b>2</b> lỗi (đúng như dòng đầu của báo cáo) ✓</p>",
           """Cách kiểm khác là một công cụ hoàn toàn khác. Lệnh đếm dòng cho biết tệp có tám dòng dữ liệu không tính tiêu đề. Chương trình báo đọc tám dòng, gồm sáu hợp lệ và hai lỗi. Hai cách đếm độc lập khớp nhau, nên không dòng nào bị rơi mà không ai biết.""", clear=True),
        st("<p>Kiểm bất biến cho tệp lỗi: sáu dòng hợp lệ, nạp 12 300 000 và rút 300 000 (dòng rút <code>abc</code> bị loại, dòng <code>doi</code> bị loại).</p>"
           "$$7\\,500\\,000 + 4\\,000\\,000 + 500\\,000 = 12\\,000\\,000 = 12\\,300\\,000 - 300\\,000 \\; ✓$$",
           """Kiểm thêm bất biến cho tệp có lỗi. Chỉ sáu dòng hợp lệ được tính, nạp mười hai triệu ba trăm nghìn và rút ba trăm nghìn. Tổng số dư mười hai triệu đúng bằng hiệu đó. Bất biến thoả, nhưng nhớ rằng nó thoả với mọi tập dòng hợp lệ, nên vẫn cần đếm dòng.""", clear=True),
    ], checks=["6 + 2 == 8", "7500000 + 4000000 + 500000 == 12000000", "12300000 - 300000 == 12000000"])
    sc_scale = sc("scale", "concept", "Khi sổ cái lớn gấp một nghìn lần: bản nào còn sống?", [
        st(term_block(du_an, 6, 8, title="Một triệu dòng, bộ nhớ tối đa 32 megabyte: bản giữ danh sách")
           + "<p class='note'><code>App</code> giữ mọi <code>GiaoDich</code> trong một danh sách rồi mới tạo đường ống.</p>",
           """Ta thử quy mô thật. Tạo sổ cái một triệu dòng. Bản dự án chạy tốt trên tám dòng, giữ mọi giao dịch trong một danh sách, thì hết bộ nhớ với giới hạn ba mươi hai megabyte. Mỗi bản ghi cùng ba chuỗi và một ngày tốn hàng trăm byte, nên một triệu dòng vượt xa giới hạn.""", clear=True),
        st(term_block(du_an, 8, 11, title="Bản đọc theo dòng (32 MB) và bản song song (64 MB rồi 128 MB)")
           + "<p class='note'>Tổng số dư khớp bất biến. Song song giữ nhiều dòng cùng lúc nên cần nhiều bộ nhớ hơn đọc theo dòng.</p>",
           """Bản đọc theo dòng chỉ giữ một dòng và một bản đồ một trăm tài khoản, nên chạy xong và vẫn thoả bất biến. Bản song song chia các dòng cho nhiều luồng, dùng bộ gom an toàn cho nhiều luồng, và cho kết quả đúng bằng bản tuần tự. Nhưng nó giữ nhiều dòng cùng lúc, nên với sáu mươi bốn megabyte vẫn hết bộ nhớ, và phải có một trăm hai mươi tám megabyte mới chạy. Nếu thay bộ gom bằng bản đồ thường thì đây chính là lỗi tranh chấp của bài về luồng.""", clear=True),
        st(table(["số dòng", "1 000", "1 000 000", "1 000 000 000"],
                 [["bộ nhớ khi giữ danh sách giao dịch (≥ 200 byte mỗi dòng, ước lượng)", "≥ 200 KB", "<b>≥ 200 MB</b>", "<b>≥ 200 GB</b>"],
                  ["bộ nhớ khi đọc theo dòng (một dòng + bản đồ tài khoản)", "gần như nhau", "gần như nhau", "gần như nhau"],
                  ["thời gian đọc (tỉ lệ so với 1 000 dòng)", "×1", "×1 000", "<b>×1 000 000</b>"]])
           + "<p class='note'>Đánh đổi: đọc theo dòng cho báo cáo <b>một lượt</b>; cần truy vấn nhiều kiểu thì phải đọc lại, hoặc đưa dữ liệu vào cơ sở dữ liệu có chỉ mục. Song song giúp việc <b>tính toán</b>; việc <b>đọc đĩa</b> bị giới hạn bởi tốc độ đĩa.</p>",
           """Tóm lại theo quy mô. Giữ danh sách thì bộ nhớ tăng theo số dòng, hai trăm megabyte cho một triệu dòng và hai trăm gigabyte cho một tỉ dòng. Đọc theo dòng thì bộ nhớ gần như không đổi, nhưng thời gian vẫn tăng đều theo số dòng. Đánh đổi là báo cáo chỉ một lượt, cần truy vấn nhiều kiểu thì phải dùng cơ sở dữ liệu có chỉ mục.
           Và song song chỉ giúp phần tính toán, còn đọc đĩa bị giới hạn bởi tốc độ đĩa.""", clear=True),
    ], checks=["1000 * 200 == 200000", "1000000 * 200 == 200000000", "1000000000 * 200 == 200000000000", f"sum((-1 if i % 3 == 0 else 1) * (i % 7 + 1) * 1000 for i in range(1, 1000001)) == {TONG_LON}"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Quên bỏ dòng tiêu đề: nó bị coi là một giao dịch.</div>'
           + term_block(du_an, 5, 6),
           """Lỗi thứ nhất là quên bỏ dòng tiêu đề. Dòng chữ tên các cột bị đưa vào hàm phân tích như một giao dịch, và cột tiền chứa chữ so tiền gạch dưới. Nó báo lỗi rõ ràng, nhưng nếu ta nuốt lỗi thì mất một dòng và không ai để ý."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Bỏ dòng lỗi lặng lẽ: bất biến vẫn khớp, báo cáo vẫn trông đúng.</div>'
           + "<p>Báo cáo trên tệp lỗi vẫn in <b>(khop)</b> dù mất 2 dòng. Chỉ có <b>đối chiếu số dòng</b> (8 = 6 + 2) và <b>nhật ký cảnh báo</b> mới phát hiện được.</p>"
           + "<p>Quy tắc: mỗi dòng bị loại phải để lại <b>dấu vết</b> (nhật ký) và <b>con số</b> (đếm), và con số đó phải đối chiếu được với nguồn.</p>",
           """Lỗi thứ hai hay gặp ở người đã đi làm. Bỏ dòng lỗi một cách lặng lẽ, và bất biến vẫn khớp, báo cáo vẫn trông đúng. Báo cáo trên tệp lỗi vẫn báo khớp dù mất hai dòng. Chỉ đối chiếu số dòng và nhật ký cảnh báo mới phát hiện được. Mỗi dòng bị loại phải để lại dấu vết và một con số có thể đối chiếu với nguồn.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Thiếu một ca kiểm: dòng giao dịch số tiền âm lọt vào sổ cái.</div>'
           + term_block(du_an, 11, 13, title="Gỡ kiểm tra tiền dương rồi chạy lại bộ kiểm thử"),
           """Lỗi thứ ba cũng của người đã đi làm. Một kiểm tra nghiệp vụ, số tiền phải dương, nằm lặng lẽ trong hàm phân tích. Ta thử gỡ nó đi rồi chạy lại bộ kiểm thử. Đúng một ca báo hỏng, là ca số tiền âm. Nếu ta chưa từng viết ca đó thì kiểm tra có thể bị xoá mà mọi cổng vẫn xanh, và nạp âm sẽ lẳng lặng thành rút.""", clear=True),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Sổ cái 5 dòng (<code>tai_khoan,loai,so_tien</code>): <code>X,nap,900</code>; <code>Y,nap,400</code>; <code>X,rut,250</code>; <code>Y,rut,xx</code>; <code>X,nap,100</code>.</p>
<ol><li>Số dư X, Y sau khi bỏ dòng lỗi? Tổng số dư? Bất biến <code>nap − rut</code> có khớp không?</li>
<li>Đối chiếu số dòng: đọc = hợp lệ + lỗi = ?</li></ol>
<p><b>Chọn A hay B?</b> Báo cáo cho tệp 50 GB trên máy 8 GB. A: <code>List</code> rồi <code>stream()</code>. B: bộ gom cộng dồn khi đọc từng dòng. Muốn thêm <code>parallel()</code> thì bộ gom cần điều kiện gì?</p>""",
           """Bây giờ tới phần bạn tự làm. Sổ cái năm dòng, một dòng lỗi. Hãy tính số dư hai tài khoản sau khi bỏ dòng lỗi, tổng số dư, và bất biến có khớp không. Rồi đối chiếu số dòng.
           Cuối cùng chọn giữa danh sách rồi đường ống, và bộ gom cộng dồn khi đọc từng dòng, cho tệp năm mươi gigabyte trên máy tám gigabyte. Và muốn thêm song song thì bộ gom cần điều kiện gì. Hãy dừng video và tự làm.""", pause=30),
        st(table(["câu", "đáp án", "vì sao"],
                 [["1", "X = 900 − 250 + 100 = <b>750</b>; Y = <b>400</b>; tổng <b>1 150</b>; nạp 1 400 − rút 250 = <b>1 150</b> ✓", "dòng <code>Y,rut,xx</code> bị loại; bất biến thoả"],
                  ["2", "<b>5 = 4 hợp lệ + 1 lỗi</b>", "bất biến không thấy dòng bị loại; đối chiếu số dòng mới thấy"],
                  ["3", "<b>B</b>; bộ gom phải <b>an toàn cho nhiều luồng</b>", "A cần ≥ 200 byte × số dòng ≫ 8 GB; B giữ bộ nhớ không đổi; song song cần bản đồ/bộ cộng an toàn"]]),
           """Đáp án câu một, số dư của X là chín trăm trừ hai trăm năm mươi cộng một trăm, bằng bảy trăm năm mươi. Y là bốn trăm. Tổng một nghìn một trăm năm mươi, bằng nạp một nghìn bốn trăm trừ rút hai trăm năm mươi. Câu hai, năm dòng bằng bốn hợp lệ cộng một lỗi.
           Câu ba chọn phương án B, vì danh sách cần nhiều hơn tám gigabyte, còn bộ gom giữ bộ nhớ không đổi. Muốn song song thì bộ gom phải an toàn cho nhiều luồng.""",
           focus=[1, "1.2", "1.3", "1.4", "1.4", "1.4"]),
        st("""<div class="box key"><b>Quy tắc:</b> mỗi dòng bị loại phải <b>có dấu vết và có số đếm</b>; hai cách đếm độc lập phải <b>khớp</b>; tệp lớn thì <b>đọc theo dòng</b>; song song chỉ khi <b>bộ gom an toàn</b>.</div>""",
           """Quy tắc rút ra. Mỗi dòng bị loại phải có dấu vết và có số đếm. Hai cách đếm độc lập phải khớp. Tệp lớn thì đọc theo dòng. Và song song chỉ khi bộ gom an toàn cho nhiều luồng."""),
    ], checks=["900 - 250 + 100 == 750", "750 + 400 == 1150", "(900 + 400 + 100) - 250 == 1150", "5 == 4 + 1"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("gói nhỏ, mỗi tệp một việc", "phân tích + kiểm từng dòng", "dòng lỗi: nhật ký + đếm", "bất biến: tổng số dư = nạp − rút",
                 "đối chiếu số dòng", "tệp lớn: đọc theo dòng", "song song cần bộ gom an toàn"),
           """Tổng kết chuỗi logic. Chia gói nhỏ, mỗi tệp một việc. Phân tích và kiểm từng dòng. Dòng lỗi thì ghi nhật ký và đếm. Kiểm bất biến tổng số dư bằng nạp trừ rút. Đối chiếu số dòng bằng một cách đếm độc lập.
           Tệp lớn thì đọc theo dòng. Và song song cần bộ gom an toàn cho nhiều luồng."""),
        st("""<div class='box key'><b>Tư duy:</b> một báo cáo đúng không chỉ là <b>số đúng</b>, mà là số đúng <b>kèm bằng chứng</b>: kiểm thử đã chạy, dòng lỗi đã đếm, bất biến đã thoả,
và biết rõ <b>ở quy mô nào</b> thiết kế này sẽ gãy.</div>""",
           """Điều cần mang theo. Một báo cáo đúng không chỉ là số đúng, mà là số đúng kèm bằng chứng. Kiểm thử đã chạy, dòng lỗi đã đếm, bất biến đã thoả, và biết rõ ở quy mô nào thiết kế này sẽ gãy. Để chạy một chương trình như vậy nhiều tháng, bước tiếp theo là hiểu bộ nhớ và bộ thu gom rác của máy ảo.""", forward_ref=True),
    ])
    return lesson("L09", "du_an_so_cai", "Bài 9 — Dự án tình huống: sổ cái tệp CSV tới báo cáo",
                  "curriculum/jv2.yaml L09; audit/jv2/verify_jv2.py L09 (javac/java chạy thật, JDK 21; dự án nhiều gói, -Xmx32m cho phép đo bộ nhớ); "
                  "java.util.stream.Collectors.groupingByConcurrent (Java SE 21 API: gom song song an toàn); java.util.logging; "
                  "java.nio.file.Files.lines (đọc lười); RFC 4180 (CSV); "
                  "Pacioli, L. (1494), Summa de arithmetica (nguyên lý bút toán kép: tổng ghi nợ bằng tổng ghi có); dev.java/learn",
                  ["Dựng dự án nhiều gói gồm bản ghi, bộ đọc, báo cáo, nhật ký và kiểm thử, rồi biên dịch và chạy bằng lệnh",
                   "Tính số dư theo tài khoản và kiểm bất biến tổng số dư bằng tổng nạp trừ tổng rút",
                   "Nêu cách đối chiếu số dòng và nhật ký để không bỏ lặng lẽ dòng lỗi",
                   "Nhận ra bản giữ danh sách gãy ở một triệu dòng, bản đọc theo dòng sống, song song cần bộ gom an toàn",
                   "Viết chương trình sổ cái nhỏ bỏ qua dòng lỗi, in số dư và kiểm bất biến"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_lab, sc_rec],
                  covers=[(1, "example"), (2, "example"), (3, "check"), (4, "scale"), (5, "practice")])
