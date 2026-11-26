package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class KiemL10Test extends FullStackBaseTest {
    @Autowired MockMvc mvc;
    @Autowired AccountRepo accounts;
    @Autowired JournalRepo journals;
    @Autowired StringRedisTemplate redis;
    @Autowired FullStackService svc;

    @BeforeEach
    void reset() {
        redis.getConnectionFactory().getConnection().serverCommands().flushDb();
        journals.deleteAllInBatch();
        accounts.deleteAllInBatch();
        accounts.save(new Account("TK1", 1_000_000));
        accounts.save(new Account("TK2", 500_000));
    }

    @Test
    void endToEndHttpPostgresRedisInvalidationAndKafkaEvent() throws Exception {
        assertEquals(1_000_000L, svc.cachedBalance("TK1"));
        mvc.perform(post("/api/v1/full-transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromId\":\"TK1\",\"toId\":\"TK2\",\"amount\":250000}"))
            .andExpect(status().isCreated());

        assertEquals(750_000L, svc.cachedBalance("TK1"));
        assertEquals(750_000L, svc.cachedBalance("TK2"));
        assertEquals(0L, journals.net());

        long end = System.currentTimeMillis() + 15_000;
        while (!svc.getEvents().contains("TK1->TK2:250000") && System.currentTimeMillis() < end) {
            Thread.sleep(150);
        }
        assertTrue(svc.getEvents().contains("TK1->TK2:250000"));
    }

    @Test
    void allThreeRealContainersAreRunning() {
        assertTrue(PG.getJdbcUrl().startsWith("jdbc:postgresql://"));
        assertTrue(REDIS.isRunning());
        assertTrue(KAFKA.getBootstrapServers().contains(":"));
    }
}
