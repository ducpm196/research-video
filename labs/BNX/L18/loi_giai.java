import java.time.*;

public class Lab {
    interface Cong { boolean chuyen(String tk, long soTien); }

    // Đề: dưới 2 000 000: 0; từ 2 000 000 tới dưới 20 000 000: 3 000; từ 20 000 000: 4 000
    static long tinh(long soTien) {
        if (soTien < 2_000_000) return 0;
        if (soTien <= 20_000_000) return 3_000;   // nhầm dấu: phải là <
        return 4_000;
    }

    static long chuyen(Cong cong, String tk, long soTien) {
        long phi = tinh(soTien);
        if (!cong.chuyen(tk, soTien + phi)) throw new IllegalStateException();
        return phi;
    }

    static boolean kip(Clock dongHo) {
        return LocalTime.now(dongHo).isBefore(LocalTime.of(17, 0));
    }

    static int dat = 0, truot = 0;

    static void ca(long vao, long mongDoi) {
        long nhan = tinh(vao);
        boolean ok = nhan == mongDoi;
        if (ok) dat++; else truot++;
        System.out.println("ca " + vao + ": mong doi " + mongDoi + ", nhan " + nhan
                + ", " + (ok ? "DAT" : "TRUOT"));
    }

    public static void main(String[] args) {
        ca(1_999_999, 0);
        ca(2_000_000, 3_000);
        ca(19_999_999, 3_000);
        ca(20_000_000, 4_000);
        ca(30_000_000, 4_000);
        System.out.println("tong: " + dat + " dat, " + truot + " truot");

        long[] ghi = new long[2];
        Cong gia = (tk, soTien) -> { ghi[0]++; ghi[1] = soTien; return true; };
        chuyen(gia, "TK07", 12_000_000);
        System.out.println("cong goi " + ghi[0] + " lan, so tien " + ghi[1]);

        ZoneOffset vn = ZoneOffset.ofHours(7);
        Instant t = Instant.parse("2026-11-11T16:59:00+07:00");
        System.out.println(kip(Clock.fixed(t, vn)));
        System.out.println(kip(Clock.fixed(t.plusSeconds(60), vn)));
    }
}
