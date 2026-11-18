LOI_KIEM_TRA = {"IOException", "SQLException", "Exception"}   # kiểm tra: phải khai hoặc bắt
LOI_KHONG_KIEM_TRA = {"IllegalArgumentException", "RuntimeException", "NullPointerException"}


def hoan_tac(loi, rollback_for=()):
    if loi is None:
        return False
    if loi == "Error":
        return True
    if loi in LOI_KHONG_KIEM_TRA:
        return True
    return loi in rollback_for or ("Exception" in rollback_for and loi in LOI_KIEM_TRA)


CAC_CA = [
    ("IllegalArgumentException", ()),
    ("IOException", ()),
    ("IOException", ("Exception",)),
    ("Error", ()),
    (None, ()),
]
for loi, khai in CAC_CA:
    print(f"{loi or 'khong loi'} + {','.join(khai) or 'khong khai'}: {'hoan tac' if hoan_tac(loi, khai) else 'chot'}")
