package vn.nganhang.chuyenkhoan;
import jakarta.persistence.*;
@Entity @Table(name = "journal_entries")
public class JournalEntry {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    private String accountId; private long amount;
    protected JournalEntry() {}
    public JournalEntry(String accountId, long amount) { this.accountId = accountId; this.amount = amount; }
}
