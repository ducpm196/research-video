def fold(node):
    if not isinstance(node, tuple): return node
    op, a, b = node[0], fold(node[1]), fold(node[2])
    if isinstance(a, int) and isinstance(b, int):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '//' and b != 0: return a // b
    return (op, a, b)
print(f"folded={fold(('+', ('*', 3, 6), 'y'))}")
