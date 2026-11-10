# SC1 nhóm 4 — CS112, CSA, OSY, NET, BCH, ESY: 68 khối

> Người điều phối ghi tệp này, nguyên văn từ câu trả lời cuối của tác tử nhóm 4 (công cụ không cho tác tử ghi tệp báo cáo). Kết quả cổng do người điều phối chạy lại nằm ở `report_SC1.md`.

Sổ: `audit/review/screen_code/{CS112,CSA,OSY,NET,BCH,ESY}.yaml`, 37 nguồn. CS112 chỉ đọc và sửa `lessons/cs112/`, `audit/cs112/`; không chạm CS115.

## 1. Số theo khoá
| Khoá | khối | run | syntax | fragment | output | pseudo | other | unverified_claims |
|---|---|---|---|---|---|---|---|---|
| CS112 | 22 | 0 | 2 | 0 | 0 | 20 | 0 | 22 |
| CSA | 13 | 6 | 1 | 0 | 2 | 0 | 4 | 4 |
| OSY | 12 | 0 | 4 | 0 | 0 | 5 | 3 | 8 |
| NET | 10 | 0 | 0 | 0 | 0 | 0 | 10 | 0 |
| BCH | 8 | 0 | 0 | 0 | 0 | 3 | 5 | 3 |
| ESY | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 3 |
| **Tổng** | **68** | **6** | **10** | **0** | **2** | **28** | **22** | **40** |

- **pseudo (28)**:
  - Mọi khối đều có chữ Việt trong thân, hoặc đầu hàm kiểu `f(a, l, r):`, `for j = 1..n` (WARN 0).
  - Mỗi điều bài nói về kết quả được kiểm bằng bản Python dịch sát từng dòng (`twin_of`).
  - Hai khối không có twin: OSY L04 sym chỉ là định nghĩa; OSY L05 example 0 1 được kiểm cùng bên sản xuất.
- **other (22)**: NET 10, BCH 5, OSY 3 là phép tính bit, mã băm hoặc dữ liệu. Mỗi khối có nguồn Python đọc nguyên văn (`files:`) và tính lại:
  - CRC: chỗ đặt 1011, từng hàng XOR, số bước bị lược, phần dư;
  - /20, /21, /26 bằng `ipaddress`;
  - SHA-256 theo quy ước `|`;
  - Dijkstra; tập làm việc; `stat.filemode`.
- **other, CSA**:
  - 3 khối hợp ngữ do máy ảo Python chạy nguyên văn (L07: r1 = 55, 33 lệnh, vết 3 vòng).
  - L09: mô hình đường ống 5 tầng.
  - CSA L16 (bash `cat /sys/...`): đã đối chiếu docs.kernel.org (trang ghi 7.4.0-rc2, truy cập 2026-11-10).
- **syntax/c (10)**: pycparser C99 với `c_wrap`/`c_typedefs`; kết quả kiểm bằng twin Python. Theo bản cổng 11:45Z, đã chuyển 7 khối C có chú thích từ `other` sang `syntax/c`.
- **Ca âm**: 6 lỗi cấy vào khối làm nguồn FAIL; bản ESY L01 cũ làm `src:ESY:L01_bits` FAIL.

## 2. Lỗi đã sửa (MUST 0, SHOULD 2)
| Khối | Mức | Trích nguyên chữ (cũ) | Vì sao sai + bằng chứng | Sửa thành | lint/render/verify |
|---|---|---|---|---|---|
| ESY L01 ops 0 0 | SHOULD | `bit = (reg >> 4) & 1;   // đọc bit 4  : 10010001 → 1` | Ba dòng đầu chạy nối tiếp; sau dòng 3 reg = 10011001 (153). `src:ESY:L01_bits` với bản cũ báo "chú thích ghi trước = 10010001, chạy thật reg = 10011001". Bit vẫn = 1 | `// đọc bit 4  : 10011001 → 1` + check `(153, '10011001', 1)`; lời đọc giữ nguyên | lint 0/0; render 78 khung 0 vấn đề; verify_esy 72/72 |
| CS112 L25 dsu 0 0 | SHOULD | `find(x):  if cha[x] != x:  cha[x] = find(cha[x]);   return cha[x]` (một dòng) | Theo quy ước của khoá (L08, L16, L17, L23: "`if …: A; B` thì B thuộc nhánh"), `return` rơi vào nhánh, nên find(gốc) không trả gì; gõ lại bằng Python sẽ sai | tách 3 dòng, sửa `focus`, `src:CS112:L25_dsu_twin` kiểm find(5) = 1, nén đường, hợp theo kích thước; `sync_tpl_from_lesson.py cs112 --write` 0 lệch | lint 0/0; render 79 khung 0 vấn đề; verify_cs112 FAIL 0; p2 37/0 |

