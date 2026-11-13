# Lab FND L06 — Viết tay JSON, đọc YAML

Tạo `doc_ghi.sh`:

1. **Viết tay** tệp `don.json` bằng `cat > don.json <<'EOF' … EOF`: đơn `ma` 21, `khach` `Tran Mai`, `da_tra` `false` (viết thường), `hang` là mảng 3 phần tử, mỗi phần tử có `ten`, `sl`, `gia`: `ao` 4 × 90000, `non` 1 × 45000, `tat` 6 × 8000.
2. Tạo `doc.py` (chép nguyên; đọc JSON bằng Python, in số mặt hàng và tổng tiền) rồi chạy `python doc.py`:

```python
import json
d = json.load(open("don.json"))
hang = d["hang"]
tong = sum(h["sl"] * h["gia"] for h in hang)
print(len(hang), tong)
```

3. Đọc YAML dưới đây **bằng mắt**, rồi dùng `echo` in bốn số (mỗi số một dòng): (a) cổng của `may_chu`; (b) số tên miền trong `ten_mien`; (c) tổng hai cổng (`may_chu` + `co_so_du_lieu`); (d) `thu_lai`.

```yaml
may_chu:
  cong: 8080
  ten_mien: [a.vn, b.vn]
co_so_du_lieu:
  host: localhost
  cong: 5432
gioi_han:
  thu_lai: 3
```

Chạy `bash doc_ghi.sh`; chấm: `bash labs/cham.sh FND L06 doc_ghi.sh`. Cần Python theo bài đầu tiên. Dòng sai cú pháp JSON sẽ in lỗi (đọc dòng, cột) thay cho số.
