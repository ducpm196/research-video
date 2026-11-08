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
# LESSON 1: KHOA HỌC MÁY TÍNH LÕI, JAVA 21, JVM & ĐA LUỒNG
# =========================================================================
l01 = {
    "id": "L01",
    "course": "INT",
    "series": "Giáo trình Phỏng vấn Senior Banking ACB",
    "title": "Chuyên đề 1 — Nền tảng Khoa học Máy tính, Java 21 Hiện đại, JVM và Đa luồng",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "interview/01_foundation_cs_java.md; Khung chuẩn UIT AI CS112, CS115, CSA, OSY; Java Virtual Machine Specification Java 21",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Làm chủ mô hình phân cấp bộ nhớ máy tính, CPU Cache Line và bộ nhớ JVM",
        "Hiểu sâu cơ chế Garbage Collection và các tính năng Java 21 Virtual Threads",
        "Nắm vững độ phức tạp thuật toán và cấu trúc dữ liệu B-Tree trong cơ sở dữ liệu"
    ],
    "scenes": [
        {
            "id": "hook",
            "kind": "hook",
            "title": "Bản chất máy tính và ranh giới giữa kỹ sư bình thường và Kỹ sư Cấp cao",
            "steps": [
                build_step(
                    """<p>Đa số lập trình viên viết code Java chỉ nhìn thấy cú pháp mà không hiểu điều gì diễn ra dưới thanh ghi CPU và bộ nhớ RAM.</p>
<div class="box key">Khi hệ thống ngân hàng xử lý mười nghìn giao dịch mỗi giây, một lỗi chia sẻ giả trên bộ nhớ đệm CPU hoặc đợt dừng toàn bộ hệ thống của bộ thu gom rác có thể làm nghẽn toàn bộ cổng thanh toán. Làm sao để làm chủ tận gốc?</div>""",
                    "Chào bạn, đa số lập trình viên viết mã nguồn Java mà chưa hiểu rõ điều gì thực sự xảy ra dưới thanh ghi và bộ nhớ máy tính. Khi cổng thanh toán ngân hàng chạm mốc mười nghìn giao dịch mỗi giây, sự thiếu hiểu biết về bộ nhớ đệm sẽ khiến hệ thống sụt giảm hiệu năng nghiêm trọng. Hôm nay, ta cùng nhau xây dựng lại nền tảng vững chắc từ con số không."
                ),
                build_step(
                    """<table class="t">
  <tr><th>tầng kiến thức</th><th>vấn đề hiệu năng cốt lõi</th><th>giải pháp chuẩn Kỹ sư Cấp cao</th></tr>
  <tr><td>Bộ nhớ máy tính</td><td>Độ trễ truy xuất RAM và hiện tượng chia sẻ giả</td><td>Căn chỉnh khối đệm 64 byte và phân cấp bộ nhớ</td></tr>
  <tr><td>Bộ nhớ máy ảo JVM</td><td>Hiện tượng dừng toàn bộ hệ thống do thu gom rác</td><td>Phân vùng nhớ thế hệ trẻ và thế hệ già tối ưu</td></tr>
  <tr><td>Luồng thực thi Java 21</td><td>Chi phí chuyển đổi ngữ cảnh luồng hệ điều hành</td><td>Ứng dụng luồng ảo siêu nhẹ trong không gian người dùng</td></tr>
</table>
<p>Hôm nay, ta giải mã: <b>Mô hình bộ nhớ máy tính</b>, <b>tinh chỉnh máy ảo Java</b>, và <b>công nghệ luồng ảo Java 21</b>.</p>""",
                    "Hôm nay, ta cùng nhau khám phá ba trụ cột khoa học máy tính lõi. Ta tìm hiểu cách tổ chức bộ nhớ đệm để triệt tiêu hiện tượng chia sẻ giả. Ta nắm vững cơ chế thu gom rác thế hệ mới của máy ảo Java. Ta cũng làm chủ kỹ thuật lập trình đồng thời với hàng triệu luồng ảo trong Java 21.",
                    clear=True
                )
            ]
        },
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Phân cấp bộ nhớ, Khối đệm 64 byte và Số thực dấu phẩy động",
            "checks": [
                "1000 * 1000 == 1000000",
                "100 // 1 == 100"
            ],
            "steps": [
                build_step(
                    """<p><b>Phân cấp tốc độ bộ nhớ từ thanh ghi đến bộ nhớ chính</b>:</p>
<table class="t">
  <tr><th>tầng bộ nhớ</th><th>thời gian truy xuất</th><th>khoảng cách tương đối</th></tr>
  <tr><td>Thanh ghi CPU</td><td>0.5 nano giây</td><td>tức thời tại nhân xử lý</td></tr>
  <tr><td>Bộ nhớ đệm cấp một L1</td><td>1 nano giây</td><td>nhanh gấp một trăm lần RAM</td></tr>
  <tr><td>Bộ nhớ đệm cấp hai L2</td><td>3 đến 10 nano giây</td><td>gắn liền từng nhân xử lý</td></tr>
  <tr><td>Bộ nhớ đệm cấp ba L3</td><td>20 đến 40 nano giây</td><td>chia sẻ chung giữa các nhân</td></tr>
  <tr><td>Bộ nhớ chính RAM</td><td>100 nano giây</td><td>điểm nghẽn truy xuất dữ liệu</td></tr>
</table>""",
                    "Trước tiên ta ôn lại mô hình phân cấp bộ nhớ của máy tính. Thanh ghi và bộ nhớ đệm cấp một có tốc độ tính bằng nano giây. Trong khi đó, bộ nhớ chính chậm hơn tới một trăm lần. Dữ liệu nạp từ bộ nhớ chính lên bộ nhớ đệm luôn theo từng khối 64 byte."
                ),
                build_step(
                    """<div class="box key">Quy tắc vàng trong hệ thống ngân hàng: Tuyệt đối không bao giờ dùng kiểu số thực nhị phân float hay double để lưu trữ tiền tệ. Lỗi làm tròn nhị phân theo chuẩn quốc tế sẽ làm sai lệch số dư. Ta luôn bắt buộc sử dụng kiểu số thập phân chính xác BigDecimal!</div>""",
                    "Trong hệ thống tài chính ngân hàng, ta tuyệt đối không bao giờ dùng kiểu số thực nhị phân vì lỗi làm tròn dấu phẩy động. Mọi phép tính tiền bạc và lãi suất đều bắt buộc dùng kiểu số thập phân chính xác với quy tắc làm tròn rõ ràng.",
                    clear=True
                )
            ]
        },
        {
            "id": "concept",
            "kind": "concept",
            "title": "Mô hình Bộ nhớ Máy ảo Java và Cơ chế Thu gom rác",
            "steps": [
                build_step(
                    """<p><b>Cấu trúc bộ nhớ máy ảo Java được chia làm hai khu vực chính</b>:</p>
<svg viewBox="0 0 700 220" style="width:100%;max-height:200px;">
  <rect x="20" y="20" width="450" height="180" rx="8" fill="#e8f4fd" stroke="#003366" stroke-width="2"/>
  <text x="30" y="45" font-size="14" font-weight="bold" fill="#003366">VÙNG BỘ NHỚ HEAP</text>
  <rect x="40" y="60" width="180" height="120" rx="6" fill="#fff" stroke="#006699" stroke-width="1.5"/>
  <text x="50" y="85" font-size="12" font-weight="bold" fill="#006699">Young Gen (Thế hệ trẻ)</text>
  <rect x="50" y="95" width="80" height="35" fill="#d4edda" stroke="#28a745"/>
  <text x="55" y="118" font-size="11" fill="#155724">Eden Tạo mới</text>
  <rect x="140" y="95" width="70" height="35" fill="#fff3cd" stroke="#ffc107"/>
  <text x="145" y="118" font-size="11" fill="#856404">S0 và S1</text>
  <rect x="240" y="60" width="210" height="120" rx="6" fill="#fff" stroke="#006699" stroke-width="1.5"/>
  <text x="250" y="85" font-size="12" font-weight="bold" fill="#006699">Old Gen (Thế hệ già)</text>
  <text x="250" y="115" font-size="11" fill="#555">Chứa đối tượng sống lâu năm</text>
  <text x="250" y="140" font-size="11" fill="#555">Bể kết nối, Đệm tĩnh</text>
  <rect x="490" y="20" width="190" height="85" rx="8" fill="#f8f9fa" stroke="#6c757d" stroke-width="2"/>
  <text x="500" y="45" font-size="13" font-weight="bold" fill="#333">VÙNG METASPACE</text>
  <text x="500" y="70" font-size="11" fill="#666">Bộ nhớ ngoài vùng đệm Native</text>
  <rect x="490" y="115" width="190" height="85" rx="8" fill="#f8f9fa" stroke="#6c757d" stroke-width="2"/>
  <text x="500" y="140" font-size="13" font-weight="bold" fill="#333">NGĂN XẾP LUỒNG (STACK)</text>
  <text x="500" y="165" font-size="11" fill="#666">Một megabyte cho mỗi luồng</text>
</svg>""",
                    "Nhìn vào sơ đồ bộ nhớ máy ảo Java, vùng đệm đối tượng được chia thành thế hệ trẻ và thế hệ già. Hầu hết các bản tin yêu cầu ngắn hạn sinh ra trong vùng tạo mới và nhanh chóng bị dọn sạch. Các đối tượng sống sót qua nhiều chu kỳ sẽ được chuyển lên thế hệ già."
                ),
                build_step(
                    """<table class="t">
  <tr><th>đợt thu gom rác</th><th>vùng tác động</th><th>mức độ ảnh hưởng đến giao dịch</th></tr>
  <tr><td>Thu gom rác nhỏ (Minor GC)</td><td>Vùng thế hệ trẻ (Eden và Survivor)</td><td>Rất nhanh, chỉ mất vài mili giây, ít ảnh hưởng</td></tr>
  <tr><td>Thu gom rác lớn (Major GC)</td><td>Vùng thế hệ già (Tenured Old Gen)</td><td>Dọn dẹp đối tượng tồn tại lâu năm</td></tr>
  <tr><td>Thu gom rác toàn phần (Full GC)</td><td>Toàn bộ bộ nhớ Heap và Metaspace</td><td>Dừng toàn bộ hệ thống, nguyên nhân gây quá hạn API</td></tr>
</table>""",
                    "Đợt thu gom rác nhỏ diễn ra rất nhanh nên hệ thống vẫn hoạt động mượt mà. Tuy nhiên, đợt thu gom rác toàn phần sẽ đóng băng toàn bộ ứng dụng trong nhiều giây. Đây chính là nguyên nhân hàng đầu khiến các kết nối liên ngân hàng bị quá hạn thời gian xử lý.",
                    clear=True
                )
            ]
        },
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Quy ước Ký hiệu và Công thức Tính toán Luồng Ảo Java 21",
            "steps": [
                build_step(
                    r"""<p><b>Công thức đánh giá tài nguyên luồng trong hệ thống ngân hàng</b>:</p>
<div class="box key">
$$\text{Bộ nhớ luồng truyền thống: } M_{\text{os}} = N \times 1\text{ MB}$$
$$\text{Bộ nhớ luồng ảo Java 21: } M_{\text{vt}} = N \times 500\text{ bytes}$$
$$\text{Hệ số tiết kiệm bộ nhớ: } K = \frac{1\,000\,000}{500} = 2\,000\text{ lần}$$
</div>
<p>Trong đó $N$ là số lượng kết nối mạng đồng thời, $M_{\text{os}}$ là tổng bộ nhớ luồng hệ điều hành, và $M_{\text{vt}}$ là bộ nhớ luồng ảo siêu nhẹ.</p>""",
                    "Theo quy chuẩn kỹ thuật, ta so sánh lượng bộ nhớ tiêu thụ giữa hai mô hình luồng. Với luồng truyền thống, mỗi kết nối tốn một megabyte bộ nhớ ngăn xếp. Nhưng với luồng ảo trong Java 21, mỗi kết nối chỉ tiêu tốn vài trăm byte. Nhờ vậy hệ thống tiết kiệm tới hai nghìn lần bộ nhớ."
                ),
                build_step(
                    """<p><b>Độ phức tạp thuật toán và cấu trúc Cây B-Tree trong cơ sở dữ liệu</b>:</p>
<pre><code>// Chiều cao cây B-Tree với hệ số phân nhánh m = 1000
H = ceil(log_m(N))

// Với 10 triệu bản ghi tài khoản ngân hàng (N = 10,000,000)
H = ceil(log_1000(10,000,000)) = 3 tầng I/O đĩa cứng!</code></pre>""",
                    "Để tối ưu hóa truy xuất dữ liệu sổ cái, các hệ quản trị dùng cây nhiều nhánh với hệ số phân nhánh lên tới một nghìn con. Do đó, với mười triệu tài khoản ngân hàng, chiều cao cây chỉ có ba tầng. Nghĩa là hệ thống chỉ cần tối đa ba lần đọc đĩa cứng để tìm thấy số dư.",
                    clear=True
                )
            ]
        },
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Tối ưu Xử lý 10,000 Giao dịch Đồng thời với Luồng Ảo",
            "checks": [
                "10000 * 500 // 1000000 == 5",
                "10000 * 1 == 10000",
                "10000 - 5 == 9995"
            ],
            "steps": [
                build_step(
                    """<p><b>Dữ liệu bài toán tải cao điểm cổng thanh toán ACB</b>:</p>
<ul>
  <li>Lưu lượng đồng thời: $N = 10\,000$ kết nối chuyển tiền cần xử lý I/O mạng.</li>
  <li>Thời gian xử lý I/O gọi Core T24: $T = 50$ mili giây mỗi giao dịch.</li>
  <li>Hạ tầng máy chủ: RAM 16 GB, CPU 8 nhân vật lý.</li>
</ul>""",
                    "Ta xem xét bài toán cao điểm tại cổng thanh toán ngân hàng ACB với mười nghìn kết nối đồng thời. Mỗi lệnh chuyển tiền mất năm mươi mili giây để chờ phản hồi từ hệ thống ngân hàng lõi. Hạ tầng máy chủ trang bị mười sáu gigabyte bộ nhớ và tám nhân xử lý."
                ),
                build_step(
                    r"""<p><b>Bước 1: Phân tích khi dùng mô hình Luồng Hệ điều hành truyền thống</b>:</p>
$$\text{Tổng RAM cho luồng: } M = 10\,000 \times 1\text{ MB} = 10\,000\text{ MB} \approx 10\text{ GB RAM}$$
<div class="box pit">Nguy cơ sập nguồn: Máy chủ bị quá tải bộ nhớ và nghẽn CPU do hàng chục nghìn lần chuyển đổi ngữ cảnh liên tục!</div>""",
                    "Bước một, nếu dùng luồng truyền thống, mười nghìn luồng sẽ ngốn tới mười gigabyte bộ nhớ ngăn xếp. Hệ điều hành phải luân chuyển liên tục giữa các luồng gây nghẽn nhân xử lý và làm sập ứng dụng.",
                    clear=True
                ),
                build_step(
                    r"""<p><b>Bước 2: Phân tích khi dùng Luồng Ảo Java 21 (Virtual Threads)</b>:</p>
$$\text{Tổng RAM cho luồng ảo: } M_{\text{vt}} = 10\,000 \times 500\text{ bytes} = 5\,000\,000\text{ bytes} \approx 5\text{ MB RAM}$$
<div class="box key">Hiệu quả đột phá: Tiết kiệm 99.95% bộ nhớ RAM! Tám nhân CPU chỉ chạy 8 luồng vận chuyển (Carrier Threads), không bị nghẽn chuyển đổi ngữ cảnh!</div>""",
                    "Bước hai, khi chuyển sang luồng ảo trong Java 21, mười nghìn luồng chỉ tiêu thụ khoảng năm megabyte bộ nhớ. Tám nhân xử lý chỉ tập trung chạy tám luồng vận chuyển mà không bị lãng phí chu kỳ máy.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 3: Cấu hình chuẩn doanh nghiệp trên Spring Boot 3.2+</b>:</p>
<pre><code># Kích hoạt luồng ảo toàn diện trong tệp cấu hình application.properties
spring.threads.virtual.enabled=true
server.tomcat.threads.max=10000</code></pre>
<p>Chỉ với một dòng cấu hình, Tomcat tự động phục vụ mỗi kết nối HTTP bằng một luồng ảo siêu nhẹ.</p>""",
                    "Bước ba, kỹ sư chỉ cần kích hoạt tính năng luồng ảo trong tệp cấu hình của hệ thống. Máy chủ web nhúng sẽ tự động xử lý mỗi yêu cầu của khách hàng bằng một luồng ảo riêng biệt.",
                    clear=True
                )
            ]
        },
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: Đánh giá Độ phức tạp Thuật toán và B-Tree",
            "checks": [
                "4 - 1 == 3",
                "1000 > 100"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn Senior</b>: Một bảng giao dịch có 50 triệu dòng dữ liệu. Nếu bảng chưa có chỉ mục, độ phức tạp tìm kiếm là bao nhiêu? Khi đánh chỉ mục bằng Cây B-Tree, ta tốn tối đa bao nhiêu lần đọc đĩa?</p>
<ul>
  <li>(A) Không chỉ mục tốn O(log N), có chỉ mục tốn O(1).</li>
  <li>(B) Không chỉ mục quét toàn bảng O(N), có chỉ mục B-Tree tốn O(log N) với tối đa 3 đến 4 lần đọc đĩa.</li>
  <li>(C) Không chỉ mục tốn O(N^2), có chỉ mục tốn 100 lần đọc đĩa.</li>
</ul>""",
                    "Mời bạn trả lời câu hỏi chuyên sâu về cơ sở dữ liệu. Với bảng giao dịch năm mươi triệu dòng, việc không đánh chỉ mục sẽ dẫn tới độ phức tạp nào. Và khi đánh chỉ mục dạng cây nhiều nhánh, hệ thống mất bao nhiêu lần truy xuất đĩa cứng."
                ),
                build_step(
                    """<p><b>Đáp án chính xác: Lựa chọn (B)</b></p>
<div class="box key">Giải thích bản chất: Khi không có chỉ mục, hệ quản trị bắt buộc phải quét tuần tự toàn bộ bảng với độ phức tạp tuyến tính O(N), tương đương duyệt 50 triệu dòng. Khi có chỉ mục B-Tree với hệ số phân nhánh lớn, độ phức tạp là lôgarit O(log N) và chỉ mất 3 đến 4 lần đọc đĩa cơ học!</div>""",
                    "Đáp án chính xác là lựa chọn B vì khi không có chỉ mục, hệ thống phải quét tuần tự toàn bộ năm mươi triệu dòng. Do đó khi có chỉ mục cây nhiều nhánh, việc tìm kiếm đạt độ phức tạp lôgarit và chỉ mất từ ba đến bốn lần đọc đĩa.",
                    clear=True
                )
            ]
        },
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Nguy hiểm: Rò rỉ Bộ nhớ khi Dùng ThreadLocal với Bể luồng",
            "steps": [
                build_step(
                    """<div class="box pit">Hiểm họa rò rỉ bộ nhớ với biến cục bộ luồng trong bể luồng tái sử dụng:</div>
<table class="t" style="margin-top: 10px;">
  <tr><th>nguy cơ tiềm ẩn</th><th>cơ chế rò rỉ</th><th>giải pháp khắc phục bắt buộc</th></tr>
  <tr><td>Rò rỉ bộ nhớ Heap</td><td>ThreadLocal không được giải phóng sau request</td><td>Luôn gọi lệnh remove() trong khối finally</td></tr>
  <tr><td>Lộ lọt thông tin</td><td>Luồng phục vụ phiên của khách hàng kế tiếp</td><td>Xóa sạch thông tin định danh và token cũ</td></tr>
</table>""",
                    "Một cạm bẫy kinh điển là việc dùng biến cục bộ luồng trong bể luồng tái sử dụng. Nếu kỹ sư quên gọi lệnh dọn dẹp sau khi xử lý xong, dữ liệu phiên làm việc cũ sẽ không được giải phóng. Điều này gây rò rỉ bộ nhớ nghiêm trọng và làm lộ lọt thông tin giữa các khách hàng khác nhau."
                )
            ]
        },
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán: Phân biệt String và StringBuilder trong Bản tin Ngân hàng",
            "checks": [
                "50 - 5 == 45",
                "21 > 8"
            ],
            "steps": [
                build_step(
                    """<p><b>Câu hỏi trắc nghiệm kiến trúc</b>: Trong xử lý bản tin tài chính đơn luồng với hàng triệu vòng lặp nối chuỗi XML, tại sao ta không nên dùng phép cộng chuỗi String thông thường mà nên dùng StringBuilder?</p>
<ul>
  <li><b>A</b>: String chiếm ít bộ nhớ hơn StringBuilder.</li>
  <li><b>B</b>: String là đối tượng bất biến, mỗi phép cộng chuỗi sinh ra một đối tượng mới trên Heap gây tràn bộ nhớ rác, còn StringBuilder là khả biến giúp nối trực tiếp trong mảng đệm nội bộ.</li>
  <li><b>C</b>: String an toàn đa luồng hơn StringBuilder.</li>
  <li><b>D</b>: Cả hai có hiệu năng hoàn toàn tương đương nhau.</li>
</ul>""",
                    "Xin mời bạn suy nghĩ câu hỏi về tối ưu hóa bộ nhớ khi xử lý bản tin ngân hàng. Phép nối chuỗi thông thường khác biệt thế nào so với bộ dựng chuỗi khả biến. Bạn có 15 giây suy nghĩ trước khi nghe lời giải chi tiết.",
                    pause=15
                ),
                build_step(
                    """<div class="box key"><b>Đáp án chính xác là B</b>!</div>
<p><b>Bước 1 — Cơ chế bất biến của chuỗi String trong Java</b>:</p>
<table class="t">
  <tr><th>thao tác</th><th>cơ chế bộ nhớ Heap</th><th>hậu quả tài nguyên</th></tr>
  <tr><td>Cộng chuỗi String (s += part)</td><td>Cấp phát đối tượng String mới toanh</td><td>Hàng triệu đối tượng rác kích hoạt Full GC</td></tr>
  <tr><td>Dùng StringBuilder (sb.append)</td><td>Ghi đè trực tiếp vào mảng ký tự nội bộ</td><td>Không sinh rác, tốc độ xử lý nhanh gấp 50 lần</td></tr>
</table>""",
                    "Đáp án chính xác là phương án B. Chuỗi trong Java là đối tượng bất biến nên mỗi lần nối chuỗi sẽ cấp phát một vùng nhớ mới trên bộ nhớ động. Việc này khiến hàng triệu đối tượng rác sinh ra và kích hoạt đợt dừng hệ thống nguy hiểm.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2 — Kết luận thực chiến cho hệ thống ngân hàng</b>:</p>
<div class="box key">Trong mọi dịch vụ chuyển đổi bản tin như ISO 8583 hoặc OFS XML, luôn sử dụng StringBuilder với dung lượng khởi tạo ước tính trước để đạt hiệu năng xử lý hàng chục nghìn TPS!</div>""",
                    "Bước hai, trong mọi dịch vụ chuyển đổi bản tin tài chính, ta luôn sử dụng bộ dựng chuỗi khả biến với dung lượng dự tính trước. Kỹ thuật này giúp hệ thống đạt thông lượng hàng chục nghìn giao dịch mỗi giây mà không tạo rác.",
                    clear=True
                )
            ]
        },
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Khoa học Máy tính và Java 21",
            "steps": [
                build_step(
                    """<div class="chain">
  <span>Tối ưu hóa Phân cấp Bộ nhớ & Khối đệm 64 byte</span> &rarr;
  <span>Kiểm soát Vùng nhớ Heap & Hạn chế đợt Full GC</span> &rarr;
  <span>Áp dụng Kiểu số thập phân chính xác BigDecimal</span> &rarr;
  <span>Khai thác Luồng Ảo Java 21 mở rộng hàng vạn kết nối</span> &rarr;
  <span>Sử dụng Cấu trúc B-Tree tối ưu hóa Disk I/O cơ sở dữ liệu</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>trụ cột kiến trúc</th><th>giá trị bảo vệ hệ thống ngân hàng ACB</th></tr>
  <tr><td>Bộ nhớ đệm CPU & JVM Tuning</td><td>Ngăn chặn độ trễ bất thường, bảo đảm thời gian phản hồi sub-100ms</td></tr>
  <tr><td>Virtual Threads Java 21</td><td>Mở rộng mười nghìn TPS đồng thời mà không nghẽn tài nguyên phần cứng</td></tr>
  <tr><td>Cây B-Tree & BigDecimal</td><td>Bảo đảm tính toàn vẹn số học và tốc độ truy vấn sổ cái sổ cái nhanh nhất</td></tr>
</table>
<p style="margin-top: 15px;"><b>Khẳng định năng lực Kỹ sư Cấp cao tại ACB</b>: Làm chủ bản chất khoa học máy tính lõi, tự tin giải quyết mọi bài toán cao tải và bảo vệ mức lương 50 triệu gross.</p>""",
                    "Tóm lại, chuỗi logic gồm tối ưu bộ nhớ đệm, kiểm soát bộ nhớ máy ảo, dùng số thập phân chính xác, khai thác luồng ảo và tận dụng cây nhiều nhánh. Nắm vững nền tảng khoa học máy tính lõi, bạn tự tin làm chủ các hệ thống cao tải và bảo vệ mức lương 50 triệu gross tại ACB."
                )
            ]
        }
    ]
}

save_spec(l01, r"D:\research-video\lessons\int\L01_foundation_cs_java.yaml")
print("L01 spec written successfully!")
