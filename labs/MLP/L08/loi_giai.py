import sys
import numpy as np
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    X, y = make_circles(
        n_samples=int(kv["n_samples"]),
        factor=float(kv["factor"]),
        noise=float(kv["noise"]),
        random_state=seed,
    )
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=float(kv["test_size"]), stratify=y, random_state=seed)
    lin = Pipeline([("sc", StandardScaler()), ("c", LogisticRegression(random_state=seed))]).fit(X_tr, y_tr)
    poly = Pipeline([
        ("pf", PolynomialFeatures(degree=int(kv["degree"]), include_bias=False)),
        ("sc", StandardScaler()),
        ("c", LogisticRegression(random_state=seed)),
    ]).fit(X_tr, y_tr)
    ok = all(tr.max() < te.min() for tr, te in TimeSeriesSplit(n_splits=int(kv["ts_splits"])).split(np.arange(int(kv["ts_len"]))))
    print(f"linear_acc={lin.score(X_te, y_te):.3f}")
    print(f"poly2_acc={poly.score(X_te, y_te):.3f}")
    print(f"strict_causal_splits={int(ok)}")


if __name__ == "__main__":
    main()
