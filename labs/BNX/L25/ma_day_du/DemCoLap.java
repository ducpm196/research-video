import java.sql.*;
public class DemCoLap {
  static final String U = "jdbc:h2:mem:iso;DB_CLOSE_DELAY=-1";
  static long so(Connection c) throws Exception {
    try (ResultSet r = c.createStatement().executeQuery(
        "select so_du from tk where id = 1")) {
      r.next();
      return r.getLong(1);
    }
  }
  static String thu(int muc) throws Exception {
    try (Connection a = DriverManager.getConnection(U, "sa", "");
         Connection b = DriverManager.getConnection(U, "sa", "")) {
      b.createStatement().execute("update tk set so_du = 1000");
      a.setAutoCommit(false);
      a.setTransactionIsolation(muc);
      long l1 = so(a);
      b.createStatement().execute("update tk set so_du = so_du + 50");
      long l2 = so(a);
      a.commit();
      return l1 + " -> " + l2;
    }
  }
  public static void main(String[] x) throws Exception {
    try (Connection c = DriverManager.getConnection(U, "sa", "")) {
      c.createStatement().execute("create table tk (id int, so_du bigint)");
      c.createStatement().execute("insert into tk values (1, 1000)");
    }
    System.out.println("READ_COMMITTED: "
        + thu(Connection.TRANSACTION_READ_COMMITTED));
    System.out.println("REPEATABLE_READ: "
        + thu(Connection.TRANSACTION_REPEATABLE_READ));
    System.out.println("SERIALIZABLE: "
        + thu(Connection.TRANSACTION_SERIALIZABLE));
  }
}
