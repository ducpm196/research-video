package vn.nganhang.chuyenkhoan;

import org.springframework.data.jpa.repository.JpaRepository;

public interface AuditEntryRepo extends JpaRepository<AuditEntry, Long> {}
