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

l00 = {
    "id": "L00",
    "course": "INT",
    "series": "Khung Chuẩn Phỏng vấn Kỹ sư Tích hợp Ngân hàng",
    "title": "Chuyên đề 0 — Lộ trình Năng lực Phỏng vấn Banking: Từ Con số 0 đến Deal Lương 50M Gross",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "interview/00_overview_roadmap.md; Khung chuẩn ACB Core Integration; ACM CS2023 Curriculum",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Định vị lộ trình thực chiến từ con số không và mất gốc đến kỹ sư ngân hàng cấp cao",
        "Nắm vững 5 tầng kiến trúc kỹ thuật: Java lõi, Microservices, Hệ phân tán, T24 và NAPAS",
        "Làm chủ chiến lược biến văn bằng AI trường UIT thành lợi thế cạnh tranh thương lượng lương 50 triệu gross"
    ],
    "scenes": [
        {
            "id": "hook",
            "kind": "hook",
            "title": "Khoảng cách thực tế giữa xem video lý thuyết và đỗ kỹ sư ngân hàng cấp cao",
            "steps": [
                build_step(
                    """<p>Một lập trình viên mới bắt đầu hoặc mất gốc tự hỏi liệu chỉ xem một chuỗi video ngắn có đủ sức đỗ kỹ sư tích hợp ngân hàng với mức lương 50 triệu gross hay không?</p>
<div class="box key">Câu trả lời thẳng thắn là không thể nếu chỉ học vẹt kiến thức bề mặt. Cần một lộ trình khổ luyện có hệ thống từ nền tảng máy tính đến nghiệp vụ tài chính chuyên sâu.</div>""",
                    "Chào bạn, nhiều bạn băn khoăn liệu chỉ xem vài chục phút video có đủ để trở thành kỹ sư ngân hàng cấp cao và thương lượng mức lương 50 triệu gross hay không. Câu trả lời trung thực là hoàn toàn không thể nếu bạn chỉ học vẹt mà thiếu nền tảng. Bài học này sẽ vạch rõ toàn bộ lộ trình năng lực giúp bạn nâng cao năng lực thực chất."
                ),
                build_step(
                    """<table class="t">
  <tr><th>tầng năng lực</th><th>nguy cơ nếu học vẹt</th><th>giải pháp chuẩn kỹ sư cấp cao</th></tr>
  <tr><td>Nền tảng máy tính</td><td>Bị đánh trượt khi hỏi về bộ nhớ đệm CPU</td><td>Nắm chắc 632 chuyên đề khoa học máy tính</td></tr>
  <tr><td>Hệ thống phân tán</td><td>Gây lỗi trừ tiền kép khi mạng bị ngắt</td><td>Làm chủ mô hình SAGA và khóa phân tán Redis</td></tr>
  <tr><td>Văn bằng đại học</td><td>Bị ép giá lương vì bằng trí tuệ nhân tạo</td><td>Biến văn bằng AI thành bộ nhân năng lực công nghệ</td></tr>
</table>
<p>Hôm nay, ta giải mã: <b>Kim tự tháp năng lực</b>, <b>nghiệp vụ ngân hàng lõi</b>, và <b>chiến lược phỏng vấn 50 triệu gross</b>.</p>""",
                    "Hôm nay, ta cùng nhau giải mã kim tự tháp năng lực toàn diện. Ta tìm hiểu cách kết nối nền tảng máy tính với hệ thống ngân hàng thực tế. Ta làm chủ quy trình nghiệp vụ cốt lõi không thể thay thế. Ta cũng xây dựng chiến lược biến tấm bằng đại học thành vũ khí đàm phán thu nhập xứng đáng.",
                    clear=True
                )
            ]
        },
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Đơn vị đo lường lưu lượng và độ trễ trong giao dịch ngân hàng",
            "checks": [
                "1000 * 50 == 50000",
                "100 // 10 == 10"
            ],
            "steps": [
                build_step(
                    """<p><b>Các chỉ số kỹ thuật đo lường hiệu năng cốt lõi</b>:</p>
<table class="t">
  <tr><th>chỉ số kỹ thuật</th><th>ý nghĩa trong ngân hàng</th><th>ngưỡng yêu cầu thực tế</th></tr>
  <tr><td>Giao dịch mỗi giây TPS</td><td>Số lượng bản tin tài chính xử lý đồng thời</td><td>Từ 5000 đến 50000 lệnh mỗi giây</td></tr>
  <tr><td>Độ trễ phản hồi Latency</td><td>Thời gian hoàn tất một yêu cầu thanh toán</td><td>Dưới 100 mili giây cho giao dịch thẻ</td></tr>
  <tr><td>Tính sẵn sàng Availability</td><td>Thời gian hệ thống hoạt động liên tục</td><td>Đạt chuẩn bốn số chín 99.99 phần trăm</td></tr>
</table>""",
                    "Trước tiên ta ôn lại các chỉ số hiệu năng cơ bản trong ngân hàng. Lưu lượng giao dịch mỗi giây phản ánh sức chịu tải của cổng tích hợp. Độ trễ phản hồi quyết định trải nghiệm thanh toán của khách hàng. Còn tính sẵn sàng bốn số chín bảo đảm hệ thống không bị gián đoạn hoạt động."
                ),
                build_step(
                    """<div class="box info">
  <h4>Phép tính lưu lượng đồng thời</h4>
  <p>Một cổng thanh toán xử lý 50000 giao dịch mỗi giây với thời gian phục vụ 10 mili giây.</p>
  <p class="math-block">50000 \\text{ TPS} \\times 10 \\text{ ms} = 500000 \\text{ req·ms}</p>
  <p>Số kết nối đồng thời trung bình luôn duy trì ở mức:</p>
  <p class="math-block">\\frac{50000 \\times 10}{1000} = 500 \\text{ kết nối song song}</p>
</div>""",
                    "Kỹ sư cấp cao luôn đo lường tải bằng con số cụ thể. Với 50000 giao dịch mỗi giây và độ trễ 10 mili giây, hệ thống phải duy trì ổn định 500 kết nối song song liên tục. Đây là cơ sở để cấu hình kích thước bể kết nối mạng.",
                    clear=True
                )
            ]
        },
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kim tự tháp năm tầng năng lực từ con số không đến Senior",
            "steps": [
                build_step(
                    """<p><b>Kiến trúc năm tầng năng lực của kỹ sư ngân hàng cấp cao</b>:</p>
<svg viewBox="0 0 700 240" style="width:100%;max-height:220px;">
  <polygon points="350,10 650,230 50,230" fill="#f0f7ff" stroke="#003366" stroke-width="2"/>
  <line x1="110" y1="185" x2="590" y2="185" stroke="#003366" stroke-width="1.5"/>
  <line x1="170" y1="140" x2="530" y2="140" stroke="#003366" stroke-width="1.5"/>
  <line x1="230" y1="95" x2="470" y2="95" stroke="#003366" stroke-width="1.5"/>
  <line x1="290" y1="55" x2="410" y2="55" stroke="#003366" stroke-width="1.5"/>
  <text x="350" y="42" font-size="12" font-weight="bold" fill="#003366" text-anchor="middle">TẦNG 5: AI MULTIPLIER &amp; DEAL 50M</text>
  <text x="350" y="80" font-size="12" font-weight="bold" fill="#003366" text-anchor="middle">TẦNG 4: NGHIỆP VỤ T24, NAPAS, SQUAD</text>
  <text x="350" y="122" font-size="12" font-weight="bold" fill="#003366" text-anchor="middle">TẦNG 3: HỆ PHÂN TÁN, SAGA, OUTBOX, KAFKA</text>
  <text x="350" y="167" font-size="12" font-weight="bold" fill="#003366" text-anchor="middle">TẦNG 2: MICROSERVICES, SPRING BOOT, REDIS</text>
  <text x="350" y="212" font-size="12" font-weight="bold" fill="#003366" text-anchor="middle">TẦNG 1: KHOA HỌC MÁY TÍNH, JAVA 21, JVM, B-TREE</text>
</svg>""",
                    "Quan sát kim tự tháp năng lực, bạn sẽ thấy lộ trình phát triển gồm 5 tầng rõ rệt. Tầng một là khoa học máy tính và Java lõi. Tầng hai là dịch vụ nhỏ và cơ sở dữ liệu. Tầng ba là hệ thống phân tán chịu lỗi. Tầng bốn là nghiệp vụ tài chính chuyên sâu. Và tầng đỉnh cao là bộ nhân công nghệ trí tuệ nhân tạo."
                ),
                build_step(
                    """<table class="t">
  <tr><th>tầng năng lực</th><th>hậu quả khi thiếu hụt</th><th>yêu cầu chuẩn mực</th></tr>
  <tr><td>Tầng 1 (Khoa học máy tính)</td><td>Nghẽn bộ nhớ đệm CPU, rò rỉ bộ nhớ Heap</td><td>Nắm chắc kiến trúc máy tính và JVM</td></tr>
  <tr><td>Tầng 3 (Hệ thống phân tán)</td><td>Trừ tiền kép, sai lệch sổ cái hạch toán</td><td>Làm chủ mô hình SAGA và Outbox</td></tr>
  <tr><td>Tầng 5 (Bộ nhân công nghệ)</td><td>Bị ép lương, thiếu điểm nhấn khác biệt</td><td>Ứng dụng AI tối ưu phân luồng hệ thống</td></tr>
</table>""",
                    "Các tầng năng lực có mối quan hệ phụ thuộc nhân quả chặt chẽ. Nếu thiếu nền tảng máy tính, bạn sẽ viết mã làm nghẽn bộ nhớ. Nếu thiếu kiến thức hệ phân tán, bạn sẽ làm mất mát tiền của khách hàng. Do đó người mới bắt đầu phải học tuần tự từng bước vững chắc.",
                    clear=True
                )
            ]
        },
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Công thức Giá trị Kinh doanh và Tỉ lệ Thu nhập Kỳ vọng",
            "steps": [
                build_step(
                    r"""<p><b>Công thức lượng hóa giá trị đóng góp của kỹ sư ngân hàng cấp cao</b>:</p>
<div class="box key">
$$\text{Giá trị kinh doanh: } V = B_{\text{tiet kiem}} + B_{\text{doanh thu}} - C_{\text{ha tang}}$$
$$\text{Thu nhập năm 50M: } S_{\text{nam}} = 50 \times 12 = 600\text{ triệu VNĐ}$$
$$\text{Tổng gói thu nhập ACB: } T_{\text{total}} = 600 + (50 \times 3) = 750\text{ triệu VNĐ}$$
</div>
<p>Trong đó $V$ là giá trị thặng dư tạo ra, $B$ là lợi ích kinh doanh, và $T_{\text{total}}$ là tổng gói thu nhập thực nhận.</p>""",
                    "Để bảo vệ mức lương 50 triệu gross, ta sử dụng công thức lượng hóa giá trị kinh doanh. Kỹ sư cấp cao phải chứng minh giá trị mình tạo ra vượt xa chi phí bỏ ra. Với mức lương cứng 50 triệu, thu nhập một năm là 600 triệu đồng. Cộng thêm 3 tháng thưởng kinh doanh, tổng thu nhập đạt 750 triệu đồng."
                ),
                build_step(
                    """<table class="t">
  <tr><th>nguyên tắc đàm phán</th><th>hành vi sai lầm</th><th>hành vi chuẩn mực</th></tr>
  <tr><td>Cơ sở xác định lương</td><td>Dựa vào nhu cầu chi tiêu cá nhân</td><td>Dựa vào giá trị giải quyết tắc nghẽn</td></tr>
  <tr><td>Bảo vệ năng lực</td><td>Nói lý thuyết suông</td><td>Dẫn chứng kiến trúc và số liệu cụ thể</td></tr>
  <tr><td>Văn bằng công nghệ</td><td>Tự ti vì học trái ngành</td><td>Khẳng định lợi thế thuật toán AI tối ưu</td></tr>
</table>""",
                    "Quy tắc vàng khi đàm phán lương là tuyệt đối không nói về nhu cầu chi tiêu cá nhân. Bạn phải định vị bản thân như một nhà giải quyết bài toán kinh doanh. Hãy lấy các giải pháp giảm thiểu rủi ro tài chính làm điểm tựa vững chắc để chốt mức thu nhập mong muốn.",
                    clear=True
                )
            ]
        },
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Bốn bước giải bài toán chống trừ tiền kép khi chuyển khoản",
            "checks": [
                "60000 // 60 == 1000",
                "120 - 60 == 60",
                "50000 > 10000",
                "60 > 30"
            ],
            "steps": [
                build_step(
                    """<p><b>Bài toán thực tế</b>: Khách hàng nhấn chuyển khoản 20 triệu đồng qua App ACB, mạng 4G bị chập chờn.</p>
<div class="step">Khách hàng nhấn nút chuyển 2 lần liên tiếp trong khoảng thời gian 500 mili giây.</div>
<p>Làm thế nào để hệ thống chỉ trừ tiền duy nhất một lần và phản hồi chính xác?</p>""",
                    "Ta xét bài toán kinh điển trong phỏng vấn kỹ sư ngân hàng. Khách hàng thực hiện chuyển 20 triệu đồng nhưng mạng viễn thông chập chờn. Khách hàng mất kiên nhẫn và nhấn nút chuyển hai lần liên tiếp. Hệ thống phải xử lý thế nào để chỉ trừ tiền đúng một lần duy nhất."
                ),
                build_step(
                    """<p><b>Bước 1: Thiết lập khóa phân tán Redis bằng lệnh nguyên tử</b>:</p>
<pre><code>// Sử dụng khóa duy nhất theo mã giao dịch của khách hàng
SET lock:transfer:TXN_998822 1 NX EX 60</code></pre>
<p>Yêu cầu đầu tiên chiếm được khóa thành công trong 60 giây. Yêu cầu thứ hai bị chặn ngay lập tức.</p>""",
                    "Bước một, cổng tích hợp sử dụng lệnh nguyên tử của Redis để tạo khóa phân tán theo mã giao dịch. Khóa này có hiệu lực trong 60 giây. Yêu cầu đầu tiên lấy được khóa sẽ đi tiếp, trong khi yêu cầu thứ hai bị chặn đứng ngay lập tức.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2: Kiểm tra bảng lịch sử giao dịch với khóa dòng bi quan</b>:</p>
<pre><code>SELECT status FROM payment_transactions 
WHERE idempotency_key = 'KEY_123' FOR UPDATE;</code></pre>
<p>Nếu bản ghi đã tồn tại ở trạng thái Đang xử lý hoặc Thành công, trả về kết quả cũ ngay lập tức.</p>""",
                    "Bước hai, dịch vụ truy vấn bảng thanh toán trong cơ sở dữ liệu với khóa dòng bi quan. Nếu mã giao dịch đã tồn tại, hệ thống lập tức hoàn trả trạng thái trước đó cho khách hàng mà không thực hiện lệnh trừ tiền lần hai.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 3: Gửi bản tin trừ tiền vào Core Banking T24 qua hàng đợi IBM MQ</b>:</p>
<div class="box ok">Bản tin mang mã định danh duy nhất. Core T24 kiểm tra số dư và hạch toán đúng một lần.</div>
<p><b>Bước 4: Giải phóng khóa phân tán và hoàn tất phản hồi</b>.</p>""",
                    "Bước ba, hệ thống gửi bản tin trừ tiền sang hệ thống ngân hàng lõi qua hàng đợi tin cậy với mã định danh không đổi. Sau khi có phản hồi, bước bốn sẽ giải phóng khóa phân tán và gửi thông báo thành công cho người dùng.",
                    clear=True
                )
            ]
        },
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: Đánh giá Năng lực Phản xạ Kiến trúc Phân tán",
            "checks": [
                "4 - 1 == 3",
                "50 > 30"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn</b>: Khi kết nối giữa cổng thanh toán và Core Banking T24 bị đứt giữa chừng, bạn chọn giải pháp nào?</p>
<table class="t">
  <tr><th>phương án</th><th>cách thức xử lý mạng</th><th>đánh giá an toàn tài chính</th></tr>
  <tr><td>Phương án A</td><td>Báo lỗi thất bại ngay lập tức</td><td>Rất nguy hiểm, dễ trừ tiền kép</td></tr>
  <tr><td>Phương án B</td><td>Treo trạng thái nghi ngờ, đối soát bù trừ</td><td>Chuẩn mực ngân hàng tuyệt đối</td></tr>
  <tr><td>Phương án C</td><td>Gửi lại lệnh liên tục tự động</td><td>Gây quá tải và treo sổ cái Core</td></tr>
</table>""",
                    "Mời bạn trả lời câu hỏi tình huống phỏng vấn cấp cao. Vì đường truyền mạng bị đứt đoạn bất ngờ nên ta chưa rõ giao dịch đã được hạch toán hay chưa. Do đó bạn sẽ lựa chọn cách xử lý nào để bảo đảm an toàn dữ liệu tuyệt đối."
                ),
                build_step(
                    """<p><b>Đáp án chính xác: Lựa chọn Phương án B</b></p>
<div class="box key">Nguyên lý ngân hàng: Mất kết nối mạng không đồng nghĩa với giao dịch thất bại. Bản tin có thể đã tới đích và trừ tiền thành công. Trả về thất bại sẽ dẫn tới trừ tiền kép nếu khách hàng chuyển lại. Bắt buộc treo trạng thái và đối soát bù trừ!</div>""",
                    "Đáp án chính xác là lựa chọn B. Trong hệ thống tài chính, mất kết nối mạng không có nghĩa là giao dịch đã thất bại. Hệ thống bắt buộc phải giữ trạng thái nghi ngờ và kích hoạt quy trình đối soát bù trừ để không làm thất thoát tiền.",
                    clear=True
                )
            ]
        },
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Nguy hiểm: Ngụy biện về văn bằng Trí tuệ Nhân tạo UIT",
            "steps": [
                build_step(
                    """<table class="t">
  <tr><th>cách trả lời</th><th>nội dung ứng viên nói</th><th>hậu quả đánh giá</th></tr>
  <tr><td>Ngụy biện sai lầm</td><td>Học AI khó xin việc nên chuyển sang làm backend</td><td>Bị đánh giá trái ngành, ép lương dưới 25 triệu</td></tr>
  <tr><td>Kỹ sư cấp cao</td><td>Văn bằng AI rèn luyện thuật toán tối ưu phân luồng</td><td>Định vị nhân tài công nghệ, deal lương 50 triệu</td></tr>
</table>""",
                    "Một sai lầm chết người của ứng viên là tự nhận mình làm trái ngành vì thị trường khó khăn. Câu trả lời này sẽ phá huỷ hoàn toàn hình ảnh chuyên nghiệp của bạn. Hội đồng tuyển dụng sẽ coi bạn là tay ngang và thẳng tay ép mức thu nhập xuống đáy."
                ),
                build_step(
                    """<div class="box ok">
  <h4>Cách trả lời chuẩn Kỹ sư Cấp cao</h4>
  <p><i>"Em chọn ngành AI tại UIT vì đây là đỉnh cao của khoa học máy tính và thuật toán. 38 học phần rèn luyện cho em tư duy giải quyết các bài toán tối ưu lưu lượng phức tạp. Em ứng dụng AI như một bộ nhân công nghệ giúp hệ thống ngân hàng chạy nhanh hơn và an toàn hơn."</i></p>
</div>""",
                    "Cách trả lời chuẩn mực là khẳng định ngành trí tuệ nhân tạo là đỉnh cao của khoa học máy tính. 38 học phần tại trường giúp bạn sở hữu tư duy giải thuật vượt trội. Bạn xem công nghệ này là lợi thế cạnh tranh để tối ưu hóa hệ thống ngân hàng phức tạp.",
                    clear=True
                )
            ]
        },
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán: Xác định Gói Thu nhập và Mức Lương Gross",
            "checks": [
                "50 * 12 == 600",
                "750 - 600 == 150",
                "150 // 50 == 3"
            ],
            "steps": [
                build_step(
                    """<p class="quiz-q">Câu hỏi: Một ứng viên deal thành công mức lương cứng 50 triệu gross mỗi tháng tại ACB. Với chính sách thưởng 3 tháng lương kinh doanh cuối năm, tổng thu nhập thực nhận trong 12 tháng làm việc là bao nhiêu?</p>
<div class="step">A: 600 triệu đồng một năm</div>
<div class="step">B: 700 triệu đồng một năm</div>
<div class="step">C: 750 triệu đồng một năm</div>""",
                    "Mời bạn tính toán gói thu nhập: Với mức lương 50 triệu gross một tháng và 3 tháng lương thưởng, tổng thu nhập hàng năm của bạn là bao nhiêu?",
                    pause=5
                ),
                build_step(
                    """<table class="t">
  <tr><th>thành phần thu nhập</th><th>công thức tính toán</th><th>giá trị quy đổi</th></tr>
  <tr><td>Lương cơ bản 12 tháng</td><td>50 triệu nhân 12 tháng</td><td>600 triệu đồng</td></tr>
  <tr><td>Thưởng kinh doanh 3 tháng</td><td>50 triệu nhân 3 tháng</td><td>150 triệu đồng</td></tr>
  <tr><td>Tổng gói thu nhập năm</td><td>600 triệu cộng 150 triệu</td><td>750 triệu đồng</td></tr>
</table>""",
                    "Bước một, ta lấy 50 triệu nhân 12 tháng để có 600 triệu lương cơ bản. Bước hai, ta cộng thêm 3 tháng lương thưởng tương đương 150 triệu đồng.",
                    clear=True
                ),
                build_step(
                    r"""<p><b>Đáp án chính xác: Lựa chọn C (750 triệu đồng)</b></p>
<div class="box key">
$$\text{Tổng thu nhập ACB: } T = 600 + 150 = 750\text{ triệu VNĐ}$$
<p>Mức thu nhập này phản ánh đúng giá trị của một kỹ sư tích hợp ngân hàng cấp cao có năng lực giải quyết sự cố phân tán và am hiểu nghiệp vụ T24.</p>
</div>""",
                    "Tổng thu nhập cả năm đạt 750 triệu đồng. Con số này hoàn toàn khả thi nếu bạn chứng minh được năng lực làm chủ hệ thống ngân hàng lõi và cổng chuyển mạch liên ngân hàng.",
                    clear=True
                )
            ]
        },
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tóm lược Chuỗi Logic Lột xác Năng lực Kỹ sư Ngân hàng",
            "steps": [
                build_step(
                    """<p><b>Chuỗi logic năm bước tiến hóa từ con số không đến Senior Banking 50M</b>:</p>
<div class="chain">
  <div class="node">1. Nền tảng khoa học máy tính và Java 21</div>
  <div class="arrow">↓</div>
  <div class="node">2. Kỹ nghệ Microservices và Spring Boot</div>
  <div class="arrow">↓</div>
  <div class="node">3. Hệ thống phân tán và mẫu SAGA Outbox</div>
  <div class="arrow">↓</div>
  <div class="node">4. Nghiệp vụ lõi T24 và Chuyển mạch NAPAS</div>
  <div class="arrow">↓</div>
  <div class="node">5. Bảo vệ văn bằng AI và deal lương 50M gross</div>
</div>""",
                    "Tóm lại, chuỗi tiến hóa năng lực của bạn phải trải qua đủ 5 bước mạch lạc. Từ nền tảng máy tính, qua kỹ nghệ dịch vụ nhỏ, đến hệ thống phân tán chịu lỗi. Tiếp đó là làm chủ nghiệp vụ ngân hàng lõi, và cuối cùng là bảo vệ giá trị để đạt mức lương 50 triệu gross. Chúc bạn kiên định trên con đường chinh phục đỉnh cao sự nghiệp."
                )
            ]
        }
    ]
}

with open(r"D:\research-video\lessons\int\L00_overview_zero_to_senior.yaml", "w", encoding="utf-8") as f:
    yaml.dump(l00, f, allow_unicode=True, sort_keys=False)
print("Saved L00_overview_zero_to_senior.yaml")
