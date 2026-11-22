# Lab SEC L11 — Tính kỳ vọng số lần đoán khi dùng ngẫu nhiên hoá địa chỉ (ASLR) với 16 bit và 28 bit

Viết chương trình Python tính số vùng địa chỉ có thể với `16` bit (`2^16 = 65 536`), với `28` bit (`2^28 = 268 435 456`) và kỳ vọng số lần đoán trung bình `(2^16)/2 = 32 768` khi chương trình khởi động lại mỗi lần đoán sai **nhưng giữ nguyên bố trí địa chỉ**, in đúng 3 dòng:
1. `slots_16bit=65536`
2. `expected_guesses_16=32768`
3. `slots_28bit=268435456`

Chấm tự động:
```bash
bash labs/cham.sh SEC L11 duong_dan/bai_cua_ban.py
```
