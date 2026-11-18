import com.sun.net.httpserver.*;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.*;
public class MayChu {
    static long a = 2_000_000, b = 2_000_000;                 // hai số dư thử
    static Map<String, String> daXuLy = new HashMap<>();      // khoá lũy đẳng -> phản hồi đã trả
    static void tra(HttpExchange ex, String s) throws IOException {
        ex.sendResponseHeaders(200, s.length());
        ex.getResponseBody().write(s.getBytes());
        ex.close();
    }
    public static void main(String[] args) throws Exception {
        HttpServer sv = HttpServer.create(new InetSocketAddress(8099), 0);
        sv.createContext("/chuyen", ex -> tra(ex, "so du " + (a -= 500_000)));
        sv.createContext("/chuyen-co-khoa", ex -> tra(ex, daXuLy.computeIfAbsent(
            ex.getRequestHeaders().getFirst("Idempotency-Key"), k -> "so du " + (b -= 500_000))));
        sv.start();
    }
}
