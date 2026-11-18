import java.util.*;
import java.util.function.Supplier;

interface MiniServlet {
    void init();
    String service(String ten);
    void destroy();
}

class ChaoVi implements MiniServlet {
    int dem = 0;
    public void init() { System.out.println("init ChaoVi"); }
    public String service(String ten) { dem++; return "Xin chao " + ten + " (so " + dem + ")"; }
    public void destroy() { System.out.println("destroy ChaoVi"); }
}

class ChaoAnh implements MiniServlet {
    int dem = 0;
    public void init() { System.out.println("init ChaoAnh"); }
    public String service(String ten) { dem++; return "Hello " + ten + " (so " + dem + ")"; }
    public void destroy() { System.out.println("destroy ChaoAnh"); }
}

public class MauBoChua {
    Map<String, Supplier<MiniServlet>> khaiBao = new LinkedHashMap<>();
    Map<String, MiniServlet> dangChay = new LinkedHashMap<>();

    String xuLy(String duong, String ten) {
        MiniServlet s = dangChay.get(duong);
        if (s == null) {
            s = khaiBao.get(duong).get();
            s.init();
            dangChay.put(duong, s);
        }
        return duong + "?ten=" + ten + " -> " + s.service(ten);
    }

    void dung() {
        for (MiniServlet s : dangChay.values()) s.destroy();
    }

    public static void main(String[] a) {
        MauBoChua c = new MauBoChua();
        c.khaiBao.put("/vi", ChaoVi::new);
        c.khaiBao.put("/en", ChaoAnh::new);
        System.out.println(c.xuLy("/vi", "Lan"));
        System.out.println(c.xuLy("/vi", "Minh"));
        System.out.println(c.xuLy("/en", "Ann"));
        System.out.println(c.xuLy("/vi", "Hoa"));
        c.dung();
    }
}
