class Vi {
    private String ten;
    private long tien;                       // bất biến: tien luôn >= 0

    Vi(String ten) {                         // hàm tạo: ví mới, tiền 0
        this.ten = ten;
        this.tien = 0;
    }

    void them(long soTien) {
        if (soTien > 0) {
            tien += soTien;
        }
    }

    boolean chi(long soTien) {
        if (soTien <= 0 || soTien > tien) {
            System.out.println("Tu choi chi " + soTien + ", con " + tien);
            return false;
        }
        tien -= soTien;
        return true;
    }

    long layTien() {
        return tien;
    }

    public String toString() {
        return ten + ": " + tien + " dong";
    }
}

public class QuanLyVi {
    public static void main(String[] args) {
        Vi lan = new Vi("Lan");
        Vi minh = new Vi("Minh");
        lan.them(800000);
        lan.chi(250000);
        lan.chi(900000);                     // quá số tiền đang có: bị từ chối
        minh.them(50000);
        minh.chi(50000);
        System.out.println(lan);
        System.out.println(minh);
        System.out.println("Tong: " + (lan.layTien() + minh.layTien()));
    }
}
