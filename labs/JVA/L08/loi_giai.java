import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

public class DoiSoat {
    public static void main(String[] args) throws Exception {
        Path tep = Path.of("lenh.txt");
        Files.writeString(tep, "A001;1200000\nA002;350000\nA003;2000000\nA004;75000\n");
        String[] dong = Files.readString(tep).split("\n");
        long tong = 0;
        int lon = 0;                                        // số lệnh trên 1 triệu
        for (int i = 0; i < dong.length; i++) {
            long soTien = Long.parseLong(dong[i].split(";")[1]);
            tong += soTien;
            if (soTien > 1000000) {
                lon++;
            }
        }
        System.out.println(dong.length + " dong");
        System.out.println("Tong: " + String.format(Locale.US, "%,d", tong));
        System.out.println("Tren 1 trieu: " + lon);
        for (int i = 0; i < dong.length; i++) {
            String[] phan = dong[i].split(";");
            System.out.println(phan[0] + " | " + String.format(Locale.US, "%,d", Long.parseLong(phan[1])) + " dong");
        }
    }
}
