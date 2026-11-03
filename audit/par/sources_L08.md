# Nguồn PAR L08 — luồng, khối, nhóm 32 luồng, phân kỳ, truy cập gộp

Đọc nguyên văn 2026-11-02.

## [BPG] NVIDIA, CUDA C++ Best Practices Guide (bản hiện hành tại docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
Tải bằng curl, bỏ thẻ HTML (scratchpad par_work/srcB/bpg.txt). Trang CUDA C++ Programming Guide (docs.nvidia.com/cuda/cuda-c-programming-guide)
qua WebFetch chỉ trả mục lục (bản đã tái cấu trúc) → dùng Best Practices Guide, cùng hãng, cùng trang chính thức.

Câu trích:
- “Global memory loads and stores by threads of a warp are coalesced by the device into as few as possible transactions.”
- “the concurrent accesses of the threads of a warp will coalesce into a number of transactions equal to the number of 32-byte transactions necessary to service all of the threads of the warp.” (compute capability 6.0 trở lên)
- “The k -th thread accesses the k -th word in a 32-byte aligned array … (e.g., adjacent float values), four coalesced 32-byte transactions will service that memory access.” → liền nhau: 4 giao dịch.
- “If sequential threads in a warp access memory that is sequential but not aligned with a 32-byte segment, five 32-byte segments will be requested” → lệch đầu đoạn: 5.
- “A stride of 2 results in a 50% of load/store efficiency since half the elements in the transaction are not used and represent wasted bandwidth.”
- “As the stride increases, the effective bandwidth decreases until the point where 32 32-byte segments are loaded for the 32 threads in a warp” → bước lớn: 32 đoạn.
- “In a typical system, thousands of threads are queued up for work (in warps of 32 threads each).”
- “Flow control instructions (if, switch, do, for, while) can significantly affect the instruction throughput by causing threads of the same warp to diverge; that is, to follow different execution paths. If this happens, the different execution paths must be executed separately”
- “the controlling condition should be written so as to minimize the number of divergent warps … A trivial example is when the controlling condition depends only on (threadIdx / WSIZE) where WSIZE is the warp size. In this case, no warp diverges” → câu 3 của quiz.

## [NI08] J. Nickolls, I. Buck, M. Garland, K. Skadron, “Scalable Parallel Programming with CUDA”, ACM Queue 6(2), 3–4/2008
queue.acm.org trả 403 → đọc bản chép của khoá học tại https://grothoff.org/christian/teaching/2008/4704/scalable_cuda.pdf (scratchpad par_work/src/nickolls08.txt).
- “executes threads in groups of 32 parallel threads called warps. (This term originates from weaving, the first parallel thread technology.)”
- “A warp executes one common instruction at a time, so full efficiency is realized when all 32 threads of a warp agree on their execution path. If threads of a warp diverge via a data-dependent conditional branch, the warp serially executes each branch path taken, disabling threads that are not on that path”
- “CUDA requires that thread blocks execute independently. It must be possible to execute blocks in any order, in parallel or in series.”
- “the number of blocks can be dictated by the size of the data being processed rather than by the number of processors in the system.”
- “It coalesces individual accesses of parallel threads in the same warp into fewer memory-block accesses when the addresses fall in the same block and meet alignment criteria.”

## Điều KHÔNG dạy / đã sửa
- Giáo án cũ ghi “32 luồng đọc 32 số 4 byte liền nhau = 128 byte, một giao dịch”: đúng với mô hình đoạn 128 byte của thế hệ cũ, nhưng
  hướng dẫn hiện hành tính bằng giao dịch 32 byte → 4 giao dịch. Bài dạy 4 (và 32 khi bước 32, không đổi). Đã sửa giáo án + VER PAR:L08.
- Không nêu số lõi, số cụm xử lý của thẻ cụ thể nào (thuộc bài 13); không nói “nhanh gấp 100 lần”.
- Thời gian 1 / 2 / 8 ms của ba phiên bản là số minh hoạ; tỉ lệ 2 và 8 suy từ số lượt và số giao dịch, đúng khi nhân bị chặn bởi đúng yếu tố đó.
- Xác suất 2/2³² giả định dấu của các số độc lập, mỗi dấu 1/2 (ghi trên màn hình “nửa dương, nửa âm”).
