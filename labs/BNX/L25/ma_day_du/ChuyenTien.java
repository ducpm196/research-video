import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.*;
import org.springframework.transaction.support.*;
public class ChuyenTien {
  final JdbcTemplate j;
  final NhatKy nk;
  ChuyenTien(JdbcTemplate j, NhatKy nk) { this.j = j; this.nk = nk; }
  static final String TRU =
      "update tk set so_du = so_du - 100 where id = 1";
  @Transactional
  public void chuyenLoi(boolean rieng) {
    j.update(TRU);
    if (rieng) nk.ghiRieng("thu chuyen"); else nk.ghi("thu chuyen");
    throw new IllegalStateException("het han muc");
  }
  @Transactional
  public void chuyenKiem() throws Exception {
    j.update(TRU);
    throw new Exception("loi kiem tra");
  }
  @Transactional(rollbackFor = Exception.class)
  public void chuyenKiemHoanTac() throws Exception {
    j.update(TRU);
    throw new Exception("loi kiem tra");
  }
  @Transactional(propagation = Propagation.REQUIRES_NEW)
  public boolean rieng() {
    return TransactionSynchronizationManager
        .isActualTransactionActive();
  }
  public boolean goiNoiBo() { return this.rieng(); }
}
