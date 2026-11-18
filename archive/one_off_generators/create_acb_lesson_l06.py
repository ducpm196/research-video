import yaml

lesson = {
    "id": "L06",
    "course": "ACB",
    "series": "Phỏng vấn Kỹ sư Tích hợp ACB",
    "title": "Bài 6 — Xác thực Sinh trắc học Quyết định 2345 và Bảo mật Ngân hàng Mở",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "curriculum/acb.yaml L06; Quyết định 2345/QĐ-NHNN; Kiến trúc bio-authentication-service và Open Banking Gateway ACB 2026",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Nắm vững quy định 2345 của Ngân hàng Nhà nước về xác thực khuôn mặt sinh trắc học",
        "Tích hợp SDK chống giả mạo Liveness Detection và Cổng định danh dân cư VNeID",
        "Thiết lập bước kiểm tra sinh trắc học làm điều kiện tiên quyết trong luồng SAGA"
    ],
    "scenes": [
        # 1. HOOK
        {
            "id": "hook",
            "kind": "hook",
            "title": "Bài toán bảo vệ tài khoản ngân hàng trước làn sóng Deepfake và Lừa đảo",
            "steps": [
                {
                    "show": """<p>Từ ngày 01 tháng 07 năm 2024, Ngân hàng Nhà nước ban hành Quyết định 2345 bắt buộc xác thực sinh trắc học.</p>
<div class="box key">Mọi giao dịch chuyển tiền trên 10 triệu đồng hoặc tích lũy trong ngày vượt 20 triệu đồng đều bắt buộc phải quét khuôn mặt sống trùng khớp với dữ liệu thẻ căn cước gắn chip.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Chào bạn, trước làn sóng lừa đảo công nghệ cao và giả mạo khuôn mặt, Ngân hàng Nhà nước đã ban hành Quyết định 2345. Mọi giao dịch chuyển tiền giá trị lớn đều bắt buộc phải đối soát khuôn mặt với căn cước công dân gắn chíp. Đây là lá chắn an ninh tối thượng bảo vệ tài sản của khách hàng."
                },
                {
                    "clear": True,
                    "show": """<table class="t">
  <tr><th>thách thức kỹ thuật</th><th>nguy cơ bảo mật</th><th>giải pháp kiến trúc chuẩn Senior</th></tr>
  <tr><td>Kẻ gian dùng video giả mạo Deepfake</td><td>Tài khoản bị chiếm đoạt số tiền lớn</td><td>SDK kiểm tra độ sống Liveness Detection 3D</td></tr>
  <tr><td>Cổng xác thực quốc gia bị nghẽn mạng</td><td>Giao dịch của khách hàng bị treo đứng</td><td>Bộ đệm phiên làm việc và kiểm tra tải tự động</td></tr>
  <tr><td>Kẻ xấu gọi thẳng API hạch toán Core</td><td>Bỏ qua bước quét khuôn mặt trên ứng dụng</td><td>Điều kiện tiên quyết SAGA Pre-condition Gate</td></tr>
</table>
<p>Hôm nay, ta giải mã: <b>Chuẩn an ninh Quyết định 2345</b>, <b>cơ chế kiểm tra độ sống chống giả mạo</b>, và <b>kiến trúc cổng xác thực sinh trắc học an toàn</b>.</p>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Hôm nay, ta cùng nhau khám phá trọn vẹn kiến trúc an ninh này. Ta tìm hiểu tiêu chuẩn xác thực sinh trắc học theo quy định ngân hàng. Ta nắm vững cơ chế kiểm tra độ sống chống video giả mạo. Ta cũng làm chủ cổng bảo mật làm điều kiện tiên quyết trong điều phối giao dịch."
                }
            ]
        },
        # 2. PREREQ
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Ngưỡng giao dịch 10 triệu, Dữ liệu chip CCCD và Giao thức mTLS",
            "checks": [
                "10000000 + 10000000 == 20000000",
                "20000000 // 10000000 == 2"
            ],
            "steps": [
                {
                    "show": """<p><b>Ba quy tắc vàng trong Quyết định 2345 của Ngân hàng Nhà nước</b>:</p>
<table class="t">
  <tr><th>hạn mức giao dịch</th><th>yêu cầu bắt buộc</th><th>hình thức xác thực</th></tr>
  <tr><td>Dưới 10 triệu đồng/lần</td><td>Xác thực tiêu chuẩn</td><td>Mã PIN hoặc OTP ứng dụng ngân hàng</td></tr>
  <tr><td>Từ 10 triệu đồng/lần trở lên</td><td>Bắt buộc sinh trắc học</td><td>Khuôn mặt trùng khớp với dữ liệu chíp CCCD</td></tr>
  <tr><td>Tổng giao dịch ngày trên 20 triệu</td><td>Bắt buộc sinh trắc học</td><td>Quét khuôn mặt cho toàn bộ các lệnh phát sinh sau đó</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Trước tiên ta ôn lại ba quy tắc vàng trong Quyết định 2345. Giao dịch dưới mười triệu đồng chỉ cần xác thực mã pin hoặc mật mã dùng một lần. Khi số tiền từ mười triệu đồng trở lên, khách hàng bắt buộc phải quét khuôn mặt. Nếu tổng tiền chuyển trong ngày vượt 20 triệu đồng, các lệnh sau đó đều phải xác thực sinh trắc học."
                },
                {
                    "clear": True,
                    "show": """<div class="box key">Ví dụ: Buổi sáng khách chuyển $8$ triệu đồng (chưa cần khuôn mặt). Buổi chiều khách chuyển tiếp $14$ triệu đồng $\to$ Vượt hạn mức $10$ triệu và tổng ngày đạt $22$ triệu đồng.<br/>
Cả hai điều kiện đều chạm ngưỡng, hệ thống kích hoạt cổng sinh trắc học ngay lập tức!</div>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Ta xét một ví dụ thực tế trên ứng dụng ngân hàng. Buổi sáng khách hàng chuyển tám triệu đồng thành công mà chưa cần quét mặt. Buổi chiều khách chuyển tiếp 14 triệu đồng khiến tổng tiền trong ngày vượt 22 triệu đồng. Cổng thanh toán lập tức yêu cầu nhận diện khuôn mặt trước khi hạch toán."
                }
            ]
        },
        # 3. CONCEPT
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kiến trúc Cổng Xác thực Sinh trắc học và Điều kiện Tiên quyết SAGA",
            "steps": [
                {
                    "show": """<div>
  <svg width="1500" height="380" viewBox="0 0 1500 380">
    <g font-size="22" fill="#1f2937">
      <text x="750" y="35" text-anchor="middle" font-weight="bold" font-size="26">Kiến trúc Cổng Sinh trắc học Quyết định 2345 và Điều phối SAGA</text>
      <rect x="50" y="70" width="300" height="240" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
      <text x="200" y="115" text-anchor="middle" font-weight="bold">1. Mobile Client</text>
      <text x="200" y="160" text-anchor="middle">Quét 3D khuôn mặt</text>
      <text x="200" y="200" text-anchor="middle">Kiểm tra độ sống Liveness</text>
      <text x="200" y="240" text-anchor="middle">Mã hóa dữ liệu gửi lên</text>

      <rect x="440" y="70" width="320" height="240" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>
      <text x="600" y="115" text-anchor="middle" font-weight="bold">2. Biometric Gateway</text>
      <text x="600" y="160" text-anchor="middle">Xác thực mTLS hai chiều</text>
      <text x="600" y="200" text-anchor="middle">So khớp với chíp CCCD</text>
      <text x="600" y="240" text-anchor="middle">Sinh chứng chỉ phiên</text>

      <rect x="850" y="70" width="280" height="240" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
      <text x="990" y="115" text-anchor="middle" font-weight="bold">3. SAGA Orchestrator</text>
      <text x="990" y="160" text-anchor="middle">Kiểm tra vé sinh trắc học</text>
      <text x="990" y="200" text-anchor="middle">Chặn đứng nếu thiếu vé</text>
      <text x="990" y="240" text-anchor="middle">Điều kiện tiên quyết</text>

      <rect x="1210" y="70" width="250" height="240" rx="12" fill="#f3e8ff" stroke="#9333ea" stroke-width="3"/>
      <text x="1335" y="115" text-anchor="middle" font-weight="bold">4. Core T24 & NAPAS</text>
      <text x="1335" y="160" text-anchor="middle">Trích nợ tài khoản</text>
      <text x="1335" y="200" text-anchor="middle">Chuyển mạch liên ngân hàng</text>
      <text x="1335" y="240" text-anchor="middle">Giao dịch an toàn 100%</text>

      <line x1="350" y1="150" x2="440" y2="150" stroke="#0284c7" stroke-width="4"/>
      <line x1="760" y1="150" x2="850" y2="150" stroke="#d97706" stroke-width="4"/>
      <line x1="1130" y1="150" x2="1210" y2="150" stroke="#16a34a" stroke-width="4"/>
    </g>
  </svg>
</div>""",
                    "focus": [0, 0, 0, 0, 0],
                    "say": "Nhìn lên sơ đồ kiến trúc an ninh bốn tầng. Bước một, ứng dụng di động quét khuôn mặt và kiểm tra độ sống ba chiều. Bước hai, cổng sinh trắc học đối soát dữ liệu qua đường truyền bảo mật hai chiều. Bước ba, động cơ điều phối kiểm tra vé xác thực trước khi hạch toán. Bước bốn, hệ thống lõi và cổng chuyển mạch hoàn tất giao dịch an toàn."
                },
                {
                    "clear": True,
                    "show": """<table class="t">
  <tr><th>công nghệ bảo mật</th><th>nguyên lý hoạt động</th><th>vai trò trong ngân hàng</th></tr>
  <tr><td>Liveness Detection</td><td>Phân tích phản xạ ánh sáng và chuyển động vi mô trên mặt</td><td>Chặn đứng ảnh in, màn hình video và mặt nạ cao su</td></tr>
  <tr><td>mTLS Authentication</td><td>Cả máy khách và máy chủ đều phải trình chứng chỉ số SSL</td><td>Chống tấn công nghe lén Man in the middle trên đường truyền</td></tr>
  <tr><td>SAGA Pre-condition</td><td>Không bao giờ phát sinh lệnh trừ tiền nếu chưa có vé hợp lệ</td><td>Bảo đảm không kẻ gian nào có thể gọi lậu API chuyển tiền</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Bảng tổng hợp làm rõ ba trụ cột bảo mật không thể tách rời. Công nghệ kiểm tra độ sống ngăn ngừa hoàn toàn các thủ đoạn dùng ảnh in hay mặt nạ. Giao thức bảo mật hai chiều bảo vệ đường truyền dữ liệu không bị nghe lén. Điều kiện tiên quyết bảo đảm không ai có thể gọi lậu vào hệ thống hạch toán ngân hàng."
                }
            ]
        },
        # 4. SYMBOL
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Cấu trúc Vé Xác thực Sinh trắc học Biometric Ticket",
            "steps": [
                {
                    "show": """<p><b>Đặc tả vé xác thực sinh trắc học được ký điện tử mã hóa</b>:</p>
<div class="box code"><code>{<br/>
&nbsp;&nbsp;"ticket_id": "bio_sec_893412",<br/>
&nbsp;&nbsp;"cif": "10098234",<br/>
&nbsp;&nbsp;"id_card_no": "079096001234",<br/>
&nbsp;&nbsp;"match_score": 0.965,<br/>
&nbsp;&nbsp;"liveness_passed": true,<br/>
&nbsp;&nbsp;"expires_at": 1730948400<br/>
}</code></div>
<div class="box key">Nguyên lý an toàn: Vé có thời hạn hiệu lực tối đa $3$ phút và chỉ được dùng duy nhất một lần (One-Time Ticket)!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Đây là cấu trúc vé xác thực sinh trắc học được ký điện tử trong hệ thống. Vé lưu trữ mã khách hàng, độ khớp khuôn mặt và kết quả kiểm tra độ sống. Vé chỉ có hiệu lực trong vòng ba phút và bị huỷ ngay sau khi giao dịch hoàn tất."
                }
            ]
        },
        # 5. EXAMPLE
        {
            "id": "example",
            "kind": "example",
            "title": "Quy trình xác thực giao dịch năm mươi triệu đồng thực tế",
            "checks": [
                "50000000 > 10000000",
                "180 - 150 == 30",
                "450 < 1000"
            ],
            "steps": [
                {
                    "show": """<p><b>Bước 1 — Người dùng tạo lệnh chuyển tiền 50 triệu đồng</b>:</p>
<div class="box key">Khách hàng nhập số tiền $50\\,000\\,000$ VND trên ứng dụng ACB One.<br/>
Hệ thống kiểm tra số tiền lớn hơn ngưỡng $10\\,000\\,000$ VND.<br/>
Cổng thanh toán yêu cầu người dùng mở camera quét khuôn mặt sống 3D.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước một, khách hàng tạo lệnh chuyển tiền 50 triệu đồng trên ứng dụng. Cổng dịch vụ nhận thấy số tiền vượt ngưỡng mười triệu đồng theo quy định. Ứng dụng lập tức yêu cầu khách hàng đưa khuôn mặt vào khung hình quét trực tiếp."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Kiểm tra độ sống Liveness Detection và so khớp Căn cước</b>:</p>
<div class="box key">SDK phân tích chuyển động mắt và vi biểu cảm khuôn mặt: Đạt chuẩn $96.5\\%$.<br/>
Dữ liệu đặc trưng được gửi qua kết nối mTLS sang Cổng định danh dân cư.<br/>
Hệ thống xác nhận khuôn mặt trùng khớp hoàn toàn với ảnh lưu trong chip CCCD!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước hai, bộ công cụ phân tích độ sống xác nhận người đang quét là thực thể sống. Dữ liệu khuôn mặt được mã hóa và gửi qua đường truyền bảo mật tới cổng định danh. Kết quả xác nhận trùng khớp hoàn toàn với ảnh lưu trên chíp căn cước."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 3 — Sinh vé xác thực và gửi kèm lệnh chuyển tiền SAGA</b>:</p>
<table class="t">
  <tr><th>tham số lệnh</th><th>giá trị kiểm tra</th><th>trạng thái an ninh</th></tr>
  <tr><td>Mã vé Ticket ID</td><td>bio_sec_893412</td><td>Hợp lệ và chưa từng sử dụng</td></tr>
  <tr><td>Thời gian hiệu lực</td><td>Còn 150 giây</td><td>Chưa bị hết hạn</td></tr>
  <tr><td>Điểm số khớp mặt</td><td>0.965 (Ngưỡng &gt; 0.85)</td><td>Đạt chuẩn an ninh tối cao</td></tr>
</table>
<div class="box key">Động cơ SAGA xác thực vé thành công, cho phép kích hoạt trích nợ Core T24!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước ba, cổng an ninh sinh vé điện tử gửi kèm theo yêu cầu giao dịch. Động cơ điều phối kiểm tra vé còn hiệu lực và chưa từng được sử dụng trước đây. Khi điều kiện tiên quyết được thỏa mãn, lệnh trừ tiền mới được phát hành sang Core T24."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 4 — Hoàn tất chuyển tiền liên ngân hàng qua NAPAS</b>:</p>
<div class="box key">Tổng thời gian toàn trình từ lúc quét mặt đến khi nhận tiền: <b>$450$ mili giây</b>.<br/>
Giao dịch thành công mỹ mãn, khách hàng nhận thông báo số dư ngay lập tức.<br/>
Ngân hàng bảo vệ an toàn tuyệt đối số tiền $50$ triệu đồng của khách hàng!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước bốn, cổng chuyển mạch hoàn tất việc chuyển tiền sang ngân hàng thụ hưởng. Toàn bộ quy trình chỉ tiêu tốn 450 mi li giây, mang lại trải nghiệm mượt mà. Số tiền 50 triệu đồng của khách hàng được bảo vệ an toàn tuyệt đối."
                }
            ]
        },
        # 6. CHECK
        {
            "id": "check",
            "kind": "check",
            "title": "Kiểm tra xử lý tình huống tấn công vượt rào bypass khuôn mặt",
            "checks": [
                "450 < 1500",
                "100 - 99 == 1"
            ],
            "steps": [
                {
                    "show": """<p><b>Tình huống phỏng vấn</b>: Hacker dùng phần mềm can thiệp vào điện thoại để bỏ qua bước quét khuôn mặt và gọi thẳng API chuyển tiền. Hệ thống của bạn ngăn chặn thế nào?</p>
<table class="t">
  <tr><th>hệ thống yếu kém</th><th>hạ tầng kiên cố chuẩn Senior ACB</th></tr>
  <tr><td>Tin tưởng cờ xác thực gửi từ ứng dụng di động</td><td>Kiểm tra chữ ký số của vé sinh trắc học tại Backend</td></tr>
  <tr><td>Bị hacker rút sạch tiền tài khoản khách</td><td>Truy vấn bộ nhớ đệm xác minh tính duy nhất của vé</td></tr>
  <tr><td>Gây khủng hoảng uy tín thương hiệu</td><td>Chặn đứng giao dịch ngay tại tầng Gateway và báo động an ninh</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Ta kiểm tra tình huống thực tế khi tin tặc can thiệp mã nguồn ứng dụng để bỏ qua bước quét mặt. Do hệ thống yếu kém chỉ tin vào cờ gửi từ máy khách, kẻ gian có thể rút sạch tiền trong tài khoản. Bởi vì điều này gây ra hậu quả vô cùng nghiêm trọng cho ngân hàng."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Quy tắc Zero Trust</b>: Backend ngân hàng tuyệt đối không bao giờ tin tưởng máy khách di động! Mọi lệnh chuyển tiền giá trị lớn nếu thiếu vé xác thực sinh trắc học hợp lệ từ máy chủ bảo mật đều bị từ chối thẳng thừng tại API Gateway với mã lỗi <b>403 Forbidden</b>.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Do đó, hạ tầng ngân hàng luôn áp dụng nguyên tắc không bao giờ tin tưởng máy khách. Mọi yêu cầu chuyển tiền thiếu chữ ký số hợp lệ đều bị chặn đứng ngay lập tức tại cổng đón nhận. Nhờ vậy, tài sản của khách hàng luôn được bảo vệ an toàn tuyệt đối."
                }
            ]
        },
        # 7. PITFALL
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Ba sai lầm nghiêm trọng trong triển khai sinh trắc học ngân hàng",
            "steps": [
                {
                    "show": """<table class="t">
  <tr><th>sai lầm sơ cấp</th><th>hậu quả kỹ thuật & tài chính</th><th>giải pháp chuẩn Senior</th></tr>
  <tr><td>Quét mặt sau khi đã trừ tiền</td><td>Trừ tiền thành công nhưng khách quét mặt thất bại $\to$ Bị giam tiền</td><td>Đặt sinh trắc học làm điều kiện tiên quyết trước hạch toán</td></tr>
  <tr><td>Tái sử dụng vé xác thực sinh trắc học</td><td>Kẻ gian bắt gói tin cũ và thực hiện lệnh chuyển tiền lậu</td><td>Vé chỉ được dùng một lần duy nhất và hết hạn sau 3 phút</td></tr>
  <tr><td>Không có cơ chế thử lại khi nghẽn mạng</td><td>Khách hàng không chuyển được tiền trong giờ cao điểm</td><td>Tối ưu hóa bộ đệm phiên và đường truyền chuyên dụng</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Có ba sai lầm chí mạng cần tránh khi làm sinh trắc học. Thứ nhất là trừ tiền trước khi quét mặt khiến tiền của khách bị giam vô lý khi quét lỗi. Thứ hai là để vé xác thực bị dùng lại tạo lỗ hổng cho tin tặc. Thứ ba là thiếu cơ chế đường truyền dự phòng khiến hệ thống bị treo nghẽn khi quá tải."
                }
            ]
        },
        # 8. QUIZ
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Thử thách kiến trúc bảo mật ngân hàng mở tại ACB",
            "checks": [
                "403 - 400 == 3",
                "2345 - 2000 == 345"
            ],
            "steps": [
                {
                    "pause": 15,
                    "show": """<p><b>Câu hỏi trắc nghiệm kiến trúc</b>: Theo quy định an ninh ngân hàng, tại sao bước xác thực sinh trắc học khuôn mặt phải được đặt làm Điều kiện Tiên quyết (Pre-condition) trong luồng SAGA thay vì là một bước song song?</p>
<ul>
  <li><b>A</b>: Vì nếu trừ tiền trước hoặc làm song song, khi xác thực khuôn mặt thất bại, tài khoản khách hàng đã bị trừ tiền và ngân hàng phải thực hiện bồi hoàn phức tạp.</li>
  <li><b>B</b>: Vì máy chủ không thể chạy đa luồng.</li>
  <li><b>C</b>: Vì Core T24 không hỗ trợ giao thức HTTP.</li>
  <li><b>D</b>: Vì thẻ căn cước công dân sẽ bị khóa nếu chạy song song.</li>
</ul>""",
                    "focus": [0, 0, 0],
                    "say": "Hãy cùng bước vào câu hỏi trắc nghiệm kiến trúc thực chiến của ACB. Tại sao bước sinh trắc học bắt buộc phải là điều kiện tiên quyết trong luồng giao dịch? Bạn có 15 giây suy nghĩ trước khi nghe đáp án chuẩn xác."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Đáp án chính xác là A</b>!</div>
<p><b>Bước 1 — Nguyên lý bảo toàn số dư tài khoản</b>:</p>
<p>Trong giao dịch tài chính, việc trích nợ tài khoản là bước thay đổi trạng thái có tính chất trọng yếu nhất. Không bao giờ được phép trích nợ khi người thực hiện chưa được chứng minh là chủ tài khoản hợp pháp.</p>""",
                    "focus": [0, 0],
                    "say": "Đáp án chính xác là phương án A. Bước một, việc trích nợ là hành động làm thay đổi tài sản của khách hàng nên chỉ được diễn ra khi danh tính đã được xác thực an toàn."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Giảm thiểu rủi ro bồi hoàn và sai lệch sổ cái</b>:</p>
<div class="box key">Nếu cho phép chạy song song hoặc trừ tiền trước, khi người dùng quét mặt hỏng (do trời tối hoặc góc nghiêng), hệ thống phải kích hoạt giao dịch bù trừ (Compensating Transaction) rất tốn kém và gây hoang mang cho người dùng. Đặt làm điều kiện tiên quyết giúp hệ thống luôn an toàn và sạch sẽ!</div>""",
                    "focus": [0, 0],
                    "say": "Bước hai, nếu trừ tiền trước, việc quét mặt hỏng sẽ buộc ngân hàng phải chạy quy trình hoàn tiền phức tạp. Đặt sinh trắc học làm điều kiện tiên quyết giúp luồng giao dịch luôn an toàn tuyệt đối."
                }
            ]
        },
        # 9. RECAP
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Sinh trắc học Quyết định 2345",
            "steps": [
                {
                    "show": """<div class="chain">
  <span>Kiểm tra ngưỡng tiền trên 10 triệu</span> &rarr;
  <span>Quét khuôn mặt 3D Liveness Detection</span> &rarr;
  <span>So khớp chíp CCCD qua kết nối mTLS</span> &rarr;
  <span>Sinh vé xác thực điện tử một lần</span> &rarr;
  <span>Điều kiện tiên quyết SAGA Pre-condition</span> &rarr;
  <span>Hạch toán Core T24 và NAPAS an toàn</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>trụ cột kỹ thuật</th><th>giá trị bảo vệ tài chính</th></tr>
  <tr><td>Liveness Detection 3D</td><td>Triệt tiêu 100% rủi ro Deepfake và giả mạo danh tính</td></tr>
  <tr><td>SAGA Pre-condition Gate</td><td>Bảo đảm không bao giờ trích nợ khi danh tính chưa hợp lệ</td></tr>
</table>
<p style="margin-top: 15px;"><b>Khẳng định đẳng cấp Senior tại ngân hàng ACB</b>: Nắm vững quy định 2345, làm chủ công nghệ sinh trắc học ngân hàng số và tự tin đàm phán mức lương 50 triệu gross.</p>""",
                    "focus": [0, 0],
                    "say": "Tóm lại, chuỗi logic gồm kiểm tra hạn mức, quét khuôn mặt sống, so khớp căn cước công dân, cấp vé một lần và điều phối hạch toán an toàn. Nắm vững giải pháp này, bạn hoàn toàn tự tin dẫn dắt các bài toán chuyển đổi số lớn và đàm phán mức lương 50 triệu gross tại ACB."
                }
            ]
        }
    ]
}

with open("lessons/acb/L06_sinh_trac_hoc_qd2345_va_bao_mat_ngan_hang.yaml", "w", encoding="utf-8") as f:
    yaml.dump(lesson, f, allow_unicode=True, sort_keys=False, width=1000)

print("Created lessons/acb/L06_sinh_trac_hoc_qd2345_va_bao_mat_ngan_hang.yaml successfully")
