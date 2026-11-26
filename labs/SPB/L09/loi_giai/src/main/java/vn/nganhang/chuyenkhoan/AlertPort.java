package vn.nganhang.chuyenkhoan;

public interface AlertPort {
    void sent(String fromId, String toId, long amount);
}
