# Lab BNX L16 — Bể luồng có hàng đợi giới hạn và việc lá của cây chia đôi

Viết `Lab.java` (một tệp, một lớp `public class Lab`, chỉ cần `import java.util.concurrent.*;`). Số liệu là số minh hoạ.

**Phần 1 — hàng đợi giới hạn.** Dựng `ThreadPoolExecutor` có **3 luồng cố định** (số lõi = số tối đa = 3, thời gian giữ luồng thừa `0, TimeUnit.SECONDS`)
và `ArrayBlockingQueue` **5 chỗ**. Dùng một `CountDownLatch(1)` làm chốt: mỗi việc chỉ gọi `cua.await()` nên giữ nguyên luồng cho tới khi bạn thả chốt (khối `catch (InterruptedException e)` để trống).
Gửi **liền 14 việc** bằng `be.execute(...)`; việc nào bể từ chối thì `RejectedExecutionException` được ném ra: bắt lại và đếm `nhan`, `tuChoi`.
Rồi in 3 dòng: `so luong:` (số luồng của bể), `trong hang doi:` (số việc đang nằm trong hàng), `nhan <a>, tu choi <b>`.
Cuối cùng thả chốt (`cua.countDown()`) và `be.shutdown()`.

**Phần 2 — số lượt.** In `so luot cho 14 viec:` với số lượt khi 14 việc chia cho 3 luồng (chia làm tròn lên, tính bằng số nguyên).

**Phần 3 — việc lá.** Viết hàm đệ quy `la(int n)` trả về số việc lá khi chia đôi `n` phần tử tới khi mỗi mảnh không quá **5 000**
(`n <= 5000` thì là 1 lá; ngược lại là `la(n - n / 2) + la(n / 2)`). In `so viec la:` cho `n = 100000`.

In đúng 5 dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh BNX L16 Lab.java`.
