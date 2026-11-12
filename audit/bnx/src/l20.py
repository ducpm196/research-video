from lib import *

# ── Mã Go hiện trên màn hình (chạy NGUYÊN VĂN bằng go run: audit/bnx/screen/l20.yaml, audit/bnx/ver/l20.py) ──
# Mỗi hằng là MỘT tệp main.go đầy đủ; màn hình hiện từng đoạn liên tiếp bằng code(…, lines=(a, b)). Thụt lề 2 dấu cách (đúng cú pháp, không qua gofmt).
# G_FIBER chép NGUYÊN VĂN audit/bnx/deps/l20/fiber/main.go (ver/l20.py so sánh từng byte).
GO_NAME = {"G_LOI": "TaiKhoanLoi", "G_DEM": "DemCoKhoa", "G_KHONG": "DemKhongKhoa", "G_KENH": "KenhCoDem", "G_HTTP": "HttpNho",
           "G_FIBER": "FiberNho", "G_BOQUA": "BoQuaLoi", "G_ROIRI": "RoiRi", "G_KIEM": "KiemLai"}

G_LOI = r'''
package main

import (
  "errors"
  "fmt"
)

type TaiKhoan struct {
  So   string
  SoDu int
}

func rut(tk TaiKhoan, tien int) (TaiKhoan, error) {
  if tien > tk.SoDu {
    return tk, errors.New("không đủ số dư")
  }
  tk.SoDu -= tien
  return tk, nil
}

func main() {
  tk := TaiKhoan{So: "001", SoDu: 500}
  for _, tien := range []int{200, 400} {
    moi, err := rut(tk, tien)
    if err != nil {
      fmt.Println("rút", tien, "lỗi:", err, "- số dư vẫn", tk.SoDu)
      continue
    }
    tk = moi
    fmt.Println("rút", tien, "xong, còn", tk.SoDu)
  }
}
'''

G_DEM = r'''
package main

import (
  "fmt"
  "sync"
)

func main() {
  var nhom sync.WaitGroup
  var khoa sync.Mutex
  dem := 0
  for i := 0; i < 1000; i++ {
    nhom.Add(1)
    go func() {
      defer nhom.Done()
      khoa.Lock()
      dem++
      khoa.Unlock()
    }()
  }
  nhom.Wait()
  fmt.Println("bộ đếm:", dem)
}
'''

G_KHONG = r'''
package main

import (
  "fmt"
  "sync"
)

func main() {
  var nhom sync.WaitGroup
  dem := 0
  for i := 0; i < 1000; i++ {
    nhom.Add(1)
    go func() {
      defer nhom.Done()
      dem++
    }()
  }
  nhom.Wait()
  fmt.Println("bộ đếm:", dem)
}
'''

G_KENH = r'''
package main

import "fmt"

func thuGui(ch chan int, v int) {
  select {
  case ch <- v:
    fmt.Println("gửi", v, "xong, đang chứa", len(ch))
  default:
    fmt.Println("gửi", v, "phải chờ bên nhận")
  }
}

func main() {
  ch := make(chan int, 3)
  for v := 1; v <= 4; v++ {
    thuGui(ch, v)
  }
  fmt.Println("nhận", <-ch)
  thuGui(ch, 4)
  khong := make(chan int)
  thuGui(khong, 1)
}
'''

G_HTTP = r'''
package main

import (
  "fmt"
  "io"
  "net"
  "net/http"
  "strings"
)

func sucKhoe(w http.ResponseWriter, r *http.Request) {
  w.Header().Set("Content-Type", "application/json")
  fmt.Fprint(w, `{"trang_thai":"ok"}`)
}

func main() {
  mux := http.NewServeMux()
  mux.HandleFunc("GET /suc-khoe", sucKhoe)
  ln, err := net.Listen("tcp", "127.0.0.1:0")
  if err != nil {
    fmt.Println("không mở được cổng:", err)
    return
  }
  go http.Serve(ln, mux)
  goc := "http://" + ln.Addr().String()
  goi(goc, "GET", "/suc-khoe")
  goi(goc, "POST", "/suc-khoe")
  goi(goc, "GET", "/khong-co")
}

func goi(goc, pt, duong string) {
  req, err := http.NewRequest(pt, goc+duong, nil)
  if err != nil {
    fmt.Println("lỗi tạo yêu cầu:", err)
    return
  }
  tl, err := http.DefaultClient.Do(req)
  if err != nil {
    fmt.Println("lỗi gọi:", err)
    return
  }
  defer tl.Body.Close()
  than, err := io.ReadAll(tl.Body)
  if err != nil {
    fmt.Println("lỗi đọc:", err)
    return
  }
  kq := strings.TrimSpace(string(than))
  fmt.Println(pt, duong, tl.StatusCode, kq)
}
'''

G_FIBER = r'''
package main

import (
  "fmt"
  "io"
  "net"
  "net/http"

  "github.com/gofiber/fiber/v2"
)

func main() {
  app := fiber.New(fiber.Config{DisableStartupMessage: true})
  app.Get("/suc-khoe", func(c *fiber.Ctx) error {
    return c.JSON(fiber.Map{"trang_thai": "ok"})
  })
  app.Get("/tai-khoan/:so", func(c *fiber.Ctx) error {
    return c.JSON(fiber.Map{"so": c.Params("so")})
  })
  ln, err := net.Listen("tcp", "127.0.0.1:0")
  if err != nil {
    fmt.Println("không mở được cổng:", err)
    return
  }
  go app.Listener(ln)
  goc := "http://" + ln.Addr().String()
  for _, duong := range []string{"/suc-khoe", "/tai-khoan/001"} {
    tl, err := http.Get(goc + duong)
    if err != nil {
      fmt.Println("lỗi gọi:", err)
      return
    }
    than, _ := io.ReadAll(tl.Body)
    tl.Body.Close()
    fmt.Println(duong, tl.StatusCode, string(than))
  }
  app.Shutdown()
}
'''

G_BOQUA = r'''
package main

import (
  "fmt"
  "strconv"
)

func main() {
  so, _ := strconv.Atoi("12a")
  fmt.Println("bỏ qua lỗi, số đọc được:", so)
  so, err := strconv.Atoi("12a")
  fmt.Println("kiểm lỗi:", so, err)
}
'''

G_ROIRI = r'''
package main

import (
  "fmt"
  "runtime"
  "time"
)

func thu(dem int) int {
  for i := 0; i < 1000; i++ {
    kq := make(chan int, dem)
    go func() { kq <- i }() // bên nhận đã bỏ đi, không ai nhận
  }
  time.Sleep(200 * time.Millisecond)
  return runtime.NumGoroutine()
}

func main() {
  fmt.Println("kênh đệm 1, còn sống:", thu(1))
  fmt.Println("kênh không đệm, còn sống:", thu(0))
}
'''

G_KIEM = r'''
package main

import (
  "fmt"
  "sync"
  "sync/atomic"
)

func main() {
  var nhom sync.WaitGroup
  var a atomic.Int64
  ch := make(chan int, 1000)
  for i := 0; i < 1000; i++ {
    nhom.Add(1)
    go func() {
      defer nhom.Done()
      a.Add(1)
      ch <- 1
    }()
  }
  nhom.Wait()
  close(ch)
  tong := 0
  for v := range ch {
    tong += v
  }
  fmt.Println("atomic:", a.Load(), "- qua kênh:", tong)
}
'''

# Lệnh bash hiện trên màn hình (chạy trong thư mục có main.go = chương trình tương ứng; sổ ghi `files`)
CMD_RACE = 'go run -race main.go 2>&1 | grep -E "DATA RACE|exit status" | uniq'
CMD_RACE2 = "go run -race main.go"

# Đầu ra thật (chạy 2026-11-12, go1.25.5 windows/amd64; mỗi chương trình chạy nhiều lần cho cùng kết quả)
OUT_LOI = """
rút 200 xong, còn 300
rút 400 lỗi: không đủ số dư - số dư vẫn 300
"""
OUT_DEM = """
bộ đếm: 1000
"""
OUT_RACE = """
WARNING: DATA RACE
exit status 66
"""
OUT_KENH = """
gửi 1 xong, đang chứa 1
gửi 2 xong, đang chứa 2
gửi 3 xong, đang chứa 3
gửi 4 phải chờ bên nhận
nhận 1
gửi 4 xong, đang chứa 3
gửi 1 phải chờ bên nhận
"""
OUT_HTTP = """
GET /suc-khoe 200 {"trang_thai":"ok"}
POST /suc-khoe 405 Method Not Allowed
GET /khong-co 404 404 page not found
"""
OUT_FIBER = """
/suc-khoe 200 {"trang_thai":"ok"}
/tai-khoan/001 200 {"so":"001"}
"""
OUT_BOQUA = """
bỏ qua lỗi, số đọc được: 0
kiểm lỗi: 0 strconv.Atoi: parsing "12a": invalid syntax
"""
OUT_ROIRI = """
kênh đệm 1, còn sống: 1
kênh không đệm, còn sống: 1001
"""
OUT_KIEM = """
atomic: 1000 - qua kênh: 1000
"""

