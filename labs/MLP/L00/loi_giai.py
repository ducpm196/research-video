import sys
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def parse_kv(text: str) -> dict[str, str]:
    kv = {}
    for line in text.splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v
    return kv


def main() -> None:
    kv = parse_kv(sys.stdin.read())
    n_samples = int(kv["n_samples"])
    n_features = int(kv["n_features"])
    test_size = float(kv["test_size"])
    seed = int(kv["seed"])
    tr_v = np.array([[float(x)] for x in kv["train_vals"].split(",")])
    te_v = np.array([[float(x)] for x in kv["test_vals"].split(",")])

    X, y = make_classification(n_samples=n_samples, n_features=n_features, random_state=seed)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=test_size, stratify=y, random_state=seed)
    pipe = Pipeline([("sc", StandardScaler()), ("clf", LogisticRegression(random_state=seed))]).fit(X_tr, y_tr)
    m_ok = StandardScaler().fit(tr_v).mean_[0]
    m_lk = StandardScaler().fit(np.vstack([tr_v, te_v])).mean_[0]
    print(f"clean_mean={m_ok:.2f}")
    print(f"leak_mean={m_lk:.2f}")
    print(f"pipe_test_acc={pipe.score(X_te, y_te):.3f}")


if __name__ == "__main__":
    main()
