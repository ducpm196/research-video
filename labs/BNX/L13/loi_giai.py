tot = [("FROM", [], 5), ("WORKDIR", [], 1), ("COPY pom.xml", ["pom.xml"], 1),
       ("RUN tai phu thuoc", [], 80),
       ("COPY src", ["src/Dao.java", "src/Main.java"], 2), ("RUN dong goi", [], 25)]
xau = [("FROM", [], 5),
       ("COPY . .", ["pom.xml", "src/Dao.java", "src/Main.java"], 3),
       ("RUN tai va dong goi", [], 105)]


def dung_lai(lop, sua):
    for i, (ten, dau_vao, giay) in enumerate(lop):
        if sua in dau_vao:
            return list(range(i + 1, len(lop) + 1)), sum(l[2] for l in lop[i:])
    return [], 0


def so_dot(D, mu, ms):
    san, dot = 0, 0
    while san < D:
        san += min(mu + ms, D - san)
        dot += 1
    return dot


for sua in ("src/Dao.java", "pom.xml"):
    cac, giay = dung_lai(tot, sua)
    print("sua", sua + ":", "lop", *cac, "-", giay, "giay")
print("sai thu tu, sua src/Dao.java:", dung_lai(xau, "src/Dao.java")[1], "giay")
D, mu, ms = 12, 1, 2
print(f"D={D} thieu {mu} thua {ms}:", so_dot(D, mu, ms), "dot, toi thieu", D - mu, "toi da", D + ms)
D = 10
mu, ms = D // 4, -(-D // 4)
print(f"D={D} 25%/25%:", so_dot(D, mu, ms), "dot, toi thieu", D - mu, "toi da", D + ms)
