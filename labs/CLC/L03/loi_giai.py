import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def ev(pol, act):
    hits = [e for e, a in pol if act in a or '*' in a]
    return 'DENY' if 'Deny' in hits else ('ALLOW' if 'Allow' in hits else 'DENY')
p_ro = [('Allow', {'s3:GetObject'})]; p_mix = [('Allow', {'*'}), ('Deny', {'ec2:TerminateInstances'})]
print(f'read_allow={ev(p_ro, kv["q1"])}\nterminate_deny={ev(p_mix, kv["q2"])}\nunmatched_default={ev(p_ro, kv["q3"])}')
