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
sed -i 's/int b = 250$/int b = 250;/' Tong.java
sed -i 's/soluong/so_luong/' tinh.py
sed -i 's/^ech /echo /' chao.sh
javac Tong.java && java Tong
python tinh.py
bash chao.sh
