# Lab MLP L01 — ColumnTransformer điền khuyết trung vị & mã hóa bỏ qua nhãn lạ

Đọc từ `stdin`:
- Dòng 1: `train=<val,cat;val,cat;...>` (giá trị số hoặc `nan`)
- Dòng 2: `test=<val,cat>`

Yêu cầu: dùng `ColumnTransformer` với `SimpleImputer(strategy='median')` cho cột `[0]` và `OneHotEncoder(handle_unknown='ignore')` cho cột `[1]`. Khớp trên `train` và biến đổi `test`, in đúng 3 dòng:
```
train_median=<.1f>
test_imputed_val=<.1f>
unknown_ohe_sum=<int>
```

Chấm tự động: `bash labs/cham.sh MLP L01 duong_dan/bai_cua_ban.py`
