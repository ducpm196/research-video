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
# LESSON 6: BỘ 100 CÂU HỎI PHỎNG VẤN THỰC CHIẾN SENIOR BANKING ACB
# =========================================================================
l06 = {
    "id": "L06",
    "course": "INT",
    "series": "Giáo trình Phỏng vấn Senior Banking ACB",
    "title": "Chuyên đề 6 — Bộ 100 Câu hỏi Phỏng vấn Thực chiến Senior Banking ACB",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "interview/06_interview_qa_bank_100.md; Ngân hàng câu hỏi tuyển dụng Khối Công nghệ Thông tin ACB 2026",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Làm chủ phản xạ 5 nhóm câu hỏi: Khoa học máy tính lõi, Microservices, Hệ phân tán, Nghiệp vụ T24 và Thiết kế hệ thống",
        "Nắm vững phương pháp trả lời đào sâu 5 tầng kỹ thuật và giải thích sự cố sản xuất thực tế",
        "Chứng minh phẩm chất Kỹ sư Cấp cao luôn đặt an toàn dòng tiền và tính toàn vẹn hệ thống lên hàng đầu"
    ],
    "scenes": [
        {
            "id": "hook",
            "kind": "hook",
            "title": "Nghệ thuật đối thoại kỹ thuật với Hội đồng Kiến trúc và Lãnh đạo Khối CNTT ACB",
            "steps": [
                build_step(
                    """<p>Hội đồng phỏng vấn Kỹ sư Cấp cao tại ACB không bao giờ hỏi các định nghĩa trắc nghiệm lý thuyết sách vở.</p>
<div class="box key">Họ sẽ liên tục xoáy sâu vào các điểm nghẽn cao tải, phân tích nguyên nhân sự cố sản xuất và chất vấn phương án kiến trúc. Làm thế nào để phản xạ tự nhiên và trả lời trôi chảy mọi câu hỏi khó nhất?</div>""",
                    "Chào bạn, buổi phỏng vấn Kỹ sư Cấp cao tại ngân hàng Á Châu là một cuộc đối thoại kỹ thuật chuyên sâu giữa các chuyên gia. Hội đồng tuyển dụng sẽ liên tục đào sâu vào các tình huống sự cố thực tế và thử thách bản lĩnh kiến trúc của bạn. Hôm nay, ta cùng nhau rèn luyện phản xạ sát thủ trước một trăm câu hỏi hóc búa nhất."
                ),
                build_step(
                    """<table class="t">
  <tr><th>nhóm câu hỏi</th><th>phạm vi chuyên môn</th><th>tiêu chuẩn phản xạ chuẩn Senior</th></tr>
  <tr><td>Phần 1: Khoa học máy tính</td><td>Bộ nhớ máy ảo, đa luồng và cấu trúc dữ liệu</td><td>Nắm chắc bản chất thanh ghi, cây B-Tree và luồng ảo</td></tr>
  <tr><td>Phần 2 & 3: Dịch vụ nhỏ & Phân tán</td><td>Quản lý giao dịch Spring, Kafka và Oracle</td><td>Mô hình SAGA, hộp thư sự kiện và triệt tiêu bế tắc</td></tr>
  <tr><td>Phần 4 & 5: Nghiệp vụ & Thiết kế</td><td>Core T24, NAPAS, tín dụng và kiến trúc 10k TPS</td><td>Bảo toàn dòng tiền và giải thích bằng số liệu định lượng</td></tr>
</table>
<p>Hôm nay, ta làm chủ: <b>Phương pháp trả lời đào sâu 5 tầng</b>, <b>thiết kế cổng thanh toán 10000 TPS</b>, và <b>bản lĩnh xử lý sự cố</b>.</p>""",
                    "Hôm nay, ta cùng nhau giải mã toàn bộ năm nhóm câu hỏi trọng điểm. Ta nắm vững phương pháp trả lời đào sâu năm tầng để thuyết phục hoàn toàn các kiến trúc sư trưởng. Ta học cách thiết kế hệ thống thanh toán mười nghìn giao dịch mỗi giây. Ta cũng tôi luyện bản lĩnh của người kỹ sư luôn đặt an toàn dòng tiền lên hàng đầu.",
                    clear=True
                )
            ]
        },
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Cấu trúc Bộ 100 Câu hỏi và Phương pháp Trả lời Đào sâu 5 Tầng",
            "checks": [
                "20 * 5 == 100",
                "100 // 10 == 10"
            ],
            "steps": [
                build_step(
                    """<p><b>Phương pháp trả lời Đào sâu 5 Tầng (5-Whys Deep Dive Methodology)</b>:</p>
<table class="t">
  <tr><th>tầng trả lời</th><th>nội dung bắt buộc</th><th>cách ghi điểm tuyệt đối</th></tr>
  <tr><td>Tầng 1: Định nghĩa</td><td>Khái niệm kỹ thuật ngắn gọn, súc tích</td><td>Nêu đúng bản chất trong 2 câu</td></tr>
  <tr><td>Tầng 2: Cơ chế ngầm</td><td>Nguyên lý hoạt động dưới tầng hệ điều hành hoặc máy ảo</td><td>Giải thích cơ chế bộ nhớ và dòng chảy dữ liệu</td></tr>
  <tr><td>Tầng 3: Tình huống biên</td><td>Các trường hợp mạng lỗi, bế tắc khóa hoặc quá hạn</td><td>Chỉ ra nguy cơ tiềm ẩn mà người khác bỏ qua</td></tr>
  <tr><td>Tầng 4: Sự cố thực tế</td><td>Câu chuyện từng xử lý thành công trên môi trường thật</td><td>Nêu bối cảnh, hành động và kết quả tại OCB</td></tr>
  <tr><td>Tầng 5: Số liệu đo lường</td><td>Thông số thông lượng, độ trễ và tỉ lệ sẵn sàng</td><td>Chứng minh bằng con số cụ thể mili giây và TPS</td></tr>
</table>""",
                    "Trước tiên ta ôn lại phương pháp trả lời năm tầng chuyên nghiệp. Khi nhận câu hỏi, bạn không chỉ nêu định nghĩa ngắn gọn mà phải giải thích tường tận cơ chế ngầm bên dưới. Tiếp theo, bạn nêu các trường hợp lỗi biên, dẫn chứng sự cố thực tế từng xử lý và chốt lại bằng số liệu đo lường thuyết phục."
                ),
                build_step(
                    """<div class="box key">Tư duy Kỹ sư Cấp cao thực thụ: Không phải là người viết những đoạn mã nguồn phức tạp nhất, mà là người luôn đặt tính an toàn và bảo toàn dòng tiền của khách hàng lên vị trí số một, dự báo trước mọi điểm lỗi và viết mã nguồn tự phục hồi!</div>""",
                    "Thước đo giá trị của một Kỹ sư Cấp cao nằm ở tư duy phòng ngừa rủi ro. Bạn luôn đặt an toàn vốn của ngân hàng lên hàng đầu, biết cách dự báo trước các điểm nghẽn và thiết kế hệ thống có khả năng tự phục hồi khi có biến cố xảy ra.",
                    clear=True
                )
            ]
        },
        {
            "id": "concept",
            "kind": "concept",
            "title": "Thiết kế Cổng Thanh toán Payment Hub 10,000 TPS cho ACB",
            "steps": [
                build_step(
                    """<p><b>Kiến trúc 4 Tầng Cổng Thanh toán Payment Hub 10,000 TPS</b>:</p>
<svg viewBox="0 0 700 220" style="width:100%;max-height:200px;">
  <rect x="20" y="20" width="660" height="40" rx="6" fill="#e8f4fd" stroke="#003366"/>
  <text x="30" y="45" font-size="12" font-weight="bold" fill="#003366">TẦNG 1: CỔNG VÀO (INGRESS) — Cụm API Gateway, Kiểm tra mTLS, Giới hạn tốc độ</text>
  <rect x="20" y="70" width="660" height="40" rx="6" fill="#d4edda" stroke="#28a745"/>
  <text x="30" y="95" font-size="12" font-weight="bold" fill="#155724">TẦNG 2: ĐIỀU PHỐI (ORCHESTRATION) — Java 21 Luồng Ảo, Máy trạng thái SAGA</text>
  <rect x="20" y="120" width="660" height="40" rx="6" fill="#fff3cd" stroke="#ffc107"/>
  <text x="30" y="145" font-size="12" font-weight="bold" fill="#856404">TẦNG 3: TRUYỀN DỮ LIỆU (STREAMING) — Apache Kafka cụm đôi, Hộp thư Outbox CDC</text>
  <rect x="20" y="170" width="660" height="40" rx="6" fill="#f8d7da" stroke="#dc3545"/>
  <text x="30" y="195" font-size="12" font-weight="bold" fill="#721c24">TẦNG 4: BỘ ĐIỀU HỢP (ADAPTERS) — Core T24 qua IBM MQ, Cổng NAPAS qua TCP Socket</text>
</svg>""",
                    "Khi được yêu cầu thiết kế cổng thanh toán mười nghìn giao dịch mỗi giây, ta vẽ ngay sơ đồ kiến trúc bốn tầng mạch lạc. Tầng cổng vào chịu trách nhiệm bảo mật và phân luồng. Tầng điều phối áp dụng luồng ảo Java 21. Tầng truyền dữ liệu dùng đường truyền sự kiện cụm đôi, và tầng điều hợp kết nối độc lập với ngân hàng lõi."
                ),
                build_step(
                    """<div class="box key">Chiến lược thời gian quá hạn phân tầng: Dịch vụ nội bộ ngân hàng (Core T24, thẻ) khống chế thời gian dưới 3 giây. Dịch vụ đối tác bên ngoài (Cổng CIC, thuế, điện thoại) đặt thời gian dưới 8 giây kết hợp cơ chế gọi lại bất đồng bộ để chống cạn kiệt tài nguyên!</div>""",
                    "Một điểm cộng lớn là việc thiết lập ma trận thời gian quá hạn phân tầng. Đối với các hệ thống nội bộ, ta khống chế thời gian phản hồi dưới ba giây. Đối với các đối tác ngoài mạng lưới, ta cho phép tối đa tám giây kết hợp cơ chế phản hồi bất đồng bộ để bảo vệ cổng giao tiếp.",
                    clear=True
                )
            ]
        },
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Ma trận Đo lường và Chỉ số SLA Vàng của Cổng Thanh toán",
            "checks": [
                "10000 // 100 == 100",
                "9999 // 100 == 99"
            ],
            "steps": [
                build_step(
                    r"""<p><b>Bốn Chỉ số Vàng Giám sát Hệ thống Thanh toán Ngân hàng</b>:</p>
<div class="box key">
$$\text{Thông lượng đỉnh (Throughput): } \text{TPS} \ge 10\,000\text{ giao dịch mỗi giây}$$
$$\text{Độ trễ trung bình (Latency): } T_{\text{avg}} \le 120\text{ mili giây}$$
$$\text{Tỉ lệ sẵn sàng (Availability): } A \ge 99.99\%\text{ (Downtime } < 52\text{ phút mỗi năm)}$$
$$\text{Tỉ lệ lỗi giao dịch (Error Rate): } E < 0.001\%$$
</div>""",
                    "Trong phần thi thiết kế hệ thống, ta luôn chứng minh bằng bốn chỉ số vàng đo lường. Hệ thống đạt thông lượng mười nghìn giao dịch mỗi giây với độ trễ phản hồi chỉ một trăm hai mươi mili giây. Độ sẵn sàng đạt bốn số chín, bảo đảm thời gian gián đoạn dưới năm mươi hai phút trong cả năm."
                ),
                build_step(
                    r"""<p><b>Quy tắc Phản biện Kiến trúc Microservices và Đơn khối Mô-đun</b>:</p>
<pre><code>// Nguyên tắc đánh đổi kiến trúc của Kỹ sư Cấp cao
if (domainComplexity == LOW && teamSize < 10) {
    chooseModularMonolith(); // Triển khai đơn khối mô-đun, tiết kiệm chi phí
} else {
    chooseMicroservicesWithSaga(); // Tách dịch vụ nhỏ khi lưu lượng bùng nổ
}</code></pre>""",
                    "Khi hội đồng hỏi về việc chọn kiến trúc dịch vụ nhỏ hay đơn khối, ta phản biện dựa trên phân tích chi phí lợi ích. Nếu nghiệp vụ ít biến động và đội ngũ tinh gọn, ta ưu tiên đơn khối dạng mô đun để giảm chi phí hạ tầng. Chỉ khi lưu lượng bùng nổ và các nhóm độc lập, ta mới tách dịch vụ nhỏ.",
                    clear=True
                )
            ]
        },
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Kể Câu chuyện Sự cố Sản xuất Thực tế tại OCB",
            "checks": [
                "3000 // 1000 == 3",
                "8000 // 1000 == 8",
                "100 - 90 == 10"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn kinh điển</b>: Hãy kể lại sự cố kỹ thuật nghiêm trọng nhất mà bạn từng trực tiếp điều tra và khắc phục trên môi trường thực tế?</p>
<ul>
  <li>Bối cảnh: Sự cố bế tắc khóa Oracle ORA-00060 ngày thanh toán lương 25 hàng tháng tại OCB.</li>
  <li>Lưu lượng: Tăng gấp 6 lần bình thường, hàng trăm luồng bị treo cứng, cổng API báo lỗi 504.</li>
  <li>Nhiệm vụ: Tìm ra nguyên nhân gốc rễ và khôi phục dịch vụ trong vòng 15 phút.</li>
</ul>""",
                    "Ta cùng thực hành câu trả lời cho câu hỏi phỏng vấn kinh điển về sự cố thực tế. Bối cảnh diễn ra vào ngày chi lương định kỳ tại ngân hàng cũ, lưu lượng tăng vọt gấp sáu lần bình thường khiến cổng thanh toán bị treo cứng. Đây là cơ hội vàng để chứng minh bản lĩnh của bạn."
                ),
                build_step(
                    """<p><b>Bước 1: Hành động ứng cứu tức thời và trích xuất tệp nhật ký vết</b>:</p>
<div class="box pit">Hành động: Không khởi động lại máy chủ một cách mù quáng! Tôi lập tức truy cập thư mục nhật ký cảnh báo của Oracle, trích xuất tệp vết chấm trc và đọc biểu đồ chu trình bế tắc khóa Deadlock Graph!</div>""",
                    "Bước một, người kỹ sư bản lĩnh không khởi động lại hệ thống một cách hoảng loạn. Bạn lập tức truy cập thư mục nhật ký chuyên dụng, trích xuất tệp vết và đọc biểu đồ chu trình bế tắc để định vị chính xác hai câu lệnh xung đột.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2: Tìm ra nguyên nhân gốc rễ trong 5 phút</b>:</p>
<pre><code>-- Phát hiện: Hai câu lệnh cập nhật số dư đảo ngược thứ tự tài khoản
-- Kết hợp việc bảng con lịch sử giao dịch bị thiếu chỉ mục khóa ngoại
CREATE INDEX idx_tx_history_fk 
ON transaction_history(account_no) ONLINE;</code></pre>
<div class="box key">Tạo chỉ mục trực tuyến ngay lập tức mà không cần khóa bảng, giải tỏa 80% áp lực khóa!</div>""",
                    "Bước hai, bạn chỉ ra nguyên nhân gốc rễ là việc khóa tài khoản lộn xộn kết hợp thiếu chỉ mục khóa ngoại trên bảng con. Bạn xử lý khẩn cấp bằng lệnh tạo chỉ mục trực tuyến mà không làm gián đoạn các phiên giao dịch đang chạy.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 3: Giải pháp lâu dài và kết quả đo lường thuyết phục</b>:</p>
<div class="box key">Viết lại thủ tục lưu trữ áp dụng sắp xếp tài khoản tăng dần trước khi khóa hàng. Kết quả: Triệt tiêu 100% lỗi bế tắc khóa, đưa thời gian phản hồi API từ 8 giây xuống còn 150 mili giây, bảo đảm SLA 99.99%!</div>""",
                    "Bước ba, bạn trình bày giải pháp lâu dài bằng thuật toán sắp xếp thứ tự tài khoản trước khi khóa hàng. Kết quả thực nghiệm triệt tiêu hoàn toàn lỗi bế tắc khóa và đưa thời gian phản hồi về mức một trăm năm mươi mili giây.",
                    clear=True
                )
            ]
        },
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: Cân bằng Giữa Bảo mật Sinh trắc học và Trải nghiệm Người dùng",
            "checks": [
                "4 * 25 == 100",
                "100 // 2 == 50"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn Senior</b>: Quyết định 2345 yêu cầu xác thực khuôn mặt cho mọi giao dịch trên 10 triệu đồng. Làm sao bạn bảo đảm tuân thủ pháp lý mà không làm khách hàng khó chịu vì độ trễ?</p>
<ul>
  <li>(A) Bắt buộc xác thực khuôn mặt cho mọi giao dịch kể cả một nghìn đồng.</li>
  <li>(B) Áp dụng cơ chế Xác thực theo mức độ rủi ro (Risk-Based Authentication): Giao dịch nhỏ và địa điểm quen thuộc chỉ cần xác thực nhẹ; chỉ kích hoạt sinh trắc học 3D khi số tiền trên 10 triệu hoặc xuất hiện hành vi bất thường.</li>
  <li>(C) Bỏ qua kiểm tra sinh trắc học để người dùng chuyển tiền cho nhanh.</li>
</ul>""",
                    "Mời bạn trả lời câu hỏi về cân bằng giữa an ninh bảo mật và trải nghiệm người dùng. Khi áp dụng quy định bắt buộc về sinh trắc học khuôn mặt của Ngân hàng Nhà nước, kỹ sư cấp cao sẽ thiết kế giải pháp như thế nào để giữ chân khách hàng."
                ),
                build_step(
                    """<p><b>Đáp án chính xác: Lựa chọn (B)</b></p>
<div class="box key">Giải thích vì: Cơ chế xác thực theo rủi ro kết hợp mô hình AI phát hiện điểm bất thường giúp phân loại giao dịch thông minh. Do đó 90% giao dịch nhỏ hàng ngày diễn ra mượt mà trong khi các giao dịch lớn trên 10 triệu được bảo vệ tuyệt đối theo đúng luật định!</div>""",
                    "Đáp án chính xác là lựa chọn B vì cơ chế xác thực theo mức độ rủi ro giúp phân loại giao dịch thông minh. Do đó các khoản chuyển tiền nhỏ diễn ra nhanh chóng, còn các giao dịch giá trị lớn vẫn được bảo vệ nghiêm ngặt theo đúng luật định.",
                    clear=True
                )
            ]
        },
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Nguy hiểm: Trả lời Lý thuyết Giáo điều mà Thiếu Dẫn chứng Thực tế",
            "steps": [
                build_step(
                    """<div class="box pit">Sai lầm lớn nhất khiến ứng viên bị đánh rớt vị trí Kỹ sư Cấp cao:</div>
<table class="t" style="margin-top: 10px;">
  <tr><th>cách trả lời non nớt</th><th>đánh giá của hội đồng tuyển dụng</th><th>cách sửa chuẩn Senior ACB</th></tr>
  <tr><td>Chỉ đọc thuộc lòng định nghĩa</td><td>Nghi ngờ ứng viên chỉ học vẹt trên mạng</td><td>Luôn gắn với dự án thực tế tại OCB và ACB</td></tr>
  <tr><td>Nói chung chung là hệ thống rất nhanh</td><td>Thiếu tư duy kỹ thuật định lượng</td><td>Nêu rõ thông số TPS, độ trễ ms và mã lỗi</td></tr>
</table>""",
                    "Sai lầm lớn nhất khiến ứng viên trượt phỏng vấn là việc trả lời lý thuyết chung chung mà không có số liệu đo lường. Hội đồng tuyển dụng cần nghe các trải nghiệm thực tế, các quyết định đánh đổi kiến trúc và những bài học xương máu trong sản xuất."
                )
            ]
        },
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán: Kế hoạch 90 Ngày Đầu tiên nếu Gia nhập ACB",
            "checks": [
                "30 + 30 == 60",
                "60 + 30 == 90"
            ],
            "steps": [
                build_step(
                    """<p><b>Câu hỏi trắc nghiệm của Giám đốc Khối CNTT</b>: Nếu được nhận vào ACB với mức đãi ngộ 50 triệu gross, kế hoạch hành động trong 90 ngày đầu tiên của bạn là gì?</p>
<ul>
  <li><b>A</b>: Đòi viết lại toàn bộ hệ thống cũ từ đầu bằng ngôn ngữ lập trình mới nhất.</li>
  <li><b>B</b>: 30 ngày đầu nắm vững kiến trúc hiện hữu và quy trình bảo mật; 60 ngày tiếp theo trực tiếp tối ưu hóa một phân hệ lõi; 90 ngày độc lập dẫn dắt dự án tích hợp mới và chuyển giao công nghệ.</li>
  <li><b>C</b>: Chỉ ngồi đợi đồng nghiệp giao việc gì thì làm việc đó.</li>
  <li><b>D</b>: Xin nghỉ phép dài ngày để làm quen môi trường mới.</li>
</ul>""",
                    "Xin mời bạn lựa chọn kế hoạch hành động chín mươi ngày đầu tiên khi gia nhập ngân hàng. Đây là câu hỏi quyết định bạn có được giao trọng trách lớn hay không. Bạn có 15 giây suy nghĩ trước khi nghe đáp án chuẩn.",
                    pause=15
                ),
                build_step(
                    """<div class="box key"><b>Đáp án chính xác là B</b>!</div>
<p><b>Bước 1 — Phân kỳ mục tiêu hành động rõ ràng</b>:</p>
<table class="t">
  <tr><th>giai đoạn</th><th>mục tiêu cốt lõi</th><th>kết quả bàn giao cụ thể</th></tr>
  <tr><td>30 ngày đầu</td><td>Hòa nhập và nắm vững kiến trúc</td><td>Lập bản đồ rủi ro các cổng tích hợp hiện hữu</td></tr>
  <tr><td>60 ngày</td><td>Tạo ra giá trị thực tế ngay</td><td>Trực tiếp tối ưu hóa bộ điều hợp Core T24 hoặc NAPAS</td></tr>
  <tr><td>90 ngày</td><td>Khẳng định vai trò dẫn dắt</td><td>Làm chủ dự án mới và tổ chức hội thảo chia sẻ nội bộ</td></tr>
</table>""",
                    "Đáp án chính xác là phương án B. Bạn chia lộ trình thành ba mốc ba mươi ngày rõ ràng. Tháng đầu tiên hòa nhập và nắm vững quy trình, tháng thứ hai tạo ra kết quả tối ưu thực tế, và tháng thứ ba độc lập dẫn dắt dự án trọng điểm.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2 — Khẳng định cam kết với Ban Lãnh đạo ACB</b>:</p>
<div class="box key">Một kế hoạch 90 ngày sắc sảo chứng minh bạn là nhân sự cấp cao vào để cống hiến và giải quyết vấn đề ngay lập tức, hoàn toàn xứng đáng với mức lương 50 triệu gross mỗi tháng!</div>""",
                    "Bước hai, một kế hoạch hành động cụ thể chứng minh bạn là một nhân sự vào để gánh vác trách nhiệm ngay lập tức mà không cần đào tạo lại. Điều này giúp lãnh đạo hoàn toàn an tâm khi phê duyệt mức đãi ngộ cao nhất cho bạn.",
                    clear=True
                )
            ]
        },
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Phỏng vấn Thực chiến Senior Banking",
            "steps": [
                build_step(
                    """<div class="chain">
  <span>Làm chủ 100 Câu hỏi Thực chiến theo Phương pháp 5 Tầng</span> &rarr;
  <span>Thiết kế Cổng Thanh toán 10000 TPS đạt Chuẩn 4 Số 9</span> &rarr;
  <span>Dẫn chứng Sự cố Sản xuất Thực tế và Số liệu Đo lường</span> &rarr;
  <span>Cân bằng Giữa Bảo mật Sinh trắc học và Trải nghiệm Người dùng</span> &rarr;
  <span>Xác lập Kế hoạch 90 Ngày tạo Giá trị Ngay Tuần Đầu tiên</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>trụ cột bản lĩnh</th><th>ấn tượng tạo ra trước Hội đồng Tuyển dụng ACB</th></tr>
  <tr><td>Phương pháp trả lời 5 tầng</td><td>Chứng minh năng lực am hiểu bản chất hệ thống từ phần cứng đến nghiệp vụ</td></tr>
  <tr><td>Thiết kế hệ thống lớn</td><td>Khẳng định tư duy kiến trúc phân tán chịu tải cao và phòng ngừa rủi ro</td></tr>
  <tr><td>Kế hoạch 90 ngày hành động</td><td>Xác lập vị thế nhân sự cấp cao vào là làm được việc ngay lập tức</td></tr>
</table>
<p style="margin-top: 15px;"><b>Tự tin chiến thắng trong phòng phỏng vấn ACB</b>: Nắm chắc vũ khí kỹ thuật, phản xạ sắc bén và bảo vệ trọn vẹn mức đãi ngộ 50 triệu gross.</p>""",
                    "Tóm lại, chuỗi logic gồm làm chủ một trăm câu hỏi, thiết kế hệ thống lớn và xác lập kế hoạch chín mươi ngày. Tự tin thể hiện bản lĩnh chuyên môn, bạn chắc chắn sẽ chinh phục hoàn toàn hội đồng tuyển dụng tại ACB."
                )
            ]
        }
    ]
}

save_spec(l06, r"D:\research-video\lessons\int\L06_interview_qa_bank_100.yaml")
print("L06 generated successfully!")

# =========================================================================
# LESSON 7: CHIẾN LƯỢC VÀ KỊCH BẢN ĐÀM PHÁN LƯƠNG 50M GROSS TẠI ACB
# =========================================================================
l07 = {
    "id": "L07",
    "course": "INT",
    "series": "Giáo trình Phỏng vấn Senior Banking ACB",
    "title": "Chuyên đề 7 — Chiến lược Đàm phán Lương 50 Triệu Gross",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "interview/07_salary_negotiation_50m_gross.md; Báo cáo thị trường lương Ngân hàng Việt Nam 2026; Kỹ thuật đàm phán nhân sự cấp cao",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Làm chủ ma trận định lượng giá trị và chứng minh lợi tức đầu tư 50 triệu gross cho ngân hàng",
        "Thuần thục kịch bản đối đáp 3 vòng: Sàng lọc nhân sự, hội đồng kỹ thuật và chốt đãi ngộ",
        "Hóa giải hoàn toàn các đòn ép giá về số năm kinh nghiệm và kiểm tra đối soát phúc lợi ngoài lương"
    ],
    "scenes": [
        {
            "id": "hook",
            "kind": "hook",
            "title": "Nghệ thuật Đàm phán Mức lương 50 Triệu Gross",
            "steps": [
                build_step(
                    """<p>Đa số kỹ sư đi phỏng vấn bị động chấp nhận mức lương do phòng nhân sự áp đặt theo khung thâm niên có sẵn.</p>
<div class="box key">Tại sao một kỹ sư có 3 năm thực chiến chuyên sâu ngân hàng lõi lại có thể tự tin deal mức lương 50 triệu gross tương đương 750 triệu một năm? Bí quyết nằm ở việc chuyển dịch cuộc đối thoại từ thời gian làm việc sang giá trị hoàn vốn đầu tư!</div>""",
                    "Chào bạn, nhiều kỹ sư tài năng thường ngập ngừng khi đàm phán mức lương vì bị rào cản số năm kinh nghiệm đè nặng. Trong mắt các ngân hàng lớn, giá trị của một Kỹ sư Cấp cao không đo bằng số tháng ngồi ở văn phòng, mà đo bằng quy mô rủi ro mà bạn có thể giải quyết. Hôm nay, ta cùng nhau giải mã chiến lược đàm phán chốt chắc mức lương năm mươi triệu gross."
                ),
                build_step(
                    """<table class="t">
  <tr><th>đối thoại thông thường</th><th>đối thoại chuyển dịch giá trị (Value Anchor)</th></tr>
  <tr><td>Em có 3 năm kinh nghiệm, mong muốn lương 40 triệu</td><td>Tôi chịu trách nhiệm an toàn cho cổng thanh toán hàng tỉ đồng</td></tr>
  <tr><td>Hỏi gì đáp nấy, phụ thuộc vào khung lương của HR</td><td>Chứng minh lợi tức đầu tư giúp ngân hàng tiết kiệm hàng tỉ đồng</td></tr>
  <tr><td>Bị ép giá do bằng cấp liên thông gần nhất</td><td>Khẳng định bằng AI là vũ khí cấp số nhân giải quyết bài toán khó</td></tr>
</table>
<p>Hôm nay, ta làm chủ: <b>Ma trận lợi tức đầu tư ROI</b>, <b>kịch bản đối đáp 3 vòng phỏng vấn</b>, và <b>nghệ thuật hóa giải đòn ép giá</b>.</p>""",
                    "Hôm nay, ta cùng nhau khám phá ba kỹ thuật đàm phán của nhân sự cấp cao. Ta tìm hiểu cách xây dựng ma trận lợi tức đầu tư để chứng minh giá trị vượt trội. Ta nắm vững kịch bản đối đáp chi tiết qua từng vòng tuyển dụng. Ta cũng làm chủ nghệ thuật phản biện thông minh trước mọi câu hỏi ép giá của phòng nhân sự.",
                    clear=True
                )
            ]
        },
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Căn cứ Tài chính và Ma trận Lợi tức Đầu tư ROI",
            "checks": [
                "50000000 * 12 == 600000000",
                "50 - 42 == 8"
            ],
            "steps": [
                build_step(
                    """<p><b>Ma trận So sánh Chi phí Tuyển dụng và Giá trị Bảo vệ Tài sản</b>:</p>
<table class="t">
  <tr><th>chi phí ngân hàng chi trả (50M Gross)</th><th>giá trị Kỹ sư Cấp cao mang lại cho ACB</th></tr>
  <tr><td>Lương cơ bản: 600 triệu đồng một năm</td><td>Ngăn chặn 1 sự cố sập Core T24: Tránh thiệt hại 2 đến 5 tỉ đồng</td></tr>
  <tr><td>Thưởng và phụ cấp: 150 triệu đồng một năm</td><td>Tối ưu hóa cước tin nhắn đa kênh: Tiết kiệm 1.2 tỉ đồng một năm</td></tr>
  <tr><td>Chi phí bảo hiểm và trang thiết bị máy trạm</td><td>Gánh vác dự án ngay tuần đầu: Tiết kiệm 300 triệu tiền đào tạo lại</td></tr>
</table>""",
                    "Trước tiên ta ôn lại bài toán tài chính từ góc nhìn của ban điều hành ngân hàng. Chi phí trả mức lương năm mươi triệu gross tương đương khoảng bảy trăm năm mươi triệu một năm. Nhưng một kỹ sư giỏi có thể ngăn ngừa sự cố sập hệ thống trị giá hàng tỉ đồng và tiết kiệm hàng trăm triệu chi phí đào tạo lại."
                ),
                build_step(
                    """<div class="box key">Quy tắc vàng ở vòng sàng lọc hồ sơ: Tuyệt đối không bao giờ khai báo mức lương cơ bản thấp! Ta luôn neo giá trị vào Tổng thu nhập thực tế bao gồm phụ cấp kỹ thuật cao tải và các kỳ thưởng hiệu quả kinh doanh!</div>""",
                    "Nguyên tắc cốt tử ngay từ vòng đầu tiên là không bao giờ khai mức lương cứng đơn thuần. Bạn luôn phải neo giá trị vào tổng thu nhập thực tế bao gồm các khoản phụ cấp trách nhiệm và thưởng kinh doanh để mở rộng dư địa đàm phán.",
                    clear=True
                )
            ]
        },
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kịch bản Đối thoại Chi tiết Qua Ba Vòng Tuyển dụng ACB",
            "steps": [
                build_step(
                    """<p><b>Quy trình Đàm phán 3 Vòng Tuyển dụng tại ACB</b>:</p>
<svg viewBox="0 0 700 220" style="width:100%;max-height:200px;">
  <rect x="20" y="30" width="200" height="160" rx="8" fill="#e8f4fd" stroke="#003366" stroke-width="2"/>
  <text x="30" y="55" font-size="13" font-weight="bold" fill="#003366">VÒNG 1: HR SÀNG LỌC</text>
  <text x="30" y="85" font-size="11" fill="#333">Hỏi mức thu nhập hiện tại</text>
  <text x="30" y="110" font-size="11" fill="#006699">Neo Total Comp 40-42M</text>
  <text x="30" y="135" font-size="11" fill="#555">Kỳ vọng 50M xứng tầm</text>
  <text x="30" y="160" font-size="11" fill="#555">Nhấn mạnh làm được việc ngay</text>
  <rect x="250" y="30" width="200" height="160" rx="8" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="260" y="55" font-size="13" font-weight="bold" fill="#155724">VÒNG 2: HỘI ĐỒNG KỸ THUẬT</text>
  <text x="260" y="85" font-size="11" fill="#333">Hỏi tại sao đáng giá 50M</text>
  <text x="260" y="110" font-size="11" fill="#28a745">Thực chiến T24 & NAPAS</text>
  <text x="260" y="135" font-size="11" fill="#555">Khử Deadlock Oracle</text>
  <text x="260" y="160" font-size="11" fill="#555">Bằng Cử nhân AI UIT</text>
  <rect x="480" y="30" width="200" height="160" rx="8" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
  <text x="490" y="55" font-size="13" font-weight="bold" fill="#856404">VÒNG 3: TRƯỞNG PHÒNG HR</text>
  <text x="490" y="85" font-size="11" fill="#333">HR ép giá mức 42 triệu</text>
  <text x="490" y="110" font-size="11" fill="#d39e00">Đối ứng kiên định giá trị</text>
  <text x="490" y="135" font-size="11" fill="#555">Đề xuất phụ cấp kỹ thuật</text>
  <text x="490" y="160" font-size="11" fill="#555">Cam kết KPI thử việc</text>
</svg>""",
                    "Quy trình đàm phán trải qua ba vòng độc lập. Ở vòng một, bạn khéo léo neo giá trị vào tổng thu nhập bốn mươi hai triệu và đề xuất mức kỳ vọng năm mươi triệu. Ở vòng hai, bạn dùng chuyên môn thực chiến thuyết phục hội đồng kỹ thuật. Ở vòng ba, bạn giữ vững lập trường kiên định để chốt thỏa thuận có lợi nhất."
                ),
                build_step(
                    """<div class="box key">Chiến thuật Đối ứng Kiên định Firm Counter-Offer: Khi phòng nhân sự đề xuất mức 42 triệu do vướng khung kinh nghiệm, ta không vội đồng ý mà đưa ra đề xuất cấu trúc linh hoạt: 46 triệu lương cứng cộng 4 triệu phụ cấp kỹ thuật cao tải, hoặc cam kết KPI cụ thể trong 6 tháng thử việc!</div>""",
                    "Khi nhận đề xuất thấp hơn kỳ vọng, kỹ sư thông minh không từ chối gay gắt mà áp dụng kỹ thuật đối ứng kiên định. Bạn có thể đề xuất tách một phần thành phụ cấp trách nhiệm hệ thống cao tải, hoặc gắn liền với cam kết hiệu quả thử việc để tháo gỡ vướng mắc cho phòng nhân sự.",
                    clear=True
                )
            ]
        },
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Công thức Định dạng Thu nhập và Cấu trúc Gói Đãi ngộ Toàn diện",
            "checks": [
                "46000000 + 4000000 == 50000000",
                "600000000 + 150000000 == 750000000"
            ],
            "steps": [
                build_step(
                    r"""<p><b>Ba Cấu trúc Đề xuất Linh hoạt để Đạt mục tiêu 50M Gross</b>:</p>
<div class="box key">
$$\text{Phương án A (Chuẩn): } 50\,000\,000\text{ VND Gross mỗi tháng}$$
$$\text{Phương án B (Linh hoạt): } 46\,000\,000\text{ Lương cứng} + 4\,000\,000\text{ Phụ cấp cao tải}$$
$$\text{Phương án C (Thử thách): } 50\,000\,000\text{ Gross đi kèm cam kết KPI tối ưu T24}$$
</div>
<p>Tổng thu nhập năm tương đương từ 700 đến 850 triệu đồng bao gồm 13 đến 15 tháng lương và thưởng hiệu quả kinh doanh!</p>""",
                    "Ta chuẩn bị sẵn ba phương án linh hoạt để chốt mức đãi ngộ mong muốn. Nếu ngân hàng gặp rào cản về thang bảng lương cứng, phương án kết hợp phụ cấp chuyên môn hoặc cam kết hiệu quả kinh doanh sẽ giúp giải quyết nút thắt cho cả hai bên."
                ),
                build_step(
                    r"""<p><b>Danh mục 4 Phúc lợi Ngoài lương Bắt buộc phải Đối soát</b>:</p>
<div class="box ok">
<p>1. Tháng lương 13 cố định + Thưởng kinh doanh KPI (2 đến 4 tháng lương)</p>
<p>2. Gói bảo hiểm sức khoẻ cao cấp PVI Care riêng cho cấp Senior</p>
<p>3. Cấp phát máy trạm hiệu năng cao phục vụ lập trình</p>
<p>4. Tài trợ 100% lệ phí thi chứng chỉ quốc tế Oracle và Confluent</p>
</div>""",
                    "Ngoài tiền lương hàng tháng, bạn cần kiểm tra kỹ bốn chế độ phúc lợi kèm theo. Tháng lương thứ mười ba, các kỳ thưởng hiệu quả kinh doanh, gói bảo hiểm chăm sóc sức khoẻ cao cấp và ngân sách thi chứng chỉ quốc tế là những quyền lợi không thể bỏ qua.",
                    clear=True
                )
            ]
        },
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Bẻ gãy Ba Đòn Ép giá Kinh điển của Tuyển dụng",
            "checks": [
                "15 - 12 == 3",
                "50000000 * 15 == 750000000",
                "50 - 45 == 5"
            ],
            "steps": [
                build_step(
                    """<p><b>Đòn ép giá số 1: Thị trường năm nay các ngân hàng đều thắt chặt ngân sách tuyển dụng</b></p>
<div class="box pit">Tâm lý nhân sự: Tạo áp lực khan hiếm cơ hội việc làm để ép ứng viên hạ thấp mức kỳ vọng lương.</div>
<div class="box key">Lời đáp trả chuẩn mực: Dạ em rất hiểu ngân hàng đang tối ưu hóa chi phí vận hành. Chính vì vậy, việc tuyển một Kỹ sư Cấp cao có thể làm chủ hệ thống ngay tuần đầu tiên, không tốn chi phí sai sót hay chi phí đào tạo lại là giải pháp tiết kiệm ngân sách hiệu quả nhất cho ACB!</div>""",
                    "Khi phòng nhân sự nói thị trường thắt chặt ngân sách, bạn đảo ngược tình thế bằng cách chứng minh tuyển kỹ sư làm được việc ngay là tiết kiệm nhất. Ngân hàng sẽ không mất chi phí sửa chữa sai sót và không tốn nhiều tháng đào tạo lại."
                ),
                build_step(
                    """<p><b>Đòn ép giá số 2: Bạn mới tốt nghiệp bằng Cử nhân AI tại UIT, liệu có quá sớm để nhận mức 50 triệu?</b></p>
<table class="t" style="margin-bottom: 8px;">
  <tr><th>yếu tố đánh giá</th><th>góc nhìn của nhân sự</th><th>thực tế năng lực của ứng viên</th></tr>
  <tr><td>Bằng Cử nhân AI UIT</td><td>Mới nhận bằng năm 2026</td><td>Mảnh ghép học thuật bổ trợ cho 6 năm thực chiến</td></tr>
  <tr><td>Kinh nghiệm công tác</td><td>Nghi ngờ thời gian làm việc</td><td>Hơn 6 năm liên tục tại FPT, Sutrix, Mirae Asset và OCB</td></tr>
</table>
<div class="box key">Lời đáp trả chuẩn mực: Dạ em đã có hơn 6 năm liên tục làm việc với các hệ thống lớn từ FPT, Sutrix, Mirae Asset đến ngân hàng OCB. Bằng Cử nhân AI tại UIT là vũ khí học thuật em trang bị thêm để giải quyết các bài toán cao tải và gian lận, chứ không phải em là người mới vào nghề!</div>""",
                    "Khi người phỏng vấn vin vào bằng cấp đại học mới tốt nghiệp, bạn làm rõ quá trình sáu năm công tác liên tục tại các tập đoàn công nghệ lớn. Tấm bằng đại học là mảnh ghép học thuật cao cấp bổ trợ cho kinh nghiệm dày dặn chứ không phản ánh thâm niên của bạn.",
                    clear=True
                ),
                build_step(
                    """<p><b>Đòn ép giá số 3: Nếu bạn nhận mức 45 triệu, ngân hàng sẽ bù đắp bằng các kỳ thưởng cuối năm rất cao</b></p>
<div class="box pit">Tâm lý nhân sự: Dịch chuyển rủi ro tài chính sang ứng viên vì tiền thưởng phụ thuộc vào kết quả kinh doanh chung.</div>
<div class="box key">Lời đáp trả chuẩn mực: Dạ em rất trân trọng chế độ thưởng hấp dẫn của ACB. Tuy nhiên, mức lương cứng 50 triệu là thước đo cam kết trách nhiệm và sự công nhận năng lực thực tế, giúp em dốc trọn một trăm phần trăm tâm huyết cho các bài toán công nghệ lớn của ngân hàng!</div>""",
                    "Khi nhà tuyển dụng đề xuất hạ lương cứng để bù bằng tiền thưởng, bạn lịch thiệp khẳng định mức lương hàng tháng là thước đo cam kết năng lực. Mức thu nhập ổn định giúp bạn toàn tâm toàn ý cống hiến cho các dự án huyết mạch của ngân hàng.",
                    clear=True
                ),
                build_step(
                    """<p><b>Kết quả sau 3 vòng đối thoại chuẩn mực tại ACB</b>:</p>
<div class="box key">Ban Nhân sự phê duyệt mức ngoại lệ: 50,000,000 VND Gross/tháng đi kèm gói phúc lợi Chuyên viên chính. Tổng thu nhập năm đạt 750 triệu đồng, chính thức gia nhập đội ngũ Kỹ sư Tích hợp Cấp cao!</div>""",
                    "Sau ba vòng đối thoại đĩnh đạc và thuyết phục, hội đồng nhân sự sẽ đồng thuận phê duyệt mức đãi ngộ ngoại lệ cho bạn. Bạn chính thức bước vào hàng ngũ kỹ sư cấp cao với mức lương năm mươi triệu gross hoàn toàn xứng đáng.",
                    clear=True
                )
            ]
        },
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: Bản lĩnh Giữ vững Mức lương Kỳ vọng",
            "checks": [
                "750 // 15 == 50",
                "600 // 12 == 50"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn Offer</b>: Trưởng phòng tuyển dụng gọi điện: ACB rất ấn tượng với chuyên môn của bạn nhưng theo khung chính sách thâm niên 3 năm, ngân hàng chỉ duyệt tối đa 42 triệu gross. Bạn có đồng ý nhận thư mời nhận việc không?</p>
<table class="t" style="margin-bottom: 8px;">
  <tr><th>phương án</th><th>mức lương gross</th><th>giải pháp tháo gỡ chính sách</th></tr>
  <tr><td>Đề xuất nhân sự</td><td>42 triệu</td><td>Bị ép theo khung thâm niên cứng</td></tr>
  <tr><td>Đề xuất ứng viên</td><td>46 triệu + 4 triệu phụ cấp</td><td>Gỡ nút thắt chính sách, bảo đảm mục tiêu 50 triệu</td></tr>
</table>
<ul>
  <li>(A) Vội vàng đồng ý ngay vì sợ bị huỷ bỏ lời mời làm việc.</li>
  <li>(B) Lịch sự bày tỏ sự trân trọng, tái khẳng định giá trị có thể tạo ra ngay tuần đầu tiên, và kiên định đề xuất cấu trúc 46 triệu cứng cộng 4 triệu phụ cấp hoặc cam kết KPI để đạt mục tiêu 50 triệu.</li>
  <li>(C) Bực tức và cúp máy ngay lập tức.</li>
</ul>""",
                    "Mời bạn thử sức với tình huống chốt thư mời làm việc thực tế. Khi người đứng đầu phòng tuyển dụng thông báo mức lương thấp hơn kỳ vọng do vướng chính sách, ứng viên xuất sắc sẽ xử lý khéo léo ra sao."
                ),
                build_step(
                    """<p><b>Đáp án chính xác: Lựa chọn (B)</b></p>
<div class="box key">Giải thích vì: Ngân hàng đã mất nhiều công sức phỏng vấn và rất muốn tuyển bạn. Việc bạn đưa ra giải pháp cấu trúc linh hoạt giúp người quản lý nhân sự có căn cứ hợp lý để giải trình với ban tổng giám đốc phê duyệt trường hợp đặc cách!</div>""",
                    "Đáp án chính xác là lựa chọn B vì nhà tuyển dụng đã rất muốn có bạn sau nhiều vòng kiểm tra. Do đó việc bạn đề xuất giải pháp linh hoạt sẽ giúp họ có cơ sở để xin phê duyệt đặc cách mức ngân sách cao nhất.",
                    clear=True
                )
            ]
        },
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Nguy hiểm: Khai báo Lương Thấp ở Vòng Sơ loại",
            "steps": [
                build_step(
                    """<div class="box pit">Cạm bẫy tâm lý tai hại nhất của ứng viên:</div>
<table class="t" style="margin-top: 10px;">
  <tr><th>sai lầm sơ loại</th><th>hậu quả đàm phán</th><th>chiến thuật khắc phục</th></tr>
  <tr><td>Khai mức lương cũ 25 triệu</td><td>Bị trói chặt mức tăng tối đa 20% đến 30%</td><td>Luôn nói về Tổng thu nhập 40 đến 42 triệu</td></tr>
  <tr><td>Nói lương bao nhiêu cũng được</td><td>Bị đánh giá là thiếu tự tin và non kinh nghiệm</td><td>Xác lập con số kỳ vọng 50 triệu dứt khoát</td></tr>
</table>""",
                    "Cạm bẫy lớn nhất là việc khai báo mức lương cơ bản cũ quá thấp ở vòng sơ loại. Nếu bạn khai lương cũ thấp, phòng nhân sự sẽ tự động áp mức trần tăng trưởng thông thường và không bao giờ đồng ý mức lương năm mươi triệu."
                )
            ]
        },
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán: Phân tích Tổng Thu nhập Năm Thực nhận",
            "checks": [
                "50 * 15 == 750",
                "750 - 600 == 150"
            ],
            "steps": [
                build_step(
                    """<p><b>Câu hỏi trắc nghiệm tài chính cá nhân</b>: Với mức lương 50 triệu gross tại ACB đi kèm chế độ 13 tháng lương cố định và 2 tháng thưởng hiệu quả kinh doanh, tổng thu nhập trước thuế trong năm của bạn là bao nhiêu?</p>
<ul>
  <li><b>A</b>: Đúng 600 triệu đồng tròn.</li>
  <li><b>B</b>: 750 triệu đồng mỗi năm (tương đương 15 tháng lương).</li>
  <li><b>C</b>: 500 triệu đồng.</li>
  <li><b>D</b>: 1 tỉ đồng.</li>
</ul>""",
                    "Xin mời bạn tính toán nhanh tổng thu nhập năm thực tế khi đạt mức lương kỳ vọng tại ngân hàng. Bạn có 15 giây suy nghĩ trước khi nghe công thức tính toán chuẩn mực.",
                    pause=15
                ),
                build_step(
                    """<div class="box key"><b>Đáp án chính xác là B</b>!</div>
<p><b>Bước 1 — Bóc tách cấu trúc thu nhập cả năm</b>:</p>
<table class="t">
  <tr><th>khoản thu nhập</th><th>công thức tính toán</th><th>tổng số tiền thực nhận</th></tr>
  <tr><td>Lương 12 tháng</td><td>50 triệu nhân 12 tháng</td><td>600 triệu đồng</td></tr>
  <tr><td>Lương tháng 13 & Thưởng KPI</td><td>50 triệu nhân 3 tháng</td><td>150 triệu đồng</td></tr>
  <tr><td>Tổng thu nhập năm</td><td>600 triệu cộng 150 triệu</td><td>750 triệu đồng một năm</td></tr>
</table>""",
                    "Đáp án chính xác là phương án B. Mức lương năm mươi triệu nhân với mười lăm tháng lương thực tế mang lại tổng thu nhập bảy trăm năm mươi triệu đồng một năm. Đây là mức đãi ngộ mơ ước khẳng định vị thế vững chắc của bạn trong ngành tài chính.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2 — Giá trị tự hào của Kỹ sư Tích hợp Ngân hàng</b>:</p>
<div class="box key">Mức thu nhập 750 triệu đồng mỗi năm là sự đền đáp xứng đáng cho những đêm miệt mài trực sự cố, những dòng lệnh tối ưu hóa chuẩn xác và bản lĩnh làm chủ các cổng giao dịch huyết mạch của quốc gia!</div>""",
                    "Bước hai, mức thu nhập này là sự ghi nhận xứng đáng cho những nỗ lực học tập và cống hiến không ngừng nghỉ. Bạn hoàn toàn có quyền tự hào về năng lực chuyên môn và bước tiến vững chắc trong sự nghiệp của mình.",
                    clear=True
                )
            ]
        },
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Chiến lược Đàm phán 50M Gross",
            "steps": [
                build_step(
                    """<div class="chain">
  <span>Dịch chuyển Cuộc đối thoại sang Lợi tức Đầu tư ROI</span> &rarr;
  <span>Neo Giá trị vào Tổng thu nhập Total Comp ở Vòng 1</span> &rarr;
  <span>Chứng minh Vũ khí Cấp số nhân Cử nhân AI ở Vòng 2</span> &rarr;
  <span>Đưa ra Đề xuất Đối ứng Kiên định Firm Counter-Offer</span> &rarr;
  <span>Kiểm tra Toàn diện 4 Quyền lợi Phúc lợi Ngoài lương</span>
</div>""",
                    "Tóm lại, chuỗi logic gồm dịch chuyển sang lợi tức đầu tư, neo tổng thu nhập và đối ứng kiên định."
                ),
                build_step(
                    """<table class="t">
  <tr><th>nguyên tắc đàm phán</th><th>hành vi thực hiện</th><th>kết quả đạt được</th></tr>
  <tr><td>Tự tin về giá trị</td><td>Nói bằng ngôn ngữ bảo vệ tài sản và số liệu đo lường</td><td>Xóa bỏ định kiến về số năm thâm niên</td></tr>
  <tr><td>Linh hoạt về cấu trúc</td><td>Sẵn sàng đề xuất phụ cấp kỹ thuật và cam kết KPI</td><td>Gỡ nút thắt chính sách cho phòng nhân sự</td></tr>
  <tr><td>Kiên định với mục tiêu</td><td>Không hạ thấp giá trị bản thân trước các đòn ép giá</td><td>Chốt vững mức lương 50 triệu gross tại ACB</td></tr>
</table>
<p style="margin-top: 15px;"><b>Chúc mừng bạn làm chủ trọn vẹn các chuyên đề</b>: Tự tin bước vào phòng phỏng vấn, khẳng định đẳng cấp Kỹ sư Cấp cao và chạm tay vào mức thu nhập mơ ước!</p>""",
                    "Chúc bạn tự tin bước vào phòng phỏng vấn, khẳng định đẳng cấp Kỹ sư Cấp cao và chạm tay vào mức lương mơ ước tại ACB.",
                    clear=True
                )
            ]
        }
    ]
}

save_spec(l07, r"D:\research-video\lessons\int\L07_salary_negotiation_50m_gross.yaml")
print("L07 generated successfully!")
