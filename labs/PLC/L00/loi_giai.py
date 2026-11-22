def check_syntax(tokens):
    depth = 0
    for tk in tokens:
        if tk == '(': depth += 1
        elif tk == ')': depth -= 1
        if depth < 0: return False
    return depth == 0
def check_sem(env, var):
    return var in env
print(f"syn_err={int(not check_syntax(['(', '1', '+', '2']))} sem_err={int(not check_sem({'x': 1}, 'y'))}")
