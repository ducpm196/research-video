# Nguồn bài CVI L08 — phát hiện đối tượng

Đọc 2026-11-03 (curl + pdftotext từ arXiv; kho mã cocoapi chính thức trên GitHub; bản tải ở scratchpad `cvi_work/src/`).

## [R15] O. Russakovsky và cộng sự, “ImageNet Large Scale Visual Recognition Challenge”, IJCV 2015 — https://arxiv.org/pdf/1409.0575
| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Here d(bij, Bik) is the error of localization, defined as 0 if the area of intersection of boxes bij and Bik divided by the areas of their union is greater than 0.5, and 1 otherwise. (Everingham et al., 2010)” | định nghĩa giao trên hợp, ngưỡng 0,5 |
| “The criteria for object detection was adopted from PASCAL VOC (Everingham et al., 2010). It is designed to penalize the algorithm for missing object instances, for duplicate detections of one instance, and for false positive detections.” | ghép, lỗi 1 (phạt hộp trùng) |
| “These detections are greedily matched to the ground truth boxes {Bik} using Algorithm 2.” … “Order {(bj, sj)} in descending order of sj … Let C = {Bk ∈ U : IOU(Bk, bj) ≥ thr(Bk)} … Let k = arg max … IOU(Bk, bj); Set U = U \ Bk” | thuật toán ghép (alg.cvi_match_dets) |
| “The final metric for evaluating an algorithm on a given object class is average precision over the different levels of recall achieved by varying the threshold t.” | AP của một lớp |
| “if the ground truth box B is of dimensions w × h then thr(B) = min(0.5, wh / ((w + 10)(h + 10)))” … “this changes the threshold only on objects which are smaller than approximately 25 × 25 pixels” | lỗi 3 (vật nhỏ, 4 × 4 → 0,082) |

## [Y16] J. Redmon, S. Divvala, R. Girshick, A. Farhadi, “You Only Look Once: Unified, Real-Time Object Detection” — https://arxiv.org/pdf/1506.02640
| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Non-maximal suppression can be used to fix these multiple detections. While not critical to performance as it is for R-CNN or DPM, non-maximal suppression adds 2-3% in mAP.” | ghi chú ở cảnh loại bỏ không cực đại |
| “Our base YOLO model processes images in real-time at 45 frames per second.”; Bảng 1: “YOLO 2007+2012 63.4 45” (PASCAL VOC 2007) | (chỉ trong `source`, không dạy thêm) |

## [COCO] kho cocoapi chính thức — https://raw.githubusercontent.com/cocodataset/cocoapi/master/PythonAPI/pycocotools/cocoeval.py và coco.py
| Câu trích nguyên văn | Dùng ở |
|---|---|
| “iouThrs - [.5:.05:.95] T=10 IoU thresholds for evaluation” | trung bình 10 ngưỡng (0,392) |
| “recThrs - [0:.01:1] R=101 recall thresholds for evaluation” | tự kiểm 2 (101 mức độ phủ, alg.cvi_ap101) |
| “if pr[i] > pr[i-1]: pr[i-1] = pr[i]” | đường bao lấy max bên phải |
| `stats[1] = _summarize(1, iouThr=.5, …)`, `stats[2] = _summarize(1, iouThr=.75, …)` | bộ chấm báo riêng ngưỡng 0,5 và 0,75 |
| coco.py: “bb = ann['bbox']; x1, x2, y1, y2 = [bb[0], bb[0]+bb[2], bb[1], bb[1]+bb[3]]” | lỗi 4: hộp ghi [x, y, rộng, cao] |

## NOT_VERIFIED / điều KHÔNG dạy
- M. Everingham và cộng sự, “The PASCAL Visual Object Classes (VOC) Challenge”, IJCV 2010: máy chủ www.robots.ox.ac.uk / host.robots.ox.ac.uk
  từ chối kết nối (curl lỗi 28, WebFetch ECONNREFUSED, 2026-11-03); bản Springer cần đăng nhập. Tiêu chí 0,5 chỉ dạy theo câu dẫn của [R15].
  KHÔNG dạy cách tính “AP 11 điểm” của VOC 2007 (không có câu nguồn đọc được).
- Ba người, các hộp, điểm tin cậy, lớp “xe” AP 0,60, camera cổng / robot gắp là SỐ MINH HOẠ.
