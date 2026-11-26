package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;

class UnitTransferServiceTest {
    @Test void executesHappyPath() {
        AccountGateway gw = mock(AccountGateway.class);
        AlertPort alerts = mock(AlertPort.class);
        when(gw.balanceOf("A")).thenReturn(500_000L);
        UnitTransferService svc = new UnitTransferService(gw, alerts);
        assertEquals("OK:A->B:100000", svc.execute("A", "B", 100_000L));
    }
}
