from sklearn.datasets import make_classification
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score
X, y = make_classification(n_samples=1000, weights=[0.96, 0.04], n_informative=6, random_state=42)
X_tr, X_te, y_tr, y_te = X[:750], X[750:], y[:750], y[750:]
gb = HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42).fit(X_tr, y_tr)
p = gb.predict_proba(X_te)[:, 1]
pr = average_precision_score(y_te, p)
base = average_precision_score(y_te, [0.0] * len(y_te))
print(f'test_n={len(y_te)}')
print(f'gb_pr_auc={pr:.3f}')
print(f'beats_baseline={int(pr > base)}')
