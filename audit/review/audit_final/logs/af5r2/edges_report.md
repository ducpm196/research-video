# AF5R2 — Rà 25 cạnh `requires_ext` ngược chặng: bài X có thật sự cần bài Y không

Ngày đọc: 2026-11-23. Người đọc: tác tử chỉ-đọc (không sửa tệp nào của kho; tệp này là tệp duy nhất được ghi).

Phạm vi: 24 cạnh theo danh sách gốc, cộng cạnh thứ 25 (WEB:L14 ← DVO:L07) do bên điều phối bổ sung giữa chừng.

## 0. Kết luận ngắn

- **25/25 cạnh: `HA`. 0 `GIU`. 0 `KHONG_RO`.**
- Lý do chung (OBSERVED trong từng bài): mọi bài X đều có cảnh `prereq` giảng lại tại chỗ đúng khái niệm mà cạnh `requires_ext` trỏ tới (nhiều cảnh ghi hẳn "Nhắc lại từ đầu"), hoặc bài X không hề dùng khái niệm của Y.
- Không bài X nào có câu `show`/`say` trỏ về bài Y hay khoá của Y ("đã học ở…", "như ở khoá…"). Tên bài Y chỉ xuất hiện trong trường siêu dữ liệu `source:` (không lên màn hình, không đọc thành lời).
- Một cạnh `HA` yếu nhất cần lưu ý: **#13 WEB:L03 ← PLC:L07** (mã trên màn hình truyền hàm không tên `() => …` làm đối số mà không chú giải cú pháp; lời đọc có nói tác dụng từng dòng). Xem mục 3.
- Điều tôi KHÔNG kiểm: việc bài nào thuộc chặng S nào (nhận theo đề bài), nội dung trọn vẹn của các bài Y, và các tệp `labs/` ngoài hai đề nêu ở mục 5.

## 1. Bảng 25 cạnh (24 gốc + 1 bổ sung)

Ký hiệu chứng cứ: `cảnh.bước` theo `id` cảnh và số thứ tự bước (từ 1) trong đặc tả X; `say` = lời đọc, `show` = màn hình. Dòng giáo án là dòng `requires_ext` của X trong `curriculum/<khoá>.yaml`. Không mục X nào trong giáo án có `see_also` hay chú thích lý do cạnh ngay cạnh mục.

