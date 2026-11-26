import sys
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    c_grid = [float(x) for x in kv["c_grid"].split(",")]
    X, y = make_classification(n_samples=int(kv["n_samples"]), n_features=int(kv["n_features"]), random_state=seed)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=float(kv["test_size"]), stratify=y, random_state=seed)
    pipe = Pipeline([("sc", StandardScaler()), ("clf", LogisticRegression(random_state=seed))])
    cv = StratifiedKFold(n_splits=int(kv["n_splits"]), shuffle=True, random_state=seed)
    gs = GridSearchCV(pipe, {"clf__C": c_grid}, cv=cv, scoring="f1").fit(X_tr, y_tr)
    cnts = [int(y_tr[te].sum()) for _, te in cv.split(X_tr, y_tr)]
    print(f"best_c={gs.best_params_['clf__C']}")
    print(f"cv_f1={gs.best_score_:.3f}")
    print(f"equal_folds_positive={int(len(set(cnts)) == 1)}")


if __name__ == "__main__":
    main()
