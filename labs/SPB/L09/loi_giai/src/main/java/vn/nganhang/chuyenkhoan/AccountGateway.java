package vn.nganhang.chuyenkhoan;

public interface AccountGateway {
    long balanceOf(String id);
    void debit(String id, long amount);
    void credit(String id, long amount);
}
