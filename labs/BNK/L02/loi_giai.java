import java.lang.reflect.*;
public class ChuyenKhoanProxy {
    interface Dich { void chuyenKhoan(); void tinhPhi(); void thongBao(); }
    static int moGiaoDich = 0;
    static class DichThat implements Dich {
        public void chuyenKhoan() { tinhPhi(); thongBao(); }   // hai lời gọi thẳng bằng this
        public void tinhPhi() { }
        public void thongBao() { }
    }
    public static void main(String[] args) {
        Dich that = new DichThat();
        Dich proxy = (Dich) Proxy.newProxyInstance(Dich.class.getClassLoader(), new Class<?>[] { Dich.class },
            (p, m, a) -> {
                moGiaoDich++;
                return m.invoke(that, a);
            });
        proxy.chuyenKhoan();
        System.out.println("sau chuyenKhoan: " + moGiaoDich);
        proxy.tinhPhi();
        System.out.println("sau tinhPhi: " + moGiaoDich);
        proxy.thongBao();
        System.out.println("sau thongBao: " + moGiaoDich);
    }
}
