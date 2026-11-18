import lib2
from lib2 import *
from libj import jstep, nowrap
from spoken_b import _spoken
from labkit import write_lab, practice_scene

lib2.begin("L20")

# ── Mã Go hiện trên màn hình (AF2, nhánh B: viết gọn để mỗi chương trình ≤ 24 dòng, hiện đủ package/import, chia tối đa 2 khung ≤ 12 dòng).
#    Mỗi chương trình Go là một prog(kind="other") (nguồn ghi vào thư mục chạy); chương trình bash đi kèm chạy `go run` trên nó và cho đầu ra THẬT.
#    Đầu ra viết không dấu (ASCII). Thụt lề 2 dấu cách (đúng cú pháp, không qua gofmt); dấu chấm phẩy ngăn các mục cùng dòng là cú pháp hợp lệ của Go. ──
_GO_REASON = "Chương trình Go đầy đủ của bài (màn hình hiện từng đoạn liên tiếp); chạy thật bằng `go run main.go` ở chương trình bash đi kèm."
_GO_CHECK = "Biên dịch và chạy cùng chương trình bash đi kèm (khối `files`), khớp từng ký tự đầu ra; Go 1.25.5."

GO_LOI = prog("goLoi", r'''
package main
import ("errors"; "fmt")
type TaiKhoan struct{ So string; SoDu int }
func rut(tk TaiKhoan, tien int) (TaiKhoan, error) {
  if tien > tk.SoDu {
    return tk, errors.New("khong du so du")
  }
  tk.SoDu -= tien
  return tk, nil
}
func main() {
  tk := TaiKhoan{So: "001", SoDu: 500}
  for _, tien := range []int{200, 400} {
    moi, err := rut(tk, tien)
    if err != nil {
      fmt.Println("rut", tien, "loi:", err, "- so du van", tk.SoDu)
      continue
    }
    tk = moi
    fmt.Println("rut", tien, "xong, con", tk.SoDu)
  }
}
''', lang="go", kind="other", reason=_GO_REASON, read_check=_GO_CHECK)
R_LOI = prog("Loi", "go run main.go", lang="bash", files={"main.go": "goLoi"}, timeout=240,
             claims=["rút 200 xong còn 300; rút 400 báo không đủ số dư và số dư vẫn 300"])

GO_DEM = prog("goDem", r'''
package main
import ("fmt"; "sync")
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
  fmt.Println("bo dem:", dem)
}
''', lang="go", kind="other", reason=_GO_REASON, read_check=_GO_CHECK)
R_DEM = prog("Dem", "go run main.go", lang="bash", files={"main.go": "goDem"}, timeout=240,
             claims=["một nghìn luồng nhẹ, mỗi luồng cộng một trong khoá, bộ đếm đúng 1000"])

GO_KHONG = prog("goKhong", r'''
package main
import ("fmt"; "sync")
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
  fmt.Println("bo dem:", dem)
}
''', lang="go", kind="other", reason="Biến thể không khoá của goDem; kết quả ngẫu nhiên nên bài chỉ chạy nó với cờ -race (chương trình bash Race) và lấy hai dòng cố định.", read_check=_GO_CHECK)
CMD_RACE = 'go run -race main.go 2>&1 | grep -E "DATA RACE|exit status" | uniq'
R_RACE = prog("Race", CMD_RACE, lang="bash", files={"main.go": "goKhong"}, timeout=400,
              claims=["bỏ khoá: trình phát hiện tranh chấp báo WARNING: DATA RACE và thoát với mã 66"])

GO_KENH = prog("goKenh", r'''
package main
import "fmt"
func thuGui(ch chan int, v int) {
  select {
  case ch <- v:
    fmt.Println("gui", v, "xong, dang chua", len(ch))
  default:
    fmt.Println("gui", v, "phai cho ben nhan")
  }
}
func main() {
  ch := make(chan int, 3)
  for v := 1; v <= 4; v++ {
    thuGui(ch, v)
  }
  fmt.Println("nhan", <-ch)
  thuGui(ch, 4)
  khong := make(chan int)
  thuGui(khong, 1)
}
''', lang="go", kind="other", reason=_GO_REASON, read_check=_GO_CHECK)
R_KENH = prog("Kenh", "go run main.go", lang="bash", files={"main.go": "goKenh"}, timeout=240,
              claims=["kênh đệm 3 nhận 3 giá trị, giá trị thứ 4 phải chờ; sau khi nhận một thì gửi được; kênh không đệm gửi phải chờ"])

GO_HTTP = prog("goHttp", r'''
package main
import ("fmt"; "io"; "net"; "net/http"; "strings")
func sucKhoe(w http.ResponseWriter, r *http.Request) {
  w.Header().Set("Content-Type", "application/json")
  fmt.Fprint(w, `{"trang_thai":"ok"}`)
}
func main() {
  mux := http.NewServeMux()
  mux.HandleFunc("GET /suc-khoe", sucKhoe)
  ln, _ := net.Listen("tcp", "127.0.0.1:0")
  go http.Serve(ln, mux)
  goc := "http://" + ln.Addr().String()
  for _, yc := range []string{"GET /suc-khoe", "POST /suc-khoe", "GET /khong-co"} {
    pt, duong, _ := strings.Cut(yc, " ")
    req, _ := http.NewRequest(pt, goc+duong, nil)
    tl, err := http.DefaultClient.Do(req)
    if err != nil {
      fmt.Println("loi goi:", err)
      return
    }
    than, _ := io.ReadAll(tl.Body); tl.Body.Close()
    fmt.Println(yc, tl.StatusCode, strings.TrimSpace(string(than)))
  }
}
''', lang="go", kind="other", reason=_GO_REASON, read_check=_GO_CHECK)
R_HTTP = prog("Http", "go run main.go", lang="bash", files={"main.go": "goHttp"}, timeout=240,
              claims=["GET /suc-khoe trả 200 với JSON; POST trả 405; đường dẫn lạ trả 404"])

_FIBER_DIR = "D:/research-video/audit/bnx/deps/l20/fiber"
GO_FIBER = prog("goFiber", r'''
package main
import ("fmt"; "io"; "net"; "net/http"; "github.com/gofiber/fiber/v2")
func main() {
  app := fiber.New(fiber.Config{DisableStartupMessage: true})
  app.Get("/suc-khoe", func(c *fiber.Ctx) error {
    return c.JSON(fiber.Map{"trang_thai": "ok"})
  })
  app.Get("/tai-khoan/:so", func(c *fiber.Ctx) error {
    return c.JSON(fiber.Map{"so": c.Params("so")})
  })
  ln, _ := net.Listen("tcp", "127.0.0.1:0")
  go app.Listener(ln)
  goc := "http://" + ln.Addr().String()
  for _, duong := range []string{"/suc-khoe", "/tai-khoan/001"} {
    tl, err := http.Get(goc + duong)
    if err != nil {
      fmt.Println("loi goi:", err)
      return
    }
    than, _ := io.ReadAll(tl.Body); tl.Body.Close()
    fmt.Println(duong, tl.StatusCode, string(than))
  }
  app.Shutdown()
}
''', lang="go", kind="other",
    reason="main.go của mô-đun Fiber v2.52.16 ở audit/bnx/deps/l20/fiber (chép nguyên văn vào đó lúc import, ver/l20.py so từng byte); cần mô-đun ngoài nên chương trình bash `go run .` chạy ngay trong thư mục ấy.",
    read_check="Chạy bằng chương trình bash đi kèm (`go run .` trong audit/bnx/deps/l20/fiber, mô-đun nằm trong bộ nhớ đệm Go); khớp từng ký tự đầu ra.")
try:
    _fd = lib2.ROOT / "audit" / "bnx" / "deps" / "l20" / "fiber"
    if _fd.exists():
        (_fd / "main.go").write_text(GO_FIBER.code + "\n", encoding="utf-8", newline="\n")
except OSError:
    pass
R_FIBER = prog("Fiber", f'cd "{_FIBER_DIR}" && go run .', lang="bash", timeout=400,
               claims=["hai tuyến Fiber trả 200: /suc-khoe và /tai-khoan/001 với tham số đường dẫn"])

