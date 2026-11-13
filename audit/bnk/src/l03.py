from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    may_chu = prog("MayChu", """
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
}""", out="", lang="java", extra={"kind": "syntax", "reason": "máy chủ chạy nền, được chạy thật bởi nguồn CurlThu cùng tệp này"})
    curl_thu = prog("CurlThu", """
java MayChu.java > /dev/null 2>&1 &
SV=$!
trap 'kill $SV; wait $SV 2>/dev/null; sleep 1' EXIT
until curl -s -o /dev/null localhost:8099/; do sleep 0.3; done
curl -s -w "\\n" -X POST localhost:8099/chuyen
curl -s -w "\\n" -X POST localhost:8099/chuyen
curl -s -w "\\n" -X POST localhost:8099/chuyen
curl -s -w "\\n" -X POST localhost:8099/chuyen-co-khoa -H "Idempotency-Key: abc"
curl -s -w "\\n" -X POST localhost:8099/chuyen-co-khoa -H "Idempotency-Key: abc"
curl -s -w "\\n" -X POST localhost:8099/chuyen-co-khoa -H "Idempotency-Key: abc"
""", out="""so du 1500000
so du 1000000
so du 500000
so du 1500000
so du 1500000
so du 1500000""", lang="bash", extra={"files": {"MayChu.java": "src:BNK:L03_MayChu"}, "timeout": 90})
    xu_ly = prog("XuLyTrung", """
import java.util.*;
public class XuLyTrung {
    static long soDu = 3_000_000;
    static Map<String, Long> daXuLy = new HashMap<>();
    static long chuyen(String khoa) {
        return daXuLy.computeIfAbsent(khoa, k -> soDu -= 700_000);
    }
    public static void main(String[] args) {
        for (String k : new String[] { "k1", "k1", "k2", "k1" }) {
            System.out.println(k + " -> " + chuyen(k));
        }
    }
}""", out="""k1 -> 2300000
k1 -> 2300000
k2 -> 1600000
k1 -> 2300000""")
    sql_khoa = prog("KhoaLuyDang", """
CREATE TABLE khoa_luy_dang (khoa TEXT PRIMARY KEY, phan_hoi TEXT);
INSERT OR IGNORE INTO khoa_luy_dang VALUES ('abc', 'so du 1500000');
INSERT OR IGNORE INTO khoa_luy_dang VALUES ('abc', 'so du 1000000');
INSERT OR IGNORE INTO khoa_luy_dang VALUES ('abc', 'so du 500000');
SELECT COUNT(*) FROM khoa_luy_dang;
SELECT phan_hoi FROM khoa_luy_dang WHERE khoa = 'abc';""", out="""1
so du 1500000""", lang="sqlite")
    hook = sc("hook", "hook", "Vì sao một lần bấm chuyển tiền lại bị trừ ba lần?", [
        st("""<p>Khách bấm chuyển $500\\,000$ đồng. Mạng chập chờn nên ứng dụng không nhận được phản hồi và <b>tự thử lại</b> hai lần nữa.</p>
<div class="box key">Máy chủ nhận đủ <b>ba</b> yêu cầu. Nếu không phòng bị, tài khoản bị trừ <b>ba lần</b>.</div>""",
           """Chào bạn, khách bấm chuyển năm trăm nghìn đồng. Mạng chập chờn nên ứng dụng không nhận được phản hồi và tự thử lại thêm hai lần.
           Máy chủ nhận đủ ba yêu cầu, và nếu không phòng bị, tài khoản bị trừ ba lần."""),
        st(table(["ý hỏi", "bài này trả lời"],
                 [["vì sao thử lại là bình thường", "mạng có thể mất phản hồi, người gọi không biết việc đã xong chưa"],
                  ["làm sao thử lại mà không trừ trùng", "khoá lũy đẳng: cùng khoá thì chỉ làm một lần"]]),
           """Hôm nay ta trả lời hai câu. Vì sao thử lại là chuyện bình thường, và làm sao thử lại mà không trừ trùng.
           Đáp án là khoá lũy đẳng: cùng một khoá thì chỉ làm một lần."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① HTTP và REST API", "HTTP là giao thức web: mỗi yêu cầu gồm một phương thức (GET, POST…) và một đường dẫn; REST API là cách một dịch vụ mở chức năng qua các đường dẫn đó", "<code>POST /transfers</code>"],
                  ["② Yêu cầu và phản hồi", "người gọi gửi yêu cầu, máy chủ trả phản hồi", "yêu cầu chuyển tiền, phản hồi thành công"],
                  ["③ Mã trạng thái", "số báo kết quả: 2xx thành công, 4xx lỗi người gọi, 5xx lỗi máy chủ", "200 thành công, 404 không thấy, 503 tạm không phục vụ"],
                  ["④ Hết giờ chờ", "chờ quá lâu thì người gọi bỏ cuộc, dù máy chủ có thể đã làm xong", "chờ 3 giây không thấy gì"]]),
           """Trước hết ta cần hiểu bốn điều. HTTP là giao thức web. Mỗi yêu cầu gồm một phương thức, như lấy hay gửi, và một đường dẫn. REST API là cách một dịch vụ mở chức năng của nó qua các đường dẫn đó.
           Người gọi gửi yêu cầu, máy chủ trả phản hồi. Mã trạng thái báo kết quả. Các mã bắt đầu bằng chữ số hai là thành công, bắt đầu bằng bốn là lỗi người gọi, bắt đầu bằng năm là lỗi máy chủ.
           Còn hết giờ chờ nghĩa là người gọi bỏ cuộc, dù máy chủ có thể đã làm xong."""),
        st("""$$2\\,000\\,000 - 500\\,000 = 1\\,500\\,000$$""",
           """Một ví dụ số. Số dư hai triệu, trừ năm trăm nghìn còn một triệu năm trăm nghìn. Đó là kết quả đúng cho một lần chuyển."""),
    ], checks=["2000000 - 500000 == 1500000"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["GET", "đọc dữ liệu, không làm thay đổi gì: an toàn"],
                  ["POST", "tạo hoặc thực hiện việc mới: mỗi lần gọi có thể làm thêm một việc"],
                  ["PUT", "ghi đè tới trạng thái đã cho: gọi nhiều lần cũng cho một kết quả"],
                  ["lũy đẳng", "gọi một lần hay nhiều lần, kết quả cuối cùng như nhau"],
                  ["khoá lũy đẳng", "mã duy nhất do người gọi sinh ra cho mỗi việc, gửi kèm mọi lần thử"]]),
           """Bảng này giải mã năm từ. G E T là đọc, không thay đổi gì. P O S T là làm một việc mới, mỗi lần gọi có thể làm thêm. P U T là ghi đè tới trạng thái đã cho, gọi nhiều lần cho cùng kết quả.
           Lũy đẳng nghĩa là gọi một lần hay nhiều lần, kết quả cuối như nhau. Khoá lũy đẳng là mã duy nhất người gọi gửi kèm mọi lần thử."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: phản hồi mất, thử lại, và khoá chặn trùng", [
        st(svg(1500, 420,
               box(40, 160, 260, 100, ["Ứng dụng", "người gọi"], C_BLUE, bold=True),
               box(1200, 160, 260, 100, ["Máy chủ", "đã trừ tiền"], C_GREEN, bold=True),
               arrow(300, 190, 1195, 190, "#2a78d6", "1. chuyển 500 000"),
               arrow(1195, 235, 305, 235, "#dc2626", "2. phản hồi bị mất trên đường về", dash=True),
               arrow(300, 290, 1195, 290, "#2a78d6", "3. không thấy gì nên thử lại"),
               txt(750, 380, "Người gọi không phân biệt được “chưa làm” và “đã làm nhưng mất phản hồi”", 26, "middle", "#1f2937", True)),
           """Hình cho thấy điều mấu chốt. Ứng dụng gửi lệnh chuyển. Máy chủ đã trừ tiền xong, nhưng phản hồi bị mất trên đường về. Ứng dụng không thấy gì nên thử lại.
           Người gọi không thể phân biệt hai trường hợp, là chưa làm, và đã làm nhưng mất phản hồi."""),
        st(svg(1500, 440,
               box(40, 160, 240, 100, ["Ứng dụng", "khoá k1"], C_BLUE, bold=True),
               box(520, 40, 420, 100, "lần 1: chưa thấy k1 → làm", C_GREEN),
               box(520, 170, 420, 100, "lần 2: đã có k1 → trả kết quả cũ", C_AMBER),
               box(520, 300, 420, 100, "lần 3: đã có k1 → trả kết quả cũ", C_AMBER),
               box(1120, 160, 340, 100, ["bảng khoá", "k1 → kết quả"], C_PURPLE, bold=True),
               arrow(280, 190, 515, 90, "#2a78d6"), arrow(280, 210, 515, 220, "#2a78d6"), arrow(280, 235, 515, 345, "#2a78d6"),
               arrow(945, 90, 1115, 190, "#9333ea", "ghi"), arrow(945, 220, 1115, 220, "#9333ea", "tra")),
           """Có khoá lũy đẳng thì khác. Mỗi lần thử đều mang cùng khoá k một. Lần một, máy chủ chưa thấy khoá nên làm việc và ghi khoá cùng kết quả vào bảng.
           Lần hai và lần ba, máy chủ thấy khoá đã có, nên trả lại kết quả cũ mà không làm lại."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: thử lại an toàn", [
        st("""<p><b>Bước 1.</b> Hết giờ chờ chỉ cho biết <b>chưa nhận phản hồi</b>, không cho biết máy chủ đã làm hay chưa. Muốn biết kết quả, người gọi phải gửi lại hoặc hỏi lại, nên thử lại là chuyện thường xảy ra.</p>
<span class='note'>Làm thử: 3 lần gửi, 0 phản hồi tới nơi, vẫn không biết số lần đã trừ.</span>""",
           """Bước một, vì hết giờ chờ chỉ cho biết chưa nhận được phản hồi, chứ không cho biết máy chủ đã làm hay chưa, nên muốn biết kết quả người gọi phải gửi lại hoặc hỏi lại. Thử lại vì thế là chuyện thường xảy ra.
           Làm thử, ba lần gửi mà không phản hồi nào tới nơi, người gọi vẫn không biết đã trừ mấy lần."""),
        st("""<p><b>Bước 2.</b> Người gọi sinh <b>một khoá duy nhất cho mỗi việc</b> rồi gửi kèm cả ba lần. Khoá đại diện cho <i>việc</i>, không đại diện cho <i>lần gửi</i>.</p>
<span class='note'>Làm thử: ba lần gửi, một khoá k1.</span>""",
           """Bước hai, vì cả ba lần gửi đều là cùng một việc, nên người gọi sinh một khoá duy nhất cho việc đó và gửi kèm mọi lần. Khoá đại diện cho việc, không đại diện cho lần gửi.
           Làm thử, ba lần gửi nhưng chỉ có một khoá."""),
        st("""<p><b>Bước 3.</b> Máy chủ tra khoá. Chưa có thì làm rồi lưu <b>trong cùng một giao dịch</b> với việc trừ tiền. Đã có thì trả kết quả đã lưu.</p>
<span class='note'>Làm thử: số lần trừ tiền = số khoá khác nhau = 1.</span>""",
           """Bước ba, máy chủ tra khoá. Chưa có thì làm việc và lưu khoá trong cùng một giao dịch với việc trừ tiền. Đã có thì trả kết quả đã lưu.
           Vì vậy số lần trừ tiền bằng số khoá khác nhau, tức là một."""),
    ], checks=["len({'k1', 'k1', 'k1'}) == 1", "alg.bnk_unique_key_rows(3) == 1"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Số dư đầu $2\\,000\\,000$, mỗi lần chuyển $500\\,000$, thử tổng cộng $3$ lần.</p>
$$① \\; \\text{không khoá: } 3 \\cdot 500\\,000 = \\hl{1\\,500\\,000}\\ \\text{đã trừ}$$""",
           """Ta tính cả hai trường hợp. Số dư đầu hai triệu, mỗi lần chuyển năm trăm nghìn, thử ba lần. Phép tính thứ nhất, không có khoá, bị trừ ba nhân năm trăm nghìn, là một triệu năm trăm nghìn."""),
        st("""<p>Dùng lại $1\\,500\\,000$ ở phép ①.</p>
$$② \\; 2\\,000\\,000 - 1\\,500\\,000 = \\hl{500\\,000}\\ \\text{còn lại}$$""",
           """Phép tính thứ hai, số dư còn hai triệu trừ một triệu năm trăm nghìn, bằng năm trăm nghìn."""),
        st("""$$③ \\; \\text{có khoá: } 1 \\cdot 500\\,000 = \\hlg{500\\,000}\\ \\text{đã trừ}$$""",
           """Phép tính thứ ba, khi có khoá, chỉ trừ một lần, tức năm trăm nghìn."""),
        st("""$$④ \\; 2\\,000\\,000 - 500\\,000 = \\hlg{1\\,500\\,000}\\ \\text{còn lại}$$""",
           """Phép tính thứ tư, số dư còn hai triệu trừ năm trăm nghìn, bằng một triệu năm trăm nghìn, đúng như một lần chuyển."""),
        st("""$$⑤ \\; 1\\,500\\,000 - 500\\,000 = \\hl{1\\,000\\,000}\\ \\text{bị trừ oan khi không có khoá}$$""",
           """Phép tính thứ năm, chênh lệch giữa hai trường hợp là một triệu năm trăm nghìn trừ năm trăm nghìn, bằng một triệu, chính là số tiền bị trừ oan khi không có khoá."""),
    ], checks=["3 * 500000 == 1500000", "alg.bnk_retry_sim(2000000, 500000, 3, False) == 500000",
               "alg.bnk_retry_sim(2000000, 500000, 3, True) == 1500000",
               "alg.bnk_retry_sim(2000000, 500000, 3, True) - alg.bnk_retry_sim(2000000, 500000, 3, False) == 1000000"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: để cơ sở dữ liệu chặn trùng", [
        st("""<p>Đường khác: tạo bảng có ràng buộc <code>UNIQUE</code> trên khoá, rồi chèn cùng khoá ba lần. Ràng buộc cho phép <b>đúng một dòng</b> vào.</p>
$$\\text{số dòng} = \\hl{1}$$""",
           """Kiểm bằng đường khác. Trong cơ sở dữ liệu, bảng là nơi lưu các dòng, và ràng buộc duy nhất là luật cấm hai dòng có cùng giá trị ở một cột. Ta tạo một bảng có ràng buộc duy nhất trên khoá rồi chèn cùng khoá ba lần. Vì cơ sở dữ liệu chỉ cho một dòng vào, số dòng cuối cùng là một.
           Cách này chặn trùng ngay cả khi hai lần thử đến cùng lúc."""),
        st(table(["phương thức", "an toàn (không đổi dữ liệu)", "lũy đẳng"],
                 [["GET", "có", "có"], ["PUT", "không", "có"], ["DELETE", "không", "có"], ["POST", "không", "không (cần khoá)"]]),
           """Bảng này tổng hợp các phương thức. Đọc là an toàn và lũy đẳng. Ghi đè và xoá thay đổi dữ liệu nhưng lũy đẳng. Còn P O S T không lũy đẳng, nên cần khoá nếu muốn thử lại an toàn."""),
    ], checks=["alg.bnk_unique_key_rows(3) == 1", "alg.bnk_unique_key_rows(1) == 1"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Cho rằng gọi lại cho an toàn. Với việc thay đổi tiền, gọi lại <b class="red">không</b> an toàn nếu không có khoá.</div>""",
           """Lỗi thứ nhất, của người mới. Cho rằng cứ gọi lại là an toàn. Với việc thay đổi tiền, gọi lại không an toàn nếu không có khoá."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Kiểm tra rồi mới chèn</b>: đọc xem khoá có chưa, chưa có thì làm. Hai lần thử đến cùng lúc đều thấy “chưa có” rồi đều làm.
<br><span class="note">Cách chữa: ràng buộc UNIQUE, để cơ sở dữ liệu quyết định.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là kiểm tra rồi mới chèn. Đọc xem khoá đã có chưa, chưa có thì làm. Hai lần thử đến cùng lúc đều thấy chưa có, nên đều làm.
           Cách chữa là dùng ràng buộc duy nhất, để cơ sở dữ liệu quyết định."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Dùng lại cùng khoá cho yêu cầu <b>khác nội dung</b>. Máy chủ phải từ chối thay vì trả kết quả cũ. Khoá cũng cần hạn lưu đủ dài hơn thời gian thử lại.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là dùng lại cùng khoá cho một yêu cầu khác nội dung. Máy chủ phải từ chối thay vì trả kết quả cũ.
           Khoá cũng cần được lưu lâu hơn thời gian người gọi còn thử lại."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Số dư 1 000 000, chuyển 200 000, thử 5 lần, không khoá. Còn bao nhiêu?"],
                  ["2", "Cùng đề nhưng có khoá lũy đẳng. Còn bao nhiêu?"],
                  ["3", "Quyết định: lưu khoá ở bộ đệm (vùng lưu tạm trong bộ nhớ, đọc rất nhanh, có thể mất) hay trong cơ sở dữ liệu cùng giao dịch trừ tiền?"]]),
           """Đến lượt bạn. Câu một, số dư một triệu, chuyển hai trăm nghìn, thử năm lần, không khoá, còn bao nhiêu? Câu hai, cùng đề nhưng có khoá lũy đẳng, còn bao nhiêu?
           Câu ba, lưu khoá ở bộ đệm, tức vùng lưu tạm trong bộ nhớ đọc rất nhanh nhưng có thể mất, hay trong cơ sở dữ liệu cùng giao dịch trừ tiền? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: bị trừ $5 \\cdot 200\\,000 = 1\\,000\\,000$.</p>
$$1\\,000\\,000 - 1\\,000\\,000 = \\hl{0}$$""",
           """Đáp án câu một. Bị trừ năm nhân hai trăm nghìn, là một triệu, nên số dư còn lại bằng không."""),
        st("""<p>Câu 2: chỉ trừ một lần.</p>
$$1\\,000\\,000 - 200\\,000 = \\hlg{800\\,000}$$""",
           """Đáp án câu hai. Có khoá thì chỉ trừ một lần, nên còn tám trăm nghìn."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["khoá trong cơ sở dữ liệu, cùng giao dịch", "khoá và việc trừ tiền cùng thành công hoặc cùng huỷ", "tốn thêm một lần ghi"],
                  ["khoá chỉ ở bộ đệm", "nhanh", "không cùng giao dịch với việc trừ: khoá có thể hết hạn, mất khi chuyển dự phòng, hoặc ghi xong mà việc trừ bị huỷ"]]),
           """Đáp án câu ba. Lưu khoá trong cơ sở dữ liệu cùng giao dịch thì khoá và việc trừ tiền cùng thành công hoặc cùng huỷ, đổi lại tốn thêm một lần ghi.
           Chỉ lưu ở bộ đệm thì nhanh, nhưng khoá không cùng giao dịch với việc trừ tiền. Khoá có thể hết hạn, mất khi chuyển sang máy dự phòng,
           hoặc ghi xong mà việc trừ lại bị huỷ."""),
    ], checks=["alg.bnk_retry_sim(1000000, 200000, 5, False) == 0", "alg.bnk_retry_sim(1000000, 200000, 5, True) == 800000"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mất phản hồi", "người gọi thử lại", "cùng một khoá", "máy chủ chỉ làm một lần"),
           """Tổng kết chuỗi logic. Phản hồi có thể mất, nên người gọi thử lại. Mọi lần thử mang cùng một khoá, và máy chủ chỉ làm một lần."""),
        st("""<div class='box key'><b>Tư duy:</b> trong mạng, “không nhận được phản hồi” khác với “việc chưa làm”.
Thiết kế mọi việc thay đổi tiền sao cho <b>thử lại không gây hại</b>.</div>""",
           """Điều cần mang theo. Trong mạng, không nhận được phản hồi khác với việc chưa làm. Hãy thiết kế mọi việc thay đổi tiền sao cho thử lại không gây hại."""),
    ])
    # ── AF2: P1 curl/tiêu đề/cổng, mã chạy thật (máy chủ + curl, SQL), quy mô, tự làm ──
    add_steps([pre], "prereq", [
        st(table(["thêm ba điều", "nghĩa", "ví dụ"],
                 [["⑤ curl", "công cụ dòng lệnh gửi một yêu cầu HTTP tới một địa chỉ rồi in phản hồi; cờ <code>-s</code> im lặng, <code>-X POST</code> chọn phương thức, <code>-H</code> thêm tiêu đề, <code>-w \"\\n\"</code> in thêm xuống dòng cuối", "<code>curl -s -X POST địa_chỉ</code>"],
                  ["⑥ Tiêu đề (header)", "dòng chữ kèm theo yêu cầu, dạng <code>Tên: giá trị</code>", "<code>Idempotency-Key: abc</code>"],
                  ["⑦ localhost và cổng", "<code>localhost</code> là chính máy này; <b>cổng</b> là số cửa mà chương trình lắng nghe yêu cầu", "<code>localhost:8099</code>"]]),
           """Thêm ba điều nữa. Công cụ dòng lệnh để gọi địa chỉ web gửi một yêu cầu tới một địa chỉ rồi in phản hồi. Mỗi cờ lệnh của nó có một việc, như im lặng, chọn phương thức, thêm tiêu đề, hay in thêm dòng trống cuối.
           Tiêu đề là dòng chữ kèm theo yêu cầu, dạng tên, dấu hai chấm, giá trị. Còn máy nội bộ là chính máy này, và cổng là số cửa mà chương trình lắng nghe yêu cầu.""", clear=True),
    ], at=1)
    pre["title"] = "Trước hết: bảy điều cần hiểu"
    run = sc("chay_that", "example", "Chạy thật: máy chủ nhỏ và sáu lần gọi", [
        st(code_block(may_chu, lines=(6, 12), title="Tệp MayChu.java (phần 1): hai số dư và bảng nhớ khoá"),
           """Ta dựng một máy chủ nhỏ bằng thư viện có sẵn của Java. Hai biến là hai số dư thử, mỗi số hai triệu. Bản đồ này ghi nhớ khoá nào đã xử lý, kèm phản hồi đã trả.
           Hàm trả viết phản hồi về cho người gọi."""),
        st(code_block(may_chu, lines=(14, 18), title="Phần 2: hai đường dẫn"),
           """Máy chủ lắng nghe ở cổng tám nghìn không trăm chín mươi chín. Đường dẫn thứ nhất không kiểm khoá, nên mỗi lần được gọi là trừ năm trăm nghìn rồi trả số dư.
           Đường dẫn thứ hai lấy khoá từ tiêu đề. Nếu khoá chưa có thì trừ tiền, lưu phản hồi và trả. Nếu khoá đã có thì trả lại đúng phản hồi cũ.""", clear=True),
        st(code_block(curl_thu, lines=(5, 10), title="Cửa sổ lệnh thứ hai (máy chủ chạy ở cửa sổ thứ nhất bằng java MayChu.java)"),
           """Ở cửa sổ lệnh thứ hai, ta gửi sáu yêu cầu. Ba yêu cầu đầu đi tới đường dẫn không khoá. Ba yêu cầu sau đi tới đường dẫn có khoá, và cùng mang một khoá giống nhau, giống như ứng dụng thử lại.""", clear=True),
        st(out_block(curl_thu),
           """Khi chạy thật, không khoá thì cả ba lần đều bị trừ, số dư còn năm trăm nghìn, tức là bị trừ oan hai lần. Có khoá thì lần đầu trừ, hai lần sau nhận lại đúng phản hồi cũ, số dư vẫn một triệu năm trăm nghìn.
           Máy chủ mẫu này xử lý lần lượt từng yêu cầu. Hai yêu cầu cùng khoá đến cùng lúc cần thêm một cơ chế chặn, như ràng buộc duy nhất ở bước sau.""", clear=True),
    ])
    add_steps([chk], "check", [
        st(code_block(sql_khoa, title="Chạy thật: bảng khoá, chèn cùng khoá ba lần (sqlite)"),
           """Máy chủ thật không giữ khoá trong bộ nhớ, vì khởi động lại là mất, nên lưu vào bảng. Lệnh tạo bảng khai cột khoá là khoá chính, nghĩa là cơ sở dữ liệu không cho hai dòng trùng giá trị ở cột này.
           Lệnh chèn thêm một dòng. Với cách bỏ qua nếu trùng của cơ sở dữ liệu nhỏ này, lần chèn trùng bị bỏ qua. Ta chèn cùng một khoá ba lần.""", clear=True),
        st(out_block(sql_khoa),
           """Khi chạy thật, lệnh đếm cho ra một, và dòng còn lại mang phản hồi của lần chèn đầu. Vì khoá chính từ chối khoá trùng, nên ngay cả hai yêu cầu cùng khoá đến cùng lúc, cơ sở dữ liệu chỉ cho một cái vào.
           Cách bỏ qua nếu trùng là riêng của cơ sở dữ liệu này, cơ sở khác dùng cách bắt lỗi trùng khoá.""", clear=True),
    ], at=1)
    scale = sc("quy_mo", "example", "Quy mô: thử lại nhỏ, thiệt hại lớn khi tải tăng", [
        st("""<p>Mỗi ngày có $N$ lệnh chuyển $500\\,000$ đồng. Giả sử $0{,}1\\%$ lệnh mất phản hồi và ứng dụng thử lại một lần (số minh hoạ). Không có khoá thì mỗi lần như vậy trừ oan một lần:
$$\\text{thiệt hại} = N \\cdot 0{,}001 \\cdot 500\\,000\\ \\text{đồng}$$</p>"""
           + table(["tải", "lệnh mỗi ngày $N$", "lệnh bị trừ trùng", "thiệt hại mỗi ngày", "bảng khoá (64 byte mỗi khoá)"],
                   [["×1", "100 000", "100", "50 000 000 đồng", "6,4 MB"],
                    ["×100", "10 000 000", "10 000", "<b>5 tỉ đồng</b>", "640 MB"],
                    ["×10 000", "1 000 000 000", "1 000 000", "<b>500 tỉ đồng</b>", "<b>64 GB</b>"]]),
           """Mỗi ngày có N lệnh chuyển năm trăm nghìn đồng. Giả sử một phần nghìn số lệnh mất phản hồi và ứng dụng thử lại một lần. Đây là số minh hoạ.
           Không có khoá thì mỗi lần như vậy trừ oan một lần. Ở một trăm nghìn lệnh mỗi ngày, có một trăm lệnh trừ trùng, năm mươi triệu đồng. Tải tăng một trăm lần thì thiệt hại năm tỉ đồng mỗi ngày.
           Tải tăng mười nghìn lần thì thiệt hại năm trăm tỉ đồng mỗi ngày.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Nhân viên đối soát và hoàn tiền thủ công: ở ×1 là 100 lệnh mỗi ngày, làm được; ở ×100 là 10 000 lệnh; ở ×10 000 là 1 triệu lệnh mỗi ngày, không ai làm nổi.
<b>Khoá lũy đẳng</b> giải được, nhưng bảng khoá phình theo: 6,4 MB, 640 MB, 64 GB mỗi ngày (mỗi khoá 64 byte, số minh hoạ).</div>
<div class="box key"><b>Đánh đổi:</b> cho khoá <b>hết hạn</b> (ví dụ sau 24 giờ) và chia bảng theo ngày để dọn nhanh. Giữ ngắn thì nhẹ bảng, nhưng ứng dụng thử lại muộn hơn thời hạn sẽ bị trừ trùng; giữ dài thì tốn chỗ.</div>""",
           """Giải pháp cũ là nhân viên đối soát rồi hoàn tiền thủ công. Ở tải gốc là một trăm lệnh mỗi ngày, làm được. Ở tải gấp trăm lần là mười nghìn lệnh, và ở tải gấp mười nghìn lần là một triệu lệnh mỗi ngày, không ai làm nổi.
           Khoá lũy đẳng giải được chuyện này, nhưng bảng khoá phình theo. Nếu mỗi khoá chiếm sáu mươi bốn byte, bảng tăng từ sáu phẩy bốn mê ga byte tới sáu mươi bốn nghìn mê ga byte mỗi ngày.
           Đánh đổi là cho khoá hết hạn, ví dụ sau hai mươi bốn giờ, và chia bảng theo ngày để dọn nhanh. Giữ ngắn thì nhẹ bảng nhưng ứng dụng thử lại muộn hơn thời hạn sẽ bị trừ trùng, còn giữ dài thì tốn chỗ.""", clear=True),
    ], checks=["100000 * 0.001 == 100", "100 * 500000 == 50_000_000", "10_000_000 * 0.001 == 10000", "10000 * 500000 == 5_000_000_000",
               "1_000_000_000 * 0.001 == 1_000_000", "1_000_000 * 500000 == 500_000_000_000", "100000 * 64 == 6_400_000",
               "10_000_000 * 64 == 640_000_000", "1_000_000_000 * 64 == 64_000_000_000"])
    write_lab("BNK", "L03", """# Lab BNK L03 — Bốn yêu cầu, hai khoá

Số dư đầu **3 000 000**; mỗi yêu cầu chuyển **trừ 700 000**. Bốn yêu cầu đến theo thứ tự với khoá lũy đẳng `k1`, `k1`, `k2`, `k1` (hai lần thử lại cùng khoá `k1`).

Viết chương trình `XuLyTrung` (tệp `XuLyTrung.java`):
1. Hàm `static long chuyen(String khoa)`: nếu `khoa` chưa xử lý thì trừ 700 000 vào số dư và nhớ **phản hồi** (số dư sau khi trừ); nếu đã xử lý thì **trả lại đúng phản hồi đã nhớ**, không trừ nữa. (Gợi ý: `Map<String, Long>` và `computeIfAbsent`.)
2. Với từng khoá trong dãy, in một dòng đúng dạng `k1 -> 2300000`.

Chạy: `javac XuLyTrung.java && java XuLyTrung`. Chấm: `bash labs/cham.sh BNK L03 XuLyTrung.java`.
""", "java", xu_ly["code"], xu_ly["out"])
    lab = practice_scene(sc, "Tự làm: bốn yêu cầu, hai khoá", practice_steps(
        st, "BNK", "L03",
        """<p><b>Đề</b>: số dư 3 000 000, mỗi yêu cầu trừ 700 000. Bốn yêu cầu mang khoá <code>k1</code>, <code>k1</code>, <code>k2</code>, <code>k1</code>. Viết <code>XuLyTrung.java</code>:</p>
<ol><li>hàm <code>chuyen(String khoa)</code>: khoá mới thì trừ và nhớ phản hồi (số dư sau trừ); khoá cũ thì trả lại phản hồi đã nhớ</li>
<li>mỗi khoá in một dòng <code>k1 -&gt; 2300000</code></li></ol>
<p class="note">Chạy: <code>javac XuLyTrung.java &amp;&amp; java XuLyTrung</code>.</p>""",
        """Bây giờ tới phần bạn tự làm. Số dư ba triệu, mỗi yêu cầu trừ bảy trăm nghìn. Bốn yêu cầu đến với khoá k một, k một, k hai, rồi lại k một. Hãy viết hàm xử lý: khoá mới thì trừ tiền và nhớ phản hồi, khoá đã có thì trả lại phản hồi cũ mà không trừ nữa.
        Mỗi khoá in một dòng, gồm khoá, mũi tên, và phản hồi. Hãy dừng video, tự viết và chạy, đừng chép lại ví dụ.""",
        xu_ly["out"], "XuLyTrung.java",
        """<div class="box key"><b>Nếu kẹt:</b> dùng <code>Map&lt;String, Long&gt; daXuLy</code> và <code>return daXuLy.computeIfAbsent(khoa, k -&gt; soDu -= 700_000);</code>
(<code>computeIfAbsent</code>: khoá chưa có thì chạy phần sau mũi tên, lưu rồi trả; có rồi thì trả luôn giá trị cũ).
Lời giải ở <code>labs/BNK/L03/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, dùng một bản đồ từ khoá sang số. Hàm tính phản hồi chỉ chạy khi khoá chưa có trong bản đồ, nên nó trừ tiền đúng một lần cho mỗi khoá, còn lần sau trả luôn giá trị cũ.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=120), "BNK", "L03")
    return lesson("L03", "rest_api_khoa_luy_dang", "Bài 3 — REST API và khoá lũy đẳng",
                  "curriculum/bnk.yaml L03; audit/bnk/verify_bnk.py L03; audit/review/screen_code/BNK.yaml (máy chủ com.sun.net.httpserver + curl + sqlite chạy thật, JDK 21); RFC 9110 HTTP Semantics (phương thức an toàn và lũy đẳng); Java SE 21 API: com.sun.net.httpserver.HttpServer, Map.computeIfAbsent; sqlite: INSERT OR IGNORE, PRIMARY KEY",
                  ["Nêu vì sao thử lại là bình thường trong mạng", "Tính số tiền bị trừ oan khi không có khoá lũy đẳng",
                   "Thiết kế bảng khoá để chặn xử lý trùng", "Phân biệt phương thức an toàn và lũy đẳng",
                   "Chạy một máy chủ nhỏ và gọi bằng công cụ dòng lệnh để thấy thử lại gây trừ trùng",
                   "Tính thiệt hại và dung lượng bảng khoá khi tải tăng ×100 và ×10 000",
                   "Viết hàm xử lý yêu cầu chặn trùng bằng khoá lũy đẳng"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "intuition"), (2, "example"), (3, "check"), (4, "sym"), (5, "chay_that"), (6, "quy_mo"), (7, "practice")])
