import sys
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    X, y = make_classification(
        n_samples=int(kv["n_samples"]),
        n_features=int(kv["n_features"]),
        n_informative=int(kv["n_informative"]),
        random_state=seed,
    )
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=float(kv["test_size"]), stratify=y, random_state=seed)
    dt = DecisionTreeClassifier(random_state=seed).fit(X_tr, y_tr)
    rf = RandomForestClassifier(
        n_estimators=int(kv["n_estimators"]),
        max_depth=int(kv["max_depth"]),
        random_state=seed,
    ).fit(X_tr, y_tr)
    print(f"dt_train_acc={dt.score(X_tr, y_tr):.3f}")
    print(f"rf_test_acc={rf.score(X_te, y_te):.3f}")
    print(f"importances_sum={rf.feature_importances_.sum():.2f}")


if __name__ == "__main__":
    main()
