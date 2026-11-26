import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
wf = (kv['wf_p'] ** int(kv['wf_n'])) * 100; ag = (kv['ag_p'] ** int(kv['ag_n'])) * 100
print(f'fixed_workflow={wf:.1f}% autonomous_agent={ag:.1f}%')
