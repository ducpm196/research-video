from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def rep(rel: str, old: str, new: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if new and new in txt and old not in txt:
        return
    if not new and old not in txt:
        return
    assert old in txt, f"Missing in {rel}: {old!r}"
    assert txt.count(old) == 1, f"Multi in {rel}: {old!r}"
    p.write_text(txt.replace(old, new, 1), encoding="utf-8")


rep("lessons/cs115/L31_nmf.yaml", "hàng vạn tài liệu hoặc bảng đánh giá thưa", "hàng vạn bài viết hoặc bảng đánh giá thưa")
rep("lessons/cs115/L32_tsne.yaml", "độ lệch KL bất đối xứng", "độ lệch bất đối xứng giữa hai phân phối")
rep("lessons/cs115/L33_tong_on.yaml", "phân cụm, mạng nơ-ron hay SVM", "phân cụm hay mạng nơ-ron")
rep("lessons/cs115/L35_rnn_lstm.yaml", "Kiến trúc chú ý song song ở bài 41 nhờ kết nối thẳng", "Kiến trúc chú ý song song ra đời sau này nhờ kết nối thẳng")
rep("lessons/cs115/L36_boosting.yaml",
    """- sentence: AdaBoost tính trọng số mô hình từ sai số và tăng trọng số các mẫu bị sai.
  reason: AdaBoost chép “Adabook” — như câu giới thiệu
""",
    "")
rep("lessons/cs115/L37_autoencoder.yaml", "như ReLU hay GELU mở ra", "phi tuyến mượt hơn mở ra")
rep("lessons/cs115/L39_hoc_tang_cuong.yaml", "Phương trình Bellman tạo cầu nối", "Phương trình tự nhất quán tạo cầu nối")
rep("lessons/cs115/L39_hoc_tang_cuong.yaml", "Thuật toán Q-learning học trực tiếp", "Thuật toán học bảng giá trị Q này học trực tiếp")
rep("lessons/cs115/L40_umap.yaml", "Tương tự phương pháp tê ét en e của bài 32, hãy chú ý điều chỉnh số láng giềng k khi muốn cân bằng giữa chi tiết cục bộ với cấu trúc liên kết vừa phải của toàn tập dữ liệu lớn.", "Tương tự phương pháp tê ét en e của bài 32, hãy chỉnh số láng giềng k hợp lý. Mức k phù hợp giúp cân bằng chi tiết cục bộ và cấu trúc chung.")
rep("lessons/cs115/L41_attention.yaml", "cho mọi token trong chuỗi", "cho mọi từ tố trong chuỗi")
rep("lessons/cs115/L42_vae_gan.yaml", "trừ độ lệch KL giữ mã ẩn", "trừ độ lệch phân phối giữ mã ẩn")
rep("lessons/cs115/L42_vae_gan.yaml", "Điểm cân bằng Nash đạt tại xác suất", "Điểm cân bằng hai bên đạt tại xác suất")
rep("lessons/cs115/L43_diffusion.yaml", "bằng mã lệnh ngắn gọn trên máy.", "bằng mã lệnh ngắn gọn trên máy.")
rep("lessons/cs115/L43_diffusion.yaml", "Mối nối trực tiếp giữa sai số bình phương trên nhiễu và phân phối chuẩn giúp toàn bộ quy trình sinh ảnh vận hành cực kỳ ổn định và dễ kiểm chứng bằng mã lệnh ngắn gọn trên máy.", "Mối nối trực tiếp giữa sai số bình phương trên nhiễu và phân phối chuẩn giúp quy trình sinh ảnh cực kỳ ổn định. Nhờ vậy bạn dễ dàng tự kiểm chứng công thức bằng đoạn mã ngắn gọn.")

def append_r0(rel: str, ext: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if ext.strip() in txt:
        return
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old = recap["steps"][0]["say"]
    assert old in txt and txt.count(old) == 1
    p.write_text(txt.replace(old, old.rstrip() + " " + ext.strip(), 1), encoding="utf-8")

append_r0("lessons/cs115/L30_gmm_em.yaml", "Nhờ gán xác suất mềm thay vì cắt cứng ranh giới, mô hình giữ được thông tin ở vùng giao thoa giữa nhiều nhóm dữ liệu chồng lấn. Trong thực tế hãy luôn chạy nhiều lần từ các hạt giống khởi tạo khác nhau rồi chọn nghiệm có giá trị hợp lý lớn nhất. Kết hợp khởi tạo bằng K trung bình trước một vài vòng sẽ giúp thuật toán hội tụ nhanh và ổn định hơn.")
append_r0("lessons/cs115/L32_tsne.yaml", "Cách đối chiếu đa góc nhìn giúp bạn tránh ngộ nhận ranh giới giả trên bản vẽ hai chiều.")
append_r0("lessons/cs115/L37_autoencoder.yaml", "Luôn đối chiếu lỗi tái tạo trên tập kiểm định để chốt bề rộng cổ chai vừa đủ gọn.")
append_r0("lessons/cs115/L38_ica.yaml", "Hãy thử ngay bài thực hành với dãy đổi dấu phóng đại để kiểm chứng tính bất biến của độ nhọn dư.")
append_r0("lessons/cs115/L40_umap.yaml", "Kết hợp đồng thời chỉ số định lượng trên không gian gốc và bản đồ hai chiều giúp báo cáo phân tích đứng vững.")
append_r0("lessons/cs115/L41_attention.yaml", "Nắm chắc cơ chế phân bổ trọng số tự động này sẽ giúp bạn thiết kế hệ thống ngôn ngữ hiệu quả.")
append_r0("lessons/cs115/L43_diffusion.yaml", "Chúc mừng bạn đã đi trọn vẹn bốn mươi tư bài học nền tảng toán cho khoa học máy tính và trí tuệ nhân tạo.")

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for cmd in (
    [PY, "-B", "-u", "audit/s9_11/up_s9_cs115.py"],
    [PY, "-B", "-u", "tools/lv.py", "curriculum", "curriculum/cs115.yaml"],
    [PY, "-B", "-u", "audit/verify_cs115_tex.py"],
):
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"

for i in range(22, 44):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    with redirect_stdout(io.StringIO()):
        res = lv.lint(sp, quiet=True)
    assert not res.errors and not res.warnings, f"{lid}: E={res.errors} W={res.warnings}"
    assert w >= 1645, f"{lid}: {w} < 1645"
    for sc in sp["scenes"]:
        for idx, st in enumerate(sc["steps"]):
            say = st.get("say") or ""
            foc = st.get("focus")
            sents = lv.sentences(say)
            if foc is not None:
                assert len(foc) == len(sents), f"{lid}:{sc['id']}#{idx} focus mismatch"
            for s in sents:
                assert len(s) <= 170 and len(s.split()) <= 38 and "càng " not in s.lower() and not re.search(r"[$_^]", s), f"{lid}: {s}"
    print(f"VERIFIED {lid}: w={w} FAIL=0 WARN=0", flush=True)

r = subprocess.run([PY, "-B", "-u", "audit/layout_scan.py", "CS115"], cwd=ROOT)
assert r.returncode == 0, "FAILED: layout_scan.py CS115"
print("CS115 STAGE 9 FULL GATES PASSED!", flush=True)
