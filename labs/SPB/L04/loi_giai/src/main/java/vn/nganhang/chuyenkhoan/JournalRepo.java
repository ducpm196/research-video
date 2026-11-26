package vn.nganhang.chuyenkhoan;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface JournalRepo extends JpaRepository<JournalEntry, Long> {
    @Query("SELECT COALESCE(SUM(j.amount), 0) FROM JournalEntry j")
    long netSum();
}
