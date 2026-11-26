import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
class Rect:
    def set_w(self, w): self.w = w
    def set_h(self, h): self.h = h
    def area(self): return self.w * self.h
class Square(Rect):
    def set_w(self, w): self.w = self.h = w
    def set_h(self, h): self.w = self.h = h
def test_r(o, w, h): o.set_w(w); o.set_h(h); return o.area()
ra = test_r(Rect(), kv['w'], kv['h'])
sa = test_r(Square(), kv['w'], kv['h'])
print(f'rect_area={ra}')
print(f'square_area={sa}')
print(f'lsp_violated={int(sa != ra)}')
