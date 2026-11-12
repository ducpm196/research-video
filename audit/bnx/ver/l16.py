"""Kiểm độc lập BNX L16 (bể luồng, CompletableFuture, ForkJoinPool). Đường khác với tools/checklib_bnx/l16.py:
- bể luồng: mô phỏng TỪNG MILI GIÂY (vòng lặp đồng hồ, danh sách luồng và hàng đợi), không dùng heap;
- số việc lá: duyệt bằng hàng đợi theo SỐ PHẦN TỬ (không đệ quy theo đoạn), và công thức 2^k;
- tổng: sum(range) và công thức cấp số cộng;
- chạy NGUYÊN VĂN sáu chương trình Java ở audit/bnx/src/l16.py bằng javac/java thật, so đầu ra với khối trên màn hình.
Thiếu javac/java → SKIP (cổng FAIL, NOT_VERIFIED)."""
import math
import shutil
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l16 as src  # noqa: E402


def tick_sim(durations, n_threads, queue_cap=None):
    """Đồng hồ nhảy từng mili giây. Mọi việc gửi lúc 0 theo thứ tự. Trả (kết thúc từng việc | None nếu bị từ chối)."""
    running, queue, end = [], deque(), [None] * len(durations)
    rejected = []
    for i, d in enumerate(durations):          # gửi liền, chưa việc nào xong
        if len(running) < n_threads:
            running.append([i, d])
        elif queue_cap is None or len(queue) < queue_cap:
            queue.append(i)
        else:
            rejected.append(i)
    t = 0
    while running:
        t += 1
        for r in running:
            r[1] -= 1
        done = [r for r in running if r[1] <= 0]
        for r in sorted(done):
            end[r[0]] = t
            running.remove(r)
        while queue and len(running) < n_threads:
            j = queue.popleft()
            if durations[j] == 0:
                end[j] = t
            else:
                running.append([j, durations[j]])
    return end, rejected


