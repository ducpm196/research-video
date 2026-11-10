# Nguồn PAR L13 — Hành trình: bộ xử lý đồ hoạ từ vẽ hình tới huấn luyện trên hàng trăm thẻ

Đọc nguyên văn 2026-11-02 (curl + pdftotext; bản tải ở scratchpad `par_work/src/`). Nhãn dùng trong `stage.source` của bài.

## [OW05] J. D. Owens, D. Luebke, N. Govindaraju, M. Harris, J. Krüger, A. E. Lefohn, T. J. Purcell, “A Survey of General-Purpose Computation on Graphics Hardware”, Eurographics 2005 State of the Art Report
- Bản đọc: https://research.nvidia.com/sites/default/files/pubs/2005-08_A-Survey-of/ASurveyofGeneralPurposeComputationonGraphicsHardware.pdf (bản do NVIDIA Research lưu).
- “For example, the NVIDIA GeForce 6800 Ultra ($417 as of June 2005) can achieve a sustained 35.2 GB/sec of memory bandwidth; the
  ATI X800 XT ($447) can sustain over 63 GFLOPS (compare to 14.8 GFLOPS theoretical peak for a 3.7 GHz Intel Pentium4 SSE unit [Buc04]).”
- “GPUs typically have multiple vertex and fragment processors (for example, the NVIDIA GeForce 6800 Ultra and ATI Radeon X800 XT each
  have 6 vertex and 16 fragment processors).”
- “A typical GPGPU program uses the fragment processor as the computation engine in the GPU.” … “Each of these sections can be considered
  a kernel and is implemented as a fragment program. The input and output of each kernel program is one or more data arrays, which are
  stored (sometimes only transiently) in textures in GPU memory.”
- “As a simple example, initiating a GPGPU computation usually involves drawing a primitive. Looking up data from memory is done by
  issuing a texture fetch. … the shading languages … force the GPGPU application writer to think in terms of geometric primitives,
  fragments, and textures.”
- “… fragment processors are incapable of memory scatter.”
- “On each rendering pass, the size of the output, the computational range, is reduced by one half. In general, we can compute a
  reduction over a set of data in O(log n) steps using the parallel GPU hardware, compared to O(n) steps for a sequential reduction on
  the CPU.”
- “Fatahalian et al. [FSH04] … focused on matrix-matrix multiplication and discovered that these operations are strongly limited by
  memory bandwidth when implemented on the GPU.”
- FFT: “These implementations are primarily limited by memory bandwidth and the lack of effective caching in today's GPUs, and only by
  processing two FFTs simultaneously can match the performance of a highly tuned CPU implementation.”

## [NI08] J. Nickolls, I. Buck, M. Garland, K. Skadron, “Scalable Parallel Programming with CUDA”, ACM Queue 6(2), 3–4/2008, tr. 40–53
- queue.acm.org/detail.cfm?id=1365500 trả HTTP 403 cho công cụ. Bản đọc: bản chép của một khoá học tại
  https://grothoff.org/christian/teaching/2008/4704/scalable_cuda.pdf (đối chiếu tên tác giả, tiêu đề với trang research.nvidia.com).
- “Since NVIDIA released CUDA in 2007, developers have rapidly developed scalable parallel programs for a wide range of applications …
  These applications scale transparently to hundreds of processor cores and thousands of concurrent threads.”
- “Introduced by NVIDIA in November 2006, the Tesla unified graphics and computing architecture significantly extends the GPU beyond
  graphics …”
- “Current GPU implementations range from 768 to 12,288 concurrently executing threads.” “Figure A shows a GPU with 14 SMs--a total of
  112 SP (streaming processor) cores …”
- “An SM consists of eight scalar SP cores … The SM creates, manages, and executes up to 768 concurrent threads in hardware with zero
  scheduling overhead.”
- “… executes threads in groups of 32 parallel threads called warps.” “Each SM manages a pool of 24 warps of 32 threads per warp, a
  total of 768 threads.”
- “A warp executes one common instruction at a time, so full efficiency is realized when all 32 threads of a warp agree on their
  execution path. If threads of a warp diverge via a data-dependent conditional branch, the warp serially executes each branch path
  taken, disabling threads that are not on that path …”
- “CUDA requires that thread blocks execute independently. It must be possible to execute blocks in any order, in parallel or in
  series.” “This independence requirement allows thread blocks to be scheduled in any order across any number of cores …”
