import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from labkit import write_lab, practice_steps, practice_scene
from libj import jstep, nowrap

lib2.begin("L31")

# ── Mã chạy THẬT: Python 3 (nhật ký, chỉ mục đảo), JDK 21 (mã xuất chỉ số), ảnh Docker chính thức của Prometheus 3.16.0 (ghim băm, `docker run --rm`,
#    mỗi lần một container, tự gỡ). Đầu ra tất định (đồng hồ giả, đếm dòng, đếm byte, số liệu tĩnh) — đệm ở audit/bnx/progcache/L31.json.
#    KHÔNG chạy: Elasticsearch/Logstash/Kibana, Grafana (bài nói rõ "mô phỏng" ở phần chỉ mục đảo; Grafana chỉ giảng khái niệm). ──
PROM_IMG = "prom/prometheus@sha256:e04987641b57704f408e31f6373ba4138ecf27cb4a165d24aabb6c38fddd0f06"

P_LOG = prog("NhatKy", r'''
import json
gio = iter(range(1000, 2000, 7))              # dong ho gia, mili giay
nhat_ky = []
def ghi(dv, cid, ev, **them):
    nhat_ky.append({"t": next(gio), "dv": dv, "cid": cid, "ev": ev, **them})
ghi("cong", "a1", "nhan", duong="/chuyen")
ghi("cong", "b2", "nhan", duong="/so-du")
ghi("tt", "a1", "tru-tien", tien=500)
ghi("tt", "b2", "doc-so-du")
ghi("sc", "a1", "loi", ma="HET_GIO")
ghi("cong", "a1", "tra", http=504)
for d in nhat_ky:
    print(json.dumps(d, separators=(",", ":")))
a1 = [d for d in nhat_ky if d["cid"] == "a1"]
print("a1:", " > ".join(d["dv"] + ":" + d["ev"] for d in a1))
print("a1 mat", a1[-1]["t"] - a1[0]["t"], "ms")
''', lang="python", claims=["nhật ký JSON mỗi dòng một sự kiện; lọc theo mã tương quan a1 dựng lại đường đi cong > tt > sc > cong và mất 35 ms"])

P_IDX = prog("ChiMuc", r'''
DV = ["cong", "tt", "sc", "kh", "tb"]
for n in (1000, 1000000):
    dong = [(DV[i % 5], "ERROR" if i % 1000 in (7, 8) else "INFO")
            for i in range(n)]
    chi_muc = {}
    for i, (dv, muc) in enumerate(dong):
        chi_muc.setdefault(muc, []).append(i)
        chi_muc.setdefault(dv, []).append(i)
    a, b = chi_muc["ERROR"], set(chi_muc["sc"])
    khop = [i for i in a if i in b]
    print(n, "dong: khop", len(khop), "| quet", n, "dong |",
          "chi muc xet", len(a), "dong")
''', lang="python", timeout=180, claims=["chỉ mục đảo: 1 000 dòng xét 2 dòng, 1 000 000 dòng xét 2 000 dòng (khớp 1 và 1 000); quét hết phải đọc cả 1 000 và 1 000 000 dòng"])

J_XUAT = prog("XuatChiSo", r'''
public class XuatChiSo {
  public static void main(String[] a) {
    int nguoi = Integer.parseInt(a[0]);       // 0 = khong gan nhan user
    String[] duong = {"/chuyen", "/so-du"};
    String[] ma = {"200", "500"};
    int[][] so = {{980, 20}, {4990, 10}};
    StringBuilder s = new StringBuilder();
    s.append("# HELP http_requests_total So yeu cau da nhan.\n");
    s.append("# TYPE http_requests_total counter\n");
    for (int d = 0; d < 2; d++)
      for (int c = 0; c < 2; c++) {
        String nhan = "route=\"" + duong[d] + "\",code=\"" + ma[c] + "\"";
        if (nguoi == 0)
          s.append("http_requests_total{" + nhan + "} " + so[d][c] + "\n");
        else
          for (int u = 1; u <= nguoi; u++)
            s.append("http_requests_total{" + nhan + ",user=\"u" + u + "\"} 1\n");
      }
    s.append("# TYPE dang_xu_ly gauge\ndang_xu_ly 3\n");
    System.out.print(s);
  }
}
''', lang="java", kind="other", reason="XuatChiSo.java: in văn bản chỉ số theo định dạng văn bản của Prometheus (bộ đếm có nhãn route, code; tuỳ chọn thêm nhãn user).",
    read_check="Chạy bằng `java XuatChiSo.java` trong nguồn L31_ChayMay và L31_DemChuoi; đầu ra khớp từng dòng.")

SH_TEST = prog("ChayTest", r'''
IMG=''' + PROM_IMG + r'''
command -v docker >/dev/null || { echo "NOT_VERIFIED: thieu docker" >&2; exit 97; }
docker image inspect $IMG >/dev/null 2>&1 || docker pull -q $IMG >/dev/null 2>&1 || { echo "NOT_VERIFIED: khong co anh Prometheus" >&2; exit 97; }
cat > rules.yml <<'EOF'
groups:
- name: bnx
  rules:
  - alert: NganSachChayNhanh
    expr: |
      sum(rate(http_requests_total{code=~"5.."}[5m]))
        / sum(rate(http_requests_total[5m])) / 0.001 > 2
    for: 2m
    labels: {severity: page}
EOF
cat > test.yml <<'EOF'
rule_files: [rules.yml]
evaluation_interval: 1m
tests:
- interval: 1m
  input_series:
  - series: 'http_requests_total{code="200"}'
    values: '0+995x12'
  - series: 'http_requests_total{code="500"}'
    values: '0+5x12'
  promql_expr_test:
  - expr: |
      sum(rate(http_requests_total{code=~"5.."}[5m]))
        / sum(rate(http_requests_total[5m])) / 0.001
    eval_time: 10m
    exp_samples:
    - value: 5
  alert_rule_test:
  - {eval_time: 2m, alertname: NganSachChayNhanh, exp_alerts: []}
  - eval_time: 4m
    alertname: NganSachChayNhanh
    exp_alerts:
    - exp_labels: {severity: page}
- interval: 1m
  input_series:
  - series: 'http_requests_total{code="200"}'
    values: '0+999x12'
  - series: 'http_requests_total{code="500"}'
    values: '0+1x12'
  alert_rule_test:
  - {eval_time: 10m, alertname: NganSachChayNhanh, exp_alerts: []}
EOF
tar cf - rules.yml test.yml | docker run --rm -i --entrypoint sh $IMG \
  -c 'cd /tmp && tar x && promtool test rules test.yml'
''', lang="bash", timeout=300,
    claims=["promtool (Prometheus 3.16.0) kiểm luật: tốc độ đốt ngân sách lỗi 5 ở phút 10; cảnh báo chưa bắn ở phút 2 (for 2m), bắn ở phút 4; chuỗi lỗi 0,1% không bắn"])

_TL = SH_TEST.code.split(chr(10))
_I2 = [k for k, l in enumerate(_TL) if l.startswith("- interval")][1] + 1   # dòng đầu của ca kiểm thứ hai trong test.yml

SH_MAY = prog("ChayMay", r'''
IMG=''' + PROM_IMG + r'''
command -v docker >/dev/null || { echo "NOT_VERIFIED: thieu docker" >&2; exit 97; }
docker image inspect $IMG >/dev/null 2>&1 || docker pull -q $IMG >/dev/null 2>&1 || { echo "NOT_VERIFIED: khong co anh Prometheus" >&2; exit 97; }
java XuatChiSo.java 0 > metrics
cat metrics
cat > prom.yml <<'EOF'
global: {scrape_interval: 1s}
scrape_configs:
- job_name: bnx
  fallback_scrape_protocol: PrometheusText0.0.4
  static_configs: [{targets: ['localhost:9100']}]
EOF
cat > in.sh <<'EOF'
mkdir -p www && cp metrics www/
busybox httpd -p 9100 -h www
prometheus --config.file=prom.yml --storage.tsdb.path=d >/dev/null 2>&1 &
q() {
  wget -qO- --post-data "query=$1" \
    http://localhost:9090/api/v1/query 2>/dev/null |
  sed 's/.*"value":\[[0-9.]*,"\([^"]*\)"\].*/\1/'
}
for i in $(seq 1 60); do [ "$(q up)" = 1 ] && break; sleep 1; done
echo "up = $(q up)"
L='sum(http_requests_total{code="500"})'
echo "loi 500 = $(q "$L")"
echo "ty le loi = $(q "$L/sum(http_requests_total)")"
EOF
tar cf - metrics prom.yml in.sh | docker run --rm -i --entrypoint sh $IMG \
  -c 'cd /tmp && tar x && sh in.sh'
''', lang="bash", files={"XuatChiSo.java": "XuatChiSo"}, timeout=300,
    claims=["Prometheus 3.16.0 thật kéo văn bản chỉ số: up = 1; tổng lỗi 500 là 30; tỉ lệ lỗi 0,005"])

