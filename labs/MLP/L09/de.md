# Lab MLP L09 — Chuẩn hóa + PCA & KMeans đo phương sai và bất thường

Đọc từ `stdin`:
`n_samples=<int> centers=<int> n_features=<int> cluster_std=<float> seed=<int> n_components=<int> probe_far=<x,y> probe_near=<x,y>`

Yêu cầu: trên `make_blobs(..., random_state=seed)` sau `StandardScaler()`, chạy `PCA(n_components=n_components, random_state=seed)` và `KMeans(n_clusters=centers, n_init=10, random_state=seed)`, cùng kiểm khoảng cách tới tâm `KMeans(n_clusters=2, n_init=10, random_state=seed)` khớp trên `[[0,0],[0.1,-0.1],[10,10],[10.1,9.9]]` cho `probe_far` vs `probe_near`.

In đúng 3 dòng: `pca_var_sum=<.3f>`, `kmeans_clusters=<int>`, `anomaly_further=<0_hoặc_1>`.
Chấm tự động: `bash labs/cham.sh MLP L09 duong_dan/bai_cua_ban.py`
