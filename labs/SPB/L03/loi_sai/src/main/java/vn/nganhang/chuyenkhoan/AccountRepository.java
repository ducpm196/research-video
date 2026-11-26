package vn.nganhang.chuyenkhoan;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
public interface AccountRepository extends JpaRepository<Account, String> {
    @Query("SELECT a FROM Account a ORDER BY a.id")
    List<Account> findAllWithEntries();
}
