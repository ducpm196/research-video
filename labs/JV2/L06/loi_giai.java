import java.util.function.LongSupplier;

public class KiemPhiChuyenKhoan {
    static int dat = 0, hong = 0;

    static long phiChuyenKhoan(long soTien, boolean cungNganHang) {
        if (soTien <= 0) {
            throw new IllegalArgumentException("so tien phai duong");
        }
        if (cungNganHang) {
            return 0;
        }
        if (soTien < 500000) {
            return 2000;
        }
        if (soTien <= 5000000) {
            return 7000;
        }
        return 11000;
    }

    static void kiem(String ten, long mong, LongSupplier thuc) {
        long v = thuc.getAsLong();
        if (mong == v) {
            dat++;
            System.out.println("DAT  " + ten);
        } else {
            hong++;
            System.out.println("HONG " + ten + ": mong " + mong + ", thuc " + v);
        }
    }

    static void kiemNgoaiLe(String ten, long soTien) {
        try {
            phiChuyenKhoan(soTien, false);
            hong++;
            System.out.println("HONG " + ten + ": khong nem ngoai le");
        } catch (IllegalArgumentException e) {
            dat++;
            System.out.println("DAT  " + ten);
        }
    }

    public static void main(String[] args) {
        kiem("cung ngan hang", 0, () -> phiChuyenKhoan(2000000, true));
        kiem("bien 500000", 2000, () -> phiChuyenKhoan(500000, false));
        kiem("sau bien 500001", 7000, () -> phiChuyenKhoan(500001, false));
        kiem("bien 5000000", 7000, () -> phiChuyenKhoan(5000000, false));
        kiemNgoaiLe("so khong", 0);
        System.out.println("dat " + dat + ", hong " + hong);
    }
}
