# Lab BNX L20 — Luồng nhẹ, khoá và kênh có đệm (cần Go)

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
