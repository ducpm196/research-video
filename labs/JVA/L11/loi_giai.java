interface LaiSuat {
    long lai(long goc);
}

class LaiCoDinh implements LaiSuat {
    @Override
    public long lai(long goc) {
        return goc * 4 / 1000;                       // 0,4% (số minh hoạ)
    }
}

class LaiBac implements LaiSuat {
    @Override
    public long lai(long goc) {
        return goc < 50000000 ? goc * 3 / 1000 : goc * 5 / 1000;   // hai bậc (số minh hoạ)
    }
}

record KyHan(String ten, int thang) {}

enum LoaiThe { THUONG, VANG }

public class LaiSuatLab {
    static long hanMuc(LoaiThe t) {
        return switch (t) {
            case THUONG -> 20000000;
            case VANG -> 100000000;
        };
    }

    public static void main(String[] args) {
        LaiSuat[] ds = { new LaiCoDinh(), new LaiBac() };
        for (LaiSuat l : ds) {
            System.out.println(l.lai(10000000) + " " + l.lai(80000000));
        }
        KyHan a = new KyHan("6T", 6);
        KyHan b = new KyHan("6T", 6);
        System.out.println(a.equals(b) + " " + (a == b));
        System.out.println("Han muc VANG: " + hanMuc(LoaiThe.VANG));
    }
}
