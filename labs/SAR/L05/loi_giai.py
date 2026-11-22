import math
rf = 3
shards = math.ceil(8000 / 400)
nodes = shards * rf
print(f'shards_needed={shards}')
print(f'total_nodes_rf3={nodes}')
print(f'total_stored_tb={8 * rf}')
