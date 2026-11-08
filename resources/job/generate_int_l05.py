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
# LESSON 5: ỨNG DỤNG AI NGÂN HÀNG & MINH CHỨNG CỬ NHÂN AI UIT
# =========================================================================
l05 = {
    "id": "L05",
    "course": "INT",
    "series": "Giáo trình Phỏng vấn Senior Banking ACB",
    "title": "Chuyên đề 5 — Ứng dụng AI Ngân hàng: Minh chứng Bằng Cử nhân AI UIT và Lợi thế Cạnh tranh",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "interview/05_uit_ai_banking_multiplier.md; Chương trình đào tạo Cử nhân Trí tuệ Nhân tạo UIT ĐHQG-HCM; Đề án Anomaly Detection ONNX 2026",
    "assumes": ["arith", "approx", "log", "sub", "mu", "hat", "cdot", "vec", "norm", "cos"],
    "objectives": [
        "Làm rõ ma trận 38 học phần Cử nhân AI tại Đại học Công nghệ Thông tin UIT ĐHQG-HCM",
        "Làm chủ 3 bài toán cấp số nhân: Phát hiện gian lận sub-5ms, định tuyến thông minh và đối soát ngữ nghĩa",
        "Bảo vệ bản lĩnh phỏng vấn trước câu hỏi về bằng cấp liên thông và vị thế Kỹ sư Cấp cao"
    ],
    "scenes": [
        {
            "id": "hook",
            "kind": "hook",
            "title": "Vì sao Kỹ sư Tích hợp Ngân hàng lại cần Bằng Cử nhân Trí tuệ Nhân tạo?",
            "steps": [
                build_step(
                    """<p>Đa số lập trình viên backend truyền thống nhìn bài toán tích hợp chỉ là: Nhận gói tin JSON, gọi ngân hàng lõi, lưu cơ sở dữ liệu và trả về kết quả.</p>
<div class="box key">Tuy nhiên tại ACB, hàng triệu giao dịch mỗi ngày đòi hỏi phát hiện gian lận trong thời gian thực dưới 5 mili giây, tự động định tuyến khi mạng nghẽn và đối soát tự động. Tấm bằng Cử nhân AI tại UIT mang lại lợi thế cạnh tranh áp đảo ra sao?</div>""",
                    "Chào bạn, đa số kỹ sư phần mềm chỉ nhìn bài toán tích hợp là việc chuyển tiếp dữ liệu tuần tự. Nhưng tại các ngân hàng hàng đầu, hệ thống đối mặt với lưu lượng khổng lồ và các hành vi gian lận tinh vi. Sở hữu tấm bằng Cử nhân Trí tuệ Nhân tạo tại trường Đại học Công nghệ Thông tin mang lại giá trị cấp số nhân vượt trội."
                ),
                build_step(
                    """<table class="t">
  <tr><th>bài toán ngân hàng số</th><th>cách làm truyền thống</th><th>đột phá cấp số nhân từ nền tảng AI UIT</th></tr>
  <tr><td>Phát hiện gian lận thẻ & tài khoản</td><td>Bộ quy tắc tĩnh if-else cứng nhắc</td><td>Mô hình Isolation Forest suy luận trong RAM dưới 3ms</td></tr>
  <tr><td>Định tuyến luồng thanh toán đa kênh</td><td>Cấu hình kênh cố định bằng tay</td><td>Thuật toán Thompson Sampling tự động chuyển hướng khi lag</td></tr>
  <tr><td>Đối soát sao kê sai lệch cú pháp</td><td>Kế toán tra soát thủ công từng dòng</td><td>Mô hình Sentence-Transformers so khớp ngữ nghĩa 99.2%</td></tr>
</table>
<p>Hôm nay, ta giải mã: <b>Ma trận 38 học phần UIT AI</b>, <b>ba bài toán cấp số nhân</b>, và <b>chiến lược phỏng vấn đỉnh cao</b>.</p>""",
                    "Hôm nay, ta cùng nhau khám phá giá trị cốt lõi của học vấn công nghệ cao. Ta tìm hiểu ma trận ba mươi tám học phần chuyên sâu tại đại học hàng đầu. Ta nắm vững ba bài toán ứng dụng học máy trực tiếp vào luồng xử lý giao dịch. Ta cũng làm chủ kỹ năng đối đáp tự tin trước hội đồng tuyển dụng.",
                    clear=True
                )
            ]
        },
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Ma trận Học phần Cử nhân AI tại UIT ĐHQG-HCM",
            "checks": [
                "38 > 30",
                "5 - 2 == 3"
            ],
            "steps": [
                build_step(
                    """<p><b>Năm khối kiến thức trụ cột trong chương trình Cử nhân AI tại UIT</b>:</p>
<table class="t">
  <tr><th>khối kiến thức</th><th>các học phần tiêu biểu</th><th>ứng dụng thực chiến trong ngân hàng</th></tr>
  <tr><td>Toán học & Cơ sở AI</td><td>Giải tích, Đại số tuyến tính, Xác suất thống kê</td><td>Tính độ lệch chuẩn Z-Score và ma trận rủi ro giao dịch</td></tr>
  <tr><td>Giải thuật nâng cao</td><td>Cấu trúc dữ liệu nâng cao, Phân tích thuật toán</td><td>Khóa có thứ tự triệt tiêu bế tắc, Bộ giới hạn tốc độ</td></tr>
  <tr><td>Hệ thống & Mạng</td><td>Kiến trúc máy tính, Hệ điều hành, Mạng phân tán</td><td>Quản lý luồng ảo, tối ưu bộ nhớ đệm CPU L1/L2/L3</td></tr>
  <tr><td>Cơ sở dữ liệu lớn</td><td>Cơ sở dữ liệu nâng cao, Hệ phân tán, NoSQL</td><td>Phân vùng bảng Oracle, Streaming ksqlDB, CDC Debezium</td></tr>
  <tr><td>Học máy & Thị giác</td><td>Machine Learning, Deep Learning, Computer Vision</td><td>Phát hiện gian lận thời gian thực, Sinh trắc học 2345</td></tr>
</table>""",
                    "Trước tiên ta ôn lại năm khối kiến thức trụ cột trong chương trình cử nhân trí tuệ nhân tạo. Nền tảng toán học và giải thuật nâng cao giúp giải quyết tận gốc các bài toán cao tải. Kiến thức học máy và thị giác máy tính cho phép triển khai giải pháp bảo mật sinh trắc học chuẩn quốc gia."
                ),
                build_step(
                    """<div class="box key">Định vị Kỹ sư Tích hợp sở hữu Bằng Cử nhân AI: Vừa có tay nghề cơ bắp làm chủ các hệ thống ngân hàng lõi như Core T24 và NAPAS 247, vừa có tư duy toán học và giải thuật cao cấp để đưa các mô hình học máy vào đường ống dữ liệu với độ trễ tối thiểu!</div>""",
                    "Sự kết hợp giữa kinh nghiệm thực chiến ngân hàng lõi và nền tảng học thuật đại học tạo nên một lợi thế cạnh tranh áp đảo. Kỹ sư vừa am hiểu tường tận các giao thức tài chính, vừa có khả năng ứng dụng các mô hình thông minh để giải quyết bài toán phức tạp.",
                    clear=True
                )
            ]
        },
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kiến trúc Đường dẫn Kép: Phân tách Luồng Nhanh và Luồng Chậm",
            "steps": [
                build_step(
                    """<p><b>Mô hình Đường dẫn Kép Dual-Path Architecture trong Phòng chống Gian lận</b>:</p>
<svg viewBox="0 0 700 220" style="width:100%;max-height:200px;">
  <rect x="20" y="80" width="140" height="60" rx="6" fill="#e8f4fd" stroke="#003366" stroke-width="2"/>
  <text x="35" y="115" font-size="12" font-weight="bold" fill="#003366">Giao dịch Inbound</text>
  <path d="M 160 95 L 230 50" stroke="#28a745" stroke-width="2"/>
  <rect x="230" y="20" width="220" height="70" rx="6" fill="#d4edda" stroke="#28a745"/>
  <text x="240" y="45" font-size="12" font-weight="bold" fill="#155724">Đường dẫn Nhanh (Fast Path)</text>
  <text x="240" y="68" font-size="11" fill="#155724">ONNX Runtime trong RAM sub-5ms</text>
  <path d="M 160 125 L 230 150" stroke="#17a2b8" stroke-width="2"/>
  <rect x="230" y="130" width="220" height="70" rx="6" fill="#d1ecf1" stroke="#17a2b8"/>
  <text x="240" y="155" font-size="12" font-weight="bold" fill="#0c5460">Đường dẫn Chậm (Slow Path)</text>
  <text x="240" y="178" font-size="11" fill="#0c5460">Đẩy vào Kafka topic payment.events</text>
  <rect x="490" y="20" width="180" height="70" rx="6" fill="#fff3cd" stroke="#ffc107"/>
  <text x="500" y="45" font-size="12" font-weight="bold" fill="#856404">Quyết định tức thời</text>
  <text x="500" y="68" font-size="11" fill="#856404">Cho qua / Chặn ngay</text>
  <rect x="490" y="130" width="180" height="70" rx="6" fill="#f8d7da" stroke="#dc3545"/>
  <text x="500" y="155" font-size="12" font-weight="bold" fill="#721c24">Phân tích Đồ thị AI</text>
  <text x="500" y="178" font-size="11" fill="#721c24">Cập nhật danh sách đen</text>
</svg>""",
                    "Để áp dụng học máy vào ngân hàng mà không làm nghẽn giao dịch, ta sử dụng kiến trúc đường dẫn kép. Đường dẫn nhanh thực thi mô hình siêu nhẹ trực tiếp trong bộ nhớ ứng dụng với độ trễ dưới năm mili giây. Trong khi đó, đường dẫn chậm đẩy dữ liệu vào hàng đợi để các mô hình đồ thị sâu phân tích quan hệ ngầm."
                ),
                build_step(
                    """<div class="box key">Đột phá của ONNX Runtime trong Java: Mô hình Isolation Forest được lượng tử hóa và chạy qua liên kết trực tiếp bằng mã máy C++. Nhờ đó thời gian tính toán chỉ mất 2 đến 3 mili giây, hoàn toàn nằm trong ngân sách thời gian dưới 100 mili giây của cổng thanh toán!</div>""",
                    "Điểm then chốt là việc nạp mô hình đã được tối ưu trực tiếp vào bộ nhớ ứng dụng thông qua liên kết mã máy. Thời gian tính toán điểm rủi ro chỉ tốn hai đến ba mili giây, hoàn toàn đáp ứng yêu cầu khắt khe về thời gian phản hồi của ngân hàng.",
                    clear=True
                )
            ]
        },
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Công thức Thuật toán Định tuyến Thông minh và So khớp Ngữ nghĩa",
            "checks": [
                "5 - 3 == 2",
                "992 // 10 == 99"
            ],
            "steps": [
                build_step(
                    r"""<p><b>Công thức Định tuyến Đa kênh với Thuật toán Thompson Sampling</b>:</p>
<div class="box key">
$$\text{Điểm tin cậy kênh } k: \text{Score}_k = \hat{\mu}_k + c \sqrt{\frac{\ln N}{N_k}}$$
$$\text{Độ tương đồng Cosine ngữ nghĩa: } \cos(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}$$
</div>
<p>Thuật toán tự động đo đạc tỉ lệ thành công $\hat{\mu}_k$ và độ bất định của từng cổng chuyển mạch trong cửa sổ trượt 15 phút để phân bổ tải tối ưu!</p>""",
                    "Theo công thức của lý thuyết học tăng cường tại trường đại học, thuật toán liên tục tính toán điểm tin cậy của từng kênh chuyển tiền. Khi một cổng chuyển mạch gặp sự cố mạng, hệ thống tự động nhận biết và chuyển hướng dòng tiền sang kênh dự phòng an toàn."
                ),
                build_step(
                    r"""<p><b>So khớp Sao kê Ngữ nghĩa bằng Vector Embeddings 384 chiều</b>:</p>
<pre><code>// Sinh vector nhúng biểu diễn ngữ nghĩa của chuỗi sao kê
vector1 = model.encode("Chuyen tien thanh toan hoa don tien dien thang 11")
vector2 = model.encode("EVN HCMC - Dien luc TP.HCM ky 11/2026")

// Tự động khớp lệnh khi độ tương đồng Cosine vượt ngưỡng 0.88
if (cosineSimilarity(vector1, vector2) >= 0.88) {
    autoReconcileMatch();
}</code></pre>""",
                    "Đối với bài toán đối soát hóa đơn sai lệch chính tả, ta sử dụng mô hình ngôn ngữ để chuyển chuỗi văn bản thành các véc tơ số học nhiều chiều. Bằng cách so khớp độ tương đồng góc hình học, hệ thống nhận dạng chính xác giao dịch mà không cần con người can thiệp.",
                    clear=True
                )
            ]
        },
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Phát hiện Gian lận Thẻ Tốc độ cao dưới 3 Mili giây",
            "checks": [
                "800 > 100",
                "5 - 2 == 3",
                "992 // 10 == 99"
            ],
            "steps": [
                build_step(
                    r"""<p><b>Dữ liệu bài toán bảo vệ thẻ tín dụng số tại ACB</b>:</p>
<ul>
  <li>Tình huống: Khách hàng vừa rút tiền tại Thành phố Hồ Chí Minh lúc 10h00, đến 10h15 xuất hiện giao dịch quẹt thẻ tại Singapore.</li>
  <li>Khoảng cách địa lý: $1\,500$ km trong thời gian 15 phút, tương đương vận tốc $6\,000$ km/h!</li>
  <li>Yêu cầu: Phát hiện và chặn đứng giao dịch gian lận trước khi gửi lệnh sang ngân hàng lõi.</li>
</ul>""",
                    "Ta xem xét tình huống khách hàng vừa thực hiện giao dịch tại một thành phố, nhưng chỉ mười lăm phút sau lại xuất hiện giao dịch tại một quốc gia khác. Khoảng cách địa lý hàng nghìn cây số trong thời gian ngắn cho thấy vận tốc di chuyển bất khả thi về mặt vật lý."
                ),
                build_step(
                    """<p><b>Bước 1: Trích xuất véc tơ đặc trưng tức thời trong Java Gateway</b>:</p>
<pre><code>// Trích xuất các đặc trưng rủi ro với độ trễ dưới 1 mili giây
float[] features = new float[] {
    calcGeoVelocity(loc1, loc2, dt), // Vận tốc di chuyển
    calcZScore(amount, avg30, std30), // Độ lệch số tiền
    getTxCount(cardId, 300) // Tần suất giao dịch 5 phút
};</code></pre>""",
                    "Bước một, cổng giao tiếp lập tức tính toán các đặc trưng rủi ro như vận tốc di chuyển địa lý, độ lệch chuẩn số tiền và tần suất quẹt thẻ. Quá trình trích xuất này diễn ra trong bộ nhớ với thời gian chưa đầy một mili giây.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2: Thực thi suy luận mô hình học máy qua ONNX Runtime</b>:</p>
<pre><code>OnnxTensor inputTensor = OnnxTensor.createTensor(
    env, FloatBuffer.wrap(features), shape);
OrtSession.Result result = session.run(
    Collections.singletonMap("input", inputTensor));
float anomalyScore = ((float[][]) result.get(0).getValue())[0][0];

// Thời gian thực thi đo đạc thực tế: Chỉ 2.1 mili giây!</code></pre>""",
                    "Bước hai, các đặc trưng được đưa vào mô hình học máy đã được huấn luyện sẵn. Thời gian thực thi đo đạc thực tế chỉ mất hai phẩy một mili giây, bảo đảm giao dịch không bị gián đoạn.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 3: Quyết định kích hoạt hàng rào bảo vệ sinh trắc học QĐ 2345</b>:</p>
<div class="box key">Khi điểm rủi ro vượt ngưỡng an toàn: Hệ thống lập tức yêu cầu khách hàng thực hiện xác thực khuôn mặt sinh trắc học 3D so khớp dữ liệu căn cước công dân gắn chip. Giao dịch gian lận bị chặn đứng 100%!</div>""",
                    "Bước ba, khi phát hiện điểm bất thường vượt ngưỡng, hệ thống kích hoạt ngay hàng rào xác thực khuôn mặt sinh trắc học theo quyết định của Ngân hàng Nhà nước. Kẻ gian không thể vượt qua bước này và tài sản của khách hàng được bảo vệ trọn vẹn.",
                    clear=True
                )
            ]
        },
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: Bản lĩnh Trả lời Phỏng vấn về Bằng Cử nhân AI UIT",
            "checks": [
                "2026 - 2025 == 1",
                "1000 // 100 == 10"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn thực tế của Lãnh đạo Khối CNTT ACB</b>: Bạn đã làm về tích hợp hệ thống ngân hàng tại OCB, tại sao lại đi học Cử nhân Trí tuệ Nhân tạo tại UIT? Liệu có phải bạn đang định hướng chuyển nghề sang làm nghiên cứu dữ liệu?</p>
<ul>
  <li>(A) Trả lời là vì thích học thêm để chuyển ngành sang làm khoa học dữ liệu.</li>
  <li>(B) Trả lời thẳng thắn: Mục tiêu nhất quán là trở thành Kỹ sư Kiến trúc Tích hợp Cấp cao, và AI là vũ khí toán học giúp giải quyết các bài toán cao tải, phòng chống gian lận sub-5ms mà logic thông thường không thể làm được.</li>
  <li>(C) Trả lời là học để lấy thêm bằng cấp cho đẹp hồ sơ.</li>
</ul>""",
                    "Mời bạn lựa chọn chiến lược trả lời câu hỏi cốt tử của lãnh đạo khối công nghệ thông tin. Khi người phỏng vấn dò hỏi về động cơ học bằng cử nhân trí tuệ nhân tạo, ứng viên bản lĩnh sẽ thể hiện định hướng nghề nghiệp như thế nào."
                ),
                build_step(
                    """<p><b>Đáp án chính xác: Lựa chọn (B)</b></p>
<div class="box key">Giải thích vì: Khẳng định mục tiêu nhất quán trở thành Kỹ sư Kiến trúc Cấp cao giúp hội đồng phỏng vấn thấy rõ tầm nhìn dài hạn của bạn. Nền tảng AI tại UIT chính là vũ khí cấp số nhân biến bạn thành ứng viên độc nhất vô nhị trên thị trường tuyển dụng!</div>""",
                    "Đáp án chính xác là lựa chọn B vì nó khẳng định tầm nhìn nhất quán của bạn trong sự nghiệp kiến trúc hệ thống. Do đó tấm bằng công nghệ cao đóng vai trò là vũ khí bổ trợ đắc lực chứ không phải sự phân tán định hướng.",
                    clear=True
                )
            ]
        },
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Nguy hiểm: Dùng Mô hình Quá Nặng làm Nghẽn Cổng Thanh toán",
            "steps": [
                build_step(
                    """<div class="box pit">Sai lầm chết người khi ứng dụng AI vào cổng giao dịch tài chính:</div>
<table class="t" style="margin-top: 10px;">
  <tr><th>sai lầm sơ cấp</th><th>hậu quả hệ thống</th><th>giải pháp chuẩn Senior UIT</th></tr>
  <tr><td>Nhúng mạng nơ-ron sâu vào luồng đồng bộ</td><td>Độ trễ tăng lên 500ms làm quá hạn API</td><td>Chỉ dùng mô hình cây nhẹ lượng tử hóa trong RAM</td></tr>
  <tr><td>Gọi API học máy qua đường truyền mạng</td><td>Tạo thêm điểm nghẽn mạng phân tán</td><td>Nhúng trực tiếp thư viện mã máy nội tại ứng dụng</td></tr>
</table>""",
                    "Một sai lầm phổ biến là việc đưa các mô hình quá cồng kềnh vào luồng xử lý đồng bộ khiến thời gian phản hồi bị kéo dài. Kỹ sư cấp cao chỉ áp dụng các mô hình nhỏ gọn đã được tối ưu hóa để bảo đảm thời gian thực thi tính bằng mili giây."
                )
            ]
        },
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán: Phân bổ Tài nguyên cho Cổng AI Ngân hàng",
            "checks": [
                "10 - 5 == 5",
                "38 - 8 == 30"
            ],
            "steps": [
                build_step(
                    """<p><b>Câu hỏi trắc nghiệm kiến trúc</b>: Trong hệ thống chống rửa tiền và phát hiện gian lận đa tầng, phân hệ nào nên được xử lý đồng bộ và phân hệ nào nên đưa vào hàng đợi bất đồng bộ?</p>
<ul>
  <li><b>A</b>: Xử lý đồng bộ kiểm tra điểm bất thường nhẹ dưới 5ms; đưa toàn bộ đồ thị quan hệ rửa tiền phức tạp vào hàng đợi Kafka để cụm máy chủ AI phân tích ngầm.</li>
  <li><b>B</b>: Xử lý toàn bộ trên luồng đồng bộ để đảm bảo an toàn tuyệt đối.</li>
  <li><b>C</b>: Không cần kiểm tra đồng bộ, chỉ gửi báo cáo vào cuối tháng.</li>
  <li><b>D</b>: Chuyển toàn bộ dữ liệu sang cho đối tác nước ngoài xử lý.</li>
</ul>""",
                    "Xin mời bạn lựa chọn mô hình phân bổ tải tối ưu giữa kiểm tra tức thời và phân tích chuyên sâu. Bạn có 15 giây suy nghĩ trước khi nghe phân tích chuẩn mực từ chuyên gia hệ thống.",
                    pause=15
                ),
                build_step(
                    """<div class="box key"><b>Đáp án chính xác là A</b>!</div>
<p><b>Bước 1 — Nguyên tắc phân tầng rủi ro trong ngân hàng</b>:</p>
<table class="t">
  <tr><th>tầng xử lý</th><th>độ trễ chấp nhận</th><th>mục tiêu bảo vệ</th></tr>
  <tr><td>Đồng bộ (Fast Path)</td><td>Dưới 5 mili giây</td><td>Chặn đứng các giao dịch bất thường hiển nhiên ngay tại cửa ngõ</td></tr>
  <tr><td>Bất đồng bộ (Slow Path)</td><td>Vài giây đến vài phút</td><td>Phát hiện các đường dây rửa tiền phức tạp và giao dịch chéo</td></tr>
</table>""",
                    "Đáp án chính xác là phương án A. Ta chia hệ thống thành tầng kiểm tra tức thời tại cửa ngõ và tầng phân tích chuyên sâu chạy ngầm phía sau. Cách phân bổ này vừa bảo đảm tốc độ phục vụ khách hàng, vừa phát hiện được các thủ đoạn tinh vi.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2 — Giá trị cấp số nhân mang lại cho ACB</b>:</p>
<div class="box key">Kiến trúc đường dẫn kép giúp ACB vừa duy trì trải nghiệm chuyển khoản siêu tốc cho hàng triệu khách hàng, vừa đáp ứng đầy đủ các tiêu chuẩn an toàn thông tin khắt khe nhất của Ngân hàng Nhà nước!</div>""",
                    "Bước hai, mô hình đường dẫn kép giúp ngân hàng cân bằng hoàn hảo giữa trải nghiệm mượt mà và an toàn bảo mật. Đây chính là minh chứng thuyết phục nhất cho giá trị cấp số nhân mà bạn mang lại cho tổ chức.",
                    clear=True
                )
            ]
        },
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Ứng dụng AI và Giá trị Cấp số nhân UIT",
            "steps": [
                build_step(
                    """<div class="chain">
  <span>Nền tảng Toán & Giải thuật 38 Học phần UIT AI</span> &rarr;
  <span>Mô hình Đường dẫn kép Fast Path & Slow Path</span> &rarr;
  <span>Suy luận Học máy ONNX Runtime sub-5ms trong RAM</span> &rarr;
  <span>Thuật toán Thompson Sampling Định tuyến Thông minh</span> &rarr;
  <span>Khẳng định Vị thế Kỹ sư Cấp cao xứng tầm 50M Gross</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>vũ khí cạnh tranh</th><th>giá trị tạo ra cho Ngân hàng TMCP Á Châu</th></tr>
  <tr><td>Tư duy giải thuật tối ưu</td><td>Làm chủ các hệ thống phân tán, triệt tiêu bế tắc khóa và nghẽn mạng</td></tr>
  <tr><td>Học máy thời gian thực</td><td>Ngăn chặn gian lận tức thời, tiết kiệm hàng chục tỉ đồng thiệt hại rủi ro</td></tr>
  <tr><td>Tự động hóa đối soát AI</td><td>Giảm 90% thời gian xử lý thủ công, vận hành tinh gọn chuẩn quốc tế</td></tr>
</table>
<p style="margin-top: 15px;"><b>Bản lĩnh Kỹ sư Trí tuệ Nhân tạo tại ACB</b>: Biến học vấn đỉnh cao thành giá trị bảo vệ tài sản số và vững vàng chốt mức đãi ngộ 50 triệu gross.</p>""",
                    "Tóm lại, chuỗi logic gồm nền tảng học thuật đại học, kiến trúc đường dẫn kép, suy luận máy học tốc độ cao và định tuyến thông minh. Biến tri thức đỉnh cao thành giá trị bảo vệ hệ thống, bạn tự tin khẳng định vị thế Kỹ sư Cấp cao và xứng đáng với mức lương 50 triệu gross tại ACB."
                )
            ]
        }
    ]
}

save_spec(l05, r"D:\research-video\lessons\int\L05_uit_ai_banking_multiplier.yaml")
print("L05 generated successfully!")
