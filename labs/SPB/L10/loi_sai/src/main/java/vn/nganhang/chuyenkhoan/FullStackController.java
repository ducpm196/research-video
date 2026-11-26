package vn.nganhang.chuyenkhoan;

import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
public class FullStackController {
    private final FullStackService svc;
    public FullStackController(FullStackService svc) { this.svc = svc; }
    public record Req(String fromId, String toId, long amount) {}

    @PostMapping("/api/v1/full-transfers")
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, String> post(@RequestBody Req req) {
        svc.transfer(req.fromId(), req.toId(), req.amount());
        return Map.of("status", "DONE");
    }
}
