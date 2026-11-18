import yaml

lesson = {
    "id": "L08",
    "course": "ACB",
    "series": "Phỏng vấn Kỹ sư Tích hợp ACB",
    "title": "Bài 8 — Tín dụng Squad Lending: Thấu chi Sổ tiết kiệm, Lương và Cổng CIC",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "curriculum/acb.yaml L08; Nghiệp vụ Tín dụng Squad Lending OCB, Thấu chi Cầm cố Sổ tiết kiệm T24 AZ, Thấu chi Lương Batch Payroll, Ký số Cloud CA và Cổng CIC B2B NHNN 2026",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Làm chủ nghiệp vụ Thấu chi Cầm cố Sổ tiết kiệm LTV 90 phần trăm và Thấu chi Lương tín chấp trên Core T24",
        "Thiết kế luồng phê duyệt tự động LOS, ký số Cloud CA và tra cứu Cổng CIC B2B qua mTLS",
        "Triển khai cơ chế Giải ngân Idempotent qua NAPAS và trích nợ từng phần Partial Debit từ tài khoản CASA"
    ],
    "scenes": [
        # 1. HOOK
        {
            "id": "hook",
            "kind": "hook",
            "title": "Thách thức tích hợp tín dụng thấu chi và cầm cố sổ tiết kiệm",
            "steps": [
                {
                    "show": """<p>Khách hàng cần vốn gấp nhưng không muốn rút sổ tiết kiệm để tránh mất tiền lãi có kỳ hạn.</p>
<div class="box key">Làm sao một ngân hàng như ACB có thể cấp thấu chi 85 triệu đồng bằng cách cầm cố sổ tiết kiệm 100 triệu, ký số hợp đồng online và giải ngân trong 1 phút mà không lo thất thoát vốn?</div>""",
                    "focus": [0, 0, 0],
                    "say": "Chào bạn, người gửi tiền cần vốn gấp nhưng không muốn rút sổ tiết kiệm để tránh mất toàn bộ tiền lãi có kỳ hạn. Họ mong muốn được cấp hạn mức thấu chi tức thì dựa trên chính sổ tiết kiệm đó. Ngân hàng cần giải pháp tích hợp tự động hoàn toàn từ cầm cố, phong tỏa sổ cái đến giải ngân siêu tốc."
                },
                {
                    "clear": True,
                    "show": """<table class="t">
  <tr><th>sản phẩm tín dụng</th><th>nghiệp vụ cốt lõi</th><th>phân hệ tích hợp</th></tr>
  <tr><td>Thấu chi cầm cố sổ tiết kiệm</td><td>Phong tỏa sổ T24, cấp hạn mức LTV 90%</td><td>ODB Lending và service khóa tài khoản</td></tr>
  <tr><td>Thấu chi lương tín chấp</td><td>Đánh giá dòng tiền lương, cấp hạn mức 3x</td><td>Hệ thống chi lương lô và danh sách ưu tiên</td></tr>
  <tr><td>Ký số Cloud CA và Cổng CIC</td><td>Ký hợp đồng từ xa, tra cứu 5 nhóm nợ</td><td>Cổng ký số đám mây và kết nối bảo mật CIC</td></tr>
</table>
<p>Hôm nay, ta làm chủ: <b>Thấu chi cầm cố sổ tiết kiệm</b>, <b>Thấu chi lương tín chấp</b>, và <b>Giải ngân an toàn</b>.</p>""",
                    "focus": [0, 0, 0],
                    "say": "Hôm nay, ta cùng nhau khám phá trọn vẹn hệ sinh thái tín dụng bán lẻ tốc độ cao. Ta làm chủ nghiệp vụ thấu chi cầm cố sổ tiết kiệm và thấu chi lương theo lô. Ta thiết lập cơ chế phong tỏa sổ cái và giải ngân an toàn tuyệt đối."
                }
            ]
        },
        # 2. PREREQ
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Thấu chi, Tỉ lệ LTV, Biên độ Spread và Khóa Phong tỏa",
            "checks": [
                "100000000 * 85 // 100 == 85000000",
                "85000000 > 50000000"
            ],
            "steps": [
                {
                    "show": """<p><b>Bốn khái niệm then chốt trong hệ sinh thái tín dụng số</b>:</p>
<table class="t">
  <tr><th>khái niệm</th><th>định nghĩa nghiệp vụ</th><th>vai trò kỹ thuật trên Core T24</th></tr>
  <tr><td>Thấu chi cầm cố</td><td>Vay vốn dựa trên thế chấp hợp đồng tiền gửi điện tử</td><td>Cấp hạn mức chi tiêu âm trên tài khoản CASA</td></tr>
  <tr><td>Tỉ lệ LTV</td><td>Tỉ lệ cấp vốn trên giá trị sổ tiết kiệm (85% đến 90%)</td><td>Công thức toán học khống chế hạn mức trần</td></tr>
  <tr><td>Biên độ Spread</td><td>Độ chênh lệch giữa lãi suất vay và lãi suất tiền gửi</td><td>Xác định biểu lãi suất tự động cho khoản vay</td></tr>
  <tr><td>Ký số Cloud CA</td><td>Ký số hợp đồng tín dụng trên nền tảng đám mây</td><td>Xác thực khuôn mặt sinh trắc học và mã OTP</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Trước tiên ta ôn lại bốn khái niệm then chốt trong hệ thống tín dụng ngân hàng. Thấu chi cầm cố cho phép khách hàng chi tiêu vượt số dư bằng cách thế chấp sổ tiết kiệm. Tỉ lệ cấp vốn khống chế hạn mức tối đa, còn biên độ chênh lệch quy định lãi suất khoản vay."
                },
                {
                    "clear": True,
                    "show": """<div class="box key">Nguyên tắc phong tỏa hai pha trên Core T24: Khi cấp thấu chi cầm cố, số dư sổ tiết kiệm phải được khóa phong tỏa trước. Khách hàng tuyệt đối không được rút tiền gửi khi chưa tất toán xong khoản thấu chi để bảo đảm an toàn thu hồi vốn!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Do sổ tiết kiệm đóng vai trò là tài sản bảo đảm, ngân hàng bắt buộc phải khóa phong tỏa số dư trên hệ thống lõi trước khi cấp hạn mức. Người vay không thể rút tiền gửi khi chưa trả hết dư nợ thấu chi. Nguyên tắc này bảo vệ an toàn vốn tuyệt đối cho ngân hàng."
                }
            ]
        },
        # 3. CONCEPT
        {
            "id": "concept",
            "kind": "concept",
            "title": "Kiến trúc Hệ sinh thái Tín dụng Squad Lending và Core T24",
            "steps": [
                {
                    "show": """<div>
  <svg width="1500" height="380" viewBox="0 0 1500 380">
    <g font-size="22" fill="#1f2937">
      <text x="750" y="35" text-anchor="middle" font-weight="bold" font-size="26">Kiến trúc Tín dụng Thấu chi Cầm cố Sổ tiết kiệm và Thấu chi Lương</text>
      <rect x="50" y="70" width="280" height="240" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
      <text x="190" y="115" text-anchor="middle" font-weight="bold">1. LOS & App Portal</text>
      <text x="190" y="160" text-anchor="middle">Chọn sổ tiết kiệm 100M</text>
      <text x="190" y="200" text-anchor="middle">Ký số Cloud CA</text>
      <text x="190" y="240" text-anchor="middle">Quét mặt sinh trắc học</text>

      <rect x="410" y="70" width="320" height="240" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>
      <text x="570" y="115" text-anchor="middle" font-weight="bold">2. Lending Hub</text>
      <text x="570" y="160" text-anchor="middle">Tra cứu Cổng CIC B2B</text>
      <text x="570" y="200" text-anchor="middle">Kiểm tra Whitelist lương</text>
      <text x="570" y="240" text-anchor="middle">Tính LTV và Lãi Spread</text>

      <rect x="810" y="70" width="290" height="240" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
      <text x="955" y="115" text-anchor="middle" font-weight="bold">3. Core Banking T24</text>
      <text x="955" y="160" text-anchor="middle">Khóa phong tỏa sổ AZ</text>
      <text x="955" y="200" text-anchor="middle">Cấp hạn mức thấu chi CASA</text>
      <text x="955" y="240" text-anchor="middle">Hạch toán sổ cái hai pha</text>

      <rect x="1180" y="70" width="280" height="240" rx="12" fill="#f3e8ff" stroke="#9333ea" stroke-width="3"/>
      <text x="1320" y="115" text-anchor="middle" font-weight="bold">4. Cổng NAPAS 247</text>
      <text x="1320" y="160" text-anchor="middle">Giải ngân liên ngân hàng</text>
      <text x="1320" y="200" text-anchor="middle">Khóa phân tán Redis</text>
      <text x="1320" y="240" text-anchor="middle">Trích nợ Partial Debit</text>

      <line x1="330" y1="150" x2="410" y2="150" stroke="#0284c7" stroke-width="4"/>
      <line x1="730" y1="150" x2="810" y2="150" stroke="#d97706" stroke-width="4"/>
      <line x1="1100" y1="150" x2="1180" y2="150" stroke="#16a34a" stroke-width="4"/>
    </g>
  </svg>
</div>""",
                    "focus": [0, 0, 0],
                    "say": "Đây là bức tranh toàn cảnh kiến trúc tín dụng tự động tốc độ cao. Khách hàng chọn sổ tiết kiệm cần cầm cố rồi ký số hợp đồng qua đám mây. Trục tích hợp điều phối kiểm tra lịch sử nợ, phát lệnh phong tỏa sổ tiết kiệm trên lõi và cấp hạn mức giải ngân an toàn."
                },
                {
                    "clear": True,
                    "show": """<p><b>Ba dòng sản phẩm tín dụng chủ lực trong Squad Lending</b>:</p>
<table class="t">
  <tr><th>dòng sản phẩm</th><th>phương thức cấp vốn</th><th>đặc điểm kiến trúc tích hợp</th></tr>
  <tr><td>Thấu chi cầm cố sổ tiết kiệm</td><td>Cấp hạn mức LTV 85% đến 90% dựa trên sổ tiền gửi</td><td>Phong tỏa tài khoản AZ và mở hạn mức thấu chi CASA</td></tr>
  <tr><td>Thấu chi lương tín chấp</td><td>Cấp hạn mức gấp 2 đến 3 lần lương hàng tháng</td><td>Phân tích lịch sử chi lương lô và lọc danh sách ưu tiên</td></tr>
  <tr><td>Vay trên thẻ tín dụng</td><td>Trích xuất hạn mức thẻ khả dụng sang tiền mặt</td><td>Đồng bộ hệ thống thẻ và phát hành thẻ ảo tức thì</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Hệ sinh thái tín dụng gồm ba dòng sản phẩm chính. Thấu chi cầm cố dựa trên tài sản bảo đảm là sổ tiền gửi có sẵn. Thấu chi lương dựa trên dòng tiền thu nhập ổn định, còn vay trên thẻ chuyển đổi hạn mức thẻ thành tiền mặt linh hoạt."
                }
            ]
        },
        # 4. SYMBOL
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Quy ước Ký hiệu và Công thức Thấu chi Cầm cố",
            "steps": [
                {
                    "show": """<p><b>Công thức tính toán hạn mức và lãi suất thấu chi</b>:</p>
<div class="box key">
$$\\text{Hạn mức cấp: } H = V \\times 85\\%$$
$$\\text{Lãi suất thấu chi: } r = 6\\% + 2.5\\% = 8.5\\%\\text{ mỗi năm}$$
$$\\text{Tiền lãi thực tế mỗi tháng: } L = S \\times \\frac{r}{12}$$
</div>
<p>Trong đó $V$ là giá trị sổ tiết kiệm, $r$ là lãi suất thấu chi gồm lãi tiền gửi cộng biên độ chênh lệch, và $S$ là số tiền rút thấu chi thực tế.</p>""",
                    "focus": [0, 0, 0],
                    "say": "Theo quy chuẩn nghiệp vụ, ta thiết lập công thức tính toán tài chính. Hạn mức thấu chi bằng giá trị sổ tiết kiệm nhân với tỉ lệ cấp vốn. Lãi suất vay bằng lãi tiền gửi cộng biên độ chênh lệch, và người vay chỉ trả lãi trên số tiền thực tế sử dụng."
                },
                {
                    "clear": True,
                    "show": """<p><b>Cơ chế phong tỏa sổ tiết kiệm trước khi cấp hạn mức trên Core T24</b>:</p>
<pre><code>// 1. Phong tỏa số dư sổ tiết kiệm trên phân hệ tiền gửi
err := t24.LockDepositAccount(ctx, depositAccNo, holdAmount)
if err != nil { return ErrDepositLockFailed }

// 2. Cấp hạn mức thấu chi vào tài khoản thanh toán CASA
err = t24.GrantOverdraftLimit(ctx, casaAccNo, limitAmount)
if err != nil { t24.UnlockDepositAccount(ctx, depositAccNo); return err }</code></pre>""",
                    "focus": [0, 0, 0],
                    "say": "Để bảo đảm an toàn sổ cái, ta áp dụng quy trình hai pha nghiêm ngặt. Bước một hệ thống khóa phong tỏa số dư trên sổ tiết kiệm. Nếu thành công thì bước hai mới cấp hạn mức chi tiêu, còn nếu thất bại thì lập tức giải phóng tài nguyên."
                }
            ]
        },
        # 5. EXAMPLE
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Cầm cố Sổ tiết kiệm 100 Triệu thấu chi 85 Triệu",
            "checks": [
                "100000000 * 85 // 100 == 85000000",
                "60 + 25 == 85",
                "50000000 * 85 // 12000 == 354166",
                "354166 > 300000",
                "85000000 > 50000000"
            ],
            "steps": [
                {
                    "show": """<p><b>Dữ liệu bài toán thấu chi cầm cố sổ tiết kiệm</b>:</p>
<ul>
<li>Sổ tiết kiệm điện tử có giá trị: $V = 100\\,000\\,000$ đồng, lãi suất tiền gửi $6\\%$ mỗi năm.</li>
<li>Tỉ lệ cấp vốn: $85\\%$, biên độ chênh lệch: $2.5\\%$ mỗi năm.</li>
<li>Khách hàng rút số tiền thấu chi thực tế: $S = 50\\,000\\,000$ đồng trong thời gian $1$ tháng.</li>
</ul>""",
                    "focus": [0, 0, 0],
                    "say": "Ta xem xét khách hàng có sổ tiết kiệm một trăm triệu đồng với lãi suất sáu phần trăm một năm. Tỉ lệ cấp vốn tám mươi lăm phần trăm và biên độ lãi vay là hai phẩy năm phần trăm. Khách hàng rút năm mươi triệu đồng để chi tiêu trong một tháng."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 1: Tính hạn mức thấu chi và lãi suất vay</b>:</p>
$$\\text{Hạn mức tối đa: } H = 100\\,000\\,000 \\times 85\\% = 85\\,000\\,000\\text{ đồng}$$
$$\\text{Lãi suất vay thấu chi: } r = 6\\% + 2.5\\% = 8.5\\%\\text{ mỗi năm}$$""",
                    "focus": [0, 0],
                    "say": "Theo công thức, bước một ta tính được hạn mức thấu chi tối đa là tám mươi lăm triệu đồng. Lãi suất vay thấu chi bằng sáu phần trăm cộng hai phẩy năm phần trăm được tám phẩy năm phần trăm một năm."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2: Tính tiền lãi thực tế phải trả trong tháng</b>:</p>
$$\\text{Tiền lãi vay 1 tháng: } L = 50\\,000\\,000 \\times \\frac{8.5\\%}{12} \\approx 354\\,167\\text{ đồng}$$
<div class="box key">Hiệu quả tài chính: Khách hàng chỉ tốn 354 nghìn đồng tiền lãi vay nhưng vẫn bảo toàn nguyên vẹn toàn bộ tiền lãi của sổ tiết kiệm 100 triệu đồng!</div>""",
                    "focus": [0, 0],
                    "say": "Bước hai, vì khách hàng chỉ rút năm mươi triệu nên tiền lãi vay một tháng chỉ có ba trăm năm mươi tư nghìn đồng. Do đó người vay giải quyết được việc gấp mà không làm mất khoản tiền lãi tiết kiệm lớn hơn rất nhiều."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 3: Điều phối luồng tích hợp hệ thống</b>:</p>
<table class="t">
<tr><th>trình tự</th><th>phân hệ xử lý</th><th>thao tác kỹ thuật</th></tr>
<tr><td>1. Khóa sổ</td><td>Core T24 AZ</td><td>Phong tỏa 100 triệu trên sổ tiết kiệm</td></tr>
<tr><td>2. Mở hạn mức</td><td>Core T24 CASA</td><td>Cấp hạn mức thấu chi 85 triệu vào tài khoản</td></tr>
<tr><td>3. Ký số</td><td>FPT Cloud CA</td><td>Xác thực sinh trắc học và ký hợp đồng số</td></tr>
<tr><td>4. Giải ngân</td><td>NAPAS 247</td><td>Chuyển 50 triệu qua NAPAS với khóa Redis 300s</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Bước ba hệ thống điều phối toàn diện các phân hệ. Sổ tiết kiệm được phong tỏa trên lõi trước, tiếp theo hạn mức thấu chi được cấp vào tài khoản. Khách hàng ký số hợp đồng điện tử và nhận tiền chuyển khoản ngay trong một phút."
                }
            ]
        },
        # 6. CHECK
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: Xử lý Rút Sổ khi Đang Thấu chi",
            "checks": [
                "85000000 > 50000000",
                "85 - 60 == 25"
            ],
            "steps": [
                {
                    "show": """<p><b>Tình huống nghiệp vụ rủi ro khi phỏng vấn Senior</b>:</p>
<div class="box key">Nếu khách hàng đang có dư nợ thấu chi 50 triệu đồng mà cố tình bấm nút rút sổ tiết kiệm 100 triệu trên ứng dụng, hệ thống xử lý ra sao?</div>
<ul>
<li>(A) Tự động cho rút toàn bộ 100 triệu về tài khoản.</li>
<li>(B) Báo lỗi và khóa toàn bộ tài khoản của người dùng.</li>
<li>(C) Từ chối rút sổ vì số dư đang bị phong tỏa, chỉ cho phép tất toán khi đã trả hết nợ hoặc chọn tính năng tất toán cấn trừ nợ.</li>
</ul>""",
                    "focus": [0, 0, 0],
                    "say": "Vì khách hàng đang có dư nợ thấu chi chưa trả hết, một tình huống thực tế đặt ra là khi người vay muốn rút sớm sổ tiết kiệm. Do đó hệ thống ngân hàng phải xử lý cẩn trọng để không thất thoát tài sản. Mời bạn chọn phương án xử lý chuẩn mực nhất theo quy định."
                },
                {
                    "clear": True,
                    "show": """<p><b>Đáp án chính xác: Lựa chọn (C)</b></p>
<div class="box key">Cơ chế bảo vệ: Sổ tiết kiệm đang ở trạng thái bị phong tỏa (Locked Account) trên Core T24!</div>
<p>1. Lệnh rút tiền bị chặn ngay tại tầng lõi vì số dư khả dụng của sổ tiết kiệm bằng 0.</p>
<p>2. Khách hàng chỉ có 2 lựa chọn: Nộp tiền trả hết dư nợ 50 triệu để giải chấp, hoặc thực hiện <b>Tất toán Cấn trừ Tự động</b>.</p>
<p>3. Khi cấn trừ: Hệ thống thu hồi 50 triệu gốc và lãi vay, phần tiền dư còn lại được chuyển về tài khoản CASA!</p>""",
                    "focus": [0, 0, 0],
                    "say": "Đáp án chính xác là lựa chọn C. Do tài khoản tiền gửi đang bị phong tỏa trên hệ thống lõi nên lệnh rút tiền sẽ bị từ chối ngay lập tức. Khách hàng có thể chọn tính năng tự động cấn trừ để thu hồi nợ trước rồi nhận lại số tiền thừa."
                }
            ]
        },
        # 7. PITFALL
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Phỏng vấn: Sai lầm Thứ tự Khóa và Thu hồi Nợ",
            "steps": [
                {
                    "show": """<p><b>Ba sai lầm nghiêm trọng trong tích hợp tín dụng thấu chi</b>:</p>
<table class="t">
<tr><th>sai lầm sơ cấp</th><th>hậu quả tài chính</th><th>giải pháp chuẩn Senior</th></tr>
<tr><td>Cấp hạn mức trước khi phong tỏa sổ</td><td>Khách hàng rút tiền gửi tẩu tán vốn</td><td>Áp dụng quy trình hai pha: khóa sổ thành công mới cấp hạn mức</td></tr>
<tr><td>Không hỗ trợ trích nợ từng phần</td><td>Treo nợ quá hạn vì tài khoản thiếu vài nghìn đồng</td><td>Thiết lập Partial Debit thu tối đa số dư khả dụng</td></tr>
<tr><td>Giải ngân không có khóa độc quyền</td><td>Người dùng bị chi tiền hai lần khi mạng lỗi</td><td>Khóa phân tán Redis 300s kết hợp máy trạng thái SAGA</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Nhiều kỹ sư mắc sai lầm khi cấp hạn mức trước khi phong tỏa sổ tiết kiệm khiến người vay có cơ hội rút sạch tiền. Sai lầm khác là từ chối thu nợ khi tài khoản thiếu một số tiền nhỏ. Ta khắc phục bằng quy trình khóa chặt chẽ và trích nợ từng phần thông minh."
                },
                {
                    "clear": True,
                    "show": """<div class="box key">Bài học phỏng vấn Senior: Tính toàn vẹn sổ cái đòi hỏi mọi hành động cấp vốn phải có tài sản bảo đảm khóa chặn trước. Cơ chế thu hồi nợ phải linh hoạt trích nợ từng phần để giảm thiểu tỉ lệ nợ xấu cho ngân hàng!</div>""",
                    "focus": [0, 0],
                    "say": "Quy tắc cốt lõi của ngân hàng là không bao giờ cấp tín dụng khi tài sản bảo đảm chưa được phong tỏa an toàn. Đồng thời tiến trình thu nợ tự động phải hỗ trợ trích nợ từng phần để bảo vệ điểm tín dụng cho khách hàng."
                }
            ]
        },
        # 8. QUIZ
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán và Điều phối Thấu chi",
            "checks": [
                "100000000 * 90 // 100 == 90000000",
                "90000000 - 85000000 == 5000000"
            ],
            "steps": [
                {
                    "pause": 15,
                    "show": """<p><b>Câu hỏi trắc nghiệm kiến trúc tín dụng</b>: Khi một khách hàng muốn vay thấu chi với tỉ lệ cấp vốn tối đa 90% trên sổ tiết kiệm 100 triệu đồng, nhưng hồ sơ tra cứu Cổng CIC cho thấy khách hàng đang có nợ nhóm 2 tại một tổ chức tín dụng khác, hệ thống xử lý ra sao?</p>
<ul>
  <li><b>A</b>: Tiếp tục cấp hạn mức 90 triệu đồng vì có sổ tiết kiệm bảo đảm 100%.</li>
  <li><b>B</b>: Từ chối luồng phê duyệt tự động ngay tại cổng kiểm soát rủi ro vì vi phạm chính sách nợ nhóm 2.</li>
  <li><b>C</b>: Tự động tịch thu sổ tiết kiệm của khách hàng.</li>
  <li><b>D</b>: Chuyển khoản nợ nhóm 2 sang cho ngân hàng khác.</li>
</ul>""",
                    "focus": [0, 0, 0, 0],
                    "say": "Xin mời bạn trả lời câu hỏi nghiệp vụ tín dụng. Khách hàng có sổ tiết kiệm bảo đảm nhưng lại đang dính nợ nhóm hai tại một tổ chức tín dụng khác. Hệ thống kiểm soát rủi ro sẽ ra quyết định thế nào. Bạn có 15 giây suy nghĩ trước khi nghe đáp án chuẩn xác."
                },
                {
                    "clear": True,
                    "show": """<div class="box key"><b>Đáp án chính xác là B</b>!</div>
<p><b>Bước 1 — Nguyên tắc quản trị rủi ro tín dụng tại ngân hàng</b>:</p>
<table class="t">
  <tr><th>yếu tố kiểm tra</th><th>kết quả thực tế</th><th>quy định rủi ro ngân hàng</th></tr>
  <tr><td>Tài sản bảo đảm</td><td>Sổ tiết kiệm 100 triệu hợp lệ</td><td>Đủ điều kiện về tài sản</td></tr>
  <tr><td>Lịch sử tín dụng CIC</td><td>Đang có nợ Nhóm 2 (Cần chú ý)</td><td>Vi phạm điều kiện phê duyệt tự động thẳng</td></tr>
</table>""",
                    "focus": [0, 0, 0],
                    "say": "Đáp án chính xác là phương án B. Dù khách hàng có sổ tiết kiệm làm tài sản thế chấp nhưng lịch sử tín dụng quốc gia cho thấy đang có nợ nhóm hai. Đây là dấu hiệu rủi ro thanh toán cần đặc biệt lưu ý."
                },
                {
                    "clear": True,
                    "show": """<p><b>Bước 2 — Hành động điều phối của hệ thống</b>:</p>
<div class="box key">Hệ thống lập tức dừng luồng phê duyệt thẳng tự động, ghi log vi phạm chính sách tín dụng và chuyển hồ sơ sang luồng thẩm định ngoại lệ của cấp phê duyệt rủi ro, không tự ý giải ngân tự động!</div>""",
                    "focus": [0, 0, 0],
                    "say": "Bước hai, hệ thống tự động chặn luồng phê duyệt thẳng để ngăn ngừa rủi ro phát sinh. Hồ sơ được chuyển sang luồng thẩm định có sự can thiệp của chuyên viên quản trị rủi ro. Tính năng này giúp ngân hàng kiểm soát chặt chẽ danh mục cho vay."
                }
            ]
        },
        # 9. RECAP
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Hệ sinh thái Tín dụng Squad Lending",
            "steps": [
                {
                    "show": """<div class="chain">
  <span>Tiếp nhận hồ sơ thấu chi sổ / lương & E-KYC</span> &rarr;
  <span>Tra cứu Cổng CIC B2B qua mTLS & Lọc Whitelist</span> &rarr;
  <span>Phong tỏa sổ tiết kiệm trên Core T24 & Ký số Cloud CA</span> &rarr;
  <span>Cấp hạn mức thấu chi CASA LTV 85% - 90%</span> &rarr;
  <span>Khóa phân tán Redis 300s & Giải ngân NAPAS 247</span> &rarr;
  <span>Thu nợ định kỳ Auto-Debit & Trích nợ từng phần</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>trụ cột kiến trúc</th><th>giá trị bảo vệ tài chính ngân hàng ACB</th></tr>
  <tr><td>Thấu chi cầm cố sổ & lương</td><td>Đa dạng hóa sản phẩm tín dụng số, cấp vốn siêu tốc sub-1 phút</td></tr>
  <tr><td>Phong tỏa hai pha T24</td><td>Triệt tiêu 100% rủi ro rút tiền gửi khi đang có dư nợ thấu chi</td></tr>
  <tr><td>Ký số Cloud CA & Trích nợ từng phần</td><td>Tự động hóa toàn trình không cần giấy tờ và tối ưu hóa thu hồi nợ</td></tr>
</table>
<p style="margin-top: 15px;"><b>Khẳng định đẳng cấp Senior tại ngân hàng ACB</b>: Nắm vững hệ sinh thái tín dụng thấu chi, làm chủ phân hệ Core T24, bảo vệ tài sản ngân hàng và tự tin chinh phục mức lương 50 triệu gross.</p>""",
                    "focus": [0, 0, 0],
                    "say": "Tóm lại, chuỗi logic gồm tiếp nhận nhu cầu, tra cứu lịch sử nợ, phong tỏa sổ tiết kiệm, cấp hạn mức thấu chi và giải ngân liên ngân hàng an toàn. Nắm vững giải pháp toàn diện này, bạn tự tin làm chủ toàn bộ hệ thống tín dụng ngân hàng số. Bạn hoàn toàn xứng đáng với mức đãi ngộ 50 triệu gross tại ACB."
                }
            ]
        }
    ]
}

with open("lessons/acb/L08_squad_lending_tich_hop_cic_giai_ngan.yaml", "w", encoding="utf-8") as f:
    yaml.dump(lesson, f, allow_unicode=True, sort_keys=False, width=1000)

print("Created lessons/acb/L08_squad_lending_tich_hop_cic_giai_ngan.yaml successfully")
