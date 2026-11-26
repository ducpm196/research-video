import sys
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    X, y = make_classification(n_samples=int(kv["n_samples"]), n_features=int(kv["n_features"]), random_state=seed)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=float(kv["test_size"]), stratify=y, random_state=seed)
    pipe = Pipeline([("sc", StandardScaler()), ("clf", LogisticRegression(random_state=seed))]).fit(X_tr, y_tr)
    p = pipe.predict_proba(X_te)[:, 1]
    r_hi = recall_score(y_te, (p >= float(kv["th_hi"])).astype(int))
    r_lo = recall_score(y_te, (p >= float(kv["th_lo"])).astype(int))
    print(f"r_at_50={r_hi:.3f}")
    print(f"r_at_30={r_lo:.3f}")
    print(f"recall_monotone_non_decreasing={int(r_lo >= r_hi)}")


if __name__ == "__main__":
    main()