SH_DEM = prog("DemChuoi", r'''
for n in 0 100 10000; do
  java XuatChiSo.java $n > m$n
  echo "$n gia tri nhan user: $(grep -vc '^#' m$n) chuoi, $(wc -c < m$n) byte"
done
''', lang="bash", files={"XuatChiSo.java": "XuatChiSo"}, timeout=200,
    claims=["một lần kéo số liệu: 5 chuỗi 324 byte; thêm nhãn user 100 giá trị: 401 chuỗi 24 287 byte; 10 000 giá trị: 40 001 chuỗi 2 495 695 byte"])

# ── Lab (cham.sh, Python): dựng đường đi, đếm lỗi, tốc độ đốt ──
LAB_PY = r'''
import json
NK = [
    '{"t":500,"dv":"gw","cid":"c9","ev":"nhan"}',
    '{"t":505,"dv":"gw","cid":"d4","ev":"nhan"}',
    '{"t":520,"dv":"pay","cid":"c9","ev":"tru"}',
    '{"t":526,"dv":"pay","cid":"d4","ev":"loi"}',
    '{"t":560,"dv":"gw","cid":"c9","ev":"tra"}',
    '{"t":545,"dv":"led","cid":"c9","ev":"ghi"}',
]
SU_KIEN = [json.loads(d) for d in NK]
c9 = sorted((d for d in SU_KIEN if d["cid"] == "c9"), key=lambda d: d["t"])
print("c9:", " > ".join(d["dv"] + ":" + d["ev"] for d in c9))
print("c9 mat", c9[-1]["t"] - c9[0]["t"], "ms")
loi = sum(1 for d in SU_KIEN if d["ev"] == "loi")
print("so dong loi:", loi)
YEU_CAU, YEU_CAU_LOI, SLO = 200, 6, 0.99
print("toc do dot:", round(YEU_CAU_LOI / YEU_CAU / (1 - SLO), 1))
'''
LAB_OUT = """c9: gw:nhan > pay:tru > led:ghi > gw:tra
c9 mat 60 ms
so dong loi: 1
toc do dot: 3.0"""
LAB_DE = """# Lab BNX L31 — Dựng đường đi từ nhật ký và tính tốc độ đốt ngân sách

Dưới đây là sáu dòng nhật ký JSON (số minh hoạ), **theo thứ tự đến kho**, không theo thứ tự thời gian (`t` là mili giây của đồng hồ giả):

```
{"t":500,"dv":"gw","cid":"c9","ev":"nhan"}
{"t":505,"dv":"gw","cid":"d4","ev":"nhan"}
{"t":520,"dv":"pay","cid":"c9","ev":"tru"}
{"t":526,"dv":"pay","cid":"d4","ev":"loi"}
{"t":560,"dv":"gw","cid":"c9","ev":"tra"}
{"t":545,"dv":"led","cid":"c9","ev":"ghi"}
```

Viết `mau.py` (chỉ thư viện chuẩn, dùng `json`):
1. Đọc sáu dòng, lọc những dòng có `cid` là `c9`, **sắp theo `t`**, in `c9: <dv>:<ev> > <dv>:<ev> > …`.
2. In `c9 mat <số> ms` (từ sự kiện đầu tới sự kiện cuối của c9).
3. Đếm số dòng có `ev` là `loi` trong cả sáu dòng, in `so dong loi: <số>`.
4. Mục tiêu độ sẵn sàng (SLO) 99%; trong 200 yêu cầu có 6 yêu cầu lỗi. **Tốc độ đốt** = tỉ lệ lỗi chia ngân sách lỗi (1 − SLO). In `toc do dot: <số>` làm tròn 1 chữ số thập phân.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L31 mau.py`.
"""


