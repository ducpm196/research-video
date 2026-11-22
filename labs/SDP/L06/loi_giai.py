class Rect:
    def set_w(self, w): self.w = w
    def set_h(self, h): self.h = h
    def area(self): return self.w * self.h
class Square(Rect):
    def set_w(self, w): self.w = self.h = w
    def set_h(self, h): self.w = self.h = h
def test_r(o): o.set_w(5); o.set_h(4); return o.area()
ra, sa = test_r(Rect()), test_r(Square())
print(f'rect_area={ra}')
print(f'square_area={sa}')
print(f'lsp_violated={int(sa != 20)}')
