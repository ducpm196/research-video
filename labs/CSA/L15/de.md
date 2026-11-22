# Lab CSA L15 (Mô phỏng I/O) — So sánh phần trăm CPU bận giữa Polling, Interrupt và DMA

Viết chương trình Python tính thời gian CPU tốn mỗi giây trên CPU `1 GHz` khi truyền `1 000 KB/s`: Ngắt từng khối `4 KB` tốn `1 000` chu kỳ/lần so với DMA chỉ báo ngắt 1 lần sau `1 000 KB` (cộng `500` chu kỳ thiết lập), in đúng 3 dòng:
1. `irq_cycles_per_s=250000`
2. `dma_cycles_per_s=1500`
3. `dma_saved_pct=99.4%`

Chấm tự động:
```bash
bash labs/cham.sh CSA L15 duong_dan/bai_cua_ban.py
```
