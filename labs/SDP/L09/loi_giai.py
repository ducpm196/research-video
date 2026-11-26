import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def size(node): return node if isinstance(node, int) else sum(size(c) for c in node)
sub = [int(v) for v in kv['sub_files'].split(',')]
root = [int(v) for v in kv['root_files'].split(',')] + [sub]
cost = int(kv['base_coffee'])
for ex in kv['extras'].split(','):
    cost += int(ex)
print(f'composite_folder_size={size(root)}')
print(f'sub_folder_size={size(sub)}')
print(f'decorated_coffee={cost}')
