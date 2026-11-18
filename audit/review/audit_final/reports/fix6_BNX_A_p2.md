# fix6 BNX_A phần 2 (nhánh A2: L04–L07), 2026-11-16

## TIẾN ĐỘ
- [x] L04, L05, L06, L07 xong. Không chạy docker/dbrun/build/tts/asr/git; không chạy `screen_try --merge`; không sửa `audit/review/screen_code/BNX.yaml`.

## Bài đổi (requeue): L04, L05, L06, L07
Nguồn sửa: `audit/bnx/src/l04.py … l07.py`, sinh lại bằng `gen.py`. Không sửa `tools/registry/symbols.BNX.yaml` (chỉ dùng `introduces` đã có: bnx_khoa_phan_vung, bnx_explain). Sửa tay có bằng chứng: `audit/bnx/screen/l05.yaml` (khoá `files:` may.sh/xau.sh của nguồn `src:BNX:L05_certs`, `example 2 0/3 0` → `example 3 0/4 0` vì chèn bảng openssl, cùng sha khối bash).

## Bảng từng bài
| Bài | Mục R4 → cách xử lý | Từ trước→sau | lint / render | verify / sổ mã | Chưa giảng ước còn | asr_reviewed |
|---|---|---|---|---|---|---|
| L04 | `HTTP/1.1` → thêm vào ghi chú dưới khối yêu cầu xin mã ("phiên bản giao thức") + lời đọc. SHOULD hình tuần tự: rút ngắn nhãn ② ④ ⑤ cho vừa khoảng giữa hai đường đời (xem khung 23, 28: không còn đường nét đứt gạch qua chữ) | 2288→2293 | 0/0/37; render 108 khung 0 vấn đề | verify_bnx 23/23 PASS; screen_fast PASS 11, FAIL/STALE/MISSING/ORPHAN 0 | 0 | 5→5 |
| L05 | `-CAkey`, `-not_before/-not_after`, `openssl verify -CAfile` → bảng mới "lệnh openssl thêm" (4 hàng) đứng trước bước B; `critical`/`keyCertSign` → hàng `-addext` bảng đầu; `c, _ = nghe.accept()`, `t.sendall(x.encode())`, `loi.append`, `a; b` → bảng mới trước mã phục vụ; `if ten:`, `create_connection(getsockname())`, `t.recv(64).decode()`, f-string `\n` → bảng mới trước mã khách; `th.join()`, `with … as s, \` → hàng bảng Thread/with; `//`, `def … nam=365`, `for _`, `while`, `+=` → bảng mới ở cảnh quymo trước `xoay`; gợi ý Tự làm nhắc `//` (7 // 2 = 3). Bỏ "như ở bài bốn" ở lỗi 2. Cắt ~290 từ ở hook, prereq, sym, intuition, formula, ví dụ, quiz, pitfalls, recap | 2298→2297 | 0/0/35; render 126 khung 0 vấn đề, xem khung 47, 73, 89 | verify_bnx 21/21 PASS; screen_fast PASS 14, 0/0/0/0 | 0 | 5→4 (một câu quiz.3 bị cắt) |
| L06 | `IS NULL`/`IF … THEN`/`OR` → bảng mới ở cảnh sym (trước bảng câu SQL); `NUMBER`, `VARCHAR2(10)`, `INSERT … VALUES` (kể cả nhiều dòng) → bảng mới trong prereq trước khi dựng bảng; cờ docker → lệnh Docker tách khỏi đề Tự làm, thành step riêng cuối cảnh (bảng 3 hàng: `run -d --name -p -e`, `logs`, `exec -it … sqlplus`) giống L07 practice.4 (SHOULD). Cắt bù ở recap, ví dụ, pitfalls, quiz, check | 2262→2291 | 0/0/38; render 133 khung 0 vấn đề, xem khung 13, 31, 125 | KHÔNG chạy ver/screen_fast (Oracle/Docker); `screen_keep` + `shacheck`: 20/20 khối sha khớp, 0 MISSING/STALE/ORPHAN; chữ trong mọi khối mã không đổi | 0 | 8→7 |
| L07 | "biến gắn" → định nghĩa tại chỗ (ghi chú + lời đọc, bước 3 công thức); `VALUES LESS THAN`, `DATE '…' + TRUNC((ROWNUM-1)/10)`/`MOD` → bảng sym mới "lệnh tạo bảng"; `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(…))` → bảng sym "xem kế hoạch" tách riêng; `->>` → giải thích trong đề Tự làm + lời đọc. Cắt bù prereq, formula, quiz, quymo, check, recap | 2273→2297 | 0/0/39; render 127 khung 0 vấn đề, xem khung 17, 21, 50 | KHÔNG chạy ver/screen_fast (Oracle); `screen_keep` + `shacheck`: 24/24 khối sha khớp, 0 MISSING/STALE/ORPHAN; chữ trong mọi khối mã không đổi | 0 | 8→8 |

Số từ đếm bằng tổng `len(say.split())` của YAML sinh ra (`dump.py`), cùng số với lint. Mọi `say` 4–38 từ, lint 0 WARN.
asr_reviewed: `gen.py` chỉ giữ câu còn nguyên văn; câu bị sửa/cắt mất mục rà (L05 −1, L06 −1 so với trước phiên này), cần nghe lại ASR các câu mới/đổi.

## SHOULD đã sửa (thuộc L04–L07)
- L04 intuition.1 nhãn hình tuần tự: rút ngắn nhãn để nằm gọn giữa hai đường đời.
- L06 practice.1: lệnh Docker tách khỏi đề thành step riêng (bảng cờ docker, chữ ghi trên màn hình đủ lớn, không còn đoạn chữ xám nhỏ 7 dòng).

## Không làm / ghi chú
- L06, L07: không chạy `verify_bnx.py L06/L07` và `screen_fast` (cần Oracle/Docker, bị cấm); các khối mã giữ nguyên văn nên ledger vẫn khớp theo sha. `screen_code check` đầy đủ (Oracle) để người điều phối chạy khi được phép.
- Pháp lý/nguồn: giữ nguyên nhãn và số hiệu (L04 TT 64/2024/TT-NHNN không đổi); không thêm nguồn mới.
- Lời giải thích Docker ở L06 dùng `logs` (không `-f`) so với L07 (`logs -f`): khối L06 chỉ là bảng nghĩa, không phải khối chạy.
