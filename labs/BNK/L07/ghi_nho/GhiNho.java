import java.util.Arrays;
public class GhiNho {
    static int[] chay(boolean ghiNhoTruoc) {
        int[] dem = new int[5];                 // số lần xử lý mỗi thông điệp 0..4
        int viTri = 0;                          // vị trí đã ghi nhớ
        boolean daSap = false;
        while (viTri < 5) {
            int m = viTri;
            if (ghiNhoTruoc) {
                viTri = m + 1;                  // ghi nhớ trước
                if (m == 2 && !daSap) { daSap = true; continue; }   // sập: chưa kịp xử lý
                dem[m]++;
            } else {
                dem[m]++;                       // xử lý trước
                if (m == 2 && !daSap) { daSap = true; continue; }   // sập: chưa kịp ghi nhớ
                viTri = m + 1;
            }
        }
        return dem;
    }
    public static void main(String[] args) {
        System.out.println("ghi nho truoc: " + Arrays.toString(chay(true)));
        System.out.println("xu ly truoc:   " + Arrays.toString(chay(false)));
    }
}
