# Lab AIP L02 — Máy đo Drift PSI & Cổng Tự động Tái huấn luyện

Đọc từ `stdin` 3 dòng:
- Dòng 1: `base=<p1,p2,...>` (tỉ lệ từng giỏ ở tập gốc)
- Dòng 2: `prod=<q1,q2,...>` (tỉ lệ từng giỏ ở tập vận hành)
- Dòng 3: `old_f1=<float> new_f1=<float> margin=<float>`

Yêu cầu:
1. Chuẩn hoá nếu tổng chưa đúng 1 (chia cho tổng), sau đó kẹp từng phần tử tối thiểu `1e-6`, tính `PSI = sum((q - p) * ln(q / p))`.
2. Phân mức trôi: `SEVERE` nếu `PSI >= 0.20`, `WARN` nếu `0.10 <= PSI < 0.20`, ngược lại `STABLE`.
3. Xác định `retrain_decision`: nếu không `SEVERE` ghi `NO_RETRAIN`; nếu `SEVERE` và `new_f1 >= old_f1 + margin` ghi `PROMOTE_NEW`, ngược lại `KEEP_OLD_ALERT`.

In đúng 3 dòng: `psi=<.4f>`, `drift_level=<STABLE|WARN|SEVERE>`, `retrain_decision=<NO_RETRAIN|PROMOTE_NEW|KEEP_OLD_ALERT>`.

Chấm tự động: `bash labs/cham.sh AIP L02 duong_dan/bai_cua_ban.py`