| # | cạnh | khái niệm của Y mà X dùng | X giảng lại tại chỗ? | kết luận | chứng cứ |
|---|---|---|---|---|---|
| 1 | DVO:L04 ← CLD:L02 | Y dạy ảnh container là chồng lớp, bộ nhớ đệm khi dựng, ghim phiên bản. X chỉ dùng mã băm và khoảng phiên bản; không dùng ảnh/lớp container | có (mã băm); khoảng phiên bản lấy từ DVO bài 2 | HA | `dvo.yaml:46`. `lessons/dvo/L04_*.yaml:79` prereq.1 say: "Trước hết, ôn hàm băm. … Hàm băm biến một dãy byte bất kỳ thành một chuỗi 64 ký tự, và ta chỉ xem 12 ký tự đầu." Dòng 90 prereq.2: "ở bài 2 ta đã ghi phụ thuộc bằng một khoảng phiên bản" (bài 2 của chính DVO). Chữ "container" chỉ có ở dòng 8 (`source`). |
| 2 | DVO:L05 ← CLD:L05 | trạng thái mong muốn, vòng điều khiển (so – tính khác biệt – làm phần thiếu) | có | HA | `dvo.yaml:54`. prereq.2 say: "Thứ hai, nhắc lại từ đầu thế nào là vòng điều khiển. Đó là một chương trình chạy mãi, cứ vài giây lại làm ba việc, giống máy điều hoà đặt 25 độ, đo được 28 độ thì làm lạnh, về đủ 25 độ thì nghỉ." Không có Pod/Deployment/Kubernetes trong bài (grep 0). |
| 3 | DVO:L06 ← CLD:L13 | tách cấu hình khỏi sản phẩm; xoá ở lớp sau không xoá bí mật; kho bí mật, quyền tối thiểu | có | HA | `dvo.yaml:62`. prereq.2 say: "Thứ hai, nhắc lại từ đầu thế nào là ảnh đóng gói chương trình. … mỗi bước tạo một lớp chồng lên lớp trước, và lớp sau chỉ ghi thêm chứ không sửa được lớp cũ." sym.1 định nghĩa tại chỗ biến môi trường, kho bí mật, quyền tối thiểu, xoay vòng. Ví dụ chính của bài chạy trên lịch sử kho mã, không trên ảnh. |
| 4 | DVO:L07 ← CLD:L08 | phát hành thử (canary) theo bậc lưu lượng. Cuốn chiếu, xanh–lam, số Pod sẵn sàng: X không dùng | có | HA | `dvo.yaml:70`. sym.1 say: "Phát hành thử cho bản mới nhận một phần nhỏ lưu lượng, tức một phần nhỏ các yêu cầu người dùng gửi tới. Phần đó tăng dần từ 1 lên 5, 25 rồi 100 phần trăm, mỗi bậc đều so chỉ số với bản cũ." "cuốn chiếu", "xanh–lam": grep 0 trong X. |
| 5 | DVO:L07 ← DSC:L08 | quyết định bằng xác suất đuôi dưới giả thuyết "tốt như cũ"; định trước ngưỡng và cỡ mẫu; không nhìn trộm rồi dừng sớm. Sai số chuẩn, 1,96, mức ý nghĩa, độ mạnh: X không dùng | có | HA | `dvo.yaml:70`. prereq.2 say: "Bài này làm đúng việc đó, chỉ thay đồng xu bằng 1000 yêu cầu, mỗi yêu cầu lỗi hay không lỗi, và máy làm thay phần đếm." pitfalls.2 say: "Mỗi lần nhìn là thêm một cơ hội để may rủi tạo ra một lúc trông đẹp." Các từ "sai số chuẩn", "1,96", "mức ý nghĩa", "độ mạnh": grep 0. Ghi chú: đầu tệp có `assumes: prob`. |
| 6 | DVO:L10 ← CLD:L12 | Y dạy SLI, SLO, ngân sách lỗi. X không dùng khái niệm nào trong đó; X tự dạy MTBF, MTTR, độ sẵn sàng | không cần (không dùng) | HA | `dvo.yaml:93`. sym.1 say: "Độ sẵn sàng là phần thời gian chạy tốt, bằng thời gian giữa hai lần hỏng chia tổng của nó với thời gian khôi phục." "ngân sách lỗi"/"SLO" chỉ có ở dòng 8 (`source`). |
| 7 | DVO:L11 ← CLD:L11 | nhật ký và chỉ số (hai loại tín hiệu); "1% yêu cầu chậm nhất" (phân vị nói bằng lời thường). Vết truy vết, độ trễ đuôi khi gọi song song: X không dùng | có | HA | `dvo.yaml:101`. intuition.1 say: "Nhánh trên là nhật ký, mỗi yêu cầu ghi một dòng chừng 1 ki lô byte… Nhánh dưới là chỉ số, chỉ vài con số mỗi giây như số yêu cầu, số lỗi, độ trễ". pitfalls.2 say (giảng luôn ngân sách lỗi của CLD:L12): "Ngân sách lỗi nghĩa là nếu nhóm cam kết 99 phẩy 9 phần trăm yêu cầu thành công trong 30 ngày, thì 0 phẩy 1 phần trăm còn lại là phần được phép lỗi." "phân vị", "truy vết": grep 0. |
| 8 | SDP:L12 ← PLC:L07 | chia sẻ tham chiếu (trường `source` của X ghi PLC bài 7 với nghĩa này); hàm bọc hàm (dòng `@functools.lru_cache`) dùng như hộp đen. Bao đóng, hàm bậc cao: không được gọi tên, không cần để theo bài | một phần (chia sẻ tham chiếu: có; dòng trang trí: chỉ nói tác dụng) | HA | `sdp.yaml:109`. prereq.3 say: "phép gán không sao chép danh sách, nên hai tên có thể cùng trỏ vào một danh sách, gọi là chia sẻ tham chiếu." example.1 show: "dòng ghi nhớ bọc hàm: lần đầu gặp n thì tính rồi lưu; lần sau gặp lại thì tra bảng." Đề thực hành `labs/SDP/L12/de.md` chỉ yêu cầu `fib_naive`, `fib_memo` và bộ đếm, làm được bằng từ điển ở prereq.2. |
| 9 | SDP:L12 ← PLC:L12 | hàm thuần, dữ liệu bất biến. map/filter/reduce, dùng chung cấu trúc: X không dùng | có | HA | `sdp.yaml:109`. sym.1 say: "Hàm thuần là hàm mà cùng đầu vào thì luôn cùng đầu ra, và không đọc hay sửa gì bên ngoài như giờ hệ thống, tệp hay biến toàn cục. Dữ liệu bất biến là dữ liệu không bị sửa tại chỗ, muốn sửa thì tạo một bản mới." |
| 10 | SEC:L13 ← DSC:L11 | tỉ lệ nền; tỉ lệ cảnh báo là thật (giá trị dự đoán dương) | có (đếm thẳng trên 1 triệu sự kiện) | HA | `sec.yaml:118`. prereq.2 say: "Cách đếm này cho cùng kết quả với một công thức xác suất có tên riêng, ghi ở phần giải mã ngay sau, nhưng hôm nay ta đếm thẳng nên không cần thuộc công thức." sym.1 say: "Tỉ lệ nền là phần sự kiện thật sự là tấn công." "độ nhạy", "độ đặc hiệu": grep 0. |
| 11 | SWF:L08 ← TOC:L01 | ôtômat hữu hạn đơn định: trạng thái, bảng chuyển, mỗi cặp (trạng thái, sự kiện) đúng một đích | có | HA | `swf.yaml:75`. prereq.2 say: "Máy như vậy có tên là ô-tô-mát hữu hạn đơn định, trong đó ô-tô-mát nghĩa là máy tự chạy theo luật. … Đơn định vì mỗi lúc máy ở đúng một trạng thái, và mỗi cặp trạng thái với sự kiện chỉ dẫn tới một trạng thái." "DFA", "trạng thái chấp nhận", "bảng chữ cái": grep 0. |
| 12 | WEB:L01 ← TOC:L06 | cấu trúc lồng nhau kiểu ngoặc cân bằng, cây. Văn phạm phi ngữ cảnh, suy dẫn: X không dùng | có | HA | `web.yaml:26`. prereq.2 say: "một dãy ngoặc gọi là lồng đúng khi ngoặc mở sau phải đóng trước. … Thẻ HTML lồng nhau y hệt như ngoặc, thẻ mở là ngoặc mở, thẻ đóng là ngoặc đóng." prereq.1 dạy cây có gốc bằng thư mục ổ đĩa. "văn phạm", "suy dẫn": grep 0. |
| 13 | WEB:L03 ← PLC:L07 | hàm là giá trị: hàm không tên được truyền làm đối số để chạy sau (`setTimeout(() => …)`, `.then(() => …)`). Bao đóng = mã + môi trường, lỗi bao đóng trong vòng lặp: X không dùng | một phần (không định nghĩa "hàm là giá trị" hay cú pháp `() =>`; lời đọc nói tác dụng từng dòng) | HA (yếu nhất, xem mục 3) | `web.yaml:41`. example.1 show: `setTimeout(() => console.log(2), 0);` — example.2 say: "dòng hẹn giờ không in gì cả, nó chỉ xếp việc in 2 vào hàng tác vụ." "bao đóng", "hàm không tên", "hàm gọi lại": grep 0 trong X. |
| 14 | WEB:L06 ← SAR:L09 | lũy đẳng; khoá lũy đẳng (khoá yêu cầu) để gửi lại vô hại. "Ghi khoá cùng giao dịch với kết quả": X không dùng | có | HA | `web.yaml:64`. prereq.2 say: "Điều thứ hai là khái niệm lũy đẳng, làm một lần hay nhiều lần đều cho cùng kết quả." example.3 say: "Yêu cầu tạo đơn kèm một khoá lũy đẳng, là mã ngẫu nhiên do ứng dụng tạo cho mỗi lần đặt. Máy chủ có một bảng khoá đã gặp." "giao dịch": grep 0. |
| 15 | WEB:L08 ← SAR:L04 | ý chung "bản lưu còn dùng được bao lâu". Tỉ lệ trúng, chiến lược ghi, hết hạn đồng loạt: X không dùng | có (độ tươi, thẻ phiên bản, 304 đều định nghĩa trong bài) | HA | `web.yaml:80`. sym.1 say: "Tiêu đề thời gian tươi bằng 600 nói bản này còn tươi trong 600 giây, được dùng thẳng mà không hỏi máy chủ." prereq.2 chỉ nhắc "bài 0 và bài 6" của chính WEB. "tỉ lệ trúng", "thời gian sống", "đồng loạt": grep 0. |
| 16 | WEB:L12 ← ESY:L13 | Y dạy dòng trung bình theo chu kỳ thức–ngủ, tuổi thọ pin. X không tính gì về pin | không cần (không dùng) | HA | `web.yaml:111`. Chỗ duy nhất chạm tới: sym.1 say "…phải lưu ngay trạng thái người dùng, như đơn đang điền hay vị trí cuộn, và dừng việc tốn pin." prereq.2 trỏ về bài 3 của chính WEB: "Ở bài 3 ta đã thấy vòng lặp sự kiện". |
| 17 | WEB:L13 ← DSY:L02 | "đồng hồ máy khách không đáng tin", nhắc một câu về đồng hồ logic. Đồng hồ vector, quan hệ xảy ra trước, phát hiện ghi xung đột: X không dùng | có (một mệnh đề định nghĩa, đủ cho chỗ dùng) | HA | `web.yaml:119`. pitfalls.1 say: "Hãy dùng dấu thời gian của máy chủ, đồng hồ logic, tức một bộ đếm tăng dần theo mỗi lần sửa chứ không dựa vào giờ thật. Nhưng hai cách đó vẫn bỏ một bản, nên tốt nhất là hợp nhất theo nghĩa." "vector", "Lamport", "xảy ra trước": grep 0. |
| 18 | DEN:L12 ← DSC:L02 | phép nối theo khoá; khoá trùng làm nhân dòng | có | HA | `den.yaml:115`. prereq.1 say: "ta cần hiểu phép nối hai bảng, tức ghép mỗi dòng của bảng này với dòng của bảng kia có cùng mã, ở đây là mã khách." pitfalls.2 say: "Khách k1 có 2 dòng chiều, nối chỉ theo mã thì mỗi đơn khớp 2 dòng, và doanh thu gấp đôi." "dữ liệu gọn": grep 0. |
| 19 | AIF:L02 ← RBM:L15 | A*: g, h, f = g + h; khoảng cách Manhattan; điều kiện không vượt chi phí thật | có (dạy A* từ đầu trên trò 8 ô số) | HA | `aif.yaml:33`. sym.1 say: "g của n là chi phí đã đi từ trạng thái đầu tới nút n… h của n là ước lượng chi phí còn lại từ n tới đích, gọi là hàm đánh giá." prereq.3 say: "Khoảng cách Manhattan giữa hai ô là số bước đi dọc theo hàng và theo cột, không được đi chéo." Nền bài dựa vào AIF bài 1 ("Ở bài 1, tìm chi phí đều…"), không dựa RBM. |
| 20 | CVI:L03 ← ROB:L11 | phép chiếu lỗ kim u = f·X/Z + c_x; tham số trong. Tham số ngoài, đo độ sâu bằng hai camera: X không dùng | có (suy lại từ tam giác đồng dạng, có ví dụ số) | HA | `cvi.yaml:42`. prereq.1 say: "Trước hết, ta cần hiểu phép chiếu lỗ kim, cách camera đơn giản nhất biến một điểm ba chiều thành điểm ảnh. … Hai tam giác đồng dạng vì có cùng góc, nên độ lệch trên ảnh chia f bằng X chia Z". Nhân ma trận với vector cũng giảng lại ở prereq.2. |
| 21 | CVI:L12 ← PAR:L13 | Y kể hành trình bộ xử lý đồ hoạ. X không dùng kiến thức nào của Y | không cần (không dùng) | HA | `cvi.yaml:110`. prereq.1 say: "Bảng nhắc lại bốn điều. Ở bài 1… Ở bài 7… Ở bài 10 và 11…" (đều là bài của chính CVI). GPU chỉ xuất hiện như bối cảnh: quiz.1 "một thẻ đồ hoạ và một tuần"; recap.2 show có chú giải tại chỗ "bộ xử lý đồ hoạ (GPU)". Trường `source` của X tự ghi: "PAR bài 13 (chặng 2012 kể theo phía phần cứng — bài này kể phía dữ liệu và cách đo)". |
| 22 | CAS:L01 ← ESY:L06 | số dấu phẩy tĩnh (k bit phần lẻ), phép cắt và sai số cắt. Nhân Q8.8, tràn quay vòng/bão hoà: X không dùng | có (cảnh tên "Nhắc lại từ đầu") | HA | `cas.yaml:37`. prereq.2 say: "Số dấu phẩy tĩnh lưu một số nguyên và quy ước k bit cuối là phần lẻ, nên giá trị bằng số nguyên chia 2 mũ k. … Muốn giữ k bit phần lẻ của một số, ta nhân nó với 2 mũ k rồi bỏ phần lẻ, gọi là cắt". "Q8", "bão hoà", "quay vòng": grep 0. |
| 23 | CAS:L04 ← ESY:L10 | đảo ngược ưu tiên, kế thừa ưu tiên, khoá loại trừ, ưu tiên cố định có chiếm quyền. Lập lịch theo hạn sớm nhất, U ≤ 1: X không dùng | có (cảnh tên "Nhắc lại từ đầu") | HA | `cas.yaml:61`. prereq.2 say: "Kế thừa ưu tiên nghĩa là tác vụ đang giữ khoá tạm mang ưu tiên của tác vụ cao nhất đang chờ khoá đó, cho tới khi nhả khoá. Mục đích là để không tác vụ ưu tiên vừa nào chen vào giữa, làm tác vụ cao phải chờ lâu." "hạn sớm nhất", "độ sử dụng": grep 0. |
| 24 | SEC:L14 ← DVO:L10 | rút kinh nghiệm không đổ lỗi. MTBF, MTTR, độ sẵn sàng: X không dùng | có | HA | `sec.yaml:126`. pitfalls.3 say: "Buổi rút kinh nghiệm không đổ lỗi, mà tìm vì sao hệ thống cho phép lỗi xảy ra, rồi ghi việc cần làm có người chịu trách nhiệm và hạn chót." "MTTR", "MTBF", "độ sẵn sàng": grep 0. prereq.2 trỏ về bài 4 của chính SEC ("quyền tối thiểu"). |
| 25 | WEB:L14 ← DVO:L07 (bổ sung theo yêu cầu giữa chừng) | cờ tính năng tách triển khai khỏi phát hành; bật dần theo nhóm người dùng. Phát hành thử (canary), quyết định quay lui bằng xác suất đuôi, quay lui tự động: X không dùng | có | HA | `web.yaml:127` (`requires_ext: ["DVO:L07", "SDP:L14"]`). sym.1 say: "Cờ tính năng là mã mới đã triển khai, tức đã nằm trên máy chủ và trong ứng dụng, nhưng chưa phát hành cho người dùng thấy vì cờ còn tắt. Cờ được bật dần theo nhóm người dùng, và tắt ngay nếu lỗi, không cần phát hành lại." pitfalls.4 tự tính bật 1% so với 100% trên một triệu người. "canary", "phát hành thử", "quay lui", "lưu lượng", "DVO": grep 0 trong X, kể cả trường `source` (dòng 8 chỉ ghi "bài 6, 13" của chính WEB). |

