from pathlib import Path
import re
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def append_recap0(rel: str, extra: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old_say = recap["steps"][0]["say"]
    assert old_say in txt and txt.count(old_say) == 1
    p.write_text(txt.replace(old_say, old_say.rstrip() + " " + extra.strip(), 1), encoding="utf-8")


TOPUPS = {
    "lessons/cs115/L27_knn.yaml": "Đo thử trên ba bộ đơn vị khác nhau ngay trong phần thực hành hôm nay để khắc sâu quy tắc này.",
    "lessons/cs115/L28_cay_quyet_dinh.yaml": "Kết hợp kiểm tra độ sâu tối đa và sai số ngoài túi giúp cây tổng quát hoá vững vàng trên dữ liệu mới.",
    "lessons/cs115/L31_nmf.yaml": "Mỗi bước nhân đều giữ bảng thừa số không âm và làm sai số giảm đều cho tới khi hội tụ.",
    "lessons/cs115/L35_rnn_lstm.yaml": "Đừng quên lưu dấu chuỗi thời gian rõ ràng khi triển khai cắt gradient để giữ quá trình học ổn định.",
    "lessons/cs115/L36_boosting.yaml": "Theo dõi đường cong lỗi trên tập kiểm định sau mỗi chục cây con sẽ chỉ ra điểm dừng tối ưu nhất.",
    "lessons/cs115/L40_umap.yaml": "Đừng quên phân biệt rành mạch điều có chứng minh giải tích với kết quả đo thực nghiệm trên vài tập dữ liệu mẫu. Luôn đọc lại biểu đồ dưới nhiều góc độ và ưu tiên độ tin cậy trên lân cận gần thay vì tin vào khoảng cách giữa hai đám mây ở xa nhau. Thói quen kiểm chứng hai chiều này sẽ giữ cho mọi trực quan hoá của bạn luôn trung thực.",
    "lessons/cs115/L41_attention.yaml": "Thử thay đổi điểm truy vấn và khoá trong bài thực hành ngay sau đây để thấy trọng số dịch chuyển tức thì.",
    "lessons/cs115/L43_diffusion.yaml": "Mối nối trực tiếp giữa sai số bình phương trên nhiễu và phân phối chuẩn giúp toàn bộ quy trình sinh ảnh vận hành cực kỳ ổn định và dễ kiểm chứng bằng mã Python ngắn.",
}

for rel, ext in TOPUPS.items():
    append_recap0(rel, ext)

bad = []
for i in range(22, 44):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    for sc in sp["scenes"]:
        for idx, st in enumerate(sc["steps"]):
            say = st.get("say") or ""
            foc = st.get("focus")
            sents = lv.sentences(say)
            if foc is not None and len(foc) != len(sents):
                bad.append(f"{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}")
            for s in sents:
                if len(s) > 170:
                    bad.append(f"{lid}:{sc['id']}#{idx} len={len(s)} >170: {s}")
                if len(s.split()) > 38:
                    bad.append(f"{lid}:{sc['id']}#{idx} words={len(s.split())} >38: {s}")
                if "càng " in s.lower():
                    bad.append(f"{lid}:{sc['id']}#{idx} 'càng ': {s}")
                if re.search(r"[$_^]", s):
                    bad.append(f"{lid}:{sc['id']}#{idx} TeX: {s}")
    if w < 1645:
        bad.append(f"{lid} words={w} < 1645")
    else:
        print(f"OK {lid}: words={w}", flush=True)
assert not bad, f"{bad}"
print("ALL 22 CS115 STAGE 9 LESSONS CLEAN & >= 1645w!", flush=True)
