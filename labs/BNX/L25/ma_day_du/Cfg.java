import javax.sql.DataSource;
import org.springframework.context.annotation.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.*;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;
@Configuration
@EnableTransactionManagement
@EnableAspectJAutoProxy
public class Cfg {
  @Bean DataSource ds() {
    return new DriverManagerDataSource(
        "jdbc:h2:mem:l25;DB_CLOSE_DELAY=-1", "sa", "");
  }
  @Bean JdbcTemplate jt(DataSource d) { return new JdbcTemplate(d); }
  @Bean PlatformTransactionManager tm(DataSource d) {
    return new DataSourceTransactionManager(d);
  }
  @Bean NhatKy nk(JdbcTemplate j) { return new NhatKy(j); }
  @Bean ChuyenTien ct(JdbcTemplate j, NhatKy n) {
    return new ChuyenTien(j, n);
  }
  @Bean DoGio dg() { return new DoGio(); }
}
