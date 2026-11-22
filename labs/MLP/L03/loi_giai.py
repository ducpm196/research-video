from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
X, y = make_classification(n_samples=240, n_features=6, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)
p = pipe.predict_proba(X_te)[:, 1]
r50 = recall_score(y_te, (p >= 0.50).astype(int))
r30 = recall_score(y_te, (p >= 0.30).astype(int))
print(f'r_at_50={r50:.3f}')
print(f'r_at_30={r30:.3f}')
print(f'recall_monotone_non_decreasing={int(r30 >= r50)}')
