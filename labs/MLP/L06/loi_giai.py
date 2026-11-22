from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
X, y = make_classification(n_samples=400, n_features=12, n_informative=4, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
dt = DecisionTreeClassifier(random_state=42).fit(X_tr, y_tr)
rf = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42).fit(X_tr, y_tr)
print(f'dt_train_acc={dt.score(X_tr, y_tr):.3f}')
print(f'rf_test_acc={rf.score(X_te, y_te):.3f}')
print(f'importances_sum={rf.feature_importances_.sum():.2f}')
