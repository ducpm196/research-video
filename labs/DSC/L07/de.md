# Lab DSC L07 — Nghịch lý Simpson: thắng từng nhóm nhưng thua khi gộp

Đọc `stdin` `asm=<k,n> bsm=<k,n> alg=<k,n> blg=<k,n>`. Kiểm xem A có thắng B ở cả hai nhóm nhỏ/nặng riêng lẻ không, rồi tính tỉ lệ thành công gộp của A và B.

In 1 dòng: `sub_A_wins=<0|1> pooled_A=<.3f> pooled_B=<.3f>`.
Chấm tự động: `bash labs/cham.sh DSC L07 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
