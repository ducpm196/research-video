# Rà soát E35 — phép kiểm có hai vế giống hệt nhau (2026-10-28)

Luật E35 (tools/lv.py `_tautology`, mức WARN) ra đời sau khi phát hiện hai check giả trong bản nháp OSY L03 và L07, nay đã sửa thành phép tính thật.
Quét lại mọi bài (`lessons/*/*.yaml`), OBSERVED: 7 cảnh báo, tất cả ở khoá đã xong.

| Bài | Đoạn bị báo | Đánh giá | Bằng chứng tính lại (2026-10-28) |
|---|---|---|---|
| CS115 L17 more_data | `Rational(301, 402) == Rational(301, 402)` | Check yếu (chép hằng); số trên màn hình ĐÚNG | `Rational(300 + 1, 400 + 2) == Rational(301, 402)` → True |
| CS115 L17 quiz | `Rational(7, 10) == Rational(7, 10)` | Check yếu; số ĐÚNG | MLE = k/n = 7/10; vế còn lại của cùng check đã giải đạo hàm bằng sympy |
| CS115 L18 pitfalls | `Rational(47, 30) == Rational(47, 30)` | Check yếu; số ĐÚNG | Σxy / Σx² = 47 / 30 với x = 1..4, y = 2, 3, 5, 6 → True |
| DMS L00 quiz | `1 == 1` | Có chủ đích: tạo giá trị “đúng” cho vế phải của phép kéo theo | — |
| DMS L01 sym_equiv | `((not p) or q) == ((not p) or q)` | Check trang trí; cảnh này không đưa con số hay khẳng định nào lên màn hình | — |
| DMS L07 props | `a <= a` | Có chủ đích: kiểm tính phản xạ | — |
| DMS L07 example | `a % 3 == a % 3` | Có chủ đích: kiểm tính phản xạ của đồng dư | — |

Quyết định: KHÔNG sửa các check này trong khoá đã xong. `spec_digest` gồm cả `checks`, nên sửa sẽ làm video đã kiểm thành STALE.
Không có số sai nào trên màn hình. Khi khoá nào cần dựng lại vì lý do khác, thay 3 check của CS115 bằng các biểu thức ở cột bằng chứng.
