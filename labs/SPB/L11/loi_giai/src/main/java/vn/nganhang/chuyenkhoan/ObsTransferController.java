package vn.nganhang.chuyenkhoan;

import io.micrometer.core.instrument.MeterRegistry;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ObsTransferController {
    private static final Logger log = LoggerFactory.getLogger(ObsTransferController.class);
    private final MeterRegistry meters;

    public ObsTransferController(MeterRegistry meters) { this.meters = meters; }

    @PostMapping("/api/v1/obs-transfers")
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, String> transfer(@RequestParam(name = "amount", defaultValue = "100") long amount) {
        String status = amount > 0 ? "ok" : "rejected";
        meters.counter("bank_transfers", "status", status).increment();
        log.info("transfer_processed status={} amount={}", status, amount);
        return Map.of("status", status, "correlationId", String.valueOf(MDC.get("correlationId")));
    }
}
