public class MaChan {
    static long maCuoi = 0;
    static String giaTri = "";
    static boolean ghi(long ma, String v) {
        if (ma < maCuoi) return false;                   // từ chối mã chặn cũ
        maCuoi = ma;
        giaTri = v;
        return true;
    }
    public static void main(String[] args) {
        System.out.println("B ghi (ma 34): " + ghi(34, "B"));              // B lấy khoá sau, mã 34
        System.out.println("A tinh day ghi (ma 33): " + ghi(33, "A"));     // A tạm dừng rồi ghi muộn
        System.out.println("gia tri cuoi: " + giaTri);
    }
}
