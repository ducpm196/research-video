# Lab LLM L12 — Sinh có truy xuất (RAG): chỉ mục & recall@1

Đọc `stdin` `q=<3 số> docs=<name:x,y,z;...> relevant=<name>`. Tìm đoạn có cosin lớn nhất và kiểm khớp `relevant` để ra `recall@1`.

In 1 dòng: `top1=<name> cos=<.3f> recall_at_1=<.1f>`.
Chấm tự động: `bash labs/cham.sh LLM L12 duong_dan/bai_cua_ban.py`
