# Lab LLM L14 — Hành trình mở rộng: từ kiến trúc chú ý tới huấn luyện tối ưu

Tính hai đại lượng trên một mô hình tham chiếu giả định: (1) đổi tổng phép tính `C = 6 * 90e9 * 4.5e11` sang đơn vị `PF-ngày` (biết `1 PF-ngày = 10^15 * 86 400` phép tính); (2) tính tỉ lệ số từ tố trên mỗi tham số ở cấu hình tối ưu gồm `2.0e12` từ tố và `100e9` tham số.

Định dạng đầu ra (1 dòng):
`model_pf_days=<số nguyên> tokens_per_param=<số nguyên>`
