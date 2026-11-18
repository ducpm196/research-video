import org.hibernate.*;
public class DemNho {
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(500);
    try (Session s = sf.openSession()) {
      for (Khach k : s.createQuery("select k from Khach k join fetch "
          + "k.tk", Khach.class).getResultList())
        k.ten.length();
      System.out.println("ngu canh giu: "
          + s.getStatistics().getEntityCount() + " doi tuong");
      s.clear();
      System.out.println("sau clear: "
          + s.getStatistics().getEntityCount() + " doi tuong");
    }
  }
}
