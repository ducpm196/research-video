package vn.nganhang.chuyenkhoan;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "accounts")
public class Account {
    @Id private String id;
    private String ownerName;
    private long balance;
    @OneToMany(mappedBy = "account", fetch = FetchType.LAZY)
    private List<JournalEntry> entries = new ArrayList<>();

    protected Account() {}
    public Account(String id, String ownerName, long balance) {
        this.id = id;
        this.ownerName = ownerName;
        this.balance = balance;
    }
    public String getId() { return id; }
    public String getOwnerName() { return ownerName; }
    public long getBalance() { return balance; }
    public List<JournalEntry> getEntries() { return entries; }
}
