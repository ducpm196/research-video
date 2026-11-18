# fix5 part B: BNX L12-L23 (tac tu sua vong 5, 2026-11-15)

## Tien do
- Xong 12/12 bai (sua NGUON audit/bnx/src/l12..l23.py, gen.py tung bai, khong sua tay YAML). Gate tung bai da chay; L19 chua chay verify/screen_fast (can Docker/Redis: NOT_VERIFIED).
- Cong cuoi da chay: lab_gate BNX 39 PASS 0 FAIL (196 lab); tests/test_e52.py 0 FAIL; arith_scan BNX 58 phep tinh 0 FAIL; check_course_refs BNX 0 van de; check_next_refs 550 loi hen 0 lech; `lv.py curriculum curriculum/bnx.yaml` xem muc "Cong cuoi" cuoi tep.

## Bang tung bai
Tu loi doc = dem tach khoang trang toan bo `say` (cung cach fix4_wc). lint/render/verify/screen la ket qua that cua lan chay cuoi cua bai do.

| Bai | Muc P1 da giang (tren man hinh + loi) | Muc bo/don gian hoa | Con lai (uoc luong) | Tu loi truoc -> sau | lint | render | verify_bnx | screen_fast |
|---|---|---|---|---|---|---|---|---|
| L12 | bang gan nhieu bien `bao_dam, vi = ...` | | 0 | 2293 -> 2298 | 0/0 | 0 | PASS (31 dong) | 17 PASS, 0 FAIL |
| L13 | `c, r, k = s = todo.pop()`; so nguyen lam dieu kien (`if k:`, `if c and`); "jre" (hang bang the anh) | | 0 | 2294 -> 2300 | 0/0 | 0 | PASS | 19 PASS, 0 FAIL |
| L14 | "HTTP" (cach chuong trinh hoi dap qua mang, ca trong bang va loi) | | 0 | 2297 -> 2295 | 0/0 | 0 | PASS (26) | 9 PASS (lan dau; khong doi khoi ma) |
| L15 | `j = top = 0`, `def cung_luc(tps, w=40_000)`, `return`; "be tac"; bang thanh phan -> yeu cau -> danh doi | | 0 | 2299 -> 2257 | 0/0 | 0 | PASS (26 dong, them kiem 115,74 va 4,63) | 10 PASS, 0 FAIL |
| L16 | `throws Exception`, `extends RecursiveTask<Long>`, `import static`, `List<Integer>`/`var` (tach 2 buoc, moi hang co loi) | | 0 | 2297 -> 2290 | 0/0 | 0 | PASS (32) | 35 PASS, 0 FAIL |
| L17 | GET/POST, `Authorization: Bearer`, `WWW-Authenticate`; `javac -d out`, `java -D...`, dau `;` ngan duong tim | | 0 | 2256 -> 2298 | 0/0 | 0 | PASS (34) | 37 PASS, 1 MISSING (khoi cu, xem muc dieu phoi) |
| L18 | `import static`, `javac -d out`, `execute --class-path --select-class`, co trinh bay `--disable-banner --disable-ansi-colors --details-theme ascii`, `--details summary`; `L=lib; $L`, lap `-cp`, `\` cuoi dong | khong doi lenh (output that gan voi co) | 0 | 2299 -> 2299 | 0/0 | 0 | PASS (27) | 23 PASS, 0 FAIL |
| L19 | co `docker run -d --name`, `redis-server --port/--cluster-enabled/--cluster-config-file/--daemonize`, `redis-cli --cluster create ... --cluster-yes`, `grep -E`; `D=...; $D`; `r() {... "$@"}`, `--no-raw`; `sh -c`, `$c`, `MSET`; sym.2 doc tung hang | | 1 (cac co phu) | 2295 -> 2294 | 0/0 | 0 | KHONG CHAY (Docker/Redis): NOT_VERIFIED | KHONG CHAY; screen_keep chay: 18 khoi, chua khop 0 |
| L20 | con tro `*` (`r *http.Request`, `c *fiber.Ctx`), `Header().Set("Content-Type", ...)`; `strings.Cut`, `http.DefaultClient.Do`, `io.ReadAll`/`Body.Close`; `for ... range` tren kenh (hang bang cu phap); `go mod init`/`go get` (chu thich tren man hinh); sym.1 doc tung hang | | 1 (go mod/go get chi tren man hinh, khong doc) | 2285 -> 2296 | 0/0 | 0 | PASS (34) | 52 PASS, 0 FAIL |
| L21 | `printf ... > tep`, `sed 's/../../'`, `cp`; `openssl rsa -pubout`, `dgst -sign ... -out`, `-verify ... -signature`; `dict(a, k=v)`; `"|".join(... sorted(...))`; `sum(x != y for ... zip)` | | 0-1 | 2299 -> 2297 | 0/0 | 0 | PASS | 24 PASS, 0 FAIL |
| L22 | `MA.get(c, c)`, `"".join(...)`, mau regex trong `re.sub` va `m.group(1)`; getter `getTieuDe()` <-> `${trang.tieuDe}`; `type(x) is dict` | | 0-1 | 2300 -> 2293 | 0/0 | 0 | PASS (34) | 28 PASS, 0 FAIL |
| L23 | cat lat `a[1000:]`, `a[:1000]`; mat na `(nhan == -1).sum()`; `d[d <= c]`, `A if dk else B`, `rng.uniform`, `while len(d) > 1`; `open(...,"wb").write`, `get_inputs()[0].name`, `run(None, {...})`, gan doi; `pip install ==` (chu thich man hinh) | | 1 (pip chi tren man hinh) | 2298 -> 2297 | 0/0 | 0 | PASS (khong dong non-PASS) | 37 PASS, 0 FAIL |

Diem P1 du kien: L12-L18 dat 2 (0 muc); L19-L23 con 0-1 muc nhe nen toi thieu 1, co the 2 (cho nguoi doc cham lai). Muc "con lai" chu yeu la thong tin chi co tren man hinh khong doc thanh loi (go mod/go get, pip ==, co phu cua redis) - da bo vi khong du tran tu.

## Bai nao doi (can dung lai build/tts/asr)
TAT CA 12 bai L12-L23 doi noi dung (them step/cau say moi hoac sua loi): L12, L13, L14, L15, L16, L17, L18, L19, L20, L21, L22, L23. Rieng cac cau `say` moi/doi la cau TTS moi can nghe lai ASR: nhat la "con tro", "tieu de", "cat lat", "mat na", "ONNX", "chu hoa dat thong so", "bien bang ten thu muc".

## SHOULD
- Da sua: L15 example step 4-5 (5 = 115,74 x 0,040 xap xi 4,63; thong nhat voi 2 va de.md; ca src, checks, ver/l15.py, claims, mong doi ban Python in 4.63; ket luan "khoang 5 lenh" khong doi; o quymo ghi chu tren man hinh rang tai da lam tron 116 x 0,040 = 4,64 chi chenh do lam tron); L15 muc tieu 3 (them bang thanh phan -> yeu cau -> danh doi, KHONG sua muc tieu nen khong dong curriculum/bnx.yaml); L21 [TT37] them vao audit/bnx/sources_l21.md (Thong tu 37/2025/TT-NHNN ngay 31/10/2025, hieu luc 15/12/2025, sua doi TT 31/2024/TT-NHNN; nguon sbv.gov.vn, thuvienphapluat.vn, english.luatvietnam.vn; 2026-11-15 qua nguoi doc R3; CITED thu cap; khong ghi so dieu); L19 example step 7: chon cach ghi nhan, tieu de khung ket qua nay ghi "(da luoc cac dong -> Redirected ... ma redis-cli -c in them)"; khong bia dau ra Redis; ver/l19.py khong doi; L16 sym step 2 tach 2 buoc, doc tung hang; L19 sym.2 doc tung hang; L18 sym.2 them cac y con thieu; L20 sym.1 doc tung hang.
- Khong sua: L18 sym.0/sym.1 va L20 sym.0 (bang 4-8 hang): da co 3-5 cau doc kem focus theo hang, them nua vuot tran tu; L19 sym.0/sym.1 tuong tu (3 va 4 hang, 3 va 2 cau). L12/L16 P1 da dat nen khong them ngoai muc da neu.

## Thay doi tep chung va dieu phoi can lam
- Tep chung: KHONG sua symbols.BNX.yaml, gen.py, lib*.py, screen_code/BNX.yaml, curriculum. Them 1 muc [TT37] vao cuoi audit/bnx/sources_l21.md (tep rieng L21). Sua ver: audit/bnx/ver/l15.py (kiem moi cho 5). Khong sua checklib.
- So screen: da chay screen_keep cho L12-L23; cac tep audit/bnx/screen/l19.yaml..l23.yaml, l12..l18 duoc sinh lai. Chen step lam lech khoa nen sua tay trong tep rieng cua bai (chi doi khoa tham chieu cheo, khong doi noi dung kiem): l21.yaml muc "formula 13 0" `within` -> `BNX L21 formula 14 0`; l22.yaml nguon `L22_model` `TrangModel.java` -> `BNX L22 formula 11 0`; l23.yaml 3 `within` (-> formula 6 0, 8 0, 14 0). Dieu phoi kiem lai khi gop vao audit/review/screen_code/BNX.yaml bang screen_try.py --merge.
- Con thieu muc so: `BNX L17 example 15 1` (ket qua ca E, dau ra that `L17_spring`, dong Bearer luoc bang "..."): can stub roi dien `kind: output, of: src:BNX:L17_spring` (khoa nay dich tu 13 1 sang 15 1 do chen 2 step).
- L19: chay verify_bnx.py L19 va screen_fast.py L19 khi may co Docker; Redis song NOT_VERIFIED (them: khoi dau ra `r -c SET/GET` van thieu 2 dong Redirected tren man hinh, da ghi nhan).
- Dung lai build/tts/asr cho 12 bai tren.

## Cong cuoi (do that 2026-11-15)
- lab_gate BNX: 39 PASS, 0 FAIL (196 lab). tests/test_e52.py: 0 FAIL. arith_scan BNX: 58 phep tinh, 0 FAIL. check_course_refs BNX: 0 van de. check_next_refs: 550 loi hen, 0 lech. `lv.py curriculum curriculum/bnx.yaml`: 39 bai, 39 co dac ta, 0 loi.
- Khung PNG da xem: L15 (bang thanh phan, 00030), L17 (bang GET/POST/Bearer, 00044), L13 (bang gan chuoi, 00064): dung bo cuc, khong tran.
