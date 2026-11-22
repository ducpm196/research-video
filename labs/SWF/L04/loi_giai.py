def tri(a, b, c):
    x, y, z = sorted((a, b, c))
    if x <= 0 or x + y <= z: return 'none'
    if x == z: return 'equilateral'
    return 'isosceles' if (x == y or y == z) else 'scalene'
print(f't333={tri(3,3,3)} t334={tri(3,3,4)}')
print(f't345={tri(3,4,5)}')
print(f'boundary_123={tri(1,2,3)}')