def build():
    write_lab("BNX", "L31", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Hai giờ sáng: tìm một yêu cầu trong một triệu dòng nhật ký", [
        st("""<p>Khách báo chuyển tiền bị treo lúc 2 giờ sáng. Yêu cầu đi qua <b>ba lớp</b> (cổng, thanh toán, sổ cái); nhật ký dài <b>1 000 000</b> dòng mỗi ngày (số minh hoạ).</p>
<div class="box key">Tìm bằng cách <b>đọc hết</b>: xem <b>1 000 000</b> dòng. Tìm bằng <b>chỉ mục</b>: chỉ xem <b>2 000</b> dòng có chữ ERROR. Và một <b>mã tương quan</b> nối ba lớp thành một đường đi.
Làm sao có được điều đó, và làm sao biết sự cố trước khi khách gọi?</div>""",
           """Chào bạn, khách báo chuyển tiền bị treo lúc hai giờ sáng. Nhật ký dài một triệu dòng mỗi ngày.
           Đọc hết thì xem một triệu dòng, dùng chỉ mục thì chỉ xem hai nghìn dòng có chữ lỗi. Làm sao có được điều đó, và biết sự cố trước khi khách gọi?"""),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["nhật ký thế nào thì tìm được", "<b>có cấu trúc</b> (mỗi dòng gồm các cặp tên và giá trị) và có <b>mã tương quan</b> (<code>cid</code>)"],
                  ["tìm trong hàng triệu dòng", "<b>chỉ mục đảo</b>: ý tưởng của bộ ba ELK (Elasticsearch, Logstash, Kibana)"],
                  ["biết sức khoẻ hệ thống", "<b>chỉ số</b> có <b>nhãn</b> (Prometheus), vẽ bằng Grafana"],
                  ["biết trước khi khách gọi", "<b>cảnh báo</b> theo ngưỡng và theo <b>ngân sách lỗi</b>"]]),
           """Hôm nay ta trả lời bốn câu. Nhật ký có cấu trúc và mã tương quan, chỉ mục đảo để tìm nhanh.
           Chỉ số có nhãn cho biết sức khoẻ, cảnh báo cho biết trước khi khách gọi.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ], checks=["alg.bnx_l31_index(1000000)[:2] == (1000, 2000)"])

    pre = sc("prereq", "prereq", "Trước hết: sáu điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① nhật ký (log)", "văn bản ghi lại điều đã xảy ra, mỗi sự việc một dòng", "<code>cong nhan /chuyen</code>"],
                  ["② một yêu cầu qua nhiều dịch vụ", "mỗi dịch vụ ghi nhật ký riêng, trên máy riêng", "cổng → thanh toán → sổ cái"],
                  ["③ chỉ số (metric)", "con số đo theo thời gian: đếm, đo mức", "số yêu cầu lỗi: 30"],
                  ["④ nhãn (label)", "cặp tên=giá trị gắn vào chỉ số để chia nhóm", "<code>code=&quot;500&quot;</code>"],
                  ["⑤ bộ đếm chỉ tăng", "số chỉ tăng; <b>tốc độ</b> = phần tăng chia thời gian", "+995 mỗi phút ≈ 16,6/giây"],
                  ["⑥ ngưỡng", "mức mà vượt qua thì người trực được báo", "tỉ lệ lỗi &gt; 5%"]]),
           """Trước hết ta cần hiểu sáu điều. Nhật ký ghi điều đã xảy ra, mỗi sự việc một dòng.
           Một yêu cầu đi qua nhiều dịch vụ, mỗi dịch vụ ghi nhật ký riêng. Chỉ số là con số đo theo thời gian.
           Nhãn là cặp tên và giá trị gắn vào chỉ số. Bộ đếm chỉ tăng, và tốc độ là phần tăng chia cho thời gian.
           Ngưỡng là mức vượt qua thì người trực được báo.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["round(995 / 60, 1) == 16.6"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>cid</code>", "mã tương quan: cùng một giá trị trên mọi dòng nhật ký của một yêu cầu"],
                  ["ELK", "Elasticsearch (lưu, lập chỉ mục) + Logstash (thu thập) + Kibana (xem); Elastic Stack còn có Beats"],
                  ["<code>http_requests_total{code=&quot;500&quot;}</code>", "tên chỉ số, rồi nhãn trong ngoặc nhọn: các yêu cầu mã 500"],
                  ["<code>rate(x[5m])</code>", "tốc độ tăng mỗi giây của <code>x</code> trên cửa sổ 5 phút; viết bằng <b>PromQL</b>, ngôn ngữ truy vấn của Prometheus"],
                  ["<code>sum(…)</code>", "cộng các chuỗi lại thành một số"],
                  ["<code>for: 2m</code>", "điều kiện phải đúng liên tục 2 phút thì cảnh báo mới bắn"]]),
           """Mã tương quan là cùng một giá trị trên mọi dòng của một yêu cầu. Bộ ba nhật ký gồm nơi lưu và lập chỉ mục, công cụ thu thập và giao diện xem.
           Tên chỉ số theo sau là các nhãn. Hàm tốc độ cho số tăng mỗi giây trên cửa sổ năm phút. Hàm tổng cộng các chuỗi lại, và điều kiện đúng liên tục hai phút thì cảnh báo mới bắn.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ], checks=["alg.bnx_l31_ratio(30, 6000) == 0.005"])

    intu = sc("intuition", "intuition", "Hình dung: đường đi của nhật ký và của chỉ số", [
        st(svg(1500, 500,
               txt(750, 40, "Nhật ký: dịch vụ ghi dòng có cấu trúc, công cụ thu thập gom về, chỉ mục đảo giúp tìm nhanh", 26, "middle", "#1f2937", True),
               box(40, 110, 300, 60, "cổng (cid=a1)", C_BLUE, 24, True), box(40, 200, 300, 60, "thanh toán (cid=a1)", C_BLUE, 24, True), box(40, 290, 300, 60, "sổ cái (cid=a1)", C_BLUE, 24, True),
               box(460, 160, 280, 120, ["thu thập", "Logstash, Beats", "gom dòng về"], C_AMBER, 22, True),
               box(830, 160, 300, 120, ["lập chỉ mục", "Elasticsearch", "từ → danh sách dòng"], C_GREEN, 22, True),
               box(1220, 160, 240, 120, ["xem, tìm", "Kibana"], C_PURPLE, 22, True),
               arrow(345, 140, 455, 200, "#475569"), arrow(345, 230, 455, 225, "#475569"), arrow(345, 320, 455, 250, "#475569"),
               arrow(745, 220, 825, 220, "#475569"), arrow(1135, 220, 1215, 220, "#475569"),
               box(40, 400, 1420, 70, "Bài này MÔ PHỎNG phần lập chỉ mục bằng Python: không chạy Elasticsearch, Logstash hay Kibana trên máy", C_GRAY, 22)),
           """Đây là đường đi của nhật ký: ba dịch vụ ghi dòng có chung mã tương quan, công cụ thu thập gom về một nơi, và nơi lưu lập chỉ mục. Bài này mô phỏng phần lập chỉ mục bằng Python, không chạy bộ ba công cụ."""),
        st(svg(1500, 500,
               txt(750, 40, "Chỉ số: Prometheus kéo văn bản về, lưu theo thời gian, hỏi bằng PromQL, vẽ và cảnh báo", 26, "middle", "#1f2937", True),
               box(40, 160, 320, 120, ["ứng dụng", "/metrics: văn bản", "tên{nhãn} giá trị"], C_BLUE, 22, True),
               box(450, 160, 320, 120, ["Prometheus", "kéo (scrape) mỗi N giây", "lưu chuỗi theo thời gian"], C_GREEN, 22, True),
               box(880, 90, 280, 90, ["PromQL", "rate, sum, tỉ lệ"], C_AMBER, 22, True),
               box(1250, 90, 210, 90, ["Grafana", "vẽ biểu đồ"], C_PURPLE, 22, True),
               box(880, 250, 280, 90, ["luật cảnh báo", "ngưỡng + for"], C_RED, 22, True),
               box(1250, 250, 210, 90, ["người trực", "được báo"], C_GRAY, 22, True),
               arrow(455, 190, 365, 190, "#475569", "kéo", 20), arrow(775, 200, 875, 150, "#475569"), arrow(1165, 135, 1245, 135, "#475569"),
               arrow(775, 245, 875, 285, "#475569"), arrow(1165, 295, 1245, 295, "#475569"),
               box(40, 400, 1420, 70, "Chạy thật trong bài: Prometheus 3.16.0 (ảnh Docker chính thức). Grafana: chỉ giảng, không chạy trên máy", C_GRAY, 22)),
           """Hình thứ hai là đường đi của chỉ số: ứng dụng phơi ra một trang văn bản, hệ thu thập kéo trang ấy mỗi vài giây rồi lưu theo thời gian. Luật cảnh báo chạy truy vấn trên chuỗi ấy, vượt ngưỡng đủ lâu thì báo người trực. Hệ thu thập chạy thật từ một ảnh Docker."""),
    ], checks=["alg.bnx_l31_index(1000)[:2] == (1, 2)"])

    form = sc("formula", "formula", "Suy ra từng bước: từ dòng nhật ký tới cảnh báo", [
        st("""<p><b>Bước 1. Nhật ký có cấu trúc.</b> Dòng văn bản tự do <code>ERROR so-cai het gio giao dich a1</code> muốn lọc phải đoán bằng <b>biểu thức chính quy</b>, tức một mẫu chữ như &laquo;chữ ERROR rồi tên dịch vụ&raquo;. Mỗi dòng là một <b>đối tượng JSON</b>, tức các cặp <code>"tên":giá trị</code> trong ngoặc nhọn, thì máy lọc theo trường, không đoán.</p>
