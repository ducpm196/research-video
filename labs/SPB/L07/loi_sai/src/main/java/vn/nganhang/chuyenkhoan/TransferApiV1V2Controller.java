package vn.nganhang.chuyenkhoan;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import java.util.List;
import java.util.Map;
import java.util.stream.LongStream;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Tag(name = "Transfers", description = "Tai nguyen giao dich chuyen khoan")
public class TransferApiV1V2Controller {
    private static final List<TransferItem> STORE = LongStream.rangeClosed(1, 50)
        .mapToObj(i -> new TransferItem(i, "TK01", "TK02", 10_000L * i)).toList();

    @GetMapping("/api/v1/transfers")
    @Operation(summary = "Phan trang con tro theo ID tang dan")
    @ApiResponse(responseCode = "200", description = "Danh sach giao dich sau con tro")
    public CursorPage listByCursor(
        @RequestParam(name = "cursor", defaultValue = "0") long cursor,
        @RequestParam(name = "limit", defaultValue = "5") int limit
    ) {
        int safeLimit = Math.max(1, Math.min(limit, 20));
        List<TransferItem> slice = STORE.stream().filter(t -> t.id() >= cursor).limit(safeLimit + 1L).toList();
        boolean hasMore = slice.size() > safeLimit;
        List<TransferItem> page = hasMore ? slice.subList(0, safeLimit) : slice;
        Long next = page.isEmpty() ? null : page.get(page.size() - 1).id();
        return new CursorPage(page, next, hasMore);
    }

    public record CreateV2(String fromAccount, String toAccount, long amount, String channel) {}

    @PostMapping("/api/v2/transfers")
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Tao giao dich v2 giu tuong thich nguoc truong channel tuy chon")
    public Map<String, Object> createV2(@RequestBody CreateV2 req) {
        String ch = (req.channel() == null || req.channel().isBlank()) ? "MOBILE" : req.channel();
        return Map.of("status", "ACCEPTED", "amount", req.amount(), "channel", ch);
    }
}
