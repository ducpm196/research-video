import sys
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


def parse_rows(spec: str) -> np.ndarray:
    rows = []
    for part in spec.split(";"):
        v_s, c_s = part.split(",")
        v = np.nan if v_s.lower() == "nan" else float(v_s)
        rows.append([v, c_s])
    return np.array(rows, dtype=object)


def main() -> None:
    kv = dict(line.strip().split("=", 1) for line in sys.stdin.read().splitlines() if "=" in line)
    X_tr = parse_rows(kv["train"])
    X_te = parse_rows(kv["test"])
    ct = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), [0]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), [1]),
    ])
    ct.fit(X_tr)
    out = ct.transform(X_te)
    med = float(ct.named_transformers_["num"].statistics_[0])
    print(f"train_median={med:.1f}")
    print(f"test_imputed_val={float(out[0, 0]):.1f}")
    print(f"unknown_ohe_sum={int(sum(out[0, 1:]))}")


if __name__ == "__main__":
    main()
