"""BNX L13 — Dockerfile, GitLab CI, Deployment Kubernetes: mô hình bằng Python thuần (không YAML, không Docker, không mạng).
Bộ kiểm audit/bnx/ver/l13.py phân tích YAML thật bằng pyyaml và mô phỏng bằng cách KHÁC (liệt kê mọi trạng thái, chuỗi khoá đệm)."""
import math as _m


def bnx_k8s_abs(val, replicas, round_up):
    """maxSurge/maxUnavailable: số tuyệt đối giữ nguyên; phần trăm → maxUnavailable làm tròn xuống, maxSurge làm tròn lên (tài liệu Deployment)."""
    if isinstance(val, str) and val.endswith("%"):
        x = replicas * int(val[:-1]) / 100
        return _m.ceil(x) if round_up else _m.floor(x)
    return int(val)


def bnx_rolling_bounds(replicas, max_unavailable, max_surge):
    """(số bản sẵn sàng tối thiểu, số Pod tối đa) trong lúc cập nhật cuốn chiếu."""
    mu = bnx_k8s_abs(max_unavailable, replicas, False)
    ms = bnx_k8s_abs(max_surge, replicas, True)
    return replicas - mu, replicas + ms


def bnx_rolling_waves(replicas, max_unavailable, max_surge):
    """Bộ điều khiển Deployment theo đúng quy tắc mã nguồn Kubernetes (pkg/controller/deployment/rolling.go, util/deployment_util.go):
    mỗi lần đồng bộ: (1) TĂNG RS mới trước: scaleUp = min(replicas + maxSurge − tổng Pod, replicas − số Pod RS mới); có tăng thì kết thúc lần đồng bộ;
    (2) không tăng được thì GIẢM RS cũ: maxScaledDown = tổng Pod − minAvailable − số Pod mới chưa sẵn sàng; > 0 thì giảm
    min(số sẵn sàng − minAvailable, số Pod cũ). Lặp tới khi đứng yên, rồi CHỜ: mọi Pod mới đang khởi động cùng sẵn sàng (giả định
    khởi động đều nhau) — mỗi lần chờ là một ĐỢT.
    Trả (hàng, vết): hàng = [(đợt, cũ, mới đang khởi động, mới sẵn sàng, Pod, sẵn sàng)] lúc bắt đầu chờ; vết = mọi trạng thái (cũ, sẵn sàng mới, khởi động)."""
    lo = replicas - bnx_k8s_abs(max_unavailable, replicas, False)
    hi = replicas + bnx_k8s_abs(max_surge, replicas, True)
    old, ready, start = replicas, 0, 0
    rows, trace = [], [(old, ready, start)]
    for _ in range(100):
        while True:
            total = old + ready + start
            up = min(hi - total, replicas - (ready + start))
            if up > 0:
                start += up
                trace.append((old, ready, start))
                continue
            if total - lo - start > 0 and old:
                down = min(old + ready - lo, old)
                if down > 0:
                    old -= down
                    trace.append((old, ready, start))
                    continue
            break
        if not start:
            return rows, trace
        rows.append((len(rows) + 1, old, start, ready, old + ready + start, old + ready))
        ready, start = ready + start, 0
        trace.append((old, ready, start))
    raise RuntimeError("không hội tụ")


def bnx_rolling_summary(replicas, max_unavailable, max_surge):
    """(số đợt chờ sẵn sàng, sẵn sàng thấp nhất, số Pod cao nhất) trên MỌI trạng thái của vết."""
    rows, trace = bnx_rolling_waves(replicas, max_unavailable, max_surge)
    return len(rows), min(o + r for o, r, s in trace), max(o + r + s for o, r, s in trace)


def bnx_pipeline(stages, job_stage, failed):
    """Ngữ nghĩa GitLab: giai đoạn chạy theo thứ tự; job cùng giai đoạn chạy song song; một job hỏng thì job ở giai đoạn sau không chạy.
    job_stage: {job: giai đoạn}; failed: tập job sẽ hỏng nếu được chạy. Trả {job: 'success' | 'failed' | 'skipped'}."""
    st, broken = {}, False
    for s in stages:
        for j in [j for j, g in job_stage.items() if g == s]:
            st[j] = "skipped" if broken else ("failed" if j in failed else "success")
        if any(st[j] == "failed" for j, g in job_stage.items() if g == s):
            broken = True
    return st


def bnx_cache_rebuilt(steps, changed):
    """steps: [(lệnh, tập tệp đầu vào)] theo thứ tự trong Dockerfile; changed: tập tệp vừa sửa.
    Lớp đầu tiên có tệp đầu vào đổi bị dựng lại, và MỌI lớp sau nó cũng dựng lại. Trả danh sách chỉ số (từ 1) phải chạy lại."""
    for i, (_, inputs) in enumerate(steps):
        if inputs & changed:
            return list(range(i + 1, len(steps) + 1))
    return []


# Giai đoạn dựng của Dockerfile trong bài: tệp đầu vào của từng lệnh (src/ là cả thư mục mã nguồn)
bnx_df_good = [("FROM maven", set()), ("WORKDIR /src", set()), ("COPY pom.xml", {"pom.xml"}),
               ("RUN dependency:go-offline", set()), ("COPY src", {"src/Main.java"}), ("RUN package", set())]
bnx_df_bad = [("FROM maven", set()), ("WORKDIR /src", set()), ("COPY . .", {"pom.xml", "src/Main.java"}), ("RUN package (tải + dịch)", set())]


def bnx_build_seconds(steps, changed, cost):
    """Thời gian dựng lại = tổng thời gian các lệnh phải chạy lại (cost: {lệnh: giây}, số minh hoạ)."""
    return sum(cost.get(steps[i - 1][0], 0) for i in bnx_cache_rebuilt(steps, changed))


def bnx_short_sha(full):
    """CI_COMMIT_SHORT_SHA: tám ký tự đầu của CI_COMMIT_SHA (tài liệu biến định sẵn của GitLab)."""
    return full[:8]
