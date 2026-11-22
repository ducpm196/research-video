from pathlib import Path

p = Path("audit/s9_11/up_s10.py")
txt = p.read_text(encoding="utf-8")

repls = [
    # 1. COVERS fixes across TOC, PLC, PAR, HCI, SEP, CAS
    (
        '''    # TOC (L00..L14)
    "TOC:L00": [(1, "sym"), (2, "lang"), (3, "example")],
    "TOC:L01": [(1, "example"), (2, "example"), (3, "verify")],
    "TOC:L02": [(1, "example"), (2, "example"), (3, "pitfalls")],
    "TOC:L03": [(1, "example"), (2, "prec"), (3, "kleene")],
    "TOC:L04": [(1, "why"), (2, "example"), (3, "pitfalls")],
    "TOC:L05": [(1, "algo"), (2, "example"), (3, "unique")],
    "TOC:L06": [(1, "example"), (2, "example"), (3, "sym")],
    "TOC:L07": [(1, "trees"), (2, "example"), (3, "pitfalls")],
    "TOC:L08": [(1, "machine"), (2, "example"), (3, "equiv")],
    "TOC:L09": [(1, "design"), (2, "example"), (3, "pitfalls")],
    "TOC:L10": [(1, "evidence"), (2, "universal"), (3, "pitfalls")],
    "TOC:L11": [(1, "intuition"), (2, "proof"), (3, "pitfalls")],
    "TOC:L12": [(1, "example"), (2, "rice"), (3, "classify")],
    "TOC:L13": [(1, "sym"), (2, "equiv"), (3, "picture")],
    "TOC:L14": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5")],

    # PLC (L00..L13)
    "PLC:L00": [(1, "sym"), (2, "example"), (3, "impl")],
    "PLC:L01": [(1, "sym"), (2, "example"), (3, "automaton")],
    "PLC:L02": [(1, "example"), (2, "code"), (3, "pitfalls")],
    "PLC:L03": [(1, "sym"), (2, "assoc"), (3, "example")],
    "PLC:L04": [(1, "sym"), (2, "example"), (3, "late")],
    "PLC:L05": [(1, "example"), (2, "sym"), (3, "tradeoff")],
    "PLC:L06": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L07": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L08": [(1, "sym"), (2, "methods"), (3, "pitfalls")],
    "PLC:L09": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L10": [(1, "gen"), (2, "example"), (3, "pitfalls")],
    "PLC:L11": [(1, "limit"), (2, "example"), (3, "pitfalls")],
    "PLC:L12": [(1, "example"), (2, "sharing"), (3, "pitfalls")],
    "PLC:L13": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5")],

    # PAR (L00..L13)
    "PAR:L00": [(1, "example"), (2, "measure"), (3, "quiz")],
    "PAR:L01": [(1, "sym"), (2, "example"), (3, "measure")],
    "PAR:L02": [(1, "example"), (2, "formula"), (3, "pitfalls")],
    "PAR:L03": [(1, "intuition"), (2, "example"), (3, "example")],
    "PAR:L04": [(1, "example"), (2, "check"), (3, "example")],
    "PAR:L05": [(1, "example"), (2, "example"), (3, "check")],
    "PAR:L06": [(1, "example"), (2, "formula"), (3, "check")],
    "PAR:L07": [(1, "example"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L08": [(1, "example"), (2, "example"), (3, "check"), (4, "check")],
    "PAR:L09": [(1, "example"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L10": [(1, "check"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L11": [(1, "formula"), (2, "example"), (3, "check"), (4, "quiz")],
    "PAR:L12": [(1, "example"), (2, "example"), (3, "check"), (4, "quiz")],
    "PAR:L13": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5")],

    # HCI (L00..L12)
    "HCI:L00": [(1, "sym"), (2, "concept"), (3, "example")],
    "HCI:L01": [(1, "example"), (2, "example"), (3, "pitfalls")],
    "HCI:L02": [(1, "example"), (2, "formula"), (3, "check")],
    "HCI:L03": [(1, "formula"), (2, "example"), (3, "check")],
    "HCI:L04": [(1, "sym"), (2, "formula"), (3, "pitfalls")],
    "HCI:L05": [(1, "formula"), (2, "example"), (3, "pitfalls")],
    "HCI:L06": [(1, "formula"), (2, "example"), (3, "check"), (4, "pitfalls")],
    "HCI:L07": [(1, "example"), (2, "formula"), (3, "pitfalls")],
    "HCI:L08": [(1, "example"), (2, "concept"), (3, "check")],
    "HCI:L09": [(1, "example"), (2, "check"), (3, "concept"), (4, "example")],
    "HCI:L10": [(1, "concept"), (2, "example"), (3, "pitfalls")],
    "HCI:L11": [(1, "example"), (2, "pitfalls"), (3, "check"), (4, "pitfalls")],
    "HCI:L12": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (2, "check"), (3, "stage4")],

    # SEP (L00..L11)
    "SEP:L00": [(1, "sym"), (2, "example"), (3, "formula"), (4, "pitfalls")],
    "SEP:L01": [(1, "example"), (2, "check"), (3, "law"), (4, "pitfalls")],
    "SEP:L02": [(1, "formula"), (2, "check"), (3, "example"), (4, "check")],
    "SEP:L03": [(1, "example"), (2, "check"), (3, "pitfalls"), (4, "log")],
    "SEP:L04": [(1, "sym"), (2, "example"), (3, "check"), (4, "pitfalls")],
    "SEP:L05": [(1, "formula"), (2, "example"), (3, "check"), (4, "stop")],
    "SEP:L06": [(1, "formula"), (2, "example"), (3, "check")],''',
        '''    # TOC (L00..L14)
    "TOC:L00": [(1, "sym"), (2, "lang"), (3, "example")],
    "TOC:L01": [(1, "example"), (2, "example"), (3, "verify")],
    "TOC:L02": [(1, "example"), (2, "example"), (3, "pitfalls")],
    "TOC:L03": [(1, "example"), (2, "prec"), (3, "kleene")],
    "TOC:L04": [(1, "why"), (2, "example"), (3, "pitfalls")],
    "TOC:L05": [(1, "sym"), (2, "example"), (3, "unique")],
    "TOC:L06": [(1, "example"), (2, "example"), (3, "verify")],
    "TOC:L07": [(1, "trees"), (2, "example"), (3, "pitfalls")],
    "TOC:L08": [(1, "machine"), (2, "example"), (3, "pitfalls")],
    "TOC:L09": [(1, "design"), (2, "example"), (3, "pitfalls")],
    "TOC:L10": [(1, "evidence"), (2, "universal"), (3, "pitfalls")],
    "TOC:L11": [(1, "intuition"), (2, "proof"), (3, "pitfalls")],
    "TOC:L12": [(1, "example"), (2, "rice"), (3, "classify")],
    "TOC:L13": [(1, "sym"), (2, "equiv"), (3, "picture")],
    "TOC:L14": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5"), (3, "practice")],

    # PLC (L00..L13)
    "PLC:L00": [(1, "sym"), (2, "example"), (3, "impl")],
    "PLC:L01": [(1, "sym"), (2, "example"), (3, "automaton")],
    "PLC:L02": [(1, "example"), (2, "code"), (3, "pitfalls")],
    "PLC:L03": [(1, "sym"), (2, "assoc"), (3, "example")],
    "PLC:L04": [(1, "sym"), (2, "example"), (3, "late")],
    "PLC:L05": [(1, "example"), (2, "sym"), (3, "tradeoff")],
    "PLC:L06": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L07": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L08": [(1, "sym"), (2, "methods"), (3, "pitfalls")],
    "PLC:L09": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PLC:L10": [(1, "gen"), (2, "example"), (3, "pitfalls")],
    "PLC:L11": [(1, "limit"), (2, "example"), (3, "pitfalls")],
    "PLC:L12": [(1, "example"), (2, "sharing"), (3, "pitfalls")],
    "PLC:L13": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5"), (3, "practice")],

    # PAR (L00..L13)
    "PAR:L00": [(1, "example"), (2, "measure"), (3, "quiz")],
    "PAR:L01": [(1, "sym"), (2, "example"), (3, "pitfalls")],
    "PAR:L02": [(1, "example"), (2, "formula"), (3, "pitfalls")],
    "PAR:L03": [(1, "intuition"), (2, "example"), (3, "example")],
    "PAR:L04": [(1, "example"), (2, "check"), (3, "check")],
    "PAR:L05": [(1, "example"), (2, "example"), (3, "check")],
    "PAR:L06": [(1, "example"), (2, "formula"), (3, "check")],
    "PAR:L07": [(1, "example"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L08": [(1, "example"), (2, "example"), (3, "check"), (4, "check")],
    "PAR:L09": [(1, "example"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L10": [(1, "check"), (2, "formula"), (3, "example"), (4, "check")],
    "PAR:L11": [(1, "formula"), (2, "example"), (3, "example"), (4, "check")],
    "PAR:L12": [(1, "example"), (2, "example"), (3, "check"), (4, "quiz")],
    "PAR:L13": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5"), (3, "practice")],

    # HCI (L00..L12)
    "HCI:L00": [(1, "sym"), (2, "concept"), (3, "example")],
    "HCI:L01": [(1, "example"), (2, "example"), (3, "pitfalls")],
    "HCI:L02": [(1, "example"), (2, "formula"), (3, "check")],
    "HCI:L03": [(1, "formula"), (2, "example"), (3, "check")],
    "HCI:L04": [(1, "formula"), (2, "example"), (3, "pitfalls")],
    "HCI:L05": [(1, "formula"), (2, "example"), (3, "pitfalls")],
    "HCI:L06": [(1, "formula"), (2, "example"), (3, "example"), (4, "pitfalls")],
    "HCI:L07": [(1, "example"), (2, "formula"), (3, "pitfalls")],
    "HCI:L08": [(1, "example"), (2, "pitfalls"), (3, "check")],
    "HCI:L09": [(1, "example"), (2, "formula"), (3, "concept"), (4, "example")],
    "HCI:L10": [(1, "concept"), (2, "example"), (3, "pitfalls")],
    "HCI:L11": [(1, "formula"), (2, "intuition"), (3, "example"), (4, "pitfalls")],
    "HCI:L12": [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (2, "check"), (3, "stage4"), (3, "practice")],

    # SEP (L00..L11)
    "SEP:L00": [(1, "sym"), (2, "example"), (3, "formula"), (4, "pitfalls")],
    "SEP:L01": [(1, "example"), (2, "formula"), (3, "law"), (4, "pitfalls")],
    "SEP:L02": [(1, "example"), (2, "formula"), (3, "example"), (4, "check")],
    "SEP:L03": [(1, "example"), (2, "check"), (3, "pitfalls"), (4, "log")],
    "SEP:L04": [(1, "sym"), (2, "example"), (3, "formula"), (4, "pitfalls")],
    "SEP:L05": [(1, "example"), (2, "formula"), (3, "formula"), (4, "pitfalls")],
    "SEP:L06": [(1, "example"), (2, "formula"), (3, "check")],''',
    ),
    (
        '''    "CAS:L09": [(1, "formula"), (2, "example"), (3, "check"), (4, "check")],
    "CAS:L10": [(1, "example"), (2, "check"), (3, "check"), (4, "pitfalls")],
    "CAS:L11": [(1, "formula"), (2, "example"), (3, "check"), (4, "inventory")],''',
        '''    "CAS:L09": [(1, "formula"), (2, "example"), (3, "example"), (4, "practice")],
    "CAS:L10": [(1, "example"), (2, "check"), (3, "check"), (4, "pitfalls")],
    "CAS:L11": [(1, "formula"), (2, "example"), (3, "inventory"), (4, "quiz")],''',
    ),
    # 2. TOC fixes
    (
        '''        ("L06", "Đếm số chuỗi ngoặc cân bằng độ dài 8 (số Catalan C_4 = 14)",
         "Duyệt vét cạn tất cả `2^8 = 256` chuỗi gồm hai ký tự `'('` và `')'` độ dài `8`, giữ lại mọi chuỗi mà số ngoặc đóng không bao giờ vượt ngoặc mở ở mọi tiền tố và kết thúc cân bằng về `0`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`catalan_4=<số nguyên>`",
         """valid = []
for m in range(1 << 8):
    s = ''.join('(' if (m >> i) & 1 else ')' for i in range(8))
    bal, ok = 0, True
    for ch in s:
        bal += 1 if ch == '(' else -1
        if bal < 0:
            ok = False; break
    if ok and bal == 0:
        valid.append(s)
print(f"catalan_4={len(valid)}")"""),''',
        '''        ("L06", "Đếm số chuỗi ngoặc cân bằng gồm 5 cặp ngoặc (độ dài 10)",
         "Duyệt tất cả `2^10 = 1024` chuỗi gồm hai ký tự `'('` và `')'` độ dài `10`, giữ lại mọi chuỗi mà số ngoặc đóng không bao giờ vượt ngoặc mở ở bất kỳ tiền tố nào và kết thúc về `0` (số Catalan `C_5`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`catalan_5=<số nguyên>`",
         """valid = []
for m in range(1 << 10):
    s = ''.join('(' if (m >> i) & 1 else ')' for i in range(10))
    bal, ok = 0, True
    for ch in s:
        bal += 1 if ch == '(' else -1
        if bal < 0:
            ok = False; break
    if ok and bal == 0:
        valid.append(s)
print(f"catalan_5={len(valid)}")"""),''',
    ),
    (
        '''        ("L08", "Kiểm chuẩn ôtômat đẩy xuống (PDA) trên toàn bộ 2047 chuỗi nhị phân dài 0..10",
         "Cài ôtômat đẩy xuống (đẩy `'0'` vào ngăn xếp ở pha đầu, chuyển pha và lấy `'0'` ra khi gặp `'1'`, từ chối ký tự lạ hoặc `'0'` đứng sau `'1'`). Đối chiếu kết quả của hàm với tập ngôn ngữ chuẩn `0^n 1^n` trên toàn bộ `2047` chuỗi nhị phân độ dài `0..10`, cùng 2 mẫu riêng `'000111'` và `'010101'`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`tested=<số> all_match=<0 hoặc 1> ex_000111=<0 hoặc 1> ex_010101=<0 hoặc 1>`",
         """def pda(s):
    st, ph1 = [], False
    for ch in s:
        if ch == '0' and not ph1: st.append('0')
        elif ch == '1' and st: ph1 = True; st.pop()
        else: return False
    return not st
spec = lambda s: s == '0' * (len(s) // 2) + '1' * (len(s) // 2)
strs = [format(m, f'0{L}b') if L else ''
        for L in range(11) for m in range(1 << L)]
ok = all(pda(s) == spec(s) for s in strs)
print(f"tested={len(strs)} all_match={int(ok)}",
      f"ex_000111={int(pda('000111'))} ex_010101={int(pda('010101'))}")"""),

        ("L09", "Chạy máy Turing cộng 1 nhị phân từ trái sang phải / phải sang trái trên '10111'",''',
        '''        ("L08", "Kiểm chuẩn ôtômat đẩy xuống (PDA) trên toàn bộ chuỗi nhị phân dài 0..10",
         "Cài ôtômat đẩy xuống (đẩy `'0'` vào ngăn xếp ở pha đầu, chuyển pha và lấy `'0'` ra khi gặp `'1'`, từ chối ký tự lạ hoặc `'0'` đứng sau `'1'`). Đối chiếu kết quả của hàm với ngôn ngữ `0^n 1^n` trên toàn bộ `2047` chuỗi nhị phân độ dài `0..10`, cùng hai mẫu `'00001111'` và `'01010101'`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`tested=<số> all_match=<0 hoặc 1> ex_00001111=<0 hoặc 1> ex_01010101=<0 hoặc 1>`",
         """def pda(s):
    st, ph1 = [], False
    for ch in s:
        if ch == '0' and not ph1: st.append('0')
        elif ch == '1' and st: ph1 = True; st.pop()
        else: return False
    return not st
spec = lambda s: s == '0' * (len(s) // 2) + '1' * (len(s) // 2)
strs = [format(m, f'0{L}b') if L else ''
        for L in range(11) for m in range(1 << L)]
ok = all(pda(s) == spec(s) for s in strs)
print(f"tested={len(strs)} all_match={int(ok)}",
      f"ex_00001111={int(pda('00001111'))} ex_01010101={int(pda('01010101'))}")"""),

        ("L09", "Chạy máy Turing cộng 1 nhị phân từ phải sang trái trên '10111'",''',
    ),
    (
        '''        ("L11", "Kiểm chứng bất khả thi trên bảng chéo 3×3 của bài toán dừng",
         "Cho 3 chương trình mẫu và bảng dự đoán giả định `H(P_i, P_j)` với hàng/cột `0, 1, 2`. Kiểm tra từng trong toàn bộ `2^3 = 8` khả năng hành vi dừng của một hàng ứng viên `D = [d0, d1, d2]` trên 3 đầu vào: không có hàng `D` nào khớp cùng lúc cả phần tử đường chéo đảo ngược `not H(D, D)` nếu `D` phải có mặt trong bảng.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`table_size=3 candidates=8 possible_matches=<số nguyên>`",
         """rows = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]''',
        '''        ("L11", "Kiểm chứng nghịch lý đường chéo trên bảng 3×3 của bài toán dừng",
         "Cho bảng dự đoán giả định 3×3 `rows = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]` ứng với `H(P_i, P_j)` (`1` là dừng, `0` là lặp vô hạn). Duyệt từng hàng ứng viên `D = [d0, d1, d2]` trong `2^3 = 8` khả năng hành vi trên 3 đầu vào để kiểm chứng: nếu `D == row[idx]` thì bắt buộc `D[idx] == 1 - row[idx]` là điều không thể xảy ra.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`table_size=<số> candidates=<số> possible_matches=<số nguyên>`",
         """rows = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]''',
    ),
    (
        '''        ("L13", "Kiểm chứng chứng chỉ Tổng tập con (Subset Sum) trong thời gian đa thức",
         "Cho tập số `S = [7, 11, 13, 19, 23]` và mục tiêu `T = 41`. Viết hàm kiểm tra chứng chỉ `C = [7, 11, 23]`: xác nhận mọi phần tử của `C` nằm đúng với bội số không vượt quá trong `S` và tổng bằng `T`, đồng thời đếm số bước cộng kiểm chứng.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`cert_steps=<số nguyên> verified=<0 hoặc 1> cert_sum=<số nguyên>`",
         """S = [7, 11, 13, 19, 23]; T = 41; cert = [7, 11, 23]''',
        '''        ("L13", "Kiểm chứng chứng chỉ Tổng tập con (Subset Sum) trong thời gian đa thức",
         "Cho tập số `S = [5, 9, 14, 18, 27]` và mục tiêu `T = 46`. Viết hàm kiểm tra chứng chỉ `C = [5, 14, 27]`: xác nhận mọi phần tử của `C` nằm đúng với bội số không vượt quá trong `S` và tổng bằng `T`, đồng thời đếm số phần tử cộng kiểm chứng.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`cert_steps=<số nguyên> verified=<0 hoặc 1> cert_sum=<số nguyên>`",
         """S = [5, 9, 14, 18, 27]; T = 46; cert = [5, 14, 27]''',
    ),
    # 3. PLC fixes
    (
        '''        ("L02", "Bộ phân tích đệ quy xuống theo tầng expr/term/atom cho '2+3*4' và '(2+3)*4'",
         "Cài bộ phân tích đệ quy xuống đúng tên ba tầng trong bài là `expr`, `term`, `atom` (nhân `*` gắn chặt hơn cộng `+`), kiểm tra trên `'2+3*4'` và `'(2+3)*4'`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`p1=<số nguyên> p2=<số nguyên>`",
         """def parse_val(s):
    ts = list(s.replace(' ', ''))
    def atom():
        if ts[0] != '(': return int(ts.pop(0))
        ts.pop(0); v = expr(); ts.pop(0); return v
    def fold(op, fn):
        v = fn()
        while ts and ts[0] == op:
            ts.pop(0); v = v * fn() if op == '*' else v + fn()
        return v
    expr = lambda: fold('+', lambda: fold('*', atom))
    return expr()
print(f"p1={parse_val('2+3*4')} p2={parse_val('(2+3)*4')}")"""),

        ("L03", "Tính kết hợp trái của phép trừ 12 - 5 - 3 = (12 - 5) - 3 = 4",
         "So sánh kết quả gộp trái đúng luật của biểu thức `12 - 5 - 3` với cách gộp phải sai `12 - (5 - 3)`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`left_assoc=<số nguyên> right_assoc=<số nguyên>`",
         """nums = [12, 5, 3]
left_assoc = (nums[0] - nums[1]) - nums[2]
right_assoc = nums[0] - (nums[1] - nums[2])
print(f"left_assoc={left_assoc} right_assoc={right_assoc}")"""),

        ("L04", "Mô phỏng chuỗi môi trường tra tên: tầm vực tĩnh so với tầm vực động",
         "Cài hàm `lookup(env, name)` duyệt theo liên kết cha để so sánh tra tên theo tầm vực tĩnh (từ vị trí định nghĩa hàm với `x = 10`) và tầm vực động (theo ngăn xếp lời gọi với `x = 25`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`static=<số nguyên> dynamic=<số nguyên>`",
         """def lookup(env, name):
    while env is not None:
        if name in env['vars']: return env['vars'][name]
        env = env['parent']
global_env = {'vars': {'x': 10}, 'parent': None}
fn_def_parent = global_env
def call_fn(caller_env, dynamic=False):
    local_env = {'vars': {}, 'parent': caller_env if dynamic else fn_def_parent}
    return lookup(local_env, 'x')
caller_env = {'vars': {'x': 25}, 'parent': global_env}
print(f"static={call_fn(caller_env, False)} dynamic={call_fn(caller_env, True)}")"""),''',
        '''        ("L02", "Bộ phân tích đệ quy xuống theo tầng expr/term/atom cho hai biểu thức số học",
         "Cài bộ phân tích đệ quy xuống theo đúng thứ tự ba tầng `expr`, `term`, `atom` (nhân `*` gắn chặt hơn cộng `+`), kiểm tra trên `'3+4*5'` và `'(3+4)*5'`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`p1=<số nguyên> p2=<số nguyên>`",
         """def parse_val(s):
    ts = list(s.replace(' ', ''))
    def atom():
        if ts[0] != '(': return int(ts.pop(0))
        ts.pop(0); v = expr(); ts.pop(0); return v
    def fold(op, fn):
        v = fn()
        while ts and ts[0] == op:
            ts.pop(0); v = v * fn() if op == '*' else v + fn()
        return v
    expr = lambda: fold('+', lambda: fold('*', atom))
    return expr()
print(f"p1={parse_val('3+4*5')} p2={parse_val('(3+4)*5')}")"""),

        ("L03", "Tính kết hợp trái của phép trừ trên bộ ba số [15, 6, 2]",
         "So sánh kết quả gộp trái đúng luật của biểu thức `15 - 6 - 2` với cách gộp phải sai `15 - (6 - 2)`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`left_assoc=<số nguyên> right_assoc=<số nguyên>`",
         """nums = [15, 6, 2]
left_assoc = (nums[0] - nums[1]) - nums[2]
right_assoc = nums[0] - (nums[1] - nums[2])
print(f"left_assoc={left_assoc} right_assoc={right_assoc}")"""),

        ("L04", "Mô phỏng chuỗi môi trường tra tên: tầm vực tĩnh so với tầm vực động",
         "Cài hàm `lookup(env, name)` duyệt theo liên kết cha để so sánh tra tên theo tầm vực tĩnh (từ vị trí định nghĩa hàm với `x = 15`) và tầm vực động (theo ngăn xếp lời gọi với `x = 30`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`static=<số nguyên> dynamic=<số nguyên>`",
         """def lookup(env, name):
    while env is not None:
        if name in env['vars']: return env['vars'][name]
        env = env['parent']
global_env = {'vars': {'x': 15}, 'parent': None}
fn_def_parent = global_env
def call_fn(caller_env, dynamic=False):
    local_env = {'vars': {}, 'parent': caller_env if dynamic else fn_def_parent}
    return lookup(local_env, 'x')
caller_env = {'vars': {'x': 30}, 'parent': global_env}
print(f"static={call_fn(caller_env, False)} dynamic={call_fn(caller_env, True)}")"""),''',
    ),
    (
        '''        ("L07", "Bao đóng giữ môi trường riêng: hai bộ cộng make_adder(10, 5) và make_adder(10, 3)",
         "Cài hàm `make_adder(start, step)` trả về bao đóng mỗi lần gọi cộng thêm `step` vào biến đếm riêng bắt đầu từ `start`. Tạo `a1 = make_adder(10, 5)` gọi 2 lần (`[15, 20]`) và `a2 = make_adder(10, 3)` gọi 1 lần (`13`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`a1=<danh sách 2 phần tử> a2=<số nguyên>`",
         """def make_adder(start, step):
    val = [start]
    def inc():
        val[0] += step
        return val[0]
    return inc
a1, a2 = make_adder(10, 5), make_adder(10, 3)
print(f"a1={[a1(), a1()]} a2={a2()}")"""),

        ("L08", "Đánh dấu-quét theo chiều rộng (BFS) thu hồi vòng rác trên đồ thị vùng đống",
         "Cài thuật toán đánh dấu-quét dùng hàng đợi tìm theo chiều rộng (`pop(0)`) từ gốc `'R'` trên đồ thị đối tượng `{'R': ['X'], 'X': ['Y'], 'Y': [], 'M': ['N'], 'N': ['M'], 'K': []}` để giữ lại các nút sống và liệt kê danh sách nút rác bị thu hồi theo thứ tự tăng dần.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`alive=<danh sách sắp xếp> reclaimed=<danh sách sắp xếp>`",
         """adj = {'R': ['X'], 'X': ['Y'], 'Y': [], 'M': ['N'], 'N': ['M'], 'K': []}''',
        '''        ("L07", "Bao đóng giữ môi trường riêng: hai bộ cộng độc lập với step khác nhau",
         "Cài hàm `make_adder(start, step)` trả về bao đóng mỗi lần gọi cộng thêm `step` vào biến đếm riêng bắt đầu từ `start`. Tạo `a1 = make_adder(20, 4)` gọi 2 lần và `a2 = make_adder(20, 7)` gọi 1 lần.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`a1=<danh sách 2 phần tử> a2=<số nguyên>`",
         """def make_adder(start, step):
    val = [start]
    def inc():
        val[0] += step
        return val[0]
    return inc
a1, a2 = make_adder(20, 4), make_adder(20, 7)
print(f"a1={[a1(), a1()]} a2={a2()}")"""),

        ("L08", "Đánh dấu-quét theo chiều rộng (BFS) thu hồi vòng rác trên đồ thị vùng đống",
         "Cài thuật toán đánh dấu-quét dùng hàng đợi tìm theo chiều rộng (`pop(0)`) từ gốc `'R'` trên đồ thị đối tượng `{'R': ['A'], 'A': ['B'], 'B': [], 'C': ['D'], 'D': ['C'], 'E': []}` để giữ lại các nút sống và liệt kê danh sách nút rác bị thu hồi theo thứ tự tăng dần.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`alive=<danh sách sắp xếp> reclaimed=<danh sách sắp xếp>`",
         """adj = {'R': ['A'], 'A': ['B'], 'B': [], 'C': ['D'], 'D': ['C'], 'E': []}''',
    ),
    (
        '''        ("L10", "Máy ảo ngăn xếp giữ đúng thứ tự toán hạng trừ: tính 10 - 2 * 3 = 4",
         "Thực thi dãy lệnh máy ảo ngăn xếp `['PUSH 10', 'PUSH 2', 'PUSH 3', 'MUL', 'SUB']`, chú ý lấy `b = pop()` (số trừ) trước `a = pop()` (số bị trừ) để trả ra `a - b = 4`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`vm_result=<số nguyên>`",
         """st = []
for ins in ['PUSH 10', 'PUSH 2', 'PUSH 3', 'MUL', 'SUB']:
    if ins.startswith('PUSH'): st.append(int(ins.split()[1]))
    elif ins == 'MUL': b, a = st.pop(), st.pop(); st.append(a * b)
    elif ins == 'SUB': b, a = st.pop(), st.pop(); st.append(a - b)
print(f"vm_result={st[0]}")"""),

        ("L11", "Tối ưu gấp hằng số trên cả 4 phép +, -, *, // cho biểu thức ('+', ('*', 4, 5), 'x')",
         "Cài hàm đệ quy `fold(node)` hỗ trợ cả 4 phép `'+'`, `'-'`, `'*'`, `'//'` trên cây biểu thức có lá số nguyên hoặc tên biến chuỗi, rồi rút gọn `('+', ('*', 4, 5), 'x')` thành `('+', 20, 'x')`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`folded=<biểu thức rút gọn>`",
         """def fold(node):
    if not isinstance(node, tuple): return node
    op, a, b = node[0], fold(node[1]), fold(node[2])
    if isinstance(a, int) and isinstance(b, int):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '//' and b != 0: return a // b
    return (op, a, b)
print(f"folded={fold(('+', ('*', 4, 5), 'x'))}")"""),

        ("L12", "Cập nhật dữ liệu bất biến: tạo bộ cố định mới (10, 20, 30, 40) và giữ nguyên bản ban đầu",
         "Dùng kiểu bộ cố định (tuple) trong Python tạo `xs2 = xs1 + (40,)` từ `xs1 = (10, 20, 30)` và xác nhận `xs1` không đổi.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`xs1=<bộ gốc> xs2=<bộ mới> unchanged=<0 hoặc 1>`",
         """xs1 = (10, 20, 30)
xs2 = xs1 + (40,)
print(f"xs1={xs1} xs2={xs2} unchanged={int(len(xs1) == 3)}")"""),

        ("L13", "Kiểm chứng số liệu an toàn bộ nhớ: tỉ lệ an toàn Chrome 96.2% và mức giảm 2019->2024",
         "Tính lại hai số liệu công bố trong bài hành trình: (1) tỉ lệ không dính lỗi bộ nhớ trong nhóm 130 tính năng mới của Chromium khi chỉ có 5 lỗ hổng (`(130 - 5)/130 * 100`); (2) mức giảm tương đối tỉ lệ lỗ hổng bộ nhớ Android từ `76%` (2019) xuống `24%` (2024).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`safe_new_pct=<1 chữ số>% android_drop_pct=<1 chữ số>%`",
         """safe_new = (130 - 5) / 130 * 100
android_drop = (76 - 24) / 76 * 100
print(f"safe_new_pct={safe_new:.1f}% android_drop_pct={android_drop:.1f}%")"""),''',
        '''        ("L10", "Máy ảo ngăn xếp giữ đúng thứ tự toán hạng trừ trên biểu thức hậu tố",
         "Thực thi dãy lệnh máy ảo ngăn xếp `['PUSH 12', 'PUSH 3', 'PUSH 2', 'MUL', 'SUB']`, lấy `b = pop()` (số trừ) trước `a = pop()` (số bị trừ) để tính đúng `a - b`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`vm_result=<số nguyên>`",
         """st = []
for ins in ['PUSH 12', 'PUSH 3', 'PUSH 2', 'MUL', 'SUB']:
    if ins.startswith('PUSH'): st.append(int(ins.split()[1]))
    elif ins == 'MUL': b, a = st.pop(), st.pop(); st.append(a * b)
    elif ins == 'SUB': b, a = st.pop(), st.pop(); st.append(a - b)
print(f"vm_result={st[0]}")"""),

        ("L11", "Tối ưu gấp hằng số trên cả 4 phép +, -, *, // cho cây biểu thức",
         "Cài hàm đệ quy `fold(node)` hỗ trợ cả 4 phép `'+'`, `'-'`, `'*'`, `'//'` trên cây biểu thức có lá số nguyên hoặc tên biến chuỗi, rồi rút gọn `('+', ('*', 3, 6), 'y')`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`folded=<biểu thức rút gọn>`",
         """def fold(node):
    if not isinstance(node, tuple): return node
    op, a, b = node[0], fold(node[1]), fold(node[2])
    if isinstance(a, int) and isinstance(b, int):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '//' and b != 0: return a // b
    return (op, a, b)
print(f"folded={fold(('+', ('*', 3, 6), 'y'))}")"""),

        ("L12", "Cập nhật dữ liệu bất biến bằng bộ cố định (tuple)",
         "Dùng kiểu bộ cố định (tuple) trong Python tạo `xs2 = xs1 + (35,)` từ `xs1 = (5, 15, 25)` và kiểm chứng `xs1` ban đầu vẫn nguyên vẹn.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`xs1=<bộ gốc> xs2=<bộ mới> unchanged=<0 hoặc 1>`",
         """xs1 = (5, 15, 25)
xs2 = xs1 + (35,)
print(f"xs1={xs1} xs2={xs2} unchanged={int(len(xs1) == 3)}")"""),

        ("L13", "Kiểm chứng tỉ lệ lỗi bộ nhớ Chromium (2019) và mức giảm trên Android (2019->2024)",
         "Tính lại hai số liệu công bố trong bài hành trình: (1) tỉ lệ lỗ hổng nghiêm trọng **do hỏng bộ nhớ** của Chromium (khi chỉ `5` trên `130` lỗ hổng là không do hỏng bộ nhớ); (2) mức giảm tương đối tỉ lệ lỗ hổng bộ nhớ Android từ `76%` (2019) xuống `24%` (2024).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`mem_bug_pct=<1 chữ số>% android_drop_pct=<1 chữ số>%`",
         """mem_bug = (130 - 5) / 130 * 100
android_drop = (76 - 24) / 76 * 100
print(f"mem_bug_pct={mem_bug:.1f}% android_drop_pct={android_drop:.1f}%")"""),''',
    ),
    # 4. PAR L04 title spoiler
    (
        '        ("L04", "Lập lịch việc dài trước (LPT) giảm thời gian hoàn thành (makespan) từ 30 xuống 20",',
        '        ("L04", "So sánh lập lịch chia đôi tĩnh và việc dài trước (LPT) trên 2 lõi",',
    ),
    # 5. HCI fixes
    (
        '''        ("L00", "Kiểm chứng danh sách cảnh báo khác nhãn và tính thời gian trễ diễn tập 27 phút",
         "Kiểm tra danh sách điều khiển tách biệt rõ hai nhãn nút bấm `drill_btn = 'XAC NHAN TAP TRAN'` và `real_btn = 'GUI CANH BAO THAT'`, đồng thời tính khoảng thời gian trôi qua giữa hai mốc trong ngày `14:12` và `14:39` theo số phút.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`distinct=<0 hoặc 1> diff_min=<số nguyên>`",
         """drill_btn = 'XAC NHAN TAP TRAN'; real_btn = 'GUI CANH BAO THAT'
t1 = 14 * 60 + 12; t2 = 14 * 60 + 39
print(f"distinct={int(drill_btn != real_btn)} diff_min={t2 - t1}")"""),

        ("L01", "Ánh xạ tự nhiên: đếm hoán vị 5! = 120 của hàng 5 nút rời so với ghép vị trí",
         "Tính số cách ghép sai có thể nảy sinh khi đặt 5 nút vặn trên một hàng ngang điều khiển 5 vị trí không gian khác nhau (`math.factorial(5)`) so với ánh xạ khớp trực tiếp (`1`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`linear_guesses=<số nguyên> matched_2d=1`",
         """import math
print(f"linear_guesses={math.factorial(5)} matched_2d=1")"""),''',
        '''        ("L00", "Kiểm chứng tách nhãn nút bấm điều khiển và đo thời gian trễ diễn tập",
         "Kiểm tra danh sách điều khiển tách biệt rõ hai nhãn nút bấm `drill_btn = 'XAC NHAN TAP TRAN'` và `real_btn = 'GUI CANH BAO THAT'`, đồng thời tính số phút trôi qua giữa hai mốc `13:18` và `13:52`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`distinct=<0 hoặc 1> diff_min=<số nguyên>`",
         """drill_btn = 'XAC NHAN TAP TRAN'; real_btn = 'GUI CANH BAO THAT'
t1 = 13 * 60 + 18; t2 = 13 * 60 + 52
print(f"distinct={int(drill_btn != real_btn)} diff_min={t2 - t1}")"""),

        ("L01", "Ánh xạ tự nhiên: đếm hoán vị ghép nối của hàng 6 nút rời so với ghép đúng vị trí",
         "Tính số hoán vị ghép có thể sinh ra khi đặt `n = 6` nút xoay thẳng hàng điều khiển 6 vùng không gian rời (`math.factorial(6)`), so với đúng `1` ánh xạ khớp vị trí 2 chiều duy nhất.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`linear_guesses=<số nguyên> matched_2d=<số nguyên>`",
         """import math
n = 6
guesses = math.factorial(n)
matched = int(len(set(range(n))) == n)
print(f"linear_guesses={guesses} matched_2d={matched}")"""),''',
    ),
    (
        '''        ("L04", "Gom nhóm thông tin: mã 8 chữ số '73915284' tách thành 4 cụm 2 chữ số",
         "Tách chuỗi 8 chữ số `'73915284'` thành từng cụm 2 chữ số (`['73', '91', '52', '84']`) và kiểm tra xem số cụm mới có nằm trong ngưỡng trí nhớ làm việc `<= 4` cụm hay không.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`raw_units=<số nguyên> grouped_chunks=<số nguyên> fits_wm=<0 hoặc 1>`",
         """s = '73915284'
chunks = [s[i:i+2] for i in range(0, len(s), 2)]
print(f"raw_units={len(s)} grouped_chunks={len(chunks)} fits_wm={int(len(chunks) <= 4)}")"""),

        ("L05", "Mô hình thao tác từng bước KLM: đổi tên bằng chuột (4.35 s) vs phím F2 (2.55 s)",
         "Cộng chi phí chuẩn: dùng chuột (`H 0.4 + M 1.35 + P 1.1 + B 0.2 + P 1.1 + B 0.2 = 4.35 s`) so với dùng phím tắt `F2`, nghĩ `M`, gõ 4 phím chữ `K`, nhấn `Enter` (`0.2 + 1.35 + 4*0.2 + 0.2 = 2.55 s`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`mouse_s=<2 chữ số> keyboard_s=<2 chữ số>`",
         """mouse_s = 0.4 + 1.35 + 1.1 + 0.2 + 1.1 + 0.2
key_s = 0.2 + 1.35 + 4 * 0.2 + 0.2
print(f"mouse_s={mouse_s:.2f} keyboard_s={key_s:.2f}")"""),

        ("L06", "Công thức phát hiện lỗi khả dụng Nielsen với p=0.25 ở N=4 và N=12 người thử",
         "Tính tỉ lệ lỗi phát hiện được `1 - (1 - p)^N` dưới dạng phần trăm cho vấn đề có `p = 0.25` khi thử với `N = 4` và `N = 12` người dùng.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`n4_pct=<1 chữ số>% n12_pct=<1 chữ số>%`",
         """cov = lambda n, p=0.25: (1.0 - (1.0 - p) ** n) * 100
print(f"n4_pct={cov(4):.1f}% n12_pct={cov(12):.1f}%")"""),''',
        '''        ("L04", "Gom nhóm thông tin: chia chuỗi số thành cụm 2 chữ số và kiểm ngưỡng 4 khe nhớ",
         "Tách chuỗi 10 chữ số `'6149283750'` thành từng cụm 2 chữ số (`['61', '49', ...]`) và kiểm tra xem số cụm mới có nằm gọn trong ngưỡng trí nhớ làm việc `<= 4` cụm hay không.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`raw_units=<số nguyên> grouped_chunks=<số nguyên> fits_wm=<0 hoặc 1>`",
         """s = '6149283750'
chunks = [s[i:i+2] for i in range(0, len(s), 2)]
print(f"raw_units={len(s)} grouped_chunks={len(chunks)} fits_wm={int(len(chunks) <= 4)}")"""),

        ("L05", "Mô hình thao tác từng bước KLM: đổi tên bằng chuột so với dùng phím tắt",
         "Cộng chi phí chuẩn KLM (`K=0.20, P=1.10, H=0.40, M=1.35, BB=0.20`): dùng chuột chọn rồi bấm sửa (`H + M + P + BB + P + BB + 3*K`) so với dùng phím tắt `Ctrl+R` (`H + 2*K + M + 3*K + K`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`mouse_s=<2 chữ số> keyboard_s=<2 chữ số>`",
         """mouse_s = 0.4 + 1.35 + 1.1 + 0.2 + 1.1 + 0.2 + 3 * 0.2
key_s = 0.4 + 2 * 0.2 + 1.35 + 3 * 0.2 + 0.2
print(f"mouse_s={mouse_s:.2f} keyboard_s={key_s:.2f}")"""),

        ("L06", "Công thức phát hiện lỗi khả dụng theo số người thử độc lập N",
         "Với vấn đề có xác suất một người phát hiện được là `lam = 0.25` (tức xác suất một người bỏ sót `p_miss = 1 - lam = 0.75`): tính tỉ lệ lỗi phát hiện được `1 - (1 - lam)^N` (theo %) khi thử `N = 6` và `N = 12` người dùng độc lập.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`n6_pct=<1 chữ số>% n12_pct=<1 chữ số>%`",
         """cov = lambda n, lam=0.25: (1.0 - (1.0 - lam) ** n) * 100
print(f"n6_pct={cov(6):.1f}% n12_pct={cov(12):.1f}%")"""),''',
    ),
    (
        '''        ("L08", "Dựng hình vuông La-tinh 4×4 cân bằng thứ tự cho 4 giao diện A, B, C, D",
         "Tạo hình vuông La-tinh xoay vòng kích thước `4 × 4` cho 4 giao diện `['A', 'B', 'C', 'D']` và kiểm tra cả mọi hàng lẫn mọi cột đều chứa đủ đúng 4 giao diện.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`size=4 balanced=<0 hoặc 1> perms_total=24`",
         """import math
items = ['A', 'B', 'C', 'D']
latin = [items[r:] + items[:r] for r in range(4)]
r_ok = all(len(set(row)) == 4 for row in latin)
c_ok = all(len({latin[r][c] for r in range(4)}) == 4 for c in range(4))
ok = int(r_ok and c_ok)
print(f"size=4 balanced={ok} perms_total={math.factorial(4)}")"""),''',
        '''        ("L08", "Dựng hình vuông La-tinh 5×5 cân bằng thứ tự cho 5 giao diện",
         "Tạo hình vuông La-tinh xoay vòng kích thước `5 × 5` cho 5 giao diện `['A', 'B', 'C', 'D', 'E']`, kiểm tra mọi hàng và mọi cột đều chứa đủ 5 giao diện, và tính tổng số hoán vị đầy đủ `5!`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`size=<số nguyên> balanced=<0 hoặc 1> perms_total=<số nguyên>`",
         """import math
items = ['A', 'B', 'C', 'D', 'E']
n = len(items)
latin = [items[r:] + items[:r] for r in range(n)]
r_ok = all(len(set(row)) == n for row in latin)
c_ok = all(len({latin[r][c] for r in range(n)}) == n for c in range(n))
print(f"size={n} balanced={int(r_ok and c_ok)} perms_total={math.factorial(n)}")"""),''',
    ),
    (
        '''        ("L11", "Kiểm chứng 4 lớp rào chắn cảnh báo khẩn cấp và độ trễ sự cố 38 phút",
         "Kiểm tra cấu hình hệ thống mới gồm 4 lớp: khác môi trường tập–thật, bắt buộc xem trước không rỗng, có người thứ hai duyệt (`two_person = True`) và có mẫu đính chính sẵn (`cancel_tpl = True`), cùng thời lượng trễ `8:07 -> 8:45`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`mins_delay=<số nguyên> guards_passed=<số nguyên>`",
         """mins = (8 * 60 + 45) - (8 * 60 + 7)
guards = ['env_split', 'preview_nonempty', 'two_person', 'cancel_tpl']
print(f"mins_delay={mins} guards_passed={len(guards)}")"""),

        ("L12", "Hành trình WCAG: tính lại 65 điểm kiểm, tương phản 21:1 và diện tích 24×24 vs 44×44",
         "Tính tổng điểm kiểm chuẩn năm 1999 từ ba mức `16 + 30 + 19`, tính tỉ lệ tương phản trắng–đen `(1.0 + 0.05) / (0.0 + 0.05)`, và tính tỉ lệ diện tích nút chuẩn `44×44` so với đích tối thiểu `24×24`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`wcag1=<số nguyên> contrast_max=<1 chữ số> area_24=<số> ratio_44_24=<2 chữ số>x`",
         """wcag1 = sum([16, 30, 19])
contrast = (1.0 + 0.05) / (0.0 + 0.05)
area_24 = 24 * 24
ratio = (44 * 44) / area_24
print(f"wcag1={wcag1} contrast_max={contrast:.1f} area_24={area_24} ratio_44_24={ratio:.2f}x")"""),''',
        '''        ("L11", "Kiểm chứng rào chắn cảnh báo khẩn cấp và thời lượng phản hồi diễn tập",
         "Kiểm tra danh sách rào chắn an toàn của giao diện mới `['env_split', 'preview_nonempty', 'two_person', 'cancel_tpl']` và tính tổng thời lượng trễ diễn tập từ mốc `09:12` tới `09:49`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`mins_delay=<số nguyên> guards_passed=<số nguyên>`",
         """mins = (9 * 60 + 49) - (9 * 60 + 12)
guards = ['env_split', 'preview_nonempty', 'two_person', 'cancel_tpl']
print(f"mins_delay={mins} guards_passed={len(guards)}")"""),

        ("L12", "Hành trình WCAG: kiểm chứng tổng điểm kiểm, tỉ lệ tương phản và diện tích đích bấm",
         "Tính tổng số điểm kiểm của ba mức chuẩn năm 1999 (`[16, 30, 19]`), tính tỉ lệ tương phản `(L1 + 0.05) / (L2 + 0.05)` cho cặp độ sáng `(L1=0.90, L2=0.05)`, tính diện tích đích tối thiểu `24×24` (`area_24`) và tỉ lệ diện tích nút chuẩn `48×48` so với `24×24`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`wcag1=<số nguyên> contrast_ratio=<1 chữ số> area_24=<số> ratio_48_24=<2 chữ số>x`",
         """wcag1 = sum([16, 30, 19])
contrast = (0.90 + 0.05) / (0.05 + 0.05)
area_24 = 24 * 24
ratio = (48 * 48) / area_24
print(f"wcag1={wcag1} contrast_ratio={contrast:.1f} area_24={area_24} ratio_48_24={ratio:.2f}x")"""),''',
    ),
    # 6. SEP fixes
    (
        '''        ("L01", "Dữ liệu cá nhân: ước lượng khả năng duy nhất qua 365 ngày sinh × 60 độ tuổi × 2 giới tính",
         "Tính tổng tổ hợp `c = 365 * 60 * 2` và ước lượng xác suất một người là duy nhất trong vùng dân cư `N = 5 000` người theo công thức gần đúng `exp(-(N - 1) / c)`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`combos=<số nguyên> prob_unique=<3 chữ số>`",
         """import math
combos = 365 * 60 * 2
p_unique = math.exp(-(5000 - 1) / combos)
print(f"combos={combos} prob_unique={p_unique:.3f}")"""),''',
        '''        ("L01", "Dữ liệu cá nhân: ước lượng khả năng duy nhất qua tập thuộc tính dân cư",
         "Tính tổng tổ hợp `c = 365 * 50 * 2` (ngày sinh × độ tuổi × giới tính) và ước lượng xác suất một người là duy nhất trong vùng dân cư `N = 8 000` người theo công thức `(1 - 1/c)^(N - 1)`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`combos=<số nguyên> prob_unique=<3 chữ số>`",
         """combos = 365 * 50 * 2
p_unique = (1.0 - 1.0 / combos) ** (8000 - 1)
print(f"combos={combos} prob_unique={p_unique:.3f}")"""),''',
    ),
    (
        '''        ("L03", "Giải thích phản chứng: hồ sơ (25 triệu, 2 năm) với score = 0.4*income + 3*years >= 22",
         "Tính điểm hiện tại của hồ sơ `(income = 25, years = 2)` theo công thức `0.4 * income + 3 * years`, kiểm tra đạt ngưỡng `22` hay chưa, và tính số năm kinh nghiệm cần tăng thêm tối thiểu để đạt `22`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`score=<1 chữ số> pass=<0 hoặc 1> need_extra_years=<1 chữ số>`",
         """score = 0.4 * 25 + 3 * 2
need_years = (22 - score) / 3.0
print(f"score={score:.1f} pass={int(score >= 22)} need_extra_years={need_years:.1f}")"""),''',
        '''        ("L03", "Giải thích phản chứng: tính điểm hồ sơ và số năm cần thêm để đạt ngưỡng 22",
         "Tính điểm hiện tại của hồ sơ `(income = 30, years = 2)` theo công thức `0.4 * income + 3 * years`, kiểm tra đạt ngưỡng `22` hay chưa, và tính số năm kinh nghiệm cần tăng thêm tối thiểu để đạt `22`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`score=<1 chữ số> pass=<0 hoặc 1> need_extra_years=<1 chữ số>`",
         """score = 0.4 * 30 + 3 * 2
need_years = (22 - score) / 3.0
print(f"score={score:.1f} pass={int(score >= 22)} need_extra_years={need_years:.1f}")"""),''',
    ),
    (
        '''        ("L07", "Tính hạn công bố lỗ hổng theo lịch thật (năm nhuận 2024): 90 ngày, +30 gia hạn, và hạn 7 ngày",
         "Dùng `datetime.date` bắt đầu từ ngày `2024-02-01` (năm nhuận 2024 có 29/02): tính hạn chuẩn 90 ngày, hạn gia hạn tối đa `90 + 30 = 120` ngày khi có bản vá phối hợp, và hạn khẩn `7` ngày nếu lỗi đang bị khai thác.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`d90=<YYYY-MM-DD> d120=<YYYY-MM-DD> exploit_7d=<YYYY-MM-DD>`",
         """import datetime as dt
d0 = dt.date(2024, 2, 1)
print(f"d90={d0 + dt.timedelta(days=90)}",
      f"d120={d0 + dt.timedelta(days=120)}",
      f"exploit_7d={d0 + dt.timedelta(days=7)}")"""),

        ("L08", "Luật 3 bước chọn phương án đa bên: lọc hại nặng cực đoan rồi mới xét tổng điểm",
         "Cho điểm tác động tới 4 bên liên quan của ba phương án: `'P1': [3, 3, 2, -2]`, `'P2': [1, 1, 1, 0]`, `'P3': [0, 2, 1, 1]`. Áp dụng luật 3 bước: loại mọi phương án có điểm thấp nhất `min <= -2`, sau đó chọn phương án có điểm nhỏ nhất cao nhất (hoà thì lấy tổng điểm lớn nhất).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`filtered=<danh sách tên> fair_pick=<tên phương án>`",
         """plans = {'P1': [3, 3, 2, -2], 'P2': [1, 1, 1, 0], 'P3': [0, 2, 1, 1]}
safe = sorted(k for k, v in plans.items() if min(v) > -2)
best = max(safe, key=lambda k: (min(plans[k]), sum(plans[k])))
print(f"filtered={safe} fair_pick={best}")"""),

        ("L09", "Ước lượng ba điểm PERT (O, M, B) với O=3, M=5, B=13 ngày cho chuỗi 3 việc",
         "Áp dụng công thức của bài `E = (O + 4*M + B) / 6` và `SD = (B - O) / 6` cho một công việc có `(O=3, M=5, B=13)` ngày, rồi tính kỳ vọng tổng cho 3 công việc giống nhau nối tiếp.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`E=<2 chữ số> SD=<2 chữ số> sum_3E=<2 chữ số>`",
         """O, M, B = 3.0, 5.0, 13.0''',
        '''        ("L07", "Tính hạn công bố lỗ hổng theo lịch thật (năm nhuận 2024): hạn 90 ngày, sau vá +30 ngày (khi v<=90), và hạn 7 ngày",
         "Dùng `datetime.date` bắt đầu từ ngày `2024-02-01` (năm nhuận 2024 có 29/02): tính hạn chuẩn 90 ngày, ngày công bố sau khi vá sớm ở ngày `v = 45` (`v <= 90`, công bố ở `min(90, v + 30)` ngày sau ngày báo), và hạn khẩn `7` ngày nếu lỗi đang bị khai thác.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`d90=<YYYY-MM-DD> d_patched=<YYYY-MM-DD> exploit_7d=<YYYY-MM-DD>`",
         """import datetime as dt
d0 = dt.date(2024, 2, 1); v = 45
days_pub = min(90, v + 30) if v <= 90 else 90
print(f"d90={d0 + dt.timedelta(days=90)}",
      f"d_patched={d0 + dt.timedelta(days=days_pub)}",
      f"exploit_7d={d0 + dt.timedelta(days=7)}")"""),

        ("L08", "Luật 3 bước chọn phương án đa bên: ràng buộc không âm, tổng điểm, và ưu tiên bên yếu thế",
         "Cho điểm tác động trên thang `[-2, 2]` tới 4 bên `[công_ty, khách, nhà_hàng, tài_xế]` của ba phương án: `'P1': [2, 2, 1, -1]`, `'P2': [1, 1, 2, 0]`, `'P3': [0, 1, 1, 2]`. Áp dụng đúng luật trong bài: (1) chỉ giữ phương án có điểm nhỏ nhất `>= 0`; (2) xếp theo `(tổng điểm, điểm của bên yếu thế nhất [tài_xế])`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`filtered=<danh sách tên> fair_pick=<tên phương án>`",
         """plans = {'P1': [2, 2, 1, -1], 'P2': [1, 1, 2, 0], 'P3': [0, 1, 1, 2]}
safe = sorted(k for k, v in plans.items() if min(v) >= 0)
best = max(safe, key=lambda k: (sum(plans[k]), plans[k][-1]))
print(f"filtered={safe} fair_pick={best}")"""),

        ("L09", "Ước lượng ba điểm (O, M, B) với O=2, M=6, B=16 ngày cho chuỗi 3 việc",
         "Áp dụng công thức của bài `E = (O + 4*M + B) / 6` và `s = (B - O) / 6` cho một công việc có `(O=2, M=6, B=16)` ngày, rồi tính kỳ vọng tổng cho 3 công việc giống nhau nối tiếp.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`E=<2 chữ số> SD=<2 chữ số> sum_3E=<2 chữ số>`",
         """O, M, B = 2.0, 6.0, 16.0''',
    ),
    (
        '''        ("L11", "Sweeney & ngưỡng bảo vệ dữ liệu: tổ hợp 292 000 người trên 40 000 dân và mức phạt 4%",
         "Tính số tổ hợp phân biệt `2 * 5 * 365 * 80` (giới tính, 5 mã vùng, 365 ngày, 80 năm sinh), xác suất ước lượng một người duy nhất `1 - exp(-N / c)` trong `N = 40 000` dân (thực chất `prob_unique = exp(-N / c)` không trùng với `39 999` người khác), và mức trần phạt GDPR `4%` trên doanh thu `50 triệu EUR`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`combos=<số nguyên> prob_unique=<3 chữ số> max_gdpr_M=<1 chữ số>`",
         """import math
combos = 2 * 5 * 365 * 80
p_uniq = math.exp(-39999 / combos)
gdpr_m = 50.0 * 0.04
print(f"combos={combos} prob_unique={p_uniq:.3f} max_gdpr_M={gdpr_m:.1f}")"""),''',
        '''        ("L11", "Tổ hợp nhận dạng và mức phạt tối đa theo Luật Bảo vệ dữ liệu cá nhân (5% doanh thu)",
         "Tính số tổ hợp phân biệt `2 * 5 * 365 * 100` (2 giới tính, 5 mã vùng, 365 ngày sinh, 100 năm), xác suất một người không trùng ai `(1 - 1/c)^(N - 1)` trong nhóm `N = 50 000` dân, và mức phạt tối đa `5%` doanh thu (Điều 8 Luật 91/2025) cho công ty doanh thu `200 tỉ đồng`.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`combos=<số nguyên> prob_unique=<3 chữ số> max_fine_B=<1 chữ số>`",
         """combos = 2 * 5 * 365 * 100
p_uniq = (1.0 - 1.0 / combos) ** (50000 - 1)
fine_b = max(3.0, 200.0 * 0.05)
print(f"combos={combos} prob_unique={p_uniq:.3f} max_fine_B={fine_b:.1f}")"""),''',
    ),
    # 7. CAS fixes
    (
        '''        ("L01", "Patriot Dhahran 1991: tính sai số cắt nhị phân 24-bit của 0.1 s qua 50 giờ và 100 giờ",
         "Tính trực tiếp sai số cắt cụt số `0.1` trên hệ 24 bit dấu phẩy tĩnh `0.1 - int(0.1 * 2^24) / 2^24` và nhân với số nhịp 0.1 giây sau `50 giờ` và `100 giờ` (đạt đúng `0.3433 s`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`drift_50h=<4 chữ số> drift_100h=<4 chữ số>`",
         """scale = 1 << 24''',
        '''        ("L01", "Patriot (1991): sai số nhị phân 24-bit của 0.1 giây tích luỹ sau 50h và 100h",
         "Mô phỏng thanh ghi 24-bit (1 bit dấu + 23 bit phần lẻ, bước `scale = 1 << 23`) biểu diễn `1/10 = 0.1`: tính sai số chặt cụt mỗi tích tắc `0.1 - int(0.1 * scale)/scale`, rồi nhân với `50 giờ` và `100 giờ` ở tần số `10 Hz` (`0.1 giây/nhịp`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`drift_50h=<4 chữ số> drift_100h=<4 chữ số>`",
         """scale = 1 << 23''',
    ),
    (
        '''        ("L06", "Amazon S3 (2017): rào chắn ngưỡng tối thiểu khoẻ mạnh khi gỡ máy khỏi cụm",
         "Cho cụm `100` máy chủ có ngưỡng an toàn tối thiểu phải giữ lại `80` máy đang chạy: viết kiểm tra chặn yêu cầu gỡ `35` máy (`max_removable = 20`).\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`max_removable=<số> req=35 blocked=<0 hoặc 1>`",
         """total, min_healthy, req = 100, 80, 35''',
        '''        ("L06", "Amazon S3 (2017): rào chắn ngưỡng tối thiểu khoẻ mạnh khi gỡ máy khỏi cụm",
         "Cho cụm `120` máy chủ có ngưỡng an toàn tối thiểu phải giữ lại `90` máy đang chạy: viết kiểm tra chặn yêu cầu gỡ `40` máy.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`max_removable=<số> req=40 blocked=<0 hoặc 1>`",
         """total, min_healthy, req = 120, 90, 40''',
    ),
    (
        '''        ("L07", "Cloudflare (2019): bùng nổ bậc ba O(n^3) của mẫu '.*.*=.*' khi quét mọi vị trí đầu",
         "Tính tổng số bước quay lui tích luỹ khi bộ khớp không neo thử lại ở mọi vị trí bắt đầu `s = 0..n-1` trên chuỗi `n = 200` ký tự thiếu dấu `'='`: mỗi vị trí `s` xét `m*(m+1)//2` với `m = n - s` (tổng bằng `n*(n+1)*(n+2)//6`), so với `n` bước tuyến tính.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`n=200 cubic_steps=<số nguyên> ratio=<số nguyên>x`",
         """n = 200
cubic = sum((n - s) * (n - s + 1) // 2 for s in range(n))
print(f"n={n} cubic_steps={cubic} ratio={cubic // n}x")"""),''',
        '''        ("L07", "Cloudflare (2019): bùng nổ bậc ba O(n^3) của mẫu `.*.*=.*` khi quét mọi vị trí đầu",
         "Tính tổng số bước quay lui tích luỹ khi bộ khớp không neo thử lại ở mọi vị trí bắt đầu `s = 0..n-1` trên chuỗi `n = 150` ký tự thiếu dấu `'='`: mỗi vị trí `s` xét `m*(m+1)//2` với `m = n - s`, so với `n` bước tuyến tính.\\n\\n"
         "Định dạng đầu ra (1 dòng):\\n`n=<số nguyên> cubic_steps=<số nguyên> ratio=<số nguyên>x`",
         """n = 150
cubic = sum((n - s) * (n - s + 1) // 2 for s in range(n))
print(f"n={n} cubic_steps={cubic} ratio={cubic // n}x")"""),''',
    ),
    (
        '''overread = (1 + 2 + 65535 + 16) - 20''',
        '''overread = 65535 - (20 - 3)''',
    ),
]

for idx, (old, new) in enumerate(repls, 1):
    assert old in txt, f"Mismatch #{idx}: {old[:100]!r}"
    assert txt.count(old) == 1, f"Non-unique #{idx}"
    txt = txt.replace(old, new)

p.write_text(txt, encoding="utf-8")
print(f"Patched {p} cleanly ({len(repls)} blocks)!")
