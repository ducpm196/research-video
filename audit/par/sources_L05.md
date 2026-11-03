# Nguồn PAR L05 — bộ nhớ đệm khi song song, chia sẻ giả (đọc nguyên văn 2026-11-03)

## [CAM] University of Cambridge, Computer Laboratory, Computer Architecture course 2005, “MESI”
https://www.cl.cam.ac.uk/teaching/2005/CompArch/parallel/mesi.html (WebFetch đọc được)
- “If it is in the Shared state, all other cached copies must be invalidated first. This is typically done by a broadcast operation.”
- E: “The cache line is present only in the current cache, but is clean; it matches main memory.”
- (mục MSI) S: “Indicates that this cache line may be stored in other caches of the machine.”; I: “Indicates that this cache line is invalid.”
→ bài dạy: ghi vào một dòng thì bản sao ở lõi khác bị huỷ trước (mục “nhất quán bộ nhớ đệm”); verify_parts/L05.py mô phỏng M/S/I.

## [CPP] cppreference, std::hardware_destructive_interference_size, std::hardware_constructive_interference_size
https://en.cppreference.com/w/cpp/thread/hardware_destructive_interference_size (WebFetch đọc được)
- “Minimum offset between two objects to avoid false sharing. Guaranteed to be at least alignof(std::max_align_t)”
- giá trị “implementation-defined”; “These constants provide a portable way to access the L1 data cache line size.”
- ví dụ của trang: chú thích “64 bytes on x86-64”, kết quả in “hardware_destructive_interference_size == 64”,
  “sizeof( OneCacheLiner ) == 64”, “sizeof( TwoCacheLiner ) == 128”.
→ bài dạy (Lỗi 3): không gõ cứng 64, dùng hằng số của thư viện chuẩn; giá trị do bản cài đặt quyết định.

## [HS05] H. Sutter, The Free Lunch Is Over (2005) — trích lại từ audit/csa/sources_L16.md (đọc nguyên văn 2026-11-02 ở khoá CSA)
- “coordination overhead between the cores to ensure cache coherency” → chỉ ghi ở `source`, không đọc trong lời.

## Kiến thức nội bộ
- Khoá Hệ thống máy tính (CSA L10, L11): dòng 64 byte, tách địa chỉ theo phép chia cho 64.
- PAR bài 3: rút gọn với tổng riêng.

## Số minh hoạ / mô hình (ghi rõ trên màn hình)
- Mô hình “kéo dòng” khi người ghi trước là lõi khác, các luồng ghi xoay vòng: là mô hình đếm, không phải số đo thời gian.
- 8 luồng × 1000 lần, 16 luồng × 1000 lần, bộ đếm 8 và 4 byte, 1 triệu bộ đếm.

## Điều KHÔNG dạy
- Không nêu số lần chậm đi đo được (không có số đo nguồn); hook chỉ nói “gần như không nhanh hơn”, và số lần kéo dòng theo mô hình.
- Không nêu cỡ dòng 128 byte của máy cụ thể nào (chỉ thấy trong kết quả tìm kiếm, chưa đọc trang gốc).
- Không mô tả chi tiết trạng thái của giao thức MESI (bài chỉ dùng ý “ghi thì huỷ bản sao khác”).
