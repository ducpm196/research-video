# Lab CSA L15 — So sánh chi phí CPU giữa Polling/Ngắt và DMA

Đọc `stdin` `kbps=<int>` (đơn vị `KB/s`: kilobyte mỗi giây) ` block_kb=<int> irq_cyc=<int> dma_setup=<int>`. Tính chu kỳ ngắt mỗi khối, chu kỳ DMA 1 lần cả khối truyền và phần trăm tiết kiệm.

In đúng 3 dòng: `irq_cycles_per_s=<int>`, `dma_cycles_per_s=<int>`, `dma_saved_pct=<.1f>%`.
Chấm tự động: `bash labs/cham.sh CSA L15 duong_dan/bai_cua_ban.py`
