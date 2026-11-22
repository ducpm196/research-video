import glob
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")

# Exact string replacements in lessons/{aif,irs,agt,llm,rln,cvi}/*.yaml
PATCHES = {
    "lessons/aif/L02_a_sao.yaml": [
        ("vài trăm nút (~1 ms)", "vài chục đến trăm nút (< 1 mi-li-giây)"),
    ],
    "lessons/aif/L04_tim_kiem_cuc_bo.yaml": [
        ("Với 4 hậu (8 bước) kiểm chứng bằng tay được, còn với 10 000 hậu hay xếp lịch nhà máy (cây 10^40000), leo đồi + khởi động lại chạy trong vài giây với bộ nhớ O(N)",
         "Với 4 hậu (8 bước thử) kiểm chứng bằng tay được, còn với 10 000 hậu hay xếp lịch nhà máy (cây $10^{40000}$), leo đồi + khởi động lại chạy trong vài giây với bộ nhớ $O(N)$ (tuyến tính theo số biến)"),
    ],
    "lessons/aif/L05_thoa_rang_buoc.yaml": [
        ("3^7 = 2 187 cách gán, còn bài lập lịch 100 biến có 3^100 trạng thái",
         "$3^7 = 2\\,187$ cách gán, còn bài lập lịch 100 biến có $3^{100}$ trạng thái"),
    ],
    "lessons/aif/L08_logic_menh_de.yaml": [
        ("(2^100 > 10^30 mô hình)", "($2^{100} > 10^{30}$ mô hình)"),
    ],
    "lessons/aif/L09_suy_dien_tien_lui.yaml": [
        ("trong khi liệt kê mô hình tốn 2^1000 bước.",
         "trong khi liệt kê mô hình tốn $2^{1000}$ bước."),
        ("      <tr><td>ở mô hình đó, $Q$ đúng?</td><td>đúng → KB kéo theo Q ✓</td></tr></table>",
         "      <tr><td>ở mô hình đó, $Q$ đúng?</td><td>đúng → KB kéo theo Q ✓</td></tr>\n"
         "      <tr><td>so sánh 2 chiều</td><td>đi tiến suy mọi hệ quả từ sự kiện; đi lùi chỉ kiểm 1 mục tiêu Q</td></tr></table>"),
    ],
    "lessons/aif/L10_lap_ke_hoach.yaml": [
        ("(~10^150 trạng thái)", "($\\approx 10^{150}$ trạng thái)"),
    ],
    "lessons/aif/L11_mang_bayes.yaml": [
        ("2^50 số đồng thời", "$2^{50}$ số đồng thời"),
    ],
    "lessons/aif/L12_lap_gia_tri.yaml": [
        ("Lưới nhỏ 12 trạng thái hội tụ sau 30 vòng (~1 ms), còn bài toán điều khiển robot có hàng triệu trạng thái làm lặp bảng O(|S|²|A|) quá chậm",
         "Lưới 4×3 (11 ô đi được, 1 ô tường) hội tụ sau 30 vòng (~1 mi-li-giây), còn bài toán điều khiển robot có hàng triệu trạng thái làm lặp bảng $O(|S|^2|A|)$ (tỉ lệ bậc hai theo số trạng thái) quá chậm"),
    ],
    "lessons/aif/L13_tong_hop.yaml": [
        ("Cờ vua 80 nước sâu ~10^123 nút (không thể duyệt hết), cắt sâu 4 + alpha–beta còn ~2 449 nút",
         "Cờ vua 80 nước sâu $\\approx 10^{123}$ nút (không thể duyệt hết), cắt sâu 4 kết hợp tỉa nhánh alpha–beta (cắt nhánh kém từ sớm) còn khoảng 2 449 nút"),
    ],
    "lessons/aif/L14_hanh_trinh_may_choi_co.yaml": [
        ("4 bộ TPU:", "4 bộ xử lý tăng tốc tensor TPU:"),
    ],
    "lessons/irs/L05_hoc_xep_hang.yaml": [
        ("liệt kê mọi cặp tốn O(n²) giờ chạy",
         "liệt kê mọi cặp tốn $O(n^2)$ (tăng theo bình phương số ứng viên) giờ chạy"),
    ],
    "lessons/irs/L07_phan_ra_ma_tran.yaml": [
        ("<tr><td>$\\hat{r} = \\mathbf{p} \\cdot \\mathbf{q}$</td><td>r mũ</td><td>điểm dự đoán</td><td>2,5</td></tr>",
         "<tr><td>$\\hat{r} = \\mathbf{p} \\cdot \\mathbf{q}$</td><td>r mũ</td><td>điểm dự đoán qua tích vô hướng <code>dot(p, q)</code>, cập nhật bằng hạ dốc ngẫu nhiên (<b>SGD</b>)</td><td>2,5</td></tr>"),
    ],
    "lessons/irs/L09_khoi_dong_lanh.yaml": [
        ("(thử nghiệm ε-tham lam chỉ chia 0,00001 lượt mỗi món)",
         "(thử nghiệm ε-tham lam — chọn ngẫu nhiên món mới với xác suất ε — chỉ chia 0,00001 lượt mỗi món)"),
    ],
    "lessons/irs/L10_thien_lech_vi_tri.yaml": [
        ("<tr><td>$\\frac{1}{p_r}$</td><td>một chia p r</td><td>trọng số: một lượt bấm ở $r$ đếm thành mấy lượt</td>",
         "<tr><td>$\\frac{1}{p_r}$</td><td>một chia p r</td><td>trọng số nghịch đảo xu hướng (<b>IPS</b>): một lượt bấm ở $r$ đếm thành mấy lượt</td>"),
    ],
    "lessons/irs/L11_da_dang.yaml": [
        ("<tr><td>$\\lambda$</td><td>lambda</td><td>hệ số cân bằng: phần dành cho liên quan</td>",
         "<tr><td>$\\lambda$</td><td>lambda</td><td>hệ số cân bằng liên quan – đa dạng (<b>MMR</b>): phần dành cho liên quan</td>"),
    ],
    "lessons/agt/L01_goi_cong_cu.yaml": [
        ("<p class=\"note\">Trong thực tế, lược đồ của công cụ thường được viết theo chuẩn <b>JSON Schema</b> (bản 2020-12).</p>",
         "<p class=\"note\">Chú ý trong Python: kiểu logic <code>bool</code> (Đúng/Sai) là kiểu con của số nguyên <code>int</code> nên kiểm tra kiểu phải loại riêng <code>bool</code>. Trong thực tế, lược đồ của công cụ thường viết theo chuẩn <b>JSON Schema</b> (bản 2020-12).</p>"),
    ],
    "lessons/llm/L00_mo_hinh_ngon_ngu.yaml": [
        ("Ước lượng bằng đếm: $P(b \\mid a) = \\frac{\\text{số lần } a\\, b}{\\text{số lần } a}$.</p>",
         "Ước lượng bằng đếm: $P(b \\mid a) = \\frac{\\text{số lần } a\\, b}{\\text{số lần } a}$ (có thể biểu diễn chính xác bằng phân số <code>Fraction(tử, mẫu)</code> thay cho số thực làm tròn).</p>"),
    ],
    "lessons/llm/L01_ngram_do_hon_loan.yaml": [
        ("<p><b>Độ hỗn loạn</b>: $PP = P(w_1, \\dots, w_N)^{-1/N}$ với $N$ là số lần dự đoán. Nghĩa trực giác: mô hình bối rối như thể mỗi bước phải chọn đều trong $PP$ khả năng. <b>Càng nhỏ càng tốt</b>.</p>",
         "<p><b>Độ hỗn loạn</b> (<i>perplexity</i>): $PP = P(w_1, \\dots, w_N)^{-1/N}$ với $N$ là số lần dự đoán. Nghĩa trực giác: mô hình bối rối như thể mỗi bước phải chọn đều trong $PP$ khả năng — <b>giá trị nhỏ hơn</b> cho thấy mô hình tự tin và chuẩn xác hơn.</p>"),
    ],
    "lessons/llm/L06_huan_luyen_truoc.yaml": [
        ("(cùng dùng lôgarit tự nhiên).</p>",
         "(cùng dùng lôgarit tự nhiên; hàm mũ <code>exp(x)</code> tính $e^x$).</p>"),
    ],
    "lessons/rln/L01_bellman.yaml": [
        ("giải hệ tuyến tính trực tiếp O(n³) sập ngay",
         "giải hệ tuyến tính trực tiếp $O(n^3)$ (tốn lũy thừa bậc ba theo số trạng thái) sập ngay"),
    ],
    "lessons/rln/L06_dqn.yaml": [
        ("<tr><td>$y = r + \\gamma \\cdot \\max_{a'} Q(s', a'; \\theta_{\\text{cũ}})$</td><td>mục tiêu y</td><td>con số mạng phải học đoán; ví dụ $1 + 0{,}99 \\cdot 10 = 10{,}9$</td></tr>",
         "<tr><td>$y = r + \\gamma \\cdot \\max_{a'} Q(s', a'; \\theta_{\\text{cũ}})$</td><td>mục tiêu y</td><td>cộng thưởng với chiết khấu nhân giá trị cực đại từ mạng mục tiêu (<code>max Q_target</code>); ví dụ $1 + 0{,}99 \\cdot 10 = 10{,}9$</td></tr>"),
    ],
    "lessons/rln/L13_hanh_trinh_atari.yaml": [
        ("<div class=\"box key\"><b>Tư duy:</b> càng lớn, cái khó càng chuyển từ “làm cho nó học được” sang “đo cho đúng”.",
         "<div class=\"box key\"><b>Tư duy:</b> khi quy mô lớn dần, cái khó chuyển từ “làm cho nó học được” sang “đo cho đúng”."),
        ("khi chỉ có 1 GPU trong 1 tuần",
         "khi chỉ có 1 bộ xử lý đồ hoạ (<b>GPU</b>) trong 1 tuần"),
    ],
    "lessons/cvi/L12_hanh_trinh_imagenet.yaml": [
        ("Từ mô hình AlexNet 2012 (tăng 2 048× ảnh bằng cắt/lật) trên 1 triệu ảnh ImageNet tới dự án nhỏ 3 000 ảnh: tận dụng mô hình học sẵn để rút thời gian từ nhiều tuần GPU xuống vài giờ.",
         "Từ mạng tích chập sâu AlexNet (năm 2012, tăng 2 048× ảnh bằng cắt/lật, đo lỗi top-5 — 5 đáp án đầu) trên 1 triệu ảnh ImageNet tới dự án nhỏ 3 000 ảnh: tận dụng mô hình học sẵn rút thời gian chạy bộ xử lý đồ hoạ (<b>GPU</b>) từ nhiều tuần xuống vài giờ."),
    ],
}

