# Lab EVT L10 — Độ trễ đầu–cuối qua đồ thị vết phụ thuộc (DAG)

Trong một đồ thị phụ thuộc (`DAG`): bước `A` (`15 ms`) rẽ thành hai nhánh song song `B` (`30 ms`) và `C` (`70 ms`), cuối cùng bước `D` (`25 ms`) chờ cả hai xong. Tính tổng độ trễ nếu chạy tuần tự cả 4 bước so với đường găng song song.

Định dạng đầu ra (2 dòng):
`seq_ms=<số nguyên>`
`critical_ms=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh EVT L10 duong_dan/bai_cua_ban.py
```
