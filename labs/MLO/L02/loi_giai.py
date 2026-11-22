import hashlib
h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
v1 = h("u101,1\nu102,0")
v2 = h("u101,1\nu102,1")
print(f"h1={v1} h2={v2} changed={int(v1 != v2)}")
