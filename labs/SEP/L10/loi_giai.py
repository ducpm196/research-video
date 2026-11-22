rev = {'leftpad': ['tpl', 'cli'], 'tpl': ['web'], 'web': ['app'], 'cli': ['app'], 'app': []}
broken = set(); stack = list(rev['leftpad'])
while stack:
    p = stack.pop()
    if p not in broken:
        broken.add(p); stack.extend(rev.get(p, []))
print(f"broken_upstream={len(broken)} pkgs={sorted(broken)}")
