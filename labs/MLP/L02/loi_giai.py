import numpy as np
from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge, Lasso
X, y = make_regression(n_samples=150, n_features=12, n_informative=4, noise=2.0, random_state=42)
r10 = Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=10.0, random_state=42))]).fit(X, y)
r100 = Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=100.0, random_state=42))]).fit(X, y)
l2 = Pipeline([('sc', StandardScaler()), ('m', Lasso(alpha=2.0, random_state=42))]).fit(X, y)
rz = int(np.sum(np.abs(r10['m'].coef_) < 1e-6))
lz = int(np.sum(np.abs(l2['m'].coef_) < 1e-6))
sh = int(np.linalg.norm(r100['m'].coef_) < np.linalg.norm(r10['m'].coef_))
print(f'ridge_zero_coefs={rz}')
print(f'lasso_zero_coefs={lz}')
print(f'higher_alpha_shrinks={sh}')