def leaves_by_size(n, threshold):
    q, leaves, sizes = deque([n]), 0, []
    while q:
        m = q.popleft()
        if m <= threshold:
            leaves += 1
            sizes.append(m)
        else:
            q.append(m - m // 2)
            q.append(m // 2)
    return leaves, sizes


def run_java(text, cls, jopts=()):
    with tempfile.TemporaryDirectory() as d:
        Path(d, cls + ".java").write_text(text.strip("\n") + "\n", encoding="utf-8")
        r = subprocess.run(["javac", "-encoding", "UTF-8", "-d", d, cls + ".java"], cwd=d, capture_output=True, text=True, encoding="utf-8")
        if r.returncode:
            return r.returncode, r.stderr
        r = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", *jopts, "-cp", d, cls], cwd=d, capture_output=True,
                           text=True, encoding="utf-8", timeout=120)
        return r.returncode, r.stdout.replace("\r\n", "\n")


# LF2 (đợt đọc độc lập 2026-11-12): các điều bài nói thêm mà chỉ chạy ở bộ kiểm, KHÔNG hiện trên màn hình.
J_EXTRA = r'''
import java.util.concurrent.*;
public class Phu {
  public static void main(String[] a) throws Exception {
    // (1) bể chung: luồng nào chạy việc không truyền bể, và mức song song
    var f = CompletableFuture.supplyAsync(() -> Thread.currentThread().getName() + " daemon=" + Thread.currentThread().isDaemon());
    System.out.println("chung: par=" + ForkJoinPool.commonPool().getParallelism() + " " + f.join());
    // (2) hạn chờ không nhả luồng
    ExecutorService be = Executors.newFixedThreadPool(1);
    var cham = CompletableFuture.supplyAsync(() -> {
      try { Thread.sleep(1500); } catch (InterruptedException e) { }
      return 1;
    }, be).orTimeout(100, TimeUnit.MILLISECONDS);
    try { cham.join(); } catch (CompletionException e) { System.out.println("hết hạn: " + e.getCause().getClass().getSimpleName()); }
    long t0 = System.nanoTime();
    be.submit(() -> { }).get();
    System.out.println("việc kế đợi hơn 1000 ms: " + ((System.nanoTime() - t0) / 1_000_000 > 1000));
    be.shutdown();
    // (3) lỗi trong lời hứa kết quả
    var loi = CompletableFuture.supplyAsync(() -> { throw new IllegalStateException("hỏng"); });
    try { loi.join(); } catch (CompletionException e) { System.out.println("join: " + e.getClass().getSimpleName() + " <- " + e.getCause().getClass().getSimpleName()); }
    System.out.println("exceptionally: " + loi.exceptionally(e -> -1).join());
    // (4) số luồng tối đa chỉ dùng khi hàng đầy (lõi 2, tối đa 4, hàng 2 chỗ)
    CountDownLatch cua = new CountDownLatch(1);
    ThreadPoolExecutor p = new ThreadPoolExecutor(2, 4, 0, TimeUnit.SECONDS, new ArrayBlockingQueue<>(2));
    int nhan = 0, choi = 0;
    for (int i = 1; i <= 7; i++) {
      try { p.execute(() -> { try { cua.await(); } catch (InterruptedException e) { } }); nhan++; }
      catch (RejectedExecutionException e) { choi++; }
    }
    System.out.println("lõi2/tối đa4/hàng2: luồng " + p.getPoolSize() + ", hàng " + p.getQueue().size() + ", nhận " + nhan + ", từ chối " + choi);
    cua.countDown(); p.shutdown();
    // (5) hàng đợi không giới hạn: số luồng không vượt số lõi dù tối đa là 4
    CountDownLatch cua2 = new CountDownLatch(1);
    ThreadPoolExecutor q = new ThreadPoolExecutor(2, 4, 0, TimeUnit.SECONDS, new LinkedBlockingQueue<>());
    for (int i = 1; i <= 10; i++) q.execute(() -> { try { cua2.await(); } catch (InterruptedException e) { } });
    System.out.println("không giới hạn: luồng " + q.getPoolSize() + ", hàng " + q.getQueue().size());
    cua2.countDown(); q.shutdown();
  }
}
'''


def run(rec):
    # ── bể 4 luồng, 10 việc 100 ms
    end, _ = tick_sim([100] * 10, 4)
    rounds = sorted(set(end))
    rec("L16", rounds == [100, 200, 300] and max(end) == 300 == alg.bnx_pool_makespan([100] * 10, 4) and len(rounds) == alg.bnx_pool_rounds(10, 4)
        == math.ceil(10 / 4) == 3, f"bể 4 luồng, 10 việc 100 ms: mô phỏng từng mili giây cho các mốc xong {rounds} → 3 lượt, 300 ms")
    rec("L16", end[:4] == [100] * 4 and end[4:8] == [200] * 4 and end[8:] == [300] * 2 and alg.bnx_pool_schedule([100] * 10, 4)[4] == (100, 200)
        and alg.bnx_pool_schedule([100] * 10, 4)[9] == (200, 300), "lượt 1 việc 1–4, lượt 2 việc 5–8, lượt 3 việc 9–10 (khớp hình)")
    rec("L16", sum([100] * 10) == alg.bnx_work_total([100] * 10) == 1000 and sum(i * i for i in range(1, 11)) == 385,
        "tổng công việc 10 · 100 = 1000 ms; tổng bình phương 1..10 = 385")
    # ── ba lời gọi
    e3, _ = tick_sim([400, 200, 300], 3)
    e1, _ = tick_sim([200, 300, 400], 1)
    e2, _ = tick_sim([400, 200, 300], 2)
    rec("L16", max(e3) == 400 == alg.bnx_pool_makespan([200, 300, 400], 3) and max(e1) == 900 == alg.bnx_pool_makespan([200, 300, 400], 1)
        == alg.bnx_work_total([200, 300, 400]) and 900 - 400 == 500,
        "ba lời gọi 200, 300, 400 ms: tuần tự 900 ms, song song 3 luồng 400 ms, bớt chờ 500 ms (mô phỏng từng mili giây)")
    rec("L16", max(e2) == 500 == alg.bnx_pool_makespan([400, 200, 300], 2) and e2 == [400, 200, 500],
        "chỉ 2 luồng, gửi 400, 200, 300: luồng hai làm 200 rồi 300 → chờ 500 ms")
    names = ["điểm", "số dư", "hạn mức"]
    order = [names[i] for i in sorted(range(3), key=lambda i: e3[i])]
    rec("L16", order == ["số dư", "hạn mức", "điểm"] == alg.bnx_finish_order(list(zip(names, [400, 200, 300])), 3),
        f"thứ tự xong khi gửi điểm trước: {order}")
    # ── hàng đợi có giới hạn / không giới hạn
    _, rej = tick_sim([10 ** 6] * 10, 4, 2)
    rec("L16", (10 - len(rej), len(rej)) == (6, 4) == alg.bnx_pool_admit(10, 4, 2) and rej == [6, 7, 8, 9],
        "bể 4 luồng + hàng đợi 2 chỗ, gửi liền 10 việc: nhận 6, từ chối 4 (việc thứ 7 tới 10)")
    backlog, per_s = 0, 0
    for _s in range(60):                        # từng giây: tới 50, xử lý 4 luồng · (1000 / 100)
        per_s = sum(1000 // 100 for _ in range(4))
        backlog += 50 - per_s
    rec("L16", per_s == 40 == alg.bnx_pool_throughput(4, 100) and backlog == 600 == alg.bnx_queue_backlog(50, 4, 100, 60)
        and backlog / per_s == 15 and 20 / per_s == 0.5,
        "số minh hoạ: 40 việc/giây, tới 50/giây → 600 việc chờ sau 60 giây; việc cuối chờ 15 giây; hàng 20 chỗ chờ tối đa 0,5 giây")
    # ── chia đôi
    n_leaf, sizes = leaves_by_size(10 ** 6, 10 ** 4)
    k = next(k for k in range(64) if 10 ** 6 / 2 ** k <= 10 ** 4)
    rec("L16", n_leaf == 128 == 2 ** k == alg.bnx_fj_leaves(1, 10 ** 6, 10 ** 4) and k == 7 == alg.bnx_fj_depth(10 ** 6, 10 ** 4)
        and sorted(set(sizes)) == [7812, 7813] and sum(sizes) == 10 ** 6 and 10 ** 6 / 2 ** 6 == 15625 and 10 ** 6 / 2 ** 7 == 7812.5,
        "chia đôi 1 000 000 số, ngưỡng 10 000: 7 lần chia, 128 lá cỡ 7812 hoặc 7813 (duyệt theo số phần tử); 2^6 còn 15 625 > ngưỡng")
    rec("L16", sum(range(1, 10 ** 6 + 1)) == 500000500000 == alg.bnx_fj_sum(1, 10 ** 6, 10 ** 4) == alg.bnx_gauss(10 ** 6)
        == 10 ** 6 * (10 ** 6 + 1) // 2, "tổng 1..1 000 000 = 500 000 500 000 (sum(range) = cây chia đôi = công thức)")
    rec("L16", leaves_by_size(500000, 10 ** 4)[0] == 64 == alg.bnx_fj_leaves(1, 500000, 10 ** 4), "nửa cây (500 000 số) có 64 lá")
    # ── bể dùng chung
    es, _ = tick_sim([300, 400, 0], 2)
    shared = [n for _, _, n in sorted(zip(es, [0, 0, 1], ["chờ 300", "chờ 400", "tính"]))]
    rec("L16", es == [300, 400, 300] and shared == ["chờ 300", "tính", "chờ 400"] and alg.bnx_shared_order([300, 400], 2, True) == (shared, 300)
        and alg.bnx_shared_order([300, 400], 2, False) == (["tính", "chờ 300", "chờ 400"], 0),
        "bể chung 2 luồng: việc tính phải đợi 300 ms, xong sau 'chờ 300'; tách bể thì xong trước tiên")
    # ── câu hỏi
    q1, _ = tick_sim([200] * 8, 3)
    q2, _ = tick_sim([150, 250, 100, 500], 4)
    rec("L16", max(q1) == 600 == alg.bnx_pool_makespan([200] * 8, 3) and len(set(q1)) == 3 == alg.bnx_pool_rounds(8, 3)
        and max(q2) == 500 == alg.bnx_pool_makespan([150, 250, 100, 500], 4) and 150 + 250 + 100 + 500 == 1000
        == alg.bnx_pool_makespan([150, 250, 100, 500], 1), "câu 1: 3 lượt, 600 ms; câu 2: lần lượt 1000 ms, song song 500 ms")
    # ── chạy thật Java, nguyên văn hằng mã của bài
    if not (shutil.which("javac") and shutil.which("java")):
        rec("L16", None, "thiếu javac/java (NOT_VERIFIED: sáu chương trình Java chưa chạy)")
    else:
        for const, outc, what in (("J_POOL", "OUT_POOL", "bể 4 luồng: 4 luồng, tổng 385, 3 lượt"),
                                  ("J_QUEUE", "OUT_QUEUE", "hàng đợi 2 chỗ: nhận 6, từ chối 4"),
                                  ("J_CF", "OUT_CF", "ghép ba lời gọi: thứ tự xong, khả dụng 800, điểm 700, chờ < 900 ms"),
                                  ("J_FJ", "OUT_FJ", "chia đôi: tổng 500000500000, 128 việc lá"),
                                  ("J_SHARED", "OUT_SHARED", "bể chung so với tách bể"),
                                  ("J_CHECK", "OUT_CHECK", "một luồng: cùng tổng, cùng 128 lá")):
            outs = [run_java(getattr(src, const), src.JAVA_CLASS[const]) for _ in range(2)]
            want = getattr(src, outc).strip("\n") + "\n"
            rec("L16", all(rc == 0 and so == want for rc, so in outs),
                f"{src.JAVA_CLASS[const]}.java chạy thật 2 lần (javac + java), đầu ra khớp NGUYÊN VĂN khối trên màn hình — {what}")
    if shutil.which("javac") and shutil.which("java"):
        rc, so = run_java(J_EXTRA, "Phu")
        lines = so.strip().split("\n") if rc == 0 else []
        rec("L16", rc == 0 and len(lines) == 7 and "TimeoutException" in lines[1] and lines[2].endswith("true")
            and lines[3] == "join: CompletionException <- IllegalStateException" and lines[4] == "exceptionally: -1",
            f"chạy thật (bộ kiểm): hạn chờ orTimeout báo TimeoutException nhưng việc kế đợi hơn 1000 ms (luồng vẫn bận); join bọc lỗi gốc "
            f"trong CompletionException, exceptionally nhận lỗi: {lines[1:5]}")
        rec("L16", rc == 0 and len(lines) == 7 and lines[5] == "lõi2/tối đa4/hàng2: luồng 4, hàng 2, nhận 6, từ chối 1"
            and lines[6] == "không giới hạn: luồng 2, hàng 8",
            f"ThreadPoolExecutor: lõi 2, tối đa 4, hàng 2 chỗ nhận 6 việc (4 luồng + 2 chờ), từ chối việc thứ 7; hàng không giới hạn thì luồng không vượt số lõi: {lines[5:7]}")
        # bể chung khi chỉ có một nhân (container giới hạn 1 nhân): mỗi việc một luồng mới, không phải luồng của bể chung
        rc1, so1 = run_java(J_EXTRA, "Phu", ("-XX:ActiveProcessorCount=1",))
        l1 = so1.strip().split("\n") if rc1 == 0 else []
        rc4, so4 = run_java(J_EXTRA, "Phu", ("-XX:ActiveProcessorCount=4",))
        l4 = so4.strip().split("\n") if rc4 == 0 else []
        rec("L16", bool(l1) and bool(l4) and l1[0].startswith("chung: par=1 Thread-") and "daemon=false" in l1[0]
            and l4[0].startswith("chung: par=3 ForkJoinPool.commonPool-worker-") and "daemon=true" in l4[0],
            f"bể chung: 1 nhân → mức song song 1 (dưới 2) nên việc chạy trên luồng mới Thread-n (không phải daemon); 4 nhân → mức song song 3, luồng của bể chung: {l1[:1]} / {l4[:1]}")
    else:
        rec("L16", None, "thiếu javac/java (NOT_VERIFIED: ca bổ sung F1/F2/F3 chưa chạy)")
    consts = [getattr(src, c) for c in src.JAVA_CLASS]
    lines = [l for c in consts for l in c.strip("\n").split("\n")]
    rec("L16", max(map(len, lines)) <= 70, f"dòng mã dài nhất {max(map(len, lines))} ký tự (≤ 70)")
