package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class SmokeL03Test extends PostgresBaseTest {
    @Autowired AccountRepository repo;
    @Test void repoIsReady() { assertTrue(repo.count() >= 0); }
}
