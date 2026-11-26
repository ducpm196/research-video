package vn.nganhang.chuyenkhoan;
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;
class SmokeL12Test {
    @Test void heapCalc() { assertEquals(384L, RuntimeProfileController.maxHeapMiB(512, 75.0)); }
}
