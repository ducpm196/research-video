# Nguồn bài GFX L13 — Hành trình: chiếu sáng từ mô hình kinh nghiệm năm 1975 tới kết xuất dựa trên vật lý thời gian thực

Đọc nguyên văn và đối chiếu 2026-11-03. Nhãn dùng trong `source` và `stage.source` của bài `lessons/gfx/L13_hanh_trinh_chieu_sang.yaml`.

## [PH75] B. T. Phong, “Illumination for Computer Generated Pictures”, Communications of the ACM, Vol. 18, No. 6, pp. 311–317 (1975) & [BL77] J. F. Blinn, “Models of Light Reflection for Computer Synthesized Pictures”, Computer Graphics (SIGGRAPH '77 Proceedings), Vol. 11, No. 2, pp. 192–198 (1977)
- **Chặng 1 (1975–1977):**
  - Trước năm 1975, bề mặt đa giác thường chỉ được tô phẳng một màu mỗi mặt hoặc nội suy độ sáng khuếch tán giữa các đỉnh (Gouraud, 1971), làm mất hoặc méo vệt bóng sáng trên vật bóng.
  - Bùi Tường Phong (1975) đề xuất nội suy pháp tuyến qua bề mặt đa giác và mô hình chiếu sáng cục bộ gồm ba thành phần: môi trường (*ambient*), khuếch tán theo cô-sin góc tới, và bóng sáng phản xạ dùng luỹ thừa bậc $s$ của cô-sin góc lệch phản xạ.
  - James F. Blinn (1977) đưa vào vector nửa đường $\mathbf{h} = \frac{\mathbf{l} + \mathbf{v}}{\|\mathbf{l} + \mathbf{v}\|}$ nằm chính giữa hướng nguồn sáng $\mathbf{l}$ và hướng nhìn $\mathbf{v}$, tính phần bóng sáng bằng $(\mathbf{n} \cdot \mathbf{h})^s$ (với $\mathbf{n} \cdot \mathbf{h} = 0{,}95$: $s = 32 \Rightarrow 0{,}95^{32} \approx 0{,}194$; $s = 128 \Rightarrow 0{,}95^{128} \approx 0{,}0014$).

## [WH80] T. Whitted, “An Improved Illumination Model for Shaded Display”, Communications of the ACM, Vol. 23, No. 6, pp. 343–349 (1980) & [KA86] J. T. Kajiya, “The Rendering Equation”, Computer Graphics (SIGGRAPH '86 Proceedings), Vol. 20, No. 4, pp. 143–150 (1986)
- **Chặng 2 (1980–1986):**
  - Điểm nghẽn của mô hình cục bộ 1975–1977: mỗi bề mặt chỉ nhìn thông tin tại chính điểm đó và hướng đèn trực tiếp, không biết vật khác có che đèn hay phản chiếu vào nó không.
  - Whitted (1980) mở rộng thành cây tia đệ quy:
    > “In a simplified form, this information is stored in a tree of "rays" extending from the viewer to the first surface encountered and from there to other surfaces and to the light sources.”
    > “A point on a surface lies in shadow if it is visible to the viewer but not visible to the light source.”
  - Kajiya (1986) viết quá trình truyền sáng thành một phương trình tích phân trên các bề mặt của cảnh (bao quát nhiều thuật toán kết xuất đã biết) và giải bằng dò đường ngẫu nhiên (*Monte Carlo path tracing*):
    > “We present an integral equation which generalizes a variety of known rendering algorithms. In the course of discussing a monte carlo solution we also present a new form of variance reduction, called Hierarchical sampling…”
  - Quy luật hội tụ của lấy mẫu ngẫu nhiên: độ lệch chuẩn của sai số trung bình $N$ mẫu độc lập giảm theo $\frac{1}{\sqrt{N}}$. Muốn giảm mức nhiễu hạt đi $10$ lần, số tia mỗi điểm ảnh phải tăng gấp $10^2 = 100$ lần (ví dụ từ $16$ tia lên $1600$ tia mỗi điểm ảnh).

## [SC94] C. Schlick, “An Inexpensive BRDF Model for Physically-based Rendering”, Computer Graphics Forum, Vol. 13, No. 3, pp. 233–246 (1994)
- **Chặng 3 (1994):**
  - Điểm nghẽn khi đưa các mô hình phản xạ vật lý vào kết xuất nhanh: phương trình phản xạ điện từ chính xác theo góc tới và chiết suất chứa nhiều phép lượng giác và căn bậc hai nặng nề, còn mô hình kinh nghiệm cũ thì cho phép cộng tuỳ ý khuếch tán với phản xạ làm vật phát ra nhiều năng lượng hơn ánh sáng chiếu tới.
  - Schlick (1994) đưa ra xấp xỉ luỹ thừa bậc năm vừa rất nhẹ (chỉ nhân cơ bản) vừa bám sát đường cong vật lý:
    $$F(\theta) = F_0 + (1 - F_0)(1 - \cos\theta)^5, \qquad F_0 = \left(\frac{n - 1}{n + 1}\right)^2$$
    Với chất điện môi có chiết suất $n = 1{,}5$ (nhựa, thuỷ tinh): $F_0 = \left(\frac{1{,}5 - 1}{1{,}5 + 1}\right)^2 = 0{,}04$; tại góc $60^\circ$ ($\cos 60^\circ = 0{,}5$), $F = 0{,}04 + 0{,}96 \cdot 0{,}5^5 = 0{,}07$; phần năng lượng còn lại cho khuếch tán là $1 - F = 0{,}93$.

