import org.hibernate.*;
import org.hibernate.stat.Statistics;
public class DemN1 {
  static final String LUOI = "select k from Khach k where k.id <= :n";
  static final String NHANH =
      "select k from Khach k join fetch k.tk where k.id <= :n";
  static long dem(SessionFactory sf, String q, long n) {
    Statistics st = sf.getStatistics();
    st.clear();
    try (Session s = sf.openSession()) {
      for (Khach k : s.createQuery(q, Khach.class)
          .setParameter("n", n).getResultList())
        k.tk.size();           // đụng vào danh sách tài khoản
    }
    return st.getPrepareStatementCount();
  }
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(500);
    for (long n : new long[] {5, 50, 500})
      System.out.println(n + " khach: tai luoi " + dem(sf, LUOI, n)
          + " cau, JOIN FETCH " + dem(sf, NHANH, n) + " cau");
  }
}
