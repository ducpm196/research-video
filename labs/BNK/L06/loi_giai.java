import java.util.*;
public class BoDemNho {
    static Map<Integer, Long> boDem = new HashMap<>();
    static long tong = 0;
    static int trung = 0;
    static long soDu(int tk) {
        if (boDem.containsKey(tk)) { trung++; tong += 2; return boDem.get(tk); }
        tong += 2 + 30;
        long v = tk * 1000L;
        boDem.put(tk, v);
        return v;
    }
    public static void main(String[] args) {
        for (int i = 0; i < 40; i++) soDu(i % 4);
        System.out.println("trung " + trung + "/40, trung binh " + tong / 40.0 + " ms");
    }
}
