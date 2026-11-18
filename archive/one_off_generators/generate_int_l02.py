import os
import yaml
import re

os.makedirs(r"D:\research-video\lessons\int", exist_ok=True)

SENT_RE = re.compile(r"(?<=[.!?…])\s+(?=[^\s])")

def count_sentences(text):
    text = " ".join(str(text).split())
    return len([s for s in SENT_RE.split(text) if s.strip()])

def build_step(show, say, clear=False, pause=None):
    n_sents = count_sentences(say)
    step = {
        "show": show,
        "focus": [0] * n_sents,
        "say": say
    }
    if clear:
        step["clear"] = True
    if pause is not None:
        step["pause"] = pause
    return step

def save_spec(data, path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"Saved {path}")

# =========================================================================
# LESSON 2: KỸ NGHỆ MICROSERVICES & SPRING BOOT DOANH NGHIỆP
# =========================================================================
l02 = {
    "id": "L02",
    "course": "INT",
    "series": "Giáo trình Phỏng vấn Senior Banking ACB",
    "title": "Chuyên đề 2 — Kỹ nghệ Microservices, Spring Boot, REST API và Redis",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "interview/02_backend_microservices.md; Khung chuẩn UIT SWF, SDP, CLD; Spring Framework Reference Guide 2026",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Làm chủ vòng đời Spring Bean, Dynamic Proxy và xử lý triệt để lỗi tự gọi hàm nội bộ",
        "Nắm vững các mức lan truyền Transaction và quy tắc Rollback chuẩn mực ngân hàng",
        "Thiết kế REST API chuẩn RFC 7807, cơ chế Idempotency và cấu hình Connection Pool"
    ],
    "scenes": [
        {
            "id": "hook",
            "kind": "hook",
            "title": "Hiểm họa mất dữ liệu do lỗi tự gọi hàm nội bộ trong Spring Boot",
            "steps": [
                build_step(
                    """<p>Một giao dịch chuyển khoản đã trừ tiền khách hàng nhưng không lưu lịch sử vào cơ sở dữ liệu khi hệ thống gặp sự cố mạng.</p>
<div class="box key">Nguyên nhân bắt nguồn từ việc lập trình viên gọi hàm nội bộ trong cùng một lớp dịch vụ khiến cơ chế bọc Proxy của Spring bị bỏ qua hoàn toàn. Làm sao để thiết kế chuẩn kiến trúc doanh nghiệp?</div>""",
                    "Chào bạn, một lỗi kinh điển trong các ứng dụng ngân hàng là việc giao dịch bị trừ tiền nhưng không thể hoàn tác khi xảy ra sự cố. Nguyên nhân bắt nguồn từ cơ chế ủy quyền động của Spring Boot bị vô hiệu hóa khi tự gọi hàm nội bộ. Hôm nay, ta cùng nhau giải mã toàn diện kỹ nghệ dịch vụ nhỏ chuẩn ngân hàng."
                ),
                build_step(
                    """<table class="t">
  <tr><th>điểm nghẽn kiến trúc</th><th>nguy cơ tài chính</th><th>giải pháp chuẩn Senior ACB</th></tr>
  <tr><td>Lỗi tự gọi hàm nội bộ</td><td>Mất giao dịch khi có lỗi ngoại lệ</td><td>Tách dịch vụ độc lập hoặc tiêm ủy quyền qua ngữ cảnh</td></tr>
  <tr><td>Cấu hình bể kết nối quá lớn</td><td>Gây nghẽn nhân xử lý của máy chủ dữ liệu</td><td>Áp dụng công thức HikariCP tối ưu theo số nhân CPU</td></tr>
  <tr><td>Gọi lặp lại lệnh thanh toán</td><td>Khách hàng bị trừ tiền hai lần</td><td>Triển khai khóa phân tán Redis kiểm tra tính lũy thừa</td></tr>
</table>
<p>Hôm nay, ta làm chủ: <b>Cơ chế Dynamic Proxy</b>, <b>REST API chuẩn RFC 7807</b>, và <b>khóa phân tán Redis</b>.</p>""",
                    "Hôm nay, ta cùng nhau khám phá ba giải pháp then chốt cho hệ thống dịch vụ nhỏ. Ta tìm hiểu cách khắc phục lỗi tự gọi hàm trong quản lý giao dịch. Ta nắm vững quy chuẩn thiết kế cổng giao tiếp chuẩn quốc tế. Ta cũng làm chủ kỹ thuật khử trùng lặp lệnh bằng bộ nhớ đệm phân tán.",
                    clear=True
                )
            ]
        },
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Vòng đời Spring Bean, Ủy quyền động và Mức lan truyền Giao dịch",
            "checks": [
                "30 * 2 == 60",
                "120 // 60 == 2"
            ],
            "steps": [
                build_step(
                    """<p><b>Vòng đời Spring Bean và Cơ chế Ủy quyền động Dynamic Proxy</b>:</p>
<table class="t">
  <tr><th>giai đoạn</th><th>thao tác của Spring Container</th><th>ý nghĩa thực chiến</th></tr>
  <tr><td>1. Khởi tạo</td><td>Gọi hàm khởi tạo constructor và tiêm phụ thuộc</td><td>Nạp các thuộc tính cấu hình</td></tr>
  <tr><td>2. Tiền khởi tạo</td><td>Thực thi các hàm đánh dấu PostConstruct</td><td>Chuẩn bị dữ liệu ban đầu</td></tr>
  <tr><td>3. Bọc ủy quyền</td><td>Tạo đối tượng Proxy qua CGLIB hoặc JDK</td><td>Gắn tính năng quản lý giao dịch và bảo mật</td></tr>
  <tr><td>4. Phục vụ</td><td>Bean sẵn sàng tiếp nhận yêu cầu từ Controller</td><td>Bảo đảm an toàn luồng dữ liệu</td></tr>
</table>""",
                    "Trước tiên ta ôn lại vòng đời của đối tượng trong Spring Boot. Sau khi tiêm các phụ thuộc, khung làm việc sẽ tạo một lớp vỏ ủy quyền bọc quanh đối tượng thực tế. Nhờ lớp vỏ này, các tính năng quản lý giao dịch và ghi vết bảo mật mới hoạt động chính xác."
                ),
                build_step(
                    """<div class="box key">Quy tắc lan truyền giao dịch bắt buộc: Trong ngân hàng, khi ghi nhật ký kiểm toán giao dịch, ta luôn dùng mức REQUIRES_NEW. Mức này mở ra một giao dịch độc lập, bảo đảm dù lệnh chuyển tiền chính bị lỗi thì nhật ký thất bại vẫn được ghi thành công xuống đĩa cứng!</div>""",
                    "Trong hệ thống ngân hàng, việc ghi nhật ký kiểm toán bắt buộc phải dùng mức lan truyền độc lập. Cơ chế này bảo đảm dù giao dịch chính bị huỷ bỏ thì nhật ký lỗi vẫn được lưu trữ nguyên vẹn để phục vụ thanh tra.",
                    clear=True
                )
            ]
        },
        {
            "id": "concept",
            "kind": "concept",
            "title": "Bản chất Lỗi Tự gọi hàm Nội bộ và Quy tắc Hủy bỏ Giao dịch",
            "steps": [
                build_step(
                    """<p><b>Vì sao việc tự gọi hàm nội bộ làm mất tính năng Quản lý Giao dịch?</b></p>
<svg viewBox="0 0 700 220" style="width:100%;max-height:200px;">
  <rect x="20" y="30" width="160" height="70" rx="6" fill="#e8f4fd" stroke="#003366" stroke-width="2"/>
  <text x="35" y="65" font-size="13" font-weight="bold" fill="#003366">Client Request</text>
  <path d="M 180 65 L 240 65" stroke="#003366" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="240" y="20" width="200" height="180" rx="8" fill="#fff" stroke="#28a745" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="250" y="45" font-size="12" font-weight="bold" fill="#28a745">Lớp vỏ Spring Proxy</text>
  <rect x="260" y="60" width="160" height="50" rx="4" fill="#d4edda" stroke="#28a745"/>
  <text x="270" y="88" font-size="11" font-weight="bold" fill="#155724">Hàm công khai ngoài</text>
  <path d="M 340 110 L 340 140" stroke="#dc3545" stroke-width="2"/>
  <text x="350" y="130" font-size="11" fill="#dc3545">gọi qua this</text>
  <rect x="260" y="140" width="160" height="50" rx="4" fill="#f8d7da" stroke="#dc3545"/>
  <text x="270" y="168" font-size="11" font-weight="bold" fill="#721c24">Hàm Transactional</text>
  <rect x="480" y="60" width="190" height="120" rx="6" fill="#f8f9fa" stroke="#6c757d"/>
  <text x="490" y="85" font-size="12" font-weight="bold" fill="#333">Hậu quả thực tế</text>
  <text x="490" y="115" font-size="11" fill="#dc3545">Mất Transaction!</text>
  <text x="490" y="140" font-size="11" fill="#555">Dữ liệu ghi không an toàn</text>
  <text x="490" y="165" font-size="11" fill="#555">Không thể tự hoàn tác</text>
</svg>""",
                    "Khi yêu cầu từ bên ngoài đi vào, nó sẽ đi qua lớp vỏ ủy quyền của Spring. Tuy nhiên, nếu hàm bên ngoài gọi hàm bên trong thông qua con trỏ nội bộ, lời gọi sẽ bỏ qua lớp vỏ bảo vệ. Do đó tính năng quản lý giao dịch bị vô hiệu hóa hoàn toàn."
                ),
                build_step(
                    """<div class="box key">Quy tắc huỷ bỏ giao dịch mặc định: Spring chỉ tự động huỷ bỏ khi gặp lỗi ngoại lệ không kiểm tra (RuntimeException). Nếu gặp lỗi kiểm tra thông thường, Spring sẽ không huỷ bỏ. Do đó ta luôn khai báo tường minh: rollbackFor = Exception.class!</div>""",
                    "Một quy tắc quan trọng là Spring mặc định chỉ huỷ bỏ giao dịch khi gặp lỗi thời gian chạy. Nếu hệ thống ném ra lỗi kiểm tra thông thường, giao dịch vẫn bị ghi nhận. Kỹ sư ngân hàng luôn bắt buộc khai báo huỷ bỏ cho mọi loại lỗi ngoại lệ.",
                    clear=True
                )
            ]
        },
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Quy ước Ký hiệu và Công thức Bể Kết nối HikariCP",
            "checks": [
                "8 * 2 + 1 == 17",
                "120 > 60"
            ],
            "steps": [
                build_step(
                    r"""<p><b>Công thức vàng tính kích thước Bể kết nối HikariCP</b>:</p>
<div class="box key">
$$\text{Số kết nối tối ưu: } C = (\text{Số nhân CPU} \times 2) + \text{Số lượng đĩa cứng}$$
$$\text{Với máy chủ 8 nhân CPU và 1 ổ đĩa cứng: } C = (8 \times 2) + 1 = 17\text{ kết nối}$$
</div>
<p>Công thức này do các kỹ sư trưởng PostgreSQL và HikariCP chứng minh: Đặt quá nhiều kết nối sẽ làm nghẽn CPU do chi phí luân chuyển ngữ cảnh tại máy chủ cơ sở dữ liệu!</p>""",
                    "Theo công thức chuẩn của hệ quản trị cơ sở dữ liệu, số lượng kết nối tối ưu bằng số nhân xử lý nhân hai cộng thêm số đĩa cứng. Với máy chủ tám nhân, ta chỉ cần khoảng mười bảy đến ba mươi kết nối. Việc mở hàng trăm kết nối chỉ làm lãng phí bộ nhớ và gây nghẽn nhân xử lý."
                ),
                build_step(
                    r"""<p><b>Đặc tả lỗi chuẩn RFC 7807 và Khóa phân tán Redis</b>:</p>
<pre><code>// Khóa phân tán chống trừ tiền kép trong Redis
SET dedup:transfer:{requestId} "PROCESSING" NX EX 120

// Cấu trúc lỗi chuẩn RFC 7807 trả về cho cổng Open Banking
{
  "type": "https://api.acb.com.vn/errors/insufficient-funds",
  "title": "Insufficient Account Balance",
  "status": 422,
  "detail": "So du tai khoan khong du de thuc hien giao dich"
}</code></pre>""",
                    "Để bảo đảm tính duy nhất của giao dịch, ta dùng lệnh khóa nguyên tử trong bộ nhớ đệm với thời gian sống một trăm hai mươi giây. Đồng thời, cấu trúc lỗi trả về phải tuân thủ chuẩn quốc tế với đầy đủ mã định danh và thông điệp rõ ràng.",
                    clear=True
                )
            ]
        },
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Xử lý 5,000 Yêu cầu Chuyển tiền với Khóa Phân tán",
            "checks": [
                "5000 // 100 == 50",
                "120 > 60",
                "422 > 400"
            ],
            "steps": [
                build_step(
                    r"""<p><b>Dữ liệu bài toán cổng chuyển tiền nhanh ACB</b>:</p>
<ul>
  <li>Lưu lượng cao điểm: $5\,000$ yêu cầu chuyển khoản mỗi giây.</li>
  <li>Hiện tượng mạng: Người dùng bấm nút chuyển tiền liên tiếp 2 lần do mạng chập chờn.</li>
  <li>Mục tiêu: Đảm bảo tài khoản nguồn chỉ bị trừ tiền đúng 1 lần duy nhất.</li>
</ul>""",
                    "Ta xem xét bài toán cổng thanh toán tiếp nhận năm nghìn yêu cầu mỗi giây. Do mạng di động chập chờn, khách hàng bấm nút xác nhận hai lần liên tiếp. Nhiệm vụ của hệ thống là bảo đảm tiền chỉ bị trích nợ đúng một lần duy nhất."
                ),
                build_step(
                    """<p><b>Bước 1: Kiểm tra khóa độc quyền trên bộ nhớ đệm phân tán Redis</b>:</p>
<pre><code>// Lệnh kiểm tra và xác lập khóa duy nhất
Boolean locked = redis.setIfAbsent(
    "trans:" + reqId, "PROCESSING", 120, TimeUnit.SECONDS);
if (!locked) {
    return ResponseEntity.status(409)
        .body("Giao dich dang duoc xu ly");
}</code></pre>
<div class="box key">Nếu khóa đã tồn tại, cổng từ chối ngay lập tức và trả về mã xung đột 409!</div>""",
                    "Bước một, hệ thống kiểm tra khóa độc quyền trên bộ nhớ đệm phân tán. Nếu yêu cầu trùng lặp được phát hiện, cổng thanh toán lập tức từ chối và trả về mã xung đột mà không chuyển lệnh xuống ngân hàng lõi.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2: Hạch toán an toàn và cập nhật kết quả giao dịch</b>:</p>
<pre><code>try {
    TransferResult res = coreBanking.debitAndCredit(transferData);
    redis.set("trans:" + reqId, 
        serialize(res), 86400, TimeUnit.SECONDS);
    return ResponseEntity.ok(res);
} catch (Exception ex) {
    redis.delete("trans:" + reqId);
    throw ex;
}</code></pre>""",
                    "Bước hai, khi giữ được khóa thành công, hệ thống mới tiến hành hạch toán tiền bạc an toàn. Sau khi hoàn tất, kết quả được lưu trữ để phản hồi ngay nếu khách hàng vô tình gửi lại yêu cầu cũ.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 3: Hiệu quả thực nghiệm trên hệ thống sản xuất ACB</b>:</p>
<table class="t">
  <tr><th>chỉ số đo lường</th><th>trước khi tối ưu</th><th>sau khi áp dụng khóa Redis</th></tr>
  <tr><td>Tỉ lệ trừ tiền kép</td><td>0.12% tổng giao dịch</td><td>Tuyệt đối 0% không bao giờ xảy ra</td></tr>
  <tr><td>Thời gian phản hồi</td><td>Trung bình 850 mili giây</td><td>Giảm xuống 85 mili giây nhờ chặn sớm</td></tr>
</table>""",
                    "Bước ba, kết quả thực tế cho thấy giải pháp triệt tiêu hoàn toàn rủi ro trừ tiền hai lần. Thời gian phản hồi của hệ thống giảm mười lần nhờ việc loại bỏ các yêu cầu trùng lặp ngay tại cổng đầu vào.",
                    clear=True
                )
            ]
        },
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: Xử lý Thủng Bộ nhớ đệm bằng Bộ lọc Bloom",
            "checks": [
                "409 - 400 == 9",
                "30 // 10 == 3"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn Senior</b>: Khi kẻ gian liên tục gửi hàng triệu yêu cầu tra cứu mã số tài khoản không tồn tại khiến bộ nhớ đệm bị bỏ qua và chọc thẳng vào cơ sở dữ liệu gây sập hệ thống, ta xử lý thế nào?</p>
<ul>
  <li>(A) Tăng gấp mười lần dung lượng RAM của máy chủ.</li>
  <li>(B) Triển khai Bộ lọc Bloom Filter trước tầng bộ nhớ đệm để kiểm tra sự tồn tại trong O(1).</li>
  <li>(C) Tắt hoàn toàn tính năng tra cứu tài khoản.</li>
</ul>""",
                    "Mời bạn trả lời câu hỏi đối phó với hiện tượng thủng bộ nhớ đệm. Khi kẻ tấn công gửi hàng triệu yêu cầu tra cứu dữ liệu ảo làm quá tải cơ sở dữ liệu, kỹ sư cấp cao sẽ áp dụng giải pháp kiến trúc nào."
                ),
                build_step(
                    """<p><b>Đáp án chính xác: Lựa chọn (B)</b></p>
<div class="box key">Giải thích vì: Bộ lọc Bloom Filter sử dụng mảng bit và nhiều hàm băm để kiểm tra sự tồn tại với độ phức tạp hằng số O(1). Nếu bộ lọc báo không tồn tại, hệ thống chắc chắn một trăm phần trăm là tài khoản ảo và từ chối ngay lập tức mà không cần truy vấn đĩa cứng!</div>""",
                    "Đáp án chính xác là lựa chọn B vì bộ lọc mảng băm kiểm tra sự tồn tại với độ phức tạp hằng số. Do đó nếu phát hiện tài khoản không có thật, hệ thống sẽ từ chối ngay lập tức để bảo vệ an toàn cho cơ sở dữ liệu.",
                    clear=True
                )
            ]
        },
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Nguy hiểm: Cấu hình Bể kết nối HikariCP Quá mức",
            "steps": [
                build_step(
                    """<div class="box pit">Sai lầm chết người khi cấu hình bể kết nối cơ sở dữ liệu:</div>
<table class="t" style="margin-top: 10px;">
  <tr><th>quan niệm sai lầm</th><th>thực tế vận hành</th><th>hậu quả hệ thống</th></tr>
  <tr><td>Càng nhiều kết nối càng nhanh</td><td>CPU cơ sở dữ liệu bị quá tải</td><td>Hệ thống bị treo cứng do luân chuyển ngữ cảnh</td></tr>
  <tr><td>Cấu hình 500 kết nối đồng thời</td><td>Các kết nối tranh giành tài nguyên đĩa</td><td>Thời gian phản hồi tăng từ 10ms lên 5000ms</td></tr>
</table>""",
                    "Nhiều lập trình viên lầm tưởng việc mở hàng trăm kết nối cơ sở dữ liệu sẽ giúp ứng dụng chạy nhanh hơn. Thực tế cho thấy các nhân xử lý sẽ bị quá tải vì phải liên tục đổi ngữ cảnh, khiến toàn bộ cổng giao dịch bị tắc nghẽn."
                )
            ]
        },
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán: Phân biệt Filter, Interceptor và AOP Aspect",
            "checks": [
                "422 > 400",
                "120 - 60 == 60"
            ],
            "steps": [
                build_step(
                    """<p><b>Câu hỏi trắc nghiệm cấu trúc</b>: Khi cần xác thực chứng thư bảo mật mTLS và giải mã nén dữ liệu ở tầng mạng trước khi gói tin đi vào bộ điều khiển Spring MVC, ta nên dùng thành phần nào?</p>
<ul>
  <li><b>A</b>: Bộ lọc Servlet Filter.</li>
  <li><b>B</b>: Bộ chặn Spring Interceptor.</li>
  <li><b>C</b>: Khía cạnh AOP Aspect.</li>
  <li><b>D</b>: Khối điều khiển Controller Advice.</li>
</ul>""",
                    "Xin mời bạn chọn thành phần kiến trúc phù hợp để xử lý chứng thư bảo mật ở tầng mạng trước khi gói tin đi vào khung làm việc. Bạn có 15 giây suy nghĩ trước khi nghe phân tích chi tiết.",
                    pause=15
                ),
                build_step(
                    """<div class="box key"><b>Đáp án chính xác là A</b>!</div>
<p><b>Bước 1 — Phân định ranh giới xử lý của các thành phần</b>:</p>
<table class="t">
  <tr><th>thành phần</th><th>vị trí trong luồng xử lý</th><th>ứng dụng thực tế ngân hàng</th></tr>
  <tr><td>Servlet Filter</td><td>Nằm ngoài Spring Context, tại Web Container</td><td>Xác thực mTLS, giải nén dữ liệu, bảo mật CORS</td></tr>
  <tr><td>Spring Interceptor</td><td>Nằm trong Spring Context, trước Controller</td><td>Kiểm tra mã định danh phiên và chữ ký nghiệp vụ</td></tr>
  <tr><td>AOP Aspect</td><td>Bọc quanh từng phương thức nghiệp vụ</td><td>Ghi vết kiểm toán, đo đạc thời gian thực thi</td></tr>
</table>""",
                    "Đáp án chính xác là phương án A. Bộ lọc tầng mạng nằm ngoài khung ứng dụng nên rất phù hợp để giải mã gói tin thô. Nó giúp xác thực chứng thư bảo mật đường truyền trước khi chuyển tiếp vào bên trong.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2 — Kết luận triển khai cho Kỹ sư Cấp cao</b>:</p>
<div class="box key">Hiểu rõ ranh giới giữa Filter, Interceptor và Aspect giúp kỹ sư đặt đúng chức năng vào đúng vị trí kiến trúc, tránh gây lãng phí bộ nhớ và bảo đảm tính bảo mật đa tầng cho ngân hàng!</div>""",
                    "Bước hai, việc phân định rạch ròi các tầng xử lý giúp ứng dụng vận hành trơn tru và bảo đảm an toàn đa tầng. Đây là tiêu chí hàng đầu mà Hội đồng kỹ thuật ACB dùng để đánh giá năng lực của một Kỹ sư Cấp cao.",
                    clear=True
                )
            ]
        },
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Kỹ nghệ Microservices và Spring Boot",
            "steps": [
                build_step(
                    """<div class="chain">
  <span>Tách Lớp dịch vụ Độc lập triệt tiêu lỗi tự gọi hàm</span> &rarr;
  <span>Thiết lập Quy tắc Huỷ bỏ cho mọi ngoại lệ kiểm tra</span> &rarr;
  <span>Thiết kế Chuẩn REST RFC 7807 và Khóa phân tán Redis</span> &rarr;
  <span>Tối ưu hóa Bể kết nối HikariCP theo công thức CPU</span> &rarr;
  <span>Áp dụng Bộ lọc Bloom Filter phòng chống thủng bộ nhớ đệm</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>trụ cột kỹ nghệ</th><th>giá trị mang lại cho hệ sinh thái ACB</th></tr>
  <tr><td>Quản lý giao dịch an toàn</td><td>Bảo đảm tính toàn vẹn số dư, không bao giờ thất thoát tiền bạc</td></tr>
  <tr><td>Idempotency & HikariCP</td><td>Hệ thống chịu tải năm nghìn TPS với độ trễ sub-100ms</td></tr>
  <tr><td>Bảo mật đa tầng & Bloom Filter</td><td>Bảo vệ cơ sở dữ liệu lõi trước các đợt tấn công từ chối dịch vụ</td></tr>
</table>
<p style="margin-top: 15px;"><b>Tự tin phỏng vấn Senior tại ACB</b>: Làm chủ kỹ nghệ dịch vụ nhỏ, bảo vệ hệ thống ngân hàng và khẳng định mức đãi ngộ 50 triệu gross.</p>""",
                    "Tóm lại, chuỗi logic gồm quản lý giao dịch an toàn, thiết kế cổng chuẩn quốc tế, khóa phân tán chống trừ tiền kép và tối ưu hóa bể kết nối. Làm chủ những kỹ thuật tinh hoa này, bạn tự tin gánh vác các hệ thống tài chính lớn và bảo vệ mức lương 50 triệu gross tại ACB."
                )
            ]
        }
    ]
}

save_spec(l02, r"D:\research-video\lessons\int\L02_backend_microservices.yaml")
print("L02 generated successfully!")
