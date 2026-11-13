import java.util.concurrent.atomic.AtomicInteger;

public class DemSaiDung {
    static int thuong = 0;
    static int dongBo = 0;
    static final Object khoa = new Object();
    static AtomicInteger nguyenTu = new AtomicInteger();

    public static void main(String[] args) throws Exception {
        Runnable viec = () -> {
            for (int i = 0; i < 250000; i++) {
                thuong++;
                synchronized (khoa) {
                    dongBo++;
                }
                nguyenTu.incrementAndGet();
            }
        };
        Thread[] ds = new Thread[4];
        for (int i = 0; i < ds.length; i++) {
            ds[i] = new Thread(viec);
            ds[i].start();
        }
        for (Thread t : ds) {
            t.join();
        }
        System.out.println("Khong dong bo: dem < 1000000 -> " + (thuong < 1000000));
        System.out.println("Dong bo: " + dongBo);
        System.out.println("Nguyen tu: " + nguyenTu.get());
    }
}
