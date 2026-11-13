public class NguoiNgoiKhong {
    public static void main(String[] args) {
        int phanVung = 7, bo = 9, p = 0, khong = 0;
        for (int b = 0; b < bo; b++) {
            int so = phanVung / bo + (b < phanVung % bo ? 1 : 0);
            StringBuilder sb = new StringBuilder("bo doc " + b + ":");
            if (so == 0) { sb.append(" ngoi khong"); khong++; }
            for (int k = 0; k < so; k++) sb.append(" P").append(p++);
            System.out.println(sb);
        }
        System.out.println("so nguoi ngoi khong: " + khong);
    }
}
