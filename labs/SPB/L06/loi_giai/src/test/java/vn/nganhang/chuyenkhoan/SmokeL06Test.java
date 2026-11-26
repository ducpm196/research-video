package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class SmokeL06Test extends KafkaBaseTest {
    @Test void kafkaIsUp() { assertTrue(KAFKA.getBootstrapServers().contains(":")); }
}
