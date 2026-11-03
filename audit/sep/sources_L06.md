# Nguồn đã đọc nguyên văn cho SEP L06 (tác động môi trường của tính toán)

Đọc ngày 2026-11-02 (tải bằng curl từ arxiv.org và acm.org, trích chữ bằng pdftotext; câu dưới đây chép nguyên văn từ bản trích).
Tình huống 8 thiết bị × 0,4 kW × 720 giờ × PUE 1,2, hệ số 0,5 kg/kWh, phần phục vụ 10 kWh/ngày, câu quiz 16 × 0,3 kW × 240 giờ ×
PUE 1,5, c = 0,4 là SỐ MINH HOẠ; mọi phép tính lại ở `checks` và `audit/sep/verify_parts/L06.py`.

## [S19] E. Strubell, A. Ganesh, A. McCallum, *Energy and Policy Considerations for Deep Learning in NLP*, ACL 2019
Tải: https://arxiv.org/pdf/1906.02243
- §2: “We estimate total power consumption as combined GPU, CPU and DRAM consumption, then multiply this by Power Usage Effectiveness
  (PUE), which accounts for the additional energy required to support the compute infrastructure (mainly cooling).”
- §2: “We use a PUE coefficient of 1.58, the 2018 global average for data centers (Ascierto, 2018).”
- §2: “We train the models described in §2.1 using the default settings provided, and sample GPU and CPU power consumption during training.”

## [P21] D. Patterson và cộng sự, *Carbon Emissions and Large Neural Network Training* (2021)
Tải: https://arxiv.org/pdf/2104.10350
- §2.3: “A useful quantitative metric of datacenter efficiency is the energy overhead above and beyond what directly powers the computing
  equipment inside the datacenters. If the overhead were 50%, the Power Usage Effectiveness (PUE) would be 1.50. The US national
  datacenter average in 2018 was 1.58, which is the value [Str19] used; In 2020, it was 1.59. … The PUE for the Iowa datacenter where we
  ran Evolved Transformer is 1.11”.
- §2.4: “The gross carbon intensity of energy according to the U.S. average mix is 0.429 kg of CO2e/KWh [USE21].”
- Bảng 4, dòng “Datacenter Gross CO2e/KWh (kg/KWh when it was run)”: 0.431, 0.545, 0.415, 0.201, 0.403, 0.429 (thấp nhất 0,201, cao nhất 0,545).

## [P22] D. Patterson và cộng sự, *The Carbon Footprint of Machine Learning Training Will Plateau, Then Shrink* (2022)
Tải: https://arxiv.org/pdf/2204.05149
- “We retroactively performed these calculations based on data for one week of April in 2019, 2020, and 2021. Each time the ML portion
  was 10% to 15% of Google's total energy consumption for that week … Across all three years, about ⅗ of ML energy use is for inference
  and ⅖ for training.”
- Tóm tắt: “Inference represents about ⅗ of total ML energy usage at Google, owing to the many billion-user services that use ML.”

## [ACM18] ACM Code of Ethics (2018), nguyên tắc 1.1
Tải: https://www.acm.org/binaries/content/assets/about/acm-code-of-ethics-and-professional-conduct.pdf
- “In addition to a safe social environment, human well-being requires a safe natural environment. Therefore, computing professionals
  should promote environmental sustainability both locally and globally.”

## Ghi chú đối chiếu
- [S19] gọi 1,58 là “2018 global average”, còn [P21] gọi là “US national datacenter average in 2018” cho cùng con số. Bài giảng chỉ
  dùng cách nói của [P21] (trung bình ở Mỹ), có ghi nguồn trên màn hình; không nói “trung bình thế giới”.

## Điều KHÔNG dạy (nguồn không ghi hoặc chưa đọc)
- Không nêu hệ số phát thải của lưới điện Việt Nam (chưa đọc nguồn chính thức) — dùng 0,5 là số minh hoạ.
- Không nêu tỉ lệ ⅗ / ⅖ cho công ty khác ngoài Google; không nói “mọi mô hình phục vụ tốn hơn huấn luyện”.
- Không nêu công suất thật của một loại bộ xử lý cụ thể.
