def cookie_sent(ss, m, cross):
    if not cross: return 1
    if ss == 'None': return 1
    if ss == 'Lax': return int(m == 'GET')
    return 0
print(f'none_cross_post={cookie_sent("None", "POST", True)}')
print(f'lax_cross_post={cookie_sent("Lax", "POST", True)}')
print(f'strict_cross_post={cookie_sent("Strict", "POST", True)}')
