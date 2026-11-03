# Nguồn PAR L06 — vector hoá (đọc nguyên văn 2026-11-03)

## [RS] Rust core library documentation, core::arch::x86 (doc.rust-lang.org) — tài liệu chính thức của Rust, mô tả kiểu Intel __m256
- https://doc.rust-lang.org/core/arch/x86/struct.__m256.html: “256-bit wide set of eight f32 types, x86-specific”; “This type is the
  same as the __m256 type defined by Intel, representing a 256-bit SIMD register which internally is consisted of eight packed f32
  instances. Usage of this type typically corresponds to the avx and up target features for x86/x86_64.”
- https://doc.rust-lang.org/core/arch/x86/fn._mm256_add_ps.html: “Adds packed single-precision (32-bit) floating-point elements in a
  and b.”; ví dụ của trang cộng 8 số (1.0 … 8.0) với 0.5 trong một lệnh.
→ bài dạy: thanh ghi 256 bit chứa 8 số thực 32 bit; một lệnh cộng cả 8 làn. Tên AVX chỉ ở `source`.
- Trang Microsoft learn.microsoft.com/en-us/cpp/cpp/m256 trả 404; trang Intel compiler guide chuyển hướng về trang 404 — không dùng.

## [GCC] GCC, “Auto-vectorization in GCC” (gcc.gnu.org/projects/tree-ssa/vectorization.html)
- ví dụ vector hoá được: “for (i=0; i<256; i++){ a[i] = b[i] + c[i]; }”
- “An epilog loop is generated to handle unknown loop bounds and loop bounds that do not divide by the vectorization factor.”
  → vòng phần dư.
- “not vectorized, possible dependence between data-refs a[i_124] and a[i_83]”; “Only singleton nodes w/o self dependencies can be
  vectorized.”; bộ vector hoá cơ bản xử lý “loops that do not contain any SCCs (i.e., no dependence cycles).”
  → điều kiện: các lượt không phụ thuộc nhau; a[i] = a[i − 1] + b[i] có vòng phụ thuộc.

## Số minh hoạ (ghi rõ trên màn hình)
- 1003 phần tử; băng thông 20 GB/s; lõi 2 tỉ phép cộng/giây (Lỗi 3); thanh ghi 512 bit, 1000 phần tử ở quiz.
- Đếm LỆNH CỘNG, bỏ qua lệnh nạp, lưu, nhảy — mô hình của bài.

## Điều KHÔNG dạy
- Không nói trình biên dịch cụ thể từ chối vector hoá phép tổng số thực nếu không có cờ đặc biệt (chưa đọc nguồn nói vậy).
- Không nêu tốc độ thật của lệnh vector trên chip cụ thể; không nêu tên dòng chip có thanh ghi 512 bit.
