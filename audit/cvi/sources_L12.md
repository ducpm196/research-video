# Nguồn bài CVI L12 — Hành trình: nhận dạng ảnh quy mô lớn 2010 → 2020

Đọc nguyên văn 2026-11-03 (curl bản PDF chính thức từ arxiv.org / papers.nips.cc, trích bằng pdftotext; bản tải ở scratchpad
`cvi_work/src/`). Nhãn dùng trong `stage.source` của bài.

## [RU15] O. Russakovsky và cộng sự, “ImageNet Large Scale Visual Recognition Challenge”, IJCV 115 (2015) — https://arxiv.org/pdf/1409.0575
- Bảng 2: “ILSVRC2010 1,261,406 (668-3047) 50,000 (50) 150,000 (150)”; “ILSVRC2012-14 1,281,167 (732-1300) 50,000 (50) 100,000 (100)” (huấn luyện, kiểm định, thử) → chặng 1, chặng 5.
- “First, human users make mistakes and not all users follow the instructions. Second, users do not always agree with each other, especially for more subtle or confusing synsets” → chặng 1 điểm nghẽn.
- “The solution to these issues is to have multiple users independently label the same image. An image is considered positive only if it gets a convincing majority of the votes.” … “while five users might be necessary for obtaining a good consensus on Burmese cat images, a much smaller number is needed for cat images” … “At least 10 users are asked to vote on each of these images.” → chặng 1 cách xử lý.
- “Candidate images are collected from the Internet by querying several image search engines. For each synset, the queries are the set of WordNet synonyms.” … “we translate the queries into other languages, including Chinese, Spanish, Dutch and Italian.” → chặng 1 quy mô.
- “An average of 99.7% precision is achieved across the synsets.” … “we manually checked 1500 ILSVRC2012-2014 image classification test set images … We found 5 annotation errors, corresponding as expected to 99.7% precision.” → chặng 1 bước 2, chặng 5 bước 3, tự làm câu 2.
- Bảng kết quả: ILSVRC 2010 “NEC 28.2”; ILSVRC 2011 “XRCE 25.8”; ILSVRC 2012 “ISI 26.2”, “SuperVision 16.4”; mục 5.1: “starting from coded SIFT features and evolving to large-scale convolutional neural networks” → hình sáu cột, “đặc trưng thiết kế tay”.
- “There has been a 4.2x reduction in image classification error (from 28.2% to 6.7%)” … “The dataset has not changed since 2012, and there has been a 2.4x reduction in image classification error (from 16.4% to 6.7%)” → tự kiểm.
- “The first annotator (A1) trained on 500 images and annotated 1500 test images.” … “The average pace of labeling was approximately 1 image per minute” … “The GoogLeNet classification error on this sample was estimated to be 6.8% … The human error was estimated to be 5.1%.” → chặng 3, bài học sai 1.
- “We estimate that approximately 22 (21%) of GoogLeNet errors fall into this category, while none of the human errors do.” (vật nhỏ, mảnh); “We estimate that 28 (37%) of the human errors fall into this category, while only 7 (7%) of GoogLeNet errors do.” (giống loài chi tiết: “dogs, monkeys, snakes, birds”) → bài học sai 1.

## [KR12] A. Krizhevsky, I. Sutskever, G. E. Hinton, NIPS 2012 — https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf
- “The size of our network made overfitting a significant problem, even with 1.2 million labeled training examples” → chặng 2 điểm nghẽn. (60 triệu tham số: đã trích ở audit/par/sources_L13.md.)
- “We do this by extracting random 224 × 224 patches (and their horizontal reflections) from the 256×256 images … This increases the size of our training set by a factor of 2048, though the resulting training examples are, of course, highly inter-dependent.” → chặng 2.
- “We use dropout in the first two fully-connected layers … Without dropout, our network exhibits substantial overfitting.” → chặng 2.
- “Averaging the predictions of five similar CNNs gives an error rate of 16.4%.” … “Averaging the predictions of two CNNs that were pre-trained on the entire Fall 2011 release with the aforementioned five CNNs gives an error rate of 15.3%. The second-best contest entry achieved an error rate of 26.2%” ; “(15M images, 22K categories)” → chặng 2.

