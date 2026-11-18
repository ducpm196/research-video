import org.hibernate.*;
import org.hibernate.stat.Statistics;
public class DemBan {
  public static void main(String[] x) {
    SessionFactory sf = Kho.mo(3);
    Statistics st = sf.getStatistics();
    try (Session s = sf.openSession()) {
      st.clear();
      TaiKhoan a = s.find(TaiKhoan.class, 11L);
      TaiKhoan b = s.find(TaiKhoan.class, 11L);
      System.out.println("doc hai lan: cung doi tuong " + (a == b)
          + ", " + st.getPrepareStatementCount() + " cau SQL");
      Transaction t = s.beginTransaction();
      a.soDu = a.soDu + 500;          // không gọi hàm lưu nào
      s.createQuery("select count(t) from TaiKhoan t", Long.class)
          .getSingleResult();
      System.out.println("sau truy van, truoc chot: "
          + st.getEntityUpdateCount() + " UPDATE");
      t.commit();
    }
    try (Session s = sf.openSession()) {
      st.clear();
      TaiKhoan c = s.find(TaiKhoan.class, 12L);
      s.detach(c);                    // rời ngữ cảnh bền vững
      Transaction t = s.beginTransaction();
      c.soDu = c.soDu + 500;
      t.commit();
      System.out.println("sua doi tuong da roi: "
          + st.getEntityUpdateCount() + " UPDATE");
    }
    try (Session s = sf.openSession()) {
      System.out.println("so du 11: " + s.find(TaiKhoan.class, 11L).soDu
          + ", so du 12: " + s.find(TaiKhoan.class, 12L).soDu);
    }
  }
}
