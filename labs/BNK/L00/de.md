# Lab BNK L00 — Phí 0,3 bị cộng hai mươi lần

Một khoản phí **0,3** (đơn vị bất kỳ, số minh hoạ) bị cộng **20 lần** vào một tổng.

Viết chương trình `PhiLech` (tệp `PhiLech.java`):
1. Một biến `double` cộng `0.3` hai mươi lần; một biến `long` cộng `3` (đơn vị: một phần mười) hai mươi lần.
2. In đúng ba dòng:
   - `double: <tổng double>`
   - `so nguyen: <tổng long> phan muoi`
   - `bang 6? <kết quả so sánh tổng double == 6.0>`

Cần JDK 21: mở cửa sổ gõ lệnh (Git Bash), gõ `java -version` phải thấy số 21. Khung tệp `PhiLech.java` (viết bài vào chỗ `...`):

```java
public class PhiLech {
    public static void main(String[] args) {
        // ... khai hai biến, vòng lặp for (int i = 0; i < 20; i++), in ba dòng bằng System.out.println
    }
}
```

Chạy: `javac PhiLech.java && java PhiLech`. Chấm: `bash labs/cham.sh BNK L00 PhiLech.java`.
