# Lab LLM L05 — Chi phí bộ nhớ đệm khoá-giá trị (KV cache)

Đọc `stdin` `layers=<int> hidden=<int> ctx=<int> bytes=<int>`. Tính tổng byte và GiB của KV cache `2 * layers * hidden * ctx * bytes`.

In 1 dòng: `kv_bytes=<d> kv_GiB=<.1f>`.
Chấm tự động: `bash labs/cham.sh LLM L05 duong_dan/bai_cua_ban.py`
