# Lab LLM L07 — Sinh văn bản: nhiệt độ Softmax và top-p

Đọc `stdin` `logits=<z1,z2,z3> t2=<float> top_p=<float>`. Tính Softmax ở `T=1.0` và `T=t2`, rồi cộng dồn phần tử lớn nhất ở `T=1.0` tới khi `>= top_p`.

In 1 dòng: `T1=<list3> T06=<list3> top_p_sum=<.3f>`.
Chấm tự động: `bash labs/cham.sh LLM L07 duong_dan/bai_cua_ban.py`
