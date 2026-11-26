import sys, json
s = sys.stdin.read().strip() or '["+", ["lit", "int"], ["*", ["lit", "int"], ["lit", "int"]]]|["-", ["lit", "int"], ["lit", "str"]]'
j1, j2 = s.split("|")
t_ok, t_err = json.loads(j1), json.loads(j2)
def check_tree(node):
    if node[0] == "lit": return node[1]
    _, a, b = node
    ta, tb = check_tree(a), check_tree(b)
    return "int" if (ta == "int" and tb == "int") else None
print(f"ok_expr={int(check_tree(t_ok) is not None)} err_expr={int(check_tree(t_err) is not None)}")
