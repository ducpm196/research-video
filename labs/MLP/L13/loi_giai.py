import sys
from sklearn.datasets import make_classification
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    train_n = int(kv["train_n"])
    X, y = make_classification(
        n_samples=int(kv["n_samples"]),
        weights=[float(kv["w_neg"]), float(kv["w_pos"])],
        n_informative=int(kv["n_informative"]),
        random_state=seed,
    )
    X_tr, X_te, y_tr, y_te = X[:train_n], X[train_n:], y[:train_n], y[train_n:]
    gb = HistGradientBoostingClassifier(
        max_iter=int(kv["max_iter"]),
        learning_rate=float(kv["lr"]),
        random_state=seed,
    ).fit(X_tr, y_tr)
    p = gb.predict_proba(X_te)[:, 1]
    pr = average_precision_score(y_te, p)
    base = average_precision_score(y_te, [0.0] * len(y_te))
    print(f"test_n={len(y_te)}")
    print(f"gb_pr_auc={pr:.3f}")
    print(f"beats_baseline={int(pr > base)}")


if __name__ == "__main__":
    main()
