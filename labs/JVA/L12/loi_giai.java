import java.util.ArrayList;
import java.util.HashMap;

class KhongDuTien extends Exception {
    KhongDuTien(String thongBao) { super(thongBao); }
}

record Lenh(String tu, String den, long tien) {}

class SoCai {
    private HashMap<String, Long> soDu = new HashMap<>();
    private long tongGoc = 0;

    void mo(String stk, long tien) {
        soDu.put(stk, tien);
        tongGoc += tien;                      // tổng tiền phải giữ mãi
    }

    long tong() {
        long t = 0;
        for (long x : soDu.values()) {
            t += x;
        }
        return t;
    }

    long lay(String stk) {
        Long v = soDu.get(stk);
        if (v == null) {
            throw new IllegalArgumentException("Khong co tai khoan " + stk);
        }
        return v;
    }

    void chuyen(Lenh l) throws KhongDuTien {
        long a = lay(l.tu());                 // kiểm tra trước ...
        long b = lay(l.den());
        if (l.tien() <= 0) {
            throw new IllegalArgumentException("So tien phai duong");
        }
        if (l.tien() > a) {
            throw new KhongDuTien(l.tu() + " chi co " + a);
        }
        soDu.put(l.tu(), a - l.tien());       // ... sửa sau: trừ bên gửi
        soDu.put(l.den(), b + l.tien());      // cộng bên nhận
        kiem();                               // kiểm bất biến sau MỖI lần chuyển
    }

    void kiem() {
        if (tong() != tongGoc) {
            throw new IllegalStateException("Lech tong " + tong() + " != " + tongGoc);
        }
    }
}

public class SoCaiLab {
    public static void main(String[] args) {
        SoCai so = new SoCai();
        so.mo("P", 2000000);
        so.mo("Q", 800000);
        so.mo("R", 1200000);
        System.out.println("Mo xong: tong " + so.tong());
        ArrayList<Lenh> ds = new ArrayList<>();
        ds.add(new Lenh("P", "Q", 500000));
        ds.add(new Lenh("Q", "R", 2000000));
        ds.add(new Lenh("P", "Z", 10000));
        ds.add(new Lenh("R", "P", 700000));
        for (Lenh l : ds) {
            try {
                so.chuyen(l);
                System.out.println("OK " + l);
            } catch (KhongDuTien e) {
                System.out.println("TU CHOI " + e.getMessage());
            } catch (IllegalArgumentException e) {
                System.out.println("SAI LENH " + e.getMessage());
            }
        }
        System.out.println("P=" + so.lay("P") + " Q=" + so.lay("Q") + " R=" + so.lay("R"));
        System.out.println("Cuoi ngay: tong " + so.tong());
    }
}
