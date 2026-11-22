from pathlib import Path
import yaml

targets = {
    "lessons/gfx/L06_chieu_sang.yaml": (
        "    say: 'Tổng kết bài học, mô hình chiếu sáng cục bộ gồm ba thành phần rõ ràng. Ánh sáng môi trường giữ vùng khuất không đen kịt, khuếch tán phụ thuộc góc nguồn sáng, và bóng sáng dùng vector nửa đường. Điểm cốt lõi dễ sai là quên chuẩn hoá lại pháp tuyến trên từng mảnh sau nội suy. Hai mức quy mô minh hoạ rất rõ. Tô một quả cầu vài trăm mảnh thì cách viết nào cũng chạy nhẹ. Vẽ 2 triệu điểm ảnh ở 60 khung hình mỗi giây đòi hỏi vector nửa đường gọn nhẹ.'",
        [1, 1, 1, 2, 2, 2],
        "    say: Ở bài 7 tới, ta học về kết cấu bề mặt và cách lấy mẫu bằng nội suy song tuyến cùng mipmap chống răng cưa. Ta sẽ dán các bức ảnh chi tiết thực tế lên mô hình ba chiều thay cho hằng số màu. Hẹn gặp bạn ở video tiếp theo.",
        [1, 1, 1],
    ),
    "lessons/gfx/L13_hanh_trinh_chieu_sang.yaml": (
        "    say: 'Tổng kết khoá học Đồ hoạ máy tính, ta đã đi từ phép biến đổi toạ độ tới chiếu sáng vật lý. Nửa đường đầu giúp hiểu cắt khung nhìn, nội suy tam giác và bộ đệm độ sâu. Nửa đường sau đi vào chiếu sáng, dò tia và tối ưu hiệu năng bộ xử lý đồ hoạ. Hai mức quy mô lịch sử cho thấy bước nhảy vọt. Máy cổ năm 1975 chỉ chạy được mô hình kinh nghiệm cục bộ trên từng vật thể đơn lẻ. Trò chơi 60 khung hình mỗi giây ngày nay ghép vật liệu vật lý và khử nhiễu trong đúng 16 phẩy 67 mi li giây.'",
        [1, 1, 1, 2, 2, 2],
        "    say: Tư duy chuyên gia cần mang theo là đồ hoạ không chỉ nhằm vẽ cho đẹp bất chấp thời gian. Đó là nghệ thuật tính toán ngân sách 16 mi li giây để giữ phép toán chính xác ở chỗ mắt dễ thấy nhất. Khi nắm chắc bản chất từ ma trận tới dò tia, bạn tự tin đọc hiểu mọi kỹ thuật mới. Chúc mừng bạn đã hoàn thành trọn vẹn khoá học!",
        [1, 1, 1, 1],
    ),
    "lessons/bch/L08_hop_dong_thong_minh.yaml": (
        "    say: 'Tổng kết lại, hợp đồng là một máy trạng thái chạy công khai trên chuỗi. Mỗi hàm quy định rõ ai được gọi và hợp lệ ở trạng thái nào. Hợp đồng bắt buộc tất định để mọi nút tính ra cùng kết quả, phí tính theo đơn vị tính toán, và phải kiểm kỹ trước khi triển khai. Hai mức quy mô cho thấy chi phí vận hành. Chuyển khoản khi mạng vắng rất rẻ. Lúc mạng nghẽn, hợp đồng ghi nhiều trạng thái làm phí tăng vọt.'",
        [1, 1, 1, 2, 2, 2],
        "    say: Điều cần mang theo là nguyên tắc mã là luật cũng có nghĩa lỗi trong mã lập tức trở thành luật thực thi. Vì vậy phải rà soát biên cẩn trọng như khi soạn một hợp đồng pháp lý thật.",
        None,
    ),
}

for pstr, (s0_line, f0, s1_line, f1) in targets.items():
    p = Path(pstr)
    lines = p.read_text(encoding="utf-8").splitlines()
    rec_idx = next(i for i, l in enumerate(lines) if l.strip() == "- id: recap")
    # find step 0 say/focus and step 1 say/focus after rec_idx
    step = -1
    out = []
    i = 0
    while i < len(lines):
        if i > rec_idx:
            if lines[i].startswith("  - show:") or lines[i].startswith("  - clear:"):
                step += 1
            if lines[i].startswith("    say:") and step in (0, 1):
                out.append(s0_line if step == 0 else s1_line)
                i += 1
                continue
            if lines[i].startswith("    focus:") and (step == 0 or (step == 1 and f1 is not None)):
                out.append("    focus:")
                i += 1
                while i < len(lines) and lines[i].startswith("    - "):
                    i += 1
                for fv in (f0 if step == 0 else f1):
                    out.append(f"    - {fv}")
                continue
        out.append(lines[i])
        i += 1
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    yaml.safe_load(p.read_text(encoding="utf-8"))
    print("Patched:", pstr)
