public class SoDu {
    public static void main(String[] args) {
        long soDu = 1500000;                        // số dư đầu (số minh hoạ)
        long chuyen = 250000;                       // mỗi lệnh chuyển
        long phi = 2200;                            // phí mỗi lệnh (số minh hoạ)
        long tongChuyen = 3 * chuyen;
        long tongPhi = 3 * phi;
        soDu = soDu - tongChuyen - tongPhi;         // tính vế phải rồi ghi đè
        System.out.println("Tong chuyen: " + tongChuyen);
        System.out.println("Tong phi: " + tongPhi);
        System.out.println("So du con lai: " + soDu);
        int dot = 800000000;
        int sai = dot + dot + dot;                  // cất trong int
        long dot2 = 800000000L;
        long dung = dot2 + dot2 + dot2;             // cất trong long
        System.out.println("Int: " + sai);
        System.out.println("Long: " + dung);
    }
}
