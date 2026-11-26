package vn.nganhang.chuyenkhoan;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TransferService {
    private final AccountRepo accounts;
    private final AuditLogService audit;

    public TransferService(AccountRepo accounts, AuditLogService audit) {
        this.accounts = accounts;
        this.audit = audit;
    }

    @Transactional
    public void transfer(String fromId, String toId, long amount) throws InsufficientFundsException {
        if (fromId.equals(toId) || amount <= 0) {
            throw new IllegalArgumentException("Tham so khong hop le");
        }
        Account src = accounts.findById(fromId).orElseThrow();
        Account dst = accounts.findById(toId).orElseThrow();
        src.setBalance(src.getBalance() - amount);
        audit.record("TRY " + fromId + "->" + toId + ":" + amount);
        if (src.getBalance() < 0) {
            throw new InsufficientFundsException("Khong du so du");
        }
        dst.setBalance(dst.getBalance() + amount);
    }
}
