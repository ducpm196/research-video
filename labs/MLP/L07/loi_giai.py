from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
X, y = make_classification(n_samples=600, n_features=12, n_informative=6, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
hgb = HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42).fit(X_tr, y_tr)
f = 0.0
for _ in range(3): f += 0.1 * (10.0 - f)
print(f'n_iter={hgb.n_iter_}')
print(f'hgb_test_acc={hgb.score(X_te, y_te):.3f}')
print(f'res_after_3={10.0 - f:.3f}')
