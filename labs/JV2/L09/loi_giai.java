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
}