_KEEP_CASE = {"API", "Java", "JVM", "Spring", "HTTP", "JSON", "A", "B", "C"}


def _lower_first(t):
    w = t.split(" ", 1)[0].strip(",:")
    if w in _KEEP_CASE or (len(w) > 1 and w.isupper()):
        return t
    return t[:1].lower() + t[1:]


def _fmerge(a, b):
    if a in (0, None):
        return b
    if b in (0, None):
        return a
    la, lb = (a if isinstance(a, list) else [a]), (b if isinstance(b, list) else [b])
    return la + [x for x in lb if x not in la]


def _merge_short(st_, minw=8, maxc=170, maxw=38):
    """Câu ≤ 7 từ (TTS/ASR dễ méo) ghép vào câu sau (hoặc câu trước) bằng dấu phẩy; focus ghép theo (như bài L03)."""
    ss = lv.sentences(st_["say"])
    foc = st_.get("focus")
    fl = list(foc) if isinstance(foc, list) and len(foc) == len(ss) else None
    j = 0
    while j < len(ss):
        if len(ss[j].split()) < minw and ss[j].endswith("."):
            nxt = ss[j][:-1] + ", " + _lower_first(ss[j + 1]) if j + 1 < len(ss) else None
            if nxt and len(nxt) <= maxc and len(nxt.split()) <= maxw:
                ss[j:j + 2] = [nxt]
                if fl:
                    fl[j:j + 2] = [_fmerge(fl[j], fl[j + 1])]
                continue
            if j > 0 and ss[j - 1].endswith("."):
                prv = ss[j - 1][:-1] + ", " + _lower_first(ss[j])
                if len(prv) <= maxc and len(prv.split()) <= maxw:
                    ss[j - 1:j + 1] = [prv]
                    if fl:
                        fl[j - 1:j + 1] = [_fmerge(fl[j - 1], fl[j])]
                    j -= 1
                    continue
        j += 1
    st_["say"] = " ".join(ss)
    if fl is not None:
        st_["focus"] = fl


def _spoken(scenes):
    for sc_ in scenes:
        for s_ in sc_["steps"]:
            _merge_short(s_)
    return scenes


def build():
    hook = sc("hook", "hook", "Một nghìn yêu cầu cùng cộng một bộ đếm: ra 1000 hay ít hơn?", [
        st("""<p>Dịch vụ ngân hàng đếm số yêu cầu đã xử lý. <b>Một nghìn</b> yêu cầu tới cùng lúc, mỗi yêu cầu cộng 1 vào <b>một bộ đếm chung</b> (số minh hoạ).</p>
<div class="box key">Kỳ vọng: $1000 \\cdot 1 = 1000$. Bỏ khoá, chạy thật thì bộ đếm <b>thường thấp hơn 1000</b> và mỗi lần chạy một khác.
Vì sao, và chữa thế nào?</div>""",
           """Chào bạn, hãy tưởng tượng dịch vụ của ngân hàng đếm số yêu cầu đã xử lý. Một nghìn yêu cầu tới cùng lúc, mỗi yêu cầu cộng một vào một bộ đếm chung, với số minh hoạ.
           Ta kỳ vọng bộ đếm ra đúng một nghìn. Nhưng nếu bỏ khoá, chạy thật thì kết quả thường thấp hơn, và mỗi lần chạy một khác. Vậy vì sao, và chữa thế nào?""",
           focus=[1, 1, 2, 2, 2]),
        st("""<p>Ngôn ngữ trên màn hình: <b>Go (Golang)</b>, kèm bộ khung web <b>Fiber (Go)</b> (hai dòng trên CV).</p>"""
           + table(["câu hỏi", "bài này trả lời"],
                   [["chạy nhiều việc cùng lúc rồi chờ xong hết", "<b>luồng nhẹ</b> (goroutine) và <b>nhóm chờ</b> (WaitGroup)"],
                    ["hai việc cùng ghi một biến thì sao", "<b>tranh chấp dữ liệu</b>; khoá (Mutex); trình phát hiện tranh chấp (<code>-race</code>)"],
                    ["truyền dữ liệu giữa các việc", "<b>kênh</b> (channel) không đệm và có đệm"],
                    ["dựng dịch vụ HTTP", "gói chuẩn <code>net/http</code>, rồi bộ khung <b>Fiber</b> thêm gì"]]),
           """Ngôn ngữ ta dùng hôm nay là ngôn ngữ thứ hai trên hồ sơ, tên hiện trên màn hình, cùng một bộ khung web.
           Câu một, làm sao chạy nhiều việc cùng lúc rồi chờ xong hết, bằng luồng nhẹ và nhóm chờ.
           Câu hai, hai việc cùng ghi một biến thì sao, và khoá cùng trình phát hiện tranh chấp giúp thế nào.
           Câu ba, truyền dữ liệu giữa các việc bằng kênh có đệm và không đệm.
           Câu bốn, dựng dịch vụ HTTP bằng gói chuẩn, rồi xem bộ khung web thêm được gì.""",
           focus=[1, "2.2", "2.3", "2.4", "2.5"]),
    ], checks=["alg.bnx_l20_locked(1000) == 1000", "alg.bnx_l20_range(1000) == (1, 1000)"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① biến dùng chung", "một ô nhớ mà nhiều việc cùng đọc và ghi được", "bộ đếm = 0; hai việc cùng cộng 1"],
                  ["② đọc rồi ghi", "câu lệnh tăng một gồm <b>hai bước</b>: đọc giá trị, rồi ghi giá trị cộng 1", "đọc 0, rồi ghi 1"],
                  ["③ hàm trả nhiều giá trị", "một hàm trả cả kết quả lẫn lỗi; lỗi rỗng (nil) nghĩa là không có lỗi", "rút 200 từ số dư 500 trả (300, không lỗi)"],
                  ["④ yêu cầu và trả lời HTTP", "yêu cầu có phương thức và đường dẫn; trả lời có mã trạng thái và thân", "GET /suc-khoe trả mã 200"]]),
           """Trước hết ta cần hiểu bốn điều. Thứ nhất, biến dùng chung là một ô nhớ mà nhiều việc cùng đọc và ghi được.
           Thứ hai, câu lệnh tăng một thật ra gồm hai bước, đọc giá trị rồi ghi giá trị cộng một.
           Thứ ba, một hàm có thể trả về cả kết quả lẫn lỗi, và lỗi rỗng nghĩa là không có lỗi.
           Thứ tư, yêu cầu HTTP có phương thức và đường dẫn, còn trả lời có mã trạng thái và thân.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st("""<p>Làm thử: hai việc A và B cùng cộng 1 vào bộ đếm đang là 0, xen kẽ từng bước.</p>
