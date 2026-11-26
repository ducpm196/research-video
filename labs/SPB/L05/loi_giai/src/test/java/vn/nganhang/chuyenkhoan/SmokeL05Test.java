package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.StringRedisTemplate;

@SpringBootTest
class SmokeL05Test extends RedisBaseTest {
    @Autowired StringRedisTemplate redis;
    @Test void pingRedis() {
        redis.opsForValue().set("smoke:k", "42");
        assertEquals("42", redis.opsForValue().get("smoke:k"));
    }
}
