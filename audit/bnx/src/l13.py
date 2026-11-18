import lib2
from lib2 import *
from labkit import write_lab, practice_steps, practice_scene
from spk12 import spoken
from libj import jstep, nowrap

lib2.begin("L13")

# ── Mã trên màn hình. Dockerfile và YAML không chạy được trên máy (không có cụm Kubernetes, không có máy chạy GitLab):
#    sổ audit/bnx/screen/l13.yaml ghi `other` + read_check; audit/bnx/ver/l13.py phân tích YAML thật bằng pyyaml và mô phỏng.
#    Dockerfile được kiểm thật bằng `docker build --check` (nguồn src:BNX:L13_df_good / L13_df_bad trong sổ).
DOCKERFILE = r"""
FROM maven:3.9.9-eclipse-temurin-21 AS build
WORKDIR /src
COPY pom.xml .
RUN mvn -q dependency:go-offline
COPY src ./src
RUN mvn -q package -DskipTests
FROM eclipse-temurin:21.0.5_11-jre
WORKDIR /app
COPY --from=build /src/target/chuyen-tien.jar app.jar
USER 10001
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
"""
CI_YML = r"""
stages: [build, test, package, deploy]
variables:
  IMG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
build:
  stage: build
  script: mvn -q compile
test:
  stage: test
  script: mvn -q test
package:
  stage: package
  script:
    - echo "$CI_REGISTRY_PASSWORD" |
      docker login $CI_REGISTRY -u $CI_REGISTRY_USER --password-stdin
    - docker build -t $IMG .
    - docker push $IMG
deploy:
  stage: deploy
  script:
    - kubectl set image deployment/chuyen-tien app=$IMG
    - kubectl rollout status deployment/chuyen-tien
"""
DEPLOY_YML = r"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chuyen-tien
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels: {app: chuyen-tien}
  template:
    metadata:
      labels: {app: chuyen-tien}
    spec:
      containers:
        - name: app
          image: registry.vd.vn/bnx/chuyen-tien:0eac7e6a
          ports: [{containerPort: 8080}]
          readinessProbe:
            httpGet: {path: /ready, port: 8080}
"""
PY_ROLL = r"""
D, MU, MS = 4, 1, 1
seen, todo = set(), [(D, 0, 0)]  # (cũ, mới sẵn sàng, mới khởi động)
while todo:
    c, r, k = s = todo.pop()
    if s in seen: continue
    seen.add(s)
    if c + r + k < D + MS and r + k < D: todo.append((c, r, k + 1))
    if c and c - 1 + r >= D - MU: todo.append((c - 1, r, k))
    if k: todo.append((c, r + 1, k - 1))
print(len(seen), min(c + r for c, r, k in seen),
      max(c + r + k for c, r, k in seen), (0, D, 0) in seen)
"""
PY_ROLL_OUT = """
24 3 5 True
"""
BAD_DF = r"""
FROM eclipse-temurin:latest
ENV DB_PASSWORD=MatKhau123
COPY . /app
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
"""
BAD_DF_OUT = """
Check complete, 1 warning has been found!
WARNING: SecretsUsedInArgOrEnv - https://docs.docker.com/go/…
Do not use ARG or ENV instructions for sensitive data …
   2 | >>> ENV DB_PASSWORD=MatKhau123
"""

MERGE_SHA = "0eac7e6a33ba9714db9a6ca6a6ca184cd627bbf5"   # commit gộp của bài 0 (git thật, tái lập được)

# Quy mô: mô phỏng số đợt cập nhật cuốn chiếu (mỗi đợt thay tối đa thiếu + thừa bản); chạy THẬT bằng Python, KHÔNG phải cụm thật
DOT_PY = """def so_dot(D, mu, ms):
    san, dot = 0, 0
    while san < D:
        san += min(mu + ms, D - san)
        dot += 1
    return dot

def hang(D, mu, ms):
    print(D, mu, ms, so_dot(D, mu, ms), D - mu, D + ms)

for D in (4, 40, 400):
    hang(D, 1, 1)