GO_BOQUA = prog("goBoqua", r'''
package main
import ("fmt"; "strconv")
func main() {
  so, _ := strconv.Atoi("12a")
  fmt.Println("bo qua loi, so doc duoc:", so)
  so, err := strconv.Atoi("12a")
  fmt.Println("kiem loi:", so, err)
}
''', lang="go", kind="other", reason=_GO_REASON, read_check=_GO_CHECK)
R_BOQUA = prog("Boqua", "go run main.go", lang="bash", files={"main.go": "goBoqua"}, timeout=240,
               claims=["bỏ qua lỗi thì số đọc được là 0 mà không ai biết; kiểm lỗi thấy parsing error"])

GO_ROIRI = prog("goRoiri", r'''
package main
import ("fmt"; "runtime"; "time")
func thu(dem int) int {
  for i := 0; i < 1000; i++ {
    kq := make(chan int, dem)
    go func() { kq <- i }() // ben nhan da bo di, khong ai nhan
  }
  time.Sleep(200 * time.Millisecond)
  return runtime.NumGoroutine()
}
func main() {
  fmt.Println("kenh dem 1, con song:", thu(1))
  fmt.Println("kenh khong dem, con song:", thu(0))
}
''', lang="go", kind="other", reason=_GO_REASON, read_check=_GO_CHECK)
R_ROIRI = prog("Roiri", "go run main.go", lang="bash", files={"main.go": "goRoiri"}, timeout=240,
               claims=["kênh đệm 1: còn sống 1 luồng; kênh không đệm: còn sống 1001 luồng nhẹ (rò rỉ)"])

GO_KIEM = prog("goKiem", r'''
package main
import ("fmt"; "sync"; "sync/atomic")
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
  for v := range ch { tong += v }
  fmt.Println("atomic:", a.Load(), "- qua kenh:", tong)
}
''', lang="go", kind="other", reason=_GO_REASON, read_check=_GO_CHECK)
R_KIEM = prog("Kiem", "go run main.go", lang="bash", files={"main.go": "goKiem"}, timeout=240,
              claims=["đếm bằng bộ đếm nguyên tử và bằng kênh đều ra 1000"])

# ── Quy mô: nhiều luồng nhẹ cùng chờ, đo ngăn xếp (StackInuse) thật ở 1 000, 10 000, 100 000 ──
GO_Q = prog("goQuymo", r'''
package main
import ("fmt"; "runtime"; "sync")
func chay(n int) {
  var truoc, sau runtime.MemStats
  runtime.ReadMemStats(&truoc)
  cho := make(chan struct{})
  var xong sync.WaitGroup
  for i := 0; i < n; i++ {
    xong.Add(1)
    go func() { defer xong.Done(); <-cho }()
  }
  runtime.ReadMemStats(&sau)
  kb := (sau.StackInuse - truoc.StackInuse) / uint64(n) / 1000
  song := runtime.NumGoroutine() - 1
  fmt.Println(n, "luong:", song, "con song, moi luong giu", kb, "nghin byte")
  close(cho)
  xong.Wait()
}
func main() {
  for _, n := range []int{1000, 10000, 100000} {
    chay(n)
  }
}
''', lang="go", kind="other", reason=_GO_REASON, read_check=_GO_CHECK)
R_Q = prog("QuyMo", "go run main.go", lang="bash", files={"main.go": "goQuymo"}, timeout=400,
           claims=["1 000, 10 000, 100 000 luồng nhẹ cùng chờ: mỗi luồng giữ 8, 7, 7 nghìn byte ngăn xếp (đo trên máy này, Go 1.25.5, Windows; làm tròn xuống nghìn byte để đầu ra tất định)"])

# ── Lab (Go qua tệp .sh: cham.sh chấm .sh; người học cần Go: go.dev/dl) ──
LAB_SH = r'''
cat > main.go <<'GO'
package main
import ("fmt"; "sync")
func thuGui(ch chan int, v int) {
  select {
  case ch <- v:
    fmt.Println("gui", v, "xong, dang chua", len(ch))
  default:
    fmt.Println("gui", v, "phai cho ben nhan")
  }
}
func main() {
  var nhom sync.WaitGroup
  var khoa sync.Mutex
  dem := 0
  for i := 0; i < 5; i++ {
    nhom.Add(1)
    go func() {
      defer nhom.Done()
      khoa.Lock()
      dem += 100
      khoa.Unlock()
    }()
  }
  nhom.Wait()
  fmt.Println("bo dem:", dem)
  ch := make(chan int, 2)
  for v := 1; v <= 3; v++ {
    thuGui(ch, v)
  }
  fmt.Println("nhan", <-ch)
  thuGui(ch, 3)
}
GO
go run main.go
'''
LAB = prog("LabL20", LAB_SH, lang="bash", timeout=240)
LAB_DE = """# Lab BNX L20 — Luồng nhẹ, khoá và kênh có đệm (cần Go)

Lab này cần Go (tải ở https://go.dev/dl/, bản 1.21 trở lên; kiểm bằng `go version` trong Git Bash). Số liệu là số minh hoạ, khác ví dụ trong bài.

Viết chương trình Go `main.go` làm hai việc, rồi gói vào tệp `mau.sh` theo khuôn dưới để chấm bằng `cham.sh` (tệp `mau.sh` tạo `main.go` rồi chạy nó):

```bash
cat > main.go <<'GO'
... chương trình Go của bạn ...
GO
go run main.go
```

1. **Bộ đếm có khoá**: chạy **5 luồng nhẹ** (`go func() {...}()`), mỗi luồng cộng **100** vào một bộ đếm chung trong khoá `sync.Mutex`; dùng `sync.WaitGroup` để chờ đủ 5 luồng. In `bo dem: <số>`.
2. **Kênh có đệm 2**: tạo `ch := make(chan int, 2)`. Với mỗi `v` từ 1 tới 3 thử gửi **không chờ** bằng `select { case ch <- v: ... default: ... }`: gửi được thì in `gui <v> xong, dang chua <len(ch)>`, đầy thì in `gui <v> phai cho ben nhan`. Rồi nhận một giá trị và in `nhan <giá trị>`, rồi thử gửi lại giá trị 3 theo cách trên.

Chạy: `bash mau.sh`. Chấm: `bash labs/cham.sh BNX L20 mau.sh`.
"""


