package vn.nganhang.chuyenkhoan;
import org.springframework.data.jpa.repository.*;
public interface JournalRepo extends JpaRepository<JournalEntry, Long> {
 @Query("SELECT COALESCE(SUM(j.amount),0) FROM JournalEntry j") long net();
}
