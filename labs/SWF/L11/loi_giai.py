def m3(base, a, b):
    if a == b or b == base: return a
    if a == base: return b
    return 'CONFLICT'
print(f'merge_1_2_1={m3(1,2,1)}')
print(f'merge_1_3_3={m3(1,3,3)}')
print(f'merge_1_2_3={m3(1,2,3)}')
