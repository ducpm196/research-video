import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from libj import jstep, nowrap
from labkit import write_lab, practice_steps, practice_scene

lib2.begin("L26")

# ── Mã chạy THẬT: Apache Maven 3.9.11 (audit/bnx/deps/_tools; cần mạng lần đầu để tải plugin và phụ thuộc vào ~/.m2) ──
# Groovy 4.0.27 (audit/bnx/deps/l26) chỉ để kiểm CÚ PHÁP Jenkinsfile và build.gradle; Gradle và Jenkins KHÔNG chạy trên máy này
# (mô phỏng nhỏ bằng Python, ghi rõ trên màn hình). Đầu ra tất định (đệm ở audit/bnx/progcache/L26.json).
X_POM = prog("Pom", r'''
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>bnx</groupId>
  <artifactId>l26</artifactId>
  <version>1</version>
  <properties>
    <maven.compiler.release>21</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-text</artifactId>
      <version>1.10.0</version>
    </dependency>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
      <version>3.9</version>
    </dependency>
  </dependencies>
</project>
''', lang="xml", kind="other", reason="pom.xml của dự án thử: hai phụ thuộc trực tiếp; ghi nguyên văn vào thư mục chạy của Maven thật.",
    read_check="Phân tích được bằng trình đọc XML (ElementTree) và chạy nguyên văn bởi Maven 3.9.11 trong nguồn L26_ChayCay (đầu ra thật khớp từng dòng).")

X_POM_TT = prog("PomTT", r'''
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>bnx</groupId>
  <artifactId>l26</artifactId>
  <version>1</version>
  <properties>
    <maven.compiler.release>21</maven.compiler.release>
    <project.build.outputTimestamp>2026-01-01T00:00:00Z</project.build.outputTimestamp>
  </properties>
</project>
''', lang="xml", kind="other", reason="pom.xml thứ hai: chỉ thêm project.build.outputTimestamp (theo hướng dẫn dựng tái lập của Maven).",
    read_check="Phân tích được bằng XML và chạy nguyên văn bởi Maven 3.9.11 trong nguồn L26_ChayTaiLap (so sha256 hai lần dựng).")

J_CHAO = prog("Chao", r'''
public class Chao {
  public static void main(String[] a) {
    System.out.println("xin chao");
  }
}
''', lang="java", kind="other", reason="Chao.java: mã nguồn để Maven biên dịch.", read_check="Biên dịch bởi Maven (maven-compiler-plugin) trong nguồn L26_ChayVongDoi.")

_MVN = "M=/d/research-video/audit/bnx/deps/_tools/apache-maven-3.9.11/bin/mvn"
_CHK = 'test -x $M || { echo "NOT_VERIFIED: thiếu Maven" >&2; exit 97; }'

SH_CAY = prog("ChayCay", f'''
{_MVN}
{_CHK}
mkdir -p src/main/java && cp Chao.java src/main/java/
$M -B -q dependency:tree -DoutputFile=cay.txt && cat cay.txt
echo "-- che do chi tiet (-Dverbose):"
$M -B -q dependency:tree -Dverbose -DoutputFile=cay2.txt && cat cay2.txt
''', lang="bash", files={"pom.xml": "Pom", "Chao.java": "Chao"}, timeout=300,
    claims=["cây phụ thuộc: commons-lang3 3.9 (trực tiếp) thắng 3.12.0 (bắc cầu qua commons-text)", "Maven báo: omitted for conflict with 3.9"])

SH_VONGDOI = prog("ChayVongDoi", f'''
{_MVN}
{_CHK}
mkdir -p src/main/java && cp Chao.java src/main/java/
$M -B package | grep -- '--- ' | cut -c8-
''', lang="bash", files={"pom.xml": "Pom", "Chao.java": "Chao"}, timeout=300,
    claims=["các pha dựng theo thứ tự: resources, compile, testResources, testCompile, test, jar"])

X_POM_GOC = prog("PomGoc", r'''
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>bnx</groupId>
  <artifactId>l26</artifactId>
  <version>1</version>
  <properties>
    <maven.compiler.release>21</maven.compiler.release>
  </properties>
</project>
''', lang="xml", kind="other", reason="pom.xml gốc không đặt outputTimestamp.", read_check="Phân tích được bằng XML và chạy nguyên văn bởi Maven trong nguồn L26_ChayTaiLap.")

SH_TAILAP = prog("ChayTaiLap", f'''
{_MVN}
{_CHK}
mkdir -p src/main/java && cp Chao.java src/main/java/
dung() {{
  $M -B -q -f $1 clean package > /dev/null 2>&1
  sha256sum target/l26-1.jar | cut -d' ' -f1
}}
so() {{
  a=$(dung $1); sleep 2; b=$(dung $1)
  [ "$a" = "$b" ] && echo "$2: GIONG" || echo "$2: KHAC"
}}
so pom.xml "khong dat outputTimestamp"
so pom-tt.xml "co outputTimestamp"
''', lang="bash", files={"pom.xml": "PomGoc", "pom-tt.xml": "PomTT", "Chao.java": "Chao"}, timeout=400,
    claims=["không đặt outputTimestamp: hai lần dựng ra jar khác nhau", "đặt outputTimestamp: hai lần dựng ra jar giống nhau từng bit"])

X_POM_A = prog("PomA", r'''
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>bnx</groupId><artifactId>a</artifactId><version>1</version>
  <dependencies>
    <dependency><groupId>org.apache.commons</groupId><artifactId>commons-lang3</artifactId><version>3.9</version></dependency>
  </dependencies>
</project>
''', lang="xml", kind="other", reason="pom: 1 phụ thuộc trực tiếp (commons-lang3).", read_check="XML; chạy nguyên văn bởi Maven trong nguồn L26_ChayQuyMo.")
X_POM_B = prog("PomB", r'''
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>bnx</groupId><artifactId>b</artifactId><version>1</version>
  <dependencies>
    <dependency><groupId>org.springframework</groupId><artifactId>spring-context</artifactId><version>7.0.10</version></dependency>
  </dependencies>
</project>
''', lang="xml", kind="other", reason="pom: 1 phụ thuộc trực tiếp (spring-context).", read_check="XML; chạy nguyên văn bởi Maven trong nguồn L26_ChayQuyMo.")
X_POM_C = prog("PomC", r'''
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>bnx</groupId><artifactId>c</artifactId><version>1</version>
  <dependencies>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId><version>3.5.7</version></dependency>
  </dependencies>
</project>
''', lang="xml", kind="other", reason="pom: 1 phụ thuộc trực tiếp (spring-boot-starter-web).", read_check="XML; chạy nguyên văn bởi Maven trong nguồn L26_ChayQuyMo.")

SH_QUYMO = prog("ChayQuyMo", f'''
{_MVN}
{_CHK}
for d in a b c; do
  mkdir -p $d && cp pom-$d.xml $d/pom.xml
  (cd $d && $M -B -q dependency:list -DoutputFile=ds.txt)
  echo "$d: 1 phu thuoc truc tiep -> $(grep -c ':jar:' $d/ds.txt) jar"
done
''', lang="bash", files={"pom-a.xml": "PomA", "pom-b.xml": "PomB", "pom-c.xml": "PomC"}, timeout=600,
    claims=["đồ thị phụ thuộc: 1 phụ thuộc trực tiếp kéo theo nhiều jar bắc cầu"])

JENKINSFILE = prog("Jenkinsfile", r'''
pipeline {
  agent any
  stages {
    stage('Build') {
      steps { sh 'mvn -B package' }
    }
    stage('Test') {
      steps { sh 'mvn -B verify' }
    }
    stage('Deploy') {
      steps { sh './trien-khai.sh' }
    }
  }
  post {
    failure { echo 'dung that bai' }
  }
}
''', lang="groovy", kind="other", reason="Jenkinsfile khai báo (Declarative Pipeline) theo mẫu của tài liệu Jenkins; KHÔNG chạy trên máy này (cần máy chủ Jenkins).",
    read_check="Kiểm CÚ PHÁP Groovy bằng GroovyShell.parse thật (Groovy 4.0.27) trong nguồn L26_KiemGroovy; cấu trúc pipeline/agent/stages/stage/steps/post theo tài liệu Jenkins đã đọc (audit/bnx/sources_l26.md, [JKSYN]); không kiểm ngữ nghĩa Declarative vì cần Jenkins.")

