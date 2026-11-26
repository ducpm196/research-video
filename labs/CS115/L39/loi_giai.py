import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
td_target = kv['r'] + kv['gamma'] * kv['max_qn']
td_err = td_target - kv['q']
q_new = kv['q'] + kv['alpha'] * td_err
print(f"target={td_target:.1f} td_err={td_err:.1f}")
print(f"q_new={q_new:.2f}")
