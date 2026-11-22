import numpy as np
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
X, _ = make_blobs(n_samples=300, centers=3, n_features=6, cluster_std=1.0, random_state=42)
Xs = StandardScaler().fit_transform(X)
pca = PCA(n_components=2, random_state=42).fit(Xs)
km3 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(Xs)
km2 = KMeans(n_clusters=2, n_init=10, random_state=42).fit(np.array([[0.0,0.0],[0.1,-0.1],[10.0,10.0],[10.1,9.9]]))
far = int(km2.transform([[50.0, 50.0]]).min() > km2.transform([[0.05, 0.0]]).min())
print(f'pca_var_sum={pca.explained_variance_ratio_.sum():.3f}')
print(f'kmeans_clusters={len(set(km3.labels_))}')
print(f'anomaly_further={far}')
