import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
public class BeTac {
    static boolean lam(Lock dau, Lock sau) {
        dau.lock();                                   // khoá hàng thứ nhất
        try {
            Thread.sleep(200);                        // để luồng kia kịp khoá hàng của nó
            boolean duoc = sau.tryLock(500, TimeUnit.MILLISECONDS);   // xin hàng sau, tối đa 0,5 giây
            if (duoc) sau.unlock();
            return duoc;
        } catch (InterruptedException e) {
            return false;
        } finally { dau.unlock(); }
    }
    static String thu(Lock x1, Lock y1, Lock x2, Lock y2) throws Exception {
        boolean[] ok = new boolean[2];
        Thread t1 = new Thread(() -> ok[0] = lam(x1, y1));
        Thread t2 = new Thread(() -> ok[1] = lam(x2, y2));
        t1.start(); t2.start(); t1.join(); t2.join();
        return ok[0] && ok[1] ? "xong" : "be tac";
    }
    public static void main(String[] args) throws Exception {
        Lock a = new ReentrantLock(), b = new ReentrantLock();
        System.out.println("A roi B  va  B roi A: " + thu(a, b, b, a));
        System.out.println("A roi B  va  A roi B: " + thu(a, b, a, b));
    }
}