for rel, pairs in PATCHES.items():
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        elif new not in s:
            print(f"[WARN_NO_MATCH] {rel}: {old[:60]}", flush=True)
    p.write_text(s, encoding="utf-8")
print("PATCHED STAGE 9 TEXT GLOSSES!", flush=True)

# Run Stage 9 upgraders (AIF already passed; up_s9_llm_rl_cv covers IRS/AGT/LLM/RLN/CVI)
for cmd in [
    [PY, "-B", "-u", "audit/s9_11/up_s9_llm_rl_cv.py"],
]:
    print(">>> RUN:", " ".join(cmd), flush=True)
    p = subprocess.run(cmd, cwd=ROOT)
    assert p.returncode == 0, f"failed: {cmd}"

# Verify CS115 L22-43 + all Stage 9 courses
cs_files = sorted(glob.glob(str(ROOT / "lessons/cs115/L*.yaml")))
import re
cs_22_43 = [
    str(Path(f).relative_to(ROOT))
    for f in cs_files
    if re.search(r"L(\d+)_", Path(f).name) and 22 <= int(re.search(r"L(\d+)_", Path(f).name).group(1)) <= 43
]

for f in cs_22_43:
    p = subprocess.run([PY, "-B", "tools/lv.py", "lint", f], cwd=ROOT)
    assert p.returncode == 0, f"lint failed: {f}"