$$A \\text{ đọc } 0, \\; B \\text{ đọc } 0, \\; A \\text{ ghi } 1, \\; B \\text{ ghi } 1 \\;\\Rightarrow\\; \\hl{1} \\text{ thay vì } 2$$
<span class='note'>Nếu A làm trọn rồi mới tới B: đọc 0, ghi 1, đọc 1, ghi 2, ra 2.</span>""",
           """Làm thử ngay. Hai việc A và B cùng cộng một vào bộ đếm đang là không, và chúng xen kẽ từng bước.
           A đọc không, B cũng đọc không, rồi A ghi một, B ghi một, nên bộ đếm chỉ là một thay vì hai.
           Còn nếu A làm trọn rồi mới tới B thì ra hai, vì B đọc được số một."""),
    ], checks=["alg.bnx_l20_interleave(['A', 'B', 'A', 'B']) == 1", "alg.bnx_l20_interleave(['A', 'A', 'B', 'B']) == 2",
               "alg.bnx_l20_lost(['A', 'B', 'A', 'B']) == 1", "alg.bnx_l20_rut(500, 200) == (300, None)",
               "alg.bnx_l20_route('GET', '/suc-khoe')[0] == 200"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên trong Go", "nghĩa"],
                 [["go f()", "chạy hàm f ở một <b>luồng nhẹ</b> (goroutine) riêng; chương trình không chờ nó"],
                  ["sync.WaitGroup", "<b>nhóm chờ</b>: <code>Add</code> cộng số việc, <code>Done</code> trừ một, <code>Wait</code> chờ tới khi về 0"],
                  ["sync.Mutex", "<b>khoá</b>: giữa <code>Lock</code> và <code>Unlock</code> một lúc chỉ một luồng nhẹ được vào"],
                  ["chan int", "<b>kênh</b> truyền số nguyên; <code>make(chan int, 3)</code> có đệm 3, <code>make(chan int)</code> không đệm"],
                  ["ch &lt;- v  và  &lt;-ch", "gửi v vào kênh; nhận một giá trị từ kênh"],
                  ["error, nil", "lỗi là một <b>giá trị</b> được trả về; <code>nil</code> nghĩa là không có lỗi"],
                  ["go run -race", "chạy kèm <b>trình phát hiện tranh chấp dữ liệu</b>"],
                  ["net/http, Fiber", "gói chuẩn dựng dịch vụ HTTP; bộ khung web thêm cách viết tuyến"]]),
           """Bảng này giải mã các tên trên màn hình. Lệnh đầu chạy một hàm ở luồng nhẹ riêng, và chương trình chính không chờ nó.
           Nhóm chờ có ba lệnh: cộng số việc, trừ một khi việc xong, và chờ tới khi số việc về không.
           Khoá cho phép một lúc chỉ một luồng nhẹ nằm giữa lệnh khoá và lệnh mở.
           Kênh truyền một loại giá trị, con số trong ngoặc là sức chứa của đệm, còn không có số thì là không đệm.
           Hai mũi tên là gửi vào kênh và nhận từ kênh. Lỗi là một giá trị được trả về, và giá trị rỗng nghĩa là không có lỗi.
           Cờ phát hiện tranh chấp chạy kèm một trình bắt hai luồng cùng truy cập một biến mà không phối hợp.
           Cuối cùng, gói chuẩn dựng dịch vụ HTTP, còn bộ khung web thêm cách viết tuyến gọn hơn.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9"]),
    ], checks=["alg.bnx_l20_wg(1000, 1000) == 0", "alg.bnx_l20_accept(3, 4) == (3, 4)"])

    def lane(y, name, cells):
        s = txt(200, y + 38, name, 22, "end")
        for x, w, lab, col in cells:
            s += box(x, y, w, 60, lab, col, 22)
        return s

    intu = sc("intuition", "intuition", "Hình dung: xen kẽ đọc-ghi, kênh và dịch vụ HTTP", [
        st(svg(1500, 440,
               txt(750, 34, "Hai luồng nhẹ A, B cùng cộng 1 vào bộ đếm đang là 0", 26, "middle", "#1f2937", True),
               lane(70, "không khoá", [(220, 250, "A đọc 0", C_BLUE), (490, 250, "B đọc 0", C_GREEN), (760, 250, "A ghi 1", C_BLUE),
                                       (1030, 250, "B ghi 1", C_GREEN)]),
               txt(1300, 108, "→ bộ đếm = 1", 26, "start", "#dc2626", True),
               lane(190, "có khoá", [(220, 250, "A đọc 0", C_BLUE), (490, 250, "A ghi 1", C_BLUE), (760, 250, "B đọc 1", C_GREEN),
                                     (1030, 250, "B ghi 2", C_GREEN)]),
               txt(1300, 228, "→ bộ đếm = 2", 26, "start", "#16a34a", True),
               txt(750, 330, "Không khoá: B đọc 0 khi A chưa ghi, nên một lần cộng bị mất", 24, "middle", "#1f2937", True),
               txt(750, 380, "Có khoá: A đọc và ghi trọn vẹn rồi B mới vào, nên không lần nào bị mất", 24, "middle", "#1f2937", True)),
           """Hình này cho thấy vì sao bộ đếm sai. Hàng trên không có khoá: A đọc không, B cũng đọc không vì A chưa ghi, rồi cả hai ghi một, nên mất một lần cộng.
           Hàng dưới có khoá: A đọc và ghi trọn vẹn, rồi B mới đọc số một và ghi hai, nên không mất lần nào."""),
        st(svg(1500, 520,
               txt(750, 34, "Kênh không đệm và kênh có đệm 3", 26, "middle", "#1f2937", True),
               txt(60, 100, "không đệm", 22, "start", "#1f2937", True),
               box(60, 120, 200, 70, "bên gửi", C_BLUE, 22), arrow(260, 155, 520, 155, "#475569", "gặp nhau", 22),
               box(520, 120, 200, 70, "bên nhận", C_GREEN, 22),
               txt(760, 163, "gửi chỉ xong khi có bên nhận sẵn sàng", 24, "start"),
               txt(60, 270, "có đệm 3", 22, "start", "#1f2937", True),
               box(60, 290, 200, 70, "bên gửi", C_BLUE, 22), arrow(260, 325, 340, 325),
               box(340, 290, 110, 70, "1", C_AMBER, 24, True), box(460, 290, 110, 70, "2", C_AMBER, 24, True),
               box(580, 290, 110, 70, "3", C_AMBER, 24, True), arrow(690, 325, 770, 325),
               box(770, 290, 200, 70, "bên nhận", C_GREEN, 22),
               box(60, 400, 200, 70, "giá trị 4", C_RED, 22), txt(300, 443, "đệm đầy: phải chờ bên nhận lấy bớt", 24, "start", "#dc2626", True),
               txt(750, 505, "Không đệm: gửi chờ bên nhận. Có đệm n: gửi chờ khi đã đầy n giá trị", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là kênh. Với kênh không đệm, bên gửi chỉ xong khi có bên nhận sẵn sàng, nên hai bên phải gặp nhau.
           Với kênh có đệm ba, ba giá trị đầu vào đệm ngay mà không chờ ai. Giá trị thứ bốn thấy đệm đầy, nên phải chờ bên nhận lấy bớt một giá trị."""),
        st(svg(1500, 470,
               txt(750, 34, "Một dịch vụ HTTP nhỏ và bộ khung web đứng trên", 26, "middle", "#1f2937", True),
               box(40, 70, 260, 90, ["khách", "GET /suc-khoe"], C_BLUE, 22), arrow(300, 115, 400, 115),
               box(400, 70, 300, 90, ["bộ định tuyến", "tìm tuyến khớp"], C_AMBER, 22), arrow(700, 115, 800, 115),
               box(800, 70, 260, 90, ["hàm xử lý", "sucKhoe"], C_GREEN, 22), arrow(1060, 115, 1130, 115),
               box(1130, 70, 330, 90, ["mã 200", "thân JSON"], C_PURPLE, 22),
               panel(40, 210, 1420, 200, "Bộ khung web (Fiber) đứng trên cùng", C_GRAY, 26),
               box(70, 270, 420, 110, ["tuyến có tham số", "/tai-khoan/:so"], C_BLUE, 22),
               box(540, 270, 420, 110, ["trả JSON gọn", "c.JSON(...)"], C_GREEN, 22),
               box(1010, 270, 420, 110, ["dựng trên fasthttp", "(nhà phát triển Fiber nêu)"], C_AMBER, 22),
               txt(750, 450, "Cùng một chuyện: yêu cầu đi vào, tìm tuyến, hàm xử lý trả lời đi ra", 24, "middle", "#1f2937", True)),
           """Hình thứ ba là một dịch vụ HTTP nhỏ. Khách gửi phương thức đọc cùng đường dẫn, bộ định tuyến tìm tuyến khớp rồi gọi hàm xử lý.
           Hàm xử lý ghi mã hai trăm và thân JSON. Bộ khung web đứng trên cùng, cho viết tuyến có tham số và trả JSON gọn hơn.
           Nhưng bên dưới vẫn là cùng một chuyện: yêu cầu đi vào, tìm tuyến, và hàm xử lý trả lời đi ra."""),
    ], checks=["alg.bnx_l20_interleave(['A', 'B', 'A', 'B']) == 1", "alg.bnx_l20_interleave(['A', 'A', 'B', 'B']) == 2",
               "alg.bnx_l20_accept(3, 4) == (3, 4)", "alg.bnx_l20_route('GET', '/suc-khoe')[0] == 200",
               "alg.bnx_l20_fiber_route('/tai-khoan/001')[0] == 200"])

    form = sc("formula", "formula", "Suy ra từng bước: từ luồng nhẹ tới dịch vụ HTTP", [
        st("""<p><b>Bước 1.</b> Lệnh <code>go f()</code> chạy <code>f</code> ở luồng nhẹ riêng rồi trở về ngay, nên hàm chính có thể kết thúc <b>trước</b> các việc.
Vì vậy ta dùng nhóm chờ: <code>Add(1)</code> trước mỗi việc, <code>Done()</code> khi việc xong, <code>Wait()</code> chờ tới khi số việc về 0.</p>
<p>Làm thử: 3 lần Add, 2 lần Done.</p>
$$3 - 2 = \\hl{1} \\neq 0 \\;\\Rightarrow\\; \\text{Wait vẫn chờ}; \\qquad 1000 - 1000 = 0 \\;\\Rightarrow\\; \\text{Wait trở về}$$""",
           """Bước một, lệnh chạy ở luồng nhẹ trở về ngay, nên hàm chính có thể kết thúc trước các việc.
           Vì vậy ta dùng nhóm chờ: cộng một trước mỗi việc, trừ một khi việc xong, rồi chờ tới khi số việc về không.
           Làm thử, ba lần cộng và hai lần trừ còn dư một, nên lệnh chờ vẫn chờ.
           Một nghìn lần cộng và một nghìn lần trừ thì về không, lệnh chờ mới trở về.""", clear=True),
        st("""<p><b>Bước 2.</b> Hai luồng nhẹ cùng ghi một biến mà không phối hợp là <b>tranh chấp dữ liệu</b>.
Vì tăng một gồm đọc rồi ghi, nên một lần cộng có thể bị ghi đè, và bộ đếm cuối nằm giữa 1 và số luồng.</p>
<p>Làm thử: 3 luồng cùng cộng 1 vào 0, không khoá.</p>
$$\\text{nhỏ nhất } \\hl{1}, \\quad \\text{lớn nhất } 3; \\qquad \\text{chỉ khi xen kẽ vừa vặn mới ra } 3$$""",
           """Bước hai, hai luồng nhẹ cùng ghi một biến mà không phối hợp gọi là tranh chấp dữ liệu.
           Vì tăng một gồm đọc rồi ghi, nên một lần cộng có thể bị ghi đè, và bộ đếm cuối nằm giữa một và số luồng.
           Làm thử với ba luồng cùng cộng một vào không, kết quả nhỏ nhất là một, lớn nhất là ba.""", clear=True),
        st("""<p><b>Bước 3.</b> Khoá biến đọc-rồi-ghi thành một khối: giữa <code>Lock</code> và <code>Unlock</code> một lúc chỉ một luồng nhẹ, nên không lần cộng nào bị mất.</p>
<p>Làm thử: 1000 luồng nhẹ, mỗi luồng cộng 1 trong khoá.</p>
$$1000 \\cdot 1 = \\hlg{1000} \\quad \\text{(mọi lần chạy)}$$
<span class='note'>Đổi lại, các luồng xếp hàng qua khoá, nên đoạn nằm trong khoá càng ngắn càng tốt.</span>""",
           """Bước ba, khoá làm cho đọc rồi ghi thành một khối, vì giữa lệnh khoá và lệnh mở một lúc chỉ một luồng nhẹ được vào, nên không lần cộng nào bị mất.
           Làm thử với một nghìn luồng, mỗi luồng cộng một trong khoá, thì ra đúng một nghìn ở mọi lần chạy.
           Đổi lại, các luồng xếp hàng qua khoá, nên đoạn nằm trong khoá càng ngắn càng tốt.""", clear=True),
        st("""<p><b>Bước 4.</b> Trình phát hiện tranh chấp: chạy <code>go run -race</code>. Nó báo khi hai luồng nhẹ truy cập cùng một biến, ít nhất một lần là ghi, mà không phối hợp.
Nó chỉ thấy tranh chấp trên đường mã <b>đã chạy</b>, và làm chương trình chậm hơn.</p>
<div class="box key">Khi thấy tranh chấp, nó in cảnh báo rồi thoát với mã <b>66</b> (mặc định). Một lần in đúng kết quả chưa chứng minh là không có tranh chấp.</div>
<span class='note'>Trên máy chạy bài này (Windows), cờ <code>-race</code> cần bật cgo và có trình biên dịch C (gcc); máy khác có thể khác.</span>""",
           """Bước bốn, trình phát hiện tranh chấp bật bằng cờ phát hiện khi chạy chương trình. Nó báo khi hai luồng nhẹ truy cập cùng một biến, ít nhất một lần là ghi, mà không phối hợp.
           Nó chỉ thấy tranh chấp trên đường mã đã chạy, và làm chương trình chậm hơn. Khi thấy, nó in cảnh báo rồi thoát với mã sáu mươi sáu.
           Một lần in đúng kết quả chưa chứng minh là không có tranh chấp, nên hãy chạy kiểm thử kèm cờ này.
           Trên máy chạy bài này, cờ ấy cần bật cầu nối với mã C và có trình biên dịch C, còn máy khác có thể khác.""",
           focus=[1, 1, 1, 2, 2, 3], clear=True),
        st("""<p><b>Bước 5.</b> Kênh truyền giá trị giữa các luồng nhẹ. <b>Không đệm</b>: bên gửi chờ tới khi có bên nhận. <b>Có đệm n</b>: gửi xong ngay nếu đệm chưa đầy, đầy thì chờ.</p>
<p>Làm thử: đệm 2, gửi liền 3 giá trị, chưa ai nhận.</p>
$$2 \\text{ giá trị vào đệm}; \\qquad 2 + 1 = \\hl{3} \\text{: giá trị thứ 3 phải chờ}$$""",
           """Bước năm, kênh truyền giá trị giữa các luồng nhẹ. Kênh không đệm thì bên gửi chờ tới khi có bên nhận.
           Kênh có đệm thì gửi xong ngay nếu đệm chưa đầy, còn đầy thì phải chờ.
           Làm thử với đệm hai, gửi liền ba giá trị mà chưa ai nhận: hai giá trị vào đệm, nên giá trị thứ ba phải chờ.""", clear=True),
        st("""<p><b>Bước 6.</b> Cách báo lỗi thông thường: hàm trả <b>thêm một giá trị lỗi</b>, bên gọi phải tự kiểm. Lỗi rỗng là thành công. Bỏ qua lỗi thì chương trình chạy tiếp với giá trị không.</p>
<p>Làm thử: tài khoản 500, rút 200 rồi rút 400.</p>
$$500 - 200 = 300; \\qquad 400 > 300 \\;\\Rightarrow\\; \\text{lỗi, số dư vẫn } \\hl{300}$$""",
           """Bước sáu, cách báo lỗi thông thường của ngôn ngữ này là hàm trả thêm một giá trị lỗi, và bên gọi phải tự kiểm. Lỗi rỗng nghĩa là thành công.
           Bỏ qua lỗi thì chương trình chạy tiếp với giá trị không. Làm thử, tài khoản năm trăm, rút hai trăm còn ba trăm.
           Rút bốn trăm thì bốn trăm lớn hơn ba trăm, nên có lỗi và số dư vẫn là ba trăm.""", clear=True),
        st("""<p><b>Bước 7.</b> Dịch vụ HTTP nhỏ đăng ký tuyến <code>GET /suc-khoe</code> với một hàm xử lý. Gói chuẩn tự trả 405 khi sai phương thức và 404 khi không có đường dẫn. Mẫu tuyến có phương thức như <code>GET /suc-khoe</code> cần Go từ phiên bản 1.22.</p>"""
           + table(["yêu cầu", "mã", "thân"],
                   [["GET /suc-khoe", "200", "<code>{\"trang_thai\":\"ok\"}</code>"],
                    ["POST /suc-khoe", "405", "Method Not Allowed"],
                    ["GET /khong-co", "404", "404 page not found"]]),
           """Bước bảy, dịch vụ HTTP nhỏ đăng ký một tuyến, đọc đường dẫn kiểm sức khoẻ, với một hàm xử lý.
           Đúng tuyến thì hàm xử lý trả mã hai trăm và thân JSON. Cùng đường dẫn nhưng sai phương thức thì gói chuẩn tự trả bốn trăm linh năm, vì tuyến chỉ đăng ký cho phương thức đọc.
           Đường dẫn không đăng ký thì nhận bốn trăm linh bốn, vì không tuyến nào khớp, và mẫu tuyến có phương thức cần Go từ phiên bản một phẩy hai mươi hai.""",
           focus=[1, "2.2", "2.3", "2.4"], clear=True),
        st(table(["việc", "gói chuẩn net/http", "bộ khung Fiber"],
                 [["đăng ký tuyến", "<code>mux.HandleFunc(\"GET /suc-khoe\", f)</code>", "<code>app.Get(\"/suc-khoe\", f)</code>"],
                  ["tham số trong đường dẫn", "(bài không so sánh)", "<code>/tai-khoan/:so</code>, đọc bằng <code>c.Params(\"so\")</code>"],
                  ["trả JSON", "tự đặt tiêu đề và ghi thân (chương trình trên)", "<code>c.JSON(fiber.Map{…})</code>"],
                  ["nền bên dưới", "thư viện chuẩn", "dựng trên <b>fasthttp</b> (nhà phát triển Fiber nêu)"]])
           + """<div class="box warn">Bài dùng Fiber <b>v2.52.16</b>; nhà phát triển ghi ở bản v2: không còn được bảo trì tích cực. Để chạy thử: <code>go mod init vidu</code>, rồi <code>go get github.com/gofiber/fiber/v2@v2.52.16</code>.</div>""",
           """Bước tám, bộ khung web thêm gì lên trên gói chuẩn? Đăng ký tuyến thì cả hai đều gọn.
           Bộ khung cho viết tham số ngay trong đường dẫn và đọc bằng một lệnh. Nó cũng có lệnh trả JSON gọn, trong khi với gói chuẩn ta tự đặt tiêu đề và ghi thân.
           Bên dưới, nó dựng trên một thư viện HTTP khác, theo lời nhà phát triển của nó.
           Lưu ý, bản dùng trong bài là bản hai, mà nhà phát triển ghi ở bản hai là không còn được bảo trì tích cực, nên dự án mới cần cân nhắc phiên bản.
           Để chạy thử, cần khởi tạo một mô-đun rồi tải thư viện đúng bản đó bằng lệnh của Go.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", 2, 2], clear=True),
    ], checks=["alg.bnx_l20_wg(3, 2) == 1 and alg.bnx_l20_wg(1000, 1000) == 0", "alg.bnx_l20_range(3) == (1, 3)",
               "alg.bnx_l20_locked(1000) == 1000", "alg.bnx_l20_race_exit() == 66", "alg.bnx_l20_accept(2, 3) == (2, 3)",
               "alg.bnx_l20_rut(500, 200) == (300, None)", "alg.bnx_l20_rut(300, 400) == (300, 'không đủ số dư')",
               "alg.bnx_l20_route('GET', '/suc-khoe')[0] == 200 and alg.bnx_l20_route('POST', '/suc-khoe')[0] == 405 and alg.bnx_l20_route('GET', '/khong-co')[0] == 404",
               "alg.bnx_l20_fiber_route('/suc-khoe')[0] == 200"])

    ex = sc("example", "example", "Ví dụ chạy thật bằng Go, từng phép tính", [
        st(code(G_LOI, "main.go (trích): cấu trúc tài khoản và hàm trả lỗi", lines=(8, 19)),
           """Ta chạy thật bằng ngôn ngữ thứ hai trên hồ sơ. Chương trình đầu có một cấu trúc tài khoản gồm số tài khoản và số dư.
           Hàm rút nhận tài khoản và số tiền, rồi trả về hai giá trị: tài khoản mới và một lỗi.
           Nếu số tiền lớn hơn số dư, nó trả tài khoản cũ cùng một lỗi. Nếu đủ, nó trừ tiền và trả lỗi rỗng.""",
           focus=[0, ["2.1", "2.2", "2.3"], "2.6", ["2.7", "2.8"], ["2.10", "2.11"]], clear=True),
        st(code(G_LOI, "main.go (tiếp): rút 200 rồi rút 400", lines=(21, 32)),
           """Hàm chính tạo tài khoản có số dư năm trăm, rồi lần lượt rút hai trăm và bốn trăm.
           Mỗi lần rút, ta nhận hai giá trị về là tài khoản mới và lỗi.
           Nếu lỗi khác rỗng thì in lỗi cùng số dư cũ, rồi bỏ qua sang lần sau.
           Chỉ khi không có lỗi ta mới nhận tài khoản mới và in số dư còn lại.""",
           focus=[["2.2", "2.3"], "2.4", ["2.5", "2.6", "2.7", "2.8"], ["2.9", "2.10"]], clear=True),
        st(out(OUT_LOI) + """
$$① \\; 500 - 200 = 300; \\qquad 400 > 300 \\;\\Rightarrow\\; \\text{lỗi, số dư vẫn } \\hl{300}$$""",
           """Kết quả chạy thật: lần rút hai trăm xong và còn ba trăm.
           Lần rút bốn trăm báo không đủ số dư, và số dư vẫn là ba trăm.
           Phép tính thứ nhất: năm trăm trừ hai trăm là ba trăm, rồi bốn trăm lớn hơn ba trăm nên có lỗi, và số dư không đổi.""",
           focus=["2.1", "2.2", 3], clear=True),
        st(code(G_DEM, "main.go (trích): một nghìn luồng nhẹ cùng cộng, có khoá", lines=(8, 19)),
           """Chương trình thứ hai là bộ đếm ở đầu bài. Hàm chính khai một nhóm chờ, một khoá và bộ đếm bằng không.
           Vòng lặp chạy một nghìn lần; mỗi vòng cộng một vào nhóm chờ rồi chạy một luồng nhẹ.
           Luồng nhẹ khoá, tăng bộ đếm, rồi mở khoá, và lệnh hoãn bảo đảm việc báo xong chạy khi luồng nhẹ kết thúc.""",
           focus=[0, ["2.2", "2.3", "2.4"], ["2.5", "2.6", "2.7"], ["2.8", "2.9", "2.10", "2.11"]], clear=True),
        st(code(G_DEM, "main.go (tiếp): chờ cả nhóm rồi in", lines=(20, 23)) + out(OUT_DEM) + """
$$② \\; 1000 \\cdot 1 = \\hlg{1000}; \\qquad 1000 \\text{ lần Add} - 1000 \\text{ lần Done} = 0$$""",
           """Sau vòng lặp, hàm chính gọi lệnh chờ để đợi tới khi cả một nghìn luồng nhẹ báo xong, rồi mới in bộ đếm.
           Kết quả chạy thật in bộ đếm đúng một nghìn.
           Phép tính thứ hai: một nghìn luồng, mỗi luồng cộng một trong khoá, nên bộ đếm là một nghìn, và một nghìn lần cộng trừ một nghìn lần trừ là không, nên lệnh chờ trở về.""",
           focus=[["2.2", "2.3"], "4.1", 5], clear=True),
        st(code(G_KHONG, "Bỏ khoá và mở khoá: trong luồng nhẹ chỉ còn dem++", lines=(11, 17))
           + code(CMD_RACE, "Chạy kèm trình phát hiện, lọc lấy hai dòng cần xem"),
           """Giờ ta bỏ hai lệnh khoá và mở khoá, nên trong luồng nhẹ chỉ còn lệnh tăng bộ đếm.
           Rồi ta chạy chương trình này với cờ phát hiện tranh chấp, và lọc lấy hai dòng cần xem.""",
           focus=["2.5", "4.1"], clear=True),
        st(out(OUT_RACE) + """
$$③ \\; \\text{một cặp xen kẽ: } 2 - 1 = \\hl{1} \\text{ lần cộng bị mất}; \\qquad \\text{kết quả} = 1000 - \\text{số lần mất} \\le 1000$$""",
           """Kết quả chạy thật: trình phát hiện in cảnh báo tranh chấp dữ liệu, rồi chương trình thoát với mã sáu mươi sáu.
           Khi ta chạy chương trình này nhiều lần mà không có cờ, bộ đếm thường thấp hơn một nghìn và mỗi lần một khác, nhưng thỉnh thoảng vẫn ra đủ một nghìn.
           Phép tính thứ ba: một cặp xen kẽ làm mất một lần cộng, nên kết quả là một nghìn trừ số lần mất, và không bao giờ vượt một nghìn.""",
           focus=["2.1", 2, 3], clear=True),
        st(code(G_KENH, "main.go (trích): thử gửi vào kênh, không chịu treo", lines=(5, 12)),
           """Chương trình thứ ba là kênh. Hàm này thử gửi một giá trị vào kênh, và dùng câu lệnh chọn để không bị treo.
           Nếu gửi được ngay thì nhánh đầu in gửi xong và số giá trị đang chứa.
           Nếu không thì nhánh mặc định in rằng lệnh gửi phải chờ bên nhận, vì lệnh gửi bình thường lúc đó sẽ bị chặn.""",
           focus=[["2.1", "2.2"], ["2.3", "2.4"], ["2.5", "2.6"]], clear=True),
        st(code(G_KENH, "main.go (tiếp): kênh đệm 3 gửi 4 giá trị, rồi kênh không đệm", lines=(14, 23)),
           """Hàm chính tạo kênh có đệm ba, rồi thử gửi bốn giá trị liền nhau mà chưa ai nhận.
           Sau đó nó nhận một giá trị ra, và thử gửi lại giá trị bốn.
           Cuối cùng nó tạo một kênh không đệm, và thử gửi một giá trị khi chưa có bên nhận nào.""",
           focus=[["2.2", "2.3", "2.4", "2.5"], ["2.6", "2.7"], ["2.8", "2.9"]], clear=True),
        st(out(OUT_KENH) + """
$$④ \\; 3 + 1 = \\hl{4}: \\text{ giá trị thứ 4 phải chờ}; \\qquad 3 - 1 = 2 \\text{ đang chứa} \\;\\Rightarrow\\; 2 + 1 = 3 \\text{, gửi 4 được}$$""",
           """Kết quả chạy thật: ba giá trị đầu vào đệm ngay, đệm chứa dần một, hai, ba.
           Giá trị thứ bốn thấy đệm đầy nên phải chờ bên nhận.
           Sau khi nhận ra giá trị một, đệm còn hai giá trị, nên lần gửi bốn thứ hai xong và đệm lại chứa ba.
           Với kênh không đệm mà chưa có bên nhận, ngay giá trị đầu tiên đã phải chờ.
           Phép tính thứ tư: đệm ba nhận ba giá trị, nên giá trị thứ ba cộng một, tức thứ bốn, là giá trị phải chờ.""",
           focus=[["2.1", "2.2", "2.3"], "2.4", ["2.5", "2.6"], "2.7", 3], clear=True),
        st(code(G_HTTP, "main.go (trích): hàm xử lý và đăng ký tuyến", lines=(11, 18)),
           """Chương trình thứ tư là dịch vụ HTTP nhỏ bằng gói chuẩn. Hàm xử lý nhận nơi ghi trả lời và yêu cầu.
           Nó đặt tiêu đề cho biết thân là JSON, rồi ghi thân gồm một trường trạng thái cho biết dịch vụ đang ổn.
           Trong hàm chính, ta tạo bộ định tuyến và đăng ký tuyến đọc, đường dẫn kiểm sức khoẻ, với hàm xử lý này.""",
           focus=[0, "2.1", ["2.2", "2.3"], ["2.6", "2.7", "2.8"]], clear=True),
        st(code(G_HTTP, "main.go (tiếp): mở cổng, chạy máy chủ, gọi ba yêu cầu", lines=(19, 29)),
           """Tiếp theo ta mở một cổng trên máy này, để hệ điều hành tự chọn, và kiểm lỗi nếu không mở được.
           Rồi một luồng nhẹ chạy máy chủ trên cổng đó. Ba dòng cuối gọi ba yêu cầu: đọc đúng tuyến, gửi sai phương thức, và gọi một đường dẫn không có.
           Hàm gọi là một máy khách nhỏ, ta không đọc từng dòng của nó ở đây.""",
           focus=[["2.1", "2.2", "2.3", "2.4", "2.5"], "2.6", ["2.8", "2.9", "2.10"], 0], clear=True),
        st(out(OUT_HTTP) + """
$$⑤ \\; \\text{GET /suc-khoe} \\Rightarrow \\hl{200} \\text{ và thân JSON}; \\quad \\text{POST} \\Rightarrow 405; \\quad \\text{GET /khong-co} \\Rightarrow 404$$""",
           """Kết quả chạy thật: đọc đúng tuyến cho mã hai trăm và thân JSON có trường trạng thái cho biết dịch vụ đang ổn.
           Gửi sai phương thức nhận bốn trăm linh năm, còn đường dẫn lạ nhận bốn trăm linh bốn.
           Phép tính thứ năm: tuyến kiểm sức khoẻ trả mã hai trăm, hai trường hợp còn lại do gói chuẩn tự trả lời.""",
           focus=["2.1", ["2.2", "2.3"], 3], clear=True),
        st(code(G_FIBER, "main.go của Fiber v2.52.16 (trích): hai tuyến", lines=(9, 19)),
           """Chương trình thứ năm làm cùng việc bằng bộ khung web, nhập từ một thư viện ngoài, tên hiện trên màn hình.
           Đăng ký tuyến chỉ một lệnh, và hàm xử lý trả JSON bằng một lệnh, không phải tự đặt tiêu đề.
           Tuyến thứ hai có một ô tham số đặt tên trong đường dẫn, và hàm xử lý đọc nó bằng đúng tên đó.""",
           focus=["2.1", ["2.6", "2.7"], ["2.9", "2.10"]], clear=True),
        st(out(OUT_FIBER),
           """Kết quả chạy thật: tuyến kiểm sức khoẻ cũng trả mã hai trăm với cùng thân JSON.
           Đường dẫn tài khoản không không một cho ra phần cuối của đường dẫn, và trả lại nó trong thân.""",
           focus=["2.1", "2.2"], clear=True),
    ], checks=["alg.bnx_l20_rut(500, 200) == (300, None) and alg.bnx_l20_rut(300, 400)[0] == 300",
               "alg.bnx_l20_locked(1000) == 1000 and alg.bnx_l20_wg(1000, 1000) == 0",
               "alg.bnx_l20_lost(['A', 'B', 'A', 'B']) == 1 and alg.bnx_l20_race_exit() == 66",
               "alg.bnx_l20_chan(3, [('g', 1), ('g', 2), ('g', 3), ('g', 4), ('n',), ('g', 4)]) == [('xong', 1), ('xong', 2), ('xong', 3), ('chờ',), ('nhận', 1), ('xong', 3)]",
               "alg.bnx_l20_chan(0, [('g', 1)]) == [('chờ',)]", "alg.bnx_l20_accept(3, 4) == (3, 4)",
               "alg.bnx_l20_route('GET', '/suc-khoe') == (200, '{\"trang_thai\":\"ok\"}')",
               "alg.bnx_l20_route('POST', '/suc-khoe')[0] == 405 and alg.bnx_l20_route('GET', '/khong-co')[0] == 404",
               "alg.bnx_l20_fiber_route('/tai-khoan/001') == (200, '{\"so\":\"001\"}')"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: nguyên tử và kênh, không dùng khoá", [
        st(code(G_KIEM, "main.go: đếm bằng bộ đếm nguyên tử và bằng kênh", lines=(9, 20)),
           """Ta kiểm bằng hai đường khác, đều không dùng khoá. Đường thứ nhất là bộ đếm nguyên tử, một kiểu bộ đếm riêng cho nhiều luồng; bài này không đi sâu cách nó chạy bên trong.
           Đường thứ hai là kênh có đệm một nghìn: mỗi luồng nhẹ gửi số một vào kênh, nên các luồng không chung một biến.""",
           focus=[0, ["2.3", "2.9"], ["2.4", "2.10"]], clear=True),
        st(code(G_KIEM, "main.go (tiếp): cộng các số trong kênh bằng một luồng", lines=(21, 28))
           + code(CMD_RACE2, "Chạy kèm cờ phát hiện tranh chấp"),
           """Chờ nhóm xong, ta đóng kênh rồi cộng mọi số trong kênh bằng một vòng lặp chạy ở một luồng duy nhất.
           Sau đó in cả hai kết quả, và ta chạy kèm cờ phát hiện tranh chấp, vì kết quả đúng chưa đủ để yên tâm.""",
           focus=[["2.1", "2.2", "2.3", "2.4", "2.5", "2.6"], ["2.7", "4.1"]], clear=True),
        st(out(OUT_KIEM) + table(["đường", "cách làm", "kết quả"],
                                 [["công thức", "$1000 \\cdot 1$", "1000"],
                                  ["có khoá (chạy thật)", "Lock và Unlock quanh dem++", "1000"],
                                  ["nguyên tử (chạy thật)", "bộ đếm atomic", "1000"],
                                  ["qua kênh (chạy thật)", "cộng các số gửi vào kênh", "1000"]]),
           """Kết quả chạy thật: cả hai đường đều ra một nghìn, và trình phát hiện không báo gì.
           Bảng đặt các đường cạnh nhau: công thức, khoá, bộ đếm nguyên tử và kênh, đều ra một nghìn.
           Vì bốn đường độc lập cùng cho một kết quả, và đường không khoá không bị báo tranh chấp, ta tin bộ đếm có khoá là đúng.""",
           focus=["2.1", "3.2", "3.5"], clear=True),
    ], checks=["alg.bnx_l20_locked(1000) == 1000 and alg.bnx_l20_locked(1000, 1) == 1000 * 1",
               "alg.bnx_l20_wg(1000, 1000) == 0", "alg.bnx_l20_range(1000)[1] == 1000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới, lúc mới dựng).</b> Bỏ qua lỗi bằng dấu gạch dưới: <code>so, _ := strconv.Atoi(...)</code>.
Chuỗi không phải số thì <b class="red">so = 0</b> và chương trình chạy tiếp với dữ liệu sai, không ai báo.
<br><span class="note">Cách chữa: nhận lỗi vào một biến, kiểm lỗi khác rỗng rồi xử lý hoặc trả lên trên.</span></div>""",
           """Lỗi thứ nhất, của người mới lúc mới dựng, là bỏ qua lỗi bằng dấu gạch dưới.
           Khi chuỗi không phải số, hàm đổi chuỗi thành số trả về không, và chương trình chạy tiếp với dữ liệu sai mà không ai báo.
           Cách chữa là nhận lỗi vào một biến rồi kiểm.""", clear=True),
        st(code(G_BOQUA, "main.go (trích): đổi chuỗi 12a thành số, hai cách", lines=(8, 13)) + out(OUT_BOQUA),
           """Chương trình nhỏ này đổi chuỗi một hai a thành số hai lần. Lần đầu ta vứt lỗi, lần sau ta giữ lỗi để in.
           Kết quả chạy thật: lần đầu in số không, và không ai biết có chuyện.
           Lần sau cũng số không, nhưng kèm lỗi nói rõ chuỗi này không phải số.""",
           focus=[0, ["2.2", "2.4"], "4.1", "4.2"], clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc tải tăng).</b> Mỗi yêu cầu sinh một luồng nhẹ gửi kết quả vào kênh <b>không đệm</b>.
Yêu cầu hết hạn, bên nhận đã bỏ đi: luồng nhẹ <b class="red">kẹt mãi</b>. Luồng nhẹ rẻ (ngăn xếp nhỏ, nhà phát triển Go nêu) nhưng không miễn phí: tải tăng thì số luồng kẹt tăng theo.
<br><span class="note">Cách chữa: cho bên gửi luôn có đường thoát, ví dụ kênh có đệm 1 để gửi xong rồi kết thúc.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, lộ ra lúc tải tăng. Mỗi yêu cầu sinh một luồng nhẹ để gửi kết quả vào kênh không đệm.
           Khi yêu cầu hết hạn thì bên nhận đã bỏ đi, và luồng nhẹ kẹt mãi. Luồng nhẹ rẻ, mỗi cái chỉ giữ một ngăn xếp nhỏ theo nhà phát triển ngôn ngữ, nhưng không miễn phí.
           Nên tải tăng thì số luồng kẹt tăng theo. Cách chữa là cho bên gửi luôn có đường thoát, ví dụ kênh có đệm một.""", clear=True),
        st(code(G_ROIRI, "main.go (trích): một nghìn yêu cầu, bên nhận đã bỏ đi", lines=(9, 16)),
           """Chương trình này mô phỏng điều đó. Với mỗi yêu cầu trong một nghìn yêu cầu, hàm tạo một kênh có sức chứa do ta chọn, rồi chạy một luồng nhẹ gửi một giá trị vào kênh, mà không ai nhận.
           Sau hai trăm mili giây, hàm đếm số luồng nhẹ còn sống.""",
           focus=[0, ["2.2", "2.3", "2.4", "2.5"], ["2.6", "2.7"]], clear=True),
        st(code(G_ROIRI, "main.go (tiếp): thử kênh đệm 1, rồi kênh không đệm", lines=(18, 21)) + out(OUT_ROIRI),
           """Hàm chính thử hai lần, trước với kênh đệm một, rồi với kênh không đệm.
           Kết quả chạy thật: kênh đệm một còn sống một luồng, chính là hàm chính, vì mọi luồng gửi đã xong.
           Kênh không đệm còn sống một nghìn không trăm linh một luồng, tức một nghìn luồng nhẹ kẹt cộng với hàm chính.""",
           focus=[["2.2", "2.3"], "4.1", "4.2"], clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Hai luồng nhẹ cùng ghi một <b>bảng tra</b> (map) dùng chung mà không khoá:
nhà phát triển Go nói <b class="red">không xác định chuyện gì xảy ra</b>. Kiểm thử đạt, chạy ổn nhiều tháng, rồi hỏng khi một đường mã hiếm gặp được chạy; trình phát hiện chỉ thấy đường <b>đã chạy</b>.
<br><span class="note">Cách chữa: khoá bảo vệ bảng tra (nhà phát triển Go nêu khoá đọc-ghi là một cách phổ biến) và luôn chạy kiểm thử kèm <code>-race</code>. Kênh để truyền giá trị, không thay được khoá cho trạng thái dùng chung.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm, lộ ra lúc vận hành lâu dài. Hai luồng nhẹ cùng ghi một bảng tra dùng chung mà không khoá, và nhà phát triển ngôn ngữ nói là không xác định chuyện gì sẽ xảy ra.
           Kiểm thử vẫn đạt, hệ thống chạy ổn nhiều tháng, rồi hỏng khi một đường mã hiếm được chạy, mà trình phát hiện chỉ thấy đường đã chạy.
           Cách chữa là thêm khoá, nhà phát triển ngôn ngữ nêu khoá đọc ghi là một cách phổ biến, và luôn chạy kiểm thử kèm cờ phát hiện tranh chấp.
           Kênh dùng để truyền giá trị giữa các luồng nhẹ, nhưng không thay được khoá cho trạng thái dùng chung.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc tải tăng, dùng Fiber).</b> Giữ lại giá trị đọc từ <code>c</code> (như <code>c.Params</code> hay thân yêu cầu) sau khi hàm xử lý trả về, hoặc đưa nó sang một luồng nhẹ khác. Fiber v2 <b class="red">dùng lại vùng nhớ</b> giữa các yêu cầu: giá trị cũ có thể thành dữ liệu của yêu cầu khác.
<br><span class="note">Cách chữa: sao chép ngay trong hàm xử lý (hàm copy, hoặc CopyString của gofiber/utils), hoặc bật cấu hình <code>Immutable</code>, đổi lại chậm hơn. Nhà phát triển Fiber ghi ở trang v2.x: chỉ dùng giá trị của ngữ cảnh trong hàm xử lý, không giữ tham chiếu.</span></div>""",
           """Lỗi thứ tư, của người đã đi làm, lộ ra lúc tải tăng khi dùng bộ khung web. Giá trị đọc từ ngữ cảnh yêu cầu, như tham số hay thân yêu cầu, được bộ khung dùng lại cho yêu cầu khác.
           Nếu ta giữ nó lại sau khi hàm xử lý xong, hoặc đưa sang luồng nhẹ khác, nó có thể đổi thành dữ liệu của yêu cầu khác.
           Cách chữa là sao chép ngay trong hàm xử lý, hoặc bật cấu hình làm giá trị bất biến, đổi lại chậm hơn.
           Điều này theo trang hướng dẫn của chính nhóm làm bộ khung, bản hai.""", clear=True),
    ], checks=["alg.bnx_l20_atoi('12a') == (0, True)", "alg.bnx_l20_leak(1000, True) == 1 and alg.bnx_l20_leak(1000, False) == 1001",
               "alg.bnx_l20_leak(1000, False) == 1 + 1000"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Kênh có đệm 5, gửi liền 8 giá trị, chưa ai nhận. Mấy giá trị vào được, và giá trị thứ mấy phải chờ?"],
                  ["2", "3 luồng nhẹ, mỗi luồng cộng 1 vào bộ đếm 0, không khoá (đọc rồi ghi). Bộ đếm cuối nhỏ nhất và lớn nhất là bao nhiêu? Một lần chạy ra đúng 3 có chứng minh không có tranh chấp không?"],
                  ["3", "Quyết định (số minh hoạ): 2 luồng nhẹ làm việc, mỗi việc 50 ms, tới 50 việc/giây. Chọn: mỗi yêu cầu một luồng nhẹ mới không giới hạn, kênh đệm 20 và bên gửi chờ khi đầy, hay kênh đệm 20 và bên gửi bị từ chối khi đầy?"]]),
           """Đến lượt bạn. Câu một, kênh có đệm năm, gửi liền tám giá trị mà chưa ai nhận, thì mấy giá trị vào được và giá trị thứ mấy phải chờ?
           Câu hai, ba luồng nhẹ cùng cộng một vào bộ đếm không, không khoá, thì kết quả nhỏ nhất và lớn nhất là bao nhiêu, và một lần ra đúng ba có chứng minh gì không?
           Câu ba, hai luồng nhẹ làm việc, mỗi việc năm mươi mili giây, mà mỗi giây tới năm mươi việc, bạn chọn trong ba cách xử lý trên màn hình cách nào?
           Hãy dừng video lại và làm từng câu ra giấy trước khi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: đệm 5 nhận 5 giá trị, giá trị kế tiếp phải chờ.</p>
$$5 \\text{ giá trị vào được}; \\qquad 5 + 1 = \\hlg{6} \\text{: bên gửi bị chặn ở giá trị thứ 6}$$""",
           """Đáp án câu một. Đệm năm nhận được năm giá trị. Bên gửi bị chặn ngay ở giá trị thứ sáu, nên các giá trị thứ bảy và thứ tám còn chưa được gửi."""),
        st("""<p>Câu 2: xen kẽ xấu nhất làm mất 2 lần cộng.</p>
$$\\text{nhỏ nhất } \\hlg{1}, \\quad \\text{lớn nhất } \\hlg{3}; \\qquad \\text{ra đúng } 3 \\text{ chỉ là một cách xen kẽ trong số nhiều cách}$$""",
           """Đáp án câu hai. Ba luồng cùng đọc không rồi ghi một, kết quả nhỏ nhất là một, lớn nhất là ba.
           Một lần ra đúng ba không chứng minh gì, vì đó chỉ là một trong nhiều cách xen kẽ có thể xảy ra, nên vẫn cần chạy trình phát hiện tranh chấp."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["mỗi yêu cầu một luồng nhẹ mới, không giới hạn", "không yêu cầu nào bị từ chối ngay",
                   "làm được $2 \\cdot 1000 : 50 = 40$ việc/giây, tới 50: dư 10 việc/giây, sau 60 giây có 600 việc dở, mỗi việc giữ một luồng nhẹ"],
                  ["kênh đệm 20, bên gửi chờ khi đầy", "việc được nhận chờ nhiều nhất $20 : 40 = 0{,}5$ giây; số việc dở có trần",
                   "bên gửi bị chặn, độ trễ lan ngược ra các yêu cầu tới"],
                  ["kênh đệm 20, đầy thì từ chối", "bên gọi biết ngay để thử lại sau; bộ nhớ có trần", "khoảng 10 việc/giây bị từ chối"]]),
           """Đáp án câu ba. Hai luồng làm bốn mươi việc mỗi giây, mà mỗi giây tới năm mươi, nên mỗi giây dư mười việc.
           Nếu mỗi yêu cầu một luồng nhẹ mới không giới hạn, sau một phút có sáu trăm việc dở, và mỗi việc giữ một luồng nhẹ.
           Kênh đệm hai mươi cho việc chờ tối đa nửa giây, nhưng nếu bên gửi chờ khi đầy thì độ trễ lan ngược ra các yêu cầu tới.
           Đầy thì từ chối làm khoảng mười việc mỗi giây bị từ chối, đổi lại bên gọi biết ngay.
           Với giao dịch ngân hàng, thường chọn giới hạn rồi từ chối sớm, vì khách không chờ lâu được.""",
           focus=[0, "1.2", "1.3", "1.4", "1.4"]),
    ], checks=["alg.bnx_l20_accept(5, 8) == (5, 6)", "alg.bnx_l20_range(3) == (1, 3)",
               "alg.bnx_l20_interleave(['A', 'A', 'B', 'B', 'C', 'C']) == 3",
               "alg.bnx_l20_thru(2, 50) == 40", "(50 - alg.bnx_l20_thru(2, 50)) * 60 == 600",
               "alg.bnx_l20_wait(20, alg.bnx_l20_thru(2, 50)) == 0.5"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("luồng nhẹ + nhóm chờ", "chung một biến thì khoá", "kênh: gửi chờ khi đệm đầy", "lỗi là giá trị phải kiểm", "dịch vụ HTTP: tuyến → hàm xử lý"),
           """Tổng kết chuỗi logic. Luồng nhẹ chạy việc cùng lúc, và nhóm chờ cho hàm chính đợi xong.
           Hai luồng nhẹ cùng ghi một biến thì cần khoá, và trình phát hiện tranh chấp giúp bắt lỗi.
           Kênh truyền giá trị, và bên gửi chờ khi đệm đầy. Lỗi là giá trị phải kiểm, còn dịch vụ HTTP là tuyến nối với hàm xử lý."""),
        st("""<div class='box key'><b>Tư duy:</b> rẻ không có nghĩa là miễn phí, và chạy đúng một lần không có nghĩa là đúng.
Với mỗi luồng nhẹ hãy hỏi: nó kết thúc ra sao, nó chạm biến dùng chung nào, và lỗi của nó đi đâu.</div>""",
           """Điều cần mang theo. Rẻ không có nghĩa là miễn phí, và chạy đúng một lần không có nghĩa là đúng.
           Với mỗi luồng nhẹ, hãy hỏi nó kết thúc ra sao, nó chạm biến dùng chung nào, và lỗi của nó đi đâu."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Luồng nhẹ (goroutine) khác luồng hệ điều hành thế nào, có miễn phí không?",
                   "rẻ hơn: ngăn xếp nhỏ, nhà phát triển Go nêu chỉ vài kilô-byte, và nhiều luồng nhẹ chạy chung trên ít luồng hệ điều hành (việc nào chặn thì bộ lập lịch của Go chuyển việc khác); nhưng không miễn phí, và vẫn rò rỉ nếu bên gửi không có đường thoát"],
                  ["Kênh có đệm và không đệm khác nhau thế nào, khi nào bên gửi bị chặn?",
                   "không đệm: gửi chờ tới khi có bên nhận; đệm n: gửi chờ khi đã đầy n giá trị. Trạng thái dùng chung thì cần khoá"],
                  ["Fiber thêm gì so với net/http, và lỗi được xử lý ra sao?",
                   "bộ khung dựng trên fasthttp: tuyến có tham số, trả JSON gọn; giá trị lấy từ ngữ cảnh chỉ dùng trong hàm xử lý. Lỗi là giá trị trả về, nên phải kiểm trước khi chạy tiếp"]]),
           """Nếu người phỏng vấn hỏi về dòng ngôn ngữ thứ hai và bộ khung web trên hồ sơ, đây là ba câu hay gặp.
           Luồng nhẹ khác luồng hệ điều hành ở chỗ rẻ hơn và chạy chung trên ít luồng hệ điều hành, nhưng không miễn phí và vẫn rò rỉ được.
           Kênh không đệm bắt bên gửi chờ bên nhận, còn kênh có đệm chỉ bắt chờ khi đã đầy.
           Bộ khung web dựng trên một thư viện khác, thêm tuyến có tham số, giá trị từ ngữ cảnh chỉ dùng trong hàm xử lý, còn lỗi luôn là giá trị phải kiểm.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Bài sau: hệ thống cho vay số, một hồ sơ vay đi qua <b>chấm điểm, thẩm định, ký số</b> và chống gian lận thế nào.</p>""",
           """Ở bài hai mươi mốt, ta đi qua vòng đời một hồ sơ vay số, từ chấm điểm và thẩm định tới ký số và chống gian lận.""",
           forward_ref=True),
    ], checks=["alg.bnx_l20_locked(1000) == 1000", "alg.bnx_l20_accept(3, 4) == (3, 4)"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
    return lesson("L20", "go_goroutine_kenh_http",
                  "Bài 20 — Go cho backend: goroutine, kênh, tranh chấp dữ liệu và một dịch vụ HTTP nhỏ",
                  "curriculum/bnx.yaml L20; audit/bnx/verify_bnx.py L20; audit/bnx/sources_l20.md: tài liệu chính thức của Go (đặc tả ngôn ngữ, "
                  "gói sync, bài về trình phát hiện tranh chấp, Effective Go, Go FAQ, blog về map và về bộ định tuyến Go 1.22) và tài liệu Fiber "
                  "(đọc 2026-11-12); mã chạy thật go1.25.5 windows/amd64, Fiber v2.52.16",
                  ["Đọc và chạy một chương trình Go có hàm, cấu trúc và xử lý lỗi bằng giá trị trả về",
                   "Chạy nhiều goroutine và gom kết quả bằng nhóm chờ",
                   "Truyền dữ liệu qua kênh có đệm và không đệm, nói lúc nào bên gửi bị chặn",
                   "Viết một dịch vụ HTTP nhỏ và nói bộ khung Fiber thêm gì lên trên"],
                  scenes)
