def check_tree(node):
    if node[0] == 'lit': return node[1]
    _, a, b = node
    ta, tb = check_tree(a), check_tree(b)
    return 'int' if (ta == 'int' and tb == 'int') else None
t_ok = ('+', ('lit', 'int'), ('*', ('lit', 'int'), ('lit', 'int')))
t_err = ('-', ('lit', 'int'), ('lit', 'str'))
print(f"ok_expr={int(check_tree(t_ok) is not None)} err_expr={int(check_tree(t_err) is not None)}")
