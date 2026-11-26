package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class KiemL04Test extends PostgresBaseTest {
    @Autowired AccountRepo accounts;
    @Autowired JournalRepo journals;
    @Autowired IdempotencyRepo idems;
    @Autowired LedgerTransferService service;

    @BeforeEach
    void init() {
        journals.deleteAllInBatch();
        idems.deleteAllInBatch();
        accounts.deleteAllInBatch();
        accounts.save(new Account("TK1", 1_000_000));
        accounts.save(new Account("TK2", 1_000_000));
    }

    @Test
    void doubleEntryBalancedAndIdempotentReplay() {
        String tx1 = service.transfer("k-dup-1", "TK1", "TK2", 300_000);
        String tx2 = service.transfer("k-dup-1", "TK1", "TK2", 300_000);
        assertEquals(tx1, tx2);
        assertEquals(700_000L, accounts.findById("TK1").orElseThrow().getBalance());
        assertEquals(1_300_000L, accounts.findById("TK2").orElseThrow().getBalance());
        assertEquals(0L, journals.netSum());
        assertEquals(2L, journals.count());
    }

    @Test
    void concurrentOppositeDirectionTransfersWithoutDeadlock() throws Exception {
        int n = 10;
        CountDownLatch start = new CountDownLatch(1);
        CountDownLatch done = new CountDownLatch(n);
        try (var pool = Executors.newFixedThreadPool(4)) {
            for (int i = 0; i < n; i++) {
                final int idx = i;
                pool.submit(() -> {
                    try {
                        start.await();
                        if (idx % 2 == 0) {
                            service.transfer("k-c-" + idx, "TK1", "TK2", 10_000);
                        } else {
                            service.transfer("k-c-" + idx, "TK2", "TK1", 10_000);
                        }
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    } finally {
                        done.countDown();
                    }
                });
            }
            start.countDown();
            done.await(30, TimeUnit.SECONDS);
        }
        assertEquals(1_000_000L, accounts.findById("TK1").orElseThrow().getBalance());
        assertEquals(1_000_000L, accounts.findById("TK2").orElseThrow().getBalance());
        assertEquals(0L, journals.netSum());
    }

    @Test
    void versionColumnIncrementsOnUpdate() {
        service.transfer("k-ver-1", "TK1", "TK2", 50_000);
        assertEquals(1L, accounts.findById("TK1").orElseThrow().getVersion());
        assertEquals(1L, accounts.findById("TK2").orElseThrow().getVersion());
    }
}
