package vn.nganhang.chuyenkhoan;

import java.util.List;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderOutboxService {
    private final OutboxRepo outbox;
    private final KafkaTemplate<String, String> kafka;

    public OrderOutboxService(OutboxRepo outbox, KafkaTemplate<String, String> kafka) {
        this.outbox = outbox;
        this.kafka = kafka;
    }

    @Transactional
    public void createTransferOrder(String txPayload, boolean forceRollback) {
        outbox.save(new OutboxEvent(txPayload));
        if (forceRollback) {
            throw new IllegalStateException("Hoan tac don chuyen khoan");
        }
    }

    @Transactional
    public int publishPending() {
        List<OutboxEvent> pending = outbox.findByStatusOrderByIdAsc("PENDING");
        for (OutboxEvent ev : pending) {
            kafka.send("transfer.events", ev.getPayload());
            ev.markSent();
        }
        return pending.size();
    }
}
