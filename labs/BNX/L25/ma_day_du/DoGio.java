import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
@Aspect
public class DoGio {
  int dem = 0;
  boolean khongAm = true;
  @Around("execution(* ChuyenTien.rieng(..))")
  public Object doThoiGian(ProceedingJoinPoint p)
      throws Throwable {
    long t = System.nanoTime();
    try {
      return p.proceed();
    } finally {
      dem++;
      khongAm &= System.nanoTime() - t >= 0;
    }
  }
}
