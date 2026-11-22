def rfc6520_ok(claimed_n, rec_len):
    return claimed_n >= 0 and (1 + 2 + claimed_n + 16) <= rec_len
overread = 65535 - (20 - 3)
print(f"valid_ok={int(rfc6520_ok(4, 23))} hb_ok={int(rfc6520_ok(65535, 20))} hb_overread_B={overread}")