## 2. Tổng số

- `GIU`: 0
- `HA`: 25 (24 cạnh gốc + cạnh 25 bổ sung)
- `KHONG_RO`: 0

Vì không có cạnh `GIU`, không có cạnh nào buộc phải đổi thứ tự khoá/chặng hay thêm đoạn giảng lại để người học khỏi kẹt. Dời DVO sang S08 không tạo chỗ kẹt nào trong sáu bài DVO đã đọc (L04, L05, L06, L07, L10, L11) xét riêng theo các cạnh trỏ sang CLD và DSC; hai bài ngoài DVO có cạnh trỏ vào DVO (SEC:L14 ← DVO:L10, WEB:L14 ← DVO:L07) cũng tự giảng lại phần chúng dùng.

## 3. Cạnh `HA` cần cân nhắc khi hạ xuống `see_also`

Xếp theo mức rủi ro giảm dần. Đây là nhận định của người đọc (INFERRED từ nội dung đã đọc), không phải kết quả đo trên người học.

1. **#13 WEB:L03 ← PLC:L07 (yếu nhất).** Mã trên màn hình ở example.1 và quiz.1 dùng hàm không tên làm đối số (`setTimeout(() => console.log(2), 0)`, `.then(() => …)`, `queueMicrotask(() => …)`). Bài không nói "đây là một hàm được đưa cho `setTimeout` giữ để gọi sau" và không chú giải cú pháp `() =>`. Lời đọc bù bằng cách nói tác dụng từng dòng, nên mục tiêu của bài (đoán thứ tự in) vẫn theo được. Đề thực hành `labs/WEB/L03/de.md` yêu cầu tự viết tập lệnh Node có `Promise.resolve().then(...)` và `setTimeout(..., 0)`; người học phải chép mẫu từ màn hình.
   - Lý do vẫn xếp `HA`: phần bao đóng (trọng tâm của PLC:L07) không được dùng; PLC:L07 dạy bằng Python (`def`, `lambda`, `nonlocal`) nên cũng không lấp được chỗ hở cú pháp JavaScript; khái niệm "hàm là giá trị" còn có ở khoá nền JV2 (chỉ thấy tiêu đề bài tại `curriculum/jv2.yaml:57`, "Hàm là giá trị: hàm ngắn và đường ống Stream", chưa đọc nội dung).
   - Cách rẻ nhất nếu muốn chắc: thêm một câu ở example.1 hoặc sym.1 của WEB:L03, kiểu "phần `() => …` là một việc được gói lại, chưa chạy ngay; ta đưa nó cho lệnh hẹn giờ giữ để gọi sau". Không cần đổi chặng.
