import yaml

lesson = {
    "id": "L05",
    "course": "ACB",
    "series": "Phỏng vấn Kỹ sư Tích hợp ACB",
    "title": "Bài 5 — Cổng Chi lương theo lô Doanh nghiệp và Sao kê Divide-and-Conquer",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "curriculum/acb.yaml L05; Kiến trúc po-batch-transfer và mcs-kstream-ipn-statement-devide-conquer; Oracle Database 19c PL/SQL Guide 2026",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Thiết kế Cổng Chi lương Doanh nghiệp theo lô với mẫu Transactional Outbox",
        "Khử triệt để Deadlock ORA-00060 trong Oracle PL/SQL bằng sắp xếp tài khoản và Bulk Collect",
        "Xử lý hàng triệu dòng sao kê tài khoản bằng Kafka Streams Divide-and-Conquer"
    ],
    "scenes": [
        # 1. HOOK
        {
            "id": "hook",
            "kind": "hook",
            "title": "Bài toán chi lương cho mười nghìn nhân viên cùng một lúc ngày cuối tháng",
            "steps": [
                {
                    "show": """<p>Vào ngày 30 hàng tháng, các tập đoàn lớn đồng loạt tải lên các lô chi lương hàng chục nghìn nhân viên.</p>
<div class="box key">Nếu dùng vòng lặp gọi từng tài khoản, hệ thống sẽ sập do bế tắc khóa Oracle ORA-00060 hoặc treo nghẽn mạng liên ngân hàng. Làm sao để giải ngân toàn bộ trong 3 phút mà không sai một đồng?</div>""",
                    "focus": [0, 0, 0],
                    "say": "Chào bạn, vào ngày cuối tháng, các doanh nghiệp đồng loạt chi lương cho hàng chục nghìn nhân sự. Nếu lập trình viên dùng vòng lặp thông thường để duyệt từng lệnh, hệ thống ngân hàng sẽ bế tắc khóa ngay lập tức. Ta cần một kiến trúc phân tán mạnh mẽ để xử lý an toàn."
                },
                {
                    "clear": True,
                    "show": """<table class="t">
  <tr><th>điểm nghẽn hệ thống</th><th>hậu quả nghiêm trọng</th><th>giải pháp kiến trúc chuẩn Senior</th></tr>
  <tr><td>Vòng lặp duyệt tuần tự từng lệnh</td><td>Quá tải cổng mạng và chậm tiến độ chi lương</td><td>Mẫu Transactional Outbox và xử lý theo lô</td></tr>
  <tr><td>Khóa tài khoản lộn xộn ngẫu nhiên</td><td>Xảy ra bế tắc khóa Oracle ORA-00060</td><td>Thuật toán sắp xếp thứ tự tài khoản trước khi khóa</td></tr>
  <tr><td>Truy vấn sao kê hàng triệu giao dịch</td><td>Làm treo cơ sở dữ liệu sổ cái ngân hàng</td><td>Kỹ thuật phân nhỏ chia để trị với Kafka Streams</td></tr>
</table>
<p>Hôm nay, ta giải mã: <b>Mẫu Transactional Outbox</b>, <b>thuật toán khử bế tắc khóa Oracle PL/SQL</b>, và <b>kỹ thuật chia để trị trong sao kê tài khoản</b>.</p>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Hôm nay, ta cùng nhau khám phá ba giải pháp then chốt cho khách hàng doanh nghiệp. Ta tìm hiểu mẫu thiết kế hộp thư giao dịch bảo đảm tính toàn vẹn. Ta nắm vững thuật toán triệt tiêu bế tắc khóa trong cơ sở dữ liệu. Ta cũng làm chủ kỹ thuật chia để trị trong sao kê tài khoản."
                }
            ]
        },
        # 2. PREREQ
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Lệnh chi theo lô, Transactional Outbox và Bế tắc khóa cơ sở dữ liệu",
            "checks": [
                "10000 * 15000000 == 150000000000",
                "10000 // 1000 == 10"
            ],
            "steps": [
                {
                    "show": """<p><b>Ba khái niệm cốt lõi trong xử lý giao dịch doanh nghiệp</b>:</p>
<table class="t">
  <tr><th>khái niệm</th><th>ý nghĩa kỹ thuật</th><th>vai trò trong ngân hàng</th></tr>
  <tr><td>Batch Payroll</td><td>lô lệnh chi lương gồm hàng nghìn tài khoản con</td><td>thực hiện trích nợ công ty và ghi có cho nhân viên</td></tr>
  <tr><td>Transactional Outbox</td><td>ghi dữ liệu nghiệp vụ và sự kiện trong cùng một transaction</td><td>bảo đảm không bao giờ thất lạc lệnh chuyển tiền</td></tr>
  <tr><td>Lỗi ORA-00060</td><td>hai tiến trình cùng chờ khóa tài nguyên của nhau</td><td>làm sập tiến trình cơ sở dữ liệu và huỷ toàn bộ lô lương</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Trước tiên ta điểm lại ba khái niệm cốt lõi trong thanh toán doanh nghiệp. Chi lương theo lô là tập hợp hàng chục nghìn lệnh con được xử lý đồng thời. Mẫu hộp thư giao dịch bảo đảm dữ liệu và sự kiện luôn toàn vẹn. Lỗi ORA không không không sáu không là sự cố bế tắc khóa kinh điển cần triệt tiêu."
                },
                {
                    "clear": True,
                    "show": """<div class="box key">Quy mô bài toán thực tế: Một tập đoàn có $10\\,000$ nhân viên, mức lương bình quân $15$ triệu đồng.<br/>
Tổng số tiền giải ngân một đợt: $10\\,000 \\times 15\\,000\\,000 = 150$ tỉ đồng.<br/>
Hệ thống chia lô thành $10$ khối nhỏ, mỗi khối $1\\,000$ giao dịch để xử lý song song trên Kafka.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Ta xét một bài toán thực tế của doanh nghiệp lớn. Với mười nghìn nhân viên, tổng số tiền chi lương lên tới 150 tỉ đồng. Để xử lý hiệu quả, hệ thống băm nhỏ lô thành mười khối song song trên hàng đợi sự kiện."
                }
            ]
        },
        # 3. CONCEPT
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kiến trúc Cổng Chi lương theo lô và Động cơ Sao kê Divide-and-Conquer",
            "steps": [
                {
                    "show": """<div>
  <svg width="1500" height="380" viewBox="0 0 1500 380">
    <g font-size="22" fill="#1f2937">
      <text x="750" y="35" text-anchor="middle" font-weight="bold" font-size="26">Kiến trúc Cổng Chi lương theo lô Doanh nghiệp và Sao kê Đa kênh</text>
      <rect x="50" y="70" width="300" height="240" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
      <text x="200" y="115" text-anchor="middle" font-weight="bold">1. Danh sách chi lương</text>
      <text x="200" y="160" text-anchor="middle">Doanh nghiệp tải tệp</text>
      <text x="200" y="200" text-anchor="middle">Phân tích 10,000 lệnh</text>
      <text x="200" y="240" text-anchor="middle">Ghi bảng Outbox DB</text>

      <rect x="440" y="70" width="320" height="240" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>
      <text x="600" y="115" text-anchor="middle" font-weight="bold">2. Debezium CDC</text>
      <text x="600" y="160" text-anchor="middle">Bắt sự kiện Outbox</text>
      <text x="600" y="200" text-anchor="middle">Đẩy vào Kafka Topic</text>
      <text x="600" y="240" text-anchor="middle">Phân vùng theo Batch</text>

      <rect x="850" y="70" width="280" height="240" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
      <text x="990" y="115" text-anchor="middle" font-weight="bold">3. Router Worker</text>
      <text x="990" y="160" text-anchor="middle">Tài khoản nội bộ: T24</text>
      <text x="990" y="200" text-anchor="middle">Liên ngân hàng: NAPAS</text>
      <text x="990" y="240" text-anchor="middle">Khóa hàng có thứ tự</text>

      <rect x="1210" y="70" width="250" height="240" rx="12" fill="#f3e8ff" stroke="#9333ea" stroke-width="3"/>
      <text x="1335" y="115" text-anchor="middle" font-weight="bold">4. Hoàn tất & Sao kê</text>
      <text x="1335" y="160" text-anchor="middle">Ghi sổ cái Oracle</text>
      <text x="1335" y="200" text-anchor="middle">Kafka Streams gộp kết quả</text>
      <text x="1335" y="240" text-anchor="middle">Xuất sao kê số dư</text>

      <line x1="350" y1="150" x2="440" y2="150" stroke="#0284c7" stroke-width="4"/>
      <line x1="760" y1="150" x2="850" y2="150" stroke="#d97706" stroke-width="4"/>
      <line x1="1130" y1="150" x2="1210" y2="150" stroke="#16a34a" stroke-width="4"/>
    </g>
  </svg>
</div>""",
                    "focus": [0, 0, 0, 0, 0],
                    "say": "Nhìn lên sơ đồ luồng dữ liệu bốn tầng của cổng chi lương. Bước một, doanh nghiệp tải danh sách nhân sự lên và hệ thống ghi vào bảng Outbox. Bước hai, công nghệ bắt biến động dữ liệu đẩy các lệnh vào hàng đợi sự kiện. Bước ba, các tiến trình định tuyến phân loại lệnh nội bộ và liên ngân hàng. Bước bốn, động cơ chia để trị tổng hợp số dư và xuất sao kê tức thì."
                },
                {
                    "clear": True,
                    "show": """<table class="t">
  <tr><th>thách thức lớn</th><th>nguyên nhân gốc rễ</th><th>phương pháp giải quyết dứt điểm</th></tr>
  <tr><td>Deadlock ORA-00060</td><td>Nhiều luồng cùng khóa tài khoản theo thứ tự ngẫu nhiên</td><td>Sắp xếp số tài khoản tăng dần trước khi thực hiện khóa</td></tr>
  <tr><td>Nghẽn I/O khi xuất sao kê</td><td>Truy vấn quét cạn hàng triệu dòng trên cơ sở dữ liệu chính</td><td>Băm nhỏ khoảng thời gian truy vấn và chạy song song qua Kafka Streams</td></tr>
  <tr><td>Thất lạc lệnh khi mạng đứt</td><td>Gửi trực tiếp qua mạng mà không lưu vết giao dịch</td><td>Mẫu Transactional Outbox lưu giữ trạng thái bền vững</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Bảng tổng hợp làm rõ ba thách thức lớn và giải pháp tương ứng. Ta triệt tiêu lỗi bế tắc khóa bằng thuật toán sắp xếp thứ tự tài khoản tăng dần. Ta loại bỏ nghẽn cơ sở dữ liệu bằng cách phân đoạn thời gian sao kê. Ta bảo vệ toàn vẹn dữ liệu bằng mẫu hộp thư giao dịch lưu vết bền vững."
                }
            ]
        },
        # 4. SYMBOL
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Cú pháp Khóa hàng có thứ tự xác định và Bulk Collect trong Oracle PL/SQL",
            "steps": [
                {
                    "show": """<p><b>Thủ tục lưu trữ Oracle PL/SQL khóa hàng theo thứ tự xác định</b>:</p>
<div class="box code"><code>SELECT account_no, balance<br/>
BULK COLLECT INTO l_accounts<br/>
FROM accounts<br/>
WHERE account_no IN (SELECT column_value FROM TABLE(p_acc_list))<br/>
ORDER BY account_no ASC<br/>
FOR UPDATE;</code></div>
<div class="box key">Nguyên lý vàng: Mọi tiến trình luôn khóa các tài khoản theo thứ tự bảng chữ cái tăng dần, triệt tiêu hoàn toàn vòng lặp phụ thuộc gây Deadlock!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Đây là cú pháp mẫu mực trong thủ tục lưu trữ cơ sở dữ liệu Oracle. Ta sử dụng mệnh đề lấy dữ liệu theo mảng kết hợp khóa hàng có thứ tự tăng dần. Nhờ khóa theo thứ tự định sẵn, không bao giờ xảy ra tình trạng hai luồng chờ đợi lẫn nhau."
                }
            ]
        },
        # 5. EXAMPLE
        {
            "id": "example",
            "kind": "example",
            "title": "Minh họa cơ chế triệt tiêu Deadlock và Kỹ thuật Divide-and-Conquer",
            "checks": [
                "1000 * 10 == 10000",
                "30 // 4 == 7",
                "150000000000 // 10000 == 15000000"
            ],
            "steps": [
                {
                    "show": """<p><b>Bước 1 — Vì sao xảy ra Deadlock khi không sắp xếp thứ tự?</b>:</p>
<div class="box warn">Tiến trình A muốn chuyển tiền: Khóa Tài khoản 1, sau đó chờ khóa Tài khoản 2.<br/>
Tiến trình B cũng chuyển tiền: Khóa Tài khoản 2, sau đó chờ khóa Tài khoản 1.<br/>
Cả hai tiến trình giữ chặt tài nguyên của nhau mãi mãi, Oracle phát hiện vòng bế tắc và ném lỗi <b>ORA-00060</b>!</div>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Bước một, ta phân tích nguyên nhân gây ra bế tắc khóa khi không sắp xếp thứ tự. Tiến trình A giữ tài khoản một và chờ tài khoản hai. Cùng lúc đó, tiến trình B lại giữ tài khoản hai và chờ tài khoản một. Cả hai luồng chờ nhau vô tận khiến cơ sở dữ liệu phải huỷ giao dịch."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Thuật toán khóa hàng có thứ tự loại bỏ vòng lặp phụ thuộc</b>:</p>
<table class="t">
  <tr><th>quy tắc khóa</th><th>hành vi của Tiến trình A</th><th>hành vi của Tiến trình B</th></tr>
  <tr><td>Thứ tự tăng dần</td><td>Bắt buộc khóa Tài khoản 1 trước, Tài khoản 2 sau</td><td>Cũng phải khóa Tài khoản 1 trước, Tài khoản 2 sau</td></tr>
  <tr><td>Kết quả vận hành</td><td>Tiến trình A lấy được khóa Tài khoản 1 và hoàn tất</td><td>Tiến trình B xếp hàng chờ A nhả khóa rồi mới đi tiếp</td></tr>
</table>
<div class="box key">Không còn chu trình phụ thuộc chéo $\to$ Tỉ lệ Deadlock giảm về đúng $0\\%$!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước hai, ta áp dụng quy tắc khóa hàng có thứ tự tăng dần xác định. Cả hai tiến trình đều buộc phải xin khóa tài khoản một trước rồi mới đến tài khoản hai. Do đó, tiến trình đến sau sẽ kiên nhẫn xếp hàng chờ tiến trình trước hoàn tất."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 3 — Tối ưu hóa hiệu năng bằng Bulk Collect và Forall</b>:</p>
<div class="box key">Thay vì gọi $10\\,000$ lệnh cập nhật đơn lẻ làm tốn $10\\,000$ lần chuyển đổi ngữ cảnh (Context Switch), ta gom thành mảng dữ liệu và cập nhật hàng loạt bằng <code>FORALL</code>.<br/>
Thời gian thực thi trích nợ $10\\,000$ tài khoản giảm từ $45$ giây xuống chỉ còn <b>$1.2$ giây</b>!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước ba, ta tối ưu hóa tốc độ bằng cơ chế gom nhóm và cập nhật hàng loạt. Thay vì chạy mười nghìn câu lệnh riêng lẻ, thủ tục gom toàn bộ vào một mảng duy nhất. Thời gian xử lý trích nợ toàn bộ mười nghìn tài khoản giảm từ 45 giây xuống còn một giây."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 4 — Kỹ thuật Divide-and-Conquer trong Sao kê Tài khoản lớn</b>:</p>
<div class="box key">Khách hàng yêu cầu sao kê $30$ ngày với hơn $1\\,000\\,000$ bản ghi giao dịch.<br/>
Hệ thống chia khoảng thời gian thành $4$ phân đoạn song song (mỗi tuần một đoạn).<br/>
Bốn worker của Kafka Streams đọc dữ liệu từ các máy chủ đọc độc lập, tính toán số dư lũy kế và xuất kết quả chỉ trong $2.5$ giây!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước bốn, ta giải quyết bài toán xuất sao kê hàng triệu giao dịch bằng kỹ thuật chia để trị. Khoảng thời gian 30 ngày được băm nhỏ thành bốn phân đoạn song song. Các luồng xử lý độc lập tổng hợp số dư lũy kế và xuất kết quả chỉ trong hai giây rưỡi."
                }
            ]
        },
        # 6. CHECK
        {
            "id": "check",
            "kind": "check",
            "title": "Kiểm tra xử lý tình huống mất mạng giữa chừng khi đang chạy lô chi lương",
            "checks": [
                "10000 - 9999 == 1",
                "100 > 50"
            ],
            "steps": [
                {
                    "show": """<p><b>Tình huống phỏng vấn</b>: Khi đang thực hiện chi lương đến nhân viên thứ 5,000 thì máy chủ bị mất điện đột ngột. Bạn làm thế nào để khi khởi động lại không bị chi trùng tiền cho 5,000 người đầu tiên?</p>
<table class="t">
  <tr><th>cách xử lý sơ cấp</th><th>giải pháp chuẩn mực Senior</th></tr>
  <tr><td>Chạy lại toàn bộ danh sách từ đầu</td><td>Dựa vào bảng Outbox và khóa duy nhất Idempotency Key</td></tr>
  <tr><td>Làm nhân viên nhận lương 2 lần</td><td>Chỉ xử lý các bản ghi có trạng thái PENDING</td></tr>
  <tr><td>Gây thất thoát hàng tỉ đồng</td><td>Tiếp tục xử lý từ nhân viên thứ 5,001 một cách an toàn</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Ta kiểm tra tình huống thực tế khi máy chủ gặp sự cố giữa chừng lúc đang chi lương. Do năm nghìn người đầu tiên đã được nhận tiền, việc chạy lại toàn bộ danh sách từ đầu sẽ khiến nhân viên nhận lương hai lần. Bởi vì điều này gây ra thất thoát tài chính lớn cho doanh nghiệp."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Quy tắc đảm bảo tính duy nhất</b>: Mỗi lệnh con trong bảng Outbox đều được gắn khóa duy nhất gồm mã lô và số tài khoản. Khi máy chủ khởi động lại, tiến trình chỉ quét các bản ghi chưa hoàn tất. Các giao dịch đã thành công sẽ tự động được bỏ qua, bảo đảm an toàn tuyệt đối.</div>""",
                    "focus": [0, 0, 0],
                    "say": "Do đó, hệ thống luôn gán khóa duy nhất cho từng lệnh con trong bảng hộp thư giao dịch. Khi khởi động lại, tiến trình chỉ quét các bản ghi đang chờ xử lý. Nhờ vậy, năm nghìn người đầu tiên không bao giờ bị trừ tiền trùng lặp."
                }
            ]
        },
        # 7. PITFALL
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Ba sai lầm nghiêm trọng trong kiến trúc xử lý thanh toán theo lô",
            "steps": [
                {
                    "show": """<table class="t">
  <tr><th>sai lầm sơ cấp</th><th>hậu quả kỹ thuật & tài chính</th><th>giải pháp chuẩn Senior</th></tr>
  <tr><td>Duyệt vòng lặp gọi API từng người</td><td>Treo luồng mạng và mất hàng giờ để chi lương</td><td>Dùng Transactional Outbox và xử lý theo lô</td></tr>
  <tr><td>Khóa tài nguyên không có thứ tự</td><td>Gây bế tắc khóa Deadlock ORA-00060 trong DB</td><td>Sắp xếp tài khoản tăng dần trước khi khóa hàng</td></tr>
  <tr><td>Truy vấn quét cạn vào bảng chính Core</td><td>Làm sập hệ thống hạch toán trực tuyến của ngân hàng</td><td>Dùng Kafka Streams chia để trị trên read-replica</td></tr>
</table>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Có ba sai lầm chí mạng cần tránh khi xây dựng cổng chi lương. Thứ nhất là gọi mạng tuần tự từng người gây chậm trễ nghiêm trọng. Thứ hai là khóa dữ liệu không theo thứ tự gây bế tắc cơ sở dữ liệu. Thứ ba là truy vấn sao kê trực tiếp vào sổ cái chính thay vì dùng kỹ thuật chia để trị."
                }
            ]
        },
        # 8. QUIZ
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Thử thách kiến trúc xử lý dữ liệu lớn tại ACB",
            "checks": [
                "60 - 60 == 0",
                "1000 * 2 == 2000"
            ],
            "steps": [
                {
                    "pause": 15,
                    "show": """<p><b>Câu hỏi trắc nghiệm kiến trúc</b>: Trong cơ sở dữ liệu Oracle, tại sao việc thêm mệnh đề <code>ORDER BY account_no ASC FOR UPDATE</code> lại triệt tiêu hoàn toàn lỗi Deadlock ORA-00060?</p>
<ul>
  <li><b>A</b>: Vì mọi giao dịch đều xin khóa tài nguyên theo cùng một thứ tự định sẵn, loại bỏ hoàn toàn khả năng hình thành chu trình phụ thuộc lẫn nhau.</li>
  <li><b>B</b>: Vì lệnh ORDER BY tự động tắt tính năng khóa của Oracle.</li>
  <li><b>C</b>: Vì tài khoản sắp xếp trước sẽ được miễn phí giao dịch.</li>
  <li><b>D</b>: Vì Oracle chỉ cho phép một người dùng kết nối tại một thời điểm.</li>
</ul>""",
                    "focus": [0, 0, 0],
                    "say": "Hãy cùng bước vào câu hỏi trắc nghiệm kiến trúc thực chiến của ACB. Tại sao việc sắp xếp thứ tự tài khoản trước khi khóa lại triệt tiêu hoàn toàn lỗi bế tắc khóa? Bạn có 15 giây suy nghĩ trước khi nghe đáp án chuẩn xác."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Đáp án chính xác là A</b>!</div>
<p><b>Bước 1 — Điều kiện hình thành Deadlock</b>:</p>
<p>Deadlock chỉ xảy ra khi có chu trình chờ đợi tài nguyên khép kín giữa hai hay nhiều giao dịch đồng thời.</p>""",
                    "focus": [0, 0],
                    "say": "Đáp án chính xác là phương án A. Bước một, bế tắc khóa chỉ xảy ra khi tồn tại một chu trình chờ đợi tài nguyên khép kín giữa các giao dịch."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Cơ chế phá vỡ chu trình phụ thuộc</b>:</p>
<div class="box key">Khi toàn bộ các tiến trình cùng tuân thủ quy tắc khóa theo thứ tự bảng chữ cái tăng dần, đồ thị chờ đợi tài nguyên luôn là một đường thẳng không bao giờ có chu trình khép kín. Do đó, hiện tượng Deadlock biến mất hoàn toàn!</div>""",
                    "focus": [0, 0],
                    "say": "Bước hai, khi mọi tiến trình đều khóa tài khoản theo thứ tự tăng dần, đồ thị chờ đợi sẽ không bao giờ có vòng tròn lặp lại. Nhờ vậy, hiện tượng bế tắc khóa được triệt tiêu hoàn toàn."
                }
            ]
        },
        # 9. RECAP
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Cổng Chi lương và Sao kê Divide-and-Conquer",
            "steps": [
                {
                    "show": """<div class="chain">
  <span>Tiếp nhận file chi lương doanh nghiệp</span> &rarr;
  <span>Ghi bảng Transactional Outbox bền vững</span> &rarr;
  <span>Khóa hàng tăng dần triệt tiêu Deadlock</span> &rarr;
  <span>Gom nhóm cập nhật qua Bulk Collect</span> &rarr;
  <span>Định tuyến lệnh con qua T24 và NAPAS</span> &rarr;
  <span>Kafka Streams chia để trị xuất sao kê</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>thành tựu kỹ thuật</th><th>hiệu quả mang lại</th></tr>
  <tr><td>Khóa hàng có thứ tự</td><td>Tỉ lệ lỗi ORA-00060 giảm về 0% tuyệt đối</td></tr>
  <tr><td>Divide-and-Conquer Streams</td><td>Xuất sao kê 1 triệu dòng trong 2.5 giây</td></tr>
</table>
<p style="margin-top: 15px;"><b>Khẳng định đẳng cấp Senior tại ngân hàng ACB</b>: Nắm vững kiến trúc chi lương theo lô, làm chủ kỹ thuật tối ưu hóa cơ sở dữ liệu chuyên sâu và tự tin nhận mức đãi ngộ 50 triệu gross.</p>""",
                    "focus": [0, 0],
                    "say": "Tóm lại, chuỗi logic gồm tiếp nhận lô lương, lưu vết hộp thư giao dịch, khóa hàng có thứ tự, cập nhật hàng loạt và tổng hợp sao kê phân tán. Nắm vững giải pháp này, bạn hoàn toàn tự tin làm chủ các cổng thanh toán doanh nghiệp lớn và đàm phán mức lương 50 triệu gross tại ACB."
                }
            ]
        }
    ]
}

with open("lessons/acb/L05_cong_chi_luong_va_sao_ke_divide_conquer.yaml", "w", encoding="utf-8") as f:
    yaml.dump(lesson, f, allow_unicode=True, sort_keys=False, width=1000)

print("Created lessons/acb/L05_cong_chi_luong_va_sao_ke_divide_conquer.yaml successfully")
