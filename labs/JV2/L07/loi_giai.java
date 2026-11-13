public class TongPhi {
    static long phi(long soTien) {
        if (soTien <= 1000000) {
            return 1000;
        }
        if (soTien <= 10000000) {
            return 5000;
        }
        return 10000;
    }

    static long tongPhi(long[] ds) {
        long tong = 0;
        for (int i = 0; i < ds.length; i++) {
            tong += phi(ds[i]);
        }
        return tong;
    }

    static void baoCao(long[] ds) {
        System.out.println("So giao dich: " + ds.length);
        System.out.println("Tong phi: " + tongPhi(ds));
    }

    public static void main(String[] args) {
        baoCao(new long[]{800000, 2500000, 1000000, 12000000, 9000000});
    }
}
