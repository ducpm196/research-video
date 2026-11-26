package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class KiemL06Test extends KafkaBaseTest {
    @Autowired OrderOutboxService outboxSvc;
    @Autowired OutboxRepo outboxRepo;
    @Autowired TransferEventConsumer consumer;

    @Test
    void rolledBackOrderProducesZeroOutboxRows() {
        long before = outboxRepo.count();
        assertThrows(IllegalStateException.class, () -> outboxSvc.createTransferOrder("TX-ROLLED", true));
        assertEquals(before, outboxRepo.count());
    }

    @Test
    void validOutboxEventPublishedAndConsumed() throws Exception {
        outboxSvc.createTransferOrder("TX-VALID-100", false);
        int sent = outboxSvc.publishPending();
        assertTrue(sent >= 1);
        long deadline = System.currentTimeMillis() + 15_000;
        while (!consumer.getProcessed().contains("TX-VALID-100") && System.currentTimeMillis() < deadline) {
            Thread.sleep(150);
        }
        assertTrue(consumer.getProcessed().contains("TX-VALID-100"));
        assertEquals(0, outboxRepo.findByStatusOrderByIdAsc("PENDING").size());
    }

    @Test
    void poisonMessageRoutedToDltAfter3Attempts() throws Exception {
        outboxSvc.createTransferOrder("POISON:bad-json", false);
        outboxSvc.publishPending();
        long deadline = System.currentTimeMillis() + 20_000;
        while (!consumer.getDltReceived().contains("POISON:bad-json") && System.currentTimeMillis() < deadline) {
            Thread.sleep(150);
        }
        assertTrue(consumer.getDltReceived().contains("POISON:bad-json"));
    }
}
