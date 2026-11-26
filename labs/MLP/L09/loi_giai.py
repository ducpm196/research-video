import sys
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    centers = int(kv["centers"])
    X, _ = make_blobs(
        n_samples=int(kv["n_samples"]),
        centers=centers,
        n_features=int(kv["n_features"]),
        cluster_std=float(kv["cluster_std"]),
        random_state=seed,
    )
    Xs = StandardScaler().fit_transform(X)
    pca = PCA(n_components=int(kv["n_components"]), random_state=seed).fit(Xs)
    km = KMeans(n_clusters=centers, n_init=10, random_state=seed).fit(Xs)
    km2 = KMeans(n_clusters=2, n_init=10, random_state=seed).fit(
        np.array([[0.0, 0.0], [0.1, -0.1], [10.0, 10.0], [10.1, 9.9]])
    )
    pf = [float(x) for x in kv["probe_far"].split(",")]
    pn = [float(x) for x in kv["probe_near"].split(",")]
    far = int(km2.transform([pf]).min() > km2.transform([pn]).min())
    print(f"pca_var_sum={pca.explained_variance_ratio_.sum():.3f}")
    print(f"kmeans_clusters={len(set(km.labels_))}")
    print(f"anomaly_further={far}")


if __name__ == "__main__":
    main()
