# tools/ — kiến trúc xưởng video

Một đặc tả bài (YAML) đi qua một đường ống cố định. Mọi khác biệt giữa các chủ đề (STEM, ngoại ngữ, kỹ năng mềm, xã hội–triết học,
phim ảnh, tiếp thị liên kết) nằm ở **dữ liệu cấu hình**, không nằm trong mã: hồ sơ chuyên ngành, lớp phủ phát âm, sổ ký hiệu, mẫu bài.

```
lessons/<khoá>/<id>_<slug>.yaml      ← đặc tả bài (người/agent viết theo mẫu)
        │  lv.py lint     cấu trúc theo hồ sơ · ký hiệu trước khi dùng · checks · câu đọc được · focus · E1–E50
        │  lv.py tts      edge-tts (cache theo giọng+tốc độ+văn bản) · thử lại theo lượt · giọng dự phòng cho CẢ bài
        │  lv.py render   player.html + KaTeX trong Chromium → khung PNG · kiểm tràn, đè, chữ đè trong hình
        │  lv.py build    lint → tts → render → ffmpeg MP4 + SRT + chapters → verify (dấu băm đặc tả + văn bản TTS, một giọng)
        │  lv.py asr      faster-whisper hai mô hình (GPU nếu có) nghe lại mọi câu, theo đúng ngôn ngữ của câu
        ▼
out/<KHOÁ>/<id>/<id>.mp4, .srt, chapters.txt, preview.html, build_report.json, asr_report.md
```

## Mô-đun
| Tệp | Vai trò | Mở rộng ở đâu |
|---|---|---|
| `lv.py` | CLI và đường ống: new, new-course, lint, preview, tts, render, build, verify, asr, curriculum | luật lint chung (E1–E40) |
| `lv_profile.py` | hồ sơ chuyên ngành: nạp `profiles/*.yaml`, nhãn phân cảnh, mã ngôn ngữ của giọng, luật riêng E41–E50 | thêm luật cho lĩnh vực có rủi ro |
| `profiles/*.yaml` | stem (mặc định), language, softskill, humanities, film, affiliate | thêm một tệp = thêm một loại video |
| `vi_text.py` | chuẩn hoá tiếng Việt cho máy nghe (số → chữ, nhận chữ cái đọc kiểu Việt) | — |
| `checklib.py` | hàm kiểm dùng chung cho `checks` (tiền tố theo khoá) | hàm kiểm của khoá mới |
| `registry/lexicon_vi*.yaml` | luật đọc theo nguyên từ; lớp phủ theo khoá; mỗi luật dẫn bằng chứng dò ASR | từ mới sau khi dò (≥ 7/8) |
| `registry/symbols*.yaml` | sổ ký hiệu toán: mẫu nhận, cách đọc, luật nhất quán | ký hiệu mới |
| `registry/tts_fallback.yaml` | thứ tự giọng dự phòng cho cả bài | — |
| `templates/` | `lesson_template.yaml` (stem, `depth: full`), `case_lesson_template.yaml`, `journey_lesson_template.yaml`, `profiles/<hồ sơ>.yaml`, mẫu khoá mới, `player.html` + `player.css` | mẫu bài của hồ sơ mới |
| `vendor/` | KaTeX, piper (cài cục bộ, không sửa) | — |

## Bất biến (đã có kiểm thử)
- Hồ sơ `stem` cho khung hình giống hệt từng byte với trước khi có hồ sơ (đo trên NET L10, 46/46 khung) — đổi hồ sơ không làm video cũ STALE.
- Khoá cache TTS = giọng + tốc độ + văn bản; khoá cache ASR tiếng Việt giữ dạng cũ, ngôn ngữ khác thêm mã ngôn ngữ.
- Lời giảng một giọng; giọng bản ngữ chỉ ở step câu mẫu của hồ sơ có luật `target_language_voice`.
- `tests/test_lint.py` chứng minh lint BẮT được từng loại lỗi (E1–E50) và SẠCH với mọi bài thật và mọi mẫu hồ sơ.

## Công cụ rà toàn kho (audit/review/)
`audit_all.py` (lint + STALE + giọng + ASR), `pedagogy_scan.py` (độ sâu theo E39), `tts_speed_scan.py` (âm thanh cụt),
`check_course_refs.py`, `check_meta.py`, `status_report.py` → STATUS.md, `tracks.py` → TRACKS.md, `asr_flags.py`, `asr_hand_gen.py`.