## [SI14] K. Simonyan, A. Zisserman, arXiv 1409.1556 — https://arxiv.org/pdf/1409.1556
- “a stack of two 3 × 3 conv. layers (without spatial pooling in between) has an effective receptive field of 5 × 5; three such layers have a 7 × 7 effective receptive field.” → chặng 3 hình.
- “we incorporate three non-linear rectification layers instead of a single one, which makes the decision function more discriminative. Second, we decrease the number of parameters: … the stack is parametrised by 3(3²C²) = 27C² weights; at the same time, a single 7 × 7 conv. layer would require 7²C² = 49C² parameters, i.e. 81% more.” → chặng 3.
- “19 weight layers in the network E (16 conv. and 3 FC layers)” ; “we decreased the error rate to 6.8% using an ensemble of 2 models.” → chặng 3 quy mô.

## [SZ14] C. Szegedy và cộng sự, arXiv 1409.4842 — https://arxiv.org/pdf/1409.4842
- “GoogLeNet, a 22 layers deep network” ; bảng: “GoogLeNet 2014 1st 6.67% no” ; “The challenge uses the top-5 error rate for ranking purposes.” ; “an image is deemed correctly classified if the ground truth is among the top-5” → ký hiệu “lỗi năm đáp án”, chặng 3.

## [HE15] K. He và cộng sự, arXiv 1512.03385 — https://arxiv.org/pdf/1512.03385
- “a degradation problem has been exposed: with the network depth increasing, accuracy gets saturated (which might be unsurprising) and then degrades rapidly. Unexpectedly, such degradation is not caused by overfitting, and adding more layers to a suitably deep model leads to higher training error” → chặng 4.
- “residual nets with a depth of up to 152 layers—8× deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task.” → chặng 4.

## [HU17] J. Hu và cộng sự, arXiv 1709.01507 — https://arxiv.org/pdf/1709.01507
- “Squeeze-and-Excitation Networks formed the foundation of our ILSVRC 2017 classification submission which won first place and reduced the top-5 error to 2.251%, surpassing the winning entry of 2016 by a relative improvement of 25%.” → chặng 5.

## [RE19] B. Recht và cộng sự, arXiv 1902.10811 (ICML 2019) — https://arxiv.org/pdf/1902.10811
- “By closely following the original dataset creation processes, we test to what extent current classification models generalize to new data. We evaluate a broad range of models and find accuracy drops of 3% – 15% on CIFAR-10 and 11% – 14% on ImageNet. However, accuracy gains on the original test sets translate to larger gains on the new test sets. Our results suggest that the accuracy drops are not caused by adaptivity, but by the models' inability to generalize to slightly "harder" images” → chặng 6.
- “On ImageNet, the accuracy loss amounts to approximately five years of progress” ; “the best model on ImageNet sees an 11% drop from 83% to 72% in top-1 accuracy” → hook, chặng 6.

## [DO20] A. Dosovitskiy và cộng sự, arXiv 2010.11929 (ICLR 2021) — https://arxiv.org/pdf/2010.11929
- “When trained on mid-sized datasets such as ImageNet without strong regularization, these models yield modest accuracies of a few percentage points below ResNets of comparable size.” → chặng 6, bài học sai 4.
- “the picture changes if the models are trained on larger datasets (14M-300M images).” ; “results when pre-trained at sufficient scale and transferred to tasks with fewer datapoints” ; “the best model reaches the accuracy of 88.55% on ImageNet” → chặng 6. (Câu “14M-300M” đọc ở đoạn mở đầu, pdftotext cắt lề; nội dung trong ngoặc giữ nguyên.)

## Điều KHÔNG dạy (nguồn không ghi / không đọc được)
- “Cuộc thi kết thúc năm 2017”: trang image-net.org không kết nối được (curl hết thời gian, 2026-11-03) → NOT_VERIFIED, bài không nói.
- “Máy giỏi hơn người”: không nói; nguồn chỉ có một người chú thích trên 1500 ảnh.
- Tỉ lệ ~15% nhãn sai trong số ảnh còn bị chấm sai năm 2017 là PHÉP TÍNH CỦA BÀI (giả định tỉ lệ 5/1500 đúng cho cả bộ thử), đã ghi rõ trong lời đọc.
- Chặng 2012 không kể hai thẻ đồ hoạ (đã ở PAR bài 13).
- Đội 3000 ảnh, 5 loại sản phẩm, hai nhà máy ở câu tự làm là SỐ MINH HOẠ.
