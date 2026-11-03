# Nguồn bài CVI L10 — dịch chuyển miền

Đọc 2026-11-03 (curl + pdftotext từ arXiv; bản tải ở scratchpad `cvi_work/src/`).

## [B18] S. Beery, G. Van Horn, P. Perona, “Recognition in Terra Incognita”, ECCV 2018 — https://arxiv.org/pdf/1807.04975
| Câu trích nguyên văn | Dùng ở |
|---|---|
| “The images in our dataset are harvested from twenty camera traps deployed to monitor animal populations. Camera traps are fixed at one location, hence the background changes little across images” | cảnh nghiên cứu thật: bẫy ảnh, nền ít đổi |
| “From our pool of 20 locations, we selected 9 locations at random to use as trans-location test data, and a single random location to use as trans-location validation data. From the remaining 10 locations, we use images taken on odd days as cis-location test data.” | cách chia: 9 điểm thử, 1 điểm chỉnh, ngày lẻ để thử |
| “The remaining data is used for training, with the constraint that training and validation sets do not share the same image sequences.” | lỗi 2: không chung chuỗi ảnh |
| “On the cis-location test set we achieve a top-1 error of 20.83%, and a top-1 error of 41.08% on the trans-location test set with a 97% cis-to-trans increase in error.” | 20,83% → 41,08%, tăng 97% (tính lại ở VER) |
| “However, we find that generalization to new locations is poor, especially for classification systems.” | bài học chung |

## [R19] B. Recht, R. Roelofs, L. Schmidt, V. Shankar, “Do ImageNet Classifiers Generalize to ImageNet?”, ICML 2019 — https://arxiv.org/pdf/1902.10811
| Câu trích nguyên văn | Dùng ở |
|---|---|
| “By closely following the original dataset creation processes, we test to what extent current classification models generalize to new data.” | làm lại tập kiểm tra theo quy trình cũ |
| “The accuracy drops range from 3% to 15% on CIFAR-10 and 11% to 14% on ImageNet.” | tụt 11% tới 14% |
| “our experiments show that the relative order of models is almost exactly preserved on our new test sets” | thứ hạng gần như giữ nguyên |
| “We decided on a test set size of 2,000 for CIFAR-10 and 10,000 for ImageNet.” | 10 000 ảnh |
| “This suggests that the accuracy scores of even the best image classifiers are still highly sensitive to minutiae of the data cleaning process.” | bài học “nhạy với chi tiết nhỏ của cách thu và lọc ảnh” |

## Điều KHÔNG dạy / số minh hoạ
- Mô hình biển báo, 900/100 ảnh ngày/đêm, mưa/nắng, mùa đông 70% ban đêm, thành phố mới là SỐ MINH HOẠ.
- “Hai sai số chuẩn ≈ khoảng tin cậy 95%” là xấp xỉ chuẩn (nêu là xấp xỉ); không trích nguồn thống kê riêng.
- Không nêu con số mAP phát hiện của [B18] (bài chỉ dùng phần phân loại).
