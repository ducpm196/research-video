import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
class Rect:
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
class Circle:
    def __init__(self, r): self.r = r
    def area(self): return math.pi * self.r * self.r
class Tri:
    def __init__(self, b, h): self.b, self.h = b, h
    def area(self): return 0.5 * self.b * self.h
shapes = [Rect(kv['rw'], kv['rh']), Circle(kv['cr']), Tri(kv['tb'], kv['th'])]
print(f'rect_tri_sum={shapes[0].area() + shapes[2].area():.2f}')
print(f'circle_area={shapes[1].area():.2f}')
print(f'total_area={sum(s.area() for s in shapes):.2f}')
