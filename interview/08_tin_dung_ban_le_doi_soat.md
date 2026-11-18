# CHUYÊN ĐỀ 8: TÍN DỤNG BÁN LẺ VÀ ĐỐI SOÁT CUỐI NGÀY — LTV, DTI, TRÍCH NỢ TỪNG PHẦN, KHOÁ GIẢI NGÂN VÀ HAI CON TRỎ

> **Liên hệ với video**: tài liệu đi kèm bài INT L08 (`lessons/int/L08_tin_dung_ban_le_va_doi_soat_cuoi_ngay.yaml`, bài cuối của khoá INT, giọng NamMinh). Video: [`08_tin_dung_ban_le_doi_soat.mp4`](file:///D:/research-video/interview/video/08_tin_dung_ban_le_doi_soat.mp4) (cùng nội dung, trùng byte với [`INT_L08.mp4`](file:///D:/research-video/interview/video/INT_L08.mp4)), phụ đề [`08_tin_dung_ban_le_doi_soat.srt`](file:///D:/research-video/interview/video/08_tin_dung_ban_le_doi_soat.srt), mục lục chương [`08_tin_dung_ban_le_doi_soat_chapters.txt`](file:///D:/research-video/interview/video/08_tin_dung_ban_le_doi_soat_chapters.txt). Thời lượng và mã băm ghi ở [`MASTER_CURRICULUM_INDEX.md`](file:///D:/research-video/interview/MASTER_CURRICULUM_INDEX.md), không chép lại ở đây. Phần tín dụng bán lẻ và đối soát chi tiết hơn nằm trong [`04_banking_domain_t24_napas.md`](file:///D:/research-video/interview/04_banking_domain_t24_napas.md).
>
> **Mục tiêu**: trả lời được một câu phỏng vấn có số về tín dụng bán lẻ (hạn mức theo LTV, tỉ lệ DTI, trích nợ từng phần), nêu được vì sao khoá giải ngân hết hạn gây giải ngân trùng, và tính được số phép so sánh của đối soát ba bên cuối ngày.
>
> **Quy tắc trung thực của chuyên đề này**: mọi tỉ lệ (LTV, DTI), thời gian khoá, tốc độ so sánh và số giao dịch dưới đây là **số minh hoạ**, không phải số của ngân hàng nào và không phải số đo của ứng viên. *Squad Lending* là tên một nhóm cho vay số trong một tin tuyển dụng đã lưu (**chưa kiểm lại**); bài chỉ mượn sáu mảng tín dụng làm khung ví dụ, không khẳng định ngân hàng nào có đúng sáu mảng này. Nhóm nợ theo TT 31/2024/TT-NHNN **chưa đọc nguyên văn**: đối chiếu hai nguồn thứ cấp, thông tư này đã được TT 37/2025/TT-NHNN sửa đổi theo nguồn thứ cấp, **cần đối chiếu bản hợp nhất** trước khi dẫn con số; không dẫn số điều. Khung pháp lý của ký số từ xa (Cloud CA) cũng cần kiểm lại khi dẫn.

---

## 1. TỪ MỘT LẦN BẤM NÚT ĐẾN SỔ SÁCH ĐỐI SOÁT CUỐI NGÀY

Khách bấm vay một khoản trên ứng dụng ngân hàng số. Từ lúc bấm đến lúc tiền về tài khoản, và đến lúc cuối ngày mọi sổ khớp nhau, hệ thống phải: tính hạn mức an toàn, tra nợ xấu của khách, khoá tài sản bảo đảm, ký hợp đồng, ghi hạn mức vào hệ lõi (hệ ngân hàng lõi giữ sổ cái; ở đây lấy T24 của hãng Temenos làm ví dụ), rồi cuối ngày đối soát hàng triệu giao dịch giữa các bên.

| Mảng nghiệp vụ | Câu hỏi phỏng vấn hay gặp | Con số bạn sẽ tự tính |
|:---|:---|:---|
| Tín dụng bán lẻ | Hạn mức tối đa bao nhiêu, người vay có gánh nổi không, trả thiếu thì sao | hạn mức, tỉ lệ trả nợ trên thu nhập, số tiền thu từng phần |
| Thứ tự an toàn của sổ cái | Khoá tài sản trước hay cấp vốn trước, lỗi giữa chừng thì phục hồi thế nào | hạn mức theo tỉ lệ cho vay |
| Đối soát cuối ngày | Hàng triệu giao dịch của ba bên được so trong bao lâu | số phép so sánh ở ba cỡ dữ liệu |

---

## 2. TỪ CẦN BIẾT TRƯỚC KHI ĐỌC SƠ ĐỒ

| Từ | Nghĩa bằng lời thường |
|:---|:---|
| Thấu chi | cho tiêu quá số dư tới một hạn mức |
| Phong tỏa | khoá một khoản tiền để chủ tài khoản không rút được |
| AZ, CASA | AZ là phân hệ tiền gửi có kỳ hạn của T24; CASA là tài khoản thanh toán dùng chi tiêu hằng ngày |
| LTV | tỉ lệ cho vay trên giá trị tài sản bảo đảm. Ví dụ sổ 100 triệu, LTV 85% (tỉ lệ minh hoạ): hạn mức tối đa 100 × 0,85 = 85 triệu |
| DTI | tỉ lệ tiền trả nợ mỗi tháng trên thu nhập. Ví dụ trả 12 triệu, thu nhập 30 triệu: 12 / 30 = 40% |
| Giải ngân | ngân hàng đưa tiền vay ra cho khách: chuyển tiền vào tài khoản hoặc ghi hạn mức cho khách dùng |
| CIC, năm nhóm nợ | CIC là Trung tâm Thông tin Tín dụng Quốc gia (thuộc Ngân hàng Nhà nước Việt Nam, viết tắt NHNN). Nợ chia 5 nhóm theo TT 31/2024/TT-NHNN (nguồn thứ cấp, chưa đọc nguyên văn; đã được TT 37/2025/TT-NHNN sửa đổi, cần đối chiếu bản hợp nhất): ví dụ quá hạn 10–90 ngày là nhóm 2 (định nghĩa rút gọn, thông tư còn nêu thêm vài trường hợp khác); nhóm 3–5 là nợ xấu |
| Cloud CA, OTP | ký số từ xa với chứng thư số giữ ở nhà cung cấp; OTP là mật khẩu dùng một lần |
| B2B | kết nối thẳng giữa hai tổ chức (ngân hàng với CIC) |
| Redis, khoá 300 giây | Redis là phần mềm giữ dữ liệu trong bộ nhớ, rất nhanh, nhiều máy chủ dùng chung. Trước khi giải ngân, ghi một khoá theo mã khoản vay, tự hết hạn sau 300 giây (số minh hoạ); lệnh giải ngân trùng tới khi khoá còn thì bị chặn |
| Tài sản bảo đảm | tài sản khách đưa ra để bảo đảm trả nợ, ví dụ sổ tiết kiệm hoặc nhà; nếu không trả được, ngân hàng xử lý tài sản đó |
| Cầm cố | giao tài sản cho ngân hàng giữ làm bảo đảm, ví dụ sổ tiết kiệm bị phong tỏa trong lúc còn nợ |
| Tín chấp | vay chỉ dựa vào uy tín và thu nhập của khách, không cần tài sản bảo đảm |
| Bội số lương | hạn mức tín chấp tính bằng một số lần lương tháng, ví dụ 3 lần lương (số minh hoạ) |
| Rút tiền mặt trả góp, thẻ ảo | rút tiền từ hạn mức thẻ tín dụng rồi trả dần từng tháng; số thẻ dùng ngay trên điện thoại, chưa cần thẻ nhựa |
| Thu hộ | ngân hàng thu tiền của khách thay cho bên bán (ví dụ tiền điện) rồi chuyển lại cho bên đó |

---

## 3. TOÀN CẢNH SÁU MẢNG TÍN DỤNG BÁN LẺ

| # | Phân hệ | Nội dung chính |
|:---:|:---|:---|
| 1 | Thấu chi sổ tiết kiệm | phong tỏa sổ trên phân hệ AZ của T24; cấp hạn mức theo LTV |
| 2 | Thấu chi lương tín chấp | phân tích lô chi lương; hạn mức theo bội số lương |
| 3 | Vay trên hạn mức thẻ | rút tiền mặt trả góp; mở thẻ ảo nhanh |
| 4 | Ký số đám mây Cloud CA | hợp đồng điện tử ký từ xa; xác thực khuôn mặt cộng OTP |
| 5 | Cổng CIC B2B quốc gia | tra cứu năm nhóm nợ; kiểm soát trần DTI theo chính sách |
| 6 | Giải ngân và thu nợ | khoá Redis 300 giây; trích nợ từng phần |

**Trích nợ từng phần**: khi đến hạn thanh toán mà tài khoản khách không đủ toàn bộ số tiền, hệ thống thu tối đa theo số dư khả dụng thay vì báo lỗi, để thu hồi được nhiều nhất. Phần còn thiếu **vẫn bị tính ngày quá hạn** để phân nhóm nợ: trích nợ từng phần không xoá nợ.

---

## 4. BA CÔNG THỨC (SỐ MINH HOẠ)

| Đại lượng | Công thức viết bằng chữ | Ví dụ |
|:---|:---|:---|
| Hạn mức tối đa | giá trị tài sản bảo đảm × LTV | 100 triệu × 0,85 = 85 triệu |
| DTI | tiền trả nợ mỗi tháng / thu nhập mỗi tháng | 12 / 30 = 0,4 = 40% |
| Trích nợ từng phần | thu = số dư khả dụng nếu số dư nhỏ hơn số phải trả; còn thiếu = phải trả − thu | phải trả 5, có 2 thì thu 2, còn thiếu 3 |

Ba công thức chỉ là phép nhân, phép chia và phép trừ; điều khó là biết khi nào dùng và khi nào chính sách chặn.

---

## 5. TỰ KIỂM TRA: HẠN MỨC, DTI VÀ THU TỪNG PHẦN (SỐ MINH HOẠ)

**Tình huống**: khách có sổ tiết kiệm 150 triệu, LTV 80%. Thu nhập 25 triệu mỗi tháng, đang trả nợ khác 6 triệu mỗi tháng, khoản mới phải trả thêm 4,5 triệu mỗi tháng. Chính sách ví dụ: chặn duyệt khi DTI trên 50%. Tháng này đến hạn trả 4,5 triệu nhưng số dư khả dụng chỉ có 2,7 triệu. Hỏi: (a) hạn mức tối đa, (b) DTI sau khi vay và có bị chặn không, (c) thu từng phần được bao nhiêu, còn thiếu bao nhiêu.

| Ý | Cách tính | Kết quả |
|:---|:---|:---|
| (a) hạn mức | giá trị sổ × LTV = 150 × 0,80 | 120 triệu |
| (b) DTI | (nợ đang trả + khoản mới) / thu nhập = (6 + 4,5) / 25 | 10,5 / 25 = 42%, thấp hơn 50% nên không bị chặn |
| (c) thu từng phần | thu bằng số dư khả dụng; còn thiếu = phải trả − đã thu | thu 2,7 triệu; còn thiếu 4,5 − 2,7 = 1,8 triệu |

Phần thiếu 1,8 triệu vẫn bị tính ngày quá hạn để phân nhóm nợ.

---

## 6. ĐỐI SOÁT BA BÊN CUỐI NGÀY BẰNG HAI CON TRỎ

**Bài toán giả định**: đối soát cuối ngày (EOD, khâu xử lý cuối ngày) cho 3 000 000 giao dịch trong ngày giữa hệ lõi, NAPAS (công ty chuyển mạch tiền giữa các ngân hàng) và đối tác (ví dụ minh hoạ). Đối soát là so từng giao dịch giữa sổ của các bên để tìm chỗ lệch. Mục tiêu thiết kế giả định: xong trong 5 phút (300 giây).

Ký hiệu O(…) chỉ cỡ số phép tính khi số giao dịch N lớn: O(N) tăng tỉ lệ thuận với N, O(N log N) cỡ N nhân lôgarit cơ số 2 của N, O(N²) cỡ N nhân N.

**Cách ngây thơ**: hai vòng lặp lồng nhau O(N²): (3 × 10⁶)² = 9 × 10¹² phép so sánh cho một cặp danh sách (đối soát đủ hai cặp thì gấp đôi); ở tốc độ giả định 10⁹ phép mỗi giây là 9 000 giây = 2,5 giờ.

**Cách đúng**, hai bước:
1. **Sắp xếp** cả ba danh sách theo mã đối soát RRN (TimSort, cách sắp xếp có sẵn trong thư viện của Python và Java, cỡ O(N log N)).
2. **Duyệt đồng thời bằng hai con trỏ** O(N): con trỏ chỉ tiến một chiều nên mỗi bản ghi được xem đúng một lần.

**Chạy tay** (mảng core = [101, 103, 104, 107, 109], napas = [101, 102, 104]; i cho core, j cho napas, cùng bắt đầu từ 0):

| Bước | i, j | core[i] so napas[j] | Việc làm |
|:---:|:---:|:---|:---|
| 1 | 0, 0 | 101 = 101 | khớp; i++ và j++ |
| 2 | 1, 1 | 103 > 102 | 102 chỉ có ở napas; j++ |
| 3 | 1, 2 | 103 < 104 | 103 chỉ có ở core; i++ |
| 4 | 2, 2 | 104 = 104 | khớp; i++ và j++ |
| 5 | 3, 3 | napas đã hết | 107 và 109 còn dư ở core: đều là lệch |

**Mã giả** (giả định: mã RRN duy nhất trong mỗi danh sách và cả hai danh sách sắp xếp cùng kiểu):

```text
i = 0; j = 0;  // hai con trỏ cùng bắt đầu ở ô 0
while (i < core.size() && j < napas.size()) {  // i, j chỉ tiến
    if (core[i].rrn == napas[j].rrn)
        matchOrFlagAmount(core[i++], napas[j++]);  // so cả số tiền
    else if (core[i].rrn < napas[j].rrn) reportMissingInNapas(core[i++]);
    else reportMissingInCore(napas[j++]);
}
while (i < core.size())  reportMissingInNapas(core[i++]);  // phần dư = lệch
while (j < napas.size()) reportMissingInCore(napas[j++]);
// lặp lại cách này giữa NAPAS và Đối tác
```

Các giao dịch trùng mã được so thêm số tiền; các lệnh lệch được tách vào danh sách nghi vấn.

---

## 7. KHI DỮ LIỆU LỚN DẦN: CÁI GÌ GÃY

Công thức số phép của cột sắp xếp: 3 × N × ⌈log₂ N⌉ + 2 × (N + N), trong đó 3 lần sắp xếp ứng với ba danh sách (mỗi lần N × ⌈log₂ N⌉ phép so sánh) và 2 lượt hai con trỏ ứng với hai cặp danh sách (mỗi lượt đi qua N + N bản ghi). Giả định 10⁹ phép so sánh mỗi giây, 100 byte mỗi bản ghi (số minh hoạ); cột vòng lặp lồng nhau tính một cặp danh sách, cột sắp xếp tính cả ba danh sách. Mã Python chạy thật trong bài cho kết quả:

```text
3000000 gd: 2.5 gio vs 0.21 giay; 0.3 GB/ds
30000000 gd: 250.0 gio vs 2.37 giay; 3.0 GB/ds
300000000 gd: 25000.0 gio vs 27.3 giay; 30.0 GB/ds
```

| Số giao dịch | Vòng lặp lồng nhau (một cặp) | Sắp xếp + hai con trỏ (3 danh sách) | Điều gì gãy, cách xử lý |
|:---|---:|---:|:---|
| 3 triệu (×1) | 2,5 giờ | 0,21 giây | vòng lặp lồng nhau đã quá mục tiêu 5 phút; sắp xếp thì dư sức |
| 30 triệu (×10) | 250 giờ | 2,37 giây | 3 danh sách khoảng 9 GB, một máy 16 GB còn vừa nhưng sát |
| 300 triệu (×100) | 25 000 giờ | 27,3 giây | danh sách vượt bộ nhớ: sắp xếp ngoài bộ nhớ (chia thành mảnh vừa bộ nhớ, sắp từng mảnh rồi trộn lại), hoặc chia theo dải mã đối soát rồi đối soát từng mảnh |

**Đánh đổi**: chia mảnh cần thêm bước chia và gộp kết quả, và thời gian đọc ghi tệp thường vượt thời gian so sánh nên phải đo thật.

---

## 8. BẪY: KHOÁ GIẢI NGÂN HẾT HẠN TRƯỚC KHI HỆ LÕI KỊP TRẢ LỜI

**Sai lầm hay gặp**: tin rằng khoá Redis 300 giây (số minh hoạ) chặn được mọi lệnh giải ngân trùng.

**Tình huống**: hệ lõi quá tải nên trả lời sau 400 giây. Bên gọi hết kiên nhẫn và gửi lại lệnh ở giây thứ 350.

| Thời điểm | Khoá Redis | Điều xảy ra |
|:---|:---|:---|
| giây 0 | đặt khoá, sống 300 giây | lệnh thứ nhất gửi sang hệ lõi |
| giây 300 | khoá tự hết hạn | hệ lõi vẫn chưa trả lời |
| giây 350 | không còn khoá | lệnh thứ hai qua được, giải ngân lần hai |
| giây 400 | không còn khoá | cả hai lệnh đều được ghi: khoản vay giải ngân hai lần |

**Cách chữa**: hai lớp chặn và một lớp phát hiện.

| Lớp | Cách làm | Vì sao cần |
|:---|:---|:---|
| Khoá sớm (lớp chặn 1) | quy tắc kinh nghiệm: thời gian sống của khoá thường chọn ít nhất gấp đôi thời gian chờ tối đa; chờ tối đa 120 giây thì khoá ít nhất 240 giây | giữ khoá còn sống suốt lúc lệnh đang chạy, chưa có trả lời |
| Lớp cuối (lớp chặn 2) | ràng buộc duy nhất (cơ sở dữ liệu từ chối dòng thứ hai trùng mã) theo mã khoản vay và lần giải ngân ở hệ lõi | khoá Redis vẫn có thể mất hoặc hết hạn, còn ràng buộc thì từ chối bản ghi thứ hai |
| Đối soát (lớp phát hiện, không chặn) | so sổ hệ lõi với sổ giải ngân cuối ngày | bắt ca lọt lưới trước khi tiền thất thoát |

---

## 9. THỨ TỰ HAI PHA KHI CẤP THẤU CHI CẦM CỐ

Câu hỏi: cấp hạn mức thấu chi cầm cố sổ tiết kiệm 100 triệu với tỉ lệ cấp vốn 85% (tỉ lệ minh hoạ), thứ tự nào bảo đảm an toàn sổ cái? Đáp án đúng: **phong tỏa sổ tiết kiệm trên phân hệ tiền gửi của hệ lõi trước; sau khi thành công mới cấp hạn mức thấu chi vào tài khoản thanh toán CASA**.

| Trình tự | Thao tác trên hệ lõi | Ý nghĩa quản trị rủi ro |
|:---|:---|:---|
| Pha 1: phong tỏa | phong tỏa sổ tiết kiệm | khách không thể rút tiền gửi khi đang vay |
| Giữa hai pha: ký hợp đồng | khách ký hợp đồng (có thể ký số từ xa); thứ tự này là minh hoạ, quy trình thật theo hợp đồng cầm cố của ngân hàng | có căn cứ pháp lý trước khi cấp vốn |
| Pha 2: cấp vốn | ghi hạn mức thấu chi 85 triệu vào CASA | chỉ cấp vốn khi tài sản bảo đảm đã an toàn |

**Phục hồi khi pha 2 gặp sự cố**:
- Hệ lõi **từ chối rõ ràng** việc cấp hạn mức: hệ thống tự phát lệnh mở phong tỏa sổ tiết kiệm để trả lại trạng thái nguyên vẹn cho khách (nếu lệnh mở cũng lỗi thì đưa vào hàng đợi thử lại và đối soát).
- Chỉ **lỗi mạng hoặc hết giờ chờ**: kết quả là chưa biết, nên truy vấn hệ lõi trước và chỉ mở phong tỏa khi chắc chắn hạn mức chưa được ghi.

---

## 10. BÀI TỰ LÀM BẰNG GIẤY BÚT (`labs/INT/L08`)

Số liệu (số minh hoạ): sổ tiết kiệm 240 triệu, LTV 70%; trả nợ 9 triệu mỗi tháng trên thu nhập 36 triệu; đến hạn phải trả 12 triệu nhưng số dư khả dụng 7,5 triệu; đối soát ba danh sách, mỗi danh sách 2 000 000 giao dịch, tốc độ 10⁹ phép so sánh mỗi giây. Hãy tính tay rồi so với lời giải (`labs/INT/L08/loi_giai.md`), chỉ mở sau khi đã thử.

| Dòng | Đáp án để đối chiếu | Cách tính |
|:---:|:---|:---|
| 1 | `han muc LTV 70%: 168 trieu` | 240 × 0,70 |
| 2 | `DTI: 25%` | 9 / 36 |
| 3 | `thu tung phan: 7.5 trieu, con thieu 4.5 trieu` | thu bằng số dư khả dụng; còn thiếu 12 − 7,5 |
| 4 | `doi soat long nhau: 1.1 gio` | 2 000 000 × 2 000 000 = 4 × 10¹² phép; chia 10⁹ được 4 000 giây; chia 3 600 được 1,11 giờ, làm tròn 1,1 |
| 5 | `doi soat sap xep: 0.13 giay` | ⌈log₂ 2 000 000⌉ = 21 (2²⁰ = 1 048 576 chưa tới 2 triệu, 2²¹ = 2 097 152 đã vượt); 3 × 2 000 000 × 21 = 126 000 000; 2 × (2 000 000 + 2 000 000) = 8 000 000; tổng 134 000 000 phép, chia 10⁹ được 0,134 giây, làm tròn 0,13 |

Bài giấy bút nên không có lệnh chấm tự động. Có thể tự kiểm sau khi đã tính tay bằng một dòng lệnh Python ghi trong `labs/INT/L08/de.md`.

---

## 11. CHUỖI LOGIC CẦN NHỚ KHI PHỎNG VẤN

Hạn mức theo LTV, kiểm DTI, tra CIC → khoá tài sản trước, ký, rồi mới cấp vốn → khoá giải ngân sống lâu hơn thời gian chờ, kèm ràng buộc duy nhất → đối soát cuối ngày: sắp xếp rồi hai con trỏ O(N log N).

| Giá trị chuyên môn | Điều cần chứng minh khi phỏng vấn |
|:---|:---|
| Tín dụng bán lẻ | Tính được hạn mức, DTI, thu từng phần; thứ tự phong tỏa, ký, cấp hạn mức; chống giải ngân trùng |
| Đối soát cuối ngày | Hai con trỏ sau khi sắp xếp; số đo thật chỉ nêu nếu có; tỉ lệ và tốc độ trong bài chỉ là số minh hoạ |

---

## 12. NHỮNG ĐIỀU KHÔNG ĐƯỢC KHẲNG ĐỊNH

| Không nói | Lý do | Nói thay bằng |
|:---|:---|:---|
| "Ngân hàng nào đó có đúng sáu mảng tín dụng này" | Squad Lending chỉ là tên nhóm trong một tin tuyển dụng đã lưu, chưa kiểm lại | "Em dùng sáu mảng này làm khung để giải thích" |
| LTV 85%, DTI 50%, khoá 300 giây là chính sách của một ngân hàng | đều là số minh hoạ | "Tỉ lệ này em lấy làm ví dụ; chính sách thật do ngân hàng quy định" |
| Trích nợ từng phần là hết nợ | phần thiếu vẫn tính ngày quá hạn để phân nhóm nợ | "Phần còn thiếu vẫn tính quá hạn" |
| Khoá Redis là đủ để chặn giải ngân trùng | khoá có thể hết hạn hoặc mất | "Cần thêm ràng buộc duy nhất ở hệ lõi, và đối soát để phát hiện" |
| Số điều hoặc ngưỡng ngày của thông tư nhóm nợ như thể đã đối chiếu bản hợp nhất | TT 31/2024/TT-NHNN chưa đọc nguyên văn; TT 37/2025/TT-NHNN đã sửa đổi theo nguồn thứ cấp | "Em đối chiếu bản hợp nhất trước khi dẫn con số" |
| Số giây, giờ của đối soát là số đo thật của hệ thống nào đó | tốc độ 10⁹ phép mỗi giây và số giao dịch chỉ là giả định | "Đây là tính toán giả định; số đo thật phải đo trên hệ thống" |
