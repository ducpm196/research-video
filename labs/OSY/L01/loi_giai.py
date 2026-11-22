procs = [1]
for _ in range(4): procs.append(procs[-1] * 2)
thread_addr_spaces = [100 for _ in range(4)]
print(f'procs_fork3={procs[3]}')
print(f'procs_fork4={procs[4]}')
print(f'shared_spaces_4threads={len(set(thread_addr_spaces))}')
