package vn.nganhang.chuyenkhoan;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
@SpringBootTest
class SmokeL10Test extends FullStackBaseTest {
    @Test void containersStarted() { assertTrue(PG.isRunning() && REDIS.isRunning() && KAFKA.isRunning()); }
}
