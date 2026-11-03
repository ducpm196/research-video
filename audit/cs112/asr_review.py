"""Ghi `asr_reviewed` cho các câu ASR gắn cờ còn lại (sau khi đã viết lại các câu quá ngắn). Lý do theo nhóm đã có bằng chứng:
Theta (probe p1 8/8), lôgarit (nút thắt B20 đã biết), “ô”, tên chữ cái; câu không có từ rủi ro thì lý do viết tay ở HAND.
Câu nào còn nghi là lỗi đọc thật thì ghi NOT_VERIFIED trong lý do, để người nghe lại. Chạy sau asr_flags.py: đọc lại báo cáo ASR."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

HAND = {
    "Cái giá của mảng là khi chèn.": "mảng/mảnh, chèn/trang: cả hai mô hình nghe nhầm; “chèn” bị nghe thành chàng/tràn/chen ở nhiều câu — NOT_VERIFIED, cần người nghe",
    "Danh sách liên kết thì ngược với mảng, chèn đầu rẻ nhưng đọc phần tử thứ i đắt.": "mảng/mạng, chèn/chen, đọc/độc, đắt/đắc: nhầm thanh, âm cuối của ASR; “chèn” xem câu trên — NOT_VERIFIED",
    "Gặp ngoặc mở thì đẩy vào ngăn xếp.": "ngoặc/ngoặt, xếp/xét: nhầm âm cuối c/t, p/t của ASR",
    "Lỗi thứ nhất, quên đánh dấu đỉnh đã thăm.": "lỗi/lội, quên/quen, đỉnh/định: nhầm thanh trên câu ngắn — NOT_VERIFIED, cần người nghe",
    "Duyệt theo chiều sâu dùng đệ quy và quay lui.": "sâu/xấu (s/x), đệ quy/để quý: nhầm phụ âm đầu, thanh của ASR",
    "Tỉ số tiến về hằng số 2, nên đáp án đúng bậc.": "tỉ/tỷ là chính tả; hằng/hàng, bậc/bật là cặp ASR nhầm lặp lại ở nhiều câu (mục tham khảo)",
    "Đệ quy thô tính lặp các bài con nên tốn hàm mũ.": "đệ/để, lặp/lập, hàm/hà: nhầm thanh, âm cuối của ASR",
    "Lỗi thứ nhất, điền bảng theo từng hàng, từng cột như bảng thường.": "điền/điện, bảng/bản, cột/cục: nhầm thanh, âm cuối của ASR",
    "Phép thử là tính lại trực tiếp theo cách đặt ngoặc vừa truy vết, vì bảng có thể sai mà ngoặc thì dễ kiểm.": "ngoặc/ngọt/hoặc, bảng/bạn, mà/màng: nhầm của ASR trên cụm hiếm",
    "Chuỗi xếp hạng này gồm bốn nhóm hàm.": "chuỗi/chủi, hàm/ham: nhầm thanh; cùng từ “chuỗi” ở khung 61 cả hai mô hình nghe đúng",
    "Lỗi thứ nhất, nhầm giảm để trị với chia để trị.": "nhầm/nhằm, để/đệ: nhầm thanh của ASR (cụm “để trị” hiếm)",
    "Lỗi thứ nhất, nhầm dãy con với đoạn con.": "nhầm/nhằm, dãy/dạy: nhầm thanh ngã/nặng của ASR — NOT_VERIFIED bằng tai người",
    "Đi kèm ba ràng buộc, về bột, về đường, và số mẻ không âm.": "ràng buộc/tràng bụt, bột/bộ: nhầm âm đầu, âm cuối của ASR",
    "Bốn, với tiệm cận thì lấy giới hạn của tỉ số, đừng tin vài giá trị đầu.": "cận/trận, hạn/hàng, vài/và: nhầm của ASR; các từ này ở bài 1, 2 được nghe đúng",
    "Bẫy mười ba, điền bảng theo đoạn theo từng hàng, hãy hỏi ô cần dùng đã có chưa.": "“bẫy mười ba” → “73”: bẫy/bảy (ngã/hỏi) bị gộp thành số; 14 câu “Bẫy N” khác nghe đúng — NOT_VERIFIED bằng tai người",
    "Lưu ý, cận dưới lôgarit của n giai thừa chỉ áp dụng cho thuật toán dựa trên so sánh.": "cận/cần (thanh), giai thừa/vai thư, dựa/vừa: nhầm âm đầu, thanh của ASR; “giai thừa” nghe đúng ở các bài 2, 23 khác — NOT_VERIFIED, cần người nghe",
    "Vì thời gian tăng theo hàm mũ của số bit, thuật toán này gọi là giả đa thức, và cái túi 0 1 vẫn là NP khó.": "NP đọc “en-pê” (probe p5: 8/8); ở câu này ASR chép “en thuê” — một lần lệch âm đầu, các câu NP khác nghe đúng",
    "Bẫy mười sáu, nói sắp xếp nhanh luôn tốn n lôgarit n, hãy thử mảng đã sắp, sáu phần tử tốn tới 15 phép so sánh.": "“bẫy mười sáu” → “76”: bẫy/bảy (ngã/hỏi) gộp thành số — cùng lỗi “Bẫy mười ba” đã ghi; “lôgarit” nút thắt B20 — NOT_VERIFIED bằng tai người",
    "Một, chứng chỉ gồm đỉnh 1 và 3 độc lập, duyệt 5 cạnh thấy không cạnh nào có cả hai đầu trong tập, tốn Theta của m.": "“duyệt năm” → “Việt Nam”: ASR ghép âm (nghe giống); m đọc “em-mờ” là tên chữ cái; Theta → teta",
}
GROUP = [
    (lambda r: "t, ta" in r, "Theta đọc “Tê-ta” (probe p1: 8/8); ASR chép “teta/θ/tê ta”, cùng âm"),
    (lambda r: "lôgarit" in r, "“lôgarit” → logarith/logatrix: nút thắt B20 đã biết, cùng âm"),
    (lambda r: re.search(r"(^|, )ô(,|$)", r), "“ô” (ô của bảng/mảng) ASR chép “O/Âu”, cùng âm; chữ “ô” có trên màn hình"),
    (lambda r: "kép" in r, "w đọc “vê kép”, ASR chép “v”; chữ w hiện trên màn hình"),
    (lambda r: re.search(r"(^|, )[a-z](,|$)", r), "tên chữ cái đọc kiểu Việt, ASR chép nhầm chữ (d→dây/G, f→S, j→gi/di, i→y, x→ích, g→v/dê) — nhóm đã biết (SKILL Bước 5); chữ hiện trên màn hình"),
]

flags = {}
for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    c = line.split("\t")
    if len(c) == 6:
        flags.setdefault(c[0], []).append((c[3], c[5].strip("[]")))
for lid, rows in flags.items():
    p = next((ROOT / "lessons" / "cs112").glob(lid + "_*.yaml"))
    sp = lv.load_spec(p)
    have = {s.strip() for sc in sp["scenes"] for st in sc["steps"] for s in lv.sentences(st["say"])}
    done = {str(x["sentence"]).strip() for x in sp.get("asr_reviewed") or []}
    new = []
    for sent, risk in rows:
        if sent not in have or sent in done:
            continue
        reason = HAND.get(sent) or "; ".join(t for f, t in GROUP if f(risk))
        if not reason:
            print("THIẾU LÝ DO", lid, sent); continue
        new.append((sent, reason))
    if not new:
        continue
    text = p.read_text(encoding="utf-8")
    lines = "".join(f'  - {{sentence: "{s}", reason: "{r}"}}\n' for s, r in new)
    if "\nasr_reviewed:\n" in text:
        text = text.replace("\nasr_reviewed:\n", "\nasr_reviewed:\n" + lines, 1)
    else:
        # bỏ dòng rỗng `asr_reviewed: []` của khung bài — nếu giữ, YAML có khoá trùng (lỗi thật: 30 tệp CS112, phát hiện 2026-10-27)
        text = text.replace("\nasr_reviewed: []\n", "\n", 1)
        assert text.count("\nscenes:\n") == 1
        text = text.replace("\nscenes:\n", "\nasr_reviewed:\n" + lines + "scenes:\n", 1)
    p.write_text(text, encoding="utf-8")
    print(lid, len(new), "mục")
