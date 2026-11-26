package vn.nganhang.chuyenkhoan;

import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.kafka.KafkaContainer;
import org.testcontainers.utility.DockerImageName;

public abstract class KafkaBaseTest {
    @ServiceConnection(name = "kafka")
    static final KafkaContainer KAFKA = new KafkaContainer(
        DockerImageName.parse("apache/kafka:3.9.0@sha256:fbc7d7c428e3755cf36518d4976596002477e4c052d1f80b5b9eafd06d0fff2f")
            .asCompatibleSubstituteFor("apache/kafka")
    ).withEnv("KAFKA_LISTENERS", "PLAINTEXT://:9092,BROKER://:9093,CONTROLLER://:9094");
    static { KAFKA.start(); }
}