def build():
    write_lab("BNX", "L20", LAB_DE, "sh", LAB_SH, LAB.out)
    hook = sc("hook", "hook", "Một nghìn yêu cầu cùng cộng một bộ đếm: ra 1000 hay ít hơn?", [
        st("""<p>Dịch vụ ngân hàng đếm số yêu cầu đã xử lý. <b>Một nghìn</b> yêu cầu tới cùng lúc, mỗi yêu cầu cộng 1 vào <b>một bộ đếm chung</b> (số minh hoạ).</p>
<div class="box key">Kỳ vọng: $1000 \\cdot 1 = 1000$. Bỏ khoá, chạy thật thì bộ đếm <b>có lần thấp hơn 1000</b>, mỗi lần chạy một khác, và không lần nào chắc chắn đúng.
Vì sao, chữa thế nào, và khi số việc chạy cùng lúc tăng gấp trăm lần thì bộ nhớ ra sao?</div>""",
           """Chào bạn, hãy tưởng tượng dịch vụ của ngân hàng đếm số yêu cầu đã xử lý. Một nghìn yêu cầu tới cùng lúc, mỗi yêu cầu cộng một vào một bộ đếm chung, với số minh hoạ. Ta kỳ vọng đúng một nghìn, nhưng bỏ khoá thì có lần thấp hơn. Vì sao, và chữa thế nào?""",
           focus=[1, 1, 2, 2]),
    ], checks=["alg.bnx_l20_locked(1000) == 1000", "alg.bnx_l20_range(1000) == (1, 1000)"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① biến dùng chung", "một ô nhớ mà nhiều việc cùng đọc và ghi được", "bộ đếm = 0; hai việc cùng cộng 1"],
                  ["② đọc rồi ghi", "câu lệnh tăng một gồm <b>hai bước</b>: đọc giá trị, rồi ghi giá trị cộng 1", "A đọc 0, B đọc 0, A ghi 1, B ghi 1 → bộ đếm <b>1</b> thay vì 2; A làm trọn rồi mới tới B thì ra 2"],
                  ["③ hàm trả nhiều giá trị", "một hàm trả cả kết quả lẫn lỗi; lỗi rỗng (nil) nghĩa là không có lỗi", "rút 200 từ số dư 500 trả (300, không lỗi)"],
                  ["④ yêu cầu và trả lời HTTP", "yêu cầu có phương thức và đường dẫn; trả lời có mã trạng thái và thân", "GET /suc-khoe trả mã 200"]]),
           """Trước hết ta cần hiểu bốn điều. Biến dùng chung là một ô nhớ mà nhiều việc cùng đọc và ghi được. Lệnh tăng một gồm hai bước, đọc rồi ghi, nên nếu A và B cùng đọc không rồi cùng ghi một, bộ đếm chỉ là một thay vì hai. Hàm có thể trả về cả kết quả lẫn lỗi, và yêu cầu HTTP có phương thức và đường dẫn.""",
           focus=[0, "1.2", "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_l20_interleave(['A', 'B', 'A', 'B']) == 1", "alg.bnx_l20_interleave(['A', 'A', 'B', 'B']) == 2",
               "alg.bnx_l20_lost(['A', 'B', 'A', 'B']) == 1", "alg.bnx_l20_rut(500, 200) == (300, None)",
               "alg.bnx_l20_route('GET', '/suc-khoe')[0] == 200"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên trong Go", "nghĩa"],
                 [["go f()", "chạy hàm f ở một <b>luồng nhẹ</b> (goroutine) riêng; chương trình không chờ nó"],
                  ["sync.WaitGroup", "<b>nhóm chờ</b>: <code>Add</code> cộng số việc, <code>Done</code> trừ một, <code>Wait</code> chờ tới khi về 0"],
                  ["sync.Mutex", "<b>khoá</b>: giữa <code>Lock</code> và <code>Unlock</code> một lúc chỉ một luồng nhẹ được vào"],
                  ["chan int, ch &lt;- v, &lt;-ch", "<b>kênh</b> truyền số nguyên: <code>make(chan int, 3)</code> có đệm 3, <code>make(chan int)</code> không đệm; gửi v vào kênh; nhận một giá trị"],
                  ["select … default", "thử gửi hay nhận <b>mà không bị treo</b>: không làm được ngay thì chạy nhánh <code>default</code>"],
                  ["error, nil", "lỗi là một <b>giá trị</b> được trả về; <code>nil</code> nghĩa là không có lỗi"],
                  ["go run -race", "chạy kèm <b>trình phát hiện tranh chấp dữ liệu</b>"],
                  ["net/http, Fiber", "gói chuẩn dựng dịch vụ HTTP; Fiber là bộ khung web thêm cách viết tuyến"]]),
           """Bảng này giải mã các tên trên màn hình. Lệnh đầu chạy một hàm ở luồng nhẹ riêng, và nhóm chờ chờ tới khi số việc về không. Khoá cho một lúc chỉ một luồng nhẹ vào. Kênh truyền giá trị, con số trong ngoặc là sức chứa của đệm, và thử gửi không treo dùng nhánh mặc định. Lỗi là một giá trị được trả về.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"],
           introduces=["bnx_goroutine", "bnx_waitgroup", "bnx_mutex", "bnx_fiber", "bnx_tranh_chap"]),
        st(table(["cú pháp Go", "nghĩa"],
                 [["<code>x := 5</code>", "khai báo biến mới <code>x</code> và gán 5 (kiểu tự suy ra)"],
                  ["<code>defer nhom.Done()</code>", "hoãn lệnh này tới lúc hàm kết thúc, dù kết thúc bình thường hay không"],
                  ["<code>func() { … }()</code>, <code>for _, v := range ds</code>", "hàm không tên gọi ngay tại chỗ / lặp qua từng phần tử (hoặc nhận lần lượt từ kênh tới khi kênh đóng), <code>_</code> là chỗ bỏ qua giá trị không cần"],
                  ["<code>type TaiKhoan struct {…}</code>, <code>&amp;x</code>", "cấu trúc: gom nhiều trường thành một kiểu / địa chỉ của biến <code>x</code>"],
                  ["<code>go run main.go</code>, <code>2&gt;&amp;1 | grep … | uniq</code>", "biên dịch và chạy một tệp Go (cần cài Go) / nối đầu ra qua ống: lọc dòng có chữ cần tìm, bỏ dòng lặp liền nhau"]]),
           """Dấu hai chấm bằng khai báo biến mới, và lệnh hoãn chạy lúc hàm kết thúc. Hàm không tên gọi tại chỗ, còn vòng lặp đi qua từng phần tử hoặc nhận từ kênh tới khi kênh đóng. Cấu trúc gom trường, rồi tới lệnh chạy chương trình Go.""", clear=True, introduces=["bnx_go_defer"]),
        st(table(["cú pháp Go", "nghĩa"],
                 [["<code>package main</code>, <code>import (…)</code>", "chương trình chạy được của Go mở đầu bằng <code>package main</code>; <code>import</code> nạp các gói dùng tới, như <code>fmt</code> để in"],
                  ["<code>fmt.Println(a, b)</code>", "in các giá trị a, b ra màn hình, cách nhau một dấu cách"],
                  ["<code>if err != nil { … }</code>", "nếu lỗi khác rỗng thì làm khối bên trong; <code>!=</code> nghĩa là khác"],
                  ["<code>[]int{200, 400}</code>, <code>len(ch)</code>", "danh sách số nguyên gồm 200 và 400 / số giá trị đang nằm trong kênh <code>ch</code>"],
                  ["<code>continue</code>, <code>uint64(n)</code>", "bỏ phần còn lại của vòng này, sang vòng sau / đổi n sang số nguyên không âm 64 bit"],
                  ["<code>chan struct{}</code>", "kênh chỉ để báo hiệu, không mang dữ liệu"]]),
           """Còn một bảng cú pháp Go nền. Chương trình mở đầu bằng khai báo gói và nạp các gói cần dùng. Dấu khác so sánh lỗi với rỗng, ngoặc vuông kèm kiểu là một danh sách, và lệnh bỏ qua sang vòng sau dùng khi gặp lỗi.""", clear=True),
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
           """Hình này cho thấy vì sao bộ đếm sai. Hàng trên không có khoá nên B đọc không khi A chưa ghi, cả hai ghi một, và mất một lần cộng. Hàng dưới có khoá nên A làm trọn vẹn rồi B mới vào, không mất lần nào."""),
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
           """Hình thứ hai là kênh. Kênh không đệm thì bên gửi chỉ xong khi có bên nhận sẵn sàng. Kênh có đệm ba nhận ba giá trị đầu ngay mà không chờ ai, còn giá trị thứ bốn thấy đệm đầy nên phải chờ."""),
        st(svg(1500, 470,
               txt(750, 34, "Một dịch vụ HTTP nhỏ và bộ khung web đứng trên", 26, "middle", "#1f2937", True),
               box(40, 70, 260, 90, ["khách", "GET /suc-khoe"], C_BLUE, 22), arrow(300, 115, 400, 115),
               box(400, 70, 300, 90, ["bộ định tuyến", "tìm tuyến khớp"], C_AMBER, 22), arrow(700, 115, 800, 115),
               box(800, 70, 260, 90, ["hàm xử lý", "sucKhoe"], C_GREEN, 22), arrow(1060, 115, 1130, 115),
               box(1130, 70, 330, 90, ["mã 200", "thân JSON"], C_PURPLE, 22),
               txt(1295, 195, "JSON: chữ gồm cặp tên và giá trị", 20, "middle", "#6b7280"),
               panel(40, 210, 1420, 200, "Bộ khung web (Fiber) đứng trên cùng", C_GRAY, 26),
               box(70, 270, 420, 110, ["tuyến có tham số", "/tai-khoan/:so"], C_BLUE, 22),
               box(540, 270, 420, 110, ["trả JSON gọn", "c.JSON(...)"], C_GREEN, 22),
               box(1010, 270, 420, 110, ["dựng trên fasthttp", "(nhà phát triển Fiber nêu)"], C_AMBER, 22),
               txt(750, 450, "Cùng một chuyện: yêu cầu đi vào, tìm tuyến, hàm xử lý trả lời đi ra", 24, "middle", "#1f2937", True)),
           """Hình thứ ba là dịch vụ HTTP nhỏ. Khách gửi phương thức đọc cùng đường dẫn, bộ định tuyến tìm tuyến khớp rồi gọi hàm xử lý, hàm ấy ghi mã hai trăm cùng thân JSON, tức chữ gồm các cặp tên và giá trị."""),
    ], checks=["alg.bnx_l20_interleave(['A', 'B', 'A', 'B']) == 1", "alg.bnx_l20_interleave(['A', 'A', 'B', 'B']) == 2",
               "alg.bnx_l20_accept(3, 4) == (3, 4)", "alg.bnx_l20_route('GET', '/suc-khoe')[0] == 200",
               "alg.bnx_l20_fiber_route('/tai-khoan/001')[0] == 200"])

    form = sc("formula", "formula", "Suy ra từng bước: từ luồng nhẹ tới dịch vụ HTTP", [
        st("""<p><b>Bước 1.</b> Lệnh <code>go f()</code> chạy <code>f</code> ở luồng nhẹ riêng rồi trở về ngay, nên hàm chính có thể kết thúc <b>trước</b> các việc.
