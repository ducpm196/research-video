package vn.nganhang.chuyenkhoan;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class FullStackService {
    private final AccountRepo accounts;
    private final JournalRepo journals;
    private final StringRedisTemplate redis;
    private final KafkaTemplate<String, String> kafka;
    private final List<String> events = new CopyOnWriteArrayList<>();

    public FullStackService(AccountRepo accounts, JournalRepo journals, StringRedisTemplate redis, KafkaTemplate<String, String> kafka) {
        this.accounts = accounts;
        this.journals = journals;
        this.redis = redis;
        this.kafka = kafka;
    }

    public long cachedBalance(String id) {
        String key = "bal:" + id;
        String v = redis.opsForValue().get(key);
        if (v != null) return Long.parseLong(v);
        long b = accounts.findById(id).orElseThrow().getBalance();
        redis.opsForValue().set(key, String.valueOf(b), Duration.ofSeconds(30));
        return b;
    }

    @Transactional
    public void transfer(String fromId, String toId, long amount) {
        Account a = accounts.findById(fromId).orElseThrow();
        Account b = accounts.findById(toId).orElseThrow();
        if (a.getBalance() < amount) throw new IllegalStateException("Thieu so du");
        a.setBalance(a.getBalance() - amount);
        b.setBalance(b.getBalance() + amount);
        journals.save(new JournalEntry(fromId, -amount));
        journals.save(new JournalEntry(toId, +amount));
        redis.delete("bal:" + fromId);
        redis.delete("bal:" + toId);
        // quen gui Kafka
    }

    @KafkaListener(topics = "bank.full.events", groupId = "l10-e2e")
    public void onEvent(String payload) { events.add(payload); }
    public List<String> getEvents() { return events; }
}
