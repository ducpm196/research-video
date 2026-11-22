import math
docs = {1: 'may chu nhanh', 2: 'du lieu lon', 3: 'tim nhanh du lieu'}
postings = sorted(i for i, t in docs.items() if 'nhanh' in t.split())
avgdl = sum(len(t.split()) for t in docs.values()) / len(docs)
N, df, dl = len(docs), len(postings), len(docs[1].split())
idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
tf = docs[1].split().count('nhanh')
score = idf * (tf * 2.2) / (tf + 1.2 * (1 - 0.75 + 0.75 * dl / avgdl))
print(f'docs_with_nhanh={postings}')
print(f'bm25_doc1={score:.4f}')
