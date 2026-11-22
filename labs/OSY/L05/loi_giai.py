empty, full = 5, 0
print(f'init_empty={empty} init_full={full}')
for _ in range(4): empty -= 1; full += 1
empty += 1; full -= 1
print(f'after_4p_1c=empty:{empty},full:{full}')
for _ in range(2): empty -= 1; full += 1
print(f'final_state=empty:{empty},full:{full}')
