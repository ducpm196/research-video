package vn.nganhang.chuyenkhoan;

import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.utility.DockerImageName;

public abstract class RedisBaseTest {
    @ServiceConnection(name = "redis")
    static final GenericContainer<?> REDIS = new GenericContainer<>(
        DockerImageName.parse("redis:8@sha256:1f88291b4c57bdf249f02eb085a8669889b2d2954e91d4de5118a5da6b78dd53")
    ).withExposedPorts(6379);
    static { REDIS.start(); }
}