Vì vậy ta dùng nhóm chờ: <code>Add(1)</code> trước mỗi việc, <code>Done()</code> khi việc xong, <code>Wait()</code> chờ tới khi số việc về 0.</p>
<p>Làm thử: 3 lần Add, 2 lần Done.</p>
$$3 - 2 = \\hl{1} \\neq 0 \\;\\Rightarrow\\; \\text{Wait vẫn chờ}; \\qquad 1000 - 1000 = 0 \\;\\Rightarrow\\; \\text{Wait trở về}$$""",
           """Bước một, lệnh chạy ở luồng nhẹ trở về ngay nên hàm chính có thể kết thúc trước các việc, nên ta dùng nhóm chờ. Cộng một trước mỗi việc, trừ một khi xong, và lệnh chờ chỉ trở về khi số việc về không.""", clear=True),
        st("""<p><b>Bước 2.</b> Hai luồng nhẹ cùng ghi một biến mà không phối hợp là <b>tranh chấp dữ liệu</b>.
Vì tăng một gồm đọc rồi ghi, nên một lần cộng có thể bị ghi đè, và bộ đếm cuối nằm giữa 1 và số luồng.</p>
<p>Làm thử: 3 luồng cùng cộng 1 vào 0, không khoá.</p>
$$\\text{nhỏ nhất } \\hl{1}, \\quad \\text{lớn nhất } 3; \\qquad \\text{chỉ khi xen kẽ vừa vặn mới ra } 3$$""",
           """Bước hai, hai luồng cùng ghi một biến mà không phối hợp gọi là tranh chấp dữ liệu. Vì tăng một gồm đọc rồi ghi nên một lần cộng có thể bị ghi đè, và với ba luồng, bộ đếm cuối nằm giữa một và ba.""", clear=True),
        st("""<p><b>Bước 3.</b> Khoá biến đọc-rồi-ghi thành một khối: giữa <code>Lock</code> và <code>Unlock</code> một lúc chỉ một luồng nhẹ, nên không lần cộng nào bị mất.</p>
<p>Làm thử: 1000 luồng nhẹ, mỗi luồng cộng 1 trong khoá.</p>
$$1000 \\cdot 1 = \\hlg{1000} \\quad \\text{(mọi lần chạy)}$$
<span class='note'>Đổi lại, các luồng xếp hàng qua khoá, nên đoạn nằm trong khoá càng ngắn càng tốt.</span>""",
           """Bước ba, khoá làm đọc rồi ghi thành một khối, vì giữa lệnh khoá và lệnh mở một lúc chỉ một luồng được vào. Nên một nghìn luồng cộng một ra đúng một nghìn ở mọi lần chạy, và đoạn nằm trong khoá càng ngắn càng tốt.""", clear=True),
        st("""<p><b>Bước 4.</b> Trình phát hiện tranh chấp: chạy <code>go run -race</code>. Nó báo khi hai luồng nhẹ truy cập cùng một biến, ít nhất một lần là ghi, mà không phối hợp.
Nó chỉ thấy tranh chấp trên đường mã <b>đã chạy</b>, và làm chương trình chậm hơn.</p>
<div class="box key">Khi thấy tranh chấp, nó in cảnh báo rồi thoát với mã <b>66</b> (mặc định). Một lần in đúng kết quả chưa chứng minh là không có tranh chấp.</div>
<span class='note'>Trên máy chạy bài này (Windows), cờ <code>-race</code> cần bật cgo (cho Go gọi mã C) và có trình biên dịch C tên gcc; máy khác có thể khác.</span>""",
           """Bước bốn, trình phát hiện tranh chấp bắt lỗi ấy. Nó chỉ thấy trên đường mã đã chạy nên một lần in đúng chưa chứng minh gì, và khi thấy nó thoát với mã sáu mươi sáu.""", clear=True),
        st("""<p><b>Bước 5.</b> Kênh truyền giá trị giữa các luồng nhẹ. <b>Không đệm</b>: bên gửi chờ tới khi có bên nhận. <b>Có đệm n</b>: gửi xong ngay nếu đệm chưa đầy, đầy thì chờ.</p>
<p>Làm thử: đệm 2, gửi liền 3 giá trị, chưa ai nhận.</p>
$$2 \\text{ giá trị vào đệm}; \\qquad 2 + 1 = \\hl{3} \\text{: giá trị thứ 3 phải chờ}$$""",
           """Bước năm, kênh truyền giá trị giữa các luồng. Kênh không đệm thì bên gửi chờ tới khi có bên nhận, còn kênh đệm n thì gửi xong ngay nếu chưa đầy. Với đệm hai và ba giá trị gửi liền, hai giá trị vào đệm nên giá trị thứ ba phải chờ.""", clear=True),
        st("""<p><b>Bước 6.</b> Cách báo lỗi thông thường: hàm trả <b>thêm một giá trị lỗi</b>, bên gọi phải tự kiểm. Lỗi rỗng là thành công. Bỏ qua lỗi thì chương trình chạy tiếp với giá trị không.</p>
