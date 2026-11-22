def pick(n, kind):
    if kind == 'viz':
        return 'PCA/t-SNE'
    return 'Linear/Ridge' if n < 1000 else 'Tree/Boosting'
print("s1=", pick(500, 'tab'))
print("s2=", pick(100000, 'tab'))
print("s3=", pick(5000, 'viz'))
