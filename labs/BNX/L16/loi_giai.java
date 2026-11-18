import java.util.concurrent.*;

public class Lab {
    static int la(int n) {
        return n <= 5000 ? 1 : la(n - n / 2) + la(n / 2);
    }

    public static void main(String[] args) {
        CountDownLatch cua = new CountDownLatch(1);
        ThreadPoolExecutor be = new ThreadPoolExecutor(3, 3, 0,
                TimeUnit.SECONDS, new ArrayBlockingQueue<>(5));
        int nhan = 0, tuChoi = 0;
        for (int i = 1; i <= 14; i++) {
            try {
                be.execute(() -> {
                    try { cua.await(); } catch (InterruptedException e) { }
                });
                nhan++;
            } catch (RejectedExecutionException e) {
                tuChoi++;
            }
        }
        System.out.println("so luong: " + be.getPoolSize());
        System.out.println("trong hang doi: " + be.getQueue().size());
        System.out.println("nhan " + nhan + ", tu choi " + tuChoi);
        System.out.println("so luot cho 14 viec: " + (14 + 3 - 1) / 3);
        System.out.println("so viec la: " + la(100000));
        cua.countDown();
        be.shutdown();
    }
}
