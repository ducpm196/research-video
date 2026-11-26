package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import jakarta.persistence.EntityManagerFactory;
import java.util.List;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.support.TransactionTemplate;

@SpringBootTest
class KiemL03Test extends PostgresBaseTest {
    @Autowired AccountRepository accounts;
    @Autowired JournalEntryRepository journals;
    @Autowired EntityManagerFactory emf;
    @Autowired TransactionTemplate tx;

    @BeforeEach
    void setupData() {
        tx.executeWithoutResult(s -> {
            journals.deleteAllInBatch();
            accounts.deleteAllInBatch();
            for (int i = 1; i <= 20; i++) {
                Account a = accounts.save(new Account(String.format("ACC%02d", i), "Chu " + i, 100_000L * i));
                journals.save(new JournalEntry(a, 10_000L));
            }
        });
    }

    @Test
    void lazyTriggersNPlusOneAndJoinFetchUsesOneQuery() {
        Statistics stats = emf.unwrap(SessionFactory.class).getStatistics();
        stats.setStatisticsEnabled(true);

        stats.clear();
        tx.executeWithoutResult(s -> {
            List<Account> all = accounts.findAll();
            all.forEach(a -> a.getEntries().size());
        });
        long lazyCount = stats.getPrepareStatementCount();

        stats.clear();
        int loaded = tx.execute(s -> {
            List<Account> fast = accounts.findAllWithEntries();
            return fast.stream().mapToInt(a -> a.getEntries().size()).sum();
        });
        long fetchCount = stats.getPrepareStatementCount();

        assertEquals(20, loaded);
        assertTrue(lazyCount >= 21, "Lazy N+1 phai >= 21 SQL, thuc te=" + lazyCount);
        assertEquals(1L, fetchCount, "JOIN FETCH phai dung dung 1 SQL");
    }

    @Test
    void flywayValidatedSchemaHas20Accounts() {
        assertEquals(20, accounts.count());
        assertEquals(20, journals.count());
    }

    @Test
    void queryIsOrderedById() {
        List<Account> list = accounts.findAllWithEntries();
        assertEquals("ACC01", list.get(0).getId());
        assertEquals("ACC20", list.get(19).getId());
    }
}