<div class="box key"><code>{"t":1028,"dv":"sc","cid":"a1","ev":"loi","ma":"HET_GIO"}</code></div>""",
           """Bước một là nhật ký có cấu trúc. Dòng văn bản tự do muốn lọc phải đoán bằng biểu thức chính quy, tức một mẫu chữ. Đối tượng JSON là các cặp tên và giá trị trong ngoặc nhọn, nên máy lọc thẳng theo trường.""", clear=True, introduces=["bnx_bieu_thuc_chinh_quy"]),
        st(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                 [["<code>def ghi(dv, cid, ev, **them):</code>", "<code>**them</code> gom mọi đối số có tên còn lại vào một từ điển tên <code>them</code>", "<code>ghi(\"tt\", \"a1\", \"tru-tien\", tien=500)</code> cho <code>them = {\"tien\": 500}</code>"],
                  ["<code>{\"t\": …, \"ev\": ev, **them}</code>", "dấu <code>**</code> trong ngoặc nhọn trải từ điển <code>them</code> thành từng cặp tên và giá trị", "<code>{\"ev\": \"tru-tien\", \"tien\": 500}</code>"],
                  ["<code>gio = iter(range(1000, 2000, 7))</code>, <code>next(gio)</code>", "<code>range(1000, 2000, 7)</code>: dãy 1000, 1007, 1014, … (bước 7); <code>iter</code> cho lấy từng giá trị; <code>next(gio)</code> lấy giá trị kế tiếp", "1000, rồi 1007, rồi 1014"],
                  ["<code>nhat_ky = []</code>, <code>nhat_ky.append({…})</code>", "danh sách rỗng; <code>append</code> thêm một phần tử vào cuối", "sau 6 lệnh ghi có 6 phần tử"]]),
           """Trước khi đọc hàm ghi, nên ta xem cách viết. Hai dấu sao gom các đối số có tên còn lại vào một từ điển, và trong ngoặc nhọn thì trải nó ra. Giờ giả đếm từ một nghìn, bước bảy, mỗi lần lấy giá trị kế tiếp.""", clear=True),
        st("""<p><b>Bước 2. Mã tương quan.</b> Cổng đặt <code>cid</code> cho mỗi yêu cầu; mọi dịch vụ chép nó vào <b>mọi</b> dòng. Lọc theo <code>cid</code> là gom lại đường đi.</p>"""
           + P_LOG.show_from("def ghi", 5, title="NhatKy.py (trích): mọi dòng mang cid")
           + """$$\\text{lọc } cid = a1 \\Rightarrow \\text{cong} \\to \\text{tt} \\to \\text{sc} \\to \\text{cong}$$""",
           """Bước hai là mã tương quan. Cổng đặt một mã cho mỗi yêu cầu, và mọi dịch vụ chép mã ấy vào mọi dòng, nên lọc theo mã là gom lại đúng đường đi.""", clear=True),
        jstep([(("<code>[(DV[i % 5], \"ERROR\" if i % 1000 in (7, 8) else \"INFO\") for i in range(n)]</code>", "danh sách sinh sẵn: với <code>i</code> từ 0 tới n−1 tạo một cặp (dịch vụ, mức); <code>i % 5</code> là phần dư; mức là ERROR khi <code>i % 1000</code> là 7 hoặc 8, không thì INFO", "Tạo cặp dịch vụ và mức cho mỗi dòng; mức lỗi khi chỉ số dư bảy hoặc tám."), "", ""),
               (("<code>for i, (dv, muc) in enumerate(dong):</code>", "duyệt kèm số thứ tự <code>i</code> và tách cặp thành <code>dv</code>, <code>muc</code>", "Duyệt kèm số thứ tự, tách cặp thành hai biến."), "", ""),
               (("<code>chi_muc.setdefault(muc, []).append(i)</code>", "từ điển: khoá <code>muc</code> chưa có thì đặt danh sách rỗng; rồi thêm <code>i</code> vào danh sách của khoá", "Khoá chưa có thì đặt danh sách rỗng, rồi thêm số dòng."), "", ""),
               (("<code>set(chi_muc[\"sc\"])</code>, <code>[i for i in a if i in b]</code>", "<code>set</code>: tập hợp, tra có hay không rất nhanh; câu sau giữ các <code>i</code> của <code>a</code> cũng nằm trong <code>b</code>", "Tập hợp tra nhanh, và lọc các số dòng nằm ở cả hai nơi."), "", "")],
              intro="Bốn chỗ này nên đọc trước."),
        st("""<p><b>Bước 3. Chỉ mục đảo.</b> Thay vì đọc từng dòng, ta lập sẵn bảng <b>từ → danh sách số dòng</b>. Tìm ERROR là tra một mục của bảng, không quét cả nhật ký.</p>"""
           + P_IDX.show(lines=(1, 10), title="ChiMuc.py (phần 1): dựng chỉ mục rồi tra ERROR"),
           """Bước ba là chỉ mục đảo. Thay vì đọc từng dòng, ta lập sẵn bảng từ trỏ tới danh sách số dòng chứa từ ấy, nên tìm chữ lỗi chỉ là tra một mục.""", clear=True),
        jstep([(("<code>int nguoi = Integer.parseInt(a[0]);</code>", "<code>a[0]</code> là chuỗi gõ kèm đầu tiên; <code>parseInt</code> đổi chuỗi thành số nguyên", "Đổi chuỗi gõ kèm đầu tiên thành số nguyên."), "", ""),
               (("<code>String[] duong = {…};</code>, <code>int[][] so = {{980, 20}, {4990, 10}};</code>", "mảng chuỗi; mảng hai chiều: <code>so[d][c]</code> là hàng d, cột c", "Mảng chuỗi, và mảng hai chiều chọn ô bằng hai chỉ số."), "", ""),
               (("<code>StringBuilder s = new StringBuilder();</code>, <code>s.append(\"…\\n\");</code>", "bộ dựng chuỗi: <code>append</code> nối thêm vào cuối; <code>\\n</code> là xuống dòng", "Bộ dựng chuỗi nối thêm vào cuối; gạch ngược rồi chữ n là xuống dòng."), "", "")],
              intro="Ba chỗ này nên đọc trước."),
        st("""<p><b>Bước 4. Chỉ số = tên + nhãn + giá trị.</b> Ứng dụng phơi ra một trang văn bản; ở đây một chương trình Java nhỏ in trang ấy (tham số: số giá trị của nhãn <code>user</code>).</p>"""
           + J_XUAT.show(lines=(1, 10), title="XuatChiSo.java (1/2): chuẩn bị số liệu và dòng chú thích"),
           """Bước bốn là chỉ số gồm tên, nhãn và giá trị. Ứng dụng phơi ra một trang văn bản, nên chương trình Java nhỏ này in trang ấy; số đầu vào là số giá trị của nhãn người dùng.""", clear=True),
        jstep([(("<code>for (int d = 0; d &lt; 2; d++) for (int c = 0; c &lt; 2; c++) { … }</code>", "hai vòng đếm lồng nhau: mỗi tổ hợp (d, c) là một lần chạy thân", "Hai vòng đếm lồng nhau, nên mỗi tổ hợp là một lần chạy."), "", ""),
               (("<code>\"route=\\\"\" + duong[d] + \"\\\",code=\\\"\" + ma[c] + \"\\\"\"</code>", "<code>\\\"</code> trong chuỗi là một dấu nháy kép thật; <code>+</code> nối các phần thành <code>route=\"/chuyen\",code=\"200\"</code>", "Gạch ngược trước nháy đặt nháy thật vào chuỗi; dấu cộng nối các phần."), "", ""),
               (("<code>if (nguoi == 0) … else for (int u = 1; u &lt;= nguoi; u++)</code>", "<code>==</code> so sánh bằng; <code>nguoi</code> bằng 0 thì in một dòng, không thì lặp <code>u</code> từ 1 tới <code>nguoi</code>, mỗi lần một dòng nhãn user", "Hai dấu bằng so sánh; không người dùng thì một dòng, có thì lặp từng người."), "", "")]),
        st("""<p><b>Bước 4 (tiếp).</b> Mỗi tổ hợp nhãn là một <b>chuỗi</b> riêng, in thành một dòng.</p>"""
           + J_XUAT.show(lines=(11, 22), title="XuatChiSo.java (2/2): mỗi tổ hợp nhãn một dòng"),
           """Hai đường dẫn nhân hai mã trả lời cho bốn tổ hợp nhãn, nên có bốn dòng.""", clear=True),
        st("""<p><b>Bước 4 (kết quả).</b> Bộ đếm chỉ tăng; số đang xử lý lên xuống.</p>"""
           + SH_MAY.out_html("""# HELP http_requests_total So yeu cau da nhan.
