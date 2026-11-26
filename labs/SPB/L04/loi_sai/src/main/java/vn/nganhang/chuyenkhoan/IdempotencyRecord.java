package vn.nganhang.chuyenkhoan;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "idempotency_keys")
public class IdempotencyRecord {
    @Id private String idemKey;
    private String txId;
    private long amount;

    protected IdempotencyRecord() {}
    public IdempotencyRecord(String idemKey, String txId, long amount) {
        this.idemKey = idemKey;
        this.txId = txId;
        this.amount = amount;
    }
    public String getTxId() { return txId; }
}