2. **#8 SDP:L12 ← PLC:L07.** Dòng `@functools.lru_cache(maxsize=None)` là hàm bọc hàm nhưng bài dùng như hộp đen ("thêm một dòng ghi nhớ phía trên hàm f"). Người học không cần hiểu cơ chế để đạt ba mục tiêu của bài. Rủi ro thấp.
3. **#5 DVO:L07 ← DSC:L08.** Bài tự đủ về lập luận, nhưng vài con số do "máy" đưa ra không tự tính trong bài (xác suất đuôi 0,0033; 32%; 62%). Đây là lựa chọn sư phạm của bài, không phải phụ thuộc vào DSC:L08 (DSC:L08 dùng sai số chuẩn và ngưỡng 1,96, một đường tính khác). Đầu tệp có `assumes: prob`.
4. **#17 WEB:L13 ← DSY:L02.** "Đồng hồ logic" chỉ được định nghĩa bằng một mệnh đề, đủ cho chỗ dùng (một lời khuyên trong pitfalls.1). Đồng hồ vector không xuất hiện.

Các cạnh #6, #16, #21 là trường hợp bài X hoàn toàn không dùng khái niệm của Y; quan hệ đúng nghĩa là "liên quan".

## 4. Ghi chú kèm theo cho người quyết định

