# Lab CS115 L36 — AdaBoost alpha và Gradient Boosting (GBDT)

Đọc `stdin` `eps=<f> y=<f> f0=<f> lr=<f> steps=<int>`. Tính `alpha = 0.5 * ln((1 - eps) / eps)` và chạy `steps` bước GBDT `f += lr * (y - f)`.

In 2 dòng chuẩn: `adaboost_alpha=<.4f>`, `gbdt_f2=<.2f> rem=<.2f>`.
Chấm tự động: `bash labs/cham.sh CS115 L36 duong_dan/bai_cua_ban.py`
