# Lab RLN L10 — Học phần thưởng từ sở thích người dùng & phạt độ lệch KL

Cho hiệu điểm `r_A - r_B = 1.5`: tính xác suất `P(A > B) = 1 / (1 + exp(-1.5))` và mất mát `-ln(P)`. Đồng thời với phần thưởng thô `3.0`, tính điểm sau khi trừ phạt độ lệch Kullback–Leibler (`KL = ln(pi / pi_ref)`) với hệ số `beta = 0.2`, chính sách mới `pi = 0.9` và chính sách gốc tham chiếu `pi_ref = 0.3`.

Định dạng đầu ra (1 dòng):
`prob=<3 chữ số> loss=<3 chữ số> kl_adj_r=<3 chữ số>`