- **Câu chữ trỏ về Y:** không có ở bất kỳ bài X nào trong `show`/`say`. Các câu "ở bài N" tìm thấy đều trỏ về bài cùng khoá (DVO:L04 → DVO bài 2; DVO:L06 → DVO bài 4; SEC:L14 → SEC bài 4; WEB:L06, L08 → WEB bài 0, 6; WEB:L12 → WEB bài 3; WEB:L13 → WEB bài 6; WEB:L14 → WEB bài 6; AIF:L02 → AIF bài 1; CVI:L12 → CVI bài 1, 7, 10, 11). Riêng trường `source:` của `lessons/cvi/L03_hieu_chuan_camera.yaml:8` ghi "ROB bài 11 (… — đã học)" và "RBM bài 3 (… — đã học)"; đây là siêu dữ liệu, không lên hình, không đọc.
- **Chú thích đầu tệp giáo án có nói thứ tự học** và sẽ lệch nếu hạ cạnh mà không sửa (tôi không sửa):
  - `curriculum/dvo.yaml:8` — "song song CLD (L02, L05, L08, L11)" (tức tác giả giáo án đã coi DVO học song song CLD, không bắt buộc sau).
  - `curriculum/sdp.yaml:13` — "sau SWF (L00, L06, L08) và PLC (L07, L12); trước SAR".
  - `curriculum/swf.yaml:7` — "L08 sau TOC:L01".
  - `curriculum/web.yaml:10` — "sau … DSY L02 (đồng hồ vector)".
  - `curriculum/den.yaml:11` — "sau DBS (toàn khoá), DSY L03–L14, DSC L02".
  - `curriculum/cvi.yaml:10` — "sau CS115 L02, L21, L34 và ROB L11 (hoặc RBM L03)".
  - `curriculum/cas.yaml:21` — "mỗi bài ghi requires_ext tới các bài nền; học sau các khoá đó".
