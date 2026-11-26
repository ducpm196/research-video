package vn.nganhang.chuyenkhoan;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Account {
    @Id private String id;
    private long balance;
    protected Account() {}
    public Account(String id, long balance) { this.id = id; this.balance = balance; }
    public String getId() { return id; }
    public long getBalance() { return balance; }
    public void setBalance(long balance) { this.balance = balance; }
}
