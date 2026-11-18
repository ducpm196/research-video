# Sửa BNX L29 theo R_BNX_L24_30 (nhánh L29)

Nguồn sửa: `audit/bnx/src/l29.py` (+ `audit/bnx/ver/l29.py`, `audit/bnx/sources_l29.md`, nhóm L29 của `tools/registry/symbols.BNX.yaml`). YAML sinh bằng `gen.py L29`.

## Mục báo cáo → xử lý
| Mục | Xử lý |
|---|---|
| P1: CQRS, Event Sourcing không khai triển (chỉ ở tiêu đề/bảng CV) | Cảnh `prereq` thành "sáu điều": thêm hàng ⑥ khai triển trên màn hình (CQRS = Command Query Responsibility Segregation: tách mô hình ghi khỏi mô hình đọc; Event Sourcing = lưu chuỗi sự kiện làm nguồn sự thật, không lưu con số cuối) kèm ví dụ "bài này làm cả hai: kho sự kiện để ghi, bảng số dư để đọc"; lời đọc nói nghĩa bằng tiếng Việt (tên tiếng Anh chỉ hiện trên màn hình, chưa dò ASR). E52: `bnx_cqrs`, `bnx_event_sourcing` (`introduces` ở prereq); grep L31–L36: không bài nào dùng. sqlite đã được giảng sẵn ở hàng ④ (trigger) và hàm lời đọc đổi "sqlite" thành "cơ sở dữ liệu nhỏ"; không thêm. |
| trigger gỡ được bằng `DROP TRIGGER`, "không sửa được lịch sử" tuyệt đối | Sửa: formula step 1 thêm ghi chú trên màn hình ("trigger chỉ chặn khi chưa ai gỡ nó; người có quyền quản trị (DROP TRIGGER) vẫn sửa được; cần quyền tối thiểu và chuỗi băm nối sự kiện"), lời đọc nói giới hạn; example step ① bỏ câu "chương trình lỗi cũng không sửa được lịch sử" → "chương trình lỗi không sửa được, còn người quản trị gỡ được đoạn lệnh thì vẫn sửa được"; pitfalls Lỗi 1 thêm "người quản trị gỡ được trigger, nên vẫn cần phân quyền". `ver/l29.py` chạy sqlite thật: UPDATE bị chặn, `DROP TRIGGER` rồi UPDATE thành công. Không dạy "kiểm soát đồng thời khi ghi (phiên bản kỳ vọng)": ngoài phạm vi 16 phút/mục tiêu `covers`; ghi vào giới hạn của bài thay vì thêm cảnh. |
| "so du -15" không giải thích; đoạn sinh dữ liệu không lên màn hình | Sửa: nguồn `QuyMoPhat` gọn lại (bỏ `import time` thừa, bỏ dòng trống) để khung hiện được phần SINH dữ liệu (executemany) cùng hàm dựng lại (12 dòng); ghi chú trên màn hình "số thứ tự chẵn là nạp, lẻ là rút, tiền = i % 97 + 1 (số minh hoạ)" và "số dư âm là bình thường: dữ liệu sinh minh hoạ không chặn rút quá số dư"; lời đọc nói số dư âm vì sao. `ver/l29.py` tính lại -15 (10³) và 35 (10⁶) bằng SQL. |
| số lời đọc mà màn hình không hiện (00081: đề 800,150,90,40 ở đáp án) | Sửa: quiz đáp án câu 1 hiện lại kho `NAP 800, RUT 150, RUT 90, NAP 40` và `RUT 15`; lời đọc đáp án đọc kho. Lời đọc đề câu 1 rút gọn "kho bốn sự kiện trên màn hình". |
| Lab `de.md` mâu thuẫn ("không sửa kho" vs "thêm cả RUT 300 rồi NAP 300") | Sửa `LAB_DE` mục 3: "có thêm một sự kiện `RUT 300` bị GHI NHẦM vào cuối kho (kho thành 7 sự kiện). Không sửa, không xoá nó: thêm sự kiện bù `NAP 300` (kho 8 sự kiện), phát lại toàn bộ rồi in số dư". `loi_giai.py`/`mong_doi.txt` không đổi (500 khớp). |

## Độ dài
Lời đọc 2 270 → 2 286 từ (≤ 2 300). Đã thêm ~100 từ giảng (prereq, giới hạn trigger, số dư âm, đáp án) và cắt ~85 từ ở: câu đề quiz, recap CV, lỗi 2/4, câu tự làm, bước 3/5 formula, bảng quy mô. `covers` giữ nguyên 7/7.

## Cổng thật (PYTHONIOENCODING=utf-8, 2026-11-13)
- lint 0 FAIL, 0 WARN (31 PASS); render 105 khung, 0 vấn đề.
- `verify_bnx.py L29`: 23/23 PASS (thêm 2 dòng: DROP TRIGGER; -15/35 bằng SQL).
- `lib2.py gen-screen L29`: 16 khối, ghi 16, chưa khớp 0. `screen_fast.py L29`: PASS 24 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0.
- `lab_gate.py BNX`: 13 PASS · 0 FAIL.
- Khung đã xem: 00005 (prereq 6 hàng), 00023 (bản chụp), 00027 (trigger + ghi chú giới hạn), 00058 và 00061 (quymo: mã sinh dữ liệu, số dư âm).

NOT_VERIFIED: phát âm "CQRS/Event Sourcing" (không đọc trong lời); hiệu quả sư phạm với người học thật.
