# Mẫu H — phần 4: đã đọc 10/10 bài

Quy ước: "Mất gốc" = ĐỦ (tổng P1–P7 ≥ 12, không mục 0) / GẦN (9–11, không mục 0) / CHƯA (≤ 8 hoặc có mục 0). Số khung trong ngoặc là tên tệp `out/<KHOÁ>/<Lxx>/frames/*.png` đã mở. sha16 cả 10 tệp khớp danh sách giao.

## A. Chuẩn xác

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh đã chạy) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| LNX L06 | MUST | covers | `objective: 1 → scene: formula` | Cảnh formula chỉ có "60 / 5 = 12 lần mỗi giờ; 12 × 24 = 288 lần mỗi ngày"; không một chữ về khoá SSH. | Trỏ về cảnh dạy khoá (hiện chỉ có 1 dòng ở `sym`) hoặc viết cảnh riêng. | CONFIRMED |
| LNX L06 | MUST | covers | `objective: 3 → scene: check` | Cảnh check chỉ chạy `per_h=$((60 / 5)); per_d=$((per_h * 24))`; đọc 5 trường nằm ở sym/formula; chuyển hướng log không có cảnh nào dạy. | Trỏ về formula và thêm ví dụ dòng cron đầy đủ. | CONFIRMED |
| LNX L06 | MUST | objectives[0], title | "Phân biệt vai trò khoá công khai và khoá bí mật; đặt quyền 600 cho khoá riêng" | Cả bài chỉ có 1 ô bảng và 1 câu ("Cặp khoá đăng nhập luôn giữ phần bí mật tuyệt đối ở máy nguồn với quyền sáu trăm, còn phần công khai mới gửi sang máy chủ đích"). grep tệp: `ssh-keygen` 1 lần (ô bảng, không đọc, không chạy); `authorized_keys`/`ssh-copy-id` 0 lần; lệnh `ssh` 0 lần. | Thêm cảnh sinh khoá, chép khoá công khai, lý do quyền 600. | CONFIRMED |
| LNX L06 | MUST | objectives[2] | "…và đặt chuyển hướng log cho tác vụ nền" | `crontab` 0 lần trong tệp; không có dòng lịch hoàn chỉnh nào kèm chuyển hướng, chỉ có mảnh `>> log 2>&1` trong pitfalls. | Thêm ví dụ `*/5 * * * * /duong/dan/tuyet/doi.sh >> /tmp/x.log 2>&1` và cách cài lịch. | CONFIRMED |
| LNX L06 | SHOULD | example step 1 | "Giải mã hai bước thiết lập an toàn khi tạo khoá bí mật và đọc tệp môi trường không để lọt ra nhật ký." | Màn hình có 4 dòng (chmod, ssh-keygen, umask, cron), lời 1 câu không giảng dòng nào. Step 2 dùng `umask 077`, `set -a; source`, `${DB_PASS: -4}`, `${#DB_PASS}`, `$(( … ? 1 : 0 ))` mà không giảng; grep L01–L05 không có `set -a`, `umask`, `${#`. | Giảng từng dòng. | CONFIRMED |
| LNX L06 | SHOULD | quymo | title "Dung lượng nhật ký và mức phơi nhiễm bí mật qua ba quy mô vận hành" | Bảng chỉ có số lần chạy (720 / 8 640 / 43 200, tính lại đúng); không có dung lượng nhật ký hay mức phơi nhiễm. "cơ chế khoá chống chồng chéo và xoay vòng tệp nhật ký", "hộp thư hệ thống" chưa giảng. | Sửa tiêu đề hoặc thêm số; giảng thuật ngữ. | CONFIRMED |
| LNX L06 | SHOULD | pitfalls | màn hình "Lỗi 2: Đặt lệnh echo "Connecting $DB_PASS"…"; lời "…hoặc đưa nhầm tệp môi trường vào kho mã nguồn" | Lời thêm ý không có trên màn hình. | Đồng bộ. | CONFIRMED |
| LNX L06 | SHOULD | intuition (khung 00011) | SVG `width="960"`, chữ phụ `font-size="15"` | Sơ đồ chỉ chiếm nửa trái khung 1920×1080, chữ phụ rất nhỏ. Cùng lỗi ở MLP L04 khung 00012. | Vẽ viewBox 1500 như BNX/JVA. | CONFIRMED |
| MLP L04 | MUST | quymo | "1 000 tổ hợp siêu tham số / 20 000 lần khớp quá chậm" | 1 000 × 5 nếp = 5 000 (+1 refit), không phải 20 000. | Sửa thành 5 000. | CONFIRMED |
| MLP L04 | MUST | covers (cả 3) | `1 → example`, `2 → check`, `3 → quymo` | Hai dòng đầu đảo chéo: example là cảnh GridSearchCV (mục tiêu 2), check là cảnh đếm nhãn dương theo nếp (mục tiêu 1). quymo là bảng số lần khớp, không dạy trung bình/độ lệch chuẩn. | 1 → check, 2 → example, 3 → cảnh mới. | CONFIRMED |
| MLP L04 | MUST | objectives[2] | "Đọc điểm trung bình và độ lệch chuẩn để không chọn cấu hình ăn may một lần chia" | Cả bài chỉ 1 câu "luôn nhìn cả điểm trung bình lẫn độ lệch chuẩn qua các nếp"; không in `cv_results_`, không có số độ lệch chuẩn nào. Chạy lại (labs/.venv-ml, sklearn 1.9.1): mean = [0.921 0.921 0.917 0.917], std = [0.018 0.018 0.016 0.016], tức chênh giữa các C (0,004) nhỏ hơn std. Lời lại nói "Đầu ra xác nhận hệ thống chọn đúng siêu tham số tối ưu". | In mean ± std từng C và giảng cách đọc. | CONFIRMED |
| MLP L04 | SHOULD | example | "Ta chạy thực nghiệm này vì cần đo trực tiếp hành vi trên dữ liệu thật." | Dữ liệu là `make_classification` (tổng hợp); câu khuôn mẫu thành khẳng định sai. | Bỏ câu. | CONFIRMED |
| MLP L04 | SHOULD | hook và quymo | "chạy toàn bộ trên CPU chỉ vài trăm mi-li-giây" và "20 lần khớp (< 100 ms)" | Tự mâu thuẫn, không nguồn. Đo lại `gs.fit` trên máy này: 204 ms và 185 ms. | Ghi một số đo có nguồn. | CONFIRMED |
| MLP L04 | SHOULD | hook, prereq, example (say) | "…thì khi chia năm nếp. Thông số trung bình của nếp kiểm chứng đã ngầm lọt…"; "…bọc bên ngoài chuỗi xử lý. Giúp chọn siêu tham số…"; "…tự chọn giá trị C tốt nhất. Huấn luyện lại một mô hình sạch…" | Câu bị chặt bằng dấu chấm giữa chừng, giọng đọc ngắt sai nghĩa. | Nối lại câu. | CONFIRMED |
| MLP L04 | SHOULD | prereq, sym, quymo, pitfalls | "nếp", "kiểm chứng chéo", "refit", "mức phạt C", "RandomizedSearchCV", "Lỗi 1 (-30đ)" | grep MLP L00–L03 không có "nếp"/"kiểm chứng chéo". Bài không giảng cơ chế xoay nếp (chỉ 1 câu "khớp lại trên bốn nếp trước khi đo trên nếp thứ năm"). C là nghịch đảo độ phạt nên "mức phạt C" dễ hiểu ngược. "(-30đ)" không ứng với thang nào (cham.sh chỉ in ĐÚNG/KHÁC). | Giảng tại chỗ; bỏ điểm trừ. | CONFIRMED (grep); "hiểu ngược" là PLAUSIBLE |
| MLP L04 | SHOULD | hook title | "Kiểm chứng chéo StratifiedKFold & tìm siêu tham số GridSea" | Tiêu đề cắt cụt giữa từ, hiện nguyên ở chapters.txt 00:00. | Viết đủ. | CONFIRMED |
| MLP L04 | SHOULD | intuition | "Luồng thực thi chuẩn mực gồm ba tầng bảo vệ…" | Lời chỉ kể tầng một, tầng hai; ô thứ ba ("Chọn best_params_ / Chấm 1 lần trên Test") không được đọc. | Bổ sung. | CONFIRMED |
| MLP L04 | SHOULD | curriculum/mlp.yaml L04 | example: "C trong [0.1, 1.0, 10.0]" | Bài dùng `[0.01, 0.1, 1.0, 10.0]`, kết quả `best_C=0.01` nằm ngoài lưới của giáo án và ở mép lưới (không nhắc mở rộng lưới). | Đồng bộ. | CONFIRMED |
| PRJ L05 | MUST | objectives[2], title | "So sánh thời gian chờ và độ trễ khung khi số luồng xử lý tăng gấp 4 lần"; "…& lập lịch đa nhân" | quymo chỉ có bảng khung/s → % tải 1 nhân; không có phép so sánh chờ/độ trễ khi luồng ×4. "đa nhân" xuất hiện 3 lần, đều ở tiêu đề/lời dẫn; Round Robin trong bài là 1 CPU. covers `3 → quymo` vì thế cũng sai. | Dạy thật hoặc bỏ mục tiêu và chữ "đa nhân". | CONFIRMED |
| PRJ L05 | MUST | covers | `objective: 2 → scene: check` | check tính FCFS (`fcfs_avg=17.00 saved=11.33`); Round Robin q = 4 nằm ở example. | 2 → example. | CONFIRMED |
| PRJ L05 | MUST | pitfalls Lỗi 2 (say) | "quên đẩy lại tác vụ chưa xong vào cuối hàng đợi khiến thuật toán thoái hoá thành chạy tuần tự" | Chạy mã của bài, bỏ `q.append(i)`: fin = [0, 7, 10], rem = [20, 0, 0]. Tác vụ 24 bị bỏ dở vĩnh viễn, không phải "chạy tuần tự". | Sửa: "tác vụ dài không bao giờ xong". | CONFIRMED |
| PRJ L05 | SHOULD | example (mã) và sym | `rem, t, fin, q = [24, 3, 3], 0, [0]*3, deque([0,1,2])`; sym: "q = 4 / Lượng tử thời gian" | Cùng tên `q` cho hai thứ (lượng tử ở bảng, hàng đợi ở mã); lượng tử bị viết cứng `min(4, rem[i])`. | Đặt `hang`, `Q = 4`. | CONFIRMED |
| PRJ L05 | SHOULD | quymo | "1 000 khung/s / 0,5% tải 1 nhân / Độ trễ ổn định < 1 ms"; "100 000 khung/s / 50% tải 1 nhân" | Số hiệu năng không nguồn, không ghi "số minh hoạ" (ngầm 5 µs/khung). | Ghi nguồn hoặc nhãn minh hoạ. | CONFIRMED |
| PRJ L05 | SHOULD | formula | "tổng chờ (6 + 4 + 7) / 3 = 5,67" | Đó là trung bình, không phải tổng (tổng = 17). | Sửa nhãn. | CONFIRMED |
| PRJ L05 | SHOULD | pitfalls, curriculum, de.md | "Lỗi 1 (-30đ)"; giáo án: "kiểm thử tự động 100 điểm qua labs/cham.sh" | cham.sh chỉ in ĐÚNG/KHÁC. labs/PRJ/SPEC.md đòi de.md có "đầu vào mẫu, ràng buộc hiệu năng/bộ nhớ, thang chấm" và "ba cỡ dữ liệu"; de.md L05 dài 3 dòng đáp án, không có gì trong số đó. | Hoặc làm đúng SPEC, hoặc bỏ thang điểm. | CONFIRMED |
| PRJ L05 | SHOULD | sym, example | `struct.unpack('<HH', b)` | `struct.unpack`/`struct.pack` chỉ xuất hiện ở đúng tệp này trong toàn bộ lessons/*/*.yaml. Bài không cho thấy 4 byte trông ra sao (`struct.pack('<HH',101,64)` = `b'e\x00@\x00'`), "little-endian" chỉ dịch "nhỏ trước". | Thêm bảng 4 byte. | CONFIRMED |
| PRJ L05 | SHOULD | prereq | "Kiểm tra kích thước header + payload chuẩn Ethernet/TCP" | Khung trong bài là khung tự đặt (2 trường 16 bit), không phải Ethernet/TCP. | Bỏ chữ "chuẩn Ethernet/TCP". | CONFIRMED |
| BNX L26 | SHOULD | formula Bước 5, intuition 2 | `stage('Build') { steps { sh 'mvn -B package' } }` … `stage('Test') { steps { sh 'mvn -B verify' } }`; hình "Test / mvn verify" hỏng | Chính bài cho thấy `package` đã chạy `surefire:3.2.5:test`, nên kiểm thử đơn vị hỏng sẽ làm hỏng Build chứ không phải Test; bài không giải thích. | Build = `-DskipTests package`, hoặc nói rõ Test là kiểm thử tích hợp. | CONFIRMED (suy từ đầu ra trong bài) |
| BNX L26 | SHOULD | sym step 3 | "phiên bản dạng khoảng, `latest`" | Chữ thường `latest` không phải cú pháp của Maven (`LATEST`/`RELEASE`) hay Gradle (`latest.release`, `1.+`). CHƯA KIỂM bằng tài liệu ngoài. | Ghi đúng từng công cụ. | PLAUSIBLE |
| BNX L26 | SHOULD | hook, practice | "bản 3.9" và "bản 3.12.0"; "Gradle: cao nhất" | Bài không giảng so phiên bản theo từng thành phần (9 < 12). Chạy `'3.9' > '3.12.0'` trong Python ra True, nên so chuỗi cho kết quả ngược. Lời giải lab phải dùng `tuple(int(p) for p in v.split("."))`, `sorted`, `.items()`, không có trong các bảng "viết trong mã". | Thêm 1 dòng giảng + gợi ý. | CONFIRMED |
| JVA L04 | MUST (nhẹ) | covers | `objective: 1 → scene: practice` | Mục tiêu 1 là "Viết vòng lặp trong khi, vòng lặp đếm, vòng lặp làm rồi mới kiểm, và chọn đúng loại"; practice chỉ luyện `for`. Ba kiểu vòng lặp được dạy ở `sym`. | 1 → sym. | CONFIRMED |
| JVA L04 | SHOULD | prereq | "Ta ôn lại bốn điều." | Bảng có 5 dòng (⑤ `import`, `new`) và lời đọc đủ 5. | "năm điều". | CONFIRMED |
| ACB L03 | SHOULD | hook, symbol | "Nền tảng Confluent ksqlDB và Kafka Streams" | Bài không nêu phiên bản và không nhắc tình trạng hiện nay của ksqlDB (theo trí nhớ: Confluent khuyến nghị Flink SQL cho việc mới). CHƯA KIỂM bằng nguồn ngoài. Cú pháp trong bài (CSAS, `LEFT JOIN` luồng–bảng, `EMIT CHANGES`, `WITHIN` cho luồng–luồng, `SET … EX 86400 NX`) đọc lại không thấy sai. | Thêm 1 câu về phiên bản/tình trạng. | PLAUSIBLE |
| ACB L03 | SHOULD | hook | "hệ thống sẽ sập do nghẽn mạng"; "hệ thống sẽ nghẽn tắc ngay lập tức" | Khẳng định tuyệt đối, thiếu điều kiện. | "dễ nghẽn". | CONFIRMED |
| ACB L03 | SHOULD | quiz title, độ dài | "Thử thách kiến trúc luồng dữ liệu tại ACB" | Bài tự ghi mọi số là minh hoạ, "không phải số liệu của OCB hay ACB"; tiêu đề gợi là kiến trúc thật. Video 16,35 phút, vượt chuẩn 16 (có 240 s dừng tự làm). | Bỏ "tại ACB". | CONFIRMED |
| AIF L10 | MUST (số) | check step 1 và recap step 2 | "kho vận 100 kiện hàng ($\approx 10^{150}$ trạng thái)" | Theo chính mô hình thế giới khối của bài: 3 khối = 13 trạng thái (đúng), 100 khối = 2,42 × 10^164; riêng 100! đã là 9,33 × 10^157. Mô hình "kho vận" không được định nghĩa nên xếp PLAUSIBLE. | Sửa số hoặc nêu mô hình và nguồn. | PLAUSIBLE |
| AIF L10 | MUST | recap step 1 (say) | "Cài đặt bộ giải cho bài toán đảo chồng ba khối ngay sau đây minh hoạ rõ…"; "Khi không gian đạt hàng triệu cấu hình, ta rút ra hàm đánh giá bằng cách tạm bỏ hiệu ứng xoá. Cách này dẫn đường tìm kiếm về đích nhanh mà vẫn an toàn."; "Chính cấu trúc sạch sẽ này bảo đảm chương trình luôn tìm thấy chuỗi thao tác ít bước nhất…" | Lời độn dài 118,3 s (khung 00069–00086, 20% video) trên màn hình tĩnh 4 ô. "ngay sau đây" sai thứ tự (practice đã qua). Đưa khái niệm mới không giảng (bỏ hiệu ứng xoá). Gán tính tối ưu cho cách mã hoá thay vì cho tìm theo chiều rộng. Recap AIF L09 cùng kiểu độn. | Cắt về 3–4 câu. | CONFIRMED |
| AIF L10 | MUST | practice step 3–6 | "Bảng này giải thích từng ký hiệu dùng trong lời giải tham khảo (phần 1) để bạn tự đối chiếu cách viết." (×4) | Lời khuôn mẫu, không giảng dòng nào; mỗi bảng hiện 7,0 s, lời giải 15 dòng hiện 7,1 s. Bảng có dòng sai/không liên quan: "`not in` / Giá trị logic (True/False/None), phép logic (and/or/not)…"; "`M[i][j]` / Truy cập ô hàng i cột j" (mã chỉ có `q[0][0]`); `deque(..., maxlen=k)` (mã không dùng maxlen). | Viết bảng theo đúng mã, giảng thật. | CONFIRMED |
| AIF L10 | MUST | objectives[1], covers `2 → example` | "Tìm theo chiều rộng trong không gian trạng thái với các hành động này cho đúng kế hoạch 3 bước — ngắn nhất." | Cảnh example chỉ kiểm lại một kế hoạch cho sẵn (3 bước) rồi khẳng định; không có bước mở trạng thái, hàng đợi hay nhánh nào. Mục tiêu "Tìm kế hoạch bằng tìm kiếm trong không gian trạng thái" không được làm mẫu, trong khi lab đòi viết đúng thứ đó. | Thêm 1 lượt mở trạng thái (13 trạng thái là vẽ được). | CONFIRMED |
| AIF L10 | SHOULD | hook (say), check | "Ta cần đồ thị trạng thái chuẩn xác cho toàn tổ hợp mục tiêu để tránh bẫy tương tác này."; "lập kế hoạch phân cấp" | Thuật ngữ chưa giảng, không có trên màn hình hook. | Bỏ hoặc giảng. | CONFIRMED |
| AIF L10 | SHOULD | recap (say) | "Tìm kiếm theo chiều rộng hoặc có chỉ dẫn trên không gian trạng thái giúp tìm ra kế hoạch ngắn nhất tới mục tiêu." | Tìm có chỉ dẫn chỉ cho ngắn nhất khi hàm đánh giá chấp nhận được (chính AIF L02 dạy vậy). | Thêm điều kiện. | CONFIRMED |
| DBS L01 | MUST | covers | `objective: 3 → scene: practice` | "Biết nối = tích rồi chọn" được dạy ở `join` và `intuition`; practice là cảnh "Mở labs/DBS/L01/de.md". | 3 → join. | CONFIRMED |
| DBS L01 | MUST | practice, labs/DBS/L01 | "cài đặt bằng SQL (SQLite)"; de.md: "Viết tập lệnh SQLite tạo SV(4 dòng, gồm 1 bạn NULL lớp) và Lop(2 dòng), đo số dòng của CROSS JOIN…" | SQL là bài sau ("Bài sau (bài 2): SQL"). Đếm trong show+say của L00 và L01: `COUNT` 0 lần, phép nối chuỗi hai gạch đứng 0 lần, `CROSS JOIN`/`INNER JOIN` chỉ 1 lần (chính bảng practice), `CREATE TABLE` 1 lần ở L00. Lời giải cần cả `COUNT(*)` lẫn nối chuỗi. de.md không cho dữ liệu các dòng. | Dời lab sau L02, hoặc dạy đủ cú pháp và cho sẵn dữ liệu. | CONFIRMED |
| DBS L01 | SHOULD | check (say) | "…vẫn ra đúng An, nên thứ tự phép không làm đổi kết quả." | Khái quát tuyệt đối từ 1 ví dụ; chỉ đúng khi đẩy phép chọn xuống trước phép nối (chiếu bỏ cột `diem` trước rồi mới chọn theo `diem` thì không được). | Thêm điều kiện. | CONFIRMED |
| DBS L01 | SHOULD | practice | "Tích Đề-các CROSS JOIN nhân số dòng (4*2=8); INNER JOIN chỉ giữ cặp khớp khoá" | Ba thuật ngữ này lần đầu xuất hiện ở bảng practice, thân bài chỉ dùng "tích", "nối". | Giảng trong thân bài. | CONFIRMED |
| OSY L02 | MUST | covers | `objective: 3 → scene: practice` | "Giải thích vì sao việc ngắn nhất trước cho chờ trung bình nhỏ nhất" được dạy ở cảnh `why`; practice là cảnh "Mở labs/OSY/L02/de.md". | 3 → why. | CONFIRMED |
| OSY L02 | SHOULD | toàn bài | không có cảnh quy mô | Chỉ có 3 và 4 tiến trình; không có hai mức số liệu (P9). Video 8,54 phút, dưới chuẩn 9. | Thêm bảng quy mô. | CONFIRMED |
| OSY L02 | SHOULD | practice | "cài đặt bằng Python"; "sjf_waits=6,0,3" | Bài không có dòng mã nào; OSY L00–L02 không dạy Python (L01 dùng C). Thứ tự 6,0,3 là theo chỉ số tiến trình, thân bài viết theo thứ tự chạy "0, 3 và 6"; không giải thích. | Giải thích khuôn; thêm mã mẫu. | CONFIRMED |
| OSY L02 | SHOULD | quiz (khung 00064) | khung tô sáng công thức | Viền khung tô sáng chạm sát tử số $0+6+14+21$ và mép dưới bảng. | Thêm khoảng cách. | CONFIRMED |
| TOC L10 | MUST | covers | `objective: 1 → scene: evidence` | Phát biểu luận đề và lý do "không phải định lý" nằm ở `sym`; `evidence` chỉ nói vì sao người ta tin. | 1 → sym. | CONFIRMED |
| TOC L10 | MUST | practice step 3–4 | "Bảng này giải thích từng ký hiệu dùng trong lời giải tham khảo (phần 1) để bạn tự đối chiếu cách viết." (×2) | Cùng khuôn với AIF L10: mỗi bảng 7,0 s, lời giải 7,1 s. Dòng sai: "`A if đk else B` / Giá trị logic (True/False/None), phép logic (and/or/not)…"; "`len(ds), .join()` / …sắp xếp, cực trị, ghép đôi, đánh chỉ số, làm tròn…". | Viết theo đúng mã. | CONFIRMED |
| TOC L10 | MUST | pitfalls step 5 | "Máy tính một băng đơn / … / mô phỏng truy cập ngẫu nhiên chậm bậc $O(t^2)$"; lời: "Theo luận đề vạn năng năm 1936…" | (a) O(t²) là chặn của mô phỏng máy nhiều băng bằng một băng (Sipser 7.8), không phải của truy cập ngẫu nhiên (thêm một bậc đa thức nữa); nêu theo trí nhớ, CHƯA đối chiếu sách. (b) Không có "luận đề vạn năng"; bài dạy "luận đề Church–Turing" và "máy vạn năng". (c) Ký hiệu O(·), "khả quyết/bất khả quyết" chưa giảng (bài 11 mới tới). | Viết lại bảng hoặc bỏ. | (a) PLAUSIBLE; (b), (c) CONFIRMED |
| TOC L10 | SHOULD | recap step 2 | màn hình "chỉ chậm hơn hằng số đa thức — chứng tỏ một máy chung giải được mọi bài toán tính được"; lời "chỉ chậm thêm một hệ số đa thức" | "hằng số đa thức" tự mâu thuẫn và khác lời đọc; không nguồn; vế "chứng tỏ…" không suy ra được từ tốc độ. | Viết lại. | CONFIRMED |
| TOC L10 | SHOULD | verify step 3 | "Bộ mô phỏng là một chương trình, nên theo luận đề có một máy Turing làm đúng việc của nó — đó là $U$." | Sự tồn tại của U là định lý có cấu trúc dựng (Turing 1936, mục 6–7, chính nguồn bài ghi), không cần dựa vào luận đề không chứng minh được. | Sửa lập luận. | PLAUSIBLE |

## B+C+D. Điểm (1 dòng/bài)

| Bài | sha16 khớp | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Mất gốc | P9 | L1 | L2 | L3 | L4 | L5 | covers đúng (k/n) | Chỗ người mất gốc kẹt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LNX L06 | có | 5,59 (990 từ) | 1 | 1 | 1 | 1 | 1 | 2 | 1 | CHƯA (8) | 1 | 1 | 1 | 0 | 1 | 0 | 1/3 | Không biết SSH là gì, khoá dùng thế nào; 8 dòng Bash có 5 cú pháp lạ, giảng trong 2 câu. Quiz hỏi lại đúng 288 của ví dụ. Lab: de.md chép đủ 3 dòng đáp án, số trùng ví dụ (12, 288); đã chạy thử tệp 3 dòng `echo` thì khớp mong_doi. Lab không đụng SSH hay chuyển hướng log. |
| MLP L04 | có | 5,90 (1 017 từ) | 1 | 1 | 1 | 1 | 1 | 2 | 1 | CHƯA (8) | 1 | 1 | 2 | 1 | 2 | 1 | 0/3 | "nếp", "kiểm chứng chéo" không được dựng bằng ví dụ số; 13 dòng mã giảng trong 4 câu. Quiz là 2 câu nhớ lại (21 lần, `clf__C`). Lab: de.md không chép đáp án nhưng dữ liệu, lưới, hạt giống trùng ví dụ nên 2/3 dòng (`best_c=0.01`, `cv_f1=0.921`) đã hiện ở ví dụ; chỉ dòng `equal_folds_positive=0` là mới và de.md có giải thích. |
| PRJ L05 | có | 5,86 (1 025 từ) | 1 | 1 | 1 | 1 | 1 | 2 | 1 | CHƯA (8) | 1 | 1 | 2 | 0 | 1 | 0 | 1/3 | `struct`, little-endian, `deque` mỗi thứ 1 dòng bảng; vòng `while` dồn 4 lệnh một dòng, không có bảng dò từng lượt Round Robin. "Dự án" là 13 dòng chép từ ví dụ, đổi (101, 64) thành (7, 32); de.md chép đủ 3 dòng đáp án; `[24, 3, 3]` và 5.67 trùng ví dụ và quiz. |
| BNX L26 | có | 15,29 (2 294 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 2 | 2 | 2 | 2 | 2 | 2 | 7/7 | Luật "cao nhất" của Gradle không có mã mẫu (chỉ gợi ý); so phiên bản 3.9 với 3.12.0. Lab: đề đủ trên màn hình, đồ thị mới, có gợi ý và trỏ lời giải; de.md không chép đáp án. |
| JVA L04 | có | 13,69 (2 061 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 2 | 2 | 2 | 2 | 2 | 2 | 5/6 | Không thấy chỗ kẹt đáng kể. Lab: số mới (50 triệu, 0,6%, 6 tháng), thêm yêu cầu "tháng đầu tiên vượt", có gợi ý; chỉ luyện `for`. |
| ACB L03 | có | 16,35 (2 288 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 2 | 2 | 2 | 2 | 2 | 2 | 8/8 | Nhiều tên tiếng Anh dồn ở hook/concept (đều có chú giải). Xô thẻ chỉ dạy bằng bảng, lab đòi tự viết vòng trạng thái (có gợi ý). Lab: số mới, 4 phần, de.md không chép đáp án. |
| AIF L10 | có | 9,69 (1 685 từ, trong đó ~118 s recap độn) | 1 | 2 | 1 | 1 | 2 | 2 | 1 | GẦN (10) | 1 | 2 | 1 | 2 | 2 | 1 | 2/3 | Bài không làm mẫu việc mở trạng thái/hàng đợi nhưng lab đòi viết tìm theo chiều rộng bằng Python. Python trong khoá AIF chỉ xuất hiện ở lời giải tham khảo cuối mỗi bài; lời giải 15 dòng hiện 7 s kèm bảng chú giải sai. Lab tốt về số liệu: cấu hình mới M/P/N, cần 4 bước (một khối phải dời 2 lần). |
| DBS L01 | có | 9,19 (1 434 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 2 | 1 | 0 | 0 | 2 | 0 | 2/3 | Thân bài theo được. Kẹt ở lab: phải viết SQL có `CREATE TABLE`, `INSERT` nhiều dòng, `COUNT(*)`, nối chuỗi, `CROSS JOIN` trước khi tới bài SQL (L02). de.md chép đủ 3 dòng đáp án (8, 3, An, trùng ví dụ), không cho dữ liệu bảng, không gợi ý. |
| OSY L02 | có | 8,54 (1 391 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 1 | 1 | 1 | 0 | 2 | 0 | 2/3 | Thân bài theo được. Lab bằng Python trong khoá chưa dạy dòng Python nào (dựa CS112 qua requires_ext); de.md chép đủ 3 dòng đáp án; `[24, 3, 3]` → 17 và 3 trùng ví dụ; không gợi ý. |
| TOC L10 | có | 10,39 (1 778 từ) | 1 | 2 | 1 | 2 | 2 | 2 | 2 | ĐỦ (12) | 1 | 1 | 2 | 1 | 2 | 1 | 2/3 | Bước chèn "quy mô" cuối pitfalls dùng O(t²), "khả quyết", "luận đề vạn năng" chưa giảng. Lab: video không nói máy nào/đầu vào nào (chỉ khuôn đầu ra); de.md không chép đáp án nhưng cùng máy đảo bit với ví dụ (`1011` thành `10110`), đáp án suy ngay từ quy tắc "độ dài + 1" trong bài. |

Ghi chú chấm L1–L5:
- **L3 = 0** khi de.md chép nguyên mọi dòng đáp án và số trùng ví dụ; **L3 = 1** khi một trong hai điều đó xảy ra.
- **L2 của DBS = 0** vì ngôn ngữ lab được dạy ở bài sau.
- **mong_doi.txt** của cả 10 lab đều khớp khi chạy lại lời giải trong thư mục tạm.
- **Hệ quả của cham.sh** (đã đọc, không chạy): nó chỉ so stdout với mong_doi.txt, nên lab nào de.md hoặc video hiện đủ các dòng thì chương trình chỉ in lại cũng được "ĐÚNG".

**D. Câu khuôn mẫu dán chung (nguyên văn)**
- **PRJ L05, DBS L01, OSY L02** (giống hệt nhau từng chữ):
  - "Bây giờ đến phần bạn tự thực hành và chấm điểm trực tiếp trên máy. Bạn mở đề bài, tự viết lời giải vào tệp riêng rồi chạy lệnh chấm để đối chiếu từng dòng kết quả. Hãy bấm tạm dừng và tự làm trước."
  - "Màn hình hiển thị toàn bộ các dòng kết quả mong đợi mà chương trình của bạn phải in ra khớp từng ký tự."
- **LNX L06**:
  - "Bây giờ đến phần bạn tự viết kịch bản dòng lệnh và chấm thật trên máy. Bạn mở đề thực hành, viết lời giải vào tệp riêng rồi chạy lệnh kiểm định đối chiếu từng dòng. Hãy bấm tạm dừng và tự làm trước."
  - "Màn hình hiện toàn bộ các dòng kết quả mong đợi mà kịch bản của bạn phải in ra khớp từng ký tự."
  - "Bài tiếp theo là bài 7, tìm hiểu chủ đề tiếp nối ngay phần vừa học. Hẹn gặp bạn ở bài sau." (grep: cùng khuôn ở 9/10 bài LNX, L00–L08.)
- **MLP L04**:
  - "Vì vậy công thức định lượng giúp kiểm soát sai số và biến đổi mô hình minh bạch hơn."
  - "Ta chạy thực nghiệm này vì cần đo trực tiếp hành vi trên dữ liệu thật."
  - "Phép kiểm chứng này rất quan trọng vì đối chiếu độc lập giúp phát hiện ngay sai lệch."
  - "Bây giờ đến phần bạn tự thực hành và chấm điểm trực tiếp trên máy bằng môi trường CPU chuẩn của kho. Bạn mở tệp đề bài, tự viết lời giải hoàn chỉnh vào tệp Python riêng rồi chạy lệnh chấm tự động để đối chiếu từng dòng kết quả với đáp án chuẩn. Hãy bấm tạm dừng video và tự tay cài đặt trước khi xem lời giải."
  - "Chuỗi tổng kết kết nối ba quy tắc bất biến bạn vừa tự tay thực chứng trên CPU qua ví dụ, kiểm chứng độc lập và bài tập thực hành. Hãy giữ chắc ba nguyên tắc này khi triển khai bất kỳ đường ống học máy nào ngoài thực tế."
  - "Chúc mừng bạn đã hoàn tất trọn vẹn bài học máy thực hành trên CPU với đầy đủ bằng chứng số liệu và kiểm thử tự động."
  - Hai câu recap trên trùng nguyên văn recap MLP L03; recap không nhắc lại nội dung nào của bài.
- **PRJ L05** (thêm):
  - "Số liệu khớp chặt với công thức lý thuyết nhờ chia đúng lát thời gian."
  - "Chuỗi tổng kết nối ba mảnh ghép vừa cài đặt thành năng lực thực thi hoàn chỉnh cho dự án chặng này."
  - "Chúc mừng bạn hoàn tất trọn vẹn bài dự án và vượt qua kiểm thử tự động."
- **AIF L10, TOC L10** (giống hệt nhau):
  - "Bây giờ đến phần bạn tự thực hành và chấm thật trên máy. Hãy mở tệp đề bài, đọc kỹ dữ liệu vào cùng khuôn đầu ra cần in, tự viết chương trình rồi gõ lệnh dòng lệnh để tự chấm trước khi xem kết quả."
  - "Đây là kết quả mong đợi khi chạy đúng bài làm, dùng để bạn đối chiếu từng dòng trên máy của mình."
  - "Bảng này giải thích từng ký hiệu dùng trong lời giải tham khảo (phần N) để bạn tự đối chiếu cách viết." (AIF 4 lần, TOC 2 lần.)
  - "Cuối cùng là lời giải tham khảo bằng mã lệnh chạy ra đúng kết quả trên để bạn đối chiếu lại sau khi đã tự làm."
- **AIF L10 recap** (độn, ngoài các câu đã trích ở bảng A):
  - "Đừng quên kiểm tra thật kỹ thứ tự giải phóng vật nằm bên trên trước khi nhấc vật nằm bên dưới để tránh kế hoạch không hợp lệ."
  - "Cần lưu ý rằng các hành động đảo vị trí khối đòi hỏi kiểm soát chặt xem đỉnh khối đó đã thật sự trống hay chưa trước khi nhấc lên."
  - "Hãy thử tự tay viết thêm một vài kịch bản lập kế hoạch nhỏ để thấy rõ hiệu quả cắt giảm không gian tìm kiếm."
- **BNX L26, JVA L04, ACB L03**: lời practice viết riêng theo đề. Câu chỉ dẫn chấm dùng chung ("…lệnh in chữ ĐÚNG khi đầu ra trùng, hoặc chỉ ra dòng nào khác") có nội dung, không tính là độn.

## E. Thống kê

- **Bài có MUST**: 8/10 (LNX L06, MLP L04, PRJ L05, JVA L04, AIF L10, DBS L01, OSY L02, TOC L10). BNX L26 và ACB L03 không có MUST.
- **Số phát hiện**: 21 MUST, 33 SHOULD. Trong 21 MUST: 9 dòng về covers, 5 về mục tiêu không được dạy, 3 về số/kiến thức/đầu ra mã, 3 về lời khuôn mẫu hoặc độn, 1 về lab đòi ngôn ngữ chưa dạy.
- **Khung hình đã mở**: 46.
  - LNX 6: 00011, 00018, 00024, 00028, 00037, 00041.
  - MLP 5: 00012, 00021, 00030, 00039, 00043.
  - PRJ 5: 00020, 00024, 00033, 00043, 00047.
  - BNX 5: 00018, 00024, 00078, 00112, 00121.
  - JVA 4: 00026, 00096, 00112, 00121.
  - ACB 4: 00033, 00092, 00100, 00108.
  - AIF 5: 00020, 00061, 00065, 00068, 00080.
  - DBS 4: 00028, 00031, 00072, 00085.
  - OSY 4: 00016, 00030, 00064, 00071.
  - TOC 4: 00029, 00065, 00072, 00083.
  - Không thấy chữ tràn/đè nặng. Lỗi hình: SVG 960 px quá nhỏ (LNX, MLP), viền tô sáng chạm công thức (OSY 00064), bảng chú giải và lời giải chỉ hiện 7 s (AIF, TOC).
- **Phép tính/mã đã chạy lại**: khoảng 110.
  - 10/10 lời giải lab chạy trong thư mục tạm, đều khớp mong_doi.txt.
  - Mã trong bài: Bash của LNX; scikit-learn 1.9.1 của MLP; 4 chương trình Java của JVA (javac 21, mọi dòng "Kết quả chạy" khớp); Python của PRJ, BNX, ACB, AIF, TOC; 12 truy vấn SQLite của DBS.
  - Phiên bản phần mở rộng mặc định của Maven 3.9.11 đọc từ `maven-core-3.9.11.jar`: resources 3.3.1, compiler 3.13.0, surefire 3.2.5, jar 3.4.1 và 17 pha tới `package`, khớp bài BNX.
  - Máy đảo bit thử đủ 510 chuỗi; máy 0ⁿ1ⁿ thử đến độ dài 10.
- **CHƯA KIỂM**:
  - Chưa chạy Maven/Gradle/Jenkins/ksqlDB/Kafka/Redis thật. Số 1/9/34 jar của BNX chỉ đối chiếu bằng tên thư viện (spring-context 7.0.10, spring-boot-starter-web 3.5.7), không chạy lại.
  - Tình trạng hiện hành của ksqlDB và chặn O(t²) nêu theo trí nhớ, chưa đối chiếu nguồn.
  - Không nghe âm thanh. asr_report của cả 10 bài: thiếu audio 0, chưa xem xét 0. Số câu gắn cờ: LNX 0, MLP 5, PRJ 8, BNX 4, JVA 1, ACB 14, AIF 0, DBS 0, OSY 1, TOC 20. Chỉ đọc mục `asr_reviewed` trong đặc tả (JVA 1 mục, AIF/DBS/LNX rỗng), không đối chiếu từng câu gắn cờ với asr_report. Ở 6 bài BNX, JVA, ACB, MLP, OSY, TOC các mục này tự ghi "NOT_VERIFIED bằng tai người"; riêng 8 mục của PRJ L05 khẳng định "âm đọc TTS tiếng Việt giữ nguyên chính xác" mà không có ghi chú đó.
- **Ba lỗi hệ thống quan trọng nhất** (mỗi lỗi lặp ở ≥ 2 bài):
  1. **"Tự làm" không buộc phải làm.** Ở LNX L06, PRJ L05, DBS L01, OSY L02, cảnh practice chỉ ghi "mở de.md" bằng lời dán chung, de.md chép sẵn mọi dòng đáp án, số trùng ví dụ trong bài, không gợi ý (L3 = 0, L5 = 0). MLP L04 trùng 2/3 dòng với ví dụ. Hai lab còn đòi ngôn ngữ chưa dạy: SQL ở DBS L01 (bài SQL là L02), Python ở OSY L02. Chỉ BNX L26, JVA L04, ACB L03 đạt đủ 5 tiêu chí; AIF L10 có đề tốt nhưng thiếu đường dẫn tới lời giải.
  2. **`covers` gán máy móc.** 8/10 bài có ít nhất một dòng trỏ sai, tổng cộng 12/41 dòng. Hai kiểu lặp lại: bộ ba cố định example/check/quymo hoặc formula/example/check bất kể nội dung (MLP 0/3, PRJ 1/3, LNX 1/3), và mục tiêu trỏ vào `practice` dù được dạy ở cảnh khác (JVA, DBS, OSY). Kèm theo là mục tiêu giáo án không được dạy: LNX mục tiêu 1 và nửa mục tiêu 3, MLP mục tiêu 3, PRJ mục tiêu 3, AIF mục tiêu 2.
  3. **Bài ngắn và lời/bảng chèn khuôn mẫu.** Ba bài khoá mới (LNX, MLP, PRJ) dài 5,6–5,9 phút, khoảng 1 000 từ, đều "CHƯA" cho người mất gốc: 8–13 dòng mã giảng trong 2–4 câu, quiz hỏi lại đúng số của ví dụ, recap dán chung. Ở AIF L10 và TOC L10, phần chèn thêm là chỗ sai: bảng chú giải sai dòng hiện 7 s, recap độn 118 s (AIF, cùng kiểu ở recap AIF L09 và TOC L09), ghi chú "hai mức quy mô" có số sai hoặc không nguồn (10^150 ở AIF; O(t²) và "hằng số đa thức" ở TOC; 20 000 lần khớp và "< 100 ms" ở MLP; "0,5% tải 1 nhân" ở PRJ).
