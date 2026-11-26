package vn.nganhang.chuyenkhoan;

import java.util.List;

public record CursorPage(List<TransferItem> items, Long nextCursor, boolean hasMore) {}