**Không sửa**, để người điều phối biết:
- CS112 L10: `m = (l + r) / 2` dùng "/" là chia số nguyên theo quy ước bài 0, nhưng L10 không nhắc lại.
- CS112 L04: `fact(0)` không dừng; bài chỉ gọi với n ≥ 1.
- CSA L16: nhân Linux mới in chuỗi dài hơn "Mitigation: Enhanced IBRS"; bài đã ghi "một ví dụ kết quả".
- ESY L11: `queue_send_from_isr` / `queue_receive` / `WAIT_FOREVER` là tên chung. Tên FreeRTOS thật là `xQueueSendFromISR` / `xQueueReceive` / `portMAX_DELAY`.

## 3. unverified_claims (40)
- **CS112 (22)**: mọi khối, kiểm bằng 17 twin Python, độ trung thực INFERRED; hai khối C chưa chạy trình biên dịch C.
- **CSA (4)**:
  - L01: int8_t 127 + 1 = −128 kiểm bằng twin; theo C99 §6.3.1.3, việc đổi kiểu này do trình biên dịch quy định.
  - L07: "x86 tốn 4 lệnh mỗi vòng" chưa chạy trên x86.
  - L09: số bọt/chu kỳ từ mô hình Python.
  - L16: không chạy được `/sys` trên Windows.
- **OSY (8)**:
  - L01 ×4: mô phỏng fork bằng Python (Windows không có fork).
  - L05 ×3: máy trạng thái dịch từ văn bản nguyên văn.
  - L07: thứ tự an toàn P1, P3, P0, P2, P4.
- **BCH (3)**:
  - L01: bài không nói mã hoá chữ; dùng UTF-8.
  - L02: Merkle dùng chuỗi giao dịch mẫu.
  - L08: phí gas và huỷ khi hết đơn vị cần EVM.
- **ESY (3)**:
  - L01: twin Python của các phép bit.
  - L02: thứ tự đọc byte thấp trước là giả thiết của bài.
  - L11: hành vi chặn/ưu tiên cần RTOS thật.
- **NET (0)**.

`read_check` ghi "theo hiểu biết, chưa mở lại trong phiên" cho: RISC-V ISA 20191213, GCC manual, POSIX fork, Kurose & Ross, datasheet ATmega328P, avr-libc.

## 4. Kết quả (tác tử chạy)
- CS112: 22 khối — PASS 39 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0
- CSA: 13 khối — PASS 18 · 0 lỗi
- OSY: 12 khối — PASS 17 · 0 lỗi
- NET: 10 khối — PASS 14 · 0 lỗi
- BCH: 8 khối — PASS 12 · 0 lỗi
- ESY: 3 khối — PASS 5 · 0 lỗi

Bộ kiểm khoá: verify_esy 72/72; verify_cs112 {'PASS': 38, 'FIX': 15, 'FAIL': 0}; verify_cs112_p2 37/0.

Dựng lại: `lessons/esy/L01_thanh_ghi_bit.yaml`, `lessons/cs112/L25_cay_khung_nho_nhat.yaml` (chỉ đổi màn hình). Mẫu `audit/cs112/src/L25_cay_khung_nho_nhat.tpl.yaml` đã đồng bộ; bản cũ ở `out/_tpl_backup/cs112/`.

## 5. Đề xuất cho cổng
1. Kiểm `twin_of` trỏ tới khối có thật. **Đã làm** (người điều phối).
2. Docstring: `c_wrap` trong YAML nháy kép phải viết `\n`.
3. OSY chạy 1–2 phút vì `src:OSY:L05_prodcons` duyệt mọi xen kẽ.
