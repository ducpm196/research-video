# Lab ESY L08 — So sánh chi phí bit truyền 8 byte giữa bus SPI và I2C ở 100 kHz

Ở xung nhịp `100 kHz`, một giao dịch gửi `8` byte dữ liệu qua SPI chỉ tốn `64` nhịp (`8 * 8`), còn qua I2C cần `1` byte địa chỉ + `8` byte dữ liệu kèm 1 bit xác nhận `ACK` cho mỗi byte (`9 * 9 = 81` nhịp). Tính thời gian truyền (đơn vị micro giây) của hai bus.
In đúng 1 dòng `spi_8B_us=... i2c_8B_us=...` (1 chữ số).

Chấm tự động:
```bash
bash labs/cham.sh ESY L08 duong_dan/bai_cua_ban.py
```
