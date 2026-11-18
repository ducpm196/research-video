import org.springframework.aop.support.AopUtils;
import org.springframework.context.annotation.*;
import org.springframework.jdbc.core.JdbcTemplate;
public class DemTx {
  static JdbcTemplate j;
  interface Lenh { void chay() throws Exception; }
  static void mo(String ten, Lenh l) {
    j.update("delete from nhat_ky");
    j.update("update tk set so_du = 1000 where id = 1");
    try { l.chay(); } catch (Exception e) { }
    long sd = j.queryForObject(
        "select so_du from tk where id = 1", Long.class);
    long nk = j.queryForObject(
        "select count(*) from nhat_ky", Long.class);
    System.out.println(ten + ": so du " + sd + ", nhat ky " + nk);
  }
  public static void main(String[] a) {
    var c = new AnnotationConfigApplicationContext(Cfg.class);
    j = c.getBean(JdbcTemplate.class);
    j.execute("create table tk (id int, so_du bigint)");
    j.execute("create table nhat_ky (m varchar(40))");
    j.update("insert into tk values (1, 1000)");
    var ct = c.getBean(ChuyenTien.class);
    System.out.println("ct la proxy: " + AopUtils.isAopProxy(ct));
    mo("1 REQUIRED, loi chay", () -> ct.chuyenLoi(false));
    mo("2 REQUIRES_NEW, loi chay", () -> ct.chuyenLoi(true));
    mo("3 loi kiem tra, mac dinh", ct::chuyenKiem);
    mo("4 loi kiem tra, rollbackFor", ct::chuyenKiemHoanTac);
    System.out.println("goi qua proxy: giao dich " + ct.rieng());
    System.out.println("goi noi bo: giao dich " + ct.goiNoiBo());
    var dg = c.getBean(DoGio.class);
    System.out.println("doan cat chay " + dg.dem + " lan, khong am "
        + dg.khongAm);
  }
}
