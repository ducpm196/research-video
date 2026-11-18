def dem(n):
    chay_than = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            chay_than += 1
    so_sanh = chay_than + n  # mỗi giá trị i có thêm 1 lần so sánh cho kết quả sai để thoát
    return chay_than, so_sanh


for n in (8, 20):
    chay_than, so_sanh = dem(n)
    print(f"n = {n} so lan chay than: {chay_than}")
    print(f"n = {n} so lan so sanh: {so_sanh}")
print("cong thuc n(n+1)/2 voi n = 20:", 20 * 21 // 2)