# TYPE http_requests_total counter
http_requests_total{route="/chuyen",code="200"} 980
http_requests_total{route="/chuyen",code="500"} 20
http_requests_total{route="/so-du",code="200"} 4990
http_requests_total{route="/so-du",code="500"} 10
# TYPE dang_xu_ly gauge
dang_xu_ly 3""", "Văn bản chỉ số thật do XuatChiSo.java in ra (2 route × 2 mã = 4 chuỗi + 1 chuỗi đo mức)"),
           """Mỗi tổ hợp nhãn là một chuỗi riêng, nên có bốn chuỗi, cộng một chuỗi đo mức. Bộ đếm chỉ tăng, còn số đang xử lý lên xuống nên gọi là đồng hồ đo.""", clear=True),
        st("""<p><b>Bước 5. Truy vấn.</b> Tỉ lệ lỗi = tổng yêu cầu mã 5xx chia tổng yêu cầu; vì bộ đếm chỉ tăng nên dùng <b>tốc độ</b> (<code>rate</code>) để nói về hiện tại.</p>"""
           + """$$\\frac{30}{980 + 20 + 4990 + 10} = \\frac{30}{6000} = \\hl{0{,}005}$$""",
           """Bước năm là truy vấn. Tỉ lệ lỗi là tổng yêu cầu mã năm trăm chia tổng yêu cầu, tức năm phần nghìn. Vì bộ đếm chỉ tăng, nói về hiện tại thì dùng tốc độ trên một cửa sổ.""", clear=True),
        st("""<p><b>Bước 6. Ngân sách lỗi.</b> Mục tiêu 99,9% nghĩa là cho phép lỗi <b>0,1%</b>. <b>Tốc độ đốt</b> = tỉ lệ lỗi hiện tại chia ngân sách; bằng 1 là đốt vừa hết ngân sách cuối kỳ.</p>"""
           + """$$\\text{tốc độ đốt} = \\frac{0{,}005}{1 - 0{,}999} = \\hl{5}; \\qquad \\frac{30 \\text{ ngày}}{5} = \\hlg{6} \\text{ ngày}$$""",
           """Bước sáu là ngân sách lỗi. Mục tiêu chín mươi chín phẩy chín phần trăm nghĩa là cho phép lỗi một phần nghìn. Tốc độ đốt là tỉ lệ lỗi chia ngân sách đó, ở đây là năm nên ngân sách ba mươi ngày cạn sau sáu ngày.""", clear=True),
    ], checks=["alg.bnx_l31_path(alg.bnx_l31_demo(), 'a1') == (['cong:nhan', 'tt:tru-tien', 'sc:loi', 'cong:tra'], 35)", "alg.bnx_l31_ratio(30, 980 + 20 + 4990 + 10) == 0.005",
               "alg.bnx_l31_burn(0.005, 0.999) == 5 and alg.bnx_l31_days(5) == 6"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st(P_LOG.show(lines=(1, 11), title="Chạy thật: NhatKy.py (Python, đồng hồ giả)"),
           """Ta chạy thật bằng Python với đồng hồ giả, nên chạy lại ra đúng kết quả cũ. Sáu lệnh ghi cho hai yêu cầu xen kẽ qua ba dịch vụ.""", clear=True),
        jstep([(("<code>import json</code>, <code>json.dumps(d, separators=(\",\", \":\"))</code>", "nạp thư viện JSON; <code>dumps</code> đổi từ điển <code>d</code> thành một dòng chuỗi JSON; <code>separators</code> bỏ dấu cách thừa", "Đổi từ điển thành một dòng chuỗi JSON gọn."), "", ""),
               (("<code>for d in nhat_ky:</code>", "mỗi vòng <code>d</code> là một sự kiện của danh sách, theo thứ tự", "Mỗi vòng, biến nhận một sự kiện."), "", "")]),
        st(P_LOG.show(lines=(12, 13), title="NhatKy.py (tiếp): in từng dòng JSON")
           + P_LOG.out_html("""{"t":1000,"dv":"cong","cid":"a1","ev":"nhan","duong":"/chuyen"}
{"t":1007,"dv":"cong","cid":"b2","ev":"nhan","duong":"/so-du"}
{"t":1014,"dv":"tt","cid":"a1","ev":"tru-tien","tien":500}
{"t":1021,"dv":"tt","cid":"b2","ev":"doc-so-du"}
{"t":1028,"dv":"sc","cid":"a1","ev":"loi","ma":"HET_GIO"}
{"t":1035,"dv":"cong","cid":"a1","ev":"tra","http":504}""")
           + """$$① \\; \\text{6 dòng, mỗi dòng một đối tượng JSON; hai yêu cầu xen kẽ}$$""",
           """Phép tính thứ nhất: sáu lệnh ghi cho sáu dòng JSON, và hai yêu cầu xen kẽ nên đọc từ trên xuống không thấy câu chuyện nào.""", clear=True),
        jstep([(("<code>a1 = [d for d in nhat_ky if d[\"cid\"] == \"a1\"]</code>", "danh sách sinh sẵn có điều kiện: giữ sự kiện <code>d</code> có <code>cid</code> bằng <code>\"a1\"</code>", "Giữ các sự kiện có mã tương quan bằng a một."), "", ""),
               (("<code>\" &gt; \".join(d[\"dv\"] + \":\" + d[\"ev\"] for d in a1)</code>", "nối các chuỗi <code>dv:ev</code> của từng sự kiện, đặt <code> &gt; </code> ở giữa", "Nối chuỗi từng dòng, đặt mũi tên ở giữa."), "", ""),
               (("<code>a1[-1][\"t\"] - a1[0][\"t\"]</code>", "<code>[-1]</code> là phần tử cuối, <code>[0]</code> là phần tử đầu: giờ cuối trừ giờ đầu", "Phần tử cuối trừ phần tử đầu ra thời gian mất."), "", "")]),
        st(P_LOG.show(lines=(14, 16), title="NhatKy.py (tiếp): lọc theo cid = a1")
           + P_LOG.out_html("""a1: cong:nhan > tt:tru-tien > sc:loi > cong:tra