<p>Làm thử: tài khoản 500, rút 200 rồi rút 400.</p>
$$500 - 200 = 300; \\qquad 400 > 300 \\;\\Rightarrow\\; \\text{lỗi, số dư vẫn } \\hl{300}$$""",
           """Bước sáu, hàm trả thêm một giá trị lỗi và bên gọi phải tự kiểm, vì bỏ qua lỗi thì chương trình chạy tiếp với giá trị không. Rút hai trăm từ năm trăm còn ba trăm, và rút bốn trăm thì có lỗi, nên số dư vẫn là ba trăm.""", clear=True),
        st("""<p><b>Bước 7.</b> Dịch vụ HTTP nhỏ đăng ký tuyến <code>GET /suc-khoe</code> với một hàm xử lý. Gói chuẩn tự trả 405 khi sai phương thức và 404 khi không có đường dẫn. Mẫu tuyến có phương thức như <code>GET /suc-khoe</code> cần Go từ phiên bản 1.22.</p>"""
           + table(["yêu cầu", "mã", "thân"],
                   [["GET /suc-khoe", "200", "<code>{\"trang_thai\":\"ok\"}</code>"],
                    ["POST /suc-khoe", "405", "Method Not Allowed"],
                    ["GET /khong-co", "404", "404 page not found"]]),
           """Bước bảy, dịch vụ HTTP nhỏ đăng ký tuyến đọc đường dẫn kiểm sức khoẻ. Đúng tuyến thì trả mã hai trăm. Sai phương thức thì gói chuẩn tự trả bốn trăm linh năm vì tuyến chỉ cho phương thức đọc, còn không có đường dẫn thì trả bốn trăm linh bốn.""",
           focus=[1, "2.2", "2.3"], clear=True),
        st(table(["việc", "gói chuẩn net/http", "bộ khung Fiber"],
                 [["đăng ký tuyến", "<code>mux.HandleFunc(\"GET /suc-khoe\", f)</code>", "<code>app.Get(\"/suc-khoe\", f)</code>"],
                  ["tham số trong đường dẫn", "(bài không so sánh)", "<code>/tai-khoan/:so</code>, đọc bằng <code>c.Params(\"so\")</code>"],
                  ["trả JSON", "tự đặt tiêu đề và ghi thân (chương trình trên)", "<code>c.JSON(fiber.Map{…})</code>"],
                  ["nền bên dưới", "thư viện chuẩn", "dựng trên <b>fasthttp</b> (nhà phát triển Fiber nêu)"]])
           + """<div class="box warn">Bài dùng Fiber <b>v2.52.16</b>; nhà phát triển ghi ở bản v2: không còn được bảo trì tích cực. Để chạy thử: <code>go mod init vidu</code> (tạo mô-đun mới tên vidu), rồi <code>go get github.com/gofiber/fiber/v2@v2.52.16</code> (tải thư viện đúng phiên bản).</div>""",
           """Bước tám, bộ khung web thêm tham số ngay trong đường dẫn và lệnh trả JSON gọn, vì với gói chuẩn ta phải tự đặt tiêu đề và ghi thân.""",
           focus=["1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l20_wg(3, 2) == 1 and alg.bnx_l20_wg(1000, 1000) == 0", "alg.bnx_l20_range(3) == (1, 3)",
               "alg.bnx_l20_locked(1000) == 1000", "alg.bnx_l20_race_exit() == 66",
               "alg.bnx_l20_accept(2, 3) == (2, 3)", "alg.bnx_l20_rut(500, 200) == (300, None) and alg.bnx_l20_rut(300, 400)[0] == 300",
               "alg.bnx_l20_route('POST', '/suc-khoe')[0] == 405 and alg.bnx_l20_route('GET', '/khong-co')[0] == 404"])

    ex = sc("example", "example", "Ví dụ chạy thật bằng Go, từng phép tính", [
        jstep([(("<code>func rut(tk TaiKhoan, tien int) (TaiKhoan, error) {</code>", "khai hàm: <code>func</code>, tên, tham số (tên rồi tới kiểu), rồi trong ngoặc tròn là các kiểu hàm trả về; ở đây trả <b>hai</b> giá trị", "Khai hàm Go gồm tên, tham số viết tên rồi kiểu, và các kiểu trả về trong ngoặc tròn, ở đây là hai giá trị."), "rút <code>tien</code> từ <code>tk</code>; trả (tài khoản mới, lỗi)", ""),
               (("<code>tk := TaiKhoan{So: \"001\", SoDu: 500}</code>", "tạo một giá trị kiểu <code>TaiKhoan</code>, ghi từng trường theo dạng tên: giá trị; dấu chấm chọn trường, <code>tk.SoDu</code> là 500", "Tạo giá trị cấu trúc bằng cách ghi từng trường theo dạng tên và giá trị, rồi dấu chấm chọn một trường."), "<code>tk.So</code> là <code>\"001\"</code>", ""),
               (("<code>tk.SoDu -= tien</code>, <code>dem++</code>", "<code>-=</code>: trừ một giá trị khỏi biến; <code>dem++</code>: tăng <code>dem</code> thêm 1", "Dấu trừ bằng trừ một giá trị khỏi biến, còn hai dấu cộng tăng biến thêm một."), "500 - 200 còn 300", "")]),
        st(GO_LOI.show(lines=(1, 10), title="main.go (trích): cấu trúc tài khoản và hàm trả lỗi"),
           """Phép tính thứ nhất là chương trình có cấu trúc tài khoản và hàm rút, hàm này trả thêm một giá trị lỗi khi không đủ tiền.""",
           clear=True),
        st(GO_LOI.show(lines=(11, 22), title="main.go (tiếp): rút 200 rồi rút 400"),
           """Vòng lặp rút hai trăm rồi bốn trăm, và mỗi lần bên gọi kiểm giá trị lỗi trước khi nhận số dư mới.""",
           clear=True),
        st(R_LOI.out_html(),
           """Lần đầu còn ba trăm, lần hai báo lỗi và số dư vẫn ba trăm, vì bên gọi đã kiểm lỗi.""",
           clear=True),
        jstep([(("<code>for i := 0; i &lt; 1000; i++ {</code>", "vòng đếm, không có ngoặc tròn: khai <code>i := 0</code>; còn lặp khi <code>i &lt; 1000</code>; sau mỗi vòng <code>i++</code>", "Vòng đếm của Go có ba phần cách nhau bằng chấm phẩy: khai biến đếm, điều kiện còn lặp, và bước sau mỗi vòng."), "chạy 1000 vòng, i từ 0 tới 999", "")]),
        st(GO_DEM.show(lines=(1, 9), title="main.go (trích): một nghìn luồng nhẹ cùng cộng, có khoá"),
           """Phép tính thứ hai là một nghìn luồng nhẹ cùng cộng một vào bộ đếm, mỗi lần cộng nằm trong khoá, và nhóm chờ đếm số việc.""",
           clear=True),
        st(GO_DEM.show(lines=(10, 18), title="main.go (hết): chờ cả nhóm rồi in") + R_DEM.out_html(),
           """Chờ cả nhóm xong rồi in, kết quả chạy thật là đúng một nghìn.""",
           clear=True),
        st(GO_KHONG.show(lines=(3, 14), title="Bỏ khoá: không còn dòng var khoa sync.Mutex, trong luồng nhẹ chỉ còn dem++")
           + "<p class='note'>Chỉ bỏ <code>Lock</code>/<code>Unlock</code> mà giữ dòng khai báo thì Go báo <code>declared and not used: khoa</code> và không chạy.</p>",
           """Bỏ khoá thì xoá cả dòng khai báo khoá, kẻo Go báo biến khai mà không dùng. Khi đó trong luồng nhẹ chỉ còn lệnh tăng một.""",
           clear=True),
        st(R_RACE.show(title="Chạy kèm trình phát hiện, lọc lấy hai dòng cần xem") + R_RACE.out_html(),
           """Chạy kèm trình phát hiện, nó báo có tranh chấp dữ liệu rồi thoát với mã sáu mươi sáu.""",
           clear=True),
        st(GO_KENH.show(lines=(1, 10), title="main.go (trích): thử gửi vào kênh, không chịu treo"),
           """Phép tính thứ ba là kênh. Hàm thử gửi dùng nhánh mặc định, nên đệm đầy thì in ra thay vì treo.""",
           clear=True),
        st(GO_KENH.show(lines=(11, 20), title="main.go (hết): kênh đệm 3 gửi 4 giá trị, rồi kênh không đệm"),
           """Hàm chính gửi bốn giá trị vào kênh đệm ba, nhận một giá trị rồi gửi lại, rồi thử kênh không đệm.""",
           clear=True),
        st(R_KENH.out_html(),
           """Kênh đệm ba nhận ba giá trị đầu, giá trị thứ bốn phải chờ. Sau khi nhận một giá trị thì gửi lại được, còn kênh không đệm không có bên nhận nên gửi phải chờ.""",
           clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>r *http.Request</code>, <code>c *fiber.Ctx</code>", "dấu <code>*</code> trước kiểu là <b>con trỏ</b>: địa chỉ của một giá trị kiểu đó, nên hàm dùng chính giá trị gốc thay vì chép"],
                  ["<code>w.Header().Set(\"Content-Type\", \"application/json\")</code>", "đặt <b>tiêu đề</b> (dòng thông tin kèm trả lời): <code>Content-Type</code> báo thân trả lời là JSON"],
                  ["<code>fmt.Fprint(w, `{\"trang_thai\":\"ok\"}`)</code>", "ghi chuỗi vào <code>w</code>, nơi ghi trả lời; dấu nháy ngược bao một chuỗi giữ nguyên mọi ký tự, kể cả dấu nháy kép"]]),
           """Trước khi đọc dịch vụ, ta cần ba chỗ. Dấu sao trước kiểu là con trỏ, tức địa chỉ của giá trị gốc. Tiêu đề kiểu nội dung báo thân trả lời là JSON, và dấu nháy ngược bao một chuỗi giữ nguyên mọi ký tự.""", clear=True),
        st(GO_HTTP.show(lines=(1, 12), title="main.go (trích): hàm xử lý, đăng ký tuyến, mở cổng")
           + "<p class='note'><code>127.0.0.1</code>: địa chỉ của chính máy này; cổng là số hiệu một cửa mạng, cổng 0 nhờ máy chọn cửa trống; <code>tcp</code> là kiểu nối bên dưới HTTP.</p>",
           """Phép tính thứ tư là dịch vụ HTTP nhỏ. Hàm xử lý ghi JSON, tuyến chỉ đăng ký cho phương thức đọc, và ta mở một cổng trên chính máy mình rồi chạy máy chủ ở luồng nhẹ riêng.""",
           clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>strings.Cut(yc, \" \")</code>", "cắt chuỗi <code>yc</code> ở dấu cách đầu tiên: phần đứng trước và phần đứng sau"],
                  ["<code>http.DefaultClient.Do(req)</code>", "gửi yêu cầu <code>req</code> và nhận trả lời <code>tl</code>"],
                  ["<code>io.ReadAll(tl.Body)</code>, <code>tl.Body.Close()</code>", "đọc hết thân trả lời / đóng thân lại khi xong"]]),
           """Vòng lặp gọi dùng ba hàm mới. Hàm cắt tách phương thức khỏi đường dẫn, hàm gửi trả lời về, và hàm đọc lấy hết thân trả lời rồi đóng lại.""", clear=True),
        st(GO_HTTP.show(lines=(13, 24), title="main.go (hết): gọi ba yêu cầu; cùng với dòng mở cổng ở trên, ba chỗ lược kiểm lỗi cho vừa khung"),
           """Ta gọi ba yêu cầu bằng một vòng lặp, và lược kiểm lỗi ở ba chỗ để chương trình vừa khung hình.""",
           clear=True),
        st(R_HTTP.out_html(),
           """Đúng tuyến cho hai trăm cùng JSON, sai phương thức cho bốn trăm linh năm, đường dẫn lạ cho bốn trăm linh bốn.""",
           clear=True),
        st(GO_FIBER.show(lines=(1, 12), title="main.go của Fiber v2.52.16 (trích): hai tuyến"),
           """Phép tính thứ năm là cùng việc ấy bằng bộ khung web. Mỗi tuyến chỉ là một lời gọi, và tuyến thứ hai đọc tham số ngay trong đường dẫn.""",
           clear=True),
        st(GO_FIBER.show(lines=(13, 24), title="main.go (hết): gọi hai đường dẫn"),
           """Ta gọi hai đường dẫn bằng một vòng lặp rồi tắt máy chủ.""",
           clear=True),
        st(R_FIBER.out_html(),
           """Cả hai trả hai trăm, và tuyến thứ hai trả đúng tham số không không một đọc từ đường dẫn.""",
           clear=True),
    ], checks=["alg.bnx_l20_rut(500, 200) == (300, None) and alg.bnx_l20_rut(300, 400)[0] == 300",
               "alg.bnx_l20_locked(1000) == 1000 and alg.bnx_l20_wg(1000, 1000) == 0",
               "alg.bnx_l20_race_exit() == 66",
               "alg.bnx_l20_accept(3, 4) == (3, 4)",
               "alg.bnx_l20_route('GET', '/suc-khoe')[0] == 200 and alg.bnx_l20_route('POST', '/suc-khoe')[0] == 405 and alg.bnx_l20_route('GET', '/khong-co')[0] == 404",
               "alg.bnx_l20_fiber_route('/suc-khoe')[0] == 200 and alg.bnx_l20_fiber_route('/tai-khoan/001')[0] == 200"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: nguyên tử và kênh, không dùng khoá", [
        jstep([(("<code>close(ch)</code>", "đóng kênh: báo sẽ không gửi thêm giá trị nào", "Đóng kênh báo rằng sẽ không gửi thêm giá trị nào nữa."), "đóng sau khi mọi luồng đã gửi xong", ""),
               (("<code>for v := range ch { tong += v }</code>", "nhận lần lượt từng giá trị trong kênh tới khi kênh đã đóng và cạn; <code>tong += v</code> cộng v vào tong", "Vòng lặp trên kênh nhận từng giá trị tới khi kênh đã đóng và cạn, rồi cộng vào tổng."), "kênh có 1000 số 1 thì tong = 1000", "")], intro="Mã kiểm dùng hai chỗ mới nên ta giải trước."),
        st(GO_KIEM.show(lines=(1, 10), title="main.go: đếm bằng bộ đếm nguyên tử và bằng kênh"),
           """Kiểm bằng đường khác, không dùng khoá. Một nghìn luồng nhẹ vừa cộng vào bộ đếm nguyên tử, loại bộ đếm mà phần cứng cộng trọn một lần hoặc không cộng gì, vừa gửi một vào kênh có đệm. Hai đường độc lập nên so được với nhau.""",
           clear=True, introduces=["bnx_nguyen_tu"]),
        st(GO_KIEM.show(lines=(11, 20), title="main.go (hết): cộng các số trong kênh bằng một luồng") + R_KIEM.out_html(),
           """Rồi một luồng cộng các số trong kênh. Kết quả chạy thật: cả hai đường đều ra một nghìn, nên khớp với bộ đếm có khoá.""",
           clear=True),
    ], checks=["alg.bnx_l20_locked(1000) == 1000 and alg.bnx_l20_locked(1000, 1) == 1000 * 1"])

    quymo = sc("quymo", "example", "Khi số việc chạy cùng lúc tăng ×10 và ×100: luồng nhẹ rẻ nhưng không miễn phí", [
        st(GO_Q.show(lines=(1, 11), title="main.go (trích): cho n luồng nhẹ cùng chờ trên một kênh")
           + "<p class='note'><b>ngăn xếp</b>: vùng nhớ riêng của mỗi luồng, giữ biến cục bộ và dấu vết các hàm đang gọi; <code>StackInuse</code> là số byte ngăn xếp đang dùng.</p>",
           """Ta đo bộ nhớ khi số việc cùng chờ tăng dần, cụ thể là ngăn xếp, vùng nhớ riêng của mỗi luồng. Hàm cho n luồng nhẹ cùng chờ trên một kênh, nên cả n luồng đều sống.""",
           clear=True),
        st(GO_Q.show(lines=(12, 23), title="main.go (hết): đo ngăn xếp mỗi luồng ở 1 000, 10 000 và 100 000"),
           """Ta in hiệu của vùng ngăn xếp trước và sau, chia cho số luồng, ở ba cỡ là một nghìn, mười nghìn và một trăm nghìn.""",
           clear=True),
        st(R_Q.out_html(),
           """Kết quả chạy thật: mỗi luồng giữ tám nghìn byte ở cỡ một nghìn, rồi bảy nghìn byte ở hai cỡ lớn hơn.""",
           clear=True),
        st(table(["số luồng nhẹ cùng chờ", "còn sống", "mỗi luồng giữ (nghìn byte, đo)", "tổng ngăn xếp ≈ (triệu byte, tính n × số đo)"],
                 [[nowrap("1 000 (×1)"), "1 000", "8", "8"],
                  [nowrap("10 000 (×10)"), "10 000", "7", "70"],
                  [nowrap("100 000 (×100)"), "100 000", "7", "700"]])
           + "<p class='note'>Số đo trên máy này (Go 1.25.5, Windows), làm tròn xuống nghìn byte; đổi theo phiên bản Go và hệ điều hành. Chỉ tính ngăn xếp, chưa tính dữ liệu của từng việc.</p>",
           """Bảng cho thấy luồng nhẹ rẻ nhưng không miễn phí. Mỗi luồng giữ khoảng bảy tới tám nghìn byte ngăn xếp, nên bộ nhớ tăng thẳng theo số luồng, và một trăm nghìn việc cùng chờ tốn cỡ bảy trăm triệu byte.""",
           focus=[0, "1.2", "1.3"], clear=True),
        st(table(["cách", "được", "mất"],
                 [["mỗi yêu cầu một luồng nhẹ mới, không giới hạn", "đơn giản, không yêu cầu nào bị từ chối ngay", "bộ nhớ tăng thẳng theo số yêu cầu đang chờ, không có trần"],
                  ["nhóm luồng nhẹ cố định đọc việc từ kênh có đệm", "bộ nhớ có trần; việc dư xếp hàng", "việc ở cuối chờ lâu; đệm đầy thì bên gửi bị chặn"],
                  ["kênh đệm đầy thì từ chối", "bên gọi biết ngay để thử lại; bộ nhớ có trần", "một phần yêu cầu bị từ chối"]]),
           """Người làm nghề phải chọn khi số việc tăng. Mỗi yêu cầu một luồng nhẹ thì đơn giản nhưng bộ nhớ không có trần. Nhóm luồng cố định có trần bộ nhớ nhưng việc ở cuối phải chờ, và đệm đầy thì từ chối ngay, đổi lại một phần yêu cầu bị từ chối.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["[alg.bnx_l20_trieu(n, k) for n, k in ((1000, 8), (10000, 7), (100000, 7))] == [8, 70, 700]",
               "alg.bnx_l20_trieu(100000, 7) // alg.bnx_l20_trieu(10000, 7) == 10 and alg.bnx_l20_trieu(10000, 7) // alg.bnx_l20_trieu(1000, 7) == 10",
               "100_000 // 1_000 == 100 and 10_000 // 1_000 == 10"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Cho rằng biến đếm dùng chung thì cứ cộng là đúng, vì một lần chạy ra 1000; hoặc cho rằng kênh thay được khoá trong mọi trường hợp.
<br><span class="note">Đúng: không khoá thì kết quả đổi theo mỗi lần chạy; một lần ra đúng chưa chứng minh gì. Kênh để truyền giá trị; trạng thái dùng chung vẫn cần khoá hoặc bộ đếm nguyên tử.</span></div>""",
           """Lỗi thứ nhất, của người mới, là cho rằng biến đếm dùng chung cứ cộng là đúng vì một lần chạy ra một nghìn. Không khoá thì kết quả đổi theo mỗi lần chạy, còn kênh để truyền giá trị chứ không thay được khoá."""),
        st(GO_BOQUA.show(title="Lỗi 2 (người đã đi làm, lúc mới dựng): đổi chuỗi 12a thành số, hai cách") + R_BOQUA.out_html(),
           """Lỗi thứ hai, của người đã đi làm, là bỏ qua giá trị lỗi bằng dấu gạch dưới. Số đọc được là không mà không ai biết, còn kiểm lỗi thì thấy ngay chuỗi không phải số.""",
           clear=True),
        jstep([(("<code>time.Sleep(200 * time.Millisecond)</code>", "tạm dừng chương trình 200 mili giây để các luồng nhẹ kịp chạy", "Lệnh ngủ tạm dừng chương trình hai trăm mili giây để các luồng nhẹ kịp chạy."), "chờ 0,2 giây rồi mới đếm", ""),
               (("<code>runtime.NumGoroutine()</code>", "số luồng nhẹ đang sống, kể cả luồng chạy hàm chính", "Hàm này cho biết số luồng nhẹ đang sống, kể cả luồng của hàm chính."), "1 nghĩa là chỉ còn hàm chính", "")]),
        st(GO_ROIRI.show(lines=(1, 10), title="main.go (trích): một nghìn yêu cầu, bên nhận đã bỏ đi"),
           """Lỗi thứ ba lộ ra khi tải tăng: bên nhận bỏ đi vì hết hạn chờ. Chương trình mô phỏng một nghìn yêu cầu, mỗi yêu cầu một luồng nhẹ gửi vào kênh mà không ai nhận.""",
           clear=True),
        st(GO_ROIRI.show(lines=(11, 14), title="main.go (hết): thử kênh đệm 1, rồi kênh không đệm") + R_ROIRI.out_html(),
           """Kênh đệm một thì mọi luồng gửi xong, còn một luồng là hàm chính. Kênh không đệm thì một nghìn luồng nhẹ kẹt mãi, nên còn một nghìn không trăm linh một luồng, và cách chữa là cho bên gửi luôn có đường thoát.""",
           clear=True),
    ], checks=["alg.bnx_l20_atoi('12a') == (0, True)", "alg.bnx_l20_leak(1000, True) == 1 and alg.bnx_l20_leak(1000, False) == 1001",
               "alg.bnx_l20_leak(1000, False) == 1 + 1000"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Kênh có đệm 5, gửi liền 8 giá trị, chưa ai nhận. Mấy giá trị vào được, và giá trị thứ mấy phải chờ?"],
                  ["2", "3 luồng nhẹ, mỗi luồng cộng 1 vào bộ đếm 0, không khoá (đọc rồi ghi). Bộ đếm cuối nhỏ nhất và lớn nhất là bao nhiêu? Một lần chạy ra đúng 3 có chứng minh không có tranh chấp không?"],
                  ["3", "Quyết định (số minh hoạ): 2 luồng nhẹ làm việc, mỗi việc 50 ms, tới 50 việc/giây. Chọn: mỗi yêu cầu một luồng nhẹ mới không giới hạn, kênh đệm 20 và bên gửi chờ khi đầy, hay kênh đệm 20 và đầy thì từ chối?"]]),
           """Đến lượt bạn. Câu một, kênh có đệm năm, gửi liền tám giá trị mà chưa ai nhận, thì mấy giá trị vào được? Câu hai, ba luồng nhẹ cùng cộng một vào bộ đếm không, không khoá, thì kết quả nhỏ nhất và lớn nhất là bao nhiêu? Câu ba, chọn cách xử lý nào khi tới năm mươi việc mỗi giây? Hãy dừng video.""",
           focus=[0, "1.2", "1.3", "1.4"], pause=25),
        st("""<p>Câu 1: đệm 5 nhận 5 giá trị, giá trị kế tiếp phải chờ.</p>
$$5 \\text{ giá trị vào được}; \\qquad 5 + 1 = \\hlg{6} \\text{: bên gửi bị chặn ở giá trị thứ 6}$$""",
           """Đáp án câu một: đệm năm nhận được năm giá trị, và bên gửi bị chặn ngay ở giá trị thứ sáu."""),
        st("""<p>Câu 2: xen kẽ xấu nhất làm mất 2 lần cộng.</p>
$$\\text{nhỏ nhất } \\hlg{1}, \\quad \\text{lớn nhất } \\hlg{3}; \\qquad \\text{ra đúng } 3 \\text{ chỉ là một cách xen kẽ trong số nhiều cách}$$""",
           """Đáp án câu hai: ba luồng cùng đọc không rồi ghi một thì nhỏ nhất là một, lớn nhất là ba. Một lần ra đúng ba không chứng minh gì, vì đó chỉ là một cách xen kẽ."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["mỗi yêu cầu một luồng nhẹ mới, không giới hạn", "không yêu cầu nào bị từ chối ngay",
                   "làm được $2 \\cdot 1000 : 50 = 40$ việc/giây, tới 50: dư 10 việc/giây, sau 60 giây có 600 việc dở, mỗi việc giữ một luồng nhẹ"],
                  ["kênh đệm 20, bên gửi chờ khi đầy", "việc được nhận chờ nhiều nhất $20 : 40 = 0{,}5$ giây; số việc dở có trần",
                   "bên gửi bị chặn, độ trễ lan ngược ra các yêu cầu tới"],
                  ["kênh đệm 20, đầy thì từ chối", "bên gọi biết ngay để thử lại sau; bộ nhớ có trần", "khoảng 10 việc/giây bị từ chối"]]),
           """Đáp án câu ba: hai luồng làm bốn mươi việc mỗi giây mà tới năm mươi, nên mỗi giây dư mười việc, và sau một phút có sáu trăm việc dở. Kênh đệm hai mươi cho việc chờ tối đa nửa giây, nhưng độ trễ lan ngược, nên khách không chờ lâu được thì từ chối sớm.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_l20_accept(5, 8) == (5, 6)", "alg.bnx_l20_range(3) == (1, 3)",
               "alg.bnx_l20_interleave(['A', 'A', 'B', 'B', 'C', 'C']) == 3",
               "alg.bnx_l20_thru(2, 50) == 40", "(50 - alg.bnx_l20_thru(2, 50)) * 60 == 600",
               "alg.bnx_l20_wait(20, alg.bnx_l20_thru(2, 50)) == 0.5"])

    lab_pr = practice_scene(sc, "Tự làm: bộ đếm có khoá và kênh có đệm 2", practice_steps2(
        st, "BNX", "L20",
        """<p><b>Đề</b> (cần cài Go: tải ở <code>go.dev/dl</code>, kiểm bằng <code>go version</code>; viết trong <code>mau.sh</code>: <code>cat &gt; main.go &lt;&lt;'GO'</code> ghi mọi dòng tới chữ <code>GO</code> kế tiếp vào tệp <code>main.go</code>, rồi <code>go run main.go</code> chạy nó):</p>
