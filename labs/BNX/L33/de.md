# Lab BNX L33 — Bộ chứa tí hon: vòng đời Servlet bằng tay (Java thuần, không cần Tomcat)

Dán đoạn sau vào đầu tệp `MauBoChua.java` (ba kiểu này **cho sẵn**, đừng sửa):

```java
import java.util.*;
import java.util.function.Supplier;

interface MiniServlet {
    void init();
    String service(String ten);
    void destroy();
}

class ChaoVi implements MiniServlet {
    int dem = 0;
    public void init() { System.out.println("init ChaoVi"); }
    public String service(String ten) { dem++; return "Xin chao " + ten + " (so " + dem + ")"; }
    public void destroy() { System.out.println("destroy ChaoVi"); }
}

class ChaoAnh implements MiniServlet {
    int dem = 0;
    public void init() { System.out.println("init ChaoAnh"); }
    public String service(String ten) { dem++; return "Hello " + ten + " (so " + dem + ")"; }
    public void destroy() { System.out.println("destroy ChaoAnh"); }
}
```

Viết lớp `public class MauBoChua` (một **bộ chứa** tí hon):
1. Hai bảng: `khaiBao` (đường dẫn → hàm tạo, ví dụ `"/vi"` → `ChaoVi::new`) và `dangChay` (đường dẫn → thể hiện đã tạo). Dùng `LinkedHashMap` cho cả hai, vì `dung()` phải duyệt theo thứ tự thêm vào (`HashMap` không bảo đảm thứ tự).
2. `String xuLy(String duong, String ten)`: nếu đường dẫn **chưa có** thể hiện thì tạo bằng `khaiBao`, gọi `init()` **đúng một lần**, cất vào `dangChay`. Rồi trả `duong + "?ten=" + ten + " -> " + s.service(ten)`.
3. `void dung()`: gọi `destroy()` của từng thể hiện **đã tạo**, theo thứ tự tạo (duyệt `dangChay.values()` của `LinkedHashMap`).
4. `main`: khai báo `"/vi"` → `ChaoVi::new` và `"/en"` → `ChaoAnh::new`; in `xuLy("/vi","Lan")`, `xuLy("/vi","Minh")`, `xuLy("/en","Ann")`, `xuLy("/vi","Hoa")`; rồi gọi `dung()`.

Chạy: `javac MauBoChua.java && java MauBoChua`. Chấm: `bash labs/cham.sh BNX L33 MauBoChua.java`.
