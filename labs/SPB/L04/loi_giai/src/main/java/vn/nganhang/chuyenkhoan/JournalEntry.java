package vn.nganhang.chuyenkhoan;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "journal_entries")
public class JournalEntry {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    private String txId;
    private String accountId;
    private long amount;

    protected JournalEntry() {}
    public JournalEntry(String txId, String accountId, long amount) {
        this.txId = txId;
        this.accountId = accountId;
        this.amount = amount;
    }
    public long getAmount() { return amount; }
}
