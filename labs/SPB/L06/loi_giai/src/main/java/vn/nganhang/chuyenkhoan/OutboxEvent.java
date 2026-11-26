package vn.nganhang.chuyenkhoan;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;

@Entity
public class OutboxEvent {
    @Id @GeneratedValue private Long id;
    private String payload;
    private String status;
    protected OutboxEvent() {}
    public OutboxEvent(String payload) { this.payload = payload; this.status = "PENDING"; }
    public Long getId() { return id; }
    public String getPayload() { return payload; }
    public String getStatus() { return status; }
    public void markSent() { this.status = "SENT"; }
}
