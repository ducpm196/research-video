package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.inOrder;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InOrder;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class KiemL09UnitTest {
    @Mock AccountGateway accounts;
    @Mock AlertPort alerts;
    @InjectMocks UnitTransferService service;

    @Test
    void insufficientBalanceNeverDebitsOrAlerts() {
        when(accounts.balanceOf("A")).thenReturn(50_000L);
        assertThrows(IllegalStateException.class, () -> service.execute("A", "B", 200_000L));
        verify(accounts, never()).debit("A", 200_000L);
        verify(alerts, never()).sent("A", "B", 200_000L);
    }

    @Test
    void happyPathVerifiesStrictOrder() {
        when(accounts.balanceOf("A")).thenReturn(500_000L);
        assertEquals("OK:A->B:100000", service.execute("A", "B", 100_000L));
        InOrder ord = inOrder(accounts, alerts);
        ord.verify(accounts).balanceOf("A");
        ord.verify(accounts).debit("A", 100_000L);
        ord.verify(accounts).credit("B", 100_000L);
        ord.verify(alerts).sent("A", "B", 100_000L);
    }
}
