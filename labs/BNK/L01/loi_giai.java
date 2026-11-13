public class TongBaLuong {
    static long tong = 0;
    static final Object KHOA = new Object();
    public static void main(String[] args) throws Exception {
        Runnable viec = () -> {
            for (int i = 0; i < 200_000; i++) {
                synchronized (KHOA) { tong++; }
            }
        };
        Thread[] ds = { new Thread(viec), new Thread(viec), new Thread(viec) };
        for (Thread t : ds) t.start();
        for (Thread t : ds) t.join();
        System.out.println("tong = " + tong);
    }
}
