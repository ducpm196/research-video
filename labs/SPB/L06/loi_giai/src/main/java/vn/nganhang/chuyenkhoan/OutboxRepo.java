package vn.nganhang.chuyenkhoan;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OutboxRepo extends JpaRepository<OutboxEvent, Long> {
    List<OutboxEvent> findByStatusOrderByIdAsc(String status);
}
