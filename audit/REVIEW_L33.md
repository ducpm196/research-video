# Rà soát L33 — Bài 33 — Tổng ôn: bảng thuật toán & 3 câu hỏi vàng

- Đặc tả: `lessons/L33_tong_on.yaml`; nguồn: tex#L392–L421 (bảng hệ thống thuật toán; 3 câu hỏi vàng); AUDIT A14 (KNN không có hàm sai số), A23 (LDA: tỉ số), A24 (K-Means: tổng bình phương)
- Quy mô: 9 cảnh, 15 step, 2 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 10 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 1 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L33/build_report.json`): 47 khung, 258.467 s, built_at 2026-10-26T18:33:38Z, spec_sha256 `0114871e838d2401…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L33/asr_report.md`): câu: 47, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0; checked_at 2026-10-26T19:09:20Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 5 | 0.791 | Câu ba, tối ưu, tìm tham số bằng giải đóng, gradient descent, thuật toán lặp, hay không cần học. | Câu 3, tối yêu, tìm tham số bằng giải đóng, gradient descent, thuộc toán lập, hay không cần học. | “ưu” → nghe thành “yêu”; “đi xen thuật” → nghe thành “descent thuộc”; “lặp” → nghe thành “lập” | — | ưu, thuật, lặp | lẫn vần/thanh ưu→yêu, thuật→thuộc, lặp→lập (đều gặp ở các bài trước); “gradient descent” khớp — cần người nghe |
| 15 | 0.867 | Xích ma thường là độ lệch chuẩn, giá trị kỳ dị, hoặc hàm sigmoid. | Sít ma thường là độ lệch chuẩn, giá trị kỳ dị hoặc hàm sít moi. | “xích” → nghe thành “sít”; “xích” → nghe thành “sít” | xích, xích | — | “xích” chép “sít”, xích-moi chép “sít moi” — nút thắt sigmoid PARTIAL |

## Đã xem xét (`asr_reviewed`, 2 mục)

- “Câu ba, tối ưu, tìm tham số bằng giải đóng, gradient descent, thuật toán lặp, hay không cần học.” — lẫn vần/thanh ưu→yêu, thuật→thuộc, lặp→lập (đều gặp ở các bài trước); “gradient descent” khớp — cần người nghe
- “Xích ma thường là độ lệch chuẩn, giá trị kỳ dị, hoặc hàm sigmoid.” — “xích” chép “sít”, xích-moi chép “sít moi” — nút thắt sigmoid PARTIAL

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
