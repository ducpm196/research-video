# BRIEF_K — Đọc độc lập Mẫu K (lượt rà AF6, 2026-11-27)

Bạn là người đọc độc lập. Việc của bạn: đọc kỹ 8 bài được giao và ghi MỘT tệp báo cáo. Bạn không sửa gì trong kho.

## Người học mục tiêu và đích đến

Người học bắt đầu từ con số 0 (chưa từng lập trình), chỉ có video, thư mục `labs/` và trang học. Đích của cả kho: năng lực nền của kỹ sư senior về công nghệ thông tin, khoa học máy tính, trí tuệ nhân tạo, khoa học dữ liệu. Hãy đọc từng bài bằng con mắt đó: bài có dạy đúng không, người mất gốc có theo được không, và phần thực hành có rèn được việc mà một kỹ sư thật phải làm với chủ đề này không.

## Luật làm việc

1. Thư mục kho: `D:\research-video`. CHỈ ĐỌC kho. Tệp duy nhất được ghi trong kho là tệp báo cáo của bạn (đường dẫn ghi ở cuối lời giao việc).
2. Không chạy `build`, `tts`, `asr`, `render`, `gen.py`, bất kỳ lệnh `git` nào làm đổi kho (chỉ được `git status --short`), không cài gói.
3. Mọi lệnh chạy thử phải làm trong thư mục tạm NGOÀI kho (ví dụ `mktemp -d`); không bao giờ chạy lời giải lab với thư mục hiện hành là gốc kho. Trước khi kết thúc chạy `git status --short` ở gốc kho; nếu thấy tệp lạ do bạn tạo ngoài tệp báo cáo, ghi rõ vào báo cáo (đừng tự xoá tệp không phải của bạn).
4. KHÔNG đọc trước: `audit/review/read_af5/`, `audit/review/sample_*`, mọi tệp `handover_*`, `plan_*`, `HANDOVER.md`, `STATE.md`. Riêng `audit/review/read_af5/<KHOÁ>/<Lxx>.md` của đúng bài bạn đọc: chỉ mở SAU KHI đã viết xong nhận định của mình về bài đó (bước F).
5. Không bịa. Việc gì không chạy/không kiểm được thì ghi `CHƯA KIỂM (lý do)`. Mỗi lỗi nêu ra phải kèm trích nguyên văn và bằng chứng (phép tính lại, lệnh đã chạy và kết quả).
6. Ghi báo cáo dần sau mỗi bài (đừng đợi đọc hết 8 bài mới ghi) để không mất việc nếu bị ngắt.

## Mỗi bài làm đủ 6 bước

Tệp cần đọc: đặc tả `lessons/<khoá>/Lxx_*.yaml` (đọc TOÀN BỘ), `labs/<KHOÁ>/<Lxx>/` (đề `de.md`, `mong_doi.txt`, `loi_giai.*` hoặc thư mục `loi_giai/`, `ca_an/`, `kiem/`), dòng của bài trong `curriculum/<khoá>.yaml` (mục tiêu, tiên quyết).

**A. Chuẩn xác.** Tự tính lại mọi con số quan trọng, tự kiểm công thức, định nghĩa, khẳng định. Chạy thử đoạn mã minh hoạ nếu chạy được (Python: `D:\research-video\.venv\Scripts\python.exe`). Phân mức:
- `MUST`: sai kiến thức/công thức/số liệu; đầu ra trên màn hình khác đầu ra chạy thật; khẳng định tuyệt đối sai điều kiện; mục tiêu khai báo mà không được dạy; dùng khái niệm/cú pháp/công cụ chưa dạy tại chỗ và không có ở bài tiên quyết khiến người mất gốc kẹt; cảnh Tự làm không đủ để làm bài; lời giải không chạy ra `mong_doi.txt`.
- `SHOULD`: lệch nhỏ giữa lời (`say`) và màn hình (`show`), thiếu giả định/đánh đổi, ký hiệu không nhất quán, hình chữ quá nhỏ/chồng lấn.

**B. Câu độn.** Tìm câu trong lời đọc không mang thông tin (đúng với mọi bài, có thể dán sang bài khác mà không ai nhận ra, hoặc khẳng định chung chung kiểu "giúp hệ thống ổn định hơn" không kèm cơ chế/số liệu). Trích tối đa 6 câu tiêu biểu kèm tên cảnh; ước lượng tỉ lệ lời đọc là câu độn (0%, <5%, 5–15%, >15%).