- **Tiền lệ trong kho:** `curriculum/cas.yaml:29` đã dùng `see_also: ["DVO:L10"]  # liên quan, không bắt buộc học trước` cho CAS:L00.
- `curriculum/tracks.yaml` dòng 1–2 ghi thứ tự lộ trình được tính từ bao đóng `requires` + `requires_ext`; hạ cạnh sẽ đổi kết quả tính đó. Tôi chưa chạy `audit/review/tracks.py`.

## 5. Tệp đã đọc

### Đọc trọn nguyên tệp thô
- `lessons/dvo/L04_san_pham_dung_bat_bien.yaml` (301 dòng)
- `labs/WEB/L03/de.md`, `labs/SDP/L12/de.md`

### Đọc trọn lời đọc, màn hình đọc một phần (22 bài X còn lại, gồm WEB:L14 của cạnh 25)
Đọc qua bản trích tạo bằng một kịch bản chỉ-đọc đặt ở thư mục nháp của phiên (ngoài kho). Bản trích gồm: `title`, `source`, `assumes`, `objectives`, tiêu đề mọi cảnh, **toàn bộ `say` của mọi bước**, và `show` (đã bỏ thẻ HTML/SVG) của các cảnh loại `prereq` và `symbol`. Không đọc: `asr_reviewed`, `focus`, `checks`, toạ độ SVG, và `show` của các cảnh khác (trừ chỗ nêu dưới). Bù lại, đã grep trên tệp thô từng bài X các thuật ngữ riêng của Y và các cụm tham chiếu chéo ("đã học", "như ở", "khoá …", mã khoá).

