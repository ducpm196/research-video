from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
X, y = make_classification(n_samples=300, n_features=8, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
gs = GridSearchCV(pipe, {'clf__C': [0.01, 0.1, 1.0, 10.0]}, cv=cv, scoring='f1').fit(X_tr, y_tr)
cnts = [int(y_tr[te].sum()) for _, te in cv.split(X_tr, y_tr)]
print(f'best_c={gs.best_params_["clf__C"]}')
print(f'cv_f1={gs.best_score_:.3f}')
print(f'equal_folds_positive={int(len(set(cnts)) == 1)}')
