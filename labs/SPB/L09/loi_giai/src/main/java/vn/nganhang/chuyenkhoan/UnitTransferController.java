package vn.nganhang.chuyenkhoan;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UnitTransferController {
    private final UnitTransferService service;
    public UnitTransferController(UnitTransferService service) { this.service = service; }

    public record Req(@NotBlank String fromId, @NotBlank String toId, @Positive long amount) {}

    @PostMapping("/api/v1/unit-transfers")
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, String> submit(@Valid @RequestBody Req req) {
        return Map.of("receipt", service.execute(req.fromId(), req.toId(), req.amount()));
    }
}
