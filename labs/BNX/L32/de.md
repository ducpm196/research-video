# Lab BNX L32 — Vòng đối chiếu nhỏ: sửa lệch, tạo thiếu, xoá thừa

Trạng thái **mong muốn** (như trong Git, số minh hoạ): `a` có 2 bản sao, `b` có 1. Trạng thái **thật** của cụm (từ điển): `a` có 5 bản sao, `c` có 1 (`c` không còn trong Git).
Số bản sao là giá trị của từng tên: `MONG_MUON = {"a": 2, "b": 1}`, `THAT = {"a": 5, "c": 1}`.

Viết `mau.py`:
1. Hàm `lech()` trả danh sách tên (sắp theo chữ cái) mà trạng thái thật khác mong muốn hoặc chỉ có ở một bên. In `lech: <các tên, cách nhau ", ">` (rỗng thì in `-`).
2. Hàm `dong_bo(prune)`: với mỗi tên trong mong muốn mà thật khác: ghi `sua <tên>` nếu đã có trong thật, `tao <tên>` nếu chưa có, rồi chỉnh trạng thái thật cho khớp. Tên chỉ có ở thật: chỉ khi `prune` là đúng thì ghi `xoa <tên>` và xoá khỏi trạng thái thật.
3. Gọi `dong_bo(False)` rồi `dong_bo(True)`. In mỗi lần `dong bo (khong prune): <việc> | lech: <các tên>` và `dong bo (prune): <việc> | lech: <các tên>`, việc cách nhau ", " (rỗng thì `-`).

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L32 mau.py`.
