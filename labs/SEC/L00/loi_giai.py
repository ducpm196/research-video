import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
m = {'S': 'Authentication', 'T': 'Integrity', 'R': 'NonRepudiation', 'I': 'Confidentiality', 'D': 'Availability', 'E': 'Authorization'}
print(f'stride_unique_props={len(set(m.values()))}')
print(f'info_disclosure={m[kv["q1"]]}')
print(f'tampering={m[kv["q2"]]} spoofing={m[kv["q3"]]}')
