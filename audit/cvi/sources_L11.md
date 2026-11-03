# Nguồn bài CVI L11 — tình huống lối tắt

Đọc 2026-11-03 (curl + pdftotext từ arXiv; bản tải ở scratchpad `cvi_work/src/`).

## [B18] S. Beery, G. Van Horn, P. Perona, “Recognition in Terra Incognita”, ECCV 2018 — https://arxiv.org/pdf/1807.04975
| Câu trích nguyên văn | Dùng ở |
|---|---|
| Hình 1: “(A) Cow: 0.99, Pasture: 0.99, Grass: 0.99, No Person: 0.98, Mammal: 0.98 (B) No Person: 0.99, Water: 0.98, Beach: 0.97, Outdoors: 0.97, Seashore: 0.97” | mở đầu: bò trên đồng cỏ / bãi biển |
| “Cows in ‘common’ contexts (e.g. Alpine pastures) are detected and classified correctly (A), while cows in uncommon contexts (beach, waves and boat) are not detected (B) or classified poorly (C). Top five labels and confidence produced by ClarifAI.com shown.” | “một dịch vụ nhận dạng ảnh thương mại” (không đọc tên) |

## [G20] R. Geirhos, J.-H. Jacobsen, C. Michaelis, R. Zemel, W. Brendel, M. Bethge, F. A. Wichmann, “Shortcut Learning in Deep Neural Networks”, Nature Machine Intelligence 2020 — https://arxiv.org/pdf/2004.07780
| Câu trích nguyên văn | Dùng ở |
|---|---|
| “a DNN may appear to classify cows perfectly well--but fails when tested on pictures where cows appear outside the typical grass landscape, revealing "grass" as an unintended (shortcut) predictor for "cow"” | ví dụ bò và cỏ |
| “a machine classifier successfully detected pneumonia from X-ray scans of a number of hospitals, but its performance was surprisingly low for scans from novel hospitals: The model had unexpectedly learned to identify particular hospital systems with near-perfect accuracy (e.g. by detecting a hospital-specific metal token on the scan, see Figure 1).” | mở đầu: ảnh X-quang, dấu kim loại |
| “If cows happen to be on grassland for most of the training data, detecting grass instead of cows becomes a successful strategy for solving a classification problem in an unintended way” | bảng bốn ô (số minh hoạ dựng theo ý này) |
| “Following this taxonomy, shortcuts are decision rules that perform well on i.i.d. test data but fail on o.o.d. tests” | định nghĩa lối tắt, hai loại tập thử |
| “Never attribute to high-level abilities that which can be adequately explained by shortcut learning.”; “Morgan developed a conservative guideline for interpreting non-human behaviour as early as 1903.” | nguyên tắc ở cảnh ngôn ngữ của nghề |
| “Assessing model performance on i.i.d. test data (as the majority of current benchmarks do) is insufficient to distinguish between intended and unintended (shortcut) solutions. Consequently, o.o.d. generalisation tests will need to become the rule rather than the exception.” | bước 4 của ví dụ; bài học sai 4 |

## Điều KHÔNG dạy / số minh hoạ
- Bảng 1000 ảnh (475/25), “bộ nhận bò thật đúng 90%”, bãi đỗ xe (97/70, 93/90) là SỐ MINH HOẠ, tính lại ở verify_parts/L11.py.
- Nhận xét về bản đồ chú ý (“gợi ý để đặt phép thử, không phải bằng chứng”) là lập luận của bài, không trích nguồn; không nêu phương pháp tạo bản đồ cụ thể.
- Không nêu tên bệnh viện, dịch vụ, cá nhân; không nêu tỉ lệ chính xác của mô hình X-quang (nguồn trong [G20] là tài liệu khác, chưa đọc).
