import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
X, y = make_classification(n_samples=120, n_features=4, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))])
pipe.fit(X_tr, y_tr)
m_ok = StandardScaler().fit(np.array([[0.0], [2.0]])).mean_[0]
m_lk = StandardScaler().fit(np.array([[0.0], [2.0], [10.0]])).mean_[0]
print(f'clean_mean={m_ok:.2f}')
print(f'leak_mean={m_lk:.2f}')
print(f'pipe_test_acc={pipe.score(X_te, y_te):.3f}')
