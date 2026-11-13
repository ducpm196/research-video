import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

public class MiniDiKho {
    @Retention(RetentionPolicy.RUNTIME) @interface ThanhPhan {}
    @Retention(RetentionPolicy.RUNTIME) @interface Tiem {}

    @ThanhPhan static class KhoHang { int soLuong() { return 12; } }
    @ThanhPhan static class BangGia { long gia() { return 45000; } }
    @ThanhPhan static class DonHang {
        @Tiem KhoHang kho;
        @Tiem BangGia bang;
        long tong() { return kho.soLuong() * bang.gia(); }
    }

    static Map<Class<?>, Object> hop = new HashMap<>();

    static Object lay(Class<?> loai) throws Exception {
        if (hop.containsKey(loai)) {
            return hop.get(loai);
        }
        Object o = loai.getDeclaredConstructor().newInstance();
        hop.put(loai, o);
        for (Field f : loai.getDeclaredFields()) {
            if (f.isAnnotationPresent(Tiem.class)) {
                f.setAccessible(true);
                f.set(o, lay(f.getType()));
            }
        }
        return o;
    }

    public static void main(String[] args) throws Exception {
        DonHang d = (DonHang) lay(DonHang.class);
        System.out.println("Tong gia tri kho: " + d.tong());
        System.out.println("Cung mot BangGia: " + (d.bang == lay(BangGia.class)));
        System.out.println("So thanh phan: " + hop.size());
    }
}