for D in (4, 40, 400):
    hang(D, D // 4, -(-D // 4))
hang(400, 0, 40)"""
DOT_OUT = """4 1 1 2 3 5
40 1 1 20 39 41
400 1 1 200 399 401
4 1 1 2 3 5
40 10 10 2 30 50
400 100 100 2 300 500
400 0 40 10 400 440"""
DOT = prog("Dot", DOT_PY, lang="python", out=DOT_OUT,
           claims=["mô phỏng số đợt cập nhật cuốn chiếu: thiếu 1, thừa 1 cần 2, 20, 200 đợt ở 4, 40, 400 bản; mặc định 25% cần 2 đợt ở 4, 40, 400 bản (D chia 4 dư 3, như 3 hay 7, cần 3 đợt); cấu hình (0, 40) ở 400 bản cần 10 đợt",
                   "số bản sẵn sàng tối thiểu D − thiếu và số Pod tối đa D + thừa ở từng cấu hình"],
           unverified_claims=["đây là mô phỏng bằng công thức đợt = ceil(D / (thiếu + thừa)), đối chiếu với bộ điều khiển mô phỏng theo mã nguồn Kubernetes ở ver/l13.py trên lưới D ≤ 60; KHÔNG chạy trên cụm Kubernetes thật; 30 giây mỗi đợt là số minh hoạ"])

# Lab (số liệu khác ví dụ): Dockerfile 6 lớp, sửa một tệp mã / sửa pom.xml / Dockerfile sai thứ tự; cập nhật cuốn chiếu D = 12 và D = 10 (25%)
LAB_PY = """tot = [("FROM", [], 5), ("WORKDIR", [], 1), ("COPY pom.xml", ["pom.xml"], 1),
       ("RUN tai phu thuoc", [], 80),
       ("COPY src", ["src/Dao.java", "src/Main.java"], 2), ("RUN dong goi", [], 25)]
xau = [("FROM", [], 5),
       ("COPY . .", ["pom.xml", "src/Dao.java", "src/Main.java"], 3),
       ("RUN tai va dong goi", [], 105)]


def dung_lai(lop, sua):
    for i, (ten, dau_vao, giay) in enumerate(lop):
        if sua in dau_vao:
            return list(range(i + 1, len(lop) + 1)), sum(l[2] for l in lop[i:])
    return [], 0


def so_dot(D, mu, ms):
    san, dot = 0, 0
    while san < D:
        san += min(mu + ms, D - san)
        dot += 1
    return dot


for sua in ("src/Dao.java", "pom.xml"):
    cac, giay = dung_lai(tot, sua)
    print("sua", sua + ":", "lop", *cac, "-", giay, "giay")
print("sai thu tu, sua src/Dao.java:", dung_lai(xau, "src/Dao.java")[1], "giay")
D, mu, ms = 12, 1, 2
print(f"D={D} thieu {mu} thua {ms}:", so_dot(D, mu, ms), "dot, toi thieu", D - mu, "toi da", D + ms)
D = 10
mu, ms = D // 4, -(-D // 4)
print(f"D={D} 25%/25%:", so_dot(D, mu, ms), "dot, toi thieu", D - mu, "toi da", D + ms)"""
_lp = lib2.Prog("L13", "LabSol", LAB_PY, "python", {}, "lab", {})
_rc, _so, _se = _lp.execute()
assert _rc == 0, _se
LAB_OUT = _so.strip("\n")
EXPECT_LAB = """sua src/Dao.java: lop 5 6 - 27 giay
sua pom.xml: lop 3 4 5 6 - 108 giay
sai thu tu, sua src/Dao.java: 108 giay
D=12 thieu 1 thua 2: 4 dot, toi thieu 11 toi da 14
D=10 25%/25%: 2 dot, toi thieu 8 toi da 13"""
assert LAB_OUT == EXPECT_LAB, LAB_OUT

LAB_DE = """# Lab BNX L13 — Lớp Dockerfile phải dựng lại và số đợt cập nhật cuốn chiếu

Bài này không cần Docker hay Kubernetes: ta **mô phỏng** (mô hình Python, không phải Docker hay cụm thật) hai quy tắc đã học (`mau.py`, chỉ dùng Python có sẵn). Số liệu là số minh hoạ.

**Phần 1 — bộ nhớ đệm của lớp.** Mỗi lớp là một bộ `(tên, tệp đầu vào, số giây dựng)`. Chép hai danh sách này vào đầu tệp:

```python
tot = [("FROM", [], 5), ("WORKDIR", [], 1), ("COPY pom.xml", ["pom.xml"], 1),
       ("RUN tai phu thuoc", [], 80),
       ("COPY src", ["src/Dao.java", "src/Main.java"], 2), ("RUN dong goi", [], 25)]
xau = [("FROM", [], 5),
       ("COPY . .", ["pom.xml", "src/Dao.java", "src/Main.java"], 3),
       ("RUN tai va dong goi", [], 105)]
```

Quy tắc: lớp đầu tiên có tệp đầu vào vừa sửa phải dựng lại, và **mọi lớp sau nó** cũng vậy. Viết hàm `dung_lai(lop, sua)` trả về (danh sách số thứ tự lớp từ 1 phải dựng lại, tổng số giây). Rồi in ba dòng:

- `sua src/Dao.java: lop <các số> - <giây> giay` và `sua pom.xml: lop <các số> - <giây> giay` (danh sách `tot`);
- `sai thu tu, sua src/Dao.java: <giây> giay` (danh sách `xau`).

**Phần 2 — cập nhật cuốn chiếu.** `D` bản, được thiếu tối đa `mu` bản, thừa tối đa `ms` bản. Mỗi đợt chờ sẵn sàng thay tối đa `mu + ms` bản mới; sẵn sàng tối thiểu là `D − mu`, số Pod tối đa là `D + ms`. Khi viết bằng phần trăm: `mu` làm tròn **xuống**, `ms` làm tròn **lên**. In hai dòng (số đợt = số lần thay tối đa `mu + ms` bản cho tới khi đủ `D` bản mới):

- `D=12 thieu 1 thua 2: <đợt> dot, toi thieu <số> toi da <số>`
- `D=10 25%/25%: <đợt> dot, toi thieu <số> toi da <số>`

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L13 mau.py`. Đầu ra viết không dấu.
"""


def code_(t, **kw):
    """Khối mã có dấu $: tách mỗi $ thành một nút chữ riêng để KaTeX không coi đoạn giữa hai dấu $ là công thức."""
    return code(t, **kw).replace("$", "<span>&#36;</span>")


def note(t):
    return f"<p class='note'>{t}</p>"


def build():
    write_lab("BNX", "L13", LAB_DE, "py", LAB_PY, LAB_OUT)
    rows, _trace = alg_waves()
    hook = sc("hook", "hook", "Bản mới lên lúc 17 giờ, khách báo lỗi lúc 17 giờ 10", [
        st("""<p>Chiều thứ Sáu, bản mới của dịch vụ chuyển tiền chạy trên <b>4</b> bản trong cụm Kubernetes (hệ thống chạy dịch vụ trên nhiều máy). Mười phút sau, tổng đài báo khách chuyển tiền lỗi <span class='note'>(tình huống minh hoạ)</span>.</p>
<div class="box warn">Đang chạy bản nào? Bản đó làm từ dòng mã nào, đã qua kiểm thử chưa? Quay về bản cũ có làm khách gián đoạn không?</div>""",
           """Chào bạn, chiều thứ Sáu bản mới của dịch vụ chuyển tiền vừa chạy trên bốn bản trong cụm Kubernetes, tức hệ thống chạy dịch vụ trên nhiều máy, đây là tình huống minh hoạ.
           Mười phút sau tổng đài báo khách chuyển tiền bị lỗi. Câu hỏi đầu tiên là máy chủ chạy bản nào, từ dòng mã nào, đã qua kiểm thử chưa.""",
           focus=[1, 1, 2]),
        st(table(["câu hỏi", "bài này trả lời bằng"],
                 [["đóng gói dịch vụ Java thế nào?", "tệp dựng ảnh: phụ thuộc trước, mã sau; ghim (cố định) ảnh nền"],
                  ["ai chặn bản lỗi trước khi lên máy chủ?", "đường ống 4 giai đoạn: test hỏng thì package và deploy không chạy"],
                  ["thay bản mà khách không gián đoạn?", "thay dần: ≥ 3 sẵn sàng, ≤ 5 chạy; quay về bản cũ cũng thay dần"],
                  ["truy ngược từ máy chủ về mã?", "thẻ ảnh = 8 ký tự đầu của mã commit"],
                  ["400 bản thì thay hết mất bao lâu?", "đếm số đợt thay ở 4, 40 và 400 bản (mô phỏng)"]]),
           """Bài này đi hết con đường từ một lần chốt mã tới máy chủ. Tệp công thức dựng ảnh đóng gói dịch vụ Java, và đường ống bốn giai đoạn chặn bản lỗi. Thay dần giúp khách không thấy gián đoạn, còn thẻ ảnh mang mã chốt để truy ngược về mã.""",
           focus=[0, ["1.2", "1.3"], ["1.4", "1.5"], "1.6"]),
    ])
    pre = sc("prereq", "prereq", "Trước hết: sáu điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① container", "tiến trình chạy cô lập: có <b>hệ tệp</b> (cây thư mục và tệp nó nhìn thấy), mạng, giới hạn bộ nhớ riêng; mọi container trên một máy dùng chung <b>nhân</b> (lõi của hệ điều hành, điều khiển phần cứng)", "dịch vụ chuyển tiền"],
                  ["② ảnh (image)", "gói chỉ đọc gồm hệ tệp và lệnh khởi động; chạy ảnh thì được container", "<code>chuyen-tien:0eac7e6a</code>"],
                  ["③ tệp jar", "Java gói mã đã biên dịch thành một tệp, chạy bằng <code>java -jar</code>", "<code>app.jar</code>"],
                  ["④ cụm, Kubernetes", "cụm: nhiều máy chủ gom lại; Kubernetes: phần mềm đặt container lên các máy trong cụm và giữ đủ số bản", "cụm 3 máy, 4 bản"],
                  ["⑤ cập nhật cuốn chiếu", "thay dần bản cũ bằng bản mới, luôn còn bản phục vụ khách", "4 bản, thay dần"],
                  ["⑥ mã chốt, Dockerfile, YAML", "mã chốt (commit): mã nhận dạng một lần lưu mã vào kho Git; Dockerfile: tệp công thức dựng ảnh; YAML: định dạng cấu hình viết bằng dòng thụt lề", "<code>0eac7e6a…</code>"]]),
           """Trước hết ta cần hiểu sáu điều. Một, tiến trình cô lập có cây thư mục, mạng và bộ nhớ riêng, nhưng dùng chung nhân, tức lõi của hệ điều hành.
           Hai, ảnh là gói chỉ đọc để chạy ra tiến trình đó. Ba, tệp đóng gói là mã Java đã biên dịch.
           Bốn, cụm là nhiều máy gom lại, còn Kubernetes đặt tiến trình lên máy trong cụm. Năm, cập nhật cuốn chiếu thay dần bản cũ nên luôn còn bản phục vụ.
           Sáu, mã chốt nhận dạng một lần lưu mã vào kho Git.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"], introduces=["bnx_cuon_chieu", "bnx_dockerfile"]),
        st("""$$4 - 1 = \\hl{3} \\text{ bản phục vụ khi đang thay 1 bản}, \\qquad \\frac{3}{4} = 75\\%$$""",
           """Ví dụ số nhỏ: có bốn bản, thay một bản thì còn ba bản phục vụ, tức ba phần tư, bằng bảy mươi lăm phần trăm sức chứa.""",
           introduces=["frac"], clear=True),
    ], checks=["4 - 1 == 3 and Fraction(3, 4) == Fraction(75, 100)", "alg.bnx_rolling_bounds(4, 1, 1)[0] == 3"])
    sym = sc("sym", "symbol", "Giải mã các từ hay gặp", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["phụ thuộc", "thư viện người khác viết mà dự án dùng, ví dụ Spring"],
                  ["Maven, lệnh <code>mvn</code>", "công cụ dựng của Java: tải phụ thuộc, biên dịch, chạy kiểm thử, đóng gói thành jar; <code>-q</code>: in ít chữ; <code>dependency:go-offline</code>: tải trước mọi phụ thuộc"],
                  ["<code>pom.xml</code>", "tệp khai báo dự án và danh sách phụ thuộc cho Maven"],
                  ["<code>-DskipTests</code>", "bỏ chạy kiểm thử lúc đóng gói, vì đường ống đã có giai đoạn kiểm thử riêng"]]),
           """Bảng đầu giải mã các từ của Java. Phụ thuộc là thư viện người khác viết mà dự án dùng, và công cụ dựng tải chúng về trước rồi biên dịch, kiểm thử, đóng gói. Tuỳ chọn cuối bỏ kiểm thử lúc đóng gói, vì đường ống đã có giai đoạn riêng.""",
           focus=[0, "1.2", ["1.3", "1.4"], "1.5"]),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["<code>FROM ảnh AS build</code>", "chọn ảnh nền; <code>AS build</code> đặt tên giai đoạn dựng"],
                  ["<code>COPY</code> / <code>RUN</code>", "chép tệp vào ảnh / chạy một lệnh lúc dựng; mỗi lệnh tạo một <b>lớp</b>"],
                  ["<code>COPY --from=build</code>", "chỉ lấy tệp jar từ giai đoạn dựng; ảnh chạy không chứa mã nguồn và công cụ dựng"],
                  ["<code>WORKDIR</code> / <code>EXPOSE</code> / <code>ENV</code>", "thư mục làm việc cho các lệnh sau / ghi chú cổng dịch vụ lắng nghe / đặt biến môi trường, một cặp tên=giá trị"],
                  ["<code>USER</code> / <code>ENTRYPOINT</code>", "chạy bằng người dùng không phải quản trị / lệnh khởi động khi container chạy"],
                  ["thẻ ảnh <code>tên:thẻ</code>", "tên phiên bản của ảnh; <code>…-jre</code> là Java chỉ có phần chạy chương trình, không có công cụ biên dịch; <code>latest</code> chỉ là một thẻ bình thường, không tự là “bản mới nhất”"]]),
           """Bảng thứ hai giải mã tệp dựng ảnh. Lệnh đầu chọn ảnh nền, mỗi lệnh chép hay chạy tạo một lớp, và lệnh chép từ giai đoạn dựng chỉ lấy tệp đóng gói nên ảnh gọn. Thẻ ảnh là tên phiên bản, còn nhãn mới nhất chỉ là một thẻ thường.""",
           clear=True, introduces=["bnx_workdir_expose"]),
        st(table(["từ", "nghĩa"],
                 [["đường ống (GitLab CI)", "mỗi lần đẩy commit lên kho GitLab, máy chạy đường ống đọc tệp <code>.gitlab-ci.yml</code> và tự chạy các việc trong đó"],
                  ["stage / job", "giai đoạn / việc; job cùng giai đoạn chạy song song"],
                  ["kho ảnh (registry)", "nơi lưu ảnh; <code>docker push</code> đẩy ảnh lên, máy trong cụm kéo ảnh về để chạy"],
                  ["<code>CI_COMMIT_SHORT_SHA</code>", "biến có sẵn: 8 ký tự đầu của mã commit đang dựng"],
                  ["<code>CI_REGISTRY_USER</code>, <code>CI_REGISTRY_PASSWORD</code>", "tài khoản đường ống cấp sẵn để đẩy ảnh lên kho ảnh của dự án; mật khẩu chỉ dùng được khi job đang chạy"]]),
           """Bảng thứ ba giải mã đường ống. Mỗi lần đẩy một lần chốt lên kho mã, máy tự chạy các việc theo giai đoạn, rồi đẩy ảnh lên kho ảnh với thẻ là tám ký tự đầu của mã chốt.""",
           clear=True, introduces=["bnx_kho_anh"]),
        st(table(["từ", "nghĩa"],
                 [["Pod", "bản chạy nhỏ nhất Kubernetes quản lý, ở đây gồm một container"],
                  ["Deployment, <code>replicas</code>", "đối tượng khai báo “muốn có 4 bản của ảnh này”"],
                  ["nhãn, bộ chọn", "nhãn là cặp tên = giá trị gắn lên Pod (<code>app: chuyen-tien</code>); bộ chọn tìm mọi Pod có nhãn đó"],
                  ["bộ điều khiển", "chương trình trong Kubernetes liên tục so số bản muốn với số bản thật rồi tạo, xoá Pod cho khớp"],
                  ["<code>maxUnavailable</code> / <code>maxSurge</code>", "lúc cập nhật: được thiếu tối đa / được thừa tối đa bao nhiêu bản so với <code>replicas</code>"],
                  ["<code>readinessProbe</code>, <code>kubectl</code>", "phép kiểm sẵn sàng: chỉ nhận yêu cầu khi trả lời được đường dẫn kiểm / lệnh gửi yêu cầu tới Kubernetes"]]),
           """Bảng cuối giải mã Kubernetes. Đối tượng triển khai khai báo muốn có bốn bản, nhãn gắn lên bản chạy và bộ chọn tìm mọi bản mang nhãn đó. Bộ điều khiển so số bản muốn với số bản thật rồi tạo hay xoá cho khớp.""",
           clear=True, introduces=["bnx_pod"]),
    ])
    intu = sc("intuition", "intuition", "Hình dung: từ commit tới máy chủ, và bộ nhớ đệm của lớp", [
        st(svg(1500, 470,
               box(20, 60, 190, 90, ["commit", "0eac7e6a"], C_GRAY, size=22, bold=True),
               box(260, 60, 170, 90, "build", C_GREEN, bold=True), box(470, 60, 170, 90, "test", C_GREEN, bold=True),
               box(680, 60, 170, 90, "package", C_GREEN, bold=True), box(890, 60, 170, 90, "deploy", C_GREEN, bold=True),
               box(1110, 40, 370, 130, ["Kubernetes", "4 Pod chạy ảnh", ":0eac7e6a"], C_BLUE, size=22, bold=True),
               arrow(210, 105, 255, 105), arrow(430, 105, 465, 105), arrow(640, 105, 675, 105), arrow(850, 105, 885, 105), arrow(1060, 105, 1105, 105),
               box(20, 290, 190, 90, ["commit", "mới"], C_GRAY, size=22, bold=True),
               box(260, 290, 170, 90, "build", C_GREEN, bold=True), box(470, 290, 170, 90, ["test", "hỏng"], C_RED, size=22, bold=True),
               box(680, 290, 170, 90, ["package", "không chạy"], C_GRAY, size=20, dash=True), box(890, 290, 170, 90, ["deploy", "không chạy"], C_GRAY, size=20, dash=True),
               box(1110, 290, 370, 90, ["máy chủ giữ", "bản :0eac7e6a"], C_BLUE, size=22),
               arrow(210, 335, 255, 335), arrow(430, 335, 465, 335),
               txt(750, 230, "giai đoạn sau chỉ chạy khi mọi job của giai đoạn trước thành công", 24, "middle", "#1f2937", True),
               txt(750, 440, "test hỏng: không có ảnh mới, không ai phải quay lui", 24, "middle", "#dc2626", True)),
           """Hình trên là con đường của một lần chốt: bốn giai đoạn dựng, kiểm thử, đóng gói, triển khai, rồi bốn bản chạy ảnh mang thẻ là mã chốt.
           Hàng dưới là lần chốt lỗi: kiểm thử hỏng nên hai giai đoạn sau không chạy, máy chủ giữ bản cũ."""),
        st(svg(1500, 470,
               txt(360, 40, "Thứ tự đúng: tệp phụ thuộc trước", 26, "middle", "#16a34a", True),
               box(60, 60, 600, 52, "1  FROM maven:3.9.9-…", C_GREEN, size=22), box(60, 118, 600, 52, "2  WORKDIR /src", C_GREEN, size=22),
               box(60, 176, 600, 52, "3  COPY pom.xml", C_GREEN, size=22), box(60, 234, 600, 52, "4  RUN tải phụ thuộc", C_GREEN, size=22),
               box(60, 292, 600, 52, "5  COPY src   (sửa một tệp ở đây)", C_AMBER, size=22), box(60, 350, 600, 52, "6  RUN biên dịch, đóng gói", C_AMBER, size=22),
               txt(1110, 40, "Thứ tự sai: chép tất cả trước", 26, "middle", "#dc2626", True),
               box(810, 60, 600, 52, "1  FROM maven:3.9.9-…", C_GREEN, size=22), box(810, 118, 600, 52, "2  WORKDIR /src", C_GREEN, size=22),
               box(810, 176, 600, 52, "3  COPY . .   (sửa một tệp ở đây)", C_AMBER, size=22), box(810, 234, 600, 52, "4  RUN tải phụ thuộc + biên dịch", C_AMBER, size=22),
               txt(750, 450, "xanh: dùng lại lớp đệm; cam: phải dựng lại (lớp đổi kéo theo mọi lớp sau)", 24, "middle", "#1f2937", True)),
           """Hình dưới là bộ nhớ đệm của các lớp: một lớp đổi thì mọi lớp sau phải dựng lại.
           Bên trái chép tệp phụ thuộc trước nên sửa một tệp mã chỉ dựng lại hai lớp cuối. Bên phải chép tất cả ngay từ đầu nên phải tải lại toàn bộ phụ thuộc."""),
    ], checks=["alg.bnx_pipeline(['build', 'test', 'package', 'deploy'], {'build': 'build', 'test': 'test', 'package': 'package', 'deploy': 'deploy'}, {'test'}) == {'build': 'success', 'test': 'failed', 'package': 'skipped', 'deploy': 'skipped'}",
               "alg.bnx_cache_rebuilt(alg.bnx_df_good, {'src/Main.java'}) == [5, 6] and alg.bnx_cache_rebuilt(alg.bnx_df_bad, {'src/Main.java'}) == [3, 4]",
               "alg.bnx_short_sha('0eac7e6a33ba9714db9a6ca6a6ca184cd627bbf5') == '0eac7e6a' and alg.bnx_git_demo()['merge'].startswith('0eac7e6a')"])
    form = sc("formula", "formula", "Suy ra từng bước: từ Dockerfile tới số Pod", [
        st(code_(DOCKERFILE),
           """Bước một là tệp dựng ảnh. Giai đoạn dựng tải phụ thuộc trước rồi mới chép mã nguồn, vì tệp phụ thuộc ít đổi còn mã đổi hằng ngày, nên lớp tải phụ thuộc được giữ trong bộ nhớ đệm."""),
        st("""<p><b>Làm thử</b> (số minh hoạ: tải phụ thuộc 90 giây, biên dịch và đóng gói 30 giây). Sửa một tệp trong <code>src</code>:</p>
$$\\text{đúng thứ tự: } \\hlg{30} \\text{ giây} \\qquad \\text{sai thứ tự: } 90 + 30 = \\hl{120} \\text{ giây}$$
""" + note("30 giây chỉ đúng khi đệm của lần trước còn được giữ. Máy chạy đường ống dùng một lần thì đệm trống: phải chủ động giữ đệm mới được lợi.")
           + note("Thẻ ảnh nền có thể bị nhà phát hành trỏ sang ảnh khác. Muốn bất biến thì ghim thêm chữ ký nội dung của ảnh (digest): một chuỗi băm, tức dãy ký tự ngắn cố định tính từ nội dung ảnh, nội dung đổi thì dãy đổi."),
           """Làm thử với số minh hoạ: tải phụ thuộc chín mươi giây, biên dịch và đóng gói ba mươi giây. Sửa một tệp mã thì đúng thứ tự chạy lại ba mươi giây, sai thứ tự mất một trăm hai mươi giây.
           Con số ba mươi chỉ đúng vì đệm của lần trước còn được giữ.""",
           clear=True, focus=[1, 2, [3, 4]]),
        jstep([("yflow", "<code>stages: [build, test, package, deploy]</code>: danh sách bốn giai đoạn; <code>- docker push …</code> trong <code>script</code>: một lệnh trong danh sách lệnh của job", ""),
               (("<code>IMG: $CI_REGISTRY_IMAGE:…</code>", "khai biến tên <code>IMG</code>; <code>$TÊN</code> được thay bằng giá trị của biến TÊN khi chạy", "Khai một biến tên ảnh, và dấu đô la đứng trước tên biến được thay bằng giá trị của biến đó khi chạy."), "<code>$CI_COMMIT_SHORT_SHA</code> thành <code>0eac7e6a</code>", "")]),
        st(code_(CI_YML, lines=(1, 9)) + note("Rút gọn: mỗi job còn cần khai <code>image:</code> có công cụ của nó (ở đây là Maven)."),
           """Bước hai là tệp mô tả đường ống. Dòng đầu khai báo bốn giai đoạn theo thứ tự chạy, và biến tên ảnh ghép địa chỉ kho ảnh với tám ký tự đầu của mã chốt.""",
           clear=True, focus=[1, 2]),
        jstep([(("<code>echo \"$CI_REGISTRY_PASSWORD\" | docker login … --password-stdin</code>", "<code>echo</code> in chữ ra; dấu <code>|</code> đưa chữ đó làm đầu vào lệnh sau; <code>docker login</code> đăng nhập kho ảnh, <code>-u</code> là tên tài khoản, <code>--password-stdin</code> đọc mật khẩu từ đầu vào thay vì gõ trong lệnh", "Lệnh in chữ ra, dấu gạch đứng đưa chữ đó vào lệnh đăng nhập kho ảnh, và tuỳ chọn đọc mật khẩu từ đầu vào giúp mật khẩu không gõ trong lệnh."), "mật khẩu chỉ đi qua đường ống, không hiện trong lệnh", ""),
               (("<code>docker build -t TÊN .</code>", "dựng ảnh từ thư mục hiện tại (dấu chấm) và đặt thẻ TÊN; <code>docker push TÊN</code>: đẩy ảnh lên kho", "Lệnh dựng ảnh lấy thư mục hiện tại, tức dấu chấm, và đặt thẻ cho ảnh, rồi lệnh đẩy gửi ảnh lên kho."), "<code>docker build -t $IMG .</code>", ""),
               (("<code>kubectl set image deployment/chuyen-tien app=$IMG</code>", "bảo Kubernetes đổi ảnh của bản chạy tên <code>app</code> trong đối tượng triển khai; <code>rollout status</code>: chờ tới khi thay xong", "Lệnh này bảo Kubernetes đổi ảnh của một bản chạy trong đối tượng triển khai, và lệnh trạng thái chờ tới khi thay xong."), "<code>kubectl set image deployment/chuyen-tien app=$IMG</code>", ""),
               ], clear=True),
        st(code_(CI_YML, lines=(10, 16)) + note("Rút gọn: job này còn cần dịch vụ Docker chạy kèm trong máy chạy đường ống."),
           """Việc đóng gói đăng nhập kho ảnh bằng tài khoản đường ống cấp sẵn, vì kho chỉ nhận ảnh từ người có quyền, rồi dựng ảnh, đặt thẻ là mã chốt ngắn và đẩy lên kho.""",
           clear=True, focus=[1, 1]),
        st(code_(CI_YML, lines=(17, 21)) + note("Rút gọn: job này còn cần ảnh có <code>kubectl</code> và quyền vào cụm."),
           """Việc triển khai đổi ảnh rồi chờ cập nhật xong, và chỉ bắt đầu khi mọi việc giai đoạn trước thành công, nên kiểm thử hỏng thì không có ảnh nào được đẩy lên.""",
           clear=True, focus=[1, 1]),
        st(table(["khoá trong YAML", "nghĩa"],
                 [["<code>apiVersion</code>, <code>kind</code>, <code>metadata</code>, <code>name</code>", "phiên bản khai báo, loại đối tượng (ở đây là Deployment), rồi tên của nó"],
                  ["<code>spec</code>, <code>template</code>", "<code>spec</code>: điều ta muốn (mấy bản, cập nhật thế nào); <code>template</code>: mẫu để tạo từng Pod"],
                  ["<code>containerPort: 8080</code>", "cổng: số cửa mạng mà dịch vụ lắng nghe; 8080 là số quen dùng cho dịch vụ web"],
                  ["<code>matchLabels: {app: chuyen-tien}</code>, <code>ports: [{containerPort: 8080}]</code>, <code>- name: app</code>", "YAML: <code>{k: v}</code> là cặp khoá và giá trị viết trên một dòng; <code>[…]</code> là danh sách; dòng bắt đầu bằng <code>-</code> là một phần tử của danh sách, ở đây là container tên <code>app</code>"]]),
           """Trước khi đọc tệp khai báo, ta cần biết vài khoá, vì tệp gồm các cặp khoá và giá trị. Các khoá đầu cho biết loại đối tượng và tên, khoá đặc tả ghi điều ta muốn, còn khoá mẫu tả từng bản chạy. Ngoặc nhọn gom một cặp khoá và giá trị trên một dòng, ngoặc vuông là danh sách, và dòng bắt đầu bằng gạch ngang là một phần tử của danh sách.
           Cổng là số cửa mạng mà dịch vụ lắng nghe.""", clear=True),
        st(code_(DEPLOY_YML, lines=(1, 11)),
           """Bước ba là tệp khai báo đối tượng triển khai, vì cụm chạy theo khai báo: bốn bản, cập nhật cuốn chiếu, được thiếu tối đa một bản và được thừa tối đa một bản.""",
           clear=True),
        st(code_(DEPLOY_YML, lines=(12, 23)),
           """Bộ chọn tìm các bản mang nhãn tên dịch vụ, và phần mẫu gắn đúng nhãn đó lên mỗi bản mới nên hai bên khớp nhau. Phép kiểm sẵn sàng gọi đường dẫn kiểm ở cổng tám nghìn không trăm tám mươi.""",
           clear=True),
        st("""$$\\text{sẵn sàng} \\geq 4 - 1 = \\hlg{3} \\qquad \\text{số Pod} \\leq 4 + 1 = \\hl{5}$$
<span class='note'>Làm thử: thiếu tối đa 1 nên luôn còn ít nhất 3 bản phục vụ; thừa tối đa 1 nên cụm phải có chỗ cho bản thứ 5.</span>""",
           """Từ hai tham số suy ra hai giới hạn. Được thiếu tối đa một nên số bản sẵn sàng luôn ít nhất bốn trừ một bằng ba.
           Được thừa tối đa một nên số bản chạy nhiều nhất bốn cộng một bằng năm, và cụm phải có chỗ cho bản thứ năm.""",
           clear=True, introduces=["geq"]),
    ], checks=["alg.bnx_build_seconds(alg.bnx_df_good, {'src/Main.java'}, {'RUN dependency:go-offline': 90, 'RUN package': 30}) == 30",
               "alg.bnx_build_seconds(alg.bnx_df_bad, {'src/Main.java'}, {'RUN package (tải + dịch)': 90 + 30}) == 120",
               "alg.bnx_rolling_bounds(4, 1, 1) == (3, 5)", "alg.bnx_short_sha(alg.bnx_git_demo()['merge']) == '0eac7e6a'"])
    ex = sc("example", "example", "Ví dụ cập nhật 4 bản, từng phép tính", [
        st("""<p>Đối tượng triển khai: <code>replicas: 4</code>, <code>maxUnavailable: 1</code>, <code>maxSurge: 1</code>; ảnh đổi sang thẻ mới.</p>
$$① \\; 4 - 1 = \\hlg{3} \\text{ bản sẵn sàng tối thiểu}$$
<span class='note'>(mô hình Python theo quy tắc của bộ điều khiển, không chạy trên cụm thật)</span>""",
           """Ta mô phỏng từng bước khi đổi bốn bản sang ảnh mới. Phép tính thứ nhất: số bản sẵn sàng tối thiểu là bốn trừ một, bằng ba."""),
        st("""$$② \\; 4 + 1 = \\hl{5} \\text{ Pod tối đa cùng lúc}$$""",
           """Phép tính thứ hai: số bản chạy tối đa cùng lúc là bốn cộng một, bằng năm."""),
        st("""<p>③ Đợt 1, theo quy tắc của bộ điều khiển: tạo 1 Pod mới (tổng 4 + 1 = 5) → xoá 1 Pod cũ (còn 4 − 1 = 3 sẵn sàng, đúng mức tối thiểu) → tạo thêm 1 Pod mới (tổng lại 3 + 2 = 5).</p>
<span class='note'>2 Pod mới khởi động cùng lúc, chưa qua phép kiểm sẵn sàng nên chưa được tính; bộ điều khiển chờ chúng.</span>""",
           """Phép tính thứ ba là đợt đầu: bộ điều khiển tạo một bản mới, xoá một bản cũ vì còn ba bản sẵn sàng, rồi tạo thêm một bản mới. Hai bản mới chưa qua phép kiểm nên chưa được tính.""",
           clear=True),
        st(table(["đợt chờ", "cũ", "mới đang khởi động", "mới sẵn sàng", "Pod", "sẵn sàng"],
                 [[str(c) for c in r] for r in rows] + [["xong", "0", "0", "4", "4", "4"]]) +
           """$$④ \\; \\text{2 đợt; mọi lúc: sẵn sàng} \\geq \\hlg{3},\\ \\text{Pod} \\leq \\hl{5}$$""",
           """Phép tính thứ tư, lặp lại cho đến hết: khi hai bản mới sẵn sàng, bộ điều khiển xoá hai bản cũ và tạo hai bản mới cuối. Vậy bốn bản được thay trong hai đợt, lúc nào cũng có ít nhất ba bản sẵn sàng và nhiều nhất năm bản chạy.""",
           clear=True, focus=[1, [1, 2]]),
        st("""<p>Mỗi Pod chịu 250 giao dịch/giây, tải lúc cập nhật 600 giao dịch/giây <span class='note'>(số minh hoạ)</span>. Dùng lại 3 ở ①:</p>
$$⑤ \\; 3 \\cdot 250 = \\hlg{750} \\geq 600 \\;\\Rightarrow\\; \\text{đủ sức chứa suốt lúc cập nhật}$$""",
           """Phép tính thứ năm nối với sức chứa: mỗi bản chịu hai trăm năm mươi giao dịch mỗi giây, tải là sáu trăm, đều là số minh hoạ.
           Ba nhân hai trăm năm mươi bằng bảy trăm năm mươi, lớn hơn sáu trăm, nên suốt lúc cập nhật vẫn đủ sức chứa.""",
           clear=True),
    ], checks=["alg.bnx_rolling_bounds(4, 1, 1) == (4 - 1, 4 + 1)",
               "alg.bnx_rolling_waves(4, 1, 1)[1][:4] == [(4, 0, 0), (4, 0, 1), (3, 0, 1), (3, 0, 2)]",
               "alg.bnx_rolling_waves(4, 1, 1)[0] == [(1, 3, 2, 0, 5, 3), (2, 1, 2, 2, 5, 3)] and alg.bnx_rolling_waves(4, 1, 1)[1][-1] == (0, 4, 0)",
               "alg.bnx_rolling_summary(4, 1, 1) == (2, 3, 5)",
               "3 * 250 == 750 and 750 >= 600"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: liệt kê mọi trạng thái", [
        st(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                 [["<code>c, r, k = s = todo.pop()</code>", "lấy một trạng thái ra; <code>s</code> là tên cả bộ, đồng thời tách ba số vào <code>c</code>, <code>r</code>, <code>k</code>", "<code>a, b = x = (1, 2)</code> thì x là (1, 2), a là 1, b là 2"],
                  ["<code>if k:</code>, <code>if c and …</code>", "số khác 0 tính là đúng, số 0 tính là sai", "<code>if 3:</code> chạy, <code>if 0:</code> không chạy"],
                  ["<code>(0, D, 0) in seen</code>", "đúng khi bộ ba đó có trong tập <code>seen</code>", "<code>(1, 2) in {(1, 2)}</code> là đúng"],
                  ["<code>max(c + r + k for … in seen)</code>, <code>print(a, b)</code>", "lấy số lớn nhất trong các giá trị tính từ mọi phần tử (<code>min</code>: nhỏ nhất); <code>print</code> in các giá trị cách nhau dấu cách", "<code>max(x * 2 for x in (1, 5))</code> ra 10"]]),
           """Trước khi đọc mã, ta cần bốn ký hiệu. Dòng lấy trạng thái ra vừa đặt một tên cho cả bộ, vừa tách ba số vào ba biến. Vì máy coi số khác không là đúng nên điều kiện có thể chỉ là một số. Phép thuộc hỏi một bộ có trong tập không, còn hàm lớn nhất lấy số lớn nhất trong các giá trị tính từ mọi phần tử."""),
        st(code(PY_ROLL) + note("<code>(c, r, k)</code> là bộ ba số; <code>set</code> là tập hợp không trùng phần tử; <code>while todo:</code> lặp tới khi hết việc chờ; <code>todo.pop()</code> lấy phần tử cuối; <code>continue</code> bỏ qua trạng thái đã xét; <code>.append</code>, <code>.add</code> thêm vào danh sách, tập hợp; <code>min(… for …)</code> lấy số nhỏ nhất trong các giá trị tính từ mọi phần tử."),
           """Ta kiểm bằng đường khác vì số tính tay có thể sai: mô hình Python, không phải cụm thật, liệt kê mọi trạng thái được phép. Mỗi trạng thái là bộ ba số gồm bản cũ, bản mới sẵn sàng và bản mới đang khởi động, và vòng lặp thử thêm bản mới, xoá bản cũ, hoặc cho bản mới sẵn sàng.""", clear=True),
        st(out(PY_ROLL_OUT, "Kết quả của mô hình Python (không phải cụm Kubernetes thật)"),
           """Kết quả có hai mươi bốn trạng thái, vì thế đã duyệt hết mọi cách đi. Sẵn sàng thấp nhất là ba, nhiều nhất năm bản chạy, và trạng thái thay xong hết tới được.""", clear=True),
        st(table(["cách đổi ra số", "maxUnavailable", "maxSurge", "sẵn sàng tối thiểu", "Pod tối đa"],
                 [["số tuyệt đối 1", "1", "1", "3", "5"],
                  ["mặc định 25% của 4 = 1", "làm tròn xuống: 1", "làm tròn lên: 1", "3", "5"]]),
           """Đường kiểm thứ hai dùng mặc định hai mươi lăm phần trăm: một phần tư của bốn là một, làm tròn xuống hay lên đều ra một.
           Vì vậy cấu hình mặc định cũng cho ba bản sẵn sàng tối thiểu và năm bản tối đa.""",
           clear=True),
    ], checks=["alg.bnx_rolling_bounds(4, '25%', '25%') == (3, 5) == alg.bnx_rolling_bounds(4, 1, 1)",
               "alg.bnx_k8s_abs('25%', 4, False) == 1 == alg.bnx_k8s_abs('25%', 4, True)",
               "alg.bnx_rolling_summary(4, 1, 1)[1:] == (3, 5)"])
    quymo = sc("quymo", "example", "Khi số bản lớn dần: cập nhật mất bao lâu (mô phỏng)", [
        jstep([("pdef", "<code>def so_dot(D, mu, ms):</code>: hàm nhận số bản D, số được thiếu mu, số được thừa ms; trả về số đợt", "hàm so đợt nhận ba số và trả về số đợt."),
               ("pwhile", "<code>while san &lt; D:</code>: lặp khi số bản đã thay san còn nhỏ hơn D", ""),
               (("<code>san += min(mu + ms, D - san)</code>", "<code>min(a, b)</code>: lấy số nhỏ hơn trong hai số; <code>+=</code>: cộng vào san", "Hàm lấy số nhỏ hơn chọn số bản thay trong đợt này, rồi cộng vào số đã thay."), "mỗi đợt thay tối đa mu cộng ms bản, và không quá số còn lại", ""),
               ("pfor", "<code>for D in (4, 40, 400):</code> chạy ba lần với D bằng 4, rồi 40, rồi 400; <code>print(…)</code> in các giá trị cách nhau dấu cách", "")]),
        st(DOT.show(lines=(1, 9), title="Mô phỏng (không phải cụm thật): mỗi đợt thay tối đa thiếu + thừa bản"),
           """Ta xem việc cập nhật đổi thế nào khi số bản lớn dần, bằng mô phỏng chạy thật nhưng không phải cụm thật.""",
           focus=[2, ["2.3", "2.4", "2.5"]], clear=True),
        st(DOT.show(lines=(11, 15)) + note("<code>D // 4</code> chia lấy phần nguyên, tức làm tròn xuống; <code>-(-D // 4)</code> làm tròn lên: với D = 10 ra −(−3) = 3.") + DOT.out_html(title="Kết quả: D, thiếu, thừa, số đợt, sẵn sàng tối thiểu, Pod tối đa"),
           """Ta chạy ở bốn, bốn mươi và bốn trăm bản, với thiếu một thừa một, với mặc định hai mươi lăm phần trăm, và với không thiếu, thừa bốn mươi.""",
           focus=[["1.1", "1.2", "1.3", "1.4", "1.5"], ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7"]], clear=True),
        st(table(["số bản D", "thiếu 1, thừa 1: số đợt", "chờ nếu 30 giây mỗi đợt (số minh hoạ)", "mặc định 25%: số đợt", "chờ"],
                 [[nowrap("4 (×1)"), "2", "1 phút", "2", "1 phút"],
                  [nowrap("40 (×10)"), "20", "10 phút", "2", "1 phút"],
                  [nowrap("400 (×100)"), "200", "100 phút, đúng 1 giờ 40", "2", "1 phút"]]) + note("Cỡ lẻ như D = 3 hoặc 7 (chia 4 dư 3) cần 3 đợt: làm tròn khiến mỗi đợt thay chưa tới một nửa."),
           """Với thiếu một thừa một, số đợt tăng thẳng theo số bản, nên bốn trăm bản mất hai trăm đợt, tức một giờ bốn mươi phút nếu mỗi đợt ba mươi giây. Còn mặc định hai mươi lăm phần trăm chỉ hai đợt ở ba cỡ này, vì mỗi đợt thay một nửa số bản.""",
           focus=[0, "1.4", "1.4"], clear=True),
        st(table(["cấu hình ở 400 bản", "số đợt", "sẵn sàng tối thiểu", "Pod tối đa", "được", "mất"],
                 [["thiếu 1, thừa 1", "200", "399", "401", "gần đủ sức chứa; chỉ cần chỗ cho 1 Pod thêm", "chậm: 100 phút"],
                  ["mặc định 25%", "2", "300", "500", "nhanh: 1 phút", "tụt 25% (còn 75% sức chứa); cần chỗ cho 100 Pod thêm"],
                  ["thiếu 0, thừa 40", "10", "400", "440", "không mất sức chứa; 5 phút", "cần chỗ cho 40 Pod thêm"]]),
           """Đây là đánh đổi người làm nghề phải chọn. Mặc định hai mươi lăm phần trăm nhanh nhưng sức chứa tụt còn bảy mươi lăm phần trăm, còn không cho thiếu mà cho thừa bốn mươi giữ nguyên sức chứa, mất năm phút.""",
           focus=[0, "1.3", "1.4"], clear=True),
    ], checks=["[alg.bnx_rolling_summary(D, 1, 1) for D in (4, 40, 400)] == [(2, 3, 5), (20, 39, 41), (200, 399, 401)]",
               "[alg.bnx_rolling_summary(D, '25%', '25%') for D in (4, 40, 400)] == [(2, 3, 5), (2, 30, 50), (2, 300, 500)]",
               "alg.bnx_rolling_summary(400, 0, 40) == (10, 400, 440)",
               "[alg.bnx_l13_phut(alg.bnx_l13_dot(D, 1, 1), 30) for D in (4, 40, 400)] == [1.0, 10.0, 100.0]",
               "alg.bnx_l13_phut(2, 30) == 1.0 and alg.bnx_l13_phut(10, 30) == 5.0",
               "100 // 10 == 40 // 4 == 10 and 400 // 4 == 100 and 300 / 400 == 0.75"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Dùng thẻ <code>latest</code>: hai lần kéo có thể ra hai ảnh khác nhau, không biết máy chủ đang chạy bản nào, quay lui về “latest” vô nghĩa.</div>""" + code(BAD_DF),
           """Lỗi của người mới là dùng nhãn mới nhất cho ảnh chạy thật. Hai lần kéo có thể ra hai ảnh khác nhau, nên hãy ghim phiên bản ảnh nền và gắn thẻ ảnh bằng mã chốt."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Mật khẩu trong <code>ENV</code> của Dockerfile hay trong tệp đường ống: ai kéo ảnh, ai đọc kho mã đều thấy. <span class="note">Kiểm tệp vừa xem: chỉ <code>ENV</code> bị báo, còn <code>FROM eclipse-temurin:latest</code> không bị báo. Secret của Kubernetes (đối tượng lưu mật khẩu, khoá cho Pod dùng) mặc định lưu <b>không mã hoá</b>: nhớ bật mã hoá khi lưu.</span></div>""" + out(BAD_DF_OUT, "Kết quả chạy thật (Docker 28): docker build --check, lệnh chỉ kiểm tệp dựng ảnh, không dựng"),
           """Lỗi của người đã đi làm là ghi mật khẩu vào tệp dựng ảnh hay tệp đường ống, vì ai kéo ảnh hay đọc kho mã đều thấy.
           Bí mật phải đưa vào lúc chạy, và kho bí mật của Kubernetes mặc định không mã hoá nên phải bật.""",
           clear=True, focus=[1, [2, 3], 1], introduces=["bnx_secret_k8s"]),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Triển khai xong chưa phải phát hành an toàn. Không có <code>readinessProbe</code> thì Pod nhận yêu cầu khi Java chưa khởi động xong; không chuẩn bị quay lui thì lỗi kéo dài.
<br><span class="note">Cách chữa: khai báo phép kiểm sẵn sàng; quay lui bằng <code>kubectl rollout undo deployment/chuyen-tien</code> về bản trước.</span></div>""",
           """Lỗi thứ ba là coi triển khai xong là phát hành an toàn. Không có phép kiểm sẵn sàng thì bản chạy nhận yêu cầu khi Java chưa khởi động xong. Nên hãy khai báo phép kiểm và chuẩn bị lệnh quay lui, cũng là một lần cập nhật cuốn chiếu.""",
           clear=True),
    ], checks=["alg.bnx_rolling_bounds(4, 1, 1)[0] == 3"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Deployment 6 bản, <code>maxUnavailable: 2</code>, <code>maxSurge: 1</code>. Sẵn sàng tối thiểu bao nhiêu? Tối đa bao nhiêu Pod?"],
                  ["2", "Đường ống: build và test thành công, package hỏng. Job deploy có chạy không? Máy chủ chạy ảnh thẻ nào?"],
                  ["3", "Quyết định: 4 bản, mỗi Pod chịu 250 giao dịch/giây, tải 900 (số minh hoạ). Chọn (maxUnavailable 1, maxSurge 1) hay (0, 1)?"]]),
           """Bây giờ tới phần bạn tự làm bài. Câu một: sáu bản, được thiếu tối đa hai, được thừa tối đa một, thì sẵn sàng tối thiểu và chạy tối đa bao nhiêu bản? Câu hai hỏi về đóng gói hỏng, câu ba về sức chứa. Hãy dừng video và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1:</p>
$$6 - 2 = \\hlg{4} \\text{ sẵn sàng tối thiểu} \\qquad 6 + 1 = \\hl{7} \\text{ Pod tối đa}$$""",
           """Đáp án câu một: được thiếu tối đa hai nên sẵn sàng tối thiểu là sáu trừ hai bằng bốn, và được thừa tối đa một nên tối đa là sáu cộng một bằng bảy bản chạy."""),
        st("""<p>Câu 2: package hỏng → giai đoạn deploy <b>không chạy</b>; không có ảnh mới được đẩy, máy chủ vẫn chạy <code>:0eac7e6a</code>.</p>""",
           """Đáp án câu hai: đóng gói hỏng nên giai đoạn triển khai không chạy, vì giai đoạn sau chỉ chạy khi giai đoạn trước thành công, và máy chủ vẫn chạy ảnh thẻ cũ."""),
        st(table(["lựa chọn", "sức chứa lúc cập nhật", "được", "mất"],
                 [["(1, 1)", "$3 \\cdot 250 = 750$, thiếu so với 900", "nhanh: 2 đợt chờ; chỉ cần chỗ cho 1 Pod thêm", "<b class='red'>quá tải</b> suốt lúc cập nhật"],
                  ["(0, 1)", "$4 \\cdot 250 = 1000$, đủ cho 900", "luôn đủ 4 bản phục vụ", "cần chỗ cho Pod thứ 5; chậm hơn: 4 đợt chờ thay vì 2"]]),
           """Đáp án câu ba: được thiếu một thì chỉ còn bảy trăm năm mươi, nhỏ hơn chín trăm, nên quá tải. Không được thiếu thì luôn còn một nghìn, đủ tải, đổi lại cần chỗ cho bản thứ năm và bốn đợt thay vì hai.""",
           focus=["1.2", "1.3", "1.3"]),
    ], checks=["alg.bnx_rolling_bounds(6, 2, 1) == (4, 7)",
               "alg.bnx_pipeline(['build', 'test', 'package', 'deploy'], {'build': 'build', 'test': 'test', 'package': 'package', 'deploy': 'deploy'}, {'package'})['deploy'] == 'skipped'",
               "3 * 250 == 750 < 900 and 4 * 250 == 1000 >= 900",
               "alg.bnx_rolling_summary(4, 0, 1) == (4, 4, 5) and alg.bnx_rolling_summary(4, 1, 1)[0] == 2"])
    lab_pr = practice_scene(sc, "Tự làm: lớp phải dựng lại và số đợt cập nhật", [st(
        code(LAB_PY, lines=(1, 8), title="Dữ liệu cho sẵn: chép vào đầu mau.py (số minh hoạ)"),
        """Đây là hai danh sách lớp cho sẵn: mỗi lớp là một bộ gồm tên, danh sách tệp đầu vào và số giây dựng.""")] + practice_steps(
        st, "BNX", "L13",
        """<p><b>Đề</b>: viết <code>mau.py</code> (mô phỏng, không cần Docker) với hai danh sách lớp trong <code>de.md</code>:</p>
<ol><li>hàm <code>dung_lai(lop, sua)</code>: lớp đầu có tệp vừa sửa và mọi lớp sau phải dựng lại; in lớp và số giây cho <code>src/Dao.java</code>, <code>pom.xml</code>, và cho Dockerfile sai thứ tự</li>
<li>cập nhật cuốn chiếu: <code>D=12</code> (thiếu 1, thừa 2) và <code>D=10</code> (25%, <b>xuống</b> / <b>lên</b>): in số đợt, tối thiểu, tối đa</li></ol>
<p class="note">Số liệu khác ví dụ trong bài; đầu ra viết không dấu.</p>""",
        """Bây giờ tới phần bạn tự làm bằng mô phỏng, không cần cài Docker hay Kubernetes. Viết hàm tìm các lớp phải dựng lại khi sửa một tệp, rồi tính số đợt cho hai cấu hình cập nhật. Hãy dừng video và tự viết.""",
        EXPECT_LAB, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> duyệt lớp theo thứ tự, gặp lớp đầu tiên có <code>sua in dau_vao</code> thì cộng giây từ lớp đó tới hết. Số đợt: lặp, mỗi lần cộng <code>min(mu + ms, D − san)</code> bản sẵn sàng. Phần trăm: <code>mu = D // 4</code> (chia lấy phần nguyên, làm tròn xuống), <code>ms = −(−D // 4)</code> (làm tròn lên: D = 10 ra 3).
Lời giải ở <code>labs/BNX/L13/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, hãy duyệt lớp theo thứ tự, dừng ở lớp đầu tiên có tệp vừa sửa rồi cộng giây từ đó tới hết. Lời giải chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L13")
    lab_pr["steps"][1]["clear"] = True
    lab_pr["checks"] = ["alg.bnx_l13_lab() == (([5, 6], 27), ([3, 4, 5, 6], 108), ([2, 3], 108), (4, 11, 14), (2, 8, 13))",
                        "5 + 1 + 1 + 80 + 2 + 25 == 114 and 2 + 25 == 27 and 1 + 80 + 2 + 25 == 108 and 3 + 105 == 108"]
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("commit", "đường ống 4 giai đoạn: hỏng thì dừng", "ảnh gắn mã commit", "cuốn chiếu: ≥ 3 sẵn sàng, ≤ 5 Pod", "quy mô: số đợt = D chia (thiếu + thừa)"),
           """Tổng kết: mỗi lần chốt đi qua đường ống bốn giai đoạn, hỏng ở đâu thì dừng ở đó, và ảnh gắn thẻ là mã chốt. Số đợt cập nhật bằng số bản chia cho thiếu cộng thừa, nên cấu hình phải chọn theo quy mô.""",
           focus=[["1.1", "1.3", "1.5"], ["1.7", "1.9"]]),
        st("""<div class='box key'><b>Tư duy:</b> mỗi thứ chạy trên máy chủ phải trả lời được “từ commit nào?”. Bí mật không nằm trong ảnh, trong tệp đường ống hay trong lịch sử Git; và cấu hình cập nhật tốt ở 4 bản chưa chắc còn tốt ở 400 bản.</div>""",
           """Điều cần mang theo: mọi thứ chạy trên máy chủ phải truy ngược được về một lần chốt, và cấu hình tốt ở bốn bản chưa chắc còn tốt ở bốn trăm bản."""),
        st("""<p class='note'>Bài 14: chia hệ thống ngân hàng thành những vùng có ranh giới rõ.</p>""",
           """Ở bài mười bốn, ta học cách chia hệ thống ngân hàng thành những vùng có ranh giới rõ.""",
           forward_ref=True),
    ])
    scenes = spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L13", "docker_gitlab_ci_kubernetes", "Bài 13 — Từ commit tới máy chủ: Dockerfile, GitLab CI và triển khai lên Kubernetes",
                  "curriculum/bnx.yaml L13; audit/bnx/verify_bnx.py L13; docs.gitlab.com CI/CD YAML syntax reference (stages), Predefined CI/CD variables, "
                  "Build and push container images (đọc 2026-11-11); kubernetes.io Deployments, Secrets (đọc 2026-11-11); mã nguồn Kubernetes "
                  "pkg/controller/deployment/rolling.go, util/deployment_util.go (đọc 2026-11-11); docs.docker.com Build cache, Building best practices "
                  "(đọc 2026-11-11); docker build --check, Docker 28 (OBSERVED 2026-11-11); quy mô: mô phỏng số đợt bằng Python chạy thật (prog Dot), "
                  "đối chiếu bộ điều khiển mô phỏng theo mã nguồn Kubernetes; KHÔNG chạy trên cụm Kubernetes thật",
                  ["Đọc Dockerfile của dịch vụ Java và sắp thứ tự lệnh để tận dụng bộ nhớ đệm", "Đọc tệp .gitlab-ci.yml và thứ tự các giai đoạn",
                   "Khai báo Deployment và tính số Pod khi cập nhật cuốn chiếu", "Nêu cách gắn thẻ ảnh bằng mã commit để truy ngược",
                   "Tính số đợt và thời gian cập nhật cuốn chiếu khi số bản tăng từ 4 lên 40 và 400, và so thiếu 1 thừa 1 với mặc định 25%",
                   "Viết chương trình Python tìm các lớp Dockerfile phải dựng lại và tính số đợt cập nhật cuốn chiếu"],
                  scenes,
                  covers=[(1, "formula"), (2, "formula"), (3, "example"), (4, "formula"), (5, "quymo"), (6, "practice")])


def alg_waves():
    """Bảng đợt của ví dụ lấy từ checklib (một nguồn số); checks của cảnh và ver/l13.py đối chiếu lại."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
    import checklib
    return checklib.bnx_rolling_waves(4, 1, 1)
