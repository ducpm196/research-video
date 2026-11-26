package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class KiemL02Test {
    @Autowired AccountRepo accounts;
    @Autowired AuditEntryRepo audits;
    @Autowired TransferService service;

    @BeforeEach
    void seed() {
        audits.deleteAll();
        accounts.deleteAll();
        accounts.save(new Account("A", 500_000));
        accounts.save(new Account("B", 200_000));
    }

    @Test
    void validTransferCommitsBalancesAndAudit() throws Exception {
        service.transfer("A", "B", 150_000);
        assertEquals(350_000, accounts.findById("A").orElseThrow().getBalance());
        assertEquals(350_000, accounts.findById("B").orElseThrow().getBalance());
        assertEquals(1, audits.count());
    }

    @Test
    void checkedExceptionRollsBackAccountButKeepsRequiresNewAudit() {
        assertThrows(InsufficientFundsException.class, () -> service.transfer("A", "B", 900_000));
        assertEquals(500_000, accounts.findById("A").orElseThrow().getBalance());
        assertEquals(200_000, accounts.findById("B").orElseThrow().getBalance());
        assertEquals(1, audits.count());
    }

    @Test
    void selfTransferThrowsIllegalArgument() {
        assertThrows(IllegalArgumentException.class, () -> service.transfer("A", "A", 10_000));
    }

    @Test
    void conservationOfTotalBalance() throws Exception {
        service.transfer("A", "B", 100_000);
        long total = accounts.findAll().stream().mapToLong(Account::getBalance).sum();
        assertEquals(700_000, total);
    }
}