- “The 16KB SM shared memory has very low access latency and high bandwidth similar to an L1 cache …”
- “… enabling them to achieve speedups of 100 times or more on a variety of sophisticated applications.”
- “Although CUDA was released less than a year ago, it is already the target of massive development activity--there are tens of
  thousands of CUDA developers.”

## [KR12] A. Krizhevsky, I. Sutskever, G. E. Hinton, “ImageNet Classification with Deep Convolutional Neural Networks”, NIPS 2012
- Bản đọc: https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf
- “The neural network, which has 60 million parameters and 650,000 neurons, consists of five convolutional layers …”
- “In the end, the network's size is limited mainly by the amount of memory available on current GPUs and by the amount of training
  time that we are willing to tolerate. Our network takes between five and six days to train on two GTX 580 3GB GPUs.”
- “A single GTX 580 GPU has only 3GB of memory, which limits the maximum size of the networks that can be trained on it. … Therefore we
  spread the net across two GPUs.”
- “The parallelization scheme that we employ essentially puts half of the kernels (or neurons) on each GPU, with one additional trick:
  the GPUs communicate only in certain layers.” “… this allows us to precisely tune the amount of communication until it is an
  acceptable fraction of the amount of computation.”
- “In all, there are roughly 1.2 million training images …”; “We trained the network for roughly 90 cycles through the training set of
  1.2 million images, which took five to six days on two NVIDIA GTX 580 3GB GPUs.”

## [GO17] P. Goyal và cộng sự, “Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour”, arXiv 1706.02677 (2017)
- Bản đọc: https://arxiv.org/pdf/1706.02677
- “… our Caffe2-based system trains ResNet-50 with a minibatch size of 8192 on 256 GPUs in one hour, while matching small minibatch
  accuracy. Using commodity hardware, our implementation achieves 90% scaling efficiency when moving from 8 to 256 GPUs.”
- “… we scale ResNet-50 training, originally performed with a minibatch size of 256 images (using 8 Tesla P100 GPUs, training time is
  29 hours), to larger minibatches.”
- “Linear Scaling Rule: When the minibatch size is multiplied by k, multiply the learning rate by k.”
- “In this work, we use n = 32 which has performed well …” (số mẫu mỗi thẻ giữ cố định).
- “… minibatch size of kn = 256 and a reference learning rate of η = 0.1. Applying the linear scaling rule gives η̂ = 3.2 as the
  reference learning rate for our large minibatch runs.”
- “Gradual warmup … reaches η̂ = kη after 5 epochs …”
- “The no-warmup variant has 1.2% higher validation error than the baseline …”

## [HO18] A. Sergeev, M. Del Balso, “Horovod: fast and easy distributed deep learning in TensorFlow”, arXiv 1802.05799 (2018)
- Bản đọc: https://arxiv.org/pdf/1802.05799
- “… as datasets grew, so did the training times, which sometimes took a week or longer to complete.”
- “For example, we lost about half of our resources due to communication overhead when training on 128 GPUs.”
- “The standard distributed TensorFlow package introduces many new concepts: workers, parameter servers … in many cases it introduced
  subtle, hard-to-diagnose bugs.”
- “In early 2017 Baidu published an article evangelizing a different algorithm … called ring-allreduce … The algorithm was based on the
  approach introduced in the 2009 paper by Patarasuk and Yuan.” “… each of N nodes communicates with two of its peers 2 ∗ (N − 1)
  times.” “… if the buffer is large enough, it will optimally utilize the available network.”
- “At any point in time, various teams at Uber may be using different releases of TensorFlow. We wanted all teams to be able to
  leverage the ring-allreduce algorithm without needing to upgrade to the latest version of TensorFlow … Having a stand-alone package
  allowed us to cut the time required to install Horovod from about an hour to a few minutes …”
- “We replaced the Baidu ring-allreduce implementation with NCCL … NVIDIA's library for collective communication …”
- “… Horovod needs just a few new lines.”
- “… those with a large amount of tensors, such as ResNet-101, tended to have many tiny allreduce operations. … ring-allreduce utilizes
  the network in an optimal way if the tensors are large enough, but does not work as efficiently or quickly if they are very small.”
  “Tensor Fusion … we observed up to 65 percent improvement …”
