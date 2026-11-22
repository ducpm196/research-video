# Handover AF4-FINAL | 2026-11-22 (100% Complete — 50 Khoá · 777 Bài · 11 Chặng AF2)

**Trạng thái: DONE 100% (Kỹ thuật & Sư phạm toàn kho `50/50` khoá · `777/777` bài · `11/11` chặng chuẩn AF2 "Tự làm").**

> **Tệp chính**: [`HOC_TAP.html`](file:///D:/research-video/HOC_TAP.html) (cổng học toàn bộ 11 chặng) · [`NGHE_THU.html`](file:///D:/research-video/NGHE_THU.html) (nghe thử mẫu cả 11 chặng) · [`curriculum/STATUS.md`](file:///D:/research-video/curriculum/STATUS.md) · [`curriculum/TRACKS.md`](file:///D:/research-video/curriculum/TRACKS.md) · [`audit/review/audit_final/STATE.md`](file:///D:/research-video/audit/review/audit_final/STATE.md).

---

## 1. Tổng kết hoàn thiện toàn kho (Số đo thực nghiệm sau lần sửa cuối)

- **Quy mô toàn kho**: **`50` giáo án (`curriculum/*.yaml`) · `777` bài học (`lessons/*`) · `777` video MP4 (`out/*/*/L*.mp4`) · `777` bài lab thực hành (`labs/*`) · `9 256.9 phút` (`154.3 giờ`)** phủ trọn **11 chặng (`S01..S11`)** từ nền tảng tới chuyên sâu và dự án tổng hợp (`PRJ`).
- **Trạng thái giáo án**: Đã chuyển toàn bộ **`23` khoá** còn `status: planned` sang `status: active` (`agt, aif, bch, cas, clc, cld, cvi, dan, den, dsc, esy, evt, irs, llm, mlo, par, plc, rbm, rln, rob, sar, sep, toc`). Tổng **`48` khoá `active`** (+ `cs112`, `cs115` không trường `status:`).
- **Video, độ tươi (`FRESH`) & giải mã (`OBSERVED`)**:
  - `find_stale_all.py`: **`TOTAL_STALE=0`** (`777/777` bài khớp tuyệt đối cả `spec_sha256` lẫn `tts_sha256`).
  - `pack.py check`: **`777 bài có video · có vấn đề 0 · chưa có video 0 · tổng 9256.9 phút`**; [`xem.html`](file:///D:/research-video/xem.html): `777 trang, 7156 liên kết, chết 0`; [`HOC_TAP.html`](file:///D:/research-video/HOC_TAP.html): `777 bài (777 có video, 0 đang soạn)`, `7937` liên kết tệp, `1910` liên kết neo, `0` chết, tự kiểm/khung hình/lab `777/777`; [`HOC_TAP.md`](file:///D:/research-video/HOC_TAP.md): `778 liên kết, chết 0`; [`NGHE_THU.html`](file:///D:/research-video/NGHE_THU.html): `11 chặng, 176 câu mẫu, liên kết chết: 0`.
  - Giải mã H.264/AAC (`ffmpeg -v error -xerror -f null -`): `777/777` MP4 giải mã sạch (`777/777` ở `task-13002`, sau đó `38/38` MP4 dựng lại ở đợt sửa âm thanh cũng đạt `DECODE_38: checked=38 fail=0` ở `task-13322`).
- **Giọng đọc & ASR (`50/50` khoá)**:
  - `asr_flags.py` trên đủ `50/50` khoá: **`ASR_FLAGS_50: 50 BAD= []`** (`0` câu chưa xem xét trên toàn bộ `50` khoá).
  - `tts_speed_scan.py 0.22`: `0` câu `< 0.22 s/từ` (đợt dựng lại cuối `ACB` `1094` câu `0 < 0.22 s/từ`; 11 khoá sửa phát âm `18 580` câu `0 < 0.22 s/từ`; Chặng 8–9 trước đó `0 < 0.22 s/từ`).

---

## 2. Kết quả toàn bộ các cổng kiểm tra toàn repo (sau lần sửa cuối)

| Cổng / Công cụ | Kết quả đo được | Ghi chú phạm vi |
|---|---|---|
| `verify_plan_curricula.py` | **`612 PASS · 0 FAIL`** | Đủ `50` lộ trình |
| `check_curricula_graph.py` | **`50 lộ trình · 777 bài · 1683 cạnh · 0 lỗi`** | `0` tham chiếu hỏng, `0` chu trình, `0` VER lệch |
| `pedagogy_scan.py` | **`777/777 ĐỦ` (`0 GẦN, 0 MỎNG`)** | Đủ `50/50` khoá |
| `af2_cover.py --require S01..S11` | **`100.0%` cả 11 chặng** (`0` chặng chưa phủ) | `af2`, `practice`, `lab` `777/777` |
| `arith_scan.py` | **`1478 phép tính kiểm được, 0 FAIL`** | Toàn kho |
| `check_meta.py` | **`0 vấn đề`** | Toàn kho |
| `check_next_refs.py` | **`572 lời hẹn, 0 lệch dãy học`** | Toàn kho |
| `check_course_refs.py` | **`0 lỗi trong 777 bài học`** | Chứng chỉ/bộ nhớ/ngưỡng |
| `check_xref.py` | **`44 lượt tham chiếu sang khoá khác ở 16 tệp` (`rc=0`)** | Tham chiếu chéo hợp lệ (`PRJ` 34, `CS115` 5, `MLP` 3, `CPR` 2) |
| `check_legal.py` | **`114 lượt dẫn, 22 văn bản (0 CHUA_KIEM), 0 FAIL`** | Đã đọc nguyên văn `37/2025/TT-NHNN` |
| `sync_tpl_from_lesson.py --all` | **`tổng: 0 mẫu lệch bài`** | Đồng bộ template 100% |
| `lab_gate.py` | **`777 PASS · 0 FAIL`** | Đủ `777/777` lab tham chiếu |
| `interview_sync_video.py --check` | **`99 pairs, 99 identical, 0 mismatched`** | Đồng bộ `interview/` |
| `verify_*.py` (`50/50` khoá qua `status_report.py`) | **`50/50` khoá PASS** (`verify_acb` `312/312`, `verify_bnk` `48/48`, `verify_bnx` `1011/1011`, …) | Sau sửa `verify_acb.py` & `ACB L02` |
| `screen_code.py` (`audit_all.py` + chạy riêng `bnk`/`bnx`) | **`49/50` khoá `0 FAIL` trong `audit_all`; `BNK 107 khối 0 FAIL` (`task-13062`); `BNX 712 khối PASS 958 · FAIL 0` (`task-13272`)** | Với `bnx-ora`/`bnx-mss` đang bật (`BNX L19` có 2 dòng chập chờn đóng pipe `docker exec -i` cụm Redis khi `audit_all` chạy nặng; chạy riêng `task-13272` PASS 100%) |
| `curriculum/STATUS.md` & `TRACKS.md` | `STATUS.md`: **`776/777` hoàn thiện (`9241` phút)** · `TRACKS.md`: **`777/777 ✓` qua 13 track** | `1` bài ghi chú ở `STATUS.md` chính là 2 dòng `BNX L19` của `audit_all.py` nêu trên |
| `interview/MASTER_CURRICULUM_INDEX.md` | **`777 bài có video, 154.3 giờ`** | Cập nhật bởi `master_sections.py` |

---

## 3. Các hạng mục chốt cuối đã thực hiện trong đợt `WP-AF4-6` & hậu kiểm tai người

1. **Độc lập Mẫu G (`seed=20261201`, `50` bài đại diện đủ `50/50` khoá, loại trừ đúng `164` bài Mẫu C/D/E/F)**:
   - Sửa sạch toàn bộ `6` bài có `MUST` (`AIF L03`, `CLC L01`, `CLD L04`, `MLP L13` [2 MUST], `PRJ L09`, `TOC L14`), gỡ đồng loạt boilerplate `recap[0].say` ở `61` tệp Stage 8 (`CLC, CLD, DEN, EVT, SAR` + `DAN L02`, `LLM L00`) + sửa toàn bộ `SHOULD` bài học & lab (`BCH L06`, `CPR L02`, `DAN L02`, `DEN L02`, `ESY L13`, `HCI L02`, `NET L03`, `OSY L08`, `PLC L07`, `SDP L04`, `SEP L10`, `WEB L13`, `labs/{CLD/L04, DEN/L02, DSY/L11}/de.md`), dựng lại sạch `75/75` bài (`task-12936`, `failed=0 []`).
2. **Xử lý 100% phản hồi nghe bằng tai người từ `D:\research-video\nghe_thu_ket_qua.json` (`12` mục `fix`/`warn`)**:
   - **5 mục `fix` (4 bài)**: `FND:L07:27` (sửa câu `s f là cờ s cùng cờ f` tránh đọc thành `TS`), `DEN:L02:94` (thêm nhịp `tốc độ ổ đĩa, thay cho việc sửa rời rạc` khắc phục mất âm `đĩa`), `RLN:L10:20` (đổi `r A trừ r B` → `r của A trừ đi r của B` khắc phục đọc `EB`), `HCI:L08:33` & `HCI:L08:41` (bỏ gạch nối `A-B-C` → `A B C`, `B C A`, `C A B` cả ở ví dụ và tự luyện).
   - **7 mục `warn` & bộ luật phát âm `lexicon_vi.{ACB,BNK,BNX,FND,INT,JV2,JVA,PRJ,PYT}.yaml`**: Sửa `ACB L02` (`Hình này vẽ` → `Hình minh hoạ`, đồng thời rút đúng còn `2299` từ ≤ `2300`), `DMS L07` (`hễ phần tử a có quan hệ R với b...`), `BCH L01` (`ghép chuỗi a b với chuỗi c d`), cập nhật `SQL` → `ét kiu eo`, `Oracle` → `O-rơ-cồ`, `ksqlDB` → `ca ét kiu eo đê bê`, `PostgreSQL` → `Pốt-g-rê ét kiu eo`, `PL/SQL` → `P L ét kiu eo` (đưa `SQLite` lên trước `SQL` trong `lexicon_vi.PRJ.yaml`). Dựng lại toàn bộ `38/38` bài bị ảnh hưởng (`task-13213`, `task-13248`, `task-13317`) và rà sạch ASR (`0` câu chưa xem xét).
3. **Sửa 2 lỗi kỹ thuật ở bộ kiểm tra**:
   - [audit/review/screen_code.py](file:///D:/research-video/audit/review/screen_code.py#L243): Không tự chuyển sang `labs/.venv-ml` (`Python 3.11.9`) khi khối mã đã tự chèn `deps/l23/venv` (`Python 3.13.5`) — dứt điểm `24` lỗi `numpy._core._multiarray_umath` ở `BNX L23`.
   - [audit/acb/verify_acb.py](file:///D:/research-video/audit/acb/verify_acb.py#L461): Cập nhật kiểm tra `37/2025/TT-NHNN` khớp sổ pháp lý đã đọc nguyên văn (`HIEU_LUC` / `ORIGINAL`).

---

## 4. Lưu ý minh bạch còn mở (ngoài phần máy đã kiểm 100%)

1. **Tai người đối với 38 video vừa dựng lại âm thanh (`NOT_VERIFIED bằng tai người` ở 12 câu mới qua ASR)**: Các câu giữ nguyên của `739` bài khác đã giữ nguyên âm thanh, còn `38` bài thuộc `ACB, BCH, BNK, BNX, DEN, DMS, FND, HCI, INT, PRJ, RLN` mới dựng lại âm thanh — bạn có thể nghe kiểm lại trực tiếp trên [`NGHE_THU.html`](file:///D:/research-video/NGHE_THU.html) đã sinh mới.
2. **Docker containers `bnx-ora` & `bnx-mss`**: Đang ở trạng thái `Up` trên máy. Nếu sau này tắt máy và chạy lại `verify_bnk.py` / `verify_bnx.py` / `screen_code.py --course bnk|bnx`, cần chạy `docker start bnx-ora bnx-mss` trước.
3. **Chưa `git commit`**: Toàn bộ thay đổi đang nằm trong working tree, chờ bạn tự quyết định commit theo ý muốn.
