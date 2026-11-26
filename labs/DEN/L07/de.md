# Lab DEN L07 — Chỉ mục ngược và công thức xếp hạng BM25

Đọc `stdin` chứa các dòng `id:văn bản` và dòng cuối `query=<từ> target=<id>`. Lập chỉ mục ngược tìm các mã tài liệu chứa `query` rồi tính điểm `BM25(k1=1.2, b=0.75)` cho `target`.

In 2 dòng: `docs_with_nhanh=<list>`, `bm25_doc1=<.4f>`.
Chấm tự động: `bash labs/cham.sh DEN L07 duong_dan/bai_cua_ban.py`
