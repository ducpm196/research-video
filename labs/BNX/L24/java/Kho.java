import org.hibernate.*;
import org.hibernate.cfg.Configuration;
public class Kho {
  static SessionFactory mo(int n) {
    SessionFactory sf = new Configuration()
        .addAnnotatedClass(Khach.class)
        .addAnnotatedClass(TaiKhoan.class)
        .setProperty("hibernate.connection.url", "jdbc:h2:mem:bnx")
        .setProperty("hibernate.hbm2ddl.auto", "create-drop")
        .setProperty("hibernate.generate_statistics", "true")
        .buildSessionFactory();
    try (Session s = sf.openSession()) {
      Transaction t = s.beginTransaction();
      for (long i = 1; i <= n; i++) {
        Khach k = new Khach();
        k.id = i;
        k.ten = "K" + i;
        s.persist(k);
        for (long j = 1; j <= 2; j++) {
          TaiKhoan a = new TaiKhoan();
          a.id = i * 10 + j;
          a.khach = k;
          a.soDu = 1000 * j;
          s.persist(a);
        }
      }
      t.commit();
    }
    return sf;
  }
  static SessionFactory xem() {      // cùng CSDL trong bộ nhớ, bật in câu SQL
    return new Configuration()
        .addAnnotatedClass(Khach.class)
        .addAnnotatedClass(TaiKhoan.class)
        .setProperty("hibernate.connection.url", "jdbc:h2:mem:bnx")
        .setProperty("hibernate.show_sql", "true")
        .buildSessionFactory();
  }
}
