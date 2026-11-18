import yaml

lesson = {
    "id": "L02",
    "course": "ACB",
    "series": "Phỏng vấn Kỹ sư Tích hợp ACB",
    "title": "Bài 2 — Chuyển mạch Thanh toán Liên ngân hàng NAPAS 247: ISO 8583 và Socket TCP",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "curriculum/acb.yaml L02; Chuẩn kết nối NAPAS 247 ISO 8583 v2.0; PCI-DSS Payment Security Standard; Tài liệu kiến trúc Cổng thanh toán ACB 2026",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Hiểu sâu cấu trúc bản tin ISO 8583 MTI 0200 và 0210 qua TCP Socket nhị phân",
        "Bảo mật giải mã PIN Block qua phần cứng HSM và mã hóa MAC bit 128",
        "Triển khai khử trùng lặp phân tán và quy trình đối soát 3 bên cuối ngày"
    ],
    "scenes": [
        # 1. HOOK
        {
            "id": "hook",
            "kind": "hook",
            "title": "Huyết mạch thanh toán liên ngân hàng và tiêu chuẩn bảo mật khắt khe",
            "steps": [
                {
                    "show": """<p>Mỗi khi bạn chuyển tiền nhanh 247 trên ứng dụng ngân hàng, tiền bay sang tài khoản ngân hàng khác chỉ trong vài giây.</p>
<div class="box key">Đứng sau kỳ tích đó là <b>Cổng thanh toán NAPAS 247</b>, xử lý hàng triệu bản tin <b>ISO 8583</b> qua đường truyền <b>Socket TCP nhị phân</b>.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Chào bạn, khi bạn chuyển tiền nhanh trên ứng dụng di động, tiền sang ngay tài khoản người nhận chỉ sau vài giây. Phía sau sự mượt mà đó là cả một hệ sinh thái chuyển mạch liên ngân hàng NAPAS 247 chạy liên tục suốt ngày đêm. Từng giao dịch đều được đóng gói bằng bản tin ISO 8583 nhị phân và gửi qua đường truyền TCP chuyên dụng."
                },
                {
                    "show": """<p>Hôm nay, ta mổ xẻ: <b>Cấu trúc bản tin MTI 0200 và 0210</b>, <b>giải mã PIN Block qua thiết bị phần cứng HSM</b>, và <b>cơ chế khử trùng lặp loại trừ nguy cơ trừ tiền hai lần</b>.</p>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Hôm nay ta sẽ cùng giải mã toàn diện kiến trúc cổng NAPAS 247. Ta tìm hiểu cấu trúc gói tin chuẩn mực và cơ chế bảo mật phần cứng qua thiết bị HSM. Ta cũng nắm vững giải pháp khử trùng lặp đạt chuẩn Senior. Đây là những chủ đề then chốt giúp bạn ghi điểm tuyệt đối tại ACB."
                }
            ]
        },
        # 2. PREREQ
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Bản tin ISO 8583, mã định danh STAN và mã tham chiếu RRN",
            "checks": [
                "8000 * 60 == 480000 and 480000 * 60 == 28800000",
                "1500 - 120 == 1380 and 120 + 1380 == 1500"
            ],
            "steps": [
                {
                    "show": """<p><b>Ba khái niệm cốt lõi của chuẩn thanh toán liên ngân hàng ISO 8583</b>:</p>
<table class="t">
  <tr><th>khái niệm</th><th>định nghĩa</th><th>vai trò trong giao dịch</th></tr>
  <tr><td>MTI</td><td>Message Type Identifier (4 chữ số)</td><td>xác định loại bản tin yêu cầu 0200 hoặc phản hồi 0210</td></tr>
  <tr><td>STAN</td><td>System Trace Audit Number (6 chữ số)</td><td>mã vết kiểm toán duy nhất do ngân hàng khởi tạo</td></tr>
  <tr><td>RRN</td><td>Retrieval Reference Number (12 chữ số)</td><td>mã tham chiếu toàn cầu để tra soát và đối soát</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Trước tiên ta ôn lại ba khái niệm cốt lõi của chuẩn thanh toán liên ngân hàng. Mã loại bản tin gồm 4 chữ số giúp phân biệt lệnh yêu cầu tài chính và kết quả phản hồi. Mã vết kiểm toán là chuỗi 6 số do hệ thống phát hành sinh ra để theo dõi tiến trình. Mã tham chiếu là chuỗi 12 ký tự được dùng làm căn cứ đối soát giữa các ngân hàng."
                },
                {
                    "show": """<div class="box key">Ở thông lượng $8\,000$ giao dịch mỗi giây: Mỗi phút có $8\,000 \times 60 = 480\,000$ lệnh. Nếu độ trễ mạng là $120$ ms, thời gian dư dả so với hạn mức tối đa $1500$ ms là $1500 - 120 = 1380$ ms.</div>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Ta xem xét chỉ số hiệu năng thực tế tại cổng liên ngân hàng. Tại mức 8 nghìn giao dịch mỗi giây, mỗi phút hệ thống tiếp nhận 480 nghìn bản tin. Với độ trễ trung bình 120 mi li giây, hệ thống phản hồi cực nhanh và hoàn toàn vượt xa hạn ngạch 1500 mi li giây của mạng thanh toán. Khoảng thời gian an toàn lên tới 1380 mi li giây."
                }
            ]
        },
        # 3. CONCEPT
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kiến trúc Luồng Thanh toán Cổng NAPAS 247 qua Socket TCP",
            "steps": [
                {
                    "show": """<div>
  <svg width="1500" height="380" viewBox="0 0 1500 380">
    <g font-size="22" fill="#1f2937">
      <text x="750" y="35" text-anchor="middle" font-weight="bold" font-size="26">Kiến trúc Tích hợp Luồng Chuyển tiền NAPAS 247</text>
      <rect x="50" y="70" width="300" height="240" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
      <text x="200" y="115" text-anchor="middle" font-weight="bold">1. Digital Channel</text>
      <text x="200" y="160" text-anchor="middle">Ứng dụng ACB One</text>
      <text x="200" y="200" text-anchor="middle">Sinh mã giao dịch</text>
      <text x="200" y="240" text-anchor="middle">Xác thực sinh trắc học</text>

      <rect x="440" y="70" width="320" height="240" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>
      <text x="600" y="115" text-anchor="middle" font-weight="bold">2. NAPAS Gateway</text>
      <text x="600" y="160" text-anchor="middle">Bộ nhớ đệm khử trùng lặp</text>
      <text x="600" y="200" text-anchor="middle">Mã hóa MAC bit 128</text>
      <text x="600" y="240" text-anchor="middle">Dịch mã PIN qua HSM</text>

      <rect x="850" y="70" width="280" height="240" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
      <text x="990" y="115" text-anchor="middle" font-weight="bold">3. NAPAS Switch</text>
      <text x="990" y="160" text-anchor="middle">Socket TCP nhị phân</text>
      <text x="990" y="200" text-anchor="middle">Định tuyến liên ngân hàng</text>
      <text x="990" y="240" text-anchor="middle">Bản tin ISO 8583 0200</text>

      <rect x="1210" y="70" width="250" height="240" rx="12" fill="#f3e8ff" stroke="#9333ea" stroke-width="3"/>
      <text x="1335" y="115" text-anchor="middle" font-weight="bold">4. Core Banking</text>
      <text x="1335" y="160" text-anchor="middle">Hạch toán ghi nợ tức thì</text>
      <text x="1335" y="200" text-anchor="middle">Cập nhật số dư sổ cái</text>
      <text x="1335" y="240" text-anchor="middle">Bảo toàn dòng tiền</text>

      <line x1="350" y1="150" x2="440" y2="150" stroke="#0284c7" stroke-width="4"/>
      <line x1="760" y1="150" x2="850" y2="150" stroke="#d97706" stroke-width="4"/>
      <line x1="990" y1="310" x2="990" y2="340" stroke="#16a34a" stroke-width="4"/>
      <line x1="990" y1="340" x2="1335" y2="340" stroke="#16a34a" stroke-width="4"/>
      <line x1="1335" y1="340" x2="1335" y2="310" stroke="#16a34a" stroke-width="4"/>
    </g>
  </svg>
</div>""",
                    "focus": [0, 0, 0, 0, 0],
                    "say": "Nhìn lên sơ đồ luồng dữ liệu liên ngân hàng. Bước một, ứng dụng số nhận yêu cầu chuyển tiền và xác thực sinh trắc học của khách hàng. Bước hai, Cổng thanh toán kiểm tra khoá khử trùng lặp và chuyển mã PIN vào thiết bị phần cứng để mã hoá an toàn. Bước ba, bản tin ISO 8583 hoàn chỉnh được chuyển qua kênh truyền nhị phân đến cổng chuyển mạch. Bước bốn, hệ thống cập nhật sổ cái Core Banking và phản hồi kết quả thành công cho người gửi."
                }
            ]
        },
        # 4. SYMBOL
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Giải mã các trường dữ liệu quan trọng trong bản tin ISO 8583",
            "steps": [
                {
                    "show": """<p><b>Các trường dữ liệu (Data Elements) bắt buộc của bản tin MTI 0200</b>:</p>
<table class="t">
  <tr><th>trường dữ liệu</th><th>tên gọi kỹ thuật</th><th>nội dung nghiệp vụ</th></tr>
  <tr><td>Field 3</td><td>Processing Code</td><td>mã giao dịch (chuyển khoản từ tài khoản đến tài khoản)</td></tr>
  <tr><td>Field 4</td><td>Transaction Amount</td><td>số tiền giao dịch thể hiện theo đơn vị đồng</td></tr>
  <tr><td>Field 11</td><td>STAN (Audit Trail)</td><td>mã số vết kiểm toán 6 số nhận diện phiên gửi</td></tr>
  <tr><td>Field 37</td><td>Retrieval Ref Number</td><td>mã tham chiếu toàn cầu 12 số dùng đối soát</td></tr>
  <tr><td>Field 52</td><td>PIN Block Data</td><td>mã PIN được mã hóa dưới dạng khối nhị phân 8 byte</td></tr>
  <tr><td>Field 128</td><td>Message Auth Code</td><td>chữ ký toàn vẹn bản tin MAC chống giả mạo</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0, 0, 0],
                    "say": "Bản tin ISO 8583 bao gồm các trường dữ liệu được đánh số chuẩn quốc tế. Trường số ba xác định nghiệp vụ chuyển tiền giữa hai tài khoản ngân hàng. Trường số bốn mang số tiền của giao dịch. Trường số 11 và trường số 37 tạo thành cặp mã định danh không thể trùng lặp. Trường số 52 chứa khối mã PIN đã được bảo vệ bằng mã hóa phần cứng. Cuối cùng, trường 128 là mã xác thực toàn vẹn giúp phát hiện mọi can thiệp giả mạo."
                }
            ]
        },
        # 5. EXAMPLE
        {
            "id": "example",
            "kind": "example",
            "title": "Tính toán khả năng tải và thời gian sống khoá khử trùng lặp",
            "checks": [
                "8000 * 12 // 100 == 960",
                "60 * 1000 == 60000",
                "8000 + 4000 == 12000"
            ],
            "steps": [
                {
                    "show": """<p><b>Bước 1 — Tính số giao dịch đồng thời trên Socket TCP (Little's Law)</b>:</p>
<div class="box key">Định luật Little: $L = N \\times W$.<br/>
Với thông lượng $N = 8\,000$ lệnh/giây, thời gian phản hồi $W = 120$ ms $= 0{,}12$ giây.<br/>
Số kết nối đồng thời trung bình: $L = 8\,000 \\times 0{,}12 = 960$ kết nối.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước một, ta tính toán số lượng giao dịch hoạt động đồng thời trên đường truyền nhị phân. Áp dụng định luật Lít-tơn với lưu lượng 8 nghìn lệnh mỗi giây và độ trễ 120 mi li giây, ta có 960 giao dịch đồng thời. Do đó, tầng mạng cần quản lý một nhóm gồm ít nhất 960 kết nối hoạt động song song để không nghẽn dữ liệu."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Cấu hình khoá khử trùng lặp trong bộ nhớ đệm phân tán</b>:</p>
<table class="t">
  <tr><th>thông số cấu hình</th><th>giá trị thiết lập</th><th>lý do kỹ thuật</th></tr>
  <tr><td>Cấu trúc khoá</td><td><code>napas:dedup:{stan}:{rrn}</code></td><td>kết hợp mã vết và mã tham chiếu duy nhất</td></tr>
  <tr><td>Thời gian sống TTL</td><td>$60$ giây $= 60\,000$ ms</td><td>vượt xa thời gian chờ tối đa của mạng chuyển mạch</td></tr>
  <tr><td>Lệnh thực thi nguyên tử</td><td><code>SET ... NX EX 60</code></td><td>chỉ ghi thành công nếu khoá chưa từng tồn tại</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Bước hai, ta thiết lập khoá khử trùng lặp trong bộ nhớ đệm phân tán. Vì mạng viễn thông có thể gửi lại gói tin bị chậm, ta kết hợp mã vết và mã tham chiếu thành một khoá duy nhất. Do thời gian chờ của đối tác là 30 giây, ta đặt thời gian sống của khoá là 60 giây, tương đương 60 nghìn mi li giây để ngăn chặn tuyệt đối lỗi trừ tiền kép."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 3 — Dự phòng khả năng mở rộng vào giờ cao điểm</b>:</p>
<div class="box key">Hệ số dự phòng an toàn tải cao điểm: $1{,}5$.<br/>
Công suất thiết kế của cụm Gateway: $8\,000 \\times 1{,}5 = 8\,000 + 4\,000 = 12\,000$ giao dịch mỗi giây. Đảm bảo vận hành trơn tru trong dịp lễ Tết.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước ba, ta tính toán công suất dự phòng cho các đợt cao điểm lễ Tết. Nhân lưu lượng cơ sở với hệ số an toàn 1 phẩy 5, hệ thống được thiết kế để gánh tới 12 nghìn lệnh mỗi giây. Nhờ đó, cụm phân tán của ngân hàng luôn giữ vững độ ổn định dưới mọi đợt sóng giao dịch lớn."
                }
            ]
        },
        # 6. CHECK
        {
            "id": "check",
            "kind": "check",
            "title": "Kiểm tra xử lý tình huống mất kết nối mạng liên ngân hàng",
            "checks": [
                "1500 // 1000 == 1 and 1500 % 1000 == 500",
                "10000000 - 0 == 10000000"
            ],
            "steps": [
                {
                    "show": """<p><b>Tình huống phỏng vấn</b>: Gửi lệnh chuyển tiền 10 triệu đồng sang ngân hàng bạn. Socket TCP bị đứt giữa chừng và quá 1500 ms không nhận được bản tin 0210. Bạn xử lý thế nào?</p>
<table class="t">
  <tr><th>hành động sai lầm</th><th>hành động chuẩn mực Senior</th></tr>
  <tr><td>Báo giao dịch thất bại cho khách</td><td>Chuyển trạng thái giao dịch sang IN_DOUBT (nghi vấn)</td></tr>
  <tr><td>Tự động hoàn tiền hoặc trừ tiền lại</td><td>Kích hoạt tiến trình tra vấn trạng thái định kỳ</td></tr>
  <tr><td>Gây thất thoát 10 triệu đồng của ngân hàng</td><td>Đối soát tự động với tập tin quyết toán cuối ngày</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Ta kiểm tra tình huống kinh điển khi đường truyền vật lý bị đứt quãng khiến yêu cầu vượt quá hạn mức 1500 mi li giây. Do đối tác chưa xác nhận nhận được tiền, việc báo lỗi thất bại ngay lập tức là một sai lầm rất lớn. Nếu ngân hàng tự ý hoàn tiền trong khi đầu bên kia đã ghi có thành công, ngân hàng sẽ mất trắng 10 triệu đồng."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Quy tắc bảo toàn dòng tiền</b>: Vì kết quả mạng chưa rõ ràng, ta chuyển trạng thái sang nghi vấn. Hệ thống tự động gửi bản tin truy vấn trạng thái. Do đó, mọi khoản tiền 10 triệu đồng đều được bảo toàn nguyên vẹn và khớp đúng 100 phần trăm qua đối soát.</div>""",
                    "focus": [0, 0],
                    "say": "Vì kết quả mạng chưa thể xác định, ta lập tức chuyển lệnh sang trạng thái nghi vấn. Do tiến trình tự động sẽ truy vấn lại với cổng chuyển mạch, ngân hàng luôn bảo đảm an toàn tuyệt đối cho dòng tiền của khách hàng."
                }
            ]
        },
        # 7. PITFALL
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Ba sai lầm nghiêm trọng trong an toàn thanh toán liên ngân hàng",
            "steps": [
                {
                    "show": """<table class="t">
  <tr><th>sai lầm sơ cấp</th><th>hậu quả bảo mật & vận hành</th><th>giải pháp chuẩn Senior</th></tr>
  <tr><td>Ghi mã PIN rõ ràng vào tệp log</td><td>vi phạm nghiêm trọng chuẩn bảo mật PCI-DSS</td><td>mã hoá PIN Block và che giấu dữ liệu tuyệt đối</td></tr>
  <tr><td>Bỏ qua kiểm tra mã MAC bit 128</td><td>nguy cơ bị kẻ xấu giả mạo và sửa đổi số tiền</td><td>xác thực chữ ký phần cứng trước khi xử lý</td></tr>
  <tr><td>Không đối soát tập tin quyết toán EOD</td><td>lệch sổ cái ngân hàng mà không thể truy cứu</td><td>chạy đối soát tự động ba bên vào cuối ngày</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Có ba sai lầm chết người trong an toàn thanh toán liên ngân hàng. Thứ nhất là vô tình ghi mã PIN thô vào nhật ký hệ thống làm vi phạm tiêu chuẩn bảo mật quốc tế. Thứ hai là bỏ qua việc kiểm tra mã xác thực tin nhắn khiến kẻ xấu có thể can thiệp số tiền trên đường truyền. Thứ ba là thiếu quy trình đối soát tự động cuối ngày khiến các khoản tiền lệch sổ cái bị bỏ sót."
                }
            ]
        },
        # 8. QUIZ
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Thử thách bảo mật phần cứng tại ngân hàng ACB",
            "checks": [
                "128 // 8 == 16",
                "5000000 * 2 == 10000000"
            ],
            "steps": [
                {
                    "pause": 15,
                    "show": """<p><b>Câu hỏi trắc nghiệm kiến trúc</b>: Tại sao mã PIN của chủ thẻ bắt buộc phải được dịch mã (PIN Translation) bên trong thiết bị phần cứng chuyên dụng HSM mà không được xử lý bằng code Java trên máy chủ thông thường?</p>
<ul>
  <li><b>A</b>: Vì thiết bị HSM có vùng nhớ phần cứng tự huỷ khi bị can thiệp vật lý, bảo vệ an toàn tuyệt đối các khóa mật mã.</li>
  <li><b>B</b>: Vì máy chủ Java không thể tính toán được các phép toán nhị phân.</li>
  <li><b>C</b>: Vì thiết bị HSM giúp giảm độ trễ mạng xuống bằng 0.</li>
  <li><b>D</b>: Vì giao thức TCP chỉ tương thích với thiết bị phần cứng.</li>
</ul>""",
                    "focus": [0, 0, 0],
                    "say": "Hãy cùng bước vào thử thách bảo mật chuyên sâu của ACB. Tại sao mã PIN của chủ thẻ bắt buộc phải được dịch mã bên trong thiết bị bảo mật phần cứng chuyên dụng thay vì dùng mã lệnh thông thường? Bạn có 15 giây suy nghĩ trước khi nghe lời giải thích chi tiết."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Đáp án chính xác là A</b>!</div>
<p><b>Bước 1 — Cơ chế bảo vệ vật lý của thiết bị phần cứng HSM</b>:</p>
<p>Thiết bị phần cứng HSM lưu trữ các khóa mật mã trong vùng nhớ bảo vệ nghiêm ngặt. Nếu có bất kỳ sự can thiệp vật lý hay cố gắng trích xuất bộ nhớ, mạch bảo vệ sẽ tự huỷ khóa mã hóa ngay lập tức.</p>""",
                    "focus": [0, 0],
                    "say": "Đáp án chính xác là phương án A. Bước một, thiết bị phần cứng chuyên dụng có cơ chế tự bảo vệ và tự huỷ bộ nhớ nếu bị can thiệp trái phép, bảo đảm khoá bảo mật không bao giờ lọt ra ngoài."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Tuân thủ tiêu chuẩn quốc tế PCI-DSS</b>:</p>
<div class="box key">Quy định ngân hàng cấm mã PIN xuất hiện dưới dạng chuỗi rõ trong bộ nhớ máy chủ. Nhờ HSM, giao dịch 10 triệu đồng được mã hóa và chuyển mạch an toàn mà không hacker nào có thể đánh cắp.</div>""",
                    "focus": [0, 0],
                    "say": "Bước hai, tiêu chuẩn bảo mật ngân hàng bắt buộc mã PIN không bao giờ được lộ diện trong bộ nhớ máy chủ ứng dụng. Nhờ giải pháp phần cứng này, tiền của khách hàng luôn được bảo vệ an toàn tuyệt đối trước mọi nguy cơ."
                }
            ]
        },
        # 9. RECAP
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic cổng thanh toán liên ngân hàng NAPAS 247",
            "steps": [
                {
                    "show": """<div class="chain">
  <span>Đóng gói ISO 8583 0200</span> &rarr;
  <span>Xác thực MAC bit 128</span> &rarr;
  <span>Dịch mã PIN qua HSM</span> &rarr;
  <span>Khóa Redis khử trùng lặp</span> &rarr;
  <span>Hạch toán Core Banking</span> &rarr;
  <span>Đối soát 3 bên tự động</span>
</div>
<p style="margin-top: 15px;"><b>Hành trang vững vàng cho vị trí Senior Integration Engineer</b>: Làm chủ bản tin ISO 8583, hiểu thấu an ninh phần cứng HSM, chặn đứng trừ tiền kép và tự tin chinh phục mức lương 50 triệu gross tại ACB.</p>""",
                    "focus": [0, 0],
                    "say": "Tóm lại, chuỗi logic cổng NAPAS gồm đóng gói bản tin, kiểm tra tính toàn vẹn, dịch mã bảo mật phần cứng, khử trùng lặp và đối soát sổ cái. Nắm vững bản chất này, bạn hoàn toàn làm chủ vị trí Kỹ sư Tích hợp Cấp cao và tự tin thương lượng mức thu nhập 50 triệu gross tại ngân hàng ACB."
                }
            ]
        }
    ]
}

with open("lessons/acb/L02_chuyen_mach_napas_iso8583.yaml", "w", encoding="utf-8") as f:
    yaml.dump(lesson, f, allow_unicode=True, sort_keys=False, width=1000)

print("Created lessons/acb/L02_chuyen_mach_napas_iso8583.yaml successfully!")
