# Lab FND L01 — Đi theo cây thư mục

Tạo `di.sh` (soạn bằng trình soạn mã, lưu ở thư mục gốc của bộ khoá, mở Git Bash tại đó như bài 0). Bắt đầu bằng đoạn dựng cây này, chép nguyên: `mkdir -p` tạo thư mục (cả thư mục cha còn thiếu), `touch` tạo tệp trống, `cd` đi vào `b`; các lệnh đó học kỹ ở bài sau:

```bash
mkdir -p vp/kho/a vp/kho/b vp/ho_so
touch vp/kho/a/x.txt vp/kho/b/y.txt vp/kho/b/z.txt vp/ho_so/hd.txt
cd vp/kho/b
```

Rồi viết các lệnh, **chỉ dùng `cd` với đường dẫn tương đối** (không gõ `/` ở đầu) và `ls`:
1. đang đứng ở `b`: in nội dung `b`;
2. tới `ho_so`, in nội dung;
3. từ `ho_so` tới `a`, in nội dung;
4. in nội dung thư mục **cha** của `a` (một lệnh `ls`, không `cd`).

Chạy `bash di.sh`; chấm: `bash labs/cham.sh FND L01 di.sh`. Khác bài giảng: số tệp, tên thư mục. Chạy ngay trên cửa sổ lệnh, `ls` xếp tên thành cột (`y.txt  z.txt`); viết `ls -1` (số một) nếu muốn mỗi tên một dòng như `mong_doi.txt`. Máy chấm coi cả hai cách là ĐÚNG.
