# Mẫu E — phần 3: đã đọc 10/10 bài

Bài: HCI L10, INT L02, IRS L10, JVA L03, LLM L01, MLO L11, NET L04, OSY L13, PAR L01, PLC L00. Đã đọc toàn bộ đặc tả YAML, mục giáo án `curriculum/<khoá>.yaml`, `audit/hci/sources_L10.md`, `audit/irs/sources_L10.md`, chapters + `_frames.txt`, và 5 khung hình mỗi bài.

## 1. Chuẩn xác

| Bài | Mức (MUST/SHOULD) | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/nguồn) | Đề xuất sửa | Tin cậy (CONFIRMED/PLAUSIBLE) |
|---|---|---|---|---|---|---|
| HCI L10 | SHOULD | formula, step 1 (say) | "Vì mỗi số p i đều nhỏ hơn 1 rất nhiều, nên cứ thêm một lớp độc lập thực sự là rủi ro lại giảm đi hàng chục hoặc hàng trăm lần." | Khẳng định tuyệt đối. Bảng ký hiệu của chính bài cho $0 \le p_i \le 1$. Một lớp độc lập có $p_i = 0{,}5$ chỉ làm rủi ro giảm 2 lần, $p_i = 0{,}8$ chỉ giảm 1,25 lần. Mức giảm là $1/p_i$, không phải luôn chục hay trăm lần. | "giảm đi $1/p_i$ lần; với lớp bắt 99% lỗi ($p_i = 0{,}01$) là 100 lần" | CONFIRMED |
| HCI L10 | SHOULD | concept (show + say) | "Thứ tự ưu tiên thiết kế chống lỗi (từ mạnh nhất tới yếu nhất)" / "bạn phải ưu tiên theo đúng ba tầng từ mạnh xuống yếu" | Chính `audit/hci/sources_L10.md` (đối chiếu 2026-11-09) ghi rằng Norman (tr. 202–203) **không xếp hạng** ba cơ chế "theo thứ tự hiệu quả", và Norman gọi Undo là "perhaps the most powerful tool". Bài vẫn trình bày thứ hạng như một quy chuẩn có nguồn. | Ghi rõ "cách xếp của bài" hoặc bỏ chữ "mạnh nhất → yếu nhất", như ghi chú trong tệp nguồn đã đề xuất | CONFIRMED (theo tệp nguồn) |
| INT L02 | SHOULD | example (title, chapters 03:42, khung 00037) | "Thực hành: Xử lý 5,000 Yêu cầu Chuyển tiền với Khóa Phân tán" | Tiếng Việt dùng dấu phẩy làm dấu thập phân, nên "5,000" đọc thành 5, không phải 5 000. Thân bài lại viết $5\,000$. Chữ trên màn hình mâu thuẫn với lời đọc "năm nghìn". | "5 000" | CONFIRMED |
| INT L02 | SHOULD | recap (show + say) | "khẳng định mức đãi ngộ 50 triệu gross" / "bảo vệ mức lương 50 triệu gross tại ACB" | Con số lương thực tế không có nguồn trong bài và không có trong `source:` của bài. Đây là mục tiêu cá nhân (`interview/07_salary_negotiation_50m_gross.md`) nhưng lại được nói như kết quả chắc chắn của bài học. | Bỏ đi, hoặc ghi rõ "mục tiêu đàm phán của bạn, không phải mức chuẩn" | PLAUSIBLE |
| INT L02 | SHOULD | objectives ↔ hook/recap | "Làm chủ vòng đời Spring Bean, Dynamic Proxy và xử lý triệt để lỗi tự gọi hàm nội bộ" | Cách sửa (tách sang bean khác, hoặc lấy proxy qua ApplicationContext, theo `fix` của giáo án) chỉ xuất hiện trong một ô bảng ("Tách dịch vụ độc lập hoặc tiêm ủy quyền qua ngữ cảnh"). Không có lời đọc giải thích, không có mã trước/sau, nên mục tiêu "xử lý triệt để" không đạt. | Thêm 1 step mã: lời gọi `this.inner()` so với `otherBean.inner()`, kèm câu nói rõ vì sao lời gọi thứ hai đi qua proxy | CONFIRMED |
| MLO L11 | SHOULD | title ↔ sym step 1 | "Tối ưu mô hình để triển khai: lượng tử hoá, chưng cất" / hook "Hôm nay: lượng tử hoá và chưng cất … và cái giá phải trả" | Chưng cất chỉ có đúng một câu định nghĩa (box key ở sym). Không có ví dụ, không có số, không có "cái giá", và quiz không hỏi. Tiêu đề và câu mở bài hứa nhiều hơn những gì bài dạy. | Thêm một ví dụ số ngắn (ví dụ mô hình thầy 7 tỉ → trò 1 tỉ: bộ nhớ, độ chính xác phải đo lại), hoặc bỏ chữ "chưng cất" khỏi tiêu đề | CONFIRMED |
| PLC L00 | SHOULD | example step 1 + intuition SVG | "Riêng ký tự a còng không khớp mẫu từ tố nào của ngôn ngữ, nên lỗi bị bắt ngay ở pha từ vựng." | Màn hình không nói đây là ngôn ngữ đồ chơi (chỉ có trong chú thích YAML). Ở cảnh tự kiểm, bài lại dùng Python thật. Trong Python, `@` là một từ tố hợp lệ (phép nhân ma trận): `compile('x = 3 @ 4')` chạy qua, rồi khi chạy báo `TypeError`. Đã chạy thử. Người học thử lại bằng Python sẽ thấy khác với lời bài nói. | Ghi "trong một ngôn ngữ như C" hoặc đổi sang ký tự không hợp lệ ở mọi ngôn ngữ phổ biến (ví dụ `x = 3 $ 4` trong C/Python, hoặc dấu `` ` ``) | CONFIRMED |
| IRS L10 | — | | | không phát hiện lỗi | | |
| JVA L03 | — | | | không phát hiện lỗi | | |
| LLM L01 | — | | | không phát hiện lỗi | | |
| NET L04 | — | | | không phát hiện lỗi | | |
| OSY L13 | — | | | không phát hiện lỗi | | |
| PAR L01 | — | | | không phát hiện lỗi | | |

Tổng: **0 MUST, 7 SHOULD**.

## 2. Độ sâu cho người mất gốc

| Bài | Phút (từ chapters/srt) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HCI L10 | 8:33 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | ĐỦ | P1: "Theo định luật thời gian trỏ (bài 2)" chỉ được dẫn sang bài khác, không giảng tại chỗ. P3: khung `00023.png`: chữ SVG màu vàng, xanh nhạt và trắng (`#fde047`, `#86efac`, `#f8fafc`) trên nền kem; chữ "Chặn được lỗi!" gần như không đọc được (SVG thiết kế cho nền tối) |
| INT L02 | 7:06 | 0 | 1 | 0 | 1 | 1 | 2 | 1 | 6 | CHƯA | P1: có ≥ 8 từ chưa giảng: CGLIB/JDK proxy, PostConstruct, Singleton, "khả biến", Controller/DispatcherServlet/Spring MVC, CORS, AOP, failover, hàm băm. P2: công thức "×2 + số đĩa" không có lý do, ví dụ 5 000 yêu cầu chỉ là mã, không thử bằng số. P3: khung `00020.png`: SVG duy nhất có chữ cỡ ~11px, mũi tên `url(#arrow)` không được định nghĩa nên không hiện. P4: chỉ có phép tính $8 \cdot 2 + 1 = 17$. P5: hai câu trắc nghiệm kiểm nhớ chữ (phương án nhiễu ở câu Bloom quá hiển nhiên), cảnh tự kiểm không dừng. P7: xem SHOULD về lỗi tự gọi hàm |
| IRS L10 | 13:38 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — (Simpson, mô phỏng, cắt trọng số, Zhao 2019 có số; rất tốt) |
| JVA L03 | 8:24 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — |
| LLM L01 | 6:36 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: "từ tố" và "kho" dùng ngay từ hook nhưng không giảng lại (chỉ dựa vào bài 0) |
| MLO L11 | 7:19 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | P1: "hiệu chuẩn", "theo nhóm" (lỗi 1), "lô yêu cầu", "bộ đệm" (lỗi 3) chưa giảng. P7: chưng cất chỉ một câu |
| NET L04 | 9:55 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | P1: "địa chỉ IP", "bộ định tuyến" dùng ở lỗi 1 và lỗi 4 mà không giảng. P2: $Ge^{-2G}$ và $Ge^{-G}$ chỉ được nêu, không suy ra (phép tính thẳng $0{,}95^{18}$ bù lại được một phần) |
| OSY L13 | 9:05 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — (phần ổ thể rắn không có số, nhưng vẫn đủ cho mục tiêu) |
| PAR L01 | 10:07 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — |
| PLC L00 | 7:47 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: "biểu thức" (bước 2), "khai báo", "đối số" (quiz câu 3) chưa giảng |

Phân bố: **ĐỦ 9, GẦN 0, CHƯA 1 (INT L02)**.

## 3. Khung hình đã xem
- HCI L10: 00002 (mở đầu), 00023 (SVG phô mai, chữ khó đọc), 00036 (ví dụ bước 3), 00054 (đáp án quiz; tử số "1" của phân số bị khung highlight đè nhẹ), 00061 (tổng kết)
- INT L02: 00001, 00020 (SVG proxy, chữ nhỏ), 00037 (mã bước 2; tiêu đề "5,000"), 00053 (đáp án quiz), 00057 (tổng kết)
- IRS L10: 00007 (ôn nền), 00026 (cột xác suất nhìn thấy), 00048 (chấm ngoại tuyến 40/68), 00089 (đáp án quiz), 00096 (tổng kết)
- JVA L03: 00006 (hook), 00031 (sơ đồ ngã ba), 00054 (thử 500 000), 00086 (quiz, có nút dừng), 00097 (tổng kết)
- LLM L01: 00001, 00022 (cột độ hỗn loạn), 00028 (bảng làm trơn), 00052 (quiz), 00059 (tổng kết)
- MLO L11: 00002, 00021 (trục vạch 8/4 bit), 00046 (lỗi 4, quyết định bị lật), 00059 (đáp án quiz), 00062 (tổng kết)
- NET L04: 00002, 00024 (trục khe thời gian), 00040 (ALOHA 10 máy), 00081 (đáp án quiz), 00085 (tổng kết)
- OSY L13: 00002, 00018 (đường thẳng các trụ), 00026 (FCFS 640), 00070 (đáp án quiz), 00074 (tổng kết)
- PAR L01: 00002, 00020 (hai bức hình mạnh/yếu), 00038 (tính lại số năm 1988), 00072 (quiz câu 3), 00078 (tổng kết)
- PLC L00: 00001, 00025 (dây chuyền các pha), 00029 (lỗi từ vựng `@`), 00064 (đáp án quiz), 00068 (tổng kết)

Ngoài HCI 00023 và INT 00020, các khung không có chữ tràn, đè hay bị cắt, và hình khớp lời đọc.

## 4. Mã đã chạy / số đã tính lại
- **Java (JDK 22)**: gộp mọi đoạn mã của JVA L03 vào một tệp (rút tiền, switch mũi tên, toán tử ba ngôi, Phi với 499 999/500 000/10 000 000, ba điều kiện độc lập, thiếu ngoặc nhọn, sai dấu biên, quiz Bac/Uu tien): **14/14 dòng in ra khớp màn hình**. Riêng `if (soLan = 5)` cho đúng lỗi biên dịch `incompatible types: int cannot be converted to boolean`.
- **Python**: PLC L00, 5 dòng chạy qua `compile`/`exec`: `x = = 3` → SyntaxError, `y = z + 1` → NameError, `a/b` → ZeroDivisionError, hàm `xu_ly` cho 10/0/NameError, đều khớp. Ngoài ra `x = 3 @ 4` → TypeError, tức Python không coi `@` là lỗi từ vựng (đã báo SHOULD). IRS: numpy `default_rng(0)` cho 0,01039 và 0,05195, khớp "≈ 0,0104" và "≈ 0,052".
- **Số đã tính lại**: khoảng 150 con số trên màn hình và trong lời đọc. HCI 13, INT 3, IRS 25, LLM 12 (gồm 4/9, 1/504, 1/64, 1,225, 4,738, 2,828, 1,732), MLO 25 (bước 2/127, q = 83/−44/5, sai số, tỉ lệ 18, 4 ca bị lật, vị trí các vạch trong SVG), NET 18 (18,4/36,8/30,3%, 19,9/31,5%, 0,3659/0,3679/0,3662), OSY 14 (640, 236, LOOK 208 cũng là tối ưu theo vét cạn, 146, 60, 58), PAR 25 (111/201, 5,07–9,16 lần, 14,5, 0,69%, 921,7, 1015,8/1019,9, 60,85, 15,42, 8,71), PLC 3, phần còn lại là số trong các bài Java. **Tất cả khớp tới số chữ số được ghi.**

## 5. Nhận xét chung
- Điểm mạnh: 9/10 bài theo đúng khung hook → ôn nền → ký hiệu → hình cơ chế → ví dụ từng bước → tự kiểm bằng đường khác → lỗi của người đã đi làm → quiz có dừng và lời giải từng bước. Số liệu sạch: không có số tính sai nào.
- IRS, PAR, OSY, JVA là mẫu tốt. Các bài này đặt số minh hoạ cạnh nguồn thật (Joachims 2017, Zhao 2019, Gustafson 1988) và ghi rõ chỗ nào là phép tính lại của bài.
- Điểm yếu lặp lại 1, P1: vài thuật ngữ phụ chỉ xuất hiện trong phần "lỗi hay gặp" hoặc quiz mà không giảng (IP/bộ định tuyến, hiệu chuẩn, biểu thức/đối số, định luật thời gian trỏ, từ tố). Có ở 6/10 bài.
- Điểm yếu lặp lại 2: tiêu đề hoặc mục tiêu hứa nhiều hơn phần thân (MLO "chưng cất", INT "xử lý triệt để" lỗi tự gọi hàm).
- Điểm yếu lặp lại 3, hiển thị SVG: một số SVG viết cho nền tối hoặc dùng chữ quá nhỏ (HCI 00023, INT 00020), nên khó đọc trên nền kem của mẫu.
- INT L02 (khoá phỏng vấn) lệch hẳn so với chuẩn mất gốc: dày thuật ngữ Spring, ít số, không có ví dụ làm tay, có câu hứa lương không nguồn. Nếu khoá này cũng nhắm tới người mất gốc thì cần viết lại theo khung chuẩn.
- Công thức đôi khi được nêu mà không suy ra (NET $Ge^{-2G}$, HikariCP "×2 + đĩa"), dù phần còn lại của bài suy ra rất kỹ.
