package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class SmokeL04Test extends PostgresBaseTest {
    @Autowired JournalRepo journals;
    @Test void netIsZero() { assertEquals(0L, journals.netSum()); }
}
