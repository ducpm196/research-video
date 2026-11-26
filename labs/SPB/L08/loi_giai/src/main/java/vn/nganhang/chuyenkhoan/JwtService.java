package vn.nganhang.chuyenkhoan;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.Base64;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import org.springframework.stereotype.Service;

@Service
public class JwtService {
    private static final byte[] SECRET = "spb-l08-secret-key-256-bits-demo!!".getBytes(StandardCharsets.UTF_8);

    public record Claims(String sub, String role, long exp) {}

    public String sign(String sub, String role, long expEpochSec) {
        String h = b64("{\"alg\":\"HS256\",\"typ\":\"JWT\"}");
        String p = b64(String.format("{\"sub\":\"%s\",\"role\":\"%s\",\"exp\":%d}", sub, role, expEpochSec));
        String s = hmac(h + "." + p);
        return h + "." + p + "." + s;
    }

    public Claims verify(String token) {
        String[] parts = token.split("\\.");
        if (parts.length != 3) throw new IllegalArgumentException("Bad JWT");
        String expectedSig = hmac(parts[0] + "." + parts[1]);
        if (!MessageDigest.isEqual(expectedSig.getBytes(StandardCharsets.UTF_8), parts[2].getBytes(StandardCharsets.UTF_8))) {
            throw new IllegalArgumentException("Bad signature");
        }
        String json = new String(Base64.getUrlDecoder().decode(parts[1]), StandardCharsets.UTF_8);
        String sub = extractStr(json, "sub");
        String role = extractStr(json, "role");
        long exp = Long.parseLong(extractNum(json, "exp"));
        if (Instant.now().getEpochSecond() > exp) {
            throw new IllegalArgumentException("Expired");
        }
        return new Claims(sub, role, exp);
    }

    private static String b64(String s) {
        return Base64.getUrlEncoder().withoutPadding().encodeToString(s.getBytes(StandardCharsets.UTF_8));
    }

    private static String hmac(String data) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            mac.init(new SecretKeySpec(SECRET, "HmacSHA256"));
            return Base64.getUrlEncoder().withoutPadding().encodeToString(mac.doFinal(data.getBytes(StandardCharsets.UTF_8)));
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    private static String extractStr(String json, String key) {
        var m = java.util.regex.Pattern.compile("\"" + key + "\":\"([^\"]*)\"").matcher(json);
        if (!m.find()) throw new IllegalArgumentException("Missing " + key);
        return m.group(1);
    }

    private static String extractNum(String json, String key) {
        var m = java.util.regex.Pattern.compile("\"" + key + "\":(\\d+)").matcher(json);
        if (!m.find()) throw new IllegalArgumentException("Missing " + key);
        return m.group(1);
    }
}
