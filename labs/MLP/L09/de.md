# Lab MLP L09 — Chuẩn hóa + PCA & KMeans đo phương sai và bất thường

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): trên `make_blobs(n_samples=300, centers=3, n_features=6, cluster_std=1.0, random_state=42)` sau `StandardScaler()`, chạy `PCA(n_components=2, random_state=42)` và `KMeans(n_clusters=3, n_init=10, random_state=42)` cùng kiểm điểm lệch `[50, 50]` vs `[0.05, 0]`, in đúng 3 dòng:
1. `pca_var_sum=...`
2. `kmeans_clusters=3`
3. `anomaly_further=1`

Chấm tự động:
```bash
bash labs/cham.sh MLP L09 duong_dan/bai_cua_ban.py
```
