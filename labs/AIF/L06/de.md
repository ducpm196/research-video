# Lab AIF L06 — Minimax và cắt tỉa Alpha-Beta

Đọc `stdin` `branches=<v1,v2,v3;...>`. Tìm giá trị tối ưu ở gốc MAX (các nhánh con là MIN) và đếm tổng số lá phải thăm khi cắt tỉa trái sang phải.

In 1 dòng: `minimax=<d> leaves_visited=<d>`.
Chấm tự động: `bash labs/cham.sh AIF L06 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