a1 mat 35 ms""", "Kết quả chạy thật: lọc theo cid = a1")
           + """$$② \\; 1035 - 1000 = \\hlg{35} \\text{ ms}; \\quad \\text{lỗi nằm ở sổ cái: HET\\_GIO}$$""",
           """Phép tính thứ hai là lọc theo mã tương quan, giữ các dòng của yêu cầu a một: cổng, thanh toán, sổ cái, rồi cổng trả lời. Một nghìn không trăm ba mươi lăm trừ một nghìn là ba mươi lăm mili giây, và lỗi nằm ở sổ cái.""", clear=True),
        jstep([(("<code>cat &gt; rules.yml &lt;&lt;'EOF' … EOF</code>", "ghi các dòng giữa hai dòng <code>EOF</code> vào tệp <code>rules.yml</code>; <code>'EOF'</code> có nháy nên máy không thay biến trong đó", "Ghi các dòng giữa hai dòng đánh dấu vào tệp."), "", ""),
               (("<code>groups:</code>, <code>- name:</code>, <code>rules:</code>, <code>- alert:</code>", "YAML: thụt lề là lồng nhau; dòng bắt đầu bằng <code>-</code> là một phần tử; <code>khoá: giá trị</code>", "Thụt lề là lồng nhau, gạch ngang là một phần tử."), "", ""),
               (("<code>expr: |</code>, <code>for: 2m</code>, <code>labels: {severity: page}</code>", "<code>expr</code>: biểu thức truy vấn, <code>|</code> cho viết nhiều dòng; <code>for</code>: đúng liên tục 2 phút; <code>labels</code>: nhãn gắn vào cảnh báo", "Biểu thức nhiều dòng, đúng liên tục hai phút, kèm nhãn."), "", "")]),
        st("""<p><code>code=~"5.."</code>: dấu <code>=~</code> là khớp theo mẫu; <code>5..</code> là chữ số 5 rồi hai ký tự bất kỳ, tức mọi mã từ 500 đến 599.</p>"""
           + SH_TEST.show_from("cat > rules.yml", 11, title="Luật cảnh báo (rules.yml): bắn khi tốc độ đốt lớn hơn 2 liên tục 2 phút"),
           """Phép tính thứ ba là kiểm luật cảnh báo. Dấu bằng ngã so khớp theo mẫu, mẫu năm chấm chấm bắt mọi mã từ năm trăm đến năm trăm chín mươi chín. Tốc độ đốt lớn hơn hai liên tục hai phút thì báo người trực.""", clear=True),
        jstep([(("<code>rule_files: [rules.yml]</code>, <code>evaluation_interval: 1m</code>, <code>tests:</code>", "tệp luật cần thử; chu kỳ tính luật là 1 phút; <code>[…]</code> là danh sách; <code>tests</code> là các ca thử", "Tệp luật cần thử, chu kỳ tính, và các ca thử."), "", ""),
               (("<code>input_series:</code>, <code>- series: '…'</code>", "chuỗi số cho sẵn thay cho dữ liệu thật; mỗi <code>series</code> là một chuỗi kèm nhãn của nó", "Chuỗi số cho sẵn thay dữ liệu thật."), "", ""),
               (("<code>values: '0+995x12'</code>", "bắt đầu 0, cộng 995, lặp 12 lần: 0, 995, 1990, …; mỗi giá trị cách nhau <code>interval: 1m</code>", "Bắt đầu từ không, cộng chín trăm chín mươi lăm, lặp mười hai lần."), "", "")]),
        st(SH_TEST.show_from("cat > test.yml", 10, title="Ca kiểm (test.yml): hai chuỗi đếm có sẵn")
           + """$$③ \\; \\text{mỗi phút: } +995 \\text{ yêu cầu tốt}, +5 \\text{ yêu cầu lỗi}$$""",
           """Hai chuỗi đếm có sẵn mỗi phút thêm chín trăm chín mươi lăm yêu cầu tốt và năm yêu cầu lỗi, nên tỉ lệ lỗi là năm phần nghìn.""", clear=True),
        jstep([(("<code>promql_expr_test:</code>, <code>expr:</code>, <code>eval_time: 10m</code>, <code>exp_samples:</code>", "kiểm giá trị truy vấn: tính <code>expr</code> tại phút 10, mong đợi mẫu <code>exp_samples</code> có giá trị 5", "Tính biểu thức tại phút mười, mong đợi mẫu giá trị năm."), "", "")]),
        st(SH_TEST.show_from("promql_expr_test:", 7, title="test.yml (tiếp): điều ta mong đợi về con số"),
           """Rồi ta khai điều mong đợi. Ở phút mười, tốc độ đốt phải là năm.""", clear=True),
        jstep([(("<code>alert_rule_test:</code>, <code>eval_time</code>, <code>alertname</code>", "kiểm cảnh báo: tại thời điểm <code>eval_time</code>, cảnh báo tên <code>alertname</code> phải ở trạng thái mong đợi", "Kiểm cảnh báo tại một thời điểm, theo tên."), "", ""),
               (("<code>exp_alerts: []</code>, <code>exp_labels: {severity: page}</code>", "<code>exp_alerts</code>: các cảnh báo mong đợi; <code>[]</code> là rỗng, tức chưa bắn; có phần tử kèm <code>exp_labels</code> là đang bắn", "Rỗng là chưa bắn, có phần tử kèm nhãn là đang bắn."), "", "")]),
        st(SH_TEST.show_from("alert_rule_test:", 6, title="test.yml (tiếp): điều ta mong đợi về cảnh báo"),
           """Cảnh báo chưa bắn ở phút hai vì điều kiện chưa đủ hai phút, và phải bắn ở phút bốn kèm nhãn gọi trực.""", clear=True),
        st(SH_TEST.show(lines=(_I2, _I2 + 7), title="test.yml (hết): ca thứ hai, tỉ lệ lỗi 0,1% thì không được bắn"),
           """Ca thứ hai dùng chuỗi lỗi một phần nghìn, nên ở phút mười cảnh báo không được bắn.""", clear=True),
        st(SH_TEST.show(lines=(1, 1), title="Dòng đầu của tập lệnh: biến IMG giữ tên ảnh Docker của Prometheus 3.16.0, ghim đúng một bản")
           + table(["viết trong lệnh", "nghĩa"],
                   [["<code>IMG=prom/prometheus@sha256:…</code> rồi <code>&#36;IMG</code>", "gán tên ảnh vào biến <code>IMG</code>; về sau <code>&#36;IMG</code> là giá trị đó; phần sau dấu <code>@</code> ghim đúng một bản"],
                    ["<code>tar cf - rules.yml test.yml | docker run …</code>", "<code>tar</code> đóng hai tệp thành một gói; <code>|</code> chuyển gói sang lệnh sau"],
                    ["<code>--rm -i --entrypoint sh &#36;IMG -c '…'</code>", "<code>--rm</code>: tự xoá container (bản chạy riêng của ảnh) khi xong; <code>-i</code>: nhận dữ liệu vào; <code>--entrypoint sh</code>: chạy vỏ lệnh; <code>-c</code>: chuỗi lệnh chạy bên trong"]]),
           """Biến đầu dòng giữ tên ảnh Docker, ghim đúng một bản. Lệnh đóng gói gom hai tệp thành một gói, chuyển sang lệnh chạy ảnh và tự xoá khi xong.""", clear=True),
        st(SH_TEST.show_from("tar cf", 2, title="Chạy thật: nạp hai tệp vào ảnh Docker của Prometheus 3.16.0 (biến IMG) rồi chạy công cụ kiểm")
           + SH_TEST.out_html(title="Kết quả chạy thật (promtool 3.16.0)")
           + """$$④ \\; \\frac{5}{995 + 5} : 0{,}001 = \\hlg{5}; \\qquad ⑤ \\; \\frac{30 \\text{ ngày}}{5} = \\hl{6} \\text{ ngày}$$""",
           """Kết quả là thành công, nghĩa là mọi điều mong đợi đều đúng. Phép tính thứ tư, năm phần nghìn chia một phần nghìn là năm. Phép tính thứ năm, ngân sách ba mươi ngày cạn sau sáu ngày.""", clear=True),
    ], checks=["alg.bnx_l31_path(alg.bnx_l31_demo(), 'a1')[1] == 1035 - 1000", "alg.bnx_l31_burn(5 / (995 + 5), 0.999) == 5",
               "alg.bnx_l31_days(alg.bnx_l31_burn(0.005, 0.999)) == 6"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: hệ thu thập chạy thật", [
        jstep([(("<code>global: {scrape_interval: 1s}</code>, <code>scrape_configs:</code>", "chu kỳ kéo chung 1 giây; danh sách các việc kéo", "Chu kỳ kéo chung một giây, rồi danh sách việc kéo."), "", ""),
               (("<code>job_name: bnx</code>, <code>fallback_scrape_protocol: PrometheusText0.0.4</code>", "tên việc kéo; giao thức dự phòng khi trang không báo kiểu: văn bản của Prometheus bản 0.0.4", "Tên việc kéo, và giao thức dự phòng khi trang không báo kiểu."), "", ""),
               (("<code>static_configs: [{targets: ['localhost:9100']}]</code>", "danh sách đích cố định (<code>targets</code>): máy này, cổng 9100", "Danh sách đích cố định nên kéo từ máy này, cổng chín nghìn một trăm."), "", "")]),
        st(SH_MAY.show_from("cat > prom.yml", 7, title="Chạy thật: cấu hình để Prometheus kéo trang chỉ số mỗi 1 giây (prom.yml)"),
           """Ta kiểm bằng đường khác hẳn: chạy hệ thu thập chỉ số thật, cho nó kéo mỗi giây trang văn bản do chương trình Java in ra.""", clear=True),
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>wget -qO- --post-data \"query=&#36;1\" URL</code>", "gửi truy vấn tới địa chỉ URL rồi in trả lời ra màn hình (<code>-q</code>: không in tiến trình; <code>-O-</code>: in ra thay vì lưu tệp); <code>&#36;1</code> là đối số đầu của hàm"],
                  ["<code>| sed 's/.*\"value\":\\[[0-9.]*,\"\\([^\"]*\\)\"\\].*/\\1/'</code>", "<code>s/mẫu/thay/</code> thay phần khớp mẫu; <code>.*</code> khớp mọi ký tự; <code>\\( … \\)</code> bắt phần giá trị; <code>\\1</code> in phần bắt được, nên <code>…\"value\":[1731,\"30\"]…</code> thành <code>30</code>"],
                  ["<code>for i in &#36;(seq 1 60); do … sleep 1; done</code>", "lặp tối đa 60 lần, nghỉ 1 giây mỗi lần, cho tới khi <code>up</code> bằng 1"],
                  ["<code>[ \"&#36;(q up)\" = 1 ] &amp;&amp; break</code>", "nếu <code>q up</code> trả đúng 1 thì thoát vòng lặp ngay"]]),
           """Ta đọc cách viết hàm hỏi. Lệnh tải gửi truy vấn rồi in trả lời, nên lệnh cắt chuỗi chỉ cần giữ giá trị. Vòng lặp thử mỗi giây tối đa sáu mươi lần cho tới khi chỉ số up bằng một.""", clear=True),
        jstep([(("<code>L='sum(http_requests_total{code=\"500\"})'</code>, <code>&#36;(q \"&#36;L\")</code>", "biến <code>L</code> giữ một truy vấn; <code>&#36;(q \"&#36;L\")</code> chạy hàm <code>q</code> với truy vấn đó rồi lấy đầu ra", "Biến giữ truy vấn, hàm q chạy nó và lấy đầu ra."), "", ""),
               (("<code>\"&#36;L/sum(http_requests_total)\"</code>", "ghép truy vấn: tổng lỗi chia tổng yêu cầu là tỉ lệ lỗi", "Tổng lỗi chia tổng yêu cầu nên là tỉ lệ lỗi."), "", "")]),
        st(SH_MAY.show_from("q() {", 10, title="Hỏi hệ thu thập qua giao diện HTTP của nó (trích in.sh)"),
           """Rồi ta hỏi nó ba điều qua giao diện HTTP, vì hàm q trả về giá trị: có kéo được không, tổng lỗi năm trăm, và tỉ lệ lỗi.""", clear=True),
        st(SH_MAY.out_html("""up = 1
loi 500 = 30
ty le loi = 0.005""", "Kết quả chạy thật: Prometheus 3.16.0 kéo trang chỉ số của XuatChiSo.java")
           + table(["con số", "đường thứ nhất", "đường khác"],
                   [["tỉ lệ lỗi", "Prometheus thật: 0.005", "Python: 30 / 6000 = 0.005"],
                    ["tốc độ đốt", "ca kiểm của promtool: 5", "tính tay: 0,005 / 0,001 = 5"]]),
           """Kết quả: up bằng một là kéo thành công, tổng lỗi năm trăm là ba mươi, tỉ lệ lỗi là năm phần nghìn, nên khớp với cách tính bằng Python.""", clear=True),
    ], checks=["alg.bnx_l31_ratio(30, 6000) == 0.005", "alg.bnx_l31_burn(0.005, 0.999) == 5"])

    quymo = sc("quymo", "example", "Khi hệ thống lớn dần: số dòng phải xem và số chuỗi chỉ số", [
        st(P_IDX.out_html("""1000 dong: khop 1 | quet 1000 dong | chi muc xet 2 dong
