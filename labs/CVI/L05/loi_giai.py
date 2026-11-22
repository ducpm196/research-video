import math
ransac_n = lambda w, s=4, p=0.99: (
    math.ceil(math.log(1 - p) / math.log(1 - w ** s))
)
print(f"n_w60={ransac_n(0.6)} n_w40={ransac_n(0.4)}")
