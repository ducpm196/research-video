import yaml

lesson = {
    "id": "L04",
    "course": "ACB",
    "series": "Phỏng vấn Kỹ sư Tích hợp ACB",
    "title": "Bài 4 — Sàn Chuyển nhượng Hợp đồng Tiền gửi: Khóa Lạc quan và Máy Trạng thái T24",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "curriculum/acb.yaml L04; Kiến trúc Sàn chuyển nhượng hợp đồng tiền gửi contract-transfer Go Fiber và PostgreSQL; Temenos T24 OFS Guide 2026",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Hiểu rõ nghiệp vụ chuyển nhượng sổ tiết kiệm thứ cấp và nguy cơ xung đột đồng thời",
        "Thiết kế cơ chế Khóa Lạc quan với trường thời điểm truy cập trên PostgreSQL",
        "Tích hợp bản tin T24 OFS đổi chủ sở hữu và xử lý ma trận mã lỗi treo lệnh"
    ],
    "scenes": [
        # 1. HOOK
        {
            "id": "hook",
            "kind": "hook",
            "title": "Bài toán hai khách hàng cùng bấm mua một sổ tiết kiệm trong cùng một tích tắc",
            "steps": [
                {
                    "show": """<p>Trên sàn chuyển nhượng số, một sổ tiết kiệm lãi suất cao được chào bán công khai.</p>
<div class="box key">Nếu hai người mua cùng bấm chấp nhận trong cùng một phần nghìn giây, làm sao hệ thống ngân hàng bảo đảm chỉ một người mua thành công mà không làm nghẽn cơ sở dữ liệu?</div>""",
                    "focus": [0, 0, 0],
                    "say": "Chào bạn, trên sàn ngân hàng số, một sổ tiết kiệm lãi suất cao được chào bán. Trong cùng một tích tắc, có thể nhiều người cùng bấm nút mua. Nếu không kiểm soát chính xác, ngân hàng có thể bán một sổ cho hai người."
                },
                {
                    "show": """<table class="t">
  <tr><th>kịch bản rủi ro</th><th>hậu quả tài chính</th><th>yêu cầu kỹ thuật</th></tr>
  <tr><td>Hai người mua cùng click đồng thời</td><td>Trừ tiền hai lần cho cùng một hợp đồng</td><td>Khóa Lạc quan với thời điểm truy cập</td></tr>
  <tr><td>Core Banking T24 bị sự cố mạng</td><td>Treo lệnh hoặc mất đồng bộ số dư</td><td>Máy trạng thái chuyển sang HOLD để đối soát</td></tr>
</table>
<p>Hôm nay, ta làm chủ: <b>Bản chất thị trường tiền gửi thứ cấp</b>, <b>kỹ thuật Khóa Lạc quan</b>, và <b>máy trạng thái Core Banking T24</b>.</p>""",
                    "focus": [0, 0, 0],
                    "say": "Hôm nay, ta cùng nhau giải mã toàn bộ bài toán thực chiến này. Ta tìm hiểu nghiệp vụ chuyển nhượng hợp đồng tiền gửi. Ta nắm vững kỹ thuật Khóa Lạc quan không gây bế tắc cơ sở dữ liệu."
                }
            ]
        },
        # 2. PREREQ
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Tiền gửi tiết kiệm có kỳ hạn, mã định danh CIF và số dư",
            "checks": [
                "100000000 * 7 // 100 == 7000000",
                "500000000 > 100000000"
            ],
            "steps": [
                {
                    "show": """<p><b>Ba khái niệm cốt lõi trong nghiệp vụ tiền gửi ngân hàng</b>:</p>
<table class="t">
  <tr><th>thuật ngữ</th><th>bản chất nghiệp vụ</th><th>đặc điểm kỹ thuật</th></tr>
  <tr><td>Term Deposit</td><td>hợp đồng tiền gửi có kỳ hạn định trước</td><td>hưởng lãi suất cố định nếu giữ đến ngày đáo hạn</td></tr>
  <tr><td>Mã CIF</td><td>mã định danh duy nhất của một khách hàng</td><td>liên kết toàn bộ tài khoản và sổ tiết kiệm của người đó</td></tr>
  <tr><td>Rút trước hạn</td><td>khách hàng rút vốn trước ngày đáo hạn</td><td>bị phạt hạ toàn bộ lãi suất về mức không kỳ hạn</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Trước tiên ta điểm lại ba khái niệm cốt lõi trong ngân hàng. Hợp đồng tiền gửi có kỳ hạn mang lại lãi suất cố định hấp dẫn. Mã CIF là mã định danh duy nhất của mỗi khách hàng trong sổ cái."
                },
                {
                    "show": """<div class="box key">Ví dụ: Khách hàng gửi $500$ triệu đồng kỳ hạn $12$ tháng với lãi suất $7\\%$. Tiền lãi dự kiến là $500 \\times 7\\% = 35$ triệu đồng. Nếu rút trước hạn ở tháng thứ $11$, tiền lãi chỉ còn khoảng $458$ nghìn đồng!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Ta xét một ví dụ thực tế. Khách hàng gửi 500 triệu đồng kỳ hạn một năm với lãi suất 7 phần trăm. Nếu rút trước hạn ở tháng thứ mười một, khách hàng bị mất trắng hơn 34 triệu đồng tiền lãi."
                }
            ]
        },
        # 3. CONCEPT
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kiến trúc Sàn Giao dịch Tiền gửi và Máy Trạng thái Chuyển nhượng",
            "steps": [
                {
                    "show": """<div>
  <svg width="1500" height="380" viewBox="0 0 1500 380">
    <g font-size="22" fill="#1f2937">
      <text x="750" y="35" text-anchor="middle" font-weight="bold" font-size="26">Kiến trúc Sàn Chuyển nhượng Hợp đồng Tiền gửi Thứ cấp</text>
      <rect x="50" y="70" width="300" height="240" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
      <text x="200" y="115" text-anchor="middle" font-weight="bold">1. Người mua</text>
      <text x="200" y="160" text-anchor="middle">Ứng dụng Mobile App</text>
      <text x="200" y="200" text-anchor="middle">Bấm chấp nhận mua sổ</text>
      <text x="200" y="240" text-anchor="middle">Gửi yêu cầu mua</text>

      <rect x="440" y="70" width="320" height="240" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>
      <text x="600" y="115" text-anchor="middle" font-weight="bold">2. Fiber API Gateway</text>
      <text x="600" y="160" text-anchor="middle">Khóa Lạc quan last_access</text>
      <text x="600" y="200" text-anchor="middle">Kiểm tra dòng tác động</text>
      <text x="600" y="240" text-anchor="middle">Từ chối xung đột 409</text>

      <rect x="850" y="70" width="280" height="240" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
      <text x="990" y="115" text-anchor="middle" font-weight="bold">3. PostgreSQL DB</text>
      <text x="990" y="160" text-anchor="middle">Cập nhật trạng thái</text>
      <text x="990" y="200" text-anchor="middle">Chuyển sang PROCESSING</text>
      <text x="990" y="240" text-anchor="middle">Bảo toàn tính nhất quán</text>

      <rect x="1210" y="70" width="250" height="240" rx="12" fill="#f3e8ff" stroke="#9333ea" stroke-width="3"/>
      <text x="1335" y="115" text-anchor="middle" font-weight="bold">4. Core T24 Engine</text>
      <text x="1335" y="160" text-anchor="middle">Bản tin OFS XML</text>
      <text x="1335" y="200" text-anchor="middle">Đổi CIF sở hữu sổ</text>
      <text x="1335" y="240" text-anchor="middle">Hạch toán hoàn tất</text>

      <line x1="350" y1="150" x2="440" y2="150" stroke="#0284c7" stroke-width="4"/>
      <line x1="760" y1="150" x2="850" y2="150" stroke="#d97706" stroke-width="4"/>
      <line x1="1130" y1="150" x2="1210" y2="150" stroke="#16a34a" stroke-width="4"/>
    </g>
  </svg>
</div>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Nhìn lên sơ đồ kiến trúc bốn tầng của sàn chuyển nhượng. Khách hàng bấm mua sổ trên ứng dụng di động. Cổng Fiber tiếp nhận và thực thi câu lệnh Khóa Lạc quan trên PostgreSQL. Sau khi khóa thành công, hệ thống gửi bản tin OFS sang Core T24 để đổi quyền sở hữu sổ cái."
                },
                {
                    "clear": True,
                    "show": """<table class="t">
  <tr><th>tiêu chí so sánh</th><th>Khóa Bi quan (Pessimistic)</th><th>Khóa Lạc quan (Optimistic)</th></tr>
  <tr><td>Cơ chế thực thi</td><td>SELECT FOR UPDATE giữ khóa cứng dòng dữ liệu</td><td>UPDATE có điều kiện dấu thời gian last_access</td></tr>
  <tr><td>Hiệu năng chịu tải</td><td>Gây nghẽn hàng đợi khi nhiều người cùng xem</td><td>Hoàn toàn không nghẽn, hỗ trợ hàng triệu lượt đọc</td></tr>
  <tr><td>Ứng dụng phù hợp</td><td>Hạch toán chuyển tiền trực tiếp trong Core</td><td>Sàn giao dịch tài chính số và thương mại điện tử</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Bảng so sánh làm rõ sự khác biệt giữa hai phương pháp kiểm soát đồng thời. Khóa Bi quan gây nghẽn tắc khi hàng nghìn người cùng xem thông tin. Khóa Lạc quan cho phép đọc tự do và bảo đảm phản hồi tức thì."
                },
                {
                    "clear": True,
                    "show": """<p><b>Quy trình chuyển giao quyền sở hữu CIF trên Core T24</b>:</p>
<table class="t">
  <tr><th>bản tin T24 OFS</th><th>vai trò trong giao dịch</th><th>kết quả trả về</th></tr>
  <tr><td>ACCOUNT_T24_DEPOSIT_OFS</td><td>Kiểm tra hợp đồng tiền gửi có bị phong tỏa hay thế chấp vay vốn</td><td>Hợp đồng hợp lệ cho phép chuyển nhượng</td></tr>
  <tr><td>AZ_ACCOUNT_T24_OFS_AMD</td><td>Hạch toán chuyển đổi khách hàng thụ hưởng mới trên phân hệ tiền gửi</td><td>Cập nhật CIF mới vào sổ cái ngân hàng</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Quá trình chuyển giao trên hệ thống lõi gồm hai bước liên kết chặt chẽ. Hệ thống kiểm tra điều kiện phong tỏa để bảo đảm hợp đồng hoàn toàn trong sạch. Sau đó bản tin điều chỉnh sẽ cập nhật người sở hữu mới vào sổ cái ngân hàng."
                }
            ]
        },
        # 4. SYMBOL
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Cú pháp Câu lệnh Khóa Lạc quan với dấu thời gian",
            "steps": [
                {
                    "show": """<p><b>Câu lệnh SQL cập nhật trạng thái nguyên tử bằng Khóa Lạc quan</b>:</p>
<div class="box code"><code>UPDATE transaction<br/>
SET status = 'PROCESSING', receive_cif = :cif, last_access = NOW()<br/>
WHERE order_id = :id AND channel = :ch AND order_date = :dt AND last_access = :old_ts;</code></div>
<div class="box key">Điều kiện then chốt: Dấu thời gian <code>last_access</code> phải khớp chính xác với thời điểm đọc dữ liệu ban đầu!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Đây là câu lệnh cập nhật nguyên tử mẫu mực trong hệ thống thực tế. Ta cập nhật trạng thái đơn hàng sang xử lý và gán mã CIF người mua. Điều kiện then chốt là dấu thời gian truy cập phải trùng khớp giá trị lúc đọc."
                }
            ]
        },
        # 5. EXAMPLE
        {
            "id": "example",
            "kind": "example",
            "title": "Quy trình xử lý xung đột đồng thời và chuyển đổi trạng thái",
            "checks": [
                "500000000 // 1000000 == 500",
                "100 - 95 == 5",
                "500 - 25 == 475"
            ],
            "steps": [
                {
                    "show": """<p><b>Bước 1 — Người mua thứ nhất bấm Mua hợp đồng tiền gửi</b>:</p>
<div class="box key">Giá trị <code>last_access</code> trên cơ sở dữ liệu đang là <code>10:00:00.100</code>.<br/>
Câu lệnh thực thi thành công, số dòng tác động là <code>1</code>.<br/>
Trạng thái giao dịch chuyển sang <b>PROCESSING</b>, thời điểm mới là <code>10:00:00.120</code>.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước một, người mua thứ nhất bấm xác nhận mua hợp đồng. Dấu thời gian trong cơ sở dữ liệu khớp đúng với yêu cầu gửi lên. Câu lệnh cập nhật thành công một dòng và chuyển sang trạng thái đang xử lý."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Người mua thứ hai gửi yêu cầu sau 5 mili giây</b>:</p>
<div class="box warn">Giá trị gửi lên vẫn là thời điểm cũ <code>10:00:00.100</code>.<br/>
Tuy nhiên cơ sở dữ liệu đã đổi thành <code>10:00:00.120</code>.<br/>
Số dòng tác động trả về là <code>0</code>! Hệ thống phát hiện xung đột tức thì!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước hai, người mua thứ hai gửi lệnh sau đó năm mi li giây. Dấu thời gian gửi lên không còn khớp với giá trị vừa được cập nhật. Số dòng tác động trả về bằng không giúp hệ thống nhận diện xung đột ngay lập tức."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 3 — Trả mã lỗi 409 Conflict cho người đến sau</b>:</p>
<table class="t">
  <tr><th>thời điểm</th><th>người dùng</th><th>kết quả cập nhật</th><th>phản hồi HTTP</th></tr>
  <tr><td>10:00:00.100</td><td>Người mua 1</td><td>Thành công 1 dòng</td><td>HTTP 200 OK (Đang hạch toán)</td></tr>
  <tr><td>10:00:00.105</td><td>Người mua 2</td><td>Thất bại 0 dòng</td><td>HTTP 409 Conflict (Sổ đã bán)</td></tr>
</table>
<div class="box key">Toàn bộ quy trình loại trừ xung đột hoàn tất chỉ trong $25$ mili giây!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước ba, cổng dịch vụ lập tức trả mã lỗi 409 cho người đến sau. Không có dòng nào bị khóa cứng khiến cơ sở dữ liệu bị nghẽn tắc. Toàn bộ tiến trình xử lý chỉ tiêu tốn 25 mi li giây."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 4 — Đoạn mã xử lý kết quả trong Go Fiber</b>:</p>
<div class="box code"><code>if res.RowsAffected() == 0 {<br/>
&nbsp;&nbsp;return c.Status(fiber.StatusConflict).JSON(fiber.Map{<br/>
&nbsp;&nbsp;&nbsp;&nbsp;"code": "409", "message": "Hợp đồng tiền gửi đã có giao dịch khác!"<br/>
&nbsp;&nbsp;})<br/>
}</code></div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước bốn, ta kiểm tra kết quả dòng tác động trong mã nguồn xử lý. Nếu số dòng bằng không, hàm lập tức trả về mã xung đột kèm thông báo rõ ràng cho ứng dụng khách. Kỹ thuật này giúp loại bỏ hoàn toàn các lỗi tranh chấp dữ liệu phức tạp."
                }
            ]
        },
        # 6. CHECK
        {
            "id": "check",
            "kind": "check",
            "title": "Kiểm tra xử lý tình huống mạng Core T24 bị sự cố",
            "checks": [
                "500 > 100",
                "25 < 100"
            ],
            "steps": [
                {
                    "show": """<p><b>Tình huống phỏng vấn</b>: Sau khi trừ tiền người mua, dịch vụ gọi sang T24 để đổi CIF nhưng bị mất kết nối mạng và trả về mã lỗi 04 Timeout. Bạn xử lý thế nào?</p>
<table class="t">
  <tr><th>cách xử lý sai lầm</th><th>giải pháp chuẩn mực Senior</th></tr>
  <tr><td>Báo thất bại và hoàn tiền ngay lập tức</td><td>Chuyển trạng thái sang HOLD chờ đối soát tự động</td></tr>
  <tr><td>Mở khóa cho người khác vào mua sổ</td><td>Khóa giữ sổ tiết kiệm không cho ai mua tiếp</td></tr>
  <tr><td>Gây thất thoát tài chính nghiêm trọng</td><td>Truy vấn sổ cái T24 xác nhận trước khi hạch toán</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Ta kiểm tra tình huống thực tế khi gọi sang T24 bị lỗi mạng hoặc hết giờ. Do bản tin có thể đã ghi vào sổ cái, việc báo thất bại và hoàn tiền ngay là sai lầm nghiêm trọng. Bởi vì điều này có thể khiến khách hàng vừa nhận lại tiền vừa nhận được sổ."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Quy tắc bảo vệ tài chính</b>: Mọi mã lỗi nghi ngờ như 04, 05, 999 đều được chuyển sang trạng thái <b>HOLD</b>. Tiến trình đối soát tự động sẽ truy vấn sổ cái T24 để kiểm tra xem việc đổi CIF đã diễn ra hay chưa, bảo đảm an toàn tài chính tuyệt đối.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Do đó, quy tắc an toàn là đưa giao dịch vào trạng thái giữ lệnh để chờ đối soát. Tiến trình tự động sẽ truy vấn sổ cái T24 để kiểm tra trạng thái thực tế. Nhờ vậy, ngân hàng bảo vệ an toàn tài sản tuyệt đối."
                }
            ]
        },
        # 7. PITFALL
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Ba sai lầm nghiêm trọng trong thiết kế sàn chuyển nhượng",
            "steps": [
                {
                    "show": """<table class="t">
  <tr><th>sai lầm sơ cấp</th><th>hậu quả kỹ thuật & tài chính</th><th>giải pháp chuẩn Senior</th></tr>
  <tr><td>Dùng khóa bi quan SELECT FOR UPDATE</td><td>làm nghẽn hàng đợi khi nhiều người cùng xem sổ</td><td>dùng Khóa Lạc quan với dấu thời gian</td></tr>
  <tr><td>Không kiểm tra số dòng tác động</td><td>bán một sổ tiết kiệm cho hai khách hàng khác nhau</td><td>chỉ cho phép đi tiếp khi rows_affected bằng 1</td></tr>
  <tr><td>Tự ý huỷ lệnh khi T24 Timeout</td><td>sai lệch sổ cái và làm mất cân đối tài chính</td><td>chuyển sang HOLD và chạy đối soát tự động</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Có ba sai lầm chí mạng cần tránh khi làm sàn chuyển nhượng. Thứ nhất là dùng khóa cưỡng bức làm nghẽn toàn bộ hệ thống. Thứ hai là quên kiểm tra số dòng tác động dẫn đến bán trùng sổ. Thứ ba là tự ý huỷ lệnh khi mạng bị hết giờ thay vì đưa vào trạng thái chờ đối soát."
                }
            ]
        },
        # 8. QUIZ
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Thử thách giải quyết xung đột đồng thời tại ACB",
            "checks": [
                "409 - 400 == 9",
                "1000 - 1 == 999"
            ],
            "steps": [
                {
                    "pause": 15,
                    "show": """<p><b>Câu hỏi trắc nghiệm kiến trúc</b>: Trong hệ thống sàn chuyển nhượng hợp đồng tiền gửi, tại sao Khóa Lạc quan lại vượt trội hơn Khóa Bi quan khi phục vụ hàng triệu người dùng?</p>
<ul>
  <li><b>A</b>: Vì Khóa Lạc quan không giữ khóa trong quá trình đọc, giúp hàng nghìn người cùng xem thông tin mà không làm giảm thông lượng hệ thống.</li>
  <li><b>B</b>: Vì Khóa Lạc quan không cần cơ sở dữ liệu.</li>
  <li><b>C</b>: Vì Khóa Lạc quan tự động cộng thêm tiền lãi cho khách hàng.</li>
  <li><b>D</b>: Vì Khóa Bi quan không tương thích với Go Fiber.</li>
</ul>""",
                    "focus": [0, 0, 0],
                    "say": "Hãy cùng bước vào thử thách kiến trúc phỏng vấn tại ACB. Tại sao Khóa Lạc quan lại vượt trội hơn Khóa Bi quan trên sàn chuyển nhượng? Bạn có 15 giây suy nghĩ trước khi nghe đáp án chuẩn xác."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Đáp án chính xác là A</b>!</div>
<p><b>Bước 1 — Phân tách luồng đọc và luồng ghi</b>:</p>
<p>Trên sàn giao dịch, tỉ lệ đọc thông tin sổ tiết kiệm chiếm hơn 99 phần trăm. Khóa Lạc quan cho phép mọi người dùng đọc dữ liệu đồng thời với tốc độ tối đa mà không gây khóa tài nguyên.</p>""",
                    "focus": [0, 0],
                    "say": "Đáp án chính xác là phương án A. Trên sàn chuyển nhượng, số lượng người xem thông tin chiếm đa số nên Khóa Lạc quan giúp mọi người đọc đồng thời mà không làm ảnh hưởng tài nguyên chung."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Bảo đảm tính toàn vẹn khi ghi dữ liệu</b>:</p>
<div class="box key">Chỉ tại thời điểm bấm Mua, hệ thống mới kiểm tra dấu thời gian qua câu lệnh cập nhật nguyên tử. Người đến trước cập nhật thành công một dòng, người đến sau nhận mã lỗi 409 mà không cần chờ đợi.</div>""",
                    "focus": [0, 0],
                    "say": "Chỉ khi người dùng bấm mua thì hệ thống mới kiểm tra dấu thời gian. Người đến trước cập nhật thành công, còn người đến sau nhận lỗi ngay mà không phải xếp hàng chờ đợi."
                }
            ]
        },
        # 9. RECAP
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Sàn Chuyển nhượng Tiền gửi",
            "steps": [
                {
                    "show": """<div class="chain">
  <span>Tiếp nhận đơn mua từ Mobile App</span> &rarr;
  <span>Khóa Lạc quan qua last_access</span> &rarr;
  <span>Xác nhận rows_affected bằng 1</span> &rarr;
  <span>Chuyển trạng thái PROCESSING</span> &rarr;
  <span>Gửi bản tin OFS đổi CIF Core T24</span> &rarr;
  <span>Hạch toán thành công hoặc cách ly HOLD</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>năng lực then chốt</th><th>giá trị mang lại cho ngân hàng</th></tr>
  <tr><td>Khóa Lạc quan</td><td>Loại bỏ 100% rủi ro bán trùng mà không nghẽn cơ sở dữ liệu</td></tr>
  <tr><td>Xử lý biệt lập Timeout</td><td>Bảo vệ an toàn tài chính tuyệt đối trước các sự cố mạng lõi</td></tr>
</table>
<p style="margin-top: 15px;"><b>Khẳng định đẳng cấp Senior tại ngân hàng ACB</b>: Làm chủ kỹ thuật Khóa Lạc quan, bảo toàn tính toàn vẹn tài chính, xử lý triệt để mã lỗi T24 và tự tin chinh phục mức lương 50 triệu gross.</p>""",
                    "focus": [0, 0, 0],
                    "say": "Tóm lại, chuỗi logic gồm tiếp nhận yêu cầu, cập nhật khóa lạc quan, kiểm tra dòng tác động, gửi bản tin sang T24 và cách ly lỗi an toàn. Nắm vững giải pháp này, bạn hoàn toàn tự tin bảo vệ hệ thống trước mọi nguy cơ xung đột dữ liệu. Bạn sẵn sàng tỏa sáng ở vị trí kỹ sư tích hợp cấp cao tại ACB."
                }
            ]
        }
    ]
}

with open("lessons/acb/L04_san_chuyen_nhuong_hop_dong_tien_gui.yaml", "w", encoding="utf-8") as f:
    yaml.dump(lesson, f, allow_unicode=True, sort_keys=False, width=1000)

print("Created lessons/acb/L04_san_chuyen_nhuong_hop_dong_tien_gui.yaml successfully")
