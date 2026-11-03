# PAR L05 — tính lại bằng cách KHÁC checks của bài: mô phỏng bộ nhớ đệm riêng của từng lõi với trạng thái M / S / I (kiểu MESI rút gọn,
# theo ghi chú khoá học Cambridge: ghi vào dòng đang chia sẻ thì huỷ mọi bản sao khác), đếm số lần một lõi phải lấy quyền ghi; dòng tính
# bằng dịch bit (a >> 6) chứ không chia; đếm cặp luồng chung dòng bằng liệt kê.


def mesi_writes(addrs, rounds, line_shift=6):
    caches = [dict() for _ in addrs]  # lõi → {dòng: 'M' hoặc 'S'}
    upgrades = invalidations = 0
    for _ in range(rounds):
        for core, a in enumerate(addrs):
            ln = a >> line_shift
            if caches[core].get(ln) != "M":
                upgrades += 1                      # phải lấy quyền ghi (kéo dòng / huỷ bản sao khác)
                for other in range(len(addrs)):
                    if other != core and ln in caches[other]:
                        del caches[other][ln]; invalidations += 1
                caches[core][ln] = "M"
    return upgrades, invalidations


u8, i8 = mesi_writes([8 * i for i in range(8)], 1000)
u64, i64 = mesi_writes([64 * i for i in range(8)], 1000)
u32, _ = mesi_writes([32 * i for i in range(8)], 1000)
rec("L05a", (u8, u64, u32) == (8000, 8, 8000) and i64 == 0 and i8 == 7999
    and (u8, u64, u32) == tuple(alg.par_line_transfers([s * i for i in range(8)], 1000)[0] for s in (8, 64, 32)),
    "M/S/I: ghép sát 8000 lần lấy quyền ghi (7999 lần huỷ), đệm 64 byte 8 lần (0 huỷ), đệm 32 byte vẫn 8000")
rec("L05b", mesi_writes([0, 8], 3)[0] == 6 and mesi_writes([0, 64], 3)[0] == 2,
    "làm thử 2 luồng × 3 lần: sát nhau 6, đệm 2")
rec("L05c", [a >> 6 for a in (0, 56, 64, 130, 448)] == [0, 0, 1, 2, 7] and divmod(130, 64) == (2, 2)
    and {a >> 6 for a in range(0, 64, 8)} == {0} and sorted({(32 * i) >> 6 for i in range(8)}) == [0, 1, 2, 3],
    "dòng bằng dịch 6 bit: 0, 0, 1, 2, 7; 130 = 2 · 64 + 2; 8 bộ đếm sát nhau cùng dòng 0; đệm 32 byte dùng 4 dòng")
pairs = sum(1 for i in range(8) for j in range(i + 1, 8) if (8 * i) >> 6 == (8 * j) >> 6)
pairs64 = sum(1 for i in range(8) for j in range(i + 1, 8) if (64 * i) >> 6 == (64 * j) >> 6)
rec("L05d", pairs == 28 and pairs64 == 0 and 8 * 8 == 64 and 8 * 64 == 512, "28 cặp giẫm chân nhau / 0 cặp; 64 so với 512 byte")
u16, _ = mesi_writes([4 * i for i in range(16)], 1000)
u16p, _ = mesi_writes([64 * i for i in range(16)], 1000)
ulocal, _ = mesi_writes([4 * i for i in range(16)], 1)
rec("L05e", (u16, u16p, ulocal) == (16000, 16, 16) and 64 // 4 == 16 and 16 * 64 == 1024 and 16 * 4 == 64,
    "quiz: 16 000 / 16 / 16 lần (cục bộ ghi một lần); 1024 so với 64 byte")
rec("L05f", 10 ** 6 * 8 == 8 * 10 ** 6 and 10 ** 6 * 64 // (10 ** 6 * 8) == 8, "lỗi 4: 1 triệu bộ đếm 8 MB so với 64 MB, gấp 8")
