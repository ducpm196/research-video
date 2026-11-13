# Lab FND L05 — Đọc thông báo lỗi và sửa ba tệp hỏng

Tạo `sua.sh`. **Chép nguyên** đoạn dưới để dựng ba tệp hỏng (`<<'EOF'` nhập nhiều dòng, học dần ở các bài sau):

```bash
cat > Tong.java <<'EOF'
public class Tong {
    public static void main(String[] args) {
        int a = 100;
        int b = 250
        System.out.println("tong = " + (a + b));
    }
}
EOF
cat > tinh.py <<'EOF'
gia = 40
so_luong = 3
print("thanh tien =", gia * soluong)
EOF
cat > chao.sh <<'EOF'
echo "bat dau"
ech "xin chao"
EOF
```

Rồi:
1. chạy từng tệp một lần để **đọc** thông báo lỗi: `javac Tong.java`, `python tinh.py`, `bash chao.sh` (thông báo ở luồng lỗi, không tính vào kết quả);
2. **sửa** mỗi tệp đúng chỗ (có thể dùng `sed -i 's/cũ/mới/' tệp`);
3. chạy lại: `javac Tong.java && java Tong`, `python tinh.py`, `bash chao.sh`.

Kết quả cần đúng bốn dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh FND L05 sua.sh`. Cần JDK 21 và Python theo bài đầu tiên.
