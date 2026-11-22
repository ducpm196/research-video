from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, average_precision_score, brier_score_loss
X, y = make_classification(n_samples=600, weights=[0.95, 0.05], n_informative=4, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
p0 = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)
pb = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(class_weight='balanced', random_state=42))]).fit(X_tr, y_tr)
pr = pb.predict_proba(X_te)[:, 1]
print(f'balanced_recall_ge_raw={int(recall_score(y_te, pb.predict(X_te)) >= recall_score(y_te, p0.predict(X_te)))}')
print(f'balanced_pr_auc={average_precision_score(y_te, pr):.3f}')
print(f'balanced_brier={brier_score_loss(y_te, pr):.3f}')
