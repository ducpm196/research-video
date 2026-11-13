# Lab JV2 L00 — Cửa hàng hai tệp, hai gói

Dựng dự án nhỏ trong một thư mục tạm, **tự gõ** hai tệp (không chép từ ví dụ):

1. `src/shop/kho/Hang.java`, gói `shop.kho`: lớp `Hang` có trường `private int soLuong`, hàm tạo nhận số lượng đầu, `public boolean ban(int n)`
   (trả `false` và không đổi gì nếu `n` lớn hơn số còn; ngược lại trừ đi và trả `true`), `public int con()`.
2. `src/shop/Main.java`, gói `shop`, có `import shop.kho.Hang;`. Tạo `Hang` 12 cái, bán 5, in `ban 5 cai, con 7`; rồi bán 9, nếu bị từ chối in `ban 9 cai: tu choi, con 7`.

Biên dịch ra thư mục `out` bằng `javac -d out …`, chạy `java -cp out shop.Main`. Đóng gói `cuahang.jar` với `--main-class shop.Main`, chạy `java -jar cuahang.jar`.

Đầu ra của **cả hai lần chạy** gộp lại thành bốn dòng. Lab này chấm bằng một tệp `.sh` gom mọi lệnh của bạn:
`bash labs/cham.sh JV2 L00 lenh.sh` (tệp `lenh.sh` tạo hai tệp Java bằng `cat > … <<'EOF'`, rồi `javac`, `java`, `jar`).
