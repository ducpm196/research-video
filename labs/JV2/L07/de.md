# Lab JV2 L07 — Đọc dấu vết ngăn xếp và sửa lỗi

Chương trình `TongPhi` (số minh hoạ) tính tổng phí của năm giao dịch. Nó **đang lỗi**:

```java
public class TongPhi {
    static long phi(long soTien) {
        if (soTien <= 1000000) {
            return 1000;
        }
        if (soTien <= 10000000) {
            return 5000;
        }
        return 10000;
    }

    static long tongPhi(long[] ds) {
        long tong = 0;
        for (int i = 0; i <= ds.length; i++) {
            tong += phi(ds[i]);
        }
        return tong;
    }

    static void baoCao(long[] ds) {
        System.out.println("So giao dich: " + ds.length);
        System.out.println("Tong phi: " + tongPhi(ds));
    }

    public static void main(String[] args) {
        baoCao(new long[]{800000, 2500000, 1000000, 12000000, 9000000});
    }
}
```

Chạy bản này sẽ in `So giao dich: 5` rồi dừng với:

```
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5
	at TongPhi.tongPhi(TongPhi.java:15)
	at TongPhi.baoCao(TongPhi.java:22)
	at TongPhi.main(TongPhi.java:26)
```

Việc của bạn:
1. Đọc dấu vết **từ trên xuống**: dòng `at` đầu tiên là nơi nổ. Chỉ ra **số dòng** và **vì sao** chỉ số 5 không hợp lệ với mảng dài 5.
2. Chép chương trình vào `TongPhi.java`, sửa **một chỗ**, chạy lại.
3. Kết quả phải là hai dòng (so với tay: 1 000 + 5 000 + 1 000 + 10 000 + 5 000 = 22 000):

```
So giao dich: 5
Tong phi: 22000
```

Chạy: `javac TongPhi.java && java TongPhi`. Chấm: `bash labs/cham.sh JV2 L07 TongPhi.java`.
