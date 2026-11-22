# Lab AGT L02 — Lập kế hoạch và phân rã đồ thị phụ thuộc (DAG)

Cho đồ thị phụ thuộc gồm 5 bước: `tim` (3 s, không phụ thuộc), `docA` (5 s, sau `tim`), `docB` (2 s, sau `tim`), `tonghop` (4 s, sau cả `docA` và `docB`), `kiemtra` (1 s, sau `tonghop`). Viết mã dựng cấu trúc đồ thị phụ thuộc và tính thời gian hoàn thành từng bước để tìm thời gian chạy tuần tự, đường găng song song và thời gian tiết kiệm.

Định dạng đầu ra (1 dòng):
`sequential=<số>s critical_path=<số>s saved=<số>s`
