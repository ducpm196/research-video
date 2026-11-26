package vn.nganhang.chuyenkhoan;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;

public record TransferRequest(
    @NotBlank(message = "thieu tai khoan nguon") String fromAccount,
    @NotBlank(message = "thieu tai khoan dich") String toAccount,
    @Positive(message = "so tien phai lon hon 0") long amount
) {}