1000000 dong: khop 1000 | quet 1000000 dong | chi muc xet 2000 dong""", "Chạy thật (Python): quét hết hay dùng chỉ mục")
           + """$$10^3 \\to 10^6 \\;(\\times 1000): \\; \\text{quét } 10^3 \\to 10^6 \\text{ dòng}; \\; \\text{chỉ mục } 2 \\to 2\\,000 \\text{ dòng}$$""",
           """Đây là số đo thật khi nhật ký lớn lên một nghìn lần. Quét hết thì phải đọc một nghìn rồi một triệu dòng. Chỉ mục chỉ xem các dòng có chữ lỗi, từ hai lên hai nghìn, tăng theo số kết quả. Đây là mô phỏng chỉ mục đảo, không phải bộ ba công cụ thật.""", clear=True),
        jstep([(("<code>for n in 0 100 10000; do … done</code>, <code>java XuatChiSo.java &#36;n &gt; m&#36;n</code>", "lặp: <code>n</code> lần lượt là 0, 100, 10000; chạy chương trình với tham số <code>n</code>, ghi đầu ra vào tệp <code>m0</code>, <code>m100</code>, <code>m10000</code>", "Lặp ba cỡ, mỗi lần ghi đầu ra vào một tệp riêng."), "", ""),
               (("<code>&#36;(grep -vc '^#' m&#36;n)</code>, <code>&#36;(wc -c &lt; m&#36;n)</code>", "<code>grep -vc '^#'</code> đếm dòng KHÔNG bắt đầu bằng <code>#</code>, mỗi dòng là một chuỗi; <code>wc -c</code> đếm byte của tệp; <code>&#36;(…)</code> lấy kết quả đưa vào câu in", "Đếm dòng không phải chú thích, đếm byte, rồi đưa vào câu in."), "", "")]),
        st(SH_DEM.show(title="Lệnh đo (bash): chạy chương trình Java ba lần, đếm dòng và byte")
           + SH_DEM.out_html("""0 gia tri nhan user: 5 chuoi, 324 byte
100 gia tri nhan user: 401 chuoi, 24287 byte
10000 gia tri nhan user: 40001 chuoi, 2495695 byte""", "Chạy thật (JDK 21): một lần kéo số liệu khi thêm nhãn user")
           + """$$5 \\to 401 \\to 40\\,001 \\text{ chuỗi}; \\quad 324 \\to 24\\,287 \\to 2\\,495\\,695 \\text{ byte mỗi lần kéo}$$""",
           """Số đo thứ hai là số chuỗi chỉ số, mỗi dòng không phải chú thích là một chuỗi, cùng số byte của cả trang. Với một trăm giá trị nhãn người dùng, năm chuỗi thành bốn trăm linh một và gần hai mươi tư nghìn byte mỗi lần kéo. Với mười nghìn giá trị là bốn mươi nghìn chuỗi và gần hai phẩy năm megabyte.""", clear=True),
        st(table(["cách", "được", "mất", "chọn khi"],
                 [["ghi mọi chi tiết vào nhật ký, chỉ mục hết", "tìm được mọi thứ, kể cả điều chưa nghĩ tới", "dung lượng và chi phí lập chỉ mục tăng theo số dòng", "mới dựng; lưu ngắn ngày"],
                  ["chỉ số ít nhãn + nhật ký lỗi + mã tương quan", "rẻ; cảnh báo nhanh; truy vết khi cần", "không trả lời được câu hỏi chưa đo", "hệ thống đã chạy thật, tải lớn"],
                  ["nhãn theo mã người dùng", "xem từng người", "số chuỗi nhân lên theo số người: nguy cơ quá tải", "gần như không bao giờ: chuyển sang nhật ký"]]),
           """Bảng này là các lựa chọn. Ghi mọi chi tiết thì tìm được mọi thứ, đổi lại chi phí tăng theo số dòng. Chỉ số ít nhãn kèm nhật ký lỗi thì rẻ và báo nhanh, nhưng không trả lời câu hỏi chưa đo. Nhãn theo mã người dùng nhân số chuỗi lên, nên thông tin theo người để ở nhật ký.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l31_index(1000)[:2] == (1, 2) and alg.bnx_l31_index(1000000)[:2] == (1000, 2000)",
               "alg.bnx_l31_exposition(0) == (5, 324) and alg.bnx_l31_exposition(100) == (401, 24287) and alg.bnx_l31_exposition(10000) == (40001, 2495695)"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Ghi nhật ký <b class="red">văn bản tự do</b> và <b class="red">không có mã tương quan</b>. Hai yêu cầu xen kẽ mà không có <code>cid</code> thì không ghép được. Mọi dòng phải có mã, và nên có cấu trúc cố định.</div>
$$6 \\text{ dòng của } 2 \\text{ yêu cầu, không } cid \\Rightarrow \\text{không biết dòng nào của ai}$$""",
           """Lỗi thứ nhất là ghi nhật ký văn bản tự do và không có mã tương quan. Hai yêu cầu xen kẽ thì không có mã nào để ghép các dòng lại.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Đặt nhãn <b class="red">user_id</b> hoặc mã giao dịch vào chỉ số. Nhãn chỉ để nhóm có ít giá trị, biết trước.</div>
$$4 \\times 100 + 1 = \\hl{401}; \\qquad 4 \\times 10\\,000 + 1 = \\hl{40\\,001} \\text{ chuỗi}$$""",
           """Lỗi thứ hai: đặt mã người dùng hay mã giao dịch làm nhãn. Đo thật, một trăm giá trị thành bốn trăm linh một chuỗi, mười nghìn giá trị thành hơn bốn mươi nghìn.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Cảnh báo theo <b class="red">số tuyệt đối</b> (&gt; 50 lỗi mỗi phút). Đêm khuya 10 lỗi mỗi phút có thể là toàn bộ yêu cầu mà không báo; giờ cao điểm 51 lỗi trong 5 000 yêu cầu chỉ là 1% mà reo suốt. Dùng <b>tỉ lệ</b> hoặc tốc độ đốt.</div>
$$\\frac{51}{5\\,000} = \\hl{1\\%}$$""",
           """Lỗi thứ ba: cảnh báo theo số tuyệt đối. Đêm khuya, mười lỗi mỗi phút có thể là toàn bộ yêu cầu mà không ai được báo; giờ cao điểm, năm mươi mốt lỗi trong năm nghìn yêu cầu là một phần trăm. Hãy dùng tỉ lệ hoặc tốc độ đốt.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> <b class="red">Ghi dữ liệu nhạy cảm vào nhật ký</b> (số thẻ, mật khẩu, mã truy cập), và để cảnh báo <b class="red">không có việc để làm</b>. Nhật ký sống lâu và nhiều người đọc; mỗi cảnh báo phải kèm hướng xử lý.</div>
<table class='t'><tr><th>cảnh báo tốt</th><th>cảnh báo kém</th></tr><tr><td>tốc độ đốt &gt; 2 liên tục 2 phút; kèm cách xử lý</td><td>&ldquo;CPU cao&rdquo; không nói làm gì</td></tr></table>""",
           """Lỗi thứ tư: ghi số thẻ hay mật khẩu vào nhật ký sống lâu, và để cảnh báo không kèm việc phải làm.""", clear=True),
    ], checks=["alg.bnx_l31_exposition(100)[0] == 401 and alg.bnx_l31_exposition(10000)[0] == 40001", "round(51 / 5000, 2) == 0.01"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Mục tiêu 99,5% trong 30 ngày (43 200 phút). Ngân sách lỗi là bao nhiêu phút? Tỉ lệ lỗi hiện tại 2%: tốc độ đốt bao nhiêu, ngân sách cạn sau mấy ngày?"],
                  ["2", "Chỉ số có nhãn route (4 giá trị), code (3 giá trị), và một nhãn thêm có 500 giá trị. Có bao nhiêu chuỗi?"],
                  ["3", "Quyết định (số minh hoạ): đội muốn xem từng khách bị lỗi. Chọn: nhãn <code>user_id</code> trên chỉ số (500 000 khách), hay nhật ký có <code>cid</code> + <code>user_id</code>? Vì sao?"]]),
           """Đến lượt bạn, ba câu làm ra giấy. Câu một tính ngân sách lỗi theo phút của mục tiêu chín mươi chín phẩy năm phần trăm, rồi tốc độ đốt và số ngày cạn khi lỗi hai phần trăm.
           Câu hai đếm số chuỗi của ba nhãn.
           Câu ba chọn giữa nhãn mã khách trên chỉ số và nhật ký có mã khách.
           Hãy dừng lại làm rồi xem đáp án.""",
           pause=30),
        st("""<p>Câu 1: ngân sách = 43 200 × 0,5% = 216 phút. Tốc độ đốt = 2% : 0,5% = 4; ngân sách 30 ngày cạn sau 30 : 4 = 7,5 ngày.</p>
