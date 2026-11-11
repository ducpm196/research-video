from lib import *

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


def code_(t, **kw):
    """Khối mã có dấu $: tách mỗi $ thành một nút chữ riêng để KaTeX không coi đoạn giữa hai dấu $ là công thức."""
    return code(t, **kw).replace("$", "<span>&#36;</span>")


def note(t):
    return f"<p class='note'>{t}</p>"


def build():
    rows, _trace = alg_waves()
    hook = sc("hook", "hook", "Bản mới lên lúc 17 giờ, khách báo lỗi lúc 17 giờ 10", [
        st("""<p>Chiều thứ Sáu, bản mới của dịch vụ chuyển tiền chạy trên <b>4</b> bản trong cụm Kubernetes. Mười phút sau, tổng đài báo khách chuyển tiền lỗi <span class='note'>(tình huống minh hoạ)</span>.</p>
<div class="box warn">Đang chạy bản nào? Bản đó làm từ dòng mã nào, đã qua kiểm thử chưa? Quay về bản cũ có làm khách gián đoạn không?</div>""",
           """Chào bạn, chiều thứ Sáu, bản mới của dịch vụ chuyển tiền vừa chạy trên bốn bản trong cụm Kubernetes, đây là tình huống minh hoạ.
           Mười phút sau, tổng đài báo khách chuyển tiền bị lỗi. Câu đầu tiên ai cũng hỏi là máy chủ đang chạy bản nào, làm từ dòng mã nào, đã qua kiểm thử chưa."""),
        st(table(["câu hỏi", "bài này trả lời bằng"],
                 [["đóng gói dịch vụ Java thế nào cho nhanh và chắc?", "Dockerfile: tệp phụ thuộc trước, mã sau; ghim phiên bản ảnh nền"],
                  ["ai chặn bản lỗi trước khi lên máy chủ?", "đường ống 4 giai đoạn: test hỏng thì package và deploy không chạy"],
                  ["thay bản mà khách không thấy gián đoạn?", "cập nhật cuốn chiếu: 4 bản, luôn ≥ 3 sẵn sàng, ≤ 5 Pod"],
                  ["truy ngược từ máy chủ về mã?", "thẻ ảnh = 8 ký tự đầu của mã commit"]]),
           """Bài này đi hết con đường từ một lần chốt mã tới máy chủ. Tệp dựng ảnh đóng gói dịch vụ Java.
           Đường ống bốn giai đoạn chặn bản lỗi trước khi lên máy chủ. Cập nhật cuốn chiếu thay bản mà khách không thấy gián đoạn.
           Và thẻ ảnh mang mã chốt, để truy ngược từ máy chủ về đúng dòng mã."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① container", "tiến trình chạy cô lập: hệ tệp, mạng, giới hạn bộ nhớ riêng, dùng chung nhân hệ điều hành", "dịch vụ chuyển tiền"],
                  ["② ảnh (image)", "gói chỉ đọc gồm hệ tệp và lệnh khởi động; chạy ảnh thì được container", "<code>chuyen-tien:0eac7e6a</code>"],
                  ["③ tệp jar", "Java gói mã đã biên dịch thành một tệp, chạy bằng <code>java -jar</code>", "<code>app.jar</code>"],
                  ["④ cụm, Kubernetes", "cụm: nhiều máy chủ gom lại chạy chung; Kubernetes: phần mềm đặt container lên các máy trong cụm và tự giữ đủ số bản", "cụm 3 máy, 4 bản"],
                  ["⑤ cập nhật cuốn chiếu", "thay dần bản cũ bằng bản mới, luôn còn bản phục vụ khách", "4 bản, thay dần"]]),
           """Trước hết ta cần hiểu năm điều sẽ dùng trong bài. Một tiến trình cô lập có hệ tệp, mạng và bộ nhớ riêng, nhưng dùng chung nhân hệ điều hành của máy.
           Ảnh là gói chỉ đọc gồm hệ tệp và lệnh khởi động, chạy ảnh thì được một tiến trình như vậy. Java gói mã đã biên dịch thành một tệp đóng gói duy nhất.
           Cụm là nhiều máy chủ gom lại, còn Kubernetes đặt các tiến trình lên máy trong cụm và tự giữ đủ số bản.
           Cập nhật cuốn chiếu thay dần bản cũ bằng bản mới, nên lúc nào cũng còn bản phục vụ khách."""),
        st("""$$4 - 1 = \\hl{3} \\text{ bản phục vụ khi đang thay 1 bản}, \\qquad \\frac{3}{4} = 75\\%$$""",
           """Ta xem ngay một ví dụ số nhỏ. Có bốn bản, đang thay một bản thì còn bốn trừ một bằng ba bản phục vụ, tức ba phần tư, bằng bảy mươi lăm phần trăm sức chứa.""",
           introduces=["frac"], clear=True),
    ], checks=["4 - 1 == 3 and Fraction(3, 4) == Fraction(75, 100)", "alg.bnx_rolling_bounds(4, 1, 1)[0] == 3"])
    sym = sc("sym", "symbol", "Giải mã các từ hay gặp", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["phụ thuộc", "thư viện người khác viết mà dự án dùng, ví dụ Spring"],
                  ["Maven, lệnh <code>mvn</code>", "công cụ dựng của Java: tải phụ thuộc, biên dịch, chạy kiểm thử, đóng gói thành jar"],
                  ["<code>pom.xml</code>", "tệp khai báo dự án và danh sách phụ thuộc cho Maven"],
                  ["<code>-DskipTests</code>", "bỏ chạy kiểm thử lúc đóng gói, vì đường ống đã có giai đoạn kiểm thử riêng"]]),
           """Bảng đầu giải mã bốn từ của Java. Phụ thuộc là thư viện người khác viết mà dự án dùng, ví dụ Spring.
           Công cụ dựng của Java tải phụ thuộc, biên dịch, kiểm thử và đóng gói, theo tệp khai báo dự án.
           Tuỳ chọn cuối bỏ kiểm thử lúc đóng gói, vì đường ống đã có giai đoạn kiểm thử riêng."""),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["<code>FROM ảnh AS build</code>", "chọn ảnh nền; <code>AS build</code> đặt tên giai đoạn dựng"],
                  ["<code>COPY</code> / <code>RUN</code>", "chép tệp vào ảnh / chạy một lệnh lúc dựng; mỗi lệnh tạo một <b>lớp</b>"],
                  ["<code>COPY --from=build</code>", "chỉ lấy tệp jar từ giai đoạn dựng; ảnh chạy không chứa mã nguồn và công cụ dựng"],
                  ["<code>USER</code> / <code>ENTRYPOINT</code>", "chạy bằng người dùng không phải quản trị / lệnh khởi động khi container chạy"],
                  ["thẻ ảnh <code>tên:thẻ</code>", "tên phiên bản của ảnh; <code>latest</code> chỉ là một thẻ bình thường, không tự là “bản mới nhất”"]]),
           """Bảng thứ hai giải mã tệp dựng ảnh. Lệnh đầu chọn ảnh nền và đặt tên cho giai đoạn dựng.
           Lệnh chép tệp và lệnh chạy, mỗi lệnh tạo ra một lớp trong ảnh. Lệnh chép từ giai đoạn dựng chỉ lấy tệp đóng gói, nên ảnh chạy gọn và sạch.
           Thẻ ảnh là tên phiên bản, còn nhãn mới nhất chỉ là một thẻ bình thường, không tự nghĩa là bản mới nhất.""", clear=True),
        st(table(["từ", "nghĩa"],
                 [["đường ống (GitLab CI)", "mỗi lần đẩy commit lên kho GitLab, máy chạy đường ống đọc tệp <code>.gitlab-ci.yml</code> và tự chạy các việc trong đó"],
                  ["stage / job", "giai đoạn / việc; job cùng giai đoạn chạy song song"],
                  ["kho ảnh (registry)", "nơi lưu ảnh; <code>docker push</code> đẩy ảnh lên, máy trong cụm kéo ảnh về để chạy"],
                  ["<code>CI_COMMIT_SHORT_SHA</code>", "biến có sẵn: 8 ký tự đầu của mã commit đang dựng"],
                  ["<code>CI_REGISTRY_USER</code>, <code>CI_REGISTRY_PASSWORD</code>", "tài khoản đường ống cấp sẵn để đẩy ảnh lên kho ảnh của dự án; mật khẩu chỉ dùng được khi job đang chạy"]]),
           """Bảng thứ ba giải mã đường ống. Mỗi lần ta đẩy một lần chốt lên kho mã, máy chạy đường ống đọc tệp đường ống và tự chạy các việc trong đó.
           Các việc chia theo giai đoạn, việc cùng giai đoạn chạy song song. Đường ống đẩy ảnh lên kho ảnh, còn máy trong cụm kéo ảnh về để chạy.
           Biến mã chốt ngắn là tám ký tự đầu của mã chốt, còn hai biến cuối là tài khoản đường ống cấp sẵn để đẩy ảnh.""", clear=True),
        st(table(["từ", "nghĩa"],
                 [["Pod", "bản chạy nhỏ nhất Kubernetes quản lý, ở đây gồm một container"],
                  ["Deployment, <code>replicas</code>", "đối tượng khai báo “muốn có 4 bản của ảnh này”"],
                  ["nhãn, bộ chọn", "nhãn là cặp tên = giá trị gắn lên Pod (<code>app: chuyen-tien</code>); bộ chọn tìm mọi Pod có nhãn đó"],
                  ["bộ điều khiển", "chương trình trong Kubernetes liên tục so số bản muốn với số bản thật rồi tạo, xoá Pod cho khớp"],
                  ["<code>maxUnavailable</code> / <code>maxSurge</code>", "lúc cập nhật: được thiếu tối đa / được thừa tối đa bao nhiêu bản so với <code>replicas</code>"],
                  ["<code>readinessProbe</code>, <code>kubectl</code>", "phép kiểm sẵn sàng: chỉ nhận yêu cầu khi trả lời được đường dẫn kiểm / lệnh gửi yêu cầu tới Kubernetes"]]),
           """Bảng cuối giải mã Kubernetes. Bản chạy là đơn vị nhỏ nhất, còn đối tượng triển khai khai báo muốn có bốn bản của một ảnh.
           Nhãn gắn lên bản chạy, bộ chọn tìm mọi bản chạy mang nhãn đó. Bộ điều khiển liên tục so số bản muốn với số bản thật, rồi tạo hay xoá cho khớp.
           Hai tham số cập nhật là số được thiếu và số được thừa. Hàng cuối là phép kiểm sẵn sàng và lệnh điều khiển cụm.""", clear=True),
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
           """Hình trên là con đường của một lần chốt. Đường ống chạy bốn giai đoạn theo thứ tự, dựng, kiểm thử, đóng gói, triển khai, rồi bốn bản chạy trong Kubernetes dùng ảnh mang thẻ là mã chốt.
           Hàng dưới là một lần chốt có lỗi trong mã. Giai đoạn kiểm thử hỏng, nên đóng gói và triển khai không chạy.
           Không có ảnh mới nào được tạo, máy chủ vẫn giữ bản cũ, và không ai phải quay lui."""),
        st(svg(1500, 470,
               txt(360, 40, "Thứ tự đúng: tệp phụ thuộc trước", 26, "middle", "#16a34a", True),
               box(60, 60, 600, 52, "1  FROM maven:3.9.9-…", C_GREEN, size=22), box(60, 118, 600, 52, "2  WORKDIR /src", C_GREEN, size=22),
               box(60, 176, 600, 52, "3  COPY pom.xml", C_GREEN, size=22), box(60, 234, 600, 52, "4  RUN tải phụ thuộc", C_GREEN, size=22),
               box(60, 292, 600, 52, "5  COPY src   (sửa một tệp ở đây)", C_AMBER, size=22), box(60, 350, 600, 52, "6  RUN biên dịch, đóng gói", C_AMBER, size=22),
               txt(1110, 40, "Thứ tự sai: chép tất cả trước", 26, "middle", "#dc2626", True),
               box(810, 60, 600, 52, "1  FROM maven:3.9.9-…", C_GREEN, size=22), box(810, 118, 600, 52, "2  WORKDIR /src", C_GREEN, size=22),
               box(810, 176, 600, 52, "3  COPY . .   (sửa một tệp ở đây)", C_AMBER, size=22), box(810, 234, 600, 52, "4  RUN tải phụ thuộc + biên dịch", C_AMBER, size=22),
               txt(750, 450, "xanh: dùng lại lớp đệm; cam: phải dựng lại (lớp đổi kéo theo mọi lớp sau)", 24, "middle", "#1f2937", True)),
           """Hình dưới là bộ nhớ đệm của các lớp. Mỗi lệnh trong tệp dựng ảnh tạo một lớp, và một lớp đổi thì mọi lớp sau nó phải dựng lại.
           Bên trái, tệp khai báo phụ thuộc được chép trước, nên sửa một tệp mã chỉ làm hai lớp cuối dựng lại, bước tải phụ thuộc được dùng lại.
           Bên phải, chép tất cả ngay từ đầu, nên sửa một tệp mã cũng kéo theo tải lại toàn bộ phụ thuộc."""),
    ], checks=["alg.bnx_pipeline(['build', 'test', 'package', 'deploy'], {'build': 'build', 'test': 'test', 'package': 'package', 'deploy': 'deploy'}, {'test'}) == {'build': 'success', 'test': 'failed', 'package': 'skipped', 'deploy': 'skipped'}",
               "alg.bnx_cache_rebuilt(alg.bnx_df_good, {'src/Main.java'}) == [5, 6] and alg.bnx_cache_rebuilt(alg.bnx_df_bad, {'src/Main.java'}) == [3, 4]",
               "alg.bnx_short_sha('0eac7e6a33ba9714db9a6ca6a6ca184cd627bbf5') == '0eac7e6a' and alg.bnx_git_demo()['merge'].startswith('0eac7e6a')"])
    form = sc("formula", "formula", "Suy ra từng bước: từ Dockerfile tới số Pod", [
        st(code_(DOCKERFILE),
           """Bước một là tệp dựng ảnh. Giai đoạn dựng chép tệp khai báo phụ thuộc và tải phụ thuộc trước, rồi mới chép mã nguồn và đóng gói.
           Vì tệp phụ thuộc ít khi đổi còn mã đổi hằng ngày, thứ tự này giữ được lớp tải phụ thuộc trong bộ nhớ đệm.
           Giai đoạn chạy dùng ảnh nền chỉ có môi trường chạy Java, ghim đúng phiên bản."""),
        st("""<p><b>Làm thử</b> (số minh hoạ: tải phụ thuộc 90 giây, biên dịch và đóng gói 30 giây). Sửa một tệp trong <code>src</code>:</p>
$$\\text{đúng thứ tự: } \\hlg{30} \\text{ giây} \\qquad \\text{sai thứ tự: } 90 + 30 = \\hl{120} \\text{ giây}$$
""" + note("30 giây chỉ đúng khi máy dựng còn giữ đệm của lần trước. Máy chạy đường ống dùng một lần thì đệm trống: phải chủ động giữ đệm mới được lợi.")
           + note("Thẻ ảnh nền có thể bị nhà phát hành trỏ sang ảnh khác. Muốn bất biến tuyệt đối thì ghim thêm mã băm của ảnh (digest), dạng <code>@sha256:…</code>."),
           """Làm thử với số minh hoạ, tải phụ thuộc mất chín mươi giây, biên dịch và đóng gói mất ba mươi giây. Giả sử ta sửa một tệp mã nguồn.
           Đúng thứ tự thì chỉ chạy lại ba mươi giây, vì lớp tải phụ thuộc được dùng lại. Sai thứ tự thì mất chín mươi cộng ba mươi, bằng một trăm hai mươi giây.
           Ba mươi giây chỉ đúng khi máy dựng còn giữ đệm, vì máy chạy đường ống dùng một lần thì đệm trống từ đầu.
           Thẻ ảnh nền có thể bị trỏ sang ảnh khác, nên muốn bất biến tuyệt đối thì ghim thêm mã băm của ảnh.""",
           clear=True, focus=[1, 1, 2, 2, 3, 4]),
        st(code_(CI_YML, lines=(1, 9)) + note("Rút gọn: mỗi job còn cần khai <code>image:</code> có công cụ của nó (ở đây là Maven)."),
           """Bước hai là tệp mô tả đường ống. Dòng đầu khai báo bốn giai đoạn theo đúng thứ tự chạy.
           Biến tên ảnh ghép địa chỉ kho ảnh của dự án với tám ký tự đầu của mã chốt.
           Tệp này đã rút gọn, vì mỗi việc thật còn cần khai một ảnh có sẵn công cụ của nó.""",
           clear=True, focus=[1, 1, 1, 2]),
        st(code_(CI_YML, lines=(10, 16)) + note("Rút gọn: job này còn cần dịch vụ Docker chạy kèm trong máy chạy đường ống."),
           """Việc đóng gói trước hết đăng nhập kho ảnh bằng tài khoản mà đường ống cấp sẵn, vì kho chỉ nhận ảnh từ người có quyền.
           Mật khẩu đưa qua đầu vào chứ không gõ thẳng trong lệnh, rồi việc này dựng ảnh và đẩy lên kho với thẻ là mã chốt ngắn. Việc này còn cần một dịch vụ Docker chạy kèm, ở đây đã lược đi.""",
           clear=True, focus=[1, 1, 2]),
        st(code_(CI_YML, lines=(17, 21)) + note("Rút gọn: job này còn cần ảnh có <code>kubectl</code> và quyền vào cụm."),
           """Việc triển khai dùng lệnh điều khiển cụm đổi ảnh của đối tượng triển khai, rồi chờ cập nhật cuốn chiếu xong.
           Việc ở giai đoạn sau chỉ bắt đầu khi mọi việc của giai đoạn trước thành công, nên kiểm thử hỏng thì không có ảnh nào được đẩy lên.
           Việc này còn cần quyền vào cụm, ở đây cũng đã lược đi.""",
           clear=True, focus=[1, 1, 2]),
        st(code_(DEPLOY_YML, lines=(1, 11)),
           """Bước ba là tệp khai báo đối tượng triển khai. Nó khai báo muốn có bốn bản, cập nhật theo kiểu cuốn chiếu,
           được thiếu tối đa một bản và được thừa tối đa một bản so với bốn.""",
           clear=True),
        st(code_(DEPLOY_YML, lines=(12, 23)),
           """Bộ chọn tìm các bản chạy mang nhãn tên dịch vụ, và phần mẫu gắn đúng nhãn đó lên mỗi bản chạy mới.
           Ảnh mang thẻ không e a c bảy e sáu a, là tám ký tự đầu của mã chốt gộp hai nhánh phí ở bài không.
           Mã đó chỉ được mượn làm ví dụ, vì kho ở bài không chỉ có tệp phí, không dựng ra được dịch vụ Java.
           Phép kiểm sẵn sàng gọi đường dẫn kiểm ở cổng tám nghìn không trăm tám mươi, vì chỉ khi trả lời được thì bản chạy mới được tính là sẵn sàng.""",
           clear=True),
        st("""$$\\text{sẵn sàng} \\geq 4 - 1 = \\hlg{3} \\qquad \\text{số Pod} \\leq 4 + 1 = \\hl{5}$$
<span class='note'>Làm thử: thiếu tối đa 1 nên luôn còn ít nhất 3 bản phục vụ; thừa tối đa 1 nên cụm phải có chỗ cho bản thứ 5.</span>""",
           """Từ hai tham số suy ra ngay hai giới hạn, theo đúng nghĩa của chúng. Vì được thiếu tối đa một, số bản sẵn sàng luôn ít nhất bốn trừ một bằng ba.
           Vì được thừa tối đa một, số bản chạy cùng lúc nhiều nhất bốn cộng một bằng năm, nên cụm phải có chỗ cho bản thứ năm.""",
           clear=True, introduces=["geq"]),
    ], checks=["alg.bnx_build_seconds(alg.bnx_df_good, {'src/Main.java'}, {'RUN dependency:go-offline': 90, 'RUN package': 30}) == 30",
               "alg.bnx_build_seconds(alg.bnx_df_bad, {'src/Main.java'}, {'RUN package (tải + dịch)': 90 + 30}) == 120",
               "alg.bnx_rolling_bounds(4, 1, 1) == (3, 5)", "alg.bnx_short_sha(alg.bnx_git_demo()['merge']) == '0eac7e6a'"])
    ex = sc("example", "example", "Ví dụ cập nhật 4 bản, từng phép tính", [
        st("""<p>Đối tượng triển khai: <code>replicas: 4</code>, <code>maxUnavailable: 1</code>, <code>maxSurge: 1</code>; ảnh đổi sang thẻ mới.</p>
$$① \\; 4 - 1 = \\hlg{3} \\text{ bản sẵn sàng tối thiểu}$$""",
           """Ta mô phỏng từng bước khi đổi bốn bản sang ảnh mới. Phép tính thứ nhất, số bản sẵn sàng tối thiểu là bốn trừ một, bằng ba."""),
        st("""$$② \\; 4 + 1 = \\hl{5} \\text{ Pod tối đa cùng lúc}$$""",
           """Phép tính thứ hai, số bản chạy tối đa cùng lúc là bốn cộng một, bằng năm."""),
        st("""<p>③ Đợt 1, theo quy tắc của bộ điều khiển: tạo 1 Pod mới (tổng 4 + 1 = 5) → xoá 1 Pod cũ (còn 4 − 1 = 3 sẵn sàng, đúng mức tối thiểu) → tạo thêm 1 Pod mới (tổng lại 3 + 2 = 5).</p>
<span class='note'>2 Pod mới khởi động cùng lúc, chưa qua phép kiểm sẵn sàng nên chưa được tính; bộ điều khiển chờ chúng.</span>""",
           """Phép tính thứ ba là đợt đầu, theo đúng quy tắc của bộ điều khiển. Nó tạo một bản mới cho tổng lên năm, rồi xoá một bản cũ vì còn ba bản sẵn sàng, đúng mức tối thiểu.
           Tổng tụt về bốn nên nó tạo thêm một bản mới nữa, tổng lại là năm. Hai bản mới khởi động cùng lúc, chưa được tính là sẵn sàng, nên bộ điều khiển chờ.""",
           clear=True),
        st(table(["đợt chờ", "cũ", "mới đang khởi động", "mới sẵn sàng", "Pod", "sẵn sàng"],
                 [[str(c) for c in r] for r in rows] + [["xong", "0", "0", "4", "4", "4"]]) +
           """$$④ \\; \\text{2 đợt; mọi lúc: sẵn sàng} \\geq \\hlg{3},\\ \\text{Pod} \\leq \\hl{5}$$""",
           """Phép tính thứ tư, lặp lại cho đến hết. Khi hai bản mới sẵn sàng, bộ điều khiển xoá hai bản cũ và tạo hai bản mới cuối cùng, rồi chờ đợt thứ hai.
           Vậy bốn bản được thay trong hai đợt chờ, giả định các bản khởi động lâu như nhau, và lúc nào cũng có ít nhất ba bản sẵn sàng, nhiều nhất năm bản chạy.""",
           clear=True, focus=[1, 1, 2]),
        st("""<p>Mỗi Pod chịu 250 giao dịch/giây, tải lúc cập nhật 600 giao dịch/giây <span class='note'>(số minh hoạ)</span>. Dùng lại 3 ở ①:</p>
$$⑤ \\; 3 \\cdot 250 = \\hlg{750} \\geq 600 \\;\\Rightarrow\\; \\text{đủ sức chứa suốt lúc cập nhật}$$""",
           """Phép tính thứ năm nối với sức chứa. Giả sử mỗi bản chịu hai trăm năm mươi giao dịch mỗi giây và tải lúc đó là sáu trăm, đều là số minh hoạ.
           Dùng lại ba bản ở phép tính thứ nhất, ba nhân hai trăm năm mươi bằng bảy trăm năm mươi, lớn hơn sáu trăm, nên suốt lúc cập nhật vẫn đủ sức chứa.""",
           clear=True),
    ], checks=["alg.bnx_rolling_bounds(4, 1, 1) == (4 - 1, 4 + 1)",
               "alg.bnx_rolling_waves(4, 1, 1)[1][:4] == [(4, 0, 0), (4, 0, 1), (3, 0, 1), (3, 0, 2)]",
               "alg.bnx_rolling_waves(4, 1, 1)[0] == [(1, 3, 2, 0, 5, 3), (2, 1, 2, 2, 5, 3)] and alg.bnx_rolling_waves(4, 1, 1)[1][-1] == (0, 4, 0)",
               "alg.bnx_rolling_summary(4, 1, 1) == (2, 3, 5)",
               "3 * 250 == 750 and 750 >= 600"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: liệt kê mọi trạng thái", [
        st(code(PY_ROLL) + out(PY_ROLL_OUT),
           """Bây giờ ta kiểm lại bằng một đường khác. Ta liệt kê mọi trạng thái được phép đi qua, theo mọi thứ tự tạo, xoá và khởi động xong.
           Mỗi trạng thái ghi ba số, bản cũ, bản mới sẵn sàng, bản mới đang khởi động.
           Kết quả có hai mươi bốn trạng thái, sẵn sàng thấp nhất là ba, nhiều nhất năm bản chạy, và trạng thái thay xong hết là tới được.""",
           focus=[0, 1, 1, 3]),
        st(table(["cách đổi ra số", "maxUnavailable", "maxSurge", "sẵn sàng tối thiểu", "Pod tối đa"],
                 [["số tuyệt đối 1", "1", "1", "3", "5"],
                  ["mặc định 25% của 4 = 1", "làm tròn xuống: 1", "làm tròn lên: 1", "3", "5"]]),
           """Đường kiểm thứ hai dùng giá trị mặc định là hai mươi lăm phần trăm. Hai mươi lăm phần trăm của bốn là một, làm tròn xuống hay lên đều được một.
           Vì vậy cấu hình mặc định cũng cho ba bản sẵn sàng tối thiểu và năm bản tối đa, khớp với cách tính bằng số tuyệt đối.""",
           clear=True),
    ], checks=["alg.bnx_rolling_bounds(4, '25%', '25%') == (3, 5) == alg.bnx_rolling_bounds(4, 1, 1)",
               "alg.bnx_k8s_abs('25%', 4, False) == 1 == alg.bnx_k8s_abs('25%', 4, True)",
               "alg.bnx_rolling_summary(4, 1, 1)[1:] == (3, 5)"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Dùng thẻ <code>latest</code>: hai lần kéo có thể ra hai ảnh khác nhau, không biết máy chủ đang chạy bản nào, quay lui về “latest” vô nghĩa.</div>""" + code(BAD_DF),
           """Lỗi thứ nhất, của người mới, là dùng nhãn mới nhất cho ảnh chạy thật. Hai lần kéo có thể ra hai ảnh khác nhau, nên không biết máy chủ đang chạy bản nào.
           Quay lui về nhãn đó cũng vô nghĩa. Hãy ghim phiên bản ảnh nền và gắn thẻ ảnh bằng mã chốt."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Mật khẩu trong <code>ENV</code> của Dockerfile hay trong tệp đường ống: ai kéo ảnh, ai đọc kho mã đều thấy. <span class="note">Kiểm tệp vừa xem: chỉ <code>ENV</code> bị báo, còn <code>FROM eclipse-temurin:latest</code> không bị báo. Secret của Kubernetes mặc định lưu <b>không mã hoá</b>: nhớ bật mã hoá khi lưu.</span></div>""" + out(BAD_DF_OUT, "Kết quả chạy thật: docker build --check"),
           """Lỗi thứ hai, của người đã đi làm, là ghi mật khẩu vào tệp dựng ảnh hay tệp đường ống. Ai kéo ảnh về, hay ai đọc lịch sử kho mã, đều thấy.
           Công cụ kiểm của Docker bắt được mật khẩu, nhưng không hề cảnh báo nhãn mới nhất ở dòng đầu của tệp. Bí mật phải đưa vào lúc chạy, bằng biến được che của đường ống hoặc kho bí mật của Kubernetes.
           Kho bí mật đó mặc định lưu không mã hoá, nên người vận hành cụm phải bật mã hoá khi lưu.""",
           clear=True, focus=[1, 1, 3, 0, 1]),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Triển khai xong chưa phải phát hành an toàn. Không có <code>readinessProbe</code> thì Pod nhận yêu cầu khi Java chưa khởi động xong; không chuẩn bị quay lui thì lỗi kéo dài.
<br><span class="note">Cách chữa: khai báo phép kiểm sẵn sàng; quay lui bằng <code>kubectl rollout undo deployment/chuyen-tien</code> về bản trước.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là coi triển khai xong là phát hành an toàn. Không có phép kiểm sẵn sàng thì bản chạy nhận yêu cầu khi Java chưa khởi động xong.
           Cách chữa là khai báo phép kiểm sẵn sàng, và chuẩn bị sẵn lệnh quay lui đối tượng triển khai về bản trước.""",
           clear=True),
    ], checks=["alg.bnx_rolling_bounds(4, 1, 1)[0] == 3"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Deployment 6 bản, <code>maxUnavailable: 2</code>, <code>maxSurge: 1</code>. Sẵn sàng tối thiểu bao nhiêu? Tối đa bao nhiêu Pod?"],
                  ["2", "Đường ống: build và test thành công, package hỏng. Job deploy có chạy không? Máy chủ chạy ảnh thẻ nào?"],
                  ["3", "Quyết định: 4 bản, mỗi Pod chịu 250 giao dịch/giây, tải 900 (số minh hoạ). Chọn (maxUnavailable 1, maxSurge 1) hay (0, 1)?"]]),
           """Bây giờ tới phần bạn tự làm bài. Câu một, sáu bản, được thiếu tối đa hai, được thừa tối đa một, thì sẵn sàng tối thiểu và số bản chạy tối đa là bao nhiêu?
           Câu hai, đóng gói hỏng thì việc triển khai có chạy không, và máy chủ chạy ảnh thẻ nào?
           Câu ba là một quyết định có đánh đổi về sức chứa lúc cập nhật, số liệu trên màn hình đều là số minh hoạ.
           Hãy dừng video lại và làm ra giấy trước.""",
           pause=25),
        st("""<p>Câu 1:</p>
$$6 - 2 = \\hlg{4} \\text{ sẵn sàng tối thiểu} \\qquad 6 + 1 = \\hl{7} \\text{ Pod tối đa}$$""",
           """Bây giờ ta xem đáp án câu một. Được thiếu tối đa hai nên sẵn sàng tối thiểu là sáu trừ hai bằng bốn. Được thừa tối đa một nên tối đa là sáu cộng một bằng bảy bản chạy."""),
        st("""<p>Câu 2: package hỏng → giai đoạn deploy <b>không chạy</b>; không có ảnh mới được đẩy, máy chủ vẫn chạy <code>:0eac7e6a</code>.</p>""",
           """Tiếp theo là đáp án của câu hai. Đóng gói hỏng nên giai đoạn triển khai không chạy, vì giai đoạn sau chỉ chạy khi giai đoạn trước thành công.
           Không có ảnh mới nào được đẩy lên, nên máy chủ vẫn chạy ảnh thẻ cũ không e a c bảy e sáu a."""),
        st(table(["lựa chọn", "sức chứa lúc cập nhật", "được", "mất"],
                 [["(1, 1)", "$3 \\cdot 250 = 750$, thiếu so với 900", "nhanh: 2 đợt chờ; chỉ cần chỗ cho 1 Pod thêm", "<b class='red'>quá tải</b> suốt lúc cập nhật"],
                  ["(0, 1)", "$4 \\cdot 250 = 1000$, đủ cho 900", "luôn đủ 4 bản phục vụ", "cần chỗ cho Pod thứ 5; chậm hơn: 4 đợt chờ thay vì 2"]]),
           """Cuối cùng là đáp án của câu ba. Được thiếu một thì lúc cập nhật chỉ còn ba nhân hai trăm năm mươi bằng bảy trăm năm mươi, nhỏ hơn chín trăm, nên quá tải.
           Không được thiếu thì luôn còn bốn nhân hai trăm năm mươi bằng một nghìn, đủ chịu tải. Đổi lại cụm phải có chỗ cho bản thứ năm, và mỗi đợt chỉ thay một bản, nên cần bốn đợt chờ thay vì hai.
           Vậy giờ cao điểm nên chọn không được thiếu, hoặc dời việc cập nhật sang giờ thấp điểm."""),
    ], checks=["alg.bnx_rolling_bounds(6, 2, 1) == (4, 7)",
               "alg.bnx_pipeline(['build', 'test', 'package', 'deploy'], {'build': 'build', 'test': 'test', 'package': 'package', 'deploy': 'deploy'}, {'package'})['deploy'] == 'skipped'",
               "3 * 250 == 750 < 900 and 4 * 250 == 1000 >= 900",
               "alg.bnx_rolling_summary(4, 0, 1) == (4, 4, 5) and alg.bnx_rolling_summary(4, 1, 1)[0] == 2"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("commit", "đường ống 4 giai đoạn: hỏng thì dừng", "ảnh gắn mã commit", "cuốn chiếu: ≥ 3 sẵn sàng, ≤ 5 Pod", "kiểm sẵn sàng + quay lui"),
           """Bây giờ ta tổng kết lại chuỗi logic. Mỗi lần chốt đi qua đường ống bốn giai đoạn, hỏng ở đâu thì dừng ở đó.
           Ảnh tạo ra được gắn thẻ là mã chốt. Kubernetes thay bản theo kiểu cuốn chiếu, luôn ít nhất ba bản sẵn sàng và nhiều nhất năm bản chạy. Cuối cùng là kiểm sẵn sàng và đường quay lui."""),
        st("""<div class='box key'><b>Tư duy:</b> mỗi thứ chạy trên máy chủ phải trả lời được “từ commit nào?”. Bí mật không nằm trong ảnh, trong tệp đường ống hay trong lịch sử Git.</div>""",
           """Và đây là điều cần mang theo sau bài. Mọi thứ chạy trên máy chủ phải trả lời được câu hỏi từ lần chốt nào, và bí mật không bao giờ nằm trong ảnh, trong tệp đường ống hay trong lịch sử kho mã."""),
        st("""<p class='note'>Bài 14: chia hệ thống ngân hàng thành những vùng có ranh giới rõ, và đặt một cổng vào chung trước các dịch vụ.</p>""",
           """Ở bài mười bốn, ta học cách chia hệ thống ngân hàng thành những vùng có ranh giới rõ, và đặt một cổng vào chung đứng trước các dịch vụ.""",
           forward_ref=True),
    ])
    return lesson("L13", "docker_gitlab_ci_kubernetes", "Bài 13 — Từ commit tới máy chủ: Dockerfile, GitLab CI và triển khai lên Kubernetes",
                  "curriculum/bnx.yaml L13; audit/bnx/verify_bnx.py L13; docs.gitlab.com CI/CD YAML syntax reference (stages), Predefined CI/CD variables, "
                  "Build and push container images (đọc 2026-11-11); kubernetes.io Deployments, Secrets (đọc 2026-11-11); mã nguồn Kubernetes "
                  "pkg/controller/deployment/rolling.go, util/deployment_util.go (đọc 2026-11-11); docs.docker.com Build cache, Building best practices "
                  "(đọc 2026-11-11); docker build --check, Docker 28 (OBSERVED 2026-11-11)",
                  ["Viết Dockerfile cho dịch vụ Java theo thứ tự tận dụng bộ nhớ đệm", "Đọc tệp .gitlab-ci.yml và thứ tự các giai đoạn",
                   "Khai báo Deployment và tính số Pod khi cập nhật cuốn chiếu", "Gắn ảnh với mã commit để truy ngược"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])


def alg_waves():
    """Bảng đợt của ví dụ lấy từ checklib (một nguồn số); checks của cảnh và ver/l13.py đối chiếu lại."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
    import checklib
    return checklib.bnx_rolling_waves(4, 1, 1)
