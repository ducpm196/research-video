package vn.nganhang.chuyenkhoan;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RuntimeProfileController {
    public static long maxHeapMiB(long containerMiB, double maxRamPct) {
        return Math.round(containerMiB * (maxRamPct / 100.0));
    }

    @GetMapping("/api/v1/runtime")
    public Map<String, Object> runtime() {
        Runtime rt = Runtime.getRuntime();
        return Map.of("java", Runtime.version().feature(), "processors", rt.availableProcessors(), "maxHeapMiB512_75pct", maxHeapMiB(512, 75.0));
    }
}
