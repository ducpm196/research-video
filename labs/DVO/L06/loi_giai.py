import re
hist = ['API_KEY=sk_live_987654', 'API_KEY=env_only', 'PORT=8080']
pat = re.compile(r'sk_live_[0-9a-zA-Z]+')
leaks = sum(bool(pat.search(c)) for c in hist)
head = int(bool(pat.search(hist[-1])))
print(f'head_has_secret={head}')
print(f'history_leaked_commits={leaks}')
print(f'rotation_required={int(leaks > 0)}')
