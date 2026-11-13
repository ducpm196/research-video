# Lab JV2 L00: dựng dự án hai tệp trong gói shop, biên dịch ra out, chạy bằng -cp rồi bằng tệp đóng gói
mkdir -p src/shop/kho
cat > src/shop/kho/Hang.java <<'EOF'
package shop.kho;

public class Hang {
    private int soLuong;

    public Hang(int soLuong) {
        this.soLuong = soLuong;
    }

    public boolean ban(int n) {
        if (n > soLuong) {
            return false;
        }
        soLuong -= n;
        return true;
    }

    public int con() {
        return soLuong;
    }
}
EOF
cat > src/shop/Main.java <<'EOF'
package shop;

import shop.kho.Hang;

public class Main {
    public static void main(String[] args) {
        Hang h = new Hang(12);
        h.ban(5);
        System.out.println("ban 5 cai, con " + h.con());
        if (!h.ban(9)) {
            System.out.println("ban 9 cai: tu choi, con " + h.con());
        }
    }
}
EOF
javac -d out src/shop/kho/Hang.java src/shop/Main.java
java -cp out shop.Main
jar --create --file cuahang.jar --main-class shop.Main -C out .
java -jar cuahang.jar
