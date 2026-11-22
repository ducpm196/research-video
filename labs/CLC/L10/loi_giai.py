norm = 1800
cap2, cap3 = 2 * norm, 3 * (norm // 2)
head = 100.0 * (cap2 - norm) / norm
print(f'cap_2region={cap2}')
print(f'cap_3region={cap3}')
print(f'headroom_2region={head:.1f}%')
