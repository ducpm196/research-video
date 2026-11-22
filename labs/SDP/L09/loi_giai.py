def size(node): return node if isinstance(node, int) else sum(size(c) for c in node)
sub = [50, 20]; root = [120, 30, sub]
milk = lambda c: c + 5; sugar = lambda c: c + 2
print(f'composite_folder_size={size(root)}')
print(f'sub_folder_size={size(sub)}')
print(f'decorated_coffee={sugar(milk(30))}')
