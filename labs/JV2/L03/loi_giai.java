import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class ThongKeStream {
    record GiaoDich(int ma, String loai, long soTien) {}

    public static void main(String[] args) {
        List<GiaoDich> ds = List.of(
                new GiaoDich(1, "nap", 3000000), new GiaoDich(2, "rut", 450000),
                new GiaoDich(3, "chuyen", 800000), new GiaoDich(4, "rut", 1200000),
                new GiaoDich(5, "nap", 200000), new GiaoDich(6, "chuyen", 1500000),
                new GiaoDich(7, "rut", 500000), new GiaoDich(8, "nap", 650000));
        long rutLon = ds.stream().filter(g -> g.loai().equals("rut") && g.soTien() >= 500000)
                .mapToLong(GiaoDich::soTien).sum();
        Map<String, Long> dem = ds.stream().collect(
                Collectors.groupingBy(GiaoDich::loai, TreeMap::new, Collectors.counting()));
        Map<String, Long> tong = ds.stream().collect(
                Collectors.groupingBy(GiaoDich::loai, TreeMap::new, Collectors.summingLong(GiaoDich::soTien)));
        Map<String, Long> tongVong = new TreeMap<>();
        for (GiaoDich g : ds) {
            tongVong.merge(g.loai(), g.soTien(), Long::sum);
        }
        System.out.println("Rut tu 500000: " + rutLon);
        System.out.println("Dem: " + dem);
        System.out.println("Tong: " + tong);
        System.out.println("Khop vong lap: " + tong.equals(tongVong));
    }
}
