alloc = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
mx = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
need = [[mx[i][j]-alloc[i][j] for j in range(3)] for i in range(5)]
work = [3,3,2]; fin = [False]*5; seq = []
while len(seq) < 5:
    for i in range(5):
        if not fin[i] and all(need[i][j] <= work[j] for j in range(3)):
            work = [work[j]+alloc[i][j] for j in range(3)]; fin[i] = True; seq.append(f'P{i}'); break
print(f'safe={int(all(fin))}')
print('safe_seq=' + ','.join(seq))
print('final_avail=' + ','.join(map(str, work)))