BUILD_GRADLE = prog("BuildGradle", r'''
plugins {
    id 'java'
}
repositories {
    mavenCentral()
}
dependencies {
    implementation 'org.apache.commons:commons-text:1.10.0'
    implementation 'org.apache.commons:commons-lang3:3.9'
}
''', lang="groovy", kind="other", reason="build.gradle (Groovy DSL) tương đương pom.xml của bài; KHÔNG chạy Gradle trên máy này.",
    read_check="Kiểm CÚ PHÁP Groovy bằng GroovyShell.parse thật trong nguồn L26_KiemGroovy; tên khối plugins/repositories/dependencies và `implementation`/`mavenCentral()` theo tài liệu Gradle đã đọc ([GRDL]); không chạy Gradle nên không kiểm kết quả phân giải.")

J_KIEM = prog("KiemGroovy", r'''
import groovy.lang.GroovyShell;
import java.nio.file.*;
public class KiemGroovy {
  static String thu(String ten) throws Exception {
    String ma = Files.readString(Path.of(ten));
    try {
      new GroovyShell().parse(ma);
      return "cu phap hop le";
    } catch (Exception e) {
      return "loi cu phap";
    }
  }
  public static void main(String[] a) throws Exception {
    for (String t : a)
      System.out.println(t + ": " + thu(t));
  }
}
''', lang="java", kind="other", reason="Chương trình kiểm cú pháp Groovy (chỉ biên dịch, không chạy tệp).", read_check="Biên dịch cùng Groovy 4.0.27 và chạy trong nguồn L26_KiemGroovy.")

JENK_HONG = prog("JenkinsfileHong", r'''
pipeline {
  agent any
  stages {
    stage('Build') {
      steps { sh 'mvn -B package'
    }
  }
}
''', lang="groovy", kind="other", reason="Jenkinsfile cố ý thiếu hai dấu đóng ngoặc, để thấy trình kiểm bắt lỗi.", read_check="Phải bị GroovyShell.parse từ chối: nguồn L26_KiemGroovy in 'loi cu phap'.")

SH_KIEM = prog("ChayKiem", r'''
D=/d/research-video/audit/bnx/deps/l26
ls $D/groovy-4.0.27.jar >/dev/null 2>&1 || { echo "NOT_VERIFIED: thiếu jar" >&2; exit 97; }
mkdir -p lib out && cp $D/*.jar lib/
javac -encoding UTF-8 -cp "lib/*" -d out KiemGroovy.java
java -Dstdout.encoding=UTF-8 -cp "out;lib/*" KiemGroovy Jenkinsfile build.gradle JenkinsfileHong
''', lang="bash", files={"KiemGroovy.java": "KiemGroovy", "Jenkinsfile": "Jenkinsfile", "build.gradle": "BuildGradle", "JenkinsfileHong": "JenkinsfileHong"}, timeout=200,
    claims=["Jenkinsfile và build.gradle đúng cú pháp Groovy; tệp thiếu ngoặc bị từ chối"])

PY_PIPE = prog("MoPhong", r'''
def chay(cac_buoc, hong=None):
    ket = []
    for ten in cac_buoc:
        if hong == ten:
            ket.append(ten + ": that bai")
            break
        ket.append(ten + ": xong")
    else:
        return ket
    ket.append("post failure: dung that bai")
    return ket
for dong in chay(["Build", "Test", "Deploy"], hong="Test"):
    print(dong)
''', lang="python", reason="MÔ PHỎNG (không phải Jenkins): thứ tự các giai đoạn và hành vi `post failure`.", claims=["Test hỏng thì Deploy không chạy và nhánh post failure chạy"])

PY_GIAI = prog("GiaiPhuThuoc", r'''
CAY = {"du an": [("text", "1.10.0"), ("lang3", "3.9")],
       ("text", "1.10.0"): [("lang3", "3.12.0")]}
da, hang = {}, [(k, v, 1) for k, v in CAY["du an"]]
while hang:
    ten, ban, sau = hang.pop(0)
    if ten in da:
        print(f"bo {ten} {ban} (sau {sau}): da co {da[ten]}")
        continue
    da[ten] = ban
    hang += [(k, v, sau + 1) for k, v in CAY.get((ten, ban), [])]
print(da)
''', lang="python", reason="Bộ phân giải tự viết: duyệt theo độ sâu, người đến trước thắng (đường khác với Maven thật).", claims=["kết quả khớp mvn dependency:tree: lang3 3.9"])

# ── Lab (chạy bằng cham.sh, chỉ Python): bộ phân giải theo hai luật ──
LAB_PY = r'''
DU_AN = [("A", "1.0"), ("B", "1.0")]
CAY = {("A", "1.0"): [("X", "1.0"), ("Y", "2.0")],
       ("B", "1.0"): [("Y", "3.0"), ("Z", "1.0")],
       ("Z", "1.0"): [("X", "2.0")]}


def so(v):
    return tuple(int(p) for p in v.split("."))


def maven():
    chon, hang = {}, [(t, v) for t, v in DU_AN]
    while hang:
        ten, ban = hang.pop(0)
        if ten in chon:
            continue
        chon[ten] = ban
        hang += CAY.get((ten, ban), [])
    return chon


def gradle():
    chon, hang = {}, [(t, v) for t, v in DU_AN]
    while hang:
        ten, ban = hang.pop(0)
        if ten in chon and so(chon[ten]) >= so(ban):
            continue
        chon[ten] = ban
        hang += CAY.get((ten, ban), [])
    return chon


for ten, ban in sorted(maven().items()):
    print("maven", ten, ban)
for ten, ban in sorted(gradle().items()):
    if ten not in ("A", "B"):
        print("gradle", ten, ban)
'''
LAB_OUT = """maven A 1.0
maven B 1.0
maven X 1.0
maven Y 2.0
maven Z 1.0
gradle X 2.0
gradle Y 3.0
gradle Z 1.0"""
LAB_DE = """# Lab BNX L26 — Phân giải phiên bản phụ thuộc: Maven và Gradle

**MÔ PHỎNG**: bài này không chạy Maven, Gradle hay Jenkins thật; bạn viết bộ phân giải bằng Python thuần, với đồ thị phụ thuộc là số minh hoạ. Luật Maven đã được kiểm bằng Maven thật ở video; luật Gradle theo hướng dẫn chính thức (không chạy Gradle).

Dự án khai hai phụ thuộc trực tiếp theo thứ tự: `A 1.0`, `B 1.0`. Phụ thuộc bắc cầu (số minh hoạ):

- `A 1.0` cần `X 1.0` rồi `Y 2.0`
- `B 1.0` cần `Y 3.0` rồi `Z 1.0`
- `Z 1.0` cần `X 2.0`

Luật Maven: mỗi thư viện lấy phiên bản của khai báo **gần dự án nhất** (độ sâu nhỏ nhất); cùng độ sâu thì **khai báo trước thắng**.
Luật Gradle mặc định: lấy phiên bản **cao nhất** trong mọi yêu cầu.

Viết `mau.py` in kết quả hai luật: trước hết 5 dòng `maven <tên> <bản>` (A, B, X, Y, Z theo thứ tự chữ cái), rồi 3 dòng `gradle <tên> <bản>` cho X, Y, Z.
Gợi ý: duyệt theo độ sâu (hàng đợi), thư viện nào đã chọn thì bỏ yêu cầu sau (Maven); với Gradle thì chỉ giữ khi phiên bản cao hơn.
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L26 mau.py`.
"""


