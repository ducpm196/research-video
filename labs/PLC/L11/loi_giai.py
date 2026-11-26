import sys, json
s = sys.stdin.read().strip() or '["+", ["*", 3, 6], "y"]'
node_in = json.loads(s)
to_t = lambda v: tuple(to_t(x) for x in v) if isinstance(v, list) else v
def fold(node):
    if not isinstance(node, tuple): return node
    op, a, b = node[0], fold(node[1]), fold(node[2])
    if isinstance(a, int) and isinstance(b, int):
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "//" and b != 0: return a // b
    return (op, a, b)
print(f"folded={fold(to_t(node_in))}")
