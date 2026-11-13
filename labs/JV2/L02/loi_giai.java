import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class SapXepGiaoDich {
    record GiaoDich(int ma, String loai, long soTien) {}

    static class TheoLoaiRoiTien implements Comparator<GiaoDich> {
        public int compare(GiaoDich a, GiaoDich b) {
            int c = a.loai().compareTo(b.loai());
            if (c != 0) {
                return c;
            }
            return Long.compare(b.soTien(), a.soTien());
        }
    }

    public static void main(String[] args) {
        List<GiaoDich> ds = new ArrayList<>(List.of(
                new GiaoDich(1, "chuyen", 900000), new GiaoDich(2, "nap", 250000), new GiaoDich(3, "chuyen", 150000),
                new GiaoDich(4, "rut", 600000), new GiaoDich(5, "nap", 4000000), new GiaoDich(6, "rut", 900000),
                new GiaoDich(7, "chuyen", 900000)));
        ds.sort(new TheoLoaiRoiTien());
        for (GiaoDich g : ds) {
            System.out.println(g.ma() + " " + g.loai() + " " + g.soTien());
        }
    }
}
