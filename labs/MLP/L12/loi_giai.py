import json
import math
import sys
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    check_n = int(kv["check_n"])
    X, y = make_classification(n_samples=int(kv["n_samples"]), n_features=int(kv["n_features"]), random_state=seed)
    pipe = Pipeline([("sc", StandardScaler()), ("clf", LogisticRegression(random_state=seed))]).fit(X, y)
    pkg = json.loads(json.dumps({
        "mean": pipe["sc"].mean_.tolist(),
        "scale": pipe["sc"].scale_.tolist(),
        "w": pipe["clf"].coef_[0].tolist(),
        "b": float(pipe["clf"].intercept_[0]),
    }))
    probs, diffs = [], []
    for row, ref in zip(X[:check_n], pipe.predict_proba(X[:check_n])[:, 1]):
        z = sum(((v - m) / s) * w for v, m, s, w in zip(row, pkg["mean"], pkg["scale"], pkg["w"])) + pkg["b"]
        p = 1.0 / (1.0 + math.exp(-z))
        probs.append(p)
        diffs.append(abs(p - float(ref)))
    print(f"json_keys_ok={int(set(pkg) == {'mean', 'scale', 'w', 'b'})}")
    print(f"match_lt_1e9={int(max(diffs) < 1e-9)}")
    print(f"first_prob={probs[0]:.6f}")


if __name__ == "__main__":
    main()
