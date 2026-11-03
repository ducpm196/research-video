# Nguồn đã đọc nguyên văn cho CAS L03 (Mars Climate Orbiter, 23/9/1999)

Đọc ngày 2026-11-02. Bản tải để ở thư mục nháp của phiên, không đưa vào kho. Chỉ trích câu bài giảng dựa vào (CITED); số khác là phép
tính lại (VER: `checks`, `audit/cas/ver/L03.py`, `audit/verify_plan_curricula.py` CAS:L03) hoặc ghi “(số minh hoạ)”.

## [MIB99] Mars Climate Orbiter Mishap Investigation Board, *Phase I Report*, 10/11/1999
Tải: llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf (HTTP 200, 1 460 534 byte; bản PDF của NASA Lessons Learned, đọc bằng pdftotext).
sunnyday.mit.edu/accidents/MCO_report.pdf: hết thời gian kết nối (không cần).
- “The MCO was launched on December 11, 1998, and was lost sometime following the spacecraft's entry into Mars occultation during the Mars
  Orbit Insertion (MOI) maneuver. The spacecraft's carrier signal was last seen at approximately 09:04:52 UTC on Thursday, September 23, 1999.”
- “the root cause for the loss of the MCO spacecraft was the failure to use metric units in the coding of a ground software file, "Small
  Forces," used in trajectory models.” “The data in the AMD file was required to be in metric units per existing software interface
  documentation, and the trajectory modelers assumed the data was provided in metric units per the requirements.”
- “These Angular Momentum Desaturation (AMD) events occurred 10-14 times more often than was expected by the operations navigation team. This
  was because the MCO solar array was asymmetrical relative to the spacecraft body … This asymmetric effect significantly increased the
  Sun-induced (solar pressure-induced) momentum buildup on the spacecraft.”
- “At the time of Mars insertion, the spacecraft trajectory was approximately 170 kilometers lower than planned.”
- “The Board recognizes that mistakes occur on spacecraft projects. However, sufficient processes are usually in place on projects to catch
  these mistakes before they become critical to mission success. Unfortunately for MCO, the root cause was not caught by the processes in-place”
- Hình tóm tắt nhiệm vụ: “629 kg launch mass”; “Launch 12/11/98”; “Arrival 9/23/99”.
- Mục 2: “Throughout spring and summer of 1999, concerns existed at the working level regarding discrepancies observed between navigation
  solutions. Residuals … was noted but only informally reported.” “The Doppler-only solutions consistently indicated a flight path insertion
  closer to the planet. These discrepancies were not resolved.”
- “TCM-4 … the first periapse altitude … would be at a distance of 226km.” “TCM-4 was executed as planned on September 15, 1999.”
  “the first periapse distance had decreased to the range of 150-170km”; “Approximately one hour prior to MOI … calculated to be as low as
  110km. The minimum periapse altitude considered survivable by MCO is 80 km.”
- “The MOI engine start occurred at 09:00:46 (UTC) on September 23, 1999. … loss of signal at 09:04:52 (UTC), which occurred 49 seconds
  earlier than predicted.”
- “On September 29, 1999, it was discovered that the small forces V's … was low by a factor of 4.45 (1 pound force=4.45 Newtons) because
  the impulse bit data contained in the AMD file was delivered in lb-sec instead of the specified and expected units of Newton-sec.” “… an
  initial periapsis (lowest point of orbit) of 57 km which was judged too low for spacecraft survival.”
- Mục 5: “the Board determined that there were 8 contributing causes”. “The Software Interface Specification (SIS) … specifies the units
  associated with the impulse bit to be Newton-seconds (N-s).” “The AMD software installed on the spacecraft used metric units for the
  computation and was correct.” “Mismodeling only occurred in the ground software.” “the navigation software underestimated the effect of the
  thruster firings on the spacecraft trajectory by a factor of 4.45”. Mục 4: “The SIS, which was not followed, defines both the format and
  units of the AMD file”.
- “During the first four months of the MCO cruise flight, the ground software AMD files were not used … because of multiple file format
  errors … the operations navigation team used email from the contractor to notify them when an AMD desaturation event was occurring”;
  “it was not until April 1999 … Almost immediately (within a week) it became apparent that the files contained anomalous data that was
  indicating underestimation of the trajectory perturbations due to desaturation events.”
- “A request to perform a TCM-5 was discussed verbally shortly before the MOI onboard procedure was initiated, but was never executed.”
- Khuyến nghị: “verify the consistent use of units throughout the MPL spacecraft design and operation. The Board recommends a software audit
  for SIS compliance on all data transferred between the JPL operations navigation team and the spacecraft operations team.” “several other
  navigation methods should be compared to the prime navigation method”.

## [NIST] NIST SP 811, Phụ lục B.8 (www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8, HTTP 200)
- “pound-force (lbf) … newton (N) 4.448 222 E+00”; “pound (avoirdupois) (lb) … kilogram (kg) 4.535 924 E-01”; “acceleration of free fall,
  standard (g n) … 9.806 65 E+00”. Bài: 0,4535924 × 9,80665 ≈ 4,4482 (VER).

## Phép tính của bài (VER)
- 1/4,448 ≈ 22,5% thấy được, 77,5% bỏ sót (mọi x); 226 − 57 = 169 ≈ “170 km”; 80 − 57 = 23; 09:00:46 → 09:04:52 = 4 phút 6 giây.
- Xung 10 lbf·s mỗi lần, 100 lần đốt: SỐ MINH HOẠ; 629 kg là khối lượng LÚC PHÓNG (bài ghi rõ, phép tính chỉ minh hoạ cơ chế).
- Mã lớp XungLuc trên màn hình: chép nguyên văn từ tệp bài và chạy trong `audit/cas/ver/L03.py` (L03g).

## Điều KHÔNG dạy (nguồn không ghi)
- Xung lực thật của mỗi lần đốt, số lần đốt thật, khối lượng tàu lúc tới sao Hoả: báo cáo không ghi → chỉ số minh hoạ.
- Tàu cháy trong khí quyển hay văng ra không gian: báo cáo ghi “either was destroyed in the atmosphere or re-entered heliocentric space”
  → bài chỉ nói “không bao giờ trở lại”.
- Tên nhà thầu và cơ quan chỉ ở `source`/màn hình (JPL, nhà thầu) — lời đọc nói “đội dẫn đường”, “đội vận hành tàu của nhà thầu”; không nêu tên người.
