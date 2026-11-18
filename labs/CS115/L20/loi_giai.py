import math


def sigma(z):
    return 1 / (1 + math.exp(-z))


for z in (0, 2, -2):
    print(f"sigmoid({z}) = {round(sigma(z), 4)}")
yh = sigma(2)


def bce(y, yhat):
    return -(y * math.log(yhat) + (1 - y) * math.log(1 - yhat))


print("BCE nhan 1, du doan 0.8808:", round(bce(1, yh), 4))
print("BCE nhan 0, du doan 0.8808:", round(bce(0, yh), 4))
print(f"gradient yhat - y: nhan 1: {round(yh - 1, 4)}, nhan 0: {round(yh - 0, 4)}")


def softmax(z):
    m = max(z)
    e = [math.exp(t - m) for t in z]
    s = sum(e)
    return [round(t / s, 4) for t in e]


print("softmax [2, 1, 0]:", softmax([2, 1, 0]))
print("softmax [1000, 1001] on dinh:", softmax([1000, 1001]))