for cmd in [
    [PY, "-B", "audit/review/sync_tpl_from_lesson.py", "CS115", "--write"],
    [PY, "-B", "audit/review/screen_code.py", "check", "--course", "CS115"],
    [PY, "-B", "audit/review/lab_gate.py", "CS115"],
    [PY, "-B", "tools/lv.py", "curriculum", "curriculum/cs115.yaml"],
    [PY, "-B", "audit/verify_cs115_tex.py"],
    [PY, "-B", "audit/review/arith_scan.py", "CS115"],
]:
    print(">>> RUN:", " ".join(cmd[:4]), flush=True)
    p = subprocess.run(cmd, cwd=ROOT)
    assert p.returncode == 0, f"failed: {cmd}"

for c in ("AIF", "IRS", "AGT", "LLM", "RLN", "CVI"):
    files = [str(Path(f).relative_to(ROOT)) for f in sorted(glob.glob(str(ROOT / f"lessons/{c.lower()}/L*.yaml")))]
    for f in files:
        p = subprocess.run([PY, "-B", "tools/lv.py", "lint", f], cwd=ROOT)
        assert p.returncode == 0, f"lint failed: {f}"
    for cmd in [
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"],
    ]:
        print(">>> RUN:", " ".join(cmd[:4]), flush=True)
        p = subprocess.run(cmd, cwd=ROOT)
        assert p.returncode == 0, f"failed: {cmd}"

# Sequential layout_scan on all 7 Stage 9 courses
for c in ("CS115", "AIF", "IRS", "AGT", "LLM", "RLN", "CVI"):
    print(f">>> LAYOUT SCAN {c}", flush=True)
    p = subprocess.run([PY, "-B", "audit/layout_scan.py", c], cwd=ROOT)
    assert p.returncode == 0, f"layout_scan failed: {c}"

print("STAGE 9 ALL 106 LESSONS POLISHED + GATES + LAYOUT SCAN 100% PASS!", flush=True)
