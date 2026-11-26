# Lab BNK L12 — Đối soát sáu mã

Hai sổ (số tiền là số minh hoạ):
- ngân hàng: `a1=150, a2=250, a3=350, a4=450, a5=550, a6=650`
- chuyển mạch: `a1=150, a2=250, a3=300, a4=450, a7=700, a8=50`

Viết chương trình `doi_soat.py` (Python): dùng hai từ điển, phân loại bốn loại (khớp; lệch tiền; chỉ ngân hàng; chỉ chuyển mạch) rồi in đúng hai dòng:

```
khop <k> - lech tien <l> - chi ngan hang <nh> - chi chuyen mach <cm>
chenh tien: <hiệu>
```

(`chenh tien` = tổng tiền chuyển mạch trừ tổng tiền ngân hàng.) Mẹo in: `print("khop", k, "-", "lech tien", l)` in các giá trị cách nhau một dấu cách.

Chạy: `python doi_soat.py`. Chấm: `bash labs/cham.sh BNK L12 doi_soat.py`.
