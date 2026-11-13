import java.util.Arrays;

public class SauTaiKhoan {
    public static void main(String[] args) {
        long[] soDu = {820000, 150000, 2400000, 150000, 3600000, 90000};
        long tong = 0;
        int nhoNhat = 0;                             // chỉ số của số dư nhỏ nhất
        int dem = 0;                                 // số tài khoản dưới 200000
        for (int i = 0; i < soDu.length; i++) {
            tong += soDu[i];
            if (soDu[i] < soDu[nhoNhat]) {
                nhoNhat = i;
            }
            if (soDu[i] < 200000) {
                dem++;
            }
        }
        System.out.println("Tong: " + tong);
        System.out.println("Nho nhat: " + soDu[nhoNhat] + " o chi so " + nhoNhat);
        System.out.println("So tai khoan duoi 200000: " + dem);
        long[] banSao = Arrays.copyOf(soDu, soDu.length);
        Arrays.sort(banSao);
        System.out.println(Arrays.toString(banSao));
        System.out.println("Goc: " + Arrays.toString(soDu));
    }
}
