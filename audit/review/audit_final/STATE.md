# STATE đợt AF2 (sổ sống; phiên khác đọc `handover_AF1_*`, `plan_AF1_*`, tệp này là đủ làm tiếp)

Cập nhật: 2026-11-12T18:50Z. Quyết định D-1…D-6 dùng MẶC ĐỊNH (người dùng giao toàn quyền ở tin nhắn ngày 2026-11-13).

## Sổ tác tử (≤ 4 cùng lúc; tiếp tục bằng SendMessage tới id, KHÔNG mở tác tử mới cho cùng việc; lưu báo cáo ra tệp NGAY khi nhận)
| Việc | id | Trạng thái |
|---|---|---|
| Thiết kế lại HOC_TAP (`pack_dev.py` → `HOC_TAP.dev.html`) | a0ee400a3d6ba6997 | XONG: 42/42 phép thử, 0 lỗi JS, tương phản ≥ 5,9:1; CHƯA áp vào pack.py (xem việc tiếp theo) |
| Soạn khoá FND (11 bài) — `BRIEF_FND.md` | a8fa304492dabea0b | XONG (verify 70/70); đang dựng video |
| Soạn khoá JV2 (10 bài) — `BRIEF_JV2.md` | a160f034e515be4d0 | XONG (verify 75/75, lint/render sạch, 10 lab PASS); đã vào hàng dựng |
| Nâng JVA L00–L12 — `BRIEF_JVA.md` | ae30a55676664f8ee | XONG (143/143 verify, 13 lab PASS, screen_code PASS); đã vào hàng dựng |
| Sổ screen_code cho FND + JV2 | a4a9b2ed8181efeee | đang chạy |
| Nâng BNK L00–L14 — `BRIEF_BNK.md` | a55bf1edfd9b08cbb | XONG (verify 36/36, 15 lab PASS, screen_code PASS); đã vào hàng dựng |
| Sửa mẫu F nhóm A (13 bài) — `BRIEF_FIXF.md` | adbc07b90acbda1f3 | đang chạy |
| Sửa mẫu F nhóm B (13 bài) | a7a63d8150b1e645a | đang chạy |

## Tiến độ gói việc
- WP0 XONG 2026-11-12T20:15Z: mốc ở `logs/BASELINE_AF2.md`. `snap/` đã chụp (scratchpad phiên). Cổng đầu đợt: `logs/gates_pre.out` (chạy lại lần 2 lúc 18:3xZ vì lần 1 chết khi tool kết thúc: PHẢI chạy bằng `run_in_background` trực tiếp, không `nohup … &`).
- WP1: xong E51/E53 trong `tools/lv.py` (bài khai `af2: true` + `covers` + cảnh `practice` có `lab:`), kind `practice` (stem.yaml, player.css `.k-practice`), `.dim` opacity .38→.66 (tương phản 2,2→4,8:1); `audit/review/lab_gate.py`, `check_next_refs.py` (G-ORDER), `check_legal.py` + `audit/legal/registry.yaml` (G-LEGAL), `audit/labkit.py`. Chưa làm: E52 (thuật ngữ tại chỗ), E54 (phép tính hiển thị), E55 (thuật ngữ liên khoá).
- WP2: `labs/ENV.md`, `labs/check_env.sh`, `labs/cham.sh`, `labs/sqlrun.py` (máy này chưa có `sqlite3` CLI → chạy bằng Python). Bài mẫu JVA L04: nguồn đã sửa (`audit/jva/src/l04.py`), CHƯA chạy gen (chờ gates_pre xong).
- G-ORDER đo: 551 lời hẹn "Bài sau (bài N)", 93 lệch dãy học → sửa bằng đổi thuật toán xếp dãy (DFS "kéo tiên quyết vào đúng lúc") trong `pack.py stages()` thay vì sửa chữ.

## Phát hiện G-ORDER (đã đo bằng nguyên mẫu scratchpad `order_proto.py`)
Thêm cạnh ngầm L(k)→L(k+1) trong cùng khoá vào `pack.lesson_index` (CHỈ để xếp dãy) cho: 551 lời hẹn, 0 lệch; 0 vi phạm tiên quyết; 0 cặp liền kề bị đảo; 680/680 bài có chỗ (không có cạnh ngầm: 93 lệch). Áp dụng vào `pack.py` sau khi design agent xong (tránh xung đột với `pack_dev.py`), và thêm FND/JV2/PYT vào STAGES, tracks.yaml.

## Dọn dẹp đã làm
16 tệp bàn giao gốc cũ → `archive/handovers/` (git mv; HANDOVER.md đã trỏ lại).

## Việc tiếp theo (theo thứ tự)
1. Khi `gates_pre.out` xong: đọc từng dòng tổng; lưu mốc.
2. Chạy `gen.py L04` JVA → lint → render → verify_jva → lab_gate; xem khung `practice`; dựng; chấm bằng người đọc.
3. Brief `BRIEF_AF2.md` → tác tử: FND (10 bài), JV2 (10 bài), nâng JVA L00–L12.
4. Đổi thuật toán xếp dãy; thêm khoá mới vào STAGES/tracks.yaml; swap `pack_dev.py` → `pack.py`.

## 2026-11-13T23:45Z — bẫy TTS
4 luồng dựng cùng lúc → Edge TTS chặn (NoAudioReceived), mỗi bài chờ 3 phút + dựng lại. Đã tắt luồng c, d; CHỈ 2 luồng (a, b) khi có câu mới (đúng quy tắc LF2). Hàng: `audit/review/audit_final/rebuild.queue`; sổ xong: `rebuild.done` (ghi cả bài FAIL: grep "FAIL sau" trong `logs/rebuild.*.out`).

## 2026-11-13T04:55Z — AF2 XONG phần thực hiện (trạng thái cuối phiên)
Đọc `handover_AF2_20261113T0400Z.md` và `plan_AF3_next.md`. Tác tử: không còn tác tử chạy (FND/JV2/JVA/BNK/FIXF A,B/screen_code đều xong; các tác tử chờ tiến trình nền đã TaskStop). Hàng dựng rỗng (`rebuild.queue` − `rebuild.done` = 0); không còn luồng dựng. `HOC_TAP.html`, `HOC_TAP.md`, `xem.html` đã sinh lại lúc cuối (701 bài, 49 bài có Tự làm). Việc kế tiếp: AF3 (PYT trước).
