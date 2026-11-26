import sys
n = int(sys.stdin.read().split('=')[1])
print(f'mesh_channels={n * (n - 1)} hub_channels={2 * (n - 1)}')