def build():
    write_lab("BNX", "L26", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Hai công cụ dựng, cùng một đồ thị phụ thuộc, hai phiên bản khác nhau", [
        st("""<p>Dự án khai thẳng thư viện <code>commons-lang3</code> bản <b>3.9</b>. Nhưng thư viện <code>commons-text</code> mà dự án dùng lại cần <code>commons-lang3</code> bản <b>3.12.0</b>.</p>
<div class="box key">Chạy Maven thật: <b>3.9</b> thắng, và báo <code>omitted for conflict with 3.9</code>. Luật mặc định của <b>Gradle</b> (công cụ dựng thứ hai cho Java, đọc <code>build.gradle</code> thay cho <code>pom.xml</code>; theo hướng dẫn chính thức): lấy bản <b>cao nhất</b>, tức 3.12.0.
Cùng đồ thị, hai công cụ, hai kết quả. Làm sao biết bản nào đang chạy, và làm sao để máy bạn và mọi máy khác dựng ra cùng một sản phẩm?</div>""",
           """Chào bạn, dự án khai thẳng một thư viện tiện ích ở bản ba chấm chín. Nhưng một thư viện khác cần chính nó ở bản ba chấm mười hai chấm không. Chạy công cụ dựng thật, bản ba chấm chín thắng và bản kia bị bỏ vì xung đột, còn công cụ dựng thứ hai mặc định lấy bản cao nhất. Vậy làm sao biết bản nào đang chạy, và làm sao để mọi máy cùng ra một sản phẩm?""", focus=[1, 2, 2, 2, 3, 3], introduces=["bnx_gradle"]),
    ], checks=["alg.bnx_l26_maven([('text', '1.10.0'), ('lang3', '3.9')], {('text', '1.10.0'): [('lang3', '3.12.0')]})['lang3'] == '3.9'",
               "alg.bnx_l26_gradle([('text', '1.10.0'), ('lang3', '3.9')], {('text', '1.10.0'): [('lang3', '3.12.0')]})['lang3'] == '3.12.0'"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① thư viện, phiên bản", "gói mã người khác viết sẵn, đóng thành tệp <b>jar</b>; mỗi bản có số phiên bản", "commons-lang3 bản 3.9 và bản 3.12.0 là hai tệp khác nhau"],
                  ["② phụ thuộc", "thư viện mà dự án cần để biên dịch hoặc chạy", "dự án cần commons-text"],
                  ["③ phụ thuộc bắc cầu", "thư viện mình cần lại cần thư viện khác", "commons-text cần commons-lang3"],
                  ["④ dựng (build)", "biến mã nguồn thành sản phẩm chạy được: biên dịch, kiểm thử, đóng gói", "ra một tệp jar"],
                  ["⑤ tệp mô tả dự án", "tệp chữ khai báo dự án cần gì, dựng thế nào; công cụ đọc rồi làm", "<code>pom.xml</code> (Maven), <code>build.gradle</code> (Gradle)"]]),
           """Trước hết ta cần hiểu năm điều. Thư viện là gói mã người khác viết sẵn, mỗi bản có một số phiên bản. Phụ thuộc là thư viện mà dự án cần, và phụ thuộc bắc cầu là khi thư viện mình cần lại cần thêm thư viện khác. Dựng là biến mã nguồn thành sản phẩm chạy được, qua biên dịch, kiểm thử và đóng gói. Tệp mô tả dự án khai báo dự án cần gì và dựng thế nào.""",
           focus=[0, "1.2", ["1.3", "1.4"], "1.5", "1.6"]),
    ], checks=["3 + 9 + 34 > 0"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>&lt;dependency&gt;</code>", "một phụ thuộc: <code>groupId</code> (nhóm), <code>artifactId</code> (tên), <code>version</code> (phiên bản)"],
                  ["pha (phase)", "một chặng của vòng đời dựng, như <code>process-resources</code>, <code>compile</code>, <code>test</code>, <code>package</code>"],
                  ["mục tiêu (goal)", "việc cụ thể của một <b>phần mở rộng</b> (plugin), gắn vào một pha; ví dụ <code>compiler:compile</code> gắn vào pha <code>compile</code>"],
                  ["<code>mvn dependency:tree</code>", "lệnh in <b>cây phụ thuộc</b>: dự án ở gốc, mỗi cấp thụt vào là một tầng bắc cầu"],
                  ["<code>omitted for conflict</code>", "báo: phiên bản này bị <b>bỏ</b> vì xung đột với phiên bản đã chọn"],
                  ["<code>Jenkinsfile</code>", "tệp khai báo <b>đường ống</b> dựng cho <b>Jenkins</b>, phần mềm chạy trên <b>máy chủ dựng</b> (máy riêng chuyên dựng tự động khi có mã mới): <code>pipeline</code>, <code>stages</code>, <code>stage</code>, <code>steps</code>, <code>post</code>"],
                  ["<code>outputTimestamp</code>", "mốc thời gian cố định để ghi vào tệp dựng, thay cho giờ chạy thật"]]),
           """Mỗi khối phụ thuộc có ba phần là nhóm, tên và phiên bản. Pha là một chặng của vòng đời dựng, còn mục tiêu là việc cụ thể của phần mở rộng, gắn vào một pha. Lệnh cây phụ thuộc in dự án ở gốc, mỗi cấp thụt vào là một tầng bắc cầu. Dòng báo bỏ vì xung đột cho biết phiên bản đó đụng phiên bản đã chọn. Tệp đường ống dành cho máy chủ dựng, máy riêng chuyên dựng tự động khi có mã mới. Mốc thời gian đầu ra là giờ cố định ghi vào tệp dựng.""",
           focus=["1.2", ["1.3", "1.4"], "1.5", "1.6", "1.7", "1.8"],
           introduces=["bnx_jenkins", "bnx_may_dung"]),
        st(table(["viết trong lệnh", "đọc là", "ví dụ nhỏ"],
                 [["<code>&#36;M -B -q dependency:tree -DoutputFile=cay.txt &amp;&amp; cat cay.txt</code>", "<code>&#36;M</code>: biến chứa đường dẫn lệnh <code>mvn</code> (đặt ở dòng đầu); <code>-B</code> chạy không hỏi, <code>-q</code> ít chữ; <code>-Dx=y</code> đặt tham số <code>x</code> bằng <code>y</code>; <code>&amp;&amp;</code> chạy lệnh sau nếu lệnh trước thành công; <code>cat</code> in tệp", "<code>echo hi &amp;&amp; echo ok</code> in cả hai dòng"],
                  ["<code>mvn -B package | grep -- '--- ' | cut -c8-</code>", "dấu <code>|</code> đưa đầu ra lệnh trái làm đầu vào lệnh phải; <code>grep</code> giữ dòng có chuỗi <code>--- </code> (<code>--</code> báo hết tuỳ chọn); <code>cut -c8-</code> bỏ 7 ký tự đầu mỗi dòng", "<code>cut -c3-</code> biến <code>abcde</code> thành <code>cde</code>"],
                  ["<code>a=&#36;(dung &#36;1)</code>, <code>cut -d' ' -f1</code>", "<code>dung() { … }</code> là hàm; <code>&#36;1</code>, <code>&#36;2</code> là đối số đầu, đối số hai; <code>&#36;(…)</code> lấy đầu ra của lệnh gán cho biến <code>a</code>; <code>cut -d' ' -f1</code> lấy cột đầu của dòng, các cột tách bằng dấu cách", "<code>a=&#36;(echo xin)</code> thì <code>a</code> là <code>xin</code>; <code>sleep 2</code> chờ 2 giây; <code>[ x = y ] &amp;&amp; A || B</code>: x bằng y thì làm A, không thì làm B"]]),
           """Trước hết, đọc vài ký hiệu của lệnh. Biến chứa đường dẫn lệnh dựng, các tuỳ chọn gạch ngang chọn chế độ chạy, hai dấu và nối lệnh sau chỉ chạy khi lệnh trước thành công. Dấu gạch đứng đưa đầu ra lệnh trái vào lệnh phải, lọc giữ dòng có chuỗi cho trước, rồi cắt bỏ vài ký tự đầu mỗi dòng. Cuối cùng là hàm với đối số đầu và đối số hai, lấy đầu ra lệnh gán vào biến, chờ một lúc, và phép so sánh chọn việc làm.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st(table(["viết trong mã", "đọc là", "ví dụ nhỏ"],
                 [["<code>for d in a b c; do … done</code>", "lặp: <code>d</code> lần lượt là <code>a</code>, <code>b</code>, <code>c</code>; mỗi lần chạy các dòng giữa <code>do</code> và <code>done</code>", "<code>&#36;d</code> là giá trị hiện tại của <code>d</code>"],
                  ["<code>implementation 'org.apache.commons:commons-lang3:3.9'</code>", "Gradle: một phụ thuộc viết gọn thành <code>nhóm:tên:bản</code>", "<code>mavenCentral()</code> là kho tải thư viện"],
                  ["phiên bản dạng khoảng, <code>latest</code>", "khoảng như <code>[3.0,4.0)</code>: bản nào trong khoảng cũng được; <code>latest</code>: bản mới nhất ở thời điểm dựng, nên mỗi lần dựng có thể một khác", "<code>[3.0,4.0)</code> gồm 3.0, không gồm 4.0"]]),
           """Tiếp theo là vòng lặp liệt kê từng giá trị. Một phụ thuộc của công cụ dựng thứ hai viết gọn thành nhóm, tên và bản. Phiên bản dạng khoảng hay chữ mới nhất cho phép nhiều bản, nên mỗi lần dựng có thể một khác.""",
           focus=["1.2", "1.3", "1.4"], clear=True),
    ], checks=["len(alg.bnx_l26_phases()) == 6"])

    intu = sc("intuition", "intuition", "Hình dung: cây phụ thuộc và đường ống dựng", [
        st(svg(1500, 520,
               txt(750, 40, "Cây phụ thuộc: bản của khai báo gần dự án nhất thắng (Maven)", 26, "middle", "#1f2937", True),
               box(560, 80, 380, 70, ["dự án l26", "(gốc, độ sâu 0)"], C_BLUE, 22, True),
               box(160, 230, 420, 80, ["commons-text 1.10.0", "(độ sâu 1)"], C_AMBER, 22),
               box(920, 230, 420, 80, ["commons-lang3 3.9", "(độ sâu 1) THẮNG"], C_GREEN, 22, True),
               box(160, 380, 420, 80, ["commons-lang3 3.12.0", "(độ sâu 2) bị bỏ"], C_RED, 22, False, True),
               arrow(700, 155, 430, 225), arrow(800, 155, 1070, 225), arrow(370, 315, 370, 375, "#dc2626"), txt(395, 352, "cần", 22, "start", "#dc2626", True),
               txt(1130, 400, "Maven: gần nhất thắng, cùng độ sâu thì khai báo trước thắng", 22, "middle", "#16a34a", True),
               txt(1130, 440, "Gradle (mặc định): lấy bản cao nhất → 3.12.0", 22, "middle", "#d97706", True),
               txt(750, 495, "Muốn chắc một bản: khai nó thẳng trong tệp mô tả dự án", 22, "middle", "#1f2937", True)),
           """Hình này là cây phụ thuộc: dự án ở gốc, hai phụ thuộc trực tiếp ở độ sâu một. Thư viện thứ nhất cần thư viện tiện ích ở bản mới hơn, độ sâu hai, còn dự án tự khai bản cũ ở độ sâu một. Công cụ thứ nhất cho bản gần dự án nhất thắng, công cụ thứ hai lấy bản cao nhất. Muốn chắc một bản, hãy khai thẳng."""),
        st(svg(1500, 430,
               txt(750, 40, "Jenkinsfile: các giai đoạn nối tiếp, hỏng thì dừng và chạy nhánh post", 26, "middle", "#1f2937", True),
               box(60, 130, 280, 90, ["Build", "mvn package"], C_GREEN, 24, True),
               box(430, 130, 280, 90, ["Test", "mvn verify"], C_RED, 24, True),
               box(800, 130, 280, 90, ["Deploy", "không chạy"], C_GRAY, 24, False, True),
               box(1170, 260, 270, 90, ["post failure", "echo dung that bai"], C_AMBER, 22, True),
               arrow(345, 175, 425, 175), arrow(715, 175, 795, 175, "#9ca3af", None, 20, True), arrow(580, 225, 1166, 300, "#d97706", "hỏng", 20),
               txt(750, 385, "MÔ PHỎNG — Jenkins không chạy trên máy này", 34, "middle", "#b45309", True),
               txt(750, 412, "hình mô tả quy tắc theo hướng dẫn chính thức", 22, "middle", "#475569")),
           """Hình thứ hai là đường ống ba giai đoạn nối tiếp. Kiểm thử hỏng thì giai đoạn sau không chạy và nhánh thất bại chạy. Ta chỉ vẽ lại quy tắc, vì máy chủ dựng không chạy ở đây.""",
           ),
    ], checks=["alg.bnx_l26_maven([('text', '1.10.0'), ('lang3', '3.9')], {('text', '1.10.0'): [('lang3', '3.12.0')]}) == {'text': '1.10.0', 'lang3': '3.9'}"])

    form = sc("formula", "formula", "Suy ra từng bước: từ tệp mô tả dự án tới sản phẩm dựng ra", [
        st("""<p><b>Bước 1.</b> Muốn mọi máy dựng giống nhau, ta ghi mọi thứ vào <b>một tệp mô tả dự án</b>: tên dự án, bản Java, và danh sách phụ thuộc. Công cụ đọc tệp này rồi tự tải thư viện và dựng.</p>"""
           + X_POM.show(lines=(9, 20), title="pom.xml (trích): hai phụ thuộc trực tiếp"),
           """Bước một: ghi mọi thứ vào một tệp mô tả dự án, gồm tên, bản Java và danh sách phụ thuộc. Công cụ đọc tệp nên tự tải thư viện và dựng.""", focus=[1, 3],
           clear=True),
        st("""<p><b>Bước 2. Vòng đời.</b> Một lệnh dựng đi qua <b>các pha nối tiếp</b> theo thứ tự cố định, từ pha đầu tới pha được gọi. Pha chỉ là chặng: việc làm thật do <b>mục tiêu</b> của phần mở rộng gắn vào pha.</p>"""
           + table(["pha", "mục tiêu gắn vào (phần mở rộng:mục tiêu)"],
                   [["process-resources", "resources:resources"],
                    ["compile", "compiler:compile"],
                    ["process-test-resources", "resources:testResources"],
                    ["test-compile", "compiler:testCompile"],
                    ["test", "surefire:test"],
                    ["package", "jar:jar"]])
           + """$$\\text{gọi package} \\Rightarrow 17 \\text{ pha, } \\hl{6} \\text{ mục tiêu chạy theo thứ tự}$$""",
           """Bước hai là vòng đời: một lệnh dựng đi qua các pha nối tiếp theo thứ tự cố định. Pha chỉ là chặng, việc làm thật do mục tiêu gắn vào pha. Gọi pha đóng gói đi qua mười bảy pha, trong đó sáu pha có mục tiêu như bảng.""",
           clear=True),
        st("""<p><b>Bước 3. Phụ thuộc bắc cầu.</b> Mỗi thư viện có tệp mô tả riêng, khai thư viện nó cần. Công cụ lần theo, nên một phụ thuộc trực tiếp kéo theo cả chùm: ở phần ví dụ, <b>1</b> phụ thuộc kéo <b>9</b>, rồi <b>34</b> gói thư viện tuỳ dự án.</p>
$$1 \\to 1; \\qquad 1 \\to 9; \\qquad 1 \\to 34 \\;\\; (\\text{số đo thật ở phần ví dụ})$$""",
           """Bước ba là phụ thuộc bắc cầu: công cụ lần theo tệp mô tả của từng thư viện. Nên một phụ thuộc trực tiếp kéo theo cả chùm: ba dự án thử là một, chín và ba mươi bốn gói.""",
           clear=True),
        st("""<p><b>Bước 4. Xung đột.</b> Khi cùng một thư viện xuất hiện ở hai bản, công cụ phải chọn một. <b>Maven</b>: bản của khai báo <b>gần dự án nhất</b> (độ sâu nhỏ nhất); cùng độ sâu thì <b>khai báo trước</b> thắng. <b>Gradle</b> mặc định: bản <b>cao nhất</b>.</p>"""
           + table(["thư viện", "yêu cầu", "độ sâu", "Maven chọn", "Gradle chọn"],
                   [["lang3", "3.9 (dự án khai)", "1", "<b>3.9</b>", "3.12.0"],
                    ["lang3", "3.12.0 (qua text)", "2", "bỏ", "(cao nhất)"]]),
           """Bước bốn là xung đột: cùng một thư viện ở hai bản thì chỉ một bản vào được, nên công cụ phải chọn. Công cụ thứ nhất chọn khai báo gần dự án nhất, cùng độ sâu thì khai báo trước thắng. Công cụ thứ hai chọn bản cao nhất.""",
           focus=[[1], 1, 2], clear=True),
        st("""<p><b>Bước 5. Đường ống.</b> Máy chủ dựng đọc <b>Jenkinsfile</b> nằm cùng mã nguồn, viết bằng <b>Groovy</b> (ngôn ngữ kịch bản chạy trên Java). <code>pipeline</code> chứa <code>stages</code>, mỗi <code>stage</code> có <code>steps</code>.
<code>agent any</code>: chạy trên máy dựng nào đang rảnh. <code>sh '…'</code>: chạy một lệnh như bạn gõ tay.</p>"""
           + JENKINSFILE.show(lines=(1, 9), title="Jenkinsfile (trích, phần 1)"),
           """Bước năm là đường ống: máy chủ dựng đọc một tệp khai báo nằm cùng mã nguồn. Tệp viết bằng một ngôn ngữ kịch bản chạy trên Java, ta chỉ cần đọc các khối lồng nhau. Dòng chọn máy nghĩa là chạy trên máy đang rảnh, dòng lệnh chạy một lệnh như gõ tay.""",
           clear=True, introduces=["bnx_groovy", "bnx_agent", "bnx_sh"]),
        st("""<p>Giai đoạn cuối triển khai; khối <code>post</code> chạy khi xong hoặc khi hỏng, và <code>failure</code> chỉ chạy khi có giai đoạn hỏng.</p>"""
           + JENKINSFILE.show(lines=(10, 17), title="Jenkinsfile (trích, phần 2)"),
           """Giai đoạn cuối là triển khai, và khối sau cùng chạy khi xong hoặc khi hỏng, nghĩa là nhánh thất bại chỉ chạy khi có giai đoạn hỏng.""",
           clear=True),
        st("""<p><b>Bước 6. Dựng tái lập.</b> Một jar có chứa <b>mốc thời gian</b> của từng tệp bên trong, nên hai lần dựng cùng mã nguồn vẫn có thể ra hai jar khác nhau từng bit. Đặt <code>project.build.outputTimestamp</code> cố định mốc đó. Cách thử: dựng hai lần, so <b>mã băm</b> (sha256): dãy ký tự ngắn tính từ toàn bộ nội dung tệp; đổi một bit thì cả dãy đổi.</p>"""
           + """$$\\text{sha256(gói lần 1)} = \\text{sha256(gói lần 2)} \\;\\Rightarrow\\; \\text{dựng tái lập}$$""",
           """Bước sáu là dựng tái lập: một gói chứa mốc thời gian của từng tệp bên trong, nên hai lần dựng cùng mã nguồn vẫn có thể khác nhau từng bit. Đặt mốc cố định thì hết khác. Cách thử là so mã băm, dãy ký tự ngắn tính từ toàn bộ nội dung gói.""",
           clear=True, introduces=["bnx_ma_bam"]),
    ], checks=["alg.bnx_l26_maven([('text', '1.10.0'), ('lang3', '3.9')], {('text', '1.10.0'): [('lang3', '3.12.0')]})['lang3'] == '3.9'",
               "alg.bnx_l26_gradle([('text', '1.10.0'), ('lang3', '3.9')], {('text', '1.10.0'): [('lang3', '3.12.0')]})['lang3'] == '3.12.0'",
               "len(alg.bnx_l26_phases()) == 6 and len(alg.bnx_l26_phase_goals()) == 6 and alg.bnx_l26_phase_count() == 17",
               "[g.split(':')[1] for p, g in alg.bnx_l26_phase_goals()] == alg.bnx_l26_phases()"])

    ex = sc("example", "example", "Ví dụ chạy thật Maven, từng phép tính", [
        st(SH_CAY.show(lines=(4, 6), title="Chạy thật: in cây phụ thuộc, rồi chạy lại ở chế độ chi tiết"),
           """Ta chạy thật công cụ dựng thứ nhất, bản ba chấm chín mười một, trên tệp mô tả vừa xem. Lệnh đầu in cây thường, lệnh sau in thêm các bản bị bỏ vì xung đột.""",
           clear=True),
        st(SH_CAY.out_html()
           + """$$① \\; \\text{lang3 3.9 ở độ sâu 1 thắng 3.12.0 ở độ sâu 2: } \\hl{\\text{omitted for conflict with 3.9}}$$""",
           """Phép tính thứ nhất, kết quả thật: cây thường chỉ có hai phụ thuộc trực tiếp. Bản chi tiết cho thấy thư viện tiện ích bản ba chấm mười hai nằm dưới thư viện xử lý chữ, bị bỏ vì xung đột với bản ba chấm chín.""",
           clear=True),
        st(SH_VONGDOI.show(lines=(4, 4), title="Chạy thật: dựng tới pha package, chỉ giữ dòng tên mục tiêu") + SH_VONGDOI.out_html()
           + """$$② \\; 6 \\text{ mục tiêu của phần mở rộng chạy đúng thứ tự: resources} \\to \\text{jar}$$""",
           """Phép tính thứ hai là vòng đời: gọi pha đóng gói, công cụ chạy sáu mục tiêu theo đúng thứ tự, mỗi mục tiêu gắn vào một pha như bảng vừa xem. Mỗi dòng ghi phần mở rộng, mục tiêu và phiên bản thật.""", focus=[1, 4],
           clear=True),
        jstep([(("<code>M=…/bin/mvn</code>, <code>test -x $M || { …; exit 97; }</code>",
                 "đặt biến <code>M</code> là đường dẫn lệnh <code>mvn</code>; <code>test -x</code> hỏi tệp đó chạy được không; <code>||</code> làm vế sau nếu vế trước thất bại; <code>exit 97</code> dừng với mã 97",
                 "Biến chứa đường dẫn lệnh dựng, và dừng chương trình nếu lệnh ấy không chạy được."), "thiếu <code>mvn</code> thì in lỗi rồi dừng", ""),
               (("<code>mkdir -p src/main/java &amp;&amp; cp Chao.java src/main/java/</code>",
                 "<code>mkdir -p</code>: tạo thư mục (cả thư mục cha nếu thiếu); <code>cp A B</code>: chép tệp A vào B; <code>&amp;&amp;</code>: chỉ chép khi tạo xong",
                 "Tạo thư mục rồi chép tệp mã nguồn vào, chỉ khi tạo xong."), "", ""),
               (("<code>$M -B -q -f $1 clean package &gt; /dev/null 2&gt;&amp;1</code>",
                 "<code>-f $1</code>: dùng tệp mô tả tên trong đối số đầu; <code>clean package</code>: xoá đầu ra cũ rồi dựng gói; <code>&gt; /dev/null</code>: bỏ chữ in ra; <code>2&gt;&amp;1</code>: bỏ luôn chữ báo lỗi",
                 "Dựng sạch theo tệp mô tả đưa vào, và bỏ hết chữ in ra."), "", ""),
               (("<code>sha256sum target/l26-1.jar</code>",
                 "in mã băm sha256 của tệp (cột đầu), rồi tên tệp",
                 "Lệnh băm in mã băm rồi tên tệp, lệnh cắt giữ cột đầu."), "", "")]),
        st(SH_TAILAP.show(lines=(1, 7), title="Mã dựng hai lần (1/2): đặt lệnh, hàm dung dựng rồi in mã băm"),
           """Phép tính thứ ba là dựng tái lập. Hàm này dựng sạch một lần theo tệp mô tả đưa vào, rồi in mã băm của gói.""",
           clear=True),
        st(SH_TAILAP.show(lines=(8, 13), title="Mã dựng hai lần (2/2): cách nhau 2 giây, so mã băm sha256 (kết quả ở khung sau)"),
           """Hàm so gọi hàm dựng hai lần cách nhau hai giây rồi so mã băm. Lần đầu dùng tệp không đặt mốc thời gian, lần sau dùng tệp có mốc cố định.""",
           clear=True),
        st(SH_TAILAP.out_html()
           + """$$③ \\; \\text{không đặt mốc: } \\hl{\\text{khác}}; \\qquad \\text{đặt } 2026\\text{-}01\\text{-}01\\text{: } \\hlg{\\text{giống}}$$""",
           """Không đặt mốc thời gian thì hai gói khác nhau, đặt mốc cố định thì hai gói giống nhau từng bit. Đây là số đo cho gói một lớp nhỏ này, không nói mọi dự án tái lập được nhờ một thuộc tính.""", focus=[1, 3],
           clear=True),
        st(SH_KIEM.out_html("""Jenkinsfile: cu phap hop le
build.gradle: cu phap hop le
JenkinsfileHong: loi cu phap""", "Kiểm CÚ PHÁP bằng trình biên dịch Groovy thật (không chạy Jenkins, không chạy Gradle)")
           + """$$④ \\; \\text{chỉ kiểm cú pháp: 2 tệp đúng, 1 tệp thiếu ngoặc bị từ chối}$$""",
           """Phép tính thứ tư: máy này không có máy chủ dựng, nên ta chỉ kiểm cú pháp bằng trình biên dịch của ngôn ngữ kịch bản thật. Tệp đúng thì qua, tệp thiếu ngoặc bị từ chối, nhưng chưa chứng minh đường ống chạy đúng.""", focus=[1, 3],
           clear=True),
        jstep([(("<code>def chay(cac_buoc, hong=None):</code>",
                 "khai hàm Python: <code>def</code>, tên, tham số, dấu hai chấm; các dòng thụt vào là thân; <code>hong=None</code>: tham số có giá trị mặc định rỗng nếu không truyền",
                 "Khai hàm, trong đó tham số có thể có giá trị mặc định rỗng."), "<code>chay([\"Build\"])</code> thì <code>hong</code> là rỗng", ""),
               (("<code>ket = []</code>, <code>ket.append(x)</code>, <code>ten + \": xong\"</code>",
                 "<code>[]</code>: danh sách rỗng; <code>append</code>: thêm một phần tử vào cuối danh sách; <code>+</code> giữa hai chuỗi: nối lại",
                 "Danh sách rỗng, thêm phần tử vào cuối, và dấu cộng nối hai chuỗi."), "", ""),
               (("<code>if hong == ten:</code>, <code>break</code>",
                 "<code>==</code>: hỏi hai giá trị có bằng nhau; <code>break</code>: thoát vòng lặp ngay lập tức",
                 "Hai dấu bằng so sánh hai giá trị, còn lệnh thoát rời khỏi vòng lặp ngay."), "", ""),
               (("<code>for … : … else:</code>",
                 "khối <code>else</code> của vòng <code>for</code> chỉ chạy khi vòng lặp chạy hết mà <b>không</b> gặp <code>break</code>; gặp <code>break</code> thì bỏ qua <code>else</code>",
                 "Khối ngược lại của vòng lặp chạy khi vòng không gặp lệnh thoát."), "", "")]),
        st(PY_PIPE.show(lines=(1, 13), title="MÔ PHỎNG bằng Python (không phải Jenkins): giai đoạn Test hỏng"),
           """Phép tính thứ năm là hành vi khi một giai đoạn hỏng, và đây là mô phỏng, không phải máy chủ thật. Hàm chạy các giai đoạn lần lượt, gặp giai đoạn hỏng thì dừng rồi chạy nhánh khi thất bại.""",
           clear=True),
        st(PY_PIPE.out_html("""Build: xong
Test: that bai
post failure: dung that bai""", "Kết quả mô phỏng (Python, không phải Jenkins)")
           + """$$⑤ \\; \\text{Test hỏng} \\Rightarrow \\text{Deploy không chạy; nhánh post failure chạy}$$""",
           """Kết quả mô phỏng: kiểm thử hỏng, giai đoạn triển khai không chạy và nhánh khi thất bại chạy, đúng như hướng dẫn mô tả.""",
           clear=True),
    ], checks=["alg.bnx_l26_maven([('text', '1.10.0'), ('lang3', '3.9')], {('text', '1.10.0'): [('lang3', '3.12.0')]})['lang3'] == '3.9'",
               "alg.bnx_l26_phases() == ['resources', 'compile', 'testResources', 'testCompile', 'test', 'jar']"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: bộ phân giải tự viết", [
        jstep([(("<code>CAY = {\"du an\": [(\"text\", \"1.10.0\"), …], (\"text\", \"1.10.0\"): […]}</code>",
                 "từ điển: <code>{khoá: giá trị}</code>; khoá là chuỗi hoặc cặp (tên, bản); giá trị là danh sách các cặp mà nó cần; <code>CAY[\"du an\"]</code> lấy giá trị của khoá <code>\"du an\"</code>",
                 "Từ điển gồm các cặp khoá và giá trị, giá trị ở đây là danh sách thư viện."), "<code>CAY[\"du an\"]</code> là hai cặp đầu tiên", ""),
               (("<code>da, hang = {}, [(k, v, 1) for k, v in CAY[\"du an\"]]</code>",
                 "gán hai biến một lúc: <code>da</code> là từ điển rỗng <code>{}</code>; <code>hang</code> là danh sách sinh sẵn: mỗi cặp <code>k, v</code> của dự án thành bộ ba <code>(k, v, 1)</code>, số 1 là độ sâu",
                 "Gán hai biến một lúc: từ điển rỗng và danh sách sinh sẵn."), "", ""),
               (("<code>while hang:</code>",
                 "lặp chừng nào danh sách <code>hang</code> còn phần tử; danh sách rỗng thì dừng",
                 "Lặp chừng nào danh sách còn phần tử, rỗng thì dừng."), "", ""),
               (("<code>ten, ban, sau = hang.pop(0)</code>",
                 "<code>pop(0)</code>: lấy phần tử đầu danh sách ra và bỏ nó khỏi danh sách; ba giá trị của bộ ba gán vào ba tên",
                 "Lấy phần tử đầu ra khỏi danh sách nên danh sách ngắn dần, rồi gán ba giá trị vào ba tên."), "", "")]),
        jstep([(("<code>if ten in da:</code> … <code>continue</code>",
                 "<code>in</code>: đúng khi <code>ten</code> đã là khoá của <code>da</code>; <code>continue</code>: bỏ phần còn lại của vòng này, sang vòng kế tiếp",
                 "Phép thuộc hỏi tên đã có chưa, và lệnh tiếp tục bỏ phần còn lại của vòng này."), "", ""),
               (("<code>print(f\"bo {ten} {ban} (sau {sau}): da co {da[ten]}\")</code>",
                 "chuỗi f: phần trong ngoặc nhọn được thay bằng giá trị; <code>da[ten]</code>: giá trị của khoá <code>ten</code> trong <code>da</code>",
                 "Chuỗi f thay phần trong ngoặc nhọn bằng giá trị của biểu thức."), "", ""),
               (("<code>da[ten] = ban</code>",
                 "ghi vào <code>da</code>: khoá <code>ten</code> có giá trị <code>ban</code> (người đến trước giữ chỗ)",
                 "Ghi vào từ điển: người đến trước giữ chỗ."), "", ""),
               (("<code>hang += [(k, v, sau + 1) for k, v in CAY.get((ten, ban), [])]</code>",
                 "<code>CAY.get(khoá, [])</code>: giá trị của khoá, không có khoá thì trả danh sách rỗng; <code>+=</code>: nối thêm vào cuối <code>hang</code>; mỗi cặp mới có độ sâu <code>sau + 1</code>",
                 "Lấy các thư viện nó cần, không có thì rỗng, rồi nối vào cuối hàng với độ sâu tăng một."), "", "")]),
        st(PY_GIAI.show(lines=(1, 11), title="Bộ phân giải tự viết: duyệt theo độ sâu, người đến trước thắng"),
           """Ta kiểm bằng đường khác, không dùng công cụ dựng, vì bộ phân giải viết tay cho thấy rõ luật chọn. Nó duyệt hàng đợi theo thứ tự khai báo, thư viện đã chọn thì mọi yêu cầu sau về nó bị bỏ.""", focus=[1, 2],
           clear=True),
        st(PY_GIAI.out_html() + table(["cách", "lang3 được chọn", "dòng bị bỏ"],
                                    [["Maven chạy thật (dependency:tree -Dverbose)", "3.9", "omitted for conflict with 3.9"],
                                     ["bộ phân giải tự viết", "3.9", "bo lang3 3.12.0 (sau 2): da co 3.9"],
                                     ["luật Gradle (theo hướng dẫn chính thức)", "3.12.0", "(không chạy Gradle)"]]),
           """Bộ phân giải tự viết chọn bản ba chấm chín, giống công cụ dựng thật, và bỏ đúng bản ba chấm mười hai ở độ sâu hai. Hai đường độc lập khớp nhau nên ta tin luật gần nhất thắng; hàng cuối là luật theo hướng dẫn, ta không chạy.""", focus=[1, 3],
           clear=True),
    ], checks=["alg.bnx_l26_maven([('text', '1.10.0'), ('lang3', '3.9')], {('text', '1.10.0'): [('lang3', '3.12.0')]})['lang3'] == '3.9'"])

    quymo = sc("quymo", "example", "Khi dự án lớn dần: số gói thư viện và số máy dựng", [
        jstep([(("<code>mkdir -p $d &amp;&amp; cp pom-$d.xml $d/pom.xml</code>",
                 "tạo thư mục tên <code>d</code>, rồi chép <code>pom-d.xml</code> vào đó và đổi tên thành <code>pom.xml</code>",
                 "Tạo thư mục riêng cho từng dự án thử, rồi chép tệp mô tả vào."), "", ""),
               (("<code>(cd $d &amp;&amp; $M -B -q dependency:list -DoutputFile=ds.txt)</code>",
                 "cặp ngoặc tròn chạy lệnh trong vỏ riêng: <code>cd</code> đổi thư mục chỉ bên trong; <code>dependency:list</code> ghi danh sách mọi gói đã phân giải ra <code>ds.txt</code>",
                 "Cặp ngoặc tròn chạy trong vỏ riêng nên đổi thư mục chỉ có hiệu lực bên trong; lệnh danh sách ghi mọi gói ra tệp."), "", ""),
               (("<code>grep -c ':jar:' $d/ds.txt</code>",
                 "đếm số dòng có chuỗi <code>:jar:</code>; mỗi dòng của danh sách là một gói jar",
                 "Lệnh lọc đếm số dòng mô tả một gói thư viện, tức là số gói."), "", "")]),
        st(SH_QUYMO.show(lines=(3, 7), title="Chạy thật: mỗi dự án thử khai đúng 1 phụ thuộc, đếm gói thư viện đã phân giải") + SH_QUYMO.out_html()
           + """$$1 \\text{ phụ thuộc trực tiếp} \\to 1,\\; 9,\\; 34 \\text{ gói thư viện (đo thật)}$$""",
           """Số đo thật: ba dự án thử, mỗi dự án chỉ khai một phụ thuộc trực tiếp. Thư viện tiện ích kéo một gói, thư viện lõi của Spring kéo chín gói, bộ khởi đầu dịch vụ web của Spring kéo ba mươi bốn gói. Càng nhiều gói, càng nhiều chỗ xung đột.""", focus=[1, [2, 3, 4], 4],
           clear=True),
        st(table(["lượt dựng mỗi giờ (số minh hoạ)", "mỗi lượt (phút)", "phút dựng cần mỗi giờ", "máy dựng tối thiểu", "so với ×1"],
                 [["4", "10", "40", "1", nowrap("×1")],
                  ["400", "10", nowrap("4 000"), "67", nowrap("×100")],
                  [nowrap("40 000"), "10", nowrap("400 000"), nowrap("6 667"), nowrap("×10 000")]]),
           """Còn máy chủ dựng khi nhiều người cùng đẩy mã? Số minh hoạ: bốn lượt mỗi giờ, mỗi lượt mười phút, cần bốn mươi phút nên một máy là đủ. Gấp một trăm lần là bốn trăm lượt, cần sáu mươi bảy máy. Gấp mười nghìn lần cần sáu nghìn sáu trăm sáu mươi bảy máy, nên một máy dựng chung gãy từ lâu. Đánh đổi là dựng song song hoặc rút ngắn mỗi lượt bằng bộ đệm.""", clear=True),
    ], checks=["[alg.bnx_l26_agents(b, 10) for b in (4, 400, 40000)] == [1, 67, 6667]", "4 * 10 == 40 and 400 * 10 == 4000 and 40000 * 10 == 400000",
               "400 // 4 == 40000 // 400 == 100"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tin rằng bản khai trong tệp mô tả là bản <b class="red">đang chạy</b>. Dự án khai <code>commons-lang3</code> 3.9 thì được 3.9 vì khai thẳng; nhưng thư viện khai <b>bắc cầu</b>
mà ta không khai thẳng thì bản thật do luật chọn quyết định. Cách xem: in cây phụ thuộc, tìm dòng <code>omitted for conflict</code>.</div>"""
           + SH_CAY.out_html(),
           """Lỗi thứ nhất, của người mới, là tin rằng bản khai là bản đang chạy. Thư viện bắc cầu thì luật chọn quyết định. Cách xem là in cây phụ thuộc và tìm dòng báo bỏ vì xung đột.""", focus=[1, 2, 3], clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Khai bản <b class="red">cũ hơn</b> bản mà thư viện khác cần, để "cho khớp". Chạy thật: Maven ép bản cũ 3.9, thư viện <code>commons-text</code> được dựng và kiểm thử với bản 3.12.0
nhưng chạy với bản 3.9: lỗi chỉ lộ lúc chạy, nếu hàm nó gọi chưa có ở bản cũ.</div>""",
           """Lỗi thứ hai: khai bản cũ hơn bản mà thư viện khác cần. Công cụ ép dùng bản cũ, nên thư viện kia chỉ lỗi lúc chạy nếu hàm nó gọi chưa có ở bản cũ.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Một máy dựng dùng chung, mỗi lượt 10 phút. Ở 4 lượt mỗi giờ thì ổn; ở 400 lượt mỗi giờ cần <b class="red">67 máy</b>:
hàng đợi dựng dài thêm mãi, lập trình viên chờ hàng giờ. Phòng: đo thời gian chờ ở hàng đợi, và dự trù máy theo công thức trước khi đội lớn.</div>""",
           """Lỗi thứ ba, lộ ra khi tải tăng: một máy dựng dùng chung, mỗi lượt mười phút. Bốn trăm lượt mỗi giờ cần sáu mươi bảy máy, nếu không hàng đợi dài mãi. Cách phòng là dự trù số máy trước khi đội lớn.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> Khai phiên bản <b class="red">dạng khoảng hoặc <code>latest</code></b>, hoặc dựng không ghim: một lần dựng sau nhiều tháng kéo thư viện mới, sản phẩm đổi mà mã không đổi.
Cách chữa: ghim phiên bản, đặt <code>outputTimestamp</code>, và so mã băm hai lần dựng trên máy chủ dựng; ai cũng dựng lại được đúng sản phẩm đã phát hành.</div>""",
           """Lỗi thứ tư, lộ ra khi vận hành lâu: khai phiên bản dạng khoảng hoặc không ghim. Dựng sau nhiều tháng kéo thư viện mới, nên sản phẩm đổi mà mã không đổi. Cách chữa là ghim phiên bản, đặt mốc cố định và so mã băm.""", clear=True),
    ], checks=["alg.bnx_l26_agents(400, 10) == 67", "alg.bnx_l26_maven([('text', '1.10.0'), ('lang3', '3.9')], {('text', '1.10.0'): [('lang3', '3.12.0')]})['lang3'] == '3.9'"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Dự án khai <code>P 1.0</code> rồi <code>Q 1.0</code>. <code>P 1.0</code> cần <code>Z 2.0</code>; <code>Q 1.0</code> cần <code>Z 3.0</code>. Cả hai ở cùng độ sâu 2. Maven chọn <code>Z</code> bản nào? Gradle (mặc định) chọn bản nào?"],
                  ["2", "Tính số máy dựng tối thiểu: 120 lượt dựng mỗi giờ, mỗi lượt 15 phút (số minh hoạ). Nếu mỗi lượt giảm còn 5 phút thì sao?"],
                  ["3", "Quyết định: sản phẩm phát hành tháng trước cần dựng lại đúng từng bit để điều tra sự cố. Chọn: ghim phiên bản + <code>outputTimestamp</code>, chỉ ghim phiên bản, hay để mặc định? Vì sao?"]]),
           """Đến lượt bạn, ba câu để làm ra giấy: hai công cụ chọn bản nào, cần bao nhiêu máy dựng, và chọn cách nào để dựng lại đúng từng bit. Hãy dừng lại làm ra giấy rồi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=30),
        st("""<p>Câu 1: cùng độ sâu thì <b>khai báo trước thắng</b> (Maven); Gradle lấy cao nhất.</p>
$$\\text{Maven: } Z = \\hlg{2.0} \\;(\\text{P khai trước Q}); \\qquad \\text{Gradle: } Z = \\hlg{3.0}$$""",
           """Đáp án câu một, ở công cụ thứ nhất, cùng độ sâu thì khai báo trước thắng, nên chọn bản hai chấm không. Công cụ thứ hai lấy bản cao nhất, tức bản ba chấm không."""),
        st("""<p>Câu 2: số máy = phút dựng mỗi giờ : 60, làm tròn lên.</p>
$$120 \\times 15 = 1800 \\text{ phút}; \\; 1800 : 60 = \\hlg{30} \\text{ máy}; \\qquad 120 \\times 5 = 600; \\; 600 : 60 = \\hlg{10} \\text{ máy}$$""",
           """Đáp án câu hai, một trăm hai mươi lượt nhân mười lăm phút là một nghìn tám trăm phút mỗi giờ, chia sáu mươi được ba mươi máy. Còn năm phút mỗi lượt thì sáu trăm phút, cần mười máy."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["ghim phiên bản + outputTimestamp", "dựng lại ra đúng cùng mã băm; điều tra chắc chắn", "phải cập nhật phiên bản chủ động, có việc bảo trì"],
                  ["chỉ ghim phiên bản", "cùng thư viện, nhưng gói vẫn có thể khác bit do mốc thời gian", "so sánh bằng mã băm sẽ lệch"],
                  ["để mặc định", "không phải làm gì", "bản phụ thuộc có thể đổi giữa hai lần dựng: không dựng lại được"]]),
           """Đáp án câu ba, ghim phiên bản cùng mốc cố định cho dựng lại ra đúng mã băm, đổi lại phải cập nhật chủ động. Chỉ ghim phiên bản thì gói vẫn có thể khác bit, để mặc định thì bản phụ thuộc đổi giữa hai lần dựng."""),
    ], checks=["alg.bnx_l26_maven([('P', '1.0'), ('Q', '1.0')], {('P', '1.0'): [('Z', '2.0')], ('Q', '1.0'): [('Z', '3.0')]})['Z'] == '2.0'",
               "alg.bnx_l26_gradle([('P', '1.0'), ('Q', '1.0')], {('P', '1.0'): [('Z', '2.0')], ('Q', '1.0'): [('Z', '3.0')]})['Z'] == '3.0'",
               "alg.bnx_l26_agents(120, 15) == 30 and alg.bnx_l26_agents(120, 5) == 10"])

    lab_pr = practice_scene(sc, "Tự làm: phân giải phiên bản theo hai luật", practice_steps(
        st, "BNX", "L26",
        """<p><b>Đề (MÔ PHỎNG, không chạy Maven hay Gradle)</b>: dự án khai <code>A 1.0</code>, <code>B 1.0</code>. <code>A 1.0</code> cần <code>X 1.0</code>, <code>Y 2.0</code>; <code>B 1.0</code> cần <code>Y 3.0</code>, <code>Z 1.0</code>; <code>Z 1.0</code> cần <code>X 2.0</code>.</p>
<p>Viết <code>mau.py</code> in 5 dòng <code>maven &lt;tên&gt; &lt;bản&gt;</code> (A, B, X, Y, Z) rồi 3 dòng <code>gradle &lt;tên&gt; &lt;bản&gt;</code> (X, Y, Z). Maven: gần nhất, cùng độ sâu thì khai trước thắng. Gradle: cao nhất.</p>
<p>Duyệt theo hàng đợi. Số liệu khác ví dụ trong bài; chi tiết trong <code>de.md</code>.</p>""",
        """Đến phần bạn tự làm, một mô phỏng không chạy công cụ thật: dự án khai hai thư viện, các thư viện cần nhau theo đồ thị nhỏ trong đề. Viết chương trình Python in kết quả theo hai luật, gần nhất thắng rồi bản cao nhất. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> dùng hàng đợi; tên đã chọn thì bỏ yêu cầu sau, chưa thì chọn và thêm các thư viện nó cần vào cuối hàng. Luật cao nhất: chọn lại khi bản mới cao hơn.
Lời giải đầy đủ ở <code>labs/BNX/L26/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, dùng một hàng đợi: tên đã chọn thì bỏ, chưa thì chọn và thêm thư viện nó cần vào cuối hàng. Với luật cao nhất, chọn lại khi bản mới cao hơn. Lời giải chỉ mở sau khi đã tự thử.""", pause=150), "BNX", "L26")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("tệp mô tả dự án", "vòng đời: các pha nối tiếp", "bắc cầu → xung đột", "gần nhất thắng / cao nhất thắng", "ghim + mốc thời gian → tái lập"),
           """Công cụ chạy các pha nối tiếp theo tệp mô tả dự án. Phụ thuộc bắc cầu gây xung đột phiên bản, mỗi công cụ một luật chọn. Muốn dựng tái lập thì ghim phiên bản, đặt mốc cố định và so mã băm."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng đoán bản đang chạy, hãy <b>in cây phụ thuộc</b>. Mỗi thư viện thêm vào là thêm cả chùm bắc cầu và thêm chỗ xung đột.
Dựng là việc phải <b>lặp lại được</b>: ghim, cố định, rồi chứng minh bằng mã băm.</div>""",
           """Đừng đoán bản đang chạy, hãy in cây phụ thuộc, vì mỗi thư viện thêm vào là thêm cả một chùm bắc cầu và chỗ xung đột. Dựng phải lặp lại được: ghim, cố định mốc rồi chứng minh bằng mã băm."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Maven, Gradle: vòng đời và xung đột phiên bản?", "các pha nối tiếp tới pha được gọi; bắc cầu kéo cả chùm; Maven gần nhất thắng (khai trước thắng nếu cùng độ sâu), Gradle mặc định cao nhất; xem bằng dependency:tree"],
                  ["Jenkins: pipeline khai báo gồm gì?", "pipeline → agent, stages → stage → steps, post; Jenkinsfile lưu cùng mã nguồn để duyệt và có lịch sử; khi một giai đoạn hỏng thì các giai đoạn sau không chạy, post failure chạy"],
                  ["Dựng tái lập là gì, làm sao chứng minh?", "cùng mã, môi trường, lệnh thì ra tệp giống từng bit; đặt outputTimestamp, ghim phiên bản, dựng hai lần rồi so sha256"]]),
           """Người phỏng vấn thường hỏi ba câu về dòng này trên hồ sơ: vòng đời và xung đột phiên bản, đường ống khai báo gồm gì, và dựng tái lập, câu trả lời ngắn nằm sẵn trên bảng.""", clear=True),
        st("""<p>Bài sau: <b>tích hợp hệ cũ</b> bằng phong bì XML và truyền tệp lô an toàn, kèm kiểm toàn vẹn.</p>""",
           """Ở bài hai mươi bảy, ta tìm hiểu tích hợp hệ thống cũ bằng phong bì XML và truyền tệp lô an toàn, kèm kiểm toàn vẹn.""",
           forward_ref=True),
    ], checks=["alg.bnx_l26_agents(4, 10) == 1"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L26", "maven_gradle_jenkins",
                  "Bài 26 — Maven, Gradle và Jenkins: vòng đời, xung đột phiên bản và dựng tái lập",
                  "curriculum/bnx.yaml L26; audit/bnx/verify_bnx.py L26; audit/bnx/sources_l26.md: hướng dẫn Maven (Lifecycle, Dependency Mechanism, Reproducible Builds), "
                  "hướng dẫn chính thức Gradle (Dependency Resolution, Java plugin), hướng dẫn chính thức Jenkins (Pipeline Syntax, Jenkinsfile; đọc 2026-11-13); Maven 3.9.11 chạy thật trên Temurin JDK 21.0.13; "
                  "Gradle và Jenkins không chạy (chỉ kiểm cú pháp Groovy 4.0.27 và mô phỏng nhỏ)",
                  ["Đọc vòng đời dựng mặc định của Maven qua các mục tiêu của phần mở rộng in ra khi chạy mvn package",
                   "Đọc cây phụ thuộc bắc cầu của một pom.xml bằng dependency:tree và nhận ra dòng bị bỏ vì xung đột",
                   "Xác định phiên bản được chọn theo luật gần nhất thắng của Maven",
                   "Đọc một Jenkinsfile khai báo và nói thứ tự giai đoạn cùng nhánh post khi một giai đoạn hỏng",
                   "Chứng minh dựng tái lập bằng cách dựng hai lần và so sha256 của jar",
                   "Đọc số gói thư viện đo thật ở ba dự án thử và tính số máy dựng tối thiểu khi lượt dựng gấp 100 và 10 000 lần",
                   "Viết bộ phân giải phiên bản theo luật gần nhất thắng của Maven và theo luật cao nhất của Gradle"],
                  scenes,
                  covers=[(1, "example"), (2, "example"), (3, "check"), (4, "example"), (5, "example"), (6, "quymo"), (7, "practice")])
