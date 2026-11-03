# SEP L08 — tính lại bằng vòng lặp thuần (không dùng sum/min/max có sẵn) và liệt kê mọi thứ tự ưu tiên (khác `checks`).
from itertools import permutations


def total(v):
    t = 0
    for x in v:
        t += x
    return t


def smallest(v):
    m = v[0]
    for x in v[1:]:
        if x < m:
            m = x
    return m


def choose(opts, weak):
    """Luật ba bước: lọc nhỏ nhất ≥ 0 → tổng lớn nhất → điểm bên yếu thế lớn nhất (cột weak)."""
    keep = [k for k in opts if smallest(opts[k]) >= 0]
    best = None
    for k in keep:
        key = (total(opts[k]), opts[k][weak])
        if best is None or key > best[0]:
            best = (key, k)
    return best[1] if best else None


food = {"X": [2, 2, 2, -2], "Y": [1, 1, 1, 0], "Z": [0, 1, 1, 1]}
rec("L08a", [total(food[k]) for k in "XYZ"] == [4, 3, 3] and [smallest(food[k]) for k in "XYZ"] == [-2, 0, 0]
    and all(-2 <= x <= 2 for v in food.values() for x in v), "giao đồ ăn: tổng 4/3/3, nhỏ nhất −2/0/0, mọi điểm trong −2…2")
rec("L08b", choose(food, 3) == "Z" and max(food, key=lambda k: total(food[k])) == "X",
    "luật ba bước chọn Z; chỉ so tổng thì chọn X")
# đường kiểm: mọi thứ tự liệt kê phương án đều cho cùng kết quả (không phụ thuộc thứ tự đọc bảng)
rec("L08c", all(choose({k: food[k] for k in p}, 3) == "Z" for p in permutations("XYZ")),
    "liệt kê 6 thứ tự đọc bảng: luôn chọn Z")
rec("L08d", max(range(-2, 3)) * 3 + (-2) == 4, "thang −2…2 có một bên −2: tổng lớn nhất là 4 (giáo án ghi 5 là sai thang)")
food5 = {k: v + [d] for (k, v), d in zip(food.items(), (-1, 0, 0))}
rec("L08e", total(food5["X"]) == 3 and smallest(food5["X"]) == -2, "thêm người ở khu phố: X tổng 3, vẫn nhỏ nhất −2")
school = {"A": [2, 1, 2, -1], "B": [1, 1, 0, 1], "C": [0, 0, 1, 2], "D": [2, 2, 1, 0]}
no_d = {k: v for k, v in school.items() if k != "D"}
rec("L08f", [total(school[k]) for k in "ABCD"] == [4, 3, 3, 5] and choose(school, 3) == "D" and choose(no_d, 3) == "C"
    and all(choose({k: no_d[k] for k in p}, 3) == "C" for p in permutations("ABC")),
    "quiz: tổng 4/3/3/5; chọn D; bỏ D → C (mọi thứ tự)")
rec("L08g", 0.001 * 1000000 == 1000, "nhắc bài 5: 0,001 × 1 000 000 = 1000")