<ol><li><b>5 luồng nhẹ</b> mỗi luồng cộng <b>100</b> vào bộ đếm trong <code>sync.Mutex</code>, chờ bằng <code>WaitGroup</code>; in <code>bo dem: …</code></li><li>kênh đệm <b>2</b>: với v = 1, 2, 3 thử gửi không chờ bằng <code>select … default</code>, in <code>gui v xong, dang chua …</code> hoặc <code>gui v phai cho ben nhan</code>; nhận một giá trị, rồi thử gửi lại 3</li></ol>
<p class="note">Khuôn tệp và chữ in nằm ở <code>de.md</code>; số liệu khác ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm, cần cài Go. Hãy viết chương trình chạy năm luồng nhẹ, mỗi luồng cộng một trăm vào bộ đếm có khoá, rồi in bộ đếm. Sau đó dùng kênh đệm hai, thử gửi ba giá trị không chờ, nhận một rồi gửi lại. Hãy dừng video và tự viết.""",
        LAB.out, "mau.sh",
        """<div class="box key"><b>Nếu kẹt:</b> nhóm chờ: <code>nhom.Add(1)</code> trước mỗi luồng, <code>defer nhom.Done()</code> trong luồng, <code>nhom.Wait()</code> sau vòng lặp. Thử gửi không chờ: <code>select { case ch &lt;- v: … default: … }</code>.
