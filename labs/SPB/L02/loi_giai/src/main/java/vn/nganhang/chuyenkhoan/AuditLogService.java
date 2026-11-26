package vn.nganhang.chuyenkhoan;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuditLogService {
    private final AuditEntryRepo repo;
    public AuditLogService(AuditEntryRepo repo) { this.repo = repo; }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void record(String msg) {
        repo.save(new AuditEntry(msg));
    }
}
