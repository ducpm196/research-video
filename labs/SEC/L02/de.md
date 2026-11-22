# Lab SEC L02 — Tính entropy log2(N^L) của mật khẩu ký tự vs cụm từ Diceware

Viết chương trình Python tính entropy của `8` chữ thường ngẫu nhiên (`26^8`) so với `4` từ ngẫu nhiên chọn từ từ điển `7 776` từ (cụm từ Diceware, `7776^4`), và kiểm tra 4 từ có mạnh hơn 8 chữ thường không (`1` = có, `0` = không), in đúng 3 dòng:
1. `bits_8_lower=37.6`
2. `bits_4_words=51.7`
3. `words_stronger=1`

Chấm tự động:
```bash
bash labs/cham.sh SEC L02 duong_dan/bai_cua_ban.py
```