- `lessons/dvo/L05_ha_tang_dang_ma.yaml`
- `lessons/dvo/L06_cau_hinh_bi_mat_moi_truong.yaml`
- `lessons/dvo/L07_phat_hanh_tiem_tien.yaml`
- `lessons/dvo/L10_su_co.yaml` (vừa là X của cạnh 6, vừa là Y của cạnh 24)
- `lessons/dvo/L11_theo_doi_canh_bao.yaml`
- `lessons/sdp/L12_ky_thuat_ham.yaml` (đọc thêm `show` của cảnh example và pitfalls)
- `lessons/sec/L13_nhat_ky_phat_hien.yaml`
- `lessons/sec/L14_ung_pho_su_co.yaml`
- `lessons/swf/L08_may_trang_thai.yaml`
- `lessons/web/L01_html_dom.yaml`
- `lessons/web/L03_vong_lap_su_kien.yaml` (đọc thêm `show` của intuition, example, pitfalls, quiz)
- `lessons/web/L06_thiet_ke_api.yaml`
- `lessons/web/L08_bo_nho_dem_http.yaml`
- `lessons/web/L12_ung_dung_di_dong.yaml`
- `lessons/web/L13_ngoai_tuyen_dong_bo.yaml`
- `lessons/web/L14_tien_hoa_api.yaml` (cạnh 25; bài Y của cạnh này là DVO:L07, đã đọc trọn lời đọc ở trên)
- `lessons/den/L12_kho_du_lieu.yaml`
- `lessons/aif/L02_a_sao.yaml`
- `lessons/cvi/L03_hieu_chuan_camera.yaml`
- `lessons/cvi/L12_hanh_trinh_imagenet.yaml`
- `lessons/cas/L01_patriot.yaml`
- `lessons/cas/L04_mars_pathfinder.yaml`

