package vn.nganhang.chuyenkhoan;

import org.springframework.data.jpa.repository.JpaRepository;

public interface IdempotencyRepo extends JpaRepository<IdempotencyRecord, String> {}
