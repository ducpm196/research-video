import math, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
sh = math.ceil((kv['tb'] * 1000) / kv['max_node_gb'])
print(f'shards_needed={sh}\ntotal_nodes_rf3={sh * kv["rf"]}\ntotal_stored_tb={kv["tb"] * kv["rf"]}')
