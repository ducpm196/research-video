import org.hibernate.*;
import java.util.*;
public class DemTrang {
  static void in(String ten, Session s, List<Khach> ds, long cau) {
    System.out.println(ten + ": " + ds.size() + " khach, " + cau
        + " cau, ngu canh giu " + s.getStatistics().getEntityCount() + " doi tuong");
  }
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(500);
    try (Session s = sf.openSession()) {
      sf.getStatistics().clear();
      List<Khach> ds = s.createQuery("select k from Khach k join fetch k.tk",
          Khach.class).setMaxResults(20).getResultList();
      in("cat tai cho (join fetch + trang)", s, ds, sf.getStatistics().getPrepareStatementCount());
    }
    try (Session s = sf.openSession()) {
      sf.getStatistics().clear();
      List<Long> ma = s.createQuery("select k.id from Khach k order by k.id",
          Long.class).setMaxResults(20).getResultList();
      List<Khach> ds = s.createQuery("select k from Khach k join fetch k.tk "
          + "where k.id in :ma", Khach.class).setParameter("ma", ma).getResultList();
      in("hai buoc (lay ma roi join fetch)", s, ds, sf.getStatistics().getPrepareStatementCount());
    }
  }
}
