m = {'S':'Authentication','T':'Integrity','R':'NonRepudiation','I':'Confidentiality','D':'Availability','E':'Authorization'}
print(f'stride_unique_props={len(set(m.values()))}')
print(f'info_disclosure={m["I"]}')
print(f'tampering={m["T"]} spoofing={m["S"]}')
