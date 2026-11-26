package vn.nganhang.chuyenkhoan;

import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.kafka.KafkaContainer;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.DockerImageName;

public abstract class FullStackBaseTest {
    @ServiceConnection(name = "postgres")
    static final PostgreSQLContainer PG = new PostgreSQLContainer(
        DockerImageName.parse("postgres:17-alpine@sha256:d3244e8ce3f165ee3c93d9c4a4b1d0fe48b3a89e2287b717fdcbbde92d405065")
            .asCompatibleSubstituteFor("postgres"));
    @ServiceConnection(name = "redis")
    static final GenericContainer<?> REDIS = new GenericContainer<>(
        DockerImageName.parse("redis:8@sha256:1f88291b4c57bdf249f02eb085a8669889b2d2954e91d4de5118a5da6b78dd53")
    ).withExposedPorts(6379);
    @ServiceConnection(name = "kafka")
    static final KafkaContainer KAFKA = new KafkaContainer(
        DockerImageName.parse("apache/kafka:3.9.0@sha256:fbc7d7c428e3755cf36518d4976596002477e4c052d1f80b5b9eafd06d0fff2f")
            .asCompatibleSubstituteFor("apache/kafka")
    ).withEnv("KAFKA_LISTENERS", "PLAINTEXT://:9092,BROKER://:9093,CONTROLLER://:9094");

    static {
        PG.start(); REDIS.start(); KAFKA.start();
    }
}
