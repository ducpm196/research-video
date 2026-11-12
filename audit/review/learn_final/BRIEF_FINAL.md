# Đọc chốt trước khi học: chặng 6–11 (đợt LF2, 2026-11-11)

Người dùng sắp học thật toàn bộ lộ trình từ con số 0 tới chuyên gia. 537 bài của chặng 6–11 chưa được một người đọc độc lập đọc trọn sau lần sửa gần nhất. Bạn nhận một lô trong số đó.
Đây là **lượt chốt phiên bản**: mục tiêu là bắt hết lỗi làm người học **hiểu sai** hoặc **kẹt**, không phải trau chuốt.

## Luật nền
Đọc trọn [`audit/review/learn_start/BRIEF_LS1.md`](../learn_start/BRIEF_LS1.md) và làm theo, trừ các điểm đổi dưới đây. Bạn **CHỈ ĐỌC**, không sửa tệp nào trong kho, không chạy build/tts/asr/render/git, không ghi tệp báo cáo. Tệp tạm chỉ đặt trong thư mục scratchpad ghi trong lời nhắn.

## Lô của bạn
`audit/review/learn_final/batches.json` → phần tử có `id` ghi trong lời nhắn. `lessons` là các bài theo đúng thứ tự học. `before` là các khoá người học đã học xong trước lô này (cộng các bài đứng trước trong chính lô). Một thuật ngữ đã giảng ở đó thì không tính là BLOCK-TERM; bạn không cần mở các bài ấy trừ khi nghi ngờ.

## Điểm đổi so với BRIEF_LS1 (để giữ chi phí hợp lý)
1. Mỗi bài đọc **trọn đặc tả** `lessons/<khoá>/<bài>.yaml` và **mục của bài trong giáo án** `curriculum/<khoá>.yaml`. Không cần mở `.srt` (lời đọc chính là `say`).
2. Khung hình: mở **2 khung** mỗi bài trong `out/<KHOÁ>/<Lxx>/frames/` (một khung hình cơ chế hoặc ví dụ có nhiều chữ nhất, một khung quiz hoặc tổng kết). Mở thêm chỉ khi thấy dấu hiệu tràn, đè.
3. Tính lại bằng Python **mọi con số** và chạy thử mã chạy được như BRIEF_LS1 yêu cầu. Viết một script cho mỗi bài hoặc mỗi nhóm bài, chạy, rồi mới kết luận.
4. Mức báo:
   - **MUST** và **BLOCK-TERM / BLOCK-STEP / BLOCK-QUIZ**: báo hết, kèm chuỗi cũ nguyên văn và chuỗi mới.
   - **SHOULD**: chỉ báo khi điều đó có thể làm người học nhớ sai một dữ kiện (khẳng định tuyệt đối sai, thiếu điều kiện áp dụng, số thực tế không nguồn, dữ kiện đã lỗi thời tính tới tháng 11/2026). Tối đa 2 mục mỗi bài. Không báo văn phong, cách diễn đạt, bố cục.
5. Với bài về công nghệ thay đổi nhanh (đám mây, Kubernetes, LLM, agent, MLOps, bảo mật, blockchain), kiểm thêm: dữ kiện về phiên bản, mặc định, giá, giới hạn có còn đúng tới 11/2026 không. Nếu bạn không chắc và không có nguồn, ghi mức SHOULD với tin cậy PLAUSIBLE, đừng đoán.
6. Bài tình huống / hành trình có `stage: {year, scale, source}` hoặc `audit/<khoá>/sources_*.md`: đối chiếu năm, con số, tên sự kiện trong bài với tệp nguồn ấy. Lệch là MUST.

## Chuỗi mới đề xuất phải áp được ngay
Như BRIEF_LS1: chuỗi cũ nguyên văn, khớp đúng một chỗ trong tệp; sửa `say` thì sửa cả `show` tương ứng; `say` là tiếng Việt nói được, không thêm từ ngoại mới, câu dài hơn 7 từ, **không đổi số câu** của một step có `focus` dạng danh sách (thêm mệnh đề vào câu đã có). Không viện khoá khác ("như đã học ở khoá…") trong chuỗi mới: giảng lại ngay tại chỗ bằng một mệnh đề.
Chuỗi mới càng ngắn càng tốt: mỗi thay đổi lời đọc buộc dựng lại cả video.

## Câu trả lời cuối
Bạn không ghi được tệp báo cáo (môi trường chặn), nên làm đúng hai bước sau để báo cáo đầy đủ nằm trong nhật ký còn câu trả lời cuối thì gọn:
1. Viết **báo cáo đầy đủ** thành một tin nhắn văn bản thường (bắt đầu bằng dòng `ĐÃ ĐỌC K/K bài: …`, rồi bảng phát hiện đủ chuỗi cũ/chuỗi mới, bảng từng bài, nhận xét), và **trong cùng lượt đó** gọi lệnh Bash `date -u +%FT%TZ`. Người điều phối trích báo cáo này từ nhật ký tác vụ.
2. **Câu trả lời cuối chỉ gồm**: dòng `TÓM TẮT ĐÃ ĐỌC K/K bài`, số MUST / BLOCK / SHOULD, và mỗi phát hiện một dòng `Bài · Mức · tóm tắt không quá 15 từ · tin cậy`. Không lặp lại bảng đầy đủ.

Báo cáo đầy đủ ở bước 1 theo đúng định dạng mục "Trả lời người điều phối" của BRIEF_LS1 (dòng `ĐÃ ĐỌC K/K bài`, bảng phát hiện, bảng từng bài, tối đa 6 gạch nhận xét). Sắp bảng phát hiện theo mức: MUST trước, rồi BLOCK, rồi SHOULD. Nếu bạn không kịp đọc hết lô, ghi rõ bài nào **chưa đọc**; đừng ghi "không phát hiện" cho bài chưa đọc trọn.
