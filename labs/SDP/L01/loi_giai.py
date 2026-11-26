import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def naive(s):
    val, found = 0, False
    for ch in s:
        if '0' <= ch <= '9':
            val = val * 10 + (ord(ch) - ord('0'))
            found = True
        else:
            break
    return val if found else 0
def strict(s): return int(s)
raised = 0
try:
    strict(kv['bad'])
except ValueError:
    raised = 1
print(f'naive_12a={naive(kv["bad"])}')
print(f'strict_42={strict(kv["good"])}')
print(f'strict_12a_raised={raised}')
