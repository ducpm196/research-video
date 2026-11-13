import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

public class TongTheoLoai {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("giao_dich.csv");
        Files.writeString(p, "ma,loai,so_tien\n1,chuyen,850000\n2,nap,4000000\n3,chuyen,150000\n"
                + "4,rut,600000\n5,nap,250000\n6,chuyen,400000\n7,rut,900000\n");
        Map<String, Long> tong = new HashMap<>();
        Map<String, Integer> dem = new HashMap<>();
        long tatCa = 0;
        try (BufferedReader br = Files.newBufferedReader(p)) {
            br.readLine();
            String dong;
            while ((dong = br.readLine()) != null) {
                String[] f = dong.split(",");
                long tien = Long.parseLong(f[2]);
                tong.put(f[1], tong.getOrDefault(f[1], 0L) + tien);
                dem.put(f[1], dem.getOrDefault(f[1], 0) + 1);
                tatCa += tien;
            }
        }
        for (String loai : new String[]{"nap", "rut", "chuyen"}) {
            System.out.println(loai + ": " + dem.get(loai) + " giao dich, tong " + tong.get(loai));
        }
        System.out.println("Tong tat ca: " + tatCa);
    }
}