Lời giải ở <code>labs/BNX/L20/loi_giai.sh</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, cộng nhóm chờ một trước mỗi luồng, trừ một trong luồng, rồi chờ sau vòng lặp. Thử gửi không chờ dùng lựa chọn có nhánh mặc định. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=120), "BNX", "L20")

    rec = sc("recap", "recap", "Chuỗi logic, góc phỏng vấn & tư duy cần mang theo", [
        st(chain("go f(): luồng nhẹ + WaitGroup", "ghi chung không khoá → tranh chấp", "Mutex / atomic / kênh", "go run -race: chỉ thấy đường đã chạy", "lỗi là giá trị phải kiểm", "luồng nhẹ rẻ, không miễn phí"),
           """Tổng kết: ghi chung không khoá gây tranh chấp, và khoá hay bộ đếm nguyên tử hay kênh chữa được. Trình phát hiện chỉ thấy đường đã chạy, lỗi là giá trị phải kiểm, và luồng nhẹ rẻ nhưng không miễn phí.""",
           focus=[0, "1.1", "1.3", "1.5", "1.7", "1.9"]),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["Goroutine khác luồng hệ điều hành thế nào?", "nhẹ hơn luồng do hệ điều hành lập lịch, vì bộ chạy của Go lập lịch và bắt đầu bằng ngăn xếp nhỏ; vẫn tốn bộ nhớ và vẫn rò rỉ được (rò rỉ: việc kẹt mãi, không ai dọn)"],
                  ["Khi nào dùng Mutex, khi nào dùng channel?", "channel để truyền giá trị giữa các luồng nhẹ; trạng thái dùng chung cần khoá hoặc bộ đếm nguyên tử; kiểm bằng -race"],
                  ["Fiber thêm gì so với net/http?", "tuyến có tham số, trả JSON gọn; dựng trên fasthttp; ghi ở bản v2: không còn bảo trì tích cực"]])
           + "<span class='note'>Trả lời bằng cơ chế; không nêu số liệu của tổ chức thật, không nói đã làm ở quy mô nào.</span>",
           """Người phỏng vấn hay hỏi ba câu: luồng nhẹ khác luồng hệ điều hành thế nào, khi nào dùng khoá và khi nào dùng kênh, và bộ khung web thêm gì. Hãy trả lời bằng cơ chế.""",
           focus=[1, 1], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> với mỗi đoạn mã đồng thời, hỏi ba điều: biến nào được <b>nhiều việc cùng ghi</b>, việc nào <b>có đường thoát</b> khi bên kia bỏ đi, và khi số việc tăng gấp trăm lần thì <b>bộ nhớ và hàng đợi</b> ra sao.</div>
