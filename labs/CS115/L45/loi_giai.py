import math

ETA, BETA1, BETA2 = 0.001, 0.9, 0.999
LAM = 0.0001
W_A, W_B = 1.0, 1.0


def adam_cac_buoc(g, so_buoc):
    # gradient của hàm mất mát không đổi qua các bước; trả về độ dài mỗi bước và căn của s hiệu chỉnh
    m, s = 0.0, 0.0
    buoc, can_s = [], 0.0
    for k in range(1, so_buoc + 1):
        m = BETA1 * m + (1 - BETA1) * g
        s = BETA2 * s + (1 - BETA2) * g * g
        m_hc = m / (1 - BETA1 ** k)
        s_hc = s / (1 - BETA2 ** k)
        can_s = math.sqrt(s_hc)
        buoc.append(round(ETA * m_hc / can_s, 6))
    return buoc, can_s


buoc_a, can_a = adam_cac_buoc(10.0, 3)
buoc_b, can_b = adam_cac_buoc(0.1, 3)
print("buoc Adam A (g=10):", buoc_a)
print("buoc Adam B (g=0.1):", buoc_b)
print("can s A:", round(can_a, 4))
print("can s B:", round(can_b, 4))

l2_a = ETA * LAM * W_A / can_a
l2_b = ETA * LAM * W_B / can_b
tach_a = ETA * LAM * W_A
tach_b = ETA * LAM * W_B
print(f"phat L2 keo ve 0 A: {l2_a:.1e}")
print(f"phat L2 keo ve 0 B: {l2_b:.1e}")
print(f"tach roi keo ve 0 A: {tach_a:.1e}")
print(f"tach roi keo ve 0 B: {tach_b:.1e}")
print("ti so B chia A, phat L2:", round(l2_b / l2_a, 2))
print("ti so B chia A, tach roi:", round(tach_b / tach_a, 2))
