import math

mu, var = 50, 64
sigma = math.sqrt(var)
print("sigma:", sigma)
print("z(58):", (58 - mu) / sigma)
print("z(34):", (34 - mu) / sigma)


def phi(z):
    return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)


def xap_xi(k):
    h = 2 / k
    return sum(phi(-1 + (i + 0.5) * h) * h for i in range(k))


print("xap xi 10 cot:", round(xap_xi(10), 4))
print("xap xi 100 cot:", round(xap_xi(100), 4))
print("chinh xac:", round(math.erf(1 / math.sqrt(2)), 4))
print("2 sigma:", round(math.erf(2 / math.sqrt(2)), 4))
md = 1 / (0.1 * math.sqrt(2 * math.pi))
print("mat do tai tam (sigma=0.1):", round(md, 4))
print("lon hon 1:", md > 1)
