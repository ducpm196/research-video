package vn.nganhang.chuyenkhoan;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Version;

@Entity
@Table(name = "accounts")
public class Account {
    @Id private String id;
    private long balance;
    @Version private long version;

    protected Account() {}
    public Account(String id, long balance) { this.id = id; this.balance = balance; }
    public String getId() { return id; }
    public long getBalance() { return balance; }
    public void setBalance(long balance) { this.balance = balance; }
    public long getVersion() { return version; }
}
