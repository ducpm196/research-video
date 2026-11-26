import json, math
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
X, y = make_classification(n_samples=120, n_features=4, random_state=42)
pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))]).fit(X, y)
pkg = json.loads(json.dumps({'mean': pipe['sc'].mean_.tolist(), 'scale': pipe['sc'].scale_.tolist(),
                             'w': pipe['clf'].coef_[0].tolist(), 'b': float(pipe['clf'].intercept_[0])}))
probs, diffs = [], []
for row, ref in zip(X[:5], pipe.predict_proba(X[:5])[:, 1]):
    z = sum(((v - m) / s) * w for v, m, s, w in zip(row, pkg['mean'], pkg['scale'], pkg['w'])) + pkg['b']
    p = 1.0 / (1.0 + math.exp(-z)); probs.append(p); diffs.append(abs(p - float(ref)))
print(f'json_keys_ok={int(set(pkg) == {"mean", "scale", "w", "b"})}')
print(f'match_lt_1e9={int(max(diffs) < 1e-9)}')
print(f'first_prob={probs[0]:.6f}')
