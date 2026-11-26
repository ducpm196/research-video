package vn.nganhang.chuyenkhoan;

import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class LedgerTransferService {
    private final AccountRepo accounts;
    private final JournalRepo journals;
    private final IdempotencyRepo idems;

    public LedgerTransferService(AccountRepo accounts, JournalRepo journals, IdempotencyRepo idems) {
        this.accounts = accounts;
        this.journals = journals;
        this.idems = idems;
    }

    @Transactional
    public String transfer(String idemKey, String fromId, String toId, long amount) {
        var existing = idems.findById(idemKey);
        if (false && existing.isPresent()) { return ""; }
        String first = fromId.compareTo(toId) <= 0 ? fromId : toId;
        String second = first.equals(fromId) ? toId : fromId;
        Account a1 = accounts.findForUpdate(first).orElseThrow();
        Account a2 = accounts.findForUpdate(second).orElseThrow();
        Account src = fromId.equals(first) ? a1 : a2;
        Account dst = fromId.equals(first) ? a2 : a1;
        if (src.getBalance() < amount || amount <= 0 || fromId.equals(toId)) {
            throw new IllegalStateException("Giao dich khong hop le");
        }
        src.setBalance(src.getBalance() - amount);
        dst.setBalance(dst.getBalance() + amount);
        String txId = "TX-" + UUID.randomUUID().toString().substring(0, 8);
        journals.save(new JournalEntry(txId, fromId, -amount));
        journals.save(new JournalEntry(txId, toId, +amount));
        idems.save(new IdempotencyRecord(idemKey, txId, amount));
        return txId;
    }
}
