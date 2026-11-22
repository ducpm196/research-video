policy = {
    'read_file': 'allow', 'email_ext': 'confirm',
    'pay_wire': 'confirm', 'exec_shell': 'deny',
}
actions = ['read_file', 'email_ext', 'pay_wire', 'exec_shell']
auto_run = [a for a in actions if policy.get(a) == 'allow']
print(f"auto_executed={auto_run} blocked={policy['exec_shell']}")