- “… scaling using both Inception V3 and ResNet-101 models achieved an 88 percent efficiency mark. In other words, the training was
  about twice as fast as standard distributed TensorFlow.”
- “RDMA, however, did help Horovod exceed 90 percent scaling efficiency on both models. Meanwhile, the VGG-16 model experienced a
  significant 30 percent speedup when we leveraged RDMA networking. … These characteristics shifted the critical path from GPU
  computation to communication …”
- “… in the future, we intend to continue leveraging the open source community …”

## Phép tính lại (VER PAR:L13, verify_parts/L13.py)
- 63 / 14,8 ≈ 4,26; 24 × 32 = 768; 12 288 / 768 = 16 cụm; 14 × 8 = 112; 90 × 1,2 triệu ảnh trong 5–6 ngày ≈ 208–250 ảnh/giây;
  29 giờ × 8/256 = 0,906 giờ lý tưởng, chia 90% ≈ 1,007 giờ; 0,1 × 8192/256 = 3,2; 8192/256 = 32 ảnh mỗi thẻ; 0,88/0,50 = 1,76;
  2 · 127/128 ≈ 1,98 D; 2(n − 1) bước mỗi lần gộp.

## Điều KHÔNG dạy (nguồn không ghi hoặc bài không cần)
- Không nói “thẻ đồ hoạ nhanh gấp 100 lần” chung chung: [NI08] chỉ ghi “100 times or more on a variety of sophisticated applications”;
  [OW05] ghi nhân ma trận và FFT bị băng thông chặn, FFT chỉ ngang CPU đã tối ưu.
- Không nói mạng năm 2012 là “mạng đầu tiên chạy trên thẻ đồ hoạ” — [KR12] không ghi vậy.
- Không nói trọng số chiếm bao nhiêu trong 3 GB (bài báo không ghi kiểu số; không suy diễn phần còn lại của bộ nhớ dùng cho gì).
- Hiệu suất 90% của [GO17] là khi đi từ 8 lên 256 thẻ, không phải từ 1 thẻ.
- Không nêu tên cá nhân; tên hãng, tên thẻ, tên thư viện chỉ trên màn hình (lexicon_vi.PAR.yaml).

## Đọc kiểm đợt C (2026-11-09) — BN-0038 “mốc năm thư viện”
- CUDA Toolkit Archive, https://developer.nvidia.com/cuda-toolkit-archive (curl 2026-11-09, no revision given): dòng “CUDA Toolkit 1.0 (June 2007)”,
  “CUDA Toolkit 1.1 (Dec 2007)” → mốc “năm 2007, mô hình lập trình riêng” của chặng 2 KIỂM ĐƯỢC (khớp [NI08] “Since NVIDIA released CUDA in 2007”).
- arXiv 1802.05799 (trang abs, curl 2026-11-09): “Submitted on 15 Feb 2018”; tóm tắt gọi Horovod là “open source library … ring reduction”.
  Mốc đầu 2017 lấy từ [HO18] (“In early 2017 Baidu published an article evangelizing … ring-allreduce”). Lời đọc trục thời gian đã viết lại cho
  khớp hai mốc kiểm được: “Đầu năm 2017, cách gộp theo vòng được giới thiệu cho học sâu, và bài báo tháng 2 năm 2018 … mô tả thư viện mã nguồn mở”.
  Ngày thư viện được mở mã nguồn trên kho mã (trước bài báo) KHÔNG kiểm (uber.com/blog/horovod trả 14 byte) → bài không nêu ngày đó.
- cuDNN (Chetlur và cộng sự, arXiv 1410.0759, “Submitted on 3 Oct 2014”) mở được; bài KHÔNG nhắc cuDNN nên không thêm.
- [KR12] papers.nips.cc đã đọc ở đợt trước (câu trích ở trên); không đổi.
- NVIDIA CUDA Programming Guide, docs.nvidia.com/cuda/cuda-c-programming-guide (curl 2026-11-09): tiêu đề “CUDA Programming Guide 13.5”, “Last updated
  on Oct 31, 2026”. Câu về warp/khối độc lập trong bài dẫn từ [NI08] và CUDA C++ Best Practices Guide (L08); trang con của bản 13.5 tải về không trích
  được văn bản bằng công cụ, nên không ghi “trích nguyên văn” từ bản 13.5.
