import sys
import numpy as np
from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge, Lasso


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    X, y = make_regression(
        n_samples=int(kv["n_samples"]),
        n_features=int(kv["n_features"]),
        n_informative=int(kv["n_informative"]),
        noise=float(kv["noise"]),
        random_state=seed,
    )
    rl = Pipeline([("sc", StandardScaler()), ("m", Ridge(alpha=float(kv["r_low"]), random_state=seed))]).fit(X, y)
    rh = Pipeline([("sc", StandardScaler()), ("m", Ridge(alpha=float(kv["r_high"]), random_state=seed))]).fit(X, y)
    las = Pipeline([("sc", StandardScaler()), ("m", Lasso(alpha=float(kv["lasso_alpha"]), random_state=seed))]).fit(X, y)
    rz = int(np.sum(np.abs(rl["m"].coef_) < 1e-6))
    lz = int(np.sum(np.abs(las["m"].coef_) < 1e-6))
    sh = int(np.linalg.norm(rh["m"].coef_) < np.linalg.norm(rl["m"].coef_))
    print(f"ridge_zero_coefs={rz}")
    print(f"lasso_zero_coefs={lz}")
    print(f"higher_alpha_shrinks={sh}")


if __name__ == "__main__":
    main()
