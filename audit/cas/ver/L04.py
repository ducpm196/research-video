# CAS L04 — Mars Pathfinder. Đường KHÁC `checks` (alg.cas_inversion_sim, bước 1 ms): mô phỏng THEO SỰ KIỆN viết riêng ở đây
# (nhảy thẳng tới mốc sự kiện kế tiếp), đối chiếu với công thức r + M và với checklib.


def event_sim(r, M, inherit, t_block=2, need=1):
    """Thấp giữ khoá tới khi còn r ms lúc cao bị chặn (mốc t_block); vừa cần M ms, thức cùng lúc với cao. Trả về mốc cao xong."""
    t = t_block
    if inherit:                 # thấp mang ưu tiên cao: chạy nốt r, nhả khoá; cao chạy ngay
        t += r
    else:                       # vừa (ưu tiên 2) hơn thấp (1): vừa chạy hết M, rồi thấp chạy nốt r
        t += M + r
    return t + need


tasks = lambda m: [dict(name="thap", prio=1, release=0, steps=[("lock", 4)]), dict(name="cao", prio=3, release=2, steps=[("lock", 1)]),
                   dict(name="vua", prio=2, release=2, steps=[("cpu", m)])]
ok = all(event_sim(2, m, inh) == alg.cas_inversion_sim(tasks(m), inh)[0]["cao"] for m in range(0, 61) for inh in (False, True))
rec("L04a", ok, "mô phỏng sự kiện = mô phỏng từng ms (checklib) với mọi M từ 0 tới 60, có và không kế thừa")
rec("L04b", event_sim(2, 50, False) - 2 - 1 == 52 and event_sim(2, 50, True) - 2 - 1 == 2, "chờ: 2 + 50 = 52 ms; có kế thừa 2 ms (khớp CAS:L04)")
fin = [event_sim(2, m, False) - 2 for m in (5, 7, 8, 30)]
rec("L04c", fin == [8, 10, 11, 33] and all(event_sim(2, m, True) - 2 == 3 for m in (5, 7, 8, 30)), "xong sau 8 / 10 / 11 / 33 ms; có kế thừa luôn 3 ms")
rec("L04d", max(m for m in range(100) if event_sim(2, m, False) - 2 <= 10) == 7, "hạn 10 ms: không kế thừa chỉ chịu được M ≤ 7")
rec("L04e", event_sim(2, 20, False) - 2 == 23 and event_sim(2, 20, True) - 2 == 3, "quiz: M = 20 → 23 ms (trễ) / 3 ms")
rec("L04f", 1000 // 8 == 125 and 1 / 8 == 0.125, "8 Hz → chu kỳ 0,125 s = 125 ms")
