big_gb, sm_gb, nodes = 800, 2, 50
bc = (nodes - 1) * sm_gb
sh = (big_gb + sm_gb) * (nodes - 1) / nodes
print(f'broadcast_gb={bc}')
print(f'shuffle_gb={sh:.2f}')
print(f'network_saved_pct={100 * (sh - bc) / sh:.1f}%')
