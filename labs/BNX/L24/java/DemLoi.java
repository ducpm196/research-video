import org.hibernate.*;
public class DemLoi {
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(3);
    Khach k;
    try (Session s = sf.openSession()) {
      k = s.find(Khach.class, 1L);
    }                                 // phiên đã đóng
    try {
      System.out.println(k.tk.size());
    } catch (LazyInitializationException e) {
      System.out.println("loi: " + e.getClass().getSimpleName());
    }
  }
}