**C. Thực hành.** Trả lời từng ý:
1. Chỉ với video của bài này và `de.md`, người mất gốc có tự làm được lab không? Đề có định nghĩa đủ định dạng vào, ý nghĩa từng giá trị ra, quy tắc làm tròn không? Nêu chỗ thiếu.
2. Lab có rèn đúng kỹ năng khó nhất trong mục tiêu của bài không, hay chỉ là một phép tính bên lề?
3. Xếp loại lab, chọn một: `CÔNG CỤ THẬT` (dùng đúng công cụ/thư viện/ngôn ngữ mà nghề dùng cho chủ đề này, ví dụ SQL thật, gcc, Docker, sklearn, Spring), `MÔ PHỎNG CÓ NGHĨA` (tự cài một cơ chế cốt lõi của chủ đề, ≥ ~20 dòng có lôgic), `TÍNH CÔNG THỨC` (đọc vài tham số, áp một công thức, in 1–3 dòng). Ghi số dòng mã của lời giải.
4. Chấm thật: chép lời giải ra thư mục tạm rồi chạy `bash labs/cham.sh <KHOÁ> <Lxx> <đường_dẫn_tệp_tạm>` từ thư mục tạm (gọi bằng đường dẫn tuyệt đối tới `labs/cham.sh`). Ghi kết quả. Sau đó thử một "bài làm in cứng": tệp chỉ in nguyên văn nội dung `mong_doi.txt`; bài này PHẢI bị chấm trượt nếu lab có `ca_an/`. Ghi kết quả thật. Với lab kiểu dự án (`loi_giai/` là thư mục, cần Maven/Docker): nếu không chạy được trong thời gian hợp lý thì đọc mã + `kiem/` và ghi `CHƯA KIỂM (lý do)`.

**D. Khoảng cách tới nghề.** Tối đa 3 gạch đầu dòng: với chủ đề này, việc gì một kỹ sư có nền vững phải làm được mà bài + lab chưa rèn (ví dụ: chưa từng chạy công cụ thật, chưa đọc lỗi thật, chưa đo trên dữ liệu thật, chưa viết kiểm thử). Chỉ nêu điều cụ thể, kiểm được.

**E. Khung hình.** Mở 3–4 ảnh trong `out/<KHOÁ>/<Lxx>/frames/` (chọn rải đều, có ít nhất một ảnh của cảnh Tự làm nếu tìm được). Ghi tên tệp đã xem; chữ có đọc được, có tràn/chồng, có khớp nội dung đặc tả không.

**F. Đối chiếu.** Sau khi xong A–E của bài, mở `audit/review/read_af5/<KHOÁ>/<Lxx>.md`. Ghi: báo cáo đó chấm gì (MUST/SHOULD, điểm P, điểm L), bạn đồng ý hay không, và liệt kê điều bạn tìm ra mà báo cáo đó bỏ sót (hoặc ngược lại, điều báo cáo đó đúng mà bạn sót).

## Khuôn tệp báo cáo

```markdown
# Mẫu K — người đọc <K1|K2|K3|K4> — <ngày giờ UTC lúc bắt đầu>

## <KHOÁ> <Lxx> — <tiêu đề> — sha256 16 ký tự đầu của tệp YAML: `<...>`
### A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên văn | Vì sao sai + bằng chứng | Đề xuất sửa |
### B. Câu độn (ước lượng: ...)
### C. Thực hành
### D. Khoảng cách tới nghề
### E. Khung hình
### F. Đối chiếu read_af5
(… lặp cho đủ 8 bài …)

## Bảng tổng (bắt buộc, đúng 8 dòng)
| Bài | MUST | SHOULD | Độn | Loại lab | Dòng mã lời giải | Mất gốc tự làm được? (CÓ/KHÓ/KHÔNG) | Lời giải PASS? | In cứng bị trượt? | read_af5 bỏ sót gì |
## Nhận xét chung (≤ 10 dòng): mẫu hình lặp lại giữa các bài, điều đáng lo nhất, điều làm tốt.
```

Câu trả lời cuối cùng gửi về cho người điều phối: chỉ cần bảng tổng 8 dòng và ≤ 5 dòng nhận xét; mọi chi tiết nằm trong tệp.
