package vn.nganhang.chuyenkhoan;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;

@Entity
public class AuditEntry {
    @Id @GeneratedValue private Long id;
    private String message;
    protected AuditEntry() {}
    public AuditEntry(String message) { this.message = message; }
    public Long getId() { return id; }
    public String getMessage() { return message; }
}
