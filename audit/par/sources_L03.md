# Nguồn PAR L03 — tranh chấp, phép toán nguyên tử, phép rút gọn (đọc nguyên văn 2026-11-02)

## [PT] PyTorch documentation, “Reproducibility” (notes/randomness), bản 2.15
https://docs.pytorch.org/docs/2.15/notes/randomness.html (bản `stable` chuyển hướng tới 2.15; WebFetch đọc được).
- “Completely reproducible results are not guaranteed across PyTorch releases, individual commits, or different platforms.”
- “Deterministic operations are often slower than nondeterministic operations”
- “The backward pass uses non-deterministic atomic operations by default.”
- “Each backend performs floating-point accumulation in a different order,” … “because floating-point addition is not associative,
  the results will differ between backends.”
- torch.use_deterministic_algorithms “lets you configure PyTorch to use deterministic algorithms instead of nondeterministic ones where
  available”
→ bài dạy (Lỗi 3, Lỗi 4): phép cộng số thực không kết hợp nên kết quả khác theo cách tính; phép nguyên tử bị ghi là không tất định;
  phép tất định thường chậm hơn. Lời đọc nói “một thư viện học sâu lớn”, tên PyTorch chỉ trên màn hình.

## [NI08] J. Nickolls, I. Buck, M. Garland, K. Skadron, Scalable Parallel Programming with CUDA, ACM Queue 6(2), 2008
queue.acm.org trả 403; đọc bản chép tại https://grothoff.org/christian/teaching/2008/4704/scalable_cuda.pdf (pdftotext).
- “The latest Tesla-architecture GPUs also provide atomic read-modify-write memory instructions, facilitating parallel reductions and
  parallel-data structure management.”
→ chỉ dùng làm nguồn đối chiếu cho định nghĩa “đọc–sửa–ghi nguyên tử”; không đọc trong lời.

## Kiến thức nội bộ (bài đã dựng của dự án, nói lại nội dung trong prereq)
- Khoá Hệ điều hành (OSY L04): x++ = đọc, cộng, ghi; 20 cách xen kẽ (18 ra 1, 2 ra 2); 924 cách khi mỗi luồng tăng 2 lần, kết quả 2, 3, 4.
- Khoá Hệ thống máy tính (CSA L04): số thực làm tròn sau mỗi phép, phép cộng không kết hợp.

## Số minh hoạ (ghi rõ trên màn hình)
- 8 luồng × 1000 lần tăng; 16 luồng × 10 000 sự kiện; 8 khoản 0,1 đồng.
- Mô hình mỗi lần tăng 1 bước; phép nguyên tử trên cùng một biến nối tiếp nhau (mô hình của bài, không phải số đo phần cứng).

## Điều KHÔNG dạy
- Không nêu số chu kỳ hay tốc độ của phép nguyên tử trên phần cứng cụ thể (chưa đọc nguồn đo).
- Không nói phép nguyên tử luôn chậm hơn khoá, hay ngược lại.
- Không dùng tên hàm cụ thể của thư viện trong lời đọc.
