# Lab SAR L01 — Ma trận đánh đổi cho bản ghi quyết định kiến trúc (ADR)

Đọc `stdin` `w=<w1,w2,w3> rdbms=<a,b,c> kv=<a,b,c>`. Tính điểm có trọng số cho `RDBMS` và `ShardedKV` rồi chọn phương án điểm cao hơn.

In 3 dòng: `rdbms_score=<.2f>`, `sharded_kv_score=<.2f>`, `chosen=<RDBMS|ShardedKV>`.
Chấm tự động: `bash labs/cham.sh SAR L01 duong_dan/bai_cua_ban.py`
