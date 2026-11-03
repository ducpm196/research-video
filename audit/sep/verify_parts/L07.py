# SEP L07 — tính lại bằng số thứ tự ngày trong năm và bảng số ngày mỗi tháng tự lập (khác `checks`: datetime + timedelta).
import calendar


def add_days(y, m, d, k):
    """Cộng k ngày bằng cách đi từng tháng, dùng calendar.monthrange (không dùng timedelta)."""
    while k > 0:
        dim = calendar.monthrange(y, m)[1]
        step = min(k, dim - d + 1)
        d += step
        k -= step
        if d > dim:
            d, m = 1, m + 1
            if m > 12:
                m, y = 1, y + 1
    return (d, m, y)


def disclose(v, H=90):
    """Ngày công bố theo 90+30: vá ở ngày v (None = chưa vá) với hạn H."""
    return v + 30 if v is not None and v <= H else H


rec("L07a", [disclose(47), disclose(83), disclose(None), disclose(5, H=7)] == [77, 113, 90, 35],
    "luật 90+30: vá 47 → 77; vá 83 → 113; không vá → 90; khai thác thật, vá ngày 5 → 35")
rec("L07b", add_days(2025, 1, 1, 90) == (1, 4, 2025) and add_days(2025, 1, 1, 47) == (17, 2, 2025)
    and add_days(2025, 1, 1, 77) == (19, 3, 2025) and add_days(2025, 1, 1, 7) == (8, 1, 2025),
    "báo 1/1/2025: hạn vá 1/4; vá 17/2; công bố 19/3; hạn 7 ngày 8/1")
doy = lambda y, m, d: sum(calendar.monthrange(y, k)[1] for k in range(1, m)) + d
rec("L07c", doy(2025, 3, 19) == 1 + 77 and doy(2025, 4, 1) == 1 + 90 and doy(2025, 3, 19) - doy(2025, 2, 17) == 30
    and 31 + 28 + 31 == 90, "đường kiểm số thứ tự ngày: 19/3 là ngày 78, 1/4 là ngày 91; 17/2 → 19/3 = 30 ngày")
rec("L07d", add_days(2024, 1, 1, 90) == (31, 3, 2024) and calendar.isleap(2024) and not calendar.isleap(2025),
    "năm nhuận: 1/1/2024 + 90 = 31/3/2024")
rec("L07e", add_days(2025, 3, 10, 90) == (8, 6, 2025) and add_days(2025, 3, 10, 20) == (30, 3, 2025)
    and add_days(2025, 3, 10, disclose(20)) == (29, 4, 2025) and add_days(2025, 3, 10, 7) == (17, 3, 2025)
    and (31 - 10 + 1) - 1 + 30 + 31 == 82, "quiz: báo 10/3 → hạn 8/6; vá 30/3 → công bố ngày 50 = 29/4; hạn 7 ngày 17/3")
rec("L07f", add_days(2014, 4, 3, 4) == (7, 4, 2014) and doy(2014, 4, 7) - doy(2014, 4, 3) == 4,
    "Heartbleed: tìm ra 3/4/2014, bản sửa 7/4/2014 → 4 ngày (heartbleed.com)")
