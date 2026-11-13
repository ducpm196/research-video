public class RutATM {
    static long tinhPhiRut(long soTien) {                // phí rút (số minh hoạ)
        if (soTien < 2000000) {
            return 1100;
        }
        return 3300;
    }

    static long conLai(long soDu, long soTien) {         // gọi lồng hàm tính phí
        return soDu - soTien - tinhPhiRut(soTien);
    }

    static void nap(long[] tk, long soTien) {            // nhận mảng: đổi được ô
        tk[0] = tk[0] + soTien;
    }

    public static void main(String[] args) {
        System.out.println("Phi rut 1500000: " + tinhPhiRut(1500000));
        System.out.println("Phi rut 2000000: " + tinhPhiRut(2000000));
        System.out.println("Con lai: " + conLai(10000000, 2000000));
        long[] tk = {10000000};
        nap(tk, 500000);
        System.out.println("Sau nap: " + tk[0]);
    }
}
