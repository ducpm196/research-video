layers = ['FROM py', 'COPY req.txt', 'RUN pip install', 'COPY src']
hits = lambda ch: layers.index(ch)
print(f'hits_src_change={hits("COPY src")}')
print(f'hits_req_change={hits("COPY req.txt")}')
