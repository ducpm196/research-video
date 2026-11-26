import sys
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    lr = float(kv["lr"])
    X, y = make_classification(
        n_samples=int(kv["n_samples"]),
        n_features=int(kv["n_features"]),
        n_informative=int(kv["n_informative"]),
        random_state=seed,
    )
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=float(kv["test_size"]), stratify=y, random_state=seed)
    hgb = HistGradientBoostingClassifier(
        max_iter=int(kv["max_iter"]),
        learning_rate=lr,
        random_state=seed,
    ).fit(X_tr, y_tr)
    f = 0.0
    tgt = float(kv["target"])
    for _ in range(int(kv["res_steps"])):
        f += lr * (tgt - f)
    print(f"n_iter={hgb.n_iter_}")
    print(f"hgb_test_acc={hgb.score(X_te, y_te):.3f}")
    print(f"res_after_3={tgt - f:.3f}")


if __name__ == "__main__":
    main()
