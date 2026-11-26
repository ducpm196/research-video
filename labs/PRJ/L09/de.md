# Dự án PRJ L09 — Bộ kiểm DFA 'ab' & tính trần song song Amdahl

Đọc từ luồng chuẩn (`stdin`) 2 dòng:
- Dòng 1: `s1=<chuỗi_1> s2=<chuỗi_2>`
- Dòng 2: `p=<tỉ_lệ_song_song_0_1> cores=<số_nhân>`

Yêu cầu chương trình Python:
1. Cài hàm `dfa(s)` mô phỏng ôtômat hữu hạn đơn định 3 trạng thái nhận đúng chuỗi chỉ gồm `'a', 'b'` và kết thúc bằng `'ab'` (trả về `1` nếu hợp lệ, `0` nếu không hợp lệ).
2. Đánh giá `dfa(s1)` và `dfa(s2)`.
3. Tính hệ số tăng tốc theo định luật Amdahl tại `cores` nhân: `S(N) = 1 / ((1 - p) + p / cores)` và giới hạn khi vô hạn nhân `S_inf = 1 / (1 - p)`.

In đúng 3 dòng (hệ số Amdahl làm tròn 2 chữ số thập phân):
```
dfa_aaab=<0_hoặc_1> dfa_aba=<0_hoặc_1>
amdahl_8cores=<.2f>
amdahl_inf=<.2f>
```

Chấm tự động:
```bash
bash labs/cham.sh PRJ L09 duong_dan/bai_cua_ban.py
```
