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
    if new in txt and old not in txt:
        return
    assert old in txt, f"Missing in {rel}: {old[:110]!r}"
    assert txt.count(old) == 1
    p.write_text(txt.replace(old, new, 1), encoding="utf-8")


def append_recap0(rel: str, extra: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if extra.strip() in txt:
        return
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old = recap["steps"][0]["say"]
    assert old in txt and txt.count(old) == 1
    p.write_text(txt.replace(old, old.rstrip() + " " + extra.strip(), 1), encoding="utf-8")


rep("lessons/aif/L08_logic_menh_de.yaml",
    "trước khi chuyển sang bộ suy diễn luật tuyến tính ở bài tiếp theo.",
    "trước khi học phương pháp suy diễn nhanh dựa trên tập luật xác định.")
rep("lessons/aif/L09_suy_dien_tien_lui.yaml",
    "Ngược lại nếu cơ sở dữ liệu chứa hàng nghìn luật phức tạp trong khi người dùng chỉ cần biết một câu kết luận duy nhất có đúng hay không, suy diễn lùi tiết kiệm rất nhiều phép đối chiếu dư thừa.",
    "Ngược lại nếu kho có hàng nghìn luật mà ta chỉ cần hỏi đúng một câu kết luận, suy diễn lùi sẽ thắng thế. Nó bỏ qua mọi nhánh không chạm đích nên tiết kiệm rất nhiều phép đối chiếu dư thừa.")

AIF_TOP = {
    "lessons/aif/L01_bai_toan_tim_kiem.yaml": "Giữ chắc sự khác biệt về thời điểm kiểm tra đích sẽ bảo đảm bạn viết đúng cả hai thuật toán.",
    "lessons/aif/L05_thoa_rang_buoc.yaml": "Khi hiểu rõ cấu trúc đồ thị ràng buộc, bạn dễ dàng chuyển đổi qua lại giữa các bài toán lập lịch, tô màu hay xếp chỗ. Đừng bỏ qua thao tác đếm nghiệm hợp lệ ngay trong phần thực hành bên dưới.",
    "lessons/aif/L06_tro_choi_doi_khang.yaml": "Thứ tự duyệt nước tốt từ gốc xuống sẽ quyết định lượng nhánh được cắt bỏ ngay tầng đầu. Nắm vững hai cận đối lập giúp bạn tự tin phân tích mọi cây trò chơi đối kháng.",
    "lessons/aif/L07_cay_mo_phong_ngau_nhien.yaml": "Bài tập tính điểm công thức UCB1 sắp tới giúp bạn kiểm chứng ngay cách cân bằng thử nghiệm.",
    "lessons/aif/L08_logic_menh_de.yaml": "Học tốt cách kiểm chứng từng mô hình chân trị giúp bạn xây nền vững vàng cho suy luận logic tự động. Chúc bạn thực hành tốt câu lệnh kiểm định ba biến ngay sau đây.",
    "lessons/aif/L09_suy_dien_tien_lui.yaml": "Nắm rõ ranh giới giữ chặt một kết luận dương mỗi luật giúp bạn tránh mở rộng nhầm sang những câu tổng quát ngoài khả năng suy diễn tuyến tính.",
    "lessons/aif/L10_lap_ke_hoach.yaml": "Thực hành tìm số bước tối thiểu trên ba khối đảo ngược giúp bạn nắm trọn tư duy chuyển trạng thái bằng hành động.",
    "lessons/aif/L12_lap_gia_tri.yaml": "Chú ý dùng biến tạm lưu bản mới của mọi ô sau mỗi lượt cập nhật rồi mới gán lại đồng loạt.",
    "lessons/aif/L13_tong_hop.yaml": "Chìa khoá của kỹ sư giỏi là không ép một phương pháp duy nhất cho mọi bài toán. Biết kết hợp sức mạnh tìm kiếm chính xác cùng khả năng ước lượng học từ dữ liệu giúp giải quyết trọn vẹn các bài toán lớn.",
}
for rel, ext in AIF_TOP.items():
    append_recap0(rel, ext)

bad = []
for i in range(15):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "aif").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    with redirect_stdout(io.StringIO()):
        res = lv.lint(sp, quiet=True)
    if res.errors or res.warnings:
        bad.append(f"{lid} E={res.errors} W={res.warnings}")
    if w < 1645:
        bad.append(f"{lid} w={w} (need +{1655-w})")
    for sc in sp["scenes"]:
        for idx, st in enumerate(sc["steps"]):
            say = st.get("say") or ""
            foc = st.get("focus")
            sents = lv.sentences(say)
            if foc is not None and len(foc) != len(sents):
                bad.append(f"{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}")
            for s in sents:
                if len(s) > 170: bad.append(f"{lid}:{sc['id']}#{idx} >170 ({len(s)}): {s}")
                if len(s.split()) > 38: bad.append(f"{lid}:{sc['id']}#{idx} >38w ({len(s.split())}): {s}")
                if "càng " in s.lower(): bad.append(f"{lid}:{sc['id']}#{idx} 'càng ': {s}")
                if re.search(r"[$_^]", s): bad.append(f"{lid}:{sc['id']}#{idx} TeX: {s}")
    print(f"AIF:{lid}: w={w} E={len(res.errors)} W={len(res.warnings)}", flush=True)
for b in bad:
    print("BAD:", b, flush=True)
assert not bad, f"{len(bad)} AIF issues"

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for cmd in (
    [PY, "-B", "-u", "audit/s9_11/up_s9_data_ai.py", "AIF"],
    [PY, "-B", "-u", "tools/lv.py", "curriculum", "curriculum/aif.yaml"],
    [PY, "-B", "-u", "audit/aif/verify_aif.py"],
):
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"
print("AIF STAGE 9 UPGRADE & VERIFY PASSED!", flush=True)
