non_p = 2 + 10 * 2
pers = 2 + 10 * 1
print(f'http_nonpersistent_rtt={non_p}')
print(f'http_persistent_seq_rtt={pers}')
print(f'saved_rtt={non_p - pers}')
