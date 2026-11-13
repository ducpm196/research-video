public class PhiLech {
    public static void main(String[] args) {
        double tong = 0;
        long phanMuoi = 0;
        for (int i = 0; i < 20; i++) {
            tong += 0.3;
            phanMuoi += 3;
        }
        System.out.println("double: " + tong);
        System.out.println("so nguyen: " + phanMuoi + " phan muoi");
        System.out.println("bang 6? " + (tong == 6.0));
    }
}
