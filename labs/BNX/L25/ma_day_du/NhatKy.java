import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.*;
public class NhatKy {
  final JdbcTemplate j;
  NhatKy(JdbcTemplate j) { this.j = j; }
  @Transactional
  public void ghi(String m) {
    j.update("insert into nhat_ky values (?)", m);
  }
  @Transactional(propagation = Propagation.REQUIRES_NEW)
  public void ghiRieng(String m) {
    j.update("insert into nhat_ky values (?)", m);
  }
}
