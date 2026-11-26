# Lab MLP L12 — Xuất mô hình JSON an toàn & đối chiếu sai số suy luận thuần

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): huấn luyện `Pipeline` (`StandardScaler` + `LogisticRegression(random_state=42)`) trên `make_classification(n_samples=120, n_features=4, random_state=42)`, xuất `mean, scale, w, b` qua `json.loads(json.dumps(...))`, đối chiếu xác suất thuần `1/(1+exp(-z))` trên 5 mẫu đầu so với `predict_proba`, in đúng 3 dòng:
1. `json_keys_ok=1`
2. `match_lt_1e9=1`
3. `first_prob=...`

Chấm tự động:
```bash
bash labs/cham.sh MLP L12 duong_dan/bai_cua_ban.py
```
