# Lab FND L03 — Thống kê giao dịch bằng ống

Tạo `thong_ke.sh`. **Dòng đầu chép nguyên** (tạo dữ liệu giả `gd.csv`; `<<'EOF'` nhập nhiều dòng, bài sau giải thích):

```bash
cat > gd.csv <<'EOF'
ma,loai,kenh,so_tien
1,rut,atm,500000
2,chuyen,app,1200000
3,thanh_toan,pos,85000
4,chuyen,app,300000
5,nap,quay,5000000
6,rut,atm,2000000
7,chuyen,web,450000
8,thanh_toan,pos,120000
9,chuyen,app,75000
10,rut,atm,1000000
11,nap,app,3000000
12,thanh_toan,web,260000
13,chuyen,app,640000
14,thanh_toan,pos,45000
15,rut,quay,700000
EOF
```

Rồi viết bốn lệnh, **luôn bỏ dòng tiêu đề** (`tail -n +2`), in lần lượt:
1. tổng số giao dịch;
2. số giao dịch **từng loại** (cột 2): `cut`, `sort`, `uniq -c`;
3. loại có **nhiều nhất** (kèm số lần);
4. **ba** số tiền lớn nhất (cột 4): xếp theo số, giảm dần.

Chạy `bash thong_ke.sh`; chấm: `bash labs/cham.sh FND L03 thong_ke.sh`. Khác bài giảng: dữ liệu (15 dòng, cột kênh thay cho tài khoản), câu hỏi.
