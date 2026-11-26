package vn.nganhang.chuyenkhoan;

import org.springframework.stereotype.Service;

@Service
public class UnitTransferService {
    private final AccountGateway accounts;
    private final AlertPort alerts;

    public UnitTransferService(AccountGateway accounts, AlertPort alerts) {
        this.accounts = accounts;
        this.alerts = alerts;
    }

    public String execute(String fromId, String toId, long amount) {
        if (amount <= 0 || fromId.equals(toId)) {
            throw new IllegalArgumentException("Tham so khong hop le");
        }
        long bal = accounts.balanceOf(fromId);
        if (bal < amount) {
            throw new IllegalStateException("Thieu so du");
        }
        accounts.debit(fromId, amount);
        accounts.credit(toId, amount);
        alerts.sent(fromId, toId, amount);
        return "OK:" + fromId + "->" + toId + ":" + amount;
    }
}
