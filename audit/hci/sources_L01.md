# Nguồn bài HCI L01 — Mô hình tâm trí, dấu hiệu gợi ý và ánh xạ tự nhiên

Đọc nguyên văn ngày 2026-11-03. Phép đếm số cách ghép một–một $n!$ được kiểm bằng `checks` (`alg.hci_mappings`) và `audit/verify_plan_curricula.py` (`HCI:L01`).

## [NO13] Donald A. Norman — *The Design of Everyday Things: Revised and Expanded Edition*. Basic Books, 2013, chương 1 (*The Psychopathology of Everyday Things*) và chương 3 (*Knowledge in the Head and in the World*).

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Mental models, as the name implies, are the conceptual models in people’s minds that represent their understanding of how things work.” | `sym`, `concept`: định nghĩa mô hình tâm trí của người dùng |
| “Affordances determine what actions are possible. Signifiers communicate where the action should take place.” | `sym`, `concept`, `pitfalls`: phân biệt khả năng vật lý của vật với dấu hiệu gợi ý cho người dùng biết thao tác ở đâu |
| “Mapping is a technical term, borrowed from mathematics, meaning the relationship between the elements of two sets of things. Suppose there are four lights in a row on the ceiling and four switches in a row on the wall. Which switch controls which light? The mapping Problem.” | `prereq`, `sym`, `formula`: ánh xạ là phép ghép tương ứng giữa tập nút điều khiển và tập thiết bị được điều khiển |
| “With four burners, there are twenty-four possible arrangements of controls ($4 \times 3 \times 2 \times 1 = 24$). … Why not arrange the burners and the controls in a two-dimensional rectangular pattern? Then the controls map naturally to the burners.” | `hook`, `intuition`, `formula`, `example`: bếp 4 lò xếp ô vuông nhưng 4 núm xếp hàng ngang có $4! = 24$ cách ghép; xếp núm theo đúng ô vuông chỉ còn 1 cách tự nhiên |
| “Any time you see signs Having to be pasted on a device (such as ‘Push’ or ‘Pull’ on a door), it is a signal of bad design: natural mapping and good signifiers should make labels unnecessary.” | `pitfalls` (lỗi 1): nhãn chữ là cứu chữa sau cùng khi bố cục và dấu hiệu gợi ý chưa đủ rõ |

## Điều KHÔNG dạy / NOT_VERIFIED
- Bảng điều khiển đèn phòng họp 3 công tắc, hệ thống âm thanh 5 nút trượt, cửa kính văn phòng trong phần tự làm là SỐ MINH HOẠ cho phép đếm $n!$ và thiết kế ánh xạ tự nhiên.
- Tên tác giả `Norman` chỉ hiện trên màn hình; lời đọc dùng “tác giả cuốn sách kinh điển về thiết kế đồ vật hằng ngày”.
