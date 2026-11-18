import java.sql.*;
import javax.sql.DataSource;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.jdbc.datasource.AbstractDataSource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.support.TransactionTemplate;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
public class DemBe {
  static class Be extends AbstractDataSource {
    final Semaphore cho;
    Be(int n) { cho = new Semaphore(n); }
    public Connection getConnection() throws SQLException {
      try {
        if (!cho.tryAcquire(400, TimeUnit.MILLISECONDS))
          throw new SQLException("het gio cho ket noi");
      } catch (InterruptedException e) { throw new SQLException(e); }
      Connection c = DriverManager.getConnection(
          "jdbc:h2:mem:be;DB_CLOSE_DELAY=-1", "sa", "");
      return (Connection) java.lang.reflect.Proxy.newProxyInstance(
          getClass().getClassLoader(), new Class<?>[] {Connection.class},
          (p, m, a) -> {
            Object r = m.invoke(c, a);
            if (m.getName().equals("close")) cho.release();
            return r;
          });
    }
    public Connection getConnection(String u, String p)
        throws SQLException { return getConnection(); }
  }
  static void doc(DataSource ds) {
    new JdbcTemplate(ds).queryForObject("select 1", Integer.class);
  }
  static void cho(CyclicBarrier b) {
    try { b.await(); } catch (Exception e) { }
  }
  static int chay(int luong, int be) throws Exception {
    var ds = new Be(be);
    var tm = new DataSourceTransactionManager(ds);
    var ngoai = new TransactionTemplate(tm);
    var trong = new TransactionTemplate(tm);
    trong.setPropagationBehavior(
        TransactionDefinition.PROPAGATION_REQUIRES_NEW);
    var loi = new AtomicInteger();
    var xong = new CountDownLatch(luong);
    var nhom = Executors.newFixedThreadPool(luong);
    var cua = new CyclicBarrier(luong);
    var cua2 = new CyclicBarrier(luong);
    for (int i = 0; i < luong; i++) nhom.submit(() -> {
      try {
        ngoai.executeWithoutResult(s -> {
          doc(ds);
          cho(cua);
          try {
            trong.executeWithoutResult(t -> doc(ds));
          } catch (Exception e) { loi.incrementAndGet(); }
          cho(cua2);
        });
      } catch (Exception e) { }
      xong.countDown();
    });
    xong.await();
    nhom.shutdown();
    return loi.get();
  }
  public static void main(String[] x) throws Exception {
    for (int[] c : new int[][] {{3, 3}, {3, 4}, {6, 6}, {6, 7}})
      System.out.println(c[0] + " luong, be " + c[1] + " ket noi: "
          + chay(c[0], c[1]) + " luong het gio");
  }
}
