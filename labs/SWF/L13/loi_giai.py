import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
cpd = kv['per_min'] * 60 * 24
print(f'commits_per_day={cpd}')
print(f'edits_per_part={kv["edits"] / kv["modules"]:.2f}')
print(f'test_triggers_day={cpd * kv["tests_per_commit"]}')
