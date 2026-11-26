# Lab PRJ L00 (Đạt / Chưa đạt theo labs/PRJ/SPEC.md) — Sổ giao dịch đa công cụ

Viết chương trình Python đọc dữ liệu CSV từ `stdin` (`sys.stdin.read().splitlines()`), lọc dòng lỗi và đối chiếu kết quả giữa Python và SQLite (`:memory:`).

## Định dạng đầu vào (`stdin`)
- Mỗi dòng có dạng `<tai_khoan>,<loai>,<so_tien>` (ngăn cách bởi dấu phẩy, không có dòng tiêu đề).
- Hợp lệ khi:
  - Dòng có đúng 3 trường sau khi `strip()`.
  - `<tai_khoan>` khác rỗng; `<loai>` thuộc `IN` hoặc `OUT`.
  - `<so_tien>` là chuỗi chỉ gồm chữ số nguyên dương (`> 0`, không dấu âm, không chữ).
- Mọi dòng khác (dòng rỗng, thiếu/thừa cột, loại lạ, số âm hoặc `0`, chữ không phải số) được tính là 1 dòng lỗi (`bad += 1`), tuyệt đối không để văng ngoại lệ.

## Định dạng đầu ra (`stdout`, đúng 4 dòng)
1. `valid=<V> bad=<E> valid_pct=<P>%` (`P` làm tròn 1 chữ số thập phân; nếu tổng dòng `= 0` thì `valid_pct=0.0%`).
2. `py_net=<net> sql_net=<sql_net>` (số dư ròng; nếu không có dòng hợp lệ thì cả hai đều bằng `0`).
3. `in_total=<sum_in> out_total=<sum_out>`
4. `acc_nets=<a1>:<v1>,<a2>:<v2>,...` (sắp xếp tăng dần theo tên tài khoản, trong đó `<vi> = tổng IN - tổng OUT` của tài khoản `<ai>`; nếu không có dòng hợp lệ thì in `acc_nets=none`).

## Ví dụ minh hoạ nhỏ (khác `du_lieu.txt`)
Nếu `stdin` có 2 dòng `k1,IN,100` và `k1,OUT,abc`:
- Dòng 1 hợp lệ (`IN 100`), dòng 2 lỗi -> `valid=1 bad=1 valid_pct=50.0%`, `py_net=100 sql_net=100`, `in_total=100 out_total=0`, `acc_nets=k1:100`.

## Chấm tự động (kiểm cả `du_lieu.txt` và `ca_an/`)
```bash
bash labs/cham.sh PRJ L00 duong_dan/bai_cua_ban.py
```
