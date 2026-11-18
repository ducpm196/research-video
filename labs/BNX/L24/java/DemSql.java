import org.hibernate.*;
public class DemSql {
  public static void main(String[] x) {
    SessionFactory goc = Kho.mo(2);
    SessionFactory sf = Kho.xem();
    try (Session s = sf.openSession()) {
      for (Khach k : s.createQuery("select k from Khach k",
          Khach.class).getResultList())
        System.out.println(k.ten + ": " + k.tk.size() + " tai khoan");
    }
  }
}
