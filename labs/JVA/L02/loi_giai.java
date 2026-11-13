public class ChiaHoaDon {
    public static void main(String[] args) {
        long tong = 2500000;                        // hoá đơn chia đều (số minh hoạ)
        int soNguoi = 7;
        System.out.println("Moi nguoi: " + tong / soNguoi);
        System.out.println("Du: " + tong % soNguoi);
        long soTien = 987654;
        System.out.println("Phi dung: " + soTien * 3 / 1000);          // phí 0,3%: nhân trước, chia sau
        System.out.println("Phi chia truoc: " + soTien / 1000 * 3);    // chia trước: mất phần lẻ
        int soNguoi2 = 0;
        boolean chiaDuoc = soNguoi2 != 0 && tong / soNguoi2 > 100000;  // phép kiểm đứng trước
        System.out.println("Chia duoc: " + chiaDuoc);
    }
}
