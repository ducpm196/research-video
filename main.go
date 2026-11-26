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
