import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
decide = lambda vs: 'COMMIT' if all(v == 'YES' for v in vs.split(',')) else 'ABORT'
blk = int(kv['state'] == 'PREPARED' and int(kv['coord_up']) == 0)
print(f'all_yes_commit={int(decide(kv["votes1"]) == "COMMIT")}')
print(f'one_no_abort={int(decide(kv["votes2"]) == "ABORT")}')
print(f'prepared_blocked_on_coord_loss={blk}')