Với các bài có cảnh practice nhiều hơn hai bước (DEN:L12, AIF:L02, CVI:L03, CVI:L12, CAS:L01, CAS:L04), hai bước đầu của cảnh practice (lời hướng dẫn chấm, dùng chung mọi bài) bị lọc khỏi bản trích; các bước còn lại chỉ đọc `say`.

### Chỉ đọc `objectives` + tiêu đề các cảnh (bài Y)
`lessons/cld/L02`, `cld/L05`, `cld/L08`, `cld/L11`, `cld/L12`, `cld/L13`, `dsc/L02`, `dsc/L08`, `dsc/L11`, `plc/L12`, `toc/L01`, `toc/L06`, `sar/L04`, `sar/L09`, `esy/L06`, `esy/L10`, `esy/L13`, `dsy/L02`, `rbm/L15`, `rob/L11`, `par/L13`.

Riêng `lessons/plc/L07_bao_dong.yaml`: đọc thêm `show` + `say` của các cảnh hook, prereq, sym, intuition, recap (để xét cạnh 8 và 13).

### Giáo án (đọc một phần)
- Mục của từng bài X và dòng chú thích đầu tệp: `curriculum/dvo.yaml` (đọc dòng 14–120), `sdp.yaml`, `sec.yaml`, `swf.yaml`, `web.yaml`, `den.yaml`, `aif.yaml`, `cvi.yaml`, `cas.yaml` (mỗi tệp: khoảng 3 dòng trước và 9 dòng sau `id` của X, cùng các dòng `#` đầu tệp).
- `curriculum/tracks.yaml` dòng 1–60.
- `curriculum/jv2.yaml`: chỉ một dòng tiêu đề (dòng 57) qua grep.

### Giới hạn của lần đọc này
- Không xem video đã dựng, không nghe âm thanh; chỉ đọc đặc tả.
- Không kiểm vị trí chặng S01…S11 của từng khoá.
- Không đọc trọn bài Y, nên cột "khái niệm của Y" dựa trên `objectives` và tiêu đề cảnh của Y.
- Kết luận `HA` nghĩa là "trong đặc tả X có đoạn giảng lại đủ để theo bài"; chưa có phép thử trên người học thật.
