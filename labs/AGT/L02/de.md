# Lab AGT L02 — Lập kế hoạch và đường găng đồ thị phụ thuộc (DAG)

Đọc `stdin` chuỗi dạng `d=tim:<int>,docA:<int>,docB:<int>,tonghop:<int>,kiemtra:<int>`. Với `docA`, `docB` cùng phụ thuộc `tim` và chạy song song trước `tonghop -> kiemtra`, tính tổng thời gian tuần tự, đường găng `critical_path` và thời gian tiết kiệm `saved`.

In 1 dòng: `sequential=<d>s critical_path=<d>s saved=<d>s`.
Chấm tự động: `bash labs/cham.sh AGT L02 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
