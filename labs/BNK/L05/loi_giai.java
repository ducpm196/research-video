public class ThuTuKhoa {
    public static void main(String[] args) {
        int[][] lenh = { {4, 9}, {9, 4}, {7, 4}, {4, 7} };
        for (int[] l : lenh) {
            int dau = Math.min(l[0], l[1]);
            int sau = Math.max(l[0], l[1]);
            System.out.println(l[0] + " -> " + l[1] + ": khoa " + dau + " roi " + sau);
        }
    }
}
