# Lab LLM L14 — Quy đổi PF-ngày và tỉ lệ token trên tham số

Đọc `stdin` `params=<f> train_toks=<f> opt_toks=<f> opt_params=<f>`. Đổi `6 * params * train_toks` sang PF-ngày (`10^15 * 86400`) và tính `opt_toks / opt_params`.

In 1 dòng: `model_pf_days=<d> tokens_per_param=<d>`.
Chấm tự động: `bash labs/cham.sh LLM L14 duong_dan/bai_cua_ban.py`
