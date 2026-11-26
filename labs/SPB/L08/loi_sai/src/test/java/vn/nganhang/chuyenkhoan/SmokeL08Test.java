package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.time.Instant;
import org.junit.jupiter.api.Test;

class SmokeL08Test {
    @Test void signAndVerify() {
        JwtService svc = new JwtService();
        String tok = svc.sign("an", "TELLER", Instant.now().getEpochSecond() + 300);
        assertEquals("an", svc.verify(tok).sub());
    }
}
