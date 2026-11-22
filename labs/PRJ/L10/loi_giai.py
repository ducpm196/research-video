import hashlib
h = lambda b: hashlib.sha256(b.encode()).hexdigest()
def merkle(xs):
    hs = [h(x) for x in xs]
    return h(h(hs[0]+hs[1]) + h(hs[2]+hs[3]))
u = 3/10 + 5/20; x = 0.0
for _ in range(5): x += 0.5 * (10.0 - x)
r1 = merkle(['tx0','tx1','tx2','tx3']); r2 = merkle(['tx0','tx1','tx2*','tx3'])
print(f'rms_u={u:.2f} schedulable={int(u <= 2*(2**0.5-1))}')
print(f'pid_step5={x:.3f}')
print(f'merkle_tamper_detected={int(r1 != r2)}')
