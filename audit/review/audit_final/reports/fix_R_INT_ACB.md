# fix_R_INT_ACB: sửa INT (9 bài, thêm L08) và ACB (9 bài) theo R_INT_ACB, 2026-11-14

## Cổng thật (chạy lại cuối)
- lint: INT L00..L08 và ACB L00..L08 đều 0 FAIL 0 WARN; render: 0 vấn đề (đã xem lưới khung INT L04, L08, ACB L06..L08).
- `audit/int/verify_int.py` 207 PASS; `audit/acb/verify_acb.py` 260 PASS.
- `lab_gate.py INT` 9 PASS; `lab_gate.py ACB` 9 PASS.
- `screen_code.py check --course INT` PASS 83, 0 STALE/MISSING/ORPHAN; ACB PASS 81, 0.
- `lv.py curriculum` INT (9 bài) và ACB (9 bài) 0 lỗi; `check_curricula_graph.py` sạch; `check_next_refs.py` 0 lệch; `tests/test_e52.py` 0 FAIL; `audit/verify_plan_curricula.py` thêm INT:L04, INT:L08 (585 PASS, 0 FAIL).
- `check_legal.py`: INT/ACB sạch; còn 1 FAIL ngoài phạm vi (`lessons/bnk/L13...` dẫn TT 50/2024 trơn). Tôi đã vá YAML hỏng của `audit/legal/registry.yaml` (dòng 50/2024 có ": " trong tiêu đề, do nhánh khác sửa).
- Lời đọc: INT 1 759–2 236 từ, ACB 1 773–2 263 từ (đều ≤ 2 300); INT L04 = 1 963 (≤ 2 100), INT L08 = 1 875.

## INT
- **L04 tách**: còn OFS + IBM MQ (thêm cảnh concept có SVG và quiz chọn khoá khử trùng), ISO 8583/PIN/HSM, cảnh quy mô mới (STAN quay vòng 10 000/1 000/100 giây; tin chờ 200/2 000/20 000), mã 68 kèm "cần kiểm đặc tả", MTI 0400/0420 thống nhất (đảo chỉ khi đã biết chắc thất bại). Lab mới 5 dòng (bitmap, khối PIN, STAN, chặn nhầm, tin chờ).
- **L08 mới** (`lessons/int/L08_tin_dung_ban_le_va_doi_soat_cuoi_ngay.yaml`, `requires: [L07]`, `requires_ext` PYT:L00–L03): af2 + covers, prereq/concept/symbol/check/example/quymo/pitfall (khoá 300 s hết hạn)/quiz hai pha/practice + `labs/INT/L08`; LTV, DTI, CIC, EOD giảng tại chỗ (thêm 6 mục `symbols.INT.yaml`: HSM, STAN, LTV, DTI, CIC, EOD); TT 31/2024 kèm "đã được TT 37/2025 sửa đổi, cần đối chiếu bản hợp nhất" (bỏ dẫn NĐ 23/2025). Đã cập nhật `curriculum/int.yaml`, `verify_int.py`, `screen_code/INT.yaml`, `verify_plan_curricula.py`. INT L00 (nhãn tầng 4 + câu nói) và INT L07 (recap) trỏ tới L08 là bài cuối.
- **L00**: hai nhóm vai trò nói theo "nghiêng về", mức 3 và bản thiết kế có ở cả hai nhóm, JBoss/JSP/MS SQL/sở hữu mảng là dấu hiệu chính (phần sở hữu mảng ghi chưa kiểm chứng); lab L00 đổi theo; câu SELECT … FOR UPDATE ghi "trên Oracle và PostgreSQL" (MySQL InnoDB khác).
- **L02**: thêm mục tiêu + covers cho cảnh Bloom (YAML và giáo án). **L03**: "mô hình đơn giản hoá" cho 20 000/20 lần đổi ngữ cảnh.
- **L05 (P1 1→2 dự kiến)**: giảng ln và "cận tin cậy trên", model.encode/384 chiều, thêm bước Isolation Forest (cách tách + giới hạn), quiz và check có phương án nhiễu hợp lý, thêm bước loại B/C/D; QĐ 2345 thay bằng TT 50/2024 sửa đổi bởi TT 77/2025 (QĐ 2345 chưa đọc nguyên văn); bỏ "giảm đáng kể".
- **L06**: pháp lý như L05 (YAML và `labs/INT/L06/de.md`); bỏ đường dẫn `interview/06...` khỏi màn hình (bài tự đứng được); quiz C/D viết lại hợp lý và có giải thích loại A/C/D; hai nhóm vai trò theo L00.
- `verify_int.py` thêm kiểm: tách L04/L08, QĐ 2345 luôn kèm "chưa đọc nguyên văn", Bloom có covers, hai nhóm "cả hai", không dẫn tệp interview/ trong L06.

## ACB (nhánh phụ, đã đối chiếu lại các cổng)
M2 sửa `labs/ACB/L08/de.md` (bỏ dấu hai chấm); 9 lab ACB tự viết `mau.py` theo `de.md` chấm `cham.sh` 9/9 ĐÚNG; thêm kiểm `de.md` ↔ `mong_doi.txt` vào `verify_acb.py`. L06 bỏ "Quyết định 2345" làm căn cứ ở tiêu đề/nhãn/recap, quy tắc "về 0" ghi giả định minh hoạ; L08 TT 37/2025 và mục tiêu 5; L00 quiz "số minh hoạ", Redis→thông lượng ghi (L00, L02), MTI chung câu; L03 NX đặt trước; L05 3,0 s; L07 hai phân loại hiện trên màn hình, 1e9 phép/s; L04/L01 sửa chữ. Tôi sửa thêm ACB L00 câu trả lời lương: bỏ "50 triệu gross" và 650/700/850, dùng L = 40 (số minh hoạ) và dặn hỏi khung trước.

## Tài liệu phỏng vấn
`interview/00, 04, 05, 06, 07, README`, `MASTER_CURRICULUM_INDEX.md`, `HANDOVER_INTERVIEW.md`, `SOURCE_CODE_VIDEO_MAP.md`: bỏ 50M/số lương không nguồn/tên người thật (Câu 76), QĐ 2345 không còn là căn cứ; `07_...50m_gross.md` viết lại theo INT L07 (tên tệp giữ). Chưa làm: khối do công cụ sinh trong MASTER_CURRICULUM_INDEX (giữa BEGIN/END) còn tiêu đề cũ và chưa có hàng INT L08, cần chạy `interview_gen_tables.py` (ghi) khi dựng lại; `resources/job/` CV còn tên người tham chiếu (ngoài phạm vi). `interview_sync_video.py --check`: 92 cặp, 56 lệch do bản sao video cũ.

## Không làm / để người điều phối
- M1: dựng lại mp4/srt/chapters 12 bài (INT L05–L08 mới, ACB L00–L08) và dựng mới INT L04, L08; `HOC_TAP.md/.html` do `pack.py page` sinh lại.
- Câu ASR chưa xem xét INT L00–L03 (sau dựng); asr_reviewed của INT L04 chỉ giữ các câu còn tồn tại.
- Chưa dò phát âm ASR cho lời đọc mới (L04, L08, L05 Isolation Forest...).
- Tiêu đề INT L06 vẫn ghi "100 câu" (video chỉ 5 tình huống, hook nói rõ).