## [BU12] B. Burley, “Physically-Based Shading at Disney”, SIGGRAPH 2012 Course: Practical Physically-Based Shading in Film and Game Production (2012) & [KA13] B. Karis, “Real Shading in Unreal Engine 4”, SIGGRAPH 2013 Course: Physically Based Shading in Theory and Practice (2013)
- **Chặng 4 (2012–2013):**
  - Điểm nghẽn ở quy mô sản xuất phim và trò chơi lớn: hoạ sĩ phải chỉnh hàng chục tham số kinh nghiệm rời rạc cho từng vật liệu dưới từng cảnh sáng khác nhau; đổi ánh sáng từ ngoài trời vào trong nhà là vật liệu trông giả và phải chỉnh lại bằng tay.
  - Burley (2012) và Karis (2013) chuẩn hoá bộ tham số vật liệu dựa trên vật lý: màu gốc (`BaseColor`), độ kim loại (`Metallic` $\in [0, 1]$, thường là $0$ cho phi kim hoặc $1$ cho kim loại), và độ nhám cảm nhận (`Roughness` $r \in [0, 1]$):
    > “Our material model is a simplification of Disney's, with an eye towards efficiency for real-time rendering.” [KA13]
    > “We also adopted Disney's reparameterization of $\alpha = \text{Roughness}^2$.” [KA13]
    > “We found variable index of refraction (IOR) to be fairly unimportant for nonmetals... F0 of nonmetals is now a constant 0.04.” [KA13]
  - Với độ nhám cảm nhận $r = 0{,}5$, tham số độ nhám vi diện là $\alpha = r^2 = 0{,}25$ (giúp thanh trượt từ $0$ tới $1$ thay đổi độ bóng đều mắt người hơn). Với phi kim (`Metallic` $= 0$), $F_0$ giữ cố định bằng $0{,}04$, phần khuếch tán nhân $(1 - F) = 0{,}93$ ở $\cos\theta = 0{,}5$; với kim loại (`Metallic` $= 1$), khuếch tán bằng $0$ và $F_0$ lấy trực tiếp từ màu gốc.

## Điều KHÔNG dạy / NOT_VERIFIED
- Không đi sâu cài đặt bảng tra cứu tích phân tách đôi (*split-sum approximation LUT*) cho chiếu sáng môi trường của Karis (2013).
- Các con số ngân sách dự án ở phần tự làm (trò chơi di động 60 khung mỗi giây, trò chơi máy tính có thẻ đồ hoạ rời, phim hoạt hình kết xuất ngoại tuyến) là SỐ MINH HOẠ để người học luyện ra quyết định chọn mô hình theo quy mô và ngân sách.

## Đối chiếu nguồn mở (đợt C, 2026-11-09)
- [BU12] notes v3 (link ở sources_L10.md) §5.4 “Specular D details”, nguyên văn: “For roughness, we found that mapping α = roughness² results in a more perceptually linear change in the roughness.” → phép bình phương độ nhám do Burley 2012 đề xuất; [KA13] nguyên văn “We also adopted Disney's reparameterization of α = Roughness².” Bài trước ghi “Bình phương độ nhám [KA13]” → sửa thành “đề xuất trong [BU12], được [KA13] dùng lại”.
- [KA13] về độ kim loại: hỏi “Is Metallic binary?”, tác giả viết nên trả lời là có — khớp cách bài coi m ∈ {0, 1}.
- [KA86]: câu trích “We present an integral equation which generalizes a variety of known rendering algorithms” (đợt trước) — phương trình của Kajiya viết dạng tích phân trên các bề mặt của cảnh (ánh sáng giữa hai điểm), không phải “trên bán cầu”; bài và ghi chú trên đã sửa: “bao quát được nhiều thuật toán kết xuất đã biết” thay vì “thống nhất mọi hiện tượng truyền sáng … trên bán cầu”. Chưa mở lại bài báo gốc trong đợt này (dựa vào câu trích đợt trước và dạng phương trình chuẩn).
- Đợt C sửa thêm: “phần khuếch tán nhận đúng 93%” → tối đa 93%; “sai màu hoàn toàn” → trông sai, phải chỉnh tay; “năm 2012 chuẩn hoá toàn bộ vật liệu” → bộ tham số vật liệu cho phim và trò chơi; “sự ra đời của kỹ thuật dò tia” → dò tia đệ quy (dò tia dạng bắn tia đã có trước 1980).
