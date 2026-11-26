package vn.nganhang.chuyenkhoan;

import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SecureTransferController {
    private static final Map<String, String> OWNERS = Map.of("TK-AN", "an", "TK-BINH", "binh");

    public record TransferCmd(String fromAccount, String toAccount, long amount) {}

    @PostMapping("/api/v1/transfers")
    public ResponseEntity<Map<String, Object>> transfer(@RequestBody TransferCmd cmd, Authentication auth) {
        String owner = OWNERS.get(cmd.fromAccount());
        if (owner == null || !owner.equals(auth.getName())) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(Map.of("error", "Khong co quyen tren tai khoan nguon"));
        }
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("status", "ACCEPTED", "amount", cmd.amount()));
    }
}
