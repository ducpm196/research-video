# Nguồn bài CVI L07 — phân loại ảnh và học chuyển giao

Đọc 2026-11-03 (curl từ arxiv.org + pdftotext; bản tải ở scratchpad `cvi_work/src/`).

## [H15] K. He, X. Zhang, S. Ren, J. Sun, “Deep Residual Learning for Image Recognition”, arXiv:1512.03385 (v1, 10/12/2015)
https://arxiv.org/pdf/1512.03385

| Mục | Câu trích nguyên văn (bảng trích bị vỡ cột — đã đối chiếu từng ô) | Dùng ở |
|---|---|---|
| bảng 1 | “conv1 112×112 — 7×7, 64, stride 2”; “3×3 max pool, stride 2”; “conv2_x 56×56”; “conv5_x 7×7 — [3×3, 512; 3×3, 512] ×2” (cột 18-layer); “average pool, 1000-d fc, softmax”; “FLOPs 1.8×10⁹” | trường tiếp nhận 7 → 11 → 19; 224 → 112 → 56; đặc trưng 512 số; lớp 3 × 3 × 512 × 512 (tham số TỰ TÍNH: 2 359 808) |
| 3.4 | “A 224×224 crop is randomly sampled from an image or its horizontal flip, with the per-pixel mean subtracted [21].” | ảnh tự nhiên lật ngang vẫn giữ nhãn; lỗi 4 (trừ trung bình khi học) |

## [Y14] J. Yosinski, J. Clune, Y. Bengio, H. Lipson, “How transferable are features in deep neural networks?”, arXiv:1411.1792 (NIPS 2014)
https://arxiv.org/pdf/1411.1792

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| tóm tắt | “on the first layer they learn features similar to Gabor filters and color blobs. Such first-layer features appear not to be specific to a particular dataset or task, but general in that they are applicable to many datasets and tasks. Features must eventually transition from general to specific by the last layer of the network.” | hình 2: “lớp đầu chung (nét, vệt màu), lớp cuối riêng” |
| 1 | “When the target dataset is significantly smaller than the base dataset, transfer learning can be a powerful tool to enable training a large target network without overfitting” | lý do học chuyển giao |
| 1 | “the transferred feature layers can be left frozen, meaning that they do not change during training on the new task.” | thuật ngữ “đóng băng” |
| 1 | “If the target dataset is small and the number of parameters is large, fine-tuning may result in overfitting, so the features are often left frozen. On the other hand, if the target dataset is large or the number of parameters is small, so that overfitting is not a problem, then the base features can be fine-tuned” | lỗi 1; câu tự làm 3 |

## [R15] O. Russakovsky và cộng sự, “ImageNet Large Scale Visual Recognition Challenge”, arXiv:1409.0575 (IJCV 2015)
| Câu trích nguyên văn | Dùng ở |
|---|---|
| “… are 1000 object classes and approximately 1.2 million training images, 50 thousand validation images and 100 …” (mục 3.1, bộ phân loại ảnh; cột trái bản trích) | “học sẵn trên hơn một triệu ảnh” |

## Điều KHÔNG dạy (nguồn không ghi / số minh hoạ)
- Xưởng 300 ảnh, 10 loại lỗi, 100% / 60%, 2000 ảnh quả, chuẩn hoá (x − 120)/60 là SỐ MINH HOẠ. Bài báo năm 2015 trừ trung bình
  từng điểm ảnh; con số 120 và 60 không phải của bài báo.
- Tổng số tham số của mạng 18 lớp KHÔNG có trong [H15] (bảng 1 chỉ ghi FLOPs) → bài không nêu; chỉ tính tham số của một lớp.
- Chữ số bảy đoạn là mô hình đơn giản do bài tự dựng (không phải bộ dữ liệu chữ viết tay nào).

## [I15] S. Ioffe, C. Szegedy, “Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift”, arXiv:1502.03167 (2015) — đọc lại nguồn 2026-11-13 (curl + pypdf), mẫu F CVI L07 SHOULD “hệ số tự do”
| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| 3.2 | “Note that, since we normalize Wu+b, the bias b can be ignored since its effect will be canceled by the subsequent mean subtraction (the role of the bias is subsumed by β in Alg.1).” | ví dụ 1 bước 2: mạng có chuẩn hoá theo lô sau tích chập thì bỏ hệ số tự do → 3·3·512·512 = 2 359 296 (không cộng 512) |
| [H15] 3.4 (đọc lại 2026-11-13) | “We adopt batch normalization (BN) [16] right after each convolution and before activation, following [16].” (mạng có lối tắt chuẩn hoá theo lô sau mỗi tích chập) | cùng chỗ |
