package vn.nganhang.chuyenkhoan;

import java.time.Duration;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class BalanceCacheService {
    private final AccountRepo accounts;
    private final StringRedisTemplate redis;
    private final AtomicInteger dbReads = new AtomicInteger();

    public BalanceCacheService(AccountRepo accounts, StringRedisTemplate redis) {
        this.accounts = accounts;
        this.redis = redis;
    }

    public int getDbReads() { return dbReads.get(); }
    public void resetDbReads() { dbReads.set(0); }

    public long getBalance(String accId) {
        String key = "bal:" + accId;
        String cached = redis.opsForValue().get(key);
        if (cached != null) {
            return Long.parseLong(cached);
        }
        String lockKey = "lock:bal:" + accId;
        String token = UUID.randomUUID().toString();
        Boolean acquired = redis.opsForValue().setIfAbsent(lockKey, token, Duration.ofSeconds(5));
        if (Boolean.TRUE.equals(acquired)) {
            try {
                String doubleCheck = redis.opsForValue().get(key);
                if (doubleCheck != null) return Long.parseLong(doubleCheck);
                long bal = loadFromDb(accId);
                long ttl = 30L + ThreadLocalRandom.current().nextInt(6);
                redis.opsForValue().set(key, String.valueOf(bal), Duration.ofSeconds(ttl));
                return bal;
            } finally {
                if (token.equals(redis.opsForValue().get(lockKey))) {
                    redis.delete(lockKey);
                }
            }
        }
        for (int i = 0; i < 40; i++) {
            try { Thread.sleep(25); } catch (InterruptedException ignored) { Thread.currentThread().interrupt(); }
            String retry = redis.opsForValue().get(key);
            if (retry != null) return Long.parseLong(retry);
        }
        return loadFromDb(accId);
    }

    @Transactional
    public void deposit(String accId, long delta) {
        Account a = accounts.findById(accId).orElseThrow();
        a.setBalance(a.getBalance() + delta);
        accounts.saveAndFlush(a);
        // quen xoa dem
    }

    private long loadFromDb(String accId) {
        dbReads.incrementAndGet();
        return accounts.findById(accId).orElseThrow().getBalance();
    }
}
