package vn.nganhang.chuyenkhoan;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import org.springframework.kafka.annotation.BackOff;
import org.springframework.kafka.annotation.DltHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.RetryableTopic;
import org.springframework.stereotype.Component;

@Component
public class TransferEventConsumer {
    private final List<String> processed = new CopyOnWriteArrayList<>();
    private final List<String> dltReceived = new CopyOnWriteArrayList<>();

    @RetryableTopic(attempts = "3", backOff = @BackOff(delay = 100), dltTopicSuffix = "-dlt")
    @KafkaListener(topics = "transfer.events", groupId = "chuyenkhoan-l06")
    public void onMessage(String msg) {
        if (msg.startsWith("POISON:")) {
            throw new IllegalArgumentException("Ban tin doc to: " + msg);
        }
        processed.add(msg);
    }

    @DltHandler
    public void onDlt(String msg) {
        dltReceived.add(msg);
    }

    public List<String> getProcessed() { return processed; }
    public List<String> getDltReceived() { return dltReceived; }
}
