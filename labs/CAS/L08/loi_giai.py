import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
hours = (float(kv['gb']) * 8000.0) / float(kv['mbps']) / 3600.0
print(f'aborted={int(kv["host"] != kv["target"])} restore_hours={hours:.2f}')
