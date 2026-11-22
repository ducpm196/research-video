p1, p2 = 0, 0
p1 += 1; msg1 = p1
p2 += 1; p2 = max(p2, msg1) + 1; recv2 = p2
p2 += 1; p1 = max(p1, p2) + 1
print(f'p2_recv={recv2}')
print(f'p2_next={p2}')
print(f'p1_recv_back={p1}')
