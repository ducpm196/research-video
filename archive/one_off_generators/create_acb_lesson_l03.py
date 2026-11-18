import yaml

lesson = {
    "id": "L03",
    "course": "ACB",
    "series": "Phỏng vấn Kỹ sư Tích hợp ACB",
    "title": "Bài 3 — Kiến trúc Streaming với ksqlDB và Kafka: Omnichannel Notification Hub",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "curriculum/acb.yaml L03; Confluent Platform ksqlDB Documentation; Apache Kafka Streams Guide; Kiến trúc Notification Hub OCB và ACB 2026",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Xây dựng luồng xử lý biến động số dư thời gian thực qua Kafka CDC và ksqlDB",
        "Thực hiện Stream-Table Join phân luồng thông báo OTT Push, SMS Brandname và Email",
        "Thiết kế hàng đợi ưu tiên Priority Queue và cơ chế Dead Letter Queue chống thất lạc"
    ],
    "scenes": [
        # 1. HOOK
        {
            "id": "hook",
            "kind": "hook",
            "title": "Bài toán gửi 50 nghìn tin nhắn mỗi phút mà không làm nghẽn hệ thống",
            "steps": [
                {
                    "show": """<p>Khi hàng triệu khách hàng đồng loạt nhận lương, mỗi giây phát sinh hàng chục nghìn biến động số dư.</p>
<div class="box key">Nếu từng microservice tự gọi trực tiếp sang nhà mạng viễn thông, hệ thống sẽ sập do nghẽn mạng và chi phí cước viễn thông bùng nổ.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Chào bạn, khi hàng triệu khách hàng đồng loạt nhận lương vào đầu tháng, hệ thống ngân hàng phát sinh hàng chục nghìn giao dịch mỗi giây. Khách hàng mong muốn nhận thông báo biến động số dư tức thì trong chưa đầy một giây. Nếu mỗi dịch vụ tự gọi sang nhà mạng viễn thông, hệ thống sẽ nghẽn tắc ngay lập tức."
                },
                {
                    "show": """<p>Hôm nay, ta mổ xẻ: <b>Nền tảng Confluent ksqlDB và Kafka Streams</b>, <b>kỹ thuật Stream-Table Join thời gian thực</b>, và <b>kiến trúc Omnichannel Notification Hub tiết kiệm 70% chi phí SMS</b>.</p>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Hôm nay ta cùng khám phá giải pháp đẳng cấp của các ngân hàng lớn. Ta phân tích nền tảng Confluent cây-x-cu-l-đê-bê và Kafka Streams. Ta tìm hiểu kỹ thuật kết hợp luồng dữ liệu thời gian thực. Ta cũng giải mã trung tâm thông báo đa kênh giúp tiết kiệm 70 phần trăm chi phí cước viễn thông cho ngân hàng."
                }
            ]
        },
        # 2. PREREQ
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Stream, Table, Change Data Capture và định dạng Avro",
            "checks": [
                "50000 * 60 == 3000000 and 3000000 * 24 == 72000000",
                "1000 // 500 == 2 and 500 * 2 == 1000"
            ],
            "steps": [
                {
                    "show": """<p><b>Bốn khái niệm nền tảng trong truyền phát dữ liệu Confluent</b>:</p>
<table class="t">
  <tr><th>khái niệm</th><th>ý nghĩa kỹ thuật</th><th>vai trò trong ngân hàng</th></tr>
  <tr><td>Stream</td><td>dòng sự kiện chảy liên tục không ngừng</td><td>chuỗi các giao dịch phát sinh theo thời gian</td></tr>
  <tr><td>Table</td><td>ảnh chụp trạng thái hiện tại của một khóa</td><td>thông tin hồ sơ và cài đặt nhận tin của khách</td></tr>
  <tr><td>CDC</td><td>Change Data Capture bắt thay đổi dữ liệu</td><td>bắt biến động số dư từ cơ sở dữ liệu sổ cái</td></tr>
  <tr><td>Avro Schema</td><td>chuẩn nén và tiến hóa cấu trúc dữ liệu</td><td>bảo đảm tính tương thích giữa các dịch vụ</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0, 0],
                    "say": "Trước tiên ta ôn lại bốn khái niệm then chốt trong xử lý luồng dữ liệu. Luồng là dòng sự kiện chảy liên tục thể hiện các giao dịch vừa phát sinh. Bảng là ảnh chụp trạng thái mới nhất lưu trữ cài đặt nhận tin của từng khách hàng. Kỹ thuật bắt biến động dữ liệu giúp trích xuất tức thời các dòng tiền mới. Chuẩn cấu trúc dữ liệu Avro giúp bảo đảm tính tương thích lâu dài."
                },
                {
                    "show": """<div class="box key">Ở lưu lượng $50\,000$ thông báo mỗi phút: Mỗi giờ có $50\,000 \times 60 = 3\,000\,000$ tin nhắn. Mỗi ngày hệ thống chuyển phát tới $72\,000\,000$ tin nhắn. Độ trễ yêu cầu dưới $500$ ms, tức mỗi giây phải hoàn tất $1\,000 / 500 = 2$ chu kỳ chuyển phát.</div>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Ta xem xét quy mô xử lý thực tế của một ngân hàng bán lẻ hàng đầu. Tại mức 50 nghìn thông báo mỗi phút, mỗi giờ có 3 triệu bản tin được phát đi. Tổng lưu lượng một ngày đạt tới 72 triệu thông báo. Toàn bộ chu trình phải hoàn tất trong vòng 500 mi li giây để người dùng không phải chờ đợi."
                }
            ]
        },
        # 3. CONCEPT
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kiến trúc Xử lý Luồng và Trung tâm Thông báo Đa kênh",
            "steps": [
                {
                    "show": """<div>
  <svg width="1500" height="380" viewBox="0 0 1500 380">
    <g font-size="22" fill="#1f2937">
      <text x="750" y="35" text-anchor="middle" font-weight="bold" font-size="26">Kiến trúc Streaming ksqlDB và Omnichannel Notification Hub</text>
      <rect x="50" y="70" width="300" height="240" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
      <text x="200" y="115" text-anchor="middle" font-weight="bold">1. Core Banking</text>
      <text x="200" y="160" text-anchor="middle">Biến động số dư</text>
      <text x="200" y="200" text-anchor="middle">Bắt CDC thời gian thực</text>
      <text x="200" y="240" text-anchor="middle">Đẩy vào Kafka Topic</text>

      <rect x="440" y="70" width="320" height="240" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>
      <text x="600" y="115" text-anchor="middle" font-weight="bold">2. Confluent ksqlDB</text>
      <text x="600" y="160" text-anchor="middle">Stream-Table Join</text>
      <text x="600" y="200" text-anchor="middle">Lọc ngưỡng &gt; 50k VND</text>
      <text x="600" y="240" text-anchor="middle">Phân luồng kênh thông báo</text>

      <rect x="850" y="70" width="280" height="240" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
      <text x="990" y="115" text-anchor="middle" font-weight="bold">3. Notification Hub</text>
      <text x="990" y="160" text-anchor="middle">Hàng đợi ưu tiên OTP</text>
      <text x="990" y="200" text-anchor="middle">Khử trùng lặp Redis 24h</text>
      <text x="990" y="240" text-anchor="middle">Cầu dao chống quá tải</text>

      <rect x="1210" y="70" width="250" height="240" rx="12" fill="#f3e8ff" stroke="#9333ea" stroke-width="3"/>
      <text x="1335" y="115" text-anchor="middle" font-weight="bold">4. Omnichannel Delivery</text>
      <text x="1335" y="160" text-anchor="middle">OTT App Push (Free)</text>
      <text x="1335" y="200" text-anchor="middle">SMS Brandname Viễn thông</text>
      <text x="1335" y="240" text-anchor="middle">Email sao kê định kỳ</text>

      <line x1="350" y1="150" x2="440" y2="150" stroke="#0284c7" stroke-width="4"/>
      <line x1="760" y1="150" x2="850" y2="150" stroke="#d97706" stroke-width="4"/>
      <line x1="1130" y1="150" x2="1210" y2="150" stroke="#16a34a" stroke-width="4"/>
    </g>
  </svg>
</div>""",
                    "focus": [0, 0, 0, 0, 0],
                    "say": "Nhìn lên sơ đồ luồng dữ liệu truyền phát. Bước một, cơ chế bắt biến động dữ liệu trích xuất giao dịch từ Core Banking và đẩy vào hàng đợi sự kiện. Bước hai, máy chủ cây-x-cu-l-đê-bê kết hợp luồng giao dịch với bảng hồ sơ khách hàng để chọn kênh gửi tối ưu. Bước ba, Trung tâm thông báo phân loại mức ưu tiên và kiểm tra khóa chống gửi trùng. Bước bốn, bản tin được chuyển phát tức thì qua kênh di động, tin nhắn viễn thông hoặc thư điện tử."
                }
            ]
        },
        # 4. SYMBOL
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Cú pháp câu lệnh Stream-Table Join trong ksqlDB",
            "steps": [
                {
                    "show": """<p><b>Câu lệnh ksqlDB phân luồng thông báo tự động theo thời gian thực</b>:</p>
<div class="box code"><code>CREATE STREAM s_routed_notifications AS<br/>
SELECT e.account_no, e.amount, e.balance, p.phone_number, p.email,<br/>
&nbsp;&nbsp;CASE WHEN p.is_app_installed = TRUE THEN 'OTT_PUSH'<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WHEN e.amount >= 50000 THEN 'SMS_BRANDNAME' ELSE 'EMAIL' END AS target_channel<br/>
FROM s_balance_events e LEFT JOIN t_customer_preferences p<br/>
ON e.account_no = p.account_no EMIT CHANGES;</code></div>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Câu lệnh cây-x-cu-l-đê-bê thể hiện sức mạnh xử lý luồng tức thời. Ta tạo một luồng mới bằng cách kết hợp luồng sự kiện giao dịch với bảng hồ sơ khách hàng. Mệnh đề điều kiện kiểm tra nếu khách hàng đã cài ứng dụng di động thì định tuyến sang thông báo đẩy miễn phí. Nếu chưa cài ứng dụng và số tiền lớn hơn 50 nghìn đồng, hệ thống sẽ gửi tin nhắn viễn thông có phí."
                }
            ]
        },
        # 5. EXAMPLE
        {
            "id": "example",
            "kind": "example",
            "title": "Tính toán tối ưu hóa chi phí và hiệu năng chuyển phát",
            "checks": [
                "50000 // 60 == 833 and 833 * 60 == 49980",
                "50000 * 70 // 100 == 35000",
                "50000 - 35000 == 15000"
            ],
            "steps": [
                {
                    "show": """<p><b>Bước 1 — Tính lưu lượng xử lý mỗi giây (TPS) của luồng thông báo</b>:</p>
<div class="box key">Lưu lượng tổng: $50\,000$ tin nhắn mỗi phút.<br/>
Lưu lượng mỗi giây: $50\,000 / 60 \\approx 833$ tin nhắn mỗi giây.<br/>
Tại thời điểm đỉnh tải: hệ thống cần xử lý tới $1\,500$ thông báo mỗi giây.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước một, ta tính toán lưu lượng trung bình mỗi giây của đường ống thông báo. Với 50 nghìn tin nhắn mỗi phút, tốc độ xử lý tương đương xấp xỉ 833 tin nhắn trong một giây. Do đó, cụm máy chủ cần được cấu hình nhóm xử lý song song để đáp ứng mức đỉnh 1500 lệnh mỗi giây."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Tính toán tỉ lệ tiết kiệm chi phí viễn thông</b>:</p>
<table class="t">
  <tr><th>kênh chuyển phát</th><th>tỉ lệ phân luồng</th><th>số lượng tin/phút</th><th>chi phí phát sinh</th></tr>
  <tr><td>OTT App Push</td><td>$70\\%$ khách cài ứng dụng</td><td>$50\,000 \\times 70\\% = 35\,000$ tin</td><td>$0$ đồng (hoàn toàn miễn phí)</td></tr>
  <tr><td>SMS Brandname</td><td>$30\\%$ chưa cài ứng dụng</td><td>$50\,000 - 35\,000 = 15\,000$ tin</td><td>chỉ trả cước cho $15\,000$ tin</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Bước hai, ta tính toán bài toán kinh tế khi định tuyến thông minh. Vì có 70 phần trăm khách hàng đã cài ứng dụng di động, ta chuyển 35 nghìn tin sang dạng thông báo đẩy miễn phí. Do đó, ngân hàng chỉ phải trả cước viễn thông cho 15 nghìn tin nhắn, tiết kiệm được hàng tỉ đồng chi phí mỗi tháng."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 3 — Cơ chế bảo vệ chống gửi tin nhắn trùng lặp</b>:</p>
<div class="box key">Thiết lập bộ nhớ đệm phân tán: <code>SET noti:sent:{event_id} 1 EX 86400 NX</code>.<br/>
Khóa lưu giữ trong $86\,400$ giây $= 24$ giờ. Ngăn chặn triệt để hiện tượng khách hàng nhận 2 tin nhắn trừ tiền giống nhau gây hoang mang.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước ba, ta thiết lập khóa chống gửi tin nhắn trùng lặp trong bộ nhớ đệm phân tán. Khóa được giữ trong 24 giờ tương đương 86 nghìn 400 giây. Nhờ lệnh nguyên tử này, mọi bản tin trùng lặp do mạng chập chờn đều bị loại bỏ ngay lập tức."
                }
            ]
        },
        # 6. CHECK
        {
            "id": "check",
            "kind": "check",
            "title": "Kiểm tra xử lý tình huống nhà mạng viễn thông gặp sự cố",
            "checks": [
                "86400 // 3600 == 24",
                "50000000 - 0 == 50000000"
            ],
            "steps": [
                {
                    "show": """<p><b>Tình huống phỏng vấn</b>: Cổng nhà mạng viễn thông chính báo lỗi HTTP 503 hoặc quá tải nghẽn mạng trong giờ trả lương. Bạn xử lý thế nào để mã OTP không bị chậm trễ?</p>
<table class="t">
  <tr><th>cách xử lý sơ cấp</th><th>giải pháp chuẩn mực Senior</th></tr>
  <tr><td>Tiếp tục gọi thử lại liên tục</td><td>Kích hoạt cầu dao tự động chuyển sang nhà mạng phụ trong 200 ms</td></tr>
  <tr><td>Làm nghẽn luồng xử lý của hệ thống</td><td>Tách riêng hàng đợi ưu tiên cho mã OTP và cảnh báo giao dịch</td></tr>
  <tr><td>Làm thất lạc mã xác thực của khách</td><td>Đẩy các tin nhắn thường vào hàng đợi chờ xử lý sau</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Ta kiểm tra tình huống thực tế khi đối tác viễn thông bị nghẽn mạng vào ngày cao điểm. Do nhà mạng trả về lỗi quá tải, cách làm vụng về là tiếp tục thử lại liên tục khiến hàng nghìn luồng máy chủ bị đóng băng. Hậu quả là mã xác thực bị chậm trễ khiến khách hàng không thể thực hiện giao dịch."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Quy tắc chuyển mạng tự động</b>: Khi tỉ lệ lỗi vượt quá ngưỡng 10 phần trăm, cầu dao tự động chuyển hướng sang cổng viễn thông dự phòng trong vòng 200 ms. Do đó, mã xác thực cho giao dịch 50 triệu đồng luôn được gửi đến điện thoại khách hàng trong vòng chưa đầy nửa giây.</div>""",
                    "focus": [0, 0],
                    "say": "Vì tính cấp bách của mã xác thực, cơ chế cầu dao tự động sẽ chuyển hướng sang nhà mạng dự phòng trong 200 mi li giây. Nhờ đó, giao dịch 50 triệu đồng của khách hàng luôn được bảo đảm an toàn và thông suốt tuyệt đối."
                }
            ]
        },
        # 7. PITFALL
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Ba sai lầm nghiêm trọng trong kiến trúc Streaming thông báo",
            "steps": [
                {
                    "show": """<table class="t">
  <tr><th>sai lầm sơ cấp</th><th>hậu quả kỹ thuật & tài chính</th><th>giải pháp chuẩn Senior</th></tr>
  <tr><td>Gộp chung mã OTP và tin quảng cáo</td><td>mã OTP bị xếp hàng sau hàng nghìn tin quảng bá</td><td>tách riêng hàng đợi ưu tiên Priority Queue</td></tr>
  <tr><td>Bỏ qua hàng đợi tin lỗi Dead Letter Queue</td><td>bản tin lỗi bị xóa mất, không thể tra soát</td><td>lưu toàn bộ bản tin hỏng vào hàng đợi lưu vết</td></tr>
  <tr><td>Không kiểm soát tốc độ gửi qua nhà mạng</td><td>nhà mạng chặn kết nối do vi phạm chính sách cước</td><td>áp dụng thuật toán Token Bucket giới hạn tốc độ</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Có ba sai lầm chí mạng trong thiết kế trung tâm thông báo. Thứ nhất là gộp chung tin nhắn mã xác thực với tin tức tiếp thị khiến mã bảo mật bị nghẽn lại phía sau. Thứ hai là thiếu hàng đợi tin lỗi khiến các thông báo quan trọng bị mất dấu khi đối tác lỗi mạng. Thứ ba là không kiểm soát tốc độ gửi khiến hệ thống bị nhà mạng tạm khóa vì nghi ngờ thư rác."
                }
            ]
        },
        # 8. QUIZ
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Thử thách kiến trúc luồng dữ liệu tại ACB",
            "checks": [
                "3 * 5 == 15",
                "50000 * 2 == 100000"
            ],
            "steps": [
                {
                    "pause": 15,
                    "show": """<p><b>Câu hỏi trắc nghiệm kiến trúc</b>: Trong Confluent ksqlDB, tại sao bảng hồ sơ người dùng <code>t_customer_preferences</code> phải được tạo dưới dạng <code>TABLE</code> thay vì dạng <code>STREAM</code> khi thực hiện kết hợp dữ liệu?</p>
<ul>
  <li><b>A</b>: Vì Table lưu trữ trạng thái mới nhất của mỗi số tài khoản, cho phép tra cứu tức thời cấu hình nhận tin mà không cần quét lại toàn bộ lịch sử.</li>
  <li><b>B</b>: Vì ksqlDB không cho phép hai Stream kết hợp với nhau.</li>
  <li><b>C</b>: Vì Table giúp giảm dung lượng ổ đĩa về bằng 0.</li>
  <li><b>D</b>: Vì Stream chỉ chạy được trên một máy chủ đơn lẻ.</li>
</ul>""",
                    "focus": [0, 0, 0],
                    "say": "Hãy cùng bước vào câu hỏi trắc nghiệm kiến trúc thực chiến của ACB. Trong công nghệ cây-x-cu-l-đê-bê, tại sao bảng hồ sơ người dùng bắt buộc phải được tạo dưới dạng Bảng thay vì dạng Luồng? Bạn có 15 giây suy nghĩ trước khi nghe đáp án chuẩn xác."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Đáp án chính xác là A</b>!</div>
<p><b>Bước 1 — Bản chất của đối tượng Table trong ksqlDB</b>:</p>
<p>Bảng đại diện cho trạng thái hiện tại của dữ liệu theo từng khóa tài khoản. Khi có biến động số dư, hệ thống chỉ cần lấy bản ghi cấu hình mới nhất của đúng khách hàng đó.</p>""",
                    "focus": [0, 0],
                    "say": "Đáp án chính xác là phương án A. Bước một, đối tượng Bảng duy trì trạng thái mới nhất cho mỗi khách hàng, giúp việc tra cứu thông tin nhận tin diễn ra tức thì."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Tối ưu hóa hiệu năng và bộ nhớ</b>:</p>
<div class="box key">Nếu dùng Stream, hệ thống phải lưu và quét qua hàng triệu bản ghi lịch sử, gây lãng phí bộ nhớ và làm tăng độ trễ vượt quá ngưỡng $500$ ms. Mô hình Stream-Table Join là bí quyết giúp hệ thống đạt $50\,000$ tin nhắn mỗi phút một cách mượt mà.</div>""",
                    "focus": [0, 0],
                    "say": "Bước hai, nếu dùng dạng Luồng, hệ thống sẽ phải lưu trữ toàn bộ lịch sử thay đổi khiến bộ nhớ bị quá tải. Kỹ thuật kết hợp giữa Luồng và Bảng là bí quyết cốt lõi giúp hệ thống đạt hiệu năng đỉnh cao."
                }
            ]
        },
        # 9. RECAP
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Streaming và Notification Hub",
            "steps": [
                {
                    "show": """<div class="chain">
  <span>Bắt biến động CDC Core T24</span> &rarr;
  <span>Stream-Table Join qua ksqlDB</span> &rarr;
  <span>Phân luồng OTT Push và SMS</span> &rarr;
  <span>Hàng đợi ưu tiên Priority Queue</span> &rarr;
  <span>Khử trùng lặp Redis 24h</span> &rarr;
  <span>Chuyển phát đa kênh an toàn</span>
</div>
<p style="margin-top: 15px;"><b>Khẳng định đẳng cấp Senior tại ngân hàng ACB</b>: Nắm vững hệ sinh thái Confluent, tối ưu hóa 50 nghìn thông báo mỗi phút, tiết kiệm 70% chi phí viễn thông và tự tin chinh phục mức đãi ngộ 50 triệu gross.</p>""",
                    "focus": [0, 0],
                    "say": "Tóm lại, chuỗi logic truyền phát gồm bắt biến động dữ liệu, kết hợp luồng qua cây-x-cu-l-đê-bê, phân luồng đa kênh, khử trùng lặp và chuyển phát an toàn. Nắm vững giải pháp này, bạn hoàn toàn tự tin tỏa sáng ở vị trí Kỹ sư Tích hợp Cấp cao và chinh phục mức thu nhập 50 triệu gross tại ACB."
                }
            ]
        }
    ]
}

with open("lessons/acb/L03_streaming_ksqldb_notification_hub.yaml", "w", encoding="utf-8") as f:
    yaml.dump(lesson, f, allow_unicode=True, sort_keys=False, width=1000)

print("Created lessons/acb/L03_streaming_ksqldb_notification_hub.yaml successfully!")
