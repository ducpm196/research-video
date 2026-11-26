package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.StringRedisTemplate;

@SpringBootTest
class KiemL05Test extends RedisBaseTest {
    @Autowired AccountRepo accounts;
    @Autowired BalanceCacheService cache;
    @Autowired StringRedisTemplate redis;

    @BeforeEach
    void init() {
        redis.getConnectionFactory().getConnection().serverCommands().flushDb();
        accounts.deleteAll();
        accounts.save(new Account("TK1", 500_000));
        cache.resetDbReads();
    }

    @Test
    void cacheAsideHitAvoidsSecondDbRead() {
        assertEquals(500_000L, cache.getBalance("TK1"));
        assertEquals(500_000L, cache.getBalance("TK1"));
        assertEquals(1, cache.getDbReads());
    }

    @Test
    void depositInvalidatesStaleCacheImmediately() {
        assertEquals(500_000L, cache.getBalance("TK1"));
        cache.deposit("TK1", 200_000L);
        assertEquals(700_000L, cache.getBalance("TK1"));
    }

    @Test
    void stampedeGuardWithSetNxPrevents20DbReads() throws Exception {
        int n = 20;
        CountDownLatch ready = new CountDownLatch(1);
        List<Future<Long>> results = new ArrayList<>();
        try (var pool = Executors.newFixedThreadPool(8)) {
            for (int i = 0; i < n; i++) {
                results.add(pool.submit(() -> {
                    ready.await();
                    return cache.getBalance("TK1");
                }));
            }
            ready.countDown();
            for (var f : results) {
                assertEquals(500_000L, f.get());
            }
        }
        assertTrue(cache.getDbReads() <= 2, "SET NX phai giam DB reads con <= 2, thuc te=" + cache.getDbReads());
    }
}
