logs = [(1,3), (1,0), (1,2), (1,0), (1,0), (1,5), (1,1), (1,0)]
by_login = sum(1 for l, _ in logs if l > 0)
by_action = sum(1 for _, a in logs if a > 0)
print(f"active_login={by_login} active_action={by_action}")
