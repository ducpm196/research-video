import sys
sys.path.insert(0, "D:/research-video/audit/bnx/deps/l23/venv/Lib/site-packages")
import numpy as np
from sklearn.ensemble import IsolationForest
for n_la in (10, 100, 1000):
    rng = np.random.default_rng(42)
    thuong = rng.normal(500, 50, n_la * 100)
    la = rng.normal(50_000, 2_000, n_la)
    X = np.concatenate([thuong, la]).reshape(-1, 1)
    mm = IsolationForest(n_estimators=100, contamination=0.01,
                         random_state=42).fit(X)
    p = mm.predict(X)
    nut = sum(t.tree_.node_count for t in mm.estimators_)
    print(len(X), "diem:", (p == -1).sum(), "bi gan -1,",
          (p[len(thuong):] == -1).sum(), "la that,", nut, "nut cua rung")