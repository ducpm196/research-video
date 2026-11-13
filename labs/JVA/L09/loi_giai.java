import java.util.ArrayList;
import java.util.HashMap;

public class ThongKe {
    public static void main(String[] args) {
        String[] loai = {"CK", "NAP", "CK", "RUT", "CK", "NAP", "CK"};
        HashMap<String, Integer> dem = new HashMap<>();
        for (String t : loai) {
            dem.put(t, dem.getOrDefault(t, 0) + 1);       // lấy số cũ, cộng một, đặt lại
        }
        ArrayList<Long> tien = new ArrayList<>();
        tien.add(300000L);
        tien.add(900000L);
        tien.add(120000L);
        tien.add(450000L);
        tien.sort((a, b) -> Long.compare(b, a));          // lớn trước
        System.out.println("So giao dich: " + loai.length);
        System.out.println("CK: " + dem.get("CK"));
        System.out.println("NAP: " + dem.get("NAP"));
        System.out.println("RUT: " + dem.get("RUT"));
        System.out.println("Lon truoc: " + tien);
    }
}