<p class='small'>Bài sau: một hệ cho vay số, từ trạng thái hồ sơ, chấm điểm, ký số tới chống gian lận.</p>""",
           """Điều cần mang theo: với mỗi đoạn mã đồng thời, hỏi biến nào được nhiều việc cùng ghi, và việc nào có đường thoát khi bên kia bỏ đi. Rồi hỏi bộ nhớ ra sao khi việc tăng gấp trăm lần. Bài sau là một hệ cho vay số.""",
           clear=True, forward_ref=True),
    ], checks=["alg.bnx_l20_locked(1000) == 1000", "alg.bnx_l20_leak(1000, False) == 1001"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L20", "go_goroutine_kenh_http",
                  "Bài 20 — Go cho backend: goroutine, kênh, tranh chấp dữ liệu và một dịch vụ HTTP nhỏ",
                  "curriculum/bnx.yaml L20; audit/bnx/verify_bnx.py L20; audit/bnx/sources_l20.md: tài liệu chính thức của Go (Effective Go, Memory Model, "
                  "Race Detector, net/http), Fiber v2 (docs.gofiber.io), đọc 2026-11-12; mọi chương trình Go chạy thật bằng go1.25.5 windows/amd64, "
                  "Fiber v2.52.16 (audit/bnx/deps/l20/README.md); đầu ra viết không dấu; quy mô: đo ngăn xếp mỗi luồng của 1 000, 10 000, 100 000 luồng nhẹ (số đo trên máy này, làm tròn xuống nghìn byte); lab: Go chạy thật qua cham.sh",
                  ["Đọc một chương trình Go có hàm, cấu trúc và xử lý lỗi bằng giá trị trả về",
                   "Chạy nhiều goroutine và gom kết quả bằng nhóm chờ",
                   "Truyền dữ liệu qua kênh có đệm và không đệm, nói lúc nào bên gửi bị chặn",
                   "Đọc một dịch vụ HTTP nhỏ và nêu bộ khung Fiber thêm gì lên trên",
                   "So sánh bộ nhớ ngăn xếp khi 1 000, 10 000 và 100 000 luồng nhẹ cùng chờ",
                   "Viết chương trình Go dùng luồng nhẹ có khoá và kênh có đệm hai"],
                  scenes,
                  covers=[(1, "example"), (2, "example"), (3, "example"), (4, "example"), (5, "quymo"), (6, "practice")])