$$43\\,200 \\times 0{,}005 = \\hlg{216}; \\quad \\frac{0{,}02}{0{,}005} = \\hl{4}; \\quad \\frac{30}{4} = \\hlg{7{,}5} \\text{ ngày}$$""",
           """Đáp án câu một. Ngân sách là bốn mươi ba nghìn hai trăm nhân năm phần nghìn, bằng hai trăm mười sáu phút. Tốc độ đốt là hai phần trăm chia năm phần nghìn, bằng bốn, nên ngân sách cạn sau ba mươi chia bốn, tức bảy ngày rưỡi."""),
        st("""<p>Câu 2: số chuỗi = tích số giá trị các nhãn.</p>
$$4 \\times 3 \\times 500 = \\hlg{6\\,000} \\text{ chuỗi}$$""",
           """Đáp án câu hai. Số chuỗi là tích số giá trị của các nhãn, bốn nhân ba nhân năm trăm bằng sáu nghìn chuỗi."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["nhãn <code>user_id</code> trên chỉ số", "xem từng khách bằng biểu đồ", "4 × 3 × 500 000 = 6 000 000 chuỗi: Prometheus quá tải"],
                  ["nhật ký có <code>cid</code> + <code>user_id</code>", "tìm một khách qua chỉ mục, rẻ khi cần; dựng đường đi", "mỗi truy vấn phải gõ; không có biểu đồ tổng quan sẵn"]]),
           """Đáp án câu ba. Nhãn mã khách nhân số chuỗi lên sáu triệu, và hệ thu thập quá tải.
           Nhật ký có mã khách cho tìm một khách rẻ hơn, đổi lại không có biểu đồ tổng quan sẵn.""",
           focus=[0, "1.2", "1.3"]),
    ], checks=["alg.bnx_l31_budget_min(0.995) == 216 and alg.bnx_l31_burn(0.02, 0.995) == 4 and alg.bnx_l31_days(4) == 7.5", "4 * 3 * 500 == 6000", "4 * 3 * 500000 == 6000000"])

    lab_pr = practice_scene(sc, "Tự làm: dựng đường đi từ nhật ký và tính tốc độ đốt", practice_steps2(
        st, "BNX", "L31",
        """<p><b>Đề</b>: sáu dòng nhật ký JSON <b>không theo thứ tự thời gian</b>. Lọc <code>cid</code> là <code>c9</code>, sắp theo <code>t</code>, in đường đi và thời gian; đếm dòng <code>loi</code>; tính tốc độ đốt với mục tiêu độ sẵn sàng 99% (tên viết tắt SLO) khi 6/200 yêu cầu lỗi.</p>
<p>Dữ liệu và định dạng đầu ra nằm trong <code>de.md</code>; số liệu <b>khác</b> ví dụ trong bài.</p>""",
        """Tới phần bạn tự làm. Từ sáu dòng nhật ký không theo thứ tự thời gian, lọc mã tương quan c chín, sắp theo thời gian, in đường đi và thời gian mất, rồi đếm dòng lỗi. Sau đó tính tốc độ đốt khi mục tiêu độ sẵn sàng chín mươi chín phần trăm mà hai trăm yêu cầu có sáu lỗi. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>json.loads</code> đổi một dòng thành từ điển; <code>sorted(…, key=lambda d: d["t"])</code> sắp theo thời gian; tốc độ đốt = (6 / 200) / (1 − 0,99).
Lời giải đầy đủ ở <code>labs/BNX/L31/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, dùng hàm đọc JSON để đổi mỗi dòng thành từ điển, và sắp theo khoá thời gian. Lời giải đầy đủ nằm trong thư mục thực hành, chỉ mở sau khi bạn đã tự thử.""", pause=180), "BNX", "L31")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("nhật ký có cấu trúc + cid", "chỉ mục đảo để tìm nhanh", "chỉ số có nhãn ít giá trị", "tỉ lệ và tốc độ đốt", "cảnh báo có việc để làm"),
           """Nhật ký có cấu trúc và mã tương quan để dựng đường đi, chỉ mục đảo để tìm nhanh. Chỉ số ít nhãn cho biết sức khoẻ, tốc độ đốt cho biết có đáng báo không, và cảnh báo cần có việc để làm."""),
        st("""<div class='box key'><b>Tư duy:</b> nhật ký trả lời câu hỏi <b>&laquo;chuyện gì đã xảy ra với yêu cầu này&raquo;</b>, chỉ số trả lời <b>&laquo;hệ thống đang khoẻ hay yếu&raquo;</b>, cảnh báo trả lời <b>&laquo;ai cần làm gì ngay&raquo;</b>. Ba thứ khác nhau, đừng bắt một thứ làm việc của hai thứ kia.
Và ELK, Grafana chỉ là công cụ: ý tưởng (chỉ mục đảo, nhãn, ngân sách lỗi) mới là thứ mang theo.</div>""",
           """Nhật ký trả lời chuyện gì đã xảy ra, chỉ số trả lời hệ thống khoẻ hay yếu, cảnh báo trả lời ai cần làm gì ngay. Công cụ sẽ đổi, ý tưởng ở lại."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Log tập trung bằng ELK: bạn dùng thế nào?", "nhật ký JSON có mã tương quan; thu thập gom về; chỉ mục đảo để tìm (đo mô phỏng: 1 000 000 dòng, chỉ xem 2 000); không ghi dữ liệu nhạy cảm"],
                  ["Prometheus + Grafana: đo gì, cảnh báo thế nào?", "chỉ số có nhãn ít giá trị (số yêu cầu, lỗi, độ trễ); cảnh báo theo tỉ lệ và tốc độ đốt ngân sách lỗi, có <code>for</code>; thử luật bằng promtool"],
                  ["Vì sao không gắn user_id vào nhãn?", "mỗi giá trị là một chuỗi: 10 000 giá trị thành 40 001 chuỗi và ≈ 2,5 MB mỗi lần kéo (số đo thật); thông tin theo người để ở nhật ký"]]),
           """Có ba câu hay gặp. Nhật ký tập trung cần mã tương quan, chỉ mục đảo, không ghi dữ liệu nhạy cảm. Chỉ số cần nhãn ít giá trị, vì mười nghìn giá trị thành hơn bốn mươi nghìn chuỗi.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Bài sau: <b>GitOps và bí mật</b>: trạng thái mong muốn nằm trong Git, vòng đối chiếu và cấp bí mật có hạn.</p>""",
           """Ở bài ba mươi hai, ta tìm hiểu quản lý hệ thống bằng kho mã nguồn: trạng thái mong muốn, vòng đối chiếu, và bí mật có hạn.""",
           forward_ref=True),
    ], checks=["alg.bnx_l31_exposition(10000)[0] == 40001"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L31", "quan_sat_nhat_ky_chi_so_canh_bao",
                  "Bài 31 — Quan sát hệ thống: nhật ký có cấu trúc, ELK, Prometheus, Grafana và cảnh báo",
                  "curriculum/bnx.yaml L31; audit/bnx/verify_bnx.py L31; audit/bnx/sources_l31.md: tài liệu Prometheus (mô hình dữ liệu, kiểu chỉ số, đặt tên, luật cảnh báo, kiểm thử luật, cấu hình), "
                  "Elastic (bài Elasticsearch from the bottom up), Grafana (nguồn dữ liệu Prometheus), đọc 2026-11-14; Prometheus 3.16.0 chạy thật bằng ảnh Docker chính thức, Python 3, JDK 21",
                  OBJ31,
                  scenes, assumes=["bnx_ma_bam"],
                  covers=COV31)


OBJ31 = ["Viết nhật ký có cấu trúc kèm mã tương quan và dựng lại đường đi của một yêu cầu qua ba dịch vụ",
         "So sánh số dòng phải xem khi quét hết nhật ký với khi dùng chỉ mục đảo ở 1 000 và 1 000 000 dòng",
         "Đọc văn bản chỉ số của Prometheus và nói vì sao nhãn quyết định số chuỗi",
         "Tính tỉ lệ lỗi và kiểm luật cảnh báo bằng công cụ promtool",
         "Tính tốc độ đốt ngân sách lỗi và số ngày cạn ngân sách",
         "Đếm số chuỗi và dung lượng một lần kéo số liệu khi nhãn có 1, 100 và 10 000 giá trị",
         "Mô tả đường đi từ ứng dụng tới bảng điều khiển và cảnh báo trong chuỗi quan sát",
         "Viết lại phép dựng đường đi và tính tốc độ đốt trên số liệu mới"]
COV31 = [(1, "example"), (2, "quymo"), (3, "formula"), (4, "example"), (5, "example"), (6, "quymo"), (7, "intuition"), (8, "practice")]
