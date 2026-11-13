import java.util.*;
public class XuLyTrung {
    static long soDu = 3_000_000;
    static Map<String, Long> daXuLy = new HashMap<>();
    static long chuyen(String khoa) {
        return daXuLy.computeIfAbsent(khoa, k -> soDu -= 700_000);
    }
    public static void main(String[] args) {
        for (String k : new String[] { "k1", "k1", "k2", "k1" }) {
            System.out.println(k + " -> " + chuyen(k));
        }
    }
}
