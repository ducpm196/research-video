D = range(20)

x1 = [x for x in D if not x * x > x]
print('1: sai, phan vi du x=' + str(x1[0]) if x1 else '1: dung')
x2 = [x for x in D if x * x == 2 * x + 3]
print('2: dung, vi du x=' + str(x2[0]) if x2 else '2: sai')
print('3:', 'dung' if all(any(x + y == 19 for y in D) for x in D) else 'sai')
print('4:', 'dung' if any(all(x + y == 19 for x in D) for y in D) else 'sai')
x5 = [x for x in D if not any(y > x for y in D)]
print('5: sai, phan vi du x=' + str(x5[0]) if x5 else '5: dung')
