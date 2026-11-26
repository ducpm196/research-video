package vn.nganhang.chuyenkhoan;

import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.DockerImageName;

public abstract class PostgresBaseTest {
    @ServiceConnection(name = "postgres")
    static final PostgreSQLContainer PG = new PostgreSQLContainer(
        DockerImageName.parse("postgres:17-alpine@sha256:d3244e8ce3f165ee3c93d9c4a4b1d0fe48b3a89e2287b717fdcbbde92d405065")
            .asCompatibleSubstituteFor("postgres")
    );
    static { PG.start(); }
}
