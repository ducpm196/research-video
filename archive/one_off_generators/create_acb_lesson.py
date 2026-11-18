import os
import sys
import yaml

content = """id: L00
course: ACB
series: "Phỏng vấn Kỹ sư Tích hợp ACB"
title: "Bài 0 — Cẩm nang Phỏng vấn Tích hợp Ngân hàng: Từ Mất gốc đến Senior"
voice: vi-VN-NamMinhNeural
rate: "-5%"
depth: full
source: "curriculum/acb.yaml L00; OCB Global System Analytics Hub (hub-system-graph.md); JD Tuyển dụng Kỹ sư Tích hợp ACB 2026; Chuẩn thanh toán quốc tế ISO 8583 MTI 0200/0210; Temenos T24 OFS XML over IBM MQ"
assumes: [arith, approx]
objectives:
  - "Hiểu rõ kiến trúc tích hợp Core Banking Temenos T24 và Cổng thanh toán NAPAS 247"
  - "Làm chủ mô hình điều phối SAGA, chống trừ tiền kép và tối ưu hóa Oracle 19c"
  - "Nắm vững kịch bản phản xạ tình huống thực tế và tự tin deal mức lương 50 triệu gross"

scenes:
  # ──────────────────────── 1. HOOK ────────────────────────
  - id: hook
    kind: hook
    title: "Khoảng cách giữa lập trình viên bình thường và Kỹ sư Tích hợp Ngân hàng"
    steps:
      - show: |
          <p>Nhiều bạn nghĩ làm backend tích hợp chỉ đơn giản là viết vài API RESTful để lưu dữ liệu vào cơ sở dữ liệu. Nhưng khi bước vào ngân hàng lớn như ACB, một lệnh chuyển tiền bị nghẽn mạng có thể gây thất thoát hàng tỷ đồng hoặc trừ tiền hai lần của khách hàng.</p>
          <div class="box key">Hôm nay: <b>Toàn cảnh kiến trúc tích hợp ngân hàng</b> — từ Temenos T24, NAPAS 247, SAGA đến bí quyết chinh phục mức lương <b>50 triệu gross</b>.</div>
        focus: [1, 2]
        say: "Chào bạn, nhiều bạn nghĩ làm lập trình viên tích hợp chỉ đơn giản là viết vài giao diện lập trình ứng dụng REST để lưu dữ liệu vào bảng. Nhưng trong môi trường ngân hàng thực tế, một lệnh chuyển tiền bị nghẽn mạng có thể làm thất thoát hàng tỷ đồng hoặc trừ tiền hai lần của khách hàng. Hôm nay, chúng ta cùng phân tích toàn cảnh kiến trúc tích hợp ngân hàng, từ Core T24, Cổng NAPAS, điều phối giao dịch phân tán, cho đến bí quyết đàm phán mức lương 50 triệu gross."

  # ──────────────────────── 2. PREREQ ────────────────────────
  - id: prereq
    kind: prereq
    title: "Ôn lại: Đơn vị thời gian, bắt tay mạng và tính nhất quán dữ liệu"
    checks:
      - "1000 * 1000 == 1000000 and 1000 // 10 == 100"
      - "10000 // 100 == 100 and 60 * 1000 == 60000"
    steps:
      - show: |
          <table class="t">
            <tr><th>thông số</th><th>giá trị ngân hàng</th><th>ý nghĩa thực tế</th></tr>
            <tr><td>Độ trễ P99</td><td>dưới 100 ms</td><td>99% giao dịch phản hồi dưới 0,1 giây</td></tr>
            <tr><td>Thông lượng</td><td>10 000 TPS</td><td>hệ thống gánh 10 nghìn lệnh mỗi giây</td></tr>
            <tr><td>Thời gian sống khoá</td><td>60 giây</td><td>khoá chống trùng lặp giữ trong một phút</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4"]
        say: "Trước tiên ta ôn lại ba chỉ số hiệu năng huyết mạch trong ngân hàng. Một giây bằng một nghìn mi li giây. Độ trễ 99 phần trăm phải dưới 100 mi li giây, nghĩa là hầu hết giao dịch chuyển tiền phải phản hồi chớp nhoáng. Thông lượng giờ cao điểm đạt 10 nghìn giao dịch mỗi giây. Và khoá khử trùng lặp được giữ trong 60 giây, tức 60 nghìn mi li giây."

  # ──────────────────────── 3. SYMBOL ────────────────────────
  - id: symbol
    kind: symbol
    title: "Giải mã các thuật ngữ và ký hiệu cốt lõi trong ngành ngân hàng"
    steps:
      - show: |
          <table class="t">
            <tr><th>thuật ngữ</th><th>tên đầy đủ</th><th>vai trò kỹ thuật</th></tr>
            <tr><td>T24 OFS</td><td>Open Financial Service</td><td>chuỗi bản tin giao tiếp với Core Banking Temenos T24</td></tr>
            <tr><td>ISO 8583</td><td>Financial Transaction Message</td><td>chuẩn bản tin tài chính liên ngân hàng qua socket TCP</td></tr>
            <tr><td>SAGA</td><td>Distributed Saga Pattern</td><td>chuỗi giao dịch cục bộ kèm giao dịch bồi hoàn tự động</td></tr>
            <tr><td>STAN / RRN</td><td>Trace & Reference Number</td><td>số định danh đối soát giao dịch duy nhất trong ngày</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4", "1.5"]
        say: "Để phỏng vấn tự tin, bạn cần giải mã chuẩn xác bốn thuật ngữ nền tảng. Thứ nhất, bản tin OFS là định dạng giao tiếp chuẩn của Core Banking Temenos T24 qua hàng đợi IBM MQ. Thứ hai, chuẩn ISO 8583 là giao thức bản tin tài chính qua cổng chuyển mạch NAPAS. Thứ ba, mô hình SAGA là chuỗi giao dịch phân tán giúp tự động hoàn tiền khi đối tác sập. Và thứ tư, số kiểm toán STAN cùng số tham chiếu RRN là hai mã số dùng để đối soát liên ngân hàng."

  # ──────────────────────── 4. CONCEPT ────────────────────────
  - id: concept
    kind: concept
    title: "Kiến trúc luồng chuyển tiền liên ngân hàng 247 qua cổng NAPAS"
    steps:
      - show: |
          <div>
            <svg width="1500" height="380" viewBox="0 0 1500 380">
              <g font-size="22" fill="#1f2937">
                <text x="750" y="35" text-anchor="middle" font-weight="bold" font-size="26">Kiến trúc Tích hợp Luồng Thanh toán Ngân hàng ACB</text>
                <rect x="40" y="70" width="260" height="240" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
                <text x="170" y="115" text-anchor="middle" font-weight="bold">1. Kênh số & Ứng dụng</text>
                <text x="170" y="160" text-anchor="middle">ACB One App</text>
                <text x="170" y="200" text-anchor="middle">API Gateway</text>
                <text x="170" y="240" text-anchor="middle">Xác thực mTLS & FaceID</text>

                <rect x="360" y="70" width="340" height="240" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>
                <text x="530" y="115" text-anchor="middle" font-weight="bold">2. Payment Hub & SAGA</text>
                <text x="530" y="160" text-anchor="middle">Khử trùng lặp Redis dedup</text>
                <text x="530" y="200" text-anchor="middle">Máy trạng thái Saga State</text>
                <text x="530" y="240" text-anchor="middle">Hàng đợi sự kiện Kafka</text>

                <rect x="760" y="70" width="320" height="240" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
                <text x="920" y="115" text-anchor="middle" font-weight="bold">3. Cổng NAPAS & HSM</text>
                <text x="920" y="160" text-anchor="middle">Bản tin ISO 8583 0200/0210</text>
                <text x="920" y="200" text-anchor="middle">Socket TCP nhị phân</text>
                <text x="920" y="240" text-anchor="middle">Mã hoá PIN Block phần cứng</text>

                <rect x="1140" y="70" width="320" height="240" rx="12" fill="#f3e8ff" stroke="#9333ea" stroke-width="3"/>
                <text x="1300" y="115" text-anchor="middle" font-weight="bold">4. Core Banking T24</text>
                <text x="1300" y="160" text-anchor="middle">IBM MQ OFS Queue</text>
                <text x="1300" y="200" text-anchor="middle">Hạch toán ghi nợ ghi có</text>
                <text x="1300" y="240" text-anchor="middle">Oracle 19c PL-SQL</text>

                <line x1="300" y1="190" x2="360" y2="190" stroke="#0284c7" stroke-width="4"/>
                <line x1="700" y1="190" x2="760" y2="190" stroke="#d97706" stroke-width="4"/>
                <line x1="1080" y1="190" x2="1140" y2="190" stroke="#16a34a" stroke-width="4"/>
              </g>
            </svg>
          </div>
        focus: [1, 1, 1, 1]
        say: "Hãy nhìn vào bức tranh toàn cảnh kiến trúc gồm bốn tầng khép kín. Tầng một là kênh số tiếp nhận yêu cầu và xác thực sinh trắc học. Tầng hai là trung tâm thanh toán kiểm tra khử trùng lặp trong Redis và điều phối trạng thái giao dịch qua Kafka. Tầng ba đóng gói bản tin tài chính ISO 8583 gửi qua socket TCP tới cổng NAPAS kết hợp mã hoá phần cứng. Và tầng bốn giao tiếp với Core Banking Temenos T24 qua hàng đợi IBM MQ để hạch toán số dư trên cơ sở dữ liệu Oracle."

  # ──────────────────────── 5. EXAMPLE ────────────────────────
  - id: example
    kind: example
    title: "Tính toán lưu lượng và kiểm soát rủi ro trừ tiền hai lần"
    checks:
      - "10000 * 60 == 600000 and 600000 * 60 == 36000000"
      - "120 + 35 == 155 and 1500 - 155 == 1345"
      - "5000000 // 1000000 == 5 and 5 * 1000 == 5000"
      - "60 * 1000 == 60000"
    steps:
      - show: |
          <table class="t">
            <tr><th>bước tính toán</th><th>công thức số liệu</th><th>kết quả kiểm chứng</th></tr>
            <tr><td>Lưu lượng mỗi phút</td><td>10 000 nhân 60 giây</td><td>600 nghìn giao dịch mỗi phút</td></tr>
            <tr><td>Lưu lượng mỗi giờ</td><td>600 000 nhân 60 phút</td><td>36 triệu giao dịch mỗi giờ</td></tr>
            <tr><td>Thời gian phản hồi</td><td>120 ms cộng 35 ms</td><td>155 ms toàn trình (SLA 1500 ms)</td></tr>
            <tr><td>Thời gian sống khoá</td><td>60 nhân 1000 ms</td><td>60 000 ms giữ khoá chống lặp</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4", "1.5"]
        say: "Ta cùng kiểm tra số liệu tải thực tế của hệ thống. Ở mức 10 nghìn lệnh mỗi giây, mỗi phút hệ thống xử lý 600 nghìn giao dịch, và mỗi giờ lên tới 36 triệu giao dịch. Thời gian xử lý mạng NAPAS 120 mi li giây cộng thời gian hạch toán Core 35 mi li giây ra tổng thời gian 155 mi li giây, nằm rất sâu dưới hạn mức 1500 mi li giây của ngân hàng. Khoá nguyên tử trong Redis được đặt thời gian hết hạn là 60 giây để chặn đứng mọi gói tin gửi lặp."

  # ──────────────────────── 6. CHECK ────────────────────────
  - id: check
    kind: check
    title: "Kiểm tra lại cơ chế bồi hoàn SAGA khi đối tác thứ ba gặp sự cố"
    checks:
      - "1000000 - 500000 == 500000 and 500000 + 500000 == 1000000"
      - "3000 // 1000 == 3 and 10000 - 9999 == 1"
    steps:
      - show: |
          <p>Giả sử khách hàng có 1 triệu đồng, thanh toán hoá đơn điện lực 500 nghìn đồng. Core Banking đã trừ 500 nghìn, số dư còn 500 nghìn. Nhưng cổng điện lực phản hồi hết giờ.</p>
          <div class="box key">Quy tắc vàng: <b>Không hoàn tiền vội vã</b>! Chuyển trạng thái sang nghi vấn, kích hoạt lệnh kiểm tra trạng thái sau 3 giây, nếu đối tác xác nhận chưa nhận tiền thì mới gọi Core hoàn lại 500 nghìn, đưa số dư về đúng 1 triệu đồng.</div>
        focus: [1, 2]
        say: "Bây giờ ta kiểm tra tình huống kinh điển khi đối tác thứ ba bị nghẽn. Giả sử tài khoản có một triệu đồng, trừ nợ 500 nghìn để trả tiền điện, số dư còn 500 nghìn đồng nhưng đối tác báo hết giờ. Người chưa có kinh nghiệm sẽ vội vàng hoàn tiền ngay, dẫn tới nguy cơ đối tác đã gạch nợ thành công và ngân hàng mất trắng 500 nghìn. Kỹ sư cấp cao sẽ giữ lệnh ở trạng thái nghi vấn, tra cứu trạng thái sau 3 giây, và chỉ khi đối tác xác nhận chưa nhận tiền mới kích hoạt giao dịch bồi hoàn để hoàn lại đủ một triệu đồng."

  # ──────────────────────── 7. PITFALL ────────────────────────
  - id: pitfall
    kind: pitfall
    title: "Ba sai lầm nghiêm trọng khiến ứng viên bị đánh trượt vòng kỹ thuật"
    steps:
      - show: |
          <table class="t">
            <tr><th>sai lầm sơ cấp</th><th>hậu quả kỹ thuật</th><th>giải pháp chuẩn Senior</th></tr>
            <tr><td>Tự gọi hàm nội bộ trong Spring</td><td>mất giao dịch quản lý @Transactional</td><td>tách dịch vụ riêng hoặc tự tiêm phụ thuộc</td></tr>
            <tr><td>Khoá tài khoản ngẫu nhiên</td><td>gây lỗi Deadlock ORA-00060 trong Oracle</td><td>khoá theo thứ tự tăng dần của số tài khoản</td></tr>
            <tr><td>Thiếu chỉ mục khoá ngoại</td><td>khoá toàn bộ bảng con khi cập nhật cha</td><td>đánh chỉ mục B-Tree trên mọi cột khoá ngoại</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4"]
        say: "Có ba sai lầm chết người mà người phỏng vấn ACB hay dùng để thử thách ứng viên. Thứ nhất là gọi hàm nội bộ trong cùng một lớp Spring, khiến cơ chế uỷ quyền động không bắt được và mất trắng giao dịch khi có sự cố. Thứ hai là cập nhật tài khoản chuyển và nhận theo thứ tự ngẫu nhiên, dẫn tới bế tắc khoá chéo Deadlock trong Oracle. Ta giải quyết triệt để bằng cách luôn khoá tài khoản nhỏ trước, lớn sau. Và thứ ba là quên đánh chỉ mục trên khoá ngoại, làm Oracle khoá toàn bộ bảng con."

  # ──────────────────────── 8. QUIZ ────────────────────────
  - id: quiz
    kind: quiz
    title: "Tự kiểm tra phản xạ kiến trúc và định vị bản thân"
    checks:
      - "50 - 45 == 5 and 45 + 5 == 50"
      - "12 * 50 == 600 and 600 + 150 == 750"
    steps:
      - show: |
          <p><b>Câu hỏi tình huống</b>: Khi nhà tuyển dụng nói bạn mới có 3 năm tại OCB nên chỉ trả mức lương 35 đến 40 triệu gross, bạn sẽ trả lời thế nào?</p>
          <div class="box key">Đáp án: Khẳng định 3 năm tại OCB giữ vị trí Chuyên viên chính gánh vác các hệ sinh thái huyết mạch T24 và NAPAS, kết hợp kinh nghiệm tài chính tiêu dùng tại Mirae Asset và bằng Cử nhân AI tại trường top UIT. Mức <b>50 triệu gross</b> tương đương 600 triệu lương năm, cùng thưởng hiệu quả đạt tổng gói 750 triệu, hoàn toàn xứng đáng với giá trị tạo ra ngay từ ngày đầu.</div>
        focus: [1, 2]
        say: "Hãy tự kiểm tra câu hỏi quyết định về thương lượng thu nhập. Khi nhà tuyển dụng nói bạn chỉ nên nhận 35 đến 40 triệu vì số năm làm việc, câu trả lời bản lĩnh là chứng minh chiều sâu thực chiến. Bạn là Chuyên viên chính tại OCB trực tiếp kiến trúc cổng Core T24 và NAPAS, từng phụ trách hệ thống cho vay tiêu dùng tại Mirae Asset, và có bằng Cử nhân Trí tuệ Nhân tạo tại trường Đại học Công nghệ Thông tin. Mức lương 50 triệu gross mỗi tháng là 600 triệu một năm, hoàn toàn tương xứng với giá trị tạo ra ngay từ ngày đầu tiên."

  # ──────────────────────── 9. RECAP ────────────────────────
  - id: recap
    kind: recap
    title: "Tổng kết chuỗi logic và hành trang bước vào phòng phỏng vấn"
    steps:
      - show: |
          <table class="t">
            <tr><th>trụ cột</th><th>năng lực then chốt</th><th>cam kết đầu ra</th></tr>
            <tr><td>Nghiệp vụ lõi</td><td>Core T24, NAPAS 247, SAGA, Cho vay LMS</td><td>kiểm soát 100% dòng tiền, không trừ kép</td></tr>
            <tr><td>Kỹ thuật phân tán</td><td>Kafka, Redis, Oracle 19c PL-SQL, Docker</td><td>chịu tải 10 000 TPS, độ trễ sub-100ms</td></tr>
            <tr><td>Đột phá AI</td><td>Phát hiện gian lận thời gian thực, định tuyến</td><td>vũ khí khác biệt vượt trội so với dev thường</td></tr>
            <tr><td>Định vị tài chính</td><td>Chuyên viên chính cấp cao & Cử nhân AI UIT</td><td>bảo vệ vững chắc mức lương 50 triệu gross</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4", "1.5"]
        say: "Tóm lại, hành trang chinh phục ACB được xây dựng trên bốn trụ cột vững chắc. Nắm vững nghiệp vụ Core T24 và NAPAS giúp bạn bảo vệ toàn vẹn dòng tiền. Kỹ thuật hệ phân tán và tối ưu hóa Oracle đảm bảo hệ thống chịu tải cao mượt mà. Nền tảng Trí tuệ Nhân tạo từ trường UIT là vũ khí khác biệt vượt trội. Và phong thái tự tin của một Chuyên viên chính thực chiến sẽ giúp bạn bảo vệ trọn vẹn mức đãi ngộ 50 triệu gross."
"""

target_path = r"D:\research-video\lessons\acb\L00_phong_van_tich_hop_acb.yaml"
os.makedirs(os.path.dirname(target_path), exist_ok=True)
with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully created: {target_path}")

# Also copy to interview/
interview_copy = r"D:\research-video\interview\L00_phong_van_tich_hop_acb.yaml"
with open(interview_copy, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Successfully copied to: {interview_copy}")
