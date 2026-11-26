import numpy as np
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
X, y = make_circles(n_samples=300, factor=0.4, noise=0.05, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
lin = Pipeline([('sc', StandardScaler()), ('c', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)
poly = Pipeline([('pf', PolynomialFeatures(degree=2, include_bias=False)), ('sc', StandardScaler()), ('c', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)
ok = all(tr.max() < te.min() for tr, te in TimeSeriesSplit(n_splits=4).split(np.arange(100)))
print(f'linear_acc={lin.score(X_te, y_te):.3f}')
print(f'poly2_acc={poly.score(X_te, y_te):.3f}')
print(f'strict_causal_splits={int(ok)}')
