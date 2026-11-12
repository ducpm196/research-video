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
