# Lab CSA L12 — Mô phỏng Cache 2-way LRU vs ánh xạ trực tiếp

Đọc `stdin` `shift=<int> seq=<hex,...>`. Chạy cả 1-slot direct mapped và 2-way LRU trên chuỗi `seq`, in hit/miss hai phương pháp và trạng thái thứ tự thẻ cuối cùng trong LRU.

In đúng 3 dòng: `direct_mapped_hits=<d> misses=<d>`, `two_way_lru_hits=<d> misses=<d>`, `final_set0_order=<hex,...>`.
Chấm tự động: `bash labs/cham.sh CSA L12 duong_dan/bai_cua_ban.py`
