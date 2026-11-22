import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
X_tr = np.array([[10.0, 'hn'], [20.0, 'sg'], [30.0, 'hn'], [np.nan, 'sg']], dtype=object)
X_te = np.array([[np.nan, 'dn']], dtype=object)
ct = ColumnTransformer([('num', SimpleImputer(strategy='median'), [0]),
                        ('cat', OneHotEncoder(handle_unknown='ignore'), [1])])
ct.fit(X_tr); out = ct.transform(X_te)
med = ct.named_transformers_['num'].statistics_[0]
print(f'train_median={med:.1f}')
print(f'test_imputed_val={float(out[0, 0]):.1f}')
print(f'unknown_ohe_sum={int(sum(out[0, 1:]))}')
