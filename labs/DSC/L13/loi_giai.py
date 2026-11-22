from collections import Counter
rows = [('12*', '25-34'), ('12*', '25-34'), ('12*', '25-34'),
        ('45*', '35-44'), ('45*', '35-44'), ('90*', '55+')]
min_k = min(Counter(rows).values())
print(f"min_k={min_k} is_2_anon={int(min_k >= 2)}")
